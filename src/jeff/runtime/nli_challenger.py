"""One frozen P12 NLI development pass; no acquisition, generation or fallback."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import inspect
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import struct
import subprocess
import sys
import time
from datetime import datetime, timezone

MODEL = "MoritzLaurer/roberta-base-zeroshot-v2.0-c"
REVISION = "d825e740e0c59881cf0b0b1481ccf726b6d65341"
PROFILE_SHA = "619365c8a158b7270d6f4aa29cab9c32f4c283d934b777d38647637ad04e2441"
P7_SHA = "a49a0934ea45febea4817a1a602ca6391d608bfe518d6a39ae0125ab48224f69"
INPUT_SHA = "77c57b75b64a0b306c8c851bb2d3a023bddd5d237334cd288316013c26d2927a"
ROOT = Path(__file__).resolve().parents[3]
RECIPE = ROOT / "configs/runtime/p12-nli.json"
EXPLORATION_DIR = ROOT.parents[1] / "artifacts/evaluation/e13-exploration-inputs-v1"
EXPLORATION_MANIFEST = ROOT.parents[1] / "artifacts/release/e13-later-exploration-20261112-01/bindings/p12-nli.inputs.json"
EXPLORATION_HASHES = {
    "native.jsonl": "1c8dca5c849faba518478c8676be37290d7722fde2f3edfe791d71e0ca23a074",
    "reversed.jsonl": "5e115753f7ee2bc6193c1c9758ddf59f05f2bae35a79eb975678afb8ce8ed2d1",
    "pairs.json": "7572cdb4b47273d877d803203d8ff38e74dcdbfb82cac2f1a63c01830a991c5f",
    "inference-handoff.json": "256cb8ae133d3d8867446dad65a7f0b31e2dc9ee0b8eeb87850680a7c9a70867",
}
SUITES = (
    ("v2-original", 300, "2103447bf8fbca3b43c09b0506b943179e96f7e774d7ae8363eddbf940970917"),
    ("v2-reversed", 300, "ba266b3b77896d77a453b095da485b569f0cde2238d94493e0a4bcfb704c92f1"),
    ("probes-paired", 24, "051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6"),
)
PACKAGES = ("torch", "transformers", "tokenizers", "safetensors", "huggingface-hub", "numpy")
ASSETS = {"README.md", "config.json", "merges.txt", "model.safetensors",
          "special_tokens_map.json", "tokenizer.json", "tokenizer_config.json", "vocab.json"}


class Rejected(ValueError):
    pass


def require(ok, code):
    if not ok:
        raise Rejected(code)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_json_key")
        result[key] = value
    return result


def loads(text):
    return json.loads(text, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(Rejected("nonfinite_json")))


def load(path):
    return loads(Path(path).read_text(encoding="utf-8"))


def digest(path, guard=lambda: None):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
            guard()
    return h.hexdigest()


def pin(entry, guard=lambda: None):
    require(isinstance(entry, dict) and set(entry) == {"path", "sha256", "bytes"}, "pin_fields")
    path = Path(entry["path"])
    require(path.is_absolute() and path.is_file() and not path.is_symlink(), "pin_path")
    require(type(entry["bytes"]) is int and path.stat().st_size == entry["bytes"], "pin_bytes")
    require(digest(path, guard) == entry["sha256"], "pin_sha256")
    return path


def expected_shapes():
    shapes = {
        "roberta.embeddings.word_embeddings.weight": [50265, 768],
        "roberta.embeddings.position_embeddings.weight": [514, 768],
        "roberta.embeddings.token_type_embeddings.weight": [1, 768],
        "roberta.embeddings.LayerNorm.weight": [768],
        "roberta.embeddings.LayerNorm.bias": [768],
        "classifier.dense.weight": [768, 768], "classifier.dense.bias": [768],
        "classifier.out_proj.weight": [2, 768], "classifier.out_proj.bias": [2],
    }
    for layer in range(12):
        prefix = f"roberta.encoder.layer.{layer}."
        for name, shape in {
            "attention.self.query": [768, 768], "attention.self.key": [768, 768],
            "attention.self.value": [768, 768], "attention.output.dense": [768, 768],
            "attention.output.LayerNorm": [768], "intermediate.dense": [3072, 768],
            "output.dense": [768, 3072], "output.LayerNorm": [768],
        }.items():
            shapes[prefix + name + ".weight"] = shape
            shapes[prefix + name + ".bias"] = [shape[0]]
    return shapes


def header(path):
    # Bounded serializer metadata only: never decode tensors in asset preparation.
    with path.open("rb") as stream:
        raw = stream.read(8)
        require(len(raw) == 8, "serializer_prefix")
        size = struct.unpack("<Q", raw)[0]
        require(0 < size <= 1024 * 1024, "serializer_header_bound")
        data = stream.read(size)
        require(len(data) == size, "serializer_header_short")
    tensors = loads(data.decode("utf-8"))
    metadata = tensors.pop("__metadata__", {})
    require(metadata.get("format") == "pt", "serializer_format")
    shapes = expected_shapes()
    require(set(tensors) == set(shapes), "serializer_tensor_names")
    ranges, count = [], 0
    for name, shape in shapes.items():
        tensor = tensors[name]
        require(set(tensor) == {"dtype", "shape", "data_offsets"} and
                tensor["shape"] == shape and tensor["dtype"] == "F16", "serializer_tensor_metadata")
        offsets = tensor["data_offsets"]
        require(isinstance(offsets, list) and len(offsets) == 2 and
                all(type(n) is int for n in offsets), "serializer_offsets")
        n = math.prod(shape)
        require(offsets[0] >= 0 and offsets[1] - offsets[0] == n * 2, "serializer_tensor_bytes")
        ranges.append(offsets)
        count += n
    cursor = 0
    for start, end in sorted(ranges):
        require(start == cursor, "serializer_gaps_or_overlap")
        cursor = end
    require(cursor + 8 + size == path.stat().st_size and count == 124647170 and
            count <= 150000000 and path.stat().st_size <= 600000000, "serializer_limits")
    return {"header_bytes": size, "tensor_count": len(tensors), "parameters": count,
            "dtype": "F16", "shapes": shapes}


def no_remote(value):
    if isinstance(value, dict):
        require("auto_map" not in value, "auto_map_prohibited")
        for child in value.values():
            no_remote(child)
    elif isinstance(value, list):
        for child in value:
            no_remote(child)


def check_assets(binding, guard):
    """Stdlib-only pins, public Git/LFS identities, config and serializer audit."""
    require(binding["model_id"] == MODEL and binding["revision"] == REVISION, "model_identity")
    profile_path = pin(binding["research_profile"], guard)
    require(binding["research_profile"]["sha256"] == PROFILE_SHA, "research_identity")
    profile = load(profile_path)
    require(profile["model_id"] == MODEL and profile["revision"] == REVISION, "research_model")
    model_dir = Path(binding["model_dir"])
    require(model_dir.is_absolute() and model_dir.is_dir() and not model_dir.is_symlink(), "model_directory")
    require(set(p.name for p in model_dir.iterdir()) == ASSETS, "asset_allowlist")
    require(set(binding["assets"]) == ASSETS, "asset_binding_allowlist")
    public = {entry["path"]: entry for entry in profile["assets"]}
    require(set(public) == ASSETS, "research_assets")
    verified = {}
    for name in sorted(ASSETS):
        entry, upstream = binding["assets"][name], public[name]
        require(set(entry) == {"url", "sha256", "bytes"}, "asset_entry_fields")
        path = model_dir / name
        require(entry["url"] == upstream["url"] and entry["bytes"] == upstream["advertised_bytes"],
                "public_asset_identity")
        verified[name] = {**entry, "path": str(path)}
        pin({k: verified[name][k] for k in ("path", "sha256", "bytes")}, guard)
        if upstream["published_lfs_sha256"]:
            require(entry["sha256"] == upstream["published_lfs_sha256"], "public_lfs_hash")
        else:
            blob = path.read_bytes()
            git_hash = hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest()
            require(git_hash == upstream["git_blob_sha1"], "public_git_blob")
        guard()
    config = load(model_dir / "config.json")
    tokenizer_config = load(model_dir / "tokenizer_config.json")
    tokenizer_json = load(model_dir / "tokenizer.json")
    for value in (config, tokenizer_config, tokenizer_json, load(model_dir / "special_tokens_map.json")):
        no_remote(value)
    fixed = {"model_type": "roberta", "architectures": ["RobertaForSequenceClassification"],
             "hidden_size": 768, "intermediate_size": 3072, "num_hidden_layers": 12,
             "num_attention_heads": 12, "vocab_size": 50265, "max_position_embeddings": 514,
             "type_vocab_size": 1, "id2label": {"0": "entailment", "1": "not_entailment"},
             "label2id": {"entailment": 0, "not_entailment": 1}}
    require(all(config.get(k) == v for k, v in fixed.items()), "actual_model_config")
    require(config.get("num_labels", 2) == 2, "native_label_count")
    require(tokenizer_config.get("add_prefix_space") is False and
            tokenizer_config.get("tokenizer_class") in ("RobertaTokenizer", "RobertaTokenizerFast"),
            "native_tokenizer_config")
    require(tokenizer_json["model"]["type"] == "BPE" and
            tokenizer_json["pre_tokenizer"]["type"] == "ByteLevel" and
            tokenizer_json["pre_tokenizer"]["add_prefix_space"] is False and
            tokenizer_json["truncation"] is None, "native_fast_bpe")
    return model_dir, {"assets": verified, "config": config, "tokenizer_config": tokenizer_config,
                       "serializer": header(model_dir / "model.safetensors")}


def exploration_file(entry, guard, rows=False, filename=None):
    require(isinstance(entry, dict) and set(entry) ==
            ({"path", "sha256", "rows", "name"} if rows else {"path", "sha256"}), "e13_pin_fields")
    require(isinstance(entry["path"], str) and isinstance(entry["sha256"], str) and
            len(entry["sha256"]) == 64, "e13_pin_required")
    path = Path(entry["path"])
    expected = EXPLORATION_MANIFEST if filename is None else EXPLORATION_DIR / filename
    require(path == expected, "e13_exact_path")
    if filename is not None:
        require(entry["sha256"] == EXPLORATION_HASHES[filename], "e13_frozen_identity")
    require(path.is_absolute() and path.is_file() and
            not any(p.is_symlink() for p in (path, *path.parents)) and
            not any("final" in p.lower() or "reference" in p.lower() for p in path.parts),
            "e13_input_path")
    require(digest(path, guard) == entry["sha256"], "e13_input_hash")
    return path


def read_inputs(binding, guard):
    if binding["schema_version"] == "e13.nli.binding.v1":
        manifest_path = exploration_file(binding["input_manifest"], guard)
        manifest = load(manifest_path)
        require(set(manifest) == {"schema_version", "candidate", "validation_only_never_train",
                                  "release", "pair_map", "datasets"} and
                manifest["schema_version"] == "e13.exploration.inputs.v1" and
                manifest["candidate"] == "p12-nli" and
                manifest["validation_only_never_train"] is True, "e13_manifest")
        exploration_file(manifest["release"], guard, filename="inference-handoff.json")
        exploration_file(manifest["pair_map"], guard, filename="pairs.json")
        require(isinstance(manifest["datasets"], list) and len(manifest["datasets"]) == 2,
                "e13_datasets")
        for entry, name, filename in zip(manifest["datasets"], ("e13-native", "e13-reversed"),
                                         ("native.jsonl", "reversed.jsonl")):
            exploration_file(entry, guard, rows=True, filename=filename)
            require(entry["name"] == name and type(entry["rows"]) is int and
                    entry["rows"] == 200, "e13_suite_identity")
        require(manifest["datasets"][0]["rows"] == manifest["datasets"][1]["rows"], "e13_equal_rows")
        return read_decisions(manifest, guard, external=True)
    p7 = pin(binding["p7_binding"], guard)
    require(binding["p7_binding"]["sha256"] == P7_SHA, "p7_binding_identity")
    old = load(p7)
    manifest_path = pin(binding["input_manifest"], guard)
    require(binding["input_manifest"]["sha256"] == INPUT_SHA and
            old["input_manifest"]["sha256"] == INPUT_SHA and
            Path(old["input_manifest"]["path"]).resolve() == manifest_path.resolve(), "p7_input_binding")
    manifest = load(manifest_path)
    require(set(manifest) == {"schema_version", "datasets"} and
            manifest["schema_version"] == "p3.inputs.v1" and len(manifest["datasets"]) == 3,
            "input_manifest_fields")
    return read_decisions(manifest, guard)


def read_decisions(manifest, guard, external=False):
    suites, total_pairs = [], 0
    for index, entry in enumerate(manifest["datasets"]):
        if not external:
            require(set(entry) == {"name", "rows", "sha256", "path"} and
                    (entry["name"], entry["rows"], entry["sha256"]) == SUITES[index], "input_suite_identity")
        path = Path(entry["path"])
        require(path.is_absolute() and not any("final" in p.lower() or "reference" in p.lower()
                                             for p in path.parts), "input_path")
        require(digest(path, guard) == entry["sha256"], "input_file_hash")
        rows, seen = [], set()
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                row = loads(line)
                require(set(row) == {"schema_version", "id", "state", "question", "options"} and
                        row["schema_version"] == "0.1", "decision_only_fields")
                require(isinstance(row["id"], str) and row["id"].strip() and row["id"] not in seen,
                        "decision_id")
                require(isinstance(row["state"], str) and isinstance(row["question"], str) and
                        row["question"].strip(), "decision_text")
                require(isinstance(row["options"], list) and len(row["options"]) >= 2, "options")
                if external:
                    require(len(row["options"]) == 2, "e13_exact_k2")
                ids = set()
                for option in row["options"]:
                    require(set(option) == {"id", "text"} and
                            all(isinstance(option[k], str) and option[k].strip() for k in ("id", "text")) and
                            option["id"] not in ids, "option_fields")
                    ids.add(option["id"])
                seen.add(row["id"])
                total_pairs += len(row["options"])
                rows.append(row)
                guard()
        require(len(rows) == entry["rows"], "input_row_count")
        suites.append((entry, rows))
    require(total_pairs == (800 if external else 2390), "candidate_pair_count")
    return suites


def softmax(values):
    require(values and all(math.isfinite(v) for v in values), "nonfinite_scores")
    maximum = max(values)
    exps = [math.exp(v - maximum) for v in values]
    denominator = math.fsum(exps)
    result = [v / denominator for v in exps]
    require(all(math.isfinite(p) and 0 <= p <= 1 for p in result) and
            abs(math.fsum(result) - 1) <= 1e-12, "invalid_probabilities")
    return result


def logsumexp(values):
    maximum = max(values)
    return maximum + math.log(math.fsum(math.exp(v - maximum) for v in values))


def utc():
    return datetime.now(timezone.utc).isoformat()


def predict(args, receipt, journal, start):
    def record(event, **fields):
        journal.write(json.dumps({"event": event, "utc": utc(), "elapsed_seconds": time.monotonic() - start,
                                  **fields}, allow_nan=False) + "\n")
        journal.flush()
        os.fsync(journal.fileno())

    def deadline():
        require(time.monotonic() - start < 480, "cooperative_deadline")

    def memory(torch, stage):
        deadline()
        rss = int(subprocess.check_output(["/bin/ps", "-o", "rss=", "-p", str(os.getpid())],
                                         text=True, timeout=2).strip()) * 1024
        driver = torch.mps.driver_allocated_memory() if torch is not None else None
        recommended = torch.mps.recommended_max_memory() if torch is not None else None
        headroom = recommended - driver if torch is not None else None
        sample = {"stage": stage, "rss_bytes": rss, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  "driver_bytes": driver, "mps_recommended_max_memory_bytes": recommended,
                  "mps_recommended_minus_driver_bytes": headroom,
                  "mps_guard": "checked" if torch is not None else "not_checked"}
        receipt["resources"].append(sample)
        record("resource", **sample)
        require(rss <= 8 * 1024**3 and sample["peak_rss_bytes"] <= 8 * 1024**3, "rss_guard")
        if torch is not None:
            require(driver <= 8 * 1024**3, "driver_guard")
            require(headroom >= 2 * 1024**3, "recommended_headroom_guard")
        deadline()

    require(sys.platform == "darwin" and platform.machine() == "arm64", "apple_silicon_required")
    required_env = {"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
                    "HF_DATASETS_OFFLINE": "1", "PYTORCH_ENABLE_MPS_FALLBACK": "0",
                    "TOKENIZERS_PARALLELISM": "false"}
    receipt["environment"] = {key: os.environ.get(key) for key in (
        *required_env, "HOME", "HF_HOME", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
        "PYTORCH_MPS_HIGH_WATERMARK_RATIO", "PYTORCH_MPS_LOW_WATERMARK_RATIO")}
    require(all(os.environ.get(k) == v for k, v in required_env.items()), "offline_no_fallback_environment")
    require("torch" not in sys.modules and "transformers" not in sys.modules and
            "tokenizers" not in sys.modules, "fresh_process_required")
    binding_path = args.binding.resolve()
    require(binding_path.stat().st_size <= 1024 * 1024, "binding_size")
    receipt["binding"] = {"path": str(binding_path), "sha256": digest(binding_path, deadline)}
    binding = load(binding_path)
    external = binding.get("schema_version") == "e13.nli.binding.v1"
    fields = {"schema_version", "model_id", "revision", "model_dir", "research_profile",
              "assets", "input_manifest", "sources", "versions"}
    require(set(binding) == fields | ({"candidate"} if external else {"p7_binding"}) and
            (binding["candidate"] == "p12-nli" if external else
             binding["schema_version"] == "p12.binding.v1"), "binding_fields")
    receipt["schema_version"] = "e13.nli.run.v1" if external else "p12.run.v1"
    receipt["profile"] = binding["schema_version"]
    receipt["pins"] = binding
    record("binding", **receipt["binding"])
    require(set(binding["sources"]) == {"adapter", "recipe", "pyproject", "uv_lock", "roberta_model", "roberta_tokenizer"},
            "source_pin_fields")
    for key, path in {"adapter": Path(__file__).resolve(), "recipe": RECIPE,
                      "pyproject": ROOT / "pyproject.toml", "uv_lock": ROOT / "uv.lock"}.items():
        require(pin(binding["sources"][key], deadline).resolve() == path.resolve(), "source_path")
    recipe = load(RECIPE)
    fixed_recipe = {
        "schema_version": "p12.recipe.v1", "model_id": MODEL, "revision": REVISION,
        "research_profile_sha256": PROFILE_SHA,
        "premise": "Context:\n{state}\n\nQuestion:\n{question}",
        "hypothesis": "The correct answer is:\n{option_text}",
        "native_labels": {"entailment": 0, "not_entailment": 1},
        "use_fast": True, "add_prefix_space": False, "max_complete_pair_tokens": 512,
        "truncation": False, "score": "entailment_logit_minus_logsumexp_native_nonentailment_logits",
        "temperature": 1, "device": "mps", "dtype": "float32", "threads": 4,
        "decisions_per_batch": 4, "decisions": 624, "candidate_pairs": 2390,
        "native_forwards": 156, "startup_forwards": 0, "max_seconds": 480,
        "max_rss_bytes": 8589934592, "max_driver_bytes": 8589934592,
        "min_headroom_bytes": 2147483648, "max_parameters": 150000000,
        "max_safetensors_bytes": 600000000, "expected_parameters": 124647170,
    }
    require(recipe == fixed_recipe, "fixed_recipe")
    receipt["recipe"] = recipe
    require(set(binding["versions"]) == set(PACKAGES), "version_pin_fields")
    actual_versions = {p: importlib.metadata.version(p) for p in PACKAGES}
    receipt["versions"] = actual_versions
    require(actual_versions == binding["versions"], "installed_versions")
    memory(None, "before_assets")
    model_dir, evidence = check_assets(binding, deadline)
    receipt["asset_evidence"] = evidence
    # Verify every source hash before ML imports, including builtin implementation files.
    for entry in binding["sources"].values():
        pin(entry, deadline)
    suites = read_inputs(binding, deadline)
    if external:
        receipt["exploration_inputs"] = load(binding["input_manifest"]["path"])
    expected_decisions = sum(len(rows) for _, rows in suites)
    expected_pairs = sum(len(row["options"]) for _, rows in suites for row in rows)
    expected_forwards = sum((len(rows) + 3) // 4 for _, rows in suites)
    if external:
        require((expected_decisions, expected_pairs, expected_forwards) == (400, 800, 100),
                "e13_exact_workload")
    receipt["expected_counts"] = {"decisions": expected_decisions, "candidate_pairs": expected_pairs,
                                  "native_forwards": expected_forwards, "startup_forwards": 0,
                                  "suites": [{"name": entry["name"], "decisions": len(rows),
                                              "candidate_pairs": sum(len(r["options"]) for r in rows),
                                              "native_forwards": (len(rows) + 3) // 4}
                                             for entry, rows in suites]}
    receipt["effective_profile"] = {**recipe, **{key: receipt["expected_counts"][key]
                                     for key in ("decisions", "candidate_pairs", "native_forwards")},
                                     "schema_version": binding["schema_version"],
                                     "resource_guard": "mps_recommended_minus_driver"}
    receipt["suites"] = [{**entry, "written_rows": 0, "written_probabilities": 0, "status": "unstarted"}
                         for entry, _ in suites]
    deadline()
    import torch
    memory(torch, "after_torch_import_before_mps_allocation")
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    from transformers.models.roberta.modeling_roberta import RobertaForSequenceClassification
    from transformers.models.roberta.tokenization_roberta_fast import RobertaTokenizerFast

    for key, cls in (("roberta_model", RobertaForSequenceClassification), ("roberta_tokenizer", RobertaTokenizerFast)):
        require(Path(inspect.getfile(cls)).resolve() == Path(binding["sources"][key]["path"]).resolve(), "builtin_source_path")
    torch.set_num_threads(4)
    torch.set_num_interop_threads(4)
    require(torch.backends.mps.is_available() and torch.get_num_threads() == 4 and
            torch.get_num_interop_threads() == 4, "mps_threads")
    memory(torch, "before_tokenizer_load")
    receipt["tokenizer_load_attempted"] += 1
    record("tokenizer_load_attempt", count=receipt["tokenizer_load_attempted"])
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), use_fast=True, add_prefix_space=False,
                                              local_files_only=True, trust_remote_code=False)
    receipt["tokenizer_load_completed"] += 1
    require(type(tokenizer) is RobertaTokenizerFast and tokenizer.is_fast and
            tokenizer.add_prefix_space is False and tokenizer.padding_side == "right", "actual_native_tokenizer")
    memory(torch, "after_tokenizer_load")
    actual_backend = loads(tokenizer.backend_tokenizer.to_str())
    require(actual_backend["pre_tokenizer"]["type"] == "ByteLevel" and
            actual_backend["pre_tokenizer"]["add_prefix_space"] is False, "actual_fast_bpe")
    encoded_suites, token_lengths = [], []
    for entry, rows in suites:
        encodings = []
        for row in rows:
            premise = "Context:\n" + row["state"] + "\n\nQuestion:\n" + row["question"]
            hypotheses = ["The correct answer is:\n" + option["text"] for option in row["options"]]
            encoded = tokenizer([premise] * len(hypotheses), hypotheses, add_special_tokens=True,
                                truncation=False, padding=False, return_attention_mask=True,
                                return_token_type_ids=False)
            require(set(encoded) == {"input_ids", "attention_mask"} and
                    len(encoded["input_ids"]) == len(hypotheses), "tokenizer_batch_shape")
            pairs = []
            for ids, mask in zip(encoded["input_ids"], encoded["attention_mask"]):
                require(len(ids) == len(mask) and all(v == 1 for v in mask), "tokenizer_attention_mask")
                token_lengths.append(len(ids))
                pairs.append({"input_ids": ids, "attention_mask": mask})
            encodings.append(pairs)
            deadline()
        encoded_suites.append(encodings)
    receipt["tokens"] = {"pairs": len(token_lengths), "min": min(token_lengths), "max": max(token_lengths),
                         "total_unpadded": sum(token_lengths), "overflow_pairs": sum(n > 512 for n in token_lengths),
                         "pair_lengths": token_lengths}
    require(len(token_lengths) == expected_pairs and min(token_lengths) > 0 and max(token_lengths) <= 512,
            "complete_pair_token_cap_no_scores")
    memory(torch, "before_model_load")
    receipt["model_load_attempted"] += 1
    record("model_load_attempt", count=receipt["model_load_attempted"])
    model, diagnostics = AutoModelForSequenceClassification.from_pretrained(
        str(model_dir), local_files_only=True, trust_remote_code=False, use_safetensors=True,
        torch_dtype=torch.float32, attn_implementation="eager", output_loading_info=True,
        ignore_mismatched_sizes=False)
    receipt["model_load_completed"] += 1
    receipt["loading_diagnostics"] = diagnostics
    memory(torch, "after_cpu_model_load")
    require(all(key in diagnostics and diagnostics[key] == [] for key in
                ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")), "strict_loading_diagnostics")
    require(type(model) is RobertaForSequenceClassification and model.config.num_labels == 2 and
            model.config.id2label == {0: "entailment", 1: "not_entailment"} and
            model.config.label2id == {"entailment": 0, "not_entailment": 1}, "actual_model_labels")
    require({name: list(p.shape) for name, p in model.named_parameters()} == expected_shapes() and
            sum(p.numel() for p in model.parameters()) == 124647170 and
            all(p.dtype == torch.float32 for p in model.parameters()), "actual_loaded_parameters")
    memory(torch, "before_mps_model_allocation")
    model.requires_grad_(False).eval().to("mps")
    torch.mps.synchronize()
    memory(torch, "after_mps_model_load")
    require(all(p.dtype == torch.float32 and p.device.type == "mps" for p in model.parameters()),
            "actual_fp32_mps_parameters")
    for suite_index, ((entry, rows), encodings) in enumerate(zip(suites, encoded_suites)):
        stats = receipt["suites"][suite_index]
        stats["status"] = "running"
        output = args.output_dir / (entry["name"] + ".jsonl")
        with output.open("x", encoding="utf-8") as stream:
            for offset in range(0, len(rows), 4):
                batch_rows, batch_pairs = rows[offset:offset + 4], encodings[offset:offset + 4]
                flat = [pair for pairs in batch_pairs for pair in pairs]
                native = tokenizer.pad(flat, padding=True, return_tensors="pt")
                require(native["input_ids"].shape[1] <= 512, "padded_token_cap")
                memory(torch, "before_mps_batch_allocation")
                native = {k: v.to("mps") for k, v in native.items()}
                memory(torch, "before_forward")
                require(receipt["native_attempted"] < expected_forwards, "forward_budget")
                deadline()
                receipt["native_attempted"] += 1
                receipt["pairs_attempted"] += len(flat)
                record("native_attempt", attempted=receipt["native_attempted"], completed=receipt["native_completed"],
                       pairs_attempted=receipt["pairs_attempted"], pairs_completed=receipt["pairs_completed"],
                       suite=entry["name"], row_offset=offset, decisions=len(batch_rows), pairs=len(flat))
                before = time.monotonic()
                with torch.inference_mode():
                    result = model(**native)
                torch.mps.synchronize()
                receipt["native_completed"] += 1
                receipt["pairs_completed"] += len(flat)
                record("native_complete", completed=receipt["native_completed"], pairs_completed=receipt["pairs_completed"],
                       seconds=time.monotonic() - before)
                memory(torch, "after_forward")
                require(result.logits.dtype == torch.float32 and result.logits.device.type == "mps" and
                        tuple(result.logits.shape) == (len(flat), 2), "native_logits_shape_dtype_device")
                logits = result.logits.detach().cpu().tolist()
                require(all(math.isfinite(v) for pair in logits for v in pair), "nonfinite_native_logits")
                scores = [pair[0] - logsumexp(pair[1:]) for pair in logits]
                cursor = 0
                for row in batch_rows:
                    size = len(row["options"])
                    probabilities = softmax(scores[cursor:cursor + size])
                    cursor += size
                    prediction = {"schema_version": "0.1", "id": row["id"], "probabilities": [
                        {"option_id": option["id"], "probability": p}
                        for option, p in zip(row["options"], probabilities)]}
                    stream.write(json.dumps(prediction, ensure_ascii=False, allow_nan=False) + "\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                    stats["written_rows"] += 1
                    stats["written_probabilities"] += size
                record("batch_written", suite=entry["name"], rows=stats["written_rows"],
                       probabilities=stats["written_probabilities"])
                del native, result
                deadline()
        stats["status"] = "complete"
    require(receipt["native_attempted"] == receipt["native_completed"] == expected_forwards and
            receipt["pairs_attempted"] == receipt["pairs_completed"] == expected_pairs and
            sum(s["written_rows"] for s in receipt["suites"]) == expected_decisions and
            sum(s["written_probabilities"] for s in receipt["suites"]) == expected_pairs, "final_exact_counts")
    memory(torch, "end")
    deadline()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    command = parser.add_subparsers(dest="command", required=True).add_parser("predict")
    command.add_argument("--binding", type=Path, required=True)
    command.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    args.output_dir = args.output_dir.resolve()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": "p12.run.v1", "status": "failed", "started_utc": utc(),
               "python": sys.version, "platform": platform.platform(), "clock": "monotonic",
               "native_attempted": 0, "native_completed": 0, "pairs_attempted": 0, "pairs_completed": 0,
               "startup_forwards": 0, "model_load_attempted": 0, "model_load_completed": 0,
               "tokenizer_load_attempted": 0, "tokenizer_load_completed": 0,
               "suites": [], "resources": [],
               "qualification": "practical frozen NLI baseline; not a pure architecture ablation; not calibrated"}

    def interrupted(signum, frame):
        raise InterruptedError("supervisor_signal_" + str(signum))

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    exit_code = 1
    with (args.output_dir / "journal.jsonl").open("x", encoding="utf-8") as journal:
        try:
            predict(args, receipt, journal, start)
            receipt["status"] = "complete"
            exit_code = 0
        except BaseException as exc:
            # Do not copy library exceptions: they can contain input text or tensor dumps.
            receipt["failure"] = {"type": type(exc).__name__,
                                  "code": str(exc) if type(exc) in (Rejected, InterruptedError) and
                                  str(exc).replace("_", "").isalnum() else "details_suppressed"}
        finally:
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            receipt["ended_utc"] = utc()
            receipt["elapsed_seconds"] = time.monotonic() - start
            for stats in receipt["suites"]:
                if stats["status"] == "running":
                    stats["status"] = "partial" if stats["written_rows"] else "failed"
    receipt["outputs"] = {}
    for path in sorted(args.output_dir.iterdir()):
        if path.is_file():
            try:
                receipt["outputs"][path.name] = {"sha256": digest(path), "bytes": path.stat().st_size}
                path.chmod(0o444)
            except OSError:
                receipt["outputs"][path.name] = {"error": "finalization_io_failure"}
                receipt["status"] = "failed"
                exit_code = 1
    receipt["ended_utc"] = utc()
    receipt["elapsed_seconds"] = time.monotonic() - start
    with (args.output_dir / "receipt.json").open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    (args.output_dir / "receipt.json").chmod(0o444)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
