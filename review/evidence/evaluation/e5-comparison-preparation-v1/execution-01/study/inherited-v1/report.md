# E3 released-validation: inherited-v1

Reference: `/Users/destiner/Code/jeff/artifacts/evaluation/e3-v2-freeze-v1/inherited-v1/validation.jsonl`; SHA-256 `8d4cd2e29f8b9a5dfd0b5ae4408b4f06b986eb2b2631868a0158d8dcdfc1559b`.
60 rows / 12 declared source groups. Rows and reversals are not independent observations.

## Coverage and quality

Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.

| Predictor | Valid/total | Conditional agreement | All-row success | Log loss | Missing/invalid/duplicate | Extra IDs | Unidentifiable | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | 60/60 | 20/60 | 20/60 | 1.378267 | 0/0/0 | 0 | 0 | 0 |
| m4-minilm-trained | 60/60 | 34/60 | 34/60 | 0.907554 | 0/0/0 | 0 | 0 | 0 |
| m4-msmarco-pretrained-start | 60/60 | 30/60 | 30/60 | 1.026878 | 0/0/0 | 0 | 0 | 0 |
| m4-msmarco-trained | 60/60 | 42/60 | 42/60 | 0.712621 | 0/0/0 | 0 | 0 | 0 |
| m2-v1-trained | 60/60 | 35/60 | 35/60 | 0.855288 | 0/0/0 | 0 | 0 | 0 |
| m3-v1-trained | 60/60 | 40/60 | 40/60 | 0.793701 | 0/0/0 | 0 | 0 | 0 |
| uniform | 60/60 | 17/60 | 17/60 | 1.378765 | 0/0/0 | 0 | 0 | 60 |
| lexical | 60/60 | 29/60 | 29/60 | 1.323710 | 0/0/0 | 0 | 0 | 14 |
| qwen25-05b-instruct-frozen | 60/60 | 35/60 | 35/60 | 1.194707 | 0/0/0 | 0 | 0 | 0 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| programmatic | data-pilot-v1/rule_application/original-rule-job-r1 | rule_verified | not applicable | 20 | 2 | rule_application |
| teacher | data-pilot-v1/sentiment-r2/from/jeff-data-pilot-v1-sentiment-agent-r1 | teacher | gpt-sol | 20 | 5 | sentiment |
| teacher | data:pilot-v1:intent:agent-authoring-r1 | teacher | openai/gpt-sol | 20 | 5 | intent |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rule_verified | 20 | 2 | rule_verified_accuracy | 8/20 · 1.378970 | 4/20 · 1.377048 | 5/20 · 1.366589 | 7/20 · 1.316504 | 4/20 · 1.431825 | 7/20 · 1.362848 | 6/20 · 1.379841 | 8/20 · 1.373712 | 6/20 · 1.873184 |
| teacher | 40 | 10 | teacher_agreement | 12/40 · 1.377915 | 30/40 · 0.672807 | 25/40 · 0.857023 | 35/40 · 0.410679 | 31/40 · 0.567019 | 33/40 · 0.509127 | 11/40 · 1.378227 | 21/40 · 1.298709 | 29/40 · 0.855469 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent | 20 | 5 | teacher_agreement | 6/20 · 1.373597 | 17/20 · 0.500164 | 18/20 · 0.381560 | 18/20 · 0.251990 | 20/20 · 0.067838 | 19/20 · 0.211817 | 6/20 · 1.370160 | 16/20 · 1.216725 | 20/20 · 0.025459 |
| rule_application | 20 | 2 | rule_verified_accuracy | 8/20 · 1.378970 | 4/20 · 1.377048 | 5/20 · 1.366589 | 7/20 · 1.316504 | 4/20 · 1.431825 | 7/20 · 1.362848 | 6/20 · 1.379841 | 8/20 · 1.373712 | 6/20 · 1.873184 |
| sentiment | 20 | 5 | teacher_agreement | 6/20 · 1.382234 | 13/20 · 0.845449 | 7/20 · 1.332485 | 17/20 · 0.569368 | 11/20 · 1.066200 | 14/20 · 0.806437 | 5/20 · 1.386294 | 5/20 · 1.380693 | 9/20 · 1.685479 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data:pilot-v1:intent:g26 | 4 | 1 | teacher_agreement | 1/4 · 1.378518 | 4/4 · 0.066455 | 4/4 · 0.019332 | 4/4 · 0.000322 | 4/4 · 0.002241 | 4/4 · 0.000795 | 3/4 · 1.370160 | 3/4 · 1.193414 | 4/4 · 0.006036 |
| data:pilot-v1:intent:g27 | 4 | 1 | teacher_agreement | 1/4 · 1.377123 | 2/4 · 2.115364 | 3/4 · 0.547240 | 3/4 · 0.501848 | 4/4 · 0.163599 | 4/4 · 0.194188 | 0/4 · 1.370160 | 2/4 · 1.305617 | 4/4 · 0.084663 |
| data:pilot-v1:intent:g28 | 4 | 1 | teacher_agreement | 1/4 · 1.367310 | 4/4 · 0.009464 | 4/4 · 0.000561 | 4/4 · 0.000069 | 4/4 · 0.161615 | 4/4 · 0.001515 | 1/4 · 1.370160 | 4/4 · 1.191942 | 4/4 · 0.000358 |
| data:pilot-v1:intent:g29 | 4 | 1 | teacher_agreement | 2/4 · 1.368055 | 3/4 · 0.248637 | 3/4 · 1.216777 | 3/4 · 0.754051 | 4/4 · 0.006365 | 3/4 · 0.857740 | 1/4 · 1.370160 | 3/4 · 1.186473 | 4/4 · 0.008314 |
| data:pilot-v1:intent:g30 | 4 | 1 | teacher_agreement | 1/4 · 1.376977 | 4/4 · 0.060900 | 4/4 · 0.123892 | 4/4 · 0.003659 | 4/4 · 0.005371 | 4/4 · 0.004845 | 1/4 · 1.370160 | 4/4 · 1.206181 | 4/4 · 0.027921 |
| data:pilot-v1:rule_application:g11 | 10 | 1 | rule_verified_accuracy | 2/10 · 1.329051 | 1/10 · 1.330269 | 2/10 · 1.377242 | 2/10 · 1.335161 | 2/10 · 1.334079 | 2/10 · 1.427479 | 3/10 · 1.328758 | 3/10 · 1.319537 | 3/10 · 2.089407 |
| data:pilot-v1:rule_application:g12 | 10 | 1 | rule_verified_accuracy | 6/10 · 1.428890 | 3/10 · 1.423827 | 3/10 · 1.355935 | 5/10 · 1.297848 | 2/10 · 1.529570 | 5/10 · 1.298218 | 3/10 · 1.430923 | 5/10 · 1.427887 | 3/10 · 1.656960 |
| data:pilot-v1:sentiment:g26 | 4 | 1 | teacher_agreement | 2/4 · 1.381979 | 3/4 · 1.025966 | 1/4 · 1.306202 | 4/4 · 0.321410 | 3/4 · 0.683696 | 4/4 · 0.581017 | 1/4 · 1.386294 | 1/4 · 1.384758 | 2/4 · 1.749045 |
| data:pilot-v1:sentiment:g27 | 4 | 1 | teacher_agreement | 0/4 · 1.380101 | 2/4 · 0.707228 | 1/4 · 1.402344 | 3/4 · 0.675262 | 3/4 · 0.763866 | 3/4 · 0.677976 | 0/4 · 1.386294 | 0/4 · 1.398288 | 3/4 · 1.115475 |
| data:pilot-v1:sentiment:g28 | 4 | 1 | teacher_agreement | 1/4 · 1.387006 | 3/4 · 0.701185 | 3/4 · 1.244544 | 3/4 · 0.703047 | 3/4 · 1.029880 | 1/4 · 1.004299 | 1/4 · 1.386294 | 2/4 · 1.368146 | 0/4 · 2.707418 |
| data:pilot-v1:sentiment:g29 | 4 | 1 | teacher_agreement | 1/4 · 1.385783 | 2/4 · 1.090308 | 0/4 · 1.420853 | 3/4 · 0.674895 | 1/4 · 1.369133 | 3/4 · 0.962462 | 2/4 · 1.386294 | 0/4 · 1.386543 | 2/4 · 1.000744 |
| data:pilot-v1:sentiment:g30 | 4 | 1 | teacher_agreement | 2/4 · 1.376301 | 3/4 · 0.702560 | 2/4 · 1.288482 | 4/4 · 0.472228 | 1/4 · 1.484424 | 3/4 · 0.806433 | 1/4 · 1.386294 | 2/4 · 1.365730 | 2/4 · 1.854711 |

## Paired comparisons

Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.

| Left | Right | Common/total | Agreement delta | Left loss | Right loss | Loss delta | Loss delta status | Left-only correct | Right-only correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | m4-minilm-trained | 60/60 | -0.233333 | 1.378267 | 0.907554 | 0.470713 | finite | 7 | 21 |
| m4-minilm-random-start | m4-msmarco-pretrained-start | 60/60 | -0.166667 | 1.378267 | 1.026878 | 0.351389 | finite | 7 | 17 |
| m4-minilm-random-start | m4-msmarco-trained | 60/60 | -0.366667 | 1.378267 | 0.712621 | 0.665646 | finite | 2 | 24 |
| m4-minilm-random-start | m2-v1-trained | 60/60 | -0.250000 | 1.378267 | 0.855288 | 0.522980 | finite | 10 | 25 |
| m4-minilm-random-start | m3-v1-trained | 60/60 | -0.333333 | 1.378267 | 0.793701 | 0.584566 | finite | 3 | 23 |
| m4-minilm-random-start | uniform | 60/60 | 0.050000 | 1.378267 | 1.378765 | -0.000498 | finite | 14 | 11 |
| m4-minilm-random-start | lexical | 60/60 | -0.150000 | 1.378267 | 1.323710 | 0.054557 | finite | 8 | 17 |
| m4-minilm-random-start | qwen25-05b-instruct-frozen | 60/60 | -0.250000 | 1.378267 | 1.194707 | 0.183560 | finite | 8 | 23 |
| m4-minilm-trained | m4-msmarco-pretrained-start | 60/60 | 0.066667 | 0.907554 | 1.026878 | -0.119324 | finite | 11 | 7 |
| m4-minilm-trained | m4-msmarco-trained | 60/60 | -0.133333 | 0.907554 | 0.712621 | 0.194933 | finite | 4 | 12 |
| m4-minilm-trained | m2-v1-trained | 60/60 | -0.016667 | 0.907554 | 0.855288 | 0.052266 | finite | 6 | 7 |
| m4-minilm-trained | m3-v1-trained | 60/60 | -0.100000 | 0.907554 | 0.793701 | 0.113853 | finite | 7 | 13 |
| m4-minilm-trained | uniform | 60/60 | 0.283333 | 0.907554 | 1.378765 | -0.471211 | finite | 22 | 5 |
| m4-minilm-trained | lexical | 60/60 | 0.083333 | 0.907554 | 1.323710 | -0.416156 | finite | 12 | 7 |
| m4-minilm-trained | qwen25-05b-instruct-frozen | 60/60 | -0.016667 | 0.907554 | 1.194707 | -0.287153 | finite | 10 | 11 |
| m4-msmarco-pretrained-start | m4-msmarco-trained | 60/60 | -0.200000 | 1.026878 | 0.712621 | 0.314257 | finite | 1 | 13 |
| m4-msmarco-pretrained-start | m2-v1-trained | 60/60 | -0.083333 | 1.026878 | 0.855288 | 0.171591 | finite | 8 | 13 |
| m4-msmarco-pretrained-start | m3-v1-trained | 60/60 | -0.166667 | 1.026878 | 0.793701 | 0.233177 | finite | 4 | 14 |
| m4-msmarco-pretrained-start | uniform | 60/60 | 0.216667 | 1.026878 | 1.378765 | -0.351887 | finite | 21 | 8 |
| m4-msmarco-pretrained-start | lexical | 60/60 | 0.016667 | 1.026878 | 1.323710 | -0.296832 | finite | 6 | 5 |
| m4-msmarco-pretrained-start | qwen25-05b-instruct-frozen | 60/60 | -0.083333 | 1.026878 | 1.194707 | -0.167829 | finite | 9 | 14 |
| m4-msmarco-trained | m2-v1-trained | 60/60 | 0.116667 | 0.712621 | 0.855288 | -0.142667 | finite | 14 | 7 |
| m4-msmarco-trained | m3-v1-trained | 60/60 | 0.033333 | 0.712621 | 0.793701 | -0.081080 | finite | 5 | 3 |
| m4-msmarco-trained | uniform | 60/60 | 0.416667 | 0.712621 | 1.378765 | -0.666144 | finite | 30 | 5 |
| m4-msmarco-trained | lexical | 60/60 | 0.216667 | 0.712621 | 1.323710 | -0.611089 | finite | 16 | 3 |
| m4-msmarco-trained | qwen25-05b-instruct-frozen | 60/60 | 0.116667 | 0.712621 | 1.194707 | -0.482086 | finite | 14 | 7 |
| m2-v1-trained | m3-v1-trained | 60/60 | -0.083333 | 0.855288 | 0.793701 | 0.061587 | finite | 8 | 13 |
| m2-v1-trained | uniform | 60/60 | 0.300000 | 0.855288 | 1.378765 | -0.523477 | finite | 27 | 9 |
| m2-v1-trained | lexical | 60/60 | 0.100000 | 0.855288 | 1.323710 | -0.468422 | finite | 17 | 11 |
| m2-v1-trained | qwen25-05b-instruct-frozen | 60/60 | 0.000000 | 0.855288 | 1.194707 | -0.339419 | finite | 10 | 10 |
| m3-v1-trained | uniform | 60/60 | 0.383333 | 0.793701 | 1.378765 | -0.585064 | finite | 28 | 5 |
| m3-v1-trained | lexical | 60/60 | 0.183333 | 0.793701 | 1.323710 | -0.530009 | finite | 17 | 6 |
| m3-v1-trained | qwen25-05b-instruct-frozen | 60/60 | 0.083333 | 0.793701 | 1.194707 | -0.401006 | finite | 11 | 6 |
| uniform | lexical | 60/60 | -0.200000 | 1.378765 | 1.323710 | 0.055055 | finite | 9 | 21 |
| uniform | qwen25-05b-instruct-frozen | 60/60 | -0.300000 | 1.378765 | 1.194707 | 0.184058 | finite | 9 | 27 |
| lexical | qwen25-05b-instruct-frozen | 60/60 | -0.100000 | 1.323710 | 1.194707 | 0.129003 | finite | 8 | 14 |

## Option-order sensitivity

Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.

| Predictor | Complete pairs | Groups | Original agreement | Reversed agreement | Choice consistency | Untied consistency | Either tied | Mean TV | Max probability change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | 60/60 | 12 | 20/60 | 20/60 | 60/60 | 60/60 | 0 | 0 | 0 |
| m4-minilm-trained | 60/60 | 12 | 34/60 | 34/60 | 60/60 | 60/60 | 0 | 3.07e-11 | 1.83e-09 |
| m4-msmarco-pretrained-start | 60/60 | 12 | 30/60 | 30/60 | 60/60 | 60/60 | 0 | 5.59e-10 | 1.44e-08 |
| m4-msmarco-trained | 60/60 | 12 | 42/60 | 42/60 | 60/60 | 60/60 | 0 | 3.9e-10 | 1.09e-08 |
| m2-v1-trained | 60/60 | 12 | 35/60 | 35/60 | 60/60 | 60/60 | 0 | 4.12e-11 | 9.04e-10 |
| m3-v1-trained | 60/60 | 12 | 40/60 | 40/60 | 60/60 | 60/60 | 0 | 3.27e-11 | 9.88e-10 |
| uniform | 60/60 | 12 | 17/60 | 13/60 | 0/60 | 0/0 | 60 | 0 | 0 |
| lexical | 60/60 | 12 | 29/60 | 31/60 | 46/60 | 46/46 | 14 | 0 | 0 |
| qwen25-05b-instruct-frozen | 60/60 | 12 | 35/60 | 34/60 | 41/60 | 41/60 | 0 | 0.245 | 0.78 |

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/comparison.json`; SHA-256 `11cfe8996afbc5e6d6a1e0f5f644679dd5348fc571a2a4c1fdfe043f303d2632`.
- m4-minilm-random-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/m4-minilm-random-start-order-report.json`; SHA-256 `ba8f5e9732ac65e8b1c58594604ada5c1c729678e3f56f007c5d0b834d699040`.
- m4-minilm-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/m4-minilm-trained-order-report.json`; SHA-256 `76555f319f542d39a1887ca9838253dc55ff2f71fada24c62f6e6cc81812d347`.
- m4-msmarco-pretrained-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/m4-msmarco-pretrained-start-order-report.json`; SHA-256 `61e00b3277748c44fb9561d38b1f4fc3183bfc58f60dc8f0348ccfa82cd0ae9d`.
- m4-msmarco-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/m4-msmarco-trained-order-report.json`; SHA-256 `ef2a721d5506988cab76dc14ad77ef41bb942b9f8bd95edef2dff9ae955761eb`.
- m2-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/m2-v1-trained-order-report.json`; SHA-256 `5f4da2136890a8babaf68c476864eb657d0fa9c906955b073dbfba82737678fb`.
- m3-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/m3-v1-trained-order-report.json`; SHA-256 `9cab4e798f40479bc24a3290be8aa1d5997e92e989982605aa4dc525c0b6fc48`.
- uniform order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/uniform-order-report.json`; SHA-256 `62188ee830b6417aaa1c8f92f0ea61db417942699c850846791253f97b1b13cf`.
- lexical order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/lexical-order-report.json`; SHA-256 `8928e8c00f975013ddc8988fa5c9112338e683dca0c8c02efef8f3f2031abf2b`.
- qwen25-05b-instruct-frozen order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/inherited-v1/qwen25-05b-instruct-frozen-order-report.json`; SHA-256 `010d9e6861edca3770cf644942aae6016f6fb138b6b6cf323fb7bd60446461dc`.
