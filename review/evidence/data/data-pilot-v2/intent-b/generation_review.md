# intent-b generation review

## Delivery

- Shard: `data-pilot-v2-intent-b-r1`; 200 new training rows and 40 new validation rows. No parent rows included.
- 240 preassigned singleton groups, `data:pilot-v2:intent-b:g001`–`g240`, each with `:r01`. Assignments were written before source cases; domains and splits stayed frozen.
- Exactly 20 assigned training domains and four assigned validation domains, ten separately authored scenarios each. No Cartesian expansion, paraphrase generator, or historical examples used.
- Every state, candidate set, and label was authored in this existing agent session (`openai` / `gpt-sol`). Python only compiles the authored choices and performs structural validation; it does not invent scenarios or determine semantic labels.
- Source, assignment, and generator revisions and SHA-256 hashes are in both metadata and the validation report. Recompile with `python3 generate.py` from this directory with the recorded teacher environment available.

## Content review

The same author reviewed the requests for a single actionable scope: repair versus replacement; a single booking field versus cancellation; receipts versus reimbursements; instructions versus delegation; and rejected offers followed by a clear alternative. Names, case notes, and transactions are synthetic, not private records. Candidate wording uses action descriptions rather than a fixed class vocabulary.

The ten highest local cross-split lexical pairs were reviewed. Maximum stopword-filtered state Jaccard is 0.2174. Most share generic payment-document requests (`g175/g208`, `g167/g208`, `g076/g208`, `g155/g208`, `g175/g226`, `g014/g226`). Other pairs concern completed-return evidence versus transcription billing (`g197/g235`), shoe-job versus tagged skate-job readiness (`g164/g223`), declining an audition versus declining large print (`g040/g240`), and service-location versus registered-address corrections (`g013/g202`). These are separate authored service situations, not related source cases. Generic intent categories are intentionally shared across domains; this review does not prove semantic disjointness.

## CPU validation

- Exact row counts, required fields, supplied targets, option IDs, unique row IDs, group isolation, frozen assignment mapping, and reserved-domain assignment exclusions passed.
- Zero exact state duplicates, normalized-state duplicates, canonical-input duplicates, or cross-split group overlaps within this shard.
- 236 rows use three or four choices; four rows use five or six. Target positions are independently randomized and balanced to within one row per split/option-count bucket. Singleton five/six-choice buckets cannot establish position balance statistically.
- Unique longest targets: 45/200 training and 8/40 validation. Unique shortest targets: 10/200 and 3/40. Unique maximum state-word-overlap targets: 76/200 and 16/40. Length/overlap shortcuts are quantified, not claimed absent.
- States are 18–28 whitespace-delimited words; maximum regex word counts are 28 for state, five for question, six for an option, and 38 for state + question + one option. These are word counts, not tokenizer counts.
- Two final consecutive compilations reproduced identical train, validation, metadata, and validation-report bytes. No tests, linting, API calls, network requests, tokenizers, or model loads were used.

## Boundaries and limitations

All files written are under this producer's private artifact directory. No Git operations, checkout edits, parent examples, other producer files, or evaluation data were accessed. Additional and pending spend are both GBP 0. Original synthetic content remains subject to existing provider terms; no independent redistribution licence is claimed.

Semantic review and labels came from the same teacher and are **not independent correctness verification**. Teacher immutable revision and sampling details are unavailable. Parent still owns the 256-token audit, historical/cross-producer overlap checks, and separate-session teacher spot review.

## Frozen output hashes

- `train.jsonl`: `0a0a9bbd453ae050e9364b9174f2c54e2191eba48aa679f2058efed2d497e1e7`
- `validation.jsonl`: `7f849e8b21082c64635e1b3620cb787f4393af02e6ce2dceb22c4de90948dd7c`
- `metadata.json`: `2db9e09ac189049d93f86ead8ec9f30f437f267d3b55d577107cfe0d9f311559`
- `validation_report.json`: `706ef66a82290c0ebe4705d6cdd1b32025b15a5d786372f5d374a3d462f63b09`
