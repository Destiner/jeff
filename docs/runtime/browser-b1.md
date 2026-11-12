# BROWSER-B1 — trained M9 in Safari

**GO for bounded three-case browser feasibility.** The actual trained FP32 M9 executes in a Safari WASM worker without an inference server. Independent Evaluation passed the frozen three-case P11 comparison: 11/11 finite normalized probabilities, 3/3 matching top choices, maximum as-recorded probability difference **6.777156989767885e-7** (limit1e-4), and exact equality of all **840 padded token positions / 2,520 integer entries**. This is portability evidence, not model quality, calibration or all-input equivalence. No new scoring was performed for publication.

## Scope and provenance

Canonical ignored evidence lives under `/Users/destiner/Code/jeff/artifacts/release/browser-b1-20261112-01/`: `preparation/`, `export-01/`, and `browser-01/`. The companion tracked manifest is `manifests/releases/browser-b1-20261112-01.json`. Only the original three P11 TRAIN examples were used (3/4/4 choices, 11 probabilities); these are portability examples, not held-out quality evidence. Input SHA256: `26015911424707f5c9194201d0d9ad3342e0af71399ceefe9e9a4924491e3437`.

- Checkpoint: actual M9 twelve-epoch MS MARCO, `artifacts/model/m9-msmarco-duration-20261111-01/training/checkpoint`; seven original files bound by `export-01/checkpoint-pins.json` (manifest SHA256 `fa5548ec733ddf56879c8c0968b71086e400025de21f5ce9bf119a34410763f2`). Original weights were not changed.
- Original native `cross_encoder.py` SHA256 `955ef625340373465300cc584dd7df8dc7dc12f239f74c1b79d1813bd239f481`; `scorer.py` SHA256 `83f78cb6dda53266f5dd8f84cc0865b33c7334d3922052036f1b5a184b31945c`.
- Exporter executed with SHA256 `3213547fac2392b0b1bb9c6d7d1cc701db517b470f4143e3b51239f741f50433`. **Dirty source at execution**, not retroactively a committed-source run: recorded HEAD `863e5e23aeb543724ae5c650a6049a40d155e5a3`, with untracked `docs/runtime/browser-b1-export.md` and `scripts/release/browser_b1_export.py`.
- Browser engine commit `c404fae6ad404798c7bb3680af8bf9ce61e17461`; actual executed combined host source `42659b3fd42266a6aca97ee112da9fbf0064d7b3`. Infra integrated the approved engine/host at `513bbc646c4f3da0efab4d3e532087b63cce1c73`, then UI timing-label changes at `30ad9f17994cb663216b93bc977f82c0f9ca2f1b`. Those post-run display changes were built, not retroactively executed.

## Native export actually completed

New isolated exporter environment: Python3.12.16, Torch2.15.0, Transformers4.57.6, ONNX1.19.1; CPU, four threads. The original native loader/scorer and trained scalar head remained in eval mode, FP32. Native configured/internal attention remained `sdpa` (`BertSdpaSelfAttention`); no attention substitution. Legacy exporter: `dynamo=False`, opset17, `do_constant_folding=False`, dynamic candidate/sequence dimensions. No quantization, alternate precision or Python ORT inference.

Exactly three reference forwards plus one tracing forward **entered and completed** (4 total). Retained warnings: two DeprecationWarnings and one TracerWarning from attention-mask tensor tracing; see `export-01/status.json` and `preparation/export-01.stderr.log`. The warnings are not suppressed or a claim of all-input trace correctness. Export controller elapsed10.78799775s, charged12s. ONNX graph parsing is structural validation, not independent numerical execution.

`model.onnx`: **90,997,024 bytes**, SHA256 `78fcd8a963d0ddd4d381200eb11f091a1e88ac80dab8d254cc3c6de1900ed1f1`. Original tokenizer/config copies and mapping are recorded in `export-01/asset-inventory.json` and Infra's asset manifest; no large-asset rehash was performed for this publication.

## Real browser proof

Safari27.0, dedicated `http://127.0.0.1:4173/`, window196264, handle `tab_mwdevi54f9e1ea16e96_14`. Only task-local execution and required tab metadata were used; no unrelated content inspected. `browser-01/receipt.json` records successful execution at 11:07:08–11:07:09 UTC on2026-11-12. The task-window AppleEvents bridge invoked the app API; it was not a Node-only inference demonstration.

Transformers.js **3.8.1**, ONNX Runtime Web **1.22.0-dev.20250409-89f8206ba4**, WASM backend, one thread, FP32 model. Main and worker use local-only paths; the host is static, with no Python inference backend. Engine does not auto-load. Exactly three cases ran, without extra warm-up or repeats; `errors: []` (no actual browser inference failure).

Tokenizer uses the original BERT WordPiece through JS `BertTokenizer` without special tokens, then explicit native pair construction, longest-first truncation and masks: HF JS assembled-pair truncation differs from native. Native text contract is `State:\n{state}\nQuestion:\n{question}` paired with `Candidate:\n{text}`, cap256, per-decision longest padding. One scalar per choice, choice softmax at T=1, stable option IDs/input-order ties; IDs/labels do not enter model text. Actual captured native/browser matrices have11 rows, padded lengths48/69/105. **All below256: no long-input truncation parity or all-input certification claim.** Evaluation independently confirmed equality of all three token arrays on these exact cases.

### Timing, not a controlled benchmark

| Measure | Recorded value |
|---|---:|
| Engine initialization |375.36ms|
| ONNX session creation (`modelLoadMs`; excludes model fetch) |270.08ms|
| Tokenizer load |26.239999999999995ms|
| First case inference (3×48) |128.24ms|
| Later different case (4×69), resident model |226.74ms|
| Later different case (4×105), resident model |352.42ms|
| Model interval |1.1565600000000122s|
| Whole bridge |1.170320000000007s|
| Controller |1.9822921669110656s|

Receipt worker request durations: tokenizer.json4.960000000000001ms; tokenizer_config.json4.080000000000005ms; model.onnx62.94ms; WASM13.440000000000026ms; MJS resource1.6400000000000148ms. These overlap initialization and must not be summed into a new full-visit metric. Local `no-store` loading is not a controlled cold OS/browser cache or remote-download measurement. Later calls use a loaded model but different cases; no controlled repeat/warm benchmark was run. Browser peak memory is unavailable (`null`).

Disposal explicitly completed: `disposed:true`, final app `busy:false`, `engineMetadata:null`. Browser charged3s, native12s: **15/1200s aggregate**, GBP0. This publication performs no new ML/browser/network activity.

## Assets and request boundary

Infra metadata: `artifacts/handoffs/infra/browser-b1-20261112-01/{asset-manifest-01.json,build-assets-01.json,host-server-01.jsonl}`. Staged assets total103,099,144 bytes; full dist125,634,745 bytes. The dist includes an unrequested JSEP WASM: **21,596,019 bytes according to `build-assets-01.json`**, conflicting with the supplied21,596,016-byte summary; retain the exact metadata value and flag the3-byte discrepancy rather than silently reconcile it. Dist size is not downloaded bytes. Receipt MJS resource size20,869 differs from the20,856-byte static manifest/server body; do not equate Resource Timing size with file bytes.

The server log records local GETs for the shell, exact TRAIN input, runtime/worker, tokenizer files, ONNX and WASM/MJS. It also records a favicon404, not an inference failure. Infra's `request-observation-01.json` and frozen `host-requests-browser-01.jsonl` corroborate the page/worker observations: one readiness HEAD and12 browser GETs,11 successful GETs offering103,805,736 body bytes, plus the favicon404. Required model/tokenizer/WASM/app requests succeeded; no POST, inference API or JSEP request appears. This is not a complete external-network trace, cached-download measurement or fully offline reload. Server offered body bytes are not confirmed client transfer. No inference server was used; offline reload was not demonstrated.

Infra PID7826 started11:04:19.939Z with hard expiry**12:05:49.939Z** (approximately12:05:50), not a permanent service. Its final handoff plans shutdown when Infra parks around**11:49:31Z**, unless a new explicit lifecycle agreement supersedes that. Main's model assets are not automatically installed; the demonstrated server uses Infra's staged worktree. Reproduction commands below remain available after shutdown. No public deployment is claimed.

## Reproduction (instructions only; not executed for publication)

Use the combined source containing the runtime and host. The read Infra `web/README.md` gives the scoped web commands below. Install only in the new web package; exporter installation belongs only in a new isolated environment, never historical ML environments/root packaging. Preserve existing/partial asset-copy attempts: exclusive creation rejects reused destinations.

```sh
cd web
bun install --frozen-lockfile
bun run assets \
  --model-dir /Users/destiner/Code/jeff/artifacts/release/browser-b1-20261112-01/export-01/assets \
  --inputs /private/tmp/jeff-p11-20261112-01/kit/m9-bundle/demo/inputs.jsonl
bun run build
bun run serve --port 4173 --duration-seconds 1800
```

Open `http://127.0.0.1:4173/` only under Model's serialized authorization before any model execution. The exact native exporter command, required pin schemas and parent-supervision requirement are in [browser-b1-export.md](browser-b1-export.md); the actual invocation/pins/environment are retained in `export-01/status.json` and `preparation/`. Do not rerun into `export-01`, substitute assets or treat the historical activation string as new authorization. Export supervision requires a finite hard parent timeout.

## Builds, independent acceptance and limits

Preparation retains first three TypeScript build failures (`engine-build-01.log` through `-03.log`), then fourth successful build (`engine-build-04.log`); Python package build passed (`python-build-01.log`). No tests or lint were run. These are existing build receipts, not builds repeated for this documentation handoff.

Evaluation's final `artifacts/evaluation/browser-b1-result-v1/report.md`, `comparison.json` and `projection.json` are authoritative. Reference `browser-b1-reference-v1/reference.json` was frozen before browser outcomes (SHA prefix`5b0e2813`), using actual P11 CPU evidence `55e0284c`, not the new native diagnostic probabilities. One saved-data comparator invocation passed all unchanged thresholds, including sums within1e-6, without clipping, renormalization, token repair or baseline substitution. Model's `artifacts/model/browser-b1-20261112-01/chain-return.json` closes the 15/1200-second execution ledger.

The combined host and exporter/result publication are integrated separately; their handoffs record actual main commits. Evaluation delivered the numerical result within its allowance, then disclosed4.21094seconds over its30-active-minute cap for final administrative metadata closure, without extra scoring. Dirty exporter provenance and the actual served42659b3 source remain explicit after integration. Infra's later disposal-display adjustment preserves an already-computed result but was not part of the executed source; no inference rerun was performed for it.

Long-input parity, wider input coverage, repeat latency, browser memory, offline reload, public deployment/rights, WebGPU, quantization and model quality are not demonstrated or authorized follow-on work here. No protected/private cases were accessed. The three-byte JSEP summary discrepancy is retained; metadata's21,596,019-byte entry is used rather than a silently corrected historical summary.
