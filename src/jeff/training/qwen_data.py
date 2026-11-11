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


def recipe_path(experiment="m6"):
    require(experiment in {"m6", "m7", "m8"}, "unsupported experiment")
    return {"m6": RECIPE, "m7": ROOT / "configs/model/m7-qwen-low-lr.json",
            "m8": ROOT / "configs/model/m8-qwen-readout.json"}[experiment]


def recipe(experiment="m6"):
    cfg = read_json(recipe_path(experiment))
    fixed = FIXED if experiment == "m6" else {
        **FIXED, "schema_version": f"{experiment}.recipe.v1", "learning_rate": 2e-6}
    require(set(cfg) == set(FIXED) | set(GUARDS), "unexpected recipe keys")
    require(all(type(cfg[k]) is type(v) and cfg[k] == v for k, v in fixed.items()),
            "only the fixed experiment recipe is supported")
    for key, default in GUARDS.items():
        value = cfg[key]
        require(type(value) is int and value > 0, "invalid memory guard")
        require(value >= default if key.startswith("min_") else value <= default,
                "guards may only become more conservative before audit")
    return cfg


def source_identity(experiment="m6"):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    require(not git("status", "--porcelain", "--untracked-files=all"),
            "A clean committed worktree is required")
    paths = git("ls-files").splitlines()
    hashes = {name: p3.digest(ROOT / name) for name in paths if (ROOT / name).is_file()}
    result = {"root": str(ROOT), "revision": git("rev-parse", "HEAD"), "tracked_files": hashes}
    if experiment == "m8":
        executable = {name: digest for name, digest in hashes.items()
                      if name.endswith(".py") or name in {"pyproject.toml", "uv.lock",
                          "configs/model/m8-qwen-readout.json", "configs/runtime/p3-qwen.json"}}
        result["tracked_files"] = executable
        result["operating_context"] = {name: digest for name, digest in hashes.items()
                                       if name not in executable}
    return result


def source_binding(source, experiment="m6"):
    if experiment != "m8":
        return source
    return {key: source[key] for key in ("root", "tracked_files")}


def evidence_binding(proof, experiment):
    return {**proof, "source": source_binding(proof["source"], experiment)}


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


def evidence(guard=None, experiment="m6"):
    from transformers import AutoTokenizer

    source = source_identity(experiment)
    cfg = recipe(experiment)
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
    proof = {"source": source, "recipe_path": str(recipe_path(experiment)), "recipe": cfg,
        "recipe_sha256": p3.digest(recipe_path(experiment)), "environment": env, "data": data,
        "p3_scoring_config_sha256": P3_HASH, "p3_scoring_config": scoring,
        "model_dir": str(model_dir), "model_assets": assets,
        "base_model_id": p3.MODEL, "base_revision": p3.REVISION,
        "chat_template_sha256": p3.text_hash(tokenizer.chat_template),
        "tokenizer_assets": {k: assets[k] for k in TOKENIZER_FILES if k in assets},
        "lengths": p3.distribution([r["input_tokens"] for r in schedule]),
        "boundary_checks": 1500, "schedule_algorithm": "Random(42): shuffle rows then options once per row"}
    require(source_binding(source_identity(experiment), experiment) == source_binding(source, experiment),
            "executable source changed during preflight")
    if experiment in {"m7", "m8"}:
        require_m6_schedule(schedule_text(schedule))
    return proof, schedule


def schedule_text(schedule):
    return "".join(json_line(row) for row in schedule)


M6_RUN = ARTIFACTS / "model/m6-qwen-20261111-01"
M6_SCHEDULE_SHA = "7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8"
M6_AUDIT_SHA = "16a5dd978f47e22ec4e0c0b71f99fd6d6ed4e9cb0698e3d2fe25b6ca274cb1e5"
M6_CAPACITY_SHA = "995602986e42132057df12fd823b92e0fec8492daace4e958f8ababfc11d667a"
M6_PROCESS_SHA = "5fe0640793cb7e379ddf211339bf813578c88cd95f7f0c14348328d0129efa2a"
M6_EVENTS_SHA = "69a50f63bca4a7d9e711b0713af752fe1d801b37f1d74a93a09b680985680c12"


def pinned_json(path, digest):
    raw = safe_path(path).read_bytes()
    require(sha256(raw) == digest, "historical M6 evidence hash mismatch")
    return strict_json(raw)


def require_m6_schedule(text):
    raw = safe_path(M6_RUN / "train-audit/schedule.jsonl").read_bytes()
    require(sha256(raw) == M6_SCHEDULE_SHA and text.encode("utf-8") == raw,
            "M7 must replay the actual byte-identical M6 TRAIN schedule")


def reuse_m6_capacity(capacity_path, identity, schedule):
    # Historical source identity is evidence, never substituted for the new clean source.
    require(capacity_path == (M6_RUN / "capacity/receipt.json").resolve(),
            "M7 requires the actual historical M6 capacity receipt")
    old = pinned_json(capacity_path, M6_CAPACITY_SHA)
    audit = pinned_json(M6_RUN / "train-audit/audit.json", M6_AUDIT_SHA)
    process = pinned_json(M6_RUN / "capacity-process.json", M6_PROCESS_SHA)
    events_raw = safe_path(M6_RUN / "capacity/events.jsonl").read_bytes()
    require(sha256(events_raw) == M6_EVENTS_SHA, "M6 capacity process events changed")
    events = [strict_json(line) for line in events_raw.splitlines()]
    require(old["schema_version"] == "m6.capacity.v1" and old["status"] == "complete" and
            old["command"] == "capacity" and old["presentations"] == 4 and
            old["optimizer_steps"] == 1 and old["extra_backwards"] == 4 and
            old["external_deadline_required"] is True, "incomplete M6 capacity evidence")
    require(process["returncode"] == 0 and process["timeout"] is False and
            process["automatic_retry"] is False and process["maximum_seconds"] == 600 and
            0 < process["process_wall_seconds"] < 600 and
            process["command"] == ["uv", "run", "--locked", "--extra", "model", "python", "-B",
                "-m", "jeff.training.qwen_decision", "capacity", "--audit-dir",
                str(M6_RUN / "train-audit"), "--output-dir", str(M6_RUN / "capacity")],
            "successful matching M6 supervised process required")
    require(any(e.get("sample", {}).get("stage") == "process_complete" and
                e.get("presentations") == 4 and e.get("optimizer_steps") == 1 and
                e.get("extra_backwards") == 4 for e in events), "M6 process completion missing")
    require(audit["schema_version"] == "m6.audit.v1" and audit["status"] == "complete" and
            old["identity"] == {"audit_sha256": M6_AUDIT_SHA,
                "schedule_sha256": M6_SCHEDULE_SHA, "evidence": audit["evidence"]} and
            audit["schedule_sha256"] == identity["schedule_sha256"] == M6_SCHEDULE_SHA,
            "M6 audit/capacity identity mismatch")
    historical, current = audit["evidence"], identity["evidence"]
    exclusions = {"source", "recipe_path", "recipe_sha256", "recipe"}
    require({k: v for k, v in historical.items() if k not in exclusions} ==
            {k: v for k, v in current.items() if k not in exclusions},
            "M6 model/tokenizer/template/data/length/runtime controls changed")
    require(old["fresh_start"] == {"seed": 42, "base_model_id": current["base_model_id"],
            "base_revision": current["base_revision"], "model_dir": current["model_dir"],
            "base_weight_sha256": current["model_assets"]["model.safetensors"],
            "optimizer_state": "new empty AdamW; capacity state never reused",
            "rng": "fresh process; random.seed/torch.manual_seed/torch.mps.manual_seed(42)"},
            "historical capacity must start from original P3, fresh optimizer/RNG")
    parameters = old["parameters"]
    require(parameters["dtype"] == "float32" and parameters["total"] == parameters["trainable"] and
            old["adam_allocation"] == {"state_tensors": parameters["unique_tensors"],
                "moment_bytes": parameters["total"] * 8, "step": 1},
            "historical full-parameter FP32 AdamW allocation required")
    before, after = historical["recipe"], current["recipe"]
    require(before["schema_version"] == "m6.recipe.v1" and before["learning_rate"] == 2e-5 and
            after["schema_version"] == "m7.recipe.v1" and after["learning_rate"] == 2e-6 and
            {k: v for k, v in before.items() if k not in {"schema_version", "learning_rate"}} ==
            {k: v for k, v in after.items() if k not in {"schema_version", "learning_rate"}},
            "only LR and recipe schema may differ from actual M6 recipe (including guards/foreach)")
    require_m6_schedule(schedule_text(schedule))
    longest = sorted(schedule, key=lambda r: (-r["input_tokens"], r["index"]))[:4]
    require(old["capacity_rows"] == [{"id": r["id"], "index": r["index"],
            "input_tokens": r["input_tokens"]} for r in longest], "M6 capacity shape mismatch")
    projection = old["projection"]
    require(projection["within_cap"] is True and
            0 < projection["estimated_total_seconds"] < after["maximum_run_seconds"] == 2700,
            "M6 capacity projection invalid")
    samples = old["memory_samples"]
    require(samples and any("mps_recommended_headroom_bytes" in s for s in samples),
            "M6 observed working-set headroom required")
    for s in samples:
        require(s["elapsed_seconds"] < 600 and
                s["cpu_lifetime_rss_bytes"] <= after["max_cpu_rss_bytes"] and
                s.get("mps_driver_bytes", 0) <= after["max_mps_driver_bytes"] and
                s.get("mps_recommended_headroom_bytes", after["min_recommended_headroom_bytes"]) >=
                    after["min_recommended_headroom_bytes"], "historical capacity guard violation")
    return {"path": str(capacity_path), "sha256": M6_CAPACITY_SHA,
        "audit_sha256": M6_AUDIT_SHA, "process_sha256": M6_PROCESS_SHA,
        "events_sha256": M6_EVENTS_SHA, "historical_identity": old["identity"],
        "projection": projection, "basis": "same controls/shapes; only LR 2e-5 -> 2e-6; no new probe"}


def revalidate(audit_dir, guard=None, experiment="m6"):
    audit = read_json(audit_dir / "audit.json")
    require(audit["schema_version"] == f"{experiment}.audit.v1" and audit["status"] == "complete",
            "complete matching experiment audit required")
    if experiment == "m8":
        # Recheck immutable dependencies; consume the audited schedule, never reshuffle/replay it.
        text = (audit_dir / "schedule.jsonl").read_text(encoding="utf-8")
        require_m6_schedule(text)
        schedule = [strict_json(line) for line in text.splitlines()]
        source, cfg, env = source_identity(experiment), recipe(experiment), runtime_environment()
        require(p3.digest(P3_CONFIG) == P3_HASH, "P3 scoring config changed")
        scoring = p3.configuration(P3_CONFIG)
        assets = p3.assets(MODEL_DIR.resolve(strict=True), scoring)
        _, metadata = train_rows(guard)
        proof = {**audit["evidence"], "source": source,
            "recipe_path": str(recipe_path(experiment)), "recipe": cfg,
            "recipe_sha256": p3.digest(recipe_path(experiment)), "environment": env,
            "data": metadata, "p3_scoring_config": scoring, "p3_scoring_config_sha256": P3_HASH,
            "model_dir": str(MODEL_DIR.resolve(strict=True)), "model_assets": assets,
            "tokenizer_assets": {k: assets[k] for k in TOKENIZER_FILES if k in assets}}
        require(source_binding(source_identity(experiment), experiment) == source_binding(source, experiment),
                "executable source changed during revalidation")
    else:
        proof, schedule = evidence(guard, experiment)
        text = schedule_text(schedule)
    require(evidence_binding(proof, experiment) == evidence_binding(audit["evidence"], experiment),
            "executable/config/data/assets/environment changed since audit")
    require(p3.text_hash(text) == audit["schedule_sha256"] and
            (audit_dir / "schedule.jsonl").read_bytes() == text.encode("utf-8"),
            "schedule differs from re-derived pinned TRAIN schedule")
    identity = {"audit_sha256": p3.digest(audit_dir / "audit.json"),
                "schedule_sha256": audit["schedule_sha256"], "evidence": proof}
    return identity, schedule
