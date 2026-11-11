"""Trainable joint-text candidate scorer and self-contained safe checkpoints."""

from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from transformers import AutoConfig, AutoModel, AutoTokenizer

_ARCHITECTURE = "jeff.joint_encoder_mean_pool_scalar.v1"
_FORMAT = {
    "first": "State:\n{state}\nQuestion:\n{question}",
    "second": "Candidate:\n{text}",
    "truncation": "longest_first",
    "pooling": "attention_mask_mean",
}
_DECISION_FIELDS = {"schema_version", "id", "state", "question", "options"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_decision(row: dict) -> None:
    """Validate v0.1 input fields; tolerate labels without ever encoding them."""
    if not isinstance(row, dict):
        raise ValueError("decision must be an object")
    if row.get("schema_version") != "0.1":
        raise ValueError("decision schema_version must be '0.1'")
    if not _nonempty(row.get("id")) or not _nonempty(row.get("question")):
        raise ValueError("decision id and question must be nonempty strings")
    if not isinstance(row.get("state"), str):
        raise ValueError("decision state must be a string")
    options = row.get("options")
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError("decision needs at least two options")
    seen = set()
    for option in options:
        if not isinstance(option, dict):
            raise ValueError("option must be an object")
        if not _nonempty(option.get("id")) or not _nonempty(option.get("text")):
            raise ValueError("option id and text must be nonempty strings")
        if option["id"] in seen:
            raise ValueError("option ids must be unique within a decision")
        seen.add(option["id"])


def resolve_device(device: str = "cpu") -> torch.device:
    """Resolve auto deterministically and fail rather than silently switching devices."""
    if device == "auto":
        device = "mps" if torch.backends.mps.is_available() else "cpu"
    resolved = torch.device(device)
    if resolved.type == "cpu" and resolved.index is None:
        return resolved
    if resolved.type == "mps" and resolved.index in (None, 0):
        if not torch.backends.mps.is_available():
            raise ValueError("MPS was requested but is unavailable")
        return torch.device("mps")
    if resolved.type == "cuda" and torch.cuda.is_available():
        index = resolved.index if resolved.index is not None else torch.cuda.current_device()
        if index < torch.cuda.device_count():
            return torch.device("cuda", index)
    raise ValueError(f"unsupported or unavailable device: {device}")


def _settings(max_length: int, temperature: float) -> None:
    if type(max_length) is not int or not 8 <= max_length <= 1_000_000:
        raise ValueError("max_length must be an integer between 8 and 1000000")
    if type(temperature) not in (int, float) or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be finite and positive")


def _unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON value: {value}")


def _read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain an object")
    json.dumps(value, allow_nan=False)
    return value


class CandidateScorer(nn.Module):
    """One shared scalar head over independently encoded state/question/option pairs.

    The initial head is random, not a calibrated or trained decision model. All
    backbone parameters remain trainable for the trainer's full fine-tuning.
    """

    def __init__(self, encoder: nn.Module, tokenizer, model_id: str, revision: str,
                 max_length: int = 256):
        super().__init__()
        _settings(max_length, 1.0)
        if not _nonempty(model_id) or not _nonempty(revision):
            raise ValueError("model_id and revision must be nonempty strings")
        hidden_size = getattr(encoder.config, "hidden_size", None)
        if type(hidden_size) is not int or hidden_size <= 0:
            raise ValueError("encoder must expose a positive hidden_size")
        if getattr(encoder.config, "is_encoder_decoder", False) or getattr(encoder.config, "is_decoder", False):
            raise ValueError("an encoder-only backbone is required")
        if max_length > getattr(encoder.config, "max_position_embeddings", max_length):
            raise ValueError("max_length exceeds the backbone position limit")
        self.encoder = encoder
        self.tokenizer = tokenizer
        self.head = nn.Linear(hidden_size, 1)
        self.model_id = model_id
        self.revision = revision
        self.resolved_revision = getattr(encoder.config, "_commit_hash", None)
        self.max_length = max_length
        self.temperature = 1.0
        self.encoder.requires_grad_(True)

    @property
    def backbone(self) -> nn.Module:
        return self.encoder

    @classmethod
    def from_pretrained(cls, model_id: str, revision: str, max_length: int = 256,
                        device: str = "cpu") -> CandidateScorer:
        _settings(max_length, 1.0)
        if not _nonempty(model_id) or not _nonempty(revision):
            raise ValueError("model_id and revision must be nonempty strings")
        target = resolve_device(device)
        tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision, trust_remote_code=False)
        encoder = AutoModel.from_pretrained(
            model_id, revision=revision, trust_remote_code=False, use_safetensors=True,
        )
        return cls(encoder, tokenizer, model_id, revision, max_length).to(target)

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
        device = self.head.weight.device
        tokens = {key: value.to(device) for key, value in tokens.items()}
        hidden = self.encoder(**tokens, return_dict=True).last_hidden_state
        mask = tokens["attention_mask"].unsqueeze(-1).to(hidden.dtype)
        pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp_min(1)
        scores = self.head(pooled).squeeze(-1)
        return pad_sequence(scores.split(counts), batch_first=True, padding_value=-math.inf)

    def probabilities(self, rows: list[dict]) -> torch.Tensor:
        """Normalized scores; temperature alone makes no calibration claim."""
        return torch.softmax(self(rows).float() / self.temperature, dim=-1)

    def save_checkpoint(self, path: str | Path, metadata: dict) -> None:
        """Create a new directory containing the complete encoder, tokenizer and head."""
        _settings(self.max_length, self.temperature)
        if not isinstance(metadata, dict):
            raise ValueError("checkpoint metadata must be an object")
        config = {
            "schema_version": "0.1",
            "architecture": _ARCHITECTURE,
            "input_formatting": _FORMAT,
            "max_length": self.max_length,
            "temperature": self.temperature,
            "model_id": self.model_id,
            "revision": self.revision,
            "resolved_revision": self.resolved_revision,
            "hidden_size": self.head.in_features,
            "metadata": metadata,
        }
        serialized = json.dumps(config, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        destination = Path(path)
        destination.mkdir(parents=True, exist_ok=False)
        try:
            self.encoder.save_pretrained(destination / "encoder", safe_serialization=True)
            self.tokenizer.save_pretrained(destination / "tokenizer")
            weights = {key: value.detach().cpu().contiguous() for key, value in self.head.state_dict().items()}
            save_file(weights, str(destination / "head.safetensors"))
            (destination / "checkpoint.json").write_text(serialized, encoding="utf-8")
        except BaseException:
            shutil.rmtree(destination)
            raise


def load_checkpoint(path: str | Path, device: str = "cpu") -> CandidateScorer:
    """Load only local safe weights and built-in Transformers implementations."""
    target = resolve_device(device)
    root = Path(path)
    if not root.is_dir():
        raise ValueError("checkpoint must be an existing directory")
    # Reject links so local configuration cannot redirect reads outside the artifact.
    if root.is_symlink() or any(item.is_symlink() for item in root.rglob("*")):
        raise ValueError("checkpoint must not contain symbolic links")
    config = _read_json(root / "checkpoint.json")
    expected = {
        "schema_version", "architecture", "input_formatting", "max_length", "temperature",
        "model_id", "revision", "resolved_revision", "hidden_size", "metadata",
    }
    if set(config) != expected or config["schema_version"] != "0.1":
        raise ValueError("unrecognized checkpoint schema")
    if config["architecture"] != _ARCHITECTURE or config["input_formatting"] != _FORMAT:
        raise ValueError("unrecognized checkpoint architecture or input formatting")
    _settings(config["max_length"], config["temperature"])
    if not _nonempty(config["model_id"]) or not _nonempty(config["revision"]):
        raise ValueError("invalid checkpoint base identity")
    if config["resolved_revision"] is not None and not _nonempty(config["resolved_revision"]):
        raise ValueError("invalid resolved revision")
    if not isinstance(config["metadata"], dict):
        raise ValueError("invalid checkpoint metadata")
    hidden_size = config["hidden_size"]
    if type(hidden_size) is not int or not 1 <= hidden_size <= 65536:
        raise ValueError("invalid checkpoint hidden size")
    encoder_config = _read_json(root / "encoder" / "config.json")
    tokenizer_config = _read_json(root / "tokenizer" / "tokenizer_config.json")
    if encoder_config.get("auto_map") or tokenizer_config.get("auto_map"):
        raise ValueError("custom-code checkpoint configurations are unsupported")
    if encoder_config.get("hidden_size") != hidden_size:
        raise ValueError("checkpoint hidden size does not match encoder")
    # Never fall back to pickle weights or fetch a missing base/tokenizer remotely.
    backbone_config = AutoConfig.from_pretrained(
        root / "encoder", local_files_only=True, trust_remote_code=False,
    )
    if getattr(backbone_config, "is_decoder", False) or getattr(backbone_config, "is_encoder_decoder", False):
        raise ValueError("checkpoint backbone must be an encoder")
    weights = load_file(str(root / "head.safetensors"), device="cpu")
    if set(weights) != {"weight", "bias"}:
        raise ValueError("invalid scoring head keys")
    if weights["weight"].shape != (1, hidden_size) or weights["bias"].shape != (1,):
        raise ValueError("invalid scoring head shapes")
    if any(not value.is_floating_point() or not torch.isfinite(value).all().item() for value in weights.values()):
        raise ValueError("scoring head must contain finite floating-point weights")
    index_path = root / "encoder" / "model.safetensors.index.json"
    if index_path.exists():
        index = _read_json(index_path)
        weight_map = index.get("weight_map")
        if not isinstance(weight_map, dict) or not weight_map:
            raise ValueError("invalid encoder weight index")
        for filename in weight_map.values():
            if (not isinstance(filename, str) or Path(filename).name != filename
                    or not filename.endswith(".safetensors")):
                raise ValueError("unsafe encoder weight index path")
    for key, value in tokenizer_config.items():
        if key.endswith("_file") and value is not None:
            if not isinstance(value, str) or Path(value).name != value:
                raise ValueError("unsafe tokenizer file path")
    encoder, loading_info = AutoModel.from_pretrained(
        root / "encoder", config=backbone_config, local_files_only=True,
        trust_remote_code=False, use_safetensors=True, output_loading_info=True,
    )
    if any(loading_info.get(key) for key in ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")):
        raise ValueError("checkpoint encoder weights do not exactly match its configuration")
    tokenizer = AutoTokenizer.from_pretrained(
        root / "tokenizer", local_files_only=True, trust_remote_code=False,
    )
    model = CandidateScorer(encoder, tokenizer, config["model_id"], config["revision"], config["max_length"])
    model.head.load_state_dict(weights, strict=True)
    model.temperature = float(config["temperature"])
    model.resolved_revision = config["resolved_revision"]
    return model.to(target).eval()
