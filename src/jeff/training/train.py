"""Full-backbone supervised training with immutable run artifacts."""

import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import resource
import subprocess
import sys
import time
import traceback

from .dataset import load_dataset, reject_final


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--dataset-manifest", required=True)
    result.add_argument("--output-dir", required=True)
    result.add_argument("--model-id", default="sentence-transformers/all-MiniLM-L6-v2")
    result.add_argument("--architecture", choices=("mean_pool_scalar", "retained_cross_encoder"),
                        default="mean_pool_scalar")
    result.add_argument("--revision", required=True, help="Immutable 40-hex base/tokenizer revision")
    result.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    result.add_argument("--epochs", type=int, default=3)
    result.add_argument("--batch-size", type=int, default=4)
    result.add_argument("--learning-rate", type=float, default=2e-5)
    result.add_argument("--head-learning-rate", type=float, default=5e-4)
    result.add_argument("--max-length", type=int, default=128)
    result.add_argument("--seed", type=int, default=42)
    result.add_argument("--max-steps", type=int)
    result.add_argument("--threads", type=int, default=4)
    result.add_argument("--initial-checkpoint")
    result.add_argument("--initial-checkpoint-sha256", help="SHA256 of initial checkpoint.json")
    result.add_argument("--m9-resource-guards", action="store_true")
    result.add_argument("--m9-initial-run")
    result.add_argument("--m9-initial-run-sha256")
    return result


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return repr(value)
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def write_json(path, data):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(json_safe(data), stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def git_identity(directory):
    def git(*args):
        return subprocess.check_output(
            ["git", "-C", str(directory), *args], stderr=subprocess.DEVNULL, text=True
        ).strip()
    try:
        return {
            "worktree": git("rev-parse", "--show-toplevel"),
            "revision": git("rev-parse", "HEAD"),
            "dirty": bool(git("status", "--porcelain", "--untracked-files=all")),
        }
    except (OSError, subprocess.CalledProcessError):
        return {"worktree": None, "revision": None, "dirty": None, "unavailable": True}


def environment(torch, device):
    versions = {}
    for package in ("torch", "transformers", "tokenizers", "safetensors", "huggingface-hub"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    hardware = {
        "machine": platform.machine(), "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
    }
    if sys.platform == "darwin":
        for key in ("hw.model", "machdep.cpu.brand_string", "hw.memsize"):
            try:
                hardware[key] = subprocess.check_output(
                    ["sysctl", "-n", key], text=True, stderr=subprocess.DEVNULL
                ).strip()
            except (OSError, subprocess.CalledProcessError):
                hardware[key] = None
    return {
        "python": sys.version, "platform": platform.platform(), "versions": versions,
        "torch_version": str(torch.__version__), "hardware": hardware,
        "device": str(device), "torch_threads": torch.get_num_threads(),
        "mps_built": torch.backends.mps.is_built(),
        "mps_available": torch.backends.mps.is_available(),
        "mps_fallback_environment": os.environ.get("PYTORCH_ENABLE_MPS_FALLBACK"),
    }


def memory(torch, device):
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "cpu_max_rss_bytes": raw if sys.platform == "darwin" else raw * 1024,
        "cpu_max_rss_raw": raw,
        "cpu_max_rss_raw_unit": "bytes" if sys.platform == "darwin" else "KiB",
        "cpu_max_rss_scope": "process lifetime high-water RSS; not accelerator peak",
    }
    if device.type == "mps":
        torch.mps.synchronize()
        for key, name in (("mps_current_allocated_bytes", "current_allocated_memory"),
                          ("mps_driver_allocated_bytes", "driver_allocated_memory")):
            function = getattr(torch.mps, name, None)
            result[key] = function() if function is not None else None
        result["mps_measurement"] = "point-in-time, not peak"
    return result


def parameter_hashes(torch, model, guards=None):
    if guards is not None:
        guards.check("before_parameter_hashes")
    hashes = {}
    for name, parameter in model.named_parameters():
        stream = io.BytesIO()
        # Canonical per-tensor torch serialization avoids a separate NumPy dependency.
        tensor = parameter.detach().cpu().contiguous().clone()
        if not bool(torch.isfinite(tensor).all().item()):
            raise ValueError(f"Nonfinite model parameter: {name}")
        torch.save(tensor, stream)
        hashes[name] = hashlib.sha256(stream.getvalue()).hexdigest()
    if guards is not None:
        guards.check("after_parameter_hashes")
    return hashes


def decision_inputs(rows):
    return [
        {"schema_version": row["schema_version"], "id": row["id"],
         "state": row["state"], "question": row["question"],
         "options": [{"id": option["id"], "text": option["text"]} for option in row["options"]]}
        for row in rows
    ]


def batch_loss(torch, model, rows, device):
    logits = model(decision_inputs(rows))
    expected_width = max(len(row["options"]) for row in rows)
    if logits.ndim != 2 or tuple(logits.shape) != (len(rows), expected_width):
        raise ValueError("Scorer logits must have shape batch x maximum candidate count")
    if logits.device.type != device.type:
        raise ValueError("Scorer returned logits on the wrong device")
    targets = torch.tensor(
        [next(i for i, option in enumerate(row["options"]) if option["id"] == row["target_id"]) for row in rows],
        dtype=torch.long, device=device,
    )
    loss = torch.nn.functional.cross_entropy(logits, targets)
    if not bool(torch.isfinite(loss).item()):
        raise ValueError("Nonfinite cross-entropy loss")
    return loss, logits, targets


def evaluate(torch, model, rows, batch_size, device, guards=None):
    if not rows:
        return {"count": 0, "loss": None, "top1_target_agreement": None}
    model.eval()
    loss_sum, correct = 0.0, 0
    with torch.no_grad():
        for offset in range(0, len(rows), batch_size):
            if guards is not None:
                guards.check("before_evaluation_batch")
            batch = rows[offset:offset + batch_size]
            loss, logits, targets = batch_loss(torch, model, batch, device)
            loss_sum += loss.item() * len(batch)
            correct += (logits.argmax(dim=1) == targets).sum().item()
            if guards is not None:
                guards.check("after_evaluation_batch")
    return {"count": len(rows), "loss": loss_sum / len(rows),
            "top1_target_agreement": correct / len(rows),
            "interpretation": "Agreement with supplied targets; teacher labels are not independent correctness. No calibration claim."}


def train_run(args, output, record, started, guards=None):
    import torch
    from jeff.model.scorer import CandidateScorer, validate_decision
    import jeff.model.scorer as scorer_module

    scorer_class = CandidateScorer
    if args.architecture == "retained_cross_encoder":
        from jeff.model.cross_encoder import RetainedCrossEncoder
        scorer_class = RetainedCrossEncoder
    selected_scorer_module = importlib.import_module(scorer_class.__module__)

    for name in ("epochs", "batch_size", "max_length", "threads"):
        if getattr(args, name) <= 0:
            raise ValueError(f"{name} must be positive")
    if args.max_steps is not None and args.max_steps <= 0:
        raise ValueError("max_steps must be positive when supplied")
    for name in ("learning_rate", "head_learning_rate"):
        if not math.isfinite(getattr(args, name)) or getattr(args, name) <= 0:
            raise ValueError(f"{name} must be finite and positive")
    if not re.fullmatch(r"[0-9a-fA-F]{40}", args.revision):
        raise ValueError("revision must be an immutable 40-hex commit")
    if not args.model_id.strip():
        raise ValueError("model_id must be nonempty")
    if args.seed < 0 or args.seed >= 2**64:
        raise ValueError("seed must be in [0, 2**64)")

    initial_checkpoint = getattr(args, "initial_checkpoint", None)
    initial_checkpoint_sha256 = getattr(args, "initial_checkpoint_sha256", None)
    if initial_checkpoint is None:
        if initial_checkpoint_sha256 is not None:
            raise ValueError("initial_checkpoint_sha256 requires initial_checkpoint")
    else:
        if not initial_checkpoint or args.architecture != "retained_cross_encoder":
            raise ValueError("initial_checkpoint requires retained_cross_encoder and a nonempty path")
        if not re.fullmatch(r"[0-9a-f]{64}", initial_checkpoint_sha256 or ""):
            raise ValueError("initial_checkpoint requires an exact lowercase SHA256 of checkpoint.json")
        if guards is None or not args.m9_initial_run:
            raise ValueError("M13 initialization requires guarded pinned initial-run binding")
        if args.m9_initial_run_sha256 != "d50013f9236c69ae47d0b5212a0f607ae461c8bd92a28e25cc2a1d9a162067ee":
            raise ValueError("M13 initialization requires the frozen actual M9 training run SHA256")
        checkpoint_config = Path(initial_checkpoint) / "checkpoint.json"
        if hashlib.sha256(checkpoint_config.read_bytes()).hexdigest() != initial_checkpoint_sha256:
            raise ValueError("Initial checkpoint.json bytes changed")

    rows, identity, manifest_bytes = load_dataset(args.dataset_manifest, validate_decision)
    record["dataset"] = identity
    with (output / "dataset-manifest.json").open("xb") as stream:
        stream.write(manifest_bytes)
    record["dataset"]["frozen_manifest"] = "dataset-manifest.json"
    torch.set_num_threads(args.threads)
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.device == "mps" and not torch.backends.mps.is_available():
        raise ValueError("MPS requested but unavailable; refusing silent CPU fallback")
    device = torch.device("mps" if args.device == "auto" and torch.backends.mps.is_available()
                          else "cpu" if args.device == "auto" else args.device)
    if guards is not None:
        guards.bind(torch, device)
    if device.type == "mps":
        torch.mps.manual_seed(args.seed)
    record["environment"] = environment(torch, device)
    record["seed_policy"] = "Python random + torch CPU + MPS when selected; not a guarantee of bitwise deterministic MPS kernels"
    record["code"]["source_sha256"] = {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (Path(__file__), Path(__file__).with_name("dataset.py"),
                     Path(scorer_module.__file__), Path(selected_scorer_module.__file__))
    }

    if initial_checkpoint is None:
        model = scorer_class.from_pretrained(
            args.model_id, args.revision, max_length=args.max_length, device=str(device)
        )
    else:
        model = scorer_module.load_checkpoint(initial_checkpoint, device=str(device))
        if type(model) is not scorer_class:
            raise ValueError("Initial checkpoint must contain the requested retained cross-encoder")
        if model.temperature != 1.0:
            raise ValueError("M13 initial checkpoint requires unchanged temperature 1.0")
    if guards is not None:
        guards.check("after_load")
    loaded_head_hashes = None
    if args.architecture == "retained_cross_encoder":
        if model.head_initialization != "pretrained":
            raise ValueError("Retained cross-encoder requires a pretrained ranking head")
        loaded_head_hashes = parameter_hashes(torch, model.head, guards)
    model.to(device)
    if args.architecture == "mean_pool_scalar":
        # Preserve the original random-head baseline only for the mean-pool scorer.
        model.head.reset_parameters()
    model.temperature = 1.0
    model.backbone.requires_grad_(True)
    model.head.requires_grad_(True)
    if model.model_id != args.model_id or model.revision != args.revision or model.max_length != args.max_length:
        raise ValueError("Scorer base identity/configuration differs from requested immutable base")
    if any(p.device.type != device.type for p in model.parameters()):
        raise ValueError("Not all model parameters are on the selected device")
    backbone_parameters = list(model.backbone.parameters())
    head_parameters = list(model.head.parameters())
    if not backbone_parameters or not head_parameters:
        raise ValueError("Scorer backbone and head must both have trainable parameters")
    if set(map(id, backbone_parameters)) & set(map(id, head_parameters)):
        raise ValueError("Backbone/head parameter groups overlap")
    if set(map(id, model.parameters())) != set(map(id, backbone_parameters + head_parameters)):
        raise ValueError("Unexpected parameters outside the backbone/head optimizer groups")

    baseline_hashes = parameter_hashes(torch, model, guards)
    if guards is not None:
        if not args.m9_initial_run or not re.fullmatch(r"[0-9a-f]{64}", args.m9_initial_run_sha256 or ""):
            raise ValueError("M9 requires a pinned original M4 run for pre-update identity binding")
        reference_bytes = Path(args.m9_initial_run).read_bytes()
        if hashlib.sha256(reference_bytes).hexdigest() != args.m9_initial_run_sha256:
            if initial_checkpoint is not None:
                raise ValueError("M13 trained M9 reference bytes changed")
            raise ValueError("M9 original-run reference bytes changed")
        reference = json.loads(reference_bytes)
        reference_stage = "after" if initial_checkpoint is not None else "before"
        record["m9_initial_binding"] = {
            "reference_path": str(Path(args.m9_initial_run).resolve()),
            "reference_sha256": args.m9_initial_run_sha256,
            "reference_stage": f"weights.{reference_stage}",
            "actual_parameter_hashes": baseline_hashes,
            "exact_match": baseline_hashes == reference["weights"][reference_stage],
        }
        if reference["status"] != "completed" or not record["m9_initial_binding"]["exact_match"]:
            if initial_checkpoint is not None:
                raise ValueError("M13 initial parameters differ from trained M9; no updates allowed")
            raise ValueError("M9 initial parameters differ from the original M4 start; no updates allowed")
    elif args.m9_initial_run or args.m9_initial_run_sha256:
        raise ValueError("M9 initial binding requires its resource guards")
    parameter_names = {id(parameter): name for name, parameter in model.named_parameters()}
    group_names = {
        "backbone": {parameter_names[id(parameter)] for parameter in backbone_parameters},
        "head": {parameter_names[id(parameter)] for parameter in head_parameters},
    }
    representatives = {}
    for group, module in (("backbone", model.backbone), ("head", model.head)):
        parameter = next(module.parameters())
        representatives[group] = (parameter_names[id(parameter)], parameter.detach().cpu().clone())
    record["base_model"] = {
        "model_id": model.model_id, "revision": model.revision,
        "resolved_revision": model.resolved_revision, "architecture": args.architecture,
        "tokenizer_revision": model.revision, "max_length": model.max_length,
        "temperature": model.temperature,
        "head_initialization": "pretrained" if loaded_head_hashes is not None else "random",
        "baseline": ("trained M9 checkpoint with retained trained ranking head and fresh AdamW"
                     if initial_checkpoint is not None else
                     "pretrained backbone with retained pretrained ranking head"
                     if loaded_head_hashes is not None else
                     "pretrained backbone with explicitly reset randomly initialized linear scoring head"),
    }
    if initial_checkpoint is not None:
        record["base_model"]["initialization"] = {
            "kind": "trained_checkpoint", "source": "actual M9 trained twelve-epoch endpoint",
            "checkpoint_path": str(Path(initial_checkpoint).resolve()),
            "checkpoint_config_sha256": initial_checkpoint_sha256,
            "reference_stage": "weights.after", "optimizer_state": "fresh; not resumed",
        }
    record["optimizer"] = {
        "name": "AdamW", "backbone_learning_rate": args.learning_rate,
        "head_learning_rate": args.head_learning_rate, "weight_decay": 0.01,
        "betas": [0.9, 0.999], "eps": 1e-8, "full_backbone_finetuning": True,
        "backbone_parameter_count": sum(p.numel() for p in backbone_parameters),
        "head_parameter_count": sum(p.numel() for p in head_parameters),
    }
    record["metrics"] = {"validation_before": evaluate(torch, model, rows["validation"], args.batch_size, device, guards)}
    record["weights"] = {"hash_format": "sha256 of canonical contiguous CPU tensor torch.save serialization",
                         "before": baseline_hashes}
    record["training"] = {"steps": 0, "examples_seen": 0, "epochs_completed": 0,
                          "loss_history": [], "epoch_history": [], "stopped_by_max_steps": False}
    baseline_metadata = {
        "stage": "baseline", "run": record,
        "elapsed_seconds_at_checkpoint": time.monotonic() - started,
        "memory_at_checkpoint": memory(torch, device),
    }
    if loaded_head_hashes is not None:
        baseline_head_hashes = parameter_hashes(torch, model.head, guards)
        if model.head_initialization != "pretrained" or baseline_head_hashes != loaded_head_hashes:
            if initial_checkpoint is not None:
                raise ValueError("Retained trained M9 ranking head changed before baseline save")
            raise ValueError("Retained pretrained ranking head changed before baseline save")
        provenance_key = "trained_checkpoint_head_provenance" if initial_checkpoint is not None else "pretrained_head_provenance"
        record["weights"][provenance_key] = {
            "loaded": loaded_head_hashes, "baseline": baseline_head_hashes,
            "unchanged_before_baseline_save": True,
        }
    if guards is not None:
        guards.check("before_baseline_save")
    model.save_checkpoint(output / "baseline", metadata=baseline_metadata)
    if guards is not None:
        guards.check("after_baseline_save")
    optimizer = torch.optim.AdamW(
        [{"params": backbone_parameters, "lr": args.learning_rate},
         {"params": head_parameters, "lr": args.head_learning_rate}],
        weight_decay=0.01, betas=(0.9, 0.999), eps=1e-8,
    )
    training = record["training"]
    for epoch in range(args.epochs):
        order = list(range(len(rows["train"])))
        random.shuffle(order)
        model.train()
        total_loss, count = 0.0, 0
        for offset in range(0, len(order), args.batch_size):
            if guards is not None:
                guards.check("before_training_batch")
            batch = [rows["train"][index] for index in order[offset:offset + args.batch_size]]
            optimizer.zero_grad(set_to_none=True)
            loss, _, _ = batch_loss(torch, model, batch, device)
            loss.backward()
            if guards is not None:
                guards.check("before_optimizer_step")
                guards.first_update()
            optimizer.step()
            if guards is not None:
                guards.check("after_training_batch")
            value = loss.item()
            training["steps"] += 1
            training["examples_seen"] += len(batch)
            total_loss += value * len(batch)
            count += len(batch)
            training["loss_history"].append({"step": training["steps"], "epoch": epoch + 1,
                                             "examples": len(batch), "loss": value})
            if args.max_steps is not None and training["steps"] >= args.max_steps:
                training["stopped_by_max_steps"] = True
                break
        complete = count == len(order)
        training["epochs_completed"] += int(complete)
        training["epoch_history"].append({"epoch": epoch + 1, "complete": complete,
                                          "examples": count, "mean_loss": total_loss / count})
        if training["stopped_by_max_steps"]:
            break

    if device.type == "mps":
        torch.mps.synchronize()
    after_hashes = parameter_hashes(torch, model, guards)
    changed = [name for name in baseline_hashes if baseline_hashes[name] != after_hashes[name]]
    record["weights"].update({"after": after_hashes, "changed_parameter_names": changed,
                               "changed_parameter_count": len(changed)})
    differences = {}
    parameters = dict(model.named_parameters())
    for group, (name, before) in representatives.items():
        after = parameters[name].detach().cpu()
        differences[group] = {
            "name": name, "l2_difference": torch.linalg.vector_norm(after.float() - before.float()).item(),
            "l2_before": torch.linalg.vector_norm(before.float()).item(),
        }
    record["weights"]["representative_differences"] = differences
    record["weights"]["backbone_changed"] = bool(group_names["backbone"].intersection(changed))
    record["weights"]["head_changed"] = bool(group_names["head"].intersection(changed))
    if not record["weights"]["backbone_changed"] or not record["weights"]["head_changed"]:
        raise ValueError("Training did not change both backbone and head; refusing a completed run")
    if any(not math.isfinite(item["l2_difference"]) for item in differences.values()):
        raise ValueError("Nonfinite parameter difference after training")
    record["metrics"]["validation_after"] = evaluate(torch, model, rows["validation"], args.batch_size, device, guards)
    record["runtime"] = {"elapsed_seconds": time.monotonic() - started,
                         "elapsed_scope": "through validation and weight verification, before trained checkpoint save",
                         "memory": memory(torch, device)}
    if guards is not None:
        guards.check("before_trained_save")
    checkpoint_path = output / ("checkpoint.partial" if guards is not None else "checkpoint")
    model.save_checkpoint(checkpoint_path, metadata={"stage": "trained", "run": record})
    if guards is not None:
        guards.check("after_trained_save")
    record["runtime"]["elapsed_seconds"] = time.monotonic() - started
    record["runtime"]["elapsed_scope"] = "through both checkpoint saves, before run.json write"
    record["runtime"]["memory"] = memory(torch, device)
    if guards is not None:
        guards.finish()
        checkpoint_path.rename(output / "checkpoint")
    record["status"] = "completed"
    record["completed_at"] = datetime.now(timezone.utc).isoformat()
    write_json(output / "run.json", record)
    return {"status": "completed", "output_dir": str(output), "run": str(output / "run.json"),
            "baseline": str(output / "baseline"), "checkpoint": str(output / "checkpoint"),
            "steps": training["steps"], "examples_seen": training["examples_seen"],
            "metrics": record["metrics"], "changed_weights": {
                "backbone": record["weights"]["backbone_changed"], "head": record["weights"]["head_changed"]},
            "additional_spend_gbp": 0}


def main(argv=None):
    args = parser().parse_args(argv)
    started = time.monotonic()
    output = Path(args.output_dir).expanduser().absolute()
    try:
        reject_final(output)
        reject_final(output.resolve())
        output.mkdir(parents=True, exist_ok=False)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc), "output_dir": str(output)}))
        return 1
    record = {
        "schema_version": "0.1", "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "config": vars(args).copy(), "argv": list(sys.argv if argv is None else ["jeff.training.train", *argv]),
        "invocation_cwd": str(Path.cwd()), "output_dir": str(output),
        "code": git_identity(Path(__file__).resolve().parent),
        "invocation_cwd_code": git_identity(Path.cwd()),
        "artifacts": {"baseline": "baseline", "checkpoint": "checkpoint", "manifest": "dataset-manifest.json", "run": "run.json"},
        "costs": {"currency": "GBP", "additional_spend": 0,
                  "scope": "Local training process only; no paid jobs or teacher calls. Dataset generation costs and sunk hardware/electricity are excluded."},
        "limitations": ["No calibration claim", "No final-evaluation data used", "Fresh-process checkpoint reload is a separate lead-owned step"],
    }
    guards = None
    try:
        if args.m9_resource_guards:
            from jeff.model.resource_guards import ResourceGuards
            guards = ResourceGuards(output / "m9-resources")
            record["m9_resources"] = {"events": "m9-resources.jsonl",
                                      "summary": "m9-resources.summary.json",
                                      "first_update_marker": "m9-resources.first-update-attempt.json"}
        # Reserve stdout for exactly one machine-readable result, including HF chatter.
        with contextlib.redirect_stdout(sys.stderr):
            summary = train_run(args, output, record, started, guards)
    except (Exception, KeyboardInterrupt) as exc:
        if guards is not None:
            try:
                guards.finish(error=exc)
            except Exception as guard_error:
                record["guard_close_error"] = str(guard_error)
        record.update({"status": "failed", "failed_at": datetime.now(timezone.utc).isoformat(),
                       "elapsed_seconds": time.monotonic() - started,
                       "error_type": type(exc).__name__, "error": str(exc),
                       "traceback": traceback.format_exc()})
        try:
            write_json(output / "failure.json", record)
        except (OSError, ValueError) as write_error:
            print(f"Could not write failure.json: {write_error}", file=sys.stderr)
        summary = {"status": "failed", "output_dir": str(output), "error_type": type(exc).__name__,
                   "error": str(exc), "failure": str(output / "failure.json")}
        print(json.dumps(summary, allow_nan=False))
        return 1
    print(json.dumps(summary, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
