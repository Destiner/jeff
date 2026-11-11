# rule-b generation review — data-pilot-v2-rule-b-r1

## Delivery

- **200 new train + 40 new validation rows**, all `rule_application`; no parent rows counted or consumed.
- Frozen `group_assignments.json` was written before source authoring. Full IDs are `data:pilot-v2:rule-b:g001`–`g015`; groups 001–010 contain 20 train rows each and 011–015 contain 8 validation rows each. No mechanism crosses splits; topological ordering is validation-only.
- **100 train + 20 validation policy instances**, each with two related cases and a shared `provenance.scenario_id`. All 120 pairs produce distinct outputs. These are policy instances, not 240 independent mechanisms or real-world observations.
- Original author: existing approved agent, provider **openai**, actual model alias **gpt-sol**. Immutable revision and sampling settings unavailable. Additional/pending spend: **£0/£0**.

## Source and reproduction

`author.py` saves the explicitly authored source policies/facts to `authoring_cases.jsonl`. `generate.py` renders text, calculates targets, builds same-style distractors and balances randomized target positions (seed 761903). `audit_cases.jsonl` contains IDs, scenario IDs, policy rules and facts, without saved answers. `audit.py` exports pure `expected(case) -> answertext`, with no generator or target imports.

Executed locally, standard-library CPU only:

```sh
python3 author.py
python3 generate.py
python3 validate.py
```

All **240/240** generator targets agreed with the separate audit implementation before any row was emitted as `rule_verified`. Different implementations include matrix composition versus coordinate mutation, exhaustive valid orders versus ready-node selection, recursive reverse parsing versus a postfix stack, enumeration versus clipping, and exact fractions versus cross multiplication. A second generator execution reproduced train, validation and audit-case SHA-256 hashes exactly.

## Validation and review

`validation_report.json` passes counts, required fields, targets, unique IDs/options, source/audit fact correspondence, frozen reservations, group/scenario isolation, and exact state/canonical-input duplicate checks. **Zero exact duplicate states or canonical inputs.** Hashes for source, assignment, scripts and outputs are in metadata/report.

Target positions (one-based): train/3 choices **40/40/40**; train/4 **20/20/20/20**; validation/3 **5/5/5**; validation/4 **7/6/6/6**. Longest-option baseline with first-position ties selects **60/200 train**, **11/40 validation** correctly. Training-target-text-frequency heuristic reaches **116/200 train**, **10/40 validation**: reusable answer text remains a measurable shortcut, not evidence of reasoning. Full length/frequency diagnostics are saved.

Same-session text spot review inspected both first-policy cases in all 15 mechanisms (30 rows), including choices and targets. Top local cross-split lexical candidates (maximum word-set Jaccard **0.0833**) share generic ordering vocabulary, not policies or facts; allocation and precedence examples were inspected directly. Maximum whitespace lengths: state **47**, question **10**, option **7** words. These are not tokenizer counts.

## Qualifications and boundaries

The same author specified source semantics, both implementations and rendering. Agreement is a programmatic cross-check, **not independently established natural-language correctness**; same-session self-review is not an independent teacher review. The parent must perform its 256-token CPU audit, separate-session review, cross-producer/historical deduplication and parent-integrity checks.

No Git commands, checkout edits, manifests, model/evaluation code, network calls, ML/tokenizer loads, tests, linting, private records, old v1/tiny examples, other producers or evaluation data were accessed. Only this private artifact directory was written. Original synthetic material remains subject to existing provider terms; no independent redistribution-license claim is made.
