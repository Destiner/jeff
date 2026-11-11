# M6: full-parameter Qwen decision-learning result

## Result: the fixed recipe failed to improve TRAIN fit

The one authorized run completed **1,500 presentations /375updates** and saved final weights. But deterministic same-schedule TRAIN agreement fell **805→431/1,500** and grouped CE worsened **1.357724→1.390592**. Every post-fit recorded argmax is position0. This is a degenerate outcome, not successful learning; lower online loss or two family CE improvements do not override the overall/intent regression. No retry, sweep, alternative temperature fitting, best-checkpoint selection or default promotion.

[Plan and immutable pre-outcome freezes](m6-qwen-plan.md) · [Compact run/evidence index](m6-qwen-run.json).

| Fixed TRAIN slice | Start agreement | Final agreement | Start grouped CE | Final grouped CE |
| --- | ---: | ---: | ---: | ---: |
| Overall |805/1500|431/1500|1.357723629|1.390592028|
| Intent |442/500|140/500|.396152925|1.391937832|
| Sentiment |179/500|137/500|2.019891845|1.444125607|
| Rule application |184/500|154/500|1.657126115|1.335712646|

The unchanged materialized schedule has431targets in position0, explaining final agreement exactly. Starting predicted-position counts0…5 are417/384/411/278/7/3; final counts1500/0/0/0/0/0. TRAIN-fit rows record argmax, not ties or complete probability vectors; this alone does **not** establish a unique first-option preference in every case. E6/P4 supplies independent full development probabilities and tie/order observations.

Fit is eval/no-grad on the same seeded TRAIN presentations before and after learning, with per-row CE/agreement/positions and overall/family/all880declared-source-group summaries. It is not held-out evidence. Online changing-weight mean CE1.400337771 is descriptive and not interchangeable with either fixed-snapshot fit. A fresh read-only reviewer independently replayed the schedule and all fit buckets without finding an identity, remapping, aggregation or update-accounting discrepancy. That validates the observed failure, **not its optimization/supervision/representation cause**.

## Executed intervention and control

Clean execution source `dafd5d235b53af341fbf539e4bf32dcf09a399f2`; full source/runtime/asset/config identity persisted. Frozen v2 TRAIN only:1,500unique decisions/880declared groups,500per family, one seed42 row/option shuffle with stable target-ID remapping. All prompts89–220tokens; complete P3 assistant-boundary checks, unchanged cap1024/no truncation. Whole-manifest final/split/path checks precede TRAIN-only shard reads; no D3, development/probe/reference or final data enters learning.

Full494,032,768parameter FP32/MPS AdamW2e-5, betas(.9,.999),epsilon1e-8,decay.01,clip1, microbatch1/accum4,oneepoch,no scheduler. Reused original P3 prompt/template/conditional-symbol readout,T1,SDPA,fourthreads,no cache,last-token projection. It is one combined recipe, not a controlled proof of permutation or architecture effects. No chat/generation preservation claim.

Fresh starting predictions cover E6's exact300original+300reversed+24already-paired probes and are **byte-identical** to retained P3. Predeclared1e-6absolute tolerance was frozen before comparison; observed maxdelta0.0, unchanged top sets/ties. Base/rendering/config/runtime semantics are bound separately. The initial prediction process took38.361s; no repeated baseline run or label-based comparison.

Capacity was a separately accounted fresh process:one disposable update on four longest TRAIN prompts, then four resident-moment backwards with no second update. Its state was discarded on exit. Full training freshly reloaded original pinned bytes and seeded Python/CPU/MPS42 with a new empty optimizer. Recorded full execution has1,500backwards,375clips/steps,no extra backwards and final Adam step375on all290unique parameter states. Three bounded selected parameter fingerprints changed; no claim that this is an independent tensor-by-tensor decode.

## Final checkpoint and actual costs

Run root `R=/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/`:

- `training/checkpoint/`: nine flat HF files, safe FP32weights/config/generation_config, original fourtokenizer files byte-copied, LICENSE/README. No pickle, cache, symlink or training rows inside the HF directory.
- `training/checkpoint-manifest.json`: agreed complete flat `jeff.qwen-trained-checkpoint.v1`; SHA256 `1fe8f6d169301c76698b78b8d7b067c4b10868fb755324896352d1f61310960f`. Distinguishes trained weights from original pinned lineage; hashes finalized source-run receipt without a cycle.
- `model.safetensors`:1,976,163,472B, SHA256 `ecbeb36556281cf00e9175603aecefd83f2ce3fc8a610e4b2cf056b7a4a926fb`. Nine-file inventory checked independently with one streaming trained-weight hash pass; no reviewer model load.
- `training/receipt.json`, `fit-before.jsonl`, `fit-after.jsonl`, `online.jsonl`, `events.jsonl`: exact counters, fit/positions/groups, optimizer/provenance and phase/resource records.
- `train-process.json`, `train-invocation.json`, `full-run-freeze.json`, `capacity/`, `train-audit/`, `starting/`, reviews: complete separation of disposable capacity, initial control and actual learning. Historical artifacts and failed-receipt sentinels remain preserved; successful completed receipts disambiguate sentinels.

Full process ran15:48:30.395–16:01:26.478UTC, **776.083s**,exit0/no timeout, including preflight/load/bothfits/learning/save. Capacity external8.922s is additional, not an uncounted training update. Both fit measurements and save are included in the2700s scheduled full-process cap.

CPU lifetimeRSS3,371,466,752B; maximum observed MPSdriver11,852,775,424B/current8,740,772,096B; minimum sampled recommended headroom7,216,889,856B. All frozen16GiB RSS/driver and≥2GiB recommended-headroom guards held. These measurements are **not additive or actual device/unified-memory peaks**. No allocator overrides, fallback or paid resource. Source matching/seeding is not proof of bitwise deterministic MPS learning or continuous authenticated monitoring.

## Independent handoff and limits

Runtime P4 accepted the actual completed manifest/tokenizer/inventory and completed the sole fresh-process trained624development pass, exit0 in40.527824s (16:10:46.886945–16:11:27.420722UTC). All624presentations/2390option probabilities have valid coverage; Model matched the published three output hashes/counts, checked completed receipts/process exit and accepted the slot return. Model did not duplicate final inference. Evidence: `artifacts/release/p4-m6-20261111-01/{audit/audit.json,run/receipt.json,process-receipt.json,output-validation.json,delivery-summary.json}`. The short producer IDs `training`/`training-checkpoint` are qualified by exact manifest path/hash, not treated as globally unique identity.

Actual local HF load.709607s/full-pass36.818456s/16.948022decisions/s. Runtime reports CPU lifetimeRSS554,598,400B, macOS peak process footprint3,143,828,608B and observed MPSdriver2,777,350,144B: different overlapping scopes, not additive or accelerator peaks. Fresh process/cache and offline flags are not a cold-OS-cache benchmark or network-denial attestation. Runtime success proves saved-checkpoint execution, not learning success or a memory advantage.

Evaluation E6 interprets both orders and source/family/probe regressions independently under its pre-outcome plan. TRAIN fit cannot substitute for those results or establish general rule-transfer failure by itself.

The full learning allocation is exhausted. Keep the negative final checkpoint, original P3 and all prior encoder candidates. Any causal diagnosis, new objective, LR/epoch change or fallback needs its own authorization; this failure does not reject every decoder or supervised-learning approach. £0additional actual/pending/allocation. No software tests/lint, dependencies, final access, external uploads or production/default migration.
