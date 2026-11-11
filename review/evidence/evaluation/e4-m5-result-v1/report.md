# E4 M5 fixed criterion result

**Full conjunction: FAIL.**

- coverage: True
- controls_comparable: True
- recover_lost_group: True
- no_new_error: True
- lower_probe_group_macro_loss: False
- pilot_loss_within_ceiling: True

Recovered eligible groups: eval.validation.sentiment.04. New errors: none.
All12group macro loss: historical 1.360701041; M5 1.384773252. Pilot M5 0.794524952, ceiling 0.843700812.

Cells: original target rank / target probability / signed target-minus-best-rival margin / log loss. Original is counted once per group; JSON preserves both presentations and their mean losses.

| Probe group | Historical M3 start | Historical M3 trained | M5 low-head-LR |
| --- | --- | --- | --- |
| intent.01 | 1 / 0.776807 / +0.559397 / 0.252564 | 1 / 0.682845 / +0.366630 / 0.381488 | 1 / 0.717299 / +0.435303 / 0.332263 |
| intent.02 | 2 / 0.161147 / -0.665231 / 1.825438 | 2 / 0.121467 / -0.727541 / 2.108112 | 2 / 0.119893 / -0.731471 / 2.121156 |
| intent.03 | 3 / 0.000810 / -0.524092 / 7.118072 | 3 / 0.314050 / -0.056834 / 1.158204 | 3 / 0.287107 / -0.102518 / 1.247900 |
| intent.04 | 1 / 0.998481 / +0.997386 / 0.001520 | 1 / 0.969682 / +0.948169 / 0.030788 | 1 / 0.968829 / +0.946879 / 0.031667 |
| sentiment.01 | 2 / 0.204708 / -0.549362 / 1.586171 | 2 / 0.438294 / -0.018742 / 0.824866 | 2 / 0.463801 / -0.000852 / 0.768300 |
| sentiment.02 | 4 / 0.232945 / -0.057285 / 1.456954 | 3 / 0.130976 / -0.354876 / 2.032744 | 3 / 0.134177 / -0.346046 / 2.008595 |
| sentiment.03 | 1 / 0.487243 / +0.004744 / 0.718991 | 2 / 0.491150 / -0.012360 / 0.711005 | 2 / 0.471571 / -0.051546 / 0.751686 |
| sentiment.04 | 1 / 0.824606 / +0.669155 / 0.192850 | 2 / 0.475148 / -0.024632 / 0.744129 | 1 / 0.493301 / +0.010877 / 0.706636 |
| rule_application.01 | 2 / 0.032766 / -0.934469 / 3.418378 | 2 / 0.000790 / -0.998419 / 7.142956 | 2 / 0.000570 / -0.998859 / 7.469238 |
| rule_application.02 | 1 / 0.778038 / +0.572936 / 0.250980 | 2 / 0.486317 / -0.010917 / 0.720894 | 2 / 0.492366 / -0.002837 / 0.708532 |
| rule_application.03 | 1 / 0.888894 / +0.802110 / 0.117777 | 1 / 0.990366 / +0.984762 / 0.009680 | 1 / 0.991584 / +0.986714 / 0.008452 |
| rule_application.04 | 1 / 0.603081 / +0.206162 / 0.505704 | 1 / 0.629049 / +0.258098 / 0.463546 | 1 / 0.629485 / +0.258970 / 0.462853 |

All probe labels are teacher labels, curator identity unknown. These repeatedly used development groups are not untouched final evidence or independent row trials. Missing/invalid coverage prevents success; all groups retained. Lower head LR alone is not supported under the full preregistered criterion; no default selection.
