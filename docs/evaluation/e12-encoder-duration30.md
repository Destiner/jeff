# E12 — thirty-epoch encoder endpoint

**M11 improves TRAIN fit, but does not improve broad development quality over M9's twelve-epoch endpoint.** On the separate 240 new cases, agreement falls 165→162, NLL rises .699420→.860175 and summed Brier rises .359766→.411284. Sentiment gains coexist with intent/rule losses. D3 gains three correct cases and three fully correct policies, while both proper scores worsen materially. Probe agreement and NLL improve; probe Brier does not. No further duration arm or promotion follows.

## Prospective contrast and populations

The [night criteria](night-comparisons.md) were adopted before M11 outcomes. E9's completed 70/80 sentiment, 78/80 intent and .699420442 NLL satisfied the previously fixed queue condition; that condition authorized this endpoint, not a newly reused success threshold. M11 is a **fresh original M4 MS MARCO pretrained-ranking-head start**, not continued M9 training. The duration changes from the original three epochs / M9 twelve epochs to **thirty total epochs**, 11,250 updates and 45,000 presentations. There was no endpoint selection, additional epoch or numerical rescue.

Keep four populations separate:

- Inherited development: 60 cases, native and reversed, 12 explicit source groups.
- New development: 240 cases, native and reversed, 170 groups; 80 each intent, sentiment and rules. The rule subset contains 40 policies / 10 mechanisms.
- Probes: 12 already-paired groups / 24 presentations, not another 24 derived cases or a fresh sample.
- D3: 96 original cases / 48 two-case policies / eight intentionally seen mechanisms. Its paired policy members are **different cases, not reversals**.

Source/group/policy dimensions overlap and are not pooled independent counts. Intent/sentiment/probe agreement is with teacher labels; rules use programmatic/rule-verified references. Same author/reviewer alias and unknown immutable reviewer revisions do not establish independent human truth. Development has been reused. D3's [construction and review qualifications](e4-d3-seen-rules.md) remain unchanged.

## Fixed TRAIN fit, not transfer

The [independent control review][train] supports the recorded reset, recipe and endpoint. All 105 recorded initial parameter hashes match original M4/M9 initial records; this compares producer hash evidence, not an independent tensor replay. Backbone LR2e-5, head LR5e-4, AdamW (.9,.999), epsilon1e-8, decay.01, seed42, batch4, cap256, four threads and FP32/MPS remain fixed. There is no scheduler, clipping or resume. The trainer's seeded per-epoch shuffle is source-supported; exact permutations were not materialized or independently replayed.

All 11,250 recorded losses are finite with consecutive steps and expected epochs; all 30 epochs contain 1,500 presentations. Changing-weight online loss is not fixed-final fit. Intrinsic validation was observed, not used to choose the endpoint. The saved final TRAIN fit has exact 1,500-row coverage, no ties or zero target probabilities.

| Fixed TRAIN, same 1,500 rows | Agreement | NLL | Summed Brier |
|---|---:|---:|---:|
| M4 MS MARCO, 3 epochs | 985 | .726023448 | .398784714 |
| M9, 12 epochs | 1314 | .289057329 | .164170973 |
| M11, 30 epochs | **1414** | **.123309483** | **.072368668** |

M11 fits all 500 intent and all 500 sentiment references, and 414/500 rules. Relative to M9, rules contain **130 gains and 30 losses**, not 130 unqualified improvements; 86 remain wrong. Fifteen explicit groups contain lost agreements. These TRAIN figures use raw saved probabilities: M11 NLL .123309482511 versus .123309483947 after within-tolerance normalization. The development scorer below retains its existing normalization policy; neither clips probabilities.

### Exact mechanisms now fitted in the small TRAIN view

The explicit R11 crosswalk identifies 160 TRAIN cases / 80 two-case policies, **not all 500 rules**. Evaluation independently checked it; [R14](../research/m11-mechanism-fit-append.md) also appended actual M11 vectors and consumed only Evaluation's safe D3 aggregates. No TRAIN↔D3 policy identity is invented.

| Mechanism | TRAIN M9→M11 /20 | M11 complete TRAIN policies /10 | D3 M9→M11 /12 | M11 complete D3 policies /6 |
|---|---:|---:|---:|---:|
| Lexicographic | 17→19 | 9 | 4→4 | 0 |
| FIFO | 13→20 | 10 | 6→6 | 2 |
| Discount | 16→20 | 10 | 2→1 | 0 |
| Rounding | 10→14 | 4 | 1→3 | 0 |
| Packs | 11→15 | 5 | 6→6 | 1 |
| Rates | 10→10 | 0 | 1→4 | 1 |
| Coordinates | 7→20 | 10 | 3→3 | 0 |
| Cooldown | 13→18 | 8 | 3→2 | 1 |

The mapped TRAIN subset improves 97→136/160 and 28→56 complete policies /80. **FIFO, discount and coordinates now fit all 20 observed TRAIN examples /10 policies**, unlike M9. Their new D3 policies nevertheless yield 6/12, 1/12 and 3/12 agreements, respectively. This changes the diagnosis from merely incomplete training fit to observed complete-small-TRAIN-fit alongside limited new-policy performance. It is not mechanism mastery, exhaustive branch coverage or an isolated architecture/capacity cause: source prose, policy parameters, arity and branch coverage differ. Rates remains one correct member of each TRAIN policy, with zero complete policies; no shortcut or label-error cause is identified.

## Development quality and retention

Natural-log NLL and summed multiclass Brier are lower-is-better. The unchanged scorer normalizes accepted roundoff within 1e-6. All 624 M11 presentations /2,390 probabilities are valid and untied, with no missing, invalid or extra records. Native and reversed choices agree on all 312 pairs; singleton maximal sets agree too. Tiny vector differences remain: zero choice flips is not exact probability identity or competence.

| Population | Original MS start: agreement / NLL / Brier | 3 epochs | M9: 12 epochs | M11: 30 epochs |
|---|---:|---:|---:|---:|
| Inherited /60 | 30 /1.026878 /.552223 | 42 /.712621 /.393343 | 43 /.673346 /.354056 | **42 /.757265 /.374626** |
| New /240 | 99 /1.058568 /.581492 | 141 /.917258 /.481392 | 165 /.699420 /.359766 | **162 /.860175 /.411284** |
| Probes /12 pairs, native | 7 /1.453783 /.651840 | 5 /1.876464 /.770313 | 8 /1.362500 /.425304 | **9 /1.085853 /.425596** |

All four encoder columns have the same reversed agreement and both-order agreement as their native counts. Exact order-specific proper scores remain in the bound reports. M11 new family agreement is **77 intent /72 sentiment /13 rules** of80 each, versus M9's78/70/17. M11 new rule NLL1.931114 /Brier.988070 remains poor; inherited rules are4/20 with NLL1.791009 /Brier.958864.

Relative to the three-epoch model, M11 new development improves all three headline metrics, but inherited agreement stays42 while NLL worsens and Brier improves. Relative to M9, inherited agreement and both proper scores worsen. Probe agreement rises8→9 and NLL improves, while Brier slightly worsens .425304199→.425596120. The extra both-correct probe is retained alongside all eight M9 successes, not a wholesale replacement.

| Comparator→M11 | Population | Retained both-correct | Gained | Lost |
|---|---|---:|---:|---:|
| Original MS start | New /240 | 82 | 80 | 17 |
| 3 epochs | New /240 | 122 | 40 | 19 |
| M9 | New /240 | 154 | 8 | 11 |
| 3 epochs | Inherited /60 | 35 | 7 | 7 |
| M9 | Inherited /60 | 42 | 0 | 1 |
| M9 | Probes /12 | 8 | 1 | 0 |
| M7 context | New /240 | 131 | 31 | 7 |
| M7 context | Probes /12 | 7 | 2 | 2 |

M7's order-sensitive context remains 171/170 new agreements, but only138 both-correct; M11's162 both-correct exceeds that count while losing seven specific M7 both-successes. Equal nine both-correct probes conceal two gains/two losses against M7. Separately published [M10](e11-seed-replication.md) has182/178 new agreements and157 both-correct; this is completed contextual evidence, not a newly computed matched M10 contrast or an architecture-controlled comparison.

All fourteen prior raw predictor contexts are retained in the E12 study, including original/trained MiniLM, earlier M2/M3, uniform/lexical, P3, M6 controls, M7, M8 and M9. The new M11 is the fifteenth; M10 remains in its separate completed E11 study. No old predictor is rescored. The [quality review][quality] retains all source, producer, domain, policy, mechanism, family/arity and probe membership regressions rather than selecting favourable slices.

## D3: more choices, worse proper scores

| Predictor | Agreement /96 | NLL | Summed Brier | Complete policies /48 |
|---|---:|---:|---:|---:|
| MiniLM start | 27 | 1.316860 | .729717 | 3 |
| MiniLM trained | 31 | 1.342824 | .743115 | 4 |
| MS MARCO start | 30 | 1.347340 | .748730 | 3 |
| MS MARCO 3 epochs | 26 | 1.355202 | .752642 | 5 |
| Uniform | 27 | 1.317371 | .730035 | 4 |
| Lexical | 24 | 1.319115 | .730912 | 2 |
| P3 | 29 | 1.589799 | .873581 | 6 |
| M7 | 27 | 1.449431 | .801219 | 4 |
| M9 | 26 | 1.419132 | .775609 | 2 |
| **M11** | **29** | **1.914380** | **.903707** | **5** |

M11 has worse NLL and Brier than **every retained D3 baseline**. Against M9, case retention/gain/loss/neither is18/11/8/59; complete-policy retention/gain/loss/neither is1/4/1/42. Against MS start, M11 loses20 successes/gains19; against three epochs it loses14/gains17 and retains only one of five complete policies. Equal headline counts do not imply the same successes.

| M11 mechanism | Agreement /12 | NLL | Brier | Complete policies /6 |
|---|---:|---:|---:|---:|
| Packs | 6 | 1.214576 | .688936 | 1 |
| Rates | 4 | 1.331116 | .791404 | 1 |
| Coordinates | 3 | 2.566508 | 1.201404 | 0 |
| Cooldown | 2 | 2.059736 | .995374 | 1 |
| Lexicographic | 4 | 1.389564 | .753191 | 0 |
| FIFO | 6 | .984698 | .597873 | 2 |
| Discount | 1 | 1.898230 | 1.012606 | 0 |
| Rounding | 3 | 3.870613 | 1.188867 | 0 |

Packs and lexicographic NLL improvements over M9 remain; rounding gains two choices while NLL worsens2.283350→3.870613. There is no averaged mechanism-success threshold, pooled TRAIN/D3 population or calibration/significance claim. [Independent D3 review][d3quality] checks all ten raw prediction sets, new summaries, all nine paired comparisons, old byte copies and the strict aggregate-only R14 projection.

## Execution, independent review and evidence

- M11 native training803.214302s +final TRAIN fit6.632465s =809.846767s. Original scientific freeze and immutable operational amendment remain: the latter accepts the actual P9 completion-receipt schema/path without weakening identity/closure or changing science. The original launcher is preserved.
- P10 executes **one encoder load**, 720 decisions /180 batch-four calls /2,751 probabilities, zero startup/canary/retry:624 unchanged development presentations plus96 D3 originals. Actual supervisor37.595754s, conservatively charged39s; full chain **848.846767/1500s**. Unused time is not extra authority.
- The checkpoint's embedded run snapshot still says `running`. Actual completed external run, endpoint and zero-exit process records establish completion; the stale nested status is not silently rewritten.
- P10 child lifetime RSS500,776,960B, sampled MPS driver1,108,017,152B, minimum sampled recommended headroom17,961,648,128B; separate8GiB/8GiB and2GiB floor satisfied. Training lifetime RSS2,730,344,448B /sampled driver2,310,307,840B. These overlapping scopes are nonadditive, not continuous peaks or a controlled speed comparison.
- Existing encoder `longest_first` cap256 semantics remain. Recorded padded maximum169 is **not independent untruncated-length evidence**. Source rejection of loading diagnostics is not an independently replayed strict-load guarantee. Evaluation did not load models/tokenizers or rehash weight bytes.
- Independent TRAIN/control review passed3,079 checks. [P10 binding review][runtime] passed2,806+36 checks, including all four input/output bindings, explicit reversal map, seven-file inventory metadata, counters, resource arithmetic and recorded/live group-absence observations.
- Same624 quality review checked all9,352 grouped contrasts,10,020 orientation units,5,010 pair units,3,091 regression rows and126 byte-identical retained files. D3 scored only M11 once, retaining all nine E10 contexts and six byte-identical evidence files. Review scopes/uncovered historical internals remain explicit; no substantive covered arithmetic discrepancy was found.

The [executed same624 recipe](../../configs/evaluation/e12-m11-v1.json), [D3 binding](../../configs/evaluation/e12-d3-v1.json) and [publication index](../../manifests/evaluation/e12-m11-report-v1.json) bind actual inputs, outputs and reviews. Corrected preparation v2 retains the earlier E11 pre-scoring failures; D3 preparation retains its pin-assembly filename error. No tests/lint, extra inference, new dependency, protected-final/D7 access or additional actual/pending spend. Packaging builds establish publication buildability, not scientific correctness or software-test evidence.

[train]: ../../artifacts/evaluation/e12-m11-control-review-v1/findings.md
[quality]: ../../artifacts/evaluation/e12-quality-review-v1/findings.md
[d3quality]: ../../artifacts/evaluation/e12-d3-quality-review-v1/findings.md
[runtime]: ../../artifacts/evaluation/e12-p10-binding-v1/findings.md
