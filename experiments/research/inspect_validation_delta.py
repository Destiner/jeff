"""Decompose existing validation predictions without loading or running a model."""

import argparse
import hashlib
import json
import math
from pathlib import Path


def read_rows(path):
    if "final" in path.resolve().parts:
        raise ValueError("Reserved final artifacts are not research inputs")
    data = path.read_bytes()
    rows = [json.loads(line) for line in data.splitlines() if line.strip()]
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError(f"Duplicate IDs: {path}")
    return {row["id"]: row for row in rows}, hashlib.sha256(data).hexdigest()


def probability_map(row, option_ids):
    items = row["probabilities"]
    values = {item["option_id"]: item["probability"] for item in items}
    if len(values) != len(items) or set(values) != set(option_ids):
        raise ValueError(f"Option coverage/uniqueness failure: {row['id']}")
    if any(type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1
           for p in values.values()) or abs(sum(values.values()) - 1) > 1e-5:
        raise ValueError(f"Invalid probabilities: {row['id']}")
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", required=True, type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--trained", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    examples, examples_hash = read_rows(args.examples)
    baseline, baseline_hash = read_rows(args.baseline)
    trained, trained_hash = read_rows(args.trained)
    if not examples or set(examples) != set(baseline) or set(examples) != set(trained):
        raise ValueError("Nonempty, exact example coverage required; do not drop failures")
    if any(row["split"] != "validation" for row in examples.values()):
        raise ValueError("Only validation examples are allowed")
    differences = []
    totals = {stage: {"correct": 0, "log_loss": 0.0} for stage in ("baseline", "trained")}
    for identifier, example in examples.items():
        option_ids = [option["id"] for option in example["options"]]
        result = {"id": identifier, "task_family": example["task_family"],
                  "group_id": example["group_id"], "label_basis": example["provenance"]["label_basis"],
                  "target_id": example["target_id"]}
        for stage, rows in (("baseline", baseline), ("trained", trained)):
            values = probability_map(rows[identifier], option_ids)
            chosen = max(option_ids, key=lambda option: values[option])
            target_probability = values[example["target_id"]]
            if target_probability <= 0:
                raise ValueError("Zero target probability: infinite log loss needs separate reporting")
            log_loss = -math.log(target_probability)
            ordered = sorted(values.values(), reverse=True)
            result[stage] = {
                "chosen_id": chosen, "target_probability": target_probability,
                "top_probability": ordered[0], "top_two_margin": ordered[0] - ordered[1],
                "log_loss": log_loss, "target_agreement": chosen == example["target_id"],
                "max_distance_from_uniform": max(abs(p - 1 / len(option_ids)) for p in values.values()),
            }
            totals[stage]["correct"] += int(result[stage]["target_agreement"])
            totals[stage]["log_loss"] += log_loss / len(examples)
        result["target_probability_delta"] = result["trained"]["target_probability"] - result["baseline"]["target_probability"]
        result["log_loss_delta"] = result["trained"]["log_loss"] - result["baseline"]["log_loss"]
        differences.append(result)
    report = {
        "kind": "validation_delta_analysis", "examples": len(examples), "coverage": 1.0,
        "input_sha256": {"examples": examples_hash, "baseline": baseline_hash, "trained": trained_hash},
        "input_paths": {key: str(getattr(args, key).resolve()) for key in ("examples", "baseline", "trained")},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "summary": totals, "per_example": differences,
        "limitations": ["No model execution; arithmetic on saved predictions only.",
                        "Teacher labels measure agreement, not independently verified correctness.",
                        "Small plumbing set cannot select architecture or establish generalization."],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output.resolve()), "examples": len(examples), "summary": totals}))


if __name__ == "__main__":
    main()
