"""M8/M12: fresh-process audit/train; no capacity command or probe.

Owner must supervise the entire process and enforce the remaining aggregate
budget (M8: 2700s; M12: 590s), including audits/failed attempts. See M8.md. Importing
this module does not import torch/transformers or load model/tokenizer assets.
"""

import argparse
import copy
import inspect
import json
import math
import os
from pathlib import Path
import random
import shutil
import signal
import struct
import time

from jeff.model import qwen_readout_proof as proof
from jeff.training import qwen_data as data
from jeff.training import qwen_decision as legacy
from jeff.training import qwen_head_lr as head_lr

p3 = data.p3
require = p3.require
AUTHORIZATION = "M8-ONE-original-P3-frozen-six-row-1500-375-seed42"
M7_RUN = data.ARTIFACTS / "model/m7-qwen-low-lr-20261111-01"
M7_PREFIT = M7_RUN / "training/fit-before.jsonl"
M7_PREFIT_SHA = "4940b17902562c8da5cf34e80eaa3618fa5ab52c20ad90715fd6dc6d3c9d12d5"
M7_RECEIPT_SHA = "c78ad96769b76c2cabb7c2b0ec87dde13bca78e2f7e2256a51b6ca545b54e156"
LOGIT_TOLERANCE = 1e-4
PROBABILITY_TOLERANCE = 1e-6


def save_status(directory, receipt):
    # A durable pre-step ATTEMPT survives a failed/partial native optimizer call.
    path = directory / "status.json"
    temporary = directory / "status.json.tmp"
    with temporary.open("w") as stream:
        status = {k: receipt[k] for k in (
            "status", "presentations", "optimizer_steps", "optimizer_step_attempts")}
        if "backbone_forwards" in receipt:
            status["backbone_forwards"] = receipt["backbone_forwards"]
        stream.write(data.json_line(status))
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def pinned_prefit(receipt, schedule):
    historical = data.pinned_json(M7_RUN / "training/receipt.json", M7_RECEIPT_SHA)
    require(historical["schema_version"] == "m7.train.v1" and
            historical["status"] == "complete" and historical["optimizer_steps"] == 375 and
            historical["presentations"] == 1500 and
            historical["identity"]["schedule_sha256"] == data.M6_SCHEDULE_SHA and
            historical["fit_before"]["rows_sha256"] == M7_PREFIT_SHA and
            historical["fit_before"]["overall"]["rows"] == 1500,
            "wrong M7 original-base prefit receipt")
    require(p3.digest(data.safe_path(M7_PREFIT)) == M7_PREFIT_SHA, "M7 prefit changed")
    rows = [data.strict_json(line) for line in M7_PREFIT.read_bytes().splitlines()]
    require(len(rows) == len(schedule) == 1500, "M7 prefit coverage")
    for row, expected in zip(rows, schedule):
        require(row["id"] == expected["id"] and row["index"] == expected["index"] and
                row["option_ids"] == expected["option_ids"] and
                row["target_id"] == expected["target_id"] and
                row["allowed_answer_ids"] == expected["answer_ids"] and
                row["target_position"] == expected["target_position"], "M7 prefit identity mismatch")
    current = receipt["identity"]["evidence"]
    previous = historical["identity"]["evidence"]
    excluded = {"source", "recipe", "recipe_path", "recipe_sha256"}
    require({k: v for k, v in current.items() if k not in excluded} ==
            {k: v for k, v in previous.items() if k not in excluded},
            "M7 prefit original base/tokenizer/data/runtime identity changed")
    receipt["starting_control_source"] = {
        "path": str(M7_PREFIT), "sha256": M7_PREFIT_SHA,
        "receipt": {"path": str(M7_RUN / "training/receipt.json"), "sha256": M7_RECEIPT_SHA},
        "source": previous["source"], "schedule_sha256": data.M6_SCHEDULE_SHA,
        "scope": "1500 original-P3 TRAIN prefit rows; not M7 learned weights"}
    return rows


def capacity_reuse(identity, schedule):
    # Reuse the existing strict source/shape checks, not their full-parameter claim.
    comparable = copy.deepcopy(identity)
    comparable["evidence"]["recipe"]["schema_version"] = "m7.recipe.v1"
    record = data.reuse_m6_capacity((data.M6_RUN / "capacity/receipt.json").resolve(),
                                  comparable, schedule)
    record["historical_full_parameter_projection"] = record.pop("projection")
    record["basis"] = "historical original-base source/shape evidence only; no new capacity probe"
    record["adaptation_scope_changed"] = True
    record["current_trainable_scalars"] = proof.HEAD_PARAMETERS
    record["export_peak_and_projection_verified"] = False
    record["qualification"] = ("M6 trained all original parameters; M8 freezes them. Historical "
        "full-parameter optimizer/projection semantics and export memory are not established for M8.")
    return record


def ordered_answers(schedule):
    ids = next(row["answer_ids"] for row in schedule if len(row["answer_ids"]) == 6)
    require(len(set(ids)) == 6 and all(type(i) is int and 0 <= i < proof.VOCAB_SIZE for i in ids),
            "invalid ordered six answer token IDs")
    require(all(2 <= len(row["answer_ids"]) <= 6 and
                row["answer_ids"] == ids[:len(row["answer_ids"])] for row in schedule),
            "actual K mapping must be the pinned A-F prefix")
    return list(ids)


def load_frozen_model(monitor, receipt):
    import torch
    from transformers import AutoModelForCausalLM

    data.runtime_environment()
    require(torch.backends.mps.is_available(), "MPS required; no fallback")
    torch.set_num_threads(4)
    random.seed(42)
    torch.manual_seed(42)
    torch.mps.manual_seed(42)
    monitor.torch = torch
    receipt["fresh_start"] = {"seed": 42, "base_model_id": p3.MODEL,
        "base_revision": p3.REVISION, "model_dir": str(data.MODEL_DIR),
        "base_weight_sha256": receipt["identity"]["evidence"]["model_assets"]["model.safetensors"],
        "optimizer_state": "new empty AdamW; no historical optimizer/model state reused",
        "rng": "fresh process; random.seed/torch.manual_seed/torch.mps.manual_seed(42)"}
    with monitor.phase("load_original_tied_base"):
        model, info = AutoModelForCausalLM.from_pretrained(
            str(data.MODEL_DIR), local_files_only=True, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32, attn_implementation="sdpa",
            output_loading_info=True, ignore_mismatched_sizes=False)
        require(all(k in info and not info[k] for k in
                ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")),
                "original tied P3 must load with zero diagnostics")
        receipt["base_loading_info"] = info
        require("logits_to_keep" in inspect.signature(model.forward).parameters,
                "stock last-token projection support required")
        model.config.use_cache = False
        model.to("mps")
        model.eval()
        original = list(model.parameters())
        require(original and sum(p.numel() for p in original) == proof.ORIGINAL_PARAMETERS and
                all(p.dtype == torch.float32 and p.device.type == "mps" for p in original),
                "wrong original FP32 parameter scope/device")
        for parameter in original:
            parameter.requires_grad_(False)
        require(all(not b.is_floating_point() or b.dtype == torch.float32 for b in model.buffers()),
                "original floating buffers must be FP32")
    return torch, model, original


def frozen_facts(torch, model, original, head, optimizer):
    require(sum(p.numel() for p in original) == proof.ORIGINAL_PARAMETERS and
            len({id(p) for p in original}) == len(original), "wrong original unique parameter scope")
    require(all(not p.requires_grad and p.grad is None and p.dtype == torch.float32 for p in original),
            "original frozen flags/gradients changed")
    require(all(not m.training for m in model.modules()), "original model must remain eval")
    require(list(head.shape) == [6, proof.HIDDEN_SIZE] and head.requires_grad and
            head.dtype == torch.float32 and head.is_leaf, "wrong independent FP32 readout")
    require(all(proof.storage_disjoint(head, p) for p in original), "head aliases original storage")
    require(len(optimizer.param_groups) == 1 and len(optimizer.param_groups[0]["params"]) == 1 and
            optimizer.param_groups[0]["params"][0] is head and
            all(p is head for p in optimizer.state), "optimizer includes original parameters")
    return {"original_unique_parameters": proof.ORIGINAL_PARAMETERS,
            "original_unique_tensors": len(original), "original_requires_grad_false": True,
            "original_gradients_none": True, "original_optimizer_members": 0,
            "original_weight_decay_members": 0, "backbone_eval": True,
            "trainable_parameters": proof.HEAD_PARAMETERS, "optimizer_parameter_tensors": 1,
            "optimizer_only_W6": True, "head_disjoint_from_all_original_storage": True,
            "head_bias": False, "feature_cache": False, "backbone_context": "torch.no_grad",
            "projection_outside_backbone_no_grad": True}


def hidden_state(torch, model, row, counts=None, phase=None):
    ids = torch.tensor([row["prompt_tokens"]], dtype=torch.long, device="mps")
    with torch.no_grad():
        if counts is None:
            hidden = model.model(input_ids=ids, attention_mask=torch.ones_like(ids),
                                 use_cache=False).last_hidden_state[:, -1:, :]
        else:
            mask = torch.ones_like(ids)
            head_lr.attempt(counts, phase)
            hidden = model.model(input_ids=ids, attention_mask=mask,
                                 use_cache=False).last_hidden_state[:, -1:, :]
            torch.mps.synchronize()
            head_lr.complete(counts, phase)
    require(list(hidden.shape) == [1, 1, proof.HIDDEN_SIZE] and hidden.dtype == torch.float32,
            "wrong frozen last normalized hidden state")
    return hidden


def readout(torch, head, hidden, row):
    all_six = torch.nn.functional.linear(hidden, head)[0, 0]
    # ordered_answers has proven this is the actual token-ID mapping, not a new vocab.
    logits = all_six[:len(row["answer_ids"])]
    require(bool(torch.isfinite(logits).all().item()), "nonfinite allowed logits")
    target = torch.tensor([row["target_position"]], dtype=torch.long, device="mps")
    loss = torch.nn.functional.cross_entropy(logits.unsqueeze(0), target)
    require(bool(torch.isfinite(loss).item()), "nonfinite conditional CE")
    return loss, logits


def fit_record(torch, row, loss, logits):
    ce, predicted = float(loss.item()), int(logits.argmax().item())
    return {"index": row["index"], "id": row["id"], "ce": ce,
            "agreement": predicted == row["target_position"], "predicted_position": predicted,
            "target_position": row["target_position"], "option_ids": row["option_ids"],
            "family": row["family"], "source": row["provenance"]["source"],
            "group_id": row["group_id"], **legacy.fit_observations(torch, logits, row)}


def binding_stats(scope):
    return {"scope": scope, "rows": 0, "finite_full_coverage": False,
            "max_absolute_logit_difference": 0.0, "max_absolute_probability_difference": 0.0,
            "logit_tolerance": LOGIT_TOLERANCE, "probability_tolerance": PROBABILITY_TOLERANCE,
            "identical_probability_top_sets": True, "identical_logit_top_sets": True,
            "status": "incomplete"}


def bind(left, right, stats):
    identities = ("index", "id", "target_id", "target_position", "option_ids", "family",
                  "source", "group_id", "allowed_answer_ids", "option_count")
    require(all(left[k] == right[k] for k in identities), "rowwise binding identity mismatch")
    differences = {}
    for key, name, tolerance in (("allowed_logits", "logit", LOGIT_TOLERANCE),
                                ("conditional_probabilities", "probability", PROBABILITY_TOLERANCE)):
        a, b = left[key], right[key]
        require(len(a) == len(b) == left["option_count"] and
                all(math.isfinite(v) for v in [*a, *b]), "nonfinite or incomplete binding vectors")
        delta = max(abs(x - y) for x, y in zip(a, b))
        differences[name] = delta
        stats[f"max_absolute_{name}_difference"] = max(stats[f"max_absolute_{name}_difference"], delta)
        require(delta <= tolerance, f"fixed {name} binding tolerance exceeded; no fallback")
    for key in ("probability_top_positions", "probability_top_option_ids", "logit_top_positions"):
        if left[key] != right[key]:
            stats["identical_logit_top_sets" if key == "logit_top_positions" else
                  "identical_probability_top_sets"] = False
            raise ValueError("fixed binding top sets disagree; no fallback")
    require(math.isfinite(left["ce"]) and math.isfinite(right["ce"]), "nonfinite binding CE")
    stats["rows"] += 1
    return differences


def fit(torch, model, head, schedule, directory, monitor, label, reference=None):
    stats = binding_stats("START: W6 vs retained M7 original-base prefit" if reference is not None else
                          "FINAL: W6 vs actual untied stock-shaped full-V lm_head, same hidden state")
    rows_path = directory / f"fit-{label}.jsonl"
    binding_path = directory / f"binding-{label}.jsonl"
    ce_sum, agreements = 0.0, 0
    counts = monitor.receipt.get("backbone_forwards")
    phase = "START" if label == "before" else "FINAL"
    with rows_path.open("x") as rows_stream, binding_path.open("x") as bindings, torch.no_grad():
        for index, row in enumerate(schedule):
            with monitor.phase(f"fit_{label}:forward"):
                hidden = hidden_state(torch, model, row, counts, phase)
                loss, logits = readout(torch, head, hidden, row)
                result = fit_record(torch, row, loss, logits)
                if reference is not None:
                    compared = reference[index]
                else:
                    full = model.lm_head(hidden)
                    require(list(full.shape) == [1, 1, proof.VOCAB_SIZE] and full.dtype == torch.float32,
                            "wrong actual exported full-vocabulary projection")
                    allowed = full[0, 0, row["answer_ids"]]
                    target = torch.tensor([row["target_position"]], dtype=torch.long, device="mps")
                    stock_loss = torch.nn.functional.cross_entropy(allowed.unsqueeze(0), target)
                    compared = fit_record(torch, row, stock_loss, allowed)
                rows_stream.write(data.json_line(result))
                rows_stream.flush()
                try:
                    delta = bind(result, compared, stats)
                except BaseException as exc:
                    stats.update(status="failed", failed_index=row["index"], failed_id=row["id"])
                    bindings.write(data.json_line({"index": row["index"], "id": row["id"],
                        "small_head": result, "reference": compared, "binding_failed": True,
                        "error": str(exc)[:1000], "same_hidden_state": reference is None}))
                    bindings.flush()
                    p3.save(directory / f"binding-{label}.json", stats)
                    raise
                bindings.write(data.json_line({"index": row["index"], "id": row["id"],
                    "small_head": result, "reference": compared, "absolute_max_differences": delta,
                    "same_hidden_state": reference is None}))
                bindings.flush()
                ce_sum += result["ce"]
                agreements += int(result["agreement"])
                del hidden, loss, logits
                if reference is None:
                    del full, allowed, stock_loss
            if (index + 1) % 100 == 0:
                monitor.progress(phase=f"fit_{label}", fit_rows=index + 1)
    if counts is not None:
        head_lr.require_complete(counts, phase)
    require(stats["rows"] == 1500, "incomplete binding coverage")
    stats.update(status="complete", finite_full_coverage=True,
                 rowwise_proof={"path": str(binding_path), "sha256": p3.digest(binding_path)},
                 fit_rows={"path": str(rows_path), "sha256": p3.digest(rows_path)},
                 mean_ce=ce_sum / 1500, agreements=agreements)
    p3.save(directory / f"binding-{label}.json", stats)
    return stats


def save_head(torch, head, initial, directory, receipt, monitor, emergency=False):
    from safetensors.torch import save_file

    path = directory / ("learned-head-emergency.safetensors" if emergency else "learned-head.safetensors")
    if path.exists():
        return
    if not emergency:
        monitor.guard("learned_head_save:before")
    cpu = head.detach().cpu().contiguous()
    save_file({"W6": cpu}, str(path))
    delta = cpu - initial
    evidence = {"path": str(path), "sha256": p3.digest(path),
        "initial": proof.tensor_record(initial), "learned": proof.tensor_record(cpu),
        "movement_l2": float(torch.linalg.vector_norm(delta).item()),
        "movement_max_absolute": float(delta.abs().max().item()),
        "initial_l2": float(torch.linalg.vector_norm(initial).item()),
        "learned_l2": float(torch.linalg.vector_norm(cpu).item()),
        "optimizer_steps": receipt["optimizer_steps"],
        "optimizer_step_attempts": receipt["optimizer_step_attempts"],
        "qualification": "actual movement only; no minimum movement or hash-change success criterion"}
    p3.save(directory / ("head-evidence-emergency.json" if emergency else "head-evidence.json"), evidence)
    receipt["learned_head"] = evidence
    if not emergency:
        monitor.guard("learned_head_save:after")


def saved_header(path):
    # Metadata only: never a second weight load or a numeric reload canary.
    with path.open("rb") as stream:
        length_bytes = stream.read(8)
        require(len(length_bytes) == 8, "truncated safe header")
        length = struct.unpack("<Q", length_bytes)[0]
        require(0 < length < 16 * 2**20, "unbounded safe header")
        header = data.strict_json(stream.read(length))
    return {k: v for k, v in header.items() if k != "__metadata__"}


def save_checkpoint(model, directory, receipt, monitor):
    checkpoint = directory / "checkpoint"
    checkpoint.mkdir(exist_ok=False)
    with monitor.phase("save_checkpoint"):
        model.save_pretrained(str(checkpoint), safe_serialization=True, max_shard_size="5GB")
        assets = receipt["identity"]["evidence"]["tokenizer_assets"]
        require(set(assets) == {"tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"},
                "expected original four tokenizer files")
        for name, sha in assets.items():
            require(not (checkpoint / name).exists(), "refusing tokenizer overwrite")
            shutil.copyfile(data.MODEL_DIR / name, checkpoint / name)
            require(p3.digest(checkpoint / name) == sha, "tokenizer byte-copy mismatch")
        for name in ("LICENSE", "README.md"):
            if name in receipt["identity"]["evidence"]["model_assets"]:
                shutil.copyfile(data.MODEL_DIR / name, checkpoint / name)
        header = saved_header(checkpoint / "model.safetensors")
        expected = {name: list(value.shape) for name, value in model.state_dict().items()}
        require(set(header) == set(expected) and all(header[k]["shape"] == shape and
                header[k]["dtype"] == "F32" for k, shape in expected.items()),
                "saved safe tensor keys/shapes/dtypes differ from actual export")
        for name in ("model.embed_tokens.weight", "lm_head.weight"):
            require(header[name]["shape"] == [proof.VOCAB_SIZE, proof.HIDDEN_SIZE],
                    "serialized full embedding/head missing")
        config = data.read_json(checkpoint / "config.json")
        require(config["tie_word_embeddings"] is False and config["vocab_size"] == proof.VOCAB_SIZE and
                config["hidden_size"] == proof.HIDDEN_SIZE and
                config.get("torch_dtype", config.get("dtype")) == "float32", "wrong saved HF config")
        original_config = data.read_json(data.MODEL_DIR / "config.json")
        require(data.json_line(config) == data.json_line(proof.export_config(original_config)),
                "saved configuration differs from exact pinned HF normalization")
        require(not list(checkpoint.glob("*.index.json")), "sharded export prohibited")
        receipt["saved_metadata"] = {"config": config, "tensor_header": header,
            "qualification": "saved header/config inspection only; P6 owns sole fresh numerical reload"}
        inventory = {}
        for path in sorted(checkpoint.rglob("*")):
            if path.is_file():
                monitor.guard("checkpoint_inventory:before_file")
                inventory[str(path.relative_to(checkpoint))] = {
                    "sha256": p3.digest(path), "bytes": path.stat().st_size}
                monitor.guard("checkpoint_inventory:after_file")
                path.chmod(0o444)
        checkpoint.chmod(0o555)
    receipt["checkpoint_files"], receipt["tokenizer_assets"] = inventory, assets


def train(args, receipt, monitor, schedule, directory):
    authorization = head_lr.AUTHORIZATION if args.experiment == "m12" else AUTHORIZATION
    require(args.authorize_run == authorization, "explicit one-attempt experiment authorization required")
    require(len(args.comparison_freeze_sha256) == 64 and
            all(c in "0123456789abcdef" for c in args.comparison_freeze_sha256), "comparison freeze SHA required")
    receipt["comparison_freeze_sha256"] = args.comparison_freeze_sha256
    receipt["authorization"] = authorization
    reuse = head_lr.capacity_reuse if args.experiment == "m12" else capacity_reuse
    receipt["capacity_reuse"] = reuse(receipt["identity"], schedule)
    reference = pinned_prefit(receipt, schedule)
    answer_ids = ordered_answers(schedule)
    torch, model, original = load_frozen_model(monitor, receipt)
    head = initial = None
    try:
        with monitor.phase("freeze_and_initialize_head"):
            require(model.config.tie_word_embeddings is True and
                    model.lm_head.weight is model.model.embed_tokens.weight and model.lm_head.bias is None,
                    "original P3 must be genuinely tied and bias-free")
            require(list(model.lm_head.weight.shape) == [proof.VOCAB_SIZE, proof.HIDDEN_SIZE], "wrong base shape")
            for parameter in original:
                parameter.requires_grad_(False)
            head = torch.nn.Parameter(model.lm_head.weight[answer_ids].detach().clone().contiguous())
            initial = head.detach().cpu().clone()
            optimizer = legacy.optimizer_for(torch, [head], monitor.cfg)
            scope_before = frozen_facts(torch, model, original, head, optimizer)
            receipt["parameters"] = scope_before
            if args.experiment == "m12":
                require(scope_before == receipt["capacity_reuse"]["historical_scope"],
                        "M12 frozen scope differs from actual M8")
        with monitor.phase("original_tensor_proof"):
            before = proof.backbone_records(model, monitor.guard)
            output_before = proof.output_records(model.lm_head.weight, answer_ids, monitor.guard)
            require(output_before["ordered_answer_rows"] == proof.tensor_record(initial, monitor.guard),
                    "initial W6 does not match actual original ordered answer rows")
            config_before = copy.deepcopy(model.config.to_dict())
            original_config = data.read_json(data.MODEL_DIR / "config.json")
            p3.save(directory / "original-tensor-proof.json", {
                "backbone": before, "output": output_before, "scope": scope_before,
                "materialized_config": config_before, "original_config": original_config})
        receipt["fit_before"] = fit(torch, model, head, schedule, directory, monitor, "before", reference)
        del reference
        optimizer.zero_grad(set_to_none=True)
        with (directory / "online.jsonl").open("x") as online, (directory / "gradient-norms.jsonl").open("x") as norms:
            for index, row in enumerate(schedule):
                with monitor.phase("train_forward"):
                    hidden = hidden_state(torch, model, row, receipt.get("backbone_forwards"), "TRAIN")
                    loss, logits = readout(torch, head, hidden, row)
                    ce = float(loss.item())
                with monitor.phase("train_backward"):
                    (loss / 4).backward()
                    del hidden, loss, logits
                receipt["presentations"] += 1
                online.write(data.json_line({"index": row["index"], "id": row["id"], "ce": ce,
                    "update": index // 4 + 1, "qualification": "online changing-head descriptive conditional CE"}))
                online.flush()
                if (index + 1) % 4 == 0:
                    with monitor.phase("train_clip"):
                        require(head.grad is not None, "missing W6 gradient")
                        norm = torch.nn.utils.clip_grad_norm_([head], 1.0, error_if_nonfinite=True, foreach=False)
                        value = float(norm.item())
                        require(math.isfinite(value) and value >= 0, "nonfinite gradient norm")
                        norms.write(data.json_line({"update": index // 4 + 1, "preclip_norm": value,
                                                   "presentations": receipt["presentations"]}))
                        norms.flush()
                    with monitor.phase("train_optimizer_step"):
                        receipt["optimizer_step_attempts"] += 1
                        save_status(directory, receipt)
                        monitor.progress(phase="optimizer_step_ATTEMPT",
                            attempt=receipt["optimizer_step_attempts"], completed=receipt["optimizer_steps"])
                        optimizer.step()
                        torch.mps.synchronize()
                        receipt["optimizer_steps"] += 1
                        save_status(directory, receipt)
                    optimizer.zero_grad(set_to_none=True)
                monitor.guard("train_row_complete")
        require(receipt["optimizer_steps"] == receipt["optimizer_step_attempts"] == 375 and
                receipt["presentations"] == 1500, "wrong learning coverage")
        if "backbone_forwards" in receipt:
            head_lr.require_complete(receipt["backbone_forwards"], "TRAIN")
        # Preserve the only learned state before any scope/export/FINAL operation.
        save_head(torch, head, initial, directory, receipt, monitor)
        receipt["gradient_norms"] = {"path": str(directory / "gradient-norms.jsonl"),
            "sha256": p3.digest(directory / "gradient-norms.jsonl"), "values": 375}
        receipt["online"] = {"path": str(directory / "online.jsonl"),
            "sha256": p3.digest(directory / "online.jsonl"), "rows": 1500}
        receipt["adam_final_state"] = legacy.moment_evidence(torch, optimizer, [head], 375)
        scope_after = frozen_facts(torch, model, original, head, optimizer)
        require(scope_before == scope_after, "frozen scope facts changed")
        with monitor.phase("frozen_tensor_proof_after"):
            after = proof.backbone_records(model, monitor.guard)
            require(before == after, "original backbone parameters/fixed buffers changed")
        with monitor.phase("construct_untied_full_vocab_export"):
            # Allocate from ORIGINAL frozen table, never from random module initialization.
            table = model.lm_head.weight.detach().clone().contiguous()
            with torch.no_grad():
                table[answer_ids] = head.detach()
            exported = torch.nn.Linear(proof.HIDDEN_SIZE, proof.VOCAB_SIZE,
                                       bias=False, device="meta", dtype=torch.float32)
            exported.weight = torch.nn.Parameter(table, requires_grad=False)
            model.set_output_embeddings(exported)
            model.config.tie_word_embeddings = False
            model.eval()
            require(model.lm_head is exported and model.lm_head.bias is None and
                    proof.storage_disjoint(model.lm_head.weight, model.model.embed_tokens.weight) and
                    proof.storage_disjoint(model.lm_head.weight, head), "export is not genuinely independent")
            output_after = proof.output_records(model.lm_head.weight, answer_ids, monitor.guard)
            require(output_before["nonanswer_rows"] == output_after["nonanswer_rows"], "non-answer rows changed")
            require(output_after["ordered_answer_rows"] == receipt["learned_head"]["learned"],
                    "full export ordered rows do not match saved learned W6")
            require(output_after["answer_rows"] == {
                str(token): proof.tensor_record(head[i], monitor.guard) for i, token in enumerate(answer_ids)},
                "learned six-row placement mismatch")
            config_after = model.config.to_dict()
            diff = {k: {"before": config_before.get(k), "after": config_after.get(k)}
                    for k in set(config_before) | set(config_after) if config_before.get(k) != config_after.get(k)}
            require(diff == {"tie_word_embeddings": {"before": True, "after": False}}, "uncontrolled export config mutation")
        receipt["fit_after"] = fit(torch, model, head, schedule, directory, monitor, "after")
        with monitor.phase("export_backbone_proof"):
            export_backbone = proof.backbone_records(model, monitor.guard)
            require(export_backbone == before, "export mutated original backbone or fixed buffers")
            require(frozen_facts(torch, model, original, head, optimizer) == scope_before,
                    "frozen flags or gradients changed after export/FINAL")
        del optimizer
        save_checkpoint(model, directory, receipt, monitor)
        require(data.source_binding(data.source_identity(args.experiment), args.experiment) ==
                data.source_binding(receipt["identity"]["evidence"]["source"], args.experiment),
                "executable source changed during run")
        receipt["readout_proof_body"] = {
            "schema_version": proof.SCHEMA, "status": "complete",
            "adaptation_kind": proof.ADAPTATION, "representation": proof.REPRESENTATION,
            "answer_token_ids": answer_ids, "answer_symbols": list("ABCDEF"),
            "hidden_size": proof.HIDDEN_SIZE, "vocab_size": proof.VOCAB_SIZE,
            "dtype": "float32", "bias": False, "tie_word_embeddings": False,
            "original_base_assets": receipt["identity"]["evidence"]["model_assets"],
            "original_base_model_id": p3.MODEL, "original_base_revision": p3.REVISION,
            "backbone_before": before, "backbone_after": after, "backbone_export": export_backbone,
            "scope_before": scope_before, "scope_after": scope_after,
            "export_storage": {"input_output_disjoint": True, "head_output_disjoint": True,
                               "independent_full_vocab_parameter": True},
            "output_before": output_before, "output_after": output_after,
            "learned_head": receipt["learned_head"],
            "original_config": original_config, "materialized_config_before": config_before,
            "materialized_config_after": config_after, "config_diff": diff,
            "saved_config": receipt["saved_metadata"]["config"],
            "start_binding": receipt["fit_before"], "final_binding": receipt["fit_after"],
            "starting_control_source": receipt["starting_control_source"],
            "completed_training": {"presentations": 1500, "optimizer_steps": 375,
                "optimizer_step_attempts": 375, "scope": "TRAIN only; one epoch; W6 only",
                "schedule_sha256": data.M6_SCHEDULE_SHA, "gradient_norms": receipt["gradient_norms"],
                "online": receipt["online"], "adam_final_state": receipt["adam_final_state"]},
            "qualification": "P6 must verify loaded tensors/config/storage; no fresh reload in producer"}
        monitor.guard("train_complete")
    except BaseException:
        if head is not None and initial is not None and receipt["optimizer_step_attempts"]:
            try:
                save_head(torch, head, initial, directory, receipt, monitor, emergency=True)
            except BaseException as exc:
                receipt["emergency_head_save_error"] = {"type": type(exc).__name__, "message": str(exc)[:1000]}
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit")
    training = commands.add_parser("train")
    for command in (audit, training):
        command.add_argument("--experiment", choices=("m8", "m12"), default="m8")
        command.add_argument("--output-dir", type=Path, required=True)
        command.add_argument("--supervisor-receipt", type=Path, required=True,
            help="prelaunch owner JSON attestation, copied/bound in output; external enforcement required")
    training.add_argument("--audit-dir", type=Path, required=True)
    training.add_argument("--authorize-run", required=True)
    training.add_argument("--comparison-freeze-sha256", required=True)
    args = parser.parse_args()
    start = time.monotonic()
    directory = args.output_dir.expanduser().resolve()
    require(not any("final" in part.lower() for part in directory.parts), "final output path forbidden")
    directory.mkdir(parents=True, exist_ok=False)
    receipt = {"schema_version": f"{args.experiment}.{args.command}.v1", "command": args.command,
        "status": "failed", "output_dir": str(directory), "memory_samples": [], "phase_seconds": {},
        "presentations": 0, "optimizer_steps": 0, "optimizer_step_attempts": 0,
        "extra_backwards": 0, "external_deadline_required": True,
        "memory_qualification": "CPU lifetime RSS and sampled MPS driver; not peaks, never sum scopes"}
    if args.experiment == "m12" and args.command == "train":
        receipt["backbone_forwards"] = head_lr.new_counts()
    p3.save(directory / "failure-receipt.json", {**receipt,
        "error": "incomplete start sentinel; not an actual completed zero-update receipt; inspect status/events"})
    save_status(directory, receipt)
    monitor, exit_code = None, 0
    old_term = signal.getsignal(signal.SIGTERM)

    def terminated(signum, frame):
        raise TimeoutError("external supervisor SIGTERM")

    signal.signal(signal.SIGTERM, terminated)
    try:
        maximum_seconds = 590 if args.experiment == "m12" else 2700
        monitor = legacy.Monitor(directory, receipt, start, maximum_seconds, args.experiment)
        with monitor.phase("supervisor_attestation"):
            supervisor_path = data.safe_path(args.supervisor_receipt)
            supervisor = data.read_json(supervisor_path)
            require(supervisor.get("schema_version") == f"{args.experiment}.supervisor.v1" and
                    supervisor.get("external_enforcement") is True and supervisor.get("automatic_retry") is False and
                    supervisor.get("fresh_process") is True and supervisor.get("command") == args.command and
                    supervisor.get("output_dir") == str(directory), "matching external supervisor required")
            supervisor_pid = supervisor.get("supervisor_pid")
            require(type(supervisor_pid) is int and supervisor_pid > 0 and supervisor_pid != os.getpid(),
                    "external supervisor process identity required")
            os.kill(supervisor_pid, 0)
            remaining = supervisor.get("remaining_aggregate_seconds")
            require(type(remaining) is int and 0 < remaining <= maximum_seconds and
                    type(supervisor.get("process_max_seconds")) is int and
                    0 < supervisor["process_max_seconds"] <= remaining,
                    "external process/remaining aggregate bound required")
            monitor.seconds = supervisor["process_max_seconds"]
            receipt["supervisor"] = {"path": str(supervisor_path), "sha256": p3.digest(supervisor_path),
                                     "attestation": supervisor}
            p3.save(directory / "supervisor.json", supervisor)
        with monitor.phase("revalidation"):
            if args.command == "audit":
                evidence, schedule = data.evidence(monitor.guard, args.experiment)
                text = data.schedule_text(schedule)
                (directory / "schedule.jsonl").write_text(text, encoding="utf-8")
                receipt.update(evidence=evidence, schedule_sha256=p3.text_hash(text))
            else:
                identity, schedule = data.revalidate(args.audit_dir.resolve(), monitor.guard, args.experiment)
                receipt["identity"] = identity
                # Full schedule/evidence stays with this run, not just the audit directory.
                (directory / "schedule.jsonl").write_text(data.schedule_text(schedule), encoding="utf-8")
        if args.command == "train":
            train(args, receipt, monitor, schedule, directory)
        monitor.guard("process_complete")
        if args.command == "train":
            body = receipt.pop("readout_proof_body")
            p3.save(directory / "readout-proof.json", body)
            receipt["readout_proof"] = {"path": str(directory / "readout-proof.json"),
                                        "sha256": p3.digest(directory / "readout-proof.json")}
        receipt["status"] = "complete"
    except BaseException as exc:
        receipt.pop("readout_proof_body", None)
        receipt["status"] = "failed"
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:2000], "retry": False}
        exit_code = 1
    finally:
        if monitor is not None:
            try:
                monitor.sample("work_end")
            except Exception as exc:
                receipt["end_memory_sample_error"] = type(exc).__name__
        receipt["process_runtime_seconds"] = time.monotonic() - start
        receipt["cpu_lifetime_rss_bytes"] = legacy.rss_bytes()
        receipt_path = directory / ("audit.json" if args.command == "audit" else "receipt.json")
        # Keep the run directory writable for failed-receipt replacement; files seal first.
        pending_manifest = directory / "checkpoint-manifest.pending.json"
        published_manifest = directory / "checkpoint-manifest.json"
        try:
            if monitor is not None and receipt["status"] == "complete":
                monitor.guard("publication:before")
            save_status(directory, receipt)
            p3.save(receipt_path, receipt)
            if args.command == "train" and receipt["status"] == "complete":
                manifest = legacy.checkpoint_manifest(directory, receipt)
                manifest.update(schema_version="jeff.qwen-trained-checkpoint.v2",
                    adaptation_kind=proof.ADAPTATION, representation=proof.REPRESENTATION,
                    readout_proof=receipt["readout_proof"])
                p3.save(pending_manifest, manifest)
            if monitor is not None and receipt["status"] == "complete":
                monitor.guard("publication:after_io")
            if monitor is not None and not monitor.events.closed:
                monitor.events.close()
            for path in directory.iterdir():
                if path.is_file():
                    path.chmod(0o444)
            signal.signal(signal.SIGTERM, old_term)
            print(json.dumps({"prepared_status": receipt["status"], "receipt": str(receipt_path),
                              "seconds": receipt["process_runtime_seconds"]}), flush=True)
            if pending_manifest.exists():
                pending_manifest.rename(published_manifest)
        except BaseException as exc:
            if published_manifest.exists():
                published_manifest.rename(directory / "checkpoint-manifest.failed.json")
            receipt["status"] = "failed"
            receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:2000], "retry": False}
            receipt["process_runtime_seconds"] = time.monotonic() - start
            exit_code = 1
            failed_path = directory / "failed-publication-receipt.json"
            p3.save(failed_path, receipt)
            failed_path.replace(receipt_path)
            save_status(directory, receipt)
        finally:
            if receipt["status"] != "complete":
                if monitor is not None and not monitor.events.closed:
                    monitor.events.close()
                signal.signal(signal.SIGTERM, old_term)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
