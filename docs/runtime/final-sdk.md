# Browser SDK and final application handoff

**2026-11-12 · M9 · `@jeff/sdk` 0.1.0.** The separately packed SDK has an independently accepted, six-case **online Safari/WASM proof**. The production queue, chat and playground are implemented and built, but their newly planned browser acceptance is **UNATTEMPTED**. New SDK/application offline inference is **UNVERIFIED**. These are separate evidence boundaries; the historical B2 result does not fill either gap.

Use the [SDK API/deployment guide](../../sdk/README.md) and [application setup](../../web/README.md). The package remains `private: true`, with no npm publication. Public source availability does not supply model weights, choose a first-party license, or make a fresh clone immediately runnable. The [machine-readable record](../../manifests/releases/final-sdk-20261112-01.json) contains identity and evidence pins. Large evidence and the local model archive remain ignored local artifacts, not files distributed with the public repository.

## API and deployment

```ts
const engine = await createEngine({
  assetBaseUrl: '/models/m9/',
  ortBaseUrl: '/ort/',
  expectedModelId: 'm9-msmarco-duration-20261111-01',
  signal,
});
try {
  const prediction = await engine.predict(input);
  // Alternatively, one predictWithDiagnostics(input) call supplies diagnostics.
} finally {
  await engine.dispose();
}
```

The API preserves explicit decision and option IDs/order, snapshots inputs and serializes requests. Convenience defaults/string options are supported. The lifetime signal covers initialization and requests; disposal is idempotent. Initialization, dispatched prediction and disposal have source bounds of 120s, 60s and 5s respectively; the proof controller's stricter scheduling limits are separate. Fatal failures close the engine; recovery is explicit, not an automatic retry. The SDK does not log/persist inputs or use a remote inference fallback. Diagnostic payloads can reveal tokenized input.

The package includes built ESM, declarations, an actual module worker and a small descriptor, **not weights, ORT files/WASM, fixtures or a service worker**. A bundler may rewrite/copy the package-relative worker to a hashed asset. Deployment owns its reachable worker graph, same-origin HTTP(S) asset-directory URLs, secure context, MIME/security headers, model files, exact ORT files and optional cache implementation. The actual packed proof used non-root `/sdk-proof/models/m9/` and `/sdk-proof/ort/` bases.

Fixed versions are Transformers.js **3.8.1**, ORT **1.22.0-dev.20250409-89f8206ba4**, TypeScript **5.9.3** and Vite **7.2.2**. Infra owns the root private workspace and sole root lockfile; Runtime did not independently change that dependency graph. The final worker is **527,652 bytes**, without embedded WASM or relative static JS imports. The oversized intermediate worker and failed type-resolution builds remain retained.

## Model identity and scorer

`model.json` uses schema `jeff.browser-encoder.v1`; its declared model is `m9-msmarco-duration-20261111-01`. The SDK checks the byte length and SHA-256 of each supplied model/tokenizer buffer before use. `expectedModelId` validates the descriptor declaration. This is **publisher-declared provenance**, not signed authenticity or a reconstruction of the native checkpoint; ORT is separately staged, not a descriptor-hashed model buffer.

The original BERT state/question–candidate pair format, FP32 scalar logits, across-choice stable **T=1 softmax**, single-thread WASM and complete-pair **256-token rejection** remain unchanged. There is no sigmoid, silent truncation, tolerance adjustment or checkpoint relabeling. Another checkpoint needs its own descriptor, pins and execution evidence. Probabilities are not certified calibrated.

M13's separately completed training and independent scientific review rejected promotion because retention proper-score limits failed. M9 remains selected. There was **no M13 export, browser binding, retraining or rescue**. See [the final scientific result](../evaluation/final-sprint-results.md); Runtime did not read private final references or duplicate that scoring.

## Source, build and integration identities

| Layer | Identity / evidence |
| --- | --- |
| SDK API and worker | `e1b8e55`, then isolated-ORT-types fix **`4a1334d585bec2dd69aec9f07eb68e0fcc4c3771`**; this is the executed SDK identity. |
| Infra SDK adoption | Cherry-pick `9c34ac0`; actual SDK + web build passed around 18:35. |
| Separate package consumer | Built at **18:20:19** using an extracted `npm pack --ignore-scripts` archive, not a source alias. |
| Actual proof consumer | `consumer-02`: public factory, 4,652-byte entry, 527,652-byte worker; archive/current runtime equality recorded. Served HTML additionally includes Infra's separate offline module. |
| README-only update | Owner `b4ddfbd`, Infra cherry `1ddd278`; later prose does not alter execution identity. |
| Initial production integration | **`acfae4cc187287f47e45212f5284b569ca4aaf9c`**. |
| Final capture-only app source | **`b7de809bd01bdd58902c2ea4ea2bc468f26e7c2b`**, integrated **`07c7d4fe1f39b95f95eaa6b77470e801e2ea200e`**. Actual served app manifest `19876c1858b65fc905679d25`. |

Source/build/packaging evidence is not inference. Report publication is another revision, not a replacement execution identity.

## Actual packed-SDK online proof

The successful **online-02** phase ran in Safari **27**, with a secure, cross-origin-isolated localhost document and the actual WASM worker. Browser interval: **19:12:04.439–19:12:05.929 UTC**; controller closure: **19:12:06.300334**. Exactly **one initialization, six attempted/completed calls and 24 raw probabilities**: first three `predict`, last three `predictWithDiagnostics`. No warmup or extra call. The receipt records no errors, observed finally/disposal and confirmed controller closure.

Evaluation independently compared the saved outputs and separately reviewed the functional execution evidence:

- Maximum **as-recorded** probability drift **8.8668822495474586e-7**, below **1e-4**; canonical tops **6/6** exact.
- Finite/range checks and sum deviation **≤1e-6** passed, with exact submitted input, semantic option IDs and ordering. No normalization, clipping or smoothing.
- Three detailed calls: **9 matrices / 1,668 integers exact**, including shapes and positional option rows. The **three plain calls remain token-unverified**.
- Functional disposition: **ACCEPTED, bounded online packed-SDK `/sdk-proof/` only**. Actual served entry/worker, public calls, descriptor validation, histories and source-supported worker termination join the arithmetic evidence.

This is independent **saved-evidence review**, not an independent operator rerun. Native option-row ownership is source-supported by ordered flattening and actual post-forward capture; records lack self-describing option-row IDs/rendered-text hashes. No universal tokenizer equivalence, quality, calibration, generalization, all-browser, controlled latency or long-input claim follows.

Exact local Evaluation records under `artifacts/evaluation/final-sprint-20261112-01/`:

- `sdk-online-comparison-v1/report.md` — SHA `e5324b2adbb3ca09f910856d5d28c37d96ec18b7adf5874e814c643f864d9a06`.
- `sdk-online-comparison-v1/result.json` — SHA `72450eacad8bfdd1959e7770ff8f5325b6338f5ad78dde2fefaea2282c33b8f3`.
- `sdk-functional-review-v1/report.md` — SHA `c310be2689d49fb3f4700a881d57c0e360ea66f787947c0286718910c05af7db`.
- `sdk-functional-review-v1/receipt.json` — SHA `d72f2ccd54a0cf30ed6503b3ac05b2078baad8e881dbc19bcf888f5c696357ce`.
- `diagnostic-binding-review-v1/report.md` supplies the qualified native positional binding.

## Preserved failure, accounting and offline gap

Original activation `9962e791-baf9-463e-8882-ce660eb95bb1` was issued **19:03:38.530309**, with deadline **19:15**. **Online-01 failed before browser contact at 19:07:42**: outer 55s equalled stage 45s plus cleanup 10s, leaving no validation margin. External time **0.02s**, conservative charge **2s**. No model/worker/tokenizer call occurred. Its original `closure_confirmed:false` remains: no browser finally existed, not evidence of a live worker.

Explicit renewal `d3e2f108-cc50-4c95-9ba4-0603cf432559` at **19:11:12.712543** changed only stage **45→40s**, preserving the 55s outer cap, original deadline, SDK, inputs and host. Online-02 took **2.10s external / 4s charged**. Combined shared ledger: **6/300s CLOSED**; unused **294s is not authority**. All attempts and original fields remain intact. Recorded browser time, controller time, external time and conservative charges have different scopes and are not additive latency measurements.

Cache preparation completed **19:12:37.991**: **10 assets / 103,406,073 bytes**, version `0cf646f414d61b147cf6f064`, matching scoped controller. This checked presence/recorded lengths, not browser cryptographic integrity.

Infra reported actual server signal **19:14:04.712124**, PID absence **19:14:04.716081**, and refusal errno61; sent **19:14:04.751473**. Runtime read at **19:14:20**, after the latest full-55s start **19:14:05**. **No offline phase, fresh-document navigation or inference was attempted.** The cap/deadline was not shortened or extended to manufacture proof. Cache completion and host shutdown do not establish offline inference or whole-machine offline operation.

Known inference closure was **19:12:06**; chain return was actually sent **19:15:54**, not backdated. Own proof tab23 closed/control released **19:16:48**. Infra later restored a **new PID81264**, HEAD200 **19:17:30.530923**. Later production hosting used Infra PID93888/launcher93851; its scheduled **23:15** expiry is not an observed future shutdown. Runtime does not supervise that independent finite static host.

Browser RSS and peak remain **unknown**. Sampled normal pressure is not continuous monitoring, an 8GiB certification, MPS headroom, OOM diagnosis or global absence of user workers.

## Final production applications: built, acceptance unattempted

The user approved both comfortable layouts. Queue and chat are genuine lazy SDK consumers with separate manual actions; the generic editable playground remains available. Queue/chat capture-only `window.jeffApp` exposes successful in-memory raw histories, state and disposal, **not a separate prediction route**. History contains `{input,prediction,engineMetadata,wallMs}`; errors are not invented as successful records. There is one lazy engine per page, not one cross-page SPA engine.

The new frozen acceptance packet specified exactly two queue cases, two chat cases and two playground cases; four normal-button/simple calls plus two explicitly preselected generic-bridge detailed calls, three serial engines with disposal before successors. No new native reference was generated. Packet SHA: `7fab64e0ed2a740a6946e49d66c08975d3360eba46b91158bb9d7d610e4da291`.

- Infra's actual capture build became available **20:11:00**, later than its estimate.
- Runtime completed static readiness **20:13:30.396205**: three fresh owned query-marked pages, zero histories, null engine metadata, no attempt. Fifteen served small HTML/JS/CSS/worker bodies matched the published graph pins. Model/ORT pins remained Infra inventory evidence; there was no model load.
- Runtime proposed one aggregate **55s controller / 40s stage**, stricter than Model's conditional three-page **180s** allocation. **20:05 was a READY target**, not a grant or execution deadline.
- Model picked up READY at **20:15:09**, after its **20:15** availability ended. **No activation was ever issued.** Runtime did not launch the controller, initialize a model or predict. New charge **0s**; shared ledger stays **6/300s closed**.
- Runtime read the closure notices at **20:22:56**. All three owned preparation tabs were closed and control released by **20:24:03**. Closing the first shifted the other handles; stale close attempts were refused, then the two uniquely query-marked, non-selected task pages were rebound and closed. No selected/user/Infra tab was closed.

The actual result is **UNATTEMPTED**, neither numerical/functional PASS nor FAIL. Static source readiness is not app inference acceptance; SDK proof and historical B2 offline proof cannot substitute. Preserved preparation is not a runnable grant or a guarantee of controller correctness. Future execution needs a new explicit bounded handoff and fresh readiness. See [Evaluation's closure](../evaluation/final-sprint-results.md).

## Local model-only handoff

A separate authorized, **local-only** M9 archive was prepared without export, model execution, new dependencies or uploads:

- `artifacts/release/m9-model-handoff-20261112-01/m9-model-only.tar.gz`: **83,460,462 bytes**, SHA **`19efaf76ccb97264b9461288a8e7d221738370204e295779e74283c1e73d6592`**.
- Exactly four pinned model/descriptor files plus seven notice/documentation/checksum files; no ORT, wheels, native checkpoint, fixtures, training or evaluation data. Exact member allowlist/content hashes were checked.
- Base `cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`. Retained pinned card declares Apache-2.0. Canonical Apache text, pinned card, attribution and prominent fine-tuning/export/tokenizer modification notice accompany the bundle. Canonical text is not misrepresented as a LICENSE retrieved from that model repository.
- Flat SDK placement and the current web copier's nested tokenizer export layout are documented separately. The flat archive is not directly a `--model-dir` export layout; SDK/ORT/runtime installation remains separate.

**No weight publication was performed or authorized by this preparation.** First-party licensing, applicable provider/account/training-output rights, upstream-corpus and deeper-base attribution decisions remain unresolved. Model-card licensing is not blanket legal clearance; source visibility is not weight-upload authority. The local bundle does not by itself make a public clone runnable or prove inference.

## Local evidence index

Under `artifacts/release/final-sdk-20261112-01/`: `consumer-02/binding.json`, `host-source-01/receipt.json`, `online-01/`, `online-02/{receipt.json,controller-return.json}`, `cache-prepare-01.json`, `browser-control-return-01.json`, retained build logs and source preparation. The old delivery summary's then-pending review/restoration fields remain chronological evidence, not current status.

Under `artifacts/release/final-app-20261112-01/`: `preparation/{readiness.json,source-binding.json,plan.template.json}`, original source-only draft and `closure.json`. The plan retains no actual activation. Infra's `artifacts/infra/final-sprint-20261112-01/app-inspection-publish.json` records the app graph. Model-only archive metadata/notices are in its separate local directory above. No protected final/retention reference access, duplicate scientific scoring or inference occurred for publication.
