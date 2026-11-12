# M10 — Qwen seed7 TRAIN results

## Status and scope

One actual learning attempt completed on 2026-11-12, 02:06:07–02:18:06 UTC.
The nine-file v1 checkpoint is saved and unchanged. Parent streaming hashes and
process/group absence are verified; this report does not decode or rehash weights.
Independent E11 CPU TRAIN review completed 65/65 checks. P9 fresh reload and
E11 development evaluation are **not complete**; no promotion follows.
This initial draft is not a gate. Parent will add actual future P9 native closure
before final review. Main M10 documentation is not yet integrated.

## Controlled recipe

Execution source: `a23c04cef0bff3e87deaffc3b8f5fed73ea818ee`.
Fresh original P3 weights, not M7 continuation: full 494,032,768 FP32 parameters.
The only scientific change from M7 is seed42→7, including RNG and a new row/option
schedule: `207365e681aa22da7904f2c555cf4dd207b776c5ecc8f77a1ac141b17b3e3236`.
These are not the same TRAIN presentations as seed42; START is **777, not 805**.
LR 2e-6, 1,500 presentations, 375 updates, AdamW, microbatch1/accum4 remain M7's
recipe (one epoch; clip1; no scheduler). No post-update retry or fallback occurred.

## Fixed-checkpoint TRAIN fit

Agreement is against source/teacher labels, not independently established truth.

| Population | START→FINAL agreement | Producer mean CE START→FINAL |
| --- | ---: | ---: |
| All TRAIN | 777→1214 /1500 | 1.3897271330680354→0.4160545839496617 |
| Intent | 436→498 /500 | 0.355663976→0.020749456 |
| Sentiment | 174→483 /500 | 2.093026357→0.123621193 |
| Rules | 167→233 /500 | 1.720491066→1.103793104 |

E11 corroborates all 3,000 saved vectors and the actual seed7 schedule across nine
TRAIN shards. Independent FP64 logit CE is 1.389727139→0.416054592; its small
difference from producer FP32 arithmetic is roundoff, not a contradictory result.
All raw tops are strict: no exact ties. Same-ID gains/losses are 514/77 overall,
140/74 for rules. CE worsens on 252 rows; Brier worsens on 242.
All 375 preclip norms are finite; 360 exceed1. These are not Adam update bounds.
FINAL rule winner positions are **0:26, 1:83, 2:388, 3:3**: strong third-position
tendency persists. No semantic rule competence, transfer, calibration, significance,
better-seed selection, or architecture/capacity claim is supported.
E11 independently checked arithmetic/source after seeing first-look claims, not
pre-outcome criterion selection. No review, reshuffle, or tokenization was repeated here.

## Preserved preparation and failure history

CPU preparation I–S sibling-import/AST-source-comparison failures remain preserved.
Exact M7 environment repair grant `b1a7c2c8` expired at02:06; refreeze was02:05:28,
then actual training started02:06:07. Root01 native audit succeeded and had already
loaded the tokenizer. TRAIN revalidation then failed **before model load**, because
wrapper-forced scientific environment keys differed from M7's historically unset
keys. It is not a failure before tokenizer use. Root01 has no ATTEMPT marker;
root02 has the first-learning marker. The completed receipt supersedes root02's
initial zero-count incomplete sentinel; that sentinel is not another learning run.

## Time, memory and cost

Actual process wall: 718.6951539576985s. Aggregate: 728.1505363737233s/2400s,
including root01 audit3.457409583032131s, pre-load failure2.8124029161408544s,
and root02 audit3.1855699168518186s. Unused budget is not retry authority.
CPU lifetime RSS max3,377,381,376B; sampled MPS driver max11,886,329,856B;
minimum sampled recommended headroom7,183,335,424B. External sampled per-process
RSS max2,813,263,872B is a separate scope. These quantities are not additive;
sampled MPS/current RSS observations are not guaranteed continuous peaks.
Additional actual/pending spend: £0/£0.

## P9 remains open

First P9 attempt failed at initial Transformers import: the launcher selected the
orchestration-only root venv instead of Runtime's existing environment. Zero model
or tokenizer construction and zero forwards; all recorded groups are absent.
Charge the full outer309.808853250s despite the ~0.09s native child. Preserve
`release/p9-m10-20261112-01/` and original packets; do not relabel failure as success.
Explicit renewal remains pending in this evidence snapshot. Neither P9 nor E11
development is delivered, and no remaining-time reuse or promotion is authorized.

## Evidence

Compact [run inventory](m10-qwen-seed7-run.json) references the actual root02,
parent `checkpoint-ready.json`, independent `e11-m10-control-review-v1`, both
02:21/03:01 handoffs and parent `p9-failed-return.json`. Large vectors, per-row
losses, private held-out data and weights are intentionally absent from this report.
