"""M6 TRAIN-only boundary and replay evidence; no model construction."""

import json
import os
from pathlib import Path
import random
import subprocess
from collections import Counter

from jeff.runtime import qwen_challenger as p3
from jeff.training.dataset import safe_path, strict_json, validate_labeled, nonempty, sha256

ROOT = p3.ROOT
ARTIFACTS = Path("/Users/destiner/Code/jeff/artifacts")
MANIFEST = ARTIFACTS / "data/data-pilot-v2/manifest.json"
MANIFEST_HASH = "d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac"
MODEL_DIR = ARTIFACTS / "release/p3-qwen-20261111-01/download/model"
P3_CONFIG = ROOT / "configs/runtime/p3-qwen.json"
P3_HASH = "2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f"
RECIPE = ROOT / "configs/model/m6-qwen.json"
TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt",
                   "added_tokens.json", "special_tokens_map.json", "chat_template.jinja")
FIXED = {"schema_version": "m6.recipe.v1", "seed": 42, "train_rows": 1500,
         "epochs": 1, "microbatch": 1, "accumulation": 4, "updates": 375,
         "optimizer": "AdamW", "learning_rate": 2e-5, "betas": [0.9, 0.999],
         "epsilon": 1e-8, "weight_decay": 0.01, "gradient_clip": 1.0,
         "foreach": False, "max_input_tokens": 1024,
         "maximum_run_seconds": 2700, "maximum_capacity_seconds": 600}
GUARDS = {"max_cpu_rss_bytes": 16 * 2**30, "max_mps_driver_bytes": 16 * 2**30,
          "min_recommended_headroom_bytes": 2 * 2**30}
require = p3.require


def read_json(path):
    return strict_json(Path(path).read_bytes())


def json_line(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"


def recipe():
    cfg = read_json(RECIPE)
    require(set(cfg) == set(FIXED) | set(GUARDS), "unexpected recipe keys")
    require(all(type(cfg[k]) is type(v) and cfg[k] == v for k, v in FIXED.items()),
            "only the fixed M6 recipe is supported")
    for key, default in GUARDS.items():
        value = cfg[key]
        require(type(value) is int and value > 0, "invalid memory guard")
        require(value >= default if key.startswith("min_") else value <= default,
                "guards may only become more conservative before audit")
    return cfg


def source_identity():
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    require(not git("status", "--porcelain", "--untracked-files=all"),
            "M6 requires a clean committed worktree")
    paths = git("ls-files").splitlines()
    return {"root": str(ROOT), "revision": git("rev-parse", "HEAD"),
            "tracked_files": {name: p3.digest(ROOT / name) for name in paths
                              if (ROOT / name).is_file()}}


def runtime_environment():
    require(os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") in (None, "0"),
            "MPS fallback prohibited")
    require(not any(k.startswith("PYTORCH_MPS_") or k in
                    {"PYTORCH_ALLOC_CONF", "PYTORCH_CUDA_ALLOC_CONF"} for k in os.environ),
            "allocator/backend overrides prohibited")
    controls = ("PYTORCH_ENABLE_MPS_FALLBACK", "TORCH_DEVICE_BACKEND_AUTOLOAD",
                "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
                "TOKENIZERS_PARALLELISM", "HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE")
    return {**p3.environment(), "backend_environment": {k: os.environ.get(k) for k in controls}}


def train_rows(guard=None):
    # Unlike load_dataset, preflight all paths but never open validation shards.
    from jeff.model.scorer import validate_decision

    root = ARTIFACTS.resolve(strict=True)
    require(Path(os.environ.get("JEFF_ARTIFACTS_DIR", str(root))).resolve() == root,
            "unexpected artifact root")
    protected = (root / "evaluation/final").resolve()
    manifest_path = safe_path(MANIFEST, root, protected)
    manifest_bytes = manifest_path.read_bytes()
    require(sha256(manifest_bytes) == MANIFEST_HASH, "wrong frozen TRAIN release")
    manifest = strict_json(manifest_bytes)
    require(manifest.get("schema_version") == "0.1", "manifest schema")
    nonempty(manifest.get("dataset_id"), "dataset_id")
    shards = manifest.get("shards")
    require(isinstance(shards, list) and shards, "manifest shards required")
    require(all(isinstance(s, dict) and s.get("split") in {"train", "validation"}
                for s in shards), "whole-manifest final-split preflight failed")
    planned, paths = [], set()
    for shard in shards:
        nonempty(shard.get("path"), "shard.path")
        relative = Path(shard["path"])
        require(not relative.is_absolute() and ".." not in relative.parts and
                not any("final" in part.lower() for part in relative.parts),
                "unsafe shard path")
        path = safe_path(root / relative, root, protected)
        require(not any("final" in part.lower() for part in path.parts), "final path forbidden")
        require(path not in paths, "duplicate resolved shard path")
        paths.add(path)
        sha = shard.get("sha256")
        require(isinstance(sha, str) and len(sha) == 64 and
                all(c in "0123456789abcdefABCDEF" for c in sha), "invalid shard digest")
        require(type(shard.get("rows")) is int and shard["rows"] >= 0, "invalid shard count")
        planned.append((shard, path))
    rows, verified, ids, contents, duplicates = [], [], set(), {}, []
    for shard, path in planned:
        if shard["split"] != "train":
            continue
        require(safe_path(root / shard["path"], root, protected) == path, "shard moved")
        raw = path.read_bytes()
        require(sha256(raw) == shard["sha256"].lower(), "TRAIN shard hash mismatch")
        batch = []
        for line in raw.decode("utf-8").splitlines():
            if not line.strip():
                continue
            if guard is not None:
                guard("preflight_train_row")
            row = strict_json(line)
            validate_labeled(row, "train", validate_decision)
            require(2 <= len(row["options"]) <= 6, "M6 supports only A-F")
            require(row["id"] not in ids, "duplicate TRAIN ID")
            ids.add(row["id"])
            signature = p3.text_hash(json.dumps([row["state"], row["question"],
                sorted(o["text"] for o in row["options"])]))
            if signature in contents:
                duplicates.append({"id": row["id"], "matches_id": contents[signature]})
            contents[signature] = row["id"]
            batch.append(row)
        require(len(batch) == shard["rows"], "TRAIN shard row count mismatch")
        rows.extend(batch)
        verified.append({**shard, "resolved_path": str(path)})
    require(len(rows) == len(ids) == 1500, "exactly 1500 unique TRAIN rows required")
    metadata = {"manifest_path": str(manifest_path), "manifest_sha256": MANIFEST_HASH,
                "dataset_id": manifest["dataset_id"], "train_shards": verified,
                "rows": len(rows), "unique_ids": len(ids),
                "unique_groups": len({r["group_id"] for r in rows}),
                "likely_content_duplicates": duplicates,
                "label_basis": dict(Counter(r["provenance"]["label_basis"] for r in rows)),
                "families": dict(Counter(r["task_family"] for r in rows)),
                "family_source_groups": dict(Counter(json.dumps([r["task_family"],
                    r["provenance"]["source"], r["group_id"]]) for r in rows)),
                "source_groups": dict(Counter(json.dumps([r["provenance"]["source"],
                    r["group_id"]]) for r in rows))}
    return rows, metadata


def evidence(guard=None):
    from transformers import AutoTokenizer

    source = source_identity()
    cfg = recipe()
    env = runtime_environment()
    require(p3.digest(P3_CONFIG) == P3_HASH, "P3 scoring config changed")
    scoring = p3.configuration(P3_CONFIG)
    require(scoring["max_input_tokens"] == cfg["max_input_tokens"], "P3 cap mismatch")
    model_dir = MODEL_DIR.resolve(strict=True)
    assets = p3.assets(model_dir, scoring)
    rows, data = train_rows(guard)
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True,
                                              trust_remote_code=False)
    require(isinstance(tokenizer.chat_template, str) and tokenizer.chat_template,
            "official chat template required")
    rng = random.Random(42)
    rng.shuffle(rows)
    schedule = []
    for index, row in enumerate(rows):
        if guard is not None:
            guard("preflight_tokenize_row")
        options = list(row["options"])
        rng.shuffle(options)
        decision = {k: row[k] for k in ("schema_version", "id", "state", "question")}
        decision["options"] = [{"id": o["id"], "text": o["text"]} for o in options]
        prompt, answers = p3.prepare(tokenizer, scoring, decision)
        option_ids = [o["id"] for o in options]
        schedule.append({"index": index, "id": row["id"], "decision": decision,
            "option_ids": option_ids, "original_option_ids": [o["id"] for o in row["options"]],
            "target_id": row["target_id"], "target_position": option_ids.index(row["target_id"]),
            "family": row["task_family"], "group_id": row["group_id"],
            "provenance": row["provenance"], "prompt_tokens": prompt,
            "input_tokens": len(prompt), "answer_ids": answers,
            "prompt_token_sha256": p3.text_hash(json.dumps(prompt))})
    proof = {"source": source, "recipe_path": str(RECIPE), "recipe": cfg,
        "recipe_sha256": p3.digest(RECIPE), "environment": env, "data": data,
        "p3_scoring_config_sha256": P3_HASH, "p3_scoring_config": scoring,
        "model_dir": str(model_dir), "model_assets": assets,
        "base_model_id": p3.MODEL, "base_revision": p3.REVISION,
        "chat_template_sha256": p3.text_hash(tokenizer.chat_template),
        "tokenizer_assets": {k: assets[k] for k in TOKENIZER_FILES if k in assets},
        "lengths": p3.distribution([r["input_tokens"] for r in schedule]),
        "boundary_checks": 1500, "schedule_algorithm": "Random(42): shuffle rows then options once per row"}
    require(source_identity() == source, "source changed during preflight")
    return proof, schedule


def schedule_text(schedule):
    return "".join(json_line(row) for row in schedule)


def revalidate(audit_dir, guard=None):
    audit = read_json(audit_dir / "audit.json")
    require(audit["schema_version"] == "m6.audit.v1" and audit["status"] == "complete",
            "complete M6 audit required")
    proof, schedule = evidence(guard)
    require(proof == audit["evidence"], "source/config/data/assets/environment changed since audit")
    text = schedule_text(schedule)
    require(p3.text_hash(text) == audit["schedule_sha256"] and
            (audit_dir / "schedule.jsonl").read_bytes() == text.encode("utf-8"),
            "schedule differs from re-derived pinned TRAIN schedule")
    identity = {"audit_sha256": p3.digest(audit_dir / "audit.json"),
                "schedule_sha256": audit["schedule_sha256"], "evidence": proof}
    return identity, schedule
