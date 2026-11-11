# First actual training → save → fresh reload result

The earliest loop works; its model quality does not. These measurements use `data-tiny-v1`, six training rows and three teacher-labeled validation rows. All three validation groups are separate from training, but this sample is too small to establish generalization.

## Same-reference comparison

The Evaluation workstream's published `jeff.evaluation.compare` was executed, without modifying evaluation code, against fresh-process model predictions and its existing baseline files. All four runs have 3/3 valid predictions, no missing/invalid/duplicate/extra records.

| Model | Teacher agreement | Natural-log loss |
| --- | ---: | ---: |
| Uniform | 0/3 | 1.098612 |
| Lexical | 0/3 | 1.115433 |
| Pretrained MiniLM + random scalar head | 1/3 | 1.096828 |
| After six training steps | 0/3 | 1.103520 |

Uniform uses first-option tie-breaking, not stochastic sampling. The trained checkpoint is preserved as the first working reference, **not** selected as a quality improvement. No calibration claim follows from these results.

Full comparison: `${JEFF_ARTIFACTS_DIR}/model/tiny-20261111-01/comparison.json`. The reference is `${JEFF_ARTIFACTS_DIR}/data/data-tiny-v1/validation.jsonl`, SHA256 `6854d9e86516ba3af759fdd003c41b594fc0005e827860158cec8039e242d65e`.

## Actual learning and portability

- Apple M5, 24 GiB, MPS. Two epochs, batch size 2, six optimizer steps, 12 example presentations.
- 103 parameter tensors changed. Word-embedding L2 change: 0.0125173. Scalar head weight L2 change: 0.0296191.
- Elapsed training-run time 20.680 seconds, including model initialization/download and checkpoint saves. CPU high-water RSS 767,492,096 bytes. End-point MPS allocated 362,869,760 bytes and driver 1,178,599,424 bytes; not GPU peaks.
- Each checkpoint occupies approximately 88 MiB on disk and contains full encoder/tokenizer/head files.
- Baseline and trained inference each ran in a separate offline Python process with a separate empty Hugging Face cache. Each produced three predictions (0.350 / 0.231 seconds internal CLI time, excluding interpreter/import startup).
- `uv build --no-sources` produced a wheel and sdist. The wheel was installed with `uv pip install --no-deps` into a separate environment containing the approved dependencies. From an artifact directory outside the source checkout, offline CPU inference loaded the trained checkpoint and produced probabilities for two new development-only decisions, with two and four choices respectively (0.236 seconds internal CLI time).
- New-input files: `${JEFF_ARTIFACTS_DIR}/model/novel-inputs-20261111-01/inputs.jsonl` and `cpu-wheel-predictions.jsonl`. They have no assigned labels and are not quality evaluation data.

No training/inference/build command failed. A subagent encoder/backbone attribute mismatch was corrected before execution. Read-only source review found no material contract defect; it is not runtime evidence. No software tests or linters were run. Additional spend: £0 actual and £0 pending.

## Reproducibility and next bounded task

`tiny-run.json` records full paths, dataset hashes, initial dirty code identity and source hashes. The implementation was subsequently committed as `d56ee3e` without changing executed source. Exact successful commands and logs are in the public model handoffs. Model output paths are immutable; use a new ID to reproduce.

The first loop intentionally did not wait for the full pilot. Once Data publishes it, train a fresh initialization with `configs/model/minilm-pilot.json` settings, preserving its own random-head baseline and using the same validation inputs for before/after comparison. Do not train the pilot from this tiny checkpoint or concatenate tiny examples automatically. A pretrained relevance-head architecture comparison is a later separate hypothesis, not part of the first loop.
