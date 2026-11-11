"""Audit expansion boundaries and exploratory shortcuts without loading a model."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import runpy

from .assemble import write_new
from .validate import canonical_text, load_json, shard_path


def load_manifest(path, root):
    if any(part in {"evaluation", "final"} for part in path.resolve().parts):
        raise ValueError("training audit refuses evaluation/final manifests")
    manifest = load_json(path.read_text())
    rows, assignments, hashes = [], {}, {}
    for entry in manifest["shards"]:
        if entry["split"] not in {"train", "validation"}:
            raise ValueError("training audit refuses final shards")
        source = shard_path(root, entry["path"])
        payload = source.read_bytes()
        if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
            raise ValueError("hash mismatch: " + str(source))
        part = [load_json(line) for line in payload.decode().splitlines()]
        if len(part) != entry["rows"] or any(r["split"] != entry["split"] for r in part):
            raise ValueError("count/split mismatch: " + str(source))
        rows.extend(part)
        hashes[entry["path"]] = entry["sha256"]
        allocation = shard_path(root, str(source.parent.relative_to(root) / "group_assignments.json"))
        if allocation.exists():
            plan = load_json(allocation.read_text())
            assignments.update(plan.get("groups", plan))
    return manifest, rows, assignments, hashes


def content_key(row):
    return (canonical_text(row["state"]), canonical_text(row["question"]),
            tuple(sorted(canonical_text(o["text"]) for o in row["options"])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--parent-manifest", required=True, type=Path)
    parser.add_argument("--historical-manifest", action="append", default=[], type=Path)
    parser.add_argument("--artifacts-dir", required=True, type=Path)
    parser.add_argument("--research-script", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.artifacts_dir.resolve()
    manifest, rows, assignments, hashes = load_manifest(args.manifest, root)
    parent, parent_rows, _, parent_hashes = load_manifest(args.parent_manifest, root)
    parent_ids = {row["id"] for row in parent_rows}
    current = {row["id"]: row for row in rows}
    errors = []
    if len(current) != len(rows):
        errors.append("duplicate current IDs")
    if any(entry not in manifest["shards"] for entry in parent["shards"]):
        errors.append("parent shard entry omitted or changed")
    if any(current.get(row["id"]) != row for row in parent_rows):
        errors.append("parent row omitted or changed")
    historical = list(parent_rows)
    for path in args.historical_manifest:
        _, part, _, recorded = load_manifest(path, root)
        historical.extend(part)
        parent_hashes.update(recorded)
    group_splits, scenario_splits = {}, {}
    for row in historical + rows:
        if group_splits.setdefault(row["group_id"], row["split"]) != row["split"]:
            errors.append("historical group crossed splits: " + row["group_id"])
        scenario = row["provenance"].get("scenario_id")
        if scenario and scenario_splits.setdefault(scenario, row["split"]) != row["split"]:
            errors.append("policy scenario crossed splits: " + scenario)
    old_validation = {content_key(row): row["id"] for row in historical if row["split"] == "validation"}
    for row in rows:
        if row["split"] == "train" and content_key(row) in old_validation:
            errors.append("historical validation input in train: " + row["id"])
    new = [row for row in rows if row["id"] not in parent_ids]
    # Reuse the reviewed CPU diagnostics without changing Research-owned code.
    research = runpy.run_path(str(args.research_script.resolve()))
    strata = {}
    for name, part in (("inherited_v1", parent_rows), ("new_v2", new), ("combined_v2", rows)):
        summary, records = research["shortcut_summary"](part)
        strata[name] = {"rows": len(part), "shortcuts": summary}
        write_new(args.output.parent / (name + "-heuristic-rows.json"), records)
    comparison_rows = list(current.values())
    comparison_ids = set(current)
    for row in historical:
        if row["id"] not in comparison_ids:
            comparison_rows.append(row)
            comparison_ids.add(row["id"])
    overlap = research["overlap_summary"](comparison_rows)
    overlap["word_normalized_full_input_collisions"] = overlap.pop("exact_normalized_full_input")
    overlap["word_normalized_state_collisions"] = overlap.pop("exact_normalized_state")
    overlap["qualification"] = "Word normalization removes meaningful code symbols/case. Such collisions are lexical flags, NOT exact duplicates or conflicting labels. Exact checks preserve those characters. Historical comparison includes tiny rows, not just v2."
    coverage = {}
    for family in ("intent", "sentiment", "rule_application"):
        for split in ("train", "validation"):
            part = [row for row in new if row["task_family"] == family and row["split"] == split]
            groups = {row["group_id"] for row in part}
            domains = {assignments[g].get("domain") for g in groups} - {None}
            mechanisms = {assignments[g].get("mechanism") for g in groups} - {None}
            policies = {r["provenance"].get("scenario_id") for r in part} - {None}
            coverage[split + "/" + family] = {"rows": len(part), "groups": len(groups), "named_domains": len(domains),
                "named_mechanisms": len(mechanisms), "policy_scenarios": len(policies),
                "rows_per_group": dict(Counter(Counter(r["group_id"] for r in part).values()))}
    report = {"schema_version": "0.1", "dataset_id": manifest["dataset_id"], "valid_boundaries": not errors,
        "errors": errors, "manifest_sha256": hashlib.sha256(args.manifest.read_bytes()).hexdigest(),
        "parent_dataset_id": parent["dataset_id"], "parent_manifest_sha256": hashlib.sha256(args.parent_manifest.read_bytes()).hexdigest(),
        "parent_shards_preserved": len(parent["shards"]), "parent_rows_preserved": len(parent_rows),
        "source_sha256": hashes, "historical_sha256": parent_hashes,
        "research_script_sha256": hashlib.sha256(args.research_script.read_bytes()).hexdigest(),
        "strata": strata, "new_coverage": coverage, "historical_overlap": overlap,
        "limitations": ["Exploratory reference-label diagnostics, not independent accuracy or causal evidence of model shortcuts",
                        "Singleton source IDs and separately authored policies do not establish statistical independence",
                        "Heuristic negative findings cannot prove absence of semantic validation derivatives",
                        "Rule mechanisms remain split-disjoint; no seen-mechanism validation claim"]}
    write_new(args.output, report)
    print(json.dumps({"dataset_id": manifest["dataset_id"], "valid_boundaries": not errors,
                      "coverage": coverage, "new_validation_longest_intent": strata["new_v2"]["shortcuts"]["intent"]["validation"]["heuristic_correct"]["longest_characters"],
                      "cross_split_overlap": overlap["pairs_at_least_0_65"], "errors": errors}))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
