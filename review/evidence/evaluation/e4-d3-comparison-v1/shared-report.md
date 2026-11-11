# D3 originals: six predictors

Reference: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-d3-released-boundary-v1/reference/validation.jsonl`; SHA-256 `6d5d8ce3ea1b85f131b5926c4fe724083b7e03c6e6360adfe4f4a0dc3c97d3ae`.
96 rows / 48 declared source groups. Rows and reversals are not independent observations.

## Coverage and quality

Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.

| Predictor | Valid/total | Conditional agreement | All-row success | Log loss | Missing/invalid/duplicate | Extra IDs | Unidentifiable | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minilm_start | 96/96 | 27/96 | 27/96 | 1.316860 | 0/0/0 | 0 | 0 | 0 |
| minilm_trained | 96/96 | 31/96 | 31/96 | 1.342824 | 0/0/0 | 0 | 0 | 0 |
| msmarco_start | 96/96 | 30/96 | 30/96 | 1.347340 | 0/0/0 | 0 | 0 | 0 |
| msmarco_trained | 96/96 | 26/96 | 26/96 | 1.355202 | 0/0/0 | 0 | 0 | 0 |
| uniform | 96/96 | 27/96 | 27/96 | 1.317371 | 0/0/0 | 0 | 0 | 96 |
| lexical | 96/96 | 24/96 | 24/96 | 1.319115 | 0/0/0 | 0 | 0 | 59 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| programmatic | data-d3-seen-rules-v1-geometry-original-20261112-704931 | rule_verified | not applicable | 48 | 24 | rule_application |
| programmatic | data-d3-seen-rules-v1-ordering-r2 | rule_verified | not applicable | 48 | 24 | rule_application |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | minilm_start | minilm_trained | msmarco_start | msmarco_trained | uniform | lexical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rule_verified | 96 | 48 | rule_verified_accuracy | 27/96 · 1.316860 | 31/96 · 1.342824 | 30/96 · 1.347340 | 26/96 · 1.355202 | 27/96 · 1.317371 | 24/96 · 1.319115 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | minilm_start | minilm_trained | msmarco_start | msmarco_trained | uniform | lexical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rule_application | 96 | 48 | rule_verified_accuracy | 27/96 · 1.316860 | 31/96 · 1.342824 | 30/96 · 1.347340 | 26/96 · 1.355202 | 27/96 · 1.317371 | 24/96 · 1.319115 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | minilm_start | minilm_trained | msmarco_start | msmarco_trained | uniform | lexical |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data:d3-seen-rules-v1:cooldown:p01 | 2 | 1 | rule_verified_accuracy | 2/2 · 1.385282 | 1/2 · 1.218623 | 0/2 · 1.430749 | 1/2 · 1.405664 | 0/2 · 1.386294 | 1/2 · 1.319513 |
| data:d3-seen-rules-v1:cooldown:p02 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386202 | 0/2 · 1.624007 | 0/2 · 1.433930 | 0/2 · 1.633823 | 1/2 · 1.386294 | 0/2 · 1.432149 |
| data:d3-seen-rules-v1:cooldown:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386580 | 0/2 · 1.704610 | 0/2 · 1.483602 | 0/2 · 1.699277 | 1/2 · 1.386294 | 0/2 · 1.456756 |
| data:d3-seen-rules-v1:cooldown:p04 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.385518 | 0/2 · 1.825492 | 0/2 · 1.364732 | 0/2 · 1.754973 | 2/2 · 1.386294 | 0/2 · 1.439023 |
| data:d3-seen-rules-v1:cooldown:p05 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386787 | 0/2 · 1.585216 | 1/2 · 1.404056 | 0/2 · 1.574883 | 1/2 · 1.386294 | 0/2 · 1.458953 |
| data:d3-seen-rules-v1:cooldown:p06 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386115 | 0/2 · 1.628729 | 1/2 · 1.382565 | 0/2 · 1.581807 | 0/2 · 1.386294 | 0/2 · 1.397456 |
| data:d3-seen-rules-v1:coordinates:p01 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.385266 | 0/2 · 1.370052 | 1/2 · 1.332678 | 1/2 · 1.379729 | 0/2 · 1.386294 | 0/2 · 1.370148 |
| data:d3-seen-rules-v1:coordinates:p02 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.387002 | 1/2 · 1.444712 | 0/2 · 1.423154 | 1/2 · 1.386739 | 2/2 · 1.386294 | 1/2 · 1.427597 |
| data:d3-seen-rules-v1:coordinates:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.387209 | 0/2 · 1.362851 | 0/2 · 1.394421 | 1/2 · 1.382077 | 1/2 · 1.386294 | 1/2 · 1.353078 |
| data:d3-seen-rules-v1:coordinates:p04 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.386062 | 0/2 · 1.395100 | 0/2 · 1.407174 | 0/2 · 1.393099 | 0/2 · 1.386294 | 0/2 · 1.405586 |
| data:d3-seen-rules-v1:coordinates:p05 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.387524 | 0/2 · 1.375943 | 1/2 · 1.375676 | 0/2 · 1.382834 | 0/2 · 1.386294 | 1/2 · 1.339029 |
| data:d3-seen-rules-v1:coordinates:p06 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.387283 | 2/2 · 1.287299 | 0/2 · 1.360185 | 0/2 · 1.382476 | 0/2 · 1.386294 | 0/2 · 1.337529 |
| data:d3-seen-rules-v1:discount:p01 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.384991 | 2/2 · 0.934863 | 2/2 · 1.092143 | 0/2 · 1.383851 | 1/2 · 1.386294 | 1/2 · 1.386294 |
| data:d3-seen-rules-v1:discount:p02 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386474 | 0/2 · 1.577594 | 1/2 · 1.417736 | 2/2 · 1.334363 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:discount:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386913 | 0/2 · 1.629833 | 1/2 · 1.284263 | 2/2 · 1.353109 | 0/2 · 1.386294 | 0/2 · 1.418018 |
| data:d3-seen-rules-v1:discount:p04 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.386231 | 1/2 · 1.240900 | 0/2 · 1.439885 | 0/2 · 1.432174 | 1/2 · 1.386294 | 1/2 · 1.358159 |
| data:d3-seen-rules-v1:discount:p05 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.382307 | 1/2 · 1.384416 | 1/2 · 1.498794 | 1/2 · 1.394941 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:discount:p06 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.386488 | 1/2 · 1.451030 | 1/2 · 1.397730 | 0/2 · 1.390070 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:fifo:p01 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.097751 | 1/2 · 1.015808 | 0/2 · 1.099373 | 2/2 · 1.087244 | 1/2 · 1.098612 | 1/2 · 1.110295 |
| data:d3-seen-rules-v1:fifo:p02 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.098460 | 2/2 · 0.969363 | 1/2 · 1.107831 | 2/2 · 1.081476 | 0/2 · 1.098612 | 2/2 · 1.056562 |
| data:d3-seen-rules-v1:fifo:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.098568 | 1/2 · 0.999101 | 1/2 · 1.094025 | 1/2 · 1.078553 | 2/2 · 1.098612 | 2/2 · 1.087953 |
| data:d3-seen-rules-v1:fifo:p04 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.100576 | 1/2 · 1.060936 | 0/2 · 1.107979 | 1/2 · 1.090133 | 1/2 · 1.098612 | 1/2 · 1.072656 |
| data:d3-seen-rules-v1:fifo:p05 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.095447 | 1/2 · 0.743201 | 0/2 · 1.127559 | 0/2 · 1.101612 | 0/2 · 1.098612 | 1/2 · 1.061882 |
| data:d3-seen-rules-v1:fifo:p06 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.095423 | 0/2 · 1.232085 | 0/2 · 1.151261 | 1/2 · 1.114855 | 0/2 · 1.098612 | 0/2 · 1.113468 |
| data:d3-seen-rules-v1:lexicographic:p01 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.383148 | 1/2 · 1.405326 | 1/2 · 1.347238 | 0/2 · 1.414538 | 1/2 · 1.386294 | 1/2 · 1.386294 |
| data:d3-seen-rules-v1:lexicographic:p02 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.379892 | 1/2 · 1.344445 | 1/2 · 1.324003 | 1/2 · 1.364352 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:lexicographic:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.388774 | 0/2 · 1.431779 | 1/2 · 1.395427 | 0/2 · 1.390831 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:lexicographic:p04 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.383678 | 1/2 · 1.423763 | 0/2 · 1.397759 | 0/2 · 1.376579 | 1/2 · 1.386294 | 1/2 · 1.386294 |
| data:d3-seen-rules-v1:lexicographic:p05 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.378852 | 1/2 · 1.393283 | 1/2 · 1.358822 | 1/2 · 1.322960 | 1/2 · 1.386294 | 1/2 · 1.386294 |
| data:d3-seen-rules-v1:lexicographic:p06 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.382732 | 1/2 · 1.387699 | 1/2 · 1.357880 | 0/2 · 1.399095 | 1/2 · 1.386294 | 1/2 · 1.386294 |
| data:d3-seen-rules-v1:packs:p01 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.384934 | 1/2 · 1.390322 | 0/2 · 1.402419 | 1/2 · 1.363906 | 1/2 · 1.386294 | 1/2 · 1.373688 |
| data:d3-seen-rules-v1:packs:p02 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.387435 | 1/2 · 1.155546 | 1/2 · 1.336485 | 1/2 · 1.358235 | 0/2 · 1.386294 | 1/2 · 1.360895 |
| data:d3-seen-rules-v1:packs:p03 | 2 | 1 | rule_verified_accuracy | 2/2 · 1.094344 | 0/2 · 1.283194 | 1/2 · 0.991155 | 1/2 · 1.069944 | 1/2 · 1.098612 | 0/2 · 1.134586 |
| data:d3-seen-rules-v1:packs:p04 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.384709 | 1/2 · 1.429795 | 0/2 · 1.393617 | 1/2 · 1.375255 | 0/2 · 1.386294 | 0/2 · 1.375488 |
| data:d3-seen-rules-v1:packs:p05 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.241542 | 1/2 · 1.104435 | 1/2 · 1.191000 | 0/2 · 1.201114 | 2/2 · 1.242453 | 1/2 · 1.234918 |
| data:d3-seen-rules-v1:packs:p06 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.392130 | 2/2 · 1.207803 | 2/2 · 1.345841 | 0/2 · 1.381612 | 0/2 · 1.386294 | 0/2 · 1.426891 |
| data:d3-seen-rules-v1:rates:p01 | 2 | 1 | rule_verified_accuracy | 2/2 · 1.096171 | 0/2 · 1.157760 | 2/2 · 1.028916 | 0/2 · 1.106635 | 0/2 · 1.098612 | 0/2 · 1.098612 |
| data:d3-seen-rules-v1:rates:p02 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.096485 | 0/2 · 1.251898 | 1/2 · 1.086352 | 0/2 · 1.107451 | 1/2 · 1.098612 | 1/2 · 1.098612 |
| data:d3-seen-rules-v1:rates:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.394602 | 1/2 · 1.349843 | 1/2 · 1.365575 | 2/2 · 1.344852 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:rates:p04 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.099873 | 0/2 · 1.089870 | 0/2 · 1.061994 | 1/2 · 1.102576 | 0/2 · 1.098612 | 0/2 · 1.098612 |
| data:d3-seen-rules-v1:rates:p05 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.095868 | 1/2 · 1.190583 | 1/2 · 1.094733 | 0/2 · 1.119681 | 1/2 · 1.098612 | 1/2 · 1.098612 |
| data:d3-seen-rules-v1:rates:p06 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.388754 | 1/2 · 1.345026 | 1/2 · 1.408730 | 0/2 · 1.430815 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:rounding:p01 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.384639 | 1/2 · 1.516670 | 0/2 · 1.507363 | 0/2 · 1.452108 | 1/2 · 1.386294 | 1/2 · 1.407785 |
| data:d3-seen-rules-v1:rounding:p02 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.387437 | 0/2 · 1.781238 | 0/2 · 2.156095 | 0/2 · 1.631187 | 0/2 · 1.386294 | 0/2 · 1.424810 |
| data:d3-seen-rules-v1:rounding:p03 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.388871 | 0/2 · 1.390983 | 1/2 · 1.345081 | 0/2 · 1.537597 | 0/2 · 1.386294 | 0/2 · 1.386294 |
| data:d3-seen-rules-v1:rounding:p04 | 2 | 1 | rule_verified_accuracy | 0/2 · 1.389476 | 0/2 · 1.458931 | 0/2 · 2.026681 | 0/2 · 1.608261 | 0/2 · 1.386294 | 0/2 · 1.405768 |
| data:d3-seen-rules-v1:rounding:p05 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.384062 | 0/2 · 1.631984 | 0/2 · 1.727587 | 0/2 · 1.456618 | 1/2 · 1.386294 | 0/2 · 1.387960 |
| data:d3-seen-rules-v1:rounding:p06 | 2 | 1 | rule_verified_accuracy | 1/2 · 1.384396 | 1/2 · 1.271590 | 1/2 · 1.410077 | 1/2 · 1.333720 | 1/2 · 1.386294 | 1/2 · 1.352642 |

## Paired comparisons

Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.

| Left | Right | Common/total | Agreement delta | Left loss | Right loss | Loss delta | Loss delta status | Left-only correct | Right-only correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minilm_start | minilm_trained | 96/96 | -0.041667 | 1.316860 | 1.342824 | -0.025964 | finite | 15 | 19 |
| minilm_start | msmarco_start | 96/96 | -0.031250 | 1.316860 | 1.347340 | -0.030481 | finite | 16 | 19 |
| minilm_start | msmarco_trained | 96/96 | 0.010417 | 1.316860 | 1.355202 | -0.038342 | finite | 20 | 19 |
| minilm_start | uniform | 96/96 | 0.000000 | 1.316860 | 1.317371 | -0.000511 | finite | 16 | 16 |
| minilm_start | lexical | 96/96 | 0.031250 | 1.316860 | 1.319115 | -0.002255 | finite | 19 | 16 |
| minilm_trained | msmarco_start | 96/96 | 0.010417 | 1.342824 | 1.347340 | -0.004517 | finite | 18 | 17 |
| minilm_trained | msmarco_trained | 96/96 | 0.052083 | 1.342824 | 1.355202 | -0.012378 | finite | 18 | 13 |
| minilm_trained | uniform | 96/96 | 0.041667 | 1.342824 | 1.317371 | 0.025453 | finite | 19 | 15 |
| minilm_trained | lexical | 96/96 | 0.072917 | 1.342824 | 1.319115 | 0.023709 | finite | 12 | 5 |
| msmarco_start | msmarco_trained | 96/96 | 0.041667 | 1.347340 | 1.355202 | -0.007862 | finite | 19 | 15 |
| msmarco_start | uniform | 96/96 | 0.031250 | 1.347340 | 1.317371 | 0.029970 | finite | 23 | 20 |
| msmarco_start | lexical | 96/96 | 0.062500 | 1.347340 | 1.319115 | 0.028225 | finite | 22 | 16 |
| msmarco_trained | uniform | 96/96 | -0.010417 | 1.355202 | 1.317371 | 0.037831 | finite | 19 | 20 |
| msmarco_trained | lexical | 96/96 | 0.020833 | 1.355202 | 1.319115 | 0.036087 | finite | 15 | 13 |
| uniform | lexical | 96/96 | 0.031250 | 1.317371 | 1.319115 | -0.001744 | finite | 11 | 8 |

## Option-order sensitivity

Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.

No matching order reports supplied; no option-order conclusion.

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-d3-comparison-v1/comparison.json`; SHA-256 `652d21c03342bc835260f1ed28b161b5fc4f2b59ddce0a8efd4abf6e613dcb5f`.
