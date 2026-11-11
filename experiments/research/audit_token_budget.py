"""Read-only train/validation token-budget audit; no model loading or inference."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path

from tokenizers import Tokenizer


def digest(data):
    return hashlib.sha256(data).hexdigest()


def field_tokens(encoding, question_start, candidate_start):
    counts = Counter()
    for sequence, (start, end), special in zip(
        encoding.sequence_ids, encoding.offsets, encoding.special_tokens_mask
    ):
        if special or start == end:
            continue
        if sequence == 0 and end > question_start:
            counts["question"] += 1
        elif sequence == 1 and end > candidate_start:
            counts["candidate"] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--tokenizer", type=Path, required=True)
    parser.add_argument("--tokenizer-source", required=True)
    parser.add_argument("--max-length", type=int, nargs="+", default=[128, 256, 512])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if any(length < 4 for length in args.max_length):
        raise ValueError("Pair budgets must allow special tokens and both sequences")
    if "final" in args.manifest.resolve().parts:
        raise ValueError("Reserved final artifacts are not research inputs")
    manifest_bytes = args.manifest.read_bytes()
    manifest = json.loads(manifest_bytes)
    root = args.artifacts_dir.resolve()
    shard_paths = []
    for shard in manifest["shards"]:
        path = (root / shard["path"]).resolve()
        if shard["split"] not in {"train", "validation"} or "final" in path.parts:
            raise ValueError("Only published train/validation shards are allowed")
        if not path.is_relative_to(root):
            raise ValueError("Shard path must remain inside the artifact root")
        shard_paths.append((shard, path))
    rows = []
    for shard, path in shard_paths:
        data = path.read_bytes()
        if digest(data) != shard["sha256"]:
            raise ValueError(f"Published shard hash mismatch: {path}")
        shard_rows = [json.loads(line) for line in data.splitlines() if line.strip()]
        if len(shard_rows) != shard["rows"]:
            raise ValueError(f"Published row count mismatch: {path}")
        if any(row["split"] != shard["split"] for row in shard_rows):
            raise ValueError(f"Row split disagrees with manifest: {path}")
        rows.extend(shard_rows)
    if not rows:
        raise ValueError("No train/validation data to audit")

    tokenizer_bytes = args.tokenizer.read_bytes()
    full = Tokenizer.from_str(tokenizer_bytes.decode())
    full.no_padding()
    full.no_truncation()
    truncated = {}
    for length in sorted(set(args.max_length)):
        tokenizer = Tokenizer.from_str(tokenizer_bytes.decode())
        tokenizer.no_padding()
        tokenizer.enable_truncation(length, strategy="longest_first", direction="right")
        truncated[length] = tokenizer
    lengths = []
    summaries = {length: Counter() for length in truncated}
    affected = {length: [] for length in truncated}
    for row in rows:
        prefix = f"State:\n{row['state']}\nQuestion:\n"
        first = prefix + row["question"]
        for option in row["options"]:
            second = "Candidate:\n" + option["text"]
            reference = full.encode(first, second)
            original = field_tokens(reference, len(prefix), len("Candidate:\n"))
            lengths.append(len(reference.ids))
            for length, tokenizer in truncated.items():
                encoded = tokenizer.encode(first, second)
                retained = field_tokens(encoded, len(prefix), len("Candidate:\n"))
                lost_question = original["question"] - retained["question"]
                lost_candidate = original["candidate"] - retained["candidate"]
                summary = summaries[length]
                summary["candidate_pairs"] += 1
                summary["over_budget_pairs"] += int(len(reference.ids) > length)
                summary["question_loss_pairs"] += int(lost_question > 0)
                summary["candidate_loss_pairs"] += int(lost_candidate > 0)
                if lost_question or lost_candidate:
                    affected[length].append({
                        "id": row["id"], "option_id": option["id"],
                        "split": row["split"], "task_family": row["task_family"],
                        "full_pair_tokens": len(reference.ids),
                        "question_tokens_lost": lost_question,
                        "candidate_tokens_lost": lost_candidate,
                    })
    lengths.sort()
    report = {
        "kind": "token_budget_data_audit", "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset_id": manifest["dataset_id"], "manifest": str(args.manifest.resolve()),
        "manifest_sha256": digest(manifest_bytes), "rows": len(rows),
        "split_counts": dict(Counter(row["split"] for row in rows)),
        "tokenizer_source": args.tokenizer_source,
        "tokenizer_sha256": digest(tokenizer_bytes),
        "tokenizers_version": importlib.metadata.version("tokenizers"),
        "script_sha256": digest(Path(__file__).read_bytes()),
        "format": "(State:\\n{state}\\nQuestion:\\n{question}, Candidate:\\n{option.text})",
        "truncation": "longest_first, right; exact Rust tokenizer, no model execution",
        "full_pair_tokens": {
            "min": lengths[0], "p50": lengths[math.ceil(len(lengths) * .5) - 1],
            "p95": lengths[math.ceil(len(lengths) * .95) - 1], "max": lengths[-1],
        },
        "budgets": {str(length): {**dict(summaries[length]), "affected": affected[length]}
                    for length in truncated},
        "limitations": [
            "Token-budget evidence only; no model accuracy, latency or peak-memory measurement.",
            "Budgets share examples and are not independent evaluation samples.",
            "No claim about unseen longer inputs or reserved final evaluation.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output.resolve()), "dataset_id": report["dataset_id"],
                      "rows": len(rows), "full_pair_tokens": report["full_pair_tokens"],
                      "budgets": {key: {k: v for k, v in value.items() if k != "affected"}
                                  for key, value in report["budgets"].items()}}))


if __name__ == "__main__":
    main()
