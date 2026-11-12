# E13 exploration — source preparation only

Lead d02118e6 permits minimal source preparation, not native execution. Actual Data release and native execution grant remain pending. No audit, tokenization, weight access or inference was performed for this change. This is not a ready-to-run handoff.

Template: `configs/runtime/e13-exploration-inputs-v1.template.json`. Nulls intentionally fail validation; replace only after the actual release arrives. Exact top-level fields are shown in the template. `candidate` is one of `p3`, `m7`, `m10`, `m12`; no arbitrary checkpoint or M8. `release` and `pair_map` are existing-file `{path, sha256}` descriptors, bound into audit evidence and rehashed on prediction. Their contents are not prompts; metadata semantic approval remains Data/lead-owned.

Datasets must be exactly `e13-native`, then `e13-reversed`, with the existing `{name,path,sha256,rows}` fields. Counts must equal actual file rows, be equal positive integers at most 200 each, and total at least three existing rows for startup. Decision rows retain only `schema_version,id,state,question,options`; option fields remain `id,text`. Labels, raw family fields and metadata are prohibited. The manifest marker `validation_only_never_train` must be literal true. Final/reference paths, symlink paths and parent traversal are rejected for E13 inputs, metadata and candidate paths.

Use the unchanged original P3 scoring config: cap 1024, FP32/MPS/SDPA, T=1, cache disabled, same render. P3 requires its original retained download/model directory and pinned download manifest; all asset hashes must match that manifest. M7/M10/M12 require their exact pinned manifest hashes and the existing strict checkpoint validator, including all inventory/provenance checks. V2 remains disallowed for execution profiles.

The existing audit/predict path is reused. Only this profile derives its forward maximum from `3 + sum(actual suite rows)`; exact suite names/counts and three startup forwards remain enforced. P8/P9 and the v2 300/300/24, 627-forward checks are unchanged.

Blockers: actual Data release/pair map and hashes, actual label-free files/counts, explicit native execution authority, and later authorized audit/runtime validation. No tests, lint, build, imports, tokenizer, model execution, network or commit were performed.
