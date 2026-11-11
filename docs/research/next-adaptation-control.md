# R7: one fixed-feature readout control after M7

**Recommendation, not execution authority:** make the next controlled contrast a **pretrained-initialized, readout-only Qwen adaptation**, keeping the original transformer and shared embedding frozen. Compare this one new treatment with the already-authorized full-parameter low-LR M7 and original P3. Do not add a data, prompt, LR or seed sweep.

This is an operational parameter-scope contrast, **not an identified repair for letter bias**. M7/E7 outcomes were pending when the design was chosen. M7 continues independently; Research sign-off, D6 and this document are not gates. If M7 fails, the contrast asks whether restricting adaptation can preserve useful pretrained discrimination while learning. If M7 succeeds, the **same contrast** checks whether that gain requires broader adaptation or is attainable by reweighting fixed features. This is confirmation of a scope hypothesis, not a repeatability experiment or independent validation of M7. There is one treatment, not a success/failure menu or a preauthorized rescue.

## Why this rather than more data or a static offset

- M6 failed even deterministic TRAIN fit: agreement805→431/1500, CE1.357724→1.390592. E6 independently establishes strict first-position choice on624 development presentations, not a uniform distribution. Some proper-score exceptions remain; not every metric worsened.
- Model's bounded source/update review and Data D5 found no demonstrated objective/target/schedule defect. That does not establish native-gradient correctness or identify the cause. M7 already tests the10× smaller nominal LR; do not repeat that comparison or add another value.
- Frozen P3 has useful signal, notably intent/probes, but poor rule probability/order behavior. Retained encoders also fail broad rule transfer; an encoder return or architecture migration is not an established remedy.
- [R6](order-instability-diagnosis.md) identifies a transferable mirror contrast in some strata, not a universal fixed prior. Letter reassignment and content order interact. A six-row **contextual linear readout** can change the use of existing features; it is not six constant letter offsets. No claim that R6 proves a readout cause.
- D4 exposed TRAIN branch/output coverage weaknesses, not a demonstrated label erratum; Data's D6 quantification/design was requested directly. New coverage is a separate future data hypothesis. It cannot by itself explain failure to improve fit on the existing labels, and inserting up to96 new examples here would confound the scope contrast.

## Exact proposed treatment

Start from **original P3**, `Qwen/Qwen2.5-0.5B-Instruct` revision `7ae557604adf67be50417f59c2c2f167def9a775`, never M6/M7's final weights.

| Held fixed | Specification |
| --- | --- |
| Data | Released v2 TRAIN:1500 decisions/880 declared groups,500 per family; unchanged targets and shards. Manifest SHA256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`. No D6 insertion, held-out examples or new labels. |
| Exposure | Exact M6/M7 materialized row **and option** schedule, SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`; seed42. No schedule regenerated from a guessed RNG procedure. |
| Input/readout meaning | P3 tokenizer, official template/instruction/assistant boundary, actual allowed A–F token IDs, original option identities, cap1024/no truncation, T1; CE/softmax over the K supplied symbols, not all six or full vocabulary. |
| Optimization | M7 nominal recipe: FP32/MPS, AdamW2e-6, betas(.9,.999),epsilon1e-8,decay.01,clip1, `foreach=False`; microbatch1/accum4, one epoch375 updates, no scheduler; four threads. Final checkpoint, no development selection. |

**Only adaptation scope changes:**

1. Freeze **every original parameter**, including final normalization and the entire tied input/output table. Exclude all original parameters from AdamW and weight decay.
2. Clone the six allowed output rows into a separately stored, trainable, **bias-free** `W_head[6,H]`. Initialize from original P3 rows; no random replacement. A view or a re-tied parameter is not this intervention.
3. Obtain the original transformer's final normalized hidden vector `h(x)` at the assistant boundary. Train only `W_head @ h(x)`, restricting to the actual K symbols for that case. Frozen backbone runs under `no_grad`; the head operation runs outside it. No inference-mode tensor reused for autograd, feature cache, additional forward, dropout, pooling, candidate encoder or rationale loss.
4. Keep one six-row parameter/optimizer, including ordinary AdamW decay/moment behavior on coordinates not directly used by a particular K. Do not add per-K optimizers or masks.

Original tied embeddings must stay unchanged: unfreezing or writing learned rows into that table also changes prompt embeddings and violates the contrast. The new head is small, but the full frozen494M-parameter base is still required.

### Binding and saved artifact

At initialization, the six-row projection equals the selected P3 vocabulary logits **algebraically**, not necessarily bit-for-bit under a different MPS matrix kernel. Before any update, bind the ordinary deterministic1500-row pre-fit outputs to M7's saved original-base pre-fit vectors/logits and exact input/token metadata. Proposed fixed tolerances are max absolute1e-6 for conditional probabilities and1e-4 for allowed logits, with identical option identities/top sets; these are engineering tolerances, not measured guarantees. Exact top-set agreement is deliberately stricter near ties than numeric tolerance; preserve discrepancies as binding evidence, not failed learning. Missing valid controls or a failed tolerance blocks this recipe before learning; do not loosen tolerances, run extra controls or swap methods after outcomes without separate authorization.

Save the six-row tensor with a versioned reconstruction manifest: base/tokenizer hashes, ordered token IDs, shape/dtype, prompt/forward recipe, training/schedule/source hashes and final step count. Runtime must reload the **same frozen base plus head** in a fresh process. This is not silently compatible with the current self-contained trained-HF contract and is not a stock-generation checkpoint. Model/Runtime need an explicit, reviewed contract amendment if execution is authorized. Conditional head probabilities do not provide full-vocabulary allowed-token mass or preserve a chat/generation capability claim. No dependency or new framework is required in principle; nothing is implemented here.

## Falsifiable interpretation frozen before a new outcome

Use original P3 and M7 as controls; failed M6 and M4 encoders are contextual comparators, not matched architectures. The question is whether the restricted path can improve the fixed decision objective **without sacrificing the already-useful pretrained signal** under this same recipe.

| Observed result | Supported conclusion | Not established |
| --- | --- | --- |
| Head-only improves TRAIN CE/agreement versus original P3, with broad both-order development proper-score/retention improvements; M7 does not | Fixed original features support useful adaptation here; limiting the update path is practically promising under this recipe. | Transformer updates alone caused failure; a pure letter bias was removed; general reliability. |
| Both improve broadly versus P3, with similar pattern | Some observed benefit is attainable without changing the backbone; broader adaptation is not demonstrably required for that pattern. | Statistical equivalence, robust replication, or equal future capacity. |
| M7 improves TRAIN and development while head-only does not | Broader adaptation is useful relative to **this** head initialization/LR/exposure budget. | An optimized head could never work or representations must change in general. |
| Head-only fits TRAIN better but not development | Fixed-feature adaptation can fit these labels; transfer/source mismatch remains. | Which dataset, feature or label mechanism causes that mismatch. |
| Neither improves TRAIN versus original P3, or head barely moves | No support for this matched readout control; preserve the negative result and its observed movement/gradient evidence. | Missing reasoning capacity, impossible head learning or a backend defect. No automatic LR rescue. |

The interpretation rows are not exhaustive: crossed TRAIN/development or mixed-family outcomes stay mixed under E7's interpretation, rather than being forced into “broad improvement.”

TRAIN reports must include same-rendering before/after CE, agreement, full vectors/logits/top sets/margins, family/source summaries and actual answer-position distribution. Persist every already-computed preclip norm and before/after head parameter change; do not add per-step whole-model scans. Show ties and near-null adaptation rather than inferring them from argmax. Identical nominal LR/clip **does not equalize effective steps**: scope changes moment histories, shared-table coupling, parameter count and joint gradient clipping. The contrast manipulates that operational bundle, not scope independently of optimization geometry.

Evaluation owns the existing inherited60/new240/probe24-over12 populations, both orders, coverage/ties, NLL/Brier, source/family contributions, rule flips/both-order correctness and intent/probe retention. Use E7's frozen interpretation rather than a new composite or a threshold chosen from this treatment. Improvement relative to failed M6 alone is insufficient; smaller TV can accompany consistently wrong choices. Negative family/source contributions remain visible. No D3 addition, final access, new evaluation cases, confidence calibration or significance certificate. Previously consulted development evidence remains exploratory.

## D6 relationship and cost

Direct request: `artifacts/handoffs/research/20261111T1647-R7-D6-design-coordination.md`. Only TRAIN-derived coverage facts/design are requested; no E6/R6 protected cases or paraphrases are sent. D6 remains design-only: no authoring/release or insertion into M7 or this contrast. Any later coverage experiment must separate novel-policy/branch coverage from extra examples, updates, teacher verification and exposure; that is **not a second R7 experiment**.

At first design freeze, D6's quantitative ranking is pending. Existing evidence supports considering reachable output/branch diversity, not forcing impossible distractors to become targets. Preserve unknown enumeration/label-verification limits. D6 should remain available to strategy without blocking this narrower optimization question.

- **Data/teacher:**0 new decisions,0 new labels,0 paid teacher calls. Existing approved artifacts only.
- **Implementation estimate:**2–4 engineering hours across Model/Runtime for training path, artifact/reload agreement, source review and binding; Evaluation can reuse its scorer. Judgment, not measured effort. A failed binding is not permission to expand the experiment.
- **Compute estimate:** roughly3–7 minutes for the future full train/fit/save process, plus one separately authorized existing-size624-presentation **development** pass of the final checkpoint (P4's measured40.53s is only an anchor). M6 measured776.08s whole process and551.83s learning segment, with114.23s forward/292.12s backward/20.65s clip/124.04s optimizer. Removing most backward/optimizer work is promising, not a measured speedup.
- **Memory:**6H trainable FP32 scalars plus their gradients/moments, but approximately1.98GB base weights remain. Frozen P3's roughly2.77GB observed MPS-driver maximum is only an inference-scale reference. Do not add it to RSS or claim a measured head-run peak. Retain proposed45min external/16GiB RSS-driver/≥2GiB recommended-headroom guards and Model scheduling; no separate disposable learning probe, retries or fallback.
- **Paid cost:**£0 expected/allocated/spent. Implementation and a future execution need separate authorization; no cloud/dependency budget implied.

## Provenance and current state

Design uses R6's delivered frozen-model result, `docs/model/m6-qwen-{results,diagnosis}.md`, Data D5 delivery and `artifacts/handoffs/model/20261111T1643-M7-adopted-low-lr.md`; no new literature survey or raw held-out input. Focused review: `artifacts/research/r7-20261111T164550Z/readout-control-review.md`. Exact delivery commit/time, D6 update if received, and review/build receipts are in the R7 handoff/evidence log.

This is one proposed contrast, not code, a trained model, a promise of learning improvement, an R6 causal repair or an active fallback. M7/E7 continue on their own frozen plan. The lead/user strategy discussion can accept, reject or defer the recommendation without waiting for Research.
