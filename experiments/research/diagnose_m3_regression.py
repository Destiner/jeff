"""Augment frozen Evaluation outcomes with ranks/margins; no model execution."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

from jeff.evaluation.metrics import validate_prediction

from audit_pilot_shortcuts import sentiment_class
from inspect_validation_delta import read_rows


RECIPE_SHA256 = "a456847c240dec875822df8672676ebdee4614c765363405e228c1569887b805"
SNAPSHOTS = {
    "M2_start": "random-head-256", "M2_trained": "trained-256",
    "M3_start": "pretrained-msmarco-256", "M3_trained": "trained-msmarco-256",
}


def snapshot(outcome, example):
    probabilities = outcome["probabilities"]
    option_ids = [option["id"] for option in example["options"]]
    target = example["target_id"]
    ordered = sorted(option_ids, key=lambda key: -probabilities[key])
    rival = max((key for key in option_ids if key != target), key=probabilities.get)
    p, q = probabilities[target], probabilities[rival]
    if p <= 0 or q <= 0:
        raise ValueError("This bounded finite log-ratio analysis requires positive probabilities")
    return {
        "choice_id": outcome["choice_id"], "correct": outcome["correct"],
        "target_rank": ordered.index(target) + 1,
        "target_probability": p, "best_rival_id": rival,
        "target_minus_rival": p - q, "target_log_ratio": math.log(p / q),
        "top_two_margin": probabilities[ordered[0]] - probabilities[ordered[1]],
        "log_loss": outcome["log_loss"],
    }


def transitions(rows, left, right):
    result = Counter()
    for row in rows:
        a, b = row["snapshots"][left], row["snapshots"][right]
        result[("C" if a["correct"] else "W") + "->" + ("C" if b["correct"] else "W")] += 1
    return dict(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    root, sources = args.artifacts_dir.resolve(), {}
    output = args.output_dir.resolve()
    if not output.is_relative_to(root / "research") or output == root / "research":
        raise ValueError("Output must be a new child of shared Research artifact storage")
    allowed = [root / relative for relative in (
        "evaluation/e2-m3-v2", "evaluation/data-pilot-v1", "evaluation/probes-v1",
        "model/pilot-256-validation-20261111-01", "model/m2-e2-inference-20261111-01",
        "model/msmarco-256-inference-20261111-01",
    )]

    def checked_file(path, expected):
        path = Path(path).resolve()
        if "final" in path.parts or not any(path.is_relative_to(base) for base in allowed):
            raise ValueError("Input outside explicitly authorized development artifacts")
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if digest != expected:
            raise ValueError(f"Frozen source hash mismatch: {path}")
        sources[str(path)] = digest
        return path, payload

    def receipt(entry):
        return checked_file(entry["path"], entry["sha256"])

    recipe_path = root / "evaluation/e2-m3-v2/recipe.json"
    _, payload = checked_file(recipe_path, RECIPE_SHA256)
    recipe = json.loads(payload)
    pair_receipt = recipe["orders"]["probe-order/trained-msmarco-256.json"]["pairs"]
    _, payload = receipt(pair_receipt)
    pairs = json.loads(payload)
    result = {}
    for suite, filename in (("pilot", "comparison.json"), ("probes", "probes-comparison.json")):
        spec = recipe["comparisons"][filename]
        _, payload = receipt(spec["output"])
        comparison = json.loads(payload)
        path, _ = receipt(spec["examples"])
        examples, _ = read_rows(path)
        if any(row["split"] != "validation" for row in examples.values()):
            raise ValueError("Only published validation references are authorized")
        outcomes = {}
        for name, run_name in SNAPSHOTS.items():
            run = comparison["runs"][run_name]
            path, _ = receipt(spec["predictions"][run_name])
            predictions, _ = read_rows(path)
            saved = {row["id"]: row for row in run["outcomes"]}
            if run["status"] != "ok" or len(saved) != len(run["outcomes"]) or set(saved) != set(examples) or set(predictions) != set(examples):
                raise ValueError("Complete unique valid coverage required")
            for identifier, example in examples.items():
                normalized, _ = validate_prediction(predictions[identifier], example)
                if saved[identifier]["probabilities"] != normalized or saved[identifier]["target_id"] != example["target_id"]:
                    raise ValueError("Saved Evaluation outcome disagrees with source prediction/reference")
            outcomes[name] = saved
        selected = list(examples)
        reversal = None
        if suite == "probes":
            selected = [pair["original_id"] for pair in pairs]
            all_ids = [pair[key] for pair in pairs for key in ("original_id", "reversed_id")]
            if len(set(all_ids)) != len(all_ids) or set(all_ids) != set(examples) or len({pair["group_id"] for pair in pairs}) != len(pairs):
                raise ValueError("Probe pairs must partition references into unique source groups")
            reversal = {name: {"same_choice_pairs": 0, "max_probability_difference": 0.0} for name in SNAPSHOTS}
            for pair in pairs:
                a, b = examples[pair["original_id"]], examples[pair["reversed_id"]]
                if a["options"] != list(reversed(b["options"])) or any(a[key] != b[key] for key in ("state", "question", "target_id", "group_id", "task_family")) or a["group_id"] != pair["group_id"]:
                    raise ValueError("Probe pair is not an exact option reversal")
                for name, rows in outcomes.items():
                    left, right = rows[a["id"]], rows[b["id"]]
                    reversal[name]["same_choice_pairs"] += left["choice_id"] == right["choice_id"]
                    delta = max(abs(p - right["probabilities"][key]) for key, p in left["probabilities"].items())
                    reversal[name]["max_probability_difference"] = max(reversal[name]["max_probability_difference"], delta)
        rows = [{"id": identifier, "group_id": examples[identifier]["group_id"],
                 "task_family": examples[identifier]["task_family"],
                 "snapshots": {name: snapshot(values[identifier], examples[identifier]) for name, values in outcomes.items()}}
                for identifier in selected]
        initial, trained = [comparison["runs"][SNAPSHOTS[name]] for name in ("M3_start", "M3_trained")]
        attribution = []
        n = initial["overall"]["examples"]
        for group, before in initial["per_source_group"].items():
            after = trained["per_source_group"][group]
            attribution.append({"group_id": group, "presentations": before["examples"],
                "loss_start": before["log_loss"]["mean"], "loss_trained": after["log_loss"]["mean"],
                "contribution_to_mean_loss_improvement": before["examples"] / n * (before["log_loss"]["mean"] - after["log_loss"]["mean"])})
        result[suite] = {
            "presentations": len(examples), "analyzed_rows": len(rows),
            "source_groups": len({row["group_id"] for row in rows}), "rows": rows,
            "transitions": {label: transitions(rows, a, b) for label, a, b in (
                ("M2_training", "M2_start", "M2_trained"), ("M3_training", "M3_start", "M3_trained"),
                ("trained_M2_to_M3", "M2_trained", "M3_trained"))},
            "M3_loss_attribution": attribution, "probe_reversals": reversal,
            "published_metrics": {name: {key: comparison["runs"][run][key] for key in ("overall", "per_family", "per_source_group")}
                                  for name, run in SNAPSHOTS.items()},
        }
        if suite == "pilot":
            rule_counts, sentiment_confusions = {}, {}
            for name, values in outcomes.items():
                rule_counts[name], confusion = {}, Counter()
                for identifier, example in examples.items():
                    texts = {option["id"]: option["text"] for option in example["options"]}
                    chosen = texts[values[identifier]["choice_id"]]
                    if example["task_family"] == "rule_application":
                        group = example["group_id"]
                        rule_counts[name].setdefault(group, Counter())[chosen] += 1
                    if example["task_family"] == "sentiment":
                        confusion[sentiment_class(texts[example["target_id"]]) + "->" + sentiment_class(chosen)] += 1
                sentiment_confusions[name] = dict(confusion)
            result[suite]["rule_choice_text_counts"] = rule_counts
            result[suite]["sentiment_confusions"] = sentiment_confusions
    output.mkdir(parents=True, exist_ok=False)
    report = {"task": "R4-M3-regression-diagnosis", "created_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sources, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "helper_sha256": {str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest() for path in (
            Path(__file__).with_name("inspect_validation_delta.py"),
            Path(__file__).with_name("audit_pilot_shortcuts.py"),
            Path(validate_prediction.__code__.co_filename),
        )},
        "datasets": result, "limitations": [
            "Evaluation metrics reused unchanged; added rank/margin arithmetic is not a new scorer",
            "Probe reversals collapsed using pair map; no independent sample claim",
            "Log probability ratios recover relative score gaps at temperature one, not absolute logits",
            "Exploratory development diagnosis, not causal identification, new labels or untouched final evidence",
        ]}
    with (output / "diagnosis.json").open("x") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(json.dumps({suite: {key: values[key] for key in ("presentations", "analyzed_rows", "source_groups", "transitions")}
                      for suite, values in result.items()}))


if __name__ == "__main__":
    main()
