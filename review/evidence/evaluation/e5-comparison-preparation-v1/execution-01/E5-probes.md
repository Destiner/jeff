# E5 frozen decoder comparison: probes (24 presentations)

Reference: `/Users/destiner/Code/jeff/artifacts/evaluation/e3-v2-freeze-v1/probes/validation.jsonl`; SHA-256 `4258ba3945ab378518f56a7d3cb73138bbee1be04940f019f92ecdb7f96440da`.
24 rows / 12 declared source groups. Rows and reversals are not independent observations.

## Coverage and quality

Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.

| Predictor | Valid/total | Conditional agreement | All-row success | Log loss | Missing/invalid/duplicate | Extra IDs | Unidentifiable | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | 24/24 | 2/24 | 2/24 | 1.057107 | 0/0/0 | 0 | 0 | 0 |
| m4-minilm-trained | 24/24 | 12/24 | 12/24 | 1.025456 | 0/0/0 | 0 | 0 | 0 |
| m4-msmarco-pretrained-start | 24/24 | 14/24 | 14/24 | 1.453783 | 0/0/0 | 0 | 0 | 0 |
| m4-msmarco-trained | 24/24 | 10/24 | 10/24 | 1.876464 | 0/0/0 | 0 | 0 | 0 |
| m2-v1-trained | 24/24 | 16/24 | 16/24 | 0.710407 | 0/0/0 | 0 | 0 | 0 |
| m3-v1-trained | 24/24 | 8/24 | 8/24 | 1.360701 | 0/0/0 | 0 | 0 | 0 |
| uniform | 24/24 | 8/24 | 8/24 | 1.055008 | 0/0/0 | 0 | 0 | 24 |
| lexical | 24/24 | 9/24 | 9/24 | 1.047044 | 0/0/0 | 0 | 0 | 8 |
| qwen25-05b-instruct-frozen | 24/24 | 20/24 | 20/24 | 0.534509 | 0/0/0 | 0 | 0 | 0 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| teacher | evaluation-probes-v1 | teacher | unknown | 24 | 12 | intent, rule_application, sentiment |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| teacher | 24 | 12 | teacher_agreement | 2/24 · 1.057107 | 12/24 · 1.025456 | 14/24 · 1.453783 | 10/24 · 1.876464 | 16/24 · 0.710407 | 8/24 · 1.360701 | 8/24 · 1.055008 | 9/24 · 1.047044 | 20/24 · 0.534509 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent | 8 | 4 | teacher_agreement | 2/8 · 1.089613 | 6/8 · 0.765721 | 4/8 · 2.299398 | 2/8 · 1.412754 | 6/8 · 0.598436 | 4/8 · 0.919648 | 2/8 · 1.098612 | 2/8 · 1.094522 | 8/8 · 0.158820 |
| rule_application | 8 | 4 | teacher_agreement | 0/8 · 0.899523 | 2/8 · 1.309512 | 6/8 · 1.073209 | 4/8 · 2.637630 | 4/8 · 0.912532 | 4/8 · 2.084269 | 3/8 · 0.895880 | 4/8 · 0.901599 | 6/8 · 0.571991 |
| sentiment | 8 | 4 | teacher_agreement | 0/8 · 1.182186 | 4/8 · 1.001136 | 4/8 · 0.988742 | 4/8 · 1.579008 | 6/8 · 0.620252 | 0/8 · 1.078186 | 3/8 · 1.170533 | 3/8 · 1.145011 | 6/8 · 0.872717 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eval.validation.intent.01 | 2 | 1 | teacher_agreement | 2/2 · 1.060672 | 0/2 · 2.722793 | 2/2 · 0.252564 | 0/2 · 0.896270 | 2/2 · 0.350200 | 2/2 · 0.381488 | 0/2 · 1.098612 | 0/2 · 1.058196 | 2/2 · 0.011854 |
| eval.validation.intent.02 | 2 | 1 | teacher_agreement | 0/2 · 1.097434 | 2/2 · 0.009008 | 0/2 · 1.825438 | 0/2 · 1.106439 | 2/2 · 0.039563 | 0/2 · 2.108112 | 1/2 · 1.098612 | 0/2 · 1.077631 | 2/2 · 0.050735 |
| eval.validation.intent.03 | 2 | 1 | teacher_agreement | 0/2 · 1.099122 | 2/2 · 0.216478 | 0/2 · 7.118072 | 0/2 · 3.647120 | 0/2 · 1.492584 | 0/2 · 1.158204 | 1/2 · 1.098612 | 0/2 · 1.204138 | 2/2 · 0.360408 |
| eval.validation.intent.04 | 2 | 1 | teacher_agreement | 0/2 · 1.101223 | 2/2 · 0.114606 | 2/2 · 0.001520 | 2/2 · 0.001186 | 2/2 · 0.511398 | 2/2 · 0.030788 | 0/2 · 1.098612 | 2/2 · 1.038122 | 2/2 · 0.212284 |
| eval.validation.rule_application.01 | 2 | 1 | teacher_agreement | 0/2 · 0.694281 | 0/2 · 2.016432 | 0/2 · 3.418378 | 0/2 · 9.418985 | 0/2 · 1.167164 | 0/2 · 7.142956 | 1/2 · 0.693147 | 0/2 · 0.828966 | 2/2 · 0.080916 |
| eval.validation.rule_application.02 | 2 | 1 | teacher_agreement | 0/2 · 1.106273 | 0/2 · 1.049966 | 2/2 · 0.250980 | 2/2 · 0.087005 | 2/2 · 1.029049 | 0/2 · 0.720894 | 1/2 · 1.098612 | 2/2 · 1.030019 | 2/2 · 0.289589 |
| eval.validation.rule_application.03 | 2 | 1 | teacher_agreement | 0/2 · 1.099022 | 0/2 · 1.596698 | 2/2 · 0.117777 | 2/2 · 0.002158 | 2/2 · 0.713718 | 2/2 · 0.009680 | 0/2 · 1.098612 | 2/2 · 0.979494 | 2/2 · 0.108197 |
| eval.validation.rule_application.04 | 2 | 1 | teacher_agreement | 0/2 · 0.698517 | 2/2 · 0.574952 | 2/2 · 0.505704 | 0/2 · 1.042370 | 0/2 · 0.740198 | 2/2 · 0.463546 | 1/2 · 0.693147 | 0/2 · 0.767918 | 0/2 · 1.809263 |
| eval.validation.sentiment.01 | 2 | 1 | teacher_agreement | 0/2 · 1.111767 | 2/2 · 0.548310 | 0/2 · 1.586171 | 0/2 · 3.020330 | 2/2 · 0.494553 | 0/2 · 0.824866 | 1/2 · 1.098612 | 1/2 · 1.054080 | 2/2 · 0.000036 |
| eval.validation.sentiment.02 | 2 | 1 | teacher_agreement | 0/2 · 1.402996 | 0/2 · 1.697488 | 0/2 · 1.456954 | 0/2 · 3.245798 | 0/2 · 0.897365 | 0/2 · 2.032744 | 1/2 · 1.386294 | 1/2 · 1.386294 | 1/2 · 0.984404 |
| eval.validation.sentiment.03 | 2 | 1 | teacher_agreement | 0/2 · 1.103599 | 0/2 · 1.440705 | 2/2 · 0.718991 | 2/2 · 0.002050 | 2/2 · 0.672351 | 0/2 · 0.711005 | 0/2 · 1.098612 | 1/2 · 1.059997 | 2/2 · 0.001671 |
| eval.validation.sentiment.04 | 2 | 1 | teacher_agreement | 0/2 · 1.110383 | 2/2 · 0.318040 | 2/2 · 0.192850 | 2/2 · 0.047855 | 2/2 · 0.416741 | 0/2 · 0.744129 | 1/2 · 1.098612 | 0/2 · 1.079673 | 1/2 · 2.504756 |

## Paired comparisons

Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.

| Left | Right | Common/total | Agreement delta | Left loss | Right loss | Loss delta | Loss delta status | Left-only correct | Right-only correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | m4-minilm-trained | 24/24 | -0.416667 | 1.057107 | 1.025456 | 0.031651 | finite | 2 | 12 |
| m4-minilm-random-start | m4-msmarco-pretrained-start | 24/24 | -0.500000 | 1.057107 | 1.453783 | -0.396676 | finite | 0 | 12 |
| m4-minilm-random-start | m4-msmarco-trained | 24/24 | -0.333333 | 1.057107 | 1.876464 | -0.819357 | finite | 2 | 10 |
| m4-minilm-random-start | m2-v1-trained | 24/24 | -0.583333 | 1.057107 | 0.710407 | 0.346700 | finite | 0 | 14 |
| m4-minilm-random-start | m3-v1-trained | 24/24 | -0.250000 | 1.057107 | 1.360701 | -0.303594 | finite | 0 | 6 |
| m4-minilm-random-start | uniform | 24/24 | -0.250000 | 1.057107 | 1.055008 | 0.002099 | finite | 2 | 8 |
| m4-minilm-random-start | lexical | 24/24 | -0.291667 | 1.057107 | 1.047044 | 0.010063 | finite | 2 | 9 |
| m4-minilm-random-start | qwen25-05b-instruct-frozen | 24/24 | -0.750000 | 1.057107 | 0.534509 | 0.522598 | finite | 0 | 18 |
| m4-minilm-trained | m4-msmarco-pretrained-start | 24/24 | -0.083333 | 1.025456 | 1.453783 | -0.428327 | finite | 6 | 8 |
| m4-minilm-trained | m4-msmarco-trained | 24/24 | 0.083333 | 1.025456 | 1.876464 | -0.851008 | finite | 8 | 6 |
| m4-minilm-trained | m2-v1-trained | 24/24 | -0.166667 | 1.025456 | 0.710407 | 0.315049 | finite | 4 | 8 |
| m4-minilm-trained | m3-v1-trained | 24/24 | 0.166667 | 1.025456 | 1.360701 | -0.335245 | finite | 8 | 4 |
| m4-minilm-trained | uniform | 24/24 | 0.166667 | 1.025456 | 1.055008 | -0.029552 | finite | 7 | 3 |
| m4-minilm-trained | lexical | 24/24 | 0.125000 | 1.025456 | 1.047044 | -0.021588 | finite | 9 | 6 |
| m4-minilm-trained | qwen25-05b-instruct-frozen | 24/24 | -0.333333 | 1.025456 | 0.534509 | 0.490947 | finite | 3 | 11 |
| m4-msmarco-pretrained-start | m4-msmarco-trained | 24/24 | 0.166667 | 1.453783 | 1.876464 | -0.422681 | finite | 4 | 0 |
| m4-msmarco-pretrained-start | m2-v1-trained | 24/24 | -0.083333 | 1.453783 | 0.710407 | 0.743376 | finite | 2 | 4 |
| m4-msmarco-pretrained-start | m3-v1-trained | 24/24 | 0.250000 | 1.453783 | 1.360701 | 0.093082 | finite | 6 | 0 |
| m4-msmarco-pretrained-start | uniform | 24/24 | 0.250000 | 1.453783 | 1.055008 | 0.398775 | finite | 11 | 5 |
| m4-msmarco-pretrained-start | lexical | 24/24 | 0.208333 | 1.453783 | 1.047044 | 0.406739 | finite | 7 | 2 |
| m4-msmarco-pretrained-start | qwen25-05b-instruct-frozen | 24/24 | -0.250000 | 1.453783 | 0.534509 | 0.919274 | finite | 3 | 9 |
| m4-msmarco-trained | m2-v1-trained | 24/24 | -0.250000 | 1.876464 | 0.710407 | 1.166057 | finite | 0 | 6 |
| m4-msmarco-trained | m3-v1-trained | 24/24 | 0.083333 | 1.876464 | 1.360701 | 0.515763 | finite | 6 | 4 |
| m4-msmarco-trained | uniform | 24/24 | 0.083333 | 1.876464 | 1.055008 | 0.821456 | finite | 8 | 6 |
| m4-msmarco-trained | lexical | 24/24 | 0.041667 | 1.876464 | 1.047044 | 0.829420 | finite | 3 | 2 |
| m4-msmarco-trained | qwen25-05b-instruct-frozen | 24/24 | -0.416667 | 1.876464 | 0.534509 | 1.341954 | finite | 1 | 11 |
| m2-v1-trained | m3-v1-trained | 24/24 | 0.333333 | 0.710407 | 1.360701 | -0.650294 | finite | 10 | 2 |
| m2-v1-trained | uniform | 24/24 | 0.333333 | 0.710407 | 1.055008 | -0.344601 | finite | 12 | 4 |
| m2-v1-trained | lexical | 24/24 | 0.291667 | 0.710407 | 1.047044 | -0.336637 | finite | 8 | 1 |
| m2-v1-trained | qwen25-05b-instruct-frozen | 24/24 | -0.166667 | 0.710407 | 0.534509 | 0.175897 | finite | 1 | 5 |
| m3-v1-trained | uniform | 24/24 | 0.000000 | 1.360701 | 1.055008 | 0.305693 | finite | 7 | 7 |
| m3-v1-trained | lexical | 24/24 | -0.041667 | 1.360701 | 1.047044 | 0.313657 | finite | 4 | 5 |
| m3-v1-trained | qwen25-05b-instruct-frozen | 24/24 | -0.500000 | 1.360701 | 0.534509 | 0.826192 | finite | 2 | 14 |
| uniform | lexical | 24/24 | -0.041667 | 1.055008 | 1.047044 | 0.007964 | finite | 5 | 6 |
| uniform | qwen25-05b-instruct-frozen | 24/24 | -0.500000 | 1.055008 | 0.534509 | 0.520499 | finite | 2 | 14 |
| lexical | qwen25-05b-instruct-frozen | 24/24 | -0.458333 | 1.047044 | 0.534509 | 0.512535 | finite | 1 | 12 |

## Option-order sensitivity

Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.

| Predictor | Complete pairs | Groups | Original agreement | Reversed agreement | Choice consistency | Untied consistency | Either tied | Mean TV | Max probability change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | 12/12 | 12 | 1/12 | 1/12 | 12/12 | 12/12 | 0 | 0 | 0 |
| m4-minilm-trained | 12/12 | 12 | 6/12 | 6/12 | 12/12 | 12/12 | 0 | 4.29e-10 | 3.63e-09 |
| m4-msmarco-pretrained-start | 12/12 | 12 | 7/12 | 7/12 | 12/12 | 12/12 | 0 | 2.41e-10 | 1.64e-09 |
| m4-msmarco-trained | 12/12 | 12 | 5/12 | 5/12 | 12/12 | 12/12 | 0 | 4.89e-10 | 2.97e-09 |
| m2-v1-trained | 12/12 | 12 | 8/12 | 8/12 | 12/12 | 12/12 | 0 | 5.75e-10 | 6.91e-09 |
| m3-v1-trained | 12/12 | 12 | 4/12 | 4/12 | 12/12 | 12/12 | 0 | 1.82e-10 | 2.19e-09 |
| uniform | 12/12 | 12 | 4/12 | 4/12 | 0/12 | 0/0 | 12 | 0 | 0 |
| lexical | 12/12 | 12 | 4/12 | 5/12 | 8/12 | 8/8 | 4 | 0 | 0 |
| qwen25-05b-instruct-frozen | 12/12 | 12 | 9/12 | 11/12 | 10/12 | 10/12 | 0 | 0.258 | 0.988 |

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/comparison.json`; SHA-256 `6231de042b8320d9fbd51691055761f58f054377582f63428b94a65d6f323e4d`.
- m4-minilm-random-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/m4-minilm-random-start-order-report.json`; SHA-256 `423cefea737b843d2dc9f7884f5eceb984aabef31816888ceacc0f4e3b64d414`.
- m4-minilm-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/m4-minilm-trained-order-report.json`; SHA-256 `ba67c2fd67ee398c1fc7acb035f35c7e62da994e0d9fbca518b1251de2fdbafd`.
- m4-msmarco-pretrained-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/m4-msmarco-pretrained-start-order-report.json`; SHA-256 `b30c1b385fbb209b56441072dffea55337ef6c994ec70c43025ea1c230563f1a`.
- m4-msmarco-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/m4-msmarco-trained-order-report.json`; SHA-256 `da0e0710e981722cbd4797d6d74274aac8050290ef46edfdd51e001e7181367f`.
- m2-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/m2-v1-trained-order-report.json`; SHA-256 `e2d21e8a51007c5470d04da60695ab8fae4c85e0b9af08c5f46293dab34b9cc5`.
- m3-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/m3-v1-trained-order-report.json`; SHA-256 `af1a650bc71bc044536ccbb82951eb96f8ebcc5c94004a5bea25b7a8dc98493a`.
- uniform order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/uniform-order-report.json`; SHA-256 `05c5807d6e24c39b6da44b70af41f52ceb0b78d01a4582f2cd6d7727d8679549`.
- lexical order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/lexical-order-report.json`; SHA-256 `6ad923bd5c2ec31eff12a8a3f2b7b8f41e388bf029b5b3c311535afedf1a7046`.
- qwen25-05b-instruct-frozen order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/probes/qwen25-05b-instruct-frozen-order-report.json`; SHA-256 `e82516ca7d21e5fc11c6cead2518fc6ff2196f76dd0aab189b0778f0383dd560`.
