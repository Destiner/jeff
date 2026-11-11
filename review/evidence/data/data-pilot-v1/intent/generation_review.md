# Intent pilot r1 — generation and review

## Deliverables

All files are under `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/intent/`:

- `train.jsonl`: 100 rows, groups `data:pilot-v1:intent:g01`–`g25`.
- `validation.jsonl`: 20 rows, groups `data:pilot-v1:intent:g26`–`g30`.
- `group_assignments.json`: 30 full group IDs mapped to frozen splits, named domains/mechanisms, source-group revision 1, and four planned rows each. Written before any row content was authored.
- `metadata.json`: source/teacher identity, settings, full group plan, counts, constraints, limitations, and spend.
- `generate.py`: original teacher-authored text and local deterministic serialization/option ordering. No model calls or external dependencies.
- `validation_report.json`: executed structural/duplicate/position checks and final JSONL SHA-256 values.
- `generation_review.md`: this note.

## Group plan and content

The 25 training clusters cover public libraries, parcel delivery, city buses, community gardening, adult language courses, bicycle workshops, water utilities, museum visits, pet boarding, amateur theatre, recycling centres, music lessons, campgrounds, housing repairs, food cooperatives, swimming pools, astronomy clubs, school meals, photo printing, neighbourhood volunteers, rail stations, ceramics studios, sports leagues, archive research, and mobile service.

The five validation source scenarios are held out as whole groups: community apiary activities, canal boat hire, seed library services, makerspace laser cutting, and visiting choir festival participation. These are new scenario clusters, not claims that every abstract intent or topical word is unseen. All related variants stay within their assigned group/split. Each group contains four substantively different requests rather than name-swapped paraphrases.

Inputs mix short enquiries and contextual requests, explicit negation of competing actions, irrelevant narrative, and indirect information requests. Options are natural action descriptions with plausible competing requests. There are 30 three-choice rows, 60 four-choice rows, and 30 five-choice rows. Target positions cycle deterministically within each split/option-count bucket; position frequency differs by at most one in each bucket. Opaque option IDs are SHA-256-derived strings and must not be used as model input.

## Labeling and source

Teacher: actual exposed alias `openai/gpt-sol`, obtained only from `PI_PROVIDER` and `PI_MODEL`. Immutable revision, temperature, top-p and generation seed were not exposed and are recorded as unknown. Every row has `kind: teacher`, `label_basis: teacher`, and source job `data:pilot-v1:intent:agent-authoring-r1`. The existing agent authored the state, options and intended target. Python only serialized that authored content and placed the target at its assigned position; this is not a rule-verified semantic label audit.

The authoring teacher reviewed the request/target relationship and distractors across all 120 examples. Particular irrelevant-narrative/negation cases reviewed include bus cleanliness versus pass refusal (`g03:r03`), paid lessons versus future automatic payments (`g12:r04`), bicycle trouble versus volunteer shift cover (`g20:r02`), apiary latch repair versus bee health (`g26:r04`), and pianist travel versus programme spelling (`g30:r03`). These are self-review, not independent human/model verification. Ambiguous multi-intent cases were excluded during authoring.

## Commands and checks actually executed

Ran `python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/intent/generate.py`, then a standard-library inline Python dataset-validation pass confined to this directory. No software tests, test runners, linting, build, model inference, API/network calls, Git operations, or other shard inspection occurred.

Validation passed: JSON parsing; exact 100/20 split counts; required schema fields; family and split; unique namespaced row IDs; nonempty string questions/options; 2–6 options; unique option IDs/texts per row; exactly one target; teacher provenance; all 30 preassigned groups with four rows each; no cross-split group overlap; target-position balance per split/arity; no exact normalized state or full-input duplicates. All-pairs normalized state SequenceMatcher scanning found no pairs at similarity >= 0.80. This heuristic is not a semantic deduplication guarantee. Parent-level cross-shard validation remains the lead's responsibility.

## Constraints, costs, and risks

Original synthetic content only; no external datasets or private real records. Usage remains subject to existing provider/access terms; no separately asserted redistribution license. Additional spend **£0**; pending spend **£0**. Existing approved access cost is not separately attributed.

Limitations: small English-only synthetic sample, action-style options, no binary/six-choice coverage, clean single-intent selection rather than realistic ambiguity, possible teacher mistakes and stylistic regularities, and shared generic actions across scenario-isolated splits. No independent correctness or calibration claim is made. No final/evaluation data or reserved passage-entailment examples were inspected or generated.

The JSONL shards are complete and frozen for handoff. No checkout, shared contract, manifest, model/evaluation implementation, or Git state was modified. The parent lead owns combined validation and immutable manifest assembly.
