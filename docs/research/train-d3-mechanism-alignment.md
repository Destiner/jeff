# R11: D3's eight mechanisms remain incompletely fitted on TRAIN

**M9 fits these exact mapped TRAIN groups better, but none is fully fitted: 97/160 rows and 28/80 complete two-case policies.** This is not a clean “all eight mechanisms learned, only new-policy transfer failed” result. Nor does residual TRAIN error explain every D3 change: substantial fitting gains coexist with weak or regressing new-policy outcomes. The evidence supports **mixed incomplete fitting and limited transfer**, not an identified neural cause or a prescribed data remedy.

## Explicit mapping and actual denominators

The crosswalk comes from `configs/data/d3-seen-rules-v1.json` (`mechanisms[].id`, `training_group_id`, `training_shard`), confirmed by Data message `2b154635-ee55-4ac5-9608-8417b6b83aaa`. No mechanism was inferred from an opaque ID substring.

| D3 mechanism | Exact released TRAIN group |
| --- | --- |
| lexicographic | `data:pilot-v2:rule-a:g002` |
| fifo | `data:pilot-v2:rule-a:g003` |
| discount | `data:pilot-v2:rule-a:g005` |
| rounding | `data:pilot-v2:rule-a:g007` |
| packs | `data:pilot-v2:rule-b:g002` |
| rates | `data:pilot-v2:rule-b:g005` |
| coordinates | `data:pilot-v2:rule-b:g006` |
| cooldown | `data:pilot-v2:rule-b:g008` |

Every mapped group actually has **20 TRAIN rows**, one declared mechanism `group_id`, and **10 observed `provenance.scenario_id` policies with two cases each**. Thus this is160/500rule rows, not all500 or all1500TRAIN. Four mechanisms share the rule-a source; four share rule-b. Ten policies are not ten independent producers/algorithms.

D3 has **12 original cases / six new policies per mechanism**, 96/48 overall. Its policy IDs are joined through the explicitly documented namespace/mechanism/p01–p06 construction and checked against the full aggregate key set—not guessed from substrings. **No one-to-one TRAIN-policy↔D3-policy mapping exists.** Mechanism identity does not assert identical policy parameters, wording, answer arity or difficulty.

## TRAIN: all three saved endpoints, same references

Cells are **agreement /20 · mean natural-log NLL**. MiniLM and M4 MS MARCO are three-epoch endpoints; M9 is the fresh original-MS-MARCO twelve-epoch endpoint, not nine resumed epochs. MiniLM→M9 is not a duration-only comparison.

| Mechanism | M4 MiniLM | M4 MS MARCO | M9 | Uniform NLL |
| --- | ---: | ---: | ---: | ---: |
| lexicographic |13 ·1.059227|9 ·1.072016|17 ·0.608613|1.098612|
| fifo |14 ·1.085641|3 ·1.417815|13 ·0.683296|1.386294|
| discount |7 ·1.303584|6 ·1.369229|16 ·0.950894|1.386294|
| rounding |9 ·1.264651|4 ·1.416379|10 ·1.089970|1.386294|
| packs |11 ·0.962708|7 ·1.234960|11 ·0.897883|1.242453|
| rates |10 ·1.014193|10 ·0.957317|10 ·0.884267|1.098612|
| coordinates |1 ·1.266280|1 ·1.260696|7 ·1.146740|1.242453|
| cooldown |9 ·1.271766|9 ·1.309731|13 ·1.044376|1.386294|
| **All160** |**74 ·1.153506**|**49 ·1.254768**|**97 ·0.913255**|**1.278414**|

M9 lowers TRAIN NLL versus M4 MS MARCO **in all eight groups**, and beats each group's uniform NLL. Top-choice counts range7–17/20, however; no group reaches20/20. Complete two-case policy counts rise **6→28/80** (MiniLM14/80). M4 MS MARCO→M9 gains60same-ID agreements and loses12, not48unqualified improvements. The all-rule238/185/314of500 and full-TRAIN1083/985/1314of1500 anchors reproduce exactly but do not replace this alignment.

## D3: actual E10 outcomes, not a future inference request

Only Evaluation's approved `artifacts/evaluation/e10-r11-aggregate-v1/aggregates.json` was consumed. E10's actual P8 outputs were already scored; its publication is main `630aab0dfe22f107b147dee80db98e45a549ceb3`. No raw D3 cases, targets, prediction rows or embedded provenance paths were opened by this analysis.

Cells are **agreement /12 · NLL**. Uniform contributes only its probability-loss reference here, not a first-tie accuracy claim.

| Mechanism | M4 MiniLM | M4 MS MARCO | M9 | Uniform NLL |
| --- | ---: | ---: | ---: | ---: |
| lexicographic |5 ·1.397716|2 ·1.378059|4 ·1.416331|1.386294|
| fifo |6 ·1.003416|7 ·1.092312|6 ·0.975910|1.098612|
| discount |5 ·1.369773|5 ·1.381418|2 ·1.372716|1.386294|
| rounding |2 ·1.508566|1 ·1.503249|1 ·2.283350|1.386294|
| packs |6 ·1.261849|4 ·1.291678|6 ·1.241300|1.314374|
| rates |3 ·1.230830|3 ·1.202002|1 ·1.237173|1.194506|
| coordinates |3 ·1.372659|3 ·1.384492|3 ·1.419737|1.386294|
| cooldown |1 ·1.597780|1 ·1.608404|3 ·1.406540|1.386294|
| **All96** |**31 ·1.342824**|**26 ·1.355202**|**26 ·1.419132**|**1.317371**|

M9 ties M4 MS MARCO's26/96 agreements but worsens NLL1.355202→1.419132 and summed Brier0.752642→0.775609; fully correct D3 policies fall5→2/48. The two populations' arities differ—e.g. lexicographic uniform NLL ln3→ln4 and FIFO ln4→ln3—so the TRAIN-to-D3 loss difference is not a matched causal transfer effect.

### Complete policies and same-TRAIN-ID changes

A policy is complete only when **both distinct cases** agree with their references; these are not reversal pairs. TRAIN maxima are all unique. E10 separately reports neural D3 maxima unique; uniform's exported complete-policy counts use first-tie selection and are not unique-top successes.

| Mechanism | TRAIN M4 MS→M9 complete /10 | TRAIN gains / losses | D3 M4 MS→M9 complete /6 |
| --- | ---: | ---: | ---: |
| lexicographic |3→7|9 /1|0→0|
| fifo |0→6|10 /0|2→1|
| discount |1→6|10 /0|2→0|
| rounding |0→1|6 /0|0→0|
| packs |1→3|8 /4|0→1|
| rates |1→0|6 /6|1→0|
| coordinates |0→1|7 /1|0→0|
| cooldown |0→4|4 /0|0→0|

All80TRAIN policy summaries and48D3 policy outcomes remain in the evidence, including NLL/Brier; no selective subset of policies was dropped. E10's M9-vs-M4 D3 policy transitions retain `fifo:p02`, gain `packs:p06`, and lose `discount:p02`, `discount:p03`, `fifo:p01`, `rates:p03` (all under the documented D3 namespace). This is a within-D3 comparison, not a TRAIN-policy pairing.

## What changes the diagnosis

- **Not a fully fitted mechanism-transfer test:** even the strongest mapped TRAIN group, lexicographic, is17/20 and7/10complete policies; coordinates remain7/20 and1/10. Zero groups supply evidence of perfect observed TRAIN fit, let alone algorithm mastery. No new fitted/unfitted threshold was chosen after results.
- **More fitting is not uniform transfer:** discount TRAIN6→16/20 and1→6complete policies accompanies D3agreement5→2/12 and2→0complete policies, despite a small D3NLL improvement. Rounding TRAIN4→10/20 accompanies D3NLL1.503249→2.283350. These do not isolate whether prose, policy details, arity, shortcuts or optimization are responsible.
- **Keep counterexamples:** packs improves D3agreement4→6/12 and proper scores, but TRAIN remains11/20; cooldown improves D3agreement1→3 while staying below uniform NLL. FIFO loses one D3agreement and one complete policy while its NLL improves. Lexicographic gains two agreements while NLL worsens. “All metrics worsened” would be false.
- **Rates hide churn:** unchanged10/20TRAIN agreement consists of six gains and six losses; complete TRAIN policies fall1→0/10 despite lower NLL. D3falls3→1/12. This is not evidence of a stable mastered subskill or proof of a particular shortcut.

The practical conclusion is to retain **mechanism-specific incomplete fit plus heterogeneous transfer** in the evidence, rather than cite314/500 as proof the eight D3 mechanisms were learned. This does not authorize an LR rescue, more epochs, D7 release, new cases or a change to the night queue.

## Arithmetic, reference basis and reproducibility

Stable row/option IDs join the three existing full-TRAIN files in `artifacts/model/m9-msmarco-duration-20261111-01/`: `fit-minilm.jsonl`, `fit-msmarco.jsonl`, `fit-final.jsonl`, against `train-reference.jsonl`. Selected references match released TRAIN on IDs, state/question, ordered options, targets, groups, provenance and split. All4500vectors have exact coverage, finite valid probabilities, no duplicate IDs/options, no zero targets and no exact top ties; maximum sum error≤1.69e−7. No clipping or renormalization is used for TRAIN. E10's retained scorer divides by the observed sum within its1e−6tolerance; these roundoff conventions are disclosed rather than silently pooled.

Uniform NLL is mean lnK for the actual rows; Brier sums over options. Equal20TRAIN rows and12D3 rows per mechanism make each respective case mean an equal-mechanism mean, but do not make cases independent or permit pooling populations. Reference `rule_verified` is existing teacher/programmatic provenance under the same exposed teacher alias, **not new human verification**. Ten TRAIN policies and six D3 policies share authoring sources/styles; unknown correspondence stays unknown. One historical seed/recipe does not establish causal architecture limits, calibration or an effective data remedy.

Evidence root: `artifacts/research/r11-20261112T014014Z/`. Canonical full output: `analysis/reproduction-01/{actualresults.json,report.md}`. Runnable stdlib arithmetic: `analysis/analyze.py`; independent arithmetic: `independent/{independent.py,results.json,findings.md}`. Run the former with project Python `-I -S` and `--output-dir` pointing to a **new, nonexistent child of `analysis/`**. Existing outputs are never overwritten. No model/tokenizer/weights, forwards, final payloads, new dataset, dependency, tests/lint or spend were involved.

The initial script/output remain preserved. Before delivery, the owner replaced misleading D3 `strict_fully_correct_policies` naming with the exported choice-convention wording, explicitly enforced unique maxima for TRAIN policy completeness, and extended the released-reference comparison to state/question. Actual scientific metrics did not change. Independent agreement/NLL/tie/policy-count comparisons match: 1,670 binding/comparison checks, no discrepancies, maximum compared numeric difference0 (`arithmetic-comparison-receipt-v2.json`). The first owner comparison incorrectly compared D3's structured NLL object with a scalar; its failed receipt and script remain preserved. Selecting the existing `mean` field corrected that comparison without changing either analysis. Final source review and build receipts accompany the delivery; actual-data reproduction is not a software test suite.
