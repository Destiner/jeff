"""Reproduce R3 candidate shortcuts with R2 helpers; no ML or dataset writes."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path

from audit_pilot_shortcuts import sha, shortcut_summary


CANDIDATE = "data/data-pilot-v2/pre-review-r2/manifest.json"
CANDIDATE_SHA256 = "345e935b46ca3d1226dfd603208bf5d1e1e16982d425319f678e34447b0c9483"
PARENT = "data/data-pilot-v1/manifest.json"
PARENT_SHA256 = "62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180"
DATA_AUDIT = "data/data-pilot-v2/quality-audit/audit.json"
DATA_AUDIT_SHA256 = "d044f6d2e55594962648a10344f441a8577cac598b523acff915c7b3c2fe2c17"


def read_source(root, relative, hashes, expected=None):
    path = (root / relative).resolve()
    allowed = (root / "data/data-pilot-v1", root / "data/data-pilot-v2")
    if "final" in path.parts or not any(path.is_relative_to(base) for base in allowed):
        raise ValueError("Only pilot-v1/v2 data paths are authorized")
    payload = path.read_bytes()
    digest = sha(payload)
    if expected is not None and digest != expected:
        raise ValueError(f"Frozen input hash mismatch: {relative}")
    hashes[relative] = digest
    return payload


def counts(rows):
    return {
        split: {
            "rows": sum(row["split"] == split for row in rows),
            "groups": len({row["group_id"] for row in rows if row["split"] == split}),
            "families": dict(Counter(row["task_family"] for row in rows if row["split"] == split)),
        }
        for split in ("train", "validation")
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    root, hashes = args.artifacts_dir.resolve(), {}
    manifest = json.loads(read_source(root, CANDIDATE, hashes, CANDIDATE_SHA256))
    parent = json.loads(read_source(root, PARENT, hashes, PARENT_SHA256))
    data_audit = json.loads(read_source(root, DATA_AUDIT, hashes, DATA_AUDIT_SHA256))
    helper = Path(__file__).with_name("audit_pilot_shortcuts.py")
    if data_audit["manifest_sha256"] != CANDIDATE_SHA256 or data_audit["research_script_sha256"] != sha(helper.read_bytes()):
        raise ValueError("Data receipt must describe this candidate and the unchanged R2 helper")
    if any(entry not in manifest["shards"] for entry in parent["shards"]):
        raise ValueError("Parent shard entry omitted or changed")
    parent_paths = {entry["path"] for entry in parent["shards"]}
    inherited, added, producers, rows = [], [], {}, []
    for entry in manifest["shards"]:
        if entry["split"] not in {"train", "validation"}:
            raise ValueError("Only train/validation are authorized")
        payload = read_source(root, entry["path"], hashes, entry["sha256"])
        if data_audit["source_sha256"].get(entry["path"]) != entry["sha256"]:
            raise ValueError("Data receipt shard identity mismatch")
        part = [json.loads(line) for line in payload.splitlines() if line.strip()]
        if len(part) != entry["rows"] or any(row["split"] != entry["split"] for row in part):
            raise ValueError("Shard count/split mismatch")
        rows.extend(part)
        if entry["path"] in parent_paths:
            inherited.extend(part)
        else:
            added.extend(part)
            producers.setdefault(Path(entry["path"]).parent.name, []).extend(part)
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate candidate IDs")
    if {row["group_id"] for row in inherited} & {row["group_id"] for row in added}:
        raise ValueError("New and inherited groups overlap")
    if {row["group_id"] for row in rows if row["split"] == "train"} & {row["group_id"] for row in rows if row["split"] == "validation"}:
        raise ValueError("Candidate groups cross splits")

    strata = {}
    for name, part in (("new_v2", added), ("combined_v2", rows)):
        summary, _ = shortcut_summary(part)
        if summary != data_audit["strata"][name]["shortcuts"]:
            raise ValueError(f"Reproduction differs from Data receipt: {name}")
        strata[name] = {"counts": counts(part), "shortcuts": summary}
    strata["inherited_v1"] = {
        "counts": counts(inherited),
        "shortcuts": data_audit["strata"]["inherited_v1"]["shortcuts"],
        "evidence": "Reused completed R2/Data receipt; not a repeated v1 investigation",
    }
    report = {
        "task": "R3-frozen-v2-candidate-shortcuts",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashes,
        "script_sha256": sha(Path(__file__).read_bytes()),
        "r2_helper_sha256": sha(helper.read_bytes()),
        "strata": strata,
        "new_producers": {name: shortcut_summary(part)[0] for name, part in sorted(producers.items())},
        "data_receipt_reproduced": ["new_v2/shortcuts", "combined_v2/shortcuts"],
        "limitations": [
            "Hash-pinned pre-review-r2 candidate only; not a release authorization or general validator",
            "Length/fixed selectors use R2 first-option tie breaks; train priors pool each supplied stratum",
            "Producer summaries use producer-only training priors; not comparable to pooled prior scores",
            "Inherited summaries reused; no full lexical scan, label certification or model-use attribution",
            "Fresh denotes added shard/ID lineage, not statistical or semantic independence",
            "Historical v1/tiny exclusions and bounded semantic reviews are separate R3 evidence",
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=False)
    with (args.output_dir / "audit.json").open("x") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output_dir": str(args.output_dir.resolve()), "rows": len(rows),
                      "strata": {name: value["counts"] for name, value in strata.items()},
                      "new_intent_longest_validation": strata["new_v2"]["shortcuts"]["intent"]["validation"]["heuristic_correct"]["longest_characters"]}))


if __name__ == "__main__":
    main()
