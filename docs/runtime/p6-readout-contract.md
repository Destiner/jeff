# P6: explicit frozen-base readout acceptance

P6 adds `jeff.qwen-trained-checkpoint.v2` to the existing audit/predict path. It is not another inference backend. Historical v1 manifests and no-manifest P3 scoring retain their execution path; v2-only markers cannot be declared as v1. Unknown versions, representations or missing proof fail closed. Implementation/build evidence alone is not executed compatibility or a learning result.

## Artifact and source contract

The existing flat inventory, original tokenizer bytes, original model lineage, source receipt, scoring-config pin and path controls remain mandatory. v2 additionally requires:

- `adaptation_kind: frozen-base-six-row-readout` and `representation: hf-untied-full-vocab`;
- `readout_proof: {path, sha256}` pointing to the regular sibling `jeff.qwen-readout-proof.v1` JSON, outside the HF inventory;
- the exact producer field tree and canonical FP32 records documented in [`src/jeff/training/M8.md`](../../src/jeff/training/M8.md).

`qwen_readout.py` validates original P3 asset/config pins, the exact M7 data/schedule/nominal optimizer recipe, complete original tensor maps, frozen scope, learned-row/export identities, START/FINAL limits, completed source-receipt crosslinks and referenced evidence hashes. It does not read TRAIN row content or independently reconstruct historical optimizer behavior. Near-null movement remains valid: six trainable rows is not a minimum-effect requirement.

Saved config must equal the exact agreed original-to-export transform: untied, FP32, cache disabled, Transformers4.57.6 serialization, disabled sliding-window normalization, null rope scaling and24full-attention layer types. Architecture, vocabulary and tokenizer/scoring semantics do not change. The shared Model-owned `qwen_readout_proof` helper supplies bounded, little-endian FP32 tensor hashing; its source and Runtime validator/header-inspector sources are frozen into audit evidence. v2 also pins the imported Jeff package files and dependency definitions. Git revision/status remain recorded operating context, not scientific equality keys; executable files must still be clean and byte-identical. Historical v1 audit comparisons are unchanged.

The metadata-only `qwen_safetensors.py` reads at most a1MiB header, not decoded weights. It requires the complete original290parameter names plus `lm_head.weight`, exact F32 shapes, both full tables, and nonoverlapping contiguous payload ranges without trailing bytes. The nonpersistent RoPE buffer is checked separately after loading, not expected in serialized state. Whole-file hashes alone do not prove live tensor identity.

## Sole fresh execution

Use the unchanged CLI with `audit --checkpoint-manifest /absolute/checkpoint-manifest.json`, followed by `predict` from its clean frozen revision. Audit hashes files and tokenizes; it does not instantiate a model or decode weights. The shared helper's enclosing Model package imports torch and scorer definitions, so this is not a torch-import-free process. The P6 owner must verify the completed Model process and v2 audit, then obtain Model's single-use compute grant before prediction. No implicit grant follows from an idle machine or successful audit.

Only v2 requests `output_loading_info=True` and requires all four diagnostic lists present and empty, in addition to successful strict shape loading. It inspects actual input/output backing-storage separation on CPU, migrates the stock model to FP32/MPS, then validates its actual config, complete parameter/buffer/state names, serialized geometry and canonical tensor identities. CPU storage uses byte intervals; allocator-owned MPS storage uses distinct opaque Metal buffer handles, rejecting shared-buffer views. MPS handles are not payload addresses, so adding tensor byte lengths to them is invalid. This scoped identity check is not a general proof for arbitrary externally aliased Metal buffers. All frozen-before/after/export records and full/answer/non-answer output records must match. Chunked proof transfers share the execution resource/deadline guards and run before any forward. Receipt fields distinguish loading, storage inspection, proof work and suite timing.

P6 requires the same300original +300reversed +24already-paired presentations, with the existing first3unscored startup rows: **627 attempted and completed model forwards**, no canary or second backbone pass. The existing template, option-ID mapping, conditional T1 softmax, FP32/MPS/SDPA, batch1/four threads, cap1024, no cache and last-token-only projection remain unchanged. Paired probes are not reversed again. Attempt counters increment immediately before the actual model call; failures do not grant a retry.

The owner supervisor bounds each granted execution to TERM at300seconds and KILL after at most10seconds, including imports, repeated evidence validation, loading/proof/startup and scoring. Internal8GiB CPU lifetime-RSS and MPS-driver guards remain separate, with the activation's>=2GiB recommended MPS headroom guard; their scopes overlap and must not be added. MPS observations are samples, not true peaks. Fresh HOME/cache and offline/local-only settings are not OS network denial or fully offline installation.

## Interpretation and failure boundary

Actual reloaded identities plus Model's same-hidden-state FINAL binding support the export representation; they are **not a measured fresh small-head-versus-stock comparison on every development case**. Producer history is attested and source-bound, not independently replayed by Runtime. Evaluation owns held-out quality and promotion conclusions.

No structural/numerical mismatch may be repaired by relaxed tolerances, another representation or extra inference. Preserve failed attempts and source/audit refreezes. Only expressly permitted zero-forward plumbing corrections within the existing grant bound are eligible. Return the slot and send available outputs/coverage, hashes, startup counts, strict-load proofs and process receipts directly to E8; documentation integration is not a scoring gate.

Each independent full FP32 output table adds544,538,624bytes (519.3125MiB); total untied parameter payload is2,520,669,696bytes before headers/assets. These are payload arithmetic, not process peaks. No new dependency, platform, model publication or paid service is introduced.
