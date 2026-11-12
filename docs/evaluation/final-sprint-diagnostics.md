# Final-sprint saved diagnostics

Saved exploratory evidence only. No M13 learning outcome, final promotion, or actual browser parity is established here. Authored preferences are not verified human truth; these small synthetic suites do not establish calibration, causality, or generalization.

## What the diagnostics support

M9's workspace-routing signal should not be lost in the S1 aggregate: **9/12 preferred versus START 5/12**, with acceptable counts 11/12 versus 8/12. On separate direct-sentiment S2, **M9 13/16 versus START 7/16** (8 matched gains, 2 losses). M9 nevertheless matches only **2/4 negative** authored labels, versus START 4/4. These are useful adaptation signals, not confirmation on a fresh final holdout.

M10 improves many choice counts but has consequential proper-score tradeoffs. On S2 its mean predictor reaches 15/16 versus M9 13/16, yet NLL is worse (0.404202 versus 0.330177), despite better Brier (0.151995 versus 0.205109). On S1, M10-mean's reactions and tickets NLL remain worse than START; paraphrase proper scores also remain worse. No single headline captures those differences.

## Method and denominators

S1 has **96 presentations = 48 cases × two formats, in 40 groups**, not 96 independent observations. S2 has 16 cases/groups, four per sentiment class, with 12 routine and four awkward cases. Suites are not pooled. S1 raw option counts are four or five; S2 has four options.

Choice counts use all presentations and separately report preferred and acceptable agreement. Proper scores use only singleton-acceptable references: **S1 n=72; S2 n=16**. NLL uses natural logarithms; Brier sums squared error over all options before averaging presentations. Lower is better. Zero target mass remains infinite NLL, never silently removed.

For each validated raw vector v, let N(v) = v / sum(v). The explicitly **SUM-NORMALIZED two-view mean** is:

`p_mean(i) = 0.5 × [v_native(i)/sum(v_native) + v_reversed(i)/sum(v_reversed)]`

Views are aligned by semantic option identity; this is a two-forward predictor, not one serving call or a per-case better-order selection. Mean ties use native input order; raw-profile ties use their own input order. Admission requires finite [0,1] values and sum error ≤1e-6 before normalization. No clipping, smoothing, imputation, or raw-file edits; **no historical byte-equivalence claim** follows.

## S1 saved summaries

All tables below transcribe saved summaries, with no new model calls or scoring. START is the original MSSTART baseline. Each cell is preferred / acceptable; NLL / summed Brier.

| Predictor | Overall /96; proper n=72 |
|---|---|
| M9 | 38 / 42; 1.62359 / 0.78469 |
| START | 45 / 51; 1.29324 / 0.68186 |
| M10 native | 57 / 64; 1.50461 / 0.63279 |
| M10 reversed | 62 / 69; 1.57004 / 0.56763 |
| M10 sum-normalized mean | 61 / 69; 1.13618 / 0.49774 |

### Domain

| Domain (choice / proper n) | M9 | START | M10 native | M10 reversed | M10 mean |
|---|---|---|---|---|---|
| Creature (24 / 20) | 10 / 10; 1.49792 / .76626 | 15 / 15; 1.20080 / .65199 | 16 / 16; 1.48977 / .67853 | 17 / 17; 1.12812 / .50704 | 17 / 17; .90887 / .47570 |
| Reactions (24 / 16) | 7 / 9; 1.89878 / .96319 | 9 / 10; 1.61359 / .80071 | 13 / 16; 2.07789 / .70139 | 15 / 17; 2.46704 / .73228 | 14 / 17; 1.82542 / .62728 |
| Sorter (24 / 16) | 14 / 16; .85063 / .51965 | 12 / 17; 1.05451 / .55871 | 16 / 20; .69021 / .35733 | 17 / 22; .17382 / .10874 | 18 / 23; .30097 / .17348 |
| Tickets (24 / 20) | 7 / 7; 2.14747 / .87236 | 9 / 9; 1.32039 / .71517 | 12 / 12; 1.71233 / .75254 | 13 / 13; 2.41133 / .86361 | 12 / 12; 1.48028 / .67554 |

Sorter aggregates two distinct tasks; bookmarks/resource taxonomy is not workspace routing. Workspace counts above retain that distinction; full option-set and joint strata remain in the saved results.

### Rendering

| Format (choice / proper n) | M9 | START | M10 native | M10 reversed | M10 mean |
|---|---|---|---|---|---|
| Described (48 / 36) | 22 / 25; 1.52513 / .69468 | 27 / 29; 1.28139 / .67886 | 28 / 31; 1.66981 / .67242 | 34 / 37; 1.77288 / .54933 | 30 / 33; 1.17217 / .48792 |
| Label (48 / 36) | 16 / 17; 1.72204 / .87471 | 18 / 22; 1.30509 / .68486 | 29 / 33; 1.33940 / .59317 | 28 / 32; 1.36719 / .58592 | 31 / 36; 1.10019 / .50755 |

### Kind

| Kind (choice / proper n) | M9 | START | M10 native | M10 reversed | M10 mean |
|---|---|---|---|---|---|
| Boundary (32 / 8) | 11 / 15; 1.66888 / .87050 | 15 / 21; 1.23368 / .70321 | 15 / 22; 2.00510 / .82244 | 17 / 24; 2.99301 / 1.08721 | 14 / 22; 1.41809 / .79936 |
| Paraphrase (12 / 12) | 3 / 3; 1.88726 / .96700 | 5 / 5; 1.21282 / .62938 | 5 / 5; 2.46612 / 1.07511 | 5 / 5; 2.87860 / 1.00580 | 5 / 5; 1.91409 / .84581 |
| Routine (52 / 52) | 24 / 24; 1.55577 / .72942 | 25 / 25; 1.32096 / .69069 | 37 / 37; 1.20572 / .50154 | 40 / 40; 1.04914 / .38657 | 42 / 42; .91330 / .37101 |

M10 native/reversed semantic choices flip on 35/96 S1 presentations; both orders are preferred on 43/96 and acceptable on 52/96. Both renderings are preferred for M9 on 12/48 cases, START 14/48, native 23/48, reversed 27/48, mean 25/48. Rendering and order sensitivity remain material.

## S2 saved summaries

All 16 references are singleton-acceptable, so preferred equals acceptable and proper n=16. S2 has no S1-style domain/format strata; none are invented.

| Predictor | Preferred = acceptable /16 | NLL | Summed Brier | Positive /4 | Negative /4 | Neutral /4 | Mixed /4 | Routine /12 | Awkward /4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M9 | 13 | .330177 | .205109 | 4 | 2 | 4 | 3 | 10 | 3 |
| START | 7 | 1.427232 | .743309 | 3 | 4 | 0 | 0 | 6 | 1 |
| M10 native | 14 | .495434 | .223829 | 4 | 4 | 4 | 2 | 10 | 4 |
| M10 reversed | 15 | .372715 | .127078 | 4 | 4 | 4 | 3 | 11 | 4 |
| M10 sum-normalized mean | 15 | .404202 | .151995 | 4 | 4 | 4 | 3 | 11 | 4 |

M10 flips once between orders; the mean matches reversed choices on all 16. These are validation-only, AI-authored and separately AI-reviewed cases, never training data.

## Three separate evidence layers

1. **Saved analysis/source pins:** [S1 report](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s1-v1/report.md), [results](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s1-v1/results.json), [pins](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s1-v1/pins.json); [S2 report](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s2-v1/report.md), [results](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s2-v1/results.json), [pins](../../artifacts/evaluation/final-sprint-20261112-01/analysis-s2-v1/pins.json). Pin/coverage checks support the analyzed bytes, not teacher-label truth.
2. **Independent arithmetic:** [numeric review](../../artifacts/evaluation/final-sprint-20261112-01/diagnostic-numeric-review-v1/report.md) checked 18,246 leaves, maximum absolute delta 0 at tolerance 1e-12, with counts/identities exact. It independently recomputed saved aggregates, not new predictions. Its read scope excluded the S2 manifest, so that manifest hash was not independently verified there. Narrative causal claims were not certified.
3. **Execution binding:** [binding review](../../artifacts/evaluation/final-sprint-20261112-01/diagnostic-binding-review-v1/report.md) supports five saved jobs' source/configuration, receipts, ordered outputs, closure and M9 same-pass token capture. It is not an independent weight/tensor/tokenizer-asset audit or scientific approval. Original START binding uses retained path/configuration and strict loader; M9/M10 weight identities reuse saved inventory digests, not fresh weight rehashes. Captured token rows have positional option correspondence, not explicit per-row option IDs; no SDK comparison was performed.

The five reviewed jobs account for 56 charge seconds; ledger 60/600 also includes a separate unreviewed four-second Research probe. CPU FP32/four-thread and closure claims are saved execution evidence; sampled pressure/memory checks are not continuous resource proofs. M10 scores are relative conditional option probabilities, not calibrated confidence or full-vocabulary probabilities.

## Publication boundary

The [prospective plan summary](final-sprint-plan.md) records chronology, fixed gates, release qualification and pending operational work. S1/S2 diagnostics do not substitute for reserved64 or retained-task gates. This publication transcribes saved evidence without rereading protected references, source cases or weights or rerunning arithmetic. Package builds are separate from scientific review; no software tests or lint were run.
