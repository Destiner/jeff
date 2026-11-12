# M8 stays near original P3 and far below M7

**The frozen-base six-row readout yields modest proper-score and order gains, not broad recovery.** New agreement moves P3→M8 from 129→130/240 original and 118→119 reversed, versus M7's 171/170. New-rule both-correct rises 4→6/80, while broad both-correct is 82→86 (M7 138). Limited head movement does not establish that frozen features lack capacity.

## Adaptation-scope contrast

Original P3 is the unadapted pinned Qwen2.5-0.5B-Instruct starting system. M7 adapted all original parameters; M8 instead freezes all **494,032,768** original parameters and trains one independent, bias-free FP32 A–F head with **5,376 scalars**. Both start from original P3, not a trained predecessor. M8 preserves M7's released data, materialized schedule, seed 42, nominal AdamW LR 2e−6, 375 updates and one 1,500-row epoch. Different optimization geometry means this is not a pure causal ablation. Export materializes an untied full-vocabulary output table, replacing only the six learned rows.

## Evidence scope and scoring

The unchanged E7 population contains 624 presentations: inherited 60 decisions/12 groups and new 240 decisions/170 groups, each original and reversed, plus 24 presentations of 12 already-paired probes (not reversed again). Each new predictor has 624 valid unique outputs, exact option coverage, finite probabilities, no invalid rows, zero target probabilities, infinite losses or exact raw top ties. Natural-log NLL and summed multiclass Brier use the established row-sum normalization only when absolute residual ≤1e−6; no clipping or score rescue.

All 12 earlier predictors and their scored reports/vectors remain byte-for-byte retained; only M8/M9 were newly scored. Context includes uniform, original/trained encoders, P3, failed M6 and M7. MiniLM's starting baseline is a pretrained encoder with a random scoring **head**, not a wholly random model; the original MS MARCO comparator retains its pretrained ranking head. [Complete recipes, references, source slices and raw evidence](../../artifacts/evaluation/e8-e9-analysis-v1/appendix.md) retain every baseline, including unfavorable contrasts.

## Broad held-out results

| Stratum | Order | Predictor | Agreement | NLL | Summed Brier |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | original | P3 original | 35/60 | 1.194707 | 0.599128 |
| inherited-v1 | original | M7 | 45/60 | 0.576872 | 0.314785 |
| inherited-v1 | original | M8 readout | 35/60 | 1.191182 | 0.594447 |
| inherited-v1 | reversed | P3 original | 34/60 | 0.966733 | 0.537541 |
| inherited-v1 | reversed | M7 | 44/60 | 0.552224 | 0.297745 |
| inherited-v1 | reversed | M8 readout | 34/60 | 0.959838 | 0.532837 |
| new-v2 | original | P3 original | 129/240 | 1.312350 | 0.633492 |
| new-v2 | original | M7 | 171/240 | 0.669211 | 0.352959 |
| new-v2 | original | M8 readout | 130/240 | 1.300082 | 0.630714 |
| new-v2 | reversed | P3 original | 118/240 | 1.410621 | 0.687402 |
| new-v2 | reversed | M7 | 170/240 | 0.618564 | 0.337570 |
| new-v2 | reversed | M8 readout | 119/240 | 1.380115 | 0.675376 |

## Family exceptions and order behavior

- New intent: P3→M8 original 74→74/80, reversed 67→68; sentiment 30→31 and 29→29; rules 25→25 and 22→22. Sentiment original Brier worsens 0.900924→0.907113 despite its one-case gain.
- Inherited family agreements are unchanged: intent 20/18, sentiment 9/10, rules 6/6 (original/reversed, each /20). Sentiment NLL worsens in both orders; reversed sentiment Brier and original rule Brier also worsen. Full family tables are retained in the linked analysis, not hidden by broad averages.
- Both-correct/choice flips: inherited P3 28/19, M7 39/21, M8 28/18; new P3 82/122, M7 138/101, M8 86/113. Rule both-correct: inherited 3→3/20 and new 4→6/80 versus P3; M7 is zero in both strata.

| Stratum | Order | Rule presentations | Strict first | Ties | Smallest raw margin |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | v2-original | 20 | 4 | 0 | 0.041534 |
| inherited-v1 | v2-reversed | 20 | 1 | 0 | 0.051596 |
| new-v2 | v2-original | 80 | 27 | 0 | 0.003985 |
| new-v2 | v2-reversed | 80 | 27 | 0 | 0.002705 |
| probes | probes-paired | 8 | 3 | 0 | 0.128905 |

Counts above are M8 strict first-position choices from actual input joins, not ID suffixes. M7 chooses first untied on all 200 inherited/new rule presentations. M8's exact raw maxima are untied everywhere, so strict unique both-correct equals ordinary both-correct. Uniform top-set inclusion/overlap is not discrimination; tie-broken choices and raw top sets remain separate in the appendix.

## Exact probe retention

| Reference | Old both | New both | Retained | Gained | Lost |
| --- | --- | --- | --- | --- | --- |
| P3 original | 9 | 9 | 9 | 0 | 0 |
| M7 | 9 | 9 | 7 | 2 | 2 |

Against P3, no both-correct pair is gained or lost. Against M7, gains are `eval.validation.rule_application.02` and `eval.validation.rule_application.03`; losses are `eval.validation.sentiment.02` and `eval.validation.sentiment.04`. Presentation agreement P3/M7/M8 is 20/21/19 out of 24; pair-macro NLL 0.534509/0.300645/0.528313 and Brier 0.284486/0.183459/0.269743. Equal nine-pair totals do not mean equal membership.

## Fixed TRAIN fit — not held-out transfer

| Family | Agreement START→END | NLL START→END | Brier START→END |
| --- | --- | --- | --- |
| Overall /1500 | 805→804 | 1.357724→1.332200 | 0.650797→0.640291 |
| Intent /500 | 442→441 | 0.396153→0.370048 | 0.187359→0.176579 |
| Sentiment /500 | 179→179 | 2.019892→1.997229 | 0.923670→0.916429 |
| Rules /500 | 184→184 | 1.657126→1.629324 | 0.841362→0.827866 |

75 choices change: **16 wrong→right, 17 right→wrong**. Producer-attested head movement is L2 0.005199586 (0.45206% of initial norm), maximum absolute 0.000294833; all 375 preclip norms exceed clip 1. Better probability fit without improved ranking is not semantic success or a capacity verdict. Retained M7 TRAIN context is 1,130/1,500, including 176/500 rules; it is not rerun here.

## Execution controls and numerical boundaries

The [control review](../../artifacts/evaluation/e8-control-review-v1/findings.md) binds saved original-before/after/export maps, fixed buffers, exact schedule, unchanged non-answer rows and learned-row placement. START TRAIN vectors are byte-identical to original-base M7 START; all 1,500 START and END conditional bindings have max logit/probability differences 0/0 and identical top sets. END reference uses the actual full stock `lm_head` on the same hidden states, not a surrogate projection. These historical forwards and optimizer resets remain producer-attested, not independently tensor-replayed.

P6 actually performs a fresh strict stock reload: saved untied configuration, both full tensors, empty load diagnostics and observed disjoint CPU storage/distinct MPS handles. It completes 627 forwards: three unscored startups plus the 624 development presentations, exit 0 and recorded process closure. This establishes reload/execution, **not a measured fresh small-head-versus-stock numerical comparison on every development case**; that comparison remains unmeasured. Header/maps/source evidence is not independent tensor decoding or arbitrary external-Metal alias proof.

Model process time is 246.449 s (252.999 s including audits, within 2,700 s); separate P6 is 36.246 s within 310 s. Model lifetime RSS is 3,367,747,584 B and sampled MPS driver maximum 2,772,107,264 B; P6 sampled driver is 2,768,961,536 B. Separate 16 GiB Model and 8 GiB Runtime guards and ≥2 GiB recommended headroom apply. Overlapping memory scopes are nonadditive, samples are not true peaks, and recommended headroom is not free RAM. Added output-table payload is not allocator peak; no causal speedup is claimed. Additional actual/pending spend £0.

## Interpretation and limitations

Lead predeclared the unchanged references, source units and component-wise interpretation before execution (wave2050 for E8; wave2135 for E9). Evaluation adopted after outputs existed, approximately **00:31–00:43 UTC on 12 November 2026**: this is not an independent unseen-outcome freeze. Development is held out from TRAIN but reused across milestones; there is one seed. Reversed pairs, within-source rows and overlapping source dimensions are dependent, not independent replications.

Agreement with teacher/source labels is not independently established semantic truth. Released rule-verified labels retain same-alias limitations; probes include teacher-only references. No composite ranking, significance, calibration, automatic promotion or architectural-capacity conclusion follows. M7/M9 comparisons differ in pretraining, rendering, capacity and training history, not architecture alone.

## Independent quality review

The [independent raw-arithmetic review](../../artifacts/evaluation/e8-e9-quality-review-v1/findings.md) checks the 624 actual inputs for each new predictor, all 17,368 contrasts and 7,630 regression selections, exact probe membership, grouped means and raw choices. Its 459,085 initial comparisons and 19,838 supplemental checks leave no substantive discrepancy. All 792 initial mismatches were ordering-only differences in tied top-set lists; semantic set equality resolves them, with both original and corrective receipts preserved. It also verifies 108 retained bundle/report files and three comparison reports against E7 hashes. This is independent numerical review, not independent semantic relabeling.

[Executed two-predictor recipe](../../configs/evaluation/e8-e9-new-predictors-v1.json); publication index: [e8-m8-report-v1.json](../../manifests/evaluation/e8-m8-report-v1.json).

## Retained evidence and failures

[Immutable held-out analysis](../../artifacts/evaluation/e8-e9-analysis-v1/e8-report-candidate.md) and [appendix](../../artifacts/evaluation/e8-e9-analysis-v1/appendix.md) retain full family tables, all source regressions, exact pair losses, positional means/population SD, raw vectors/top sets and pins. Source regression flags include any lost agreement or worsened proper score, even with net gains; overlapping dimensions must not be summed. [Control evidence and preserved failures](../../artifacts/evaluation/e8-control-review-v1/findings.md) distinguish pre-load checker/refreeze corrections and incomplete sentinels from learning attempts, and retain review invocation errors. No extra failed learning run is inferred.
