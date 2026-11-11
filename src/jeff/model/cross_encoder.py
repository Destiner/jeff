"""Joint candidate scoring with an intact pretrained BERT scalar classifier."""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer, BertForSequenceClassification

from .scorer import _nonempty, _read_json, _settings, resolve_device, validate_decision

_ARCHITECTURE = "jeff.pretrained_cross_encoder_scalar.v1"
_FORMAT = {
    "first": "State:\n{state}\nQuestion:\n{question}",
    "second": "Candidate:\n{text}",
    "truncation": "longest_first",
    "padding": "longest",
    "pooling": "native_pooled_cls",
}
_SCORING = {"output": "raw_scalar", "per_candidate_sigmoid": False, "normalization": "softmax"}


def _exact_weights(loading_info: dict) -> None:
    if any(loading_info.get(key) for key in ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")):
        raise ValueError("pretrained classifier weights do not exactly match its configuration")


def _supported_config(config) -> None:
    if (config.model_type != "bert" or config.num_labels != 1
            or getattr(config, "is_decoder", False)
            or getattr(config, "is_encoder_decoder", False)
            or getattr(config, "auto_map", None)):
        raise ValueError("an encoder-only BertForSequenceClassification with num_labels=1 is required")


class RetainedCrossEncoder(nn.Module):
    """Retain the native pooler, dropout and scalar head; normalize across choices only."""

    head_initialization = "pretrained"

    def __init__(self, classifier_model: nn.Module, tokenizer, model_id: str, revision: str,
                 max_length: int = 256):
        super().__init__()
        _settings(max_length, 1.0)
        if not _nonempty(model_id) or not _nonempty(revision):
            raise ValueError("model_id and revision must be nonempty strings")
        if type(classifier_model) is not BertForSequenceClassification:
            raise ValueError("only native BertForSequenceClassification is supported")
        _supported_config(classifier_model.config)
        if max_length > classifier_model.config.max_position_embeddings:
            raise ValueError("max_length exceeds the backbone position limit")
        self.classifier_model = classifier_model
        self.tokenizer = tokenizer
        self.model_id = model_id
        self.revision = revision
        self.resolved_revision = getattr(classifier_model.config, "_commit_hash", None)
        self.max_length = max_length
        self.temperature = 1.0
        self.classifier_model.requires_grad_(True)

    @property
    def backbone(self) -> nn.Module:
        return self.classifier_model.base_model

    @property
    def head(self) -> nn.Module:
        return self.classifier_model.classifier

    @classmethod
    def from_pretrained(cls, model_id: str, revision: str, max_length: int = 256,
                        device: str = "cpu") -> RetainedCrossEncoder:
        _settings(max_length, 1.0)
        if not _nonempty(model_id) or not _nonempty(revision):
            raise ValueError("model_id and revision must be nonempty strings")
        target = resolve_device(device)
        config = AutoConfig.from_pretrained(model_id, revision=revision, trust_remote_code=False)
        _supported_config(config)
        classifier, loading_info = AutoModelForSequenceClassification.from_pretrained(
            model_id, revision=getattr(config, "_commit_hash", None) or revision, config=config,
            trust_remote_code=False, use_safetensors=True, output_loading_info=True,
            ignore_mismatched_sizes=False,
        )
        _exact_weights(loading_info)
        tokenizer = AutoTokenizer.from_pretrained(
            model_id, revision=getattr(config, "_commit_hash", None) or revision, trust_remote_code=False,
        )
        return cls(classifier, tokenizer, model_id, revision, max_length).to(target)

    def forward(self, rows: list[dict]) -> torch.Tensor:
        if not isinstance(rows, list) or not rows:
            raise ValueError("rows must be a nonempty list of decisions")
        _settings(self.max_length, self.temperature)
        first, second, counts = [], [], []
        for row in rows:
            validate_decision(row)
            context = f"State:\n{row['state']}\nQuestion:\n{row['question']}"
            counts.append(len(row["options"]))
            for option in row["options"]:
                first.append(context)
                second.append(f"Candidate:\n{option['text']}")
        tokens = self.tokenizer(
            first, second, padding=True, truncation="longest_first",
            max_length=self.max_length, return_tensors="pt",
        )
        # Only native text inputs are forwarded: never labels or task metadata.
        tokens = {key: value.to(self.head.weight.device) for key, value in tokens.items()
                  if key in {"input_ids", "attention_mask", "token_type_ids"}}
        scores = self.classifier_model(**tokens, return_dict=True).logits.squeeze(-1)
        return pad_sequence(scores.split(counts), batch_first=True, padding_value=-math.inf)

    def probabilities(self, rows: list[dict]) -> torch.Tensor:
        return torch.softmax(self(rows).float() / self.temperature, dim=-1)

    def save_checkpoint(self, path: str | Path, metadata: dict) -> None:
        _settings(self.max_length, self.temperature)
        if not isinstance(metadata, dict):
            raise ValueError("checkpoint metadata must be an object")
        config = {
            "schema_version": "0.1",
            "architecture": _ARCHITECTURE,
            "input_formatting": _FORMAT,
            "scoring": _SCORING,
            "head_initialization": self.head_initialization,
            "max_length": self.max_length,
            "temperature": self.temperature,
            "model_id": self.model_id,
            "revision": self.revision,
            "resolved_revision": self.resolved_revision,
            "tokenizer_id": self.model_id,
            "tokenizer_revision": self.revision,
            "tokenizer_resolved_revision": self.resolved_revision,
            "metadata": metadata,
        }
        serialized = json.dumps(config, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        destination = Path(path)
        destination.mkdir(parents=True, exist_ok=False)
        try:
            self.classifier_model.save_pretrained(destination / "encoder", safe_serialization=True)
            self.tokenizer.save_pretrained(destination / "tokenizer")
            (destination / "checkpoint.json").write_text(serialized, encoding="utf-8")
        except BaseException:
            shutil.rmtree(destination)
            raise


def _safe_filename(value: object) -> bool:
    return (isinstance(value, str) and bool(value) and value not in {".", ".."}
            and Path(value).name == value and not any(char in value for char in ("/", "\\", ":", "\x00")))


def _safe_local_config(value: object) -> None:
    """Reject custom-code routing and file references escaping their local directory."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "auto_map":
                raise ValueError("custom-code checkpoint configurations are unsupported")
            if key.endswith("_file") and item is not None and not _safe_filename(item):
                raise ValueError("unsafe checkpoint file path")
            if key.endswith("_files") and item is not None:
                if not isinstance(item, list) or not all(_safe_filename(name) for name in item):
                    raise ValueError("unsafe checkpoint file paths")
            _safe_local_config(item)
    elif isinstance(value, list):
        for item in value:
            _safe_local_config(item)


def load_retained_checkpoint(root: str | Path, config: dict, device: str) -> RetainedCrossEncoder:
    """Load a complete local classifier without replacing or reinitializing its head."""
    target = resolve_device(device)
    root = Path(root)
    if not root.is_dir() or root.is_symlink() or any(item.is_symlink() for item in root.rglob("*")):
        raise ValueError("checkpoint must be a local directory without symbolic links")
    expected = {
        "schema_version", "architecture", "input_formatting", "scoring", "head_initialization",
        "max_length", "temperature", "model_id", "revision", "resolved_revision",
        "tokenizer_id", "tokenizer_revision", "tokenizer_resolved_revision", "metadata",
    }
    if not isinstance(config, dict) or set(config) != expected or config["schema_version"] != "0.1":
        raise ValueError("unrecognized retained checkpoint schema")
    if (config["architecture"] != _ARCHITECTURE or config["input_formatting"] != _FORMAT
            or config["scoring"] != _SCORING or config["head_initialization"] != "pretrained"):
        raise ValueError("unrecognized retained checkpoint architecture or scoring")
    _settings(config["max_length"], config["temperature"])
    for key in ("model_id", "revision", "tokenizer_id", "tokenizer_revision"):
        if not _nonempty(config[key]):
            raise ValueError("invalid checkpoint model/tokenizer identity")
    for key in ("resolved_revision", "tokenizer_resolved_revision"):
        if config[key] is not None and not _nonempty(config[key]):
            raise ValueError("invalid checkpoint resolved revision")
    if (config["tokenizer_id"] != config["model_id"]
            or config["tokenizer_revision"] != config["revision"]
            or config["tokenizer_resolved_revision"] != config["resolved_revision"]):
        raise ValueError("tokenizer must share the pretrained classifier identity")
    if not isinstance(config["metadata"], dict):
        raise ValueError("invalid checkpoint metadata")
    encoder_config = _read_json(root / "encoder" / "config.json")
    tokenizer_config = _read_json(root / "tokenizer" / "tokenizer_config.json")
    _safe_local_config(encoder_config)
    _safe_local_config(tokenizer_config)
    index_path = root / "encoder" / "model.safetensors.index.json"
    if index_path.exists():
        index = _read_json(index_path)
        weight_map = index.get("weight_map")
        if not isinstance(weight_map, dict) or not weight_map:
            raise ValueError("invalid classifier weight index")
        for filename in weight_map.values():
            if (not _safe_filename(filename) or not filename.endswith(".safetensors")
                    or not (root / "encoder" / filename).is_file()):
                raise ValueError("unsafe or missing classifier weight index path")
    classifier_config = AutoConfig.from_pretrained(
        root / "encoder", local_files_only=True, trust_remote_code=False,
    )
    _supported_config(classifier_config)
    classifier, loading_info = AutoModelForSequenceClassification.from_pretrained(
        root / "encoder", config=classifier_config, local_files_only=True,
        trust_remote_code=False, use_safetensors=True, output_loading_info=True,
        ignore_mismatched_sizes=False,
    )
    _exact_weights(loading_info)
    tokenizer = AutoTokenizer.from_pretrained(
        root / "tokenizer", local_files_only=True, trust_remote_code=False,
    )
    model = RetainedCrossEncoder(classifier, tokenizer, config["model_id"], config["revision"], config["max_length"])
    model.temperature = float(config["temperature"])
    model.resolved_revision = config["resolved_revision"]
    return model.to(target).eval()
