#!/usr/bin/env python3
"""E4 Track B release boundary only; CPU bytes/metadata checks, never inference.

Run from the Evaluation worktree with PYTHONPATH=src. Adapted for Data013's
published captured-shard schema; runs only against the explicitly released hash.
Only boundary.json marks completion. Failed namespaces must not be reused.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

from jeff.evaluation import common
from jeff.evaluation.common import (BASES, KINDS, fingerprint, input_only,
    load_examples, nonempty, parse_json, records, validate_examples,
    validate_input, write_json, write_jsonl)

EXPECTED = {
    "lexicographic": ("rule-a", "g002"), "fifo": ("rule-a", "g003"),
    "discount": ("rule-a", "g005"), "rounding": ("rule-a", "g007"),
    "packs": ("rule-b", "g002"), "rates": ("rule-b", "g005"),
    "coordinates": ("rule-b", "g006"), "cooldown": ("rule-b", "g008"),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe(value):
    # Check both lexical and resolved paths, including symlink targets, before IO.
    path = Path(value).absolute()
    for candidate in (path, path.resolve()):
        require(not any(p.lower() == "final" or p.lower().startswith(
            ("final-", "final_", "final.")) for p in candidate.parts),
            f"Reserved final path refused: {candidate}")
    return path.resolve()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def keys(row):
    result = {}
    for mode in ("exact", "nfc_outerstrip"):
        norm = (lambda s: s) if mode == "exact" else (lambda s: unicodedata.normalize("NFC", s).strip())
        state, question = norm(row["state"]), norm(row["question"])
        texts = [norm(o["text"]) for o in row["options"]]
        # No case folding, punctuation removal, internal whitespace folding or NFKC.
        result[mode + ":ordered_input"] = digest([state, question, texts])
        result[mode + ":orderfree_decision"] = digest([state, question, sorted(texts)])
        result[mode + ":state"] = digest(state)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("release-dir", "expected-manifest-sha256", "publication-handoff", "output-dir"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    root = safe(os.environ.get("JEFF_ARTIFACTS_DIR", "/Users/destiner/Code/jeff/artifacts"))
    release, handoff, output = map(safe, (args.release_dir, args.publication_handoff, args.output_dir))
    require(output.parent == root / "evaluation" and not output.exists(), "Output must be a new direct Evaluation namespace")
    require(root / "data" in release.parents and not any(
        "pre-review" in p.lower() or "candidate" in p.lower() for p in release.parts),
        "Require Data's published directory, not a candidate")
    require(handoff.parent == root / "handoffs/data", "Require a public Data handoff")
    require(re.fullmatch(r"[0-9a-f]{64}", args.expected_manifest_sha256), "Expected manifest hash required")
    pins = {}

    def artifact(value):
        require(not Path(value).is_absolute(), "Artifact reference must be relative")
        path = safe(root / value)
        require(root in path.parents, "Artifact reference escapes root")
        return path

    def pin(value, expected=None):
        path = safe(value)
        item = fingerprint(path)
        require(expected is None or item["sha256"] == expected, f"Hash mismatch: {path}")
        require(pins.setdefault(str(path), item) == item, f"Input changed: {path}")
        return item

    def doc(value):
        path = safe(value)
        pin(path)
        return parse_json(path.read_text(encoding="utf-8"))

    def shards(path):
        obj = doc(path)
        require(obj.get("schema_version") == "0.1" and nonempty(obj.get("dataset_id")), "Invalid manifest")
        items = obj.get("shards")
        require(isinstance(items, list) and items, "Empty manifest")
        planned = []
        seen = set()
        # Validate every path and split before opening ANY shard, including train.
        for item in items:
            require(item.get("split") in ("train", "validation"), "Final/unknown manifest split refused")
            p = artifact(item["path"])
            require(p not in seen and type(item.get("rows")) is int and item["rows"] > 0, "Duplicate shard/count error")
            require(re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", "")), "Invalid shard hash")
            seen.add(p)
            planned.append((item, p))
        return obj, planned

    def read_rows(path, split):
        pin(path)
        if split == "validation":
            rows = load_examples(path)
        else:
            rows, ids = [], set()
            for line, row, error in records(path):
                require(error is None, f"Malformed historical train record {path}:{line}: {error}")
                choices = validate_input(row)
                require(row.get("split") == "train" and nonempty(row.get("group_id")) and nonempty(row.get("task_family")), "Invalid train identity")
                require(row["id"] not in ids and row.get("target_id") in choices, "Duplicate train ID/invalid target")
                prov = row.get("provenance", {})
                require(prov.get("kind") in KINDS and prov.get("label_basis") in BASES and nonempty(prov.get("source")), "Invalid train provenance")
                require(row["task_family"] != "passage_entailment", "Reserved family refused")
                if prov["kind"] == "teacher" or prov["label_basis"] == "teacher":
                    require(nonempty(prov.get("teacher_model")), "Missing train teacher alias")
                ids.add(row["id"])
                rows.append(row)
        require(all(r["split"] == split for r in rows), "Shard split mismatch")
        return rows

    manifest_path = safe(release / "manifest.json")
    pin(manifest_path, args.expected_manifest_sha256)
    pin(handoff)
    publication = handoff.read_text(encoding="utf-8")
    require(args.expected_manifest_sha256 in publication and
        (str(release) in publication or str(release.relative_to(root)) in publication) and
        re.search(r"publish|release", publication, re.I) and re.search(r"validation", publication, re.I),
        "Handoff must explicitly publish this validation release directory/hash")
    manifest, planned = shards(manifest_path)
    require(manifest["dataset_id"] == "data-d3-seen-rules-v1" and all(s["split"] == "validation" for s, _ in planned), "Not D3 validation-only release")
    provenance = doc(release / "provenance.json")
    freeze = doc(release / "freeze.json")
    sidecar = doc(release / "case-metadata.json")
    require(all(d.get("dataset_id") == manifest["dataset_id"] for d in (provenance, freeze, sidecar)), "Dataset metadata identity mismatch")
    pin(manifest_path, freeze["manifest_sha256"])
    pin(release / "case-metadata.json", freeze["case_metadata_sha256"])
    for name, sha in freeze["files_sha256"].items():
        pin(safe(release / name), sha)
    for name, sha in freeze["helper_source_sha256"].items():
        pin(safe(root.parent / ".worktrees/data/src/jeff/data" / name), sha)
    for name, sha in freeze["evidence_sha256"].items():
        pin(safe(name), sha)
    require(freeze.get("predictions_requested_by_data") is False and freeze.get("permanently_training_excluded") is True,
        "Release must be frozen before Data prediction requests and permanently excluded")
    require(provenance.get("permanently_training_excluded") is True and provenance.get("derivatives_never_train") is True and
        provenance.get("stratum") == "seen_mechanism_new_policy", "Missing usage boundary")
    # Plan location is explicit if published, otherwise the Data-owned preauthoring config.
    plan_path = artifact(provenance["plan"]) if "plan" in provenance else safe(root.parent / ".worktrees/data/configs/data/d3-seen-rules-v1.json")
    pin(plan_path, provenance["plan_sha256"])
    plan = doc(plan_path)
    plan_mechanisms = {m["id"]: m for m in plan["mechanisms"]}
    require(set(plan_mechanisms) == set(EXPECTED), "Unexpected preauthoring mechanism plan")
    require(freeze["plan_sha256"] == provenance["plan_sha256"], "Freeze/plan disagreement")
    visited = set()

    def listed_hashes(value, base):
        """Pin listed artifact byte hashes, recursively; never import producer code."""
        if isinstance(value, list):
            for item in value:
                listed_hashes(item, base)
        elif isinstance(value, dict):
            for field, child in value.items():
                if isinstance(child, dict) and (field == "sha256" or field.endswith("_sha256")):
                    for name, sha in child.items():
                        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
                            continue
                        p = safe(name) if Path(name).is_absolute() else (artifact(name) if name.startswith(("data/", "evaluation/", "model/")) else safe(base / name))
                        pin(p, sha)
                        # Index entries bind archived bytes. Historical metadata may
                        # describe a mutable config's old hash; do not reinterpret it
                        # as a demand that today's source workspace still has old bytes.
                elif field == "sha256" and isinstance(child, str) and "path" in value:
                    pin(safe(value["path"]) if Path(value["path"]).is_absolute() else artifact(value["path"]), child)
                elif field.endswith("_sha256") and isinstance(child, str) and isinstance(value.get(field[:-7]), str):
                    name = value[field[:-7]]
                    p = safe(name) if Path(name).is_absolute() else (artifact(name) if name.startswith(("data/", "evaluation/", "model/")) else safe(base / name))
                    pin(p, child)
                else:
                    listed_hashes(child, base)
    listed_hashes(provenance, release)
    # Published review/exclusion/validation receipts are pinned, not rerun.
    for name in ("validation.json", "exclusion.json"):
        doc(release / name)
    review_path = safe(provenance["review_report"]["path"])
    pin(review_path, provenance["review_report"]["sha256"])
    require(freeze["evidence_sha256"].get(str(review_path)) == provenance["review_report"]["sha256"], "Review not bound by publisher freeze")
    review = doc(review_path)
    require(review.get("verdict") == "pass" and review.get("must_fix_count") == 0, "Missing passing published review")
    for name, sha in review["input_hashes_before"].items():
        pin(safe(release.parent / name), sha)
    reviewed_manifest, reviewed_shards = shards(release.parent / "pre-review-r3/manifest.json")
    require([(s["sha256"], s["rows"], s["split"]) for s, _ in reviewed_shards] ==
        [(s["sha256"], s["rows"], s["split"]) for s, _ in planned], "Released snapshots differ from reviewed r3 shards")
    validation = doc(release / "validation.json")
    require(validation.get("valid") is True and validation.get("errors") == [] and validation.get("rows") == 96 and
        validation.get("publication_manifest_sha256") == args.expected_manifest_sha256, "Published validation identity mismatch")
    pin(release / "validation-input.json", validation["manifest_sha256"])
    training_path = artifact(provenance["training_manifest"])
    train_hash = provenance["training_manifest_sha256"]
    pin(training_path, train_hash)
    training_manifest, training_shards = shards(training_path)
    require(training_manifest["dataset_id"] == "data-pilot-v2", "Wrong training dataset")
    readiness = doc(root / "evaluation/e4-d3-readiness-v1/mechanism-mapping.json")
    for item in readiness["pins"]:
        pin(item["path"], item["sha256"])
    for model in ("minilm", "msmarco"):
        base = root / "model/m4-v2-20261111-01" / model
        pin(base / "dataset-manifest.json", train_hash)
        run = doc(base / "run.json")
        require(run["status"] == "completed" and safe(run["config"]["dataset_manifest"]) == training_path,
            "M4 run training manifest path mismatch")
        require(run["dataset"]["manifest_sha256"] == train_hash, "M4 run training manifest hash mismatch")
    rows = []
    for shard, path in planned:
        pin(path, shard["sha256"])
        batch = read_rows(path, "validation")
        require(len(batch) == shard["rows"], "D3 shard count mismatch")
        rows.extend(batch)
    validate_examples(rows)
    require(len(rows) == 96 and all(r["task_family"] == "rule_application" for r in rows), "Expected 96 rule rows")
    metadata = sidecar["cases"]
    require(isinstance(metadata, list) and len(metadata) == 96, "Incomplete case sidecar")
    by_id = {c["id"]: c for c in metadata}
    require(len(by_id) == 96 and set(by_id) == {r["id"] for r in rows}, "Duplicate/missing/extra case metadata")
    group_cases, mechanism_groups, units = defaultdict(list), defaultdict(set), []
    train_cache, exposure_units = {}, {}
    train_index = {str(p): s for s, p in training_shards}
    for row in rows:
        c, prov = by_id[row["id"]], row["provenance"]
        group, mechanism = row["group_id"], c["mechanism_id"]
        require(mechanism in EXPECTED and c["group_id"] == c["policy_instance_id"] == group == prov.get("policy_instance_id") and
            prov.get("mechanism_id") == mechanism and prov.get("usage") == "validation_only_never_train", "Case/provenance/policy mismatch")
        require(c.get("split") == "validation" and c.get("stratum") == "seen_mechanism_new_policy" and
            c.get("intentional_mechanism_overlap") is True and c.get("permanently_training_excluded") is True and
            c["label_basis"] == prov["label_basis"], "Sidecar usage/label mismatch")
        require(group.startswith("data:d3-seen-rules-v1:") and nonempty(c.get("policy_domain")) and nonempty(c.get("teacher_alias")), "Missing new policy/label identity")
        policy_plan = plan_mechanisms[mechanism]
        require(c["policy_domain"] in policy_plan["policy_domains"] and c["mechanism_name"] == policy_plan["name"], "Case not in preauthoring policy/mechanism plan")
        require(c["id"].startswith(group + ":") and group == f"data:d3-seen-rules-v1:{mechanism}:p{policy_plan['policy_domains'].index(c['policy_domain']) + 1:02d}", "Policy domain/group assignment mismatch")
        exposure = c["training_exposure"]
        producer, suffix = EXPECTED[mechanism]
        oldgroup = f"data:pilot-v2:{producer}:{suffix}"
        oldpath = artifact(exposure["shard"])
        require(exposure["dataset_id"] == "data-pilot-v2" and exposure["manifest_sha256"] == train_hash and
            exposure["group_id"] == oldgroup and oldpath == artifact(f"data/data-pilot-v2/{producer}/train.jsonl"), "Wrong mechanism exposure mapping")
        pin(artifact(exposure["assignment_path"]), exposure["assignment_sha256"])
        shard = train_index.get(str(oldpath), {})
        require(shard.get("split") == "train" and shard.get("sha256") == exposure["shard_sha256"], "Exposure is not exact released TRAIN shard")
        if mechanism not in exposure_units:
            pin(oldpath, shard["sha256"])
            if oldpath not in train_cache:
                train_cache[oldpath] = read_rows(oldpath, "train")
                require(len(train_cache[oldpath]) == shard["rows"], "Training exposure count mismatch")
            assigned = doc(oldpath.parent / "group_assignments.json")["groups"][oldgroup]
            train_metadata = doc(oldpath.parent / "metadata.json")
            require(assigned["split"] == "train" and assigned["mechanism"] == policy_plan["name"] and
                policy_plan["training_group_id"] == oldgroup and artifact(policy_plan["training_shard"]) == oldpath,
                "Mechanism name/plan/TRAIN assignment mismatch")
            pin(oldpath.parent / "group_assignments.json", exposure["assignment_sha256"])
            matching = [r for r in train_cache[oldpath] if r["group_id"] == oldgroup]
            require(matching and all(r["task_family"] == "rule_application" for r in matching), "Absent/wrong-family training group")
            exposure_units[mechanism] = {**exposure, "resolved_mechanism_name": assigned["mechanism"],
                "train_group_rows": len(matching), "sidecar_mechanism_name": c["mechanism_name"]}
        require(exposure == {k: exposure_units[mechanism][k] for k in exposure}, "Inconsistent mechanism exposure")
        group_cases[group].append(row["id"])
        mechanism_groups[mechanism].add(group)
        units.append({"case_id": row["id"], "policy_instance_id": group, "group_id": group,
            "mechanism_id": mechanism, "task_family": row["task_family"], "split": "validation",
            "label_basis": prov["label_basis"], "provenance_kind": prov["kind"],
            "teacher_alias": c["teacher_alias"], "row_teacher_model": prov.get("teacher_model"), "teacher_revision": "unknown",
            "training_exposure": exposure, "input_sha256": digest(input_only(row)), "row_sha256": digest(row)})
    require(len(group_cases) == 48 and all(len(ids) == 2 for ids in group_cases.values()) and
        len(mechanism_groups) == 8 and all(len(gs) == 6 for gs in mechanism_groups.values()), "Policy/mechanism denominator mismatch")
    require(all(len({by_id[i]["mechanism_id"] for i in ids}) == 1 for ids in group_cases.values()), "Policy crosses mechanisms")
    computed_counts = {"decisions": 96, "source_policy_groups": 48, "mechanisms": 8,
        "decisions_per_mechanism": dict(Counter(c["mechanism_id"] for c in metadata)),
        "policy_groups_per_mechanism": {m: len(g) for m, g in mechanism_groups.items()}}
    require(sidecar["counts"] == provenance["counts"] == computed_counts, "Declared counts mismatch")
    # Independent exclusion, including superseded corpora. Do not glob data trees.
    corpus_plans = []
    for name in ("data/data-pilot-v2/manifest.json", "data/data-pilot-v2/pre-review-r2/manifest.json",
                 "data/data-pilot-v1/manifest.json", "data/data-tiny-v1/manifest.json"):
        _, source_shards = shards(artifact(name))
        corpus_plans.extend((name, s, p) for s, p in source_shards)
    for name, count in (("evaluation/probes-v1/manifest.json", 24),
                        ("evaluation/pilot-order-v1/manifest.json", 120)):
        _, probe_shards = shards(artifact(name))
        require(all(s["split"] == "validation" for s, _ in probe_shards) and sum(s["rows"] for s, _ in probe_shards) == count, "Probe manifest count/split mismatch")
        corpus_plans.extend((name, s, p) for s, p in probe_shards)
    name = "data/data-pilot-v1/sentiment/validation.jsonl"
    corpus_plans.append((name, {"split": "validation", "rows": 20}, artifact(name)))
    ids, groups = {r["id"] for r in rows}, set(group_cases)
    d3keys = defaultdict(set)
    for row in rows:
        for kind, key in keys(row).items():
            if "state" not in kind:
                require(key not in d3keys[kind], "Duplicate D3 decision content")
            d3keys[kind].add(key)
    corpora = []
    prior_policy_ids = set()
    for origin, shard, path in corpus_plans:
        pin(path, shard.get("sha256"))
        history = read_rows(path, shard["split"])
        require(len(history) == shard["rows"], "Historical count mismatch")
        hits = Counter({"id": 0, "group": 0, **{k: 0 for k in d3keys}})
        for old in history:
            prior_policy_ids.add(old["group_id"])
            if nonempty(old["provenance"].get("policy_instance_id")):
                prior_policy_ids.add(old["provenance"]["policy_instance_id"])
            hits["id"] += old["id"] in ids
            hits["group"] += old["group_id"] in groups
            for kind, key in keys(old).items():
                hits[kind] += key in d3keys[kind]
        require(not any(hits.values()), f"Historical copied-case/identity conflict: {origin}")
        corpora.append({"origin": origin, **pin(path), "rows": len(history), "split": shard["split"],
            "groups": len({r["group_id"] for r in history}), "hits": dict(hits), "errors": 0})
    require(not groups.intersection(prior_policy_ids), "Reused historical policy identity")
    # Catch mutation of any pinned byte before creating any prediction input.
    for item in list(pins.values()):
        pin(item["path"], item["sha256"])
    output.mkdir(parents=True, exist_ok=False)
    env = {**os.environ, "JEFF_ARTIFACTS_DIR": str(root)}
    subprocess.run([sys.executable, "-m", "jeff.evaluation.assemble", "--manifest", str(manifest_path),
        "--dataset-id", "evaluation-e4-d3-seen-rules-v1", "--output-dir", str(output / "reference")], check=True, env=env)
    reference = output / "reference/validation.jsonl"
    require(load_examples(reference) == rows, "Assembler changed reference")
    subprocess.run([sys.executable, "-m", "jeff.evaluation.prepare", "--examples", str(reference),
        "--output", str(output / "inputs.jsonl"), "--receipt", str(output / "prepare-receipt.json")], check=True, env=env)
    write_json(output / "units.json", {"cases": units,
        "policies": [{"policy_instance_id": g, "case_ids": cases, "mechanism_id": by_id[cases[0]]["mechanism_id"]} for g, cases in sorted(group_cases.items())],
        "mechanisms": exposure_units})
    for item in list(pins.values()):
        pin(item["path"], item["sha256"])
    # Last write: owner must require this receipt before requesting predictions.
    write_json(output / "boundary.json", {
        "schema_version": "evaluation/e4-d3-boundary/0.1", "status": "released_boundary_complete",
        "completed_at": datetime.now(timezone.utc).isoformat(), "code": fingerprint(safe(__file__)),
        "common_code": fingerprint(safe(common.__file__)),
        "pipeline_code": [fingerprint(safe(Path(common.__file__).parent / n)) for n in ("assemble.py", "prepare.py")],
        "publication_handoff": pin(handoff), "release_manifest": pin(manifest_path),
        "pins": sorted(pins.values(), key=lambda p: p["path"]),
        "reference": fingerprint(reference), "inputs": fingerprint(output / "inputs.jsonl"),
        "units": fingerprint(output / "units.json"), "counts": computed_counts,
        "coverage": {"reference_rows": 96, "mapped_cases": 96, "unmapped_cases": 0, "errors": 0},
        "exclusion": {"corpora": corpora, "hits": 0, "errors": 0, "semantic_clearance": False,
            "normalization": "exact and NFC+outerstrip; case/sign/bracket/math punctuation preserved"},
        "label_provenance": {"basis_counts": dict(Counter(r["provenance"]["label_basis"] for r in rows)),
            "kind_counts": dict(Counter(r["provenance"]["kind"] for r in rows)),
            "teacher_aliases": sorted({c["teacher_alias"] for c in metadata}), "immutable_teacher_revision": "unknown"},
        "limitations": ["Intentionally seen mechanisms, new declared policy/source units; not mechanism-disjoint or iid.",
            "Byte/identity/content-key exclusions do not establish semantic novelty or correctness.",
            "Published rule/rendered-text verification evidence is pinned, not independently executed or semantically cleared.",
            "Two cases per policy are not option reversal pairs; no E3 ancestry is asserted.",
            "No predictions, scoring, final evaluation, or promotion performed."],
        "data_limitations": provenance.get("limitations", []), "additional_spend_gbp": 0,
        "pending_spend_gbp": 0, "inference_requested": False})
    print(output / "boundary.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        failure = Path(__file__).parent / ("failure-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + ".json")
        write_json(failure, {"status": "failed", "error_type": type(exc).__name__, "error": str(exc), "argv": sys.argv, "code": fingerprint(safe(__file__))})
        raise
