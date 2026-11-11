"""Cheap, label-blind prediction baselines: uniform and lexical overlap."""
from __future__ import annotations

import argparse
import math
import re

from .common import fingerprint, records, validate_input, write_json, write_jsonl

STOPWORDS = frozenset("a an the and or of to in is it this that for with as be on at by from what which how should does do".split())


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS


def predict(row, method):
    validate_input(row)
    options = row["options"]
    if method == "uniform":
        probabilities = [1 / len(options)] * len(options)
    else:
        context = tokens(row["state"] + " " + row["question"])
        scores = []
        for option in options:
            candidate = tokens(option["text"])
            scores.append(len(context & candidate) / math.sqrt(len(context) * len(candidate)) if context and candidate else 0)
        weights = [math.exp(score - max(scores)) for score in scores]
        total = math.fsum(weights)
        probabilities = [weight / total for weight in weights]
    return {"schema_version": "0.1", "id": row["id"],
            "probabilities": [{"option_id": option["id"], "probability": p} for option, p in zip(options, probabilities)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Label-free decision inputs only")
    parser.add_argument("--method", required=True, choices=("uniform", "lexical"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    rows, ids = [], set()
    for line, row, error in records(args.input):
        if error:
            raise ValueError(f"Invalid input on line {line}: {error}")
        if set(row) != {"schema_version", "id", "state", "question", "options"}:
            raise ValueError("Baseline inputs must be allowlisted label-free decision inputs")
        validate_input(row)
        if row["id"] in ids:
            raise ValueError("Duplicate input id")
        ids.add(row["id"])
        rows.append(predict(row, args.method))
    write_jsonl(args.output, rows)
    write_json(args.receipt, {"schema_version": "evaluation/0.1", "method": args.method,
                            "input": fingerprint(args.input), "predictions": fingerprint(args.output), "rows": len(rows),
                            "definition": "p=1/K" if args.method == "uniform" else "softmax of set-token cosine overlap, temperature 1; lowercase ASCII word tokens; fixed stopwords",
                            "stopwords": sorted(STOPWORDS) if args.method == "lexical" else [],
                            "tie_break": "first option in reference input order", "training": "none",
                            "cost_gbp": 0})
    print(f"Wrote {len(rows)} {args.method} predictions: {args.output}")


if __name__ == "__main__":
    main()
