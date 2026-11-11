# M8 readiness: six-row learning, ordinary untied HF export

**Assessment only — no implementation or ML grant.** Model and Runtime inspected repository/installed-library source and small configuration metadata within the 18:47–19:12 UTC window on 2026-11-11. No model, tokenizer or weight load, numerical experiment, dependency change or production code was performed. M6/M7 and the immutable Fable snapshot remain untouched; E7 finishes independently.

**Recommendation:** retain R7's independent six-row training head, then export it through an explicitly **untied, full-vocabulary HF output projection**. Installed Transformers 4.57.6 supports this representation with the existing Qwen loader/scorer. It avoids a second inference backend, but is **not yet an executed compatibility or equivalence result**. Runtime's source concurrence is mailbox `350555e3-7cb5-4d3b-a3b0-75ad6aa654a3`; final note confirmation is recorded in the delivery handoff.

## Exact parameter and readout identity

- Load original pinned P3 with its original tied configuration and strict loading diagnostics, never M6/M7 weights. Freeze **all 494,032,768 original parameters**, including input embeddings, every transformer layer, final normalization and the shared original output table. Keep them outside the optimizer and decay; record the fixed buffers/configuration too.
- Independently clone the actual six A–F output rows into one bias-free FP32 parameter `W6[6,896]` — 5,376 trainable scalars, no shared storage. Do not train a full-vocabulary tensor with gradient masking, remap the vocabulary to six IDs, or write learned rows into the original input table.
- Run the frozen backbone in eval mode under `no_grad`, **not inference mode**; its returned final hidden state is already normalized. Apply `W6` outside that context at the last assistant-boundary token. Select only the actual K supplied symbols before CE/softmax, with the ordered token-ID mapping pinned and supported K limited to 2–6. No hidden-state cache or second backbone pass.
- Keep the R7/M7 data, exact materialized row/option schedule, seed and nominal optimizer recipe: AdamW2e-6, decay .01, clip1, microbatch1/accum4, 375 updates, one epoch. One six-row optimizer parameter retains ordinary decay/moment behavior even on rows unused by a particular K. Equal LR/clip does not equalize optimization geometry with full-parameter M7.

## Export and stock reload

After learning, clone the original **entire** output table into independently allocated FP32 `Wfull[151936,896]`; replace exactly the six pinned rows with `W6`. All non-answer output rows retain original values. Set saved `tie_word_embeddings=false` and install the independent bias-free output module. Original input embeddings/backbone/norm remain unchanged. Save a self-contained, unsharded safe HF directory with both `model.embed_tokens.weight` and `lm_head.weight`, original tokenizer bytes and explicit export provenance. `safe_serialization=True` does not itself convert tensors to FP32.

Stock `AutoModelForCausalLM.from_pretrained` can then load the artifact and reuse the existing FP32/MPS/SDPA, `use_cache=False`, `logits_to_keep=1` path: full-vocabulary last-token projection, followed by existing allowed-ID selection and conditional T1 softmax. This is an artifact representation change for the **same treatment**, not another trained arm or a generation-quality claim.

**Fail-closed hazards:**

1. Flipping the config flag alone does not break a live alias. HF save deduplicates actual shared storage; a missing independent head can subsequently be randomly initialized with a warning. Do not load the original tied checkpoint with an untied override and assume a full head was restored.
2. Require both serialized tensors, full shapes, FP32/no bias, zero missing/unexpected/mismatched/error loading diagnostics, saved/reloaded false tie flag and disjoint input/output storage. Do not merely compare Python object identity or rely on file hashes and warnings.
3. `_tied_weights_keys=["lm_head.weight"]` is not an unconditional deletion rule: with genuinely independent storage, both tensors survive safe saving. No library subclass or override is indicated by this source review.

## Small explicit contract extension

The existing P4/P5 flat inventory and stock loader could accept this full HF artifact already, but their identity checks **do not establish frozen scope or correct untied export**. Propose **`jeff.qwen-trained-checkpoint.v2`**, with mandatory `adaptation_kind: frozen-base-six-row-readout` and `representation: hf-untied-full-vocab`, preserving v1 unchanged. Old readers reject v2 rather than silently ignore its semantics; v2 rejects missing proof or unknown representations, without downgrade. Reuse the existing validator's paths, hashes, inventory, tokenizer and scoring checks; add:

- representation/adaptation kind; original base-file pins; ordered six token IDs; H/V, dtype, no-bias and untied flag; controlled HF-config differences;
- a hashed Model scope/export/binding receipt: original materialized FP32 tensor identities, frozen before/after identities, exact six learned rows and unchanged non-answer output rows;
- Runtime's strict load diagnostics, actual tensor/config/nonaliasing checks and reloaded identities, recorded in the audit/inference receipts with new source pins. These check current tensors against bound Model evidence, not independently attest historical training.

Preserve P3 scoring-config bytes, original tokenizer/template, label-free datasets, decision-output schema, final624 population and Runtime's existing guards/supervisor. New trained weights/config/manifest, implementation/audit hashes and treatment provenance must be distinct. No sidecar is silently added to the HF directory or hashed while ignored. Exact field spelling/schema version needs explicit implementation authority and joint agreement before execution; this note adopts no production contract.

## Verification required in a future grant

**Before updates:** hash the loaded original FP32 parameters/fixed buffers and record optimizer membership, frozen flags and head/base nonaliasing. Bind the existing 1,500-row TRAIN pre-fit to M7's saved original-base logits/probabilities and token/option identities. Retain R7's proposed fixed tolerances, max absolute1e-4 logits/1e-6 conditional probabilities plus identical top sets and complete finite coverage. Six-row and full-V GEMMs are algebraically equal, not guaranteed numerically identical on MPS. A failed binding stops before learning; no tolerance relaxation or rescue.

**After updates/export:** recheck all frozen tensors, learned-row placement and every non-answer output row against the original FP32 materialization. Original BF16 file hashes alone cannot prove this across conversion/export. Compare the six-row projection with the **actual exported bias-free `lm_head(hidden[:, -1:, :])` module**, using stock-shaped `[1,1,H]` FP32 input on the matching backend, from the same newly computed hidden states in the existing final TRAIN fit. A different-rank matrix multiply is not this stock-projection binding. Compare logits, actual-K probabilities and top sets under the same fixed numerical limits. This adds projection work, **not another transformer forward**, and must be explicitly frozen/budgeted before learning in the future authorization. Initial agreement alone does not prove final agreement.

**Fresh reload:** verify the actual saved/reloaded config, tensor identities, shapes and storage separation, not just producer metadata. Matching outputs may be compared only where the future authorized execution already produces them. Component equivalence plus exact reloaded tensor identity supports the representation, but is not a measured full small-head-versus-stock comparison on every development input. No additional numeric TRAIN-reload canary is required for this readiness conclusion. If a future claim needs one, predeclare their fixed TRAIN-only identities/count/thresholds and obtain a bounded explicit allowance; do not invent another TRAIN/dev pass, reuse evaluation cases for training, or conceal the comparison gap. The usual three Runtime startup forwards also require an explicit future budget. No extra forward, capacity probe or checkpoint is authorized now.

## Compared with independent base + small-head storage

| Route | Reuse and cost | Limitation |
| --- | --- | --- |
| **Untied full HF export (preferred)** | Same stock loader/full-V scorer; small semantic-validator/load-check extension. About2.521GB FP32 weight payload, plus headers/assets. | Adds544,538,624B (519.3125MiB) versus the tied FP32 base; full-V projection remains. Requires real independent storage and export/reload proof. |
| Base + separate six-row tensor | Head is21,504B; can reference the existing roughly0.99GB BF16 base on disk, widened to about1.976GB FP32 when loaded. | Needs explicit base/head reconstruction, token mapping and a maintained six-row readout branch. Existing Runtime would otherwise reject the extra file or silently score only the base. Viable for compact storage, not the smallest Runtime delta. |

The six-row weight/gradient/two-moment payload is86,016B, excluding framework/state overhead. The full frozen base remains necessary in both routes. Added export-table allocation, CPU/device transfers, serialization and allocator retention create uncertain transients; avoid an unnecessary full-model deepcopy. These are byte arithmetic, **not measured RSS/MPS peaks**. Do not sum overlapping CPU and accelerator scopes or claim a speedup; retain proposed45min/16GiB/≥2GiB-headroom training guards and existing8GiB/≤310s Runtime limits, subject to future measured acceptance.

**Revised effort estimate:** Model training/export/scope proof about1–2 engineering hours; Runtime semantic-validator/load/audit changes about0.5–1 hour; joint binding/review about0.5 hour: **roughly2–3.5 person-hours**, potentially overlapping, not a promised elapsed time or measured saving. Separate-head storage remains roughlyR7's2–4-hour estimate with more Runtime maintenance; neither route is a config-only switch. Future train/fit/export roughly3–7min plus validation/I/O uncertainty; one624 stock inference pass anchored by P5's39.07s, not a forecast guarantee. No new dependency/framework is evidently necessary; £0 additional actual/pending/allocated. Implementation and every execution still require new authority.

## Source evidence

Installed `transformers/models/qwen2/modeling_qwen2.py:395–415,449–463` (normalized hidden state, head construction/projection); `modeling_utils.py:1863–1880,2986–3021,3113–3118,3900–3928,4021–4089,4966–4974,5064–5065,5853–5895` (accessors, tying, safe saving, load/init hazards). Repository `src/jeff/runtime/qwen_{challenger,checkpoint}.py` and `src/jeff/training/qwen_decision.py` establish the current inference and full-parameter-training boundaries. Dimensions/tie/dtype come from the original P3 `config.json`, not decoded weights. Runtime's bounded supporting reviews are `artifacts/release/m8-readiness-20261111-1848/{hf-source-review.md,runtime-interface-review.md}`. This resolves a source-level packaging blocker, not scientific efficacy, native numerical correctness or executed portability.
