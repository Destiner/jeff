# Actual comparisons and limitations

All values below come from frozen prediction files scored independently of Training. Full reports include SHA-256 references, per-family/basis/option-count results, coverage/failures, individual outcomes, Brier scores, descriptive confidence bins, and paired common-valid comparisons. No evaluator loaded a model.

## Tiny starting versus trained

Data `data-tiny-v1`: 3 validation examples, 3 groups, teacher labels. Same label-free inputs for four predictors, full 3/3 coverage and no prediction failures/extras.

| Predictor | Teacher agreement | Log loss (nats) |
| --- | --- | --- |
| Uniform (first-option tie-break) | 0/3 | 1.098612 |
| Lexical | 0/3 | 1.115433 |
| Pretrained MiniLM + random scalar head | 1/3 | 1.096828 |
| Tiny-trained MiniLM | 0/3 | 1.103520 |

Per-family teacher agreement, starting → trained: intent 1/1 → 0/1; sentiment 0/1 → 0/1; rule_application 0/1 → 0/1. Log loss: intent 1.073444 → 1.083977; sentiment 1.098981 → 1.106603; rule_application 1.118058 → 1.119979. Target probability declined on all three. The intent answer changed from appointment rescheduling to additional booking with a tiny winning margin (~0.000254). These are valid-output disagreements, not software/inference failures.

Tiny training did not improve validation. This is plumbing evidence, not an estimate of useful quality. The starting head is random, not a pretrained task head. Model's run record identifies full-finetuning of `sentence-transformers/all-MiniLM-L6-v2`, revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, trained on six examples. Fresh reload is Model's executed evidence; Evaluation reproduced only scoring of returned files.

Report: `evaluation/tiny-trained-comparison-v1/comparison.json`. Model predictions/checkpoints: `model/tiny-20261111-01/`.

## Full pilot simple baselines (before pilot-trained predictions)

Data `data-pilot-v1`: 60 validation examples, 12 groups. Evaluation verified all three validation shard SHA-256s, row counts, and split membership against the published manifest, preserving IDs/options/labels while serializing one reference file. Training shards were not read by assembly. Data's separate validation report owns cross-split/group/duplicate checks.

Mixed labels: 40 teacher, 20 `rule_verified` per Data provenance. Report the aggregate as **reference-label agreement**, not pure teacher agreement or independently verified overall accuracy. Evaluation has not independently recomputed the rule labels.

| Predictor | Valid / total | Reference-label agreement | Log loss |
| --- | --- | --- | --- |
| Uniform | 60/60 | 17/60 (28.33%) | 1.378765 |
| Lexical | 60/60 | 29/60 (48.33%) | 1.323710 |

| Family / label basis | Uniform agreement | Lexical agreement | Uniform loss | Lexical loss |
| --- | --- | --- | --- | --- |
| Intent / teacher | 6/20 | 16/20 | 1.370160 | 1.216725 |
| Sentiment / teacher | 5/20 | 5/20 | 1.386294 | 1.380693 |
| Rule application / rule_verified | 6/20 | 8/20 | 1.379841 | 1.373712 |

No invalid/missing/duplicate/extra/unidentifiable predictions. Common-valid pair 60/60. Lexical wins by 12/60 (20 percentage points) and 0.055055 nats in mean log loss; this is a simple baseline comparison, not a training improvement.

Most rows are correlated within only 12 groups; rule validation has two mechanisms. Do not interpret row count as 60 independent tasks or claim calibration from five sparse confidence bins. Teacher labels and synthetic/template coverage remain material limitations.

Reference: `evaluation/data-pilot-v1/validation.jsonl`, manifest and assembly receipt beside it. Baselines/report/label-free inputs: `evaluation/pilot-baselines-v1/`. Requested Model's preserved starting and trained pilot predictions on that exact `inputs.jsonl`; none are claimed here. This is a prepared next experiment, not a blocker to the completed tiny-model comparison.

## Adversarial validation and final boundary

See [validation-probes.md](validation-probes.md) for actual baseline/model comparisons on 12 source groups / 24 presentations. Both tiny model snapshots achieve only 2/24 teacher agreement, versus uniform 8/24 and lexical 9/24; choice order consistency does not rescue correctness.

The separately curated 24-group final set remains sealed and unscored. `passage_entailment` has not been used for training, validation probes, or iterative repair. See [final-design.md](final-design.md). No final result is claimed.

All runs use local CPU scoring. Additional spend £0; no paid inference, software tests, or linting by Evaluation.
