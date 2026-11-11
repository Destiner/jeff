"""Independent manifest validation with a preflight boundary around final data."""

import hashlib
import json
import os
from collections import Counter
from pathlib import Path


FAMILIES = {"intent", "sentiment", "rule_application"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Nonfinite JSON constant: {value}")


def strict_json(data):
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant)


def nonempty(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")


def reject_final(path):
    parts = [part.lower() for part in Path(path).parts]
    if any(a == "evaluation" and b == "final" for a, b in zip(parts, parts[1:])):
        raise ValueError(f"Protected final-evaluation path: {path}")


def safe_path(path, root=None, protected=None):
    path = Path(path).expanduser()
    reject_final(path.absolute())
    resolved = path.resolve(strict=True)
    reject_final(resolved)
    if protected is not None and resolved.is_relative_to(protected):
        raise ValueError(f"Resolved path is inside protected final evaluation: {path}")
    if root is not None and not resolved.is_relative_to(root):
        raise ValueError(f"Path escapes JEFF_ARTIFACTS_DIR: {path}")
    if not resolved.is_file():
        raise ValueError(f"Not a regular file: {path}")
    return resolved


def validate_labeled(row, split, validate_decision):
    if not isinstance(row, dict) or row.get("schema_version") != "0.1":
        raise ValueError("Every row must be a schema_version 0.1 object")
    validate_decision(row)
    # Enforce the contract independently of the inference validator's return value.
    nonempty(row.get("id"), "id")
    if not isinstance(row.get("state"), str):
        raise ValueError("state must be text")
    nonempty(row.get("question"), "question")
    options = row.get("options")
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError("options must contain at least two choices")
    option_ids = set()
    for option in options:
        if not isinstance(option, dict):
            raise ValueError("Each option must be an object")
        nonempty(option.get("id"), "option.id")
        nonempty(option.get("text"), "option.text")
        if option["id"] in option_ids:
            raise ValueError("Duplicate option id")
        option_ids.add(option["id"])
    nonempty(row.get("target_id"), "target_id")
    if row["target_id"] not in option_ids:
        raise ValueError("target_id is not a supplied option")
    if row.get("split") != split:
        raise ValueError("Row split does not match its shard")
    nonempty(row.get("group_id"), "group_id")
    nonempty(row.get("task_family"), "task_family")
    if row["task_family"] not in FAMILIES:
        raise ValueError("task_family is outside the current training reservation")
    provenance = row.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("provenance must be an object")
    if provenance.get("kind") not in {"teacher", "public_dataset", "programmatic", "human"}:
        raise ValueError("Invalid provenance.kind")
    if provenance.get("label_basis") not in {"teacher", "source_label", "rule_verified", "human_verified"}:
        raise ValueError("Invalid provenance.label_basis")
    nonempty(provenance.get("source"), "provenance.source")
    if provenance["kind"] == "teacher" or provenance["label_basis"] == "teacher":
        nonempty(provenance.get("teacher_model"), "provenance.teacher_model (use unknown if unknown)")


def load_dataset(manifest_path, validate_decision):
    artifact_env = os.environ.get("JEFF_ARTIFACTS_DIR")
    if not artifact_env:
        raise ValueError("JEFF_ARTIFACTS_DIR is required")
    reject_final(Path(artifact_env).expanduser().absolute())
    root = Path(artifact_env).expanduser().resolve(strict=True)
    reject_final(root)
    if not root.is_dir():
        raise ValueError("JEFF_ARTIFACTS_DIR must be a directory")
    protected = (root / "evaluation" / "final").resolve()
    manifest_path = safe_path(manifest_path, protected=protected)
    manifest_bytes = manifest_path.read_bytes()
    manifest = strict_json(manifest_bytes)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "0.1":
        raise ValueError("Manifest must be a schema_version 0.1 object")
    nonempty(manifest.get("dataset_id"), "dataset_id")
    shards = manifest.get("shards")
    if not isinstance(shards, list):
        raise ValueError("Manifest shards must be a list")
    # Preflight the ENTIRE manifest before opening even the first shard.
    for shard in shards:
        if not isinstance(shard, dict) or shard.get("split") not in {"train", "validation"}:
            raise ValueError("Training manifest may contain only train/validation shards; final is forbidden")
    planned = []
    seen_paths = set()
    for shard in shards:
        nonempty(shard.get("path"), "shard.path")
        relative = Path(shard["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Shard paths must be artifact-relative without traversal")
        path = safe_path(root / relative, root, protected)
        if path in seen_paths:
            raise ValueError("Duplicate resolved shard path")
        seen_paths.add(path)
        digest = shard.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
            raise ValueError("Shard sha256 must be 64 hexadecimal characters")
        if type(shard.get("rows")) is not int or shard["rows"] < 0:
            raise ValueError("Shard rows must be a nonnegative integer")
        planned.append((shard, path))
    rows = {"train": [], "validation": []}
    ids, groups, contents = set(), {}, {}
    duplicate_content = []
    verified_shards = []
    for shard, path in planned:
        # Resolve again in case a producer changed a symlink after preflight.
        if safe_path(root / shard["path"], root, protected) != path:
            raise ValueError("Shard path changed after preflight")
        data = path.read_bytes()
        actual_hash = sha256(data)
        if actual_hash != shard["sha256"].lower():
            raise ValueError(f"SHA256 mismatch: {shard['path']}")
        shard_rows = []
        for line_number, line in enumerate(data.decode("utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = strict_json(line)
                validate_labeled(row, shard["split"], validate_decision)
                if row["id"] in ids:
                    raise ValueError("Duplicate example id")
                ids.add(row["id"])
                previous_split = groups.setdefault(row["group_id"], row["split"])
                if previous_split != row["split"]:
                    raise ValueError("Group leakage between train and validation")
                content = json.dumps([row["state"], row["question"], sorted(o["text"] for o in row["options"])], ensure_ascii=False)
                signature = sha256(content.encode("utf-8"))
                if signature in contents:
                    duplicate_content.append({"id": row["id"], "matches_id": contents[signature]})
                else:
                    contents[signature] = row["id"]
                shard_rows.append(row)
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"{shard['path']}:{line_number}: {exc}") from exc
        if len(shard_rows) != shard["rows"]:
            raise ValueError(f"Row-count mismatch: {shard['path']}")
        rows[shard["split"]].extend(shard_rows)
        verified_shards.append({**shard, "resolved_path": str(path), "sha256": actual_hash})
    if not rows["train"]:
        raise ValueError("At least one training row is required")
    identity = {
        "schema_version": "0.1", "dataset_id": manifest["dataset_id"],
        "manifest_path": str(manifest_path), "manifest_sha256": sha256(manifest_bytes),
        "artifact_root": str(root), "shards": verified_shards,
        "counts": {split: len(items) for split, items in rows.items()},
        "families": {split: dict(Counter(r["task_family"] for r in items)) for split, items in rows.items()},
        "label_basis": {split: dict(Counter(r["provenance"]["label_basis"] for r in items)) for split, items in rows.items()},
        "likely_content_duplicates": duplicate_content,
    }
    return rows, identity, manifest_bytes
