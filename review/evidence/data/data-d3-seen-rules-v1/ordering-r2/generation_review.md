# Ordering r2: immutable choice-construction revision

Only wrong option text and per-row provenance source/teacher representation changed.
All 48 target texts, target IDs/slots, ordered option IDs, arities, facts, policy
wording, questions, states, stable row/group IDs, named assignment plan and split
are preserved. This is a new candidate identity; IDs name the same policy cases,
not new independent examples. Validation only, including every derivative.

## Construction and helper handling

`distractor_constructions.json` records every revised wrong slot and its generating
misapplication. Discount errors are explicit wrong-order, omitted/repeated-step,
wrong-base, cash/percent confusion and additive-percent programs. Rounding errors
are computed from the measured value using named wrong grids, tie directions or
floor/ceiling modes. All option numbers retain the target's stated precision and
unit; no arbitrary offsets or padding. FIFO alternatives greedily exhaust different
batch priorities, selected by ID-hashed permutation enumeration, deduplicating
allocations before selection. Every FIFO choice meets demand and capacities.
The exact programs and per-case selections are in `revise.py`; no search over
heuristic scores, reauthoring of facts or target changes was performed.

`audit.py`, `audit_cases.jsonl`, `source_cases.jsonl` and assignments are byte-identical
copies. Source cases contain only policies/facts, not distractor descriptions, so
there are no stale distractor descriptions to replace. Pure `expected` and `stated`
were imported with bytecode disabled, without running the helper main. No helper
edit was needed. The copied helper's OLD authoring main is intentionally NOT the r2
validator: it assumes old provenance and all rounding distractors on the correct
grid. Off-grid wrong-grid answers are now intentional; `revise.py` validates units,
precision, uniqueness, nonnegative values and recorded construction instead.
The parent authoring/generator/finalization scripts were not executed or copied as
r2 entry points. `revise.py` is the revision/audit entry point and refuses overwrites.
To reproduce, copy it alone to a fresh sibling output directory of `ordering/`
and invoke with actual PI_PROVIDER/PI_MODEL set. It never mutates parent files.

## Provenance

Teacher is actual source alias openai/gpt-sol; source teacher_model object was
normalized to its equivalent string, a metadata-only change. Revision author is
recorded from actual PI_PROVIDER/PI_MODEL, not inferred from source. No new model
calls or costs occurred; source authoring attribution is preserved separately from
revision authorship. Parent metadata and every source file hash are in
`parent_refs.json`; exact old/new JSONL row hashes and full expected recomputation
are in `validation_report.json`. Manifest hashes distinguish the immutable drafts.

## Interpretation and limits

Same-author expected recomputation and exact rendered state/question reconstruction
passed 48/48 each. This is arithmetic/renderer consistency, NOT independently
verified natural-language correctness. Descriptive old/new shortcut counts and
per-row evidence follow in `validation_report.json`. First/length diagnostics use
first-option tie-break; fractional length credits are also included. Numeric ranks,
extremes, lower median, decimal formats, terminal digits and FIFO most/fewest-zero
choices are inspected, not treated as held-out shortcut accuracy. Arity and target
slots are intentionally immutable. A correct FIFO allocation with two zero batches
has an unavoidable depletion signature at low demand; boundary cases remain easy.
No claim that options alone are statistically independent of labels is warranted
from 12 cases/mechanism. Wrong rounding grids are pedagogically meaningful but can
sometimes be rejected by grid membership. Omitted-discount errors often increase
an amount. Paired dependence, repeated policies, common author/templates and small
sample size remain limitations. No hidden or final data, history, model predictions,
network, API, training, spend, Git, mailbox, tests or lint were used.
