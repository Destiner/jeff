# E4 M5 LR control — probes

Reference: `/Users/destiner/Code/jeff/artifacts/evaluation/probes-v1/validation.jsonl`; SHA-256 `4258ba3945ab378518f56a7d3cb73138bbee1be04940f019f92ecdb7f96440da`.
24 rows / 12 declared source groups. Rows and reversals are not independent observations.

## Coverage and quality

Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.

| Predictor | Valid/total | Conditional agreement | All-row success | Log loss | Missing/invalid/duplicate | Extra IDs | Unidentifiable | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform | 24/24 | 8/24 | 8/24 | 1.055008 | 0/0/0 | 0 | 0 | 24 |
| lexical | 24/24 | 9/24 | 9/24 | 1.047044 | 0/0/0 | 0 | 0 | 8 |
| m3-pretrained-start | 24/24 | 14/24 | 14/24 | 1.453783 | 0/0/0 | 0 | 0 | 0 |
| m3-historical-trained | 24/24 | 8/24 | 8/24 | 1.360701 | 0/0/0 | 0 | 0 | 0 |
| m2-context | 24/24 | 16/24 | 16/24 | 0.710407 | 0/0/0 | 0 | 0 | 0 |
| m5-pretrained-start | 24/24 | 14/24 | 14/24 | 1.453783 | 0/0/0 | 0 | 0 | 0 |
| m5-low-head-lr | 24/24 | 10/24 | 10/24 | 1.384773 | 0/0/0 | 0 | 0 | 0 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| teacher | evaluation-probes-v1 | teacher | unknown | 24 | 12 | intent, rule_application, sentiment |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | uniform | lexical | m3-pretrained-start | m3-historical-trained | m2-context | m5-pretrained-start | m5-low-head-lr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| teacher | 24 | 12 | teacher_agreement | 8/24 · 1.055008 | 9/24 · 1.047044 | 14/24 · 1.453783 | 8/24 · 1.360701 | 16/24 · 0.710407 | 14/24 · 1.453783 | 10/24 · 1.384773 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | uniform | lexical | m3-pretrained-start | m3-historical-trained | m2-context | m5-pretrained-start | m5-low-head-lr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent | 8 | 4 | teacher_agreement | 2/8 · 1.098612 | 2/8 · 1.094522 | 4/8 · 2.299398 | 4/8 · 0.919648 | 6/8 · 0.598436 | 4/8 · 2.299398 | 4/8 · 0.933246 |
| rule_application | 8 | 4 | teacher_agreement | 3/8 · 0.895880 | 4/8 · 0.901599 | 6/8 · 1.073209 | 4/8 · 2.084269 | 4/8 · 0.912532 | 6/8 · 1.073209 | 4/8 · 2.162269 |
| sentiment | 8 | 4 | teacher_agreement | 3/8 · 1.170533 | 3/8 · 1.145011 | 4/8 · 0.988742 | 0/8 · 1.078186 | 6/8 · 0.620252 | 4/8 · 0.988742 | 2/8 · 1.058804 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | uniform | lexical | m3-pretrained-start | m3-historical-trained | m2-context | m5-pretrained-start | m5-low-head-lr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eval.validation.intent.01 | 2 | 1 | teacher_agreement | 0/2 · 1.098612 | 0/2 · 1.058196 | 2/2 · 0.252564 | 2/2 · 0.381488 | 2/2 · 0.350200 | 2/2 · 0.252564 | 2/2 · 0.332263 |
| eval.validation.intent.02 | 2 | 1 | teacher_agreement | 1/2 · 1.098612 | 0/2 · 1.077631 | 0/2 · 1.825438 | 0/2 · 2.108112 | 2/2 · 0.039563 | 0/2 · 1.825438 | 0/2 · 2.121156 |
| eval.validation.intent.03 | 2 | 1 | teacher_agreement | 1/2 · 1.098612 | 0/2 · 1.204138 | 0/2 · 7.118072 | 0/2 · 1.158204 | 0/2 · 1.492584 | 0/2 · 7.118072 | 0/2 · 1.247900 |
| eval.validation.intent.04 | 2 | 1 | teacher_agreement | 0/2 · 1.098612 | 2/2 · 1.038122 | 2/2 · 0.001520 | 2/2 · 0.030788 | 2/2 · 0.511398 | 2/2 · 0.001520 | 2/2 · 0.031667 |
| eval.validation.rule_application.01 | 2 | 1 | teacher_agreement | 1/2 · 0.693147 | 0/2 · 0.828966 | 0/2 · 3.418378 | 0/2 · 7.142956 | 0/2 · 1.167164 | 0/2 · 3.418378 | 0/2 · 7.469238 |
| eval.validation.rule_application.02 | 2 | 1 | teacher_agreement | 1/2 · 1.098612 | 2/2 · 1.030019 | 2/2 · 0.250980 | 0/2 · 0.720894 | 2/2 · 1.029049 | 2/2 · 0.250980 | 0/2 · 0.708532 |
| eval.validation.rule_application.03 | 2 | 1 | teacher_agreement | 0/2 · 1.098612 | 2/2 · 0.979494 | 2/2 · 0.117777 | 2/2 · 0.009680 | 2/2 · 0.713718 | 2/2 · 0.117777 | 2/2 · 0.008452 |
| eval.validation.rule_application.04 | 2 | 1 | teacher_agreement | 1/2 · 0.693147 | 0/2 · 0.767918 | 2/2 · 0.505704 | 2/2 · 0.463546 | 0/2 · 0.740198 | 2/2 · 0.505704 | 2/2 · 0.462853 |
| eval.validation.sentiment.01 | 2 | 1 | teacher_agreement | 1/2 · 1.098612 | 1/2 · 1.054080 | 0/2 · 1.586171 | 0/2 · 0.824866 | 2/2 · 0.494553 | 0/2 · 1.586171 | 0/2 · 0.768300 |
| eval.validation.sentiment.02 | 2 | 1 | teacher_agreement | 1/2 · 1.386294 | 1/2 · 1.386294 | 0/2 · 1.456954 | 0/2 · 2.032744 | 0/2 · 0.897365 | 0/2 · 1.456954 | 0/2 · 2.008595 |
| eval.validation.sentiment.03 | 2 | 1 | teacher_agreement | 0/2 · 1.098612 | 1/2 · 1.059997 | 2/2 · 0.718991 | 0/2 · 0.711005 | 2/2 · 0.672351 | 2/2 · 0.718991 | 0/2 · 0.751686 |
| eval.validation.sentiment.04 | 2 | 1 | teacher_agreement | 1/2 · 1.098612 | 0/2 · 1.079673 | 2/2 · 0.192850 | 0/2 · 0.744129 | 2/2 · 0.416741 | 2/2 · 0.192850 | 2/2 · 0.706636 |

## Paired comparisons

Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.

| Left | Right | Common/total | Agreement delta | Left loss | Right loss | Loss delta | Loss delta status | Left-only correct | Right-only correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform | lexical | 24/24 | -0.041667 | 1.055008 | 1.047044 | 0.007964 | finite | 5 | 6 |
| uniform | m3-pretrained-start | 24/24 | -0.250000 | 1.055008 | 1.453783 | -0.398775 | finite | 5 | 11 |
| uniform | m3-historical-trained | 24/24 | 0.000000 | 1.055008 | 1.360701 | -0.305693 | finite | 7 | 7 |
| uniform | m2-context | 24/24 | -0.333333 | 1.055008 | 0.710407 | 0.344601 | finite | 4 | 12 |
| uniform | m5-pretrained-start | 24/24 | -0.250000 | 1.055008 | 1.453783 | -0.398775 | finite | 5 | 11 |
| uniform | m5-low-head-lr | 24/24 | -0.083333 | 1.055008 | 1.384773 | -0.329765 | finite | 6 | 8 |
| lexical | m3-pretrained-start | 24/24 | -0.208333 | 1.047044 | 1.453783 | -0.406739 | finite | 2 | 7 |
| lexical | m3-historical-trained | 24/24 | 0.041667 | 1.047044 | 1.360701 | -0.313657 | finite | 5 | 4 |
| lexical | m2-context | 24/24 | -0.291667 | 1.047044 | 0.710407 | 0.336637 | finite | 1 | 8 |
| lexical | m5-pretrained-start | 24/24 | -0.208333 | 1.047044 | 1.453783 | -0.406739 | finite | 2 | 7 |
| lexical | m5-low-head-lr | 24/24 | -0.041667 | 1.047044 | 1.384773 | -0.337729 | finite | 5 | 6 |
| m3-pretrained-start | m3-historical-trained | 24/24 | 0.250000 | 1.453783 | 1.360701 | 0.093082 | finite | 6 | 0 |
| m3-pretrained-start | m2-context | 24/24 | -0.083333 | 1.453783 | 0.710407 | 0.743376 | finite | 2 | 4 |
| m3-pretrained-start | m5-pretrained-start | 24/24 | 0.000000 | 1.453783 | 1.453783 | 0.000000 | finite | 0 | 0 |
| m3-pretrained-start | m5-low-head-lr | 24/24 | 0.166667 | 1.453783 | 1.384773 | 0.069010 | finite | 4 | 0 |
| m3-historical-trained | m2-context | 24/24 | -0.333333 | 1.360701 | 0.710407 | 0.650294 | finite | 2 | 10 |
| m3-historical-trained | m5-pretrained-start | 24/24 | -0.250000 | 1.360701 | 1.453783 | -0.093082 | finite | 0 | 6 |
| m3-historical-trained | m5-low-head-lr | 24/24 | -0.083333 | 1.360701 | 1.384773 | -0.024072 | finite | 0 | 2 |
| m2-context | m5-pretrained-start | 24/24 | 0.083333 | 0.710407 | 1.453783 | -0.743376 | finite | 4 | 2 |
| m2-context | m5-low-head-lr | 24/24 | 0.250000 | 0.710407 | 1.384773 | -0.674366 | finite | 8 | 2 |
| m5-pretrained-start | m5-low-head-lr | 24/24 | 0.166667 | 1.453783 | 1.384773 | 0.069010 | finite | 4 | 0 |

## Option-order sensitivity

Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.

| Predictor | Complete pairs | Groups | Original agreement | Reversed agreement | Choice consistency | Untied consistency | Either tied | Mean TV | Max probability change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| uniform | 12/12 | 12 | 4/12 | 4/12 | 0/12 | 0/0 | 12 | 0 | 0 |
| lexical | 12/12 | 12 | 4/12 | 5/12 | 8/12 | 8/8 | 4 | 0 | 0 |
| m3-pretrained-start | 12/12 | 12 | 7/12 | 7/12 | 12/12 | 12/12 | 0 | 2.29e-10 | 1.64e-09 |
| m3-historical-trained | 12/12 | 12 | 4/12 | 4/12 | 12/12 | 12/12 | 0 | 1.82e-10 | 2.19e-09 |
| m2-context | 12/12 | 12 | 8/12 | 8/12 | 12/12 | 12/12 | 0 | 5.75e-10 | 6.91e-09 |
| m5-pretrained-start | 12/12 | 12 | 7/12 | 7/12 | 12/12 | 12/12 | 0 | 2.29e-10 | 1.64e-09 |
| m5-low-head-lr | 12/12 | 12 | 5/12 | 5/12 | 12/12 | 12/12 | 0 | 1.3e-09 | 1.01e-08 |

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/comparison.json`; SHA-256 `5ee579ac9f043df1de602201788571ed220f02183f3394c2941e37c304a549ed`.
- uniform order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/uniform-order.json`; SHA-256 `f6800d2860b04977f3536500700af886699fb29666f9c8dbc1a1daac2ab4b3c0`.
- lexical order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/lexical-order.json`; SHA-256 `21a27d66213f0eebe3d8d7a60f06d5c42734ee174ec88e60de9605ccfafa2bea`.
- m3-pretrained-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/m3-pretrained-start-order.json`; SHA-256 `a7309ac56b961913856bf591c65aee855821404788952b85c8bc5ded46e6791b`.
- m3-historical-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/m3-historical-trained-order.json`; SHA-256 `46743a88018f93b8e4b9158bacf750d98bbcbc649465241cb327d57d91ba3b46`.
- m2-context order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/m2-context-order.json`; SHA-256 `4e63402f4b44fbc3d1928a76e6d1fe2d22727b575b76180267c26a4a993ced8b`.
- m5-pretrained-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/m5-pretrained-start-order.json`; SHA-256 `c961a24e8d593f50e022980a0e044813d4ec62f4e1f6575ef7f064484009655d`.
- m5-low-head-lr order: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-comparison-v1/probes/m5-low-head-lr-order.json`; SHA-256 `97bbd1131a7286cc6c27b1fa72b8de6d48571b9493495cb20cc37a7823e2cb75`.
