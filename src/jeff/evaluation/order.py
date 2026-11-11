"""Validation-only option reversal analysis, preserving option identities."""
from __future__ import annotations

import argparse
from collections import defaultdict
import math
from pathlib import Path

from .common import fingerprint, load_examples, parse_json, write_json
from .metrics import rate, score_examples, summarize


def pair_summary(pairs):
    valid = [pair for pair in pairs if pair["status"] == "valid"]
    untied = [pair for pair in valid if not pair["either_tied"]]
    n = len(valid)
    return {
        "pairs": len(pairs), "complete_pair_coverage": rate(n, len(pairs)),
        "choice_consistency": rate(sum(pair["same_choice"] for pair in valid), n),
        "choice_consistency_without_ties": rate(sum(pair["same_choice"] for pair in untied), len(untied)),
        "either_tied": sum(pair["either_tied"] for pair in valid),
        "both_correct": sum(pair["original_correct"] and pair["reversed_correct"] for pair in valid),
        "original_only_correct": sum(pair["original_correct"] and not pair["reversed_correct"] for pair in valid),
        "reversed_only_correct": sum(not pair["original_correct"] and pair["reversed_correct"] for pair in valid),
        "neither_correct": sum(not pair["original_correct"] and not pair["reversed_correct"] for pair in valid),
        "mean_total_variation": math.fsum(pair["total_variation"] for pair in valid) / n if n else None,
        "max_probability_change": max((pair["max_probability_change"] for pair in valid), default=None),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", required=True)
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--pairs", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    examples = load_examples(args.examples)
    if any(row["split"] != "validation" for row in examples):
        raise ValueError("Option-order analysis is validation-only")
    by_id = {row["id"]: row for row in examples}
    definitions = parse_json(Path(args.pairs).read_text(encoding="utf-8"))
    assigned = set()
    groups = set()
    for pair in definitions:
        left, right = by_id[pair["original_id"]], by_id[pair["reversed_id"]]
        if left["id"] == right["id"] or left["id"] in assigned or right["id"] in assigned or pair["group_id"] in groups:
            raise ValueError("Pair IDs/groups must be distinct and used exactly once")
        if left["group_id"] != pair["group_id"] or right["group_id"] != pair["group_id"]:
            raise ValueError("Pair group mismatch")
        for field in ("state", "question", "target_id", "task_family", "provenance"):
            if left[field] != right[field]:
                raise ValueError("Pairs must differ only by example ID and option order")
        if left["options"] != list(reversed(right["options"])):
            raise ValueError("Expected exact reversed option objects with IDs preserved")
        assigned.update((left["id"], right["id"]))
        groups.add(pair["group_id"])
    if assigned != set(by_id):
        raise ValueError("Pair definitions must cover all reference examples")
    report = score_examples(examples, args.predictions)
    outcomes = {row["id"]: row for row in report["outcomes"]}
    pairs, originals, reversals = [], [], []
    family_pairs = defaultdict(list)
    for definition in definitions:
        left, right = outcomes[definition["original_id"]], outcomes[definition["reversed_id"]]
        originals.append(left)
        reversals.append(right)
        pair = {**definition, "family": left["task_family"],
                "original_status": left["status"], "reversed_status": right["status"], "status": "incomplete"}
        if left["status"] == right["status"] == "valid":
            changes = [abs(left["probabilities"][key] - right["probabilities"][key]) for key in left["probabilities"]]
            pair.update(status="valid", same_choice=left["choice_id"] == right["choice_id"],
                        original_correct=left["correct"], reversed_correct=right["correct"],
                        either_tied=left["tie_size"] > 1 or right["tie_size"] > 1,
                        total_variation=math.fsum(changes) / 2, max_probability_change=max(changes))
        pairs.append(pair)
        family_pairs[pair["family"]].append(pair)
    write_json(args.output, {
        "report_schema_version": "evaluation/0.1", "examples_file": fingerprint(args.examples),
        "pair_file": fingerprint(args.pairs), "prediction_report": report,
        "overall": pair_summary(pairs), "original": summarize(originals), "reversed": summarize(reversals),
        "per_family": {family: pair_summary(rows) for family, rows in sorted(family_pairs.items())},
        "pairs": pairs,
        "limitation": "Two presentations per source group, not independent samples. Tied-choice changes are separated from probability changes. No final data used.",
    })
    print(f"Analyzed {len(pairs)} validation-only order pairs: {args.output}")
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
