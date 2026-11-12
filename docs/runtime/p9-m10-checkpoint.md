# P9 — M10 checkpoint reload

P9 completed one actual fresh-process M10 checkpoint prediction on FP32/MPS with the unchanged P3 scorer: **624 presentations, 2,390 option probabilities, exactly 627 attempted/completed forwards** (3 existing startup forwards + 624 decisions). Runtime validated coverage, IDs, options, order and normalization without labels. This is execution evidence, not quality, speedup, true-learning evidence or promotion.

## Actual source and delivery

The executed source is `120bc288d3e955d9753053f5c95bca62c53e7d60`, in isolated `.worktrees/release-p9`, not this documentation revision. The checkpoint is `artifacts/model/m10-qwen-seed7-20261112-02/training/checkpoint`; its checkpoint manifest and the immutable execution packet bind the actual bytes. The corrected interpreter was the already-provisioned `/Users/destiner/Code/jeff/.worktrees/release/.venv/bin/python`. No dependency installation, scoring/config/data/precision change, canary, fallback, extra ordering or retry after a model outcome occurred.

Outputs were delivered directly before documentation to Model (`6b37439b-6910-4de9-bac6-8485eb30422e`), Evaluation (`1bb8ac84-6a80-40ea-bdc6-dd0b0e8494fd`) and Lead (`420cb9c5-6e70-4773-8beb-a7221760291e`). These are delivery messages, not recipient acceptance receipts. The [compact manifest](../../manifests/releases/p9-m10-20261112-02.json) pins full SHA-256 evidence and output paths; artifacts remain under the repository root, outside this worktree.

| Successful `-02/run/` output | Rows | Probabilities |
| --- | ---: | ---: |
| `v2-original.jsonl` | 300 | 1,160 |
| `v2-reversed.jsonl` | 300 | 1,160 |
| `probes-paired.jsonl` | 24 | 70 |

## Failed attempt and explicit renewal

`artifacts/release/p9-m10-20261112-01` is a separate failed, zero-output attempt. Its launcher selected root `.venv/bin/python`, the lightweight coordination interpreter, and audit failed with `ModuleNotFoundError: No module named 'transformers'` before ML/tokenizer/weight loading: zero loads and forwards. The supervisor receipt ended at 0.8023657081648707 seconds, but the outer loop waited through its watchdog: **the full 309.808853250 seconds remains charged**, not merely 0.802 seconds. Original errors and receipts remain unchanged, including the misleading outer `slot_returnable: false`; separate closure records establish actual absence.

Lead `84dfaa52-7b76-4db5-88ed-0fcc083cbc6c` explicitly authorized a minimal interpreter/early-failure-closure repair and an additional 310 seconds, total allowance **≤619.808853250 seconds**. Model `c0cba4dc-a8a5-46c3-910f-b7150fc65262` activated the repaired immutable `-02` packet after prior-group absence. This was not reuse of the original allowance or authority for a second actual prediction.

## Timing and resource return

Successful `-02` audit and predict exited 0; phase walls were 3.3755382923409343 and 36.65089841699228 seconds. The supervisor recorded 40.748247750103474 seconds. The **final watchdog observation was 40.75646716589108 seconds**; rounding that observation conservatively upward gives a **41-second operational charge**. It is not an externally measured full post-exit wall interval. Combined charge is **350.808853250 seconds**, including the entire failed attempt, within the renewed allowance.

Both attempts' started groups were gone on owner recheck: `-01` supervisor/audit groups 83588/83589 and watchdog PID 83587; `-02` supervisor/audit/predict groups 92334/92339/92374 and watchdog PID 92333. Runtime returned the slot directly. Model independently confirmed failed-01 closure in `artifacts/model/night-20261112/p9-failed-return.json`. Model's actual successful-02 receipt arrived during documentation: `artifacts/model/m10-qwen-seed7-20261112-02/p9-return.json`, checked at `2026-11-12T03:15:26.315942+00:00`, records independent label-free verification and no active groups. `artifacts/model/night-20261112/p9-m11-closure.json` binds that return and actual phase completion paths. Both are pinned in the manifest.

## Resource and STDERR qualifications

`/usr/bin/time -l` recorded audit 3.32 real / 2.17 user / 0.35 sys seconds and 395,771,904-byte maximum RSS; predict 36.60 real / 5.08 user / 0.90 sys seconds and 553,697,280-byte maximum RSS. The prediction receipt observed MPS current allocation up to 2,013,552,384 bytes, driver allocation up to 2,768,977,920 bytes and minimum recommended headroom 16,300,687,360 bytes. CPU RSS and MPS observations overlap and must not be added; sampled MPS maxima are **not peak memory** or proof of an unsampled bound. CPU process-lifetime RSS is a different measurement from sampled allocator observations.

Both successful STDERR logs retain the tokenizer incorrect-regex warning; prediction also retains the `torch_dtype` deprecation warning. No tokenizer flag or scoring repair was silently applied. These warnings qualify the unchanged execution and remain available with the receipts, not suppressed as clean STDERR.

## Interpretation boundary

E11 independent interpretation remains pending an actual Evaluation delivery message at this documentation snapshot; existing analysis artifacts alone are not a delivery receipt. Runtime did not score them or access protected final material. Model's independent successful-run closure is now available in the actual receipts above; it is not quality scoring. No M10 TRAIN statistics are used here to infer true learning. This documentation-only change ran no tests, lint, builds, ML, dependency imports, weights, network or mailbox operations.
