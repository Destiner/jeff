# BROWSER-B2: actual M10 → FP16 WebGPU scorer

**Source-ready only.** No model load, tokenizer execution, native inference,
conversion, ONNX export, browser execution, build, test or lint was performed
while writing this module. Browser compatibility and numerical parity remain
unmeasured. This is one route, not a quantization/backend experiment ladder.

## Activation interface

Run only under the separately supplied supervising parent, using its chosen
already-prepared Python environment. The parent owns authorization, serialization,
actual sampled RSS ≤12 GiB, four-thread limits, aggregate ≤1200-second Qwen
native/export/browser budget and absolute stop. The child has stage-level
`ru_maxrss` guards and a finite SIGALRM deadline, not sampled memory enforcement.
Signals can be delayed inside native calls; they do not replace the parent.

```sh
"$PYTHON" -m jeff.model.browser_qwen_export \
  --checkpoint /Users/destiner/Code/jeff/artifacts/model/m10-qwen-seed7-20261112-02/training/checkpoint \
  --inputs /private/tmp/jeff-p11-20261112-01/kit/m9-bundle/demo/inputs.jsonl \
  --output-root /absolute/NEW-attempt-directory \
  --activate BROWSER-B2-M10-FP16 \
  --deadline-utc 2026-11-12T13:10:00Z \
  --timeout-seconds 900
```

`900` is an example child bound, **not** extra budget. Parent must choose remaining
aggregate time and may set an earlier deadline. Both command start and actual
`torch.onnx.export` start must be no later than 12:40 UTC on 2026-11-12. The child
rejects a deadline later than 13:10 UTC. Activation is explicit, not permission
to run without the Model owner's slot. Importing the module uses stdlib only.

On deterministic export-plumbing retry, use another NEW output root and add:

```sh
--reuse-native-references /absolute/earlier-attempt/native-references.json
```

This file must be read-only, complete, and match the exact checkpoint/input
binding, prepared prompts/token IDs/mappings, package/Python/platform versions,
strict load diagnostics and parameter/tying metadata. Reuse still reloads the
actual checkpoint but makes **zero** native-reference forwards. It never falls
back to another reference pass on a mismatch. If a failed attempt entered native
forwards without freezing a complete reference, stop and report the partial
receipt; do not launch a replacement reference pass. Preserve every attempt.

## Frozen native semantics

Renderer is sourced from `src/jeff/runtime/qwen_challenger.py` `SYSTEM`, `USER`,
`prepare()` and `forward()`. The module deliberately does not invoke that
runtime's broader audit/predict CLI or access its dataset suites.

- Official local tokenizer chat template, system + user messages,
  `add_generation_prompt=True`.
- Exactly the three SHA-pinned original P11 short decision-only inputs, no labels
  or other data. Option IDs are mappings, never prompt features.
- Encode with `add_special_tokens=False`, `truncation=False`; reject embedded
  special-token strings. A–F appended to each rendered prompt must each be an
  identical token prefix followed by exactly one distinct token. The six answer
  IDs must agree across the three prompts. Only actual supplied options are
  rendered; checking unused suffix letters does not add model calls/cases.
- One FP32 CPU SDPA load, eval + inference mode, four threads, local-only,
  no remote code, no cache/generation. Strict empty missing/unexpected/mismatched/
  error load diagnostics; expected 494,032,768 unique parameters and actual
  tied embedding/head storage are checked and recorded.
- Exactly three reference calls, no warmup. Native model computes the **full
  vocabulary** LM head only at the final boundary (`logits_to_keep=1`). Store the
  selected six native FP32 logits; compute FP32 T1 softmax over first K logits,
  where K is the input option count. Unused A–F entries never enter the softmax.

The immutable `native-references.json` contains binding, prompt text, full prompt
IDs, six answer IDs, option mappings/text, six native logits, K probabilities,
top option, versions, load/tying metadata and 3/3 entered/completed counts. It is
fsynced, made read-only and hashed **before** any FP16 conversion/export. Partial
rows and entered/completed counters are durably recorded in `receipt.json`.

## Graph and browser interface

| Item | Contract |
| --- | --- |
| File | `model.onnx`, legacy `torch.onnx.export(dynamo=False)`, opset 17, single file / `external_data=False` below 2 GB |
| Input | `input_ids`: int64 `[1, sequence]`; one unpadded full prompt, dynamic sequence, no truncation |
| Output | `logits`: float32 `[1, 6]`, ordered A, B, C, D, E, F |
| Weights | Full trained M10 backbone and complete trained embedding converted to FP16; six rows copied **from the actual loaded trained output head** into FP16 projection |
| Readout | Final-normalized backbone hidden state at the last input position → FP16 linear projection → float32 output cast |
| Attention | Eager **export only**; dynamic 4-D additive causal mask and explicit position/cache positions; no KV cache |
| Runtime transform | Slice first K output entries, stable FP32 T1 softmax, map back to original ordered option IDs |

Stock native Qwen applies its linear head to that same final-normalized hidden
state. Selecting six rows computes exactly those six components in real
arithmetic; it does not introduce a frozen-base readout or retrain anything.
Native tied embedding/head semantics are checked before and after conversion;
the exported embedding stays complete, while the six-row projection is an
independent rounded copy of the tied trained rows. RoPE's non-learned `inv_freq`
is retained in FP32 because stock Qwen explicitly computes rotary frequencies
in FP32; learned parameters remain FP16. Reduced precision and SDPA→eager can
change numbers and still require the actual browser gate.

The explicit `{"full_attention": mask}` mapping bypasses HF 4.57's mask-builder
vmap path, without replacing the actual decoder layers or final norm. Installed
Qwen/HF and Torch exporter **source text** was inspected, not imported. Legacy
export is limited to one entered/completed wrapper tracing forward, on the first
of the same three prompts. No post-export native/ONNX execution is included.

## Outputs, identity and failure handling

- `source-checkpoint-manifest.json`: unchanged copied original manifest.
- `assets/`: copied config, generation config, tokenizer JSON/config, vocab,
  merges, LICENSE and README. Config remains an immutable source config, not a
  claim that graph computations are FP32. Use `export-contract.json` for graph
  precision and interface.
- `native-references.json`: complete immutable reference, retained even if later
  conversion/export fails.
- `model.onnx` and `export-contract.json`: only successful export products.
- `receipt.json`: atomically replaced stage/failure receipt, timing, lifetime RSS,
  forward counters, provenance, diagnostics, metadata and artifact hashes.

The original manifest SHA and its existing 1,976,163,472-byte weight SHA inventory
are pinned; the giant native safetensors file is **stat-checked, not rehashed**.
Small copied assets are verified against that manifest. Newly produced artifacts
are hashed once each. Native sources/checkpoints/historical artifacts are never
written. Failed/partial artifacts remain in their NEW attempt root. Abrupt SIGKILL
can leave only the last durable stage/counter; the parent must retain its own
termination evidence. Never serve a partial ONNX or infer success from its mere
presence; require a complete receipt.

FP16 parameter payload is approximately 988 MB; the single largest embedding is
151936 × 896 × 2 = **272,269,312 bytes**, larger than a 256 MiB buffer limit. Runtime
must establish actual WebGPU FP16/limits support separately. No automatic fallback
or alternate model/backend is provided. The actual browser must pass exact
prompts/token IDs/mappings, finite probabilities and sums within 1e-6, max absolute
native/browser probability difference ≤0.01, and identical top choices on **all
three** fixed inputs. Report discrepancies, not a claim of general quality or
calibration. Qwen must remain outside the normal demo unless that gate passes.
