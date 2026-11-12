"""M10-only historical full-scope reuse and durable first-update boundary."""

import os

from jeff.training import qwen_data as data

require = data.require
AUTHORIZATION = "M10-ONE-original-P3-full-1500-375-seed7-lr2e-6"
M7_RUN = data.ARTIFACTS / "model/m7-qwen-low-lr-20261111-01"
M7_RECEIPT_SHA = "c78ad96769b76c2cabb7c2b0ec87dde13bca78e2f7e2256a51b6ca545b54e156"
M7_AUDIT_SHA = "3182c01d5128342a3338ba3bf05ed8a9b79524f1a58c8620e7686063645eb814"
M7_PROCESS_SHA = "26cef7e812511a087f16883a3626c749689e3b03e648a072d4be4026c2b517c3"


def reuse_m7_capacity(path, identity, schedule):
    require(path == (M7_RUN / "training/receipt.json").resolve(),
            "M10 requires actual completed M7 full-scope receipt, not a new probe")
    old = data.pinned_json(path, M7_RECEIPT_SHA)
    audit = data.pinned_json(M7_RUN / "train-audit/audit.json", M7_AUDIT_SHA)
    process = data.pinned_json(M7_RUN / "train-process.json", M7_PROCESS_SHA)
    require(old["schema_version"] == "m7.train.v1" and old["status"] == "complete" and
            old["command"] == "train" and old["presentations"] == 1500 and
            old["optimizer_steps"] == 375 and old["extra_backwards"] == 0 and
            old["authorization"] == "M7-ONE-original-P3-LR2e-6-1500-375-seed42" and
            old["external_deadline_required"] is True, "incomplete M7 full-scope evidence")
    require(process["returncode"] == 0 and process["timeout"] is False and
            process["automatic_retry"] is False and process["maximum_seconds"] == 2700 and
            0 < process["process_wall_seconds"] < 2400,
            "successful supervised M7 full run required")
    require(audit["schema_version"] == "m7.audit.v1" and audit["status"] == "complete" and
            old["identity"] == {"audit_sha256": M7_AUDIT_SHA,
                "schedule_sha256": data.M6_SCHEDULE_SHA, "evidence": audit["evidence"]},
            "M7 full-run audit binding changed")
    previous, current = audit["evidence"], identity["evidence"]
    # New source/recipe identities are bound by M10's own audit, not substituted for M7.
    excluded = {"source", "recipe_path", "recipe_sha256", "recipe", "lengths", "schedule_algorithm"}
    require({k: v for k, v in previous.items() if k not in excluded} ==
            {k: v for k, v in current.items() if k not in excluded},
            "M10 base/scorer/tokenizer/template/TRAIN/runtime scientific pins changed")
    before, after = previous["recipe"], current["recipe"]
    require(before["schema_version"] == "m7.recipe.v1" and before["seed"] == 42 and
            before["maximum_run_seconds"] == 2700 and after["schema_version"] == "m10.recipe.v1" and
            after["seed"] == 7 and after["maximum_run_seconds"] == 2400 and
            {k: v for k, v in before.items() if k not in
                {"schema_version", "seed", "maximum_run_seconds"}} ==
            {k: v for k, v in after.items() if k not in
                {"schema_version", "seed", "maximum_run_seconds"}},
            "M10 permits only seed, recipe identity and operational budget differences from M7")
    require(previous["schedule_algorithm"] == "Random(42): shuffle rows then options once per row" and
            current["schedule_algorithm"] == "Random(7): shuffle rows then options once per row" and
            len(schedule) == 1500 and len({r["id"] for r in schedule}) == 1500 and
            all(r["index"] == i and r["option_ids"] == [o["id"] for o in r["decision"]["options"]] and
                r["option_ids"][r["target_position"]] == r["target_id"] for i, r in enumerate(schedule)) and
            data.p3.text_hash(data.schedule_text(schedule)) == identity["schedule_sha256"],
            "M10 materialized seed7 schedule/target-ID remapping mismatch")
    # Permutation may change token lengths, not capacity: every new prompt must fit the
    # maximum actually exercised by the completed full-parameter M7 run.
    require(current["lengths"] == data.p3.distribution([r["input_tokens"] for r in schedule]) and
            0 < current["lengths"]["max"] <= previous["lengths"]["max"] <= 1024,
            "seed7 shapes exceed completed M7 scope; stop without a new capacity probe")
    require(old["fresh_start"] == {"seed": 42, "base_model_id": current["base_model_id"],
            "base_revision": current["base_revision"], "model_dir": current["model_dir"],
            "base_weight_sha256": current["model_assets"]["model.safetensors"],
            "optimizer_state": "new empty AdamW; capacity state never reused",
            "rng": "fresh process; random.seed/torch.manual_seed/torch.mps.manual_seed(42)"},
            "historical M7 must start from original P3")
    parameters = old["parameters"]
    require(parameters["dtype"] == "float32" and parameters["total"] == parameters["trainable"] and
            old["adam_final_state"] == {"state_tensors": parameters["unique_tensors"],
                "moment_bytes": parameters["total"] * 8, "step": 375} and
            old["fit_before"]["overall"]["rows"] == old["fit_after"]["overall"]["rows"] == 1500 and
            old["gradient_norms"]["values"] == 375 and
            len(old["phase_seconds"]["train_forward"]) ==
                len(old["phase_seconds"]["train_backward"]) == 1500 and
            len(old["phase_seconds"]["train_optimizer_step"]) == 375,
            "historical full FP32 model/AdamW/fit scope incomplete")
    samples = old["memory_samples"]
    require(samples and any("mps_recommended_headroom_bytes" in s for s in samples),
            "historical M7 observed headroom required")
    for sample in samples:
        require(sample["elapsed_seconds"] < after["maximum_run_seconds"] and
                sample["cpu_lifetime_rss_bytes"] <= after["max_cpu_rss_bytes"] and
                sample.get("mps_driver_bytes", 0) <= after["max_mps_driver_bytes"] and
                sample.get("mps_recommended_headroom_bytes", after["min_recommended_headroom_bytes"]) >=
                    after["min_recommended_headroom_bytes"], "historical M7 guard violation")
    return {"path": str(path), "sha256": M7_RECEIPT_SHA, "audit_sha256": M7_AUDIT_SHA,
        "process_sha256": M7_PROCESS_SHA, "historical_identity": old["identity"],
        "schedule_sha256": identity["schedule_sha256"],
        "allowed_differences": {
            "seed": "42 -> 7; row/option permutation and fresh-process RNG reset only",
            "identity": "new source/recipe/audit/schedule/run identity; historical source retained",
            "operational_budget": "2700 -> 2400 seconds; unchanged memory guards"},
        "historical_max_input_tokens": previous["lengths"]["max"],
        "current_max_input_tokens": current["lengths"]["max"],
        "basis": "completed M7 full FP32/AdamW scope; only seed/new identity/operational budget differ; no new probe",
        "qualification": "historical observed memory/time, not a new peak or deadline guarantee; no historical weights or optimizer reused"}


def first_update_attempt(directory, receipt):
    path = directory / "ATTEMPT.json"
    record = {"schema_version": "m10.attempt.v1", "status": "first_update_attempted",
        "authorization": AUTHORIZATION, "presentations": receipt["presentations"],
        "optimizer_steps_before": receipt["optimizer_steps"],
        "audit_sha256": receipt["identity"]["audit_sha256"],
        "schedule_sha256": receipt["identity"]["schedule_sha256"],
        "comparison_freeze_sha256": receipt["comparison_freeze_sha256"],
        "restart": False,
        "meaning": "durable BEFORE first optimizer.step; existence spends attempt even if step completion is unknown"}
    require(record["presentations"] == 4 and record["optimizer_steps_before"] == 0,
            "invalid first-update boundary")
    with path.open("x", encoding="utf-8") as stream:
        stream.write(data.json_line(record))
        stream.flush()
        os.fsync(stream.fileno())
    # Persist both the marker and the new run directory's own directory entry.
    for directory_path in (directory, directory.parent):
        fd = os.open(directory_path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    receipt["first_update_attempt"] = {"path": str(path), "sha256": data.p3.digest(path), **record}
