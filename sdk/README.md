# @jeff/sdk

Private local ESM package, version `0.1.0`, for the compatible FP32 decision encoder in a secure browser context with module workers (HTTPS or localhost). The built package supplies `dist/index.js`, TypeScript declarations and the actual `dist/worker.js`. It does not include Qwen, model weights, WASM, example fixtures or a service worker. This is not a public npm submission or a claim of general browser, Node, SSR or public redistribution support.

## Local integration

The Infra-owned root workspace should include this package; demos consume `"@jeff/sdk": "workspace:*"`. Do not create a second dependency/lockfile setup for a demo. Runtime dependencies are exactly `@huggingface/transformers@3.8.1` and `onnxruntime-web@1.22.0-dev.20250409-89f8206ba4`; consumers must retain those same fixed versions. Build tooling is TypeScript `5.9.3` and Vite `7.2.2`. The package build command is `bun run --cwd sdk build` from the workspace root. The host bundler/deployment must retain the built module worker next to the built SDK entry as referenced by `new URL('./worker.js', import.meta.url)`.

### Stage local assets

Manual local deployment needs only the retained B1 export, the packaged small descriptor and two files from the exact installed ORT version. No fixture data, assets registry or new copy tooling is required. Set these absolute paths for your checkout, installed package and host public directory; do not assume root-hoisted `node_modules`:

```sh
JEFF_ROOT=/Users/destiner/Code/jeff
SDK_DIR="$JEFF_ROOT/sdk"
EXPORT="$JEFF_ROOT/artifacts/release/browser-b1-20261112-01/export-01/assets"
ORT_DIST=/absolute/path/to/installed/onnxruntime-web/dist
DEST=/absolute/path/to/host/public/jeff-m9-local-01

# Run as one subshell. Refuse existing destinations, including partial copies.
(
  set -eu
  for source in \
    "$EXPORT/model.onnx" \
    "$EXPORT/tokenizer/tokenizer.json" \
    "$EXPORT/tokenizer/tokenizer_config.json" \
    "$SDK_DIR/models/m9.json" \
    "$ORT_DIST/ort-wasm-simd-threaded.mjs" \
    "$ORT_DIST/ort-wasm-simd-threaded.wasm"; do
    test -f "$source" || { printf 'Missing source: %s\n' "$source" >&2; exit 1; }
  done
  # Parent directory must already exist. mkdir deliberately has no -p.
  mkdir "$DEST"
  mkdir "$DEST/model" "$DEST/ort"
  cp -n "$EXPORT/model.onnx" "$DEST/model/model.onnx"
  cp -n "$EXPORT/tokenizer/tokenizer.json" "$DEST/model/tokenizer.json"
  cp -n "$EXPORT/tokenizer/tokenizer_config.json" "$DEST/model/tokenizer_config.json"
  cp -n "$SDK_DIR/models/m9.json" "$DEST/model/model.json"
  cp -n "$ORT_DIST/ort-wasm-simd-threaded.mjs" "$DEST/ort/ort-wasm-simd-threaded.mjs"
  cp -n "$ORT_DIST/ort-wasm-simd-threaded.wasm" "$DEST/ort/ort-wasm-simd-threaded.wasm"
)
```

If a copy fails, leave that partial directory intact for inspection and choose a new destination; do not merge into, delete or overwrite an existing deployment. `ORT_DIST` must belong to the pinned ORT version above, not an arbitrary installation. Keep the two ORT filenames unchanged. Serve the resulting directory at `/jeff-m9-local-01/` on the app origin, including suitable JavaScript/WASM MIME types. Adjust the URLs below if you choose another fresh directory name. The descriptor provenance and inventory are documented in [models/README.md](models/README.md).

## Predict

```ts
import { createEngine } from '@jeff/sdk';

const engine = await createEngine({
  assetBaseUrl: '/jeff-m9-local-01/model/',
  ortBaseUrl: '/jeff-m9-local-01/ort/',
  expectedModelId: 'm9-msmarco-duration-20261111-01', // optional verification
});

try {
  const prediction = await engine.predict({
    state: 'I have 20 minutes before my next meeting.',
    question: 'Which task should I do now?',
    options: [
      { id: 'reply', text: 'Reply to one short email.' },
      { id: 'report', text: 'Start writing a long report.' },
    ],
  });
  // Prediction only: { schema_version: '0.1', id, probabilities:
  //   [{ option_id: 'reply', probability: number }, ...] }
  // Render prediction.probabilities in your UI.
} finally {
  await engine.dispose();
}
```

`predict(input: DecisionInput): Promise<Prediction>` returns only the v0.1 prediction, not a diagnostics wrapper. Supply a nonempty question and at least two options with nonempty, unique IDs and nonempty text. State defaults to `''`; wire `schema_version` defaults to `'0.1'`; omitted decision ID becomes `sdk:${crypto.randomUUID()}`. A string-only options array is also accepted and receives IDs `option-1`, `option-2`, etc. Do not mix strings and option objects. An explicit valid `Decision` retains its schema version, ID, state, question and option IDs/text. Input is snapshotted before queueing so subsequent caller mutation does not change it.

This is the trained M9 source/scorer described by the selected descriptor: FP32 scalar logits, the existing BERT formatter pairing `State:\n{state}\nQuestion:\n{question}` with `Candidate:\n{text}`, and softmax T=1 across the supplied choices. Each encoded pair, including special tokens, must fit 256 tokens. Overlength input is rejected, not silently truncated; no formatter or truncation redesign is implied. These probabilities are not claimed to be calibrated.

## Metadata and optional diagnostics

`engine.metadata.model` is the fetched, validated descriptor (`ModelDescriptor`), including its ID, label, checkpoint declaration and file pins. `expectedModelId` only checks that identity; it is not a free-form display label. Metadata also includes the WASM backend, single-thread setting, dependency versions, initialization timings and request records.

When diagnostics are needed, use `predictWithDiagnostics` **instead of** `predict` for that decision, not as a second inference pass just to log it:

```ts
const { prediction, diagnostics } = await engine.predictWithDiagnostics(input);
// Use prediction normally; inspect diagnostics only when explicitly needed.
```

Here `input` is your `DecisionInput`. The returned `Result` contains the prediction plus token IDs/masks/type IDs, logits, timings and request records. Tokenized inputs can reveal sensitive content. The SDK does not log or persist inputs or diagnostics, add telemetry, store inputs, or fall back to remote inference. Caller code must make its own privacy choices. Request records are best-effort observations, not a complete network audit; dynamic ORT module imports can appear via Resource Timing.

## Lifetime, failures and local loading

Both base URLs are explicit same-origin HTTP(S) directory URLs ending in `/`, without credentials, query or fragment. The worker fetches `model.json`, then checks **all three** model/tokenizer assets' byte lengths and SHA-256 hashes against that descriptor before using each asset. The same-origin descriptor is publisher-declared provenance, not a trusted signature or full-checkpoint verification. ORT files are separate pinned-version runtime deployment inputs, not descriptor-hashed model files.

`createEngine` accepts optional `onProgress(event)` and `signal: AbortSignal`. Progress exposes stage/message and, where available, received/total bytes. The signal controls the **whole engine lifetime**, including initialization and pending requests; it is not a per-prediction cancel option. Aborting terminates the worker and closes the engine. Predictions are serialized. Initialization has a 120-second deadline, each dispatched prediction 60 seconds (queue wait is separate), and disposal a 5-second bound including queue draining. `dispose()` is idempotent and prevents new predictions.

A fatal worker/runtime error or deadline closes the engine, terminates its worker and rejects pending work. Errors reported by the worker, including overlength input, are fatal to that engine; main-thread input validation rejects before dispatch. Recovery/reset is explicit: dispose the old engine and call `createEngine` again, with a fresh signal if the old one was aborted. No automatic retry or remote fallback occurs.

Offline caching and service-worker scope/cache graphs belong to the host, not the SDK. Include the descriptor, all three model/tokenizer assets, the two ORT files and actual built app/SDK/worker resources in a new host cache graph if offline operation is required. SDK fetches use `no-store`; a host service worker may still supply responses. Do not infer offline readiness from this copy recipe.

## Evidence boundary

These are source/API and local deployment instructions. Historical B2 success is not proof for the extracted SDK. Numerical parity, performance, a separate consumer's deployed worker graph and online/offline behavior require actual scheduled SDK execution evidence; no such pass is claimed here.
