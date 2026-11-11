# First pilot comparison

The pilot arrived while the first-loop handoff was being finalized, so it was run immediately without another decision or a research gate. The tiny checkpoint remains preserved. No implementation changed between tiny and pilot runs.

## Dataset and run

- `data-pilot-v1`: 300 train, 60 validation; 100/20 rows per family. Train/validation use 60/12 effective source groups. No tiny data is included.
- Validation provenance: 40 teacher labels and 20 producer-rule-verified labels. Intent/sentiment results measure teacher agreement, not independently verified correctness. Rule labels carry Data's verification provenance; Model did not independently review each label.
- Start: fresh pretrained MiniLM and random head, not the tiny trained checkpoint. Same immutable revision and formatting.
- Clean executed commit: `3a737389c91ce950bff7c9d468681c2b7ac19279`.
- Three epochs, batch four, 225 steps / 900 presentations; backbone LR 2e-5, head LR 5e-4, seed 42, max length 128.
- Full provenance, immutable manifest hash, metrics and runtime: `pilot-run.json` and artifact `model/pilot-20261111-01/run.json`.

## Fresh-process comparison

Evaluation's existing exporter produced decision-only inputs per family. Each baseline and trained inference ran in a separate offline MPS process. Evaluation's unchanged baseline/comparison CLIs then scored the saved probabilities, with the same reference rows for every model.

| Run | Reference-label agreement, n=60 | Mean log loss |
| --- | ---: | ---: |
| Uniform, first-option ties | 17/60 (28.3%) | 1.378765 |
| Lexical | 29/60 (48.3%) | 1.323710 |
| Pretrained encoder + random head | 19/60 (31.7%) | 1.378223 |
| Trained pilot | **36/60 (60.0%)** | **0.843401** |

All runs have 60/60 coverage and zero prediction failures. Overall agreement mixes label bases and must not be presented as wholly verified accuracy.

| Family | Effective validation groups | Initial → trained | Initial → trained log loss |
| --- | ---: | ---: | ---: |
| Intent, teacher agreement | 5 | 6/20 → 20/20 | 1.373597 → 0.067838 |
| Sentiment, teacher agreement | 5 | 6/20 → 11/20 | 1.382234 → 1.066197 |
| Rule application, rule-label accuracy | 2 | **7/20 → 5/20** | **1.378838 → 1.396167** |

The overall improvement is not uniform: rule performance deteriorated. Validation is small and grouped, and no final data was examined. No calibrated-confidence or broad generalization claim.

## Important truncation finding

A post-run audit using Research's unchanged tokenizer audit script found 45/1,412 candidate pairs exceeded 128 tokens. **All 45 were rule-validation pairs, and question tokens were truncated in each; candidate text was intact.** Full pair length ranged from 41 to 169 tokens. At 256 tokens, none would truncate.

This qualifies the rule result: it is not a clean measure of rule comprehension with complete inputs. No training pairs were truncated. A natural next controlled comparison is a 256-token cap or question-preserving state budgeting, maintaining the current result/checkpoint as the reference. That follow-up was not part of the initial task. The subsequently authorized LD002 repeat is recorded separately in `pilot-256-results.md`; the original run/artifacts remain unchanged.

Audit artifact: `model/pilot-20261111-01/token-budget.json`.

## Runtime and artifacts

Apple M5, 24 GiB, MPS, no CPU fallback. The run took 20.481 seconds including checkpoint saves, with cached base downloads. CPU lifetime high-water RSS: 1,074,069,504 bytes. End-point MPS current/driver allocations: 366,998,528 / 2,256,502,784 bytes, not GPU peaks. 103 named parameter tensors changed; representative word embeddings/head weight L2 deltas were 0.312480 / 0.380187.

Under `JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts`:

- Checkpoint: `model/pilot-20261111-01/checkpoint`; initial baseline: sibling `baseline`.
- Each of `model/pilot-validation-20261111-01/{intent,sentiment-r2,rule_application}/` contains `inputs.jsonl`, exporter receipt, `baseline-predictions.jsonl`, `checkpoint-predictions.jsonl`, uniform/lexical predictions, and `comparison.json`.
- Optional 24-row validation probes were also predicted with the pilot baseline and trained checkpoint: `model/pilot-probes-20261111-01/{baseline,checkpoint}-predictions.jsonl`. Evaluation owns probe labels, scoring and order analysis; Model inspected only label-free inputs.
- Exact commands are in `handoffs/model/20261111-1040-pilot-complete.md`.

No failed training/inference/build invocation; no software tests/linting. Additional spend remains £0 actual / £0 pending. All jobs finished.
