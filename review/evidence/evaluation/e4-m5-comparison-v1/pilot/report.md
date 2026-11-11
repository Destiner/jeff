# E4 M5 LR control — pilot

Reference: `/Users/destiner/Code/jeff/artifacts/evaluation/data-pilot-v1/validation.jsonl`; SHA-256 `8d4cd2e29f8b9a5dfd0b5ae4408b4f06b986eb2b2631868a0158d8dcdfc1559b`.
60 rows / 12 declared source groups. Rows and reversals are not independent observations.

## Coverage and quality

Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.

| Predictor | Valid/total | Conditional agreement | All-row success | Log loss | Missing/invalid/duplicate | Extra IDs | Unidentifiable | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform | 60/60 | 17/60 | 17/60 | 1.378765 | 0/0/0 | 0 | 0 | 60 |
| lexical | 60/60 | 29/60 | 29/60 | 1.323710 | 0/0/0 | 0 | 0 | 14 |
| m3-pretrained-start | 60/60 | 30/60 | 30/60 | 1.026878 | 0/0/0 | 0 | 0 | 0 |
| m3-historical-trained | 60/60 | 40/60 | 40/60 | 0.793701 | 0/0/0 | 0 | 0 | 0 |
| m2-context | 60/60 | 35/60 | 35/60 | 0.855288 | 0/0/0 | 0 | 0 | 0 |
| m5-pretrained-start | 60/60 | 30/60 | 30/60 | 1.026878 | 0/0/0 | 0 | 0 | 0 |
| m5-low-head-lr | 60/60 | 40/60 | 40/60 | 0.794525 | 0/0/0 | 0 | 0 | 0 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| programmatic | data-pilot-v1/rule_application/original-rule-job-r1 | rule_verified | not applicable | 20 | 2 | rule_application |
| teacher | data-pilot-v1/sentiment-r2/from/jeff-data-pilot-v1-sentiment-agent-r1 | teacher | gpt-sol | 20 | 5 | sentiment |
| teacher | data:pilot-v1:intent:agent-authoring-r1 | teacher | openai/gpt-sol | 20 | 5 | intent |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | uniform | lexical | m3-pretrained-start | m3-historical-trained | m2-context | m5-pretrained-start | m5-low-head-lr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rule_verified | 20 | 2 | rule_verified_accuracy | 6/20 · 1.379841 | 8/20 · 1.373712 | 5/20 · 1.366589 | 7/20 · 1.362848 | 4/20 · 1.431825 | 5/20 · 1.366589 | 7/20 · 1.358932 |
| teacher | 40 | 10 | teacher_agreement | 11/40 · 1.378227 | 21/40 · 1.298709 | 25/40 · 0.857023 | 33/40 · 0.509127 | 31/40 · 0.567019 | 25/40 · 0.857023 | 33/40 · 0.512322 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | uniform | lexical | m3-pretrained-start | m3-historical-trained | m2-context | m5-pretrained-start | m5-low-head-lr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent | 20 | 5 | teacher_agreement | 6/20 · 1.370160 | 16/20 · 1.216725 | 18/20 · 0.381560 | 19/20 · 0.211817 | 20/20 · 0.067838 | 18/20 · 0.381560 | 19/20 · 0.211776 |
| rule_application | 20 | 2 | rule_verified_accuracy | 6/20 · 1.379841 | 8/20 · 1.373712 | 5/20 · 1.366589 | 7/20 · 1.362848 | 4/20 · 1.431825 | 5/20 · 1.366589 | 7/20 · 1.358932 |
| sentiment | 20 | 5 | teacher_agreement | 5/20 · 1.386294 | 5/20 · 1.380693 | 7/20 · 1.332485 | 14/20 · 0.806437 | 11/20 · 1.066200 | 7/20 · 1.332485 | 14/20 · 0.812867 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | uniform | lexical | m3-pretrained-start | m3-historical-trained | m2-context | m5-pretrained-start | m5-low-head-lr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data:pilot-v1:intent:g26 | 4 | 1 | teacher_agreement | 3/4 · 1.370160 | 3/4 · 1.193414 | 4/4 · 0.019332 | 4/4 · 0.000795 | 4/4 · 0.002241 | 4/4 · 0.019332 | 4/4 · 0.000548 |
| data:pilot-v1:intent:g27 | 4 | 1 | teacher_agreement | 0/4 · 1.370160 | 2/4 · 1.305617 | 3/4 · 0.547240 | 4/4 · 0.194188 | 4/4 · 0.163599 | 3/4 · 0.547240 | 4/4 · 0.195014 |
| data:pilot-v1:intent:g28 | 4 | 1 | teacher_agreement | 1/4 · 1.370160 | 4/4 · 1.191942 | 4/4 · 0.000561 | 4/4 · 0.001515 | 4/4 · 0.161615 | 4/4 · 0.000561 | 4/4 · 0.001058 |
| data:pilot-v1:intent:g29 | 4 | 1 | teacher_agreement | 1/4 · 1.370160 | 3/4 · 1.186473 | 3/4 · 1.216777 | 3/4 · 0.857740 | 4/4 · 0.006365 | 3/4 · 1.216777 | 3/4 · 0.858315 |
| data:pilot-v1:intent:g30 | 4 | 1 | teacher_agreement | 1/4 · 1.370160 | 4/4 · 1.206181 | 4/4 · 0.123892 | 4/4 · 0.004845 | 4/4 · 0.005371 | 4/4 · 0.123892 | 4/4 · 0.003948 |
| data:pilot-v1:rule_application:g11 | 10 | 1 | rule_verified_accuracy | 3/10 · 1.328758 | 3/10 · 1.319537 | 2/10 · 1.377242 | 2/10 · 1.427479 | 2/10 · 1.334079 | 2/10 · 1.377242 | 2/10 · 1.414830 |
| data:pilot-v1:rule_application:g12 | 10 | 1 | rule_verified_accuracy | 3/10 · 1.430923 | 5/10 · 1.427887 | 3/10 · 1.355935 | 5/10 · 1.298218 | 2/10 · 1.529570 | 3/10 · 1.355935 | 5/10 · 1.303034 |
| data:pilot-v1:sentiment:g26 | 4 | 1 | teacher_agreement | 1/4 · 1.386294 | 1/4 · 1.384758 | 1/4 · 1.306202 | 4/4 · 0.581017 | 3/4 · 0.683696 | 1/4 · 1.306202 | 4/4 · 0.588122 |
| data:pilot-v1:sentiment:g27 | 4 | 1 | teacher_agreement | 0/4 · 1.386294 | 0/4 · 1.398288 | 1/4 · 1.402344 | 3/4 · 0.677976 | 3/4 · 0.763866 | 1/4 · 1.402344 | 3/4 · 0.670005 |
| data:pilot-v1:sentiment:g28 | 4 | 1 | teacher_agreement | 1/4 · 1.386294 | 2/4 · 1.368146 | 3/4 · 1.244544 | 1/4 · 1.004299 | 3/4 · 1.029880 | 3/4 · 1.244544 | 1/4 · 1.002987 |
| data:pilot-v1:sentiment:g29 | 4 | 1 | teacher_agreement | 2/4 · 1.386294 | 0/4 · 1.386543 | 0/4 · 1.420853 | 3/4 · 0.962462 | 1/4 · 1.369133 | 0/4 · 1.420853 | 3/4 · 0.976762 |
| data:pilot-v1:sentiment:g30 | 4 | 1 | teacher_agreement | 1/4 · 1.386294 | 2/4 · 1.365730 | 2/4 · 1.288482 | 3/4 · 0.806433 | 1/4 · 1.484424 | 2/4 · 1.288482 | 3/4 · 0.826456 |

## Paired comparisons

Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.

| Left | Right | Common/total | Agreement delta | Left loss | Right loss | Loss delta | Loss delta status | Left-only correct | Right-only correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform | lexical | 60/60 | -0.200000 | 1.378765 | 1.323710 | 0.055055 | finite | 9 | 21 |
| uniform | m3-pretrained-start | 60/60 | -0.216667 | 1.378765 | 1.026878 | 0.351887 | finite | 8 | 21 |
| uniform | m3-historical-trained | 60/60 | -0.383333 | 1.378765 | 0.793701 | 0.585064 | finite | 5 | 28 |
| uniform | m2-context | 60/60 | -0.300000 | 1.378765 | 0.855288 | 0.523477 | finite | 9 | 27 |
| uniform | m5-pretrained-start | 60/60 | -0.216667 | 1.378765 | 1.026878 | 0.351887 | finite | 8 | 21 |
| uniform | m5-low-head-lr | 60/60 | -0.383333 | 1.378765 | 0.794525 | 0.584240 | finite | 5 | 28 |
| lexical | m3-pretrained-start | 60/60 | -0.016667 | 1.323710 | 1.026878 | 0.296832 | finite | 5 | 6 |
| lexical | m3-historical-trained | 60/60 | -0.183333 | 1.323710 | 0.793701 | 0.530009 | finite | 6 | 17 |
| lexical | m2-context | 60/60 | -0.100000 | 1.323710 | 0.855288 | 0.468422 | finite | 11 | 17 |
| lexical | m5-pretrained-start | 60/60 | -0.016667 | 1.323710 | 1.026878 | 0.296832 | finite | 5 | 6 |
| lexical | m5-low-head-lr | 60/60 | -0.183333 | 1.323710 | 0.794525 | 0.529185 | finite | 6 | 17 |
| m3-pretrained-start | m3-historical-trained | 60/60 | -0.166667 | 1.026878 | 0.793701 | 0.233177 | finite | 4 | 14 |
| m3-pretrained-start | m2-context | 60/60 | -0.083333 | 1.026878 | 0.855288 | 0.171591 | finite | 8 | 13 |
| m3-pretrained-start | m5-pretrained-start | 60/60 | 0.000000 | 1.026878 | 1.026878 | 0.000000 | finite | 0 | 0 |
| m3-pretrained-start | m5-low-head-lr | 60/60 | -0.166667 | 1.026878 | 0.794525 | 0.232353 | finite | 4 | 14 |
| m3-historical-trained | m2-context | 60/60 | 0.083333 | 0.793701 | 0.855288 | -0.061587 | finite | 13 | 8 |
| m3-historical-trained | m5-pretrained-start | 60/60 | 0.166667 | 0.793701 | 1.026878 | -0.233177 | finite | 14 | 4 |
| m3-historical-trained | m5-low-head-lr | 60/60 | 0.000000 | 0.793701 | 0.794525 | -0.000824 | finite | 0 | 0 |
| m2-context | m5-pretrained-start | 60/60 | 0.083333 | 0.855288 | 1.026878 | -0.171591 | finite | 13 | 8 |
| m2-context | m5-low-head-lr | 60/60 | -0.083333 | 0.855288 | 0.794525 | 0.060763 | finite | 8 | 13 |
| m5-pretrained-start | m5-low-head-lr | 60/60 | -0.166667 | 1.026878 | 0.794525 | 0.232353 | finite | 4 | 14 |

## Option-order sensitivity

Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.

No matching order reports supplied; no option-order conclusion.

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/pilot/comparison.json`; SHA-256 `74bf9d75c540bceb5bf2bbeb5a48b0dacc67a2b9d8fe9bf14cc0e37d0deb60b3`.
