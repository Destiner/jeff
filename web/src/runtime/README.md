# B1 browser engine — source-only handoff

```ts
import { createEngine } from './runtime';
const engine = await createEngine({
  assetBaseUrl: '/models/m9/',
  onProgress: ({ stage, message }) => console.info(stage, message),
});
try {
  const { prediction, diagnostics } = await engine.predict(decision);
} finally {
  await engine.dispose();
}
```

`Decision`, `Prediction`, `Result`, `Metadata`, `Progress` and `RequestRecord` are exported from `index.ts`. JSON decision/prediction fields are v0.1. Only state, question and option text enter model text. IDs and input order are retained; equal probabilities use input order when selecting a maximum. No DOM or HTML processing.

## Host contract

Infra owns package configuration/build/serving. Pin `@huggingface/transformers@3.8.1` and `onnxruntime-web@1.22.0-dev.20250409-89f8206ba4`. Actual loaded library versions are checked and returned. Importing `index.ts` does not create a worker or load model assets; calling `createEngine` does.

`assetBaseUrl` must be a same-origin HTTP(S) directory ending in `/`, without credentials/query/fragment. Supply the actual exported FP32 checkpoint at `<base>model.onnx`, and the original `<base>tokenizer.json` plus `<base>tokenizer_config.json`. No nested-tokenizer copy is assumed. If Infra keeps tokenizer files nested, it must copy those two originals to the base or coordinate a source change before execution. No config.json/Model Hub lookup occurs: `new BertTokenizer(originalJSON, originalConfig)` is used.

Serve the matching installed ORT files at `/ort/ort-wasm-simd-threaded.mjs` (JavaScript MIME type) and `/ort/ort-wasm-simd-threaded.wasm` (`application/wasm`). The allowlist contains exactly these five model/tokenizer/runtime URLs. Worker fetch uses same-origin mode, no redirects/credentials and `cache: 'no-store'`. Transformers browser/FS/custom caches and remote models are disabled. WASM is explicit, one thread, proxy disabled. Dynamic module imports are browser-managed; the worker fetch wrapper cannot enforce cache/redirect behavior for `.mjs`. Serve those local files without redirects; enforce same-origin script/connect policy in the host if required. No telemetry or remote fallback is implemented.

## Semantics and limits

Pinned HFJS source inspection found pair truncation calls `truncateHelper` on the **assembled** pair; it does not implement native `longest_first`. Therefore this worker uses only `encode(..., {add_special_tokens:false})`, then explicitly constructs `[CLS] A [SEP] B [SEP]`, segments 0/1, right truncation to 253 content tokens and longest padding per decision to a maximum of 256. Length allocation follows the fast Hugging Face tokenizers Rust longest-first algorithm: preserve the shorter sequence where possible; otherwise split 126/127, favoring the originally longer sequence for the odd token (B for equal original lengths). This differs from a simplistic repeated pop-on-ties implementation. Source reference: `huggingface/tokenizers`, `v0.22.1/tokenizers/src/utils/truncation.rs`; HFJS reference: `3.8.1/src/tokenizers.js`. This is a source-derived implementation, **not demonstrated general tokenizer parity**. Requires original BERT WordPiece/BertNormalizer/BertPreTokenizer and standard pair template; unsupported layouts fail explicitly. Long inputs follow the described implementation but have no execution/parity evidence yet.

Inputs are int64 `[options,sequence]` for all three named inputs; output must be FP32 `logits[options,1]`. Stable T=1 group softmax, never sigmoid. No calibration claim.

Predictions serialize on the main thread and worker. Init deadline 120s, each active prediction 60s, disposal 5s total including queued work; any worker error/deadline terminates it and rejects pending requests. Disposal normally waits for the active work and releases the ORT session before termination; the hard deadline terminates even if release cannot complete. Invalid decisions reject without closing an otherwise healthy engine.

`modelLoadMs` measures actual ORT session creation, not model download; `initializationMs` includes tokenizer fetch/construction and model fetch/session creation. `tokenizerLoadMs` is reported separately. Prediction `inferenceMs` measures session.run; `tokenizerMs` includes formatting/tokenization/tensor preparation; `totalMs` includes both. Diagnostics include actual padded input arrays, raw logits and backend. Request records measure completed explicit fetch bodies and durations, including WASM if fetched by ORT; `.mjs` Resource Timing is best-effort, bytes null when unavailable. These are known-asset observations, not proof of all page requests, offline reload or cold-cache network transfer. JS bundle requests are host-owned. Browser version is its actual user-agent string.

## Readiness

Implementation only. No package is present in this isolated source worktree, so no build has run. No tests/lint, browser/native/tokenizer/model execution, dependency installation or commits were performed. Infra/Runtime must build the assembled package and inspect browser requests, exact token arrays and numerical parity on the three authorized cases before claiming acceptance. No numerical, long-input or offline proof is claimed.
