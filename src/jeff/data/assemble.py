"""Assemble frozen producer shards against the preassigned pilot group plan."""

import argparse
from collections import Counter
import hashlib
import json
import math
import os
from pathlib import Path

from .validate import load_json, shard_path, validate


def write_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as output:
        json.dump(value, output, indent=2)
        output.write("\n")


def checked_path(root, path):
    return shard_path(root, str(path.relative_to(root)))


def producer_accounting(metadata):
    teacher = metadata.get("teacher", {})
    identity = metadata.get("source_identity", {})
    if not isinstance(identity, dict):
        identity = {}
    provider = teacher.get("provider", identity.get("teacher_provider"))
    model = teacher.get("model_alias", identity.get("teacher_model"))
    if not all(isinstance(value, str) and value.strip() for value in (provider, model)):
        raise ValueError("producer must identify its actual teacher/source")
    cost = metadata.get("cost", {})
    usage = metadata.get("usage_and_license", {})
    if cost.get("currency", "GBP") != "GBP":
        raise ValueError("cost accounting requires explicit GBP conversion")
    amounts = []
    for key in ("additional_spend", "pending_spend"):
        value = metadata.get(key + "_gbp", cost.get(key, usage.get(key + "_gbp")))
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError("producer cost must be explicit and nonnegative: " + key)
        amounts.append(value)
    revision = teacher.get("immutable_revision", identity.get("immutable_teacher_revision"))
    alias = provider + "/" + model + (" (immutable revision unavailable)" if revision is None else "@" + str(revision))
    return alias, amounts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--artifacts-dir", default=os.environ.get("JEFF_ARTIFACTS_DIR"))
    args = parser.parse_args()
    if not args.artifacts_dir:
        parser.error("set JEFF_ARTIFACTS_DIR or --artifacts-dir")
    root = Path(args.artifacts_dir).resolve()
    config = load_json(args.config.read_text())
    directory = shard_path(root, config["artifact_prefix"])
    manifest = {"schema_version": "0.1", "dataset_id": config["dataset_id"], "shards": []}
    provenance = {"schema_version": "0.1", "dataset_id": config["dataset_id"],
                  "assignment_config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
                  "additional_spend_gbp": 0, "pending_spend_gbp": 0, "sources": []}
    for assignment in config["assignments"]:
        original = checked_path(root, directory / assignment["artifact_directory"])
        published = checked_path(root, directory / assignment.get("published_directory", assignment["artifact_directory"]))
        if not original.is_relative_to(directory) or not published.is_relative_to(directory):
            raise ValueError("producer paths must stay inside the configured dataset directory")
        allocation = load_json(checked_path(root, original / "group_assignments.json").read_text())
        allocated = allocation.get("groups", allocation)
        metadata_path = checked_path(root, published / "metadata.json")
        metadata = load_json(metadata_path.read_text())
        alias, (actual, pending) = producer_accounting(metadata)
        provenance["additional_spend_gbp"] += actual
        provenance["pending_spend_gbp"] += pending
        source = {"task_family": assignment["task_family"], "metadata_path": str(metadata_path.relative_to(root)),
                  "teacher_alias": alias, "artifact_sha256": {}}
        bases = set()
        for item in sorted(set(original.glob("*.py")) | set(original.glob("*.json")) | set(published.glob("*.json"))):
            item = checked_path(root, item)
            source["artifact_sha256"][str(item.relative_to(root))] = hashlib.sha256(item.read_bytes()).hexdigest()
        for split in ("train", "validation"):
            path = checked_path(root, published / (split + ".jsonl"))
            payload = path.read_bytes()
            rows = [load_json(line) for line in payload.decode().splitlines()]
            planned = {assignment["group_namespace"] + g for g in assignment[split + "_groups"]}
            observed = Counter(row["group_id"] for row in rows)
            if set(observed) != planned or any(n != assignment["rows_per_group"] for n in observed.values()):
                raise ValueError("row/group plan mismatch: " + str(path))
            for row in rows:
                bases.add(row["provenance"]["label_basis"])
                if row["split"] != split or allocated[row["group_id"]]["split"] != split:
                    raise ValueError("frozen allocation mismatch: " + row["id"])
                if row["task_family"] != assignment["task_family"]:
                    raise ValueError("family allocation mismatch: " + row["id"])
            manifest["shards"].append({"path": str(path.relative_to(root)), "split": split,
                                       "sha256": hashlib.sha256(payload).hexdigest(), "rows": len(rows)})
        source["label_basis"] = next(iter(bases)) if len(bases) == 1 else sorted(bases)
        provenance["sources"].append(source)
    for key in ("additional_spend_gbp", "pending_spend_gbp"):
        if provenance[key] != config[key]:
            raise ValueError("reported producer spending differs from configured accounting: " + key)
    candidate = directory / "candidate-manifest.json"
    write_new(candidate, manifest)
    report = validate(candidate, root)
    write_new(args.report, report)
    if not report["valid"]:
        raise SystemExit("assembly rejected; inspect " + str(args.report))
    write_new(args.manifest, manifest)
    write_new(directory / "manifest.json", manifest)
    write_new(directory / "provenance.json", provenance)
    write_new(args.manifest.with_name(args.manifest.stem + ".provenance.json"), provenance)
    print(json.dumps({"dataset_id": manifest["dataset_id"], "rows": report["rows"], "counts": report["counts"],
                      "manifest": str(args.manifest), "likely_duplicate_counts": report["likely_duplicate_counts"]}))


if __name__ == "__main__":
    main()
