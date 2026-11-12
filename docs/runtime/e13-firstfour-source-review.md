# First-four E13 source review

Source-only; no native approval. No project imports/execution, ML/tokenizer/weight reads, tests, lint, network, build or commit. NLI untouched. Requested lead revision `1345de7c` is not resolvable in this checkout; HEAD observed `a70fdd8`.

## Small fixes

- E13 Qwen and encoder require typed integer 200 rows per orientation and K2 decisions, rather than permitting undersized runs.
- Encoder requires native then reversed suite order; coverage therefore derives 400 decisions, 100 native batch calls, 800 pairs and zero startup calls. Qwen derives 403 forwards including three startup calls.
- Encoder source pins now include the runtime package initializer.

## Source observations / remaining blockers

- Frozen helper exports `decode`, type-sensitive recursive `same`, and `CHECKPOINT_FILES`; `_rows` and `_write_batch` signatures match use. Encoder complete-pair precheck uses the existing formatter with truncation disabled, rejects lengths above 256 before scorer use, and native pre-hook compares attention-mask lengths to complete lengths. Existing scorer retains longest-first truncation. This is source evidence, not observed zero discard.
- M4 baseline inventory is `checkpoints["msmarco-baseline"].files` (list); M9 plan exposes `checkpoint_files` (mapping). Adapter handles those actual metadata formats. No checkpoint weights read during review.
- Input path allowlisting is NOT enforced by these adapters: hashes authenticate supplied descriptors, not the four exact approved source paths. Parent must bind/verify the four exact paths under `artifacts/evaluation/e13-exploration-inputs-v1`; review did not list/read that directory or decision bodies. Do not infer sibling authorization from generic safe-path validation.
- Fresh process per predictor remains an external supervision obligation; neither adapter alone attests process freshness.
- Qwen E13 executable/dependency proof is weaker than v2: E13 binds challenger source and Git cleanliness but the explicit dependency hash map is v2-only. Parent must pin dependencies/source tree before execution. Existing dirty shared checkout fails Qwen's clean-tree guard; do not weaken that guard merely to run.
- Qwen preserves original v2 300/300/24 and 627-forward guards, P8 99 and P9 627 caps; E13-only branch derives 403. No native old-profile regression verification performed.
- Both retain separate RSS/driver 8 GiB limits and recommended-minus-driver >=2 GiB guard. Encoder cooperative deadline does not replace parent's whole-process supervisor.

## Metadata pins verified by byte hashing

- Original P3 download manifest: `7741a686ef6f0cc211438961223fb089e5f3a62da17c582cca27b021ce6191b5` (Qwen also requires original retained path and inventory equality).
- Frozen P10 helper: `c5f57f0a767df16ec57ab4b2dad50616bbfe8b9f1cad43b8c9b0511897bcb3b2`.
- M9 checkpoint plan: `3052ba633d1b8093a2d9074388268c2714bacc6dca3cccb09284345154fabee4`.
- M7 manifest constant is `70163c8567781bb7151b11c125999ea4bc6ec1ff52af52c52a205f9f4dbdd022`; its actual bytes were not independently rehashed in this bounded review.

Older preparation docs describing 1..200 rows are superseded for the reviewed first-four path by exact 200+200/K2 checks. M10/M12 and M11 are not prerequisites for first-four execution.
