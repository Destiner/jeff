# P10 — M11 encoder checkpoint runtime

**Completed and Model-verified closed, not promoted.** This publication indexes retained execution metadata for `artifacts/release/p10-m11-20261112-01/`; it does not rerun inference or score predictions. The [release manifest](../../manifests/releases/p10-m11-20261112-01.json) records exact output and receipt SHA-256 descriptors from the Model closure.

## Actual Runtime pass

One fresh M11 encoder load produced **720 decisions, 180 attempted/completed native batch calls, 2,751 probabilities and zero startup calls**. Suites are original development 300, reversed development 300, already-paired probes 24 and D3 seen-mechanism rules 96. Reversals are not independent cases; the D3 policy pairs are distinct cases, not reversals. This is a Runtime prediction pass, not producer training.

The process receipt records zero exit, complete driver evidence and absent process group. Model's terminal closure records no active groups and label-free output/hash/ordered-option/counter checks; maximum recorded normalization error is `1.553006114818345e-07`. These are retained execution claims, not a fresh independent replay.

| Accounting scope | Seconds |
|---|---:|
| Parent entry through publication | 37.59575429186225 |
| Conservative Runtime charge | 39 |
| Producer training plus final TRAIN fit | 809.8467665826902 |
| Charged chain / ceiling | 848.8467665826902 / 1500 |
| Runtime cap | 120 |

The charge rounds upward and includes a one-second publication allowance. This is not a controlled latency benchmark. Unused allocation grants no new work. Runtime controls remain FP32/MPS, no fallback, batch four, four threads, cap 256 and temperature 1. Recorded RSS/driver/headroom checks have distinct sampled or lifetime scopes; recommended headroom is not physical free RAM or a continuous peak guarantee.

## Producer and quality boundaries

M11 is a fresh original MS MARCO start trained for **30 total epochs, 11,250 updates and 45,000 presentations**, not continued M9 training. [Model's results](../model/m11-msmarco-duration30-results.md) retain the exact source/recipe, TRAIN fit, resource accounting and historical qualifications. Source/build inspection alone is not native execution proof; the process/native receipts and Model closure are separate evidence.

[E12](../evaluation/e12-encoder-duration30.md) owns quality: improved TRAIN fit did **not** deliver broad development improvement over M9. New agreement falls 165→162/240 while NLL/Brier worsen; inherited results regress. Sentiment/probe gains remain alongside intent/rule losses and the probe Brier exception. D3 gains three agreements and three complete policies but worsens both proper scores, worse than every retained D3 baseline. No broad transfer, calibration, mechanism mastery or promotion claim follows. Reused development, teacher/reference truth and D3 construction/reviewer qualifications remain unchanged; the full report retains source/family/policy regressions.

## Evidence and publication limits

- Canonical root: `/Users/destiner/Code/jeff/artifacts/release/p10-m11-20261112-01/`.
- Terminal Model closure: `/Users/destiner/Code/jeff/artifacts/model/m11-msmarco-duration30-20261112-01/p10-return.json` (resolved through public Model metadata; not under `night-20261112`).
- Manifest pins `process-invocation.json`, `process-receipt.json`, `binding.json`, `run/receipt.json`, `delivery-summary.json` and all four prediction outputs. Output bytes were not reread or rescored for this publication.
- The artifact README is historical source-only preparation, not the terminal execution status. Preparation does not supersede completed receipts, nor do completed receipts erase its operational qualifications.

No evidence or executed tree was modified. No ML/tokenizer imports, weights, protected final/reference/input access, new scoring, tests/lint, network or experiment belongs to this documentation task. Packaging verification is separate from runtime and quality evidence.
