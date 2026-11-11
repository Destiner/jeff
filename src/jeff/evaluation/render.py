"""Render existing validation comparisons as a repeatable Markdown report."""
from __future__ import annotations

import argparse
from pathlib import Path

from .common import fingerprint, parse_json


def number(value):
    return "—" if value is None else f"{value:.6f}"


def ratio(value):
    return f'{value["numerator"]}/{value["denominator"]}'


def loss(value):
    return "+infinity" if value["status"] == "positive_infinity" else number(value["mean"])


def escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers, rows):
    return ["| " + " | ".join(map(escape, headers)) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
            *("| " + " | ".join(map(escape, row)) + " |" for row in rows), ""]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison", required=True)
    parser.add_argument("--order", action="append", default=[], metavar="PREDICTOR=REPORT")
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", default="Validation comparison")
    args = parser.parse_args()
    report = parse_json(Path(args.comparison).read_text(encoding="utf-8"))
    if report.get("split") != "validation":
        raise ValueError("This renderer is validation-only")
    runs = report["runs"]
    if not runs:
        raise ValueError("Comparison has no predictors")
    reference = next(iter(runs.values()))
    lines = [f"# {escape(args.title)}", "",
             f'Reference: `{report["examples_file"]["path"]}`; SHA-256 `{report["examples_file"]["sha256"]}`.',
             f'{reference["overall"]["examples"]} rows / {reference["overall"]["groups"]} declared source groups. Rows and reversals are not independent observations.', "",
             "## Coverage and quality", "",
             "Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.", ""]
    lines += table(["Predictor", "Valid/total", "Conditional agreement", "All-row success", "Log loss", "Missing/invalid/duplicate", "Extra IDs", "Unidentifiable", "Ties"], [
        [name, ratio(run["overall"]["coverage"]), ratio(run["overall"]["top_choice"]["on_valid"]),
         ratio(run["overall"]["top_choice"]["on_all_failure_as_unsuccessful"]), loss(run["overall"]["log_loss"]),
         "/".join(str(run["overall"]["failures"][key]) for key in ("missing", "invalid", "duplicate")),
         len(run["extra_prediction_ids"]), run["unidentifiable_records"], run["overall"]["ties"]["examples"]]
        for name, run in runs.items()])
    lines += ["## Label provenance", "", "Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.", ""]
    provenance = reference.get("reference_provenance", [])
    if provenance:
        lines += table(["Kind", "Source", "Label basis", "Teacher model", "Rows", "Groups", "Families"], [
            [row["kind"], row["source"], row["label_basis"], row["teacher_model"] or "not applicable",
             row["rows"], row["groups"], ", ".join(row["families"])] for row in provenance])
    else:
        lines += ["Source report does not include teacher/source identifiers; consult the hashed reference file.", ""]
    for label, field in (("Per label basis", "per_label_basis"), ("Per family", "per_family"), ("Per source group", "per_source_group")):
        lines += [f"## {label}", "", "Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.", ""]
        rows = []
        for key, metrics in reference[field].items():
            row = [key, metrics["examples"], metrics["groups"], metrics["top_choice"]["name"]]
            for run in runs.values():
                result = run[field][key]
                row.append(f'{ratio(result["top_choice"]["on_valid"])} · {loss(result["log_loss"])}')
            rows.append(row)
        lines += table([label, "Rows", "Groups", "Metric", *runs], rows)
    lines += ["## Paired comparisons", "", "Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.", ""]
    lines += table(["Left", "Right", "Common/total", "Agreement delta", "Left loss", "Right loss", "Loss delta", "Loss delta status", "Left-only correct", "Right-only correct"], [
        [pair["left_name"], pair["right_name"], ratio(pair["common_valid"]),
         number(pair["agreement_delta_left_minus_right"]), loss(pair["left"]["log_loss"]), loss(pair["right"]["log_loss"]),
         number(pair["log_loss_delta_left_minus_right"]), pair["loss_delta_status"],
         pair["outcome_pairs"]["left_only_correct"], pair["outcome_pairs"]["right_only_correct"]]
        for pair in report["comparisons"]])
    order_rows, sources, seen = [], [], set()
    for item in args.order:
        name, sep, path = item.partition("=")
        if not sep or name not in runs or name in seen:
            raise ValueError("Use unique comparison predictor names for order reports")
        seen.add(name)
        order = parse_json(Path(path).read_text(encoding="utf-8"))
        expected = {row["id"]: row for row in runs[name]["outcomes"]}
        received = {row["id"]: row for row in order["prediction_report"]["outcomes"]}
        originals = [pair["original_id"] for pair in order["pairs"]]
        paired_ids = set(originals) | {pair["reversed_id"] for pair in order["pairs"]}
        if set(expected) not in (set(originals), paired_ids):
            raise ValueError("Comparison IDs must equal the order originals or all paired presentations")
        for identifier in expected:
            left, right = expected[identifier], received[identifier]
            if any(left[key] != right[key] for key in ("group_id", "task_family", "target_id", "label_basis", "status")):
                raise ValueError("Order originals do not match the comparison's reference outcomes")
            if left.get("probabilities") != right.get("probabilities"):
                raise ValueError("Order originals must reuse the exact matching predictor probabilities")
        value = order["overall"]
        quality = order["paired_quality"]
        order_rows.append([name, ratio(value["complete_pair_coverage"]), value["source_groups"],
                           ratio(quality["original"]["top_choice"]["on_valid"]), ratio(quality["reversed"]["top_choice"]["on_valid"]),
                           ratio(value["choice_consistency"]), ratio(value["choice_consistency_without_ties"]),
                           value["either_tied"], f'{value["mean_total_variation"]:.3g}' if value["mean_total_variation"] is not None else "—",
                           f'{value["max_probability_change"]:.3g}' if value["max_probability_change"] is not None else "—"])
        sources.append({"predictor": name, **fingerprint(path)})
    lines += ["## Option-order sensitivity", "", "Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.", ""]
    if order_rows:
        lines += table(["Predictor", "Complete pairs", "Groups", "Original agreement", "Reversed agreement", "Choice consistency", "Untied consistency", "Either tied", "Mean TV", "Max probability change"], order_rows)
    else:
        lines += ["No matching order reports supplied; no option-order conclusion.", ""]
    lines += ["## Interpretation and reproducibility", "",
              "These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.", "",
              f'Comparison report: `{fingerprint(args.comparison)["path"]}`; SHA-256 `{fingerprint(args.comparison)["sha256"]}`.']
    for source in sources:
        lines.append(f'- {escape(source["predictor"])} order: `{source["path"]}`; SHA-256 `{source["sha256"]}`.')
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as target:
        target.write("\n".join(lines) + "\n")
    print(f"Rendered {len(runs)} predictors: {args.output}")


if __name__ == "__main__":
    main()
