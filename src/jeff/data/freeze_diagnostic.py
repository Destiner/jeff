"""Freeze a validation-only new-policy diagnostic with explicit training exposure."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import tempfile

from .assemble import producer_accounting, write_new
from .audit import content_key, load_manifest
from .validate import canonical_text, load_json, normalized, shard_path, validate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest-copy", type=Path)
    parser.add_argument("--review-report", type=Path)
    parser.add_argument("--review-manifest", type=Path)
    parser.add_argument("--evidence", type=Path, action="append", default=[])
    args = parser.parse_args()
    if bool(args.review_report) != bool(args.review_manifest):
        parser.error("supply both --review-report and --review-manifest")
    root = args.artifacts_dir.resolve()
    final_output = shard_path(root, str(args.output_dir.resolve().relative_to(root)))
    if final_output.exists():
        raise ValueError("publication directory must not exist")
    if args.manifest_copy and (args.manifest_copy.exists() or args.manifest_copy.with_name(args.manifest_copy.stem + ".provenance.json").exists()):
        raise ValueError("manifest mirror must be new")
    config = load_json(args.config.read_text())
    if config.get("authoring_plan"):
        original_plan = shard_path(root, config["authoring_plan"])
        if digest(original_plan) != config["authoring_plan_sha256"]:
            raise ValueError("frozen authoring plan changed")
        if any(config.get(key) != value for key, value in load_json(original_plan.read_text()).items()):
            raise ValueError("publication changed a preauthoring allocation or constraint")
    if config["split"] != "validation" or config["permanently_training_excluded"] is not True:
        raise ValueError("diagnostic plan must permanently exclude training")
    source_root = shard_path(root, config["artifact_prefix"])
    training_path = shard_path(root, config["training_manifest"])
    if digest(training_path) != config["training_manifest_sha256"]:
        raise ValueError("training exposure manifest changed")
    training, historical, train_assignments, history_hashes = load_manifest(training_path, root)
    historical_manifests = {config["training_manifest"]: digest(training_path)}
    for relative in config["historical_manifests"]:
        history_path = shard_path(root, relative)
        _, part, _, hashes = load_manifest(history_path, root)
        historical.extend(part)
        history_hashes.update(hashes)
        historical_manifests[relative] = digest(history_path)
    by_id = {}
    for row in historical:
        if row["id"] in by_id and by_id[row["id"]] != row:
            raise ValueError("conflicting historical example identity")
        by_id[row["id"]] = row
    historical = list(by_id.values())
    historical_ids = {row["id"] for row in historical}
    historical_groups = {row["group_id"] for row in historical}
    historical_content = {content_key(row): row["id"] for row in historical}
    historical_states = {canonical_text(row["state"]): row["id"] for row in historical}
    training_shards = {shard["path"]: shard for shard in training["shards"] if shard["split"] == "train"}
    plans, mechanisms = {}, {}
    for mechanism in config["mechanisms"]:
        key = mechanism["id"]
        if key in mechanisms:
            raise ValueError("duplicate mechanism identity")
        mechanisms[key] = mechanism
        training_group = mechanism["training_group_id"]
        if train_assignments[training_group]["mechanism"] != mechanism["name"]:
            raise ValueError("named mechanism disagrees with training assignment")
        if mechanism["training_shard"] not in training_shards:
            raise ValueError("mechanism exposure is not a training shard")
        exposure_path = shard_path(root, mechanism["training_shard"])
        exposure_payload = exposure_path.read_bytes()
        if hashlib.sha256(exposure_payload).hexdigest() != training_shards[mechanism["training_shard"]]["sha256"]:
            raise ValueError("claimed exposure shard changed")
        exposed = [load_json(line) for line in exposure_payload.decode().splitlines()]
        exposed = [row for row in exposed if row["group_id"] == training_group]
        if not exposed or any(row["split"] != "train" or row["task_family"] != "rule_application" for row in exposed):
            raise ValueError("mechanism lacks verified training exposure")
        if len(mechanism["policy_domains"]) != config["policies_per_mechanism"]:
            raise ValueError("policy-domain plan mismatch")
        for number, domain in enumerate(mechanism["policy_domains"], 1):
            group = config["group_namespace"] + key + f":p{number:02d}"
            if group in historical_groups:
                raise ValueError("diagnostic reuses an old source group")
            plans[group] = {"mechanism": mechanism, "policy_domain": domain}

    manifest = {"schema_version": "0.1", "dataset_id": config["dataset_id"], "shards": []}
    final_output.parent.mkdir(parents=True, exist_ok=True)
    args.output_dir = Path(tempfile.mkdtemp(prefix=final_output.name + ".pending-", dir=final_output.parent))
    sources, rows, metadata_rows = [], [], []
    actual_cost = pending_cost = 0
    for producer in sorted({m["producer"] for m in mechanisms.values()}):
        published_producer = config.get("published_producers", {}).get(producer, producer)
        folder = shard_path(root, str(source_root.relative_to(root) / published_producer))
        path = shard_path(root, str(folder.relative_to(root) / "validation.jsonl"))
        metadata_path = shard_path(root, str(folder.relative_to(root) / "metadata.json"))
        metadata = load_json(metadata_path.read_text())
        alias, (actual, pending) = producer_accounting(metadata)
        actual_cost += actual
        pending_cost += pending
        payload = path.read_bytes()
        payload_sha = hashlib.sha256(payload).hexdigest()
        part = [load_json(line) for line in payload.decode().splitlines()]
        snapshot = args.output_dir / "shards" / (producer + ".jsonl")
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        with snapshot.open("xb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        allocation_path = shard_path(root, str(folder.relative_to(root) / "group_assignments.json"))
        allocation = load_json(allocation_path.read_text())["groups"]
        for row in part:
            plan = plans[row["group_id"]]
            mechanism = plan["mechanism"]
            provenance = row["provenance"]
            if mechanism["producer"] != producer or row["split"] != "validation" or row["task_family"] != "rule_application":
                raise ValueError("producer/split/family does not match plan")
            if provenance["mechanism_id"] != mechanism["id"] or provenance["policy_instance_id"] != row["group_id"]:
                raise ValueError("case-to-policy-to-mechanism mismatch")
            if provenance["usage"] != "validation_only_never_train" or provenance["label_basis"] != "rule_verified":
                raise ValueError("missing verification or permanent training exclusion")
            expected_allocation = {"split": "validation", "mechanism_id": mechanism["id"],
                                   "policy_instance_id": row["group_id"], "policy_domain": plan["policy_domain"],
                                   "training_group_id": mechanism["training_group_id"]}
            if any(allocation[row["group_id"]].get(key) != value for key, value in expected_allocation.items()):
                raise ValueError("frozen source allocation mismatch")
            allowed_ids = {row["group_id"] + f":c{i:02d}" for i in range(1, config["cases_per_policy"] + 1)}
            if row["id"] not in allowed_ids:
                raise ValueError("case ID does not follow the preassigned policy plan")
            if row["id"] in historical_ids or content_key(row) in historical_content or canonical_text(row["state"]) in historical_states:
                raise ValueError("diagnostic duplicates historical ID/input/state: " + row["id"])
            metadata_rows.append({"id": row["id"], "group_id": row["group_id"],
                "policy_instance_id": provenance["policy_instance_id"], "policy_domain": plan["policy_domain"],
                "mechanism_id": mechanism["id"], "mechanism_name": mechanism["name"],
                "stratum": config["stratum"], "split": "validation", "label_basis": provenance["label_basis"],
                "teacher_alias": alias, "intentional_mechanism_overlap": True, "permanently_training_excluded": True,
                "training_exposure": {"dataset_id": training["dataset_id"], "manifest_sha256": digest(training_path),
                    "group_id": mechanism["training_group_id"], "shard": mechanism["training_shard"],
                    "shard_sha256": training_shards[mechanism["training_shard"]]["sha256"],
                    "assignment_path": str(Path(mechanism["training_shard"]).parent / "group_assignments.json"),
                    "assignment_sha256": digest(shard_path(root, str(Path(mechanism["training_shard"]).parent / "group_assignments.json")))}})
        manifest["shards"].append({"path": str((final_output / "shards" / snapshot.name).relative_to(root)),
                                   "split": "validation", "sha256": payload_sha, "rows": len(part)})
        source_hashes = {}
        for source in sorted(folder.iterdir()):
            if source.is_file() and source.suffix in {".json", ".jsonl", ".py", ".md"}:
                safe = shard_path(root, str(source.relative_to(root)))
                source_hashes[str(source.relative_to(root))] = digest(safe)
        if source_hashes[str(path.relative_to(root))] != payload_sha:
            raise ValueError("producer changed during capture")
        sources.append({"producer": producer, "metadata": str(metadata_path.relative_to(root)), "teacher_alias": alias, "sha256": source_hashes})
        rows.extend(part)
    group_counts = Counter(row["group_id"] for row in rows)
    if len(rows) != config["expected_decisions"] or set(group_counts) != set(plans) or any(n != config["cases_per_policy"] for n in group_counts.values()):
        raise ValueError("decision/policy count mismatch")
    if len(plans) != config["expected_policy_groups"]:
        raise ValueError("policy-group total mismatch")
    if actual_cost != config["additional_spend_gbp"] or pending_cost != config["pending_spend_gbp"]:
        raise ValueError("unaccounted producer cost")

    if args.review_manifest:
        reviewed = load_json(args.review_manifest.read_text())
        bindings = lambda value: sorted((s["split"], s["sha256"], s["rows"]) for s in value["shards"])
        if reviewed["dataset_id"] != manifest["dataset_id"] or bindings(reviewed) != bindings(manifest):
            raise ValueError("published bytes differ from the reviewed candidate")
    output_manifest = args.output_dir / "manifest.json"
    write_new(output_manifest, manifest)
    staging_manifest = {**manifest, "shards": [dict(s, path=str((args.output_dir / "shards" / Path(s["path"]).name).relative_to(root))) for s in manifest["shards"]]}
    validation_input = args.output_dir / "validation-input.json"
    write_new(validation_input, staging_manifest)
    structural = validate(validation_input, root)
    structural["publication_manifest_sha256"] = digest(output_manifest)
    structural["scope"] = "Captured shard bytes validated in staging; published paths reference exactly the same hashes and counts after atomic directory rename."
    write_new(args.output_dir / "validation.json", structural)
    if not structural["valid"]:
        raise ValueError("structural validation rejected the diagnostic")
    lexical = {"raw": [], "number_masked": []}
    for mode in lexical:
        def encoding(row):
            tokens = normalized(row["state"]).split()
            if mode == "number_masked":
                tokens = ["NUM" if token.isdigit() else token for token in tokens]
            return set(zip(tokens, tokens[1:], tokens[2:]))
        old_encodings = [encoding(row) for row in historical]
        for row in rows:
            tokens = encoding(row)
            for previous, old in zip(historical, old_encodings):
                score = len(tokens & old) / len(tokens | old) if tokens | old else 0
                if score >= 0.3:
                    lexical[mode].append({"id": row["id"], "historical_id": previous["id"],
                        "historical_split": previous["split"], "similarity": round(score, 6)})
        lexical[mode].sort(key=lambda pair: -pair["similarity"])
    counts = {"decisions": len(rows), "source_policy_groups": len(group_counts), "mechanisms": len(mechanisms),
              "decisions_per_mechanism": dict(Counter(r["provenance"]["mechanism_id"] for r in rows)),
              "policy_groups_per_mechanism": dict(Counter(plans[g]["mechanism"]["id"] for g in group_counts))}
    write_new(args.output_dir / "case-metadata.json", {"schema_version": "0.1", "dataset_id": config["dataset_id"], "counts": counts, "cases": metadata_rows})
    write_new(args.output_dir / "exclusion.json", {"historical_rows": len(historical), "historical_sha256": history_hashes, "historical_manifest_sha256": historical_manifests,
        "exact_id_group_input_state_matches": 0, "lexical_candidates_at_0_3": lexical,
        "qualification": "Seen-mechanism overlap is intentional; lexical candidates are not source-copy verdicts. Exact/lexical nonmatches do not prove semantic independence. Evaluation owns probe exclusion; no evaluation/final content read."})
    provenance = {"schema_version": "0.1", "dataset_id": config["dataset_id"], "stratum": config["stratum"],
        "counts": counts, "permanently_training_excluded": True, "derivatives_never_train": True,
        "plan_sha256": digest(args.config), "training_manifest": config["training_manifest"],
        "training_manifest_sha256": digest(training_path), "sources": sources,
        "additional_spend_gbp": actual_cost, "pending_spend_gbp": pending_cost,
        "limitations": ["Developmental seen-mechanism evidence, not final or mechanism-disjoint evaluation",
            "Two cases share each new policy; common authors/algorithms remain; not iid",
            "Rule recomputation is same-author separate-algorithm consistency, not independent text verification"]}
    if args.review_report:
        provenance["review_report"] = {"path": str(args.review_report.resolve()), "sha256": digest(args.review_report)}
    write_new(args.output_dir / "provenance.json", provenance)
    evidence = args.evidence + ([args.review_report, args.review_manifest] if args.review_report else [])
    write_new(args.output_dir / "freeze.json", {"dataset_id": config["dataset_id"], "created_at": datetime.now(timezone.utc).isoformat(),
        "manifest_sha256": digest(output_manifest), "plan_sha256": digest(args.config),
        "case_metadata_sha256": digest(args.output_dir / "case-metadata.json"),
        "predictions_requested_by_data": False, "permanently_training_excluded": True,
        "publication": "Publisher-owned captured shards; completed directory atomically renamed, never replaced",
        "evidence_sha256": {str(path.resolve()): digest(path) for path in evidence},
        "helper_source_sha256": {name: digest(Path(__file__).parent / name) for name in ("freeze_diagnostic.py", "audit.py", "assemble.py", "validate.py")},
        "files_sha256": {str(path.relative_to(args.output_dir)): digest(path) for path in sorted(args.output_dir.rglob("*")) if path.is_file()}})
    if final_output.exists():
        raise ValueError("publication appeared while staging; refusing overwrite")
    os.rename(args.output_dir, final_output)
    output_manifest = final_output / "manifest.json"
    if args.manifest_copy:
        write_new(args.manifest_copy, manifest)
        write_new(args.manifest_copy.with_name(args.manifest_copy.stem + ".provenance.json"), provenance)
    print({"dataset_id": config["dataset_id"], "manifest_sha256": digest(output_manifest), "counts": counts,
           "historical_comparison_rows": len(historical), "lexical_candidates": {mode: len(pairs) for mode, pairs in lexical.items()}})


if __name__ == "__main__":
    main()
