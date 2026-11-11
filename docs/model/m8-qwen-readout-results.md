# M8: readout-only CE improves; TRAIN agreement does not

**One frozen-base run completed: TRAIN agreement 805 → 804/1,500,
mean cross-entropy 1.357724 → 1.332200. P6 strict fresh reload passed;
independent E8 outcome is PENDING.** Evaluation has not delivered quality
conclusions. P6 is a reload/output-contract gate, not a quality score.
No default promotion follows; preserve M6, M7, v1 and Fable.

## Observed learning

| TRAIN scope | Rows | Teacher agreement START → FINAL | Mean CE START → FINAL |
|---|---:|---:|---:|
| Overall | 1,500 | 805 → 804 | 1.357724 → 1.332200 |
| Intent | 500 | 442 → 441 | 0.396153 → 0.370048 |
| Sentiment | 500 | 179 → 179 | 2.019892 → 1.997229 |
| Rule application | 500 | 184 → 184 | 1.657126 → 1.629324 |

75 selections changed: 16 wrong-to-right and 17 right-to-wrong.
All 1,500 rows had strict logit and probability maxima at both endpoints;
there were no tied rows. Every row's saved logits and probabilities changed.
Maximum absolute probability-vector component change was 0.1416273713;
maximum allowed-logit change was 0.3982505798.

The six-row head's L2 movement was 0.0051995856 (0.45206% of its initial
1.1501964331 norm); maximum absolute weight movement was 0.0002948327.
Small weight movement is **not zero behavioral effect**, proof of feature
incapacity, or a causal explanation. M7's nominal LR and clipping controls
were retained, but readout-only and full-parameter optimization have different
geometry. This single fixed schedule does not isolate a cause.

These are TRAIN teacher-agreement/fit measurements, not held-out correctness
or calibration. Both TRAIN and reused development evidence have correlated
teacher labels and reused source units; row counts are not independent samples.
E8 must separately assess the retained original-P3 comparators and P6 outputs.

## What ran and what was bound

One epoch used 1,500 TRAIN presentations, 375 optimizer steps/attempts, seed 42
and AdamW LR 2e-6. Only 5,376 FP32 scalars (W6, shape 6 × 896, no bias) were
trainable. The 494,032,768 original parameters (290 unique tensors) remained
frozen, outside optimizer/weight decay, with no original gradients; the
backbone ran in eval/no-grad, without a feature cache. These historical scope
and optimizer records are **producer-attested**, not independently replayed.

START's 1,500 saved predictions are byte-identical to retained M7 original-base
prefit, SHA-256 `4940b17902562c8da5cf34e80eaa3618fa5ab52c20ad90715fd6dc6d3c9d12d5`.
The START W6/original-base and FINAL W6/actual full-vocabulary head bindings
both cover all 1,500 rows: maximum logit and probability differences **0**,
identical top sets, within frozen 1e-4/1e-6 bounds. FINAL uses the same hidden
state for both projections, adding no backbone forwards. Saved-row review
found no validation discrepancies; it did not rerun inference.

Export representation is `hf-untied-full-vocab`: independent FP32
151,936 × 896 output storage, answer IDs 32–37 (A–F), and
`tie_word_embeddings=false`. The materialized config diff is only tied →
untied; the exact saved config is pinned in the run index. Original backbone
before/after/export identities and all non-answer rows match; the ordered
learned rows match W6. Input/output/head storage is disjoint.
The full output adds **544,538,624 bytes** of parameter payload.
Nine checkpoint files were verified; `model.safetensors` is 2,520,702,368 bytes
(2.520702368 GB), not a six-row-only on-disk export.

## Reload completed, quality still pending

[Runtime P6](../runtime/p6-m8-checkpoint.md) executed source
`9eeef9cea87fbd0bda7700127e88db95c7b97f9a` in a fresh process:
627/627 forwards = 3 fixed unscored startup + 624 development presentations
(300 original, 300 reversed, 24 paired probes), wall 36.245988 seconds.
All four HF loading diagnostics were empty (missing/unexpected/mismatched/error).
CPU storage-byte ranges and allocator-owned MPS buffer identities passed;
original tensors/fixed buffers, full output, six learned rows, non-answer rows,
config and tokenizer crosslinks matched. The slot is verified and closed,
with process and group absent. Model performed no extra inference.

This is component binding plus structural reload, **not per-development-case
W6-versus-full-head numerical replay**, nor independent attestation of training
history. P6 predictions are available to Evaluation; do not treat their mere
production as held-out quality evidence.

## Execution, correction and cost

Execution source was `ab55ad5ddaec7843c21b1caada9dbccb6240b5d4`.
Before the first weight load, Runtime identified an MPS storage-checker defect:
CPU payload-address intervals cannot be applied to opaque Metal backing handles.
The correction uses CPU byte intervals and distinct nonzero allocator-owned
MPS handles, rejecting same-buffer/views while retaining shape/FP32/extent
checks. It is not a generic external-Metal alias proof. Audits 01 and 02 and
the refreeze are preserved; no numerical failure was observed. This was a
source/checker correction, not a numerical-bound or learning-recipe change.

Model process wall was **246.449293 seconds**; Model aggregate including both
audits was **252.999084 seconds**. P6's separate wall is not part of that total.
Observed CPU lifetime high-water RSS was 3,367,747,584 bytes; sampled MPS driver
maximum 2,772,107,264 bytes and current allocation maximum 2,567,286,784 bytes.
Minimum sampled recommended headroom was 16,297,558,016 bytes. These scopes
are nonadditive; allocator/headroom samples are not true peaks or free RAM.
M8 source implementation and owner/integrated wheel+sdist package builds passed;
no tests or lint were run. Additional actual/pending spend: **£0**.

## Evidence and positional appendix

[Run index](m8-qwen-readout-run.json) carries exact source, recipe, schedule,
checkpoint, proof, output and small-evidence SHA-256 pins, plus the complete
saved family × arity positional appendix: means, population SDs (denominator N),
strict position counts and ties, START and FINAL, without pooling arities.
These values were copied from the actual artifact review, not recomputed.
Overall strict position counts (positions 0–5) were
`[417,384,411,278,7,3] → [468,394,362,266,7,3]`; ties were zero.

Actual artifact root: `/Users/destiner/Code/jeff/artifacts/model/m8-qwen-readout-20261111-01/`.
Sources: `full-run-freeze.json`, `checkpoint-ready.json`, `first-look.md`,
`artifact-review.md/json`, `p6-return.json`, `prelaunch-final-review.md`, and
saved training receipt/readout proof/checkpoint manifest. Earlier artifacts'
“P6 pending” statements describe their creation time; P6 return supersedes them.
The [readiness assessment](m8-readout-readiness.md) remains immutable historical
context: the run was subsequently executed under the lead grant, not an edit
to that assessment. No additional inference or training was performed for
this publication.
