# R6 frozen-P3 diagnostic execution

Runtime completed Research's frozen diagnostic once, using original P3, **not M6-trained weights**. This records execution, identity and coverage only; Research analysis and independent predictions delivery (`da549dd3`) remain separate from P4/E6. Frozen packet main commit: `deb9c5b`. No shared Runtime code or Research runner was changed.

## Result and bounds

- 48 preselected TRAIN cases × four fixed conditions (O0L0, O0L1, O1L0, O1L1): **192 attempted = completed = written**, 48 per condition, 740 option probabilities. First forward retained exactly once; zero extra/startup/retry forwards.
- Tokenizer-only source audit passed all 192 custom-letter boundary/full-prompt checks, 95–199 tokens against cap 1024; audit performed zero forwards. Predict verified original P3 weight identity once. Output validation checked identity, coverage, finite scores and normalization only (maximum sum error `1.3702083379030228e-7`). Audit and predict passed, both exit 0, no timeout.
- Model grant `ab6fcab8-bd4d-4105-9883-4187ab2629b9`, start-by 2026-11-11 16:25 UTC, consumed once and returned. Predict actual UTC: **16:22:50.929631–16:23:03.909725**. Completion handoff confirms wrapper/child 93634/93635 exited and no Runtime ML process remains; £0 actual/pending.
- External audit wall `0.8880471671000123 s`; predict `12.979705292265862 s`; combined `13.867752459365875 s ≤ 300 s`. Queue wait is excluded. Predict received only `299.1119528329 s`, SIGTERM at `294.1119528329 s`, hard-kill deadline at remaining budget; termination grace is inside the shared external budget. Runner's own cooperative bound is additional, not a substitute.
- CPU process-lifetime maximum RSS **3,357,491,200 B**; observed MPS driver maximum **2,768,977,920 B**. Separate cooperative 8 GiB (`8589934592 B`) bounds; measurements are nonadditive and do not establish system/unified-memory or MPS peak usage.

## Identity and evidence

All artifact paths resolve under `/Users/destiner/Code/jeff/artifacts/`. The [small manifest](../../manifests/releases/r6-order-20261111-01.json) preserves exact source/packet/asset/output SHA256 pins, environment and process records.

- Evidence root: `release/r6-order-20261111-01/`.
- Compact facts: `completion-summary.json`, `output-validation.json`.
- Source audit and inference receipt: `audit/audit.json`, `run/receipt.json`.
- Outputs: `run/predictions.jsonl`, SHA256 `c9068e41915629f9419066941124c74fd7f181e93c840ca05e807d9e0056494d`.
- Receipt SHA256: `9c0e1e530bd88d0ce08f55fc26c82efdbc83dca50c20efd8748979d0d1799c7a`.
- Audit SHA256: `ddd09457f96777b9ee611601fa3bd0fb6e3bafd7dec07a3fc44740fa7e3a2d23`.
- External supervision: `launch.py`, `audit-invocation.json`, `predict-invocation.json`, `audit-process.json`, `predict-process.json`, `predict.stderr.log`.
- Exact completion handoff: `handoffs/release/20261111T1624-R6-complete-slot-returned.md`.
- Packaging-only verification: `uv build --no-sources`; log `release/r6-order-20261111-01/report-build.log`. No tests, lint or model rerun.

Unmodified Research runner `experiments/research/run_order_packet.py` SHA256: `1f3bb7bb6d652121813692db5899c434ddaba9feed9fdbfb26ade26c5a6e8599`. Packet: `research/r6-20261111T155310Z/packet-v1/`, packet.json SHA256 `7598451302c5389e62476c88e7c2489fa355e0c40611e91cfbd6da1d9dc35e03`.

Original model: `Qwen/Qwen2.5-0.5B-Instruct`, revision `7ae557604adf67be50417f59c2c2f167def9a775`, local assets `release/p3-qwen-20261111-01/download/model`. FP32/MPS/SDPA, batch 1, four threads, cache off, logits_to_keep 1; T=1 conditional softmax over allowed single-token letters, not calibrated confidence. Receipt preserves full token bindings and asset hashes.

## Limits

Fresh HOME/HF cache and local-only/offline flags are not OS network denial. Recorded load `0.5167036661878228 s` and first-forward `0.09682999970391393 s` are not cold-storage or comparative speed evidence. This task did not install dependencies, scan weights, access TRAIN source or reference/final/probe content, change defaults, assess quality/causes, or authorize another attempt. Packaging success is not inference portability evidence. Research analysis may proceed independently; parent reviews/integrates this report.
