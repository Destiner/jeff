"""Publish the original tiny, teacher-authored pipeline dataset (stdlib only)."""

import hashlib
import json
import os
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[3]
    config = json.loads((root / "configs/data/tiny-v1.json").read_text())
    artifact_root = Path(os.environ["JEFF_ARTIFACTS_DIR"])
    dataset = artifact_root / "data" / config["dataset_id"]
    dataset.mkdir(parents=True, exist_ok=False)
    # Assignments are frozen in the config before these scenarios are authored.
    seeds = [
        ("intent", "cancel", "Please stop my monthly box before it renews. I don't want another delivery.", "What does the customer want?", ["Cancel the recurring subscription", "Track an existing delivery", "Change the delivery address"], 0),
        ("intent", "invoice", "The order arrived safely. Could you send me a tax invoice for my expense claim?", "Which request should be handled?", ["Return the purchased item", "Provide a purchase invoice", "Report a missing shipment"], 1),
        ("intent", "reschedule", "I still need the consultation, but Tuesday no longer works. Is there a slot on Friday?", "What is the caller's main intent?", ["Cancel without rebooking", "Book an additional consultation", "Move an existing appointment"], 2),
        ("sentiment", "lamp", "The lamp feels sturdy and lights my desk perfectly. I'm delighted with it.", "How does the reviewer feel about the lamp?", ["Unhappy with it", "Neither pleased nor displeased", "Pleased with it"], 2),
        ("sentiment", "meal", "The soup was cold, the bread was stale, and I regretted ordering here.", "What sentiment is expressed about the meal?", ["Negative: dissatisfaction", "Positive: satisfaction", "Neutral: factual without evaluation"], 0),
        ("sentiment", "museum", "The museum opens at ten and has three floors. I visited on Thursday.", "What sentiment does this statement express about the museum?", ["Positive: approval", "Neutral: no expressed approval or disapproval", "Negative: disapproval"], 1),
        ("rule_application", "parcel", "Parcel policy: a parcel weighing at most 2 kg uses the small tier; anything heavier uses the large tier. This parcel weighs exactly 2 kg.", "Which tier applies?", ["Large tier", "Small tier"], 1),
        ("rule_application", "entry", "Access is granted only when both a ticket and photo ID are present. Mira has a ticket but no photo ID.", "What does the access rule require?", ["Deny access", "Grant access"], 0),
        ("rule_application", "priority", "Routing policy: if a report mentions smoke, send it to safety, regardless of any other issue. Otherwise, send equipment failures to maintenance and all remaining reports to reception. A report describes smoke and a broken fan.", "Where should the report go?", ["Maintenance", "Reception", "Safety"], 2),
    ]
    by_split = {"train": [], "validation": []}
    for family, scenario, state, question, choices, target in seeds:
        group = "data:tiny:" + family + ":" + scenario
        split = config["group_splits"][group]
        options = [{"id": "c" + str(i), "text": text} for i, text in enumerate(choices)]
        row = dict(schema_version="0.1", id=group + ":01", state=state,
                   question=question, options=options, target_id=options[target]["id"],
                   group_id=group, task_family=family, split=split,
                   provenance=dict(kind="teacher", source="data-tiny-v1/bootstrap",
                                   label_basis="teacher", teacher_model=config["teacher_model"]))
        by_split[split].append(row)
    manifest = dict(schema_version="0.1", dataset_id=config["dataset_id"], shards=[])
    ids, groups, contents = set(), {}, set()
    for split, rows in by_split.items():
        for row in rows:
            assert row["id"] not in ids
            ids.add(row["id"])
            assert groups.setdefault(row["group_id"], split) == split
            assert row["task_family"] in {"intent", "sentiment", "rule_application"}
            assert row["target_id"] in [o["id"] for o in row["options"]]
            assert len({o["id"] for o in row["options"]}) == len(row["options"]) >= 2
            content = (row["state"].casefold(), row["question"].casefold())
            assert content not in contents
            contents.add(content)
        path = dataset / (split + ".jsonl")
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        manifest["shards"].append(dict(path=str(path.relative_to(artifact_root)), split=split,
                                       sha256=hashlib.sha256(path.read_bytes()).hexdigest(), rows=len(rows)))
    metadata = dict(config, generation_settings={"method": "direct authoring in approved agent session", "temperature": "not exposed", "seed": "not exposed", "variants_per_group": 1},
                    usage_constraints="Original synthetic text; no external datasets or private data. Existing agent-provider terms apply; no separate redistribution license asserted.",
                    label_verification="Teacher labels only; initial structural assertions passed, not independent semantic verification.")
    (dataset / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    encoded = json.dumps(manifest, indent=2) + "\n"
    (dataset / "manifest.json").write_text(encoded)
    (root / "manifests/data/tiny-v1.json").write_text(encoded)
    print(encoded)


if __name__ == "__main__":
    main()
