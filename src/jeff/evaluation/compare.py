"""Compare named prediction files on one exact reference file and paired valid IDs."""
from __future__ import annotations

import argparse
from itertools import combinations

from .common import fingerprint, guard_final, load_examples, write_json
from .metrics import paired_comparison, score_examples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", required=True)
    parser.add_argument("--predictions", action="append", required=True, metavar="NAME=PATH")
    parser.add_argument("--output", required=True)
    parser.add_argument("--allow-final", action="store_true")
    args = parser.parse_args()
    examples = load_examples(args.examples)
    guard_final(examples, args.output, args.allow_final)
    reports = {}
    for item in args.predictions:
        name, sep, path = item.partition("=")
        if not sep or not name or name in reports:
            raise ValueError("Use unique NAME=PATH prediction arguments")
        reports[name] = score_examples(examples, path)
    if len(reports) < 2:
        raise ValueError("At least two prediction files required")
    comparisons = []
    for left, right in combinations(reports, 2):
        comparisons.append({"left_name": left, "right_name": right,
                            **paired_comparison(reports[left]["outcomes"], reports[right]["outcomes"], len(examples))})
    write_json(args.output, {"report_schema_version": "evaluation/0.1", "examples_file": fingerprint(args.examples),
                            "split": examples[0]["split"] if examples else None,
                            "runs": reports, "comparisons": comparisons})
    print(f"Compared {len(reports)} prediction files on {len(examples)} examples: {args.output}")
    return 0 if all(report["status"] == "ok" for report in reports.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
