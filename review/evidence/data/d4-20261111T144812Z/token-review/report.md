# D4 selected-input token/rendering cross-check

**No selected rule/state, question, or choice tokens were lost at the native256 cap. Truncation is not demonstrated on this sample.**

Exactly the predeclared 24 old TRAIN objects (identity/group matched against selection.json), 86 candidate pairs, 14 source-mechanism groups. Full pair lengths, including special tokens: min53, median69, p95 105, max113. Native256 longest-first/right: 0/86 over budget; 0/86 state/rule-loss, question-loss, or choice-loss pairs. All86 capped token-ID sequences equal their untruncated sequences, not merely equal field counts. No128 contrast run.

## Source-group denominators

All groups below have zero loss at256; lengths are full pair token extrema.

| Source / group | Rows | Pairs | Tokens |
|---|---:|---:|---:|
| inherited v1 g01 | 1 | 4 | 104–105 |
| inherited v1 g04 | 1 | 3 | 84–85 |
| inherited v1 g07 | 1 | 4 | 106–113 |
| inherited v1 g10 | 1 | 3 | 97 |
| rule-a g001 | 2 | 6 | 59–68 |
| rule-a g002 | 2 | 6 | 92 |
| rule-a g003 | 2 | 8 | 99 |
| rule-a g005 | 2 | 8 | 56–57 |
| rule-a g007 | 2 | 8 | 53 |
| rule-b g002 | 2 | 8 | 69 |
| rule-b g005 | 2 | 6 | 57–58 |
| rule-b g006 | 2 | 8 | 68–70 |
| rule-b g008 | 2 | 8 | 80–81 |
| rule-b g010 | 2 | 6 | 65–66 |

Source totals: inherited4 rows/14 pairs/4 groups; rule-a10/36/5; rule-b10/36/5.

## Current consumer and rendering

Current Model worktree `src/jeff/model/scorer.py` (`CandidateScorer`) and `cross_encoder.py` (`RetainedCrossEncoder`) formatter expressions were read as AST, not imported or initialized. Both produce `(State:\n{state}\nQuestion:\n{question}, Candidate:\n{option.text})`. Actual24 rows/86 renderings matched both expressions with only state/question and choice text available to formatter evaluation. Target, provenance and IDs are not interpolated; IDs in evidence files are audit metadata only. Consumer validation/option counts are not text fed to the tokenizer.

`review.json` pins SHA-256 of both current consumer source files, Research helper, pinned tokenizer JSON, selection, selected-reference, and audit script. `rendered-pairs.jsonl` records every actual rendering and exact-ID preservation. `helper-report.json` independently records the existing Research helper's native256 question/choice audit using `subset-manifest.json`, an audit-only manifest pointing to the unchanged existing selected-reference file, not a dataset release. The supplemental check covers state/rule token preservation omitted by that helper's field-loss counters.

Executed with existing Model `.venv/bin/python -B` directly and local tokenizers0.22.2. No model imports, weights, initialization, inference or training; no installs, network, tests/lint, Git/mailbox, or other example reads. Writes restricted to this new token-review directory.

This is a currentselected-input cross-check: the existing full-v2 audit already passed256, not a new claimed discovery. Purposive paired rules-only TRAIN examples are dependent, not held-out evaluation or a whole-dataset estimate. Preserved input tokens do not establish target correctness, model learning, calibration, or generalization; no claim that all data/model learning is sound. Original TRAIN identity relies on selection's existing pins; original full shards were deliberately not reopened.
