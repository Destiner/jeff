# E4 Track A — historical-only criterion receipt

**Frozen without reading any M5 outcome. Owner scores subsequently.** New exclusive directory: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-preregister-v1/`. CPU standard-library processing only; no model loads, tests, lint, paid calls, final-data access, tracked edits or merges.

## Fixed conjunction

All four conditions, plus full coverage and control comparability, are required:

1. Recover **at least one** of `eval.validation.sentiment.03`, `eval.validation.sentiment.04`, `eval.validation.rule_application.02`. A strict recovered group must choose the target in **both** original and reversal.
2. **Zero newly wrong probe groups:** no presentation correct under historical trained M3 becomes wrong in either order. Assess all 12 groups, not just the recovery candidates.
3. All-12-group macro probe loss **strictly below 1.360701041245408**. First average original/reversal log losses within each group, then average the 12 group means. Do not compute loss from an averaged probability vector or drop the clarification/conjunction outliers.
4. Pilot60 original-row mean loss **≤ 0.7937008119799213 + 0.05 = 0.8437008119799213**. This is Evaluation's exact normalized saved-prediction loss, not rounded `0.793701` and not the run's in-process `0.7937007967576695`.

Coverage is a precondition, not an additional conditional-quality denominator: exact frozen pilot60 and probe24 IDs/options; 12 probe groups and 12 complete exact reversal pairs; no missing, invalid, duplicate, extra or unidentifiable predictions. Explicit coverage/control failure means **no success**, even if a partial subset looks favorable. Zero target mass is infinite loss, not clipped. All outcomes remain reportable even if the conjunction fails. No future-outcome-based threshold or group changes.

Original-only ranks/probabilities/margins below describe one decision per source group; they are not averaged ranks. Pair means are for loss; the second order is a consistency/coverage safeguard, not another independent example. Original ties use original reference option order; reversed ties use the reversed reference order exactly as the existing scorer specifies. Averaging probabilities could hide a failure or change a tied decision, so it cannot establish recovery. Historical M3 has no choice disagreements across its 12 probe pairs in either snapshot; the stricter both-order safeguard changes no historical group classification.

## Historical probe outcomes — all 12 unique groups

Start → trained; natural-log loss. Margin is `p(target) − max p(rival)`, not a raw logit or top-two confidence. Full precision, IDs, original order, both presentations, and pair losses are in `historical-bindings.json`.

| Group | Target rank | p(target) | Signed margin | Original loss |
|---|---:|---:|---:|---:|
| intent.01 | 1→1 | 0.776807→0.682845 | +0.559397→+0.366630 | 0.252564→0.381488 |
| intent.02 | 2→2 | 0.161147→0.121467 | -0.665231→-0.727541 | 1.825438→2.108112 |
| intent.03 | 3→3 | 0.000810→0.314050 | -0.524092→-0.056834 | 7.118072→1.158204 |
| intent.04 | 1→1 | 0.998481→0.969682 | +0.997386→+0.948169 | 0.001520→0.030788 |
| sentiment.01 | 2→2 | 0.204708→0.438294 | -0.549362→-0.018742 | 1.586171→0.824866 |
| sentiment.02 | 4→3 | 0.232945→0.130976 | -0.057285→-0.354876 | 1.456954→2.032744 |
| sentiment.03 | 1→2 | 0.487243→0.491150 | +0.004744→-0.012360 | 0.718991→0.711005 |
| sentiment.04 | 1→2 | 0.824606→0.475148 | +0.669155→-0.024632 | 0.192850→0.744129 |
| rule_application.01 | 2→2 | 0.032766→0.000790 | -0.934469→-0.998419 | 3.418378→7.142956 |
| rule_application.02 | 1→2 | 0.778038→0.486317 | +0.572936→-0.010917 | 0.250980→0.720894 |
| rule_application.03 | 1→1 | 0.888894→0.990366 | +0.802110→+0.984762 | 0.117777→0.009680 |
| rule_application.04 | 1→1 | 0.603081→0.629049 | +0.206162→+0.258098 | 0.505704→0.463546 |

M3 loses exactly the three preregistered groups, recovering none: 7→4 correct unique groups. Its macro pair loss nevertheless improves 1.4537831337093712→1.360701041245408. Attribution sentiment improves target mass but loses rank because the rival improves more. The still-wrong clarification group dominates the apparent loss improvement. These observations explain why rank recovery and all-group loss are separate required conditions.

## Bindings and controls

`historical-bindings.json` verifies every reference, prediction, comparison, pair-map and order-report entry from existing `evaluation/e2-m3-v2/recipe.json`, including the exact M3-start/trained pilot60 and probe24 prediction paths/hashes. It verifies the two historical label-free input receipts and exact exported reference projections. It independently reruns only the existing CPU scorer for the four historical M3 prediction files and requires exact outcome equality with the saved E2 reports. No replacement scorer was introduced. Pair identities partition all 24 references exactly and preserve state, question, target, provenance and source group with exact reversed option objects.

It records the historical run/hash, source hashes/revision, dataset manifest/shard hashes, configs, optimizer, environment, initial recorded tensor hashes and budget. Fixed source `e37b0f3e7f2e3162abca87a76883eb81300603e0`; retained-head `cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`; pilot-v1 manifest `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`. Change only scalar-head LR 5e-4→2e-5, keeping encoder/native-pooler LR2e-5, seed42/order, pair formatting, cap256, batch4, three epochs/225 updates/900 presentations, full tuning, MPS/four threads, Torch2.15.0/Transformers4.57.6, AdamW decay.01/betas(.9,.999)/eps1e-8, native dropout and temperature1. No schedule/warmup/clipping changes. Starting-state comparability must be checked by the owner against these historical records before interpreting M5; **this receipt does not claim M5 comparability has been established**.

## Reuse R4's rule-category diagnostic, not a new analysis

Existing source: `experiments/research/diagnose_m3_regression.py`, key `datasets.pilot.rule_choice_text_counts` in `/Users/destiner/Code/jeff/artifacts/research/r4-20261111T1145/reproduction-final/diagnosis.json`. Both are hash-bound here. Reuse the existing “Water reaches no other junctions.” and “Elect nobody under this rule.” categories. The bindings map all 20 historical rule IDs to their existing no-result option IDs and target category for later reuse; no new labels/categories/mechanisms or selection threshold.

| Pilot rule group | No-result targets | Start→trained no-result choices | Start→trained agreement |
|---|---:|---:|---:|
| g11 reachability (10 rows) | 2 | 10→9 | 2→2 |
| g12 election (10 rows) | 5 | 8→10 | 3→5 |

Trained M3 chooses no-result in 19/20 and its seven correct rule choices are all no-result targets (0/13 winner/nonempty cases correct). These counts qualify what pilot performance means; they are descriptive, not another gate.

## Qualification and handoff

All probe labels are teacher labels with unknown teacher identity, including rule probes: results are teacher agreement, not independently verified correctness. Pilot labels comprise 40 teacher and 20 programmatic rule-verified examples. Reused development evidence, few correlated groups, a single seed and MPS/stochastic variation prevent causal proof or significance claims. M2's differing pretrained source/head/representation makes it context only, not this intervention's causal comparator. No calibration or final-performance claim.

Deliverables: `criterion.json` (fixed machine-readable decision policy), `historical-bindings.json` (exact hashes/controls/pair identities/full historical tables/category mapping), `findings.md` (this summary), `freeze.py` (historical receipt-generation code, exclusive output writes). No subsequent-outcome consumer was added; the owner should reuse existing compare/order tooling and apply the bound criterion. This task stops before any M5 scoring.

Execution note: the initial historical-only extraction stopped before writing receipts because the existing election option text includes “under this rule.”; corrected to that exact historical wording, then extraction completed. No historical input or tracked source was altered.
