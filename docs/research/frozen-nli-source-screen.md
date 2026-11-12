# R10: one pinned frozen NLI baseline is source-eligible

**The five source/config conditions pass for `MoritzLaurer/roberta-base-zeroshot-v2.0-c` at revision `d825e740e0c59881cf0b0b1481ccf726b6d65341`.** This activates only the lead's conditional P12 preparation path, not an immediate ML slot, measured loading success or quality claim. No substitute model, NLI training or prompt sweep is proposed.

## Eligibility evidence

| Lead condition | Observed public evidence |
| --- | --- |
| ≤150M parameters | Pinned HF API advertises **124,647,170 F16 parameters**. Not independently counted from decoded weights. |
| ≤600MB safetensors download | One `model.safetensors`, **249,318,428bytes**; no shards/index. API/tree agree. |
| Affirmative local model use terms | Pinned **model-card `license: mit`**; `-c` documentation describes commercially friendly training sources. Preserve attribution, available notices and MIT permission text. No standalone LICENSE file; no blanket upstream-title clearance. |
| Existing built-in support/no remote code | Config `RobertaForSequenceClassification`, `model_type=roberta`; native `RobertaTokenizer` config, no `auto_map` or repository Python modules. Actual installed Transformers4.57.6 source contains the native classifier, AutoModel mapping and fast tokenizer. No SentencePiece/new package is needed for this byte-level BPE model. |
| Native class mapping | Config/inverse agree: **0=`entailment`,1=`not_entailment`**. Not a three-way MNLI label order; class1 is not a separately trained contradiction class. |

[Immutable model card](https://huggingface.co/MoritzLaurer/roberta-base-zeroshot-v2.0-c/blob/d825e740e0c59881cf0b0b1481ccf726b6d65341/README.md) · [pinned API with file metadata](https://huggingface.co/api/models/MoritzLaurer/roberta-base-zeroshot-v2.0-c/revision/d825e740e0c59881cf0b0b1481ccf726b6d65341?blobs=true) · [config](https://huggingface.co/MoritzLaurer/roberta-base-zeroshot-v2.0-c/resolve/d825e740e0c59881cf0b0b1481ccf726b6d65341/config.json).

**Weight pin:** `https://huggingface.co/MoritzLaurer/roberta-base-zeroshot-v2.0-c/resolve/d825e740e0c59881cf0b0b1481ccf726b6d65341/model.safetensors`, API-advertised LFS SHA256 **`3568bb04b99e48d6e3086656534304644f3608312aa96c52edca7e6a7eeb0336`**. No weight byte/header/payload was fetched by Research. Runtime must verify downloaded size/hash and actual strict-load structure before scoring.

## Exact asset allowlist

All paths are relative to the same immutable revision's `/resolve/` URL; published sizes are not local full-download verification. Preserve original config/tokenizer bytes and record separate runtime overrides.

| Asset | Published bytes |
| --- | ---: |
| `model.safetensors` |249318428|
| `config.json` |882|
| `tokenizer.json` |2108615|
| `tokenizer_config.json` |1215|
| `special_tokens_map.json` |280|
| `vocab.json` |798293|
| `merges.txt` |456318|
| `README.md` |21113|

Total252,705,144bytes. Do not fetch or load `training_args.bin`, execute repository code, use another weight format/model or upgrade dependencies. Full published Git blob/LFS identifiers and exact URLs are retained in the source ledger; a Git blob ID is not a raw SHA256. The card is the affirmative model-license declaration, not proof every training datum's rights were independently checked. Preserve MoritzLaurer/model-ID/revision/source attribution and supplied notices without inventing a copyright holder/year; the card additionally requests the Laurer et al. paper citation.

The card identifies original RoBERTa plus synthetic Mixtral-written tasks/MNLI/FEVER-NLI for this `-c` variant. Those are publisher provenance/commercial-use statements, not an ancestry audit or a license to substitute the non-`-c` model. No concrete conflicting local-use restriction was found. The card's generic `transformers[sentencepiece]` example is not an instruction to install anything for RoBERTa.

## One rendering, fixed before scores

Profile name: **`r10-context-question-answer-v1`**. For every supplied decision and each native option, construct exactly this Unicode text pair (literal LF newlines; do not strip, normalize or paraphrase the source fields):

```python
premise = "Context:\n" + state + "\n\nQuestion:\n" + question
hypothesis = "The correct answer is:\n" + option_text
```

Keep the `Context:` header even when state is the empty string. Premise is tokenizer sequence1; hypothesis is sequence2. Opaque input/option IDs are used only to join outputs, never embedded in either string. No target, task-family/source metadata, answer letter, chat-role wrapper or demonstration is added. Each option is paired independently with the same state+question; native option order only determines output mapping.

**Reason:** the model natively judges a hypothesis given a premise. A fixed answer assertion exposes short caller-supplied labels, phrases or numeric outputs as candidate answers while retaining the actual question and context. This is a pragmatic QA-to-NLI bridge, **not the model card's topic-classification template** and not known to be optimal. Questions are not ordinary declarative NLI premises; terse labels/numbers may produce unnatural hypotheses. These are limits to report, not permission to select a different prompt after results. No example, model prediction or template variant was scored during selection.

Use the pinned native fast tokenizer configuration (`use_fast=True`, `trust_remote_code=False`, `add_prefix_space=False` as supplied), pair special tokens enabled, no truncation, and complete-pair length cap **512 including special tokens**. Config `max_position_embeddings=514` does not authorize514input tokens. Tokenize/pad complete pairs consistently; record per-case/per-option lengths and all overflow failures. Do not silently clip context, question or hypothesis. If the unchanged624-population cannot fit, stop/report the concrete incompatibility under P12 rather than dropping cases or changing the renderer.

## One fixed readout, not the zero-shot pipeline default

For candidate i's native pair logits z, use exactly the lead's score:

`score_i = z[entailment] − logsumexp(z[all native non-entailment classes])`.

For this binary configuration, **`score_i = z[0] − z[1]`**. Return stable **T1 softmax across the supplied choices**, joined back by their exact option IDs. Do not softmax entailment logits alone, normalize independent sigmoid probabilities, fit a temperature, average prompts or use the pipeline's `multi_label=False` default: those are different readouts. Load/evaluate without labels and use no gradients.

This score is native entailment log-odds, not a calibrated truth probability; cross-choice normalization conditions on the caller's alternatives and forces a distribution even when none is well supported. Independent per-option scoring is mathematically permutation-equivariant, but actual batch/padding/kernel rounding and ties still require measured order/coverage reporting; no exact numerical-invariance guarantee is asserted.

## Runtime and interpretation boundary

Propose fixed **four decisions per batch** (at most24native option pairs for existing K≤6), with only a final partial batch. FP32/MPS, fourthreads, eval/inference mode. Although stored weights/config areF16, the lead requires actual **FP32** loading/execution; native parameter payload is124647170×4=498588680bytes before buffers/activations. This is payload arithmetic, not a memory peak or fit guarantee. No quantization/precision/model fallback.

Runtime owns the smallest explicit fixed-profile adapter and one fresh, strict native load (`trust_remote_code=False`, safetensors only, complete loading diagnostics). Require original revision/config/classifier labels and actual parameter shapes/dtypes to match the bound source; preserve all output issues rather than accepting a randomly initialized head. Preparation is bounded by the lead's60owner-minutes, not by a claim that this is already implemented.

After actual readiness and a **specific Model slot**, the authorized screen is the existing624development decisions /2390candidate-pair scores, **zero startup/canary**, one pass only, ≤8minutes external process,8GiB separate RSS/driver and≥2GiB recommended headroom. M10/M11/D8 priorities remain. Pre-forward harmless plumbing failures may be preserved/refrozen within the granted cap; semantic/resource failures stop; no repeated scores or post-output renderer change. No stock P3/M8 proof needs to assert an arbitrary optimizer history for this unrelated frozen baseline.

Evaluation E14 prospectively compares family/order agreement, proper scores, strict both-order success, exact probe retention, ties/coverage/source contributions against P3/M7/M9 and meaningful baseline context. Architecture, pretraining, task alignment, tokenization,512token budget and log-odds readout all differ: this is a **practical baseline, not a pure architecture ablation or best-possible NLI score**. No promotion, significance/calibration claim or original-final access. D8 exploration and confirmation require their own grants/cohort lock; no automatic admission from source eligibility.

## Evidence, actual work and status

Evidence: `artifacts/research/r10-20261112T011854Z/` contains `model-source.md`, `model-source-ledger.json`, pinned API/tree/card/config/tokenizer metadata, retrieval times and static library-source excerpts. Research also checked the installed4.57.6 RoBERTa/AutoModel/fast-tokenizer source as text, without imports. No tokenizer vocabulary/merges/tokenizer.json or model weights were fetched, and no model/tokenizer was instantiated; only configuration, metadata and documentation were fetched.

The child initially wrote these public evidence files under the session CWD's `Code/artifacts/` rather than the shared Jeff root. Parent copied all14files without overwrite and verified byte equality; `canonical-copy-receipt.json` records both roots and hashes, originals retained. No scientific metadata or weight claim changed. This operational correction is not a model download or an unreported execution.

R10 began01:18:54UTC on2026-11-12 with20-minute cap01:38:54. Source qualification and this **single rendering/readout** are pre-score. Actual loading, token coverage, performance and quality remain Runtime/Evaluation measurements, not Research results. Exact integration/delivery/review/build receipts are in the handoff; night foreground availability continues independently through08:30:36UTC.
