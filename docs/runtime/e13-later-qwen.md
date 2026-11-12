# E13 later Qwen exploration preparation

Source-only preparation on `490277d`, within the lead `9aeea4da` late-exploration preparation scope. This is not an execution grant; ModelNativeGrant is not yet active.

## Narrow exception

Only the existing `e13.exploration.inputs.v1` profile with candidate `m12` and checkpoint-manifest SHA-256 `a3f6fd327bb52ecef730297eb0abb93f7a5a0d1b83e8fec276209b5ec6faf6a2` can use a v2 checkpoint for E13 exploration. The existing manifest pin is checked before granting the exception. The existing schema requires exactly `e13-native` then `e13-reversed`, 200 rows each, K2, label-free decision inputs, and hashed release/pair-map descriptors. Prediction accounts for exactly three existing startup rows plus 400 suite rows: 403 attempted and completed forwards.

M10's existing v1 permission and manifest pin `765d802270b8c0b090e9206c3e52f12e76ea7e224dbb4f07c9cc3c709aa6b15a` are unchanged. No M8 candidate, arbitrary v2 execution profile, confirmation profile, sibling input access, or new schema is added. P8/P9 remain v1-only; ordinary v2 remains fixed to 300/300/24 suite rows and 627 total forwards (624 scored rows).

## Preserved validation

The exception still goes through `validate_checkpoint` and the existing strict `qwen_readout.validate_metadata` chain, including the producer's fixed 4500 backbone-call counters. All existing v2 branches remain active: answer-token checks, frozen executable/audit identity, four empty HF loading diagnostic lists, CPU untied-storage proof, loaded MPS tensor/storage identities, readout proof, dtype/device checks, memory/headroom/deadline guards, and bounded forward accounting. No model, scorer, prompt, backend, metadata validator, or tensor-proof code changes.

## Evidence and remaining gates

Only source inspection, a Python standard-library AST parse, and diff review were performed. No project/ML imports, tokenizer, weights, inference, tests, lint, network, build, or commit were run. This establishes source syntax only, not runtime behavior or successful reload. Execution still requires Model's named grant, a fresh audit of the final clean/frozen executable sources, and the existing offline validation/proof path. Other owners' NLI/parent work is outside this patch.
