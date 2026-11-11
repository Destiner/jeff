"""Validate training manifests and report lexical duplication (stdlib only)."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata

FAMILIES = {"intent", "sentiment", "rule_application"}
SPLITS = {"train", "validation"}


def normalized(text):
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", text).casefold()))


def canonical_text(text):
    # Signs, brackets, case and internal spacing can be the rule's task data.
    return unicodedata.normalize("NFC", text).strip()


def load_json(text):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError("nonfinite JSON constant: " + value)

    return json.loads(text, object_pairs_hook=unique, parse_constant=reject_constant)


def shard_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("shard path must be a nonempty relative path")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("shard path escapes artifact root")
    # This validator belongs to training data; never open evaluation storage.
    if "evaluation" in path.relative_to(root).parts or "final" in path.relative_to(root).parts:
        raise ValueError("evaluation/final storage is not a training-data input")
    return path


def row_errors(row, split):
    errors = []
    if not isinstance(row, dict):
        return ["row must be an object"]
    if row.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1")
    for key in ("id", "question", "group_id", "target_id"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            errors.append(key + " must be a nonempty string")
    if not isinstance(row.get("state"), str):
        errors.append("state must be a string")
    if not isinstance(row.get("task_family"), str) or row["task_family"] not in FAMILIES:
        errors.append("family is not reserved for training")
    if row.get("split") != split:
        errors.append("row split differs from shard split")
    options = row.get("options")
    if not isinstance(options, list) or len(options) < 2:
        errors.append("at least two options required")
    else:
        option_ids, texts = [], []
        for option in options:
            if not isinstance(option, dict):
                errors.append("option must be an object")
                continue
            for key in ("id", "text"):
                if not isinstance(option.get(key), str) or not option[key].strip():
                    errors.append("option " + key + " must be a nonempty string")
            if isinstance(option.get("id"), str):
                option_ids.append(option["id"])
            if isinstance(option.get("text"), str):
                texts.append(canonical_text(option["text"]))
        if len(option_ids) != len(set(option_ids)):
            errors.append("duplicate option IDs")
        if len(texts) != len(set(texts)):
            errors.append("duplicate normalized option descriptions")
        if option_ids.count(row.get("target_id")) != 1:
            errors.append("target must identify exactly one option")
    provenance = row.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("provenance must be an object")
    else:
        if not isinstance(provenance.get("kind"), str) or provenance["kind"] not in {"teacher", "public_dataset", "programmatic", "human"}:
            errors.append("invalid provenance kind")
        if not isinstance(provenance.get("label_basis"), str) or provenance["label_basis"] not in {"teacher", "source_label", "rule_verified", "human_verified"}:
            errors.append("invalid label_basis")
        for key in ["source"] + (["teacher_model"] if provenance.get("kind") == "teacher" or provenance.get("label_basis") == "teacher" else []):
            if not isinstance(provenance.get(key), str) or not provenance[key].strip():
                errors.append("missing provenance " + key)
    return errors


def validate(manifest_path, artifact_root):
    root = Path(artifact_root).resolve()
    report = {"schema_version": "0.1", "manifest": str(Path(manifest_path).resolve()),
              "errors": [], "warnings": [], "likely_duplicates": [], "shards": []}
    errors, warnings = report["errors"], report["warnings"]
    try:
        raw = Path(manifest_path).read_bytes()
        manifest = load_json(raw.decode("utf-8"))
        report["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be an object")
        report["dataset_id"] = manifest.get("dataset_id")
        if manifest.get("schema_version") != "0.1":
            errors.append("manifest schema_version must be 0.1")
        if not isinstance(manifest.get("dataset_id"), str) or not manifest["dataset_id"].strip():
            errors.append("dataset_id must be nonempty")
        if not isinstance(manifest.get("shards"), list) or not manifest["shards"]:
            raise ValueError("nonempty shards list required")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
        report["valid"] = False
        return report

    rows, seen_paths = [], set()
    for entry in manifest["shards"]:
        try:
            if not isinstance(entry, dict):
                raise ValueError("shard entry must be an object")
            if not isinstance(entry.get("split"), str) or entry["split"] not in SPLITS:
                raise ValueError("training manifests must reject final/unknown splits before reading")
            path = shard_path(root, entry.get("path"))
            if path in seen_paths:
                raise ValueError("duplicate shard path")
            seen_paths.add(path)
            if type(entry.get("rows")) is not int or entry["rows"] < 1:
                raise ValueError("shard rows must be a positive integer")
            if not isinstance(entry.get("sha256"), str) or not re.fullmatch("[0-9a-f]{64}", entry["sha256"]):
                raise ValueError("invalid sha256")
            payload = path.read_bytes()
            if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
                raise ValueError("shard hash mismatch: " + entry["path"])
            lines = payload.decode("utf-8").splitlines()
            if len(lines) != entry["rows"]:
                errors.append(entry["path"] + ": row count mismatch")
            report["shards"].append({"path": entry["path"], "rows": len(lines), "split": entry["split"]})
            for number, line in enumerate(lines, 1):
                location = f"{entry['path']}:{number}"
                try:
                    row = load_json(line)
                    issues = row_errors(row, entry["split"])
                except ValueError as exc:
                    issues = [str(exc)]
                if issues:
                    errors.extend(location + ": " + issue for issue in issues)
                else:
                    rows.append(row)
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(str(exc))

    ids, group_splits, exact = set(), {}, {}
    counts, group_counts, positions, options, provenance = (Counter() for _ in range(5))
    state_pairs = defaultdict(list)
    for row in rows:
        row_id, group, split = row["id"], row["group_id"], row["split"]
        if row_id in ids:
            errors.append("duplicate example ID: " + row_id)
        ids.add(row_id)
        if group_splits.setdefault(group, split) != split:
            errors.append("cross-split group: " + group)
        key = split + "/" + row["task_family"]
        counts[key] += 1
        position = next(i for i, o in enumerate(row["options"]) if o["id"] == row["target_id"])
        positions[f"{key}/{len(row['options'])}-choices/{position}"] += 1
        options[f"{key}/{len(row['options'])}"] += 1
        provenance[split + "/" + row["provenance"]["label_basis"]] += 1
        if len(row["options"]) > 6:
            warnings.append(row_id + ": more than six choices (valid contract, outside pilot target)")
        context = (canonical_text(row["state"]), canonical_text(row["question"]))
        content = context + (tuple(sorted(canonical_text(o["text"]) for o in row["options"])),)
        target = canonical_text(row["options"][position]["text"])
        if content in exact:
            prior, prior_target = exact[content]
            errors.append(f"exact normalized input duplicate: {prior} / {row_id}")
            if target != prior_target:
                errors.append(f"conflicting targets: {prior} / {row_id}")
        exact[content] = (row_id, target)
        state_pairs[context].append(row_id)
    for group, split in group_splits.items():
        family = next(r["task_family"] for r in rows if r["group_id"] == group)
        group_counts[split + "/" + family] += 1
    for ids_at_context in state_pairs.values():
        if len(ids_at_context) > 1:
            warnings.append("repeated state/question: " + ", ".join(ids_at_context))

    shingles = []
    for row in rows:
        # Ignore candidate boilerplate; lexical similarity is a review aid, not proof.
        tokens = normalized(row["state"] or row["question"]).split()
        shingles.append(set(zip(tokens, tokens[1:], tokens[2:])) if len(tokens) >= 3 else set(tokens))
    for i, left in enumerate(rows):
        for j in range(i + 1, len(rows)):
            right = rows[j]
            a, b = shingles[i], shingles[j]
            score = len(a & b) / len(a | b) if a | b else 1.0
            if score >= 0.65:
                report["likely_duplicates"].append({"left": left["id"], "right": right["id"],
                    "similarity": round(score, 4), "same_group": left["group_id"] == right["group_id"],
                    "cross_split": left["split"] != right["split"]})
    report.update(valid=not errors, rows=len(rows), counts=dict(sorted(counts.items())),
                  groups=dict(sorted(group_counts.items())), option_counts=dict(sorted(options.items())),
                  target_positions_zero_based=dict(sorted(positions.items())), label_basis=dict(sorted(provenance.items())),
                  duplicate_method="Full-input NFC/outer-whitespace canonicalization preserving signs, brackets, case and internal spaces; order-independent choices. Heuristic state NFKC/casefold word-trigram Jaccard >=0.65; no semantic completeness claim",
                  likely_duplicate_counts=dict(Counter("cross_split" if p["cross_split"] else "within_group" if p["same_group"] else "cross_group_same_split" for p in report["likely_duplicates"])))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--artifacts-dir", default=os.environ.get("JEFF_ARTIFACTS_DIR"))
    args = parser.parse_args()
    if not args.artifacts_dir:
        parser.error("set JEFF_ARTIFACTS_DIR or --artifacts-dir")
    report = validate(args.manifest, args.artifacts_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps({k: report.get(k) for k in ("dataset_id", "valid", "rows", "counts", "errors", "likely_duplicate_counts")}))
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
