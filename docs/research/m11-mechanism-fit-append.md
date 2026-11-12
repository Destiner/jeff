# R14: M11 fully fits three mapped TRAIN sets, not all eight

**FIFO, discount composition and coordinates now reach20/20 unique-top TRAIN agreement and10/10complete policies each.** M9 had no20/20group in the same view. This changes the fitting premise for these particular examples; it does not demonstrate algorithm mastery, complete branch coverage or new-policy transfer.

This is the actual fixed thirty-epoch endpoint appended to [R11's exact mechanism view](train-d3-mechanism-alignment.md), not a new duration arm or retrospective success threshold. The same160TRAIN rows/80policies are used; no mapping or example was selected after M11 results.

## Same explicit populations and saved endpoint

Reuse the eight declared `configs/data/d3-seen-rules-v1.json` mechanism→TRAIN-group mappings and R11's observed `provenance.scenario_id` memberships. Every mechanism still has **20rows /10two-case policies /one declared group**. Four share rule-a's source and four rule-b's. This is160/500rule rows, not the full500 or1500TRAIN, and there is still no one-to-one TRAIN↔D3 policy mapping.

Only new predictions are `artifacts/model/m11-msmarco-duration30-20261112-01/fit-final.jsonl`, SHA256 **`aa464684c02289fd95fce747605f304d2414690038c16d0f8607d99fbf31580a`**, matching the delivered fixed endpoint. Invocation/inventory metadata binds the same existing TRAIN inputs and final checkpoint. No weights or optimizer history were decoded/replayed. Old M4/M9 arithmetic is reused from canonical R11 rather than rescored.

## Per-mechanism agreement and proper scores

Cells are **correct /20 · NLL / summed Brier**. M4 endpoints have three epochs; M9 and M11 are fresh original-MS-MARCO runs at twelve and thirty epochs, not resumed extensions. MiniLM is architectural/pretraining context, not a duration-only comparison.

| Mechanism | M4 MiniLM | M4 MS MARCO | M9 | M11 |
| --- | ---: | ---: | ---: | ---: |
| lexicographic |13 ·1.059227/.640229|9 ·1.072016/.649122|17 ·.608613/.339974|19 ·.134235/.088967|
| fifo |14 ·1.085641/.584472|3 ·1.417815/.765815|13 ·.683296/.368820|20 ·.062189/.019604|
| discount |7 ·1.303584/.712365|6 ·1.369229/.740772|16 ·.950894/.505370|20 ·.077833/.024366|
| rounding |9 ·1.264651/.690831|4 ·1.416379/.766267|10 ·1.089970/.615694|14 ·.626407/.378812|
| packs |11 ·.962708/.557906|7 ·1.234960/.703941|11 ·.897883/.529510|15 ·.445444/.285590|
| rates |10 ·1.014193/.613793|10 ·.957317/.592234|10 ·.884267/.573151|10 ·.843879/.549268|
| coordinates |1 ·1.266280/.726703|1 ·1.260696/.719732|7 ·1.146740/.658494|20 ·.154650/.062759|
| cooldown |9 ·1.271766/.690665|9 ·1.309731/.707108|13 ·1.044376/.568258|18 ·.396658/.178289|

Both proper scores improve versus M9 in all eight groups, but the accuracy/complete-policy picture remains heterogeneous. Lexicographic19/20 and cooldown18/20 retain errors; rounding14/20, packs15/20 and rates10/20 remain materially incomplete. No new “strong fit” cutoff is imposed.

| Mechanism | Complete policies /10: M4 Mini /M4 MS /M9 /M11 | M9→M11 row gains /losses |
| --- | ---: | ---: |
| lexicographic |5 /3 /7 /9|2 /0|
| fifo |5 /0 /6 /10|7 /0|
| discount |1 /1 /6 /10|4 /0|
| rounding |0 /0 /1 /4|5 /1|
| packs |3 /1 /3 /5|7 /3|
| rates |0 /1 /0 /0|1 /1|
| coordinates |0 /0 /1 /10|13 /0|
| cooldown |0 /0 /4 /8|6 /1|

A complete policy requires **both distinct cases** to have the target as unique maximum. Across80policies, M9→M11 moves28→56complete:27retained,29gained,1lost,23incomplete on both. Rates'10/20with0/10complete mathematically means exactly one correct case per two-case policy, not ten demonstrated successful policies; one gain/one loss replaces which rows succeed. That observation does not identify a shortcut or label error.

## Totals without hiding regressions

| TRAIN population | M9→M11 agreement | NLL | Brier | Same-ID gains /losses |
| --- | ---: | ---: | ---: | ---: |
| Mapped160 |97→136|.913255→.342662|.519909→.198457|45 /6|
| All500rules |314→414|.860594→.369835|.490438→.217106|130 /30|
| All1500 |1314→1414|.289057→.123309|.164171→.072369|130 /30|

All30full-TRAIN losses remain rules; the net100gain does not erase them or the86remaining rule disagreements. Intent/sentiment remain500/500 each. Uniform references and all80policy-level summaries are retained in the artifact, with no tie-break accuracy conflated with random uniform accuracy.

## D3 status and interpretation boundary

The E12 safe mechanism/policy projection was requested without blocking Evaluation or Runtime. **No M11 D3 aggregate has been received in this analysis yet.** Do not substitute the prior M9 D3 outcomes, infer a transfer gap from TRAIN alone, or inspect raw D3 labels/cases to fill the gap. If the safe packet is not available within R14's15-minute bound, this is a TRAIN-only delivery; no automatic extra window follows.

Once separately reported, new-policy outcomes must retain the six-new-policy/twelve-case D3 denominator per mechanism, distinct from these ten TRAIN policies/twenty rows. Even a poor D3 result after20/20TRAIN would not isolate architecture: prose, policy parameters, offered choices/arity, source style and branch coverage differ. Fitting two related cases per TRAIN policy is not exhaustive behavior or coverage of a mechanism's possible branches. `rule_verified` is the existing teacher/programmatic reference basis, not new independent human verification. One fixed seed/recipe and dependent sources do not establish causal capacity limits, calibration or a particular data remedy.

## Reproducibility and scope

Evidence root: `artifacts/research/r14-20261112T035750Z/`. Runnable stdlib arithmetic: `analysis/analyze.py`; actual output `analysis/actual-01/{actualresults.json,report.md,train-policy-summary.jsonl}`; byte-identical reproduction under `analysis/reproduction-01/`. Use project Python `-I -S`, `--output-dir` and a **new, nonexistent child directory**. Independent arithmetic is in `independent/{independent.py,results.json,findings.md}`. The owner compared123actual population/mechanism/policy-count/mapping quantities: zero discrepancies and maximum compared numeric difference0; `independent-comparison-receipt.json` records the scope. Fresh source/findings review is ready for TRAIN-only delivery. Original R11 and current E11/E16 results remain unchanged.

All1500M11IDs/options match; every probability is positive and finite, sum deviation≤1.525e−7, no exact top ties or zero targets. TRAIN NLL uses raw saved probabilities without clipping/renormalization; Brier sums across options. Metadata and a new consumed-prediction hash bind the actual endpoint; this was not another source/schedule audit or model invocation.

Started03:57:50UTC, hard cap04:12:50. No new ML, model/tokenizer/weight load, extra forward, corpus/mapping/survey, D7 release, NLI adaptation, dependencies, tests/lint, spend/upload or final payload access. Actual-data arithmetic/reproduction is scientific validation, not a software test suite. Research remains available for the fixed night after delivery; this report is no execution or promotion gate.
