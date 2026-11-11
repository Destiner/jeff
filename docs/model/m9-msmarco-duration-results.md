# M9: longer fresh MS MARCO training improves TRAIN fit; rules remain incomplete

**Full-TRAIN supplied-target agreement rises from M4's 985 to 1,314/1,500, and CE falls 0.726023 → 0.2890573.** Intent and sentiment reach 500/500 each; rules reach 314/500. This is a fit diagnostic, not held-out correctness, architectural incapacity, or a promotion decision. **P7 reload/development return and independent E9 quality interpretation are pending at this draft.**

## Fit first, then the predeclared branch

M9 first measured the missing full-TRAIN fit of both preserved M4 final encoders on the same 1,500 rows (500 per family), without changing those checkpoints.

| Checkpoint | Intent | Sentiment | Rules | Total | Mean CE |
| --- | ---: | ---: | ---: | ---: | ---: |
| M4 MiniLM, 3 epochs | 497 | 348 | 238 | 1,083 | 0.6662502 |
| M4 MS MARCO, 3 epochs | 499 | 301 | 185 | 985 | 0.7260234 |
| M9 MS MARCO, fresh 12 epochs | 500 | 500 | 314 | 1,314 | 0.2890573 |

Both MS MARCO sentiment (301) and rules (185) were below 450/500, activating the predeclared **one fresh original-base 12-epoch arm**. The condition required either family below 90%; it was a pragmatic TRAIN diagnostic threshold, not a product success bar. This was **not nine extra epochs resumed from M4**.

## Controlled recipe and execution

- Original `cross-encoder/ms-marco-MiniLM-L6-v2`, revision `233902d25c440f23af6f7d6e94d2946bac0bee0a`; retained pretrained scalar head and full-backbone fine-tuning.
- Same M4 recipe except duration: 3 → 12 epochs, 1,125 → 4,500 updates, 4,500 → 18,000 presentations. Same frozen `data-pilot-v2`, seed 42, batch 4, cap 256, four threads, MPS, backbone LR 2e-5 / head LR 5e-4.
- Original AdamW settings: weight decay 0.01, betas (0.9, 0.999), epsilon 1e-8; no clipping or scheduler. Original shuffle construction was retained, not independently replayed; seed equality does not guarantee bitwise MPS determinism.
- Clean execution source `b072c8ba7a4e411b73d9efa8a9062793f016545c`. One attempt, no rescue/restart/alternative arm. Receipt records 4,500 finite online loss entries, 12 complete epochs, and 18,000 presentations at the fixed endpoint.
- All 105 initial parameter hashes matched M4's before-update metadata before the first update; all 105 changed in final metadata. These are historical training attestations, **not independent tensor decoding or update replay**. The first-update-attempt marker is written before the optimizer step, not proof that the step completed.

## What changed on the same TRAIN IDs

| Family | Gains | Losses | Choice changes |
| --- | ---: | ---: | ---: |
| Intent | 1 | 0 | 1 |
| Sentiment | 199 | 0 | 199 |
| Rules | 161 | 32 | 234 |
| Total | 361 | 32 | 434 |

All 32 lost agreements are rules. The net gain of 329 does not erase these regressions or the 186 remaining rule disagreements. Incomplete fitting under this recipe is not evidence of architectural incapacity.

The producer-owned CPU saved-vector review covered **all 4,500 vectors** (three full-TRAIN snapshots): identity/order/options and unique target mappings match; every probability is finite, positive and ≤1, sums are within 1e-6 of one, and every maximum is strict. CE uses saved target probabilities without clipping or renormalization. Existing statistics match recomputation to absolute 1e-12.

Position summaries are **family × arity**, with population SD (denominator N), never pooled across arities. Full means, SD and strict choice counts remain in literal nested `R9/artifact-review.json` / `.md`; rule arity-2 N=1 and arity-5 N=3 cells are tiny. Variation and changed choices do not establish semantic generalization.

## Intrinsic validation is not E9

The unchanged original 300-row validation reports 129 → 208 agreements and CE 1.052229678 → 0.694205557 versus the fresh original base. Validation provenance is unchanged from M4; these metrics were not a checkpoint selector. They are neither independent E9 nor untouched-final evidence. No significance, calibration, general-purpose capacity or default-promotion inference is made.

## Bounds, resources and preservation

Preparation began 22:11:57Z; first fit invocation was 22:51:58Z: **40m01s, within 45 minutes**. The native implementation/source-preparation window ended 22:56:57Z; this publication is docs-only and does not extend it. Core resource guards and the initial-binding gate were reviewed; package builds passed. Strict source guards are not complete peak-resource guarantees.

Model ML process time totals **311.959970375 s**: training 292.392775500 + initial MiniLM fit 6.989023333 + initial MS MARCO fit 6.262047042 + final fit 6.316124500. P7 is excluded. All four receipts report success and absent process groups; checkpoint-ready records all processes/groups gone and **73 frozen source/data/old-asset pins unchanged**. Additional local process spend: £0.

| Job | Internal lifetime RSS HWM (bytes) | Sampled driver max (bytes) | Sampled recommended headroom min (bytes) | External max sampled per-process RSS (bytes) |
| --- | ---: | ---: | ---: | ---: |
| MiniLM fit | 493273088 | 1099644928 | 17970020352 | 493273088 |
| MS MARCO fit | 492322816 | 1099644928 | 17970020352 | 492339200 |
| Training | 2525609984 | 2298560512 | 16771104768 | 2525675520 |
| Final fit | 493174784 | 1099644928 | 17970020352 | 493191168 |

Internal RSS is a process-lifetime high-water observation; driver/headroom and external RSS are sampled, not continuous accelerator/physical-memory peaks. External values above are actual process-receipt `max_sampled_process_rss_bytes`. R9's “external tree RSS” is a **derived sum**, not the per-process guard metric or physical usage. Do not add these scopes together. Bounds were 8 GiB RSS/driver, ≥2 GiB recommended headroom, and 1,200 s aggregate; sampling cannot guarantee no intersample overshoot.

## P7 / E9 handoff remains open

The original P7 start-by 23:12Z was missed **before any ML or binding**; the preflight-unstarted record is preserved. The renewed 23:15Z handoff sets start-by 23:30Z with the same unconsumed 120-second reservation: 624 decisions / 156 batches of four, four threads, no startup/canary, within the same 1,200-second aggregate. Parent will append the actual P7 return when available. No P7 outcomes were read or scored for this publication; Runtime progress is not gated on these docs. Independent E9 quality remains pending.

## Evidence index

Root: `/Users/destiner/Code/jeff/artifacts/model/m9-msmarco-duration-20261111-01`.

[Machine-readable run index](m9-msmarco-duration-run.json) pins actual evidence paths/hashes, recipe, summaries and pending status without copying online losses or vectors. Primary receipts: `checkpoint-ready.json`, `freeze-context.json`, `branch.json`, `initial-fit-statistics.json`, `final-fit-statistics.json`, the four `*-invocation.json` / `*-process.json` pairs, and `training/run.json`. Producer review: `R9/first-look.md`, `R9/artifact-review.json` and `.md`.

The saved endpoint uses the **existing seven-file encoder format**, not a new checkpoint contract. Exact file pins are in `checkpoint-ready.json` and the run index. No new ML execution, source/config changes, weights decoding, schedule replay, tests, lint or dependency changes were performed for publication.
