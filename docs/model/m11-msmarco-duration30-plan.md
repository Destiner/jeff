# M11 — conditional original-start MS MARCO, 30 total epochs

Source/artifact preparation only, authority Lead `e1da193e`. This plan grants no
native execution. Parent integrates and independently reviews before freezing.
No shared source changes are needed: existing trainer controls and seven-file
encoder checkpoint format are intentionally retained, including the names
`--m9-resource-guards`, `--m9-initial-run`, `--m9-initial-run-sha256`.

## Branch and evidence

Gate: actual E9 M9 **new-v2, original orientation** sentiment >=54/80,
intent >=73/80, overall NLL <0.9173. Evaluation delivery `19036eb6` reports
70/80 sentiment, 78/80 intent, and overall NLL **0.6994204422058061**
(240/240 valid). Condition is met, not a new claim of independent verification.
The prospective branch record binds exact rows 4045, 1413, 1385 in
`numbers.json.orientation_units`, report, delivery receipt and input-source pins.
No rescoring, held-out content replay, or new inference is part of preparation.

Artifact root:
`/Users/destiner/Code/jeff/artifacts/model/m11-msmarco-duration30-20261112-01/`
contains `prepare.py`, `launch.py`, `branch.json`. These are templates; neither
script has been invoked. No freeze or checkpoint-ready record is created now.
Evidence root: `artifacts/evaluation/e8-e9-analysis-v1/`.

## Fixed recipe

Exactly one fresh original M4 MS MARCO pretrained start, **not M9 resume**.
30 TOTAL epochs, 11,250 updates, 45,000 presentations over the original 1,500
TRAIN rows. Same manifest/revision, retained pretrained head, seed 42,
backbone LR 2e-5/head LR 5e-4, batch 4, cap 256, four threads,
AdamW (weight decay .01, betas .9/.999, epsilon 1e-8), no scheduler or clipping.
The existing trainer measures original 300 intrinsic validation rows before and
after; its 105 original parameter hashes must match M4 before any update.
Use existing M9 full TRAIN inputs/reference and measured initial controls;
**do not replay initial M4 fits**. One final 1,500-row TRAIN fit uses the existing
predictor. Retain all M9 artifacts unchanged.

## Parent-only freeze and finite launch protocol

1. Finish independent review and integration into the frozen native Model owner
   `.worktrees/model`. Owner stays frozen across M10/P9 then M11/P10; do not
   alter its environment here. Parent explicitly invokes
   `python -B ROOT/prepare.py INTEGRATED_40_HEX_HEAD` only after integration.
   Preparation checks clean exact HEAD, pins actual source/config, commands,
   manifest/shards, base assets, original M4 reference and reused inputs, and
   branch evidence. It exclusively creates `freeze-context.json`, `freeze.json`.
   No automatic refreeze. Parent records their hashes.
2. After actual P8/M10/P9 returns, parent freezes the separate operational
   `activation.json` with its real exclusive reservation and original process
   evidence, using the exact schema in artifact `README.md`. Scientific preparation
   does not itself grant a slot. Parent invokes
   `python -B ROOT/launch.py train FREEZE_SHA ACTIVATION_SHA BRANCH_SHA` once.
   Atomic `.active-ml` lock precedes history/accounting; do not reclaim stale
   locks. Existing unresolved/failing receipts block all continuation. Fresh
   HOME, offline shared HF cache, locked uv, isolated owner source. No retry.
3. Parent checks completed run, exactly 30 epochs/11,250 steps/45,000 examples,
   original hash match, intrinsic counts and resource receipts. On success only,
   create `checkpoint-ready-for-fit.json` with the exact artifact README schema:
   six successful invocation/process/run/resource/controller/first-update evidence
   bindings and exactly seven checkpoint file bindings. The external completed run
   and native endpoint/start checks are required; embedded checkpoint metadata may
   retain its historical running status. No tensor decoding is added.
4. Parent invokes
   `python -B ROOT/launch.py fit-final FREEZE_SHA ACTIVATION_SHA READY_SHA` once.
   Supervisor verifies the bound successful training and seven files before reload.
   Parent computes TRAIN statistics from saved outputs separately, no inference
   replay. Preserve failed/partial outputs; no rescue save or publication.
5. Parent hands frozen seven-file checkpoint, source/input pins, absence receipts
   and **actual** elapsed accounting to Runtime P10. P10 is separately scheduled,
   not a launcher job. Parent must debit its actual load/inference/cleanup time
   against the same ledger; no startup/canary allowance or hidden extra run.

## One aggregate budget

**1,500 seconds total** includes train, final fit, Runtime P10. Planned train
maximum 1,200s; final fit maximum 120s; P10 reserve 120s; 60s slack remains.
Launcher reserves 240s before training (fit + P10), 120s before final fit,
subtracts actual previous process time, and leaves a one-second admission margin.
TERM at cap minus 10s, KILL at cap; group cleanup time counts, and overruns fail.
Signals latch without asynchronous exceptions; whole-group absence is required
before successful release. No invocation per job can be repeated automatically.
Unresolved history stays blocked rather than guessed away.

P10: **720 decisions = 624 dev + 96 D3**, batch 4/four threads, no startup
or canary decisions. Parent supplies the Runtime reservation and immutable
commands/input bindings at actual scheduling; this template does not schedule it.

Resource limits remain **8 GiB RSS and 8 GiB MPS driver separately**, with at
least **2 GiB recommended headroom**. Never add RSS and driver as a memory total.
In-process existing guards own headroom/driver/lifetime checks; external sampled
per-process RSS is supplemental, not continuous peak measurement. Resource,
identity, time, incomplete-run or group-absence failures mean stop, not rescue.

## Preparation verification and remaining work

Only stdlib source/JSON parsing and small evidence hashing are permitted here;
no native/project imports, weights/tokenizers decoding, forwards, tests, lint,
dependency installation or scoring/schedule replay. Owner package build passed; this is not ML
verification. Parent still owns integration, independent review, actual freeze,
ML authorization/serialization, output pinning, final-fit statistics, P10 and
aggregate return accounting. No main merge/reset belongs to this preparation.
