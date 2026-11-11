# Backbone decision: start small, preserve a useful baseline

Research task `research-backbone-20261111`, opened 2026-11-11 10:19 UTC. Initial recommendation prepared by 10:25 UTC against contracts v0.1 and committed main `1bf5236`. Initial scope: documentation/source research; no model weights downloaded or executed. Three read-only subagents covered model suitability, backend/memory, and data/evaluation independently. Subsequent CPU data/prediction analysis and Model-reported local evidence are separated in [the follow-up](follow-up.md); neither recommended checkpoint was run by Research.

## Decision for Model

**Start: `cross-encoder/ms-marco-MiniLM-L6-v2`, full fine-tuning on PyTorch MPS in FP32, preserving the pretrained scalar ranking head. Fallback: `Qwen/Qwen2.5-0.5B-Instruct`, frozen base plus rank-8 LoRA on `q_proj`/`v_proj`.** No cloud or paid work is needed to establish the initial loop.

The exact encoder repository name is `MiniLM-L6-v2`, not `MiniLM-L-6-v2`. Its config has a stale `_name_or_path` referring to an L12 model; the actual architecture fields specify **six** layers. Pin the repository revision rather than interpreting that legacy string as the model identity. [E1–E3]

Model's 10:19 dependency handoff provisionally selected `sentence-transformers/all-MiniLM-L6-v2` plus a new scalar head. **Do not stop an already working implementation or run.** If selection is still cheap, the cross-encoder retains a useful trained ranking head. If not, ship the existing loop and identify its initial new-head baseline as randomly initialized, then request a bounded cross-encoder comparison. Using an embedding checkpoint in a pair scorer is viable, but its embedding training does not pretrain the new correctness head. [A1]

### First implementation, without waiting for more research

1. For each choice, tokenize a genuine text pair: first sequence `State:\n{state}\nQuestion:\n{question}`, second sequence `{option.text}`. No IDs, labels, task family, or provenance enter the input.
2. Obtain raw scalar logits with `AutoModelForSequenceClassification`; keep the supplied head. For one example, `p = softmax(candidate_logits)` and loss is `-log(p[target_index])`. **Do not pass target indices as the model's built-in `labels`: its one-output configuration can select regression loss.** Compute grouped cross-entropy externally. Mask padded candidate slots if batching variable choice counts.
3. Begin with one complete decision (2–6 pairs) per microbatch, at most 256 combined tokens per pair, accumulating four decisions before an optimizer step. These are proposals, not measured optimal settings. Preserve question and candidate before truncating state; report overflow rather than silently dropping a decisive rule. The architecture limit is 512 including special tokens. [E2–E3]
4. First supervised recipe: full-model AdamW, proposed learning rate `2e-5`, one pilot epoch, fixed seed; preserve the pre-update baseline and the first usable checkpoint. Leave subsequent schedules/epoch selection to Model and validation evidence.
5. During Model's authorized real run, record finite loss, actual device/dtype, synchronized time, allocator/driver memory, truncation counts, saved checkpoint and fresh-process predictions. Score untouched and trained predictions on identical validation cases. No research-owned ML job is requested.

**Measured implementation update:** the approved all-MiniLM pilot should use the existing `--max-length 256`, for both untouched baseline and training. Research's CPU token audit found that 128 removes question tokens from **12/20 rule-validation decisions**; all 1,412 pilot candidate pairs fit at 256. This is a preprocessing finding, not an accuracy comparison. See [follow-up evidence](follow-up.md).

## Comparison

| | Starting encoder candidate scorer | Decoder fallback |
| --- | --- | --- |
| Exact backbone | `cross-encoder/ms-marco-MiniLM-L6-v2` | `Qwen/Qwen2.5-0.5B-Instruct` |
| Observed revision | `233902d25c440f23af6f7d6e94d2946bac0bee0a` | `7ae557604adf67be50417f59c2c2f167def9a775` |
| Parameters / architecture | ~22.7M; six-layer BERT-compatible sequence classifier, 384 hidden, one scalar | ~494M; 24-layer Qwen2 causal LM, 896 hidden, grouped-query attention |
| Existing skill | MS MARCO query–passage relevance ranking; pretrained scalar head | Instruction-tuned language modeling; plausible question/choice understanding |
| What is NOT established | Correctness, negation, supplied-rule reasoning, calibrated confidence | Superiority on Jeff, robust rules, calibrated confidence |
| Selected download estimate | ~92 MB: ~90.9 MB FP32 safetensors plus small tokenizer/config assets | ~1.00 GB: ~988 MB BF16 safetensors plus tokenizer/config assets |
| Tokenizer / context | Uncased BERT WordPiece, 30,522 vocabulary; **512 total pair tokens** | Byte-level BPE; model supports **32,768**, despite tokenizer metadata 131,072 and family-level 128K claims; begin at 256–512 |
| License | Card declares Apache-2.0 | Apache-2.0, explicit license file |
| Training strategy | Full fine-tuning; no adapter dependency needed | Frozen base, LoRA rank 8, q/v targets, no training KV cache |
| Scoring | Shared pair logits, softmax across choices | Present all option descriptions with temporary A–F symbols, score allowed assistant continuations, normalize over choices; verify exact boundary tokenization |
| Main risk | Relevance instead of truth; truncation; mistaken default regression objective | Label/order bias; logits memory; backend/dtype compatibility; more integration work |

Primary model evidence: [E1–E5, Q1–Q6]. File sizes and parameter counts come from published repository metadata, not local downloads. Counts/sizes are rounded. We did not measure either checkpoint's Jeff accuracy, throughput, or peak memory. The encoder card reports MRR@10 39.01 on MS MARCO Dev and NDCG@10 74.30 on TREC DL19; these are published retrieval results, not our decision evaluation. Its throughput is V100-based and must not be presented as laptop throughput. [E1]

For the decoder, use the official chat template and keep state in the user/task-data content, not a privileged instruction role. Never feed opaque option IDs; temporary position symbols map back to IDs outside the model. Single-token allowed symbols permit next-token logit scoring and choice-normalized CE. If any symbol is multiple tokens at the real assistant boundary, score complete continuations consistently rather than taking an arbitrary first token. Normalization is conditional on allowed choices, not proof of unconditional answer confidence. Avoid free-generated probability JSON and variable-length option-text likelihood as the initial scorer.

## Apple silicon and dependency request

- Keep Model's requested stack: native ARM64 Python 3.12, `torch>=2.6,<3`, `transformers>=4.48,<5`, `safetensors>=0.4`; **Integrator owns resolution/lock/build**. This is a requested range, not a locally verified combination. Qwen needs Transformers >=4.37; MiniLM needs no Sentence Transformers wrapper. [Q1]
- `torch.backends.mps.is_built()` / `is_available()` and a real forward/backward are owner-run acceptance checks, not proven by the architecture being supported. OS requirements depend on the resolved torch wheel; current stable MPS documentation says macOS 15+, whereas older wheels differ. Record OS, Python architecture, torch and Transformers versions. [B1–B2]
- Start FP32 explicitly. BF16 is not universally unsupported: PyTorch v2.7.1 source gates it to macOS 14+, but operation/backward support still needs verification. Do not blindly use Qwen's BF16 checkpoint metadata as the runtime dtype. [B3]
- Leave `PYTORCH_ENABLE_MPS_FALLBACK` unset initially so unsupported kernels are visible. If Model elects CPU fallback, set it before torch import and report it; it is not an OOM remedy and can reduce performance. Never disable allocator safeguards simply to force a run. [B4]
- Add `peft` only if escalating to the decoder. FP32 frozen Qwen is a reasonable first compatibility probe at this scale. Do not assume CUDA/bitsandbytes recipes imply MPS quantized training support.
- MLX-LM has actual Qwen2 architecture and LoRA/QLoRA support. It is a **backend alternative**, not another initial workstream; its default next-token objective does not implement Jeff's grouped-choice objective automatically. MLX-LM is not a drop-in BERT cross-encoder runtime. [B5–B6]

### Memory: estimates, NOT peak measurements

Decimal units; ordinary FP32 Adam parameter state is weights `4P` + gradients `4P` + two moments `8P` = `16P` bytes. This excludes activations, temporary optimizer buffers, allocator reservations, Python/framework overhead and the OS.

| Configuration | Parameter-state arithmetic |
| --- | ---: |
| Encoder full FP32 Adam, ~22.7M | ~0.363 GB |
| Qwen full FP32 Adam, ~494M | ~7.90 GB — unnecessary first-day risk |
| Frozen Qwen base | ~1.98 GB FP32 or ~0.99 GB FP16/BF16 |
| Qwen rank-8 q/v adapters across 24 layers | 540,672 parameters; ~8.65 MB FP32 Adam state, plus frozen base |

LoRA calculation: `24 × 8 × [(896 + 896) + (896 + 128)]`. Activations still backpropagate through the frozen network. At batch 1, length 512, Qwen's `151,936`-wide vocabulary produces ~297 MiB FP32 logits alone if projected at every token; masking prompt labels does not remove that tensor. Neither table is a fit guarantee. Unified memory is shared with macOS and applications. The Model handoff reports 24 GiB installed locally; **research did not independently measure hardware or MPS availability**. Recommendations must still work conservatively for the 16 GB target.

## Decision gates and data/evaluation

- **Proceed now:** encoder learning/save/reload loop, even if the provisional all-MiniLM implementation is already underway. No dependency on additional research.
- **Backend failure:** first reduce batch/length, diagnose actual operation/dtype, or use explicit CPU for a tiny actual encoder run. A larger decoder is not the first response to an MPS setup issue.
- **Semantic failure after a functioning loop:** evaluate the Qwen fallback on exactly the same validation inputs if recurring rule/negation failures persist. Likewise consider it if important examples cannot fit 512 tokens. Request the Model compute slot; do not silently truncate contexts until the task changes.
- Retain train families `intent`, `sentiment`, `rule_application`; **`passage_entailment` stays reserved**. Split related source groups before paraphrases. Do not inspect final evaluation for tuning.
- Report coverage/failures, top-choice accuracy or teacher agreement by provenance, per-family counts, log loss, ties and truncations. Include uniform probabilities: per-example uniform log loss is `log(K)`. Compare pre-update and trained checkpoints on the same cases.
- Independent pair scoring should be permutation-equivariant in evaluation mode, apart from numerical tolerance and deterministic tie-breaking. Validate by reversing existing validation options and mapping back to IDs; this is repeated measurement, not more independent examples. For decoder symbols, additionally watch position/token bias. [D1]
- At ~60 validation cases, avoid strong calibration claims or elaborate per-family ECE. Keep `T=1` initially. Do not fit temperature on those same labels and report the resulting score as held-out evidence. [D2]
- Public data is not needed to unblock the pilot. BANKING77's official card declares CC BY 4.0; preserve attribution and construct plausible 2–6-option subsets. SST-2's official card declares an unknown license, so do not presume commercial reuse rights. Locally authored, actually rule-verified scenarios offer clearer provenance. [D3–D4]

## Primary sources

Sources accessed 2026-11-11. Model files are pinned where practical; backend docs describe upstream support, not a verified local environment.

- **E1** [Encoder model card, pinned](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2/blob/233902d25c440f23af6f7d6e94d2946bac0bee0a/README.md): intended task, license, pretrained logits, retrieval metrics, V100 timing caveat.
- **E2** [Encoder config, pinned](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2/blob/233902d25c440f23af6f7d6e94d2946bac0bee0a/config.json): actual six-layer BERT classifier and Identity score activation.
- **E3** [Encoder tokenizer config, pinned](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2/blob/233902d25c440f23af6f7d6e94d2946bac0bee0a/tokenizer_config.json).
- **E4** [Encoder repository metadata](https://huggingface.co/api/models/cross-encoder/ms-marco-MiniLM-L6-v2): revision and safetensors metadata.
- **E5** [Encoder weight-file metadata](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2/blob/233902d25c440f23af6f7d6e94d2946bac0bee0a/model.safetensors).
- **A1** [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2): embedding objective, 384 dimensions, standard pipeline 256-wordpiece truncation.
- **Q1** [Qwen card, pinned](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/README.md): exact checkpoint context, instruction tuning, minimum Transformers version, chat-template example.
- **Q2** [Qwen config, pinned](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/config.json).
- **Q3** [Qwen tokenizer config, pinned](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/tokenizer_config.json).
- **Q4** [Qwen repository metadata](https://huggingface.co/api/models/Qwen/Qwen2.5-0.5B-Instruct).
- **Q5** [Qwen weight-file metadata](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/model.safetensors).
- **Q6** [Qwen license, pinned](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/7ae557604adf67be50417f59c2c2f167def9a775/LICENSE).
- **B1** [Apple: PyTorch acceleration](https://developer.apple.com/metal/pytorch/).
- **B2** [PyTorch stable MPS notes](https://docs.pytorch.org/docs/stable/notes/mps.html).
- **B3** [PyTorch v2.7.1 MPS dtype source](https://github.com/pytorch/pytorch/blob/v2.7.1/aten/src/ATen/native/mps/OperationUtils.h).
- **B4** [MPS environment variables](https://docs.pytorch.org/docs/stable/mps_environment_variables.html).
- **B5** [MLX-LM Qwen2 implementation](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/models/qwen2.py).
- **B6** [MLX-LM LoRA documentation](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md); [PEFT LoRA reference](https://huggingface.co/docs/peft/en/package_reference/lora).
- **D1** [Wei et al., ACL Findings 2024: order and token sensitivity](https://aclanthology.org/2024.findings-acl.333/). General evidence, not a measured Qwen0.5B result.
- **D2** [Guo et al., 2017: calibration and temperature scaling](https://proceedings.mlr.press/v70/guo17a.html).
- **D3** [PolyAI BANKING77 publisher card](https://huggingface.co/datasets/PolyAI/banking77/blob/main/README.md).
- **D4** [Stanford SST-2 publisher card](https://huggingface.co/datasets/stanfordnlp/sst2/blob/main/README.md).
