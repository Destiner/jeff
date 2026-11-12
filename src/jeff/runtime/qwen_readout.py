"""Fail-closed M8/M12 metadata and fresh-load identity checks; no ML imports at import.

Producer scope/binding statements attest history, not independently replayed
training truth. Only validate_loaded establishes actual reloaded tensor identity.
"""

import math
from pathlib import Path
import re
import stat

from jeff.runtime.qwen_checkpoint import MODEL, REVISION, SCORING_SHA256, TOKENIZERS

SOURCE = Path(__file__).resolve()
ADAPTATION = "frozen-base-six-row-readout"
REPRESENTATION = "hf-untied-full-vocab"
SCHEDULE = "7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8"
CONTROL = "4940b17902562c8da5cf34e80eaa3618fa5ab52c20ad90715fd6dc6d3c9d12d5"
CONTROL_RECEIPT = "c78ad96769b76c2cabb7c2b0ec87dde13bca78e2f7e2256a51b6ca545b54e156"
DATA = "d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac"
# Authoritative P3 audit SHA8e0dc65beb1c9dd5a21b2c4170853bc78bf14116429a9311c28e568c129d870a.
ORIGINAL_ASSETS = {
    **TOKENIZERS,
    "LICENSE": "832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e",
    "README.md": "b19c806a904db6dc878a0462e70b551f6b7ac78dfbb88c2eb966ca2b9109ae15",
    "config.json": "18e18afcaccafade98daf13a54092927904649e1dd4eba8299ab717d5d94ff45",
    "generation_config.json": "e558847a8b4402616f1273797b015104dc266fe4b520056fca88823ba8f8ebe6",
    "model.safetensors": "fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe",
}
ORIGINAL_CONFIG = {
    "architectures": ["Qwen2ForCausalLM"], "attention_dropout": 0.0,
    "bos_token_id": 151643, "eos_token_id": 151645, "hidden_act": "silu",
    "hidden_size": 896, "initializer_range": 0.02, "intermediate_size": 4864,
    "max_position_embeddings": 32768, "max_window_layers": 21, "model_type": "qwen2",
    "num_attention_heads": 14, "num_hidden_layers": 24, "num_key_value_heads": 2,
    "rms_norm_eps": 1e-6, "rope_theta": 1000000.0, "sliding_window": 32768,
    "tie_word_embeddings": True, "torch_dtype": "bfloat16",
    "transformers_version": "4.43.1", "use_cache": True,
    "use_sliding_window": False, "vocab_size": 151936,
}
SAVED_CONFIG = {k: v for k, v in ORIGINAL_CONFIG.items() if k != "torch_dtype"}
SAVED_CONFIG.update(dtype="float32", transformers_version="4.57.6", use_cache=False,
                    tie_word_embeddings=False, sliding_window=None, rope_scaling=None,
                    layer_types=["full_attention"] * 24)
SCOPE = {
    "original_unique_parameters": 494032768, "original_unique_tensors": 290,
    "original_requires_grad_false": True, "original_gradients_none": True,
    "original_optimizer_members": 0, "original_weight_decay_members": 0,
    "backbone_eval": True, "trainable_parameters": 5376, "optimizer_parameter_tensors": 1,
    "optimizer_only_W6": True, "head_disjoint_from_all_original_storage": True,
    "head_bias": False, "feature_cache": False, "backbone_context": "torch.no_grad",
    "projection_outside_backbone_no_grad": True,
}
RECIPE = {
    "schema_version": "m8.recipe.v1", "seed": 42, "train_rows": 1500,
    "epochs": 1, "microbatch": 1, "accumulation": 4, "updates": 375,
    "optimizer": "AdamW", "learning_rate": 2e-6, "betas": [0.9, 0.999],
    "epsilon": 1e-8, "weight_decay": 0.01, "gradient_clip": 1.0, "foreach": False,
    "max_input_tokens": 1024, "maximum_run_seconds": 2700, "maximum_capacity_seconds": 600,
}
M12_RECIPE = {
    **RECIPE, "schema_version": "m12.recipe.v1", "learning_rate": 0.0002,
    "maximum_run_seconds": 590,
}
RECIPE_PROFILES = {
    "m8.recipe.v1": ("m8.train.v1", RECIPE),
    "m12.recipe.v1": ("m12.train.v1", M12_RECIPE),
}


def _same(left, right):
    # JSON equality alone accepts True as 1, including inside shapes/metadata.
    if type(left) is not type(right):
        return False
    if isinstance(right, dict):
        return left.keys() == right.keys() and all(_same(left[k], v) for k, v in right.items())
    if isinstance(right, list):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _hash(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _finite(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def _parameter_shapes():
    shapes = {"model.embed_tokens.weight": [151936, 896], "model.norm.weight": [896]}
    for i in range(24):
        prefix = f"model.layers.{i}."
        for name, width in (("q_proj", 896), ("k_proj", 128), ("v_proj", 128)):
            shapes[prefix + "self_attn." + name + ".weight"] = [width, 896]
            shapes[prefix + "self_attn." + name + ".bias"] = [width]
        shapes[prefix + "self_attn.o_proj.weight"] = [896, 896]
        for name, shape in (("gate_proj", [4864, 896]), ("up_proj", [4864, 896]),
                            ("down_proj", [896, 4864])):
            shapes[prefix + "mlp." + name + ".weight"] = shape
        for name in ("input_layernorm", "post_attention_layernorm"):
            shapes[prefix + name + ".weight"] = [896]
    return shapes


def _record(record, shape, require):
    require(isinstance(record, dict) and set(record) == {"shape", "dtype", "bytes", "sha256"},
            "invalid canonical tensor record fields")
    require(_same(record["shape"], shape) and record["dtype"] == "float32" and
            type(record["bytes"]) is int and record["bytes"] == 4 * math.prod(shape) and
            _hash(record["sha256"]), "invalid canonical tensor shape/dtype/bytes/hash")


def _materialized(config, tied, require):
    require(isinstance(config, dict), "materialized configuration required")
    expected = {**SAVED_CONFIG, "tie_word_embeddings": tied}
    # HF to_dict includes defaults, but original architecture and scoring cannot change.
    for key, value in expected.items():
        require(key in config and _same(config[key], value), f"materialized config {key}")
    require("torch_dtype" not in config, "materialized dtype must use canonical dtype field")


def validate_metadata(manifest_path, model_dir, manifest, receipt_path, *,
                      require, load, digest, safe_path):
    """Validate only metadata and referenced file hashes, never TRAIN row content."""
    from jeff.model import qwen_readout_proof as canonical
    from jeff.runtime import qwen_safetensors

    require(_same(canonical.export_config(ORIGINAL_CONFIG), SAVED_CONFIG),
            "producer/runtime controlled config transform differs")
    root = manifest_path.parent

    def reference(ref, *, sibling=False):
        require(isinstance(ref, dict) and isinstance(ref.get("path"), str) and
                ref["path"].strip() and _hash(ref.get("sha256")), "invalid proof file reference")
        raw = root / ref["path"]
        require(not raw.is_symlink(), "proof reference must not be a symlink")
        path = safe_path(raw)
        require(stat.S_ISREG(path.stat().st_mode), "proof reference must be regular")
        require(not path.is_relative_to(model_dir), "proof evidence must be outside HF directory")
        if sibling:
            require(path.parent == root, "readout proof must be a sibling of HF directory")
        require(digest(path) == ref["sha256"], "proof reference hash mismatch")
        return path

    require(manifest.get("adaptation_kind") == ADAPTATION and
            manifest.get("representation") == REPRESENTATION, "unsupported v2 adaptation/representation")
    ref = manifest.get("readout_proof")
    require(isinstance(ref, dict) and set(ref) == {"path", "sha256"}, "v2 proof reference required")
    path = reference(ref, sibling=True)
    require(reference(manifest["source_run_receipt"]) == receipt_path,
            "source receipt reference changed")
    p = load(path)
    fields = ("schema_version status adaptation_kind representation answer_token_ids answer_symbols "
              "hidden_size vocab_size dtype bias tie_word_embeddings original_base_assets "
              "original_base_model_id original_base_revision backbone_before backbone_after "
              "backbone_export scope_before scope_after export_storage output_before output_after "
              "learned_head original_config materialized_config_before materialized_config_after "
              "config_diff saved_config start_binding final_binding starting_control_source "
              "completed_training qualification").split()
    require(isinstance(p, dict) and set(p) == set(fields), "unsupported readout proof field tree")
    fixed = {"schema_version": "jeff.qwen-readout-proof.v1", "status": "complete",
             "adaptation_kind": ADAPTATION, "representation": REPRESENTATION,
             "answer_symbols": list("ABCDEF"), "answer_token_ids": list(range(32, 38)),
             "hidden_size": 896, "vocab_size": 151936, "dtype": "float32", "bias": False,
             "tie_word_embeddings": False, "original_base_assets": ORIGINAL_ASSETS,
             "original_base_model_id": MODEL, "original_base_revision": REVISION,
             "scope_before": SCOPE, "scope_after": SCOPE,
             "export_storage": {"input_output_disjoint": True, "head_output_disjoint": True,
                                "independent_full_vocab_parameter": True},
             "original_config": ORIGINAL_CONFIG, "saved_config": SAVED_CONFIG,
             "config_diff": {"tie_word_embeddings": {"before": True, "after": False}}}
    for key, value in fixed.items():
        require(_same(p[key], value), f"invalid readout proof {key}")
    require(isinstance(p["qualification"], str) and p["qualification"].strip(),
            "proof qualification required")
    _materialized(p["materialized_config_before"], True, require)
    _materialized(p["materialized_config_after"], False, require)
    require(_same({**p["materialized_config_before"], "tie_word_embeddings": False},
                  p["materialized_config_after"]), "uncontrolled materialized config diff")
    actual_config = load(model_dir / "config.json")
    require(_same(actual_config, SAVED_CONFIG), "actual saved config differs from controlled P3 transform")
    backbone = p["backbone_before"]
    shapes = _parameter_shapes()
    require(isinstance(backbone, dict) and set(backbone) == {"parameters", "fixed_buffers"},
            "invalid backbone proof")
    for section, expected in (("parameters", shapes),
                              ("fixed_buffers", {"model.rotary_emb.inv_freq": [32]})):
        records = backbone[section]
        require(isinstance(records, dict) and set(records) == set(expected), "incomplete canonical backbone names")
        for name, shape in expected.items():
            _record(records[name], shape, require)
    require(sum(r["bytes"] // 4 for r in backbone["parameters"].values()) == 494032768 and
            len(backbone["parameters"]) == 290, "original parameter scope mismatch")
    require(_same(backbone, p["backbone_after"]) and _same(backbone, p["backbone_export"]),
            "producer backbone changed")
    for key in ("output_before", "output_after"):
        out = p[key]
        require(isinstance(out, dict) and set(out) ==
                {"full_head", "ordered_answer_rows", "answer_rows", "nonanswer_rows"}, "invalid output proof")
        for name, shape in (("full_head", [151936, 896]), ("ordered_answer_rows", [6, 896]),
                            ("nonanswer_rows", [151930, 896])):
            _record(out[name], shape, require)
        require(isinstance(out["answer_rows"], dict) and
                set(out["answer_rows"]) == {str(i) for i in p["answer_token_ids"]}, "incomplete answer row proof")
        for record in out["answer_rows"].values():
            _record(record, [896], require)
    require(_same(p["output_before"]["full_head"], backbone["parameters"]["model.embed_tokens.weight"]) and
            _same(p["output_before"]["nonanswer_rows"], p["output_after"]["nonanswer_rows"]),
            "original output/non-answer identity mismatch")
    head = p["learned_head"]
    require(isinstance(head, dict) and set(head) == set((
        "path sha256 initial learned movement_l2 movement_max_absolute initial_l2 learned_l2 "
        "optimizer_steps optimizer_step_attempts qualification").split()), "invalid learned head evidence")
    reference(head)
    require(isinstance(head["qualification"], str) and head["qualification"].strip(),
            "learned head qualification required")
    for key, out in (("initial", "output_before"), ("learned", "output_after")):
        _record(head[key], [6, 896], require)
        require(_same(head[key], p[out]["ordered_answer_rows"]), "learned/initial ordered row mismatch")
    for key in ("movement_l2", "movement_max_absolute", "initial_l2", "learned_l2"):
        require(_finite(head[key]), "nonfinite head norm/movement")
    require(type(head["optimizer_steps"]) is int and head["optimizer_steps"] == 375 and
            type(head["optimizer_step_attempts"]) is int and head["optimizer_step_attempts"] == 375,
            "incomplete learned head steps")
    for key, scope in (("start_binding", "START: W6 vs retained M7 original-base prefit"),
                       ("final_binding", "FINAL: W6 vs actual untied stock-shaped full-V lm_head, same hidden state")):
        binding = p[key]
        expected = {"scope": scope, "rows": 1500, "status": "complete", "finite_full_coverage": True,
                    "logit_tolerance": 1e-4, "probability_tolerance": 1e-6,
                    "identical_probability_top_sets": True, "identical_logit_top_sets": True}
        require(isinstance(binding, dict) and set(binding) == set(expected) | {
            "max_absolute_logit_difference", "max_absolute_probability_difference", "rowwise_proof",
            "fit_rows", "mean_ce", "agreements"}, "invalid START/FINAL field tree")
        require(all(_same(binding.get(k), v) for k, v in expected.items()), "incomplete or relaxed START/FINAL")
        for kind, tolerance in (("logit", 1e-4), ("probability", 1e-6)):
            delta = binding[f"max_absolute_{kind}_difference"]
            require(_finite(delta) and delta <= tolerance, "START/FINAL exceeds fixed tolerance")
        require(_finite(binding["mean_ce"]) and type(binding["agreements"]) is int and
                0 <= binding["agreements"] <= 1500, "invalid TRAIN summary")
        for name in ("rowwise_proof", "fit_rows"):
            require(isinstance(binding[name], dict) and set(binding[name]) == {"path", "sha256"},
                    "invalid binding file reference fields")
            reference(binding[name])
    training = p["completed_training"]
    require(isinstance(training, dict) and set(training) == {
        "presentations", "optimizer_steps", "optimizer_step_attempts", "scope", "schedule_sha256",
        "gradient_norms", "online", "adam_final_state"}, "invalid completed training fields")
    for key, value in {"presentations": 1500, "optimizer_steps": 375, "optimizer_step_attempts": 375,
                       "scope": "TRAIN only; one epoch; W6 only", "schedule_sha256": SCHEDULE,
                       "adam_final_state": {"state_tensors": 1, "moment_bytes": 43008, "step": 375}}.items():
        require(_same(training[key], value), f"incomplete training {key}")
    for key, count_key, count in (("gradient_norms", "values", 375), ("online", "rows", 1500)):
        item = training[key]
        require(isinstance(item, dict) and set(item) == {"path", "sha256", count_key} and
                _same(item[count_key], count), "invalid training file coverage")
        reference(item)
    control = p["starting_control_source"]
    require(isinstance(control, dict) and set(control) == {
        "path", "sha256", "receipt", "source", "schedule_sha256", "scope"} and
        control["sha256"] == CONTROL and control["schedule_sha256"] == SCHEDULE and
        control["scope"] == "1500 original-P3 TRAIN prefit rows; not M7 learned weights" and
        isinstance(control["receipt"], dict) and set(control["receipt"]) == {"path", "sha256"} and
        control["receipt"].get("sha256") == CONTROL_RECEIPT, "wrong original control pins")
    reference(control)
    historical = load(reference(control["receipt"]))
    require(historical["schema_version"] == "m7.train.v1" and historical["status"] == "complete" and
            _same(historical["optimizer_steps"], 375) and _same(historical["presentations"], 1500) and
            historical["identity"]["schedule_sha256"] == SCHEDULE and
            historical["fit_before"]["rows_sha256"] == CONTROL and
            _same(historical["fit_before"]["overall"]["rows"], 1500) and
            _same(control["source"], historical["identity"]["evidence"]["source"]), "wrong retained M7 receipt")
    receipt = load(receipt_path)
    require(isinstance(receipt.get("base_loading_info"), dict) and
            all(receipt["base_loading_info"].get(k) == [] for k in
                ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")),
            "producer original-base load diagnostics are incomplete or nonzero")
    recipe = receipt["identity"]["evidence"]["recipe"]
    require(isinstance(recipe, dict) and isinstance(recipe.get("schema_version"), str) and
            recipe["schema_version"] in RECIPE_PROFILES, "unsupported readout recipe profile")
    receipt_schema, expected_recipe = RECIPE_PROFILES[recipe["schema_version"]]
    require(receipt["schema_version"] == receipt_schema and receipt["status"] == "complete" and
            receipt["command"] == "train" and _same(receipt["extra_backwards"], 0),
            "incomplete source receipt or receipt/profile mismatch")
    if receipt_schema == "m12.train.v1":
        require(_same(receipt.get("backbone_forwards"), {
            "maximum": 4500, "attempted": 4500, "completed": 4500,
            "by_phase": {phase: {"attempted": 1500, "completed": 1500}
                         for phase in ("START", "TRAIN", "FINAL")},
        }), "M12 requires exactly 4500 complete backbone calls in the fixed phases")

    for key in ("presentations", "optimizer_steps", "optimizer_step_attempts", "gradient_norms", "online", "adam_final_state"):
        require(_same(receipt[key], training[key]), f"receipt training crosslink {key}")
    for key, proof_key in (("fit_before", "start_binding"), ("fit_after", "final_binding"),
                           ("parameters", "scope_before"), ("learned_head", "learned_head"),
                           ("starting_control_source", "starting_control_source")):
        require(_same(receipt[key], p[proof_key]), f"receipt proof crosslink {key}")
    require(_same(receipt["readout_proof"], ref) and _same(receipt["checkpoint_files"], manifest["files"]) and
            _same(receipt["tokenizer_assets"], manifest["tokenizer_assets"]), "receipt manifest crosslinks")
    producer_dir = Path(receipt["output_dir"])
    producer_id = producer_dir.parent.name + "/" + producer_dir.name
    require(manifest["run_id"] == producer_id and manifest["checkpoint_id"] == producer_id + "-checkpoint",
            "receipt manifest run/checkpoint identity mismatch")
    identity = receipt["identity"]
    evidence = identity["evidence"]
    for key, value in {"base_model_id": MODEL, "base_revision": REVISION, "model_assets": ORIGINAL_ASSETS,
                       "tokenizer_assets": TOKENIZERS, "p3_scoring_config_sha256": SCORING_SHA256}.items():
        require(_same(evidence[key], value), f"receipt original evidence {key}")
    require(identity["schedule_sha256"] == manifest["training_schedule_sha256"] == SCHEDULE and
            evidence["source"]["revision"] == manifest["training_code_revision"] and
            evidence["recipe_sha256"] == manifest["training_recipe_sha256"] and
            evidence["data"]["manifest_sha256"] == manifest["training_data_manifest_sha256"] == DATA,
            "receipt manifest training identity mismatch")
    guards = {"max_cpu_rss_bytes": 16 * 2**30, "max_mps_driver_bytes": 16 * 2**30,
              "min_recommended_headroom_bytes": 2 * 2**30}
    require(set(recipe) == set(expected_recipe) | set(guards) and
            all(_same(recipe[k], v) for k, v in expected_recipe.items()),
            "changed readout profile recipe")
    for key, bound in guards.items():
        value = recipe[key]
        require(type(value) is int and value > 0 and
                (value >= bound if key.startswith("min_") else value <= bound), "relaxed recipe guard")
    recipe_path = reference({"path": evidence["recipe_path"], "sha256": evidence["recipe_sha256"]})
    require(_same(load(recipe_path), recipe), "recipe file and evidence differ")
    require(evidence["source"]["tracked_files"]["src/jeff/model/qwen_readout_proof.py"] ==
            digest(Path(canonical.__file__).resolve()), "producer/runtime canonical helper source mismatch")
    excluded = {"source", "recipe", "recipe_path", "recipe_sha256"}
    require(_same({k: v for k, v in evidence.items() if k not in excluded},
                  {k: v for k, v in historical["identity"]["evidence"].items() if k not in excluded}),
            "original control evidence identity changed")
    serialized = {**backbone["parameters"], "lm_head.weight": p["output_after"]["full_head"]}
    header = qwen_safetensors.inspect_header(model_dir / "model.safetensors", serialized, require=require)
    require(_same(receipt["saved_metadata"]["config"], actual_config) and
            _same(receipt["saved_metadata"]["tensor_header"], header["tensors"]), "saved metadata receipt mismatch")
    return {"proof": p, "path": str(path), "sha256": ref["sha256"],
            "validator_source_sha256": digest(SOURCE),
            "canonical_helper_source_sha256": digest(Path(canonical.__file__).resolve()),
            "serialized_header_source_sha256": digest(qwen_safetensors.SOURCE),
            "saved_config": actual_config, "serialized_header": header,
            "qualification": "Historical producer attestations plus file/config/header checks; no training replay or tensor load."}


def validate_answer_ids(binding, answers, *, require):
    ids = binding["readout_proof"]["proof"]["answer_token_ids"]
    require(isinstance(answers, (list, tuple)) and 2 <= len(answers) <= 6 and
            all(type(i) is int for i in answers) and list(answers) == ids[:len(answers)],
            "actual answers must be exact K2..6 prefix of proof A-F IDs")


def validate_storage(model, *, require):
    """Inspect actual allocator-owned storage, including after migration."""
    from jeff.model import qwen_readout_proof as canonical

    require(type(model).__name__ == "Qwen2ForCausalLM" and
            type(model.model).__name__ == "Qwen2Model" and
            type(model.model.embed_tokens).__name__ == "Embedding" and
            type(model.lm_head).__name__ == "Linear", "unsupported actual model/module classes")
    require(model.config.tie_word_embeddings is False and model.lm_head.bias is None and
            model.get_input_embeddings() is model.model.embed_tokens and
            model.get_output_embeddings() is model.lm_head, "wrong untied module/getter configuration")
    tables = {"input": model.get_input_embeddings().weight, "output": model.get_output_embeddings().weight}
    result = {}
    for name, weight in tables.items():
        require(str(weight.dtype) == "torch.float32" and list(weight.shape) == [151936, 896] and
                weight.device.type in ("cpu", "mps") and weight.is_contiguous() and
                weight.storage_offset() == 0 and tuple(weight.stride()) == (896, 1), "invalid actual full FP32 table")
        storage = weight.untyped_storage()
        base, size = storage.data_ptr(), storage.nbytes()
        extent = weight.numel() * weight.element_size()
        require(type(base) is int and base > 0 and size >= extent == 544538624,
                "invalid table backing storage extent")
        result[name] = {"device": str(weight.device), "dtype": "float32", "shape": list(weight.shape),
                        "stride": list(weight.stride()), "storage_offset": weight.storage_offset(),
                        "storage_token": base, "storage_bytes": size, "tensor_bytes": extent}
    require(tables["input"].device == tables["output"].device and
            canonical.storage_disjoint(tables["input"], tables["output"]),
            "input/output must have independent disjoint same-device backing allocations")
    semantics = ("distinct opaque allocator-owned MTLBuffer handles" if
                 tables["input"].device.type == "mps" else "disjoint CPU backing byte intervals")
    return {**result, "input_output_disjoint": True, "storage_identity_semantics": semantics}


def validate_loaded(model, binding, loading_info, *, require, guard):
    """Hash the actual scored MPS model with the producer's bounded helper; no forwards."""
    from jeff.model import qwen_readout_proof as canonical

    guard()
    p = binding["readout_proof"]["proof"]
    require(isinstance(loading_info, dict) and all(k in loading_info and loading_info[k] == [] for k in
            ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")), "nonzero/missing HF diagnostics")
    storage = validate_storage(model, require=require)
    device = model.lm_head.weight.device
    require(device.type == "mps", "actual scored readout must be on MPS")
    _materialized(model.config.to_dict(), False, require)
    expected_parameters = {**p["backbone_before"]["parameters"], "lm_head.weight": p["output_after"]["full_head"]}
    expected_buffers = p["backbone_before"]["fixed_buffers"]

    def coverage():
        parameters = list(model.named_parameters(remove_duplicate=False))
        buffers = list(model.named_buffers(remove_duplicate=False))
        for items, expected in ((parameters, expected_parameters), (buffers, expected_buffers)):
            require(len(items) == len(expected) and {name for name, _ in items} == set(expected),
                    "actual parameter/buffer name coverage mismatch (including aliases)")
            for name, value in items:
                record = expected[name]
                require(list(value.shape) == record["shape"] and str(value.dtype) == "torch.float32" and
                        value.device == device and not value.is_meta and value.is_contiguous(),
                        "actual parameter/buffer geometry/dtype/device mismatch")
        require(not getattr(model, "hf_device_map", None) and
                all(not hasattr(module, "_hf_hook") for module in model.modules()), "offloaded model prohibited")
        state = model.state_dict()
        raw = binding["readout_proof"]["serialized_header"]["tensors"]
        require(set(state) == set(raw) == set(expected_parameters), "raw serialized/live state keyset mismatch")
        for name, value in state.items():
            require(list(value.shape) == raw[name]["shape"] and str(value.dtype) == "torch.float32" and
                    raw[name]["dtype"] == "F32" and value.device == device and not value.is_meta,
                    "raw serialized/live tensor geometry mismatch")
        return {"parameters": [name for name, _ in parameters], "fixed_buffers": [name for name, _ in buffers],
                "serialized_state": sorted(state)}

    names = coverage()
    backbone = canonical.backbone_records(model, lambda stage: guard())
    require(all(_same(backbone, p[key]) for key in ("backbone_before", "backbone_after", "backbone_export")),
            "actual loaded backbone differs from producer before/after/export")
    output = canonical.output_records(model.lm_head.weight, p["answer_token_ids"], lambda stage: guard())
    require(_same(output, p["output_after"]), "actual loaded head differs from producer export")
    require(_same(names, coverage()), "actual name coverage changed during canonical hashing")
    guard()
    return {"loading_info": loading_info, "names": names, "backbone": backbone, "output": output,
            "storage": storage, "config": model.config.to_dict(),
            "qualification": "Actual reloaded MPS identities/storage verified without forwards; producer frozen/optimizer/START/FINAL claims remain historical attestations."}
