"""Produce allowlisted label-free inference inputs from labeled examples."""
from __future__ import annotations

import argparse

from .common import fingerprint, guard_final, input_only, load_examples, write_json, write_jsonl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--allow-final", action="store_true")
    args = parser.parse_args()
    examples = load_examples(args.examples)
    guard_final(examples, args.output, args.allow_final)
    guard_final(examples, args.receipt, args.allow_final)
    write_jsonl(args.output, (input_only(row) for row in examples))
    write_json(args.receipt, {"schema_version": "evaluation/0.1",
                            "examples": fingerprint(args.examples), "inputs": fingerprint(args.output),
                            "rows": len(examples), "label_free_fields": ["schema_version", "id", "state", "question", "options"]})
    print(f"Prepared {len(examples)} label-free inputs: {args.output}")


if __name__ == "__main__":
    main()
