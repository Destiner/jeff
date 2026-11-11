"""Freeze one evaluation reference file from a published validation manifest."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from .common import fingerprint, load_examples, parse_json, validate_examples, write_json, write_jsonl


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    root = Path(os.environ["JEFF_ARTIFACTS_DIR"]).resolve()
    manifest = parse_json(Path(args.manifest).read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "0.1" or not manifest.get("dataset_id"):
        raise ValueError("Expected a version 0.1 dataset manifest")
    shards = manifest.get("shards")
    if not isinstance(shards, list) or not shards:
        raise ValueError("Manifest needs nonempty shards")
    if any(shard.get("split") not in ("train", "validation") for shard in shards):
        raise ValueError("This assembly command never consumes final manifests")
    rows, sources, paths = [], [], set()
    for shard in shards:
        if shard["split"] != "validation":
            continue
        relative = Path(shard["path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or root not in path.parents or path in paths:
            raise ValueError("Shard path must be distinct and relative inside the artifact root")
        if root / "evaluation" / "final" in path.parents:
            raise ValueError("Reserved final paths cannot be validation sources")
        paths.add(path)
        identity = fingerprint(path)
        if identity["sha256"] != shard["sha256"]:
            raise ValueError("Shard SHA-256 mismatch")
        examples = load_examples(path)
        if type(shard["rows"]) is not int or len(examples) != shard["rows"] or any(row["split"] != "validation" for row in examples):
            raise ValueError("Shard row count/split mismatch")
        rows.extend(examples)
        sources.append({**identity, "rows": len(examples)})
    if not rows:
        raise ValueError("No validation examples")
    validate_examples(rows)
    output = Path(args.output_dir).resolve()
    if root / "evaluation" not in output.parents or root / "evaluation" / "final" in output.parents:
        raise ValueError("Validation output must stay in the non-final evaluation artifact subtree")
    output.mkdir(parents=True, exist_ok=False)
    reference = output / "validation.jsonl"
    write_jsonl(reference, rows)
    write_json(output / "manifest.json", {
        "schema_version": "0.1", "dataset_id": args.dataset_id,
        "shards": [{"path": str(reference.relative_to(root)), "split": "validation", "rows": len(rows),
                    "sha256": fingerprint(reference)["sha256"]}],
    })
    write_json(output / "assembly-receipt.json", {
        "schema_version": "evaluation/0.1", "source_dataset_id": manifest["dataset_id"],
        "source_manifest": fingerprint(args.manifest), "validation_sources": sources,
        "reference": fingerprint(reference), "rows": len(rows),
        "scope": "Validation shard hashes/counts/splits and combined references checked; train content untouched. Cross-split deduplication remains Data-owned.",
    })
    print(f"Assembled {len(rows)} validation rows from {len(sources)} verified shards: {reference}")


if __name__ == "__main__":
    main()
