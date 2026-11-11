# Repeatable grouped pilot comparison

E2 reuses the file scorer, comparer, and option-order analyzer. No model imports or new dependencies. All artifact paths below are relative to `JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts`.

## Reference and model identities

The frozen reference is `evaluation/data-pilot-v1/validation.jsonl`: 60 rows, 12 declared source groups (five intent, five sentiment, two rule groups). It preserves Data pilot-v1 labels and options. Original label-free input: `evaluation/pilot-baselines-v1/inputs.jsonl`.

Uniform/lexical predictions were frozen before pilot-trained predictions arrived. Use the matching **256-token random-head** baseline for M2 training gains; the 128-token comparison is secondary. M3's starting checkpoint retains its pretrained MS MARCO relevance head and must not be called a random-head baseline.

Original 128-token per-family files were concatenated without dropping/reordering prediction records for six-way comparison; decoded input equality against the pooled 60-row input was checked. Receipt: `evaluation/e2-256-v1/128-pooling-receipt.json`. File hashes and source provenance are recorded, not inferred from filename similarity.

## Group and paired metrics

`score` now includes `per_source_group` as well as per-family/basis/option-count metrics. `compare` additionally recomputes each pair of predictors on common-valid IDs within each family and source group. The denominator is the entire reference group, even when one predictor fails. Overall metrics remain micro-averaged across rows. No row-based significance intervals are presented as if groups were independent.

A group table is essential: ten intent/sentiment groups have four rows each, while the two rule groups have ten each. Group IDs are source reservations, not proof of statistical independence or semantic novelty.

## Order experiment

```sh
uv run --locked python -m jeff.evaluation.reverse \
  --examples "$JEFF_ARTIFACTS_DIR/evaluation/data-pilot-v1/validation.jsonl" \
  --dataset-id evaluation-pilot-order-v1 \
  --output-dir "$JEFF_ARTIFACTS_DIR/evaluation/<new-order-dataset-id>"
```

The executed frozen dataset is `evaluation/pilot-order-v1/`:
- `validation.jsonl`: 120 rows = 60 originals plus 60 exact reversed-option presentations.
- `reversed-inputs.jsonl`: only the 60 new label-free inputs requested from Model.
- `paired-inputs.jsonl`: all 120 label-free inputs for simple baseline generation.
- `pairs.json`: one pair per original example, with original source group preserved.
- `receipt.json` and `manifest.json`: immutable identities.

Only order and the reversed example's ID change. Options retain opaque IDs/text and the same target. Multiple pairs may share one source group; they are not treated as new independent groups. Model owns all inference. Combine a snapshot's original predictions with that **same** snapshot's reversed predictions once each before analyzing, recording both source hashes. A reversed-only file is incomplete, not a 60-pair success.

```sh
uv run --locked python -m jeff.evaluation.order \
  --examples "$JEFF_ARTIFACTS_DIR/evaluation/pilot-order-v1/validation.jsonl" \
  --pairs "$JEFF_ARTIFACTS_DIR/evaluation/pilot-order-v1/pairs.json" \
  --predictions "<matching-120-row-prediction-file>" --output "<new-order-report.json>"
```

Order reports retain each side's full coverage and provide `paired_quality` on complete pairs only, preventing comparisons of differently filtered samples. Complete-pair consistency, no-tie consistency, probability total variation, and success transitions appear overall, by family, and by source group. Exact ties can change the chosen option without any probability change; this is reported separately.

The separate `evaluation/probes-v1/` 24-row/12-group set stays validation-only. Its predictions can be scored directly; it already contains paired presentations. Do not transfer these cases or their variants into training. No final data are part of E2/M3.

## Actual evidence and review

Primary M2 six-way file comparison executed successfully at `evaluation/e2-256-v1/comparison.json`. Simple pilot order runs at `evaluation/e2-pilot-order-v1/` cover 120/120 rows and 60/60 pairs; original 128-token model-probe comparison/order runs at `evaluation/e2-probes-128-v1/` cover 24/24 rows. Model's M2/M3 order and probe requests are recorded directly in public Evaluation handoffs; no user relay or extra ML slot.

Separate read-only metrics review confirmed paired family/group denominators and multiple-pairs-per-group handling. It identified independent valid-subset summaries in the order output; `paired_quality` was added while retaining full coverage. Separate validation analysis found corrected M2 election regressions and sentiment weaknesses; no final content was provided.

No tests, linting, model loads, or paid calls by Evaluation.
