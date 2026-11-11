# E3 released-validation: probes

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
| m6-qwen-fresh-start | 24/24 | 20/24 | 20/24 | 0.534509 | 0/0/0 | 0 | 0 | 0 |
| m6-qwen-v2-trained | 24/24 | 8/24 | 8/24 | 1.173711 | 0/0/0 | 0 | 0 | 0 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| teacher | evaluation-probes-v1 | teacher | unknown | 24 | 12 | intent, rule_application, sentiment |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen | m6-qwen-fresh-start | m6-qwen-v2-trained |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| teacher | 24 | 12 | teacher_agreement | 2/24 · 1.057107 | 12/24 · 1.025456 | 14/24 · 1.453783 | 10/24 · 1.876464 | 16/24 · 0.710407 | 8/24 · 1.360701 | 8/24 · 1.055008 | 9/24 · 1.047044 | 20/24 · 0.534509 | 20/24 · 0.534509 | 8/24 · 1.173711 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen | m6-qwen-fresh-start | m6-qwen-v2-trained |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent | 8 | 4 | teacher_agreement | 2/8 · 1.089613 | 6/8 · 0.765721 | 4/8 · 2.299398 | 2/8 · 1.412754 | 6/8 · 0.598436 | 4/8 · 0.919648 | 2/8 · 1.098612 | 2/8 · 1.094522 | 8/8 · 0.158820 | 8/8 · 0.158820 | 2/8 · 1.293956 |
| rule_application | 8 | 4 | teacher_agreement | 0/8 · 0.899523 | 2/8 · 1.309512 | 6/8 · 1.073209 | 4/8 · 2.637630 | 4/8 · 0.912532 | 4/8 · 2.084269 | 3/8 · 0.895880 | 4/8 · 0.901599 | 6/8 · 0.571991 | 6/8 · 0.571991 | 3/8 · 1.051407 |
| sentiment | 8 | 4 | teacher_agreement | 0/8 · 1.182186 | 4/8 · 1.001136 | 4/8 · 0.988742 | 4/8 · 1.579008 | 6/8 · 0.620252 | 0/8 · 1.078186 | 3/8 · 1.170533 | 3/8 · 1.145011 | 6/8 · 0.872717 | 6/8 · 0.872717 | 3/8 · 1.175770 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen | m6-qwen-fresh-start | m6-qwen-v2-trained |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| eval.validation.intent.01 | 2 | 1 | teacher_agreement | 2/2 · 1.060672 | 0/2 · 2.722793 | 2/2 · 0.252564 | 0/2 · 0.896270 | 2/2 · 0.350200 | 2/2 · 0.381488 | 0/2 · 1.098612 | 0/2 · 1.058196 | 2/2 · 0.011854 | 2/2 · 0.011854 | 0/2 · 1.585204 |
| eval.validation.intent.02 | 2 | 1 | teacher_agreement | 0/2 · 1.097434 | 2/2 · 0.009008 | 0/2 · 1.825438 | 0/2 · 1.106439 | 2/2 · 0.039563 | 0/2 · 2.108112 | 1/2 · 1.098612 | 0/2 · 1.077631 | 2/2 · 0.050735 | 2/2 · 0.050735 | 1/2 · 1.002642 |
| eval.validation.intent.03 | 2 | 1 | teacher_agreement | 0/2 · 1.099122 | 2/2 · 0.216478 | 0/2 · 7.118072 | 0/2 · 3.647120 | 0/2 · 1.492584 | 0/2 · 1.158204 | 1/2 · 1.098612 | 0/2 · 1.204138 | 2/2 · 0.360408 | 2/2 · 0.360408 | 1/2 · 1.003266 |
| eval.validation.intent.04 | 2 | 1 | teacher_agreement | 0/2 · 1.101223 | 2/2 · 0.114606 | 2/2 · 0.001520 | 2/2 · 0.001186 | 2/2 · 0.511398 | 2/2 · 0.030788 | 0/2 · 1.098612 | 2/2 · 1.038122 | 2/2 · 0.212284 | 2/2 · 0.212284 | 0/2 · 1.584711 |
| eval.validation.rule_application.01 | 2 | 1 | teacher_agreement | 0/2 · 0.694281 | 0/2 · 2.016432 | 0/2 · 3.418378 | 0/2 · 9.418985 | 0/2 · 1.167164 | 0/2 · 7.142956 | 1/2 · 0.693147 | 0/2 · 0.828966 | 2/2 · 0.080916 | 2/2 · 0.080916 | 1/2 · 0.808798 |
| eval.validation.rule_application.02 | 2 | 1 | teacher_agreement | 0/2 · 1.106273 | 0/2 · 1.049966 | 2/2 · 0.250980 | 2/2 · 0.087005 | 2/2 · 1.029049 | 0/2 · 0.720894 | 1/2 · 1.098612 | 2/2 · 1.030019 | 2/2 · 0.289589 | 2/2 · 0.289589 | 1/2 · 1.004465 |
| eval.validation.rule_application.03 | 2 | 1 | teacher_agreement | 0/2 · 1.099022 | 0/2 · 1.596698 | 2/2 · 0.117777 | 2/2 · 0.002158 | 2/2 · 0.713718 | 2/2 · 0.009680 | 0/2 · 1.098612 | 2/2 · 0.979494 | 2/2 · 0.108197 | 2/2 · 0.108197 | 0/2 · 1.582241 |
| eval.validation.rule_application.04 | 2 | 1 | teacher_agreement | 0/2 · 0.698517 | 2/2 · 0.574952 | 2/2 · 0.505704 | 0/2 · 1.042370 | 0/2 · 0.740198 | 2/2 · 0.463546 | 1/2 · 0.693147 | 0/2 · 0.767918 | 0/2 · 1.809263 | 0/2 · 1.809263 | 1/2 · 0.810124 |
| eval.validation.sentiment.01 | 2 | 1 | teacher_agreement | 0/2 · 1.111767 | 2/2 · 0.548310 | 0/2 · 1.586171 | 0/2 · 3.020330 | 2/2 · 0.494553 | 0/2 · 0.824866 | 1/2 · 1.098612 | 1/2 · 1.054080 | 2/2 · 0.000036 | 2/2 · 0.000036 | 1/2 · 1.006589 |
| eval.validation.sentiment.02 | 2 | 1 | teacher_agreement | 0/2 · 1.402996 | 0/2 · 1.697488 | 0/2 · 1.456954 | 0/2 · 3.245798 | 0/2 · 0.897365 | 0/2 · 2.032744 | 1/2 · 1.386294 | 1/2 · 1.386294 | 1/2 · 0.984404 | 1/2 · 0.984404 | 1/2 · 1.121160 |
| eval.validation.sentiment.03 | 2 | 1 | teacher_agreement | 0/2 · 1.103599 | 0/2 · 1.440705 | 2/2 · 0.718991 | 2/2 · 0.002050 | 2/2 · 0.672351 | 0/2 · 0.711005 | 0/2 · 1.098612 | 1/2 · 1.059997 | 2/2 · 0.001671 | 2/2 · 0.001671 | 0/2 · 1.569585 |
| eval.validation.sentiment.04 | 2 | 1 | teacher_agreement | 0/2 · 1.110383 | 2/2 · 0.318040 | 2/2 · 0.192850 | 2/2 · 0.047855 | 2/2 · 0.416741 | 0/2 · 0.744129 | 1/2 · 1.098612 | 0/2 · 1.079673 | 1/2 · 2.504756 | 1/2 · 2.504756 | 1/2 · 1.005747 |

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
| m4-minilm-random-start | m6-qwen-fresh-start | 24/24 | -0.750000 | 1.057107 | 0.534509 | 0.522598 | finite | 0 | 18 |
| m4-minilm-random-start | m6-qwen-v2-trained | 24/24 | -0.250000 | 1.057107 | 1.173711 | -0.116603 | finite | 2 | 8 |
| m4-minilm-trained | m4-msmarco-pretrained-start | 24/24 | -0.083333 | 1.025456 | 1.453783 | -0.428327 | finite | 6 | 8 |
| m4-minilm-trained | m4-msmarco-trained | 24/24 | 0.083333 | 1.025456 | 1.876464 | -0.851008 | finite | 8 | 6 |
| m4-minilm-trained | m2-v1-trained | 24/24 | -0.166667 | 1.025456 | 0.710407 | 0.315049 | finite | 4 | 8 |
| m4-minilm-trained | m3-v1-trained | 24/24 | 0.166667 | 1.025456 | 1.360701 | -0.335245 | finite | 8 | 4 |
| m4-minilm-trained | uniform | 24/24 | 0.166667 | 1.025456 | 1.055008 | -0.029552 | finite | 7 | 3 |
| m4-minilm-trained | lexical | 24/24 | 0.125000 | 1.025456 | 1.047044 | -0.021588 | finite | 9 | 6 |
| m4-minilm-trained | qwen25-05b-instruct-frozen | 24/24 | -0.333333 | 1.025456 | 0.534509 | 0.490947 | finite | 3 | 11 |
| m4-minilm-trained | m6-qwen-fresh-start | 24/24 | -0.333333 | 1.025456 | 0.534509 | 0.490947 | finite | 3 | 11 |
| m4-minilm-trained | m6-qwen-v2-trained | 24/24 | 0.166667 | 1.025456 | 1.173711 | -0.148255 | finite | 7 | 3 |
| m4-msmarco-pretrained-start | m4-msmarco-trained | 24/24 | 0.166667 | 1.453783 | 1.876464 | -0.422681 | finite | 4 | 0 |
| m4-msmarco-pretrained-start | m2-v1-trained | 24/24 | -0.083333 | 1.453783 | 0.710407 | 0.743376 | finite | 2 | 4 |
| m4-msmarco-pretrained-start | m3-v1-trained | 24/24 | 0.250000 | 1.453783 | 1.360701 | 0.093082 | finite | 6 | 0 |
| m4-msmarco-pretrained-start | uniform | 24/24 | 0.250000 | 1.453783 | 1.055008 | 0.398775 | finite | 11 | 5 |
| m4-msmarco-pretrained-start | lexical | 24/24 | 0.208333 | 1.453783 | 1.047044 | 0.406739 | finite | 7 | 2 |
| m4-msmarco-pretrained-start | qwen25-05b-instruct-frozen | 24/24 | -0.250000 | 1.453783 | 0.534509 | 0.919274 | finite | 3 | 9 |
| m4-msmarco-pretrained-start | m6-qwen-fresh-start | 24/24 | -0.250000 | 1.453783 | 0.534509 | 0.919274 | finite | 3 | 9 |
| m4-msmarco-pretrained-start | m6-qwen-v2-trained | 24/24 | 0.250000 | 1.453783 | 1.173711 | 0.280072 | finite | 11 | 5 |
| m4-msmarco-trained | m2-v1-trained | 24/24 | -0.250000 | 1.876464 | 0.710407 | 1.166057 | finite | 0 | 6 |
| m4-msmarco-trained | m3-v1-trained | 24/24 | 0.083333 | 1.876464 | 1.360701 | 0.515763 | finite | 6 | 4 |
| m4-msmarco-trained | uniform | 24/24 | 0.083333 | 1.876464 | 1.055008 | 0.821456 | finite | 8 | 6 |
| m4-msmarco-trained | lexical | 24/24 | 0.041667 | 1.876464 | 1.047044 | 0.829420 | finite | 3 | 2 |
| m4-msmarco-trained | qwen25-05b-instruct-frozen | 24/24 | -0.416667 | 1.876464 | 0.534509 | 1.341954 | finite | 1 | 11 |
| m4-msmarco-trained | m6-qwen-fresh-start | 24/24 | -0.416667 | 1.876464 | 0.534509 | 1.341954 | finite | 1 | 11 |
| m4-msmarco-trained | m6-qwen-v2-trained | 24/24 | 0.083333 | 1.876464 | 1.173711 | 0.702753 | finite | 8 | 6 |
| m2-v1-trained | m3-v1-trained | 24/24 | 0.333333 | 0.710407 | 1.360701 | -0.650294 | finite | 10 | 2 |
| m2-v1-trained | uniform | 24/24 | 0.333333 | 0.710407 | 1.055008 | -0.344601 | finite | 12 | 4 |
| m2-v1-trained | lexical | 24/24 | 0.291667 | 0.710407 | 1.047044 | -0.336637 | finite | 8 | 1 |
| m2-v1-trained | qwen25-05b-instruct-frozen | 24/24 | -0.166667 | 0.710407 | 0.534509 | 0.175897 | finite | 1 | 5 |
| m2-v1-trained | m6-qwen-fresh-start | 24/24 | -0.166667 | 0.710407 | 0.534509 | 0.175897 | finite | 1 | 5 |
| m2-v1-trained | m6-qwen-v2-trained | 24/24 | 0.333333 | 0.710407 | 1.173711 | -0.463304 | finite | 12 | 4 |
| m3-v1-trained | uniform | 24/24 | 0.000000 | 1.360701 | 1.055008 | 0.305693 | finite | 7 | 7 |
| m3-v1-trained | lexical | 24/24 | -0.041667 | 1.360701 | 1.047044 | 0.313657 | finite | 4 | 5 |
| m3-v1-trained | qwen25-05b-instruct-frozen | 24/24 | -0.500000 | 1.360701 | 0.534509 | 0.826192 | finite | 2 | 14 |
| m3-v1-trained | m6-qwen-fresh-start | 24/24 | -0.500000 | 1.360701 | 0.534509 | 0.826192 | finite | 2 | 14 |
| m3-v1-trained | m6-qwen-v2-trained | 24/24 | 0.000000 | 1.360701 | 1.173711 | 0.186990 | finite | 7 | 7 |
| uniform | lexical | 24/24 | -0.041667 | 1.055008 | 1.047044 | 0.007964 | finite | 5 | 6 |
| uniform | qwen25-05b-instruct-frozen | 24/24 | -0.500000 | 1.055008 | 0.534509 | 0.520499 | finite | 2 | 14 |
| uniform | m6-qwen-fresh-start | 24/24 | -0.500000 | 1.055008 | 0.534509 | 0.520499 | finite | 2 | 14 |
| uniform | m6-qwen-v2-trained | 24/24 | 0.000000 | 1.055008 | 1.173711 | -0.118703 | finite | 0 | 0 |
| lexical | qwen25-05b-instruct-frozen | 24/24 | -0.458333 | 1.047044 | 0.534509 | 0.512535 | finite | 1 | 12 |
| lexical | m6-qwen-fresh-start | 24/24 | -0.458333 | 1.047044 | 0.534509 | 0.512535 | finite | 1 | 12 |
| lexical | m6-qwen-v2-trained | 24/24 | 0.041667 | 1.047044 | 1.173711 | -0.126667 | finite | 6 | 5 |
| qwen25-05b-instruct-frozen | m6-qwen-fresh-start | 24/24 | 0.000000 | 0.534509 | 0.534509 | 0.000000 | finite | 0 | 0 |
| qwen25-05b-instruct-frozen | m6-qwen-v2-trained | 24/24 | 0.500000 | 0.534509 | 1.173711 | -0.639201 | finite | 14 | 2 |
| m6-qwen-fresh-start | m6-qwen-v2-trained | 24/24 | 0.500000 | 0.534509 | 1.173711 | -0.639201 | finite | 14 | 2 |

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
| m6-qwen-fresh-start | 12/12 | 12 | 9/12 | 11/12 | 10/12 | 10/12 | 0 | 0.258 | 0.988 |
| m6-qwen-v2-trained | 12/12 | 12 | 4/12 | 4/12 | 0/12 | 0/12 | 0 | 0.32 | 0.456 |

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/comparison.json`; SHA-256 `7ba0a7b3ba081ccedfec0834ebf2e8e3e7425734666b80ee00d46a13a44dbefc`.
- m4-minilm-random-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m4-minilm-random-start-order-report.json`; SHA-256 `c58ae1649698bd96b19da8c289d94ec360effe0eaff60dff7cccbdafbf3eb131`.
- m4-minilm-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m4-minilm-trained-order-report.json`; SHA-256 `59f5e1d38f9c7aa2bca4a921674a3b500751342a77b3248b2aea31edd8c8c697`.
- m4-msmarco-pretrained-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m4-msmarco-pretrained-start-order-report.json`; SHA-256 `891599425a62e17b1953f441b27fde01c87cd4c4d66cd831396a1cd41a6fd941`.
- m4-msmarco-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m4-msmarco-trained-order-report.json`; SHA-256 `2871de95a4bfe34a185b42866ff325165ebfc1927fa6bf98093203023a3c3629`.
- m2-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m2-v1-trained-order-report.json`; SHA-256 `ccba2f2215b137291a2398e0a309f438f9cb3b5d8adc59ac0407829d0779b0bb`.
- m3-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m3-v1-trained-order-report.json`; SHA-256 `23a5b07abd0deda03380b5499a7d34dfb6958ec9cfafbcfe97a726ade8055ed0`.
- uniform order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/uniform-order-report.json`; SHA-256 `cc37d8fdf163a69983d96afa6d5acc0e64299f772560d37e3932ca76284baa9d`.
- lexical order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/lexical-order-report.json`; SHA-256 `81b74d485f4ac81fbb6e1a529d1772d45cd8f58c3505d9f64367d953e7dd1e61`.
- qwen25-05b-instruct-frozen order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/qwen25-05b-instruct-frozen-order-report.json`; SHA-256 `4d4d38532c206357d68ce3cbade09326d6463b3967a51697530e3b545212f126`.
- m6-qwen-fresh-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m6-qwen-fresh-start-order-report.json`; SHA-256 `a22351c260c678054614e92ec5b903547547f6e206d0d01c082e72145789e283`.
- m6-qwen-v2-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v3/execution-01/study/probes/m6-qwen-v2-trained-order-report.json`; SHA-256 `706474562fad59ea628c19d171d3356584f488b5e35f14f0a13e7ded5442cb89`.
