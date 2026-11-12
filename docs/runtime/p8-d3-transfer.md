# P8 — D3 transfer outputs delivered

One serialized original-P3 → M7 → M9 chain completed in **26.150528333 s**, with all five audit/predict phases exiting 0 and all process groups absent. E10 received outputs directly (`11327819-45cf-4233-9e84-2d1931a243dc`); Model received the slot return (`d4a47afc-1481-4a1a-9f84-3c3701690b3c`). **Model independently verified and closed P8; [E10 interpretation](../evaluation/e10-seen-mechanisms.md) is complete** (main `630aab0dfe22f107b147dee80db98e45a549ceb3`). Closure receipt: `artifacts/model/night-20261112/p8-return.json`, SHA-256 `0bfafb7860b8cfffe1c58972b5c00db397f035786d1f834283e9a2d17c728f69`. Evaluation found weak seen-mechanism transfer, not promotion; Runtime did not score labels.

## Coverage and execution

Each arm consumed the same 96 D3 inputs, SHA-256 `afd02eb196889f79384488fa1998dcb95c79d96dccd1235a70fd30940c2bf928`, and delivered 96 rows / 361 option probabilities. Decoder arms each attempted/completed 99 native forwards: three existing startup rows plus 96 D3 rows. M9 completed 96 decisions in 24 native classifier calls, with no startup. Total: **294 decision/startup presentations**. No retry, extra case, reversal or canary occurred; no exact saved matching outputs were known, and M4 outputs were not replayed.

Label-free coverage, IDs/options, finite ranges and normalization passed; maximum sum error was 1.1548399925e-7. The encoder's `d3-seen-rules96` suffix is wrapper metadata, not different data. D3 is seen-mechanism transfer, not IID or new-family evidence. All scoring outputs remain immutable.

Actual source: `7e4819210c8c98aea2eb0111ad7a389cec4dccfe`. New execution profiles retain the same backend and unchanged original configuration/scoring: existing decoder adapter and encoder scorer, native FP32/MPS without fallback. The original P3 config remains `configs/runtime/p3-qwen.json`; exact config/checkpoint/tokenizer/source bindings and producer-proof crosslinks remain in the frozen packet, audits and child receipts, not duplicated here or re-audited by loading weights.

## Resource observations

Grant `eaf3cd85-e002-4288-a58c-82ef66982551` allowed 600 aggregate seconds. Execution ran 2026-11-12 01:27:55.846507–01:28:21.979555 UTC. The aggregate wrapper charges all child imports, ML and both audits, but excludes post-hoc CPU output validation. Separate 8 GiB RSS/driver and ≥2 GiB recommended-headroom guards passed.

| Phase | Child lifetime RSS bytes | Native full-process max RSS bytes | Sampled max MPS driver bytes | Minimum sampled headroom bytes |
|---|---:|---:|---:|---:|
| P3 audit | 391872512 | 392183808 | — | — |
| P3 predict | 3352379392 | 3352379392 | 2768977920 | 16300687360 |
| M7 audit | 391151616 | 391528448 | — | — |
| M7 predict | 400883712 | 477216768 | 2777350144 | 16292315136 |
| M9 predict | 493813760 | 502317056 | 1099644928 | 17970020352 |

Native peak process footprints were 337838920 / 4160751704 / 337150840 / 3139978320 / 1426097256 bytes in the same phase order. CPU RSS, footprint and MPS scopes overlap: do not sum them. Child RSS precedes final serialization; the native wrapper covers the full process. MPS samples are not continuous peaks; driver includes current allocation. Recommended headroom is recommended MPS maximum minus driver, not physical free memory. No controlled speedup or cache-flush comparison was made.

## Evidence and next boundary

Root: `/Users/destiner/Code/jeff/artifacts/release/p8-d3-20261112-01/`. The [compact release manifest](../../manifests/releases/p8-d3-20261112-01.json) pins the packet, process receipt, actual child receipts and immutable outputs. `delivery-summary.json` retains coverage and phase counters; raw logs retain native resource observations.

Immediate handoff: `artifacts/handoffs/release/20261112T0129-P8-complete-slot-returned.md`. No Runtime ML remains. P9 is prepared, **not executed**, and requires Model's actual completed M10 handoff and scheduling; unused P8 budget grants nothing further. No other Model closure is implied; M9/P7 closure was already independently recorded in the P7 report.

Fresh HOME/cache and offline flags are not OS network denial, offline-installation proof, Linux execution evidence or publication rights. This reporting pass adds no source changes, ML/imports, tests/lint, network activity or spending (£0 actual/pending). Parent owns review, build, commit and integration.
