# LD002: controlled 256-token pilot

One fresh repeat of `pilot-20261111-01`, changing only `--max-length 128` to `--max-length 256` (and the necessarily unique output directory). All prior artifacts remain untouched. No architecture, source code, dataset, optimizer, seed, epoch, batch-size, learning-rate, thread-count or device changes.

## Controls and reconstruction

- Dataset: `data-pilot-v1`, 300 train / 60 validation; manifest SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`.
- Base/tokenizer: `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- Seed 42, three epochs, batch four, backbone/head learning rates 2e-5 / 5e-4, four threads, MPS. Full fine-tuning, 225 steps / 900 presentations.
- Executed clean source revision `2f85624`; model/trainer source hashes equal the original run. New and original initial parameter hashes are identical.
- Evaluation's pooled `evaluation/pilot-baselines-v1/inputs.jsonl` was checked against concatenation of the three original family input files: all 60 decoded rows are identical in content **and order**. Input hashes are in `pilot-256-run.json`.
- New matching pre-training baseline and trained checkpoint saved, each reconstructed in a separate offline process. Both produced 60 predictions.
- Trained parameter hashes are not bitwise identical between repetitions; MPS determinism was never guaranteed. The saved audit reports tensor differences (encoder maximum absolute difference 0.000307; head 0.004997). Therefore this is a fixed-configuration comparison, not a promise that the cap was the sole bitwise difference in resulting weights.

## Primary comparison: matching 256-token baseline and trained model

Evaluation's unchanged file-based comparer ran on the saved fresh-process outputs. All rows were covered; zero missing/invalid/duplicate/extra predictions.

| Run | Reference-label agreement, n=60 | Mean log loss |
| --- | ---: | ---: |
| Uniform, first-option ties | 17/60 (28.3%) | 1.378765 |
| Lexical | 29/60 (48.3%) | 1.323710 |
| **256-token pretrained encoder + random head** | **20/60 (33.3%)** | **1.378267** |
| **256-token trained model** | **35/60 (58.3%)** | **0.855288** |

The overall metric mixes 40 teacher labels and 20 rule-verified labels. It is not wholly independently verified accuracy.

| Family / provenance | Validation rows / source groups | 256 baseline → trained | Log loss, baseline → trained |
| --- | ---: | ---: | ---: |
| Intent / teacher agreement | 20 / 5 | 6/20 → 20/20 | 1.373597 → 0.067838 |
| Sentiment / teacher agreement | 20 / 5 | 6/20 → 11/20 | 1.382234 → 1.066200 |
| Rule application / Data's rule-verified labels | 20 / 2 | **8/20 → 4/20** | **1.378970 → 1.431825** |

## Secondary comparison with preserved 128-token run

| Matching pair | Baseline agreement → trained | Baseline loss → trained |
| --- | ---: | ---: |
| 128 tokens | 19/60 → 36/60 | 1.378223 → 0.843401 |
| 256 tokens | 20/60 → 35/60 | 1.378267 → 0.855288 |

Intent and sentiment trained top choices remain 20/20 and 11/20. Rules change from 5/20 to 4/20. Do **not** use the old 128-token baseline as the primary baseline for new trained outputs.

The new tokenizer audit confirms zero over-budget or question/candidate-loss pairs at 256 across all 360 decisions / 1,412 pairs. At 128, the preserved finding is 45 question-loss pairs affecting 12 rule-validation decisions. No training pair exceeded 128; maximum complete pair length is 169.

**Conclusion:** the correction removes observed input loss but does not demonstrate improved rule performance. Rule failure cannot be explained away solely by question truncation. The validation set is small and clustered in just two rule mechanisms; this one-seed comparison is not a broad architecture or significance result. No calibrated-confidence claim and no final evaluation.

## Artifacts and runtime

Under `/Users/destiner/Code/jeff/artifacts`:

- `model/pilot-256-20261111-01/{baseline,checkpoint}/`: full self-contained snapshots.
- `model/pilot-256-20261111-01/{run.json,summary.json,token-budget.json}`: exact config, provenance, input/control identities, learning/runtime evidence, tokenizer audit.
- `model/pilot-256-validation-20261111-01/{baseline-predictions.jsonl,checkpoint-predictions.jsonl,comparison.json}`: Evaluation-ready outputs and Model-executed comparison.
- `handoffs/model/20261111-m2-256-complete.md`: exact successful commands and final branch/commit.

Apple M5 / 24 GiB, MPS; elapsed training 19.303 seconds including saves, cached base. CPU lifetime high-water RSS 1,148,125,184 bytes. End-point MPS allocated/driver memory 370,078,720 / 2,256,502,784 bytes, not GPU peaks. Baseline/trained fresh-process inference CLI times: 0.497 / 0.476 seconds, excluding interpreter/import startup.

103 named parameter tensors changed during training; representative embedding/head weight L2 deltas 0.312480 / 0.380187. No training, inference, audit, evaluation or build command failed. No software tests or linting. £0 actual / £0 pending spend; all jobs ended. No further model run is included in this task.
