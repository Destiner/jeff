# Final transfer diagnosis and one improvement opportunity

Research resumed at 17:59:11 UTC on 2026-11-12. Preliminary findings were delivered at 18:11; the selected treatment followed actual S1/S2 comparisons, the bounded TRAIN sample and one predeclared diagnostic. This is a development decision, not a claim of general capability or permission to bypass release/evaluation gates.

## Decision

**Select one full-parameter update initialized from the actual M9 checkpoint**, using 240 independently authored task-aligned examples and **80 intent + 80 sentiment + 80 rule_application** rehearsal examples from the original released TRAIN set. Preserve raw native-order T1 serving. Do not substitute a scoring correction, original-START reset, new architecture, second recipe or null-subtracted score.

Research's selected packet is [research-decision-1835.md](../../artifacts/research/final-sprint-20261112-01/research-decision-1835.md). **Model concurred at 18:36:52 UTC: the single M13 treatment is jointly frozen**, before learning and fresh reserved outcomes (mailbox `f373a0bf-f7f9-4859-a038-a07e70baded8`). Data may materialize the selected mixture. This is not execution: Data release, Evaluation's private content/exclusion freeze, exact source/initial-state binding and final-release preflight remain required.

### Why preserve M9's learning?

| Exploratory evidence | M9 | Original MS MARCO START |
|---|---:|---:|
| Selected S1 workspace preferred / acceptable, n12 | 9 / 11 | 5 / 8 |
| Workspace NLL / summed Brier, singleton n8 | .61947 / .33161 | 1.13096 / .60393 |
| S2 direct-sentiment agreement, n16 | 13 | 7 |
| S2 NLL / summed Brier, n16 | .330177 / .205109 | 1.427232 / .743309 |
| S1 tickets preferred, n24 | 7 | 9 |
| S1 tickets NLL, singleton n20 | 2.14747 | 1.32039 |
| All S1 preferred, n96 presentations | 38 | 45 |

The primary-task benefits favor M9 despite START's pooled and ticket advantages. S2 has eight matched gains and two losses relative to START; **negative sentiment remains weak: M9 2/4 versus START 4/4**. M9 positive/neutral/mixed counts are 4/4, 4/4 and 3/4.

S1 contains 48 cases in 40 groups, each rendered twice; the selected workspace slice is six cases, not representative product coverage. S2 is 16 balanced, AI-authored and separately AI-reviewed exploratory cases. Authored preferences are not verified truth. Evaluation normalizes validated vectors by their actual sums for quality arithmetic; proper scores here do not establish confidence calibration. These observations choose an initializer, not the final deployment winner.

## Ranked diagnosis

1. **Task/relation coverage is the most actionable explanation.** The exact 24-row TRAIN sample teaches concrete requested-action matching, evaluative-proposition sentiment and computed rule results. Those relations do not establish arbitrary ticket-taxonomy, social-response-policy or creature-policy competence. Repeated sentiment lexicons coexist with different targets; same-object intent alternatives require more than noun matching. The sample supports a coverage hypothesis, not memorization, defective labels, catastrophic forgetting or a full-corpus audit. Exact question-string counts are not recovered generation-template counts.
2. **Candidate preferences and scenario interactions both matter.** Ticket labels choose General feedback in 12/12 S1 cases across balanced winning positions. The empty-state probe gives Feedback .4100 versus How-to .3940, but actual contexts raise feedback probability in every case, to mean .70224. Descriptions give null Feedback .45247 versus How-to .42630; original mean .57369 and eight feedback choices. A narrow question/candidate-conditioned preference exists; it does not identify a prior-only cause. In counterevidence, described bookmarks give null Places to visit .7855 but that winner matches none of six contextual choices, with mean total variation .90515. Output dependence on context is not necessarily useful semantic dependence.
3. **Adaptation has task-specific benefits and costs.** The observed primary-task advantages and unrelated-task regressions oppose both “fine-tuning universally helped” and “reset because pooled transfer fell.” More fitting on the old mixture is not the targeted remedy. The historical M11 fit/transfer result is relevant context, not a new reanalysis or architecture verdict.
4. **No demonstrated implementation defect warrants a mechanical repair.** Execution-bound source agrees on retained trained head, strict loading/eval, state+question/candidate serialization, score sign, grouped softmax and option mapping. B1/B2 portability establishes faithfulness on its cases, not correct task formulation. Training may truncate overlength pairs while browser serving rejects them; no accepted short-case failure was attributed to this boundary. Each candidate score sees its own text, not competing descriptions; that limits some list-relative tasks without proving encoder incapacity.

## Completed discriminating observation

The sole prospective probe used **16 empty-state decisions / 66 probabilities**: first occurrence per exact question and semantic candidate set, retaining its actual order. It read no targets or outcomes during preparation and mapped to all 96 existing S1 presentations. Model executed it once; Research performed the frozen saved arithmetic. A fresh independent implementation agreed on 1,684 numeric fields with maximum difference zero. All vectors were positive and untied, with maximum sum error 1.0431e−7.

Raw probabilities were not clipped or renormalized; centered-log contrasts used positive entries, with no epsilon. One representative serves mapped option rotations based on the inspected separable scorer, not a new proof of exact all-order invariance. Empty state is out of distribution and retains question/candidate text. **No adjusted serving distribution or corrected accuracy was calculated.** The probe is exhausted; unused decision/time allowance grants no more work.

## One fixed intervention

| Field | Selected treatment |
|---|---|
| Initial weights | Actual trained M9 twelve-epoch retained-head checkpoint, `artifacts/model/m9-msmarco-duration-20261111-01/training/checkpoint` |
| Initialization proof | Strict checkpoint load; Model binds initial parameters to the pinned M9 run's `weights.after`; no head reset or optimizer-state resume |
| Fresh data | 80 workspace routing + 80 direct sentiment + 80 software-ticket intent |
| Rehearsal | 80 original intent + 80 sentiment + 80 rules, same deterministic family/ID hash selection |
| Optimization | Full parameters; fresh AdamW; backbone 2e−5, head 5e−4; weight decay .01, betas (.9,.999), epsilon 1e−8 |
| Schedule | Seed42, batch4, three epochs, 1,440 presentations, 360 updates; existing seeded epoch shuffles; no scheduler/clipping |
| Scoring | Existing renderer/tokenizer, complete-input cap256, native-order raw-logit T1 grouped softmax |
| Execution | CPU FP32, four threads; sampled RSS ≤8 GiB; pressure stop, finite supervision, serialized substantial ML; no silent fallback |
| Endpoint | Sole fixed endpoint, fresh reload and recorded TRAIN fit; no learned retry or validation-selected checkpoint |

The all-family rehearsal choice uses Lead's pre-freeze amendment. It trades 40 intent and 40 sentiment rehearsal rows for 80 old rule rows because the retention guard covers all three families. This neither expands rule research nor promises retention or policy coverage. Preserve the original 120/120 candidate; Data publishes a new immutable candidate/release and Evaluation binds its exclusions. No outcome-based replay selection, new rule authoring or protected-data access.

Model estimates 15–25 owner-minutes for the strict M9 initializer/binding adaptation; that is not measured native runtime. Exact adapted source and released data pins precede launch. Final-release tokenizer-only preflight, training, fit, candidate inference and failures share the existing 20-minute native allowance. Start no later than20:00; selection freezes21:00. Compatible export/browser acceptance has its separate five-minute allowance. Failure to satisfy the chosen treatment is no-go, not an automatic alternate initializer or second arm.

## Evaluation controls promotion

Adopt Evaluation's frozen rule unchanged: one native-order M9 incumbent and one challenger. Fresh primary routing+sentiment requires at least four preferred gains out of32, no per-domain preferred/acceptable loss, pooled NLL and Brier improvements of at least .02 each, and no per-domain proper-score worsening. At least12 singleton references per primary domain are required.

The separate retained new240 development guard allows at most six net choice losses overall and four per80-case family; NLL/Brier increases are capped at .05/.03 overall and .10/.05 per family. Report gross gains/losses and exceptions. Ticket/novel-taxonomy results cannot rescue primary or retention failure. Valid endpoint/reload and actual compatible browser parity are also required. **Otherwise retain current M9.** Research reads no fresh reserved references; S1/S2 scenarios or paraphrases cannot enter training.

## Public evidence, not a recipe guarantee

- [Exact base model card](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2): MS MARCO query–passage ranking provenance, not arbitrary-label competence or an immutable M9 function.
- [Yin et al., 2019](https://aclanthology.org/D19-1404/) and [Issues with Entailment-based Zero-shot Text Classification](https://aclanthology.org/2021.acl-short.99/): task/label distinctions matter; NLI itself is not universal.
- [Zhao et al., 2021](https://proceedings.mlr.press/v139/zhao21c/zhao21c.pdf): autoregressive contextual calibration, explicitly distinct from statistical calibration. Its null assumptions do not validate a correction for this scalar encoder.
- [Kumar et al., 2022](https://arxiv.org/html/2202.10054): conditional vision/theory counterevidence to fit-implies-transfer, not a demonstrated Jeff mechanism or support for this rehearsal ratio.

M10's stronger native/two-view diagnostic choices remain counterevidence against a broad task-impossibility claim, but neither its two-forward mean nor a new browser/quantization route is selected. New NLI, head-only training, extra old-mix duration and fitted serving corrections add unmeasured treatments rather than repair a demonstrated bug.

Evidence: [Research artifact root](../../artifacts/research/final-sprint-20261112-01/), including source/data/public briefs, predeclared probe and independent arithmetic, immutable drafts/reviews, S2 delivery and Evaluation gate. [S1 evaluation](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s1-v1/report.md). Research executed no model/tokenizer/browser work, fetched no model weights, and spent no additional money. Publication/builds do not certify numerical or model correctness.
