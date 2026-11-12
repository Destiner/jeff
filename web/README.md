# Jeff browser

A local decision scorer: context, question and2–6 explicit choices → relative scores. The trained M9 FP32 encoder runs in a browser worker with WASM; the loopback server supplies static files only. Scores are not calibrated confidence or a general-purpose reasoning claim.

## One-command local launch

Requires Bun (development used1.4.4) and this repository's retained B1 M9 export. The model is deliberately not in Git. Install pinned browser dependencies once, without native postinstall scripts:

```sh
cd web
bun install --frozen-lockfile --ignore-scripts
bun run demo
```

The launcher locates canonical artifacts through Git's common directory, safely prepares assets, builds the app and starts **http://127.0.0.1:4173/**. Defaults:

- Model: `artifacts/release/browser-b1-20261112-01/export-01/assets`.
- Inputs: durable `artifacts/infra/browser-b2-20261112-01/p11-train.jsonl`, the original three label-free TRAIN examples, SHA256 `26015911424707f5c9194201d0d9ad3342e0af71399ceefe9e9a4924491e3437`. No disposable `/tmp` dependency.
- Lifetime:7200seconds including preparation/build. Ctrl-C stops the owned process group. Maximum14400seconds; an optional absolute cutoff wins if earlier.

```sh
bun run demo --port 4173 --duration-seconds 7200 \
  --stop-at 2026-11-12T15:45:00Z
```

The dated cutoff is the B2 handoff example, not a reusable future date. Absolute `--model-dir` and `--inputs` overrides are supported. Nothing installs dependencies, downloads a remote model, exports weights or executes inference automatically. Missing prerequisites fail visibly. Use the actual exported M9 directory, never a source checkpoint or downloaded base model.

The copier validates nine explicit model/tokenizer/ORT/input assets before writing. Identical existing files are reused; conflicting or partial files are preserved and rejected, not overwritten. Source mapping remains in ignored `asset-manifest.local.json` outside the served tree. Assets live under ignored `public/models/m9/`, `public/ort/`, and `public/examples/`; build output is ignored `dist/`. The exact package pins are Transformers.js3.8.1, ORT Web1.22.0-dev.20250409-89f8206ba4, TypeScript5.9.3 and Vite7.2.2 in one `bun.lock`.

## Run and prepare offline

Fill the fields and select **Run locally**. Model loading is explicit. Progress reports actual received bytes for the current asset when its length is known; session initialization/inference remain distinct, indeterminate phases. Later runs reuse the resident worker. Editing inputs clears stale results; failed engines are released rather than silently reused. Inputs/results stay in memory and are not uploaded or persisted by the app.

Select **Make M9 available offline** while the server is available. This explicitly saves the necessary same-origin app, worker, model, tokenizer, input-example and ORT assets. It does not initialize or run a model. Readiness requires every expected cache entry plus the matching activated service-worker controller—not registration alone. Unsupported storage/Web Locks, incomplete transfers, quota failures and pending updates remain visible.

The build emits a content-versioned manifest and immutable `/sw-<version>.js`. Preparation checks response/body lengths and completed CacheAPI writes, then writes its completion marker and registers the worker. It does **not** independently verify downloaded bytes against SHA256; same-length wrong bytes are not ruled out by readiness alone. Old complete caches are retained; there is no forced `skipWaiting` or silent deletion. A waiting update may require closing and reopening this origin's tabs. Browser eviction or manually clearing site data can remove the offline copy.

Once the app reports ready, this origin can reload and run M9 while its local server is unavailable. HTTP responses remain `no-store`; the explicit versioned CacheAPI is separate. Qwen, unused JSEP payloads, unknown/query/POST routes, entered prompts and results are not in the M9 cache. Adjacent third-party notice texts under `public/notices/` are retained/served but are not part of its fourteen-file offline cache.

## Actual B2 evidence and limits

On2026-11-12, Runtime operated Safari27.0 with executed primary source **c377014c28c24249f9219d2c6cebd0dc8bd067c8**, cache version **8200802812ae241dc07f6c6e**:14required assets, **104,050,573 bytes**. It performed three original TRAIN cases online, explicitly prepared the cache, disposed the task worker, then reloaded and performed the same three cases while Infra's server was stopped. The app's cache preparation was not treated as inference proof.

- Cache complete12:41:52UTC; Infra server40767 absent/port4173refused12:49:01.
- Runtime independently checked refusal before and after its12:50:39–41server-unavailable inference. Host networking stayed on (`navigator.onLine=true`). The actual reload's retained browser-tool evidence is covered by Runtime/Evaluation, separately from the receipt's phase label.
- Both phases completed three calls, were disposed and ended not-busy/null-engine. Model charged **6/600seconds** across the two phases; no native M9 reload or automatic third pass.
- Research independently compared each phase's11probabilities against the original retained CPU reference: maximum difference **6.777156989767885e−7 ≤1e−4**, all three top choices identical, exact token matrices and finite normalized scores. No clipping or baseline replacement.
- Infra restored a static host after the offline return at12:53:20. The final handoff records its successor's exact command/PIDs/deadline. Later docs or builds are not retroactive execution revisions.

Evidence: `artifacts/release/browser-b2-20261112-01/` (phase receipts, cache and reload records); `artifacts/infra/browser-b2-20261112-01/` (builds, manifests, server lifecycle); `artifacts/research/b2-review-20261112T122925Z/` (separate numerical comparisons); Evaluation owns the independent functional/lifecycle review. See `artifacts/handoffs/infra/browser-b2-20261112-01/` for final delivery.

This is a bounded three-case, one-browser proof—not controlled cold-cache benchmarking, exhaustive OS traffic observation, arbitrary-host support, long-input equivalence or representative quality. Browser memory was unavailable, not zero. Short-input overlength pairs are rejected; general truncation behavior was not verified. Known task workers were disposed; unrelated/global user browser state remains unknown.

## Static server and capture API

The finite server binds127.0.0.1, serves only built `dist/`, accepts GET/HEAD, rejects symlink escape and sends same-origin isolation/CSP headers. No inference API, repository mount, directory listing, telemetry or remote fallback. Structured stdout records offered body bytes, not confirmed transfers or exclusively browser-originated traffic. Standalone `bun run serve` defaults1800seconds, maximum14400; supports the same absolute `--stop-at`. The B2 final static-only host is explicitly allowed to outlive foreground attention but must expire no later than15:45UTC; this does not grant background model execution or monitoring.

```js
window.jeffBrowser.loadDecision(input); // Populate only.
const receipt = await window.jeffBrowser.run(input);
const actualReceipts = window.jeffBrowser.history;
await window.jeffBrowser.dispose(); // Also aborts pending initialization/work.
const preparation = await window.jeffBrowser.offline.prepare();
const current = await window.jeffBrowser.offline.status();
```

The bridge uses the actual button paths and returns successful-only cloned history. Host checks preserve option identity, finite[0,1] scores and normalization without repair. Disposal retains the last completed comparison; edits invalidate it. Runtime owns tokenization/scoring and worker timeouts. Model schedules agent-operated inference; availability or leftover budget is not permission for another run.

## Isolated Qwen prototype and notices

The separately scheduled actual trained M10 FP16/WebGPU stretch uses `qwen-proof.html`, `src/qwen-proof.ts` and `vite.qwen.config.ts`. It is not imported by the normal M9 entry, cached or exposed as a selector. Its standalone output requires explicitly staged Model-produced assets; the ordinary launcher does not stage or retain that prototype. The actual attempt at12:57:05–09UTC initialized the trained WebGPU engine, then stopped when sampled host memory pressure changed from1to2 during its first prediction request. Zero predictions/probabilities completed; physical forward progress was not returned. Its task worker was disposed. Browser memory bytes remain unavailable, and the pressure observation does not establish a causal memory attribution. No parity gate passed, no selector was added and no retry/backend/precision change was made. Qwen charged26/1200seconds including its earlier20-second native export/reference chain; this ledger is separate from M9's6seconds. Preserve `artifacts/release/browser-b2-20261112-01/qwen-01/` and Model's original export/reference evidence. Source/build/device support is not numerical proof.

Complete bounded third-party source texts and their qualifications are retained under `public/notices/`. They are not a complete shipped-binary attribution audit or public-release clearance. Jeff first-party redistribution terms and underlying corpus/teacher/demo-row rights remain unestablished. No public upload/deployment is authorized. Python/root dependencies and historical ML environments are unchanged; builds run without software tests or lint.
