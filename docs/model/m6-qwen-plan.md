# M6: one fixed Qwen decision-learning contrast

Lead authorized R5's primary supervised recipe, not its temperature alternative. M6 adapts the preserved P3 Qwen control on existing TRAIN decisions; Runtime P4 owns the sole trained-development pass, and Evaluation E6 scores independently. This is a combined learning recipe, **not** an architecture or permutation-only ablation. No automatic promotion.

## Pre-outcome records

Artifact root `R=/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/`:

- `comparison-freeze.json`, SHA256 `5c24a089e3cb4025fb9fcdf4e10effb838d3fb7394eab96493d41b8598908e10`: starting-control tolerance, exact E6 inputs, prior P3 outputs and base assets, frozen before the new control run.
- `train-audit/audit.json` and `train-audit/schedule.jsonl`: full TRAIN-only input/boundary audit, clean source/runtime/config/asset identities and materialized schedule. Schedule SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`.
- `full-run-freeze.json`, SHA256 `13f2e6f88f6e99323645a748ecaffdc7aa709cc43cb19fb35fd6a63e435b9ed9`: source/recipe/schedule/guard/capacity/control bindings before full training. This document describes those earlier immutable records; it is not a substitute retroactive preregistration.
- Execution source `dafd5d235b53af341fbf539e4bf32dcf09a399f2`; [fixed config](../../configs/model/m6-qwen.json). Full source hash inventory is in the audit. No source/worktree update during the active run.
- E6 plan `artifacts/evaluation/e6-predeclared-v1/plan.md`, SHA256 `7b99168342b23cdec9685a357f9aef88c917e88cc4506dd109b1b0690d52928d`, fixes interpretation before M6/P4 outcomes.

## Fixed data, rendering and optimization

- Exact released v2 manifest `artifacts/data/data-pilot-v2/manifest.json`, SHA256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`. Only TRAIN shards are opened: **1,500 unique decisions /880 declared groups**,500 each intent/sentiment/rule_application. Whole-manifest path/split checks precede any shard read; training labels/provenance/never-train markers retain independent validation. Declared groups are not necessarily independent sources.
- One `random.Random(42)` row shuffle, then one option shuffle per row. Each target is remapped by stable option ID. All1,500 rendered decisions, option identities, target positions and prompt/answer tokens are materialized and hashed; capacity/full execution rederive and compare them exactly. No epoch-time resampling, filtering, all-permutation expansion or held-out examples.
- P3 base `Qwen/Qwen2.5-0.5B-Instruct@7ae557604adf67be50417f59c2c2f167def9a775`; existing local pinned assets, safe loading, no remote code/network download. Initial asset hashes match preserved P3 audit.
- Reuse Runtime's unchanged `prepare` and SYSTEM/USER template, official chat template, A–F complete assistant-boundary tokens, T1 conditional probabilities, cap1024 with **no truncation**, FP32/MPS/SDPA, microbatch1, fourCPUthreads, `use_cache=False`, `logits_to_keep=1`. Labels/IDs/metadata never enter rendered text.
- Full-parameter AdamW LR2e-5, betas(.9,.999), epsilon1e-8, weight decay.01, no scheduler. Grouped CE over allowed answer-symbol logits, divided by accumulation4; finite gradient norm/clipping1 once per update. `foreach=False` fixes the conservative optimizer/clipping allocation implementation before execution.
- Exactly one epoch /1,500 presentations /375updates;494,032,768 trainable parameters across290unique tensors. No full-vocabulary/rationale objective, new data, temperature fit, LoRA, dependency change, validation-based checkpoint selection, fallback or sweep. Preserve final weights only.

## Measured feasibility and reset

Full TRAIN audit passed all1,500 prompt/boundary checks:89–220tokens, p50=127/p95=155, zero overflow at1024. The capacity process used the four longest scheduled TRAIN rows for **one disposable update**, then four extra backwards with Adam moments resident, without a second optimizer step. No capacity weights were saved; the process exited and all its model/optimizer/RNG state was discarded.

External capacity wall8.922s. Theoretical FP32 weights+gradients+two moments7,904,524,288B excludes activations/copies/workspaces. Actual observed CPU lifetimeRSS2,898,182,144B; MPSdriver maximum10,191,831,040B/current8,730,074,368B; minimum sampled recommended-working-set headroom8,877,834,240B. CPU and MPS measurements are **not additive**, and samples are **not device/unified-memory peaks**.

Frozen guards: CPU lifetimeRSS≤16GiB; sampled MPSdriver≤16GiB; at least2GiB below reported recommended working set when available. No allocator/backend override or MPS fallback. Capacity cap600s; sole full process cap2700s including validation, fits and save. The external supervisor sends TERM10s before the cap, then KILL at the cap if needed; cooperative phase/row checks cannot interrupt blocked native operations. Preserve any abort; no automatic retry or alternative parameter recipe.

Conservative capacity projection2100.338s includes375copies of the slower longest-row update estimate,3,000copies of the slowest observed capacity-eval forward and120s save allowance. It is an estimate, not measured full-run runtime or a guarantee. Full training separately reloads the original pinned bytes, initializes a new empty optimizer, and seeds Python/CPU/MPS RNG42. Its375updates do **not** include the disposable capacity update.

## Control, train fit and interpretation

Model's fresh624 starting predictions are byte-identical to preserved P3: max per-option difference0.0, no changed top sets or ties under the predeclared1e-6absolute tolerance. Semantic/rendering/config/base identities are separately bound; tolerance alone is not comparability. One fresh control process38.361s, all624complete; no labels needed for comparison. Evidence: `starting/`, `control-audit/`, `starting-comparison.json`, process receipts and `compare-start.py`.

Before and after learning, evaluate the **same fixed1,500TRAIN schedule** in eval/no-grad mode. Persist per-row grouped CE/agreement/target and predicted positions, overall/family/source-group summaries, and changing-weight online loss separately. These are training-fit evidence, not held-out performance. Poor fit leaves capacity/optimization/supervision unresolved; good fit plus poor development behavior indicates a transfer mismatch without identifying a cause. MPS metadata/seeding does not guarantee bitwise deterministic training.

P4 alone performs fresh-process final-checkpoint inference on E6's exact300original+300reversed+24already-paired probes. No separate inherited/new inference, extra probe reversal or D3 addition; Qwen had no P3 D3 baseline. E6 owns both-order inherited/new NLL/Brier, new-rule flips and both-order correctness, intent/probe/family/source retention/regressions. Fewer flips while consistently wrong is not rule learning. Better probability scores without rankings are not general reasoning. Reused development groups, correlated constructions and teacher/rule-label limitations remain; no new composite promotion score, significance or calibration claim.

## Reload contract and resources

Self-contained `training/checkpoint/` stores safe FP32 HF weights/config/generation_config and **byte-copied original tokenizer assets**, not reserialized tokenizer output. Sibling `checkpoint-manifest.json` uses agreed `jeff.qwen-trained-checkpoint.v1` flat fields: completed trained identity, original base lineage, exact training source/data/recipe/schedule/P3 pins, tokenizer hashes and full relative file inventory. It hashes a finalized source-run receipt; the receipt does not hash the manifest, avoiding a cycle. Failed/partial runs must not publish a complete manifest. This is inference-reloadable, not an optimizer-resumable training checkpoint.

All prior checkpoints/releases/failures remain immutable. Model schedules through P4 return; ready M6/P4 outrank the separately authorized lower-priority frozen R6 diagnostic, without preemption or concurrent substantial loads. £0additionalactual/pending/allocation. No tests/lint, protected final access, paid service, upload, rootdependency or production-default change.
