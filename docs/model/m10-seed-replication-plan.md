# M10: one seed-7 replication of full-parameter M7

## Authority and treatment

Explicit Lead grant `e1da193e`: exactly ONE fresh original-P3 full-parameter
replication of M7, changing **seed42 → seed7 only** scientifically. This includes
the deterministic row/option permutation and Python/CPU/MPS RNG reset. This is
not continuation from M7 weights, a repair, a scope contrast, or a seed sweep.
Implementation preparation does not authorize the worker to execute ML. The
parent Model owner alone schedules native work after P8 returns and validates
the pre-outcome control/freeze and aggregate budget.

Fixed recipe: [`m10-qwen-seed7.json`](../../configs/model/m10-qwen-seed7.json),
`m10.recipe.v1`. Relative to actual M7, the only recipe differences are schema,
seed7 and the operational run bound2700→2400seconds. Keep LR2e-6, oneepoch,
1500TRAIN presentations/375updates, microbatch1/accum4, full FP32 AdamW,
betas(.9,.999), eps1e-8, decay.01, clip1, foreachFalse, no scheduler,
MPS/SDPA/fourthreads, train/eval modes, original P3 prompt/template/allowed-symbol
readout/T1/cap1024/no truncation/no cache/last-token projection. No new data,
capacity probe, canary, development START, intermediate pass, numerical rescue,
retry or extra learning. No held-out or final data enter this trainer.

## Parent CLI and supervision

Use a clean committed checkout, existing locked offline model environment and
M7's actual package/backend controls. Do not install dependencies, enable MPS
fallback or change allocator settings. All directories must be new.

```sh
RUN=/Users/destiner/Code/jeff/artifacts/model/UNIQUE-M10-RUN
uv run --locked --extra model python -B -m jeff.training.qwen_decision audit \
  --experiment m10 --output-dir "$RUN/train-audit"

uv run --locked --extra model python -B -m jeff.training.qwen_decision train \
  --experiment m10 --audit-dir "$RUN/train-audit" \
  --capacity-receipt /Users/destiner/Code/jeff/artifacts/model/m7-qwen-low-lr-20261111-01/training/receipt.json \
  --authorize-run M10-ONE-original-P3-full-1500-375-seed7-lr2e-6 \
  --comparison-freeze-sha256 "$PARENT_VALIDATED_COMPARISON_FREEZE_SHA256" \
  --output-dir "$RUN/training"
```

The existing `--capacity-receipt` argument deliberately points to the **completed
M7 full-training receipt**, not the M6 one-step capacity receipt. M10 capacity
CLI is rejected before directory creation and at the capacity function itself.
M6/M7 CLI defaults, historical schedule/capacity gates and M8 behavior remain.

Parent must enforce **aggregate Model ML <=2400seconds**, charging audit,
training/revalidation/load/both fits/save and any authorized Model handoff work
against the same budget. The trainer's2400-second cooperative whole-process cap
is an upper bound, not a second allocation; set external TERM/KILL to the
remaining aggregate budget. Native operations cannot be interrupted by a
cooperative guard. Serialize substantial model loads. Keep CPU lifetime RSS
and MPS driver separately <=16GiB, recommended headroom >=2GiB; never sum RSS
and driver. Samples are observations, not continuous peak guarantees.

## Materialized seed7 schedule and scientific identity

The TRAIN-only audit uses `Random(7)`: shuffle all1500rows, then shuffle options
once per row, exactly as M7's algorithm with the seed replaced. It writes the
actual `schedule.jsonl`, pins its actual SHA256 in `m10.audit.v1`, and records
ordered option IDs, original option IDs, target ID and remapped zero-based
target position, exact prompt tokens/hash and allowed-answer token IDs. The
parent must freeze **that actual new SHA**, never substitute historical seed42
`M6_SCHEDULE_SHA`. No seed7 schedule/hash is claimed before this audit executes.
Training rederives seed7 through the same boundary and requires byte equality
with the materialized audit schedule and its hash. Target-ID remapping is also
checked before model load. A new complete1500TRAIN prefit is mandatory because
option order changed; M7's original-base TRAIN prefit is **not** reused.

M10 source identity follows the existing M8 separation: tracked Python,
pyproject/lock, M10 recipe and P3 scorer config hashes are hard scientific pins;
Git revision and other tracked docs/configs remain recorded operating context.
A clean committed worktree is still mandatory. Hard pins bind audit through
completion; docs-only commits do not invalidate M10 scientific identity.
Historical M6/M7 source binding remains unchanged. Historical identities are
retained, never relabeled as current evidence. Source revisions across M7/M10
are not asserted byte-identical: source review isolates the seed/new identity/
operational-budget changes, while the parent's frozen control record establishes
unchanged scorer semantics. No broader historical-profile exception is added.

## Reused actual completed full scope; no new model probe

M10-only `qwen_seed.reuse_m7_capacity` verifies these actual immutable files under
`artifacts/model/m7-qwen-low-lr-20261111-01/` before any model load:

| File | SHA256 |
| --- | --- |
| `training/receipt.json` | `c78ad96769b76c2cabb7c2b0ec87dde13bca78e2f7e2256a51b6ca545b54e156` |
| `train-audit/audit.json` | `3182c01d5128342a3338ba3bf05ed8a9b79524f1a58c8620e7686063645eb814` |
| `train-process.json` | `26cef7e812511a087f16883a3626c749689e3b03e648a072d4be4026c2b517c3` |

Checks include successful supervised full run,1500/375/no extra backwards,
full FP32 parameter scope/Adam moments, both1500fits,375norms, actual phase
counts, original base/fresh optimizer/RNG, observed memory/headroom/time guards,
and the complete historical audit binding. Model/tokenizer/template assets,
P3 scoring config, TRAIN release/shards/metadata, packages and backend environment
must equal current evidence. Recipe equality excludes **only** schema, seed and
operational run bound. Source/recipe identities remain separately recorded;
schedule-algorithm difference must be exactly42→7. Length distribution is
recomputed from the new schedule; every new prompt must be no longer than the
maximum actually exercised by M7's completed full run (220tokens), and never
exceed cap1024. If that shape gate fails, stop without a probe or relaxed cap.
Historical738.52s full-process time is evidence, not a performance guarantee.
No M6 projection is repurposed as new M10 capacity and no M7 trained state loads.

The parent prepares the comparison/control reuse record in parallel. Original
624 P3 START outputs may be reused **only** with actual unchanged original-base,
scorer and exact development-input pins (including actual output identities).
Seed7 training order does not authorize altering development inputs. A SHA
argument records the owner's validated freeze; the trainer does not read
held-out outcomes or independently validate that record's contents. Preserve
existing controls, inputs and artifacts; zero new development START forwards.

## Attempt durability, observations and handoff

A fresh process resets `random.seed`, `torch.manual_seed` and
`torch.mps.manual_seed` to7 before original-base loading; optimizer is newly
created empty after the mandatory original-base prefit. Neither M7 learned
weights, optimizer moments nor RNG state are reused.

Immediately before the first `optimizer.step`, `training/ATTEMPT.json` is
exclusively created with authorization, audit/schedule/control-freeze hashes,
four presentations and zero completed updates. File flush + file fsync + run
directory fsync + parent-directory fsync finish **before** the update. Any
failure in durability prevents the step. Existence spends the attempt even if
step completion is unknown. The receipt also records the marker/hash. A hard
kill cannot be interpreted as permission for a post-update restart. Unique
output directories and literal authorization are not a global attempt ledger:
the parent must inspect this marker and its own durable wrapper state and must
not retry in another directory. No numerical rescue is allowed.

Both existing full1500TRAIN fit passes retain M7's richer full ordered
logits/probabilities, token/option/target IDs, exact top sets/ties and margins,
alongside CE/argmax/family/source/group aggregates. `gradient-norms.jsonl` retains
all375already-computed preclip norms, one per update, without extra forwards or
norm computations. The final-only receipt is `m10.train.v1`; checkpoint remains
ordinary full FP32 safe HF weights and unchanged
`jeff.qwen-trained-checkpoint.v1`. Qualified producer IDs follow M7. Failures keep
receipts/events and any durable ATTEMPT, never a complete checkpoint manifest.

Only checkpoint/ and checkpoint-manifest.json go to Runtime; TRAIN-labelled
schedules/fit rows stay with Model. Runtime owns the separately authorized fresh
final development pass, not this trainer. Improved TRAIN fit alone is not
transfer, calibration, a causal diagnosis of M7, significance, or promotion.
No default migration, extra spend or protected-final access is authorized.
