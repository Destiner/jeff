# E13 later-four exploration: measured source-label agreement

**Exploration only. Independent arithmetic verified, with metadata and tool-output confinement qualifications.** All observations are after 06:30 and cannot add or replace confirmation candidates; optional slots remain zero forever. First-four raw scores and three external means are retained without rescoring.

## Scope and scoring

Each family has 100 source-native cases / 100 detected groups, each with native and exact reversed presentations, K=2. COPA is native dev; WinoGrande is native train_debiased. All new raw orders and derived means have 100/100 coverage per family, no missing/invalid/duplicate records. Brier is the sum across options, not divided by K. NLL uses natural logarithms. Agreement is with public source labels, not independently verified truth. No family- or phase-pooled headline.

## Raw per-family results

| Candidate | Family | Native agreement | Reversed agreement | Native NLL | Reversed NLL | Native Brier | Reversed Brier | Both / strict both | Flips / untied | Ties N/R |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M10seed7 | COPA | 76/100 | 76/100 | 0.532077595292 | 0.592198442711 | 0.333648308106 | 0.347542993830 | 62 / 62 | 28 / 28 | 0/0 |
| M10seed7 | WinoGrande | 58/100 | 51/100 | 0.773306653408 | 0.771639862120 | 0.542982633443 | 0.559214140401 | 39 / 39 | 31 / 31 | 0/0 |
| M11thirtyepochs | COPA | 53/100 | 53/100 | 1.233212812183 | 1.233212812183 | 0.679485361990 | 0.679485361990 | 53 / 53 | 0 / 0 | 0/0 |
| M11thirtyepochs | WinoGrande | 49/100 | 49/100 | 0.815320769798 | 0.815320769798 | 0.587144060972 | 0.587144060972 | 49 / 49 | 0 / 0 | 0/0 |
| M12headLR2e-4 | COPA | 57/100 | 44/100 | 1.095875592794 | 1.329815858892 | 0.706590289741 | 0.872523815789 | 1 / 1 | 99 / 99 | 0/0 |
| M12headLR2e-4 | WinoGrande | 50/100 | 55/100 | 0.775927916925 | 0.744071753393 | 0.569674007447 | 0.539945553133 | 23 / 23 | 59 / 59 | 0/0 |
| frozenP12NLI | COPA | 62/100 | 62/100 | 0.665831505645 | 0.665831505645 | 0.467189311245 | 0.467189311245 | 62 / 62 | 0 / 0 | 0/0 |
| frozenP12NLI | WinoGrande | 53/100 | 53/100 | 0.725240392155 | 0.725240392155 | 0.527688635009 | 0.527688635009 | 53 / 53 | 0 / 0 | 0/0 |

## Authorized semantic means

Only M10 and M12: validated normalized semantic-option probabilities, (native + reversed)/2, native-scored once; no new forwards. No M11/NLI mean. Rule authored before arithmetic but exploratory after component knowledge.

| Candidate | Family | Agreement | NLL | Brier | Native gained/lost | Reversed gained/lost | Strict-both retained | Mean ties |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| m10 mean | COPA | 79/100 | 0.465956851981 | 0.284517558990 | 8/5 | 9/6 | 62 | 0 |
| m10 mean | WinoGrande | 53/100 | 0.725642167324 | 0.523636402735 | 6/11 | 8/6 | 39 | 0 |
| m12 mean | COPA | 75/100 | 0.637511477719 | 0.446131969939 | 30/12 | 44/13 | 1 | 0 |
| m12 mean | WinoGrande | 48/100 | 0.710985500301 | 0.517889677725 | 12/14 | 13/20 | 23 | 0 |

Mean NLL/Brier convexity is relative to average component loss, not a guarantee of beating the better order, selected-choice improvement, or calibration. Mean transitions show gains and losses. K=2 reversal covers all permutations; invariant maximal sets do not establish truth, and first-option tie choice can change on reversal. Uniform reference is analytic expected agreement 0.5, NLL ln(2), Brier 0.5—not deterministic tie breaking. The frozen-reference first-input tie calculation gives COPA native/reversed 56/44 and WinoGrande 49/51 agreements per 100; both-correct and strict-both are zero, selected-choice flips are 100 but maximal sets remain unchanged. This is not a new model or inference pass.

## Binding and source review

Actual Model activation cab35438-c11f-4631-89e3-471d6b4abfbe; reservation E13-EXP-LATE4-20261112-0727; created 07:27:37.589209Z, ends 07:48:00Z, granted after confirmation closure. Ready-to-actual binding changes are only authority/reservation/window, with operation crosshash updates. Source snapshot 0d2edfe499ed1d45c5835efae54b95655c3a8771. Exact v4 cohort identifiers and owner-binding/3 were used. Wino train_debiased is the actual v4 schema; stale v3 enum correction remains only in e13-exploration-schema-correction-v1. Shared source-fidelity/group/identity pins retained. Raw vectors obey original semantic IDs and 1e-6 normalization tolerance. No model/tensor/tokenizer/binary access or rehash occurred in this analysis.

NLI uses MoritzLaurer/roberta-base-zeroshot-v2.0-c@d825e740e0c59881cf0b0b1481ccf726b6d65341, research profile 619365c8a158b7270d6f4aa29cab9c32f4c283d934b777d38647637ad04e2441; recorded weights 3568bb04b99e48d6e3086656534304644f3608312aa96c52edca7e6a7eeb0336 were not opened. Literal LF premise Context:\n{state}\n\nQuestion:\n{question}; hypothesis The correct answer is:\n{option_text}. The actual R10 head uses z0 − z1: native 0 entailment minus 1 not_entailment, then T1 softmax across choices—not binary sigmoid normalization. Saved complete, untruncated lengths under the unchanged 512-token maximum (800 pairs, observed max 62) and 100 batch4 native counter/journal agree. M12 consumes strict v2 checkpoint/proof, not a new arm.

Prospective NLI guard source SHA 988795a6e3603d65e530ca93ba2c2415fe690f98c20a4f7c94054d3dafa5790e checks recommended_max_memory()-driver_allocated_memory() >=2GiB before/after load/forward, separately from 8GiB RSS/lifetime RSS/driver. Initial pre-Torch sample truthfully not_checked. Explicit future-correct evidence bound to v4 NLI branch. Historical E14/P12 missing recommended guard remains qualified and does not establish compliance; no old624 payload read or rerun. Inherited 480s cooperative timer is not an extension: outer 180s/member and the same 1154s remaining applied. Full caps 1024 Qwen/256 encoder/512 NLI. Checked source and recorded samples do not provide general native OS-open trace, continuous memory peak, or tensor certification.

## Execution and cost

Four raw v4 scoring invocations and exactly two E16 derivations completed once each, exit 0; no scoring failures/retries, extra native forwards, ML children, or background tasks. Every scoring child ran in the Evaluation worktree with PYTHONPATH and JEFF_ARTIFACTS_DIR unset using the literal absolute scientific Python -B. Commands and timestamps are in raw-execution.json and mean-execution.json. One inspection command encountered an absent optional source-ready.json path before scoring; actual ready.json was reviewed instead; no scientific script was repaired or replayed.

Native delivery: every member 400 scored presentations/800 probabilities. M10/M12 each 3 startup +400 =403 calls; M11/NLI each 100 batch4 calls and zero startup. Fresh load/member, no failures/retries recorded. All eight totals 3200 scored/6400 probabilities/12 startup/2012 calls. Final native groups absent and outer exit 0 per delivery. Late whole outer 50.66s, conservative charge 52s; prior46 ->98/1200s cumulative, 1102s unused confers no authority. Separate confirmation 45/900 unchanged. Prepublication child intervals are not summed as whole cost. £0 actual/pending additional.

## Qualifications and handoff

No significance, promotion, architecture/capacity, calibration or truth claim. Unknown pretraining exposure, source-label quality and grouping under/overmerge limits remain. Reverse views are dependent observations. No confirmation was performed. Published aggregates contain no case IDs or vectors. Review schema inspections nevertheless printed dynamic identities into tool output, violating requested confinement; those logs are retained and the operational review is not an unqualified pass. Full-precision aggregates, retention, order agreement, total variation, tie/max-set diagnostics and source qualifications are in aggregate-summary.json. The [v2 independent review](../../artifacts/evaluation/e13-laterfour-quality-v2/report.md) verifies all 1,600 raw vectors / 3,200 values and 400 means / 800 values; 2,000 saved outcomes match within 1e-12, with exact discrete decisions and no failed arithmetic assertions. Maximum Brier-identity residual is 2.5673907444456745e-16. Sixteen matched baseline comparisons use saved outcomes, not old rescoring. Four coverage-diagnostic headers retain stale failure/unpublished flags despite full valid outcomes and successful receipts.

## Baseline context and tradeoffs

Compare the [historical first-four report](e13-exploration-firstfour.md), whose four-predictor publication remains unchanged in scope: no old output was rescored. P3 is the original decoder baseline; original MS MARCO START is the pretrained ranking head, not random initialization. P3 COPA native/reversed agreement was 70/74, NLL 0.618499/0.588458, Brier 0.416476/0.384963; WinoGrande 54/46, NLL 1.354071/1.755189, Brier 0.763717/0.901972. START COPA was 59/59, NLL 0.824028, Brier 0.551855; WinoGrande 54/54, NLL 0.726625, Brier 0.531860. These are same-case descriptive contexts, not fresh baseline executions or architecture-cause estimates.

M10 improves COPA agreement and native proper scores over P3, but its reversed COPA NLL is slightly worse (0.592198 vs 0.588458). WinoGrande proper scores improve over P3 yet remain worse than analytic uniform ln(2)/0.5. M11 is below START COPA agreement and substantially worse in proper scores; WinoGrande also regresses against START. M12 COPA is extremely order-sensitive (99 flips, one strict-both success); its WinoGrande source agreement is mixed across order and both proper scores remain worse than uniform. Frozen NLI improves COPA agreement/proper scores relative to START, but WinoGrande agreement is one lower and its proper scores remain worse than uniform. Different source/pretraining histories preclude causal attribution.

M10 mean improves COPA proper scores and agreement over either component but loses 5 native and 6 reversed agreements; its WinoGrande mean agreement is below native and its proper scores remain worse than uniform. M12 mean improves COPA aggregate metrics but still loses 12 native and 13 reversed agreements; WinoGrande mean agreement falls below both orders and proper scores remain worse than uniform. Means are checkpoint-plus-two-forward rules, not new trained models or free replacements. Across all five external means, 1,000 derived vectors reuse the same 200 exploration cases, not independent observations. Do not pool these with confirmation.

All results are post-06:30: confirmation remains permanently **four raw, zero optional**, even with M10's favorable COPA result. Unknown source-label/semantic truth, pretraining exposure and grouping under/overmerge remain; no calibration, significance, promotion or architecture-cause claim. The original v1 review stopped on a reference-versus-presentation ID schema error, not an established scientific discrepancy. Owner-authorized v2 corrected only reviewer join/schema scaffolding, preserving every original artifact; three successful independent arithmetic executions added checks without replaying a scorer or native job. V1 and v2 schema inspections printed selected dynamic identities into tool output; no later-review case text or probability values were printed. The owner also read the retained v1 error receipt containing one opaque ID. These are disclosed operational confinement failures, not changes to frozen selection or results. The v2 report's generic phrase “label/teacher agreement” is imprecise: these E13 targets are public source labels, not teacher labels. Offline owner packaging is a separate record, not numerical evidence.

## Publication evidence

- [e13-laterfour-analysis-v1/public-report.md](../../artifacts/evaluation/e13-laterfour-analysis-v1/public-report.md)
- [e13-laterfour-analysis-v1/aggregate-summary.json](../../artifacts/evaluation/e13-laterfour-analysis-v1/aggregate-summary.json)
- [e13-laterfour-analysis-v1/analysis-receipt.json](../../artifacts/evaluation/e13-laterfour-analysis-v1/analysis-receipt.json)
- [e13-laterfour-analysis-v1/binding-review.json](../../artifacts/evaluation/e13-laterfour-analysis-v1/binding-review.json)
- [e13-laterfour-analysis-v1/supplemental-source-review.json](../../artifacts/evaluation/e13-laterfour-analysis-v1/supplemental-source-review.json)
- [e13-laterfour-analysis-v1/raw-execution.json](../../artifacts/evaluation/e13-laterfour-analysis-v1/raw-execution.json)
- [e13-laterfour-analysis-v1/mean-execution.json](../../artifacts/evaluation/e13-laterfour-analysis-v1/mean-execution.json)
- [e13-exploration-m10-v1/public-summary.json](../../artifacts/evaluation/e13-exploration-m10-v1/public-summary.json)
- [e13-exploration-m11-v1/public-summary.json](../../artifacts/evaluation/e13-exploration-m11-v1/public-summary.json)
- [e13-exploration-m12-v1/public-summary.json](../../artifacts/evaluation/e13-exploration-m12-v1/public-summary.json)
- [e13-exploration-p12-nli-v1/public-summary.json](../../artifacts/evaluation/e13-exploration-p12-nli-v1/public-summary.json)
- [e16-e13-m10-v1/public-summary.json](../../artifacts/evaluation/e16-e13-m10-v1/public-summary.json)
- [e16-e13-m12-v1/public-summary.json](../../artifacts/evaluation/e16-e13-m12-v1/public-summary.json)

[Executed configuration](../../configs/evaluation/e13-exploration-laterfour-v1.json) and [publication manifest](../../manifests/evaluation/e13-exploration-laterfour-report-v1.json) retain bounded safe pins and actual commands. Embedded private pin metadata is not a claim of independent private-pin review.
