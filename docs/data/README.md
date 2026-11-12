# Data

The Data workstream owns only `src/jeff/data/`, `configs/data/`, `manifests/data/`, and `docs/data/`. Follow root `AGENTS.md` and contracts v0.1. Training content is outside Git in `JEFF_ARTIFACTS_DIR/data/`; ordinary Data tooling never consumes final-evaluation storage. D8 has a narrow, explicit construction-only exception for a new sealed external population, described below; it does not relax training or old-final guards.

## Published datasets

| Dataset | Train / validation | Manifest | Purpose |
| --- | ---: | --- | --- |
| `data-tiny-v1` | 6 / 3 | `manifests/data/tiny-v1.json` | Pipeline plumbing only |
| `data-pilot-v1` | 300 / 60 | `manifests/data/pilot-v1.json` | Initial three-family training pilot |
| `data-pilot-v2` | 1,500 / 300 | `manifests/data/pilot-v2.json` | Diverse expansion, including unchanged v1 |
| `data-final-sprint-v1` | 480 / 0 | `manifests/data/final-sprint-v1.json` | 240 fresh routing/sentiment/ticket cases + 240 original TRAIN replay; chosen M13 mixture |
| `data-d3-seen-rules-v1` | 0 / 96 | `manifests/data/d3-seen-rules-v1.json` | Validation-only seen-mechanism/new-policy diagnostic; never train |

The shared root is `/Users/destiner/Code/jeff/artifacts`. Each dataset also has a standalone `manifest.json` below `data/<dataset-id>/` (D3 uses `data/data-d3-seen-rules-v1/release/manifest.json`), so Model need not merge data code to consume it. **Use the manifest, not a directory glob.** Original sentiment producer rows are retained for provenance but excluded in favor of corrected `sentiment-r2` rows. Do not concatenate tiny and pilot automatically.

See [v1 quality and provenance](pilot-v1.md), [v2 delivery and limitations](pilot-v2.md), [the final-sprint mixture, reviews and limitations](final-sprint-v1.md), and [D3's separate diagnostic and limitations](d3-seen-rules-v1.md). The final-sprint release already includes 80 original TRAIN rows per family: do not concatenate it with v2. Its data release does not independently authorize learning. D3 has 96 decisions across 48 new policies and eight deliberately trained mechanisms; it and all derivatives are permanently training-excluded. V2 contains v1: do not concatenate the two manifests. Report inherited versus new validation strata separately. Small hashed manifests/configuration live in Git; JSONL, authored source cases, generation scripts, group allocations, reviewer decisions, and detailed reports remain in artifact storage. The Git checkout alone does not contain the training rows.

## Evaluation-only external populations

[D8 source-preserving external populations](d8-external-v1.md) provide200exploration cases (`validation`) and200sealed confirmation cases (`final`), each100COPA/100WinoGrande. Both and all derivatives are permanently `validation_only_never_train`. Metadata mirrors are `manifests/data/d8-external-exploration-v1.json` and `manifests/data/d8-external-confirmation-v1.json`; use the separate canonical manifests in the D8 document, never concatenate them into training.

D8's two new families are intentionally unsupported by the training validator. Evaluation alone emits stripped native/reversed consumer inputs; reference metadata is not inference authority. Source/label/rights/pretraining qualifications, fixed selection, actual audit evidence and protected access boundaries are in the D8 document. The examples and licenses remain in local artifact storage, not in Git.

## Setup, validation, build

Python 3.12 with the shared uv package; no extra dependencies or ML stack required. From the data worktree:

```sh
uv sync --locked
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
uv run --locked python -m jeff.data.validate \
  --manifest manifests/data/pilot-v1.json \
  --output "$JEFF_ARTIFACTS_DIR/data/<new-report-id>/validation.json"
uv build --no-sources
```

Choose a new report path each time; output creation is exclusive. `--artifacts-dir` can explicitly override the environment variable. Validator exit status is nonzero on structural/hash/duplicate/isolation failure. The JSON report includes counts, group counts, provenance basis, option/target-position distributions, and lexical candidates. Likely duplicates are review findings, not automatic semantic-duplication verdicts.

Validation checks required strings/schema, unique example/option IDs, distinct normalized choice descriptions, valid targets, provenance fields, positive declared row counts, hashes, split-pure shards, allowed training families, and cross-split group overlap. Full-input canonicalization ignores option order and opaque IDs and applies Unicode NFC/outer stripping, but preserves signs, brackets, case and internal spacing: these can be task data. State word-trigram Jaccard >=0.65 flags likely duplicates; no embedding model is loaded. Evaluation/final storage and final/unknown manifest splits are refused before shard reads. Exact canonical duplicates are rejected; word-normalized collisions are heuristic only. V2 exposed false conflicts when the earlier word-only canonicalizer erased negative coordinates and bracket strings; the corrected validator passes the actual unchanged examples.

No software tests, test suites, linting, or ML inference were run by Data. Dataset validation, teacher review, actual assembly, and package builds are the evidence.

## Assembly and replay

`configs/data/pilot-v1.json` freezes producer namespaces/splits/row plans. Producers each owned separate artifact directories and wrote domain/mechanism assignments before rows. The lead serially assembles those finished shards:

```sh
uv run --locked python -m jeff.data.assemble \
  --config configs/data/pilot-v1.json \
  --manifest <new-manifest-path.json> \
  --report <new-report-path.json>
```

The command creates a candidate, validates it, then publishes the manifest and provenance. Add `--candidate-only` with new candidate/report paths to review without publishing the final dataset. V2 config supports a pinned parent manifest, retains its shard entries and bytes, and checks the expanded total; its original pre-generation plan is archived in `data/data-pilot-v2/authoring-plan.json`. It verifies every group allocation and row count. Producer paths are contained within the configured dataset directory; all reads use the training-storage guard. Source identity and spending come from metadata, with totals checked against configuration. Unknown cost is an error, not zero. It never overwrites existing assembly outputs. This is the pilot's assembly tool, not a universal external-dataset importer.

For repeat assembly, restore the four producer directories (`intent`, `sentiment`, `sentiment-r2`, `rule_application`) under a **new artifact root**, retaining `data/data-pilot-v1/` relative paths, and pass `--artifacts-dir <new-root>`. Do not copy prior assembly records into that root. Reassembly of the actual 360 rows produced an identical manifest and semantically identical provenance at `data/data-pilot-reproduction-v1/`. Changing row content instead requires a new dataset/shard ID and new group plan as appropriate.

Original producer `generate.py` files retain authored cases, and rule `audit.py` plus `audit_cases.jsonl` retain executable label evidence. Do not run producer main functions in published directories: some overwrite reports. Source replay must preserve the original author's teacher identity rather than assigning labels to the replaying process. A teacher session is not stochastically reproducible; replaying its recorded cases is deterministic serialization, not new teacher generation.

`python -m jeff.data.prepare_sentiment --source <original-directory> --output <new-directory>` applies the documented pilot correction, preserving state/subject/group/split/teacher judgments. All four sentiment classes are always offered; positions are balanced per class and split using seed 20261111. The new directory must not exist. The original data and its metadata stay untouched.

`python -m jeff.data.bootstrap` is the checkout-only tiny publisher; it reads the committed tiny config and refuses an existing dataset directory. The nine-row tiny publisher ran before parallel pilot production; full validation subsequently passed.

## Expansion boundary and shortcut audit

`python -m jeff.data.audit --manifest <expanded-manifest> --parent-manifest <v1-manifest> --historical-manifest <tiny-manifest> --artifacts-dir <root> --research-script <checkout>/experiments/research/audit_pilot_shortcuts.py --output <new-directory>/audit.json` checks inherited rows and historical split exclusions, and produces inherited/new/combined diagnostics using Research's explicitly supplied, hashed CPU helper. It needs the helper source in addition to the installed data package; no ML dependencies. Use a new output directory because its per-row diagnostic files are also immutable.

Do not open Evaluation data to broaden this audit. Evaluation owns public-probe exclusion receipts; final storage remains prohibited. Exact/lexical negative findings are not semantic-derivative clearance. Model remains responsible for training only on train rows and for tokenizer compatibility with its selected backbone.

## Costs and scope

Additional spend: **£0 actual, £0 pending**. Existing approved agent access only; subscription/token costs were not separately metered. No separately billed API or cloud jobs. Pilot/D3 content is original synthetic English, not private records; existing provider terms apply and no blanket public-domain/license claim is made. D8 instead preserves approved public-source content with explicit attribution/rights qualifications and a separately scheduled Runtime tokenizer-only audit. Data performed no D8 model/tokenizer load or inference. Local source grants are not blanket public-redistribution clearance.
