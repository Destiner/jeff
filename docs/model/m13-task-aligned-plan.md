# M13: task-aligned M9 warmstart

Source preparation only. No execution, build, tokenization, training, evaluation,
checkpoint inspection, or runtime verification is claimed here. Science follows
`artifacts/model/final-sprint-20261112-01/decision-frozen.md` and Research
choice `0b58deb4`; this document does not authorize a launch.

## One frozen endpoint

- Initialize from actual trained twelve-epoch M9, not original pretrained START.
  Retained cross-encoder, full backbone and retained trained ranking head; no
  head reset or optimizer-state continuation.
- CPU FP32, four threads, seed42, decision batch4, three complete epochs over
  480 rows: exactly 1,440 presentations and 360 optimizer updates.
- Fresh AdamW: backbone LR2e-5, head LR5e-4, weight decay .01,
  betas (.9,.999), epsilon1e-8. No scheduler, clipping, accumulation,
  early-best selection, numerical rescue, sweep, or second mixture.
- Existing tokenizer, actual-LF pair rendering, pooling/scalar head, cap256 and
  temperature1 unchanged.
- 240 fresh rows (80routing/80sentiment/80ticket), plus 240 deterministic
  original-v2 TRAIN replay (80intent/80sentiment/80rule_application), using the
  same family/ID hash ranking. No new rules, outcomes or protected cases.
  Preserve the 120/120 candidate histories; require new immutable release and
  exclusion pins. Rehearsal is not a guarantee of retention or an optimal ratio.

## Initializer and reference binding

The owner supplies the existing M9 checkpoint directory through
`--initial-checkpoint` and the exact SHA256 of its `checkpoint.json` through
`--initial-checkpoint-sha256`. Frozen checkpoint config pin:
`09c74c0374cbd46e97c608e7da8c6eb201f2f5b95370c2e347ca42320658c164`.
Existing encoder inventory pin (not independently checked by this delta):
`38908e2ce25cb02ed59f752e42fcc6dd5e67134fe8f98fb1297c40900fdcc255`.

Use the strict local `jeff.model.scorer.load_checkpoint` loader, with the exact
retained scorer class and requested model_id/revision/cap identity. Model ID is
`cross-encoder/ms-marco-MiniLM-L6-v2`, revision
`233902d25c440f23af6f7d6e94d2946bac0bee0a`, cap256. Loaded temperature must be1.
No remote/pretrained fallback is added for explicit initialization.

The owner must pass a guard to existing `train_run` and supply
`--m9-initial-run` pointing to actual M9 training/run.json, with
`--m9-initial-run-sha256`
`d50013f9236c69ae47d0b5212a0f607ae461c8bd92a28e25cc2a1d9a162067ee`.
The reference must have completed status and exact pinned bytes. All native
initial parameter hashes must equal its **weights.after** before validation,
baseline saving or any optimizer update. This is not an optimizer resume.

Without an initializer, loading, head handling, optimizer ordering and original
M9 errors remain unchanged: guarded binding still compares **weights.before**
to the original M4 start. The binding records its actual reference stage.
Warmstart metadata records checkpoint path/config SHA, trained-M9 origin and
fresh optimizer; architecture `head_initialization=pretrained` remains historical
origin, not a claim that the current trained head is original START.

Missing/unpaired initializer SHA, non-retained architecture, absent guard or
reference, wrong M9 reference pin/bytes/status, wrong scorer identity, non-T1,
and native parameter mismatch fail before updates. The config pin binds config
bytes; it alone does not authenticate all checkpoint files or tokenizer content.
The loader's existing strictness and owner-reviewed artifact/runtime pins remain
necessary. This delta does not enforce the entire scientific recipe or dataset
mixture; the owner must freeze and check them before launch.

## Owner execution gates and evidence

Before learning: final Data release; actual Evaluation64 content/exclusion
freeze and unchanged d7a3292c criteria; reviewed source/initializer/runtime pins;
ONE final-release tokenizer-only cap256 preflight. No diagnostic ledger reopening.

Owner supplies an artifact-local CPU guard using the existing
`bind/check/first_update/finish` interface, invoking existing `train_run` under a
finite parent. Existing ResourceGuards and MPS behavior are unchanged; the MPS
CLI guard is not a CPU wrapper. Require CPU FP32/four-thread evidence, 8GiB RSS
limit, pressure stop, serial closure and external successful process receipt.
Sampled guards do not guarantee continuous peaks or prevent hangs: parent owns
process-group deadline/kill/reap. Preserve the durable pre-update attempt marker,
partial outputs and failure evidence; no retry after an update attempt. Existing
save/finish/publication ordering remains unchanged.

One aggregate20-minute allowance covers final tokenizer preflight, training,
fixed480 TRAIN endpoint fit and new-candidate evaluation: only M9+M13 fresh64
native, M13 native240 retention with saved M9 baseline. No reversed fresh replay,
extra baselines or selection attempts. Separate300-second export/browser budget;
exact SDK6 input/binding evidence remains separate. Latest start20:00 and
selection freeze21:00 Europe/London on2026-11-12. One fixed endpoint and at most
one post-update attempt; current M9 is fallback. Promotion requires unchanged
prospective promotion/retention conjunction, not training loss selection.

S1 workspace and S2 primary evidence motivated M9; START's ticket/pooled-S1 and
negative-class advantages remain qualifications. No calibrated, general,
causal-isolation or guaranteed-improvement claim. Saved checkpoint, fresh-process
reload, external process receipt and authorized evaluation are still separate
owner evidence, not delivered by this source-only change.
