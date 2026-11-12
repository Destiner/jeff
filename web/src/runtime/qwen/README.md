# B2 trained-M10 Qwen adapter (source-only)

```ts
import { createQwenEngine } from './runtime/qwen';
const engine = await createQwenEngine({ assetBaseUrl: '/qwen/', onProgress });
const { prediction, diagnostics } = await engine.predict(decision);
await engine.dispose();
```

Explicit opt-in only; no UI integration, autoload, retry, generation, cache, remote model lookup, precision ladder or alternate backend. Keep M9 default and dispose the other model before initialization. Every call is serialized in a dedicated module worker. Parent deadlines are 180s initialization / 60s prediction / 5s disposal, measured from submission, including queued work. Errors/timeouts terminate the worker and reject outstanding calls. Device loss/uncaptured GPU errors also fail closed. Callback exceptions dispose the engine.

## Assets / actual producer schema

`assetBaseUrl` must be a same-origin HTTP(S) directory URL ending in `/`, without query/fragment/credentials. Serve these producer outputs **without flattening or rewriting**:

- `receipt.json`: completed `jeff.browser-b2.export.v1` receipt, including `binding`, `artifacts`, `export_contract`, strict `loading_info`, `parameter_metadata`, `fp16_parameter_metadata`.
- `export-contract.json`: producer's export contract object (there is **no schema_version or checkpoint identity field in this file**).
- `source-checkpoint-manifest.json`: exact pinned trained-v1 manifest, SHA256 `765d802270b8c0b090e9206c3e52f12e76ea7e224dbb4f07c9cc3c709aa6b15a`.
- `model.onnx`: one file below 2,000,000,000 bytes, no external data. Exact downloaded byte count must match producer inventory. Its recorded SHA is exposed, **not recomputed in browser**; producer/copier must attest model bytes separately.
- `assets/tokenizer.json`, `assets/tokenizer_config.json`: exact original files; checked against the hashed source manifest, including byte length/SHA256.

Contract bytes are checked against the receipt inventory and the parsed contract against receipt `export_contract`. Receipt binds actual trained weight SHA256 `751ecdc0433b21d200af0e38966b5b28107dc9ff2267977f0eae2e936cb5131d`, prompt/scoring controls, strict load and tied-head metadata. These are local producer/copy attestations, not independent authentication of the ONNX model. Contract/receipt structure or actual inspected graph mismatch rejects before Session creation; no guessed generic-model path.

The producer is `src/jeff/model/browser_qwen_export.py` in the Model B2 worktree; native renderer semantics are from `src/jeff/runtime/qwen_challenger.py:prepare`. Frozen final I/O: `input_ids` int64 `[1, sequence]` only → `logits` float32 `[1,6]`, ABCDEF IDs 32–37. Complete, unpadded batch1 prompt length 1..1024; no truncation. FP16 learned backbone/projection with producer-bound FP32 rotary frequencies and FP32 output. Producer/native evidence, not this adapter, establishes graph precision islands.

## Infra runtime assets

Copy **from onnxruntime-web@1.22.0-dev.20250409-89f8206ba4/dist**:

- `/ort/ort-wasm-simd-threaded.jsep.mjs` — JavaScript module, `text/javascript`.
- `/ort/ort-wasm-simd-threaded.jsep.wasm` — `application/wasm`.

Serve JSON as `application/json`, ONNX as `application/octet-stream`. JSEP module/WASM assets are necessary runtime infrastructure, **not a whole-model WASM backend selection**. Worker requests `executionProviders: ['webgpu']` only, with no alternate-backend retry. The agreed route permits CPU shape bookkeeping; the unexecuted draft's blanket `disable_cpu_ep_fallback` guard was removed before outcomes because it also forbids that bookkeeping. Actual WebGPU profiler callback counts/types are retained cumulatively; they are not a complete CPU/GPU placement audit, and timing includes profiling overhead. The actual graph's first output axis is the recorded symbolic `Castlogits_dim_0`; each returned tensor must still be exactly FP32[1,6]. Optional `signal?: AbortSignal` cancels initialization and active work, terminating only this owned worker.

All worker fetches use an exact same-origin allowlist, GET, omitted credentials and redirect:error. The fixed JSEP module is fetched through that guard, then imported from a worker-owned blob URL (revoked on disposal); its WASM path remains the exact local URL. CSP must permit this owned `blob:` module import as well as local WASM compilation. No tokenizer `from_pretrained` lookup is used. Actual decoded response bytes drive per-asset progress; totals are indeterminate if transport headers do not establish them. Successful final totals are actual bytes, not estimated model progress. Browser memory is explicitly unknown.

Loaded HFJS/ORT versions are checked before assets/session. Worker adapter must advertise shader-f16 and both buffer/storage limits >=272269312. The pinned ORT backend requests adapter limits/features itself; adapter/device setters are not overridden. After Session creation, actual ORT device and adapter are checked again and recorded. Advertising capability is not model/operator/memory success.

Rendering uses the original chat template with system+user and add_generation_prompt:true. Raw special-token strings are rejected, then complete encoding is performed without extra special tokens. Each A–F append must preserve the complete prefix and append exactly its bound token. Only the first actual K logits (K2..6) enter stable JavaScript Number T1 softmax; IDs/order remain caller-supplied and ties use original order. Diagnostics expose actual rendered text, prompt/answer IDs, all six/selected logits, K/mapping, timings, requests and actual device facts. Prompt/result diagnostics are returned only to the caller, not persisted.

## Evidence boundary

Verified source builds: `tsc --noEmit`, existing `vite build`, and an isolated Vite build using this existing `index.ts` as Rollup input with `preserveEntrySignatures:'strict'` and the existing Vite worker configuration. The isolated build emitted a ~1.27MB Qwen worker and ~1.55KB entry into `/tmp/jeff-qwen-entry-final-bcfWwC` (no page added). An earlier library-mode build in `/tmp/jeff-qwen-build-j9C0LO` inlined runtime assets and is not the recommended integration configuration. Temporary node_modules symlink removed after builds. TypeScript/bundling and source review are not native/browser parity. Ordinary Vite production build has no import of this entry and does not bundle Qwen. Infra owns a separate non-demo proof entry/page and final asset staging. No ML/tokenizer execution, weights inspection/download, browser run, new cases, tests or lint were performed for this implementation. Exactly the existing three P11 cases must still pass the separately frozen native/browser gate (exact prompts/tokens/mapping, finite/sum tolerance 1e-6, maximum probability difference <=0.01 and identical tops) before any normal-demo exposure.
