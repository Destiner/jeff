# First actual baseline comparison

Reference: Data `data-tiny-v1` validation, SHA-256 `6854d9e86516ba3af759fdd003c41b594fc0005e827860158cec8039e242d65e`. Three examples, three groups, one per family, all teacher-labeled.

| Predictor | Valid / total | Teacher agreement | Log loss (nats) | Ties |
| --- | --- | --- | --- | --- |
| Uniform | 3/3 | 0/3 (0%) | 1.098612 | 3 |
| Lexical overlap | 3/3 | 0/3 (0%) | 1.115433 | 2 |

No missing, invalid, duplicate, extra, or unidentifiable predictions. Both predictors scored 0/1 within each family. Uniform loss is 1.098612 in each family; lexical loss is 1.149075 intent, 1.098612 sentiment, 1.098612 rule_application. Common-valid paired denominator: 3/3.

These are actual executions, not expectations. Uniform picks the first option on ties; none of these three references has a first-option target. Expected random-choice agreement is 1/3, but that is not the observed deterministic score. Lexical overlap is slightly worse on loss here. This tiny shard establishes the file boundary only; it provides no meaningful model-quality or calibration evidence.

Artifacts: `JEFF_ARTIFACTS_DIR/evaluation/tiny-v1-20261111T1030/`: label-free inputs, input receipt, baseline predictions/receipts, individual reports, comparison.json.

Executed: `python3 -m jeff.evaluation.prepare`, `baseline` (uniform, lexical), `score` (both), and `compare` with `PYTHONPATH=src` from the evaluation worktree, using the above shard and artifact directory. No trained/starting model predictions were available at this first milestone. Requested from Model, never loaded a competing model. Additional spend £0.
