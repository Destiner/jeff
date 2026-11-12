# M9 gains overall and sentiment agreement, but held-out rules regress

**Fresh 12-epoch MS MARCO training improves new agreement 141→165/240 in each order versus M4's three-epoch endpoint, while rules fall 21→17/80 despite TRAIN rules rising 185→314/500.** All 165 new successes survive reversal with zero choice flips. M7 has better broad marginal agreement and proper scores, but only 138 new both-correct pairs and 101 flips. These are complementary measurements, not an architecture-cause claim or composite winner.

## Duration contrast and original comparator

M9 starts fresh from the original M4 MS MARCO pretrained cross-encoder **with its retained pretrained ranking head**, not from M4's trained checkpoint and not for twelve extra epochs. Measured M4 TRAIN sentiment 301/500 and rules 185/500 both activate the predeclared below-90% OR branch; that diagnostic threshold is not a product success bar. The fixed endpoint changes three→12 epochs, 1,125→4,500 updates and 4,500→18,000 presentations. Released data, original revision/head, seed 42, batch 4, cap 256, four threads, MPS, backbone/head LR 2e−5/5e−4 and AdamW settings remain unchanged. No intermediate checkpoint selection or validation sweep is used.

## Evidence scope and scoring

The unchanged E7 population contains 624 presentations: inherited 60 decisions/12 groups and new 240 decisions/170 groups, each original and reversed, plus 24 presentations of 12 already-paired probes (not reversed again). Each new predictor has 624 valid unique outputs, exact option coverage, finite probabilities, no invalid rows, zero target probabilities, infinite losses or exact raw top ties. Natural-log NLL and summed multiclass Brier use the established row-sum normalization only when absolute residual ≤1e−6; no clipping or score rescue.

All 12 earlier predictors and their scored reports/vectors remain byte-for-byte retained; only M8/M9 were newly scored. Context includes uniform, original/trained encoders, P3, failed M6 and M7. MiniLM's starting baseline is a pretrained encoder with a random scoring **head**, not a wholly random model; the original MS MARCO comparator retains its pretrained ranking head. [Complete recipes, references, source slices and raw evidence](../../artifacts/evaluation/e8-e9-analysis-v1/appendix.md) retain every baseline, including unfavorable contrasts.

## Broad held-out results

| Stratum | Order | Predictor | Agreement | NLL | Summed Brier |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | original | M4 pretrained start | 30/60 | 1.026878 | 0.552223 |
| inherited-v1 | original | M4 three-epoch | 42/60 | 0.712621 | 0.393343 |
| inherited-v1 | original | M9 duration | 43/60 | 0.673346 | 0.354056 |
| inherited-v1 | original | M7 | 45/60 | 0.576872 | 0.314785 |
| inherited-v1 | reversed | M4 pretrained start | 30/60 | 1.026878 | 0.552223 |
| inherited-v1 | reversed | M4 three-epoch | 42/60 | 0.712621 | 0.393343 |
| inherited-v1 | reversed | M9 duration | 43/60 | 0.673346 | 0.354056 |
| inherited-v1 | reversed | M7 | 44/60 | 0.552224 | 0.297745 |
| new-v2 | original | M4 pretrained start | 99/240 | 1.058568 | 0.581492 |
| new-v2 | original | M4 three-epoch | 141/240 | 0.917258 | 0.481392 |
| new-v2 | original | M9 duration | 165/240 | 0.699420 | 0.359766 |
| new-v2 | original | M7 | 171/240 | 0.669211 | 0.352959 |
| new-v2 | reversed | M4 pretrained start | 99/240 | 1.058568 | 0.581492 |
| new-v2 | reversed | M4 three-epoch | 141/240 | 0.917258 | 0.481392 |
| new-v2 | reversed | M9 duration | 165/240 | 0.699420 | 0.359766 |
| new-v2 | reversed | M7 | 170/240 | 0.618564 | 0.337570 |

## Family exceptions and order behavior

- Sentiment supplies most gains: inherited 17→20/20, new 43→70/80 in both orders. New sentiment NLL/Brier improve 1.249159/0.629578→0.399240/0.180991.
- Rules regress in **both orders**: inherited 7→5/20 (NLL 1.316504→1.594197; Brier 0.713169→0.880048); new 21→17/80 (1.411166→1.599282; 0.765541→0.861966). Zero flips do not make wrong choices correct.
- New intent agreement rises 77→78/80 and Brier improves, but NLL worsens 0.091450→0.099739. Inherited intent stays 18/20 with both NLL/Brier worsening 0.251990/0.158071→0.425182/0.182115; all apply in both orders.
- M4 pretrained / three-epoch / M9 both-correct totals are inherited 30/42/43 and new 99/141/165, all with zero flips; M7 is 39/138 with 21/101 flips. Rule both-correct is inherited 5/7/5 and new 15/21/17, versus M7 zero in each. Strict unique counts equal these counts for the untied maxima.

| Stratum | Order | Rule presentations | Strict first | Ties | Smallest raw margin |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | v2-original | 20 | 5 | 0 | 0.007501 |
| inherited-v1 | v2-reversed | 20 | 5 | 0 | 0.007501 |
| new-v2 | v2-original | 80 | 23 | 0 | 0.001645 |
| new-v2 | v2-reversed | 80 | 24 | 0 | 0.001645 |
| probes | probes-paired | 8 | 3 | 0 | 0.106399 |

These are M9 actual-input strict first-position counts, not prediction-list positions. All maxima are untied. This is not universal first-position collapse. Raw top-set overlap/target inclusion, uniform ties and deterministic input-order tie breaks are separately retained; overlap alone is not robust discrimination.

## Exact probe retention — not net gain alone

| Reference | Old both | New both | Retained | Gained | Lost |
| --- | --- | --- | --- | --- | --- |
| M4 pretrained start | 7 | 8 | 5 | 3 | 2 |
| M4 three-epoch | 5 | 8 | 4 | 4 | 1 |
| M7 | 9 | 8 | 6 | 2 | 3 |

Using the shared prefix `eval.validation.`:
- Versus original M4 pretrained start: gain `intent.02`, `sentiment.01`, `sentiment.02`; lose `intent.01`, `rule_application.02`.
- Versus M4 three-epoch: **retain four, gain four, lose one**. Gains `intent.02`, `sentiment.01`, `sentiment.02`, `rule_application.04`; loss `rule_application.02`. Rule pair totals stay 2/4 but membership changes.
- Versus M7: gain `rule_application.03`, `rule_application.04`; lose `intent.01`, `intent.03`, `rule_application.01`.

Presentation agreement pretrained/M4/M9/M7 is 14/10/16/21 out of 24; pair-macro NLL 1.453783/1.876464/1.362500/0.300645, Brier 0.651840/0.770313/0.425304/0.183459. M9's eight both-correct probe pairs remain below M7's nine.

## Fixed TRAIN fit — separate from held-out transfer

| Snapshot | Intent /500 | Sentiment /500 | Rules /500 | Total /1500 | NLL | Brier |
| --- | --- | --- | --- | --- | --- | --- |
| M4 MiniLM, 3 epochs | 497 | 348 | 238 | 1083 | 0.666250 | 0.370393 |
| M4 MS MARCO, 3 epochs | 499 | 301 | 185 | 985 | 0.726023 | 0.398785 |
| M9 MS MARCO, fresh 12 epochs | 500 | 500 | 314 | 1314 | 0.289057 | 0.164171 |

All snapshots cover the same 1,500 released rows/880 explicit groups, with no invalid rows or exact top ties. Versus M4 MS MARCO, M9 changes 434 choices: 361 agreement gains and 32 losses, all losses rules. Rules retain 153 successes, gain 161 and lose 32, leaving 186 disagreements. Rule TRAIN NLL/Brier remain 0.860594/0.490438. Better but incomplete fitting coexists with held-out rule regression; it is neither monotonic retention nor architectural incapacity. MiniLM context is not a matched architecture ablation.

## Genuine controls and execution limits

The [control review](../../artifacts/evaluation/e9-control-review-v1/findings.md) independently joins the released TRAIN references, probabilities, groups and provenance; verifies the conditional branch and config differences; and binds all 105 original M4 before-update parameter records exactly to M9's original start. All 105 endpoint records differ. Historical optimizer/parameter records are attestations, not independent native tensor/optimizer replay. Existing per-epoch shuffle construction is retained, not schedule-replayed. Intrinsic validation remains the original 300-row before/after observation (129→208 agreements), not an independent E9 score or checkpoint selector.

One learning attempt reaches 4,500 finite sequential online losses and 12 complete epochs. P7 uses the existing encoder loader plus frozen driver, with exact endpoint/input/source crosslinks: one fresh load, 156 completed batches of four, 624 valid outputs/2,390 probabilities, zero startup/canary, exit 0 and recorded closure. Payloads were not independently decoded or redundantly rehashed; small-file/source pins alone do not authenticate historical native execution.

Model's four-process time is 311.960 s plus P7 4.098 s = 316.058 s within 1,200 s. Separate 8 GiB RSS/driver guards and ≥2 GiB recommended headroom apply; largest internal Model lifetime RSS is 2,525,609,984 B, sampled driver 2,298,560,512 B, minimum sampled headroom 16,771,104,768 B. P7 lifetime RSS is 499,187,712 B and driver 1,108,017,152 B. These overlapping scopes are nonadditive; samples are not continuous true peaks and headroom is not physical free RAM. No causal speedup claim; additional actual/pending spend £0.

## Interpretation and limitations

Lead predeclared the unchanged references, source units and component-wise interpretation before execution (wave2050 for E8; wave2135 for E9). Evaluation adopted after outputs existed, approximately **00:31–00:43 UTC on 12 November 2026**: this is not an independent unseen-outcome freeze. Development is held out from TRAIN but reused across milestones; there is one seed. Reversed pairs, within-source rows and overlapping source dimensions are dependent, not independent replications.

Agreement with teacher/source labels is not independently established semantic truth. Released rule-verified labels retain same-alias limitations; probes include teacher-only references. No composite ranking, significance, calibration, automatic promotion or architectural-capacity conclusion follows. M7/M9 comparisons differ in pretraining, rendering, capacity and training history, not architecture alone.

## Independent quality review

The [independent raw-arithmetic review](../../artifacts/evaluation/e8-e9-quality-review-v1/findings.md) checks the 624 actual inputs for each new predictor, all 17,368 contrasts and 7,630 regression selections, exact probe membership, grouped means and raw choices. Its 459,085 initial comparisons and 19,838 supplemental checks leave no substantive discrepancy. All 792 initial mismatches were ordering-only differences in tied top-set lists; semantic set equality resolves them, with both original and corrective receipts preserved. It also verifies 108 retained bundle/report files and three comparison reports against E7 hashes. This is independent numerical review, not independent semantic relabeling.

[Executed two-predictor recipe](../../configs/evaluation/e8-e9-new-predictors-v1.json); publication index: [e9-m9-report-v1.json](../../manifests/evaluation/e9-m9-report-v1.json).

## Retained evidence and failures

[Immutable held-out analysis](../../artifacts/evaluation/e8-e9-analysis-v1/e9-report-candidate.md) and [appendix](../../artifacts/evaluation/e8-e9-analysis-v1/appendix.md) retain full family tables, every source regression, exact pair losses, positional means/population SD and raw vectors/top sets. Any lost agreement or worsened proper score flags a source regression even with net improvement; overlapping dimensions are not independent evidence. [Control evidence](../../artifacts/evaluation/e9-control-review-v1/findings.md) preserves the expired unstarted P7 reservation and renewed same unconsumed slot: no binding/ML occurred before expiry, so this is not an inference retry. No evaluation exceptions or failed learning retry are reported.
