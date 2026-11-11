# Measured orientation at the cutoff

This is a navigation aid, not an endorsed root-cause story. Consult exact reports and raw artifacts. No final evaluation was opened; these are development evidence. “Agreement” is against supplied labels, some teacher-authored and some rule-verified.

## What exists
Real local training, saved checkpoints, fresh-process reloads and independent scoring have been completed. No newer candidate is an unqualified promoted default. The initial pipeline milestone is met; broad reliable decision capability is not established.

## Populations
- v2 TRAIN:1500rows/880declared source groups,500rows per family (intent/sentiment/rules).
- Development:60inherited v1 rows and240new v2 rows; report these separately.
- Probes:24presentations of12groups, not24independent cases.
- D3:96decisions from48new policies using8deliberately seen mechanisms. Not IID or mechanism-disjoint evidence; permanently excluded from training.
- R6four-cell diagnostic:48existing TRAIN cases×4conditions. Its conclusions are not held-out accuracy.

## Key completed contrasts

| Experiment | Main observation | Important qualification |
|---|---|---|
| M4 encoders on new240 | MiniLM132/240(55%); MS MARCO141/240(58.75%); lexical99/240(41.25%) | Both candidates failed historical/probe robustness criteria. Arbitrary choice text support is not general reasoning evidence. |
| M5 reduced scalar-head LR control | Pilot40/60 unchanged; probes8→10/24 | Probe group-macro loss1.360701→1.384773 worsened; predeclared conjunction failed. |
| D3 seen-mechanism diagnostic | MiniLM27→31/96; MARCO30→26/96 | Both CE/Brier worsen. Training on related mechanisms did not establish strong transfer to these policies. |
| Frozen P3 Qwen0.5B | New129/240; probes20/24(9/12both orders) | New122/240semantic answers flip on reversal; rules65/80flip and only4/80correct both orders. Better probe agreement did not beat encoders' inherited/new proper scores. |
| M6 full-parameter Qwen run | Same-schedule TRAIN805→431/1500; CE1.357724→1.390592 | Worse than variable-arity uniform CE1.322383. All recorded TRAIN argmax positions0, but full TRAIN vectors were not saved. |
| E6 independent M6 result | New original129→65/240; reversed118→65/240; probes20→8/24 | All624development choices are first-position winners WITHOUT ties; margins.102494–.456558. New both-order agreement82→0/240; rule both-order4→0/80. |

M6 was one combined full-fine-tuning/training-permutation recipe, not an isolated test of permutation or architecture. It ran1500presentations/375updates in776.083seconds including fit/save; all resource guards passed. Its fresh624starting predictions were byte-identical to P3. Model/P4 execution success is not learning success.

Do not say every metric worsened: E6new-reversed NLL improves1.410621→1.407130 while Brier/ranking worsen; some family proper scores also improve. Overall trained probabilities remain worse than uniform in the reported inherited/new/probe populations. See ../docs/evaluation/e6-decoder-learning.md for all qualifications.

## What the diagnoses do and do not establish
- D5 checked all1500TRAIN identities, content, option permutations and target remapping: no mismatch. Row order is interleaved; maximum whole-family runs6/7/7, not a blocked-family epoch.
- Model's source review found no concrete defect in the scoped Python objective/accumulation/optimizer path. Native MPS gradient correctness and root cause remain unverified.
- D5's retained unsmoothed CE contradicts exact uniformity under that interpretation and conditionally certifies at least140TRAIN strict winners;1360TRAIN tie statuses remain unresolved. Development vectors do not fill that missing evidence.
- R6 finds partial static letter/slot effects but substantial interactions. The four-cell comparison is not a pure causal separation of letter, position and content effects. High allowed-token mass was measured in its48TRAIN cases, not across all unseen decisions.
- No model, data or backend cause has been established strongly enough to call it solved.

## Process evidence
I4's60m09s observation recorded31peer messages/16directed routes. Acknowledgement median4m26s/p90~27m38s is attention timing, not transport latency; unknown activity and right-censoring matter. One receipt-inspection improvement shipped; no causal time saving or compute bottleneck was demonstrated.

D4's24TRAIN-case/14group audit found no demonstrated label erratum and did identify supervision-coverage weaknesses. D5 subsequently answered a concrete failure-diagnosis question. These are different tasks, not one extended observation.

## Pending at this snapshot
M7/P5/E7 are authorized in review/evidence/handoffs/lead/wave-20261111-1635/. Default M7 changes only LR2e-5→2e-6 from the original base, with richer TRAIN-vector logging; a narrowly evidenced pre-learning correctness-repair substitution shares the same one-attempt budget. This is a hypothesis, not a known cure. No M7outcome is included.

I5, D6 and R7 are planned/authorized here; their later outputs are intentionally excluded. Do not use knowledge of subsequent live results in a first review of this snapshot.
