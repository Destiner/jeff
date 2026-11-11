# E4 Track A — independent M5 control review

**comparable: true**

Comparable as a recorded single-factor historical control, not independently verified initial tensor arrays or causal proof. All 105 initial torch.save-serialization parameter hash records are compared, not regenerated; checkpoint bytes are CPU-hashed without model loading. Identical starts/predictions do not establish identical stochastic training trajectories. Single-seed MPS/backend variation remains a causal confound. Source equivalence is limited to the ten relevant source/package/lock files, not entire Git commits. No criterion outcome is scored here.

## Verified controls
- Historical source `e37b0f3e7f2e3162abca87a76883eb81300603e0` versus M5 recorded `4031e7e9d371f15a53c3bae9d5db14478ace6fdb`: all ten relevant source/package/lock files rehashed from Git and compared with present Model worktree bytes; recorded four training-source pins checked independently.
- Config differences are exactly scalar-head LR `5e-4 → 2e-5` and output location. Encoder including native pooler remains `2e-5`; full tuning; retained pretrained head; no added max-steps flag.
- Frozen pilot manifest and all six train/validation shards rehashed. Same shard/row order, seed42, seeded shuffle source; reconstructed epoch ID order pins in receipt. No runtime order trace exists, so this is source/data/policy evidence.
- Cap256, batch4, three complete epochs,225updates,900presentations; MPS/four threads; complete recorded environment equal including Torch2.15.0/Transformers4.57.6. AdamW `.01`, betas `(.9,.999)`, epsilon `1e-8` unchanged. Source has no schedule/warmup/clipping.
- Tokenizer saved files byte-equal; checkpoint formatting/scoring metadata equal. Native pooled-CLS/dropout retained, hidden/attention dropout `.1`, classifier dropout null (native fallback); temperature1. All105 initial parameter-record hashes and initial validation record equal. Baseline predictions byte-identical on both frozen inputs.

## Four inference receipt rechecks

| Job | Input SHA256 | Output SHA256 | Inventory SHA256 | Binding / before-after |
|---|---|---|---|---|
| baseline-original | `2ad601da94172ebd5080fbfa67898a911042e61355f2e03e81bc64cb6a380fb1` | `cef650f002f9a7850c9f913b1e1d8dc169cc1b03db4a08ae10fafdf0a4935eb0` | `420f7c94983ecd80ef6706e89390d5b39575b50c47de893a8cec8d609e5d0260` | pass |
| baseline-probes | `051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6` | `263276ab7578cf62a363b6e4aec8f7510f532d30840b84d5cfc1cdb8bf12ef95` | `420f7c94983ecd80ef6706e89390d5b39575b50c47de893a8cec8d609e5d0260` | pass |
| checkpoint-original | `2ad601da94172ebd5080fbfa67898a911042e61355f2e03e81bc64cb6a380fb1` | `ebf50035eae1dcd1f45bf503b095ad5382f98a85397a3c4666112a9cfe33f25b` | `49d5e0c2d06213cb705d97a71cc7bbcc015cf0d5ed31579a72e002ec41270d39` | pass |
| checkpoint-probes | `051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6` | `3edaf8e82f00316ef501ea809794006c7cb32c4d346633896e8d05f3a3cb0921` | `49d5e0c2d06213cb705d97a71cc7bbcc015cf0d5ed31579a72e002ec41270d39` | pass |

Receipt JSON contains exact absolute paths, commands, individual file hash/size inventories, record pins, and all105 named initial parameter hash comparisons. The original driver and pre-invocation/complete receipts agree. Its historical before/after equality is recorded evidence; current review separately hashes each checkpoint inventory before/after each receipt check without loading a model. A current rehash cannot independently reconstruct what a past process read.

## Frozen criterion and errors
- Criterion unchanged: `/Users/destiner/Code/jeff/artifacts/evaluation/e4-m5-preregister-v1/criterion.json` SHA256 `a74b9ebf2cd7f52a0367422d7ca9db489154c7060516be2ca768e40f23e709c6`. Owner scoring is separate and concurrent; no new thresholds or outcome decision supplied.
- Errors: none.

## Boundary
Only this new exclusive artifact directory was written. No tracked changes, ML/model loads, tests, lint, builds, final-data reads, merge, or spending. This is an artifact-integrity/control review, not a software test suite.
