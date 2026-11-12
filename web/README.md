# Local Jeff apps

Three small browser apps use the built public `@jeff/sdk` package:

- **Requests** (`/`): a local request queue with editable text, explicit model suggestions, relative scores and a separate manual routing action.
- **Messages** (`/chat.html`): a transcript/composer with explicit sentiment suggestions. Positive → 🎉, negative → 💛, neutral → 👍 and mixed → 🤔 are display mappings, not separately predicted social reactions. User changes remain distinct from model suggestions.
- **Playground** (`/playground.html`): editable context, question and two to six choices, with all six workspace examples and the six released sentiment examples available as presets.

Both dark layouts use the approved comfortable density. There are no gallery controls, invented human reactors or external workspace/chat integrations. Ordinary buttons call `predict` once; optional diagnostics do not require a second prediction. No model loads on page mount. Inputs, results and local routing state stay in memory, not persistent storage or telemetry.

## Run locally

From the repository root, with Bun 1.4.4 installed:

```sh
bun install --frozen-lockfile --ignore-scripts
bun run demo
```

Open **http://127.0.0.1:4174/**. The fresh default origin avoids silently reusing the historical B2 worker on port4173. Do not unregister unrelated/user service workers.

There is one root workspace/lockfile for `sdk` and `web`. The launcher stages explicit assets, builds the SDK before its web consumers, then serves only `web/dist` on loopback. It does not install dependencies, download/export a model, run inference, expose a repository/artifact root, or provide an inference API. The server supports static GET/HEAD with isolation/security headers and rejects path escape and symlinks.

Default lifetime is **7200 seconds including staging/build**, maximum14400. Ctrl-C stops its child process group. An absolute UTC cutoff can shorten, never lengthen, that lifetime:

```sh
bun run demo --port 4174 --duration-seconds 7200 --stop-at FUTURE_UTC_ISO_TIMESTAMP
```

Replace the placeholder with a real future timestamp. The final-sprint review host's2026-11-12T23:15:00Z cutoff is historical, not a reusable date or a promise of monitoring after parking. Static-server shutdown does not establish that user-owned browser models are absent; a prepared browser page may still work without the server.

### Assets and model identity

Defaults resolve artifacts through Git's common directory, not the working directory or `/tmp`:

- Export root: `artifacts/release/browser-b1-20261112-01/export-01/assets`.
- Descriptor: tracked `sdk/models/m9.json`.

These local artifacts are not downloaded by the command. A checkout without them needs an explicitly provided compatible export. Override with `--model-dir ABSOLUTE_EXPORT_ROOT --descriptor ABSOLUTE_MODEL_JSON`.

`web/model-config.json` selects the label, asset/ORT base paths and expected model ID. The copier rejects a descriptor that differs from that selection or the supported FP32/256-token/state-question-candidate/T1 encoder contract. It verifies descriptor pins before copying only `model.json`, the model, two tokenizer files and two exact installed ORT files. Existing matching outputs/provenance are reused; conflicts/partials are preserved and rejected, not overwritten. Installed ORT symlinks are explicitly resolved for Bun's isolated linker; model/output paths still reject symlinks. Local provenance stays outside the served tree.

The SDK checks the actual model/tokenizer buffers against descriptor byte lengths and SHA-256 before use. An expected ID checks identity rather than giving arbitrary assets an M9 alias. Descriptor/checkpoint metadata remains a trusted producer binding, not a signature or independent checkpoint reconstruction. A future compatible model requires explicit selection and its own descriptor/assets; it is not promoted by renaming M9.

No P11 fixture is required for ordinary SDK/app use. The legacy optional `--inputs ABSOLUTE_P11_JSONL` stages only the exact hash-bound original three-row P11 file; it is not used by these apps or required in their cache. No labels, protected evaluation inputs or general artifact directories are copied.

## Behavior and API

- Editing invalidates the prior suggestion and route confirmation. Request/message revisions prevent stale completions from replacing edited state.
- Model loading reports actual per-asset bytes when known; inference is not presented as a fabricated percentage. Errors and overlength inputs remain errors, not invented output or silent truncation.
- Returned scores require exact option coverage, finite[0,1] values and sum deviation≤1e-6. The host does not clip or renormalize them. Exact ties remain explicit and input order is retained.
- Queue/chat share a lazy session within each page; the SDK serializes its work. Page exit aborts the owned session. Back/forward restoration keeps in-memory UI while creating a fresh lazy session.
- Ordinary user app use does not require the agents' internal experiment reservations.

The playground retains a programmatic bridge for explicit local use:

```js
window.jeffBrowser.loadDecision(input);
const simple = await window.jeffBrowser.run(input);
const detailed = await window.jeffBrowser.run(input, { diagnostics: true });
await window.jeffBrowser.dispose();
```

These are **two separate calls if both example lines are executed**. Use only the desired method for a decision. `run` defaults to public SDK `predict`; opt-in diagnostics use `predictWithDiagnostics` once. Receipts retain caller IDs and successful-only cloned history; simple receipts have no fabricated token matrices/inference timing. Disposal retains the last actual comparison. See [`sdk/README.md`](../sdk/README.md) for standalone package use, including deployment without this repository's fixtures.

## Offline preparation and evidence boundaries

The playground's explicit preparation action covers all three app pages, their emitted module/worker graph, the selected model descriptor/model/tokenizer and ORT assets. Streaming lengths, completed writes and a completion marker precede immutable worker registration. Readiness also requires the matching activated controller. No auto download, forced worker replacement, old-cache deletion or prompt/result caching occurs. Notices are adjacent assets, not part of this minimal offline graph.

Quota/storage/unsupported-browser errors remain visible. Updates can require closing old app tabs and reopening; preparation bypasses the old worker while ordinary runtime requests can use its complete cache. Storage can later be evicted. **Cache completeness is not a fresh browser SHA-256 audit:** same-length wrong cache bytes are not excluded by preparation alone. SDK model-buffer checks are separate.

Current final-sprint evidence:

- The actual independently packed SDK consumer completed one M9 initialization and six online predictions: first3 simple, last3 detailed,24probabilities. Evaluation's saved-output comparison passed with max absolute drift **8.8668822495474586e-7≤1e-4**, six matching canonical tops and raw sums≤1e-6; no normalization. The three detailed cases matched9matrices/1668integer entries. Plain-call tokens remain unverified.
- This was the isolated `/sdk-proof/index.html` consumer, **not inference through the production queue/chat/playground buttons**. Package/source, operator/lifecycle and saved-output arithmetic evidence have distinct roles. Runtime owns execution; Infra did not run a model.
- The first controller attempt stopped before contacting the browser because of preflight time arithmetic;2seconds were charged. Explicitly renewed online execution charged4seconds. The closed chain total is6/300seconds; unused seconds authorize nothing.
- Its scoped10-file cache became ready and the server actually stopped at19:14:04.712124UTC. Runtime received the stop after its latest capped start, so **fresh server-unavailable navigation/inference was not attempted**. New SDK/product-graph offline inference remains unverified. Historical B2 success does not fill that gap.

Local receipts: `artifacts/release/final-sdk-20261112-01/`; Infra staging/composition/lifecycle/build evidence: `artifacts/infra/final-sprint-20261112-01/`. Independent comparison was delivered by Evaluation in messagee5271405-8393-40b4-9f24-0fef8972b0b4. Later publication or UI builds are not retroactive execution provenance.

### Example and capability limits

The queue uses four curated S1 routine workspace inputs; both boundary inputs remain available in the playground. Input text, questions and option identity/order are retained; display titles/short labels are not model features. The six sentiment examples are exactly the separately released SDK packet positions1–4/13–14, without correctness filtering. Production hosts contain no saved predictions pretending to be live.

S1 workspace agreement was9/12preferred and11/12acceptable across six cases/two renderings, not twelve independent cases. S2 M9 matched13/16 authored sentiment references, with negative-class agreement only2/4. These small synthetic development checks do not establish general accuracy, calibration or socially appropriate reactions. No protected64cases or targets are bundled.

The original B1/B2 M9 worktree, evidence and accepted historical server-unavailable proof remain separate; see [`docs/runtime/browser-b2.md`](../docs/runtime/browser-b2.md) and [`docs/evaluation/browser-b2.md`](../docs/evaluation/browser-b2.md). Qwen is not a normal app/SDK choice; its earlier initialized-but-pressure-stopped attempt returned no predictions or parity result and is not retried here.

## Notices

`web/public/notices/` retains the bounded upstream notices and inventory from B2. It is not exhaustive binary attribution, a first-party redistribution grant, dataset/teacher/demo-text rights clearance or permission for public release. Current serving is local only.
