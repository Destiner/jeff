"""Freeze validation-only reversed-option counterparts for existing examples."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from .common import fingerprint, input_only, load_examples, validate_examples, write_json, write_jsonl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    examples = load_examples(args.examples)
    if not examples or any(row["split"] != "validation" for row in examples):
        raise ValueError("Reversal preparation accepts nonempty validation only")
    root = Path(os.environ["JEFF_ARTIFACTS_DIR"]).resolve()
    output = Path(args.output_dir).resolve()
    if root / "evaluation" not in output.parents or root / "evaluation" / "final" in output.parents:
        raise ValueError("Validation outputs must remain in the non-final evaluation subtree")
    reversed_rows, pairs = [], []
    for row in examples:
        reversed_row = {**row, "id": row["id"] + ".evaluation-reversed-v1", "options": list(reversed(row["options"]))}
        reversed_rows.append(reversed_row)
        pairs.append({"pair_id": row["id"], "group_id": row["group_id"],
                      "original_id": row["id"], "reversed_id": reversed_row["id"]})
    combined = validate_examples(examples + reversed_rows)
    output.mkdir(parents=True, exist_ok=False)
    write_jsonl(output / "validation.jsonl", combined)
    write_jsonl(output / "reversed-inputs.jsonl", (input_only(row) for row in reversed_rows))
    write_jsonl(output / "paired-inputs.jsonl", (input_only(row) for row in combined))
    write_json(output / "pairs.json", pairs)
    write_json(output / "manifest.json", {
        "schema_version": "0.1", "dataset_id": args.dataset_id,
        "shards": [{"path": str((output / "validation.jsonl").relative_to(root)), "split": "validation",
                    "rows": len(combined), "sha256": fingerprint(output / "validation.jsonl")["sha256"]}],
    })
    write_json(output / "receipt.json", {
        "schema_version": "evaluation/0.1", "source": fingerprint(args.examples),
        "reversed_inputs": fingerprint(output / "reversed-inputs.jsonl"),
        "pairs": len(pairs), "source_groups": len({row["group_id"] for row in examples}),
        "change": "Example ID suffix plus exact reversed option objects; all other reference fields unchanged",
    })
    print(f"Frozen {len(pairs)} reversal pairs in {output}")


if __name__ == "__main__":
    main()
