# P5: M7 saved-checkpoint reload

One already-completed fresh-process MPS pass reloaded the self-contained M7
Hugging Face directory through the existing flat checkpoint contract. No new
runtime implementation was needed. This delivery documents evidence only; it
runs no model/tokenizer, weight scan, fixture, test or lint, and reads no TRAIN
rows, Evaluation references or protected final content.

## Identity and coverage

Runtime is frozen at `7a5af91ed352c648ff64bff6ab9f5bdb240302c1`, with unchanged
P4 validator and P3 renderer, loader, readout and configuration. The final M7
manifest SHA-256 is
`70163c8567781bb7151b11c125999ea4bc6ec1ff52af52c52a205f9f4dbdd022`.
Trained weights are 1,976,163,472 bytes, SHA-256
`cf570cbe4ad2f847509ad6cdedb96085e3f4740c04c37889b9051dc08adc54c2`;
these are **not upstream original bytes**. Base lineage is
`Qwen/Qwen2.5-0.5B-Instruct` at
`7ae557604adf67be50417f59c2c2f167def9a775`. Model owns actual training code
`574774d631d707de9398c80dc5b936d9563e386c`.

| Unchanged input suite | Completed presentations | Valid option probabilities | Suite wall |
| --- | ---: | ---: | ---: |
| Original | 300/300 | 1,160 | 16.474 s |
| Reversed | 300/300 | 1,160 | 17.964 s |
| Already-paired probes | 24/24 | 70 | 1.279 s |
| Total | **624/624** | **2,390/2,390** | **35.717 s** |

Three fixed **unscored startup rows are separate** (0.337 s). Label-free
schema/identity/option/normalization validation completed; maximum probability
sum error was about 1.84e-7. No extra START, retry, order, fallback or new cases.

## Actual process and observed resources

- UTC: **2026-11-11 17:18:29.486849–17:19:08.558254**, exit **0**.
- External wall **39.071 s** (exact receipt value 39.07104558264837 s), including
  interpreter/import/hash-tokenization preflight, load, startup, full pass and
  output. Local model load 0.392 s; suite throughput 17.471 decisions/s.
- CPU lifetime maximum RSS **552,632,320 B**; native macOS peak process footprint
  **3,133,490,328 B**. Observed MPS current allocation 2,013,552,384 B after load,
  startup and suites; largest sampled driver allocation **2,768,977,920 B**.
  These are overlapping, nonadditive accounting scopes; samples are not MPS or
  system/unified-memory peaks.
- Fresh HOME/HF cache, local-only loading and offline environment flags; cache
  remained empty. This is not OS network denial or offline-installation proof.
  OS caches were not flushed and memory mapping was not traced: no cold-storage,
  comparative speed or comparative memory claim.
- Model grant `558f98d8` returned; wrapper/child PIDs **22652/22653 absent** per
  completed handoff. No Runtime ML process/subagent remains; actual/pending
  additional spend **£0**. No new slot or process was started for this report.
- Stderr retains the tokenizer regex warning and `torch_dtype` deprecation.
  No loading/configuration change or corrective rerun was made.

## Evidence and interpretation

Root evidence directory:
`/Users/destiner/Code/jeff/artifacts/release/p5-m7-20261111-01/`.
`delivery-summary.json`, `output-validation.json`, `process-receipt.json` and
`process.stderr.log` record actual results. The compact committed
[manifest](../../manifests/releases/p5-m7-20261111-01.json) freezes exact summary
values, input paths/hashes, output paths/hashes, checkpoint/base/training/config/
source pins, environment, process and resource facts. It also binds the small
report source files. Existing actual audit/predict hashing is distinct from
this reporting step, which performs **no new weight scan**.

Completed handoff:
`artifacts/handoffs/release/20261111T1720-P5-predictions-ready-slot-returned.md`.
E7 already has outputs via `4c6ad1fc-28bf-4c5c-b176-bc6b0fb51bc6` and independently
scores them; this documentation is not a scoring gate.

This establishes **runtime coverage and reload success**, not learning quality,
held-out transfer, calibration or default promotion. Model reports mixed TRAIN
fit: overall intent/sentiment improved, but rules agreement fell **184→176**
despite lower cross-entropy. No TRAIN rows were inspected here; argmax counts do
not establish causes or ties. Preserve the P4 negative result and R6 separate
original evidence unchanged.

Documentation source review and `uv build --no-sources` are the only delivery
checks; build log: `artifacts/release/p5-m7-20261111-01/report-build.log` at root.
No new runtime/framework/bundle/Linux/dependency work was added.
