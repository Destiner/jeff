# E6 arithmetic appendix

All numbers recomputed from saved predictions, except explicitly noted metadata ancestry. Full precision: [numbers.json](numbers.json). Dimensions overlap; do not sum them as independent samples.

## inherited-v1 — all 11 predictors

| Predictor | Order | n | Agreement count | NLL | Brier | Ties |
| --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | original | 60 | 20 | 1.378267 | 0.746036 | 0 |
| m4-minilm-trained | original | 60 | 34 | 0.907554 | 0.478135 | 0 |
| m4-msmarco-pretrained-start | original | 60 | 30 | 1.026878 | 0.552223 | 0 |
| m4-msmarco-trained | original | 60 | 42 | 0.712621 | 0.393343 | 0 |
| m2-v1-trained | original | 60 | 35 | 0.855288 | 0.461543 | 0 |
| m3-v1-trained | original | 60 | 40 | 0.793701 | 0.421937 | 0 |
| uniform | original | 60 | 17 | 1.378765 | 0.746111 | 60 |
| lexical | original | 60 | 29 | 1.323710 | 0.717805 | 14 |
| qwen25-05b-instruct-frozen | original | 60 | 35 | 1.194707 | 0.599128 | 0 |
| m6-qwen-fresh-start | original | 60 | 35 | 1.194707 | 0.599128 | 0 |
| m6-qwen-v2-trained | original | 60 | 17 | 1.442884 | 0.778014 | 0 |
| m4-minilm-random-start | reversed | 60 | 20 | 1.378267 | 0.746036 | 0 |
| m4-minilm-trained | reversed | 60 | 34 | 0.907554 | 0.478135 | 0 |
| m4-msmarco-pretrained-start | reversed | 60 | 30 | 1.026878 | 0.552223 | 0 |
| m4-msmarco-trained | reversed | 60 | 42 | 0.712621 | 0.393343 | 0 |
| m2-v1-trained | reversed | 60 | 35 | 0.855288 | 0.461543 | 0 |
| m3-v1-trained | reversed | 60 | 40 | 0.793701 | 0.421937 | 0 |
| uniform | reversed | 60 | 13 | 1.378765 | 0.746111 | 60 |
| lexical | reversed | 60 | 31 | 1.323710 | 0.717805 | 14 |
| qwen25-05b-instruct-frozen | reversed | 60 | 34 | 0.966733 | 0.537541 | 0 |
| m6-qwen-fresh-start | reversed | 60 | 34 | 0.966733 | 0.537541 | 0 |
| m6-qwen-v2-trained | reversed | 60 | 13 | 1.472594 | 0.803253 | 0 |

### Every family, all predictors

| Family | Predictor | Order | n | Agreement count | NLL | Brier | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ["intent"] | m4-minilm-random-start | original | 20 | 6 | 1.373597 | 0.743812 | 0 |
| ["intent"] | m4-minilm-trained | original | 20 | 17 | 0.500164 | 0.236403 | 0 |
| ["intent"] | m4-msmarco-pretrained-start | original | 20 | 18 | 0.381560 | 0.187610 | 0 |
| ["intent"] | m4-msmarco-trained | original | 20 | 18 | 0.251990 | 0.158071 | 0 |
| ["intent"] | m2-v1-trained | original | 20 | 20 | 0.067838 | 0.034814 | 0 |
| ["intent"] | m3-v1-trained | original | 20 | 19 | 0.211817 | 0.095649 | 0 |
| ["intent"] | uniform | original | 20 | 6 | 1.370160 | 0.741667 | 20 |
| ["intent"] | lexical | original | 20 | 16 | 1.216725 | 0.662010 | 0 |
| ["intent"] | qwen25-05b-instruct-frozen | original | 20 | 20 | 0.025459 | 0.006885 | 0 |
| ["intent"] | m6-qwen-fresh-start | original | 20 | 20 | 0.025459 | 0.006885 | 0 |
| ["intent"] | m6-qwen-v2-trained | original | 20 | 6 | 1.429288 | 0.770548 | 0 |
| ["sentiment"] | m4-minilm-random-start | original | 20 | 6 | 1.382234 | 0.747981 | 0 |
| ["sentiment"] | m4-minilm-trained | original | 20 | 13 | 0.845449 | 0.453248 | 0 |
| ["sentiment"] | m4-msmarco-pretrained-start | original | 20 | 7 | 1.332485 | 0.725701 | 0 |
| ["sentiment"] | m4-msmarco-trained | original | 20 | 17 | 0.569368 | 0.308788 | 0 |
| ["sentiment"] | m2-v1-trained | original | 20 | 11 | 1.066200 | 0.583331 | 0 |
| ["sentiment"] | m3-v1-trained | original | 20 | 14 | 0.806437 | 0.426859 | 0 |
| ["sentiment"] | uniform | original | 20 | 5 | 1.386294 | 0.750000 | 20 |
| ["sentiment"] | lexical | original | 20 | 5 | 1.380693 | 0.747237 | 14 |
| ["sentiment"] | qwen25-05b-instruct-frozen | original | 20 | 9 | 1.685479 | 0.842102 | 0 |
| ["sentiment"] | m6-qwen-fresh-start | original | 20 | 9 | 1.685479 | 0.842102 | 0 |
| ["sentiment"] | m6-qwen-v2-trained | original | 20 | 5 | 1.458895 | 0.788572 | 0 |
| ["rule_application"] | m4-minilm-random-start | original | 20 | 8 | 1.378970 | 0.746317 | 0 |
| ["rule_application"] | m4-minilm-trained | original | 20 | 4 | 1.377048 | 0.744755 | 0 |
| ["rule_application"] | m4-msmarco-pretrained-start | original | 20 | 5 | 1.366589 | 0.743357 | 0 |
| ["rule_application"] | m4-msmarco-trained | original | 20 | 7 | 1.316504 | 0.713169 | 0 |
| ["rule_application"] | m2-v1-trained | original | 20 | 4 | 1.431825 | 0.766483 | 0 |
| ["rule_application"] | m3-v1-trained | original | 20 | 7 | 1.362848 | 0.743303 | 0 |
| ["rule_application"] | uniform | original | 20 | 6 | 1.379841 | 0.746667 | 20 |
| ["rule_application"] | lexical | original | 20 | 8 | 1.373712 | 0.744168 | 0 |
| ["rule_application"] | qwen25-05b-instruct-frozen | original | 20 | 6 | 1.873184 | 0.948396 | 0 |
| ["rule_application"] | m6-qwen-fresh-start | original | 20 | 6 | 1.873184 | 0.948396 | 0 |
| ["rule_application"] | m6-qwen-v2-trained | original | 20 | 6 | 1.440470 | 0.774922 | 0 |
| ["intent"] | m4-minilm-random-start | reversed | 20 | 6 | 1.373597 | 0.743812 | 0 |
| ["intent"] | m4-minilm-trained | reversed | 20 | 17 | 0.500164 | 0.236403 | 0 |
| ["intent"] | m4-msmarco-pretrained-start | reversed | 20 | 18 | 0.381560 | 0.187610 | 0 |
| ["intent"] | m4-msmarco-trained | reversed | 20 | 18 | 0.251990 | 0.158071 | 0 |
| ["intent"] | m2-v1-trained | reversed | 20 | 20 | 0.067838 | 0.034814 | 0 |
| ["intent"] | m3-v1-trained | reversed | 20 | 19 | 0.211817 | 0.095649 | 0 |
| ["intent"] | uniform | reversed | 20 | 4 | 1.370160 | 0.741667 | 20 |
| ["intent"] | lexical | reversed | 20 | 16 | 1.216725 | 0.662010 | 0 |
| ["intent"] | qwen25-05b-instruct-frozen | reversed | 20 | 18 | 0.114291 | 0.087435 | 0 |
| ["intent"] | m6-qwen-fresh-start | reversed | 20 | 18 | 0.114291 | 0.087435 | 0 |
| ["intent"] | m6-qwen-v2-trained | reversed | 20 | 4 | 1.483218 | 0.812825 | 0 |
| ["sentiment"] | m4-minilm-random-start | reversed | 20 | 6 | 1.382234 | 0.747981 | 0 |
| ["sentiment"] | m4-minilm-trained | reversed | 20 | 13 | 0.845449 | 0.453248 | 0 |
| ["sentiment"] | m4-msmarco-pretrained-start | reversed | 20 | 7 | 1.332485 | 0.725701 | 0 |
| ["sentiment"] | m4-msmarco-trained | reversed | 20 | 17 | 0.569368 | 0.308788 | 0 |
| ["sentiment"] | m2-v1-trained | reversed | 20 | 11 | 1.066200 | 0.583331 | 0 |
| ["sentiment"] | m3-v1-trained | reversed | 20 | 14 | 0.806437 | 0.426859 | 0 |
| ["sentiment"] | uniform | reversed | 20 | 5 | 1.386294 | 0.750000 | 20 |
| ["sentiment"] | lexical | reversed | 20 | 7 | 1.380693 | 0.747237 | 14 |
| ["sentiment"] | qwen25-05b-instruct-frozen | reversed | 20 | 10 | 1.311595 | 0.692081 | 0 |
| ["sentiment"] | m6-qwen-fresh-start | reversed | 20 | 10 | 1.311595 | 0.692081 | 0 |
| ["sentiment"] | m6-qwen-v2-trained | reversed | 20 | 5 | 1.458932 | 0.788693 | 0 |
| ["rule_application"] | m4-minilm-random-start | reversed | 20 | 8 | 1.378970 | 0.746317 | 0 |
| ["rule_application"] | m4-minilm-trained | reversed | 20 | 4 | 1.377048 | 0.744755 | 0 |
| ["rule_application"] | m4-msmarco-pretrained-start | reversed | 20 | 5 | 1.366589 | 0.743357 | 0 |
| ["rule_application"] | m4-msmarco-trained | reversed | 20 | 7 | 1.316504 | 0.713169 | 0 |
| ["rule_application"] | m2-v1-trained | reversed | 20 | 4 | 1.431825 | 0.766483 | 0 |
| ["rule_application"] | m3-v1-trained | reversed | 20 | 7 | 1.362848 | 0.743303 | 0 |
| ["rule_application"] | uniform | reversed | 20 | 4 | 1.379841 | 0.746667 | 20 |
| ["rule_application"] | lexical | reversed | 20 | 8 | 1.373712 | 0.744168 | 0 |
| ["rule_application"] | qwen25-05b-instruct-frozen | reversed | 20 | 6 | 1.474312 | 0.833109 | 0 |
| ["rule_application"] | m6-qwen-fresh-start | reversed | 20 | 6 | 1.474312 | 0.833109 | 0 |
| ["rule_application"] | m6-qwen-v2-trained | reversed | 20 | 4 | 1.475633 | 0.808240 | 0 |

### Order robustness: all predictors and families

| Family/unit | Predictor | Pairs | Flips | Both | Original only | Reverse only | Neither | TV | Max change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [] | m4-minilm-random-start | 60 | 0 | 20 | 0 | 0 | 40 | 0.000000 | 0.000000 |
| ["intent"] | m4-minilm-random-start | 20 | 0 | 6 | 0 | 0 | 14 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-minilm-random-start | 20 | 0 | 6 | 0 | 0 | 14 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-minilm-random-start | 20 | 0 | 8 | 0 | 0 | 12 | 0.000000 | 0.000000 |
| [] | m4-minilm-trained | 60 | 0 | 34 | 0 | 0 | 26 | 0.000000 | 0.000000 |
| ["intent"] | m4-minilm-trained | 20 | 0 | 17 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-minilm-trained | 20 | 0 | 13 | 0 | 0 | 7 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-minilm-trained | 20 | 0 | 4 | 0 | 0 | 16 | 0.000000 | 0.000000 |
| [] | m4-msmarco-pretrained-start | 60 | 0 | 30 | 0 | 0 | 30 | 0.000000 | 0.000000 |
| ["intent"] | m4-msmarco-pretrained-start | 20 | 0 | 18 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-msmarco-pretrained-start | 20 | 0 | 7 | 0 | 0 | 13 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-msmarco-pretrained-start | 20 | 0 | 5 | 0 | 0 | 15 | 0.000000 | 0.000000 |
| [] | m4-msmarco-trained | 60 | 0 | 42 | 0 | 0 | 18 | 0.000000 | 0.000000 |
| ["intent"] | m4-msmarco-trained | 20 | 0 | 18 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-msmarco-trained | 20 | 0 | 17 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-msmarco-trained | 20 | 0 | 7 | 0 | 0 | 13 | 0.000000 | 0.000000 |
| [] | m2-v1-trained | 60 | 0 | 35 | 0 | 0 | 25 | 0.000000 | 0.000000 |
| ["intent"] | m2-v1-trained | 20 | 0 | 20 | 0 | 0 | 0 | 0.000000 | 0.000000 |
| ["sentiment"] | m2-v1-trained | 20 | 0 | 11 | 0 | 0 | 9 | 0.000000 | 0.000000 |
| ["rule_application"] | m2-v1-trained | 20 | 0 | 4 | 0 | 0 | 16 | 0.000000 | 0.000000 |
| [] | m3-v1-trained | 60 | 0 | 40 | 0 | 0 | 20 | 0.000000 | 0.000000 |
| ["intent"] | m3-v1-trained | 20 | 0 | 19 | 0 | 0 | 1 | 0.000000 | 0.000000 |
| ["sentiment"] | m3-v1-trained | 20 | 0 | 14 | 0 | 0 | 6 | 0.000000 | 0.000000 |
| ["rule_application"] | m3-v1-trained | 20 | 0 | 7 | 0 | 0 | 13 | 0.000000 | 0.000000 |
| [] | uniform | 60 | 60 | 0 | 17 | 13 | 30 | 0.000000 | 0.000000 |
| ["intent"] | uniform | 20 | 20 | 0 | 6 | 4 | 10 | 0.000000 | 0.000000 |
| ["sentiment"] | uniform | 20 | 20 | 0 | 5 | 5 | 10 | 0.000000 | 0.000000 |
| ["rule_application"] | uniform | 20 | 20 | 0 | 6 | 4 | 10 | 0.000000 | 0.000000 |
| [] | lexical | 60 | 14 | 26 | 3 | 5 | 26 | 0.000000 | 0.000000 |
| ["intent"] | lexical | 20 | 0 | 16 | 0 | 0 | 4 | 0.000000 | 0.000000 |
| ["sentiment"] | lexical | 20 | 14 | 2 | 3 | 5 | 10 | 0.000000 | 0.000000 |
| ["rule_application"] | lexical | 20 | 0 | 8 | 0 | 0 | 12 | 0.000000 | 0.000000 |
| [] | qwen25-05b-instruct-frozen | 60 | 19 | 28 | 7 | 6 | 19 | 0.244710 | 0.780268 |
| ["intent"] | qwen25-05b-instruct-frozen | 20 | 2 | 18 | 2 | 0 | 0 | 0.068672 | 0.622547 |
| ["sentiment"] | qwen25-05b-instruct-frozen | 20 | 7 | 7 | 2 | 3 | 8 | 0.329284 | 0.780268 |
| ["rule_application"] | qwen25-05b-instruct-frozen | 20 | 10 | 3 | 3 | 3 | 11 | 0.336173 | 0.716424 |
| [] | m6-qwen-fresh-start | 60 | 19 | 28 | 7 | 6 | 19 | 0.244710 | 0.780268 |
| ["intent"] | m6-qwen-fresh-start | 20 | 2 | 18 | 2 | 0 | 0 | 0.068672 | 0.622547 |
| ["sentiment"] | m6-qwen-fresh-start | 20 | 7 | 7 | 2 | 3 | 8 | 0.329284 | 0.780268 |
| ["rule_application"] | m6-qwen-fresh-start | 20 | 10 | 3 | 3 | 3 | 11 | 0.336173 | 0.716424 |
| [] | m6-qwen-v2-trained | 60 | 60 | 0 | 17 | 13 | 30 | 0.190760 | 0.310205 |
| ["intent"] | m6-qwen-v2-trained | 20 | 20 | 0 | 6 | 4 | 10 | 0.213537 | 0.306953 |
| ["sentiment"] | m6-qwen-v2-trained | 20 | 20 | 0 | 5 | 5 | 10 | 0.170508 | 0.145606 |
| ["rule_application"] | m6-qwen-v2-trained | 20 | 20 | 0 | 6 | 4 | 10 | 0.188237 | 0.310205 |

## new-v2 — all 11 predictors

| Predictor | Order | n | Agreement count | NLL | Brier | Ties |
| --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | original | 240 | 66 | 1.332467 | 0.733140 | 0 |
| m4-minilm-trained | original | 240 | 132 | 0.823115 | 0.460115 | 0 |
| m4-msmarco-pretrained-start | original | 240 | 99 | 1.058568 | 0.581492 | 0 |
| m4-msmarco-trained | original | 240 | 141 | 0.917258 | 0.481392 | 0 |
| m2-v1-trained | original | 240 | 107 | 1.136427 | 0.606945 | 0 |
| m3-v1-trained | original | 240 | 110 | 1.024844 | 0.555299 | 0 |
| uniform | original | 240 | 65 | 1.333463 | 0.733681 | 240 |
| lexical | original | 240 | 99 | 1.296868 | 0.712801 | 121 |
| qwen25-05b-instruct-frozen | original | 240 | 129 | 1.312350 | 0.633492 | 0 |
| m6-qwen-fresh-start | original | 240 | 129 | 1.312350 | 0.633492 | 0 |
| m6-qwen-v2-trained | original | 240 | 65 | 1.413320 | 0.779200 | 0 |
| m4-minilm-random-start | reversed | 240 | 66 | 1.332467 | 0.733140 | 0 |
| m4-minilm-trained | reversed | 240 | 132 | 0.823115 | 0.460115 | 0 |
| m4-msmarco-pretrained-start | reversed | 240 | 99 | 1.058568 | 0.581492 | 0 |
| m4-msmarco-trained | reversed | 240 | 141 | 0.917258 | 0.481392 | 0 |
| m2-v1-trained | reversed | 240 | 107 | 1.136427 | 0.606945 | 0 |
| m3-v1-trained | reversed | 240 | 110 | 1.024844 | 0.555299 | 0 |
| uniform | reversed | 240 | 65 | 1.333463 | 0.733681 | 240 |
| lexical | reversed | 240 | 99 | 1.296868 | 0.712801 | 121 |
| qwen25-05b-instruct-frozen | reversed | 240 | 118 | 1.410621 | 0.687402 | 0 |
| m6-qwen-fresh-start | reversed | 240 | 118 | 1.410621 | 0.687402 | 0 |
| m6-qwen-v2-trained | reversed | 240 | 65 | 1.407130 | 0.778134 | 0 |

### Every family, all predictors

| Family | Predictor | Order | n | Agreement count | NLL | Brier | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ["intent"] | m4-minilm-random-start | original | 80 | 27 | 1.308764 | 0.723961 | 0 |
| ["intent"] | m4-minilm-trained | original | 80 | 74 | 0.184336 | 0.117682 | 0 |
| ["intent"] | m4-msmarco-pretrained-start | original | 80 | 66 | 0.424631 | 0.233929 | 0 |
| ["intent"] | m4-msmarco-trained | original | 80 | 77 | 0.091450 | 0.049058 | 0 |
| ["intent"] | m2-v1-trained | original | 80 | 66 | 0.505941 | 0.251171 | 0 |
| ["intent"] | m3-v1-trained | original | 80 | 72 | 0.318603 | 0.163092 | 0 |
| ["intent"] | uniform | original | 80 | 22 | 1.310510 | 0.725000 | 80 |
| ["intent"] | lexical | original | 80 | 63 | 1.179489 | 0.652086 | 5 |
| ["intent"] | qwen25-05b-instruct-frozen | original | 80 | 74 | 0.205688 | 0.117439 | 0 |
| ["intent"] | m6-qwen-fresh-start | original | 80 | 74 | 0.205688 | 0.117439 | 0 |
| ["intent"] | m6-qwen-v2-trained | original | 80 | 22 | 1.405235 | 0.779970 | 0 |
| ["sentiment"] | m4-minilm-random-start | original | 80 | 18 | 1.386599 | 0.750152 | 0 |
| ["sentiment"] | m4-minilm-trained | original | 80 | 43 | 0.941779 | 0.517597 | 0 |
| ["sentiment"] | m4-msmarco-pretrained-start | original | 80 | 18 | 1.392514 | 0.753045 | 0 |
| ["sentiment"] | m4-msmarco-trained | original | 80 | 43 | 1.249159 | 0.629578 | 0 |
| ["sentiment"] | m2-v1-trained | original | 80 | 22 | 1.567983 | 0.830625 | 0 |
| ["sentiment"] | m3-v1-trained | original | 80 | 24 | 1.350882 | 0.732680 | 0 |
| ["sentiment"] | uniform | original | 80 | 20 | 1.386294 | 0.750000 | 80 |
| ["sentiment"] | lexical | original | 80 | 19 | 1.387730 | 0.750727 | 53 |
| ["sentiment"] | qwen25-05b-instruct-frozen | original | 80 | 30 | 1.965885 | 0.900924 | 0 |
| ["sentiment"] | m6-qwen-fresh-start | original | 80 | 30 | 1.965885 | 0.900924 | 0 |
| ["sentiment"] | m6-qwen-v2-trained | original | 80 | 20 | 1.459393 | 0.788880 | 0 |
| ["rule_application"] | m4-minilm-random-start | original | 80 | 21 | 1.302037 | 0.725306 | 0 |
| ["rule_application"] | m4-minilm-trained | original | 80 | 15 | 1.343231 | 0.745066 | 0 |
| ["rule_application"] | m4-msmarco-pretrained-start | original | 80 | 15 | 1.358558 | 0.757503 | 0 |
| ["rule_application"] | m4-msmarco-trained | original | 80 | 21 | 1.411166 | 0.765541 | 0 |
| ["rule_application"] | m2-v1-trained | original | 80 | 19 | 1.335358 | 0.739039 | 0 |
| ["rule_application"] | m3-v1-trained | original | 80 | 14 | 1.405047 | 0.770123 | 0 |
| ["rule_application"] | uniform | original | 80 | 23 | 1.303586 | 0.726042 | 80 |
| ["rule_application"] | lexical | original | 80 | 17 | 1.323385 | 0.735591 | 63 |
| ["rule_application"] | qwen25-05b-instruct-frozen | original | 80 | 25 | 1.765476 | 0.882113 | 0 |
| ["rule_application"] | m6-qwen-fresh-start | original | 80 | 25 | 1.765476 | 0.882113 | 0 |
| ["rule_application"] | m6-qwen-v2-trained | original | 80 | 23 | 1.375332 | 0.768751 | 0 |
| ["intent"] | m4-minilm-random-start | reversed | 80 | 27 | 1.308764 | 0.723961 | 0 |
| ["intent"] | m4-minilm-trained | reversed | 80 | 74 | 0.184336 | 0.117682 | 0 |
| ["intent"] | m4-msmarco-pretrained-start | reversed | 80 | 66 | 0.424631 | 0.233929 | 0 |
| ["intent"] | m4-msmarco-trained | reversed | 80 | 77 | 0.091450 | 0.049058 | 0 |
| ["intent"] | m2-v1-trained | reversed | 80 | 66 | 0.505941 | 0.251171 | 0 |
| ["intent"] | m3-v1-trained | reversed | 80 | 72 | 0.318603 | 0.163092 | 0 |
| ["intent"] | uniform | reversed | 80 | 24 | 1.310510 | 0.725000 | 80 |
| ["intent"] | lexical | reversed | 80 | 65 | 1.179489 | 0.652086 | 5 |
| ["intent"] | qwen25-05b-instruct-frozen | reversed | 80 | 67 | 0.315111 | 0.180698 | 0 |
| ["intent"] | m6-qwen-fresh-start | reversed | 80 | 67 | 0.315111 | 0.180698 | 0 |
| ["intent"] | m6-qwen-v2-trained | reversed | 80 | 24 | 1.370187 | 0.765136 | 0 |
| ["sentiment"] | m4-minilm-random-start | reversed | 80 | 18 | 1.386599 | 0.750152 | 0 |
| ["sentiment"] | m4-minilm-trained | reversed | 80 | 43 | 0.941779 | 0.517597 | 0 |
| ["sentiment"] | m4-msmarco-pretrained-start | reversed | 80 | 18 | 1.392514 | 0.753045 | 0 |
| ["sentiment"] | m4-msmarco-trained | reversed | 80 | 43 | 1.249159 | 0.629578 | 0 |
| ["sentiment"] | m2-v1-trained | reversed | 80 | 22 | 1.567983 | 0.830625 | 0 |
| ["sentiment"] | m3-v1-trained | reversed | 80 | 24 | 1.350882 | 0.732680 | 0 |
| ["sentiment"] | uniform | reversed | 80 | 20 | 1.386294 | 0.750000 | 80 |
| ["sentiment"] | lexical | reversed | 80 | 16 | 1.387730 | 0.750727 | 53 |
| ["sentiment"] | qwen25-05b-instruct-frozen | reversed | 80 | 29 | 2.150896 | 0.956534 | 0 |
| ["sentiment"] | m6-qwen-fresh-start | reversed | 80 | 29 | 2.150896 | 0.956534 | 0 |
| ["sentiment"] | m6-qwen-v2-trained | reversed | 80 | 20 | 1.459597 | 0.788987 | 0 |
| ["rule_application"] | m4-minilm-random-start | reversed | 80 | 21 | 1.302037 | 0.725306 | 0 |
| ["rule_application"] | m4-minilm-trained | reversed | 80 | 15 | 1.343231 | 0.745066 | 0 |
| ["rule_application"] | m4-msmarco-pretrained-start | reversed | 80 | 15 | 1.358558 | 0.757503 | 0 |
| ["rule_application"] | m4-msmarco-trained | reversed | 80 | 21 | 1.411166 | 0.765541 | 0 |
| ["rule_application"] | m2-v1-trained | reversed | 80 | 19 | 1.335358 | 0.739039 | 0 |
| ["rule_application"] | m3-v1-trained | reversed | 80 | 14 | 1.405047 | 0.770123 | 0 |
| ["rule_application"] | uniform | reversed | 80 | 21 | 1.303586 | 0.726042 | 80 |
| ["rule_application"] | lexical | reversed | 80 | 18 | 1.323385 | 0.735591 | 63 |
| ["rule_application"] | qwen25-05b-instruct-frozen | reversed | 80 | 22 | 1.765856 | 0.924975 | 0 |
| ["rule_application"] | m6-qwen-fresh-start | reversed | 80 | 22 | 1.765856 | 0.924975 | 0 |
| ["rule_application"] | m6-qwen-v2-trained | reversed | 80 | 21 | 1.391606 | 0.780279 | 0 |

### Order robustness: all predictors and families

| Family/unit | Predictor | Pairs | Flips | Both | Original only | Reverse only | Neither | TV | Max change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [] | m4-minilm-random-start | 240 | 0 | 66 | 0 | 0 | 174 | 0.000000 | 0.000000 |
| ["intent"] | m4-minilm-random-start | 80 | 0 | 27 | 0 | 0 | 53 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-minilm-random-start | 80 | 0 | 18 | 0 | 0 | 62 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-minilm-random-start | 80 | 0 | 21 | 0 | 0 | 59 | 0.000000 | 0.000000 |
| [] | m4-minilm-trained | 240 | 0 | 132 | 0 | 0 | 108 | 0.000000 | 0.000000 |
| ["intent"] | m4-minilm-trained | 80 | 0 | 74 | 0 | 0 | 6 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-minilm-trained | 80 | 0 | 43 | 0 | 0 | 37 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-minilm-trained | 80 | 0 | 15 | 0 | 0 | 65 | 0.000000 | 0.000000 |
| [] | m4-msmarco-pretrained-start | 240 | 0 | 99 | 0 | 0 | 141 | 0.000000 | 0.000000 |
| ["intent"] | m4-msmarco-pretrained-start | 80 | 0 | 66 | 0 | 0 | 14 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-msmarco-pretrained-start | 80 | 0 | 18 | 0 | 0 | 62 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-msmarco-pretrained-start | 80 | 0 | 15 | 0 | 0 | 65 | 0.000000 | 0.000000 |
| [] | m4-msmarco-trained | 240 | 0 | 141 | 0 | 0 | 99 | 0.000000 | 0.000000 |
| ["intent"] | m4-msmarco-trained | 80 | 0 | 77 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-msmarco-trained | 80 | 0 | 43 | 0 | 0 | 37 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-msmarco-trained | 80 | 0 | 21 | 0 | 0 | 59 | 0.000000 | 0.000000 |
| [] | m2-v1-trained | 240 | 0 | 107 | 0 | 0 | 133 | 0.000000 | 0.000000 |
| ["intent"] | m2-v1-trained | 80 | 0 | 66 | 0 | 0 | 14 | 0.000000 | 0.000000 |
| ["sentiment"] | m2-v1-trained | 80 | 0 | 22 | 0 | 0 | 58 | 0.000000 | 0.000000 |
| ["rule_application"] | m2-v1-trained | 80 | 0 | 19 | 0 | 0 | 61 | 0.000000 | 0.000000 |
| [] | m3-v1-trained | 240 | 0 | 110 | 0 | 0 | 130 | 0.000000 | 0.000000 |
| ["intent"] | m3-v1-trained | 80 | 0 | 72 | 0 | 0 | 8 | 0.000000 | 0.000000 |
| ["sentiment"] | m3-v1-trained | 80 | 0 | 24 | 0 | 0 | 56 | 0.000000 | 0.000000 |
| ["rule_application"] | m3-v1-trained | 80 | 0 | 14 | 0 | 0 | 66 | 0.000000 | 0.000000 |
| [] | uniform | 240 | 240 | 0 | 65 | 65 | 110 | 0.000000 | 0.000000 |
| ["intent"] | uniform | 80 | 80 | 0 | 22 | 24 | 34 | 0.000000 | 0.000000 |
| ["sentiment"] | uniform | 80 | 80 | 0 | 20 | 20 | 40 | 0.000000 | 0.000000 |
| ["rule_application"] | uniform | 80 | 80 | 0 | 23 | 21 | 36 | 0.000000 | 0.000000 |
| [] | lexical | 240 | 121 | 70 | 29 | 29 | 112 | 0.000000 | 0.000000 |
| ["intent"] | lexical | 80 | 5 | 62 | 1 | 3 | 14 | 0.000000 | 0.000000 |
| ["sentiment"] | lexical | 80 | 53 | 4 | 15 | 12 | 49 | 0.000000 | 0.000000 |
| ["rule_application"] | lexical | 80 | 63 | 4 | 13 | 14 | 49 | 0.000000 | 0.000000 |
| [] | qwen25-05b-instruct-frozen | 240 | 122 | 82 | 47 | 36 | 75 | 0.330491 | 0.947695 |
| ["intent"] | qwen25-05b-instruct-frozen | 80 | 14 | 64 | 10 | 3 | 3 | 0.190781 | 0.885970 |
| ["sentiment"] | qwen25-05b-instruct-frozen | 80 | 43 | 14 | 16 | 15 | 35 | 0.407972 | 0.947695 |
| ["rule_application"] | qwen25-05b-instruct-frozen | 80 | 65 | 4 | 21 | 18 | 37 | 0.392720 | 0.910997 |
| [] | m6-qwen-fresh-start | 240 | 122 | 82 | 47 | 36 | 75 | 0.330491 | 0.947695 |
| ["intent"] | m6-qwen-fresh-start | 80 | 14 | 64 | 10 | 3 | 3 | 0.190781 | 0.885970 |
| ["sentiment"] | m6-qwen-fresh-start | 80 | 43 | 14 | 16 | 15 | 35 | 0.407972 | 0.947695 |
| ["rule_application"] | m6-qwen-fresh-start | 80 | 65 | 4 | 21 | 18 | 37 | 0.392720 | 0.910997 |
| [] | m6-qwen-v2-trained | 240 | 240 | 0 | 65 | 65 | 110 | 0.206962 | 0.310961 |
| ["intent"] | m6-qwen-v2-trained | 80 | 80 | 0 | 22 | 24 | 34 | 0.238446 | 0.306024 |
| ["sentiment"] | m6-qwen-v2-trained | 80 | 80 | 0 | 20 | 20 | 40 | 0.171867 | 0.147273 |
| ["rule_application"] | m6-qwen-v2-trained | 80 | 80 | 0 | 23 | 21 | 36 | 0.210572 | 0.310961 |

## probes — all 11 predictors

| Predictor | Order | n | Agreement count | NLL | Brier | Ties |
| --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | original | 12 | 1 | 1.057107 | 0.647165 | 0 |
| m4-minilm-trained | original | 12 | 6 | 1.025456 | 0.628466 | 0 |
| m4-msmarco-pretrained-start | original | 12 | 7 | 1.453783 | 0.651840 | 0 |
| m4-msmarco-trained | original | 12 | 5 | 1.876464 | 0.770313 | 0 |
| m2-v1-trained | original | 12 | 8 | 0.710407 | 0.441728 | 0 |
| m3-v1-trained | original | 12 | 4 | 1.360701 | 0.653598 | 0 |
| uniform | original | 12 | 4 | 1.055008 | 0.645833 | 12 |
| lexical | original | 12 | 4 | 1.047044 | 0.646289 | 4 |
| qwen25-05b-instruct-frozen | original | 12 | 9 | 0.649621 | 0.317726 | 0 |
| m6-qwen-fresh-start | original | 12 | 9 | 0.649621 | 0.317726 | 0 |
| m6-qwen-v2-trained | original | 12 | 4 | 1.175404 | 0.726504 | 0 |
| m4-minilm-random-start | reversed | 12 | 1 | 1.057107 | 0.647165 | 0 |
| m4-minilm-trained | reversed | 12 | 6 | 1.025456 | 0.628466 | 0 |
| m4-msmarco-pretrained-start | reversed | 12 | 7 | 1.453783 | 0.651840 | 0 |
| m4-msmarco-trained | reversed | 12 | 5 | 1.876464 | 0.770313 | 0 |
| m2-v1-trained | reversed | 12 | 8 | 0.710407 | 0.441728 | 0 |
| m3-v1-trained | reversed | 12 | 4 | 1.360701 | 0.653598 | 0 |
| uniform | reversed | 12 | 4 | 1.055008 | 0.645833 | 12 |
| lexical | reversed | 12 | 5 | 1.047044 | 0.646289 | 4 |
| qwen25-05b-instruct-frozen | reversed | 12 | 11 | 0.419398 | 0.251247 | 0 |
| m6-qwen-fresh-start | reversed | 12 | 11 | 0.419398 | 0.251247 | 0 |
| m6-qwen-v2-trained | reversed | 12 | 4 | 1.172018 | 0.749054 | 0 |

### Every family, all predictors

| Family | Predictor | Order | n | Agreement count | NLL | Brier | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ["intent"] | m4-minilm-random-start | original | 4 | 1 | 1.089613 | 0.660632 | 0 |
| ["intent"] | m4-minilm-trained | original | 4 | 3 | 0.765721 | 0.455262 | 0 |
| ["intent"] | m4-msmarco-pretrained-start | original | 4 | 2 | 2.299398 | 0.745675 | 0 |
| ["intent"] | m4-msmarco-trained | original | 4 | 1 | 1.412754 | 0.742417 | 0 |
| ["intent"] | m2-v1-trained | original | 4 | 3 | 0.598436 | 0.335200 | 0 |
| ["intent"] | m3-v1-trained | original | 4 | 2 | 0.919648 | 0.600724 | 0 |
| ["intent"] | uniform | original | 4 | 1 | 1.098612 | 0.666667 | 4 |
| ["intent"] | lexical | original | 4 | 1 | 1.094522 | 0.664120 | 1 |
| ["intent"] | qwen25-05b-instruct-frozen | original | 4 | 4 | 0.072750 | 0.021146 | 0 |
| ["intent"] | m6-qwen-fresh-start | original | 4 | 4 | 0.072750 | 0.021146 | 0 |
| ["intent"] | m6-qwen-v2-trained | original | 4 | 1 | 1.293588 | 0.802238 | 0 |
| ["sentiment"] | m4-minilm-random-start | original | 4 | 0 | 1.182186 | 0.694558 | 0 |
| ["sentiment"] | m4-minilm-trained | original | 4 | 2 | 1.001136 | 0.557945 | 0 |
| ["sentiment"] | m4-msmarco-pretrained-start | original | 4 | 2 | 0.988742 | 0.635281 | 0 |
| ["sentiment"] | m4-msmarco-trained | original | 4 | 2 | 1.579008 | 0.855648 | 0 |
| ["sentiment"] | m2-v1-trained | original | 4 | 3 | 0.620252 | 0.361928 | 0 |
| ["sentiment"] | m3-v1-trained | original | 4 | 0 | 1.078186 | 0.664176 | 0 |
| ["sentiment"] | uniform | original | 4 | 1 | 1.170533 | 0.687500 | 4 |
| ["sentiment"] | lexical | original | 4 | 1 | 1.145011 | 0.671019 | 3 |
| ["sentiment"] | qwen25-05b-instruct-frozen | original | 4 | 2 | 1.582648 | 0.736623 | 0 |
| ["sentiment"] | m6-qwen-fresh-start | original | 4 | 2 | 1.582648 | 0.736623 | 0 |
| ["sentiment"] | m6-qwen-v2-trained | original | 4 | 1 | 1.325340 | 0.825412 | 0 |
| ["rule_application"] | m4-minilm-random-start | original | 4 | 0 | 0.899523 | 0.586306 | 0 |
| ["rule_application"] | m4-minilm-trained | original | 4 | 1 | 1.309512 | 0.872190 | 0 |
| ["rule_application"] | m4-msmarco-pretrained-start | original | 4 | 3 | 1.073209 | 0.574565 | 0 |
| ["rule_application"] | m4-msmarco-trained | original | 4 | 2 | 2.637630 | 0.712874 | 0 |
| ["rule_application"] | m2-v1-trained | original | 4 | 2 | 0.912532 | 0.628056 | 0 |
| ["rule_application"] | m3-v1-trained | original | 4 | 2 | 2.084269 | 0.695893 | 0 |
| ["rule_application"] | uniform | original | 4 | 2 | 0.895880 | 0.583333 | 4 |
| ["rule_application"] | lexical | original | 4 | 2 | 0.901599 | 0.603728 | 0 |
| ["rule_application"] | qwen25-05b-instruct-frozen | original | 4 | 3 | 0.293465 | 0.195409 | 0 |
| ["rule_application"] | m6-qwen-fresh-start | original | 4 | 3 | 0.293465 | 0.195409 | 0 |
| ["rule_application"] | m6-qwen-v2-trained | original | 4 | 2 | 0.907284 | 0.551863 | 0 |
| ["intent"] | m4-minilm-random-start | reversed | 4 | 1 | 1.089613 | 0.660632 | 0 |
| ["intent"] | m4-minilm-trained | reversed | 4 | 3 | 0.765721 | 0.455262 | 0 |
| ["intent"] | m4-msmarco-pretrained-start | reversed | 4 | 2 | 2.299398 | 0.745675 | 0 |
| ["intent"] | m4-msmarco-trained | reversed | 4 | 1 | 1.412754 | 0.742417 | 0 |
| ["intent"] | m2-v1-trained | reversed | 4 | 3 | 0.598436 | 0.335200 | 0 |
| ["intent"] | m3-v1-trained | reversed | 4 | 2 | 0.919648 | 0.600724 | 0 |
| ["intent"] | uniform | reversed | 4 | 1 | 1.098612 | 0.666667 | 4 |
| ["intent"] | lexical | reversed | 4 | 1 | 1.094522 | 0.664120 | 1 |
| ["intent"] | qwen25-05b-instruct-frozen | reversed | 4 | 4 | 0.244891 | 0.123445 | 0 |
| ["intent"] | m6-qwen-fresh-start | reversed | 4 | 4 | 0.244891 | 0.123445 | 0 |
| ["intent"] | m6-qwen-v2-trained | reversed | 4 | 1 | 1.294323 | 0.802728 | 0 |
| ["sentiment"] | m4-minilm-random-start | reversed | 4 | 0 | 1.182186 | 0.694558 | 0 |
| ["sentiment"] | m4-minilm-trained | reversed | 4 | 2 | 1.001136 | 0.557945 | 0 |
| ["sentiment"] | m4-msmarco-pretrained-start | reversed | 4 | 2 | 0.988742 | 0.635281 | 0 |
| ["sentiment"] | m4-msmarco-trained | reversed | 4 | 2 | 1.579008 | 0.855648 | 0 |
| ["sentiment"] | m2-v1-trained | reversed | 4 | 3 | 0.620252 | 0.361928 | 0 |
| ["sentiment"] | m3-v1-trained | reversed | 4 | 0 | 1.078186 | 0.664176 | 0 |
| ["sentiment"] | uniform | reversed | 4 | 2 | 1.170533 | 0.687500 | 4 |
| ["sentiment"] | lexical | reversed | 4 | 2 | 1.145011 | 0.671019 | 3 |
| ["sentiment"] | qwen25-05b-instruct-frozen | reversed | 4 | 4 | 0.162786 | 0.104993 | 0 |
| ["sentiment"] | m6-qwen-fresh-start | reversed | 4 | 4 | 0.162786 | 0.104993 | 0 |
| ["sentiment"] | m6-qwen-v2-trained | reversed | 4 | 2 | 1.026201 | 0.590215 | 0 |
| ["rule_application"] | m4-minilm-random-start | reversed | 4 | 0 | 0.899523 | 0.586306 | 0 |
| ["rule_application"] | m4-minilm-trained | reversed | 4 | 1 | 1.309512 | 0.872190 | 0 |
| ["rule_application"] | m4-msmarco-pretrained-start | reversed | 4 | 3 | 1.073209 | 0.574565 | 0 |
| ["rule_application"] | m4-msmarco-trained | reversed | 4 | 2 | 2.637630 | 0.712874 | 0 |
| ["rule_application"] | m2-v1-trained | reversed | 4 | 2 | 0.912532 | 0.628056 | 0 |
| ["rule_application"] | m3-v1-trained | reversed | 4 | 2 | 2.084269 | 0.695893 | 0 |
| ["rule_application"] | uniform | reversed | 4 | 1 | 0.895880 | 0.583333 | 4 |
| ["rule_application"] | lexical | reversed | 4 | 2 | 0.901599 | 0.603728 | 0 |
| ["rule_application"] | qwen25-05b-instruct-frozen | reversed | 4 | 3 | 0.850518 | 0.525304 | 0 |
| ["rule_application"] | m6-qwen-fresh-start | reversed | 4 | 3 | 0.850518 | 0.525304 | 0 |
| ["rule_application"] | m6-qwen-v2-trained | reversed | 4 | 1 | 1.195530 | 0.854220 | 0 |

### Order robustness: all predictors and families

| Family/unit | Predictor | Pairs | Flips | Both | Original only | Reverse only | Neither | TV | Max change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [] | m4-minilm-random-start | 12 | 0 | 1 | 0 | 0 | 11 | 0.000000 | 0.000000 |
| ["intent"] | m4-minilm-random-start | 4 | 0 | 1 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-minilm-random-start | 4 | 0 | 0 | 0 | 0 | 4 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-minilm-random-start | 4 | 0 | 0 | 0 | 0 | 4 | 0.000000 | 0.000000 |
| [] | m4-minilm-trained | 12 | 0 | 6 | 0 | 0 | 6 | 0.000000 | 0.000000 |
| ["intent"] | m4-minilm-trained | 4 | 0 | 3 | 0 | 0 | 1 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-minilm-trained | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-minilm-trained | 4 | 0 | 1 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| [] | m4-msmarco-pretrained-start | 12 | 0 | 7 | 0 | 0 | 5 | 0.000000 | 0.000000 |
| ["intent"] | m4-msmarco-pretrained-start | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-msmarco-pretrained-start | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-msmarco-pretrained-start | 4 | 0 | 3 | 0 | 0 | 1 | 0.000000 | 0.000000 |
| [] | m4-msmarco-trained | 12 | 0 | 5 | 0 | 0 | 7 | 0.000000 | 0.000000 |
| ["intent"] | m4-msmarco-trained | 4 | 0 | 1 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| ["sentiment"] | m4-msmarco-trained | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["rule_application"] | m4-msmarco-trained | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| [] | m2-v1-trained | 12 | 0 | 8 | 0 | 0 | 4 | 0.000000 | 0.000000 |
| ["intent"] | m2-v1-trained | 4 | 0 | 3 | 0 | 0 | 1 | 0.000000 | 0.000000 |
| ["sentiment"] | m2-v1-trained | 4 | 0 | 3 | 0 | 0 | 1 | 0.000000 | 0.000000 |
| ["rule_application"] | m2-v1-trained | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| [] | m3-v1-trained | 12 | 0 | 4 | 0 | 0 | 8 | 0.000000 | 0.000000 |
| ["intent"] | m3-v1-trained | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| ["sentiment"] | m3-v1-trained | 4 | 0 | 0 | 0 | 0 | 4 | 0.000000 | 0.000000 |
| ["rule_application"] | m3-v1-trained | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| [] | uniform | 12 | 12 | 0 | 4 | 4 | 4 | 0.000000 | 0.000000 |
| ["intent"] | uniform | 4 | 4 | 0 | 1 | 1 | 2 | 0.000000 | 0.000000 |
| ["sentiment"] | uniform | 4 | 4 | 0 | 1 | 2 | 1 | 0.000000 | 0.000000 |
| ["rule_application"] | uniform | 4 | 4 | 0 | 2 | 1 | 1 | 0.000000 | 0.000000 |
| [] | lexical | 12 | 4 | 3 | 1 | 2 | 6 | 0.000000 | 0.000000 |
| ["intent"] | lexical | 4 | 1 | 1 | 0 | 0 | 3 | 0.000000 | 0.000000 |
| ["sentiment"] | lexical | 4 | 3 | 0 | 1 | 2 | 1 | 0.000000 | 0.000000 |
| ["rule_application"] | lexical | 4 | 0 | 2 | 0 | 0 | 2 | 0.000000 | 0.000000 |
| [] | qwen25-05b-instruct-frozen | 12 | 2 | 9 | 0 | 2 | 1 | 0.257527 | 0.987729 |
| ["intent"] | qwen25-05b-instruct-frozen | 4 | 0 | 4 | 0 | 0 | 0 | 0.154093 | 0.304032 |
| ["sentiment"] | qwen25-05b-instruct-frozen | 4 | 2 | 2 | 0 | 2 | 0 | 0.410378 | 0.987729 |
| ["rule_application"] | qwen25-05b-instruct-frozen | 4 | 0 | 3 | 0 | 0 | 1 | 0.208110 | 0.382657 |
| [] | m6-qwen-fresh-start | 12 | 2 | 9 | 0 | 2 | 1 | 0.257527 | 0.987729 |
| ["intent"] | m6-qwen-fresh-start | 4 | 0 | 4 | 0 | 0 | 0 | 0.154093 | 0.304032 |
| ["sentiment"] | m6-qwen-fresh-start | 4 | 2 | 2 | 0 | 2 | 0 | 0.410378 | 0.987729 |
| ["rule_application"] | m6-qwen-fresh-start | 4 | 0 | 3 | 0 | 0 | 1 | 0.208110 | 0.382657 |
| [] | m6-qwen-v2-trained | 12 | 12 | 0 | 4 | 4 | 4 | 0.319989 | 0.456414 |
| ["intent"] | m6-qwen-v2-trained | 4 | 4 | 0 | 1 | 1 | 2 | 0.306643 | 0.307610 |
| ["sentiment"] | m6-qwen-v2-trained | 4 | 4 | 0 | 1 | 2 | 1 | 0.272377 | 0.307619 |
| ["rule_application"] | m6-qwen-v2-trained | 4 | 4 | 0 | 2 | 1 | 1 | 0.380945 | 0.456414 |

## Granular index

- [All orientation × source-unit × predictor metrics](all-orientation-unit-metrics.csv): every source group, producer, domain, mechanism, individual explicit policy, family × label basis, and unknown units.
- [All order × source-unit × predictor metrics](all-unit-order-metrics.csv): flips, tie-free flips, both-correct, original/reverse-only, neither, TV/max change.
- [All paired gains/losses and signed contributions](paired-gains-losses.csv): final minus fresh (= final minus P3); common-valid denominators; positive/negative NLL and Brier sums and case counts.
- [Every presentation arithmetic](per-presentation-arithmetic.csv), including all private case IDs only here.
- [Explicit E3 reviewed case→unit mapping](explicit-case-unit-mapping.csv): no ancestry parsed from IDs; policy null stays null. Frozen pair identities remain in source recipe order_pairs files pinned by source-pins.json.
- [Coverage and invalid diagnostics](coverage.csv), 33 order reports; original quality reports are checked through comparison and grouped means.
- [Exact source SHA256s](source-pins.json) and [review receipt](receipt.json).
