#!/usr/bin/env python3
"""Frozen P3 order/letter diagnostic. Runtime only; no work occurs on import."""

import argparse
import hashlib
import inspect
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import sys
import time
from importlib.metadata import version

MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
SYSTEM = "You are a decision assistant. Choose exactly one of the listed options. Reply with only its letter."
USER = "State:\n{state}\n\nQuestion:\n{question}\n\nOptions:\n{options}"
P3_AUDIT_SHA = "8e0dc65beb1c9dd5a21b2c4170853bc78bf14116429a9311c28e568c129d870a"
P3_SOURCE_SHA = "325d3a6b8e5577bba3b885fe8b61d5551305b456e2586d3949b2c45c649438d5"
P3_CONFIG_SHA = "2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f"
WEIGHT_SHA = "fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe"
CHAT_SHA = "cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f"
PACKET_SHA = "7598451302c5389e62476c88e7c2489fa355e0c40611e91cfbd6da1d9dc35e03"
LIMIT = 8 * 1024**3
SECONDS = 300
CONDITIONS = {f"O{o}L{l}" for o in (0, 1) for l in (0, 1)}
SOURCE = Path(__file__).resolve()


class GuardError(ValueError):
    """Only caller-supplied, content-free diagnostic messages."""


def require(ok, message):
    if not ok:
        raise GuardError(message)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def text_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def parse(text):
    def invalid(_):
        raise ValueError("nonfinite JSON constant")
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=invalid)


def load(path):
    return parse(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")
    path.chmod(0o444)


def safe(path):
    p = Path(path).resolve(strict=True)
    require(not any(any(word in part.lower() for word in
                        ("evaluation", "probe", "final", "reference")) for part in p.parts),
            "protected data paths prohibited")
    return p


def no_labels(value):
    # Metadata is opaque; do not interpret undocumented selection/config fields.
    if isinstance(value, dict):
        for key, child in value.items():
            require(key.lower() not in {"target", "target_id", "label", "labels", "answer",
                                        "answer_id", "correct", "correct_id", "gold", "gold_id"},
                    "labels/answers prohibited in packet metadata")
            no_labels(child)
    elif isinstance(value, list):
        for child in value:
            no_labels(child)


def environment():
    return {"python": sys.version, "platform": platform.platform(),
            "packages": {p: version(p) for p in
                         ("torch", "transformers", "tokenizers", "safetensors")}}


def read_rows(path):
    rows, ids, cases = [], set(), {}
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            require(len(rows) < 192, "more than 192 presentations")
            row = parse(line)
            require(isinstance(row, dict) and set(row) == {
                "id", "case_id", "condition", "order_reversed", "letters_reversed",
                "state", "question", "options"}, "decision packet row schema")
            require(all(isinstance(row[k], str) and row[k].strip()
                        for k in ("id", "case_id", "question")), "invalid row identifiers/text")
            require(row["id"] not in ids, "duplicate presentation id")
            ids.add(row["id"])
            require(isinstance(row["state"], str), "invalid state")
            require(type(row["order_reversed"]) is bool and
                    type(row["letters_reversed"]) is bool, "condition flags must be booleans")
            condition = f"O{int(row['order_reversed'])}L{int(row['letters_reversed'])}"
            require(row["condition"] == condition and row["id"] == row["case_id"] + "::" + condition,
                    "condition/flag/presentation identity mismatch")
            opts = row["options"]
            require(isinstance(opts, list) and 2 <= len(opts) <= 6, "require 2..6 choices")
            seen = set()
            for display, opt in enumerate(opts):
                require(isinstance(opt, dict) and set(opt) == {
                    "id", "text", "letter", "original_position"}, "option schema")
                require(all(isinstance(opt[k], str) and opt[k].strip()
                            for k in ("id", "text", "letter")), "invalid option text/id/letter")
                require(opt["id"] not in seen, "duplicate option id")
                seen.add(opt["id"])
                pos = len(opts) - 1 - display if row["order_reversed"] else display
                letter_pos = len(opts) - 1 - display if row["letters_reversed"] else display
                require(type(opt["original_position"]) is int and
                        opt["original_position"] == pos, "incorrect original position/order")
                require(opt["letter"] == chr(65 + letter_pos), "incorrect letter assignment")
            group = cases.setdefault(row["case_id"], {})
            require(condition not in group, "duplicate case condition")
            group[condition] = row
            rows.append(row)
    require(1 <= len(cases) <= 48 and len(rows) == 4 * len(cases), "case/presentation bounds")
    for group in cases.values():
        require(set(group) == CONDITIONS, "exactly four conditions per case required")
        base = group["O0L0"]
        original = [(o["id"], o["text"]) for o in base["options"]]
        for row in group.values():
            require((row["state"], row["question"]) == (base["state"], base["question"]),
                    "case text changed across conditions")
            require([(o["id"], o["text"]) for o in sorted(
                row["options"], key=lambda o: o["original_position"])] == original,
                "case options changed across conditions")
    return rows, len(cases)


def prepare(tokenizer, row):
    content = [row["state"], row["question"], *(o["text"] for o in row["options"])]
    require(not any(special in text for special in tokenizer.all_special_tokens
                    for text in content), "special-token injection in content")
    user = USER.format(state=row["state"], question=row["question"], options="\n".join(
        f"{opt['letter']}. {opt['text']}" for opt in row["options"]))
    rendered = tokenizer.apply_chat_template(
        [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        tokenize=False, add_generation_prompt=True)
    prompt = tokenizer.encode(rendered, add_special_tokens=False, truncation=False)
    require(0 < len(prompt) <= 1024, "full untruncated prompt exceeds frozen 1024 cap")
    answers = []
    for opt in row["options"]:
        complete = tokenizer.encode(rendered + opt["letter"], add_special_tokens=False,
                                    truncation=False)
        require(len(complete) == len(prompt) + 1 and complete[:-1] == prompt,
                "answer must be exactly one token after unchanged rendered prefix")
        answers.append(complete[-1])
    require(len(set(answers)) == len(answers), "answer tokens not distinct")
    return (prompt, answers), {"id": row["id"], "input_tokens": len(prompt),
        "rendered_prompt_sha256": text_hash(rendered),
        "prompt_token_sha256": text_hash(json.dumps(prompt)), "answer_token_ids": answers}


def packet_bindings(args):
    root = args.inputs.parent
    manifest_path = root / "packet.json"
    require(manifest_path.is_file() and digest(manifest_path) == PACKET_SHA,
            "preselected packet identity mismatch")
    manifest = load(manifest_path)
    require(manifest["schema_version"] == "r6.order-packet.v1" and
            manifest["cases"] == 48 and manifest["input"]["rows"] == 192 and
            set(manifest["conditions"]) == CONDITIONS and manifest["split"] == "train",
            "frozen packet scope mismatch")
    for key, path in (("input", args.inputs), ("config", args.config), ("selection", args.selection)):
        require(manifest[key]["path"] == path.name and digest(path) == manifest[key]["sha256"],
                "declared packet file binding mismatch")
    require(args.config.parent == root and args.selection.parent == root,
            "inputs/config/selection must share packet directory")
    bound = {}
    # Bind all packet files, not guessed manifest keys. Outputs must be outside this tree.
    for p in sorted(root.rglob("*")):
        require(not p.is_symlink(), "packet symlinks prohibited")
        if p.is_file():
            require(p.stat().st_size <= 32 * 1024**2, "oversized packet file")
            safe(p)
            bound[str(p.relative_to(root))] = digest(p)
    for p in (args.inputs, args.config, args.selection):
        require(p.name in bound, "missing explicit packet file")
    for p in (args.config, args.selection, root / "packet.json"):
        if p.exists():
            value = load(p)
            require(isinstance(value, (dict, list)), "packet metadata must be object/list")
            no_labels(value)
    return bound


def evidence(args, verify_weights, check):
    check()
    require(digest(args.p3_audit) == P3_AUDIT_SHA, "P3 audit attestation changed")
    p3 = load(args.p3_audit)
    require(p3["status"] == "complete", "P3 audit incomplete")
    p3 = p3["evidence"]
    require(p3["source_sha256"] == P3_SOURCE_SHA and
            p3["config_sha256"] == P3_CONFIG_SHA and
            p3["model_assets"]["model.safetensors"] == WEIGHT_SHA and
            p3["chat_template_sha256"] == CHAT_SHA, "P3 receipt pins")
    cfg = p3["config"]
    require(cfg["model_id"] == MODEL and cfg["revision"] == REVISION and
            cfg["system_prompt"] == SYSTEM and cfg["user_template"] == USER and
            cfg["max_input_tokens"] == 1024, "P3 template/model controls changed")
    expected = p3["model_assets"]
    files = {str(p.relative_to(args.model_dir)): p for p in args.model_dir.rglob("*")
             if p.is_file() and ".cache" not in p.relative_to(args.model_dir).parts}
    require(set(files) == set(expected), "model assets must exactly match frozen P3 inventory")
    for name, path in sorted(files.items()):
        check()
        require(path.resolve().is_relative_to(args.model_dir), "model asset escapes model directory")
        if name != "model.safetensors" or verify_weights:
            require(digest(path) == expected[name], "model asset hash mismatch: " + name)
        check()
    binding = packet_bindings(args)
    packet_cfg = load(args.config)
    require(packet_cfg == {**cfg, "maximum_run_seconds": SECONDS},
            "packet config differs from P3 beyond authorized runtime cap")
    rows, cases = read_rows(args.inputs)
    selection = load(args.selection)
    require(selection.get("schema_version") == "r6.selection.v1" and
            selection.get("train_manifest_sha256") ==
            "d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac",
            "released TRAIN selection identity mismatch")
    require(isinstance(selection.get("cases"), list) and len(selection["cases"]) == cases and
            {c["case_id"] for c in selection["cases"]} == {r["case_id"] for r in rows},
            "selection/presentation case coverage mismatch")
    # Audit uses only tokenizer APIs, explicitly disabling the PyTorch backend before import.
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(args.model_dir), local_files_only=True,
                                              trust_remote_code=False)
    require(isinstance(tokenizer.chat_template, str) and
            text_hash(tokenizer.chat_template) == CHAT_SHA, "official chat template mismatch")
    encoded, reports = [], []
    for row in rows:
        check()
        tokens, report = prepare(tokenizer, row)
        encoded.append(tokens)
        reports.append(report)
    proof = {"source_sha256": digest(SOURCE), "p3_audit_sha256": P3_AUDIT_SHA,
        "p3_audited_source_sha256": P3_SOURCE_SHA, "p3_config_sha256": P3_CONFIG_SHA,
        "p3_config": cfg, "model_id": MODEL, "revision": REVISION,
        "model_assets": expected, "chat_template_sha256": CHAT_SHA,
        "paths": {k: str(getattr(args, k)) for k in
                  ("inputs", "config", "selection", "model_dir", "p3_audit")},
        "inputs_sha256": digest(args.inputs), "config_sha256": digest(args.config),
        "selection_sha256": digest(args.selection), "packet_files": binding,
        "cases": cases, "presentations": len(rows), "prepared": reports,
        "environment": environment(),
        "controls": {"seconds": SECONDS, "rss_bytes": LIMIT, "mps_driver_bytes": LIMIT,
                     "batch_size": 1, "threads": 4, "dtype": "float32", "device": "mps",
                     "attention": "sdpa", "use_cache": False, "logits_to_keep": 1,
                     "temperature": 1.0, "startup_extra_forwards": 0}}
    check()
    return proof, rows, encoded


def rss():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == "darwin" else value * 1024


def predict(args, receipt, check):
    audit = load(args.audit_dir / "audit.json")
    require(audit["status"] == "pass", "audit did not pass")
    receipt["audit_sha256"] = digest(args.audit_dir / "audit.json")
    current, rows, encoded = evidence(args, True, check)
    require(current == audit["evidence"], "audit binding/tokenization/environment changed")
    receipt.update(evidence=current, expected_rows=len(rows), cases=current["cases"],
                   actual_model_asset_hashes_verified=True)
    require(os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK") in (None, "0"),
            "MPS fallback prohibited")
    import torch
    from transformers import AutoModelForCausalLM
    torch.set_num_threads(4)
    require(torch.backends.mps.is_available(), "MPS required; no fallback")

    def sample(stage):
        item = {"stage": stage, "elapsed_seconds": time.monotonic() - receipt["_start"],
                "cpu_lifetime_maxrss_bytes": rss(),
                "current_allocated_bytes": torch.mps.current_allocated_memory(),
                "driver_allocated_bytes": torch.mps.driver_allocated_memory()}
        receipt["memory_samples"].append(item)
        require(item["driver_allocated_bytes"] <= LIMIT, "MPS driver memory guard exceeded")
        check()

    sample("before_load")
    before = time.monotonic()
    model = AutoModelForCausalLM.from_pretrained(str(args.model_dir), local_files_only=True,
        trust_remote_code=False, use_safetensors=True, torch_dtype=torch.float32,
        attn_implementation="sdpa")
    sample("after_cpu_load")
    require("logits_to_keep" in inspect.signature(model.forward).parameters,
            "last-token-only projection unsupported")
    model.requires_grad_(False).eval().to("mps")
    torch.mps.synchronize()
    receipt["cold_load_seconds"] = time.monotonic() - before
    require(all(p.dtype == torch.float32 and p.device.type == "mps"
                for p in model.parameters()), "parameter dtype/device mismatch")
    sample("after_load")
    output = args.output_dir / "predictions.jsonl"
    with output.open("x", encoding="utf-8") as stream:
        for row, (prompt, answers) in zip(rows, encoded):
            receipt["active_input_id"] = row["id"]
            sample("before_forward")
            ids = torch.tensor([prompt], dtype=torch.long, device="mps")
            mask = torch.ones_like(ids)
            torch.mps.synchronize()
            before = time.monotonic()
            receipt["forward_attempts"] += 1
            with torch.inference_mode():
                result = model(input_ids=ids, attention_mask=mask,
                               use_cache=False, logits_to_keep=1)
                torch.mps.synchronize()
                elapsed = time.monotonic() - before
                receipt["completed_forwards"] += 1
                require(tuple(result.logits.shape[:2]) == (1, 1), "unexpected logits shape")
                full = result.logits[0, 0].float()
                allowed = full[answers]
                probabilities = torch.softmax(allowed, dim=0).cpu().tolist()
                logits = allowed.cpu().tolist()
                full_norm = torch.logsumexp(full, dim=0).item()
                allowed_logmass = (torch.logsumexp(allowed, dim=0).item() - full_norm)
            require(all(math.isfinite(x) for x in logits + probabilities +
                        [full_norm, allowed_logmass]), "nonfinite scores")
            require(all(0 <= p <= 1 for p in probabilities) and
                    abs(sum(probabilities) - 1) <= 1e-6 and allowed_logmass <= 1e-5,
                    "invalid conditional probabilities/mass")
            # Sort by the packet's verified original positions, not the custom letter assignment.
            aligned = sorted(zip(row["options"], probabilities, logits, answers),
                             key=lambda item: item[0]["original_position"])
            prediction = {"schema_version": "0.1", "id": row["id"],
                "case_id": row["case_id"], "condition": row["condition"],
                "probabilities": [{"option_id": o["id"], "probability": p}
                                  for o, p, _, _ in aligned],
                "chosen_option_id": row["options"][probabilities.index(max(probabilities))]["id"],
                "tied_top_option_ids_display_order": [o["id"] for o, p in
                    zip(row["options"], probabilities) if p == max(probabilities)],
                "option_scores": [{"option_id": o["id"], "original_position": o["original_position"],
                                   "letter": o["letter"], "token_id": token, "logit": logit}
                                  for o, _, logit, token in aligned],
                "log_full_vocab_normalizer": full_norm,
                "allowed_full_vocab_logmass": allowed_logmass,
                "allowed_full_vocab_mass": math.exp(allowed_logmass),
                "input_tokens": len(prompt), "forward_seconds": elapsed,
                "first_forward": receipt["completed_forwards"] == 1}
            stream.write(json.dumps(prediction, allow_nan=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
            receipt["written_rows"] += 1
            receipt["forward_seconds"].append(elapsed)
            if receipt["written_rows"] == 1:
                receipt["first_forward_seconds"] = elapsed
            del result, full, allowed, ids, mask
            sample("after_forward")
            receipt.pop("active_input_id", None)
    require(receipt["forward_attempts"] == receipt["completed_forwards"] ==
            receipt["written_rows"] == len(rows), "forward/output coverage mismatch")
    # Small packet/source recheck only; never rescan weights after inference.
    require(packet_bindings(args) == current["packet_files"] and
            digest(SOURCE) == current["source_sha256"], "packet/source changed during run")
    sample("end")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "predict"))
    for name in ("inputs", "config", "selection", "model-dir", "p3-audit", "audit-dir"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--train-only-confirmed", action="store_true", required=True,
                        help="Runtime attests packet selection is exclusively authorized TRAIN")
    args = parser.parse_args()
    start = time.monotonic()
    require(args.command != "predict" or args.output_dir is not None, "predict needs --output-dir")
    # Force offline before any model-stack import; audit explicitly prevents torch backend import.
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", HF_DATASETS_OFFLINE="1",
                      TOKENIZERS_PARALLELISM="false", HF_HUB_DISABLE_TELEMETRY="1")
    os.environ["USE_TORCH"] = "0" if args.command == "audit" else "1"
    os.environ["USE_TF"] = "0"
    os.environ["USE_FLAX"] = "0"
    directory = (args.audit_dir if args.command == "audit" else args.output_dir).resolve()
    packet_root = args.inputs.resolve().parent
    require(not directory.is_relative_to(packet_root), "output/audit must be outside packet tree")
    directory.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": "r6.order." + args.command + ".v1", "status": "failed",
        "_start": start, "expected_rows": None, "written_rows": 0, "forward_attempts": 0,
        "completed_forwards": 0, "forward_seconds": [], "memory_samples": [],
        "executor_source_sha256": digest(SOURCE),
        "train_only_operator_attestation": True, "auto_retry": False,
        "memory_scope": "CPU process-lifetime ru_maxrss; MPS cooperative observed samples, not peak",
        "runtime_scope": "whole command including hashes/tokenizer/load/forward/output; cooperative 300s",
        "probability_semantics": "T=1 conditional softmax over allowed letter tokens; not calibrated",
        "normal_letter_equivalence": "L0 uses P3 prepare rendering/readout, with supplied displayed option order"}
    code = 1

    def check():
        require(time.monotonic() - start < SECONDS, "300s cooperative command guard exceeded")
        require(rss() <= LIMIT, "8GiB CPU lifetime RSS guard exceeded")

    def interrupted(signum, frame):
        raise RuntimeError("supervisor signal " + str(signum))

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        for name in ("inputs", "config", "selection", "model_dir"):
            setattr(args, name, safe(getattr(args, name)))
        # This is the sole approved release metadata path; no referenced evaluation files are opened.
        args.p3_audit = args.p3_audit.resolve(strict=True)
        args.audit_dir = args.audit_dir.resolve()
        if args.command == "audit":
            proof, rows, _ = evidence(args, False, check)
            require("torch" not in sys.modules, "audit unexpectedly imported torch")
            receipt.update(evidence=proof, expected_rows=len(rows), cases=proof["cases"],
                weights_verification="P3 receipt attestation only; actual weight hash required at predict")
        else:
            args.output_dir = directory
            predict(args, receipt, check)
        check()
        receipt["status"] = "pass"
        code = 0
    except BaseException as exc:
        # Avoid exception strings that could quote packet content or model outputs.
        receipt["error"] = {"type": type(exc).__name__,
                            "message": str(exc) if isinstance(exc, GuardError)
                            else "operation failed; no retry"}
    finally:
        receipt.pop("_start", None)
        receipt["process_runtime_seconds"] = time.monotonic() - start
        receipt["cpu_lifetime_maxrss_bytes"] = rss()
        receipt["coverage"] = (receipt["written_rows"] / receipt["expected_rows"]
                               if receipt["expected_rows"] else None)
        receipt["output_hashes"] = {}
        for p in directory.iterdir():
            if p.is_file():
                receipt["output_hashes"][p.name] = digest(p)
                p.chmod(0o444)
        receipt["mps_observed_driver_max_bytes"] = max(
            (s["driver_allocated_bytes"] for s in receipt["memory_samples"]), default=None)
        save(directory / ("audit.json" if args.command == "audit" else "receipt.json"), receipt)
        directory.chmod(0o555)
    print(json.dumps({"status": receipt["status"], "directory": str(directory),
                      "written_rows": receipt["written_rows"], "forward_attempts": receipt["forward_attempts"]}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
