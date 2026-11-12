# E13 first-four exploration: source-label agreement and order sensitivity

## Scope and timing

This report describes the first four E13 predictors on the same 200 selected exploration cases: original P3, M7 seed42, original M4 MS MARCO pretrained-ranking-head START, and M9 twelve-epoch. It reports public-source-label agreement, not independently established semantic truth. The separate E16 section describes fixed arithmetic means of already saved predictions, not additional trained models or additional cases.

**The confirmation cohort is four mandatory raw predictors and zero optional predictors.** Although native inference finished at 06:26:55 UTC, no Evaluation quality result or eligible optional recommendation existed by the fixed 06:30 cutoff. All Evaluation scoring arithmetic and E16 means occurred afterward (raw scoring at 06:37:06–07; means at 06:37:51). Lead record `719f81b6`, published at 06:32:54, applied that fixed cutoff; it did not extend it. In particular, the later M7-mean COPA result of 81/100 cannot admit or substitute that predictor, and unselected means must not be applied to confirmation outputs.

This exploration analysis predates the separately reported confirmation results. The other four native exploration outputs (M10, M11, M12 and NLI), delivered at 07:32:35 UTC, now have a [separate measured later-four report](e13-exploration-laterfour.md), with independent arithmetic verified and metadata/confinement qualifications. No first-four output was rescored. This is a first-four exploration report, not a declaration that all E13 work is complete, a confirmation result, or a promotion recommendation. R12 remains a deferred queue, not a disproven direction.

## Population and prospective method

The [external protocol](e13-external-protocol.md) froze construction before external predictions; [D8's actual release](../data/d8-external-v1.md) distinguishes that plan from executed selection. The immutable token pool contained **800 cases**, 200 per surviving phase/family cell. All fitted both unchanged full renderers in both orders (encoder limit 256, decoder limit 1024; recorded maxima 54/89). Selection therefore took exactly the first 100 ranked representatives per cell, without refill, truncation or difficulty/label balancing. The exploration population here is **100 original COPA native-dev cases plus 100 WinoGrande native `train_debiased` cases**, each with two options and one detected component: 200 cases and 200 detected components in total. Both populations and all derivatives are permanently `validation_only_never_train`.

COPA uses the original author package at revision `14496936a3bed7b386aa8f517656d6f91e3fa77a`, under BSD-2-Clause, preserving original public item/gold associations. WinoGrande 1.1 uses the official archive at GCS generation `1600272206460138`, dataset CC BY 2.0, not its code's Apache license. Fixed task questions preserved native fact-bearing text, options, ordering and labels. SocialIQA remains quarantined because target-mapping proof was unresolved; its contexts remained grouping connectors. HellaSwag remains held for access/text-rights issues. See [source and rights evidence](../research/external-family-sources.md). Publisher grants support the qualified local assessment with attribution, not blanket upstream chain-of-title clearance or public dataset redistribution.

Grouping and ranks were input-only and prospective, including ineligible connectors, exact relations, the frozen lexical overlap predicate and Wino-specific relations, followed by whole-component exclusions and one representative per component. This report adopts the documented construction/release review; it does **not** claim a full grouping replay. Detected components do not establish semantic or statistical independence: undermerging, transitive overmerging and undocumented source relations remain possible. These task formats differ from recorded Jeff fine-tuning families, not necessarily from backbone pretraining or instruction tuning; pretraining exposure is unknown.

Across four predictors, native and reversed orders produce **1,600 scored presentations and 3,200 probability values**. They remain the same 200 cases, not 1,600 independent observations or independent reversal trials.

## Metrics and raw results

Agreement counts are out of 100 per family/order. NLL is mean negative natural-log target probability; Brier is mean summed squared error over both options, not divided by two. Valid vectors were normalized by their actual sums, without clipping. All native, reversed and paired coverages are 100/100, with no missing, invalid or duplicate outputs. Every raw and derived top set is a singleton: no exact ties. Consequently deterministic both-order agreement equals strict both-order agreement, and deterministic flips, untied flips and maximal-set changes coincide.

| Predictor | Family | Agreement native / reversed | NLL native / reversed | Brier native / reversed | Strict both /100 | Flips /100 |
| --- | --- | --- | --- | --- | ---: | ---: |
| P3 | COPA | 70 / 74 | 0.618499 / 0.588458 | 0.416476 / 0.384963 | 53 | 38 |
| P3 | WinoGrande | 54 / 46 | 1.354071 / 1.755189 | 0.763717 / 0.901972 | 6 | 88 |
| M7 | COPA | 63 / 55 | 0.848321 / 1.132566 | 0.545936 / 0.688282 | 19 | 80 |
| M7 | WinoGrande | 52 / 55 | 0.859559 / 0.809803 | 0.618401 / 0.580292 | 11 | 85 |
| MS MARCO START | COPA | 59 / 59 | 0.824028 / 0.824028 | 0.551855 / 0.551855 | 59 | 0 |
| MS MARCO START | WinoGrande | 54 / 54 | 0.726625 / 0.726625 | 0.531860 / 0.531860 | 54 | 0 |
| M9 | COPA | 57 / 57 | 0.842503 / 0.842503 | 0.556518 / 0.556518 | 57 | 0 |
| M9 | WinoGrande | 48 / 48 | 0.798804 / 0.798804 | 0.580877 / 0.580877 | 48 | 0 |

Raw aggregate sources: [P3](../../artifacts/evaluation/e13-exploration-p3-v1/public-summary.json), [M7](../../artifacts/evaluation/e13-exploration-m7-v1/public-summary.json), [MS MARCO START](../../artifacts/evaluation/e13-exploration-msmarco-start-v1/public-summary.json), [M9](../../artifacts/evaluation/e13-exploration-m9-v1/public-summary.json). Full-precision numbers are retained there and in the independent findings. Encoder summaries report zero order-aligned total variation and maximum probability change after scoring normalization, with invariant choices. This does not imply every saved raw vector or every derived floating-point representation is bit-identical.

P3 and M7 exhibit substantial order sensitivity, especially on WinoGrande. Among native source-label agreements, strict-both retention is P3 53/70 on COPA and 6/54 on WinoGrande; M7 19/63 and 11/52. The encoders retain all native agreements across order (START 59/59 and 54/54; M9 57/57 and 48/48). Order stability alone is neither truth nor calibration.

### Matched comparisons, not independent samples

Gains/losses below count matched source-label agreement changes for the challenger relative to its baseline. Strict-both comparisons use the same underlying paired cases.

| Challenger vs baseline | Family | Native gains / losses | Reversed gains / losses | Strict-both gains / losses |
| --- | --- | --- | --- | --- |
| M7 vs P3 | COPA | 7 / 14 | 3 / 22 | 1 / 35 |
| M7 vs P3 | WinoGrande | 42 / 44 | 48 / 39 | 8 / 3 |
| M9 vs MS MARCO START | COPA | 13 / 15 | 13 / 15 | 13 / 15 |
| M9 vs MS MARCO START | WinoGrande | 8 / 14 | 8 / 14 | 8 / 14 |

M7 has worse COPA proper scores than P3 in both orders, while improving WinoGrande mean proper scores despite mixed agreement changes. M9 does not improve this encoder starting baseline: its agreement and both proper scores are worse in each family/order. P3 is not the encoder's starting baseline. Per-case proper-score regressions and precise deltas remain in the [independent findings](../../artifacts/evaluation/e13-firstfour-quality-v1/findings.json); no pooled headline or composite conceals family/order regressions.

## E16: fixed semantic-option arithmetic means

E16 validates the saved pair once, aligns semantic option identities, and forms `(p + q) / 2`. Each derived native vector is scored once. There are no new forwards, raw rescoring, learned weights, temperature adjustment, tuning or imputation; an incomplete pair would stop derivation. The three checkpoint-plus-rule identities remain separate from their raw predictors. Their **600 derived native vectors reuse the same 200 cases across three predictors; they are not 600 new cases**.

| Derived predictor | Family | Agreement /100 | NLL | Brier | Raw strict-both successes retained |
| --- | --- | ---: | ---: | ---: | ---: |
| P3 mean | COPA | 76 | 0.531246 | 0.347284 | 53 / 53 |
| P3 mean | WinoGrande | 48 | 0.717833 | 0.518572 | 6 / 6 |
| M7 mean | COPA | 81 | 0.538144 | 0.358728 | 19 / 19 |
| M7 mean | WinoGrande | 47 | 0.704542 | 0.511899 | 11 / 11 |
| M9 mean | COPA | 57 | 0.842503 | 0.556518 | 57 / 57 |
| M9 mean | WinoGrande | 48 | 0.798804 | 0.580877 | 48 / 48 |

Derived aggregate sources: [P3 mean](../../artifacts/evaluation/e16-e13-p3-v1/public-summary.json), [M7 mean](../../artifacts/evaluation/e16-e13-m7-v1/public-summary.json), [M9 mean](../../artifacts/evaluation/e16-e13-m9-v1/public-summary.json).

| Mean vs component | Family | Gains / losses vs native | Gains / losses vs reversed |
| --- | --- | --- | --- |
| P3 mean | COPA | 11 / 5 | 12 / 10 |
| P3 mean | WinoGrande | 25 / 31 | 17 / 15 |
| M7 mean | COPA | 29 / 11 | 33 / 7 |
| M7 mean | WinoGrande | 12 / 17 | 24 / 32 |
| M9 mean | COPA | 0 / 0 | 0 / 0 |
| M9 mean | WinoGrande | 0 / 0 | 0 / 0 |

Averaging preserves every raw strict-both success here but can lose individual-order agreements. Both WinoGrande decoder means have NLL above `ln(2)` and summed Brier above `0.5`, the analytic uniform two-option proper-score references. The summaries' uniform random-choice expected agreement is `1/K = 0.5`; that differs from the frozen-reference first-option tie calculation: COPA native/reversed 56/44 and WinoGrande 49/51 per 100. The latter has deterministic both-correct and strict-both zero, with 100 selected-choice flips but unchanged maximal sets per family. This is an analytic reference calculation, not a new model or forward pass. P3 mean has better COPA NLL and Brier than M7 mean, but fewer source-label agreements (76 vs 81). M9 mean choices are unchanged, and scores are essentially unchanged; tiny floating-point effects must not be elevated into a stronger vector-identity claim.

The independent review reconstructed all 600 means and checked NLL convexity and the Brier identity `average component Brier − mean Brier = ||p−q||²/4`, with 1e-12 arithmetic allowance. Convexity compares against the **average component loss**, not the better order; it guarantees neither better choices nor calibration. With K=2, reversal spans the full permutation orbit, giving an invariant semantic mean/maximal set mathematically. A first-input tie breaker can still change selected semantic choice under exact ties; none occurred here. Serving this rule requires two forwards and constitutes a distinct checkpoint-plus-rule predictor, not a free replacement for a raw predictor. These post-cutoff means have no confirmation admission.

## Execution, review and limitations

- **Binding and provenance.** The [analysis report](../../artifacts/evaluation/e13-firstfour-analysis-v1/report.md), [analysis receipt](../../artifacts/evaluation/e13-firstfour-analysis-v1/analysis-receipt.json), [binding review](../../artifacts/evaluation/e13-firstfour-analysis-v1/binding-review.json) and [supplemental review](../../artifacts/evaluation/e13-firstfour-analysis-v1/supplemental-review.json) document the actual source-bound inputs (as recorded in those receipts), retained actual endpoint `837eaad1` rather than the Evaluation-copy endpoint, and unchanged semantic parameters. Recorded changes concerned reservations, activation and execution-window bindings, not source/result repair. Metadata and saved token-length/hash correspondence were reviewed; no tensor/load/tokenizer replay or complete native-open OS trace is claimed.
- **Numeric guard.** The parent's 1e-5 probability guard was weaker than Evaluation's 1e-6 requirement. All 1,600 actual raw vectors nevertheless passed the unchanged stricter guard. Maximum sum deviation was 8.940696716308594e-08 for every candidate/order. Non-unit rows normalized native/reversed were P3 166/172, M7 179/163, START 153/153 and M9 150/150. Roundoff is recorded rather than silently repaired at source.
- **Historical runtime.** Actual execution `490277de…` used one fresh process per model. Physical calls were 403 + 403 + 100 + 100 = 1,006, including six existing startup calls; physical-call accounting differs from the 1,600 scored presentations. No batch failures/retries were recorded. Whole-batch outer time was 44.02 seconds, conservatively charged as 46 seconds, leaving 1,154 of the historical 1,200-second allowance—not new authority to run anything. Recorded group-RSS maxima ranged from 488,275,968 to 3,092,987,904 bytes; other recorded RSS and headroom samples are in the binding review. Sampled RSS/MPS/driver observations and checked guards/closure are not continuous peaks, a kernel allocation hard limit or general resource-compliance certification. The prior E14/P12 missing recommended guard is separate, unchanged, and not a violation attributed to this batch.
- **Independent arithmetic.** The later [quality review](../../artifacts/evaluation/e13-firstfour-quality-v1/report.md), [final receipt](../../artifacts/evaluation/e13-firstfour-quality-v1/final-receipt.json) and [findings](../../artifacts/evaluation/e13-firstfour-quality-v1/findings.json) found no arithmetic, selected-case join, checked binding or pin discrepancies. It reconstructed 1,600 raw and 600 derived vectors independently; this supports the reviewed arithmetic, not ML execution or semantic truth. Its post-cutoff timing cannot change the cohort. The stored coverage-diagnostic headers retain their initial failure/unpublished flags despite successful complete outputs and final receipts; these stale metadata fields are not silently repaired.
- **Documentary corrections.** The initial exploration **emitter v1** raised `ValueError` on source identity before producing output. Emitter v2 corrected the literal to `train_debiased`; scorer v4 likewise corrected its expected literal before its first execution. There was no raw-scoring failure. The v3 documentary schema enum remained stale; only the separate [schema-correction supplement receipt](../../artifacts/evaluation/e13-exploration-schema-correction-v1/receipt.json) corrects that documentation, without rewriting source or results.
- **Interpretation and custody.** Source fidelity is not independent gold verification. Public pretraining exposure, source-label errors and grouping under/overmerge remain consequential limits. No old-624 retuning/replay, pooled composite, significance claim, calibration claim or promotion follows. This document contains only selected exploration aggregates, no private case IDs, text or vectors. Evidence locators—including private locators inside receipts—are not permission for Research to open payloads or protected material. No final payload was read in preparing this report. First-four arithmetic review is complete within its stated scope; the owner's separate offline packaging record is not numerical evidence.

## Publication evidence

The independent first-four review reports **15,652 numerical comparisons plus 2,478 supplemental checks and closing pins for 134 read-set files**, with no covered discrepancies. This covers first-four quality only, not all E13, all native execution or tensor replay.

Separate phased context: [locked four-raw confirmation](e13-confirmation-four-raw.md). [Executed configuration](../../configs/evaluation/e13-exploration-firstfour-v1.json) and [publication manifest](../../manifests/evaluation/e13-exploration-firstfour-report-v1.json) retain actual commands, source locks and byte/SHA-256 evidence pins. Artifact locators are not payload grants.
