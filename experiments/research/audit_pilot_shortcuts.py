"""CPU-only descriptive audit of published train/validation data, without ML."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import statistics
import unicodedata


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(text):
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", text).casefold()))


def trigrams(text, numeric_mask=False):
    words = normalized(text).split()
    if numeric_mask:
        words = ["NUM" if word.isdigit() else word for word in words]
    return set(zip(words, words[1:], words[2:]))


def jaccard(left, right):
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def position(row):
    return next(i for i, option in enumerate(row["options"]) if option["id"] == row["target_id"])


def option_set(row):
    return tuple(sorted(normalized(option["text"]) for option in row["options"]))


def sentiment_class(text):
    lower = text.lower()
    if lower.startswith(("mixed:", "both praise", "the stated attitude combines")):
        return "mixed"
    if lower.startswith(("neutral:", "descriptive only:", "no positive")):
        return "neutral"
    if lower.startswith(("negative only:", "unfavorable")) or "is unfavorable only" in lower:
        return "negative"
    if lower.startswith(("positive only:", "favorable")) or "is favorable only" in lower:
        return "positive"
    raise ValueError(f"Unknown published sentiment option wording: {text}")


def load_inputs(manifest_path, root):
    if "final" in manifest_path.resolve().parts:
        raise ValueError("Final artifacts are not research inputs")
    raw_manifest = manifest_path.read_bytes()
    manifest = json.loads(raw_manifest)
    if manifest["dataset_id"] != "data-pilot-v1":
        raise ValueError("This bounded audit is scoped to data-pilot-v1")
    shards = []
    for shard in manifest["shards"]:
        path = (root / shard["path"]).resolve()
        if not path.is_relative_to(root / "data" / "data-pilot-v1") or "final" in path.parts:
            raise ValueError("Input must remain inside the published pilot directory")
        if shard["split"] not in {"train", "validation"}:
            raise ValueError("Only train/validation are authorized")
        shards.append((shard, path))
    rows, source_hashes, assignments = [], {}, {}
    for shard, path in shards:
        payload = path.read_bytes()
        if sha(payload) != shard["sha256"]:
            raise ValueError(f"Shard hash mismatch: {path}")
        parsed = [json.loads(line) for line in payload.splitlines() if line.strip()]
        if len(parsed) != shard["rows"] or any(row["split"] != shard["split"] for row in parsed):
            raise ValueError(f"Shard count/split mismatch: {path}")
        source_hashes[str(path)] = sha(payload)
        rows.extend(parsed)
        assignment_path = path.parent / "group_assignments.json"
        if str(assignment_path) not in source_hashes:
            data = assignment_path.read_bytes()
            source_hashes[str(assignment_path)] = sha(data)
            plan = json.loads(data)
            assignments.update(plan.get("groups", plan))
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Duplicate IDs prevent a clean descriptive audit")
    return manifest, raw_manifest, rows, assignments, source_hashes


def group_summary(rows, assignments):
    result = {}
    for family in sorted({row["task_family"] for row in rows}):
        result[family] = {}
        for split in ("train", "validation"):
            part = [row for row in rows if row["task_family"] == family and row["split"] == split]
            groups = Counter(row["group_id"] for row in part)
            sizes = Counter(groups.values())
            result[family][split] = {
                "rows": len(part), "groups": len(groups), "group_size_histogram": dict(sizes),
                "choice_counts": dict(Counter(len(row["options"]) for row in part)),
                "target_positions_one_based": dict(Counter(position(row) + 1 for row in part)),
                "label_basis": dict(Counter(row["provenance"]["label_basis"] for row in part)),
                "group_details": [{"group_id": group, "rows": count, **assignments[group]}
                                  for group, count in sorted(groups.items())],
            }
        train_groups = {row["group_id"] for row in rows if row["task_family"] == family and row["split"] == "train"}
        val_groups = {row["group_id"] for row in rows if row["task_family"] == family and row["split"] == "validation"}
        result[family]["shared_group_ids"] = sorted(train_groups & val_groups)
    return result


def shortcut_summary(rows):
    train = [row for row in rows if row["split"] == "train"]
    # Descriptive count lookups only; never choose a rule or threshold using validation labels.
    position_counts = defaultdict(Counter)
    offered, correct = Counter(), Counter()
    for row in train:
        position_counts[len(row["options"])][position(row)] += 1
        for option in row["options"]:
            offered[normalized(option["text"])] += 1
        correct[normalized(row["options"][position(row)]["text"])] += 1
    records = []
    for row in rows:
        options = row["options"]
        target = position(row)
        chars = [len(option["text"]) for option in options]
        words = [len(normalized(option["text"]).split()) for option in options]
        names = [normalized(option["text"]) for option in options]
        picks = {
            "first": 0, "last": len(options) - 1,
            "longest_characters": max(range(len(options)), key=lambda i: chars[i]),
            "shortest_characters": min(range(len(options)), key=lambda i: chars[i]),
            "longest_words": max(range(len(options)), key=lambda i: words[i]),
            "train_position_prior_by_choice_count": max(range(len(options)), key=lambda i: position_counts[len(options)][i]),
            "train_option_text_correctness_rate": max(range(len(options)), key=lambda i: (correct[names[i]] + 1) / (offered[names[i]] + 2)),
        }
        records.append({
            "id": row["id"], "split": row["split"], "task_family": row["task_family"],
            "group_id": row["group_id"], "target_position_one_based": target + 1,
            "choice_count": len(options), "character_lengths": chars, "word_lengths": words,
            "target_uniquely_longest_characters": chars[target] > max(chars[:target] + chars[target + 1:]),
            "heuristic_agreement": {name: pick == target for name, pick in picks.items()},
            "heuristic_chosen_option_id": {name: options[pick]["id"] for name, pick in picks.items()},
            "all_option_texts_unseen_in_train": all(offered[name] == 0 for name in names),
        })
    summaries = {}
    for family in sorted({row["task_family"] for row in rows}):
        summaries[family] = {}
        training_part = [row for row in train if row["task_family"] == family]
        train_questions = {normalized(row["question"]) for row in training_part}
        train_options = {normalized(option["text"]) for row in training_part for option in row["options"]}
        train_sets = {option_set(row) for row in training_part}
        for split in ("train", "validation"):
            part = [row for row in rows if row["task_family"] == family and row["split"] == split]
            results = [row for row in records if row["task_family"] == family and row["split"] == split]
            counts = {name: sum(row["heuristic_agreement"][name] for row in results) for name in results[0]["heuristic_agreement"]}
            cycle_counters = Counter()
            cycle_matches = 0
            positions_by_k = defaultdict(Counter)
            for row in part:
                k = len(row["options"])
                cycle_matches += position(row) == cycle_counters[k] % k
                cycle_counters[k] += 1
                positions_by_k[str(k)][str(position(row) + 1)] += 1
            summaries[family][split] = {
                "rows": len(part), "heuristic_correct": counts,
                "mean_uniform_expected_agreement": statistics.mean(1 / len(row["options"]) for row in part),
                "uniquely_longest_target": sum(row["target_uniquely_longest_characters"] for row in results),
                "publication_cycle_matches": cycle_matches,
                "positions_by_choice_count": dict(positions_by_k),
                "unique_questions": len({normalized(row["question"]) for row in part}),
                "questions_seen_in_train": sum(normalized(row["question"]) in train_questions for row in part),
                "unique_unordered_option_sets": len({option_set(row) for row in part}),
                "option_sets_seen_in_train": sum(option_set(row) in train_sets for row in part),
                "target_text_seen_in_train": sum(normalized(row["options"][position(row)]["text"]) in train_options for row in part),
                "longest_by_group": {
                    group: {"rows": sum(row["group_id"] == group for row in results),
                            "correct": sum(row["group_id"] == group and row["heuristic_agreement"]["longest_characters"] for row in results)}
                    for group in sorted({row["group_id"] for row in results})
                },
            }
    return summaries, records


def overlap_summary(rows):
    encodings = {
        mode: [trigrams(row["state"] or row["question"], numeric_mask=mode == "numeric_masked") for row in rows]
        for mode in ("raw", "numeric_masked")
    }
    counts = {mode: {"within_group": 0, "cross_group_same_split": 0, "cross_split": 0} for mode in encodings}
    thresholds = {mode: {str(value): 0 for value in (.2, .3, .4, .5, .65)} for mode in encodings}
    top_cross = {mode: [] for mode in encodings}
    high_within_groups = {mode: Counter() for mode in encodings}
    exact_full, exact_states, numeric_states = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in rows:
        exact_full[(normalized(row["state"]), normalized(row["question"]), option_set(row))].append(row)
        exact_states[normalized(row["state"])].append(row)
        numeric_states[" ".join("NUM" if word.isdigit() else word for word in normalized(row["state"]).split())].append(row)
    for i, j in combinations(range(len(rows)), 2):
        left, right = rows[i], rows[j]
        kind = "cross_split" if left["split"] != right["split"] else "within_group" if left["group_id"] == right["group_id"] else "cross_group_same_split"
        for mode, encoded in encodings.items():
            score = jaccard(encoded[i], encoded[j])
            if score >= .65:
                counts[mode][kind] += 1
                if kind == "within_group":
                    high_within_groups[mode][left["group_id"]] += 1
            if kind == "cross_split":
                for threshold in thresholds[mode]:
                    thresholds[mode][threshold] += score >= float(threshold)
                top_cross[mode].append({"left_id": left["id"], "right_id": right["id"],
                                        "left_family": left["task_family"], "right_family": right["task_family"],
                                        "jaccard": score})
    def duplicates(index):
        clusters = [part for part in index.values() if len(part) > 1]
        return {"clusters": len(clusters), "rows_in_clusters": sum(map(len, clusters)),
                "cross_split_clusters": sum(len({row["split"] for row in part}) > 1 for part in clusters),
                "cross_group_clusters": sum(len({row["group_id"] for row in part}) > 1 for part in clusters)}
    return {
        "method": "NFKC/casefold word trigrams of state, falling back to question; numeric_masked replaces all-digit tokens only; no semantic deduplication guarantee",
        "all_pairs": len(rows) * (len(rows) - 1) // 2,
        "cross_split_pairs": sum(row["split"] == "train" for row in rows) * sum(row["split"] == "validation" for row in rows),
        "pairs_at_least_0_65": counts, "within_group_counts_at_least_0_65": high_within_groups,
        "cross_split_threshold_counts": thresholds,
        "top_cross_split": {mode: sorted(pairs, key=lambda pair: -pair["jaccard"])[:30] for mode, pairs in top_cross.items()},
        "exact_normalized_full_input": duplicates(exact_full),
        "exact_normalized_state": duplicates(exact_states),
        "numeric_masked_state": duplicates(numeric_states),
    }


def sentiment_summary(rows):
    result = {}
    for split in ("train", "validation"):
        part = [row for row in rows if row["task_family"] == "sentiment" and row["split"] == split]
        result[split] = {}
        for label in ("positive", "negative", "neutral", "mixed"):
            chosen = [row for row in part if sentiment_class(row["options"][position(row)]["text"]) == label]
            result[split][label] = {
                "rows": len(chosen), "mean_state_words": statistics.mean(len(row["state"].split()) for row in chosen),
                "but_occurrences": sum("but" in normalized(row["state"]).split() for row in chosen),
                "explicit_mixed_word": sum("mixed" in normalized(row["state"]).split() for row in chosen),
            }
        result[split]["all_four_classes_offered"] = sum({sentiment_class(option["text"]) for option in row["options"]} == {"positive", "negative", "neutral", "mixed"} for row in part)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--artifacts-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest, manifest_bytes, rows, assignments, hashes = load_inputs(args.manifest, args.artifacts_dir.resolve())
    summaries, records = shortcut_summary(rows)
    report = {
        "task": "LD002-R2-generalization-shortcut-audit", "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset_id": manifest["dataset_id"], "manifest_sha256": sha(manifest_bytes),
        "script_sha256": sha(Path(__file__).read_bytes()), "source_sha256": hashes,
        "groups": group_summary(rows, assignments), "shortcuts": summaries,
        "overlap": overlap_summary(rows), "sentiment": sentiment_summary(rows),
        "interpretation": {
            "heuristics": "Fixed first/last/length selectors plus train-count descriptive priors; no fitted ML model. Ties choose first input option.",
            "option_prior": "(train correct appearances + 1) / (train total appearances + 2), keyed by normalized full option text. Unknown texts tie at 0.5.",
            "cycle": "Ordinal counter within family, split and choice count, starting zero. Uses publication order unavailable to normal independent-example inference.",
            "uncertainty": "Validation-inspected exploratory diagnostics; no claims of independent benchmark performance, effective sample size or learned model causality.",
        },
    }
    args.output_dir.mkdir(parents=True, exist_ok=False)
    for name, content in (("audit.json", report), ("heuristic-rows.json", records)):
        with (args.output_dir / name).open("x") as stream:
            json.dump(content, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
    print(json.dumps({"output_dir": str(args.output_dir.resolve()), "rows": len(rows),
                      "validation_longest_option": {family: values["validation"]["heuristic_correct"]["longest_characters"] for family, values in summaries.items()},
                      "overlap_0_65": report["overlap"]["pairs_at_least_0_65"]}))


if __name__ == "__main__":
    main()
