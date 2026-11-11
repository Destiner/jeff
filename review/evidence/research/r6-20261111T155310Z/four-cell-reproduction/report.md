# R6 executed frozen four-cell diagnostic

48 preselected TRAIN cases, 16 per family; 9 (family, producer) source units; 192 conditions and 740 probability slots. These correlated cases are not IID or held-out task evidence. No targets/accuracy, second fitted bias model, source fit, learned correction, entropy or max-prob analysis.

## Execution and integrity

Input receipt was saved before derived metrics. All three supplied SHA256 pins matched. Coverage, strict option-ID joins and original-position/actual-letter/display-position mapping passed. K counts: {5: 2, 3: 11, 4: 34, 6: 1}.
Zeros: 0; ones: 0; tied presentations: 0; maximum sum error 1.37e-07; maximum float64 T=1 reconstruction error 1.31e-07. No normalization or epsilon repair.
Allowed-mass exp consistency maximum error 0; log-sum-exp/full-vocabulary logmass maximum error 1.85e-06.

Runtime receipts attest unchanged pinned frozen P3 model revision, asset hashes, frozen source, chat template, prompt/readout, FP32 MPS, T=1, cap1024, batch1, threads4, SDPA, no cache/fallback, zero extra startup forwards. R6 executor hash matches across audit/predict; P3 config differs only by predeclared 300s process bound (P3 1200s). This analysis checks receipts, not assets/source files themselves. No referenced paths were followed.
Runtime completed 192/192 forwards; its prediction-process workflow took 12.643s including non-forward work; externally supervised audit+predict 13.868s, both exit0. Runtime validated execution/identity/finite normalization only, not scientific model-output quality. Research owns this arithmetic and limited interpretation.

## Natural-log contrasts/scales

x is condition-wise centered log p aligned by original semantic identity. alpha=((x00-x01)+(x11-x10))/2; beta=((x00-x11)+(x01-x10))/2; R=x00-x01+x10-x11. RMS is sqrt(weighted mean across cases of option-mean squares), not mean case RMS. Alpha is letter-assignment-associated, beta position/order-associated. R should be zero under additive invariant content. These are natural-log contrasts, not recovered complete biases.

Weights: sources equal, then domains (intent/sentiment) or mechanisms (rules), falling back to source_group, then rows equal; options 1/K. Each subset is rebalanced. Raw rows are separate estimands, not deployment prevalence.

| Subset | n | alpha RMS / MA | beta RMS / MA | R RMS / MA |
|---|---:|---:|---:|---:|
| global (raw_row) | 48 | 1.3569 / 1.0706 | 1.8094 / 1.3981 | 3.2012 / 2.2705 |
| global (source_balanced) | 48 | 1.3636 / 1.0732 | 1.7936 / 1.3866 | 3.3077 / 2.3240 |
| family:intent (source_balanced) | 16 | 1.4146 / 1.1074 | 2.1901 / 1.8258 | 4.9314 / 3.9397 |
| family:rule_application (source_balanced) | 16 | 0.9625 / 0.7363 | 1.0983 / 0.7838 | 1.6548 / 1.1578 |
| family:sentiment (source_balanced) | 16 | 1.6281 / 1.3759 | 1.9100 / 1.5502 | 2.4012 / 1.8744 |
| source:intent/inherited (source_balanced) | 4 | 1.8435 / 1.5537 | 2.1060 / 1.7957 | 6.2716 / 5.2288 |
| source:intent/new_a (source_balanced) | 6 | 1.4036 / 1.0980 | 2.2538 / 1.8885 | 3.6144 / 2.8355 |
| source:intent/new_b (source_balanced) | 6 | 0.7970 / 0.6704 | 2.2077 / 1.7931 | 4.5343 / 3.7548 |
| source:rule_application/inherited (source_balanced) | 4 | 0.8039 / 0.6319 | 0.7937 / 0.5560 | 1.3949 / 1.0127 |
| source:rule_application/new_a (source_balanced) | 6 | 0.9571 / 0.7881 | 1.3828 / 1.0895 | 2.1816 / 1.4403 |
| source:rule_application/new_b (source_balanced) | 6 | 1.1033 / 0.7888 | 1.0376 / 0.7059 | 1.2289 / 1.0203 |
| source:sentiment/inherited (source_balanced) | 4 | 1.4045 / 1.0953 | 1.7924 / 1.5312 | 2.8603 / 2.0136 |
| source:sentiment/new_a (source_balanced) | 6 | 1.9016 / 1.7256 | 2.1808 / 1.6588 | 2.2269 / 1.8154 |
| source:sentiment/new_b (source_balanced) | 6 | 1.5372 / 1.3066 | 1.7250 / 1.4607 | 2.0389 / 1.7944 |
| K:3 (source_balanced) | 11 | 0.6257 / 0.4740 | 1.6171 / 1.2643 | 3.8630 / 2.4350 |
| K:4 (source_balanced) | 34 | 1.4666 / 1.2151 | 1.8643 / 1.4266 | 3.3788 / 2.3742 |
| K:5 (source_balanced) | 2 | 1.8990 / 1.4747 | 2.1649 / 1.8768 | 4.2248 / 3.8564 |
| K:6 (source_balanced) | 1 | 2.0532 / 1.8945 | 1.6475 / 1.2496 | 2.3079 / 2.0355 |

## Mirror restrictions and across-case heterogeneity

Mirror violation is the RMS of the mirror-symmetric component (v[j]+v[K-1-j])/2; it must vanish for a fixed mirror-antisymmetric account. Odd-middle is the centered-log contrast at the unmoved middle semantic option. Raw middle probability need not stay constant.

| Global source-balanced contrast | mirror violation RMS | odd-middle n | odd-middle RMS / MA |
|---|---:|---:|---:|
| alpha | 0.3488 | 13 | 0.7225 / 0.4834 |
| beta | 0.6781 | 13 | 0.7223 / 0.5657 |
| R | 0.9844 | 13 | 1.9093 / 1.6224 |

Descriptive across-case heterogeneity: within each K and original semantic slot, source-balanced SD, then RMS over slots. Means and SD vectors remain in results.json for reproduction; no fitted predictor/correction is made.

| K | alpha SD RMS | beta SD RMS | R SD RMS |
|---|---:|---:|---:|
| 3 | 0.6109 | 1.0096 | 3.6271 |
| 4 | 1.1054 | 1.1478 | 3.2760 |
| 5 | 0.9808 | 0.5399 | 3.9664 |
| 6 | 0.0000 | 0.0000 | 0.0000 |

## Paired probability and choice retention

First two pairs change letters at fixed order; next two change order at fixed option letter; last two change both factors (standard and reversed-letter reversal). TV is aligned in each indicated coordinate system. Retention uses only strict unique argmax pairs; identity/letter/position events can overlap at odd middle. Full family/source/K breakdowns, both weighting schemes and eligibility counts are in results.json.

| Pair | weighting | TV identity / letter / position | retention identity / letter / position | unique n |
|---|---|---:|---:|---:|
| O0L0~O0L1 | raw_row | 0.4303 / 0.4834 / 0.4303 | 0.4167 / 0.4167 / 0.4167 | 48 |
| O1L1~O1L0 | raw_row | 0.4065 / 0.5514 / 0.4065 | 0.4583 / 0.2917 / 0.4583 | 48 |
| O0L0~O1L1 | raw_row | 0.4213 / 0.4213 / 0.5431 | 0.4583 / 0.4583 / 0.3542 | 48 |
| O0L1~O1L0 | raw_row | 0.4446 / 0.4446 / 0.4901 | 0.3958 / 0.3958 / 0.3750 | 48 |
| O0L0~O1L0 | raw_row | 0.2709 / 0.5891 / 0.5891 | 0.6250 / 0.2500 / 0.2500 | 48 |
| O0L1~O1L1 | raw_row | 0.6142 / 0.2087 / 0.2087 | 0.1875 / 0.7917 / 0.7917 | 48 |
| O0L0~O0L1 | source_balanced | 0.4232 / 0.4878 / 0.4232 | 0.4259 / 0.4074 / 0.4259 | 48 |
| O1L1~O1L0 | source_balanced | 0.4025 / 0.5575 / 0.4025 | 0.4537 / 0.2778 / 0.4537 | 48 |
| O0L0~O1L1 | source_balanced | 0.4112 / 0.4112 / 0.5513 | 0.4722 / 0.4722 / 0.3333 | 48 |
| O0L1~O1L0 | source_balanced | 0.4368 / 0.4368 / 0.4997 | 0.4074 / 0.4074 / 0.3519 | 48 |
| O0L0~O1L0 | source_balanced | 0.2632 / 0.6006 / 0.6006 | 0.6389 / 0.2315 / 0.2315 | 48 |
| O0L1~O1L1 | source_balanced | 0.5997 / 0.2175 / 0.2175 | 0.2037 / 0.7685 / 0.7685 | 48 |

## Measured allowed full-vocabulary mass

Unweighted distribution quantiles use linear interpolation. Mean is shown both raw and source-balanced. Low allowed mass alone does not invalidate conditional classification.

| Condition | min | p10 | median | p90 | max | raw mean | balanced mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| O0L0 | 0.958810 | 0.998933 | 0.999740 | 0.999959 | 1.000000 | 0.998586 | 0.998682 |
| O0L1 | 0.966665 | 0.999121 | 0.999805 | 0.999953 | 0.999996 | 0.998887 | 0.998927 |
| O1L0 | 0.982827 | 0.998715 | 0.999743 | 0.999957 | 0.999992 | 0.998984 | 0.999034 |
| O1L1 | 0.977271 | 0.999352 | 0.999784 | 0.999962 | 0.999989 | 0.999054 | 0.999052 |

## Interpretation and limits

Nonzero R, mirror violations, odd-middle contrasts and across-case heterogeneity describe departures from a shared static additive mirror account; none uniquely identifies a neural mechanism or reasoning failure. A zero R would not establish additivity either. Letter-assignment naturalness (ascending versus descending alphabet, binding and context) remains confounded with letter effects. Content-order interactions remain confounded with position effects. Only mirror pairings are observed; mirror-symmetric letter/position preferences are unidentified. TRAIN sample/source/template/teacher dependencies prevent generalization, causal exclusivity, calibration or accuracy claims. No M6/E6 outcomes, Evaluation/probe/D3/final inputs or references were opened.

## Actual commands

This output directory records one invocation of the final script and refuses any overwrite. The earlier artifact prototype stopped before derived metrics on a semantic-order versus display-order validation error; its first receipt was overwritten with an embedded previous-attempt summary, not preserved as a standalone immutable file. That provenance limitation remains disclosed in the owner diagnosis. The binding correction and later path/report/output-immutability changes did not alter the declared estimator or weights.

```sh
/Users/destiner/Code/jeff/.venv/bin/python -I -S /Users/destiner/Code/jeff/.worktrees/research/experiments/research/analyze_four_cell.py --task-root /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z --runtime-root /Users/destiner/Code/jeff/artifacts/release/r6-order-20261111-01 --output-dir /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/four-cell-reproduction
```

Python: 3.12.16 (main, Oct 26 2026, 13:59:40) [Clang 23.1.3 ]. Analysis workflow elapsed 0.007s. Standalone stdlib CPU run only; all commands/jobs completed; no tests/lint, ML imports/load/inference/training/dependencies, mailbox, commits or merges.
