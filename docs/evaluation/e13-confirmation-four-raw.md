# E13 locked confirmation — four raw profiles

100 cases /100 detected source groups per family, full coverage in both orders for every candidate. Agreement is with public source labels, not verified truth. NLL uses natural logs; Brier is summed over both options.

| Family | Candidate | Agreement native / reverse | NLL native / reverse | Brier native / reverse | Both / strict both | Flips | Ties native / reverse |
|---|---|---:|---:|---:|---:|---:|---:|
| commonsense_causal_choice | p3 | 72 / 72 | 0.6017 / 0.6113 | 0.3842 / 0.4077 | 58 / 58 | 28 | 0 / 0 |
| commonsense_causal_choice | m7 | 62 / 64 | 1.0534 / 0.8225 | 0.5798 / 0.5279 | 30 / 30 | 66 | 0 / 0 |
| commonsense_causal_choice | msmarco-start | 58 / 58 | 0.7431 / 0.7431 | 0.5215 / 0.5215 | 58 / 58 | 0 | 0 / 0 |
| commonsense_causal_choice | m9 | 50 / 50 | 0.8047 / 0.8047 | 0.5372 / 0.5372 | 50 / 50 | 0 | 0 / 0 |
| coreference_cloze | p3 | 48 / 49 | 1.6143 / 1.7188 | 0.8870 / 0.8918 | 5 / 5 | 87 | 0 / 0 |
| coreference_cloze | m7 | 48 / 47 | 0.9570 / 0.9770 | 0.6656 / 0.6570 | 5 / 5 | 85 | 0 / 0 |
| coreference_cloze | msmarco-start | 55 / 55 | 0.7080 / 0.7080 | 0.5141 / 0.5141 | 55 / 55 | 0 | 0 / 0 |
| coreference_cloze | m9 | 48 / 48 | 0.8005 / 0.8005 | 0.5854 / 0.5854 | 48 / 48 | 0 | 0 / 0 |

All agreement/both counts above are out of100. Analytic K2 uniform: expected agreement50%, NLL ln2=0.693147, summed Brier0.5; independent random draws both25%. Uniform probability ties are not strict singleton successes. The frozen-reference first-input tie calculation is analytic, not a new model: COPA native/reversed 50/50 and WinoGrande 53/47 agreements per 100; deterministic both and strict both are 0, semantic flips 100 per family.

## Baseline comparisons

P3 is the original decoder baseline; MSMARCO START is the original pretrained ranking head, not trained or random M4. The table preserves both baselines alongside their trained counterparts; these are descriptive comparisons, not architecture attribution.

## Native/reversed cost

P3/M7 each:403 physical forwards (200 native +200 reversed +3 startup). START/M9 each:100 batch4 native classifier calls (50 per order), zero startup. Each candidate has400 decision presentations/800 probabilities and one fresh load. Whole batch43.46s;45s charged to the separate900s confirmation allocation.855s unused is not authority. £0 actual/pending. No failure/retry.

## Review and limits

Independent raw arithmetic review: **numerical pass with metadata qualifications**, authoritative [closure report](../../artifacts/evaluation/e13-confirmation-quality-v1/closure-report.md) and [closure receipt](../../artifacts/evaluation/e13-confirmation-quality-v1/closure-receipt.json). Review covered 1,600 vectors / 3,200 values; all 9,600 recomputed numeric outcome fields were bit-exact, maximum difference 0.0. The 122,679 comparisons/checks include failed assertions and are not all passing checks. Four coverage headers remain stale (`binding_or_admission_failure`, `quality_published=false`) despite valid full coverage, final receipts and four exit-zero scoring executions. Original artifacts were not rewritten. The safe aggregate has already been delivered to R15; this review is not a delivery/build gate. Exact producer output copies, input joins/schemas, ordered option IDs, finite1e-6 probabilities, all source identities, admission lengths, actual grant, ready-to-actual authority-only mutations, source pins and recorded closure were reviewed. Encoder complete pair maxima match selected admission exactly in both orders.

- Source-label agreement, not independently verified truth.
- 100 cases and100 detected source groups per family; each has native and reversed dependent presentations. Unknown pretraining exposure and grouping under/overmerge limits.
- Four locked raw native T1 profiles only; zero optional; no pooled confirmation headline, crossphase pooling, selected-confidence calibration, significance, promotion or architecture-cause claim.
- Deterministic top choice breaks exact ties by first input option; strict both requires singleton target maxima in both orders.
- No complete OS native trace or weights/binary verification; memory evidence is reviewed guards and samples, not continuous MPS/group peaks.
- Actual frozen references retain validation_only_never_train with split final. v1 unexecuted; v2 corrected only package path and expected usage literal before scoring.
- Historical exploration46/1200 and P12 unrelated missing guard unchanged.

Start 2026-11-12T07:25:13Z; deadline 2026-11-12T07:33:13Z; end 2026-11-12T07:31:56.361590+00:00; elapsed 403.36s. All four scorer children returned exit0; no delegated helpers.
Scorer pinlock `080769c495bdd36b043e3e190754636455a9dcad16d46b64fcc60502e16899b1`; native freeze `f1fee32df63ac4bb359e09e63c93fb7f358b82f1`.

Candidate binding pins:
- p3: `f14a50bad493b706705253fee5a73e5fa33fa544664ab90bfe181afd0d0ef61a`; completed 2026-11-12T07:30:34.241187+00:00
- m7: `95215e4f5ac33b2ff8429a39d31b9d55972faf78ef5b063837600bf50c4f42a8`; completed 2026-11-12T07:30:34.296726+00:00
- msmarco-start: `39bcf63604c951a90c905bd99115063c76177893ffe2adbe67a45bf19919b929`; completed 2026-11-12T07:30:34.350458+00:00
- m9: `568c40e1db35c1c31a84397141029c5b8f156bd8aa1f97f8dcab57b10a6bd467`; completed 2026-11-12T07:30:34.404323+00:00

## Locked population and scientific interpretation

This is a separate confirmation phase: COPA native **test** and WinoGrande native **dev**, 100 cases and 100 detected groups each. Frozen references use split `final` while retaining `validation_only_never_train`; that storage label is not a training grant. The fixed 06:30 cutoff was published at 06:32:54: **four mandatory raw predictors, zero optional**. Native exploration ended 06:26:55, but all first-four quality and E16 means were later; none can alter admission. No confirmation means or unselected candidates were scored here. See [first-four exploration](e13-exploration-firstfour.md); the other four native exploration outputs now have a [separate measured report](e13-exploration-laterfour.md), independent arithmetic verified with metadata and confinement qualifications, without rescoring old results. The phases remain separate.

P3/M7 use conditional-answer-symbol T1; START/M9 use scalar T1. Each has 400 scored presentations / 800 values over the same 200 cases; four predictors total 1,600 presentations / 3,200 values, not independent samples. Startup calls are 3/3/0/0 and physical calls 403/403/100/100. All coverages are full and maxima untied. Values pass the unchanged 1e-6 sum guard, normalize by actual sum without clipping; the parent 1e-5 guard is weaker. Maximum recorded deviation is 8.940696716308594e-08. Encoder order-aligned scores/choices are invariant here, not proof of raw bit identity.

P3's COPA 72/72 source-label agreements exceed M7's 62/64 and have better NLL/Brier in both orders. M7 improves WinoGrande proper scores over P3 but not native agreement (48 each), while reversed agreement falls 49 to 47; both retain only 5 strict-both successes and flip 87/85 cases. M9 loses agreement against the actual pretrained-ranking-head START baseline in COPA (58 to 50) and WinoGrande (55 to 48), and worsens both proper scores in both families. Stability is not correctness. All WinoGrande proper scores are worse than analytic uniform ln(2)/0.5. The frozen-reference first-input calculation above is distinct from expected random agreement and is not a newly scored model. No architecture-cause inference follows.

Original source labels retain possible errors and are not independent semantic truth; unknown pretraining exposure remains. Prospective detected grouping can undermerge or overmerge and does not establish independence. Repeated orders are dependent measurements; no cross-phase or family pooled headline, selected-confidence calibration, significance or promotion claim is made. Source identities and recorded construction/admission checks support their specific reviewed coverage, not complete native OS-open or tokenizer/tensor replay.

### Matched agreement gains / losses

| Challenger vs baseline | Family | Native | Reversed | Strict both |
|---|---|---:|---:|---:|
| M7 vs P3 | COPA | 5 / 15 | 11 / 19 | 3 / 31 |
| M7 vs P3 | WinoGrande | 42 / 42 | 43 / 45 | 3 / 3 |
| M9 vs START | COPA | 11 / 19 | 11 / 19 | 11 / 19 |
| M9 vs START | WinoGrande | 7 / 14 | 7 / 14 | 7 / 14 |

These are matched dependent selected-case comparisons, not independent samples. No confirmation means were made.

## Corrections and evidence custody

The closure classifies 1,600 admission-locator rewrites with IDs, input pins, token counts, audit roles, untruncated flags and numerical values unchanged. A further 1,600 reviewer wrong-format assertions were classified against the observed `admission.json#/admission/{id}/{order}` form. These are descriptive fragments, not standard JSON Pointers; no automatic locator resolution was attempted. Original artifacts remain unchanged.

Custody deviation: one inspection command failed; initial reviewer helper tool output printed selected case IDs/content contrary to confinement. Harness logs were not edited; subsequent private proof stayed under final. No case content is reproduced here. This is not perfect custody or continuous review. Independent numerical review does not certify tensors, source resources, tokenizer/runtime/binary behavior, OS isolation, memory peaks or semantic truth. The original safe aggregate's PENDING status is historical and immutable; this report and manifest reflect the closed review.

Confirmation v1 was unexecuted: the wrong usage literal and package path were corrected in v2 before any scoring; originals remain retained. Earlier construction helpers had two relative-interpreter failures (exit 127), resolved by the actual Evaluation environment and followed by owner literal-absolute-interpreter source-integrity verification. These are construction/provenance qualifications, not scientific retries or repeated scoring.

Actual scores completed at 07:30:34 UTC. Activation `35408451` and runtime revision `f1fee32` identify actual authority, distinct from historical exploration. The 900-second confirmation allocation is separate: 43.46 seconds outer, 45 charged, 855 unused—not new authority. Memory/closure records are samples and checked guards, not continuous peaks or general compliance; unrelated historical P12 limitations remain unchanged.

[Executed configuration](../../configs/evaluation/e13-confirmation-four-raw-v1.json) and [publication manifest](../../manifests/evaluation/e13-confirmation-four-raw-report-v1.json) retain exact recorded commands, binding paths/hashes, scorer source locks, safe aggregate and reviewer receipt byte/SHA-256 pins. Private binding/reference pins are copied only as metadata already recorded outside final; publication preparation did not open final/D7 payloads or claim complete independent private-pin review. Path locators are not payload grants. The owner's offline build will supply a separate packaging record, not numerical evidence.

Safe evidence:
- [e13-confirmation-public-v1/report.md](../../artifacts/evaluation/e13-confirmation-public-v1/report.md)
- [e13-confirmation-public-v1/summary.json](../../artifacts/evaluation/e13-confirmation-public-v1/summary.json)
- [e13-confirmation-analysis-v1/binding-review.json](../../artifacts/evaluation/e13-confirmation-analysis-v1/binding-review.json)
- [e13-confirmation-analysis-v1/supplemental-review.json](../../artifacts/evaluation/e13-confirmation-analysis-v1/supplemental-review.json)
- [e13-confirmation-analysis-v1/scoring-execution.json](../../artifacts/evaluation/e13-confirmation-analysis-v1/scoring-execution.json)
- [e13-confirmation-analysis-v1/session-end.json](../../artifacts/evaluation/e13-confirmation-analysis-v1/session-end.json)
- [e13-confirmation-owner-integrity-v1/receipt.json](../../artifacts/evaluation/e13-confirmation-owner-integrity-v1/receipt.json)
- [e13-confirmation-lock-adoption-v1/receipt.json](../../artifacts/evaluation/e13-confirmation-lock-adoption-v1/receipt.json)
- [e13-confirmation-scoring-preparation-v2/README.md](../../artifacts/evaluation/e13-confirmation-scoring-preparation-v2/README.md)
- [e13-confirmation-scoring-preparation-v2/correction.json](../../artifacts/evaluation/e13-confirmation-scoring-preparation-v2/correction.json)
- [e13-confirmation-scoring-preparation-v2/pins.json](../../artifacts/evaluation/e13-confirmation-scoring-preparation-v2/pins.json)
- [e13-confirmation-scoring-preparation-v2/score-confirmation.py](../../artifacts/evaluation/e13-confirmation-scoring-preparation-v2/score-confirmation.py)
- [e13-confirmation-scoring-preparation-v2/source.diff](../../artifacts/evaluation/e13-confirmation-scoring-preparation-v2/source.diff)
