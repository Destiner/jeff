# P4 trained-checkpoint runtime evidence

## Result and decision boundary

One actual fresh process accepted and reloaded the saved M6 trained checkpoint
and completed **624/624 development presentations and 2,390/2,390 option
probabilities**, exit 0. This establishes local read-only checkpoint acceptance,
reload and output-contract coverage, **not successful learning or promotion**.
Model reported TRAIN-fit regression and first-position degeneration. Runtime did
not open TRAIN rows, reference labels or protected final data and did not score
quality. E6 independently owns held-out scoring; outputs were delivered under
handoff `6e22b1f8`. No E6 quality result is asserted here, and normalized
probabilities are not evidence of calibration.

The executed runtime was frozen at
`264c44349c3eee73e539a200645abe7d9c50169c`. The additive
[checkpoint contract](p4-checkpoint-contract.md) reused the original P3 loader,
prompt, tokenizer, scoring and inputs without adjustment. No new loader,
training, retry or inference was performed for this documentation delivery.

## Identity and provenance

The small [release manifest](../../manifests/releases/p4-m6-20261111-01.json)
records exact source/config/template digests, trained lineage, input/output
hashes and evidence identities. Artifact root:
`/Users/destiner/Code/jeff/artifacts/release/p4-m6-20261111-01/`.

The actual checkpoint identity is the manifest at
`/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/checkpoint-manifest.json`,
SHA-256 `1fe8f6d169301c76698b78b8d7b067c4b10868fb755324896352d1f61310960f`.
Its producer IDs `training-checkpoint` / `training` are not globally unique
identifiers. The manifest and trained byte identity were revalidated against
frozen audit evidence before loading the sibling `checkpoint/` HF directory.
The trained FP32 safetensors are 1,976,163,472 bytes, SHA-256
`ecbeb36556281cf00e9175603aecefd83f2ce3fc8a610e4b2cf056b7a4a926fb`.
`Qwen/Qwen2.5-0.5B-Instruct` revision
`7ae557604adf67be50417f59c2c2f167def9a775` records starting lineage, not a claim
that trained bytes equal upstream bytes. Training receipt/data/recipe/schedule
hashes are provenance bindings, not independent verification of training quality.

## Actual execution and coverage

The external process ran **2026-11-11 16:10:46.886945–16:11:27.420722 UTC**,
wall **40.52782383421436 s**. This includes interpreter/import, hash/tokenization
preflight, model load, startup, full pass and output. Local saved-model load was
0.7096073748543859 s. Three fixed startup rows were separate from coverage.

| Suite | Presentations | Probabilities | Full-suite seconds | Forward latency p50 / p95 (s) |
| --- | ---: | ---: | ---: | ---: |
| v2-original | 300/300 | 1,160 | 17.09163008304313 | 0.056224165949970484 / 0.06624379102140665 |
| v2-reversed | 300/300 | 1,160 | 18.424006334040314 | 0.06085362518206239 / 0.0741504579782486 |
| probes-paired (already paired) | 24/24 | 70 | 1.3028197912499309 | 0.05383095797151327 / 0.05760437482967973 |

The full suite took 36.81845620833337 s, 16.948021841794816 decisions/s.
The probes were not doubled again. Label-free `output-validation.json` checks
schema, IDs, option coverage, finite probabilities and normalization; maximum
sum errors were 1.341104507446289e-7, 1.043081283569336e-7 and
8.940696716308594e-8 respectively. These are not accuracy measurements.

Execution used macOS 26.7.1 arm64, Python 3.12.16, Torch 2.15.0,
Transformers 4.57.6, safetensors 0.8.0 and tokenizers 0.22.2, on MPS.
Model grant `e34dfed8` was returned immediately; wrapper/child PIDs 86734/86735
exited and no Runtime Model process remained. Additional actual/pending spend:
£0. No further run is needed for E6 to score these saved predictions.

## Memory and offline qualifications

- CPU process-lifetime maximum RSS: **554,598,400 B**. This is not total unified
  memory and does not establish a memory advantage.
- Maximum **observed** MPS driver sample: **2,777,350,144 B**, not a true peak.
  Current allocated bytes at load/startup/end were 2,013,552,384 B.
- Native macOS peak process footprint: **3,143,828,608 B**, a separate OS metric,
  not a true MPS/unified-memory peak. These metrics overlap: do not sum them.
- FP32 safetensors were memory-mapped; OS caches were not flushed. Fresh process
  and empty application caches do not demonstrate cold-storage performance.
- The existing loader used local-files-only plus offline environment flags,
  a new empty HF cache and HOME; the HF cache remained empty. This is not an
  OS-level network-denial demonstration or fully offline installation evidence.

## Evidence and verification scope

`delivery-summary.json` is the compact factual source; `output-validation.json`,
`process-invocation.json`, `process-receipt.json`, `process.stderr.log`,
`audit/audit.json` and `run/receipt.json` retain the execution evidence. The
exact delivery and limitations are also recorded in
`artifacts/handoffs/release/20261111T1612-P4-predictions-ready-slot-returned.md`.
The committed release manifest references hashes already recorded in that
summary; this reporting pass did not rescan weights or rerun the model.

This docs/manifest change is source-reviewed and package-built with
`uv build --no-sources`; build log:
`artifacts/release/p4-m6-20261111-01/report-build.log` at the repository root.
Packaging success is separate from the earlier executed runtime evidence.
No tests or linting were run. There are no new Linux, offline-install,
checkpoint-bundle, publication-rights or comparative inference-performance
claims. P1/P2/P3 historical evidence and limitations remain unchanged.
