"""Coverage-aware reference-label metrics; pure standard library."""
from __future__ import annotations

from collections import Counter, defaultdict
import math

from .common import fingerprint, nonempty, records

SUM_TOLERANCE = 1e-6
LABEL_NAMES = {
    "teacher": "teacher_agreement",
    "source_label": "source_label_accuracy",
    "rule_verified": "rule_verified_accuracy",
    "human_verified": "human_verified_accuracy",
}


def rate(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "value": numerator / denominator if denominator else None}


def loss_summary(outcomes):
    n = len(outcomes)
    zeros = sum(row["target_probability"] == 0 for row in outcomes)
    return {"n": n, "zero_target_count": zeros,
            "status": "positive_infinity" if zeros else "finite" if n else "undefined",
            "mean": None if zeros or not n else math.fsum(row["log_loss"] for row in outcomes) / n}


def summarize(outcomes):
    valid = [row for row in outcomes if row["status"] == "valid"]
    n, v = len(outcomes), len(valid)
    correct = sum(row["correct"] for row in valid)
    bases = sorted({row["label_basis"] for row in outcomes})
    metric = LABEL_NAMES[bases[0]] if len(bases) == 1 else "reference_label_agreement"
    bins = []
    for index in range(5):
        members = [row for row in valid if min(4, int(row["confidence"] * 5)) == index]
        count = len(members)
        confidence = math.fsum(row["confidence"] for row in members) / count if count else None
        agreement = sum(row["correct"] for row in members) / count if count else None
        bins.append({"lower": index / 5, "upper": (index + 1) / 5,
                     "upper_inclusive": index == 4, "n": count,
                     "mean_confidence": confidence, "agreement": agreement,
                     "confidence_minus_agreement": confidence - agreement if count else None})
    return {
        "examples": n, "groups": len({row["group_id"] for row in outcomes}),
        "coverage": rate(v, n),
        "failures": {key: sum(row["status"] == key for row in outcomes)
                     for key in ("missing", "invalid", "duplicate")},
        "top_choice": {"name": metric, "on_valid": rate(correct, v),
                       "on_all_failure_as_unsuccessful": rate(correct, n)},
        "log_loss": loss_summary(valid),
        "brier": {"n": v, "mean": math.fsum(row["brier"] for row in valid) / v if v else None,
                  "definition": "sum over options, not divided by option count"},
        "ties": {"examples": sum(row["tie_size"] > 1 for row in valid),
                 "sizes": dict(sorted(Counter(str(row["tie_size"]) for row in valid).items()))},
        "uniform_random_choice_expected_agreement": math.fsum(1 / row["option_count"] for row in outcomes) / n if n else None,
        "reliability": {
            "n": v, "bins": bins,
            "ece": math.fsum(b["n"] / v * abs(b["confidence_minus_agreement"]) for b in bins if b["n"]) if v else None,
            "interpretation": "Descriptive reference-label reliability, not verified truth calibration; sparse bins and correlated groups limit interpretation.",
            "sparse": v < 100 or len({row["group_id"] for row in valid}) < 20 or any(0 < b["n"] < 20 for b in bins),
        },
    }


def validate_prediction(row, example):
    if row.get("schema_version") != "0.1":
        raise ValueError("schema_version must be '0.1'")
    values = row.get("probabilities")
    if not isinstance(values, list):
        raise ValueError("probabilities must be a list")
    probabilities = {}
    for value in values:
        if not isinstance(value, dict) or not nonempty(value.get("option_id")):
            raise ValueError("probability entries require option_id")
        option_id, probability = value["option_id"], value.get("probability")
        if option_id in probabilities:
            raise ValueError("duplicate option_id")
        if isinstance(probability, bool) or not isinstance(probability, (int, float)):
            raise ValueError("probability must be a number, not boolean")
        if not 0 <= probability <= 1 or not math.isfinite(probability):
            raise ValueError("probability must be finite and in [0,1]")
        probabilities[option_id] = probability
    if set(probabilities) != {option["id"] for option in example["options"]}:
        raise ValueError("option_id set does not match input options")
    total = math.fsum(probabilities.values())
    deviation = abs(total - 1)
    if deviation > SUM_TOLERANCE:
        raise ValueError("probabilities do not sum to one within absolute tolerance 1e-6")
    return {key: value / total for key, value in probabilities.items()}, deviation


def provenance_summary(examples):
    groups = defaultdict(list)
    for row in examples:
        source = row["provenance"]
        teacher = source.get("teacher_model") if source["kind"] == "teacher" or source["label_basis"] == "teacher" else None
        groups[(source["kind"], source["source"], source["label_basis"], teacher or "")].append(row)
    return [{"kind": kind, "source": source, "label_basis": basis, "teacher_model": teacher or None,
             "rows": len(rows), "groups": len({row["group_id"] for row in rows}),
             "families": sorted({row["task_family"] for row in rows})}
            for (kind, source, basis, teacher), rows in sorted(groups.items())]


def score_examples(examples, predictions_path):
    by_id = {row["id"]: row for row in examples}
    identified = defaultdict(list)
    diagnostics = []
    record_count = 0
    for line, row, error in records(predictions_path):
        record_count += 1
        if error or not nonempty(row.get("id")):
            diagnostics.append({"line": line, "reason": error or "missing/non-string id", "kind": "unidentifiable"})
            continue
        identified[row["id"]].append((line, row))
    extras = sorted(set(identified) - set(by_id))
    for identifier in extras:
        diagnostics.append({"id": identifier, "lines": [line for line, _ in identified[identifier]], "kind": "extra_id"})
    duplicate_ids = sorted(identifier for identifier, rows in identified.items() if len(rows) > 1)
    outcomes, deviations = [], []
    for example in examples:
        identifier = example["id"]
        outcome = {"id": identifier, "group_id": example["group_id"], "task_family": example["task_family"],
                   "label_basis": example["provenance"]["label_basis"], "option_count": len(example["options"]),
                   "target_id": example["target_id"]}
        matches = identified.get(identifier, [])
        if not matches:
            outcome.update(status="missing", reason="no identifiable prediction")
        elif len(matches) > 1:
            outcome.update(status="duplicate", reason="all repeated prediction IDs rejected")
            diagnostics.append({"id": identifier, "lines": [line for line, _ in matches], "kind": "duplicate_id"})
        else:
            line, row = matches[0]
            try:
                probabilities, deviation = validate_prediction(row, example)
                deviations.append(deviation)
                ordered = [option["id"] for option in example["options"]]
                choice = max(ordered, key=lambda key: probabilities[key])
                target_p = probabilities[example["target_id"]]
                confidence = probabilities[choice]
                outcome.update(status="valid", choice_id=choice, correct=choice == example["target_id"],
                               probabilities=probabilities, target_probability=target_p,
                               log_loss=-math.log(target_p) if target_p else None,
                               brier=math.fsum((probabilities[key] - int(key == example["target_id"])) ** 2 for key in ordered),
                               confidence=confidence, tie_size=sum(p == confidence for p in probabilities.values()))
            except ValueError as exc:
                outcome.update(status="invalid", reason=str(exc))
                diagnostics.append({"line": line, "id": identifier, "kind": "invalid_prediction", "reason": str(exc)})
        outcomes.append(outcome)
    grouped = {}
    for field in ("task_family", "label_basis", "option_count", "group_id"):
        groups = defaultdict(list)
        for row in outcomes:
            groups[str(row[field])].append(row)
        grouped[field] = {key: summarize(rows) for key, rows in sorted(groups.items())}
    family_basis = defaultdict(list)
    for row in outcomes:
        family_basis[(row["task_family"], row["label_basis"])].append(row)
    failures = any(row["status"] != "valid" for row in outcomes)
    return {
        "report_schema_version": "evaluation/0.1", "prediction_file": fingerprint(predictions_path),
        "reference_provenance": provenance_summary(examples),
        "status": "empty_reference" if not examples else "prediction_issues" if failures or diagnostics else "ok",
        "policy": {"probability_sum_absolute_tolerance": SUM_TOLERANCE,
                   "accepted_roundoff": "divide by observed sum; never clip probabilities",
                   "log_loss": "natural log; exact zero target probability is positive infinity",
                   "tie_break": "first option in reference input order; exact ties",
                   "invalid_predictions": "excluded from conditional quality; unsuccessful in all-example top-choice rate"},
        "prediction_records": record_count,
        "record_diagnostics": diagnostics,
        "extra_prediction_ids": extras, "duplicate_prediction_ids": duplicate_ids,
        "unidentifiable_records": sum(row["kind"] == "unidentifiable" for row in diagnostics),
        "roundoff": {"normalized_rows": sum(d != 0 for d in deviations), "max_sum_deviation": max(deviations, default=0)},
        "overall": summarize(outcomes), "per_family": grouped["task_family"],
        "per_source_group": grouped["group_id"],
        "per_label_basis": grouped["label_basis"], "per_option_count": grouped["option_count"],
        "per_family_label_basis": [{"family": family, "label_basis": basis, "metrics": summarize(rows)}
                                  for (family, basis), rows in sorted(family_basis.items())],
        "outcomes": outcomes,
    }


def paired_comparison(left, right, total):
    a = {row["id"]: row for row in left if row["status"] == "valid"}
    b = {row["id"]: row for row in right if row["status"] == "valid"}
    common = sorted(set(a) & set(b))
    a_summary, b_summary = summarize([a[key] for key in common]), summarize([b[key] for key in common])
    a_loss, b_loss = a_summary["log_loss"], b_summary["log_loss"]
    finite = a_loss["status"] == b_loss["status"] == "finite"
    return {
        "common_valid": rate(len(common), total), "common_valid_ids": common,
        "left": a_summary, "right": b_summary,
        "agreement_delta_left_minus_right": (a_summary["top_choice"]["on_valid"]["value"] - b_summary["top_choice"]["on_valid"]["value"]) if common else None,
        "log_loss_delta_left_minus_right": a_loss["mean"] - b_loss["mean"] if finite else None,
        "loss_delta_status": "finite" if finite else "undefined_empty_or_infinite; inspect each side",
        "outcome_pairs": {
            "left_only_correct": sum(a[key]["correct"] and not b[key]["correct"] for key in common),
            "right_only_correct": sum(b[key]["correct"] and not a[key]["correct"] for key in common),
            "both_correct": sum(a[key]["correct"] and b[key]["correct"] for key in common),
            "neither_correct": sum(not a[key]["correct"] and not b[key]["correct"] for key in common),
        },
        "warning": "Paired quality uses common valid IDs only; always compare full-reference coverage and failure counts too.",
    }
