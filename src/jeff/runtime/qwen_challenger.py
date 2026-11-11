"""Experimental P3 decoder and explicit trained reload; no training or generation.

python -m jeff.runtime.qwen_challenger audit --config configs/runtime/p3-qwen.json \
    --inputs /absolute/inputs.json --model-dir /absolute/pinned-model --audit-dir NEW
python -m jeff.runtime.qwen_challenger predict --audit-dir AUDIT --model-dir MODEL \
    --output-dir NEW --device mps

Inputs: {"schema_version":"p3.inputs.v1","datasets":[{"name":"validation",
"path":"inputs.jsonl","sha256":"...","rows":300}, ...]} (exactly three suites).
Paths are relative to the manifest. Local asset identity is an owner download
attestation, not independently authenticated against the remote repository.
Audit hashes weights but never loads them; place the complete pinned download
before auditing. For trained weights, audit with --checkpoint-manifest pointing
to the sibling manifest: base revision then denotes lineage, not weight identity.
A changed cap/asset/source/config requires a fresh audit.
"""

import argparse
import hashlib
import inspect
import json
import math
import os
from pathlib import Path
import platform
import re
import resource
import subprocess
import sys
import time
from importlib.metadata import version


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(__file__).resolve()
MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
SYSTEM = "You are a decision assistant. Choose exactly one of the listed options. Reply with only its letter."
USER = "State:\n{state}\n\nQuestion:\n{question}\n\nOptions:\n{options}"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def text_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON object key")
        result[key] = value
    return result


def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object)


def save(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")
    Path(path).chmod(0o444)


def safe_path(path):
    path = Path(path).resolve()
    require(not any("final" in part.lower() or "reference" in part.lower()
                    for part in path.parts), "final/reference paths are prohibited")
    return path


def environment():
    return {"python": sys.version, "platform": platform.platform(),
            "machine": platform.machine(),
            "packages": {p: version(p) for p in ("torch", "transformers", "safetensors", "tokenizers")}}


def configuration(path):
    cfg = load(path)
    require(cfg["schema_version"] == "p3.config.v1", "config schema")
    fixed = {"model_id": MODEL, "revision": REVISION, "system_prompt": SYSTEM,
             "user_template": USER, "symbols": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "device": "mps",
             "dtype": "float32", "batch_size": 1, "threads": 4, "temperature": 1.0,
             "startup_rows": 3, "maximum_run_seconds": 1200, "attention": "sdpa",
             "use_cache": False, "logits_to_keep": 1,
             "max_cpu_rss_bytes": 8589934592, "max_mps_driver_bytes": 8589934592}
    require(all(cfg.get(k) == v for k, v in fixed.items()), "unsupported recipe controls")
    require(type(cfg["max_input_tokens"]) is int and 1 <= cfg["max_input_tokens"] <= 2048,
            "cap must be frozen at at most 2048 before prediction")
    return cfg


def assets(model_dir, cfg):
    allowed = set(cfg["asset_allowlist"])
    files = {str(p.relative_to(model_dir)): p for p in model_dir.rglob("*")
             if p.is_file() and ".cache" not in p.relative_to(model_dir).parts}
    require(set(files) <= allowed, "unsupported model assets outside explicit allowlist")
    require({"config.json", "tokenizer_config.json", "model.safetensors"} <= set(files),
            "complete pinned model assets required (weights are hashed, not loaded in audit)")
    mc = load(model_dir / "config.json")
    require(mc.get("model_type") == "qwen2" and mc.get("architectures") == ["Qwen2ForCausalLM"],
            "unexpected model architecture")
    return {name: digest(path) for name, path in sorted(files.items())}


def read_inputs(path):
    path = safe_path(path)
    manifest = load(path)
    require(set(manifest) == {"schema_version", "datasets"} and
            manifest["schema_version"] == "p3.inputs.v1", "input manifest schema")
    require(isinstance(manifest["datasets"], list) and len(manifest["datasets"]) == 3,
            "exactly three label-free development suites required")
    suites, names = [], set()
    for entry in manifest["datasets"]:
        require(set(entry) == {"name", "path", "sha256", "rows"}, "dataset entry fields")
        name = entry["name"]
        require(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", name)
                and name not in names, "unsafe or duplicate dataset name")
        names.add(name)
        source = safe_path(path.parent / entry["path"])
        require(digest(source) == entry["sha256"], "input hash mismatch")
        require(type(entry["rows"]) is int and entry["rows"] > 0, "invalid row count")
        rows, seen = [], set()
        with source.open() as stream:
            for line in stream:
                row = json.loads(line, object_pairs_hook=unique_object)
                require(isinstance(row, dict) and set(row) ==
                        {"schema_version", "id", "state", "question", "options"},
                        "decision-only fields required; labels/metadata prohibited")
                require(row["schema_version"] == "0.1" and
                        isinstance(row["id"], str) and row["id"].strip() and
                        row["id"] not in seen, "invalid or duplicate decision ID")
                require(isinstance(row["state"], str) and isinstance(row["question"], str)
                        and row["question"].strip(), "invalid decision text")
                opts = row["options"]
                require(isinstance(opts, list) and 2 <= len(opts) <= 26, "require 2..26 choices")
                ids = set()
                for opt in opts:
                    require(isinstance(opt, dict) and set(opt) == {"id", "text"} and
                            all(isinstance(opt[k], str) and opt[k].strip() for k in ("id", "text")),
                            "invalid option fields")
                    require(opt["id"] not in ids, "duplicate option ID")
                    ids.add(opt["id"])
                seen.add(row["id"])
                rows.append(row)
        require(len(rows) == entry["rows"], "input row count mismatch")
        suites.append((name, rows, {**entry, "path": str(source)}))
    return suites


def distribution(values):
    if not values:
        return {"count": 0, "min": None, "max": None, "p50": None, "p95": None}
    ordered = sorted(values)
    return {"count": len(values), "min": ordered[0], "max": ordered[-1],
            "p50": ordered[math.ceil(0.50 * len(values)) - 1],
            "p95": ordered[math.ceil(0.95 * len(values)) - 1]}


def prepare(tokenizer, cfg, row):
    content = [row["state"], row["question"], *(o["text"] for o in row["options"])]
    require(not any(special in text for special in tokenizer.all_special_tokens for text in content),
            "unsupported: template special-token string in source content")
    letters = cfg["symbols"][:len(row["options"])]
    user = USER.format(state=row["state"], question=row["question"], options="\n".join(
        f"{letter}. {option['text']}" for letter, option in zip(letters, row["options"])))
    rendered = tokenizer.apply_chat_template(
        [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        tokenize=False, add_generation_prompt=True)
    prompt = tokenizer.encode(rendered, add_special_tokens=False, truncation=False)
    require(len(prompt) <= cfg["max_input_tokens"],
            f"unsupported: full prompt length {len(prompt)} exceeds frozen cap {cfg['max_input_tokens']}")
    answer_ids = []
    for letter in letters:
        complete = tokenizer.encode(rendered + letter, add_special_tokens=False, truncation=False)
        require(len(complete) == len(prompt) + 1 and complete[:-1] == prompt,
                "unsupported: answer boundary is not an identical prefix plus exactly one token")
        answer_ids.append(complete[-1])
    require(len(set(answer_ids)) == len(answer_ids), "answer symbols must have distinct tokens")
    return prompt, answer_ids


def evidence(config_path, manifest_path, model_dir, checkpoint_manifest=None):
    # Importing the tokenizer never imports Jeff's scorer or constructs a model.
    from transformers import AutoTokenizer

    cfg = configuration(config_path)
    binding = None
    if checkpoint_manifest is not None:
        from jeff.runtime.qwen_checkpoint import validate_checkpoint

        binding, asset_hashes = validate_checkpoint(
            checkpoint_manifest, model_dir, config_path, cfg, require=require, load=load,
            digest=digest, safe_path=safe_path, assets=assets)
    else:
        asset_hashes = assets(model_dir, cfg)
    is_v2 = (binding is not None and
             binding["manifest"]["schema_version"] == "jeff.qwen-trained-checkpoint.v2")
    if is_v2:
        from jeff.runtime import qwen_readout

    suites = read_inputs(manifest_path)
    if is_v2:
        require(tuple(len(rows) for _, rows, _ in suites) == (300, 300, 24),
                "v2 requires the frozen 300/300/24 development suites")
        require(cfg["startup_rows"] == 3, "v2 requires exactly three startup forwards")
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True, trust_remote_code=False)
    require(isinstance(tokenizer.chat_template, str) and tokenizer.chat_template, "official chat template required")
    prepared, reports = [], []
    for name, rows, entry in suites:
        encoded = []
        for row in rows:
            try:
                encoded.append(prepare(tokenizer, cfg, row))
                if is_v2:
                    qwen_readout.validate_answer_ids(binding, encoded[-1][1], require=require)
            except ValueError as exc:
                raise ValueError(f"suite {name}, input {row['id']}: {exc}") from exc
        prepared.append((name, rows, encoded))
        reports.append({"input": entry, "lengths": distribution([len(p) for p, _ in encoded]),
                        "rows": [{"id": row["id"], "input_tokens": len(prompt),
                                  "answer_token_ids": answers,
                                  "prompt_token_sha256": text_hash(json.dumps(prompt))}
                                 for row, (prompt, answers) in zip(rows, encoded)]})
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    proof = {"schema_version": "p3.audit.v1", "config_path": str(config_path),
            "config": cfg, "config_sha256": digest(config_path), "source_sha256": digest(SOURCE),
            "git_revision": revision, "git_status": subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True),
            "input_manifest_path": str(manifest_path), "input_manifest": load(manifest_path),
            "input_manifest_sha256": digest(manifest_path),
            "model_assets": asset_hashes, "chat_template_sha256": text_hash(tokenizer.chat_template),
            "environment": environment(), "suites": reports}
    if binding is not None:
        proof["trained_checkpoint"] = binding
    if is_v2:
        proof["readout_source_sha256"] = digest(Path(qwen_readout.__file__).resolve())
        executable_paths = ["pyproject.toml", "uv.lock", "src/jeff/__init__.py",
            "src/jeff/runtime/__init__.py", "src/jeff/model/__init__.py",
            "src/jeff/model/scorer.py", "src/jeff/model/qwen_readout_proof.py", *[
                f"src/jeff/runtime/{name}.py" for name in
                ("qwen_challenger", "qwen_checkpoint", "qwen_readout", "qwen_safetensors")]]
        proof["executable_sources"] = {name: digest(ROOT / name) for name in executable_paths}
        proof["executable_git_status"] = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all", "--", *executable_paths],
            cwd=ROOT, text=True)
    return proof, prepared


def memory(torch, device, stage):
    sample = {"stage": stage}
    if device == "mps":
        sample.update(current_allocated_bytes=torch.mps.current_allocated_memory(),
                      driver_allocated_bytes=torch.mps.driver_allocated_memory())
    return sample


def predict(args, receipt, start):
    audit = load(args.audit_dir / "audit.json")
    require(audit["status"] == "complete", "incomplete audit")
    frozen = audit["evidence"]
    checkpoint_manifest = (Path(frozen["trained_checkpoint"]["manifest_path"])
                           if "trained_checkpoint" in frozen else None)
    current, suites = evidence(Path(frozen["config_path"]), Path(frozen["input_manifest_path"]),
                               args.model_dir, checkpoint_manifest=checkpoint_manifest)
    cfg = current["config"]
    is_v2 = ("trained_checkpoint" in current and
             current["trained_checkpoint"]["manifest"]["schema_version"] ==
             "jeff.qwen-trained-checkpoint.v2")
    if is_v2:
        from jeff.runtime import qwen_readout

        receipt["forwards"] = {"maximum": 627, "expected_startup": 3,
                               "expected_suite_rows": [300, 300, 24],
                               "attempted": 0, "completed": 0}
        context_keys = {"git_revision", "git_status"}
        require({k: v for k, v in current.items() if k not in context_keys} ==
                {k: v for k, v in frozen.items() if k not in context_keys},
                "v2 executable/config/input/model/tokenization/environment changed since audit")
        require(not current["executable_git_status"], "v2 executable sources must be clean and frozen")
        receipt["audit_git_context"] = {k: frozen[k] for k in context_keys}
    else:
        require(current == frozen, "code/config/input/model/tokenization/environment changed since audit")
        require(not current["git_status"], "prediction requires the clean frozen code revision")
    require(args.device == cfg["device"], "device must match the pre-outcome frozen recipe")
    receipt["suites"] = [{"name": name, "status": "not_started", "expected_rows": len(rows),
                         "written_rows": 0, "coverage": 0.0,
                         "expected_input_tokens": sum(len(p) for p, _ in encoded),
                         "input_length_distribution": distribution([len(p) for p, _ in encoded])}
                        for name, rows, encoded in suites]
    receipt.update(audit_sha256=digest(args.audit_dir / "audit.json"), evidence=current,
                   device=args.device, dtype="float32", probability_semantics=cfg["probability_semantics"])
    require(os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") in (None, "0"), "MPS fallback must be disabled")
    import torch
    from transformers import AutoModelForCausalLM

    torch.set_num_threads(cfg["threads"])
    require(args.device == "cpu" or torch.backends.mps.is_available(), "MPS unavailable; no automatic fallback")

    def deadline():
        require(time.monotonic() - start < cfg["maximum_run_seconds"], "maximum total run time exceeded")
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss_bytes = rss if sys.platform == "darwin" else rss * 1024
        require(rss_bytes <= cfg["max_cpu_rss_bytes"], "CPU lifetime RSS guard exceeded")
        if args.device == "mps":
            driver = torch.mps.driver_allocated_memory()
            require(driver <= cfg["max_mps_driver_bytes"], "MPS driver allocation guard exceeded")
            if is_v2:
                headroom = torch.mps.recommended_max_memory() - driver
                receipt["minimum_observed_recommended_headroom_bytes"] = min(
                    receipt.get("minimum_observed_recommended_headroom_bytes", headroom), headroom)
                require(headroom >= 2 * 2**30, "v2 recommended MPS headroom below 2 GiB")

    def sync():
        if args.device == "mps":
            torch.mps.synchronize()

    deadline()
    load_start = time.monotonic()
    storage_seconds = 0.0
    if is_v2:
        model, loading_info = AutoModelForCausalLM.from_pretrained(
            str(args.model_dir), local_files_only=True, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32,
            attn_implementation=cfg["attention"], output_loading_info=True,
            ignore_mismatched_sizes=False)
        receipt["loading_info"] = loading_info
        require(isinstance(loading_info, dict), "v2 loading diagnostics must be an object")
        require(all(key in loading_info and loading_info[key] == [] for key in
                    ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")),
                "v2 requires all four empty loading diagnostics")
        proof_start = time.monotonic()
        try:
            receipt["readout_cpu_storage"] = qwen_readout.validate_storage(model, require=require)
        finally:
            storage_seconds = time.monotonic() - proof_start
            receipt["readout_storage_seconds"] = storage_seconds
            receipt["readout_proof_seconds"] = storage_seconds
        deadline()
    else:
        model = AutoModelForCausalLM.from_pretrained(str(args.model_dir), local_files_only=True,
            trust_remote_code=False, use_safetensors=True, torch_dtype=torch.float32,
            attn_implementation=cfg["attention"])
    require("logits_to_keep" in inspect.signature(model.forward).parameters,
            "last-token-only projection unsupported; full-prompt logits prohibited")
    model.requires_grad_(False).eval().to(args.device)
    sync()
    receipt["cold_load_seconds"] = time.monotonic() - load_start
    if is_v2:
        receipt["cold_load_seconds"] -= storage_seconds
    require(all(p.dtype == torch.float32 and p.device.type == args.device for p in model.parameters()),
            "unexpected parameter device/dtype")
    receipt["memory_samples"].append(memory(torch, args.device, "after_load"))
    if is_v2:
        proof_start = time.monotonic()
        try:
            receipt["readout_reload"] = qwen_readout.validate_loaded(
                model, current["trained_checkpoint"], loading_info, require=require, guard=deadline)
        finally:
            receipt["readout_reload_seconds"] = time.monotonic() - proof_start
            receipt["readout_proof_seconds"] = storage_seconds + receipt["readout_reload_seconds"]
            receipt["memory_samples"].append(memory(torch, args.device, "after_readout_proof"))
        deadline()

    def forward(encoded):
        deadline()
        prompt, answers = encoded
        ids = torch.tensor([prompt], dtype=torch.long, device=args.device)
        sync()
        before = time.monotonic()
        with torch.inference_mode():
            if is_v2:
                attention_mask = torch.ones_like(ids)
                require(receipt["forwards"]["attempted"] < receipt["forwards"]["maximum"],
                        "v2 forward budget exhausted")
                receipt["forwards"]["attempted"] += 1
                result = model(input_ids=ids, attention_mask=attention_mask,
                               use_cache=False, logits_to_keep=1)
                sync()
                receipt["forwards"]["completed"] += 1
            else:
                result = model(input_ids=ids, attention_mask=torch.ones_like(ids),
                               use_cache=False, logits_to_keep=1)
                sync()
            latency = time.monotonic() - before
            require(tuple(result.logits.shape[:2]) == (1, 1), "unexpected logits projection")
            probabilities = torch.softmax(result.logits[0, 0, answers].float(), dim=0).cpu().tolist()
        require(all(math.isfinite(p) and 0 <= p <= 1 for p in probabilities)
                and abs(sum(probabilities) - 1) <= 1e-6, "invalid conditional probabilities")
        deadline()
        return probabilities, latency

    startup_start = time.monotonic()
    startup = [encoded for _, _, encodings in suites for encoded in encodings][:cfg["startup_rows"]]
    if is_v2:
        require(len(startup) == 3, "v2 requires exactly three existing startup rows")
    receipt["startup"] = {"rows": 0, "forward_seconds": [], "elapsed_seconds": None}
    for encoded in startup:
        _, latency = forward(encoded)
        receipt["startup"]["rows"] += 1
        receipt["startup"]["forward_seconds"].append(latency)
    receipt["startup"]["elapsed_seconds"] = time.monotonic() - startup_start
    receipt["memory_samples"].append(memory(torch, args.device, "after_startup"))
    for suite_index, (name, rows, encodings) in enumerate(suites):
        deadline()
        stats = receipt["suites"][suite_index]
        stats.update(status="running", input_tokens=0, forward_seconds=[])
        before = time.monotonic()
        output = args.output_dir / f"{name}.jsonl"
        try:
            with output.open("x") as stream:
                for row, encoded in zip(rows, encodings):
                    stats["active_input_id"] = row["id"]
                    probabilities, latency = forward(encoded)
                    prediction = {"schema_version": "0.1", "id": row["id"], "probabilities": [
                        {"option_id": opt["id"], "probability": p}
                        for opt, p in zip(row["options"], probabilities)]}
                    stream.write(json.dumps(prediction, allow_nan=False) + "\n")
                    stream.flush()
                    stats["written_rows"] += 1
                    stats["input_tokens"] += len(encoded[0])
                    stats["forward_seconds"].append(latency)
                    del stats["active_input_id"]
            stats["status"] = "complete"
        finally:
            if stats["status"] != "complete":
                stats["status"] = "partial" if stats["written_rows"] else "failed"
            stats["elapsed_seconds"] = time.monotonic() - before
            stats["rows_per_second"] = stats["written_rows"] / stats["elapsed_seconds"]
            stats["input_tokens_per_second"] = stats["input_tokens"] / stats["elapsed_seconds"]
            stats["coverage"] = stats["written_rows"] / len(rows)
            stats["latency_seconds"] = distribution(stats["forward_seconds"])
            if output.exists():
                stats["output_sha256"] = digest(output)
                output.chmod(0o444)
    if is_v2:
        require(receipt["startup"]["rows"] == 3 and
                receipt["forwards"]["attempted"] == receipt["forwards"]["completed"] == 627,
                "v2 requires exactly 627 attempted and completed forwards")
    receipt["memory_samples"].append(memory(torch, args.device, "end"))
    deadline()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit")
    audit.add_argument("--config", type=Path, required=True)
    audit.add_argument("--inputs", type=Path, required=True)
    audit.add_argument("--audit-dir", type=Path, required=True)
    audit.add_argument("--checkpoint-manifest", type=Path)
    run = commands.add_parser("predict")
    run.add_argument("--audit-dir", type=Path, required=True)
    run.add_argument("--output-dir", type=Path, required=True)
    run.add_argument("--device", choices=("mps", "cpu"), required=True)
    for cmd in (audit, run):
        cmd.add_argument("--model-dir", type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    args.model_dir = safe_path(args.model_dir)
    args.audit_dir = args.audit_dir.resolve()
    directory = args.audit_dir if args.command == "audit" else args.output_dir.resolve()
    directory.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": "p3.audit.v1" if args.command == "audit" else "p3.run.v1",
               "status": "failed", "suites": [], "memory_samples": []}
    exit_code = 0
    try:
        if args.command == "audit":
            proof, _ = evidence(args.config.resolve(), safe_path(args.inputs), args.model_dir,
                                checkpoint_manifest=args.checkpoint_manifest)
            receipt["evidence"] = proof
            receipt["status"] = "complete"
        else:
            predict(args, receipt, start)
            receipt["status"] = "complete"
    except BaseException as exc:
        # Do not leak source content, decisions or model output in diagnostic feedback.
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:2000], "retry": False}
        exit_code = 1
    finally:
        if args.command == "predict" and "torch" in sys.modules:
            try:
                receipt["memory_samples"].append(memory(sys.modules["torch"], args.device, "process_end"))
            except Exception as exc:
                receipt["memory_sample_error"] = type(exc).__name__
        receipt["process_runtime_seconds"] = time.monotonic() - start
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        receipt["cpu_lifetime_maxrss_bytes"] = rss if sys.platform == "darwin" else rss * 1024
        receipt["memory_qualification"] = "CPU process-lifetime ru_maxrss; MPS observed samples and their maxima are NOT peak memory"
        receipt["mps_observed_maxima_bytes"] = {
            key: max((s[key] for s in receipt["memory_samples"] if key in s), default=None)
            for key in ("current_allocated_bytes", "driver_allocated_bytes")}
        save(directory / ("audit.json" if args.command == "audit" else "receipt.json"), receipt)
        directory.chmod(0o555)
    print(json.dumps({"status": receipt["status"], "receipt_dir": str(directory),
                      "process_runtime_seconds": receipt["process_runtime_seconds"]}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
