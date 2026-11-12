"""Fixed M6 / explicitly selected M7 lower-LR or M10 seed7 recipe.

M10 requires --experiment m10 on audit/train; no new capacity probe. See
docs/model/m10-seed-replication-plan.md for the bounded owner CLI.

M6 is the unchanged default CLI. M7 requires --experiment m7 on audit/train;
capacity is prohibited for M7. See M7.md beside this module for the exact owner
commands, historical capacity reuse and observation-only fields.

python -m jeff.training.qwen_decision audit --output-dir /absolute/NEW-audit
python -m jeff.training.qwen_decision capacity --audit-dir /absolute/AUDIT \
    --output-dir /absolute/NEW-capacity
python -m jeff.training.qwen_decision train --audit-dir /absolute/AUDIT \
    --capacity-receipt /absolute/CAPACITY/receipt.json \
    --authorize-run M6-1500-375-seed42 --comparison-freeze-sha256 OWNER_FROZEN_SHA256 \
    --output-dir /absolute/NEW-run

No downloads, held-out reads, retries, resume, generation or recipe search. Audit
loads only a tokenizer. Capacity performs ONE disposable optimizer step, then
four additional backwards with resident moments, never a second step. Its
conservative longest-row projection is an estimate, not a deadline guarantee.
Owner must freeze baseline comparison/tolerances separately and supply its hash;
this module does not read those outcomes. Owner enforces external 600/2700-second
process deadlines (including preflight/save). Cooperative guards cannot interrupt
a blocked native operation. SIGTERM/interrupt writes a failed receipt; SIGKILL or
host failure leaves failure-receipt.json plus flushed events, never a manifest.
Output directories must not exist. Receipts and schedules contain TRAIN labels;
only checkpoint/ and checkpoint-manifest.json are the Runtime handoff.
"""

import argparse
from contextlib import contextmanager
import hashlib
import inspect
import json
from pathlib import Path
import random
import resource
import shutil
import signal
import sys
import time

from jeff.runtime import qwen_challenger as p3
from jeff.training import qwen_data as data
from jeff.training import qwen_seed as seed

require = p3.require
AUTHORIZATION = "M6-1500-375-seed42"
M7_AUTHORIZATION = "M7-ONE-original-P3-LR2e-6-1500-375-seed42"


def rss_bytes():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return rss if sys.platform == "darwin" else rss * 1024


class Monitor:
    def __init__(self, directory, receipt, start, seconds, experiment="m6"):
        self.receipt, self.start, self.seconds = receipt, start, seconds
        self.torch = None
        self.experiment = experiment
        self.cfg = data.recipe(experiment)
        self.events = (directory / "events.jsonl").open("x")

    def sample(self, stage, duration=None):
        sample = {"stage": stage, "elapsed_seconds": time.monotonic() - self.start,
                  "cpu_lifetime_rss_bytes": rss_bytes(), "duration_seconds": duration}
        if self.torch is not None and self.torch.backends.mps.is_available():
            mps = self.torch.mps
            sample.update(mps_current_bytes=mps.current_allocated_memory(),
                          mps_driver_bytes=mps.driver_allocated_memory())
            recommended = getattr(mps, "recommended_max_memory", None)
            if recommended is not None:
                sample["mps_recommended_max_bytes"] = recommended()
                sample["mps_recommended_headroom_bytes"] = (
                    sample["mps_recommended_max_bytes"] - sample["mps_driver_bytes"])
        self.receipt["memory_samples"].append(sample)
        self.events.write(data.json_line({"sample": sample,
            "presentations": self.receipt.get("presentations", 0),
            "optimizer_steps": self.receipt.get("optimizer_steps", 0),
            "extra_backwards": self.receipt.get("extra_backwards", 0)}))
        self.events.flush()
        return sample

    def guard(self, stage):
        s = self.sample(stage)
        require(s["elapsed_seconds"] < self.seconds, "total process deadline exceeded")
        require(s["cpu_lifetime_rss_bytes"] <= self.cfg["max_cpu_rss_bytes"], "CPU RSS guard exceeded")
        if "mps_driver_bytes" in s:
            require(s["mps_driver_bytes"] <= self.cfg["max_mps_driver_bytes"], "MPS driver guard exceeded")
        if "mps_recommended_headroom_bytes" in s:
            require(s["mps_recommended_headroom_bytes"] >= self.cfg["min_recommended_headroom_bytes"],
                    "MPS recommended working-set headroom guard exceeded")

    @contextmanager
    def phase(self, name):
        self.guard(name + ":before")
        start = time.monotonic()
        try:
            yield
            if self.torch is not None:
                self.torch.mps.synchronize()
        finally:
            duration = time.monotonic() - start
            self.receipt["phase_seconds"].setdefault(name, []).append(duration)
            self.sample(name + ":after", duration)
        self.guard(name + ":guard")

    def progress(self, **values):
        record = {"elapsed_seconds": time.monotonic() - self.start, **values}
        self.events.write(data.json_line({"progress": record}))
        self.events.flush()
        print(json.dumps(record, allow_nan=False), flush=True)


def load_model(monitor, receipt):
    import torch
    from transformers import AutoModelForCausalLM

    data.runtime_environment()
    require(torch.backends.mps.is_available(), "MPS required; no fallback")
    torch.set_num_threads(4)
    rng_seed = monitor.cfg["seed"]
    random.seed(rng_seed)
    torch.manual_seed(rng_seed)
    torch.mps.manual_seed(rng_seed)
    monitor.torch = torch
    receipt["fresh_start"] = {"seed": rng_seed, "base_model_id": p3.MODEL,
        "base_revision": p3.REVISION, "model_dir": str(data.MODEL_DIR),
        "base_weight_sha256": receipt["identity"]["evidence"]["model_assets"]["model.safetensors"],
        "optimizer_state": "new empty AdamW; capacity state never reused",
        "rng": f"fresh process; random.seed/torch.manual_seed/torch.mps.manual_seed({rng_seed})"}
    with monitor.phase("load"):
        model, info = AutoModelForCausalLM.from_pretrained(
            str(data.MODEL_DIR), local_files_only=True, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32, attn_implementation="sdpa",
            output_loading_info=True, ignore_mismatched_sizes=False)
        require(not any(info.get(k) for k in ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")),
                "base model did not load exactly")
        require("logits_to_keep" in inspect.signature(model.forward).parameters,
                "last-token-only projection required")
        model.config.use_cache = False
        model.to("mps")
        model.eval()
        parameters = list(model.parameters())
        require(parameters and len({id(p) for p in parameters}) == len(parameters),
                "optimizer must receive all unique parameters exactly once")
        require(all(p.dtype == torch.float32 and p.device.type == "mps" and p.requires_grad
                    for p in parameters), "all parameters must be trainable FP32 on MPS")
        require(all(not b.is_floating_point() or b.dtype == torch.float32 for b in model.buffers()),
                "floating buffers must be FP32")
    count = sum(p.numel() for p in parameters)
    receipt["parameters"] = {"unique_tensors": len(parameters), "total": count,
        "trainable": count, "dtype": "float32", "theoretical_bytes": {
            "weights": count * 4, "gradients": count * 4,
            "adam_first_moment": count * 4, "adam_second_moment": count * 4,
            "weights_gradients_moments": count * 16}}
    return torch, model, parameters


def optimizer_for(torch, parameters, cfg):
    return torch.optim.AdamW(parameters, lr=cfg["learning_rate"], betas=tuple(cfg["betas"]),
        eps=cfg["epsilon"], weight_decay=cfg["weight_decay"], foreach=False)


def decision_loss(torch, model, row):
    ids = torch.tensor([row["prompt_tokens"]], dtype=torch.long, device="mps")
    output = model(input_ids=ids, attention_mask=torch.ones_like(ids),
                   use_cache=False, logits_to_keep=1)
    require(tuple(output.logits.shape[:2]) == (1, 1), "unexpected logits shape")
    logits = output.logits[0, 0, row["answer_ids"]].float()
    require(bool(torch.isfinite(logits).all().item()), "nonfinite allowed-symbol logits")
    target = torch.tensor([row["target_position"]], dtype=torch.long, device="mps")
    loss = torch.nn.functional.cross_entropy(logits.unsqueeze(0), target)
    require(bool(torch.isfinite(loss).item()), "nonfinite grouped CE")
    return loss, logits


def clip(torch, parameters):
    require(all(p.grad is not None for p in parameters), "missing gradient on trainable parameter")
    norm = torch.nn.utils.clip_grad_norm_(parameters, 1.0, error_if_nonfinite=True, foreach=False)
    value = float(norm.item())
    require(value > 0 and bool(torch.isfinite(norm).item()), "nonfinite or zero gradient norm")
    return value


def moment_evidence(torch, optimizer, parameters, expected_step=1):
    require(len(optimizer.state) == len(parameters), "incomplete Adam moments")
    total = 0
    for p in parameters:
        state = optimizer.state[p]
        require(set(state) == {"step", "exp_avg", "exp_avg_sq"}, "unexpected Adam state")
        require(float(state["step"].item()) == expected_step, "unexpected per-parameter Adam step count")
        for key in ("exp_avg", "exp_avg_sq"):
            value = state[key]
            require(value.dtype == torch.float32 and value.device.type == "mps" and
                    value.shape == p.shape, "unexpected Adam moment storage")
            total += value.numel() * value.element_size()
    return {"state_tensors": len(optimizer.state), "moment_bytes": total, "step": expected_step}


def fit(torch, model, schedule, path, monitor, label):
    was_training = model.training
    model.eval()
    stats = {"overall": {}, "by_family": {}, "by_source_group": {}}

    def add(bucket, ce, predicted, target):
        bucket["rows"] = bucket.get("rows", 0) + 1
        bucket["ce_sum"] = bucket.get("ce_sum", 0.0) + ce
        bucket["agreements"] = bucket.get("agreements", 0) + int(predicted == target)
        for key, pos in (("predicted_position_counts", predicted), ("target_position_counts", target)):
            counts = bucket.setdefault(key, {})
            counts[str(pos)] = counts.get(str(pos), 0) + 1

    try:
        with path.open("x") as stream, torch.no_grad():
            for index, row in enumerate(schedule):
                with monitor.phase(label + ":forward"):
                    loss, logits = decision_loss(torch, model, row)
                    ce, predicted = float(loss.item()), int(logits.argmax().item())
                result = {"index": row["index"], "id": row["id"], "ce": ce,
                    "agreement": predicted == row["target_position"], "predicted_position": predicted,
                    "target_position": row["target_position"], "option_ids": row["option_ids"],
                    "family": row["family"], "source": row["provenance"]["source"],
                    "group_id": row["group_id"]}
                if monitor.experiment in {"m7", "m10"}:
                    result.update(fit_observations(torch, logits, row))
                stream.write(data.json_line(result))
                stream.flush()
                add(stats["overall"], ce, predicted, row["target_position"])
                add(stats["by_family"].setdefault(row["family"], {}), ce, predicted, row["target_position"])
                group = json.dumps([row["provenance"]["source"], row["group_id"]])
                add(stats["by_source_group"].setdefault(group, {}), ce, predicted, row["target_position"])
                del loss, logits
                if (index + 1) % 100 == 0:
                    monitor.progress(phase=label, fit_rows=index + 1)
        for bucket in [stats["overall"], *stats["by_family"].values(), *stats["by_source_group"].values()]:
            bucket["mean_ce"] = bucket["ce_sum"] / bucket["rows"]
            bucket["agreement"] = bucket["agreements"] / bucket["rows"]
        require(stats["overall"]["rows"] == 1500, "incomplete TRAIN fit")
    finally:
        model.train(was_training)
        path.chmod(0o444)
    return {"mode": "eval; torch.no_grad (not inference_mode)", "rows_sha256": p3.digest(path),
            "path": str(path), **stats}


def fit_observations(torch, logits, row):
    # Called inside the existing no_grad fit; no extra forward, scan or objective.
    probabilities = torch.softmax(logits, dim=0)
    require(bool(torch.isfinite(probabilities).all().item()) and
            bool(((probabilities >= 0) & (probabilities <= 1)).all().item()) and
            abs(float(probabilities.sum().item()) - 1.0) <= 1e-6,
            "invalid conditional allowed-answer probabilities")
    raw = logits.tolist()
    probs = probabilities.tolist()
    top_probability, top_logit = max(probs), max(raw)
    top_positions = [i for i, p in enumerate(probs) if p == top_probability]
    logit_positions = [i for i, value in enumerate(raw) if value == top_logit]
    ordered = sorted(probs, reverse=True)
    return {"allowed_answer_ids": row["answer_ids"], "allowed_logits": raw,
        "conditional_probabilities": probs, "option_count": len(probs),
        "target_id": row["target_id"], "probability_top_positions": top_positions,
        "probability_top_option_ids": [row["option_ids"][i] for i in top_positions],
        "top_probability": top_probability, "top_logit": top_logit,
        "logit_top_positions": logit_positions, "probability_top_tie_count": len(top_positions),
        "logit_top_tie_count": len(logit_positions),
        "top_two_probability_margin": ordered[0] - ordered[1]}


def fingerprints(model):
    candidates = [(name, p) for name, p in model.named_parameters() if 2 <= p.numel() <= 8192]
    require(candidates, "no bounded parameter fingerprint candidates")
    selected = [candidates[0], candidates[len(candidates) // 2], candidates[-1]]
    return {name: hashlib.sha256(p.detach().cpu().contiguous().numpy().tobytes()).hexdigest()
            for name, p in selected}


def capacity(args, receipt, monitor, schedule):
    require(monitor.experiment == "m6", "M7/M10 capacity prohibited; no new learning probe")
    cfg = receipt["identity"]["evidence"]["recipe"]
    longest = sorted(schedule, key=lambda r: (-r["input_tokens"], r["index"]))[:4]
    receipt["capacity_rows"] = [{"id": r["id"], "index": r["index"], "input_tokens": r["input_tokens"]}
                                for r in longest]
    require(longest[0]["input_tokens"] == max(r["input_tokens"] for r in schedule),
            "capacity must exercise actual longest audited prompt")
    torch, model, parameters = load_model(monitor, receipt)
    with monitor.phase("optimizer_create"):
        optimizer = optimizer_for(torch, parameters, cfg)
    receipt["capacity_eval_seconds"] = []
    with torch.no_grad():
        for row in longest:
            with monitor.phase("capacity_eval"):
                loss, logits = decision_loss(torch, model, row)
                del loss, logits
            receipt["capacity_eval_seconds"].append(receipt["phase_seconds"]["capacity_eval"][-1])
    model.train()
    optimizer.zero_grad(set_to_none=True)
    for row in longest:
        with monitor.phase("capacity_forward"):
            loss, logits = decision_loss(torch, model, row)
            del logits
        with monitor.phase("capacity_backward"):
            (loss / 4).backward()
            del loss
        receipt["presentations"] += 1
    with monitor.phase("capacity_clip"):
        receipt["gradient_norm"] = clip(torch, parameters)
    with monitor.phase("capacity_optimizer_step"):
        optimizer.step()
        receipt["optimizer_steps"] += 1
    with monitor.phase("capacity_moments"):
        receipt["adam_allocation"] = moment_evidence(torch, optimizer, parameters)
    optimizer.zero_grad(set_to_none=True)
    for row in longest:
        with monitor.phase("steady_forward"):
            loss, logits = decision_loss(torch, model, row)
            del logits
        with monitor.phase("steady_backward"):
            (loss / 4).backward()
            del loss
        receipt["extra_backwards"] += 1
    # Clip only once per actual update; check the extra accumulated gradients without a second clip/step.
    with monitor.phase("steady_gradient_check"):
        require(all(p.grad is not None for p in parameters), "missing steady-state gradients")
        norms = torch.stack([torch.linalg.vector_norm(p.grad.detach()) for p in parameters])
        norm = torch.linalg.vector_norm(norms)
        require(bool(torch.isfinite(norm).item()) and float(norm.item()) > 0,
                "nonfinite or zero steady-state gradient norm")
        receipt["steady_gradient_norm"] = float(norm.item())
        del norms, norm
    require(receipt["optimizer_steps"] == 1 and receipt["extra_backwards"] == 4,
            "capacity authorization exceeded")
    phases = receipt["phase_seconds"]
    first_update = sum(sum(phases[k]) for k in ("capacity_forward", "capacity_backward",
                                               "capacity_clip", "capacity_optimizer_step"))
    steady_update = sum(sum(phases[k]) for k in ("steady_forward", "steady_backward")) + sum(
        sum(phases[k]) for k in ("capacity_clip", "capacity_optimizer_step"))
    fit_estimate = 3000 * max(receipt["capacity_eval_seconds"])
    elapsed = time.monotonic() - monitor.start
    estimate = elapsed + 375 * max(first_update, steady_update) + fit_estimate + 120
    receipt["projection"] = {"estimated_total_seconds": estimate, "within_cap": estimate < 2700,
        "method": "capacity elapsed + 375 * slower longest-four update + 3000 * slowest eval + 120s save allowance",
        "first_update_seconds": first_update, "steady_update_seconds": steady_update,
        "before_after_fit_seconds": fit_estimate, "save_allowance_seconds": 120,
        "qualification": "longest-input conservative extrapolation, not measured full-run time or a guarantee"}
    receipt["disposition"] = "all model/optimizer/RNG state discarded on process exit; no weights saved"
    require(estimate < 2700, "capacity projection exceeds full-process 2700s cap")
    monitor.guard("capacity_complete")


@contextmanager
def gradient_stream(directory, experiment):
    if experiment in {"m7", "m10"}:
        with (directory / "gradient-norms.jsonl").open("x") as stream:
            yield stream
    else:
        yield None


def train(args, receipt, monitor, schedule, directory):
    authorization = {"m6": AUTHORIZATION, "m7": M7_AUTHORIZATION,
                     "m10": seed.AUTHORIZATION}[args.experiment]
    require(args.authorize_run == authorization, "explicit single-run authorization required")
    require(len(args.comparison_freeze_sha256) == 64 and
            all(c in "0123456789abcdef" for c in args.comparison_freeze_sha256),
            "owner's pre-outcome comparison freeze SHA256 required")
    receipt["comparison_freeze_sha256"] = args.comparison_freeze_sha256
    if args.experiment == "m7":
        receipt["authorization"] = M7_AUTHORIZATION
        receipt["treatment"] = "original P3; only AdamW LR 2e-5 -> 2e-6; no correctness repair"
    if args.experiment == "m10":
        receipt["authorization"] = seed.AUTHORIZATION
        receipt["treatment"] = "original P3; M7 full-parameter replication; only seed42 -> seed7"
    capacity_path = data.safe_path(args.capacity_receipt)
    if args.experiment == "m10":
        receipt["capacity_reuse"] = seed.reuse_m7_capacity(capacity_path, receipt["identity"], schedule)
    elif args.experiment == "m7":
        receipt["capacity_reuse"] = data.reuse_m6_capacity(capacity_path, receipt["identity"], schedule)
    else:
        capacity_receipt = data.read_json(capacity_path)
        require(capacity_receipt.get("schema_version") == "m6.capacity.v1" and
                capacity_receipt.get("status") == "complete" and
                capacity_receipt.get("identity") == receipt["identity"] and
                capacity_receipt.get("presentations") == 4 and
                capacity_receipt.get("optimizer_steps") == 1 and
                capacity_receipt.get("extra_backwards") == 4 and
                capacity_receipt.get("projection", {}).get("within_cap") is True,
                "successful matching capacity receipt required; no bypass")
    receipt["capacity_receipt"] = {"path": str(capacity_path), "sha256": p3.digest(capacity_path)}
    torch, model, parameters = load_model(monitor, receipt)
    receipt["initial_parameter_fingerprints"] = fingerprints(model)
    receipt["fit_before"] = fit(torch, model, schedule, directory / "fit-before.jsonl", monitor, "fit_before")
    with monitor.phase("optimizer_create"):
        optimizer = optimizer_for(torch, parameters, monitor.cfg)
    model.train()
    optimizer.zero_grad(set_to_none=True)
    online_sum = 0.0
    with (directory / "online.jsonl").open("x") as stream, gradient_stream(directory, args.experiment) as norms:
        for index, row in enumerate(schedule):
            with monitor.phase("train_forward"):
                loss, logits = decision_loss(torch, model, row)
                ce = float(loss.item())
                del logits
            with monitor.phase("train_backward"):
                (loss / 4).backward()
                del loss
            receipt["presentations"] += 1
            online_sum += ce
            stream.write(data.json_line({"index": row["index"], "id": row["id"], "ce": ce,
                "update": index // 4 + 1, "qualification": "online changing-weight descriptive loss"}))
            stream.flush()
            if (index + 1) % 4 == 0:
                with monitor.phase("train_clip"):
                    norm = clip(torch, parameters)
                if norms is not None:
                    norms.write(data.json_line({"update": index // 4 + 1,
                        "presentations": receipt["presentations"], "preclip_norm": norm}))
                    norms.flush()
                with monitor.phase("train_optimizer_step"):
                    if args.experiment == "m10" and receipt["optimizer_steps"] == 0:
                        seed.first_update_attempt(directory, receipt)
                    optimizer.step()
                    receipt["optimizer_steps"] += 1
                optimizer.zero_grad(set_to_none=True)
                if receipt["optimizer_steps"] % 25 == 0:
                    monitor.progress(phase="train", updates=receipt["optimizer_steps"],
                        presentations=receipt["presentations"], last_preclip_norm=norm,
                        online_mean_ce=online_sum / receipt["presentations"])
            monitor.guard("train_row_complete")
    (directory / "online.jsonl").chmod(0o444)
    require(receipt["presentations"] == 1500 and receipt["optimizer_steps"] == 375,
            "training coverage/update count mismatch")
    with monitor.phase("final_optimizer_state"):
        receipt["adam_final_state"] = moment_evidence(torch, optimizer, parameters, expected_step=375)
    if args.experiment in {"m7", "m10"}:
        norms_path = directory / "gradient-norms.jsonl"
        norms_path.chmod(0o444)
        receipt["gradient_norms"] = {"path": str(norms_path), "sha256": p3.digest(norms_path),
            "values": receipt["optimizer_steps"], "meaning": "already-computed preclip norm, once per update"}
    receipt["online_mean_ce"] = online_sum / 1500
    receipt["online_rows_sha256"] = p3.digest(directory / "online.jsonl")
    receipt["final_parameter_fingerprints"] = fingerprints(model)
    require(receipt["initial_parameter_fingerprints"] != receipt["final_parameter_fingerprints"],
            "selected parameter fingerprints did not change")
    require(all(p.requires_grad and p.dtype == torch.float32 for p in parameters),
            "parameter training state changed")
    # Free optimizer state only after the last update; fit never mutates it or uses inference tensors.
    del optimizer
    receipt["fit_after"] = fit(torch, model, schedule, directory / "fit-after.jsonl", monitor, "fit_after")
    checkpoint = directory / "checkpoint"
    checkpoint.mkdir(exist_ok=False)
    with monitor.phase("save_checkpoint"):
        model.save_pretrained(str(checkpoint), safe_serialization=True, max_shard_size="5GB")
        tokenizer_assets = receipt["identity"]["evidence"]["tokenizer_assets"]
        for name in tokenizer_assets:
            require(not (checkpoint / name).exists(), "refusing tokenizer overwrite")
            shutil.copyfile(data.MODEL_DIR / name, checkpoint / name)
            require(p3.digest(checkpoint / name) == tokenizer_assets[name], "tokenizer byte-copy mismatch")
        for name in ("LICENSE", "LICENSE.txt", "README.md"):
            if name in receipt["identity"]["evidence"]["model_assets"]:
                require(not (checkpoint / name).exists(), "refusing asset overwrite")
                shutil.copyfile(data.MODEL_DIR / name, checkpoint / name)
        inventory = {str(p.relative_to(checkpoint)): {"sha256": p3.digest(p), "bytes": p.stat().st_size}
                     for p in sorted(checkpoint.rglob("*")) if p.is_file()}
        require("model.safetensors" in inventory, "expected single safe FP32 weight file")
        require(inventory["model.safetensors"]["sha256"] != receipt["fresh_start"]["base_weight_sha256"],
                "saved weight file unchanged")
        for path in checkpoint.rglob("*"):
            if path.is_file():
                path.chmod(0o444)
        checkpoint.chmod(0o555)
    receipt["checkpoint_files"] = inventory
    receipt["tokenizer_assets"] = tokenizer_assets
    if args.experiment == "m10":
        require(data.source_binding(data.source_identity("m10"), "m10") ==
                data.source_binding(receipt["identity"]["evidence"]["source"], "m10"),
                "scientific source changed during run")
    else:
        require(data.source_identity() == receipt["identity"]["evidence"]["source"], "source changed during run")
    monitor.guard("train_complete")


def checkpoint_manifest(directory, receipt):
    identity = receipt["identity"]
    proof = identity["evidence"]
    producer = directory.name if receipt["schema_version"] == "m6.train.v1" else (
        directory.parent.name + "/" + directory.name)
    return {"schema_version": "jeff.qwen-trained-checkpoint.v1", "status": "complete", "kind": "trained",
        "checkpoint_id": producer + "-checkpoint", "run_id": producer,
        "base_model_id": p3.MODEL, "base_revision": p3.REVISION,
        "training_code_revision": proof["source"]["revision"],
        "training_data_manifest_sha256": data.MANIFEST_HASH,
        "training_recipe_sha256": proof["recipe_sha256"],
        "training_schedule_sha256": identity["schedule_sha256"],
        "p3_scoring_config_sha256": data.P3_HASH,
        "tokenizer_assets": receipt["tokenizer_assets"], "files": receipt["checkpoint_files"],
        "source_run_receipt": {"path": str(directory / "receipt.json"),
                               "sha256": p3.digest(directory / "receipt.json")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    audit_parser = commands.add_parser("audit")
    capacity_parser = commands.add_parser("capacity")
    train_parser = commands.add_parser("train")
    for cmd in (audit_parser, capacity_parser, train_parser):
        cmd.add_argument("--output-dir", type=Path, required=True)
        cmd.add_argument("--experiment", choices=("m6", "m7", "m10"), default="m6")
    for cmd in (capacity_parser, train_parser):
        cmd.add_argument("--audit-dir", type=Path, required=True)
    train_parser.add_argument("--capacity-receipt", type=Path, required=True)
    train_parser.add_argument("--authorize-run", required=True)
    train_parser.add_argument("--comparison-freeze-sha256", required=True)
    args = parser.parse_args()
    require(not (args.experiment in {"m7", "m10"} and args.command == "capacity"),
            "M7/M10 capacity command prohibited; reuse pinned historical evidence")
    if args.experiment in {"m7", "m10"} and args.command == "train":
        authorization = M7_AUTHORIZATION if args.experiment == "m7" else seed.AUTHORIZATION
        require(args.authorize_run == authorization, "explicit experiment single-run authorization required")
    start = time.monotonic()
    directory = args.output_dir.expanduser().resolve()
    require(not any("final" in part.lower() for part in directory.parts), "final output path forbidden")
    directory.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": f"{args.experiment}.{args.command}.v1", "command": args.command,
        "status": "failed", "output_dir": str(directory), "memory_samples": [], "phase_seconds": {},
        "presentations": 0, "optimizer_steps": 0, "extra_backwards": 0,
        "memory_qualification": "observed MPS samples, NOT peaks; CPU lifetime RSS; never sum CPU and MPS",
        "external_deadline_required": True}
    p3.save(directory / "failure-receipt.json", {**receipt,
        "error": "incomplete unless a completed receipt.json/audit.json exists; inspect events.jsonl for hard termination"})
    monitor = None
    exit_code = 0
    old_term = signal.getsignal(signal.SIGTERM)

    def terminated(signum, frame):
        raise TimeoutError("external SIGTERM deadline")

    signal.signal(signal.SIGTERM, terminated)
    try:
        cfg = data.recipe(args.experiment)
        seconds = cfg["maximum_capacity_seconds"] if args.command == "capacity" else cfg["maximum_run_seconds"]
        monitor = Monitor(directory, receipt, start, seconds, args.experiment)
        with monitor.phase("revalidation"):
            if args.command == "audit":
                proof, schedule = data.evidence(monitor.guard, args.experiment)
                text = data.schedule_text(schedule)
                with (directory / "schedule.jsonl").open("x") as stream:
                    stream.write(text)
                (directory / "schedule.jsonl").chmod(0o444)
                receipt.update(evidence=proof, schedule_sha256=p3.text_hash(text))
            else:
                identity, schedule = data.revalidate(args.audit_dir.resolve(), monitor.guard, args.experiment)
                receipt["identity"] = identity
        if args.command == "capacity":
            capacity(args, receipt, monitor, schedule)
        elif args.command == "train":
            train(args, receipt, monitor, schedule, directory)
        monitor.guard("process_complete")
        receipt["status"] = "complete"
    except BaseException as exc:
        receipt["status"] = "failed"
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:2000], "retry": False}
        exit_code = 1
    finally:
        signal.signal(signal.SIGTERM, old_term)
        if monitor is not None:
            try:
                monitor.sample("process_end")
            except Exception as exc:
                receipt["end_memory_sample_error"] = type(exc).__name__
            monitor.events.close()
        receipt["process_runtime_seconds"] = time.monotonic() - start
        receipt["cpu_lifetime_rss_bytes"] = rss_bytes()
        receipt_path = directory / ("audit.json" if args.command == "audit" else "receipt.json")
        p3.save(receipt_path, receipt)
        if args.command == "train" and receipt["status"] == "complete":
            p3.save(directory / "checkpoint-manifest.json", checkpoint_manifest(directory, receipt))
        for path in directory.iterdir():
            if path.is_file():
                path.chmod(0o444)
        directory.chmod(0o555)
    print(json.dumps({"status": receipt["status"], "receipt": str(receipt_path),
                      "seconds": receipt["process_runtime_seconds"]}), flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
