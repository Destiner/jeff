# E4 Track B: D3 seen-mechanism / new-policy diagnostic

Independent CPU scoring is complete over 96 original cases, 48 two-case policy/source groups and eight intentionally seen mechanisms. Four published M4 prediction files were scored byte-for-byte unchanged, alongside existing uniform and lexical baselines. This is development evidence, separate from v2 unseen-mechanism validation and existing probes; it is neither final evaluation nor an iid sample.

This completes E4's separate diagnostic track; the [historical LR control](e4-m5-lr-control.md) remains a failed fixed conjunction. Neither track authorizes default promotion.

## Overall

Correct means agreement with the published `rule_verified` labels, not independently established semantic truth. Loss is natural-log cross-entropy, without clipping; Brier is summed over options.

| Predictor | Correct / 96 | Log loss | Brier |
|---|---:|---:|---:|
| MiniLM start | 27 | 1.316860 | 0.729717 |
| MiniLM trained | 31 | 1.342824 | 0.743115 |
| MS MARCO start | 30 | 1.347340 | 0.748730 |
| MS MARCO trained | 26 | 1.355202 | 0.752642 |
| Uniform | 27 | 1.317371 | 0.730035 |
| Lexical | 24 | 1.319115 | 0.730912 |

All six predictors cover 96/96. Missing, invalid and duplicate case counts are zero; no extra IDs, unidentifiable records or other record diagnostics occurred. Invalid/raw records were not filtered before the existing scorer. Uniform's deterministic top-choice count reflects first-option tie-breaking, not random draws.

MiniLM has 19 paired case wins and 15 regressions against its own start (12 both correct, 50 both wrong). Its complete-policy 2/2 outcomes move from 3/48 to 4/48: four gained, three lost, zero retained correct, 41 not fully correct on either side. MS MARCO has 15 wins and 19 regressions (11 both correct, 51 both wrong); complete policies move from 3/48 to 5/48: five gained, three lost, zero retained correct, 40 not fully correct on either side. All 96 cases are common-valid and all 48 policies are fully observed for each pair. Policy-level 2/2 gains do not erase case-level regressions.

## All eight mechanisms

Each row has 12 cases / six policies. Entries show own start → trained correct counts.

| Mechanism | MiniLM | MS MARCO |
|---|---:|---:|
| Packs | 3 → 6 | 5 → 4 |
| Rates | 3 → 3 | 6 → 3 |
| Coordinates | 3 → 3 | 2 → 3 |
| Cooldown | 3 → 1 | 2 → 1 |
| Lexicographic | 5 → 5 | 5 → 2 |
| FIFO | 4 → 6 | 2 → 7 |
| Discount | 3 → 5 | 6 → 5 |
| Rounding | 3 → 2 | 2 → 1 |

FIFO improves for both; MS MARCO gains five cases without a paired FIFO regression. Cooldown deteriorates for both: MiniLM loss 1.386081 → 1.597780 and MS MARCO 1.416606 → 1.608404. MS MARCO loses three net cases on both rates and lexicographic. MiniLM's packs gain is six wins versus three regressions, not uniformly improved policies. MS MARCO rounding loss improves (1.695480 → 1.503249) despite fewer correct choices.

## Provenance, controls and limits

- Published labels are programmatic/rule-verified. Author and reviewer used the same `openai/gpt-sol` alias; immutable teacher revision is unknown. Initial review agreed on 31/32; reviewed final-content material agreed on 64/64 across only 40 policies. That is not independent verification of all 96 cases or all 48 policies. “Final-content” here denotes repaired D3 authoring content, not the protected final-evaluation split.
- Frozen boundary completed at 14:22:08 UTC, before preflight at 14:30:27 and all four inference processes. Boundary reference/input/unit hashes, label-free projection, 96/48/8 mappings and published source pins were rechecked. Prior ID/group and exact/NFC+outerstrip content exclusions reported zero hits/errors; this is not semantic novelty clearance. The superseded sentiment training exclusion is separately pinned in the owner-binding supplement.
- Published residual hints remain: FIFO fewest-zero 6/12, rates slot-two 6/12, scheduling non-none 11/12 and easy boundary cases. Shared policy cases and common authoring algorithms are correlated; no statistical iid or significance claim is made.
- Actual receipts bind `input`, `output`, `checkpoint_inventory`, checkpoint directory and explicit `command`, plus fresh-process true, exit code zero, process wall time and unchanged-checkpoint declarations. These are published Model execution claims, not an independently observed runtime trace. Inference commands used MPS; this task only ran CPU metrics.
- Independently checked saved metadata `max_length=256`; identical before/after inventory record bytes covering 30 files; current file sizes; current non-tensor hashes including metadata/tokenizer assets. Published preflight audits each bind the exact tokenizer hash and 361 candidate pairs, maximum 129 tokens, zero overflow at 256. No model or tokenizer was loaded and token counts were not recomputed. Current giant tensor bytes were not rehashed; loaded tensors are **not independently attested**.
- MiniLM's starting scalar head is randomly initialized; MS MARCO's start retains pretrained cross-encoder scoring. They are different starting controls, not an architecture-isolated comparison. Probability reliability bins/ECE are descriptive, not a calibration claim.

**Conclusion:** MiniLM gains four correct cases but worsens both loss and Brier; MS MARCO loses four correct cases and also worsens both probability metrics. These results do not establish broad rule generalization or justify promotion. No new threshold, selection, training, reversal/order suite, final-data access or pooling was performed.

## Evidence

All paths below are relative to `/Users/destiner/Code/jeff/`:

- `artifacts/evaluation/e4-d3-scoring-v2/`: adapted exclusive recipe, actual receipt bindings and preparation pins. The unused v1 receipt-schema preparation remains preserved.
- `artifacts/evaluation/e4-d3-comparison-v1/report.json`: six predictors; all 48 policy and eight mechanism summaries/outcomes, strict equal-unit macros, reliability and paired regressions.
- `artifacts/evaluation/e4-d3-comparison-v1/report.md`: all eight mechanisms for all six predictors, macros and pairs.
- `artifacts/evaluation/e4-d3-comparison-v1/comparison.json` and `shared-report.md`: unchanged shared scorer/comparer/renderer outputs, raw diagnostics and case outcomes.
- `artifacts/evaluation/e4-d3-comparison-v1/execution-pins.json`, `source-recheck.json`, `receipt.json`: bindings recorded before comparison, source recheck after scoring, completion receipt written last.
- `artifacts/model/m4-d3-inference-20261111-01/`: original prediction files and Model receipts/inventories/preflight.

The initial artifact orchestration used the host Python rather than the project interpreter; the independent review records actual Python 3.12 comparison reproduction separately. No software tests/lint, framework/dependency changes or Evaluation-owned ML jobs. Additional and pending spend £0.

Tracked study definition: `configs/evaluation/e4-d3-v1.json`; hash index: `manifests/evaluation/e4-d3-report-v1.json`. Immutable outputs are exclusive-create: reruns must use a new namespace rather than overwrite this delivery.
