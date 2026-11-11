"""Prepare explicit local bundle sidecars; no model imports or network access."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    run = json.loads((args.run_dir / "run.json").read_text())
    checkpoint = json.loads((args.run_dir / "checkpoint/checkpoint.json").read_text())
    identities = {
        "sentence-transformers/all-MiniLM-L6-v2": ("m2", "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"),
        "cross-encoder/ms-marco-MiniLM-L6-v2": ("m3", "233902d25c440f23af6f7d6e94d2946bac0bee0a"),
    }
    candidate, revision = identities[checkpoint["model_id"]]
    if checkpoint["revision"] != revision or run["status"] != "completed":
        raise ValueError("requires the pinned completed M2/M3 run")
    output = args.output_dir
    output.mkdir(parents=False, exist_ok=False)
    (output / "licenses").mkdir()
    (output / "demo").mkdir()
    for source, target in [
        ("docs/runtime/BUNDLE-README.md", "README.md"),
        ("configs/runtime/requirements-macos-arm64-py312.txt", "requirements-macos-arm64-py312.txt"),
        ("configs/runtime/demo-inputs.jsonl", "demo/inputs.jsonl"),
        ("configs/runtime/licenses/APACHE-2.0.txt", "licenses/APACHE-2.0.txt"),
        (f"configs/runtime/licenses/{candidate}-model-card.md", "licenses/upstream-model-card.md"),
    ]:
        shutil.copyfile(repo / source, output / target)
    card_url = f"https://huggingface.co/{checkpoint['model_id']}/raw/{revision}/README.md"
    notice = f"""# Model origin, modifications and rights

This is Jeff's notice, not an upstream NOTICE file. Upstream model:
{checkpoint['model_id']} at {revision}.
Pinned card: {card_url}
The pinned repository declares Apache-2.0; its inventory contains no LICENSE or
NOTICE file. The canonical Apache-2.0 text and verbatim pinned card accompany
this bundle. Attribution and upstream training references remain in that card.
No upstream endorsement or trademark permission is implied.

## Modified/generated files (2026-11-11)

Jeff run {args.run_dir.name} fine-tuned checkpoint/encoder/model.safetensors
on data-pilot-v1, including the encoder and scoring head. M2 adds a newly
initialized scalar head in checkpoint/head.safetensors; M3 retains and
fine-tunes the original classifier inside encoder/model.safetensors.
checkpoint/checkpoint.json is Jeff-generated provenance/settings;
checkpoint/encoder/config.json and checkpoint/tokenizer/* were re-saved by
Transformers during checkpoint creation. This export preserves every byte of
the saved checkpoint; adjacent notices identify changes without rewriting the
immutable binary/configuration files. Review this notice placement before any
external distribution. No training data or upstream corpus is bundled.

## Distinct rights and restrictions

Apache-2.0 describes the upstream model, not a blanket license for Jeff's code,
new head, synthetic data or upstream corpora. No project license grant is
currently recorded. Jeff synthetic teacher outputs are subject to the actual
provider/account terms, not independently reviewed for redistribution or model
training rights. Teacher aliases lack immutable revisions; do not infer a
specific account contract. No external publication is authorized. Dependencies
are installed separately from their providers under their own licenses; no
dependency wheelhouse or complete dependency-license audit is included.
Original checkpoint provenance contains local project paths: privacy review is
required before distribution. Full Apache AS-IS limitations remain applicable.
"""
    (output / "licenses/NOTICE.md").write_text(notice)
    provenance = {
        "candidate": candidate.upper(), "source_run_id": args.run_dir.name,
        "source_run_sha256": sha(args.run_dir / "run.json"),
        "source_run_status": run["status"], "completed_at": run["completed_at"],
        "training_code_revision": run["code"]["revision"],
        "training_code_dirty": run["code"]["dirty"],
        "training_config": {k: v for k, v in run["config"].items() if k not in {"dataset_manifest", "output_dir"}},
        "dataset": {k: run["dataset"][k] for k in ("dataset_id", "manifest_sha256", "counts", "label_basis")},
        "root_uv_lock_sha256": sha(repo / "uv.lock"),
        "upstream_model_card_url": card_url,
        "upstream_declared_license": "Apache-2.0",
        "license_text_url": "https://www.apache.org/licenses/LICENSE-2.0.txt",
        "project_and_provider_redistribution_rights": "not cleared; no publication authorized",
        "checkpoint_metadata_note": "Save-time running snapshot and historical local paths are preserved; completed run receipt above supersedes job status. Paths are not runtime dependencies.",
        "demo": "Three original synthetic, label-free decisions authored for runtime demonstration only; no accuracy claim.",
    }
    (output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
