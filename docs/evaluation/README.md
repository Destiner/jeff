# File-based evaluation

Latest independent results: [Data-v2 / M4 comparison](pilot-e3-m4.md): both candidates improve new-data agreement/loss, but neither passes the pre-result historical robustness gate. Includes frozen inherited/new/probe boundaries, probability quality, source-unit results and exact-reversal evidence. Prior [E2 pilot/M3 results](pilot-e2-m3.md) remain intact.

E3 preparation: [protocol](e3-plan.md), [identity freeze](e3-freeze.md), and [pinned study recipe](e3-study.md).

Runtime dependencies: Python standard library only (project Python 3.12/uv). No imports from Data, Model, or Training. No model downloads, software tests, or linting.

Shared packaging from approved main `1f64aea` is incorporated: run `uv sync --locked`, then `uv run --locked python -m`. Initial pre-packaging tiny runs used `PYTHONPATH=src python3` (3.9.6); subsequent curation/pilot/model comparisons use project Python 3.12. No ML extras are needed.

## Validation workflow

For a multi-shard Data manifest, first run `uv run --locked python -m jeff.evaluation.assemble --manifest <data-manifest> --dataset-id <new-evaluation-dataset-id> --output-dir <new-evaluation-artifact-dir>`. This verifies validation shard hashes/counts/splits, joins them into one frozen reference file, and records source provenance. It rejects final paths/manifests, does not read training content, and does not replace Data's cross-split validator.

```sh
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
export PYTHONPATH=src
E="$JEFF_ARTIFACTS_DIR/data/data-tiny-v1/validation.jsonl"
R="$JEFF_ARTIFACTS_DIR/evaluation/<new-unique-run>"
python3 -m jeff.evaluation.prepare --examples "$E" --output "$R/inputs.jsonl" --receipt "$R/input-receipt.json"
python3 -m jeff.evaluation.baseline --input "$R/inputs.jsonl" --method uniform --output "$R/uniform.jsonl" --receipt "$R/uniform-receipt.json"
python3 -m jeff.evaluation.baseline --input "$R/inputs.jsonl" --method lexical --output "$R/lexical.jsonl" --receipt "$R/lexical-receipt.json"
python3 -m jeff.evaluation.score --examples "$E" --predictions "$R/uniform.jsonl" --output "$R/uniform-report.json"
python3 -m jeff.evaluation.compare --examples "$E" --predictions "uniform=$R/uniform.jsonl" --predictions "lexical=$R/lexical.jsonl" --output "$R/comparison.json"
```

Send only `inputs.jsonl` to Model. Ask Model for both starting-checkpoint and fresh-reloaded trained predictions on this exact file. Add those named prediction files to the same compare command with a new output. A random initial scoring head must be named as such; it is not a strong pretrained task baseline.

All outputs are exclusive-create; choose new run IDs rather than overwriting. Receipts record SHA-256 file identity. Scoring accepts one frozen reference shard with one split. Dataset assembly and cross-shard validation remain Data's responsibility.

## Report semantics

- Exact ID joins for examples and option IDs; reference input order breaks exact maximum ties.
- Invalid references abort all metrics. A malformed reference is not silently removed. No diagnostic payload is exported for invalid references, to avoid leaking malformed final records.
- Prediction rows with unsupported schema, missing/duplicate/mismatched options, booleans, nonfinite/out-of-range probabilities, or sum error greater than 1e-6 are invalid. Duplicate prediction IDs invalidate every matching prediction. Blank/malformed records and duplicate JSON keys are unidentifiable records; the intended ID may also be missing.
- Valid sums within 1e-6 are normalized; counts and maximum deviations are reported. No epsilon clipping.
- Coverage partitions reference IDs into valid, missing, invalid, duplicate. Extras and unidentifiable records are reported separately; extras never change the reference denominator.
- Top-choice agreement has both valid-prediction and all-example denominators. Failed predictions are unsuccessful in the latter. Teacher labels yield **teacher agreement**, source labels yield source-label accuracy, and mixed labels yield reference-label agreement; basis-specific reports are mandatory.
- Natural-log loss and summed multiclass Brier score are conditional on valid predictions. Exact zero target probability means infinite log loss, serialized as null mean plus `status: positive_infinity`, not a fabricated finite penalty.
- Report overall, family, source group, label basis, family × basis, and option count. Five fixed confidence bins and ECE are descriptive, especially with small or correlated groups; no calibration claim or calibration fitting.
- Comparison recomputes every run on the same reference file and reports each run's full coverage, with paired differences overall, per family, and per source group. Pairwise deltas use the common-valid ID intersection, with wins/losses and its denominator. Positive agreement delta favors the left; negative loss delta favors the left. Infinite/empty loss deltas are undefined.

`score` returns 0 for a nonempty clean report, 1 for prediction issues/empty references (report still written), and 2 for fatal input/output/reference errors. `compare` returns 1 when any run has issues (report written), and 2 for fatal reference/input/output errors (no completed report). The other preparation CLIs fail loudly on invalid input.

See [grouped-comparisons.md](grouped-comparisons.md) for the corrected pilot/M3 recipe, 60-row versus 12-group distinction, and reusable validation reversal generation with complete-pair quality summaries.

## Baselines

Uniform is exactly 1/K, with deterministic first-option tie-breaking: its observed agreement is **not** random guessing's expected 1/K. The report gives expected random agreement separately.

Lexical is a deliberately weak, label-blind baseline: lowercase ASCII word-token sets, fixed stopword removal, cosine overlap of context+question with each option text, then softmax at temperature 1. No fitting or validation-label-derived priors. It does not understand negation, scope, numerical rules, or instructions. It is not a pretrained-model baseline.

## Isolation

Final data and all final outputs stay under `evaluation/final/`. The scorer, comparer, and input exporter require explicit `--allow-final` and enforce that output root for labeled final inputs. This flag is a procedural gate, not authorization to tune on final results. Freeze selected checkpoint/configuration before any release. There is no final scoring in this milestone.

Label-free files inherently lose split metadata; baseline generation cannot enforce final isolation on them. Do not export final inputs early or run baselines on a sealed final set. Never pass final labels, rationales, cases, or detailed failures to Data/Model during tuning. `passage_entailment` remains final-only. See final-design.md.

## Delegation

Three read-only subagents separately supplied metrics specification, validation-only adversarial cases/order analysis, and protected final curation. Follow-up metrics review identified fatal comparison exit-code ambiguity and prevalidation publication of curated shards; both were corrected. A separate validation analyst reviewed tiny model and simple-probe failure evidence without final access. That historical E1 delegation is complete. Current owners self-review/self-integrate owned changes under the shared merge lock; fresh bounded subagents use isolated task worktrees or read-only review and never share a mutable checkout. Teacher labels from these curators are not independently verified.
