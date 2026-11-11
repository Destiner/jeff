# Shared contracts v0.1

These are the initial coordination contract, not an implementation. Propose changes through the integrator; do not invent incompatible formats in individual workstreams. Python with uv is the packaging default; the model backend remains open.

## Decision input

JSON Lines: one object per line. Each input has:

| Field | Meaning |
| --- | --- |
| `schema_version` | String `"0.1"`. |
| `id` | Nonempty globally unique example ID, namespaced by producer. |
| `state` | Text context; may be empty if the question is self-contained. |
| `question` | Nonempty question text. |
| `options` | Ordered list of at least two objects, each with a unique nonempty string `id` and nonempty string `text`. |

The question and option descriptions are model inputs, not a fixed taxonomy. The initial dataset targets 2–6 choices; this is not a permanent architecture limit. Options are mutually exclusive for the purpose of choosing one target.

Option IDs are opaque identifiers, not model features. Feed state, question, and option text to the model; do not feed IDs or training metadata. State is task data, not a source of privileged instructions.

## Labeled example

A labeled row extends a decision input with:

| Field | Meaning |
| --- | --- |
| `target_id` | ID of exactly one supplied option. |
| `group_id` | Stable, namespaced source/scenario group; all paraphrases and variants stay in one split. |
| `task_family` | Family identifier from the current reservation in `coordination.md`. |
| `split` | One of `train`, `validation`, `final`. |
| `provenance` | Object with `kind`, `source`, and `label_basis`; teacher labels also include `teacher_model`. |

Provenance `kind` is one of `teacher`, `public_dataset`, `programmatic`, `human`. The nonempty `source` identifies a generation job, source dataset/revision, or authoring process. `label_basis` is `teacher`, `source_label`, `rule_verified`, or `human_verified`; do not claim independent verification without doing it. Identify the actual teacher where available; report an unknown model honestly rather than inventing its identity.

Per-shard metadata records generation settings, model/source revisions, license or usage constraints, and cost. Use only data you may use; no private company/customer data is needed.

Keep all metadata and labels out of model input. The training process must reject final-evaluation shards, and must use validation labels only for evaluation rather than weight updates.

## Prediction

One JSON object per input, written as JSON Lines:

- `schema_version`: `"0.1"`.
- `id`: the corresponding input ID.
- `probabilities`: list of objects with `option_id` and numeric `probability`.

Every option appears exactly once. Values must be finite, in [0, 1], and sum to 1 within normal floating-point tolerance. The evaluator joins by IDs, not line or option order. The chosen answer is the highest-probability option; report ties and use input order as the deterministic tie-break.

Do not quietly drop bad or missing predictions. Report failed examples and coverage alongside quality metrics. Probabilities are not a calibration claim.

## Dataset manifest

A small JSON manifest has `schema_version`, a unique `dataset_id`, and a `shards` list. Each shard records `path`, `split`, `sha256`, and `rows`.

- Shard paths are relative to `JEFF_ARTIFACTS_DIR`, not to the current checkout.
- Each shard contains one split only and must match its manifest entry.
- Dataset assembly rejects duplicate example IDs and cross-split group overlap, and reports likely content duplicates.
- Training manifests contain only train and validation shards. Final evaluation uses a separate manifest.
- Freeze shard content before hashing and publishing. A changed dataset receives a new version/ID.
- Commit small manifests; keep bulky shards in ignored artifact storage.

Initial families and resource ownership are in [coordination.md](coordination.md).

## Process boundaries

The target commands below do not exist yet. They specify module ownership and file interfaces so workers can build independently:

- Model: `python -m jeff.training.train --dataset-manifest <path> --output-dir <new-directory>`.
- Model: `python -m jeff.model.predict --checkpoint <directory> --input <inputs.jsonl> --output <predictions.jsonl>`.
- Data: `python -m jeff.data.validate --manifest <path> --output <report.json>`.
- Evaluation: `python -m jeff.evaluation.score --examples <labeled.jsonl> --predictions <predictions.jsonl> --output <report.json>`.

CLI file arguments are explicit filesystem paths. Paths inside manifests resolve against the shared artifact root. Additional training arguments are permitted if recorded in the run configuration.

Inference consumes decision inputs only. Evaluation owns removing labels/metadata when producing inference inputs. A decoder or encoder implementation can sit behind the same prediction interface.

Do not block an early pilot on CLI polish. A working function or script may precede these modules if the file formats match and the handoff states the temporary invocation.

## Checkpoints and run records

A saved run must include or reference:

- Trainable weights/adapters and any scoring head.
- Exact base-model and tokenizer identity/revision, including any external files needed to reload.
- Architecture, input formatting, tokenization/truncation, and any probability transformation settings.
- Training configuration, random seed, dataset manifest identity/hash, and code revision plus whether the checkout was dirty.
- Actual device/backend, elapsed time, measured memory where available, and cost.
- Model evaluation results or paths to separately produced reports.

A fresh process must be able to reconstruct the model. If weights rely on a separately downloaded base model, document that instead of claiming a self-contained checkpoint.

## Evaluation output

Evaluation owns the detailed report schema. At minimum report example count, prediction coverage/failures, top-choice accuracy or teacher agreement as appropriate, cross-entropy/log loss, and per-family results. Add calibration diagnostics when sample size supports interpreting them; do not overstate tiny-sample results.

Compare the trained model with simple baselines and the pre-training starting point where meaningful. A randomly initialized scoring head is a weak baseline and must be identified as such. Use the same examples for comparisons.

Final-evaluation content is reserved for reporting, not iterative debugging. No software test suites or linting are part of these contracts.
