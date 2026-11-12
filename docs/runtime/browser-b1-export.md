# BROWSER-B1: single-attempt native M9 export

This contract was prepared source-only, then the unchanged exporter completed the authorized B1 native stage. See [the actual export and Safari result](browser-b1.md) for execution evidence and its narrow three-case acceptance. The original source preparation itself did not load a model; neither this document nor a successful build is native proof. Runtime's feasibility window is 10:35:50–12:05:50; this script does not extend it. Every future invocation needs an actual bounded Model grant. An activation string records that grant's identifier; it is **not authentication or execution authority**.

## Execution interface

Use the owner-prepared **new isolated environment**, with exactly P11's installed Torch/Transformers versions plus a pinned compatible ONNX package. No root dependency/lock changes, installation into historical environments, model substitution or network fallback. The script sets Hugging Face offline flags; these are not OS-level network denial.

```sh
/path/to/new/export-env/bin/python -B scripts/release/browser_b1_export.py \
  --activation MODEL_GRANTED_ACTIVATION_ID \
  --checkpoint /absolute/frozen/M9/checkpoint \
  --checkpoint-pins /absolute/model-checkpoint-pins.json \
  --checkpoint-pins-sha256 MODEL_SUPPLIED_SHA256 \
  --input /absolute/fixed-three-decisions.jsonl \
  --input-sha256 EVALUATION_SUPPLIED_SHA256 \
  --native-bindings /absolute/native-bindings.json \
  --native-bindings-sha256 BINDING_SHA256 \
  --native-source /absolute/original-checkout/src \
  --environment /absolute/export-environment.json \
  --environment-sha256 ENVIRONMENT_SHA256 \
  --output /absolute/artifacts/release/browser-b1-UNIQUE-attempt \
  --max-seconds 300 --max-rss-gib 8
```

**Do not run this command without Model's actual grant and an actively supervised, finite hard parent timeout.** The caller owns process supervision, aggregate execution charging, deadline/slot closure, environment provisioning and OS network restrictions. The script creates no scheduler, watcher or subprocess inference job. Resource checks sample process peak RSS and elapsed monotonic time at stage boundaries, each hash chunk and native forward entry/completion. They are cooperative: an import/load/export/native kernel may exceed a bound between samples. This is not an 8 GiB memory reservation or a hard wall-time guarantee. Parent termination can leave `running` status plus the last journal sample; the parent must preserve and report that outcome, not call it success.

The output directory must not exist. Never reuse an attempt path, delete a failed attempt, or silently retry with a different attention implementation, precision, exporter or numerical recipe.

## Required pin documents

Hashes are lowercase SHA256 strings. Pin-document schemas below are deliberately explicit; Model/Evaluation should supply or adapt their forthcoming manifests to these schemas before execution. Paths inside the native reference binding are explicit local paths. A caller-supplied hash/string is an integrity binding, not an authenticity claim.

### Model checkpoint pins

```json
{
  "schema_version": "browser-b1.checkpoint.v1",
  "checkpoint_identity": "M9-msmarco-12epoch",
  "files": {
    "checkpoint.json": "SHA256",
    "encoder/config.json": "SHA256",
    "encoder/model.safetensors": "SHA256",
    "tokenizer/tokenizer.json": "SHA256",
    "tokenizer/tokenizer_config.json": "SHA256",
    "tokenizer/special_tokens_map.json": "SHA256",
    "tokenizer/vocab.txt": "SHA256"
  }
}
```

Exactly these seven files are accepted and hashed, never other checkpoints. Symlinks and extra files are rejected before native loading. Model must establish these as the actual trained twelve-epoch M9 assets, not merely label a different checkpoint with the identity string. The pin document itself is SHA256-bound on the CLI. Original checkpoint files are neither written nor chmodded.

### Native bindings

```json
{
  "schema_version": "browser-b1.native-bindings.v1",
  "checkpoint_pins_sha256": "SHA256_OF_ABOVE_MANIFEST",
  "input_sha256": "SHA256_OF_FIXED_JSONL",
  "case_ids": [
    "data:pilot-v1:intent:g01:r01",
    "data:pilot-v1:sentiment-r2:g01:r01",
    "data:pilot-v1:rule_application:g01:r01"
  ],
  "source_files": {
    "jeff/model/cross_encoder.py": "SHA256",
    "jeff/model/scorer.py": "SHA256"
  },
  "p11_native_reference": {
    "path": "/absolute/retained/P11/native-output.jsonl",
    "sha256": "SHA256"
  }
}
```

Bind the **actual three frozen P11 input rows**, not just their IDs: their exact file hash is mandatory. JSONL contains only v0.1 `schema_version`, `id`, `state`, `question`, `options`; no labels, training metadata or protected cases. Exactly the three IDs above are accepted, in the binding's declared order (the example order is not mandatory). Native validation checks the decision structure. Retained P11 output is hash-bound for Evaluation; this exporter does not reinterpret or overwrite its historical numbers. Evaluation owns comparing old/native/browser outputs and the predeclared browser tolerance <=1e-4 with identical tops.

`--native-source` is the original source **src directory**, not the package's model subdirectory. Native loader/scorer bytes are verified, and source Git HEAD plus porcelain status are recorded. No replacement formatter, tokenizer or scalar head is introduced. Original package dependencies must already be available in the isolated environment. Other imported dependency/source files are not comprehensively attested by these two source pins.

### Environment pins

```json
{
  "schema_version": "browser-b1.environment.v1",
  "prefix": "/absolute/new/export-env",
  "python": "EXACT_PYTHON_VERSION",
  "packages": {
    "torch": "EXACT_INSTALLED_VERSION",
    "transformers": "EXACT_INSTALLED_VERSION",
    "onnx": "EXACT_INSTALLED_VERSION"
  },
  "p11_packages": {
    "torch": "EXACT_P11_INSTALLED_VERSION",
    "transformers": "EXACT_P11_INSTALLED_VERSION"
  }
}
```

The owner derives P11 versions from the installed-wheelhouse evidence, not a newer resolver result. Values are intentionally not guessed here. Installed distribution versions, imported ML versions, isolated prefix and Python version must match. Platform, executable and full interpreter string are recorded. These metadata checks are not a complete binary/dependency supply-chain attestation.

## Native/reference/export contract

1. `attempt.json`, `status.json` and append-only `journal.jsonl` exist **before ML imports or model/tokenizer loading**. Input, checkpoint, source and environment pins are checked first. Exceptions preserve a traceback, failure stage, partial artifacts, warning records, timing and sampled peak RSS. There is no silent retry or cleanup.
2. Use original `cross_encoder.load_retained_checkpoint(..., "cpu")`; its strict native classifier loader retains the saved scalar head. Require CPU FP32 parameters, all modules in eval mode, cap256 and temperature1. No precision conversion, optimizer or weight update. No attention backend argument is supplied. Record the actual native configured/internal attention backend and attention module classes, including SDPA if selected by the installed native stack.
3. Exactly **three reference classifier calls**, one original `model([decision])` per case. This runs the original formatter and tokenizer: first `State:\n{state}\nQuestion:\n{question}`, second `Candidate:\n{text}`, longest-first truncation256 and padding to the longest candidate **within each decision**, not across all three. Classifier hooks capture actual forwarded `input_ids`, `attention_mask`, `token_type_ids`, and native FP32 raw `[N,1]` logits. Native choice softmax is computed at T=1. `native-references.json` is updated after each case and preserves ordered option IDs, exact padded token arrays, logits, probabilities and input-order top choice.
4. One call to the stable `torch.onnx.export`, explicitly `dynamo=False`, opset17, `do_constant_folding=False`, eval training mode, saved parameters. A minimal wrapper returns the original classifier's `.logits`, without sigmoid or probability normalization. Inputs are int64 `input_ids`, `attention_mask`, `token_type_ids`, dynamic candidate batch and sequence axes; output is FP32 `logits[N,1]`, dynamic batch. The export example is the actual last decision's tokens; it adds no reference forward.
5. Normal legacy tracing is allowed. Hooks count **actual classifier entries and completed calls separately**, split into `references` and `export`, plus totals. Do not assert that one exporter invocation equals one classifier forward. Trace entries that fail still count. Every emitted warning is recorded with category/message/source/stage under an `always` filter, including ordinary tracer warnings, with an exact `TracerWarning` count. Do not label all warnings a failure or suppress normal tracing warnings. No exporter compatibility call is guessed or monkeypatched: if the installed native attention/export stack fails (including unsupported SDPA), retain the failure and report the explicit problem. Any prospective repair must first inspect the actual installed source and remain within Model's grant; there is no automatic attention variant fallback.
6. ONNX parsing validates graph names, dtypes, opset and dynamic dimensions, not numerical execution. No ONNX Runtime Python inference or independent optimizer runs. Built-in legacy exporter lowering remains part of the recorded Torch implementation; `do_constant_folding=False` is not a claim that no internal graph transformations occur.

## Outputs and handoff

- `attempt.json`: initial invocation/authority identifier/resource metadata.
- `status.json`: latest state, package/source/backend metadata, calls, emitted warnings, samples and failure details if any.
- `journal.jsonl`: chronological stage/resource/warning/finish evidence.
- Frozen pin/environment/binding/input copies; incremental `native-references.json`.
- `assets/model.onnx` and byte-identical original `assets/checkpoint.json`, `assets/encoder/config.json`, `assets/tokenizer/{tokenizer.json,tokenizer_config.json,special_tokens_map.json,vocab.txt}`. Original weights are **not** copied into browser assets. ONNX-generated sidecars, if any, remain in the same assets tree.
- `asset-inventory.json`: SHA256 and size for every generated/copied asset, including ONNX sidecars. Successfully completed assets are files0444/directories0555 (accidental-write protection, not WORM/authentication). Failed attempts retain writable partial output.

Browser consumers should use the documented nested local paths or explicitly copy the unchanged tokenizer/config bytes into their loader's required layout and retain that mapping/inventory. Tokenization parity can be checked directly against each reference's actual three arrays. The browser must normalize candidate logits with softmax across that decision at T=1, preserve IDs and use input order for exact ties. Native/browser load and inference timing, offline reload, request inspection, memory availability and browser backend evidence remain Runtime/Infra/Evaluation work; this exporter makes no browser success claim.
