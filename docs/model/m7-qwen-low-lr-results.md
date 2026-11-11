# M7: lower-LR TRAIN-fit results

M7 completed its **one authorized full training attempt** on 2026-11-11 at 17:11:09.986592 UTC: 1,500 training presentations, 375 AdamW updates, no extra backwards, wrapper exit 0 and no timeout. Aggregate deterministic TRAIN agreement improved from 805 to 1,130/1,500 and CE from 1.357724 to 0.530299. Intent and sentiment improved; rule agreement regressed and 472/500 final rule predictions selected input position 0.

**This is TRAIN fitting, not an end-to-end learning or held-out transfer claim.** Runtime P5 completed the one fresh-process 624-presentation reload/inference pass; Evaluation E7's independent held-out comparison remains pending in this report. No promotion, retry or default change follows from successful execution or these TRAIN results.

## Controlled execution

The [pre-execution plan](m7-qwen-low-lr-plan.md) and its immutable freeze pins remain unchanged. Execution source was clean `574774d631d707de9398c80dc5b936d9563e386c`. M7 reset to original P3 `Qwen/Qwen2.5-0.5B-Instruct@7ae557604adf67be50417f59c2c2f167def9a775`, not trained M6, with fresh seed-42 Python/CPU/MPS RNG and a new empty optimizer. The only treatment was AdamW LR **2e-5 → 2e-6**; the contingent correctness-repair branch was not selected.

The exact M6 materialized row/option schedule, targets and released TRAIN data were reused: schedule SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`. One epoch, microbatch 1 / accumulation 4, full-parameter FP32 MPS/SDPA, four threads, original P3 rendering and conditional-symbol readout, temperature 1, cap 1024 without truncation, no cache, last-token projection and all other optimizer settings stayed fixed. See the plan for exact config, control, capacity and E7 pins.

Frozen START outputs and historical capacity evidence were reused, not freshly rerun. There were zero new START forwards and no new capacity probe/update. Source/config equivalence is not a fresh numerical baseline or cryptographic installed-binary equivalence. Both existing deterministic TRAIN-fit passes still ran; saving their full vectors and the 375 already-computed preclip gradient norms was observation-only, with no extra forwards, norm calculations or weight scans.

## Fixed-schedule TRAIN fit

Agreement is against released training targets, not a blanket independently verified correctness claim. CE is mean cross-entropy over allowed answer symbols. All family and source-unit detail remains in the completed receipt.

| TRAIN subset | Rows | Agreement before → after | CE before → after |
| --- | ---: | ---: | ---: |
| All | 1,500 | 805 → 1,130 | 1.357724 → 0.530299 |
| Intent | 500 | 442 → 496 | 0.396153 → 0.029681 |
| Sentiment | 500 | 179 → 458 | 2.019892 → 0.297916 |
| Rule application | 500 | 184 → 176 | 1.657126 → 1.263300 |

A CPU-only read of all 1,500 saved rows in each fit file checked the actual allowed logits and conditional probability vectors: **zero exact maximum ties in either representation, before or after**. Thus these particular saved TRAIN argmaxes are unique, including the final rule position-0 selections; this does not establish both-order correctness, order robustness or strictness on unseen predictions. Logit and probability top sets remain separate definitions because rounding can distinguish them. No model was loaded for this check.

Rule position-0 selection rose from 168 to 472/500; only 154/500 rule targets are at position 0. Lower rule CE alongside worse agreement is not rule-learning success. Aggregate gains cannot erase that failure. Online training mean CE was 0.877500, measured along changing weights, not a substitute for either deterministic fit.

M6 historically saved scalar TRAIN CE/argmax but not full TRAIN vectors. Those missing vectors have not been reconstructed; M7 observations cannot retrospectively establish M6 TRAIN ties or flatness. M6's held-out P4/E6 evidence is separate. The source/path root cause of the M6 failure remains unknown; this lower-LR contrast does not prove a causal diagnosis.

## Timing and resource scope

Wrapper wall time was **738.520718 s** (16:58:51.463597–17:11:09.986592 UTC); receipt process runtime was **737.408516 s**. These are different scopes. The whole-process cap was 2,700 s, with external supervisor TERM at 2,690 s / KILL at 2,700 s. Cooperative guards surround phase calls and row completion; they cannot interrupt a stuck call. Recorded maximum durations below are actual individual phase calls, not phase totals or separately configured per-call deadlines.

| Phase | Calls | Total seconds | Maximum call seconds |
| --- | ---: | ---: | ---: |
| Revalidation | 1 | 2.656 | 2.656 |
| Load | 1 | 0.616 | 0.616 |
| TRAIN fit before forward | 1,500 | 83.958 | 0.244 |
| Train forward | 1,500 | 108.959 | 0.291 |
| Train backward | 1,500 | 278.966 | 0.349 |
| Clip | 375 | 19.870 | 0.176 |
| Optimizer step | 375 | 120.379 | 0.851 |
| TRAIN fit after forward | 1,500 | 114.583 | 0.237 |
| Save checkpoint | 1 | 2.713 | 2.713 |

CPU lifetime high-water RSS was 3,380,641,792 bytes. Maximum sampled MPS current allocation was 8,740,772,096 bytes; maximum sampled MPS driver allocation was 11,861,164,032 bytes. Minimum sampled recommended-working-set headroom was 7,208,501,248 bytes. MPS samples are **not peaks**. CPU lifetime RSS and MPS allocations are overlapping, nonadditive scopes: never sum them as total memory. The run retained separate 16 GiB CPU-RSS / MPS-driver limits and at least 2 GiB recommended headroom; samples and phase guard records do not guarantee unsampled peaks. Process metadata, sampling stages and exact timings are retained in the evidence index and source artifacts. Additional actual/pending spend: £0.

## Saved checkpoint and next evidence

Artifact root: `/Users/destiner/Code/jeff/artifacts/model/m7-qwen-low-lr-20261111-01/`.

| Evidence | Relative path | SHA256 |
| --- | --- | --- |
| Completed receipt | `training/receipt.json` | `c78ad96769b76c2cabb7c2b0ec87dde13bca78e2f7e2256a51b6ca545b54e156` |
| Checkpoint binding | `training/checkpoint-manifest.json` | `70163c8567781bb7151b11c125999ea4bc6ec1ff52af52c52a205f9f4dbdd022` |
| TRAIN before vectors | `training/fit-before.jsonl` | `4940b17902562c8da5cf34e80eaa3618fa5ab52c20ad90715fd6dc6d3c9d12d5` |
| TRAIN after vectors | `training/fit-after.jsonl` | `0dbaf4f403b1128bf3c75b8a174a0ac9d2b93220cd43a58a1bcae0da1d1b620a` |
| Preclip norms | `training/gradient-norms.jsonl` | `f88584d96ad8179377230c6f2fb5c83f0a389688c4a81f4fd9e316b56c7c542d` |

The final safe FP32 HF checkpoint is `training/checkpoint/`, with original four tokenizer assets byte-copied and the unchanged `jeff.qwen-trained-checkpoint.v1` sibling manifest. Receipt parameter fingerprints changed and Adam state reached step 375. File identities in the manifest are producer evidence; this docs-only review did not rehash the approximately 2 GB weights or load/decode any model/tokenizer. The initial `failure-receipt.json` is a fail-closed placeholder (zero presentations), explicitly superseded by the completed receipt; it is not another training attempt.

A separate fresh CPU-only artifact reviewer approved 52 checks and 56 streaming hash pins, including all nine checkpoint files, all 3,000 fit vectors, all 1,500 online rows and all 375 preclip norms. All shared M6 starting-fit fields match exactly across 1,500 rows. Norms range 0.013807–3581.529785; 362/375 exceed clip 1. These are preclip observations, not postclip measurements or proof of native-kernel gradients. See artifact `review.md` / `review.json`.

P5 completed exactly one offline fresh-process 300 original + 300 reversed + 24 already-paired pass, with three separate fixed startup rows, at 17:18:29.486849–17:19:08.558254 UTC: exit 0, external 39.071046 s, 624 predictions / 2,390 probabilities. Model checked the published output hashes, unique IDs/counts and successful receipts and confirmed wrapper/child 22652/22653 absent. The bounded grant is closed; there was no duplicate inference. Artifact `p5-return.json` (SHA256 `30b4f58e8bcdfba45a3a4f0c1912ef8668a34edb722f4d111c75859a5697b963`) links the three outputs and actual process receipt under `artifacts/release/p5-m7-20261111-01/`; Runtime owns its fuller reload/resource evidence.

See the [machine-readable run index](m7-qwen-low-lr-run.json). E7 must compare original P3 first, failed M6 separately, and retained encoders on the frozen units, proper scores, ties/stability, rule both-order success and family/source retention. Beating failed M6 alone is insufficient. No new cases, protected final access, calibration/significance claim or automatic promotion is authorized here.
