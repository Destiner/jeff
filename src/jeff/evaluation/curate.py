"""Freeze teacher-authored source cases into contract-format evaluation shards."""
from __future__ import annotations

import argparse
from collections import Counter
import os
from pathlib import Path

from .common import fingerprint, parse_json, validate_examples, write_json, write_jsonl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="JSON array of compact source cases; keep final sources private")
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--split", required=True, choices=("validation", "final"))
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--teacher-model", default="unknown")
    parser.add_argument("--reverse-pairs", action="store_true")
    args = parser.parse_args()
    root = Path(os.environ.get("JEFF_ARTIFACTS_DIR", "/Users/destiner/Code/jeff/artifacts")).resolve()
    output = Path(args.output_dir).resolve()
    if root / "evaluation" not in output.parents:
        raise ValueError("Output must be inside the shared evaluation artifact root")
    is_final_path = root / "evaluation" / "final" in output.parents
    if (args.split == "final") != is_final_path:
        raise ValueError("Final data must use evaluation/final; validation must not")
    if args.reverse_pairs and args.split != "validation":
        raise ValueError("Option-order probes are validation-only")
    cases = parse_json(Path(args.source).read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("Source must be a nonempty case array")
    rows, pairs = [], []
    for case in cases:
        options = [{"id": f"o{index}", "text": text} for index, text in enumerate(case["options"])]
        index = case["target"]
        if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(options):
            raise ValueError("Target must be a valid zero-based option index")
        row = {"schema_version": "0.1", "id": case["key"], "group_id": case["key"],
               "state": case["state"], "question": case["question"], "options": options,
               "target_id": options[index]["id"], "task_family": case["family"], "split": args.split,
               "provenance": {"kind": "teacher", "source": args.dataset_id,
                              "label_basis": "teacher", "teacher_model": args.teacher_model}}
        if args.reverse_pairs:
            original = {**row, "id": row["id"] + ".original"}
            reversed_row = {**row, "id": row["id"] + ".reversed", "options": list(reversed(options))}
            rows.extend((original, reversed_row))
            pairs.append({"group_id": row["group_id"], "original_id": original["id"], "reversed_id": reversed_row["id"],
                          "challenge": case.get("challenge")})
        else:
            rows.append(row)
    validated = validate_examples(rows)
    output.mkdir(parents=True, exist_ok=False)
    shard = output / (args.split + ".jsonl")
    write_jsonl(shard, validated)
    manifest = {"schema_version": "0.1", "dataset_id": args.dataset_id,
                "shards": [{"path": str(shard.relative_to(root)), "split": args.split,
                            "sha256": fingerprint(shard)["sha256"], "rows": len(validated)}]}
    write_json(output / "manifest.json", manifest)
    write_json(output / "metadata.json", {
        "schema_version": "evaluation/0.1", "dataset_id": args.dataset_id,
        "source_file": fingerprint(args.source), "source": "Original agent-authored fictional cases; separate curator workstream",
        "teacher_model": args.teacher_model, "label_basis": "teacher", "independently_verified": False,
        "external_dataset": None, "usage": "Generated output subject to applicable service terms; no third-party dataset license asserted",
        "cost_gbp": 0, "generation_settings": "Existing approved agent access; no paid API calls; manual compact-case serialization",
        "families": dict(sorted(Counter(row["task_family"] for row in validated).items())),
        "groups": len({row["group_id"] for row in validated}), "reverse_pairs": args.reverse_pairs,
        "structural_validation": "passed; unique IDs, option/target validity, one split, reserved family, provenance",
        "final_gate": "Unscored and sealed until checkpoint/configuration freeze" if args.split == "final" else None,
    })
    if pairs:
        write_json(output / "pairs.json", pairs)
    print(f"Frozen {args.dataset_id}: {len(validated)} rows; manifest={output / 'manifest.json'}")


if __name__ == "__main__":
    main()
