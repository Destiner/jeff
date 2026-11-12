# Browser B2 — offline M9 and the stopped Qwen attempt

**M9: bounded GO. Qwen: UNVERIFIED after a resource stop.** M9 passed both independent numerical comparisons and actual new-document inference with its static server unavailable. The final ordinary demo preserves the proved cache/import graph. Qwen initialized the actual trained M10 WebGPU session, but its first prediction was aborted on sampled OS memory pressure; no parity result exists and Qwen is not exposed in the normal demo.

Open **http://127.0.0.1:4173/** while the Infra-owned static host is available; its absolute expiry is **2026-11-12 15:45 UTC**. [Launch instructions](../../web/README.md) describe `bun run demo`, explicit offline preparation and retained local assets. The host has no inference backend and does not load a model automatically.

Canonical authority: `artifacts/handoffs/lead/browser-20261112-02/shared.md`. Artifact paths below are relative to `/Users/destiner/Code/jeff/`. The companion manifest binds small evidence files, without a new model-asset rehash or numerical replay.

## M9: accepted bounded proof

Executed source: `c377014c28c24249f9219d2c6cebd0dc8bd067c8`. The original M9 graph must remain exactly unchanged; no model selector or Qwen entry belongs in the normal demo.

| Phase | Independent numeric result | Scope |
| --- | --- | --- |
| Initial online | PASS: max absolute difference `6.777156989767885e-7 <= 1e-4` | Three identical top choices, eleven probabilities, exact ordered token matrices |
| Server-unavailable new document | PASS: same maximum difference and threshold | Three identical top choices, eleven probabilities, exact ordered token matrices |

These are the three original short P11 TRAIN inputs, not held-out quality evidence. Both Research reports and parent checks establish saved arithmetic/mapping, not network or lifecycle provenance. Two passes total **six calls / twenty-two values**, conservatively charged **6/600 seconds**. No native M9 reference reload or third pass was needed. Original receipts, controllers and delivery summaries are under `artifacts/release/browser-b2-20261112-01/{m9-online-01,m9-offline-01}/`; independent reviews are under `artifacts/research/b2-review-20261112T122925Z/{m9-online,m9-offline}/report.json` and the corresponding `m9-*-parent-check.json`. Model's `artifacts/model/browser-b2-20261112-01/m9-return.json` predates the completed offline arithmetic review; its then-pending wording is not a pending numeric result now.

### Actual server-unavailable/new-document evidence

All times below are UTC on 2026-11-12.

- `cache-prepare-01.json`: preparation at **12:41:52**, no model loaded; all **14 assets / 104,050,573 bytes** ready under cache version `8200802812ae241dc07f6c6e`.
- Infra `feature-host-stop-01.json`: own static host stopped and absent at **12:49:01**; localhost connection refused. No host-network toggle.
- Runtime `server-unavailable-runtime-check.json`: socket refused at **12:50:34.579**.
- The named Safari `navigate_to_url` operation on owned handle **19** returned the root document between **12:50:34.579 and 12:50:39.552**. The proof began **12:50:39.797**, completed all three calls and disposed the worker by **12:50:41**.
- Runtime `server-unavailable-after-proof.json`: socket still refused at **12:51:22**. The receipt retained the controlling versioned service worker and ready cache; `navigator.onLine` was true.
- `m9-offline-navigation-observed-later.json` was collected later, at **12:56:58.828**; it is supplemental evidence, not retroactively inserted into the original receipt. Its `timeOrigin=1794487836837.02` is **12:50:36.837 UTC**, navigation type is `navigate`, and `workerStart=3.38 ms`, consistent with the new document preceding the same recorded proof.

Together this supports actual inference after navigation to a new document while the local static server was unavailable. It does **not** establish entire-host offline operation, an OS traffic audit, or browser-side cryptographic verification of cache contents. Browser memory measurement was unavailable. Initial and reloaded timings are observations, not a benchmark distribution.

### Runtime behavior and launch handoff

Actual per-asset byte progress is distinct from session initialization; unknown totals must remain indeterminate. AbortSignal and finite initialization/cancellation APIs support bounded teardown. M9 rejects a fully encoded candidate pair above 256 tokens before inference; this is not a general truncation audit or broad long-input guarantee.

Infra actually launched the final ordinary demo at **13:04:27 UTC** from `.worktrees/infra/web`:

```sh
/opt/homebrew/bin/bun run demo --port 4173 --duration-seconds 14400 \
  --stop-at 2026-11-12T15:45:00Z
```

The dated cutoff is this handoff's limit, not a reusable future date. Static server **74636**, launcher **74617**, outer Bun **74616** remain Infra-owned with automatic absolute expiry at **15:45 UTC**, explicitly allowed beyond foreground attention. There is no background model job or monitoring promise. `artifacts/infra/browser-b2-20261112-01/final-host-03.json` records launch, HEAD 200, source and full required-manifest equality; `final-launch-03.jsonl` remains a live lifecycle log, not a frozen proof snapshot.

Final reviewed source **06576d05b92f45c26b88ef28d68ce0fc3ae3b041**, integrated as **a55771c8624b40286828220db5b672f45907a920**, is distinct from executed `c377014`. Rebuilt required manifest/version/14 assets/104,050,573 bytes match exactly, including code identities. Evaluation independently checked that equality and the final host. No third model pass was needed. The ordinary dist excludes Qwen prototype page/model and staged JSEP copies; Vite's existing unrequested 21,596,019-byte JSEP WASM emission remains outside the M9 cache.

The launcher reuses matching assets and preserves/rejects conflicting or partial files. It uses the retained B1 export and durable `artifacts/infra/browser-b2-20261112-01/p11-train.jsonl` (SHA256 `26015911424707f5c9194201d0d9ad3342e0af71399ceefe9e9a4924491e3437`), not `/tmp`. No remote download, dependency installation, export or inference occurs automatically. Pinned browser dependencies require the explicit one-time installation in the README. Twenty-one complete bounded notice texts sit beside assets, outside the fourteen-file cache; they are not a complete binary attribution audit, public-release clearance or first-party redistribution grant.

## Qwen: actual initialization, no parity outcome

Model export source: `c99cc5d480017896d4a8302ac66e5ee3e84d9fbd`. Actual combined browser source: `cd1507c80fe7364bed045106a11e7a9087a364b0`, including Runtime `9f6861e`, `e89c75f`, and `7cd6b4b`.

The export preserves the actual trained M10 seed7 learned embedding/full backbone and the six actual A–F LM-head rows. Native head/embedding tying is retained semantically by copying those trained rows for FP16 projection, not by introducing a frozen-base readout or reinitialization. The final graph has one `int64[1,L]` input and a required `float32[1,6]` logits result; no generation or KV cache. Runtime slices the first K logits in original option order and uses stable T1 softmax. Native checkpoint and FP32 references were unchanged.

Metadata attests a **989,080,308-byte FP16 graph**, SHA-256 `501bc4abe0c7ee66a885508992c61b4e75663a3d2776bf35942b7a1e498bbacd`. Graph identity is adopted from producer/copier metadata, not rehashed for this publication. Model's `native-return.json` records three completed FP32 reference forwards and one completed FP16 tracing forward, successful parent/group closure, and a conservative **20/1200-second** charge. Browser execution adds six seconds: **26/1200 seconds total**, separate from M9.

### Browser attempt and stop

`qwen-01/{receipt-after-abort.json,controller-return.json,closure-observation.json,delivery-summary.json}` record actual Safari WebGPU / shader-f16 initialization with the requested near-2-GiB device buffer limits (`2147483644` bytes). Those capability limits are **not memory capacity**. Session initialization succeeded; `engine_created=true`, with initialization metadata retained in the saved evidence.

Actual browser interval: **12:57:05.046–12:57:09.512 UTC**. One first prediction request was in flight when sampled `kern.memorystatus_vm_pressure_level` changed **1 → 2 at 4.505 seconds**. The parent requested abort of its own worker. Result: **0 completed prediction requests / 0 returned probabilities**. The physical-forward counter was unavailable in the aborted result: do not fabricate zero forwards, zero model load, or a completed forward. The controller reports failure and the receipt retains `AbortError`; this is a resource-policy stop, **not a numerical failure**.

The frozen reduced-precision gate requires exact prompt/token/option mapping, finite normalized probabilities (sum tolerance `1e-6`), maximum FP32-native/browser probability difference `<=0.01`, and identical tops on all three cases. **Gate not measured; no parity result.** There are no fake pending numbers to fill. No Qwen UI exposure, automatic retry, alternate precision/backend, new reference, or re-export is authorized. A later pressure reading of 1 does not undo the stop or authorize retry.

The generic WebGPU provider can use CPU shape operations. GPU profiling counts were not returned because the first prediction was aborted; no all-node GPU-placement proof exists. Browser RAM peak is unavailable, and the sampled OS pressure transition does not support attributing all system memory pressure causally to Qwen.

### Plumbing history and isolation

The nullable-total progress-type build failure is retained as history; compatible fix `7cd6b4b` preceded execution. Symbolic output-batch binding fix `e89c75f` also preceded outcomes; any returned tensor would still have to be `[1,6]`. The early three-input proposal was superseded by the one-input contract **before export**, not as an outcome rescue. The 12:05 adapter-only capability observation is retained at `preparation/capability.json`; it did not request a device or load a model. Historical tokenizer-regex, `torch_dtype` and legacy ONNX-export warnings remain in Model's native evidence. Infra integrated the explicitly approved Runtime source unchanged; combined TypeScript/Vite and Python builds passed.

Keep Qwen source/prototype isolated outside the user-facing M9 demo and its cache. Infra's `qwen-prototype-assets-01.json` is copier inventory attestation, not browser-side graph rehashing. `prototype-host-02.json` is static readiness only.

## Closure and independent acceptance

Both M9 workers were disposed, busy false and engine metadata null. Qwen's own worker was terminated through abort; saved initialization metadata remains as evidence, while final live state is busy false / null engine. This is task-scoped closure, not global browser/model absence.

Tab closure was incomplete: closing selected Qwen handle **20** was refused; handle **19** was stale. Relisting only the original window showed selected owned Qwen 20 and a root-localhost tab with new handle **22**, not an API flag. No forced close or unrelated user-content inspection was performed. Workers closed, tabs not fully closed; browser control released.

Research's controlling `artifacts/research/b2-review-20261112T122925Z/review-summary.md` adopts both separate M9 arithmetic passes and records no Qwen parity result. [Evaluation's final acceptance](../evaluation/browser-b2.md), integrated at `6880128564819ee1c0550746c2052661ef37979c`, independently checks the cache/server/new-document chain and final host/manifest equality without duplicate numerical scoring. Model's `artifacts/model/browser-b2-20261112-01/{native-return.json,m9-return.json,qwen-return.json}` closes the separate ledgers. [Model's results](../model/browser-b2-results.md) preserve native execution versus later publication identity.

Operational qualifications remain: Research's initial schema/pin/poll failures, Evaluation's incorrect manually transcribed closure hash before correction, and Infra's wrong uv executable path on its first integration attempt. Original failure records and producer bytes were preserved; Infra aborted only its own merge before the successful retry. These are not new model attempts or repaired numerical evidence.

Runtime publication uses small-file JSON/source inspection and an offline Python package build. Infra's combined browser build and unchanged final manifest are adopted; publication does not reload the browser or change its proved graph. Build logs are under `artifacts/release/browser-b2-20261112-01/preparation/`. No software tests/lint, new dependencies, protected references, model replay or additional actual/pending spend were introduced. Known inference workers and execution grants are closed; the explicitly finite static host is the remaining Infra-owned service.
