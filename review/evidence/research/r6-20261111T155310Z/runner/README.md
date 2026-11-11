# R6 frozen-P3 order/letter executor

**Prepared implementation only; not executed, imported, tokenized, or model-validated by Research.** No tests/lint, model imports/loads, weight scans, inference, downloads, dependencies, commits, merges, or mailbox activity were performed for this handoff. Only these new runner artifacts are delivered. Parent may copy the script into `experiments/research/` before freezing its audit. No import of Jeff runtime helpers is required.

Runtime alone may execute the separately authorized, lower-priority diagnostic after an explicit Model scheduling grant. This is **not** M6/P4/E6, a training run, a temperature experiment, or permission to access Evaluation/probe/D3/final data. Do not use a trained M6 model directory. Do not run another arm, warmup, smoke prediction, automatic retry, or background launcher. A successful run performs exactly the packet row count of model calls: 4 per case, 1–48 TRAIN cases, 4–192 calls. A failure stops without retry.

## Packet boundary and provenance

Explicit CLI paths avoid depending on undocumented metadata keys:

- `--inputs`: label-free `inputs.jsonl`.
- `--config`: packet `config.json`, **not** `configs/runtime/p3-qwen.json`.
- `--selection`: packet `selection.json`.
- All three must be regular files in the same dedicated packet directory. Every file recursively in that directory is SHA-256-bound, including `packet.json` when present, preparation source files, manifests, and any other evidence. Symlinks and files larger than 32 MiB are rejected. Keep unrelated files outside the directory.
- Both audit and prediction destinations must be new directories **outside the packet tree**. Do not put a virtual environment, model assets, audit outputs, or predictions inside it.
- Config, selection, and optional packet metadata are parsed for valid JSON with unique keys, and reject common explicit label/answer fields recursively. Their other fields remain opaque: the executor hashes their bytes; it does not claim to interpret undocumented preparation hash-binding keys, selection methods, or controls. The executed controls are fixed in source and receipts, never taken from opaque metadata.
- `--train-only-confirmed` is a required Runtime operator attestation. The runner cannot prove split provenance from label-free records. Parent must verify the frozen selection against the released TRAIN source and record preparation-source and released TRAIN hashes in the packet **before** outcomes; do not supply or open labeled data through this runner. If preparation source is not included in the packet, its claimed hash is only a preparation attestation, not independently verified source content.
- Do not change packet bytes after audit. Whole-packet file hashes and the script hash are rechecked at run end without a second weight scan.

Each JSONL row has **exactly** these keys (no `schema_version` or labels):

```text
{id, case_id, condition, order_reversed, letters_reversed,
 state, question,
 options: [{id, text, letter, original_position}]}
```

IDs/text are strings, flags are JSON booleans. `state` may be empty; question, IDs and option text may not. Option count is 2–26. Rows have unique presentation IDs, each case has exactly `O0L0`, `O0L1`, `O1L0`, `O1L1`, and options are in displayed order. For displayed position `d` and `K` options:

- `original_position = order_reversed ? K-1-d : d`, zero-based.
- `letter = chr(65 + (letters_reversed ? K-1-d : d))`.

Across all four conditions, state/question and the original-position `(option ID, text)` sequence must be identical. No case is dropped or truncated. Strict input schemas reject hidden label/metadata fields; metadata checks are not a general semantic detector for encoded labels. Parent remains responsible for permitted content and genuine TRAIN provenance.

## P3 identity and rendering

Pins are embedded in source and checked against the exact P3 audit metadata file:

| Item | SHA-256 / identity |
| --- | --- |
| Model | `Qwen/Qwen2.5-0.5B-Instruct` |
| Revision | `7ae557604adf67be50417f59c2c2f167def9a775` |
| Original `model.safetensors` | `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe` |
| P3 audit-02 receipt | `8e0dc65beb1c9dd5a21b2c4170853bc78bf14116429a9311c28e568c129d870a` |
| P3 audited runtime source | `325d3a6b8e5577bba3b885fe8b61d5551305b456e2586d3949b2c45c649438d5` |
| P3 config | `2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f` |
| Official chat template | `cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f` |

The current main-checkout `src/jeff/runtime/qwen_challenger.py` read during preparation hashes to `cb07ceaf8af6cf1b06b08d11aff7a234031877428eb0aa27e37ad609eef731a5`, **different from the historically audited P3 source**, and includes additive trained-checkpoint support. This script does not import it or claim current-source byte identity. It independently reproduces its P3 `SYSTEM`, `USER`, official `apply_chat_template(..., tokenize=False, add_generation_prompt=True)` and continuation-boundary method. Its own exact source SHA is frozen in the new audit. The historical source SHA is an attestation from the pinned P3 audit, not a dependency file imported at run time.

The conceptual equivalence for both **L0** conditions is direct: letters are `A..` in displayed order; the user option lines, system/user messages, generation prefix, full-prompt tokenizer settings, cap and answer token derivation match P3 `prepare()` for those displayed options. For L1 only the supplied letter assignment changes; no different instructions, suffix, scoring transform, or prompt search is introduced. This is source-level reasoning, not an executed equivalence test.

Tokenizer audit rejects special-token strings in source content, renders each actual prompt, checks the untruncated 1024-token cap, then encodes **each actual rendered prompt + assigned letter**. Every continuation must preserve the complete prompt token prefix and append exactly one distinct token. Audit binds rendered-prompt hashes, prompt-token hashes, answer-token IDs, and official chat-template hash for every row.

The entire P3 receipt is read as metadata only; no dataset path it references is opened. Model directory inventory and nonweight asset hashes must exactly match its `model_assets`, including model config and tokenizer config. Extra trained/checkpoint files are rejected (HF `.cache` metadata is ignored). Asset hashes ultimately inherit the P3 local-download attestation; they are not independent remote authentication.

## Future Runtime commands — do not run as Research

Use an already provisioned, isolated Python 3.12 `.venv` with the existing locked ML packages. Do not install dependencies, invoke a package manager that might download them, or use an active M6 environment. Use the same environment for both commands. The example names below are placeholders, not a launcher:

```sh
PY=/absolute/isolated/.venv/bin/python
RUNNER=/absolute/experiments/research/run_order_packet.py
PACKET=/absolute/dedicated/frozen-train-packet
MODEL=/absolute/existing/pinned-P3-model
P3AUDIT=/Users/destiner/Code/jeff/artifacts/release/p3-qwen-20261111-01/audit-02/audit.json
AUDIT=/absolute/new-unique-r6-audit
OUT=/absolute/new-unique-r6-predictions

"$PY" "$RUNNER" audit \
  --inputs "$PACKET/inputs.jsonl" --config "$PACKET/config.json" \
  --selection "$PACKET/selection.json" --model-dir "$MODEL" \
  --p3-audit "$P3AUDIT" --audit-dir "$AUDIT" --train-only-confirmed

# Only after a passed audit, under the separately scheduled Model grant:
"$PY" "$RUNNER" predict \
  --inputs "$PACKET/inputs.jsonl" --config "$PACKET/config.json" \
  --selection "$PACKET/selection.json" --model-dir "$MODEL" \
  --p3-audit "$P3AUDIT" --audit-dir "$AUDIT" --output-dir "$OUT" \
  --train-only-confirmed
```

**Audit is CPU/tokenizer-only:** `USE_TORCH=0`, `USE_TF=0`, `USE_FLAX=0` are set before importing Transformers, and it refuses success if `torch` was imported. It constructs no model and does not read weight contents. It uses the known weight SHA from the pinned P3 audit, explicitly marked as attestation-only. All other listed assets are actually hashed. Parent should not add repeated independent weight scans.

**Predict actually hashes the pinned weight file once**, before any model construction, and compares every model asset to the frozen P3 hashes; this rejects a trained M6 checkpoint even if its base lineage string matches. It regenerates the audit evidence and requires full equality, including script/config/input/selection/whole-packet hashes, tokenization, official template, model inventory and installed package versions. Copying the script to a new path without byte changes is fine; changing script bytes needs a fresh audit. Explicit data/model paths are frozen in evidence, so relocating them needs a fresh audit too.

Both commands force Hugging Face/Transformers offline mode. All `from_pretrained` calls specify `local_files_only=True`, `trust_remote_code=False`; predict also specifies `use_safetensors=True`. Missing assets fail; there is no download, remote-code or CPU fallback. Predict uses FP32/MPS, SDPA, threads=4, batch=1, `.eval()`, frozen gradients, `torch.inference_mode()`, `use_cache=False`, and `logits_to_keep=1`. No startup/warmup model call is made. The first **packet** forward has its own latency and flag rather than being excluded or rerun.

## Outputs, runtime and failure handling

Audit writes exclusively created `audit.json`; predict writes exclusively created `predictions.jsonl` and `receipt.json`. Files become mode `0444` and the new directory `0555` on normal/failure finalization. Existing directories are never reused. These are operational immutability controls, not tamper-proof storage.

Prediction rows contain:

- Contract-style `probabilities`, aligned by **original option IDs and original positions**, not by assigned letters. Probabilities are exactly `softmax(K allowed logits)` at T=1; not calibrated/full-vocabulary confidence.
- Exactly K `option_scores` with original ID/position, assigned letter, token ID and raw next-token logit. **No full-vocabulary vector is saved.**
- Scalar `log_full_vocab_normalizer`, allowed-token full-vocabulary logmass (via two logsumexp values), and its exponential mass. These are diagnostics only and never alter conditional scoring. Floating-point logmass/mass may have tiny roundoff near zero/one; do not reinterpret that as changed scores.
- Display-order deterministic top-choice tie-break and explicit tied IDs. Probability arrays are original-order aligned, so downstream tools should not infer display-order tie-breaking from array order alone.
- Prompt token count, model-forward latency and first-forward flag. No input text or targets are copied into predictions/receipts.

The run receipt includes input/source/model/packet/audit hashes, expected/persisted row counts, attempted/completed forwards, coverage, first-forward and all forward timings, cold model-load duration, whole-command elapsed time, process-lifetime CPU max RSS, sampled MPS allocation/driver memory and observed driver maximum. It hashes every output already present before writing the receipt; the receipt cannot include its own hash. Parent can hash that small file once for the final handoff.

The 300s guard covers the **whole command**, including identity hashing, tokenization, model load, execution and output. CPU process-lifetime RSS and observed MPS driver allocation are guarded at 8 GiB. Checks run around hashing/tokenization and before/after load/forwards; MPS samples are **not peak memory measurements**. Guards are cooperative, not an interrupt inside native load/forward/hash operations. A separate Runtime supervisor is required for an actual hard wall-clock/memory deadline. No background launcher is supplied. Do not run if the slot/supervisor cannot enforce these boundaries.

SIGINT/SIGTERM request failure finalization when Python regains control. Failures preserve flushed prediction rows and create a failed receipt with coverage/counts and output hashes when finalization is possible. Each prediction row is flushed/fsynced before counting it persisted. Guard failures preserve content-free reason strings; third-party exception strings are suppressed to avoid leaking packet content. No auto retry/resume. A SIGKILL, crash, full disk or uninterruptible native operation may prevent final receipt/chmod; the supervisor must record exit status, wall time, available output hashes/counts and incomplete coverage externally. Never turn a partial run into a passed packet or silently regenerate missing arms.

## Delivery status

Source-reviewed only. No audit, tokenizer execution, build, inference, software tests or lint were run. No empirical resource, token-boundary, numerical or model-output success is claimed. Runtime must report audit pass/failure and actual execution separately from this preparation. M6/P4/E6 remain untouched.
