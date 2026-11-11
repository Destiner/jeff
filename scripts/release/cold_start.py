"""Run four real CPU CLI processes during an explicitly granted Model slot.

macOS-only evidence harness, not an inference implementation or software suite.
Stage must already contain copied m2-bundle/m3-bundle and an external venv.
"""

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, type=Path)
    parser.add_argument("--deny-home", required=True, type=Path)
    parser.add_argument("--source-m2", required=True, type=Path)
    parser.add_argument("--source-m3", required=True, type=Path)
    parser.add_argument("--start-before", required=True, help="UTC deadline, e.g. 2026-11-11T11:43:00Z")
    args = parser.parse_args()
    stage = args.stage.resolve()
    denied = args.deny_home.resolve()
    if platform.system() != "Darwin" or Path(sys.base_prefix).is_relative_to(denied):
        raise ValueError("requires macOS and a Python installation outside denied home")
    evidence = stage / "evidence"
    evidence.mkdir(exist_ok=False)
    policy = '(version 1)\n(allow default)\n(deny network*)\n'
    policy += f'(deny file-read* (subpath {json.dumps(str(denied))}))\n'
    policy += '(deny file-write*)\n'
    policy += f'(allow file-write* (subpath {json.dumps(str(stage))}))\n'
    policy += '(allow file-write* (literal "/dev/null"))\n'
    profile = evidence / "offline.sb"
    profile.write_text(policy)
    preflight = """import importlib.util,json,pathlib,socket,sys
blocked={}
for name,path in [('original_home',sys.argv[1]),('original_checkout',sys.argv[2]),('original_model_cache',sys.argv[3])]:
 try:
  pathlib.Path(path).stat()
 except PermissionError:
  blocked[name]=True
 else:
  raise RuntimeError('original path was accessible: '+name)
try:
 socket.socket().bind(('127.0.0.1',0))
except PermissionError:
 blocked['network']=True
else:
 raise RuntimeError('socket operation was permitted')
blocked['jeff_module']=importlib.util.find_spec('jeff').origin
blocked['python_base']=sys.base_prefix
print(json.dumps(blocked))
"""
    records = []
    for candidate in ("m2", "m3"):
        bundle = stage / f"{candidate}-bundle"
        for kind in ("isolated", "source"):
            if time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) >= args.start_before:
                raise RuntimeError("slot start deadline passed; ask Model for renewal")
            run = evidence / f"{candidate}-{kind}"
            run.mkdir()
            for name in ("home", "hf", "xdg", "torch", "tmp"):
                (run / name).mkdir()
            env = {
                "PATH": str(Path(sys.executable).parent) + ":/usr/bin:/bin",
                "HOME": str(run / "home"), "TMPDIR": str(run / "tmp"),
                "HF_HOME": str(run / "hf"), "HF_HUB_CACHE": str(run / "hf/hub"),
                "HUGGINGFACE_HUB_CACHE": str(run / "hf/hub"),
                "XDG_CACHE_HOME": str(run / "xdg"), "TORCH_HOME": str(run / "torch"),
                "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1",
                "HF_HUB_DISABLE_TELEMETRY": "1", "HF_HUB_DISABLE_IMPLICIT_TOKEN": "1",
                "TOKENIZERS_PARALLELISM": "false", "OMP_NUM_THREADS": "2",
                "MKL_NUM_THREADS": "2", "VECLIB_MAXIMUM_THREADS": "2",
            }
            sandbox = ["/usr/bin/sandbox-exec", "-f", str(profile)] if kind == "isolated" else []
            if kind == "isolated":
                check = subprocess.run(sandbox + [sys.executable, "-I", "-c", preflight,
                    str(denied), str(args.source_m2.parents[3] / "AGENTS.md"),
                    str(args.source_m2.parents[1] / "hf-cache-20261111")],
                    cwd=stage, env=env, text=True, capture_output=True, timeout=15)
                (run / "isolation.json").write_text(check.stdout)
                (run / "isolation.stderr").write_text(check.stderr)
                if check.returncode:
                    raise RuntimeError("sandbox preflight failed: " + check.stderr)
                verified = subprocess.run(sandbox + [sys.executable, "-I", "-m", "jeff.runtime.verify", str(bundle)],
                    cwd=stage, env=env, text=True, capture_output=True, check=True, timeout=30)
                (run / "bundle-verification.json").write_text(verified.stdout)
            cache_before = [str(p.relative_to(run)) for n in ("hf", "xdg", "torch") for p in (run / n).rglob("*")]
            if cache_before:
                raise RuntimeError("model cache was not empty")
            checkpoint = bundle / "checkpoint" if kind == "isolated" else getattr(args, "source_" + candidate)
            command = sandbox + ["/usr/bin/time", "-l", sys.executable, "-I", "-m", "jeff.model.predict",
                "--checkpoint", str(checkpoint), "--input", str(bundle / "demo/inputs.jsonl"),
                "--output", str(run / "predictions.jsonl"), "--device", "cpu", "--batch-size", "1"]
            (run / "invocation.json").write_text(json.dumps({"argv": command, "env": env, "cwd": str(stage)}, indent=2) + "\n")
            if time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) >= args.start_before:
                raise RuntimeError("slot expired during preflight; ask Model for renewal")
            start = time.perf_counter()
            completed = subprocess.run(command, cwd=stage, env=env, text=True, capture_output=True, timeout=120)
            duration = time.perf_counter() - start
            (run / "stdout.log").write_text(completed.stdout)
            (run / "stderr.log").write_text(completed.stderr)
            if completed.returncode:
                raise RuntimeError("inference failed: " + completed.stderr)
            inputs = [json.loads(line) for line in (bundle / "demo/inputs.jsonl").read_text().splitlines()]
            predictions = [json.loads(line) for line in (run / "predictions.jsonl").read_text().splitlines()]
            if len(predictions) != len(inputs):
                raise ValueError("prediction coverage mismatch")
            for row, prediction in zip(inputs, predictions):
                values = prediction["probabilities"]
                if (row["id"] != prediction["id"] or
                    [o["id"] for o in row["options"]] != [v["option_id"] for v in values] or
                    any(not math.isfinite(v["probability"]) or not 0 <= v["probability"] <= 1 for v in values) or
                    not math.isclose(sum(v["probability"] for v in values), 1.0, abs_tol=1e-6)):
                    raise ValueError("invalid prediction output")
            rss = re.search(r"(\d+)\s+maximum resident set size", completed.stderr)
            records.append({"candidate": candidate, "kind": kind, "wall_seconds": duration,
                "max_rss_bytes": int(rss[1]) if rss else None, "predictions": len(predictions),
                "options": sum(len(r["options"]) for r in inputs), "cache_entries_before": cache_before,
                "cache_entries_after": [str(p.relative_to(run)) for n in ("hf", "xdg", "torch") for p in (run / n).rglob("*")],
                "returncode": completed.returncode})
        first = (evidence / f"{candidate}-isolated/predictions.jsonl").read_bytes()
        second = (evidence / f"{candidate}-source/predictions.jsonl").read_bytes()
        records[-1]["byte_identical_to_isolated"] = first == second
    summary = {"platform": platform.platform(), "machine": platform.machine(), "python": sys.version,
        "python_base": sys.base_prefix, "executable": sys.executable,
        "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions()},
        "profile_sha256": hashlib.sha256(profile.read_bytes()).hexdigest(), "runs": records,
        "timing_scope": "Fresh process wall includes sandbox/time/interpreter/import/load/inference/output; not installation, no OS page-cache flush.",
        "memory_scope": "macOS /usr/bin/time -l child process lifetime max RSS bytes; CPU, not accelerator peak.",
        "source_comparison_scope": "Same external environment/input/CPU; source checkpoint accessible, not sandbox-isolated.",
        "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (evidence / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
