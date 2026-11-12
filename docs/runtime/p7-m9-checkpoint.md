# P7 — M9 retained-encoder reload completed

**One fresh existing-scorer process delivered 624/624 development predictions and exactly 2,390 valid option probabilities in 4.098479833 seconds.** All 156 batches were attempted and completed, with zero startup rows, warmups or canaries. There was no inference retry, fallback or extra pass.

Outputs went directly to E9 (`2cbf2b01-21ed-470f-9cd8-4ff7f64fa474`); Model received the slot return (`762f0bc0-3db2-4e2c-bb36-d1f10b2223f8`). The immediate handoff is `artifacts/handoffs/release/20261111T2318-P7-predictions-ready-slot-returned.md`. **Model independently verified closure; E9 is complete:** [independent duration report](../evaluation/e9-encoder-duration.md), main `1dde6fd`. Closure is recorded in `artifacts/model/m9-msmarco-duration-20261111-01/p7-return.json` (SHA-256 `651f85c614610f2a662b6ae2ab9f74cf26de13e9ba0155062b044c38738bdb2c`) and message `dd56a650-7816-45c9-8eb3-1e6e721f2561`. E9 owns held-out conclusions; Runtime success does not promote this checkpoint.

## Execution and scope

The frozen artifact-only `predict.py`, `launch.py` and `verify_outputs.py` orchestrated existing code at `b072c8ba7a4e411b73d9efa8a9062793f016545c`. Existing `load_checkpoint` ran once; `_rows` and `_write_batch` handled three separate suites (300 original, 300 reversed, 24 already-paired probes), preserving the same frozen 624 inputs. Probes were not reversed again. Batch size was four, with four threads, FP32/MPS, token cap 256 and temperature 1. There is **no additional tracked Runtime implementation, new loader, backend or checkpoint contract for P7**.

| Measurement | Recorded result |
|---|---:|
| Process UTC, 2026-11-11 | 23:17:40.638389–23:17:44.737118 |
| External monotonic wall / exit | 4.098479833 s / 0; whole process group absent |
| Existing loader / three suites | 0.085287458 s / 2.210699418 s |
| Decisions / batches completed | 624 / 156 |
| Maximum probability-sum error | 1.2631062418222427e-7 |
| Internal lifetime CPU RSS observation | 499,187,712 bytes |
| Native full-process maximum RSS | 509,313,024 bytes |
| Native peak process footprint | 1,439,695,976 bytes |
| Maximum sampled MPS driver allocation | 1,108,017,152 bytes |
| Minimum sampled recommended MPS headroom | 17,961,648,128 bytes |

Separate 8 GiB RSS/driver guards and a ≥2 GiB recommended MPS headroom floor applied. The external bound was 120 seconds within the remaining M9 aggregate, targeting TERM at 110 seconds and group KILL by 119 seconds. These are OS scheduling targets, not real-time guarantees. The external clock includes imports, verification, loading, scoring and publication; suite timings include input/output work, not just forwards.

Memory scopes overlap and must not be summed. Internal RSS precedes final receipt serialization; the native wrapper covers the full process. MPS observations are samples, not true peaks or continuous monitoring. Recommended headroom is recommended MPS maximum minus sampled driver allocation, not system free memory. No controlled speedup comparison or cache flush was performed.

## Missed window and budget

The original 23:12 UTC start deadline expired **before the first preparation assertion, binding, supervisor or ML process**. `preflight-unstarted.json` preserves that not-started outcome, observed at 23:13:33.328913 UTC. This was an operational miss, not failed inference or a retry; it must not be hidden by the later success.

Model renewed the **same unconsumed** reservation `c00b7ab7-78f1-484d-a4fe-e6e05a099f86` through `9d8031ae-5960-4daa-add3-a48c8c9bee9d`, with start by 23:30 and end by 23:32 UTC. Endpoint activation was `112718ad-c5ec-4ea1-999f-ac1f53415656`. Source and aggregate budget were unchanged. Model's prior process wall was 311.959970375 seconds; adding P7 gives **316.058450208 seconds**, leaving **883.941549792 seconds** of 1,200. That remainder is not permission for extra work. No further Runtime ML is queued.

## Immutable artifacts and provenance

Root: `/Users/destiner/Code/jeff/artifacts/release/p7-m9-20261111-01/`. The [compact release manifest](../../manifests/releases/p7-m9-20261111-01.json) records exact file sizes and hashes, suite input pins, frozen sources and the seven-file checkpoint inventory. Checkpoint: `artifacts/model/m9-msmarco-duration-20261111-01/training/checkpoint/`.

| Artifact | SHA-256 |
|---|---|
| `binding.json` | `a49a0934ea45febea4817a1a602ca6391d608bfe518d6a39ae0125ab48224f69` |
| `run/receipt.json` | `5ffcec25d221440aa8b14d1c7e85ea4577f44627842e82c7370863884ddae8c6` |
| `run/v2-original.jsonl` | `3d3dffcf3af7147052fc20e1dbdd85bd1d852f2b3c50a70d3384baed1ad54f0d` |
| `run/v2-reversed.jsonl` | `20237f96c1c1e2bccb819029e7a262ee476a03bb92f14ae843ca4da48d3eb5f7` |
| `run/probes-paired.jsonl` | `b5fcb19fa66f0145ca5e497856d158e779b373e7faaf7361319705c36e02ceba` |
| Model endpoint `checkpoint-ready.json` | `75efbf3b4925b3d7464a225d1adf83f6e836e7374b8285857dbf96b224e12424` |
| 90,866,412-byte encoder weights | `38908e2ce25cb02ed59f752e42fcc6dd5e67134fe8f98fb1297c40900fdcc255` |

This documentation pass hashed metadata, frozen scripts and outputs using only stdlib; it did not reread weights. Checkpoint inventory hashes are the immutable execution binding, not a new weight audit. Historical checkpoint `metadata.run.status="running"` is a save-time snapshot, not the completion gate: the bound completed Model run receipt and Model activation are authoritative.

## Interpretation and limitations

Model reports TRAIN agreement 1,314/1,500, including rules 314/500. These are producer-reported TRAIN results, not held-out transfer evidence or proof of architectural incapacity. Runtime did not replay optimizer/training history or score labels. Valid normalized option probabilities do not establish calibration.

Source-review evidence is `artifacts/release/p7-preparation-20261111-2207/{driver-review,review-closure}.md`. The initial review findings were owner-closed before execution. The focused `execution-report-review.md` subsequently confirmed those three fixes and found no report/evidence discrepancy; it did not replay inference or training. Installed versions are recorded, not independent dependency lock attestation.

Fresh HOME/cache and offline/local-only flags are not OS network denial or proof of fully offline installation. Linux execution and publication rights are not established. Report preparation added no model execution or production-source changes. The owner wheel/sdist build passed (`owner-build.log`); integrated build evidence is retained separately. No software tests/lint, dependencies, downloads or network work were added. Additional spend remains £0 actual/pending/allocation.
