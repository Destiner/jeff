# M11 — more TRAIN fit, not broad transfer improvement

**The fresh 30-epoch MS MARCO endpoint improves TRAIN agreement from M9's
1,314 to 1,414/1,500, but new-development agreement falls165→162/240 and
both proper scores worsen.** D3 gains three agreements while its NLL/Brier
worsen materially. M11/P10 is complete and closed; no promotion or further
duration arm follows.

## Fixed contrast

M11 restarted the original M4 MS MARCO base
`cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`.
It is **30 total epochs**, not continuation of M9 or30additional epochs.
The recorded105 initial parameter hashes match the original M4 control.
Execution source is `a23c04cef0bff3e87deaffc3b8f5fed73ea818ee`.

The unchanged encoder recipe uses seed42, batch4, cap256, FP32/MPS/fourthreads,
backboneLR2e-5 and pretrained-headLR5e-4, with the existing optimizer,
shuffle and before/after intrinsic validation. No clipping, scheduler,
new selection rule, best-checkpoint choice or post-update restart was added.
One run completed11,250updates/45,000presentations. The prospective E9 branch
condition was met by actual M9 sentiment70/80, intent78/80 and
NLL.699420442<.9173; this was eligibility for a fixed exploratory contrast,
not a promotion or an untouched-test decision.

## Saved fixed-endpoint TRAIN fit

The sole final fit reuses the exact1,500 label-free M9 TRAIN inputs and
reference. Agreement is against supplied labels, not independent truth.
CE below is reconstructed from raw saved probabilities, without clipping
or renormalization.

| TRAIN population | M9 twelve epochs → M11 thirty epochs | Mean CE |
|---|---:|---:|
| All1,500 |1314→1414|.289057329→.123309483|
| Intent500 |500→500|.000357380→.000041338|
| Sentiment500 |500→500|.006220120→.000052332|
| Rules500 |314→414|.860594487→.369834778|

All saved maxima are strict and target probabilities positive. There are
130gains/30losses and168changed choices, all in rules;86rule disagreements
remain. Family×arity coordinate means, population SDs and winner counts are
retained in the artifact first look, without mixing arities. The independent
saved-artifact review agrees within floating-point roundoff; it checked
3,000 M9/M11 vectors and11,250 finite recorded training losses, not replayed
updates or independently decoded tensors.

Intrinsic300-row validation remains observational: original129/300,
loss1.052229678; final204/300, loss.839592848. M9 had208/300 and.694205557.
That degradation did not trigger endpoint selection, another epoch or a retry.

## Independent E12 and R14 follow-through

Evaluation owns the [complete E12 result](../evaluation/e12-encoder-duration30.md).
Only M11 was newly scored;14old development and9old D3 contexts were retained.
Development includes inherited60, new240 and12already-paired probes; these
strata, reversals and mechanism/source views are not independent sample multipliers.

| New240 | M9 | M11 |
|---|---:|---:|
| Agreement in each order / both-correct |165|162|
| Intent / sentiment / rules, each80 |78 /70 /17|77 /72 /13|
| Native NLL |.699420442|.860174719|
| Native Brier |.359766381|.411283631|

M11 has8gains/11losses on new cases. Inherited agreement43→42 and both proper
scores worsen. Probes provide a genuine exception: both-correct8→9/12,
retaining all8; NLL improves1.362500→1.085853 while Brier slightly worsens.
These mixed exceptions do not turn the fixed duration contrast into broad improvement.

D3 is96original-only cases/48new policies/eight intentionally seen mechanisms,
not96independent sources. M9→M11 agreement26→29 and complete policies2→5,
but NLL1.419132→1.914380 and Brier.775609→.903707; M11's proper scores are
worse than all nine retained D3 baselines. Case retention/gain/loss/neither
is18/11/8/59; policy counts1/4/1/42. Lexicographic/packs NLL improvements
and rounding's more hits but worse NLL remain in the full report.

[R14](../research/m11-mechanism-fit-append.md) identifies a more specific
fit/transfer distinction: the mapped FIFO, discount and coordinate TRAIN sets
now each reach20/20cases and10/10policies. Their new D3 results are respectively
6/1/3of12cases and2/0/0of6complete policies. This is complete fit on small,
particular TRAIN sets alongside limited new-policy performance—not algorithm
mastery, exhaustive branch coverage or an isolated architecture diagnosis.
TRAIN and D3 policies are not paired; source/prose/parameters/arity differ.

E12's independent TRAIN/control review reports3079checks, P10 binding2806+36,
all same624 contrasts and all ten D3 raw sets/nine comparisons in its stated
scope. No substantive discrepancy was found there. Historical internals and
source-label truth remain qualified; same-alias rule verification is not
independent human adjudication.

## Execution, resources and preserved history

Training ran03:21:30–03:34:55UTC on12November2026 for803.2143017495982s;
the sole final TRAIN fit took6.6324648330919445s. Model subtotal is
809.8467665826902s. P10 then performed one fresh encoder load with720decisions,
180native batch4calls and2751probabilities: unchanged624development plus96D3,
zero startup/canary. Its supervisor recorded37.59575429186225s, conservatively
charged39s including publication allowance. The chain closes at
**848.8467665826902/1500s**; unused651.1532334173098s grants no further work.

Before any M11 load, a102.897345s operational amendment reconciled the frozen
launcher with P9's actual separate native completion receipt. Original launcher
and freeze remain; new `launch-02.py`/`freeze-02.json` retain exact identity,
receipt-path containment, completion, command and group checks. There was no
failed M11 native attempt or scientific recipe change. The first-update marker
and all30-epoch outcomes are preserved.

Parent verified the seven checkpoint-file hashes, completed external run/fit
receipts, exact final-fit IDs/options and P10 outputs, plus actual process-group
absence. Embedded checkpoint metadata retains historical `run.status=running`;
that is not completion evidence. External completed receipts establish completion.
This inventory is not a new loader contract or independent tensor/update replay.

Separate8GiB RSS/driver ceilings and>=2GiB recommended headroom applied.
Sampled per-process RSS, CPU lifetime high-water and sampled MPS allocations
have distinct, nonadditive scopes; samples are not continuous peaks or real-time
OS guarantees. Existing longest-first256 semantics remain; no new tokenizer
length diagnostic was performed. Additional actual/pending spending is£0/£0.

## Evidence

[Machine-readable inventory](m11-msmarco-duration30-run.json) pins the original
and amended freezes, branch, run, final fit, checkpoint readiness, independent
artifact review and P10 closure under
`artifacts/model/m11-msmarco-duration30-20261112-01/`.
E12's report/index and R14's explicitly linked actual-D3 addendum retain their
own review/timing provenance. Reports and reviews did not gate native handoffs.
No protected-final/D7 consumption, dependencies, tests/lint, uploads or extra ML
were introduced by this publication.
