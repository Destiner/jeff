"""One authorized, offline CPU export attempt; imports ML only inside run()."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import time
import traceback
import warnings

ASSETS = {
    "checkpoint.json", "encoder/config.json", "encoder/model.safetensors",
    "tokenizer/tokenizer.json", "tokenizer/tokenizer_config.json",
    "tokenizer/special_tokens_map.json", "tokenizer/vocab.txt",
}
INPUTS = ("input_ids", "attention_mask", "token_type_ids")
CASE_IDS = (
    "data:pilot-v1:intent:g01:r01",
    "data:pilot-v1:sentiment-r2:g01:r01",
    "data:pilot-v1:rule_application:g01:r01",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


class Attempt:
    def __init__(self, args):
        self.args = args
        self.start = time.monotonic()
        self.out = Path(args.output).absolute()
        self.out.mkdir(parents=True, exist_ok=False)
        self.state = {
            "schema_version": "browser-b1.export.v1", "status": "running",
            "activation_id": args.activation, "activation_is_authentication": False,
            "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "arguments": vars(args), "python": sys.version, "executable": sys.executable,
            "platform": platform.platform(), "device": "cpu", "dtype": "float32",
            "threads": 4, "max_seconds": args.max_seconds, "max_rss_gib": args.max_rss_gib,
            "calls": {"export": {"entered": 0, "completed": 0},
                      "references": {"entered": 0, "completed": 0}},
            "warnings": [], "samples": [], "stage": "created",
        }
        dump(self.out / "attempt.json", self.state)
        self.event("created")

    def event(self, event, **fields):
        record = {"event": event, "elapsed_seconds": time.monotonic() - self.start, **fields}
        with (self.out / "journal.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, allow_nan=False) + "\n")
            stream.flush()
        self.state["elapsed_seconds"] = record["elapsed_seconds"]
        dump(self.out / "status.json", self.state)

    def guard(self, stage):
        self.state["stage"] = stage
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = peak if sys.platform == "darwin" else peak * 1024
        self.state["samples"].append({"stage": stage, "elapsed_seconds": time.monotonic() - self.start,
                                      "peak_rss_bytes": peak_bytes})
        self.event("resource_sample", stage=stage, peak_rss_bytes=peak_bytes)
        require(peak_bytes <= self.args.max_rss_gib * 1024**3, "sampled peak RSS exceeded limit")
        require(time.monotonic() - self.start <= self.args.max_seconds, "cooperative clock limit exceeded")

    def sha(self, path):
        digest = hashlib.sha256()
        with Path(path).open("rb") as stream:
            while block := stream.read(4 * 1024 * 1024):
                digest.update(block)
                self.guard("hashing")
        return digest.hexdigest()

    def pinned(self, path, sha):
        require(isinstance(sha, str) and len(sha) == 64, "SHA256 pin required")
        require(self.sha(path) == sha, f"SHA256 mismatch: {path}")


def run(a, attempt):
    # Set offline and resource policy before importing any ML package.
    os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
                       "HF_DATASETS_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false",
                       "OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "4",
                       "OPENBLAS_NUM_THREADS": "4", "PYTHONDONTWRITEBYTECODE": "1"})
    sys.dont_write_bytecode = True
    attempt.guard("preflight")
    attempt.state["exporter_sha256"] = attempt.sha(Path(__file__))
    for path, sha in ((a.checkpoint_pins, a.checkpoint_pins_sha256),
                      (a.input, a.input_sha256), (a.native_bindings, a.native_bindings_sha256),
                      (a.environment, a.environment_sha256)):
        attempt.pinned(path, sha)
    pins, bindings, env = load(a.checkpoint_pins), load(a.native_bindings), load(a.environment)
    require(pins["schema_version"] == "browser-b1.checkpoint.v1", "checkpoint pin schema")
    require(pins["checkpoint_identity"] == "M9-msmarco-12epoch", "exact trained M9 required")
    require(set(pins["files"]) == ASSETS, "exact seven-asset allowlist required")
    root = Path(a.checkpoint).absolute()
    require(root.is_dir() and not root.is_symlink(), "checkpoint must be a real directory")
    require(not any(p.is_symlink() for p in root.rglob("*")), "checkpoint symlink forbidden")
    require({p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()} == ASSETS,
            "unexpected or missing checkpoint assets")
    for name, sha in pins["files"].items():
        attempt.pinned(root / name, sha)
    require(bindings["schema_version"] == "browser-b1.native-bindings.v1", "native binding schema")
    require(bindings["checkpoint_pins_sha256"] == a.checkpoint_pins_sha256 and
            bindings["input_sha256"] == a.input_sha256, "binding/checkpoint/input mismatch")
    rows = [json.loads(line) for line in Path(a.input).read_text().splitlines() if line.strip()]
    require(len(rows) == 3 and {r["id"] for r in rows} == set(CASE_IDS), "exact three P11 TRAIN IDs required")
    require(bindings["case_ids"] == [r["id"] for r in rows], "bound input order mismatch")
    for row in rows:
        require(set(row) == {"schema_version", "id", "state", "question", "options"},
                "only decision fields allowed")
    source = Path(a.native_source).resolve()
    require(set(bindings["source_files"]) == {"jeff/model/cross_encoder.py", "jeff/model/scorer.py"},
            "native loader/scorer source pins required")
    for name, sha in bindings["source_files"].items():
        attempt.pinned(source / name, sha)
    reference = bindings["p11_native_reference"]
    attempt.pinned(reference["path"], reference["sha256"])
    require(env["schema_version"] == "browser-b1.environment.v1", "environment schema")
    require(sys.prefix != sys.base_prefix, "isolated environment required")
    require(Path(sys.prefix).resolve() == Path(env["prefix"]).resolve(), "environment prefix mismatch")
    require(platform.python_version() == env["python"], "Python version mismatch")
    versions = {name: importlib.metadata.version(name) for name in ("torch", "transformers", "onnx")}
    require(versions == env["packages"], "installed package versions differ from pinned environment")
    require(versions["torch"] == env["p11_packages"]["torch"] and
            versions["transformers"] == env["p11_packages"]["transformers"], "P11 stack mismatch")
    attempt.state["versions"] = versions
    attempt.state["native_source"] = str(source)
    attempt.state["source_files"] = bindings["source_files"]
    attempt.state["source_git"] = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    attempt.state["source_git_status"] = subprocess.run(
        ["git", "-C", str(source), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout
    for name, path in (("checkpoint-pins.json", a.checkpoint_pins), ("native-bindings.json", a.native_bindings),
                       ("environment.json", a.environment), ("inputs.jsonl", a.input)):
        shutil.copyfile(path, attempt.out / name)
    attempt.guard("before_ml_import")
    import torch
    import transformers
    import onnx
    require(torch.__version__ == versions["torch"] and transformers.__version__ == versions["transformers"]
            and onnx.__version__ == versions["onnx"], "imported/installed version mismatch")
    torch.set_num_threads(4)
    torch.set_num_interop_threads(4)
    require(torch.get_num_threads() == 4 and torch.get_num_interop_threads() == 4, "thread configuration mismatch")
    sys.path.insert(0, str(source))
    from jeff.model import cross_encoder, scorer
    require(Path(cross_encoder.__file__).resolve() == source / "jeff/model/cross_encoder.py"
            and Path(scorer.__file__).resolve() == source / "jeff/model/scorer.py",
            "wrong native loader/scorer imported")
    attempt.guard("before_model_tokenizer_load")
    model = cross_encoder.load_retained_checkpoint(root, load(root / "checkpoint.json"), "cpu")
    require(model.max_length == 256 and model.temperature == 1.0, "native scoring configuration mismatch")
    classifier = model.classifier_model
    require(not classifier.training and all(not m.training for m in classifier.modules()), "eval required")
    require(all(p.device.type == "cpu" and p.dtype == torch.float32 for p in classifier.parameters()),
            "native parameters must already be CPU FP32; no conversion/rescue")
    attempt.state["attention"] = {
        "configured": getattr(classifier.config, "_attn_implementation", None),
        "internal": getattr(classifier.config, "_attn_implementation_internal", None),
        "modules": sorted({type(m).__module__ + "." + type(m).__name__
                           for m in classifier.modules() if "attention" in type(m).__name__.lower()}),
    }
    attempt.state["native_class"] = type(classifier).__module__ + "." + type(classifier).__name__
    attempt.guard("loaded")
    phase = "references"
    captured = {}

    def before(module, args, kwargs):
        attempt.state["calls"][phase]["entered"] += 1
        attempt.guard(phase + "_forward_enter")
        if phase == "references":
            require(set(kwargs) == set(INPUTS) | {"return_dict"}, "native must forward exactly three inputs")
            captured["tokens"] = {k: kwargs[k].detach().cpu().tolist() for k in INPUTS}
            captured["export_tokens"] = tuple(kwargs[k].detach().clone() for k in INPUTS)

    def after(module, args, output):
        attempt.state["calls"][phase]["completed"] += 1
        if phase == "references":
            captured["logits"] = output.logits.detach().cpu().tolist()
        attempt.guard(phase + "_forward_complete")

    hooks = [classifier.register_forward_pre_hook(before, with_kwargs=True),
             classifier.register_forward_hook(after)]
    refs = []
    try:
        with torch.inference_mode():
            for row in rows:
                scores = model([row])
                probs = torch.softmax(scores.float(), dim=-1)[0]
                require(tuple(scores.shape) == (1, len(row["options"])), "native score shape")
                require(torch.isfinite(scores).all().item() and torch.isfinite(probs).all().item(), "nonfinite native output")
                require(abs(probs.sum().item() - 1) <= 1e-6, "native normalization")
                require(len(captured["logits"]) == len(row["options"]) and
                        all(len(v) == 1 for v in captured["logits"]), "native logits must be [N,1]")
                refs.append({"id": row["id"], "option_ids": [o["id"] for o in row["options"]],
                             **captured["tokens"], "logits": captured["logits"],
                             "probabilities": probs.cpu().tolist(),
                             "top_option_id": row["options"][probs.argmax().item()]["id"]})
                dump(attempt.out / "native-references.json", refs)
        require(attempt.state["calls"]["references"] == {"entered": 3, "completed": 3}, "reference call count")
        phase = "export"

        class RawLogits(torch.nn.Module):
            def __init__(self, native):
                super().__init__()
                self.native = native

            def forward(self, input_ids, attention_mask, token_type_ids):
                return self.native(input_ids=input_ids, attention_mask=attention_mask,
                                   token_type_ids=token_type_ids, return_dict=True).logits

        assets = attempt.out / "assets"
        assets.mkdir()
        for name in sorted(ASSETS - {"encoder/model.safetensors"}):
            dest = assets / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / name, dest)
        attempt.guard("before_export")
        with torch.no_grad():
            torch.onnx.export(
                RawLogits(classifier).eval(), captured["export_tokens"], str(assets / "model.onnx"),
                input_names=list(INPUTS), output_names=["logits"],
                dynamic_axes={**{k: {0: "batch", 1: "sequence"} for k in INPUTS},
                              "logits": {0: "batch"}},
                opset_version=17, dynamo=False, export_params=True, do_constant_folding=False,
                training=torch.onnx.TrainingMode.EVAL,
            )
        attempt.guard("after_export")
        # Graph structure validation only: never run ONNX in Python.
        graph = onnx.load(str(assets / "model.onnx"), load_external_data=False)
        require([(i.domain, i.version) for i in graph.opset_import] == [("", 17)], "opset mismatch")
        require([v.name for v in graph.graph.input] == list(INPUTS), "export input contract mismatch")
        require([v.name for v in graph.graph.output] == ["logits"], "export output contract mismatch")
        for value in graph.graph.input:
            dims = value.type.tensor_type.shape.dim
            require(value.type.tensor_type.elem_type == onnx.TensorProto.INT64 and len(dims) == 2
                    and [d.dim_param for d in dims] == ["batch", "sequence"], "dynamic int64 input contract")
        value = graph.graph.output[0]
        dims = value.type.tensor_type.shape.dim
        require(value.type.tensor_type.elem_type == onnx.TensorProto.FLOAT and len(dims) == 2
                and dims[0].dim_param == "batch" and dims[1].dim_value == 1, "FP32 logits[N,1] required")
        require(not any(node.op_type == "Sigmoid" for node in graph.graph.node), "unexpected sigmoid")
        inventory = {p.relative_to(assets).as_posix(): {"bytes": p.stat().st_size, "sha256": attempt.sha(p)}
                     for p in sorted(assets.rglob("*")) if p.is_file()}
        dump(attempt.out / "asset-inventory.json", inventory)
        attempt.guard("complete")
        for p in assets.rglob("*"):
            if p.is_file():
                p.chmod(0o444)
        for p in sorted((p for p in assets.rglob("*") if p.is_dir()), reverse=True):
            p.chmod(0o555)
        assets.chmod(0o555)
        attempt.state["status"] = "completed"
    finally:
        for hook in hooks:
            hook.remove()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("activation", "checkpoint", "checkpoint-pins", "checkpoint-pins-sha256", "input",
                 "input-sha256", "native-bindings", "native-bindings-sha256", "native-source",
                 "environment", "environment-sha256", "output"):
        parser.add_argument("--" + flag, required=True)
    parser.add_argument("--max-seconds", type=float, default=300)
    parser.add_argument("--max-rss-gib", type=float, default=8)
    a = parser.parse_args()
    require(a.activation.strip(), "nonempty activation ID required; ID is not authority")
    require(0 < a.max_seconds <= 300 and 0 < a.max_rss_gib <= 8, "resource bounds cannot be raised")
    attempt = Attempt(a)
    old_warning = warnings.showwarning

    def warning(message, category, filename, lineno, file=None, line=None):
        item = {"category": category.__name__, "message": str(message), "filename": filename,
                "lineno": lineno, "stage": attempt.state["stage"]}
        attempt.state["warnings"].append(item)
        attempt.event("warning", **item)
        old_warning(message, category, filename, lineno, file=file, line=line)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("always")
            warnings.showwarning = warning
            run(a, attempt)
    except BaseException as exc:
        attempt.state["status"] = "failed"
        attempt.state["failure"] = {"type": type(exc).__name__, "message": str(exc),
                                    "traceback": traceback.format_exc()}
        raise
    finally:
        warnings.showwarning = old_warning
        attempt.state["total_native_calls"] = {
            key: sum(v[key] for v in attempt.state["calls"].values()) for key in ("entered", "completed")}
        attempt.state["tracer_warning_count"] = sum(w["category"] == "TracerWarning" for w in attempt.state["warnings"])
        attempt.event("finished", status=attempt.state["status"])


if __name__ == "__main__":
    main()
