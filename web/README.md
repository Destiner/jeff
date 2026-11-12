# Jeff browser

A small local host for the trained M9 reference. The browser worker tokenizes context/question/choices and runs the exported FP32 scalar model with WASM; the server only supplies static files. Scores compare the supplied choices, not calibrated confidence or demonstrated general-purpose reasoning.

## Build and run

Requires Bun (development used1.4.4), the exact B1 M9 export from Runtime, and the three original label-free P11 TRAIN examples. Model/exported assets are intentionally not in Git. Runtime's exporter and numerical evidence are separate from this host; an empty shell build is not inference proof.

```sh
cd web
bun install --frozen-lockfile
bun run assets \
  --model-dir /Users/destiner/Code/jeff/artifacts/release/browser-b1-20261112-01/export-01/assets \
  --inputs /private/tmp/jeff-p11-20261112-01/kit/m9-bundle/demo/inputs.jsonl
bun run build
bun run serve --port 4173 --duration-seconds 1800
```

Use the **actual exported M9 directory**, not the source checkpoint or a downloaded base model. The copy step requires `model.onnx`, `encoder/config.json`, and `tokenizer/{tokenizer.json,tokenizer_config.json,special_tokens_map.json,vocab.txt}`. It flattens those six explicit assets into the served model directory and copies only those files, the pinned ORT WASM/MJS pair, and the exact hash-bound three-case input file. No checkpoint/source directory, environment, labels or private evaluation data is served.

- Model/tokenizer: ignored `public/models/m9/` → `/models/m9/`.
- Matching runtime: ignored `public/ort/` → `/ort/`.
- Three label-free TRAIN examples: ignored `public/examples/p11-train.jsonl`.
- File identity/source mapping: ignored **`asset-manifest.local.json`**, outside the served tree.

The copy step uses exclusive creation. Existing/partial copies cause a visible error rather than silently replacing an earlier attempt; preserve their evidence before deliberately preparing a fresh destination. Builds typecheck and bundle with Vite, without software tests or lint. Node-only ONNX Runtime is not used; its blocked Bun postinstall does not need approval for browser inference.

Open **http://127.0.0.1:4173/**. Fill context, question and2–6 choices, then **Run locally**. Nothing loads the model automatically. First run includes model initialization; later runs reuse that worker/session until disposed or the page closes. Disposal retains the last computed comparison with an explicit released-model state; editing inputs still clears stale results. Invalid or missing assets/results produce an error, never fixture scores. In the shared B1 workflow, only Runtime operates the model under Model's serialized reservation.

## Serving and evidence

The finite-lifetime server binds loopback only, serves built `dist/` files, accepts GET/HEAD and has no inference API, repository mount, directory listing or telemetry. It rejects symlink escape and sends same-origin isolation/CSP headers. Structured stdout records request path/status/offered byte count—not confirmed client transfer or browser-only provenance. Stop with Ctrl-C; `--duration-seconds` defaults1800 and is capped at5400. The owner must supervise its lifetime and any loaded model separately.

HTTP responses use `no-store`; there is **no service worker or offline-reload claim**. A warm already-loaded engine is different from cached downloads or a fully offline reload. Bundled assets require no external/CDN calls at inference; actual page request evidence, not this configuration alone, establishes what happened in a run.

For supervised artifact capture the same app execution path is available as:

```js
window.jeffBrowser.loadDecision(input); // Populate only; no model load.
const receipt = await window.jeffBrowser.run(input);
// receipt: input, prediction, diagnostics, engineMetadata, wallMs
const actualReceipts = window.jeffBrowser.history;
await window.jeffBrowser.dispose();
```

Calls are serial, canonical IDs/text are preserved, and only actual successful outputs enter in-memory history. The bridge neither uploads nor automatically writes inputs/results. Runtime owns timeouts, tokenization/scoring and worker disposal; the host owns form validation and checks result identity/finite normalized scores without repairing them.

The scoped package pins Transformers.js3.8.1, ORT Web1.22.0-dev.20250409-89f8206ba4, TypeScript5.9.3 and Vite7.2.2 in one `bun.lock`. No root Python dependencies or existing ML environments are changed. Numerical acceptance remains Evaluation's predeclared three-case comparison; wider parity, arbitrary-host support, quality and public rights clearance are not implied by this host.
