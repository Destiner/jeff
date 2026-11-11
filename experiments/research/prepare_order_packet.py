#!/usr/bin/env python3
"""Prepare the frozen R6 TRAIN-only packet; stdlib only, no inference/tokenization."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


MANIFEST = "data/data-pilot-v2/manifest.json"
MANIFEST_SHA = "d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac"
P3_CONFIG = "configs/runtime/p3-qwen.json"
P3_CONFIG_SHA = "2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f"
SALT = "R6/train/orderdiagnostic/v1"
CONDITIONS = ("O0L0", "O0L1", "O1L0", "O1L1")
MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
SYSTEM = "You are a decision assistant. Choose exactly one of the listed options. Reply with only its letter."
USER = "State:\n{state}\n\nQuestion:\n{question}\n\nOptions:\n{options}"
CHAT_TEMPLATE_SHA = "cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f"
# Directory, family, producer, quota, frozen allocation-metadata SHA-256.
SOURCES = (
    ("data/data-pilot-v1/intent", "intent", "inherited", 4, "9831ff3d6a17977243ac556f4bcea64cd920176b319773ee112c569db6e13175"),
    ("data/data-pilot-v2/intent-a-r2", "intent", "new_a", 6, "dbab24c2d96c1e021a90e22a0c2ccf6a7e409a2fa53b9ddc85d19f20274cb8ba"),
    ("data/data-pilot-v2/intent-b-r2", "intent", "new_b", 6, "95081b403116ef3ddf0f1124e673c036db7bfbf987afe44d054f8404c45f84ac"),
    ("data/data-pilot-v1/sentiment-r2", "sentiment", "inherited", 4, "90d050aa3ae28fd8eda5d50705f2c639ee1c383177ca0ea3baba5f50d7fac5b3"),
    ("data/data-pilot-v2/sentiment-a", "sentiment", "new_a", 6, "2f464d747cd5225578264d42e786958e460d819943027700271d44273efd9204"),
    ("data/data-pilot-v2/sentiment-b-r2", "sentiment", "new_b", 6, "0b1a24d06881e27dff29dfec59c7441c81198458eb7a6481e1fb38accc859c2d"),
    ("data/data-pilot-v1/rule_application", "rule_application", "inherited", 4, "58988ce2a56fe86f864c9002d5d04747cb7c2fbde97361dbca80ac0cdb3d9773"),
    ("data/data-pilot-v2/rule-a", "rule_application", "new_a", 6, "24ce6eccbe50a103eb91d76f3acbc1ea6f03bac80bc54d9b87f7c9914180aa70"),
    ("data/data-pilot-v2/rule-b", "rule_application", "new_b", 6, "8faf379756a21be82650cf37b8907c46c5cb181a049940e9952b081a2ba4bd5b"),
)
ALGORITHM = {
    "salt": SALT,
    "rank": "SHA256(UTF8(salt + LF + original TRAIN id)); hex ascending, id tie-break",
    "bucket_order": "SOURCES order: intent, sentiment, rule_application; inherited, new_a, new_b",
    "quotas_per_family": {"inherited": 4, "new_a": 6, "new_b": 6},
    "candidate_fields": "id, group_id, provenance parent_id/scenario_id/source, TRAIN domain/mechanism allocations only",
    "root": "parent_id else scenario_id else id; policy=scenario_id for new-v2 rules (released policy identity), null otherwise",
    "broad_source": "provenance.source before first '#' then before first ';case='; never follow reference",
    "greedy": "Within each bucket, prefer candidates with unused root AND group AND non-null policy; if none, allow repeats. Minimize (domain_count+mechanism_count, domain_count, mechanism_count, broad_source_count, group_count, hash_rank, id). Missing domain/mechanism has count 0. Counts reset per bucket. Update all counts after each pick.",
    "output_order": "bucket order, then greedy pick order, then O0L0/O0L1/O1L0/O1L1",
    "no_outcomes": "No target values, model predictions, input text, option count or label-position balancing in selection; no quota transfer or silent reduction",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def loads(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda _: fail_constant())


def fail_constant():
    raise ValueError("nonfinite JSON constant")


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def text(value, allow_empty=False):
    require(isinstance(value, str) and (allow_empty or value.strip()), "invalid string")
    return value


def local_path(root, relative):
    p = root / relative
    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
            "unsafe relative source path")
    require(p.resolve().is_relative_to(root), "source escapes repository/artifact root")
    require(not any(part.lower() in {"evaluation", "final", "probe", "probes"}
                    for part in Path(relative).parts), "excluded source path")
    require(not any(parent.is_symlink() for parent in (p, *p.parents) if parent != root.parent),
            "symlink source prohibited")
    return p


def pinned(root, relative, expected):
    p = local_path(root, relative)
    raw = p.read_bytes()
    require(sha(raw) == expected, "source hash mismatch: " + relative)
    return raw


def project(row, family, producer, source_path, allocations):
    require(isinstance(row, dict), "row must be object")
    require(row.get("schema_version") == "0.1" and row.get("split") == "train"
            and row.get("task_family") == family, "row schema/split/family mismatch")
    case_id = text(row["id"])
    group = text(row["group_id"])
    require("::" not in case_id, "reserved presentation separator in case id")
    provenance = row["provenance"]
    require(isinstance(provenance, dict), "invalid provenance")
    broad_source = text(provenance["source"]).split("#", 1)[0].split(";case=", 1)[0]
    parent = provenance.get("parent_id")
    scenario = provenance.get("scenario_id")
    for value in (parent, scenario):
        if value is not None:
            text(value)
    allocation = allocations.get(group)
    require(isinstance(allocation, dict) and allocation.get("split") == "train",
            "missing/non-TRAIN group allocation")
    domain, mechanism = allocation.get("domain"), allocation.get("mechanism")
    for value in (domain, mechanism):
        if value is not None:
            text(value)
    require(domain is not None or mechanism is not None, "no known broad stratum")
    options = row["options"]
    require(isinstance(options, list) and 2 <= len(options) <= 6, "require K=2..6")
    clean_options, ids = [], set()
    for option in options:
        require(isinstance(option, dict) and set(option) == {"id", "text"},
                "unexpected option fields")
        option_id = text(option["id"])
        require(option_id not in ids, "duplicate option id")
        ids.add(option_id)
        clean_options.append({"id": option_id, "text": text(option["text"])})
    # Whitelisting drops targets immediately; their values are never accessed.
    decision = {"id": case_id, "state": text(row["state"], allow_empty=True),
                "question": text(row["question"]), "options": clean_options}
    metadata = {"case_id": case_id, "family": family, "producer": producer,
                "source_path": source_path, "source_group": group,
                "broad_source_group": broad_source, "root": parent or scenario or case_id,
                "policy": scenario if family == "rule_application" and producer != "inherited" else None,
                "domain": domain, "mechanism": mechanism,
                "rank_sha256": sha((SALT + "\n" + case_id).encode("utf-8"))}
    return decision, metadata


def select(bucket, quota):
    require(len(bucket) >= quota, "insufficient candidates; no quota redistribution")
    counts = {k: Counter() for k in ("domain", "mechanism", "broad_source_group", "source_group", "root", "policy")}
    selected, remaining = [], list(bucket)
    for _ in range(quota):
        fresh = [item for item in remaining if all(
            item[1][k] is None or counts[k][item[1][k]] == 0
            for k in ("root", "source_group", "policy"))]
        pool = fresh or remaining

        def priority(item):
            m = item[1]
            d = counts["domain"][m["domain"]] if m["domain"] is not None else 0
            c = counts["mechanism"][m["mechanism"]] if m["mechanism"] is not None else 0
            return (d + c, d, c, counts["broad_source_group"][m["broad_source_group"]],
                    counts["source_group"][m["source_group"]], m["rank_sha256"], m["case_id"])

        chosen = min(pool, key=priority)
        chosen[1]["uniqueness_fallback"] = not bool(fresh)
        selected.append(chosen)
        remaining.remove(chosen)
        for key, counter in counts.items():
            if chosen[1][key] is not None:
                counter[chosen[1][key]] += 1
    return selected


def presentations(selected):
    records = []
    for decision, metadata in selected:
        case_id = metadata["case_id"]
        k = len(decision["options"])
        for condition in CONDITIONS:
            order_reversed = condition[1] == "1"
            letters_reversed = condition[3] == "1"
            positions = list(range(k))
            if order_reversed:
                positions.reverse()
            options = [{**decision["options"][original],
                        "letter": chr(65 + (k - 1 - display if letters_reversed else display)),
                        "original_position": original}
                       for display, original in enumerate(positions)]
            records.append({"id": case_id + "::" + condition, "case_id": case_id,
                            "condition": condition, "order_reversed": order_reversed,
                            "letters_reversed": letters_reversed, "state": decision["state"],
                            "question": decision["question"], "options": options})
    require(len(records) == 192 and len({r["id"] for r in records}) == 192,
            "presentation count/identity mismatch")
    return b"".join((json.dumps(r, ensure_ascii=False, sort_keys=True, allow_nan=False)
                     + "\n").encode("utf-8") for r in records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve(strict=True)
    artifacts = repo / "artifacts"
    output = args.output_dir.absolute()
    require(output.resolve().is_relative_to((artifacts / "research").resolve()),
            "output must be beneath artifacts/research")
    require(not output.exists() and not output.is_symlink(), "output already exists")
    require(output.parent.is_dir(), "output parent must already exist")
    manifest = loads(pinned(artifacts, MANIFEST, MANIFEST_SHA))
    require(manifest["schema_version"] == "0.1" and manifest["dataset_id"] == "data-pilot-v2",
            "manifest identity mismatch")
    entries = manifest["shards"]
    expected_train = {directory + "/train.jsonl" for directory, *_ in SOURCES}
    train = {e["path"]: e for e in entries if e["split"] == "train"}
    excluded = [e for e in entries if e["split"] != "train"]
    require(len(entries) == 18 and len(train) == 9 and len(excluded) == 9
            and len({e["path"] for e in entries}) == 18 and set(train) == expected_train,
            "unexpected manifest shard inventory")
    require(all(e["split"] == "validation" for e in excluded), "unexpected excluded split")
    require(not ({e["sha256"] for e in train.values()} & {e["sha256"] for e in excluded}),
            "TRAIN shard hash collides with excluded manifest hash")
    cfg = loads(pinned(repo, P3_CONFIG, P3_CONFIG_SHA))
    fixed = {"model_id": MODEL, "revision": REVISION, "system_prompt": SYSTEM,
             "user_template": USER, "symbols": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
             "max_input_tokens": 1024, "dtype": "float32", "device": "mps",
             "batch_size": 1, "threads": 4, "attention": "sdpa", "use_cache": False,
             "logits_to_keep": 1, "temperature": 1.0, "startup_rows": 3,
             "maximum_run_seconds": 1200,
             "max_cpu_rss_bytes": 8589934592, "max_mps_driver_bytes": 8589934592}
    require(all(cfg.get(k) == v for k, v in fixed.items()), "P3 control mismatch")
    cfg = {**cfg, "maximum_run_seconds": 300}
    selected, seen, source_hashes = [], set(), []
    for directory, family, producer, quota, allocation_sha in SOURCES:
        relative = directory + "/train.jsonl"
        entry = train[relative]
        raw = pinned(artifacts, relative, entry["sha256"])
        allocation_path = directory + "/group_assignments.json"
        allocations = loads(pinned(artifacts, allocation_path, allocation_sha))
        allocations = allocations.get("groups", allocations)
        require(isinstance(allocations, dict), "invalid group allocation container")
        bucket = []
        for line in raw.splitlines():
            require(line.strip(), "blank TRAIN line")
            item = project(loads(line), family, producer, relative, allocations)
            require(item[0]["id"] not in seen, "duplicate TRAIN id")
            seen.add(item[0]["id"])
            item[1]["train_sha256"] = entry["sha256"]
            bucket.append(item)
        expected_rows = 100 if producer == "inherited" else 200
        require(len(bucket) == entry["rows"] == expected_rows, "TRAIN row count mismatch")
        selected.extend(select(bucket, quota))
        source_hashes.append({**entry, "absolute_path": str(artifacts / relative),
                              "allocation_path": allocation_path,
                              "allocation_sha256": allocation_sha})
    require(len(seen) == 1500 and len(selected) == 48, "TRAIN/selected count mismatch")
    selection = {"schema_version": "r6.selection.v1", "algorithm": ALGORITHM,
                 "train_manifest_path": str(artifacts / MANIFEST),
                 "train_manifest_sha256": MANIFEST_SHA, "cases": [m for _, m in selected],
                 "train_sources": source_hashes}
    files = {"inputs.jsonl": presentations(selected), "selection.json": encoded(selection),
             "config.json": encoded(cfg)}
    script = Path(__file__).resolve()
    runtime = local_path(repo, "src/jeff/runtime/qwen_challenger.py")
    packet = {"schema_version": "r6.order-packet.v1", "status": "prepared_not_executed",
              "input": {"path": "inputs.jsonl", "sha256": sha(files["inputs.jsonl"]), "rows": 192},
              "cases": 48, "conditions": list(CONDITIONS), "split": "train",
              "selection": {"path": "selection.json", "sha256": sha(files["selection.json"])},
              "config": {"path": "config.json", "sha256": sha(files["config.json"])},
              "source": {"path": str(script), "sha256": sha(script.read_bytes())},
              "train_manifest": {"path": str(artifacts / MANIFEST), "sha256": MANIFEST_SHA},
              "train_sources": source_hashes,
              "excluded_shards_manifest_only_not_opened": excluded,
              "p3": {"model_id": MODEL, "revision": REVISION, "system_prompt": SYSTEM,
                     "user_template": USER, "chat_template_sha256": CHAT_TEMPLATE_SHA,
                     "config_path": str(repo / P3_CONFIG), "config_sha256": P3_CONFIG_SHA,
                     "frozen_code_revision": "49823af30d6b394a147c7b8a9f5c676526a439f3",
                     "frozen_source_sha256": "325d3a6b8e5577bba3b885fe8b61d5551305b456e2586d3949b2c45c649438d5",
                     "pin_provenance": "manifests/releases/p3-qwen-20261111-01.json",
                     "current_runtime_source_path": str(runtime),
                     "current_runtime_source_sha256": sha(runtime.read_bytes())},
              "rendering": {"option_line": "{letter}. {text}", "separator": "\n",
                            "chat": "official pinned tokenizer.apply_chat_template; tokenize=False; add_generation_prompt=True; encode(add_special_tokens=False); no truncation",
                            "original_position": "zero-based released TRAIN option index",
                            "answer_mapping": "next-token scores in displayed options order, using each option.letter; softmax T=1; join via option.id",
                            "model_prompt_fields": ["state", "question", "options[].text", "options[].letter"]},
              "resource_bounds": {"maximum_run_seconds": 300, "max_cpu_rss_bytes": 8589934592,
                                  "max_mps_driver_bytes": 8589934592,
                                  "memory_limits_are_nonadditive": True},
              "runtime_requirements": ["Model grant; Runtime execution only; unchanged frozen P3, not M6 checkpoint",
                                       "Verify all packet hashes; do not pass this packet to stock three-suite P3 reader",
                                       "Verify pinned chat-template digest, full prompt <=1024 tokens, special-token exclusion and single-token answer boundaries before model execution",
                                       "Honor supplied letters, never regenerate ascending symbols; no ids/metadata in prompts",
                                       "No generation, training, prompt search, downloads or extra diagnostic presentations",
                                       "startup_rows=3 means first three actual records; retain their predictions, do not repeat them as warmup; <=192 total forwards",
                                       "300-second total process bound includes audit/tokenization/load/inference; no fallback, retries or extra startup forwards",
                                       "Record runner source/config/assets/environment and actual resource/time evidence separately; do not mutate packet"]}
    files["packet.json"] = encoded(packet)
    # Claim only after every source and in-memory artifact has validated.
    output.mkdir(exist_ok=False)
    try:
        for name, raw in files.items():
            with (output / name).open("xb") as stream:
                stream.write(raw)
            (output / name).chmod(0o444)
    finally:
        output.chmod(0o555)
    print(json.dumps({"packet": str(output / "packet.json"),
                      "packet_sha256": sha(files["packet.json"]),
                      "cases": 48, "rows": 192, "status": "prepared_not_executed"}))


if __name__ == "__main__":
    main()
