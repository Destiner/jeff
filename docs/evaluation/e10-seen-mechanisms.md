# E10 — seen-mechanism transfer remains weak

**M7 chooses the first input option untied on all96 cases: it lowers NLL/Brier versus P3 but loses two agreements and two fully-correct policies. M9 is worse than its original pretrained MS MARCO start on all three overall metrics; versus the three-epoch checkpoint, agreement is unchanged but both proper scores worsen.**

96 original D3 cases · 48 new policies · 8 intentionally seen mechanisms · no reversals. Rule failure persists on new policies of intentionally seen mechanisms; it is not confined to the separate unseen-mechanism population. This does not isolate a causal mechanism effect.

`minilm_start` is a pretrained MiniLM encoder with a random scoring head, not an entirely random model. `msmarco_start` retains the original pretrained ranking head. The two `trained` comparators are the retained three-epoch M4 endpoints.

## Overall (reference agreement, natural-log NLL, summed multiclass Brier)

| Predictor | Agreement | NLL | Brier | Fully correct policies /48 |
|---|---:|---:|---:|---:|
| minilm_start | 27/96 (28.12%) | 1.316860 | 0.729717 | 3 |
| minilm_trained | 31/96 (32.29%) | 1.342824 | 0.743115 | 4 |
| msmarco_start | 30/96 (31.25%) | 1.347340 | 0.748730 | 3 |
| msmarco_trained | 26/96 (27.08%) | 1.355202 | 0.752642 | 5 |
| uniform | 27/96 (28.12%) | 1.317371 | 0.730035 | 4 |
| lexical | 24/96 (25.00%) | 1.319115 | 0.730912 | 2 |
| p3_frozen | 29/96 (30.21%) | 1.589799 | 0.873581 | 6 |
| m7_seed42 | 27/96 (28.12%) | 1.449431 | 0.801219 | 4 |
| m9_duration12 | 26/96 (27.08%) | 1.419132 | 0.775609 | 2 |

## Focal paired changes (new minus old; all 96 valid)

| Old → new | Δ correct | Δ NLL | Δ Brier | Case retained/gained/lost/wrong→wrong | Policy retained/gained/lost/neither |
|---|---:|---:|---:|---|---|
| p3_frozen → m7_seed42 | -2 | -0.140368 | -0.072362 | 7/20/22/47 | 1/3/5/39 |
| msmarco_start → m9_duration12 | -4 | +0.071792 | +0.026880 | 10/16/20/50 | 1/1/2/44 |
| msmarco_trained → m9_duration12 | +0 | +0.063930 | +0.022967 | 15/11/11/59 | 1/1/4/42 |

M7 improves proper scores without improving strict choice agreement; neither decoder beats retained uniform on NLL/Brier. M9 ties three-epoch agreement but worsens both proper scores and reduces fully-correct policies.

## All eight mechanisms

Cells: correct/12 · NLL · Brier. Context columns are the original and three-epoch MS MARCO/MiniLM endpoints.

| Mechanism | P3 | M7 | M9 | MS start | MS trained | Mini start | Mini trained |
|---|---|---|---|---|---|---|---|
| packs | 2/12 · 1.899016 · 1.065279 | 4/12 · 1.432943 · 0.765581 | 6/12 · 1.241300 · 0.692590 | 5/12 · 1.276753 · 0.706532 | 4/12 · 1.291678 · 0.716728 | 3/12 · 1.314182 · 0.728885 | 6/12 · 1.261849 · 0.712183 |
| rates | 2/12 · 1.480322 · 0.867037 | 2/12 · 1.502759 · 0.881631 | 1/12 · 1.237173 · 0.732115 | 6/12 · 1.174383 · 0.681125 | 3/12 · 1.202002 · 0.699360 | 3/12 · 1.195292 · 0.694673 | 3/12 · 1.230830 · 0.720341 |
| coordinates | 5/12 · 1.354238 · 0.743259 | 3/12 · 1.501129 · 0.829769 | 3/12 · 1.419737 · 0.773478 | 2/12 · 1.382215 · 0.748412 | 3/12 · 1.384492 · 0.749114 | 3/12 · 1.386724 · 0.750215 | 3/12 · 1.372659 · 0.743773 |
| cooldown | 5/12 · 1.473552 · 0.801093 | 5/12 · 1.469772 · 0.777158 | 3/12 · 1.406540 · 0.763708 | 2/12 · 1.416606 · 0.766728 | 1/12 · 1.608404 · 0.883487 | 3/12 · 1.386081 · 0.749893 | 1/12 · 1.597780 · 0.864767 |
| lexicographic | 3/12 · 1.646473 · 0.860997 | 4/12 · 1.318471 · 0.734471 | 4/12 · 1.416331 · 0.764340 | 5/12 · 1.363521 · 0.738443 | 2/12 · 1.378059 · 0.745618 | 5/12 · 1.382846 · 0.748276 | 5/12 · 1.397716 · 0.755881 |
| fifo | 4/12 · 1.464855 · 0.929791 | 4/12 · 1.203993 · 0.730115 | 6/12 · 0.975910 · 0.585536 | 2/12 · 1.114671 · 0.677284 | 7/12 · 1.092312 · 0.662459 | 4/12 · 1.097704 · 0.666061 | 6/12 · 1.003416 · 0.600062 |
| discount | 4/12 · 1.557815 · 0.811454 | 2/12 · 1.653461 · 0.880720 | 2/12 · 1.372716 · 0.747213 | 6/12 · 1.355092 · 0.732029 | 5/12 · 1.381418 · 0.747758 | 3/12 · 1.385567 · 0.749636 | 5/12 · 1.369773 · 0.739835 |
| rounding | 4/12 · 1.842117 · 0.909736 | 3/12 · 1.512918 · 0.810309 | 1/12 · 2.283350 · 1.145894 | 2/12 · 1.695480 · 0.939284 | 1/12 · 1.503249 · 0.816612 | 3/12 · 1.386480 · 0.750094 | 2/12 · 1.508566 · 0.808075 |

## Exact policy changes (fully correct on both distinct cases, not reversal correctness)

- p3_frozen → m7_seed42, retained: cooldown:p04.
- p3_frozen → m7_seed42, gained: coordinates:p02, fifo:p03, packs:p05.
- p3_frozen → m7_seed42, lost: coordinates:p01, coordinates:p06, discount:p01, fifo:p05, rates:p03.
- msmarco_start → m9_duration12, retained: packs:p06.
- msmarco_start → m9_duration12, gained: fifo:p02.
- msmarco_start → m9_duration12, lost: discount:p01, rates:p01.
- msmarco_trained → m9_duration12, retained: fifo:p02.
- msmarco_trained → m9_duration12, gained: packs:p06.
- msmarco_trained → m9_duration12, lost: discount:p02, discount:p03, fifo:p01, rates:p03.

Every one of the 48 policies is retained in the [policy table](../../artifacts/evaluation/e10-analysis-v1/policy-retention-all-pairs.csv) and [full appendix](../../artifacts/evaluation/e10-analysis-v1/full-appendix.md); all case transitions, including changed wrong→wrong choices, are in the [transition table](../../artifacts/evaluation/e10-analysis-v1/pair-case-transitions.csv).

## Coverage, strict ties, positions, and raw variation

All nine sets have 96/96 valid unique ID joins and 361 option values. Missing/invalid/duplicate/extra/unidentifiable = 0; no zero target probabilities or infinite losses. The three new scoring commands exited 0 with empty stderr. Six saved reports are reused unchanged.

- p3_frozen: exact raw ties 0/96; unique maxima 96/96; input-position choices {4: 40, 3: 21, 1: 24, 2: 11}; max raw sum deviation 1.1548399925231934e-07.
- m7_seed42: exact raw ties 0/96; unique maxima 96/96; input-position choices {1: 96}; max raw sum deviation 1.0430812835693359e-07.
- m9_duration12: exact raw ties 0/96; unique maxima 96/96; input-position choices {1: 23, 3: 30, 4: 17, 2: 26}; max raw sum deviation 1.0430812835693359e-07.

All neural predictors are untied; uniform ties all96 and lexical ties59. Uniform deterministic first-tie agreement27/96 differs from random 1/K expectation 0.269965278 and target-in-top-set overlap96/96. Positions use actual reference input order, never prediction-list order.

Raw family/arity cells contain 23 three-choice and 73 four-choice cases, all `rule_application`. Full means, population SD, sample SD, extrema, and per-position raw probability distributions are in `raw-family-arity-statistics.json` (descriptive, not uncertainty estimates).

- p3_frozen raw target-p mean ± population SD: K=3: 0.260616 ± 0.233901; K=4: 0.301962 ± 0.231330.
- m7_seed42 raw target-p mean ± population SD: K=3: 0.341810 ± 0.177596; K=4: 0.259189 ± 0.152615.
- m9_duration12 raw target-p mean ± population SD: K=3: 0.355896 ± 0.118587; K=4: 0.245459 ± 0.103625.

Target-probability variation also changes with target position and is not a content-sensitivity measure. Independently joined **coordinate** population SDs for M7 are [0.033840,0.025413,0.029169] at K3 and [0.064725,0.021338,0.019765,0.035504] at K4. These are not exactly constant vectors despite universal first-position choices. [Raw positional evidence](../../artifacts/evaluation/e10-owner-integrity-v1/positional-variation.json) preserves all three new candidates, without a calibration or semantic-discrimination claim.

## Regressions and interpretation

All source/family/group/arity/mechanism/teacher/basis/producer/domain slices and proper-score regressions for every pair are enumerated in `source-family-regressions-full.csv`; dimensions overlap and must not be summed. Unknown producer/domain remain unknown. `full-appendix.md` lists every focal regression and all policy outcomes.

D3 uses new policies on eight intentionally seen mechanisms. The new-v2 unseen-mechanism diagnostic is a different population, not a matched causal mechanism ablation, independent sample, or reason to pool denominators.

E9 M9 rule TRAIN fit314/500 versus new-v2 strict both-order17/80; M7 TRAIN176/500 versus new-v2 rule strict both-order0/80. These are cross-population context only: neither improved TRAIN fit nor D3/new-v2 differences establish architecture cause or capacity limits.

Labels remain same-alias author/reviewer `rule_verified`/programmatic evidence, not independent human truth. No promotion, calibration, significance, composite score, or semantic certification. Two cases per D3 policy are not reversals; no reversal pair correctness is reported.

## Provenance and execution

Lead predeclared E10 before P8; Evaluation adopted by01:03 UTC before outcomes. Append preparation was later (01:31–01:33), after P8 outputs existed but without inspecting them. It was source-reviewed UNEXECUTED, not execution-certified. This actual attempt completed at01:36:31 UTC without schema repair or retry.

Only the three new predictions from P8 root `artifacts/release/p8-d3-20261112-01` were scored, source revision `7e4819210c8c98aea2eb0111ad7a389cec4dccfe`. Actual delivery/process/packet schemas and candidate receipts were inspected and pinned in `provenance-review.json`; no guessed Runtime fields. The separate [P8 binding review](../../artifacts/evaluation/e10-p8-binding-v1/findings.md) passes56 checks of actual output/input hashes, grant/process/source/readout/checkpoint links and counts. Two decoder audits and three fresh inference phases complete in26.150528s under600s; P3/M7 each99 forwards (three repeated label-free startup inputs plus96 scored), M9 96decisions/24batch4 native calls and zero startup. Total294 decision/startup presentations is not the native-call count. All five phases exit0 with recorded group closure. Targeted profile changes retain the original scoring semantics; the encoder retains its existing longest-first256 behavior, not a newly asserted no-truncation contract. Reload records do not authenticate historical training. Scientific policy/mechanism counts use the explicit E4 units, not opaque-ID inference.

Recorded lifetime RSS P3/M7/M9 is3,352,379,392/400,883,712/493,813,760B; sampled MPS-driver maxima2,768,977,920/2,777,350,144/1,099,644,928B. Separate8GiB guards and≥2GiB recommended headroom hold. Overlapping scopes are nonadditive; samples are not true peaks, cached timing is not a controlled speedup, and offline flags do not prove OS network denial.

Unchanged core roundoff: accept |fsum(p)−1|≤1e−6 and divide by observed sum; no clipping. NLL uses natural log; Brier sums over options. Full-precision arithmetic, raw probabilities, exact choices and pins are preserved. `independent-audit-receipt.json` checks raw math without importing the scorer: 864 outcomes, 3,249 probabilities, 513 overall/mechanism/policy summaries, 36 pairs, 3,456 case and 1,728 policy transitions.

Original E4 report/limitations remain byte-retained. Its historical “No predictions, scoring” statement described the old preparation stage, not this completed E10 execution. Old evidence/errors are not rewritten.

Initial analysis/scoring used the global uv-managed Python3.12 entry, which resolves to the same binary as the project environment. The owner subsequently reproduced all three **complete score-report objects identically under the project venv**; [exact commands and environment receipt](../../artifacts/evaluation/e10-owner-integrity-v1/project-reproduction.json) retain that distinction. This was CPU verification of new predictions only, not another model run or replay of retained six-predictor scoring. A nonmaterial binding-review Git path-scope command error is preserved in its receipt.

[Execution and frozen dependency records](../../artifacts/evaluation/e10-d3-preparation-v1/execution-01/receipt.json), [independent arithmetic audit](../../artifacts/evaluation/e10-analysis-v1/independent-audit-receipt.json), [appendix](../../artifacts/evaluation/e10-analysis-v1/full-appendix.md), [executed input bindings](../../configs/evaluation/e10-p8-v1.json) and [publication index](../../manifests/evaluation/e10-p8-report-v1.json) make the result reproducible. No additional inference, dependencies, tests/lint or fixture activity; additional actual/pending spend £0.
