"""Remove pilot authoring shortcuts without changing teacher sentiment labels."""

import argparse
import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import random
import re
import shutil

PATTERNS = [
    r"What sentiment does the writer express toward (.+)\?",
    r"Considering only (.+), which description matches the writer's attitude\?",
    r"Which description matches the expressed attitude toward (.+)\?",
    r"Which option best captures the writer's sentiment about (.+), rather than other things mentioned\?",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be a new directory; never rewrite published shards")
    source_script = (args.source / "generate.py").read_text()
    option_sets = None
    # Read fixed option vocabulary without executing the original generator.
    for node in ast.parse(source_script).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "OPTION_SETS" for t in node.targets):
            option_sets = ast.literal_eval(node.value)
    if option_sets is None:
        raise ValueError("source option vocabulary missing")
    labels = {text: label for vocabulary in option_sets for label, text in vocabulary.items()}
    rng = random.Random(20261111)
    rows_by_split, mapping, buckets = {}, [], defaultdict(list)
    parent_hashes = {}
    for split in ("train", "validation"):
        path = args.source / (split + ".jsonl")
        parent_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        rows_by_split[split] = rows
        for row in rows:
            target_text = next(o["text"] for o in row["options"] if o["id"] == row["target_id"])
            label = labels[target_text]
            buckets[(split, label)].append(row)
    positions = {}
    for (_, label), bucket in sorted(buckets.items()):
        shuffled = bucket[:]
        rng.shuffle(shuffled)
        # Balance positions within each class as well as across the complete split.
        offset = "PNUM".index(label)
        for i, row in enumerate(shuffled):
            positions[row["id"]] = (i + offset) % 4
    for split, rows in rows_by_split.items():
        for row in rows:
            old_id = row["id"]
            target_text = next(o["text"] for o in row["options"] if o["id"] == row["target_id"])
            label = labels[target_text]
            matches = [m for pattern in PATTERNS if (m := re.fullmatch(pattern, row["question"]))]
            if len(matches) != 1:
                raise ValueError("ambiguous subject extraction: " + old_id)
            subject = matches[0].group(1)
            row["id"] = old_id.replace("data:pilot-v1:sentiment:", "data:pilot-v1:sentiment-r2:")
            row["question"] = f"What sentiment does the writer express toward {subject}?"
            vocabulary = option_sets[rng.randrange(len(option_sets))]
            ordered = [c for c in "PNUM" if c != label]
            rng.shuffle(ordered)
            ordered.insert(positions[old_id], label)
            row["options"] = [{"id": hashlib.sha256((row["id"] + ":" + str(i)).encode()).hexdigest()[:12],
                               "text": vocabulary[c]} for i, c in enumerate(ordered)]
            row["target_id"] = row["options"][positions[old_id]]["id"]
            original_source = row["provenance"]["source"]
            row["provenance"]["source"] = "data-pilot-v1/sentiment-r2/from/" + original_source
            mapping.append({"id": row["id"], "parent_id": old_id, "subject": subject, "class": label,
                            "change": "question wording and candidate set/order only; state, group, split and teacher judgment preserved"})
    args.output.mkdir(parents=True)
    for split, rows in rows_by_split.items():
        with (args.output / (split + ".jsonl")).open("x") as output:
            for row in rows:
                output.write(json.dumps(row, ensure_ascii=False) + "\n")
    shutil.copyfile(args.source / "group_assignments.json", args.output / "group_assignments.json")
    metadata = {"schema_version": "0.1", "shard_id": "data-pilot-v1-sentiment-r2",
        "teacher": {"provider": "openai", "model_alias": "gpt-sol", "immutable_revision": None},
        "revision_author": "openai/gpt-astra (exposed session alias; revision unknown)",
        "source": "Original synthetic teacher rows in ../sentiment; unchanged state, groups and labels",
        "parent_shard_hashes": parent_hashes, "parent_metadata": "../sentiment/metadata.json",
        "generation_settings": {"method": "deterministic formatting correction; no new semantic labels", "seed": 20261111,
                                "options": "all four mutually exclusive descriptions for every row", "question": "single neutral template, same original subject"},
        "reason": "Original question templates perfectly tracked sentiment class; mixed-choice availability also tracked the target. Remove both avoidable shortcuts before pilot publication.",
        "row_counts": {split: len(rows) for split, rows in rows_by_split.items()},
        "usage_constraints": "Original synthetic content under existing provider terms; no independently cleared redistribution license, external datasets or private records.",
        "additional_spend_gbp": 0, "pending_spend_gbp": 0,
        "limitations": ["Teacher labels are not independently verified", "Explicit sentiment wording and small English-only synthetic coverage remain", "No claim that every possible shortcut is removed"],
        "generator": "python -m jeff.data.prepare_sentiment --source <original-sentiment> --output <new-directory>"}
    for name, value in (("metadata.json", metadata), ("revision_map.json", mapping)):
        with (args.output / name).open("x") as output:
            json.dump(value, output, indent=2)
            output.write("\n")
    print(json.dumps({"output": str(args.output), "rows": metadata["row_counts"], "class_and_subject_preserved": len(mapping)}))


if __name__ == "__main__":
    main()
