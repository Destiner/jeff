"""CPU-only pinned validation recipe over the existing compare/order/render CLIs."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

from .baseline import predict
from .common import (INPUT_FIELDS, fingerprint, input_only, load_examples, parse_json,
                     records, validate_input, write_json, write_jsonl)


def safe_path(value):
    path = Path(value).resolve()
    for candidate in (Path(value).absolute(), path):
        if any(p.lower() == "final" or p.lower().startswith(("final-", "final.", "final_"))
               for p in candidate.parts):
            raise ValueError(f"Reserved final path: {candidate}")
    return path


def name(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value):
        raise ValueError("Names must be simple alphanumeric/hyphen/underscore identifiers")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    root = safe_path(os.environ["JEFF_ARTIFACTS_DIR"]) / "evaluation"
    output = safe_path(args.output_dir)
    if root not in output.parents or output == root or output.exists():
        raise ValueError("Output must be a new directory under artifacts/evaluation/, never final")
    config_path = safe_path(args.config)
    pins = {str(config_path): fingerprint(config_path)}
    config = parse_json(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != "e3-study/1" or config.get("status") not in ("candidate-only", "released-validation"):
        raise ValueError("Require e3-study/1 and explicit candidate-only/released-validation status")
    strata = config["strata"]
    if not isinstance(strata, dict) or not strata:
        raise ValueError("Require named strata")

    # Screen every declared pin before hashing or opening any of its targets.
    declarations = []

    def screen(value):
        if isinstance(value, dict):
            if "path" in value:
                path = safe_path(value["path"])
                if not Path(value["path"]).is_absolute() or not re.fullmatch(r"[0-9a-f]{64}", value.get("sha256", "")):
                    raise ValueError("Pins require absolute path and lowercase SHA-256")
                declarations.append((path, value["sha256"]))
            for child in value.values():
                screen(child)
        elif isinstance(value, list):
            for child in value:
                screen(child)

    screen(config)
    for path, expected in declarations:
        actual = fingerprint(path)
        if actual["sha256"] != expected or (str(path) in pins and pins[str(path)] != actual):
            raise ValueError(f"Pin mismatch: {path}")
        pins[str(path)] = actual
    for module in ("study", "baseline", "common", "compare", "score", "metrics", "order", "render"):
        path = Path(__file__).with_name(module + ".py")
        pins[str(path.resolve())] = fingerprint(path)

    def pinned(spec):
        path = safe_path(spec["path"])
        if str(path) not in pins or pins[str(path)]["sha256"] != spec["sha256"]:
            raise ValueError("Undeclared pin")
        return path

    def reference(spec):
        rows = load_examples(pinned(spec))
        if not rows or any(row["split"] != "validation" for row in rows):
            raise ValueError("Require nonempty validation-only references")
        return rows

    universes = {}

    def universe(source):
        keys = [key for key in ("source_reference", "source_inputs") if key in source]
        if len(keys) > 1:
            raise ValueError("Choose one source universe: reference or label-free inputs")
        if not keys:
            return set()
        key = keys[0]
        path = pinned(source[key])
        cache_key = (key, str(path))
        if cache_key not in universes:
            if key == "source_reference":
                rows = reference(source[key])
            else:
                rows = []
                for line, row, error in records(path):
                    if error or set(row) != set(INPUT_FIELDS) or row != input_only(row):
                        raise ValueError(f"Source inputs must be strictly label-free: {path}:{line}")
                    validate_input(row)
                    rows.append(row)
                if len({row["id"] for row in rows}) != len(rows):
                    raise ValueError("Duplicate source input IDs")
            universes[cache_key] = {row["id"] for row in rows}
        return universes[cache_key]

    baselines = config.get("baselines", ["uniform", "lexical"])
    if len(set(baselines)) != len(baselines) or any(b not in ("uniform", "lexical") for b in baselines):
        raise ValueError("Baselines: unique uniform/lexical only")
    references = {}
    for stratum, spec in strata.items():
        name(stratum)
        rows = reference(spec["examples"])
        order_rows = None
        if ("order_examples" in spec) != ("order_pairs" in spec):
            raise ValueError("Order examples and pairs must be supplied together")
        if "order_examples" in spec:
            order_rows = reference(spec["order_examples"])
            pinned(spec["order_pairs"])
        predictors = spec.get("predictors", {})
        if len(predictors) + len(baselines) < 2:
            raise ValueError("Each stratum needs at least two predictors including baselines")
        for predictor, candidate in predictors.items():
            name(predictor)
            if predictor in baselines or candidate.get("role") not in ("fresh-start", "v2-trained", "historical-retained"):
                raise ValueError("Predictor needs distinct name and role: fresh-start/v2-trained/historical-retained")
            if "order_sources" in candidate and order_rows is None:
                raise ValueError("Order sources require order references")
            for field in ("sources", "order_sources"):
                if field in candidate:
                    if not candidate[field]:
                        raise ValueError("Prediction source lists must be nonempty")
                    for source in candidate[field]:
                        pinned(source["predictions"])
                        universe(source)
                        for attestation in ("reference", "inputs"):
                            if attestation in source:
                                if attestation == "reference":
                                    reference(source[attestation])
                                else:
                                    pinned(source[attestation])
            if "sources" not in candidate:
                raise ValueError("Comparison sources required (may reuse same-snapshot order bundle)")
        references[stratum] = (rows, order_rows)

    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "config.json", config)
    commands, subsets = [], []
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2]) + os.pathsep + env.get("PYTHONPATH", "")

    def cli(module, arguments, destination, issues=False):
        command = [sys.executable, "-m", "jeff.evaluation." + module, *map(str, arguments)]
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        receipt = {"command": command, "returncode": result.returncode,
                   "stdout": result.stdout, "stderr": result.stderr}
        commands.append(receipt)
        write_json(output / f"command-{len(commands):03d}.json", receipt)
        if result.returncode not in ((0, 1) if issues else (0,)) or not destination.is_file():
            raise ValueError(f"Fatal {module} invocation; see command receipt {len(commands)}")
        receipt["output"] = fingerprint(destination)

    def bundle(sources, ids, destination):
        audit = {"output": str(destination), "sources": []}
        with destination.open("xb") as target:
            for source in sources:
                known = universe(source)
                item = {"declaration": source, "kept_lines": 0, "unidentifiable_lines": 0,
                        "excluded_known": [], "unknown_extra_ids": []}
                with pinned(source["predictions"]).open("rb") as stream:
                    for line_number, raw in enumerate(stream, 1):
                        identifier = None
                        try:
                            row = parse_json(raw.decode("utf-8"))
                            if isinstance(row, dict) and isinstance(row.get("id"), str) and row["id"].strip():
                                identifier = row["id"]
                        except (ValueError, UnicodeError):
                            pass
                        if identifier is not None and identifier not in ids and identifier in known:
                            item["excluded_known"].append({"line": line_number, "id": identifier})
                            continue
                        if identifier is None:
                            item["unidentifiable_lines"] += 1
                        elif identifier not in ids:
                            item["unknown_extra_ids"].append({"line": line_number, "id": identifier})
                        target.write(raw)
                        if not raw.endswith(b"\n"):
                            target.write(b"\n")
                        item["kept_lines"] += 1
                audit["sources"].append(item)
        audit["fingerprint"] = fingerprint(destination)
        subsets.append(audit)
        return destination

    for stratum, spec in strata.items():
        directory = output / stratum
        directory.mkdir()
        rows, order_rows = references[stratum]
        predictions, orders = {}, {}
        for method in baselines:
            path = directory / f"{method}.jsonl"
            write_jsonl(path, (predict(input_only(row), method) for row in rows))
            predictions[method] = path
            if order_rows is not None:
                path = directory / f"{method}-order.jsonl"
                write_jsonl(path, (predict(input_only(row), method) for row in order_rows))
                orders[method] = path
        for predictor, candidate in spec.get("predictors", {}).items():
            predictions[predictor] = bundle(candidate["sources"], {r["id"] for r in rows}, directory / f"{predictor}.jsonl")
            if "order_sources" in candidate:
                orders[predictor] = bundle(candidate["order_sources"], {r["id"] for r in order_rows}, directory / f"{predictor}-order.jsonl")
        comparison = directory / "comparison.json"
        arguments = ["--examples", pinned(spec["examples"]), "--output", comparison]
        for predictor, path in predictions.items():
            arguments += ["--predictions", f"{predictor}={path}"]
        cli("compare", arguments, comparison, issues=True)
        render_args = ["--comparison", comparison, "--title", f"E3 {config['status']}: {stratum}"]
        for predictor, path in orders.items():
            report = directory / f"{predictor}-order-report.json"
            cli("order", ["--examples", pinned(spec["order_examples"]), "--pairs", pinned(spec["order_pairs"]),
                          "--predictions", path, "--output", report], report, issues=True)
            render_args += ["--order", f"{predictor}={report}"]
        report = directory / "report.md"
        cli("render", [*render_args, "--output", report], report)
    write_json(output / "subsets.json", subsets)
    # A receipt is the completion marker; partial directories are never reused.
    for path, expected in pins.items():
        if fingerprint(path) != expected:
            raise ValueError(f"Input changed during study: {path}; no completion receipt")
    outputs = [fingerprint(path) for path in sorted(output.rglob("*")) if path.is_file()]
    write_json(output / "receipt.json", {
        "schema_version": "e3-study/1", "status": config["status"], "input_pins": list(pins.values()),
        "commands": commands, "outputs": outputs, "cost_gbp": 0, "model_loads": 0,
        "limitations": "Validation development only. Roles and optional reference/input attestations are caller claims, not checkpoint verification. No default promoted. Missing order sources mean no order conclusion. Raw records retained without probability normalization; only missing line terminators added. Unknown extras and unidentifiable records reach scorer. See subsets.json for every known-universe exclusion.",
    })
    print(f"Completed {config['status']} study: {output / 'receipt.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
