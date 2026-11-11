# E7 — lower-LR learning improves intent/sentiment, not rule robustness

2026-11-11. Independent comparison of the sole M7 LR2e-6 final checkpoint against original P3, failed M6 and retained encoders/baselines. [Predeclared interpretation](e7-plan.md), [executed recipe](../../configs/evaluation/e7-m7-v1.json), [hash-linked evidence index](../../manifests/evaluation/e7-m7-report-v1.json). Detailed CSVs and reproducible review live under `artifacts/evaluation/e7-quality-review-v1/`; no new inference was needed.

## Verdict: MIXED

M7 delivers substantive intent/sentiment, broad proper-score and ranking gains against **original P3**, not merely recovery from failed M6. It does **not** deliver new-rule both-order correctness or stability: all80 new rule cases flip, none is correct in both orders, and direct raw-input joins confirm first-position preference. Inherited-rule and probe-rule sensitivities remain. This is neither whole-learner failure nor blanket success. No formal binary gate, composite, automatic promotion, selected checkpoint or new experiment is introduced.

This is one seed on the same correlated development population reused through E5/E6, not untouched final data or independent generalization. Reversals are paired observations, not new independent examples. No cause is identified. The isolated nominal LR change plus telemetry is not proof of a native execution cause or an architecture ablation; readout-only R7 design is not authorized for execution here.

## Primary comparison, both orientations

Inherited60/12source groups and new240/170source groups remain separate. All12 predictors are retained. Agreement means agreement with the existing reference, with reference-basis qualifications below.

| Population | Order | Predictor | Agreement | NLL | Summed Brier |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | original | P3 original | 35/60 | 1.194706963 | 0.599127778 |
| inherited-v1 | original | M6 final | 17/60 | 1.442884125 | 0.778014052 |
| inherited-v1 | original | M7 final | 45/60 | 0.576871870 | 0.314785139 |
| inherited-v1 | reversed | P3 original | 34/60 | 0.966732759 | 0.537541497 |
| inherited-v1 | reversed | M6 final | 13/60 | 1.472594408 | 0.803252524 |
| inherited-v1 | reversed | M7 final | 44/60 | 0.552223816 | 0.297745345 |
| new-v2 | original | P3 original | 129/240 | 1.312349631 | 0.633492030 |
| new-v2 | original | M6 final | 65/240 | 1.413320085 | 0.779200217 |
| new-v2 | original | M7 final | 171/240 | 0.669211029 | 0.352958510 |
| new-v2 | reversed | P3 original | 118/240 | 1.410620678 | 0.687402352 |
| new-v2 | reversed | M6 final | 65/240 | 1.407130039 | 0.778133906 |
| new-v2 | reversed | M7 final | 170/240 | 0.618563980 | 0.337569741 |

## Both-order outcomes: broad gains can conceal rule failure

| Population | Predictor | Pairs | Both correct | Original only | Reverse only | Neither | Flips | Strict unique both |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inherited-v1 | P3 original | 60 | 28 | 7 | 6 | 19 | 19 | 28 |
| inherited-v1 | M6 final | 60 | 0 | 17 | 13 | 30 | 60 | 0 |
| inherited-v1 | M7 final | 60 | 39 | 6 | 5 | 10 | 21 | 39 |
| new-v2 | P3 original | 240 | 82 | 47 | 36 | 75 | 122 | 82 |
| new-v2 | M6 final | 240 | 0 | 65 | 65 | 110 | 240 | 0 |
| new-v2 | M7 final | 240 | 138 | 33 | 32 | 37 | 101 | 138 |
| probes | P3 original | 12 | 9 | 0 | 2 | 1 | 2 | 9 |
| probes | M6 final | 12 | 0 | 4 | 4 | 4 | 12 | 0 |
| probes | M7 final | 12 | 9 | 1 | 2 | 0 | 3 | 9 |

New overall flips fall122→101 while rule flips rise65→80/80. New neither-correct cases and all original-only/reverse-only differences are retained, not hidden behind net accuracy. Inherited flips rise19→21 even as both-correct grows28→39.

## Every family: paired gains/losses and proper-score deltas

M7 minus the stated baseline; negative loss delta improves. Denominators are common-valid presentations, not independent trials. Signed improving/worsening per-case contributions for every unit are in `paired-gains-losses.csv`.

| Population | Family | Order | Baseline | Common valid | Gains | Losses | ΔNLL | ΔBrier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inherited-v1 | intent | original | P3 original | 20 | 0 | 0 | -0.017281876 | -0.005235918 |
| inherited-v1 | intent | original | M6 final | 20 | 14 | 0 | -1.421111257 | -0.768899111 |
| inherited-v1 | sentiment | original | P3 original | 20 | 10 | 0 | -1.618732132 | -0.806555576 |
| inherited-v1 | sentiment | original | M6 final | 20 | 14 | 0 | -1.392148385 | -0.753025222 |
| inherited-v1 | rule_application | original | P3 original | 20 | 6 | 6 | -0.217491273 | -0.041236423 |
| inherited-v1 | rule_application | original | M6 final | 20 | 0 | 0 | 0.215222877 | 0.132237593 |
| inherited-v1 | intent | reversed | P3 original | 20 | 2 | 0 | -0.113586944 | -0.087425934 |
| inherited-v1 | intent | reversed | M6 final | 20 | 16 | 0 | -1.482514224 | -0.812816034 |
| inherited-v1 | sentiment | reversed | P3 original | 20 | 10 | 0 | -1.291031657 | -0.689182105 |
| inherited-v1 | sentiment | reversed | M6 final | 20 | 15 | 0 | -1.438368696 | -0.785794002 |
| inherited-v1 | rule_application | reversed | P3 original | 20 | 3 | 5 | 0.161091770 | 0.057219584 |
| inherited-v1 | rule_application | reversed | M6 final | 20 | 0 | 0 | 0.159771144 | 0.082088499 |
| new-v2 | intent | original | P3 original | 80 | 6 | 2 | -0.157405495 | -0.090002346 |
| new-v2 | intent | original | M6 final | 80 | 56 | 0 | -1.356952851 | -0.752533136 |
| new-v2 | sentiment | original | P3 original | 80 | 42 | 2 | -1.474115753 | -0.689104188 |
| new-v2 | sentiment | original | M6 final | 80 | 50 | 0 | -0.967624130 | -0.577060332 |
| new-v2 | rule_application | original | P3 original | 80 | 17 | 19 | -0.297894558 | -0.062494025 |
| new-v2 | rule_application | original | M6 final | 80 | 0 | 0 | 0.092249811 | 0.050868347 |
| new-v2 | intent | reversed | P3 original | 80 | 11 | 1 | -0.252982741 | -0.142073457 |
| new-v2 | intent | reversed | M6 final | 80 | 53 | 0 | -1.308058973 | -0.726511553 |
| new-v2 | sentiment | reversed | P3 original | 80 | 46 | 3 | -1.885768613 | -0.831873147 |
| new-v2 | sentiment | reversed | M6 final | 80 | 53 | 1 | -1.194469746 | -0.664325967 |
| new-v2 | rule_application | reversed | P3 original | 80 | 16 | 17 | -0.237418738 | -0.075551228 |
| new-v2 | rule_application | reversed | M6 final | 80 | 0 | 0 | 0.136830542 | 0.069145025 |
| probes | intent | original | P3 original | 4 | 0 | 0 | -0.047287394 | -0.019301956 |
| probes | intent | original | M6 final | 4 | 3 | 0 | -1.268124915 | -0.800394524 |
| probes | sentiment | original | P3 original | 4 | 2 | 0 | -1.565821505 | -0.735832802 |
| probes | sentiment | original | M6 final | 4 | 3 | 0 | -1.308513306 | -0.824621742 |
| probes | rule_application | original | P3 original | 4 | 1 | 2 | 0.640752429 | 0.408298302 |
| probes | rule_application | original | M6 final | 4 | 0 | 0 | 0.026933271 | 0.051844551 |
| probes | intent | reversed | P3 original | 4 | 0 | 0 | -0.194896824 | -0.113045595 |
| probes | intent | reversed | M6 final | 4 | 3 | 0 | -1.244329402 | -0.792328698 |
| probes | sentiment | reversed | P3 original | 4 | 0 | 0 | -0.069534736 | -0.079126945 |
| probes | sentiment | reversed | M6 final | 4 | 2 | 0 | -0.932949681 | -0.564349048 |
| probes | rule_application | reversed | P3 original | 4 | 0 | 0 | -0.166400538 | -0.067157440 |
| probes | rule_application | reversed | M6 final | 4 | 2 | 0 | -0.511412664 | -0.396073561 |

### Family both-order retention

| Population | Family | Predictor | Pairs | Both | Flips | Neither |
| --- | --- | --- | --- | --- | --- | --- |
| inherited-v1 | intent | P3 original | 20 | 18 | 2 | 0 |
| inherited-v1 | sentiment | P3 original | 20 | 7 | 7 | 8 |
| inherited-v1 | rule_application | P3 original | 20 | 3 | 10 | 11 |
| inherited-v1 | intent | M6 final | 20 | 0 | 20 | 10 |
| inherited-v1 | sentiment | M6 final | 20 | 0 | 20 | 10 |
| inherited-v1 | rule_application | M6 final | 20 | 0 | 20 | 10 |
| inherited-v1 | intent | M7 final | 20 | 20 | 0 | 0 |
| inherited-v1 | sentiment | M7 final | 20 | 19 | 1 | 0 |
| inherited-v1 | rule_application | M7 final | 20 | 0 | 20 | 10 |
| new-v2 | intent | P3 original | 80 | 64 | 14 | 3 |
| new-v2 | sentiment | P3 original | 80 | 14 | 43 | 35 |
| new-v2 | rule_application | P3 original | 80 | 4 | 65 | 37 |
| new-v2 | intent | M6 final | 80 | 0 | 80 | 34 |
| new-v2 | sentiment | M6 final | 80 | 0 | 80 | 40 |
| new-v2 | rule_application | M6 final | 80 | 0 | 80 | 36 |
| new-v2 | intent | M7 final | 80 | 75 | 5 | 0 |
| new-v2 | sentiment | M7 final | 80 | 63 | 16 | 1 |
| new-v2 | rule_application | M7 final | 80 | 0 | 80 | 36 |
| probes | intent | P3 original | 4 | 4 | 0 | 0 |
| probes | sentiment | P3 original | 4 | 2 | 2 | 0 |
| probes | rule_application | P3 original | 4 | 3 | 0 | 1 |
| probes | intent | M6 final | 4 | 0 | 4 | 2 |
| probes | sentiment | M6 final | 4 | 0 | 4 | 1 |
| probes | rule_application | M6 final | 4 | 0 | 4 | 1 |
| probes | intent | M7 final | 4 | 4 | 0 | 0 |
| probes | sentiment | M7 final | 4 | 4 | 0 | 0 |
| probes | rule_application | M7 final | 4 | 1 | 3 | 0 |

## Rule losses remain visible

The80 new rule cases map explicitly to40 policies and10 mechanisms. All40 policy and10 mechanism slices have zero M7 both-correct and every underlying rule case flips. Units overlap; they are not additional independent evidence. The full original/reversed losses below include original P3, M6, uniform and both trained encoders. M7 improves new-rule NLL/Brier against P3 but loses agreement25→23 original and22→21 reversed, loses P3’s4 both-correct cases, and has worse rule proper scores than M6. Inherited rules keep6 original but drop6→4 reversed; reverse NLL/Brier worsen against P3. Probe rules lose original agreement3→2 and worsen original NLL/Brier, despite improved reversed proper losses. These exceptions preclude a universal victory claim.

| Population | Order | Predictor | Agreement | NLL | Brier |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | original | m4-minilm-trained | 4/20 | 1.377048173 | 0.744755025 |
| inherited-v1 | original | m4-msmarco-trained | 7/20 | 1.316504369 | 0.713169324 |
| inherited-v1 | original | uniform | 6/20 | 1.379840509 | 0.746666667 |
| inherited-v1 | original | P3 original | 6/20 | 1.873183674 | 0.948396195 |
| inherited-v1 | original | M6 final | 6/20 | 1.440469524 | 0.774922179 |
| inherited-v1 | original | M7 final | 6/20 | 1.655692402 | 0.907159772 |
| inherited-v1 | reversed | m4-minilm-trained | 4/20 | 1.377048173 | 0.744755025 |
| inherited-v1 | reversed | m4-msmarco-trained | 7/20 | 1.316504370 | 0.713169325 |
| inherited-v1 | reversed | uniform | 4/20 | 1.379840509 | 0.746666667 |
| inherited-v1 | reversed | P3 original | 6/20 | 1.474312479 | 0.833108523 |
| inherited-v1 | reversed | M6 final | 4/20 | 1.475633105 | 0.808239608 |
| inherited-v1 | reversed | M7 final | 4/20 | 1.635404249 | 0.890328107 |
| new-v2 | original | m4-minilm-trained | 15/80 | 1.343231074 | 0.745066065 |
| new-v2 | original | m4-msmarco-trained | 21/80 | 1.411165629 | 0.765540609 |
| new-v2 | original | uniform | 23/80 | 1.303585765 | 0.726041667 |
| new-v2 | original | P3 original | 25/80 | 1.765476138 | 0.882113362 |
| new-v2 | original | M6 final | 23/80 | 1.375331768 | 0.768750989 |
| new-v2 | original | M7 final | 23/80 | 1.467581580 | 0.819619336 |
| new-v2 | reversed | m4-minilm-trained | 15/80 | 1.343231074 | 0.745066065 |
| new-v2 | reversed | m4-msmarco-trained | 21/80 | 1.411165630 | 0.765540610 |
| new-v2 | reversed | uniform | 21/80 | 1.303585765 | 0.726041667 |
| new-v2 | reversed | P3 original | 22/80 | 1.765855710 | 0.924975278 |
| new-v2 | reversed | M6 final | 21/80 | 1.391606429 | 0.780279024 |
| new-v2 | reversed | M7 final | 21/80 | 1.528436972 | 0.849424050 |
| probes | original | m4-minilm-trained | 1/4 | 1.309511799 | 0.872190365 |
| probes | original | m4-msmarco-trained | 2/4 | 2.637629531 | 0.712873665 |
| probes | original | uniform | 2/4 | 0.895879735 | 0.583333333 |
| probes | original | P3 original | 3/4 | 0.293464668 | 0.195408807 |
| probes | original | M6 final | 2/4 | 0.907283826 | 0.551862558 |
| probes | original | M7 final | 2/4 | 0.934217097 | 0.603707109 |
| probes | reversed | m4-minilm-trained | 1/4 | 1.309511799 | 0.872190365 |
| probes | reversed | m4-msmarco-trained | 2/4 | 2.637629531 | 0.712873665 |
| probes | reversed | uniform | 1/4 | 0.895879735 | 0.583333333 |
| probes | reversed | P3 original | 3/4 | 0.850517527 | 0.525303783 |
| probes | reversed | M6 final | 1/4 | 1.195529654 | 0.854219904 |
| probes | reversed | M7 final | 3/4 | 0.684116990 | 0.458146343 |

## Actual P5 input-position join

All624 actual P5 raw outputs were joined by opaque IDs to the three pinned label-free input sources, then checked against frozen state/question/ordered options and assembled raw vectors. Input/output hashes and exact joins match. No ID parsing and no inference from aggregate counts or output-list order. **All200 broad-stratum rule presentations choose input position0, untied** (40 inherited +160new); probes rules choose position0 in6/8. Intent/sentiment retain varied positions. The full family×stratum×suite distributions are below (positions are zero-based); `direct-p5-input-positions.csv` retains each join and raw margin.

| Population | Suite | Family | n | Position distribution | Ties | Minimum raw margin |
| --- | --- | --- | --- | --- | --- | --- |
| inherited-v1 | v2-original | intent | 20 | {"0": 6, "1": 6, "2": 4, "3": 3, "4": 1} | 0 | 0.747704096 |
| inherited-v1 | v2-original | rule_application | 20 | {"0": 20} | 0 | 0.086386204 |
| inherited-v1 | v2-original | sentiment | 20 | {"0": 6, "1": 5, "2": 4, "3": 5} | 0 | 0.124181628 |
| inherited-v1 | v2-reversed | intent | 20 | {"0": 4, "1": 5, "2": 6, "3": 4, "4": 1} | 0 | 0.982217084 |
| inherited-v1 | v2-reversed | rule_application | 20 | {"0": 20} | 0 | 0.201855749 |
| inherited-v1 | v2-reversed | sentiment | 20 | {"0": 5, "1": 5, "2": 5, "3": 5} | 0 | 0.740500070 |
| new-v2 | v2-original | intent | 80 | {"0": 23, "1": 22, "2": 21, "3": 10, "4": 3, "5": 1} | 0 | 0.136520833 |
| new-v2 | v2-original | rule_application | 80 | {"0": 80} | 0 | 0.162306532 |
| new-v2 | v2-original | sentiment | 80 | {"0": 27, "1": 20, "2": 19, "3": 14} | 0 | 0.088383168 |
| new-v2 | v2-reversed | intent | 80 | {"0": 25, "1": 22, "2": 19, "3": 12, "4": 1, "5": 1} | 0 | 0.097807467 |
| new-v2 | v2-reversed | rule_application | 80 | {"0": 80} | 0 | 0.199786484 |
| new-v2 | v2-reversed | sentiment | 80 | {"0": 22, "1": 23, "2": 19, "3": 16} | 0 | 0.070133626 |
| probes | probes-paired | intent | 8 | {"0": 2, "1": 4, "2": 2} | 0 | 0.722033054 |
| probes | probes-paired | rule_application | 8 | {"0": 6, "1": 2} | 0 | 0.107739925 |
| probes | probes-paired | sentiment | 8 | {"0": 3, "1": 2, "2": 2, "3": 1} | 0 | 0.599902242 |

## Probes: exact retention, not inference from equal net counts

The24 presentations are12 already-paired curated probes, four pairs per family, not an additional reversal pass. P3→M7 presentation agreement20→21/24 and both-correct9→9/12 conceal membership changes. M7 retains all4 intent stable successes and both old sentiment stable successes; gains sentiment02 and04; retains rule01; **loses formerly stable rule02 and03**. Rule04 remains non-stable. Thus7 old both-correct pairs retained,2 gained,2 lost. Versus M6, all9 M7 stable successes are gained (M6 had zero). M7 stable family counts are intent4/sentiment4/rules1; flips2→3/12. Exact pair/source-group membership is copied from frozen pairs, never inferred from IDs, and recorded in `probe-exact-retention.csv` and below.

| Explicit pair/source group | Family | Old P3 both | M7 both | Retained | Gained | Lost |
| --- | --- | --- | --- | --- | --- | --- |
| eval.validation.intent.01 | intent | True | True | True | False | False |
| eval.validation.intent.02 | intent | True | True | True | False | False |
| eval.validation.intent.03 | intent | True | True | True | False | False |
| eval.validation.intent.04 | intent | True | True | True | False | False |
| eval.validation.sentiment.01 | sentiment | True | True | True | False | False |
| eval.validation.sentiment.02 | sentiment | False | True | False | True | False |
| eval.validation.sentiment.03 | sentiment | True | True | True | False | False |
| eval.validation.sentiment.04 | sentiment | False | True | False | True | False |
| eval.validation.rule_application.01 | rule_application | True | True | True | False | False |
| eval.validation.rule_application.02 | rule_application | True | False | False | False | True |
| eval.validation.rule_application.03 | rule_application | True | False | False | False | True |
| eval.validation.rule_application.04 | rule_application | False | False | False | False | False |

### All-pair macro proper scores (12 pairs, no correctness selection)

| Predictor | Macro NLL | Macro Brier | Both correct |
| --- | --- | --- | --- |
| qwen25-05b-instruct-frozen | 0.534509491 | 0.284486434 | 9 |
| m6-qwen-v2-trained | 1.173710845 | 0.737779199 | 0 |
| m7-qwen-low-lr-trained | 0.300644729 | 0.183458695 | 9 |

## Tie-aware interpretation and arithmetic

For **every predictor**, raw exact-max semantic top sets were recomputed, joined across frozen pairs, and checked against the new supplement (per-case sets, per-pair exact equality, overlap size, both-singleton, target inclusion and strict-unique-both-correct). No epsilon or rounding determines a tie. Core first-input deterministic tie-broken choices remain distinct from semantic top-set equality/overlap; both are delivered. All M7 saved development vectors are untied. Uniform top sets tie every option: equality/overlap/target inclusion do **not** establish robust discrimination. Strict unique correctness and uniqueness denominators accompany all stability metrics in the appendix and CSV.

NLL is natural-log −log(normalized target probability); Brier sums (p−onehot)² across options, without division by K. Only already-valid vectors with sums within1e−6 are normalized by their row sum, matching core semantics; no repairs or changed outputs. Raw NLL/Brier and row sums remain separately retained. Zero target would yield infinite NLL, never an epsilon substitute; no zero targets or infinite losses occurred. Raw exact ties and core normalized arithmetic are separately checked. Per-case and aggregate agreement with core uses absolute1e−12 arithmetic tolerance, **not a quality threshold**.

Coverage:36 original quality reports in `comparison.json` and36 order reports, all12 predictors×3strata, independently checked;7,488 order presentation records =12×624, each complete and valid. No missing/duplicate/extra/unidentifiable/invalid/nonfinite rows or record diagnostics; no complete-case exclusions. Quality coverage is60/240/24 per predictor, order coverage120/480/24; valid-only and failures-as-unsuccessful denominators coincide. Main receipt has39,675 arithmetic/data checks, zero discrepancies. The completed supplemental receipt records4,424 checks with no discrepancies, covering actual explicit source-group/unit membership, raw pair supplement and all-pair macro agreement. These are actual-data analyses, not software tests.

## Context, reference basis and limits

M7 has better broad accuracy, NLL and Brier than both M4 trained encoders in both orientations; this does not imply superiority on every family, probe, source unit or task. The complete all12 context, including every exception, is retained in the appendix. MiniLM’s `random-start` is a **pretrained encoder with a random scoring head**, not a random model; MS MARCO start retains pretrained cross-encoder readout. Differing pretraining/capacity/rendering/training histories are not a matched architecture ablation.

Family×reference-basis, every explicit source group, producer/domain/mechanism/policy and unknown metadata are preserved. Intent/sentiment teacher references measure teacher agreement, not independently verified truth. Inherited and new rule_verified labels preserve their released programmatic/executable-consistency basis and same-alias/natural-language limits; teacher-authored checks are not independent ground truth. Probe rules remain teacher-only; sharing a family does not upgrade them. Unknown source metadata remains null. Existing reliability bins are descriptive only; no calibrated confidence or significance is claimed.

## Separate TRAIN/control evidence

The independently completed `../e7-train-review-v1/findings.md` reports TRAIN805→1130/1500 and logit CE1.357723636→0.530298992, but rules184→176/500 despite CE1.657126124→1.263299927; rule Brier0.722756007 remains worse than uniform0.714966667. All TRAIN before/after ties are0;472 after-fit rule position0 choices have strict positive margins. Old M6 missing TRAIN vectors/ties remain unknown, not reconstructed from M7 or development. Improved fitting and the retained gradient telemetry do not identify transfer cause.

`../e7-control-reuse-review-v1/findings.md` supplies exact624 raw START/P3 equality and unchanged schedule/control rationale; current review independently confirms raw equality again. `../e7-p5-binding-v1/receipt.json` supplies final checkpoint/reload provenance; raw source-input joins were independently performed here, without repeating giant byte audits. Source/metadata and selected fingerprints are not independent historical loaded-tensor/native-kernel attestation. No additional inference or readout-only R7 execution is authorized by this review.

## Reproducibility, immutable failures and source index

Invocation01 genuinely failed before producing score artifacts: it expected standalone quality report paths, while actual quality reports are embedded in `comparison.json`. Original `review.py`, `invocation-01-failure.txt` and stdout/stderr remain unchanged. `review-v2.py` changes only that schema access and failure filename; invocation02 completed with no failed substantive checks. Synthesis invocation01 additionally reported626 explicit-membership check failures: the analysis omitted the family element in composite unit keys and expected null instead of the summary’s `<unknown>` display sentinel. All3,744 raw pair-supplement checks passed. Original script, supplemental-receipt.json and invocation01 report/appendix remain preserved. Synthesize-v2 corrects the explicit key schema only; supplemental-receipt-v2.json records the actual second outcome. This is analysis-schema recovery, not another learning/inference attempt. All generated files use exclusive creation; reproduce in a fresh subdirectory within this review namespace, not over this delivery.

- [Complete indexed appendix](../../artifacts/evaluation/e7-quality-review-v1/appendix.md): all12 predictors, both orientations, every family, pair/tie-aware metrics and source-unit CSV index.
- [Full precision](../../artifacts/evaluation/e7-quality-review-v1/numbers.json), [coverage](../../artifacts/evaluation/e7-quality-review-v1/coverage.csv), [receipt](../../artifacts/evaluation/e7-quality-review-v1/receipt.json), [supplemental receipt](../../artifacts/evaluation/e7-quality-review-v1/supplemental-receipt-v2.json).
- [Source SHA256 and byte sizes actually read](../../artifacts/evaluation/e7-quality-review-v1/source-pins.json), including execution completion/recipe/grouped/supplement/control-differences, all36 quality and36 order reports, raw vectors, frozen references/pairs, reviewed E3 mapping, P5 input/output and separate TRAIN/control reports. No giant weight bytes were read. Source-pins plus supplemental script/source hashes give exact provenance, not execution authenticity.

No material arithmetic discrepancy found. Material outcome limitations are the rule positional failure, exact lost probe-rule successes, correlated reused development/one-seed scope, same-alias reference limits, old M6 TRAIN vector unknowns and historical execution attestation limits. No new gate. The independent review wrote only its new artifact namespace using exact project `.venv/bin/python -B` and CPU standard-library analysis. It did not run software tests/lint/syntax checks, fabricated fixtures, models/tokenizers, weight loads, network calls or final-data access. Owner publication and package builds are separate. Evaluation additional actual/pending spend remains £0.

## Execution controls, chronology and runtime

The immutable E7 plan was frozen at16:48:03.876045UTC, before Evaluation inspected M7 TRAIN-fit or P5 trained outcomes; integrated preparation3c9a0e7 preserves117scientific pins with mutable policy separately recorded. Model's actual lower-LR branch freeze16:58:51.169981UTC precedes invocation16:58:51.463597UTC. These are local records, not cryptographic timing proof. Starting624outputs were reused, not rerun: exact2390probability equality with preserved P3, no choice/top-set/tie changes, and matching recorded model/tokenizer/chat/readout/input/runtime controls. Whole Runtime source is not claimed byte-identical because checkpoint metadata support was added; reviewed scoring semantics remain unchanged. See the [control reuse review](../../artifacts/evaluation/e7-control-reuse-review-v1/findings.md).

Model execution source574774d631d707de9398c80dc5b936d9563e386c changed LR2e-5→2e-6 only as treatment. It reset original P3 weights, optimizer and RNG, reused exact M6 TRAIN schedule7fa68f68…2418e8/capacity evidence, and completed1500presentations/375updates/oneepoch. Full TRAIN vectors and all375already-computed preclip norms are telemetry additions, not additional objectives/forwards/weight scans. All1500before-fit saved CE/choice records and selected starting fingerprints match M6's original base. There was no development-best checkpoint selection, second arm, new capacity probe, new STARTpass or extra epoch. Full old M6 TRAIN vectors remain absent.

The final trained manifest70163c8567781bb7151b11c125999ea4bc6ec1ff52af52c52a205f9f4dbdd022 binds completed source receipt c78ad96769b76c2cabb7c2b0ec87dde13bca78e2f7e2256a51b6ca545b54e156 and distinct trained weight identity. [P5 owner binding](../../artifacts/evaluation/e7-p5-binding-v1/receipt.json) verifies manifest, source/run/audit and all3input/output identities, exact frozen Runtime source7a5af91ed352c648ff64bff6ab9f5bdb240302c1, and P3-equivalent full token audits/configuration/environment. Original tokenizer, official chat, complete A–F continuation boundaries, T1 conditional scoring, cap1024/no truncation, FP32/MPS/SDPA, batch1/four threads/cache-disabled readout remain unchanged. Runtime owns actual weight-byte validation and fresh load; Evaluation did not independently witness tensors or reread giant weights.

| Measured process | External wall | Scope |
|---|---:|---|
| M7 one full learning run |738.520718s|16:58:51.464–17:11:09.987UTC;375updates plus fixed before/after TRAIN fits and save;2700s cap|
| P5 one fresh final inference |39.071046s|17:18:29.487–17:19:08.558UTC;624presentations+3separate startup rows, no retry|

P5 local HF load.391540s, full suite35.716739s,17.470800decisions/s. Training CPU lifetimeRSS3,380,641,792B; observed MPSdriver maximum11,861,164,032B and minimum observed recommended headroom7,208,501,248B. P5 CPU lifetimeRSS552,632,320B, native macOS peak process footprint3,133,490,328B and observed MPSdriver maximum2,768,977,920B. Scopes overlap and are **nonadditive**; MPS samples are not true peaks. No cold-storage or matched memory/speed advantage is inferred: OS caches were not flushed and mapping was not traced. Offline/local-only flags and an empty HFcache do not demonstrate OS network denial or offline installation. See [Model M7 results](../model/m7-qwen-low-lr-results.md) and [Runtime P5 results](../runtime/p5-m7-checkpoint.md).

All375preclip norms are finite and step-bound;362exceed clip1. These observations neither identify a cause nor bound Adam parameter displacement. [Independent TRAIN review](../../artifacts/evaluation/e7-train-review-v1/findings.md) distinguishes stable-logit CE, raw/sum-normalized saved-probability NLL/Brier and FP32 rounding. Its initial event-schema assumption failed; original error/script are retained and only schema access was corrected. No learning run was repeated.

The main E7 orchestration completed on its first actual invocation, using the previously frozen runner and all12predictors. The two quality-review schema adaptations above are separate and preserved; they did not modify references, predictions, criteria or Model execution. After the interrupted owner turn, the18:47resume reused completed scoring/review and only checked integrity/published; it did not duplicate inference or scoring. The separate immutable Fable review snapshot was neither a gate nor modified.

E1–E6 conclusions, all earlier candidates/failures, and final-data isolation remain intact. This mixed result does not automatically promote a default or authorize R7 readout learning, new data, calibration, another model run or a new evaluation population.
