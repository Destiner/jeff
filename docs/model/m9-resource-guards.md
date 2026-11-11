# M9: opt-in encoder resource plumbing

Source preparation only; no launch/slot grant. M8 is finished and P6 reserved;
parent alone schedules jobs. Reference: `configs/model/m9-msmarco-duration.json`.
JSON is not consumed by the CLI: parent must freeze explicit arguments and source.

## Fit first, then conditionally train

Parent invokes the existing predictor once for each retained M4 trained encoder
on decision-only, manifest-order TRAIN1500, batch4, saving every probability and
external successful process receipt. Validate complete coverage before evaluating
the branch. Only MS MARCO sentiment **<450/500 OR rule_application <450/500** after
both fits permits one fresh duration arm. Both >=450 means skip; invalid/missing
vectors mean failure, not authorization. Intent is reported, not a branch input.

The arm starts from original `cross-encoder/ms-marco-MiniLM-L6-v2`, immutable
revision `233902d25c440f23af6f7d6e94d2946bac0bee0a`, retained pretrained ranking
head. It does **not** resume M4 or substitute a saved baseline. Same M4 recipe:
seed42, decision batch4, threads4, cap256, backbone LR2e-5, head LR5e-4;
12 epochs, global max_steps4500, 18000 presentations. AdamW weight decay .01,
betas .9/.999, epsilon1e-8; no clipping, scheduler, accumulation or extra numerical
operations. Original manifest-order indices followed by Python shuffle each epoch
and all seed/model/optimizer ordering remain unchanged. MPS is not guaranteed
bitwise deterministic. Intrinsic validation300 before/after remains unchanged,
not a selector. No extra TRAIN baseline or fit is added to the training loop.
Parent separately invokes the existing predictor for final TRAIN1500 (one
budgeted reload) and activates reserved P7 through checkpoint/process evidence.

## Explicit CLI templates (parent supplies unique paths)

Use the existing environment, not an environment sync. Set `JEFF_ARTIFACTS_DIR`
to `/Users/destiner/Code/jeff/artifacts`, `HF_HOME` to its
`model/hf-cache-20261111`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`.
Missing cached files must fail; no download is authorized.

```sh
python -m jeff.model.predict --checkpoint "$CHECKPOINT" \
  --input "$DECISION_ONLY_TRAIN" --output "$NEW_PREDICTIONS" \
  --device mps --batch-size 4 --m9-resource-guards

# Only after the parent verifies the condition and reserves downstream budget:
python -m jeff.training.train --dataset-manifest "$MANIFEST" --output-dir "$NEW_RUN" \
  --architecture retained_cross_encoder \
  --model-id cross-encoder/ms-marco-MiniLM-L6-v2 \
  --revision 233902d25c440f23af6f7d6e94d2946bac0bee0a \
  --device mps --seed 42 --batch-size 4 --threads 4 --max-length 256 \
  --learning-rate 2e-5 --head-learning-rate 5e-4 \
  --epochs 12 --max-steps 4500 --m9-resource-guards \
  --m9-initial-run "$ORIGINAL_M4_MSMARCO_RUN_JSON" \
  --m9-initial-run-sha256 "$FROZEN_ORIGINAL_RUN_SHA256"
```

Before validation or updates, guarded training compares all already-computed
initial parameter hashes with the original M4 run's `weights.before`, requiring
its pinned bytes and completed status. No additional tensor/hash scan is added.
Mismatch stops before learning; the binding and actual hashes remain in failure
metadata. The inference environment explicitly fixes OMP/MKL/VECLIB threads to4
(the existing predictor has no threads CLI flag).

## Guard evidence and completion

Without `--m9-resource-guards`, legacy execution is retained. Optional helper
arguments default to None; Runtime's `_rows(path)` and
`_write_batch(model, rows, output)` calls remain valid. Scorer/checkpoint format
and backend are unchanged. Guards receive the existing torch module; they do
not import torch, draw randomness, or add forward/backward/norm/optimizer ops.

Enabled guards require MPS and fail closed on missing/invalid telemetry. Sampled
process-lifetime RSS high water and synchronized MPS driver must each be
<=8589934592 bytes (not their sum); recommended max minus driver must be
>=2147483648 bytes. Samples surround load, each validation/prediction/training
batch, parameter hashing, saves and final publication; an extra pre-step sample
can stop after backward without an update. These are sampled limits, **not**
continuous peak guarantees. Parent owns process-group kill/reap, external RSS,
hang/deadline enforcement and the ONE aggregate1200-second allowance including
both fits, optional training/validation, final fit and P7. Reserve P7 first.

Trainer writes `m9-resources.jsonl`, `.summary.json` and, immediately BEFORE the
first optimizer.step, durable `.first-update-attempt.json` in its new run dir.
The marker is conservative: its presence forbids retry even if the step failed
or counters still say zero. Sample/marker writes are flushed and fsynced; new
entries are directory-fsynced. Predictor evidence uses prefix
`<output>.m9-resources`. JSONL elapsed timestamps preserve phase/sample timing.

Guard completion, event-file close and durable summary precede publishing
trainer `checkpoint.partial` as `checkpoint`, writing completed `run.json`, or
atomically linking final predictions. No guard runs after publication. A guard
summary alone is NOT a successful trainer/process receipt: existing completed
`run.json` AND external successful process exit remain required. For predictions,
require final output, guard evidence and external successful process exit.
Failures retain failure.json/guard evidence, baseline and any staged checkpoint;
predictor retains its temporary partial path (reported on stderr). No new weight
save is attempted after a breach. Existing checkpoint-save implementation may
remove its own incomplete directory on an internal save exception. Hard kill
can leave only partial JSONL/marker; parent preserves that evidence. There is
no post-update restart/numerical rescue, automatic branch or supervisor here.
