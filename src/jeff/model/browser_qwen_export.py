"""Explicitly activated, local-only M10 -> FP16 six-logit ONNX export.

Importing this module uses only the standard library. Actual execution belongs
in the separately supervised BROWSER-B2 job, never in source review.
"""

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import inspect
import json
import math
import os
from pathlib import Path
import platform
import resource
import shutil
import signal
import sys
import time


CHECKPOINT = Path("/Users/destiner/Code/jeff/artifacts/model/m10-qwen-seed7-20261112-02/training/checkpoint")
INPUTS = Path("/private/tmp/jeff-p11-20261112-01/kit/m9-bundle/demo/inputs.jsonl")
MANIFEST_SHA256 = "765d802270b8c0b090e9206c3e52f12e76ea7e224dbb4f07c9cc3c709aa6b15a"
WEIGHTS_SHA256 = "751ecdc0433b21d200af0e38966b5b28107dc9ff2267977f0eae2e936cb5131d"
WEIGHTS_BYTES = 1976163472
INPUTS_SHA256 = "26015911424707f5c9194201d0d9ad3342e0af71399ceefe9e9a4924491e3437"
SYSTEM = "You are a decision assistant. Choose exactly one of the listed options. Reply with only its letter."
USER = "State:\n{state}\n\nQuestion:\n{question}\n\nOptions:\n{options}"
LETTERS = "ABCDEF"
ACTIVATION = "BROWSER-B2-M10-FP16"
EXPORT_CUTOFF = datetime(2026, 11, 12, 12, 40, tzinfo=timezone.utc).timestamp()
STOP_CUTOFF = datetime(2026, 11, 12, 13, 10, tzinfo=timezone.utc).timestamp()
MAX_RSS = 12 * 2**30
ASSETS = ("config.json", "generation_config.json", "tokenizer.json",
          "tokenizer_config.json", "vocab.json", "merges.txt", "LICENSE", "README.md")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path):
    return json.loads(path.read_text())


def immutable_json(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    path.chmod(0o444)


def rss_bytes():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return rss if sys.platform == "darwin" else rss * 1024


def utc_timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "deadline must include a timezone")
    return parsed.timestamp()


class Job:
    def __init__(self, root, deadline, timeout):
        self.root = root
        self.started = time.monotonic()
        self.deadline = min(deadline, time.time() + timeout)
        self.receipt = {
            "schema_version": "jeff.browser-b2.export.v1", "status": "running",
            "stage": "created", "started_utc": datetime.now(timezone.utc).isoformat(),
            "deadline_utc": datetime.fromtimestamp(self.deadline, timezone.utc).isoformat(),
            "reference_forwards": {"entered": 0, "completed": 0},
            "tracing_forwards": {"entered": 0, "completed": 0},
            "native_partial_rows": [], "stages": [], "artifacts": {},
            "memory_qualification": "Child stage ru_maxrss guard only; parent must sample RSS and enforce whole-job bounds.",
        }
        self.persist()

    def persist(self):
        self.receipt["elapsed_seconds"] = time.monotonic() - self.started
        self.receipt["lifetime_maxrss_bytes"] = rss_bytes()
        pending = self.root / "receipt.pending.json"
        with pending.open("w") as stream:
            json.dump(self.receipt, stream, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        pending.replace(self.root / "receipt.json")

    def guard(self):
        require(time.time() < self.deadline, "job deadline exceeded")
        require(rss_bytes() <= MAX_RSS, "12 GiB lifetime RSS guard exceeded")

    def stage(self, name):
        self.receipt["stage"] = name
        self.receipt["stages"].append({"stage": name, "elapsed_seconds": time.monotonic() - self.started,
                                       "lifetime_maxrss_bytes": rss_bytes()})
        self.persist()
        self.guard()

    def enter(self, kind, maximum):
        self.guard()
        counter = self.receipt[kind + "_forwards"]
        require(counter["entered"] < maximum, kind + " forward budget exhausted")
        counter["entered"] += 1
        self.persist()

    def complete(self, kind):
        self.receipt[kind + "_forwards"]["completed"] += 1
        self.persist()
        self.guard()

    def inventory(self, path):
        name = str(path.relative_to(self.root))
        require(name not in self.receipt["artifacts"], "artifact already hashed")
        self.guard()
        self.receipt["artifacts"][name] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        self.persist()
        self.guard()


def provenance(args, job):
    require(args.checkpoint.resolve() == CHECKPOINT, "only exact trained M10 checkpoint allowed")
    require(args.inputs.resolve() == INPUTS, "only exact P11 three-input file allowed")
    manifest_path = CHECKPOINT.parent / "checkpoint-manifest.json"
    require(sha256(manifest_path) == MANIFEST_SHA256, "checkpoint manifest hash mismatch")
    manifest = load(manifest_path)
    require(manifest["status"] == "complete" and manifest["kind"] == "trained" and
            manifest["schema_version"] == "jeff.qwen-trained-checkpoint.v1", "trained v1 manifest required")
    weight = manifest["files"]["model.safetensors"]
    require(weight == {"sha256": WEIGHTS_SHA256, "bytes": WEIGHTS_BYTES}, "weight inventory mismatch")
    require((CHECKPOINT / "model.safetensors").stat().st_size == WEIGHTS_BYTES, "weight size mismatch")
    require(sha256(INPUTS) == INPUTS_SHA256, "P11 inputs hash mismatch")
    rows = [json.loads(line) for line in INPUTS.read_text().splitlines()]
    require(len(rows) == 3 and len({r["id"] for r in rows}) == 3, "exactly three unique inputs required")
    for row in rows:
        require(set(row) == {"schema_version", "id", "state", "question", "options"} and
                row["schema_version"] == "0.1", "decision-only input fields required")
        require(2 <= len(row["options"]) <= 6, "only A-F choice coverage supported")
        require(all(set(o) == {"id", "text"} for o in row["options"]), "decision-only option fields required")
    assets_dir = job.root / "assets"
    assets_dir.mkdir()
    # Copy only small declared assets; never copy or hash the native weight file.
    for name in ASSETS:
        source, target = CHECKPOINT / name, assets_dir / name
        require(source.stat().st_size == manifest["files"][name]["bytes"], "source asset size mismatch: " + name)
        shutil.copyfile(source, target)
        target.chmod(0o444)
        job.inventory(target)
        require(job.receipt["artifacts"]["assets/" + name]["sha256"] ==
                manifest["files"][name]["sha256"], "source asset hash mismatch: " + name)
    target_manifest = job.root / "source-checkpoint-manifest.json"
    shutil.copyfile(manifest_path, target_manifest)
    target_manifest.chmod(0o444)
    job.inventory(target_manifest)
    require(job.receipt["artifacts"][target_manifest.name]["sha256"] == MANIFEST_SHA256,
            "copied manifest mismatch")
    config = load(assets_dir / "config.json")
    require(config["model_type"] == "qwen2" and config["architectures"] == ["Qwen2ForCausalLM"] and
            config["hidden_size"] == 896 and config["vocab_size"] == 151936 and
            config["num_hidden_layers"] == 24 and config["tie_word_embeddings"] is True and
            set(config["layer_types"]) == {"full_attention"} and config["rope_scaling"] is None,
            "unsupported M10 architecture")
    binding = {"checkpoint_path": str(CHECKPOINT), "checkpoint_manifest_sha256": MANIFEST_SHA256,
               "weights_sha256": WEIGHTS_SHA256, "weights_bytes": WEIGHTS_BYTES,
               "weight_identity_method": "Existing pinned manifest inventory plus stat; native weight bytes NOT rehashed.",
               "inputs_path": str(INPUTS), "inputs_sha256": INPUTS_SHA256,
               "system": SYSTEM, "user_template": USER, "symbols": LETTERS,
               "native_dtype": "float32", "native_attention": "sdpa", "device": "cpu",
               "threads": 4, "temperature": 1.0, "logits_to_keep": 1, "max_input_tokens": 1024,
               "add_generation_prompt": True, "add_special_tokens": False, "truncation": False,
               "tokenizer_assets": manifest["tokenizer_assets"]}
    job.receipt["binding"] = binding
    job.persist()
    return rows, binding


def prepare(tokenizer, rows):
    require(isinstance(tokenizer.chat_template, str) and tokenizer.chat_template, "official chat template required")
    prepared = []
    for row in rows:
        content = [row["state"], row["question"], *(o["text"] for o in row["options"])]
        require(not any(special in text for special in tokenizer.all_special_tokens for text in content),
                "special-token string in input content")
        user = USER.format(state=row["state"], question=row["question"], options="\n".join(
            f"{letter}. {option['text']}" for letter, option in zip(LETTERS, row["options"])))
        rendered = tokenizer.apply_chat_template(
            [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            tokenize=False, add_generation_prompt=True)
        prompt = tokenizer.encode(rendered, add_special_tokens=False, truncation=False)
        require(0 < len(prompt) <= 1024, "prompt exceeds frozen 1024 cap; no truncation")
        answers = []
        for letter in LETTERS:
            complete = tokenizer.encode(rendered + letter, add_special_tokens=False, truncation=False)
            require(len(complete) == len(prompt) + 1 and complete[:-1] == prompt,
                    "answer suffix must be identical prefix plus exactly one token")
            answers.append(complete[-1])
        require(len(set(answers)) == 6, "six distinct answer token IDs required")
        prepared.append({"id": row["id"], "prompt_text": rendered, "input_ids": prompt,
                         "answer_token_ids": answers,
                         "option_mapping": [{"letter": LETTERS[i], "token_id": answers[i],
                                             "option_id": option["id"], "text": option["text"]}
                                            for i, option in enumerate(row["options"])]})
    require(all(p["answer_token_ids"] == prepared[0]["answer_token_ids"] for p in prepared),
            "A-F token IDs must be identical across the three prompts")
    return prepared


def validate_reference(reference, binding, prepared, versions):
    require(reference.get("schema_version") == "jeff.browser-b2.native-references.v1" and
            reference.get("status") == "complete" and reference.get("binding") == binding and
            reference.get("versions") == versions and reference.get("forwards") == {"entered": 3, "completed": 3},
            "reuse requires complete matching pinned native reference and environment")
    require(len(reference.get("rows", [])) == 3, "reuse requires all three reference rows")
    for saved, current in zip(reference["rows"], prepared):
        require(all(saved.get(key) == value for key, value in current.items()), "reuse prompt/token/mapping mismatch")
        logits, probabilities = saved["native_logits_six"], saved["native_probabilities"]
        k = len(current["option_mapping"])
        require(len(logits) == 6 and all(math.isfinite(v) for v in logits) and len(probabilities) == k and
                all(math.isfinite(v) and 0 <= v <= 1 for v in probabilities) and
                abs(sum(probabilities) - 1) <= 1e-6, "invalid frozen reference numbers")
        maximum = max(logits[:k])
        exps = [math.exp(v - maximum) for v in logits[:k]]
        expected = [v / sum(exps) for v in exps]
        require(max(abs(a - b) for a, b in zip(expected, probabilities)) <= 1e-6,
                "reference probabilities not choice-restricted T1 softmax")
    require(reference.get("loading_info") is not None and reference.get("parameter_metadata") is not None,
            "reference load diagnostics and tying metadata required")


def execute(args, job):
    job.stage("validate_provenance_and_copy_assets")
    rows, binding = provenance(args, job)
    versions = {"python": sys.version, "platform": platform.platform(),
                "packages": {name: version(name) for name in ("torch", "transformers", "onnx", "safetensors", "tokenizers")}}
    job.receipt["versions"] = versions
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", TOKENIZERS_PARALLELISM="false",
                      OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", OPENBLAS_NUM_THREADS="4")
    job.stage("import_ml_stack")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(4)
    torch.set_num_interop_threads(4)
    job.stage("prepare_exact_three")
    tokenizer = AutoTokenizer.from_pretrained(str(CHECKPOINT), local_files_only=True, trust_remote_code=False)
    prepared = prepare(tokenizer, rows)
    job.receipt["chat_template_sha256"] = hashlib.sha256(tokenizer.chat_template.encode()).hexdigest()
    reference = None
    if args.reuse_native_references is not None:
        require(args.reuse_native_references.is_file() and
                args.reuse_native_references.stat().st_mode & 0o222 == 0,
                "reuse reference must be an existing read-only immutable file")
        reference = load(args.reuse_native_references)
        validate_reference(reference, binding, prepared, versions)
        job.receipt["reference_mode"] = "explicit_reuse_no_native_forwards"
        job.receipt["reused_reference_path"] = str(args.reuse_native_references.resolve())
    else:
        job.receipt["reference_mode"] = "one_pass_exactly_three"
    job.stage("load_actual_trained_m10_fp32_sdpa")
    model, loading_info = AutoModelForCausalLM.from_pretrained(
        str(CHECKPOINT), local_files_only=True, trust_remote_code=False,
        use_safetensors=True, torch_dtype=torch.float32, attn_implementation="sdpa",
        output_loading_info=True, ignore_mismatched_sizes=False)
    job.receipt["loading_info"] = loading_info
    job.persist()
    require(isinstance(loading_info, dict) and all(loading_info.get(key) == [] for key in
            ("missing_keys", "unexpected_keys", "mismatched_keys", "error_msgs")), "strict load diagnostics must be empty")
    require("logits_to_keep" in inspect.signature(model.forward).parameters, "last-boundary full-head projection unsupported")
    model.requires_grad_(False).eval()
    require(all(p.dtype == torch.float32 and p.device.type == "cpu" for p in model.parameters()), "FP32 CPU native load required")
    require(model.config._attn_implementation == "sdpa", "native reference must use SDPA")
    head = model.get_output_embeddings()
    embedding = model.get_input_embeddings()
    metadata = {
        "unique_parameter_count": sum(p.numel() for p in model.parameters()),
        "named_parameter_count_including_aliases": sum(p.numel() for _, p in model.named_parameters(remove_duplicate=False)),
        "config_tie_word_embeddings": model.config.tie_word_embeddings,
        "head_embedding_same_parameter": head.weight is embedding.weight,
        "head_embedding_same_storage": head.weight.data_ptr() == embedding.weight.data_ptr(),
        "head_shape": list(head.weight.shape), "embedding_shape": list(embedding.weight.shape),
        "head_bias": head.bias is not None,
        "selection_source": "Actual strict-loaded trained M10 get_output_embeddings().weight; never base or M8/M12.",
    }
    job.receipt["parameter_metadata"] = metadata
    require(metadata["unique_parameter_count"] == 494032768 and metadata["head_embedding_same_parameter"] and
            metadata["head_embedding_same_storage"] and not metadata["head_bias"] and
            metadata["head_shape"] == [151936, 896], "unexpected M10 parameter count or tied head storage")
    job.stage("native_references")
    if reference is None:
        reference_rows = []
        with torch.inference_mode():
            for row in prepared:
                ids = torch.tensor([row["input_ids"]], dtype=torch.int64)
                job.enter("reference", 3)
                result = model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=False, logits_to_keep=1)
                job.complete("reference")
                require(tuple(result.logits.shape) == (1, 1, 151936), "native full-head last-boundary shape mismatch")
                logits = result.logits[0, 0, row["answer_token_ids"]].float()
                k = len(row["option_mapping"])
                probabilities = torch.softmax(logits[:k], dim=0).tolist()
                require(torch.isfinite(logits).all().item() and all(math.isfinite(p) and 0 <= p <= 1 for p in probabilities)
                        and abs(sum(probabilities) - 1) <= 1e-6, "nonfinite native logits or invalid probability sum")
                saved = {**row, "native_logits_six": logits.tolist(), "native_probabilities": probabilities,
                         "top_option_id": row["option_mapping"][max(range(k), key=lambda i: probabilities[i])]["option_id"]}
                reference_rows.append(saved)
                job.receipt["native_partial_rows"] = reference_rows
                job.persist()
                del result, logits, ids
        reference = {"schema_version": "jeff.browser-b2.native-references.v1", "status": "complete",
                     "binding": binding, "versions": versions, "rows": reference_rows,
                     "forwards": dict(job.receipt["reference_forwards"]), "loading_info": loading_info,
                     "parameter_metadata": metadata, "created_utc": datetime.now(timezone.utc).isoformat()}
        validate_reference(reference, binding, prepared, versions)
    else:
        require(reference["loading_info"] == loading_info and reference["parameter_metadata"] == metadata,
                "reused reference strict load or tying metadata differs")
    # This durable immutable boundary precedes *any* conversion or ONNX plumbing.
    reference_path = job.root / "native-references.json"
    immutable_json(reference_path, reference)
    job.inventory(reference_path)
    job.stage("native_references_frozen_before_conversion")
    require(time.time() <= EXPORT_CUTOFF, "12:40 UTC export-start cutoff missed")
    job.stage("convert_trained_backbone_and_selected_head_to_fp16")
    answer_ids = prepared[0]["answer_token_ids"]
    with torch.no_grad():
        selected = head.weight.index_select(0, torch.tensor(answer_ids, dtype=torch.int64)).detach().half().contiguous()
        # HF rotary computation explicitly uses FP32; avoid rounding its derived frequencies.
        rotary = model.model.rotary_emb
        inv_freq = rotary.inv_freq.detach().float().clone()
        model.half()
        rotary.inv_freq = inv_freq
        rotary.original_inv_freq = inv_freq
    model.set_attn_implementation("eager")
    require(model.model.config._attn_implementation == "eager" and
            all(layer.self_attn.config._attn_implementation == "eager" for layer in model.model.layers),
            "export-only eager attention switch failed")
    require(all(p.dtype == torch.float16 for p in model.model.parameters()), "FP16 trained backbone required")
    require(head.weight is embedding.weight and head.weight.data_ptr() == embedding.weight.data_ptr(),
            "native tying must survive FP16 conversion")
    job.receipt["fp16_parameter_metadata"] = {
        "backbone_parameter_count": sum(p.numel() for p in model.model.parameters()),
        "selected_head_shape": list(selected.shape), "selected_head_dtype": str(selected.dtype),
        "native_head_embedding_still_tied": True,
        "selected_head_is_independent_copy": selected.data_ptr() != head.weight.data_ptr(),
        "largest_embedding_fp16_bytes": embedding.weight.numel() * embedding.weight.element_size(),
    }

    class SixLogits(torch.nn.Module):
        def __init__(self, backbone, selected_rows):
            super().__init__()
            self.backbone = backbone
            self.register_buffer("selected_head_rows", selected_rows)

        def forward(self, input_ids):
            job.enter("tracing", 1)
            positions = torch.arange(input_ids.shape[1], dtype=torch.int64, device=input_ids.device)
            allowed = positions.unsqueeze(0) <= positions.unsqueeze(1)
            mask = torch.where(allowed, 0.0, torch.finfo(torch.float16).min).to(torch.float16)[None, None, :, :]
            # Explicit mapping bypasses HF4.57 mask creation/vmap, not attention itself.
            hidden = self.backbone(input_ids=input_ids, attention_mask={"full_attention": mask},
                                   position_ids=positions.unsqueeze(0), cache_position=positions,
                                   use_cache=False, return_dict=True).last_hidden_state
            logits = torch.nn.functional.linear(hidden[:, -1, :], self.selected_head_rows).float()
            job.complete("tracing")
            return logits

    wrapper = SixLogits(model.model, selected).requires_grad_(False).eval()
    job.receipt["export_contract"] = {
        "input": {"name": "input_ids", "dtype": "int64", "shape": [1, "sequence"]},
        "output": {"name": "logits", "dtype": "float32", "shape": [1, 6], "letters": LETTERS,
                   "answer_token_ids": answer_ids},
        "opset": 17, "dynamo": False, "external_data": False, "export_attention": "eager",
        "backbone_dtype": "float16", "projection_dtype": "float16", "rotary_inv_freq_dtype": "float32",
        "runtime_probability_rule": "Slice first K float32 logits in original option order; stable T1 softmax only over those K (JavaScript Number arithmetic).",
        "tying": "Native embedding/head tied; preserve complete trained embedding/backbone and copy only six actual trained head rows for FP16 projection.",
        "no_generation": True, "no_kv_cache": True,
        "acceptance": {"cases": 3, "exact_prompt_tokens_and_mapping": True,
                       "max_abs_native_browser_probability_difference": 0.01,
                       "identical_top_choices": True, "probability_sum_tolerance": 1e-6},
    }
    require(sum(p.numel() * p.element_size() for p in wrapper.parameters()) + selected.numel() * 2 < 2_000_000_000,
            "single-file export must stay below 2GB")
    job.stage("onnx_export_started")
    require(time.time() <= EXPORT_CUTOFF, "12:40 UTC export-start cutoff missed")
    output = job.root / "model.onnx"
    example = torch.tensor([prepared[0]["input_ids"]], dtype=torch.int64)
    with torch.no_grad():
        torch.onnx.export(wrapper, (example,), str(output), input_names=["input_ids"], output_names=["logits"],
                          opset_version=17, dynamo=False, external_data=False,
                          dynamic_axes={"input_ids": {1: "sequence"}},
                          do_constant_folding=True, export_params=True, keep_initializers_as_inputs=False)
    require(job.receipt["tracing_forwards"] == {"entered": 1, "completed": 1}, "exactly one tracing forward required")
    require(output.is_file() and 0 < output.stat().st_size < 2_000_000_000, "invalid single-file ONNX size")
    output.chmod(0o444)
    job.stage("hash_new_onnx_once")
    job.inventory(output)
    contract_path = job.root / "export-contract.json"
    immutable_json(contract_path, job.receipt["export_contract"])
    job.inventory(contract_path)
    job.stage("export_complete_browser_execution_not_performed")
    job.receipt["status"] = "complete"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True, help="NEW directory only; failed attempts remain intact")
    parser.add_argument("--activate", required=True, choices=[ACTIVATION])
    parser.add_argument("--deadline-utc", required=True, help="timezone-aware ISO timestamp, no later than 2026-11-12T13:10:00Z")
    parser.add_argument("--timeout-seconds", type=float, required=True, help="finite child bound <=1200; parent enforces aggregate budget")
    parser.add_argument("--reuse-native-references", type=Path, help="explicit immutable COMPLETE earlier reference; zero new native calls")
    args = parser.parse_args()
    deadline = utc_timestamp(args.deadline_utc)
    require(math.isfinite(args.timeout_seconds) and 0 < args.timeout_seconds <= 1200, "timeout must be finite and <=1200s")
    require(time.time() < deadline <= STOP_CUTOFF, "deadline expired or later than 13:10 UTC")
    require(time.time() <= EXPORT_CUTOFF, "12:40 UTC start cutoff missed")
    root = args.output_root.absolute()
    require(not root.exists() and not root.is_symlink(), "output root must be NEW")
    require(not root.resolve().is_relative_to(CHECKPOINT.parent), "output must not be inside immutable native training directory")
    root.mkdir(parents=True, exist_ok=False)
    job = Job(root, deadline, args.timeout_seconds)

    def interrupted(signum, frame):
        raise TimeoutError("child deadline or termination signal " + str(signum))

    old_handlers = {s: signal.signal(s, interrupted) for s in (signal.SIGALRM, signal.SIGTERM, signal.SIGINT)}
    signal.setitimer(signal.ITIMER_REAL, max(0.001, job.deadline - time.time()))
    code = 0
    try:
        execute(args, job)
    except BaseException as exc:
        job.receipt["status"] = "partial" if (job.receipt["reference_forwards"]["entered"] or
                                                args.reuse_native_references is not None) else "failed"
        job.receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:2000]}
        code = 1
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        for signum, handler in old_handlers.items():
            signal.signal(signum, handler)
        job.persist()
    print(json.dumps({"status": job.receipt["status"], "output_root": str(root),
                      "reference_forwards": job.receipt["reference_forwards"],
                      "tracing_forwards": job.receipt["tracing_forwards"]}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
