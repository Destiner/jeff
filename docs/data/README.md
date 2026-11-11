# Training data

The Data workstream owns only `src/jeff/data/`, `configs/data/`, `manifests/data/`, and `docs/data/`. Follow root `AGENTS.md` and contracts v0.1. Generated content is outside Git in `JEFF_ARTIFACTS_DIR/data/`; no final-evaluation data is consumed.

## Published datasets

| Dataset | Train / validation | Manifest | Purpose |
| --- | ---: | --- | --- |
| `data-tiny-v1` | 6 / 3 | `manifests/data/tiny-v1.json` | Pipeline plumbing only |
| `data-pilot-v1` | 300 / 60 | `manifests/data/pilot-v1.json` | Initial three-family training pilot |

The shared root is `/Users/destiner/Code/jeff/artifacts`. Each dataset also has a standalone `manifest.json` below `data/<dataset-id>/`, so Model need not merge data code to consume it. **Use the manifest, not a directory glob.** Original sentiment producer rows are retained for provenance but excluded in favor of corrected `sentiment-r2` rows. Do not concatenate tiny and pilot automatically.

See [pilot quality and provenance](pilot-v1.md). Small hashed manifests/configuration live in Git; JSONL, authored source cases, generation scripts, group allocations, reviewer decisions, and detailed reports remain in artifact storage. The Git checkout alone does not contain the training rows.

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

Validation checks required strings/schema, unique example/option IDs, distinct normalized choice descriptions, valid targets, provenance fields, positive declared row counts, hashes, split-pure shards, allowed training families, and cross-split group overlap. Full-input normalization ignores option order and opaque IDs. State word-trigram Jaccard >=0.65 flags likely duplicates; no embedding model is loaded. Evaluation/final storage and final/unknown manifest splits are refused before shard reads. Exact normalized duplicates are rejected conservatively; inspect normalization before concluding semantic identity.

No software tests, test suites, linting, or ML inference were run by Data. Dataset validation, teacher review, actual assembly, and package builds are the evidence.

## Assembly and replay

`configs/data/pilot-v1.json` freezes producer namespaces/splits/row plans. Producers each owned separate artifact directories and wrote domain/mechanism assignments before rows. The lead serially assembles those finished shards:

```sh
uv run --locked python -m jeff.data.assemble \
  --config configs/data/pilot-v1.json \
  --manifest <new-manifest-path.json> \
  --report <new-report-path.json>
```

The command creates a candidate, validates it, then publishes the manifest and provenance. It verifies every group allocation and row count. Producer paths are contained within the configured dataset directory; all reads use the training-storage guard. Source identity and spending come from metadata, with totals checked against configuration. Unknown cost is an error, not zero. It never overwrites existing assembly outputs. This is the pilot's assembly tool, not a universal external-dataset importer.

For repeat assembly, restore the four producer directories (`intent`, `sentiment`, `sentiment-r2`, `rule_application`) under a **new artifact root**, retaining `data/data-pilot-v1/` relative paths, and pass `--artifacts-dir <new-root>`. Do not copy prior assembly records into that root. Reassembly of the actual 360 rows produced an identical manifest and semantically identical provenance at `data/data-pilot-reproduction-v1/`. Changing row content instead requires a new dataset/shard ID and new group plan as appropriate.

Original producer `generate.py` files retain authored cases, and rule `audit.py` plus `audit_cases.jsonl` retain executable label evidence. Do not run producer main functions in published directories: some overwrite reports. Source replay must preserve the original author's teacher identity rather than assigning labels to the replaying process. A teacher session is not stochastically reproducible; replaying its recorded cases is deterministic serialization, not new teacher generation.

`python -m jeff.data.prepare_sentiment --source <original-directory> --output <new-directory>` applies the documented pilot correction, preserving state/subject/group/split/teacher judgments. All four sentiment classes are always offered; positions are balanced per class and split using seed 20261111. The new directory must not exist. The original data and its metadata stay untouched.

`python -m jeff.data.bootstrap` is the checkout-only tiny publisher; it reads the committed tiny config and refuses an existing dataset directory. The nine-row tiny publisher ran before parallel pilot production; full validation subsequently passed.

## Costs and scope

Additional spend: **£0 actual, £0 pending**. Existing approved agent access only; subscription/token costs were not separately metered. No separately billed API or cloud jobs, no large models, and no Model compute slot used. Original synthetic English; no private records or external datasets. Existing provider terms apply; redistribution rights were not independently reviewed and no blanket public-domain/license claim is made.
