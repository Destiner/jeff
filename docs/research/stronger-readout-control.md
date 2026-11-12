# R9: choose one larger head-LR control, not a cache framework tonight

**Recommendation:** one fresh original-P3, frozen-backbone/six-row-head run with **AdamW head LR2e-6→2e-4**, holding the completed M8 recipe otherwise fixed. This is the single proposed next study. It has **one fixed learning arm, no selection arms and no refit**. The cached L-BFGS alternative was evaluated and is **not recommended for execution under this proposal**; no automatic fallback or additional lambda/LR sweep.

Why choose it: M8's head moved only0.45206% in norm and TRAIN agreement805→804/1500, while CE improved1.357724→1.332200. E8 is near original P3, not broad recovery. A100× nominal scale is a materially stronger update opportunity with the existing producer/export path. It is **not measured to be adequate, stable or optimal**, and the higher scale may overshoot. This trades a narrower scientific answer for less implementation risk during the night queue. M10/M11 and D8/E13 proceed independently.

## Evidence and exact question

M8 changed all saved TRAIN vectors and75choices;16 wrong-to-right versus17 right-to-wrong. Small weight movement was not zero functional effect. E8's new-original/reversed agreements130/119 of240 versus P3's129/118 and M7's171/170, and rule both-correct4→6/80, do not establish fixed-feature incapacity. E9's separate encoder duration result improves sentiment but not rule transfer; it is not a matched readout control.

**Falsifiable question:** under the same original fixed features, data/exposure, optimizer family and endpoint, does a larger nominal head learning rate materially improve deterministic fitting and useful development behavior compared with M8's small-step endpoint and original P3? A positive result would establish useful adaptation within these fixed features under this recipe. A negative result remains compatible with optimizer/budget/regularization limitations or inadequate feature separability; it is not an architecture-capacity verdict. No R6 letter-versus-position cause is identified.

## The one recommended treatment

| Factor | Freeze |
| --- | --- |
| Initialization/scope | Original `Qwen/Qwen2.5-0.5B-Instruct`, revision `7ae557604adf67be50417f59c2c2f167def9a775`; never M8/M7 learned weights. All494032768 original parameters, including final normalization and tied input table, frozen/outside optimizer and decay. Only independent bias-free FP32W6[6,896] initialized from original A–F output rows learns. |
| Inputs | Existing1500 released v2 TRAIN decisions/880 declared groups/500 per family; manifest SHA256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`. Exact materialized row **and option** schedule SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`, seed42; no new data, D7/D8 rows, reversed augmentation or resampling. |
| Forward/loss | Original P3 prompt/chat template/tokenizer/assistant boundary; normalized final hidden vector, actual allowed token IDs32–37/A–F, variable-K CE over supplied symbols only, T1, cap1024/no truncation. FP32/MPS, eval/no-grad frozen backbone, four threads, no feature cache. |
| Optimizer/exposure | **AdamW LR2e-4**; unchanged betas(.9,.999),epsilon1e-8,decay.01,global clip1,`foreach=False`; microbatch1/loss÷4 accumulation, one epoch1500presentations/375updates, no scheduler. Head-only parameter membership/nonaliasing unchanged. |
| Endpoint | Fixed final head after375updates. No early/best-checkpoint selection, extra epoch, warm start, lower-LR rescue, anchor loss, per-K bias, temperature or other change. |

LR is a design choice, not inferred optimum. Do not scale the M8 endpoint movement linearly by100 and present that as a prediction: gradients, clipping and adaptive moments change with the trajectory. AdamW decay toward zero is also **not** the anchored L2-to-W0 objective assessed below.

### Measurements and interpretation

Reuse the existing same-rendering1500-row START/FINAL fit, full allowed logits/probabilities, raw top sets/ties/margins, family×arity positional summaries, row/group/family CE/agreement, all already-computed preclip norms, and head endpoint norm/change evidence. Keep online changing-weight loss distinct from fixed-snapshot fit. Report losses/gains and source/family regressions, not just overall improvement.

Primary fitting contrasts are original P3 and M8, not failed M6. Inspect whether CE/agreement improve and whether movement is still nearly null, finite but destructive, or substantively useful. No numerical movement threshold is a success gate; large movement alone is not learning. Historical MPS/source bindings do not guarantee bitwise-deterministic repeated training. One seed and repeatedly consulted development strata remain exploratory.

Evaluation retains its existing624-presentation original/reversed/probe protocol and meaningful baselines, including exact rule first-position/both-order behavior and intent/sentiment/probe retention, proper-score exceptions and coverage. Better TRAIN fit with worse transfer is an informative negative. No new composite, calibration claim, arbitrary-generalization claim, product promotion, original-final24 access or tuning on D8 confirmation. E13 exposure of a future candidate requires its separately granted once-per-fixed-checkpoint pass.

## Existing representation is reusable; admission is not automatic

The new head can use M8's **`hf-untied-full-vocab`** export: independent FP32[151936,896] output table, only answer rows32–37 replaced, every non-answer row and original backbone/input tensor unchanged, `tie_word_embeddings=false`, exact saved config/tokenizer pins and disjoint storage. Use the existing stock-HF path and tensor/header/loading checks, not a second backend. The extra table remains544538624bytes of payload; this is not a six-row-only deployed model.

Model/Runtime's00:48/00:50 reuse notes establish that current admission pins **`m8.recipe.v1`, `m8.train.v1`, LR2e-6,375updates/1500presentations/oneepoch/Adamstep375, cache=false and exact field trees**. A different LR is currently rejected. Required prospective work:

1. Add **one exact new authorized recipe/receipt/profile discriminator and LR2e-4**, preserving the old M8 profile and immutable evidence byte-for-byte. No free-form LR admission or relabelling of old artifacts.
2. Reuse existing original-base scope/nonaliasing, same-hidden-state START and FINAL1500-row binding, allowed-logit1e-4/probability1e-6 limits and identical top sets, canonical tensor/hash/export identities, source crosslinks and strict fresh Runtime load checks. No weakened tolerances or invented new historical attestations.
3. Keep counts, optimizer state and control/schedule semantics identical to M8. Planned START1500 + training1500 + FINAL1500 implies4500 backbone evaluations in the inspected loop shape; Model must bind actual attempted/completed counts before granting execution. This is source-derived expected work, not a newly verified historical forward count. No disposable capacity update, repeated START suite, extra canary or warm-up beyond the later explicitly granted Runtime protocol.
4. New unique output root, source/recipe hashes, attempt/process/deadline records, fixed final checkpoint/proof/manifest. Runtime's planned fresh existing-size pass and startup count require their own exact Model reservation; the historical627-forward P6 is an anchor, not automatic new authority.

Failed numerical/scope/nonfinite/resource bindings stop the attempt; preserve artifacts. No post-update restart, tolerance relaxation or representation swap. Any zero-update plumbing repair must be expressly included in a future grant, not inferred from this document.

## Cached L-BFGS alternative: evaluated, not an extra recommendation

The alternative directly attacks the optimizer-opportunity question and avoids repeated backbone traversal. One original-base TRAIN extraction could cache nativeFP32X[1500,896], with exact row/group/family/prompt/token/allowed-ID/target mapping and hashes. Its payload is **5,376,000bytes**; an FP64 solver copy is10,752,000bytes. No reusable hidden cache was established in M8; saved predictions are not features.

The bounded solver design in `artifacts/research/r9-20261112T010431Z/solver-design.md` specifies one CPU full-batch FP64 PyTorch L-BFGS configuration, three anchored-L2 lambdas1/.1/.01 on a fixed TRAIN fit/selection partition, then one selected all-TRAIN refit. It explicitly bounds iterations/closure calls, retains W0 references, fixes unregularized selection CE/tie-breaks and casts/export-binds the final FP32 head. The positive full-coordinate quadratic plus fixed-feature CE is strongly convex in exact arithmetic, but finite-precision L-BFGS and a fixed budget **do not certify convergence/global optimality**.

Important limitations of that design prevent treating it as immediately executable:

- The proposed704/176 split counts **declared groups**, not proven source-independent units or guaranteed family-balanced row counts. Existing singleton groups can share domains/producers, and rules share policies/mechanisms. Broader known links must be resolved before a split is frozen. Internal selection reuses TRAIN and is not held-out transfer evidence.
- Its family/group weighting, fit-derived feature-scale anchor, CPUFP64 objective, cached computation, optimizer and regularization all change together relative to M8. This would be a new fixed-feature study, **not a clean LR-only contrast**. No fresh feature normalization or bias is justified by the cache.
- `fit()` currently recomputes native features; `readout()` uses MPS targets; scope attests `feature_cache:false`. L-BFGS closure evaluations cannot honestly populate Adam step375, online sequential rows or M8's source receipt fields. It needs a narrow new cache/solver proof profile or versioned training-evidence extension, not just accepting another LR.
- Original-base START/cache/CPU projection and finalFP64→FP32/native/full-output bindings need explicit measurements under unchanged tolerances. A cache projection alone is not a fresh native-backend equivalence claim. No extra native forward may be invented to repair a mismatch.

**Cost disagreement is material:** the numerical-design reviewer judged roughly2hours producer +1hour Runtime potentially sufficient; the targeted profile/source reviewer estimated **7–15person-hours** for cache provenance, objective/device/closure accounting, proof/admission and review, versus **2–5person-hours** for the LR-only profile. These are judgments, not measurements or owner commitments. The representation path is already implemented, but its existing exact M8 gates are real work. Given uncertain cache integration cost and concurrent night priorities, choose the narrower LR-only treatment now. Do not run a partial cache study and then switch to it, or implement both under R9.

The cached alternative's full numerical specification remains a **rejected/deferred design artifact**, not an authorized contingency, additional selection arm or request to build a general optimizer framework. Model/Runtime may later propose a tighter costed cache study under separate authority; R9 makes no automatic execution choice based on future outcomes.

## Cost and prospective bounds

- **Engineering:** LR-only2–5person-hours estimated across producer/profile, Runtime admission and focused review/build/handoff. A narrow controller/profile amendment, not new optimizer/export/backend implementation. Owner estimates may refine this before authorization; if it cannot fit the queue, report remaining work instead of substituting the cache design.
- **Compute:** M8's actual producer wall246.449293s, aggregate252.999084s including audits, separate P636.245988s are relevant minutes-scale anchors because work shape is unchanged. They are not a promised runtime or speedup. Propose one aggregate15-minute local ML budget including producer/admission/audits and downstream Runtime, no retries; detailed single-process caps must be frozen by Model/Runtime before execution.
- **Memory:** retain M8's producer16GiB separate RSS/driver guards and Runtime's8GiB guards, with≥2GiB recommended MPS headroom, as proposed future bounds. M8 observed driver2,772,107,264B and CPU lifetimeRSS3,367,747,584B are overlapping scopes, not additive peaks. No fresh capacity probe is proposed. Host load/queue status still belongs to Model.
- **Resources:**0 new labels/data/dependencies/cloud/paid services;£0actual/pending allocation. No model, tokenizer, weight, feature or optimizer was loaded/executed by Research. Model schedules nonpreemptibly after the already-authorized priority chains; this proposal changes none of their recipes or reservations.

## Status and evidence

R9 started01:04:31UTC on2026-11-12,25-minute cap01:29:31. Source-only design uses the completed M8/P6 reports, independently delivered E8/E9 aggregate outcomes, existing Model/Runtime reuse notes and two bounded design reviews. Direct nonblocking coordination: `artifacts/handoffs/research/20261112T0106-R9-design-coordination.md`. No completed provenance audit or model pass was replayed.

This is one decision-ready proposal for the lead/Model/Runtime/Evaluation, **not implementation or learning authority**. The document deliberately rejects the more ambitious cache study for this queue; it neither certifies optimization adequacy nor closes the fixed-feature-capacity question. Night availability continues separately through08:30:36UTC.
