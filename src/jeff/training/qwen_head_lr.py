"""Fixed M12 authorization and historical metadata reuse; no ML imports."""

from jeff.training import qwen_data as data

require = data.require
AUTHORIZATION = "M12-ONE-original-P3-frozen-six-row-lr2e-4-1500-375-seed42"
M8_RUN = data.ARTIFACTS / "model/m8-qwen-readout-20261111-01"
M8_RECEIPT_SHA = "06f742a2bf8c3e2d6a33c9dd64bb8f02744f271e24f13f7289f021bc674542fa"


def capacity_reuse(identity, schedule):
    path = M8_RUN / "training/receipt.json"
    old = data.pinned_json(path, M8_RECEIPT_SHA)
    require(old["schema_version"] == "m8.train.v1" and old["status"] == "complete" and
            old["command"] == "train" and old["presentations"] == 1500 and
            old["optimizer_steps"] == old["optimizer_step_attempts"] == 375 and
            old["extra_backwards"] == 0, "successful actual M8 training required")
    previous, current = old["identity"]["evidence"], identity["evidence"]
    excluded = {"source", "recipe", "recipe_path", "recipe_sha256"}
    require({k: v for k, v in previous.items() if k not in excluded} ==
            {k: v for k, v in current.items() if k not in excluded},
            "M8 original assets/data/runtime controls changed; raw environment must match")
    before, after = previous["recipe"], current["recipe"]
    allowed = {"schema_version", "learning_rate", "maximum_run_seconds"}
    require(before["schema_version"] == "m8.recipe.v1" and before["learning_rate"] == 2e-6 and
            before["maximum_run_seconds"] == 2700 and after == data.recipe("m12") and
            {k: v for k, v in before.items() if k not in allowed} ==
            {k: v for k, v in after.items() if k not in allowed},
            "only fixed schema/LR/operational budget differences from actual M8 allowed")
    require(old["identity"]["schedule_sha256"] == identity["schedule_sha256"] ==
            data.M6_SCHEDULE_SHA, "M8 schedule identity mismatch")
    data.require_m6_schedule(data.schedule_text(schedule))
    scope = {"original_unique_parameters": 494032768, "original_unique_tensors": 290,
        "original_requires_grad_false": True, "original_gradients_none": True,
        "original_optimizer_members": 0, "original_weight_decay_members": 0,
        "backbone_eval": True, "trainable_parameters": 5376, "optimizer_parameter_tensors": 1,
        "optimizer_only_W6": True, "head_disjoint_from_all_original_storage": True,
        "head_bias": False, "feature_cache": False, "backbone_context": "torch.no_grad",
        "projection_outside_backbone_no_grad": True}
    require(old["parameters"] == scope and old["base_loading_info"] == {
        "missing_keys": [], "unexpected_keys": [], "mismatched_keys": [], "error_msgs": []},
        "actual M8 frozen scope/loading evidence mismatch")
    require(all(old[key]["status"] == "complete" and old[key]["rows"] == 1500 and
                old[key]["finite_full_coverage"] is True for key in ("fit_before", "fit_after")),
            "actual M8 START/FINAL coverage required")
    require(old["fresh_start"] == {"seed": 42, "base_model_id": current["base_model_id"],
        "base_revision": current["base_revision"], "model_dir": current["model_dir"],
        "base_weight_sha256": current["model_assets"]["model.safetensors"],
        "optimizer_state": "new empty AdamW; no historical optimizer/model state reused",
        "rng": "fresh process; random.seed/torch.manual_seed/torch.mps.manual_seed(42)"},
        "actual M8 must have used fresh original P3/optimizer/RNG")
    samples = old["memory_samples"]
    require(samples and any("mps_recommended_headroom_bytes" in s for s in samples),
            "actual M8 headroom observations required")
    for sample in samples:
        require(sample["cpu_lifetime_rss_bytes"] <= after["max_cpu_rss_bytes"] and
                sample.get("mps_driver_bytes", 0) <= after["max_mps_driver_bytes"] and
                sample.get("mps_recommended_headroom_bytes", after["min_recommended_headroom_bytes"]) >=
                    after["min_recommended_headroom_bytes"], "historical M8 memory guard violation")
    return {"path": str(path), "sha256": M8_RECEIPT_SHA,
        "basis": "successful actual M8 frozen scope/memory/controls only; no new capacity probe",
        "historical_recipe": before, "current_recipe": after,
        "allowed_differences": sorted(allowed), "historical_scope": scope,
        "historical_process_runtime_seconds": old["process_runtime_seconds"],
        "memory_samples": len(samples),
        "historical_max_cpu_rss_bytes": max(s["cpu_lifetime_rss_bytes"] for s in samples),
        "historical_max_mps_driver_bytes": max(s.get("mps_driver_bytes", 0) for s in samples),
        "projection_verified": False,
        "qualification": "Historical observations are not an M12 timing/memory guarantee; no learned state reused"}


def new_counts():
    return {"maximum": 4500, "attempted": 0, "completed": 0,
            "by_phase": {phase: {"attempted": 0, "completed": 0}
                         for phase in ("START", "TRAIN", "FINAL")}}


def attempt(counts, phase):
    phases = ("START", "TRAIN", "FINAL")
    require(phase in phases, "unknown M12 backbone phase")
    require(all(counts["by_phase"][p] == {"attempted": 1500, "completed": 1500}
                for p in phases[:phases.index(phase)]), "incomplete previous backbone phase")
    current = counts["by_phase"][phase]
    require(counts["attempted"] == counts["completed"] < counts["maximum"] == 4500 and
            current["attempted"] == current["completed"] < 1500,
            "M12 backbone forward limit or incomplete prior call")
    counts["attempted"] += 1
    current["attempted"] += 1


def complete(counts, phase):
    counts["completed"] += 1
    counts["by_phase"][phase]["completed"] += 1


def require_complete(counts, phase):
    require(counts["by_phase"][phase] == {"attempted": 1500, "completed": 1500},
            "incomplete M12 backbone phase")
    if phase == "FINAL":
        require(counts["attempted"] == counts["completed"] == counts["maximum"] == 4500,
                "incomplete M12 backbone coverage")
