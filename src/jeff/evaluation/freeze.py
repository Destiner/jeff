"""Freeze validation identity partitions; never consume final data or run inference."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import subprocess

from .common import (BASES, KINDS, fingerprint, input_only, load_examples, nonempty,
                     parse_json, records, validate_examples, validate_input, write_json, write_jsonl)


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()


def content_hash(row):
    return canonical_hash([row["state"], row["question"], sorted(o["text"] for o in row["options"])])


def safe_path(value):
    path = Path(value).resolve()
    if any(p.lower() == "final" or p.lower().startswith(("final-", "final.", "final_"))
           for p in path.parts):
        raise ValueError(f"Reserved final path: {path}")
    return path


def artifact_path(root, value):
    path = safe_path(root / value)
    if Path(value).is_absolute() or root not in path.parents:
        raise ValueError("Artifact paths must be relative and inside JEFF_ARTIFACTS_DIR")
    return path


def summary(rows):
    result = {"rows": len(rows), "groups": len({r["group_id"] for r in rows})}
    for field in ("task_family", "label_basis", "source"):
        key = lambda r: r[field] if field == "task_family" else r["provenance"][field]
        result[field] = {value: {"rows": count, "groups": len({r["group_id"] for r in rows if key(r) == value})}
                         for value, count in sorted(Counter(key(r) for r in rows).items())}
    return result


def identity(row, stratum, origin):
    return {"id": row["id"], "group_id": row["group_id"], "split": row["split"],
            "task_family": row["task_family"], "stratum": stratum, "origin": origin,
            "row_sha256": canonical_hash(row), "input_sha256": canonical_hash(input_only(row)),
            "order_free_content_sha256": content_hash(row), "provenance": row["provenance"]}


def checkout_identity(code):
    try:
        def git(*args):
            return subprocess.check_output(["git", *args], cwd=code.parent, text=True,
                                           stderr=subprocess.DEVNULL).strip()
        root = Path(git("rev-parse", "--show-toplevel")).resolve()
        relative = code.relative_to(root)
        git("ls-files", "--error-unmatch", "--", str(relative))
        return {"code_revision": git("rev-parse", "HEAD"),
                "tracked_dirty_at_execution": bool(git("status", "--porcelain", "--untracked-files=no")),
                "code_checkout": str(root), "code_checkout_status": "imported helper is tracked by this checkout"}
    except (OSError, ValueError, subprocess.CalledProcessError):
        return {"code_revision": None, "tracked_dirty_at_execution": None,
                "code_checkout": None, "code_checkout_status": "unknown: imported helper is not in an owning Git checkout; use code hashes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("examples", "v1-manifest", "source-manifest", "provenance", "probes", "output-dir"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--new-source", action="append", default=[], help="Exact provenance.source; repeatable")
    parser.add_argument("--new-sources", help="JSON array of exact source strings, supplied by release owner")
    parser.add_argument("--publication-status", required=True, choices=("candidate", "released"))
    args = parser.parse_args()
    root = Path(os.environ["JEFF_ARTIFACTS_DIR"]).resolve()
    output = safe_path(args.output_dir)
    if output.parent != root / "evaluation" or output.exists():
        raise ValueError("Output must be a new direct child of artifacts/evaluation/<unique-id>/")
    # Resolve all explicit paths before opening any input, including the allowlist.
    paths = {key: safe_path(getattr(args, key)) for key in
             ("examples", "v1_manifest", "source_manifest", "provenance", "probes")}
    if args.new_sources:
        paths["new_sources"] = safe_path(args.new_sources)
    pins = {}

    def pin(path):
        value = fingerprint(path)
        previous = pins.setdefault(str(path), value)
        if value != previous:
            raise ValueError(f"Input changed while freezing: {path}")
        return value

    def document(path):
        pin(path)
        return parse_json(path.read_text(encoding="utf-8"))

    def manifest(path, complete):
        doc = document(path)
        if not isinstance(doc, dict) or doc.get("schema_version") != "0.1" or not nonempty(doc.get("dataset_id")):
            raise ValueError("Expected a version 0.1 dataset manifest")
        shards = doc.get("shards")
        if not isinstance(shards, list) or not shards:
            raise ValueError("Manifest needs nonempty shards")
        seen, planned = set(), []
        for shard in shards:
            if not isinstance(shard, dict) or shard.get("split") not in ("train", "validation"):
                raise ValueError("Only train/validation manifests are accepted; no final shard reads")
            shard_path = artifact_path(root, shard["path"])
            if shard_path in seen or type(shard.get("rows")) is not int or shard["rows"] <= 0:
                raise ValueError("Duplicate shard or invalid shard count")
            if not isinstance(shard.get("sha256"), str) or len(shard["sha256"]) != 64:
                raise ValueError("Invalid shard hash")
            seen.add(shard_path)
            planned.append((shard, shard_path))
        if complete and {s["split"] for s, _ in planned} != {"train", "validation"}:
            raise ValueError("Ancestry requires the complete v1 train+validation manifest")
        rows, origins, group_splits, receipts = [], {}, {}, []
        for shard, shard_path in planned:
            if not complete and shard["split"] != "validation":
                continue
            source = pin(shard_path)
            if source["sha256"] != shard["sha256"]:
                raise ValueError(f"Shard hash mismatch: {shard_path}")
            count = 0
            # load_examples deliberately forbids train; validate ancestry without changing its split.
            for line, row, error in records(shard_path):
                if error:
                    raise ValueError(f"{shard_path}:{line}: {error}")
                options = validate_input(row)
                if row.get("split") != shard["split"] or row["id"] in origins:
                    raise ValueError("Shard split mismatch or duplicate reference ID")
                if row.get("target_id") not in options or not all(nonempty(row.get(k)) for k in ("group_id", "task_family")):
                    raise ValueError("Invalid reference target/group/family")
                prov = row.get("provenance")
                if not isinstance(prov, dict) or prov.get("kind") not in KINDS or prov.get("label_basis") not in BASES or not nonempty(prov.get("source")):
                    raise ValueError("Invalid reference provenance")
                if (prov["kind"] == "teacher" or prov["label_basis"] == "teacher") and not nonempty(prov.get("teacher_model")):
                    raise ValueError("Missing teacher identity (use unknown where unavailable)")
                if row["task_family"] == "passage_entailment":
                    raise ValueError("Reserved final family")
                if group_splits.setdefault(row["group_id"], row["split"]) != row["split"]:
                    raise ValueError("Cross-split ancestry group")
                origins[row["id"]] = {**source, "line": line}
                rows.append(row)
                count += 1
            if count != shard["rows"]:
                raise ValueError("Shard count mismatch")
            receipts.append({**source, "split": shard["split"], "rows": count})
        if not rows:
            raise ValueError("No references in manifest")
        return doc, rows, origins, receipts

    parent, old, old_origins, old_shards = manifest(paths["v1_manifest"], True)
    source, source_rows, origins, source_shards = manifest(paths["source_manifest"], False)
    provenance = document(paths["provenance"])
    if not isinstance(provenance, dict) or provenance.get("dataset_id") != source["dataset_id"]:
        raise ValueError("Provenance dataset does not match source manifest")
    parent_link = provenance.get("parent")
    if not isinstance(parent_link, dict) or parent_link.get("sha256") != pin(paths["v1_manifest"])["sha256"] or parent_link.get("dataset_id") != parent["dataset_id"]:
        raise ValueError("Provenance must pin the supplied complete parent manifest")
    supplied = document(paths["new_sources"]) if "new_sources" in paths else []
    if not isinstance(supplied, list) or not all(nonempty(s) for s in supplied + args.new_source):
        raise ValueError("New-source allowlist must contain exact nonempty strings")
    allowed = set(supplied + args.new_source)
    if not allowed:
        raise ValueError("Explicit new-source allowlist required; no inferred prefixes")

    def validation(path):
        pin(path)
        rows = load_examples(path)
        if not rows or any(r["split"] != "validation" for r in rows):
            raise ValueError("Nonempty validation-only references required")
        return rows

    assembled, probes = validation(paths["examples"]), validation(paths["probes"])
    validate_examples(source_rows)
    expected = {r["id"]: canonical_hash(r) for r in source_rows}
    if {r["id"]: canonical_hash(r) for r in assembled} != expected:
        raise ValueError("Assembled examples differ from verified source validation shards")
    old_by_id = {r["id"]: r for r in old}
    historical = old + probes
    historical_groups = {r["group_id"] for r in historical}
    historical_content = {content_hash(r) for r in historical}
    probe_ids = {r["id"] for r in probes}
    if probe_ids & set(old_by_id) or {r["group_id"] for r in probes} & {r["group_id"] for r in old} or {content_hash(r) for r in probes} & {content_hash(r) for r in old}:
        raise ValueError("Probe/parent overlap is ambiguous")
    partitions = {"inherited-v1": [], "new-v2": [], "probes": probes}
    for row in assembled:
        prior = old_by_id.get(row["id"])
        if prior is not None:
            if canonical_hash(row) != canonical_hash(prior) or prior["split"] != "validation":
                raise ValueError(f"Changed or wrong-split historical ID: {row['id']}")
            stratum = "inherited-v1"
        else:
            if row["id"] in probe_ids or row["group_id"] in historical_groups or content_hash(row) in historical_content:
                raise ValueError(f"Historical identity/group/content conflict: {row['id']}")
            if row["provenance"]["source"] not in allowed:
                raise ValueError(f"Unresolved new provenance source: {row['id']}")
            stratum = "new-v2"
        partitions[stratum].append(row)
    if {r["id"] for r in partitions["inherited-v1"]} != {r["id"] for r in old if r["split"] == "validation"}:
        raise ValueError("Not all old validation rows are present")
    if not partitions["new-v2"] or allowed != {r["provenance"]["source"] for r in partitions["new-v2"]}:
        raise ValueError("New-source allowlist must exactly cover observed newly authored sources")
    if probe_ids & set(expected) or {r["group_id"] for r in probes} & {r["group_id"] for r in assembled}:
        raise ValueError("Probes must remain separate from candidate validation")

    code = Path(__file__).resolve()
    pin(code)
    pin(Path(input_only.__code__.co_filename).resolve())
    code_identity = checkout_identity(code)
    for path in list(pins):
        pin(Path(path))
    output.mkdir(parents=True, exist_ok=False)
    outputs, identities = {}, []
    for stratum, rows in partitions.items():
        directory = output / stratum
        reference, inputs = directory / "validation.jsonl", directory / "inputs.jsonl"
        write_jsonl(reference, rows)
        write_jsonl(inputs, (input_only(r) for r in rows))
        write_json(directory / "manifest.json", {
            "schema_version": "0.1", "dataset_id": f"{output.name}-{stratum}",
            "shards": [{"path": str(reference.relative_to(root)), "split": "validation",
                        "rows": len(rows), "sha256": fingerprint(reference)["sha256"]}]})
        outputs[stratum] = {**summary(rows), "reference": fingerprint(reference), "inputs": fingerprint(inputs),
                            "manifest": fingerprint(directory / "manifest.json")}
        for line, row in enumerate(rows, 1):
            origin = {**pins[str(paths["probes"])], "line": line} if stratum == "probes" else origins[row["id"]]
            identities.append(identity(row, stratum, origin))
    write_jsonl(output / "identities.jsonl", identities)
    write_jsonl(output / "parent-identities.jsonl", (identity(r, "v1-ancestry", old_origins[r["id"]]) for r in old))
    write_json(output / "receipt.json", {
        "schema_version": "evaluation/e3-freeze/0.1", "publication_status": args.publication_status,
        "candidate_not_release": args.publication_status == "candidate", **code_identity,
        "pins": list(pins.values()),
        "source_dataset_id": source["dataset_id"], "parent_dataset_id": parent["dataset_id"],
        "v1_shards": old_shards, "source_validation_shards": source_shards,
        "new_sources": sorted(allowed), "outputs": outputs,
        "identities": fingerprint(output / "identities.jsonl"),
        "parent_identities": fingerprint(output / "parent-identities.jsonl"),
        "policy": {
            "inherited": "ID plus identical full canonical row; all parent validation retained",
            "new": "No historical ID/group/order-free exact content; exact caller-supplied source allowlist",
            "content": "Exact state/question and sorted multiset of option texts; no whitespace/case normalization",
            "assembly_order": "Any row permutation allowed; full row by ID must match; output retains assembled order",
            "hashing": "SHA-256 of UTF-8 JSON, sorted keys, compact separators, ensure_ascii=False, allow_nan=False",
            "metric_basis": "Use label_basis, not kind; mixed aggregates are supplied-label agreement",
            "probes": "Existing validation rows copied unchanged, including presentation pairs; no re-reversal"},
        "caveats": ["Development evidence only: inherited validation and probes have been reused for tuning.",
                    "New authorship is not untouched final evidence; final data was not accessed.",
                    "Source allowlist is a caller attestation from released provenance (candidate provenance for candidate runs).",
                    "Source v2 train bytes not read or verified; cross-split/semantic exclusion remains Data-owned.",
                    "Provenance is pinned, not independently adjudicated; teacher revisions may be unavailable.",
                    "Groups/presentation variants are not independent samples. A successor release needs a new freeze."]})
    print(f"Frozen {len(assembled)} validation rows plus {len(probes)} existing probes ({args.publication_status}): {output}")


if __name__ == "__main__":
    main()
