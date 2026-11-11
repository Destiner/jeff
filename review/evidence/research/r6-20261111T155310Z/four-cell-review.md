# Independent final R6 four-cell scientific review

## Verdict

**Scientific arithmetic validated on actual Runtime outputs; provenance/output-hardening fixes remain required.** No estimator change or new experiment is indicated. This is independent recomputation, not software tests or synthetic fixtures. The existing analyzer was read but neither imported nor executed. Only the project Python `/Users/destiner/Code/jeff/.venv/bin/python -I -S` and standard-library code supplied on stdin were executed.

Read boundaries: root AGENTS.md and docs/coordination.md, the explicitly permitted research artifacts, Runtime predictions, receipt and completion metadata. No receipt upstream path was followed; no original TRAIN text, Evaluation/probe/D3/final/reference input, ML/tokenizer/dependency load, inference, tests/lint, mailbox, tracked edit or commit. This review writes only this new file, exclusively.

## Actual coverage and mapping

48 preselected TRAIN cases, 16 per family, 192 unique case-condition records, 740 probability entries. K distribution is 3:11, 4:34, 5:2, 6:1. All four cells and identical semantic option-ID sets verified per case. Zero probabilities: 0; exact ones: 0; tied presentations: 0. Every pair has 48 strictly unique argmax comparisons. No flooring or renormalization.

Score arrays must not be treated as display order: original_position is semantic index j. The four (slot, letter-index) mappings are 00=(j,j), 01=(j,K−1−j), 10=(K−1−j,K−1−j), 11=(K−1−j,j). Actual letters, chosen IDs and display-sorted tie lists match these mappings independently. Option IDs, not letters or score-array positions alone, bind probabilities across conditions.

Source means use exactly nine (family,producer) units: each family × inherited/new_a/new_b. Each has 4/6/6 rows respectively; groups are domain for intent/sentiment, mechanism for rules, falling back to source_group. All 48 selected within-source groups contain one case. Each source contributes 1/9; inherited rows receive 1/36, new-producer rows 1/54. Options contribute 1/K. These are weighting units, not nine demonstrated independent teachers. Source and group balancing was recomputed by nested source/group/case averages.

## Independently recomputed contrasts

Centered natural-log probabilities are combined using the predeclared alpha, beta and R signs; RMS is square root of weighted mean option energies, not mean case RMS.

| Population | alpha / beta / R source-balanced RMS |
|---|---|
| All 48 | 1.363606517 / 1.793570165 / 3.307742309 |
| intent | 1.414639 / 2.190051 / 4.931440 |
| sentiment | 1.628056 / 1.910011 / 2.401221 |
| rule_application | 0.962547 / 1.098278 / 1.654847 |

## Independently recomputed pairs

TV and retention columns are semantic identity / actual letter / displayed position. Counts are raw integers, distinct from source-balanced retention; events may overlap at an odd middle.

| Pair | Source-balanced TV | Raw retained choice counts | Source-balanced retention |
|---|---|---|---|
| O0L0~O0L1 | 0.423244 / 0.487766 / 0.423244 | 20/48 / 20/48 / 20/48 | 0.425926 / 0.407407 / 0.425926 |
| O1L1~O1L0 | 0.402534 / 0.557488 / 0.402534 | 22/48 / 14/48 / 22/48 | 0.453704 / 0.277778 / 0.453704 |
| O0L0~O1L1 | 0.411236 / 0.411236 / 0.551319 | 22/48 / 22/48 / 17/48 | 0.472222 / 0.472222 / 0.333333 |
| O0L1~O1L0 | 0.436849 / 0.436849 / 0.499745 | 19/48 / 19/48 / 18/48 | 0.407407 / 0.407407 / 0.351852 |
| O0L0~O1L0 | 0.263245 / 0.600617 / 0.600617 | 30/48 / 12/48 / 12/48 | 0.638889 / 0.231481 / 0.231481 |
| O0L1~O1L1 | 0.599693 / 0.217547 / 0.217547 | 9/48 / 38/48 / 38/48 | 0.203704 / 0.768519 / 0.768519 |

All recomputed global contrasts, family contrasts, six-pair TVs/retentions and balanced mass means agree with results.json to maximum absolute error 4.44e-16.

Balanced allowed full-vocabulary mass means: O0L0=0.998682153, O0L1=0.998926949, O1L0=0.999034473, O1L1=0.999052495. High mass is compatible with instability: nearly all vocabulary probability can remain among valid answer letters while its division among semantic choices changes sharply. It establishes neither correctness nor calibration, nor free-generation formatting behavior.

## Interpretation

The standard-letter reversal retains semantic choice in 30/48 cases (balanced 0.638889), versus 9/48 (balanced 0.203704) under reversed-letter reversal. Conversely letter/position retention is 12/48 versus 38/48 (balanced 0.231481 versus 0.768519). Balanced semantic TV is 0.263245 versus 0.599693 (see exact recomputation table above). These are contrasting condition-dependent responses, not a universal fixed-letter explanation.

Nonzero alpha and beta are letter-assignment-associated and position/order-associated changes. Nonzero R rejects the exact additive invariant-content restriction on these observations; R is a differently scaled four-term contrast, not a fitted residual RMSE, explained variance or exclusive causal mechanism. Letter sequence familiarity/binding/context and content-order interactions remain confounded. Mirror-symmetric letter/position preferences are unidentified; zero R would not establish additivity. No task accuracy, held-out generalization, calibration, independence or reasoning-failure conclusion follows. K=5 has two cases; K=6 has one, so its zero across-case SD is mechanical, not homogeneity evidence. The current report states these limits appropriately.

## Must fix before final handoff

1. **First-attempt provenance disclosure:** the embedded previous receipt documents a schema-validation failure before metrics, with previous script hash a9601124b2554edee8e3c4947b27fe78aeb5994a4516864342a100987f6be24a. The original standalone input-receipt.json was overwritten. This is NOT a fully immutable first attempt; a surviving nested receipt/hash is not preservation of the original standalone file or original script bytes. State the overwrite and limited surviving provenance explicitly. The before-metrics failure is documented by the embedded account/control flow, not independently reconstructable from a retained failed-script artifact. No numeric evidence here requires an estimator change.
2. **Immutable final output behavior:** existing code checks only results.json/report.md then explicitly rewrites an existing input-receipt.json. Final copied script must refuse any existing receipt/results/report and use exclusive creation for outputs (prefer a unique fresh output directory). Preserve current artifacts; do not rewrite history. Partial failed attempts should remain separate.
3. **Script/report identity:** final metadata/report-only and no-overwrite changes require a new script hash and truthful distinction between the script that produced existing metrics and the final hardened copy. Do not imply the changed script produced the original run. Preserve estimator/mapping/weights unchanged and label copied results as such. Final fixes are parent-owned and are not verified by this review.

These are provenance/handoff fixes, not grounds for rerunning model inference or changing the frozen analysis. Runtime receipt/completion hashes match actual prediction bytes; receipt source/assets claims remain attestations, not independent asset/source inspection. Completion records show 192/192 forwards, exit 0, 12.642686s process runtime and 13.867752s externally supervised audit+predict, below the 300s bound.

## Optional only

Keep integer retained-choice counts alongside weighted percentages for easy review (provided above). A self-contained final receipt may record this review and unchanged-estimator copy provenance. No new fit, sensitivity search, significance calculation, causal claim or additional inference is needed.

## Reproducibility and completion

Independent arithmetic used sorted original_position plus strict option-ID dictionaries, nested source/group/case weights, condition-centered log p and dictionary-aligned TV. Comparison tolerance was 1e-12. Input hashes were checked directly against packet/receipt/completion bindings without following referenced paths.

Actual predictions SHA256: `c9068e41915629f9419066941124c74fd7f181e93c840ca05e807d9e0056494d`.
Current inspected analyzer SHA256: `8d4df354ad79a23b1eba0673e64415227010f2ffc2706661db97004bbcdcfc8f`; producing receipt script SHA256: `8d4df354ad79a23b1eba0673e64415227010f2ffc2706661db97004bbcdcfc8f`.
Probability sum maximum error: 1.37020834e-07; independent T=1 softmax reconstruction maximum error: 1.30956246e-07.

Review completed 2026-11-11T16:34:06.063944+00:00. All review commands/jobs finished; no background jobs, new compute or paid spend. Only this new review artifact was written.
