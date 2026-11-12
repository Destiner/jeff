# M9 browser engine — B1 proof and B2 short-input contract

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

HFJS assembled-pair truncation differs from native `longest_first`, so the worker encodes each side without special tokens and constructs `[CLS] A [SEP] B [SEP]` with segments0/1 and longest padding per decision. B2 deliberately supports short inputs only: if `A.length + B.length + 3 > 256`, reject before tensor construction or model inference. It does not silently truncate or claim long-input equivalence. Original BERT WordPiece/BertNormalizer/BertPreTokenizer and standard pair template are required; unsupported layouts fail explicitly. B1's earlier source-derived truncation implementation remains in its frozen execution tree; its three proof cases never reached that branch.

Inputs are int64 `[options,sequence]` for all three named inputs; output must be FP32 `logits[options,1]`. Stable T=1 group softmax, never sigmoid. No calibration claim.

Predictions serialize on the main thread and worker. Init deadline 120s, each active prediction 60s, disposal 5s total including queued work; any worker error/deadline terminates it and rejects pending requests. Disposal normally waits for the active work and releases the ORT session before termination; the hard deadline terminates even if release cannot complete. Invalid decisions reject without closing an otherwise healthy engine.

Asset progress events retain `stage,message` and may include per-asset `receivedBytes,totalBytes`. Counts are actual response-body bytes, including explicit service-worker cache responses; they are not necessarily network transfer. A total is provided only for a positive safe-integer Content-Length with absent/identity encoding and is dropped if inconsistent. Missing totals mean indeterminate progress. No fake completion percentage is emitted. The host's versioned service worker deliberately handles `cache:'no-store'` requests; Transformers' separate caches remain disabled.

`modelLoadMs` measures actual ORT session creation, not model download; `initializationMs` includes tokenizer fetch/construction and model fetch/session creation. `tokenizerLoadMs` is reported separately. Prediction `inferenceMs` measures session.run; `tokenizerMs` includes formatting/tokenization/tensor preparation; `totalMs` includes both. Diagnostics include actual padded input arrays, raw logits and backend. Request records measure completed explicit fetch bodies and durations, including WASM if fetched by ORT; `.mjs` Resource Timing is best-effort, bytes null when unavailable. These are known-asset observations, not proof of all page requests, offline reload or cold-cache network transfer. JS bundle requests are host-owned. Browser version is its actual user-agent string.

## Readiness

B1's actual Safari three-case FP32 parity and its limits are recorded in `docs/runtime/browser-b1.md`. B2 adds streamed progress and overlength rejection; the changed TypeScript/Vite build passed, but new cache/offline behavior requires its own actual proof. No tests/lint or long-input verification is authorized. Worker errors close the engine; a host must dispose/reset its engine reference before offering retry. No offline-ready claim follows merely from service-worker registration.
