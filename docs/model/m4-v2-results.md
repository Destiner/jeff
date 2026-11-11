# M4: frozen-v2 results

## Experiment and frozen identities

Question: does broader v2 training improve each candidate against its own fresh start,
without family-level inherited/probe regressions against its v1-trained predecessor?
The [pre-result plan](m4-v2-plan.md) defines a descriptive gate, not significance or promotion.
The [frozen recipe](../../configs/model/m4-v2-comparison.json) was executed once per architecture,
sequentially; no retry or post-result tuning. All old candidates remain preserved; CLI default unchanged.

- Run root: `artifacts/model/m4-v2-20261111-01/` (below, `R`).
- Both trainer receipts record clean source `812a6557a559b82882b2a24a5c2f37fa9b74a163`
  in `.worktrees/model`, with per-source SHA256 in `R/{minilm,msmarco}/run.json`.
- Released `artifacts/data/data-pilot-v2/manifest.json` SHA256:
  `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`.
  This is final/revised-r3, not the superseded pre-review-r2 candidate.
  1500 train (300 inherited + 1200 new), 300 validation (60 inherited + 240 new).
- MiniLM: `sentence-transformers/all-MiniLM-L6-v2` at
  `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, mean pooling, explicitly reset random scalar head.
- MS MARCO: `cross-encoder/ms-marco-MiniLM-L6-v2` at
  `233902d25c440f23af6f7d6e94d2946bac0bee0a`, retained pretrained ranking head/native pooling.
  Tokenizers use the respective pinned revisions. Neither run resumes M2/M3 weights.
- Evaluation identities and exact input hashes: `R/input-receipt.json` and
  `artifacts/evaluation/e3-m4-v1/{receipt,subsets}.json`; new decision input SHA256
  `a3b65924d7ea3ed9b638457d42d7274ddcdad5a0d40ad5c87fd975da0a2846e0`.

## Separate-stratum comparison

E3 independently scored predictions, not independently verified every label. Cells are
supplied-label agreement count / natural-log loss (lower loss is better); no mixed headline.
All eight E3 predictors had complete valid coverage without failures or extra IDs.
Declared source groups: new 170, inherited 12, probes 12; rows/reversals are not independent.

| Candidate | New-v2 (240) | Inherited-v1 (60) | Probes (24) |
| --- | --- | --- | --- |
| Uniform | 65 / 1.333463 | 17 / 1.378765 | 8 / 1.055008 |
| Lexical | 99 / 1.296868 | 29 / 1.323710 | 9 / 1.047044 |
| M2 MiniLM v1-trained | 107 / 1.136427 | 35 / 0.855288 | 16 / 0.710407 |
| M4 MiniLM fresh start | 66 / 1.332467 | 20 / 1.378267 | 2 / 1.057107 |
| M4 MiniLM trained | 132 / 0.823115 | 34 / 0.907554 | 12 / 1.025456 |
| M3 MS MARCO v1-trained | 110 / 1.024844 | 40 / 0.793701 | 8 / 1.360701 |
| M4 MS MARCO fresh start | 99 / 1.058568 | 30 / 1.026878 | 14 / 1.453783 |
| M4 MS MARCO trained | 141 / 0.917258 | 42 / 0.712621 | 10 / 1.876464 |

Both improve new-v2 agreement **and** loss against their own starts. **Neither passes
robustness versus its corresponding v1-trained predecessor; no promotion.** Specifically:

- MiniLM inherited intent: M2 20→17/20, loss 0.067838→0.500164.
  Probes: 16→12/24, losses worse in every family. New-rule agreement falls
  19→15/80 versus M2 and 21→15 versus fresh start; new-rule loss also worsens.
- MS MARCO inherited intent: M3 19→18/20, loss 0.211817→0.251990 despite aggregate gains.
  Probe agreement 8→10/24 hides loss 1.360701→1.876464, worse in every family;
  intent 4→2/8. Versus its fresh start probes fall 14→10/24 with higher loss.
  New-rule agreement improves 14→21/80 versus M3 but loss worsens 1.405047→1.411166.
- Between trained M4 models, MS MARCO wins nine new labels but loses on log loss
  (0.917258 vs 0.823115) and Brier (0.481392 vs 0.460115). Ranking and probability quality differ.
- New rules remain weak: MiniLM 15/80, MS MARCO 21/80, deterministic uniform 23/80
  (tie-break baseline, not learned reasoning). These 80 cases represent 40 policy instances /
  10 mechanism groups; there is no seen-mechanism rule-validation comparator.

## Controls, reload and resources

Both exact-tokenizer final-release audits cover all 1800 rows / 6848 fully serialized
state/question/candidate pairs: min 41, median 61, p95 96, max 169 tokens including pair
formatting. At shared cap 256: zero overflow, question loss or candidate loss. Reports:
`R/{minilm,msmarco}-token-budget.json`; tokenizer SHA256 in both:
`851ca67100d372ca3ae031a6abd168f53489eebfd7d89523f35c5c9b4d372c3c`.
This is no-truncation evidence for released bytes, not unseen longer inputs.

Both actually completed 1125 updates, 4500 presentations, three full epochs, batch 4,
seed 42, AdamW backbone/head LR 2e-5/5e-4, weight decay 0.01, four CPU threads, MPS.
No scheduler, calibration or early stopping; backbone and head hashes changed in each.
Equal exposure/update budgets do not equalize pretraining, pooling, dropout or realized compute;
MPS seed setting does not guarantee bitwise determinism.

`R/inference/receipt.json` records 16 successful sequential fresh-process offline reloads,
each with an initially empty unique HF_HOME: 12 M4 baseline/trained outputs across
combined/reversed/probes (300/300/24 rows), plus four preserved M2/M3 new/reversed outputs
(240 each). Existing inherited/probe M2/M3 predictions were reused, not rerun.
Per-job receipts bind commands, inputs, outputs and checkpoint roles; E3 rehashed them.
Trainer `run.json` alone is not fresh-reload evidence. Reload process walls: 1.568–3.024 s,
including startup/inference, not per-example latency.

Apple M5, 24 GiB unified RAM; Python 3.12.16, Torch 2.15.0, Transformers 4.57.6.
Training receipt measurements (bytes; elapsed through checkpoint saves, before receipt write):

| Run | Elapsed s | CPU high-water RSS | Endpoint MPS current | Endpoint MPS driver |
| --- | ---: | ---: | ---: | ---: |
| MiniLM | 74.403 | 1572257792 | 371979264 | 2265972736 |
| MS MARCO | 76.622 | 1819230208 | 374113792 | 2274361344 |

CPU RSS is process-lifetime high-water, **not accelerator peak**. MPS values are endpoint
samples, **not measured peaks**; do not sum them into a peak-memory claim.
Additional local-job spend £0; this excludes dataset generation and sunk hardware/electricity.

## Evidence, limits and bounded recommendation

Paths are relative to the shared `/Users/destiner/Code/jeff/artifacts` root unless prefixed `artifacts/`.

- Model handoff: `handoffs/model/20261111T1201-M4-predictions-ready.md`.
- E3 handoff: `handoffs/evaluation/20261111-e3-M4-independent-results.md`.
- E3 machine results: `evaluation/e3-m4-v1/{new-v2,inherited-v1,probes}/comparison.json`,
  adjacent `report.md` and `*-order-report.json`; source units: `evaluation/e3-m4-source-units-v1/`.
- Exact executed trainer argv/config/source hashes: `R/{minilm,msmarco}/run.json`;
  inference commands: `R/inference/receipt.json`, `*.invocation.json`; queue script `R/infer.py`.
  These are reproduction records, not instructions or authorization to rerun.

New labels are 160 teacher / 80 rule_verified, inherited 40/20, probes 24 teacher with unknown
curator. Same-alias author/reviewer, source/domain concentration and residual length/specificity
shortcuts limit interpretation. Reused development sets, one seed and correlated groups prevent
broad generalization or calibration claims. Changed data mixture **and updates** versus v1
preclude broad data-only causality. Hash/group exclusion checks do not prove semantic isolation.
Reserved final data stayed sealed; this documentation task did not load models or tokenizers.

One next recommendation: retain current candidates/default and, only if separately authorized,
pre-register one bounded lower-head-LR comparison as suggested by Research R4, retaining these
strata and regression gate. R4 is advisory: **no further jobs or spending are currently authorized**.
