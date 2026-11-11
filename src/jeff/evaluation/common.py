"""Strict contract readers and immutable artifact writers."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

INPUT_FIELDS = ("schema_version", "id", "state", "question", "options")
BASES = {"teacher", "source_label", "rule_verified", "human_verified"}
KINDS = {"teacher", "public_dataset", "programmatic", "human"}


class ReferenceError(ValueError):
    def __init__(self, failures):
        super().__init__("Invalid reference examples; no metrics computed")
        self.failures = failures


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"nonfinite JSON constant: {value}")


def parse_json(text):
    return json.loads(text, object_pairs_hook=_unique_object, parse_constant=_reject_constant)


def records(path):
    with Path(path).open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            try:
                row = parse_json(line)
                if not isinstance(row, dict):
                    raise ValueError("record must be an object")
                yield line_number, row, None
            except ValueError as exc:
                yield line_number, None, str(exc)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_input(row):
    if row.get("schema_version") != "0.1":
        raise ValueError("schema_version must be '0.1'")
    if not nonempty(row.get("id")) or not nonempty(row.get("question")):
        raise ValueError("id and question must be nonempty strings")
    if not isinstance(row.get("state"), str):
        raise ValueError("state must be a string")
    options = row.get("options")
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError("options must contain at least two choices")
    seen = set()
    for option in options:
        if not isinstance(option, dict) or not nonempty(option.get("id")) or not nonempty(option.get("text")):
            raise ValueError("each option needs nonempty id and text")
        if option["id"] in seen:
            raise ValueError("duplicate option id")
        seen.add(option["id"])
    return seen


def load_examples(path):
    return validate_records(records(path))


def validate_examples(rows):
    return validate_records((line, row, None) for line, row in enumerate(rows, 1))


def validate_records(source):
    rows, failures, ids, group_splits, splits = [], [], set(), {}, set()
    for line, row, error in source:
        if error:
            failures.append({"line": line, "reason": error})
            continue
        try:
            options = validate_input(row)
            if row["id"] in ids:
                raise ValueError("duplicate reference id")
            ids.add(row["id"])
            if not nonempty(row.get("target_id")) or row["target_id"] not in options:
                raise ValueError("target_id must name one supplied option")
            if not nonempty(row.get("group_id")) or not nonempty(row.get("task_family")):
                raise ValueError("group_id and task_family must be nonempty strings")
            if row.get("split") not in ("validation", "final"):
                raise ValueError("evaluation accepts validation or final, never train")
            splits.add(row["split"])
            prior = group_splits.setdefault(row["group_id"], row["split"])
            if prior != row["split"]:
                raise ValueError("cross-split group overlap")
            provenance = row.get("provenance")
            if not isinstance(provenance, dict):
                raise ValueError("provenance must be an object")
            if provenance.get("kind") not in KINDS or provenance.get("label_basis") not in BASES:
                raise ValueError("unknown provenance kind or label_basis")
            if not nonempty(provenance.get("source")):
                raise ValueError("provenance source required")
            if (provenance["kind"] == "teacher" or provenance["label_basis"] == "teacher") and not nonempty(provenance.get("teacher_model")):
                raise ValueError("teacher_model required; use 'unknown' if unavailable")
            if row["task_family"] == "passage_entailment" and row["split"] != "final":
                raise ValueError("passage_entailment is reserved for final evaluation")
            rows.append(row)
        except (ValueError, TypeError) as exc:
            failures.append({"line": line, "id": row.get("id"), "reason": str(exc)})
    if len(splits) > 1:
        failures.append({"reason": "do not mix validation and final examples"})
    if failures:
        raise ReferenceError(failures)
    return rows


def fingerprint(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return {"path": str(Path(path).resolve()), "sha256": digest.hexdigest()}


def guard_final(examples, output, allow_final=False):
    if not any(row["split"] == "final" for row in examples):
        return
    if not allow_final:
        raise ValueError("Final data is sealed: explicit --allow-final after checkpoint freeze required")
    root = Path(os.environ.get("JEFF_ARTIFACTS_DIR", "/Users/destiner/Code/jeff/artifacts")).resolve()
    final_root = root / "evaluation" / "final"
    if final_root not in Path(output).resolve().parents:
        raise ValueError("Final outputs must stay inside JEFF_ARTIFACTS_DIR/evaluation/final/")


def write_json(path, payload):
    content = json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as target:
        target.write(content)


def write_jsonl(path, rows):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8") as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")


def input_only(row):
    return {**{key: row[key] for key in INPUT_FIELDS if key != "options"},
            "options": [{"id": option["id"], "text": option["text"]} for option in row["options"]]}
