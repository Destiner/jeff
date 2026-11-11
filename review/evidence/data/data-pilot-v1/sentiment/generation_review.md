# Sentiment pilot shard — completed handoff

## Scope and outputs

Artifact directory: `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/sentiment/`

- `train.jsonl`: **100 rows**, groups `data:pilot-v1:sentiment:g01` through `g25`, four rows each.
- `validation.jsonl`: **20 rows**, groups `data:pilot-v1:sentiment:g26` through `g30`, four rows each.
- `group_assignments.json`: full group IDs, frozen split assignments, distinct named domain mechanisms, written before row content.
- `metadata.json`: teacher/source identity, settings, revision limits, class counts, usage constraints, costs, limitations.
- `generate.py`: original fixed agent-authored situations and deterministic JSONL renderer; not a model caller.
- `validate_dataset.py` and `validation_report.json`: lightweight artifact-only structural/duplicate checks and their actual results. Not a manifest or software test suite.

No checkout, shared contract, manifest, model/evaluation code, or Git modifications. No final/evaluation content inspected. No reserved-family examples produced. Only this directory was written.

## Group plan and label strategy

Training covers 25 separate source domains: cafe, bus, library, footwear, recipe app, laundry, garden tools, salon, grocery delivery, museum, headphones, fitness class, parcel lockers, desk chairs, cinema, bicycle repair, houseplants, language tutoring, food containers, pool, book club, weather app, camping tent, tailoring, pottery workshop.

Validation holds out five source domains: **pet boarding, observatory sessions, luggage storage, hearing loops, seed exchanges**. Shared sentiment vocabulary and option wording remain across splits; this is domain holdout, not a claim of linguistic independence.

Every group has four different situations, not four paraphrases of one review: one favorable, one unfavorable, one factual-neutral, and one explicitly mixed. Class order within groups varies. Counts are **25 of each class in train and 5 of each in validation** (metadata keys P/N/U/M). Some pure object-specific questions isolate criticism of one component despite praise of another. Negation includes positive absence of a feared problem and negative failures of expected service. No sarcasm or unresolved targets.

Teacher/source: exposed `PI_PROVIDER=openai`, `PI_MODEL=gpt-sol`; immutable revision, temperature, top-p, and sampling seed unavailable. Provenance source for every row is generation job `jeff-data-pilot-v1-sentiment-agent-r1`. Labels use `kind=teacher`, `label_basis=teacher`, never `rule_verified`. The Python code renders teacher-authored labels; it does not independently establish sentiment correctness.

There are **108 three-option and 12 four-option rows**. Positive-only and negative-only wording excludes the mixed option, so categories are mutually exclusive for the specified subject. Three-option mixed cases omit neutral; most other three-option cases omit mixed. This candidate-set pattern can become a shortcut and is explicitly disclosed, not evidence of generalization. All option IDs are deterministic opaque hexadecimal strings.

## Checks actually executed

Executed locally with Python CPU only:

```text
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/sentiment/generate.py
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/sentiment/validate_dataset.py
```

The same commands were rerun once after author self-review tightened positive/negative option wording to exclude mixed attitudes and simplified a question template. No software tests, linting, training, local inference, network generation, APIs, or separately billed work were run.

Final structural validation: **pass, zero errors**. JSONL parsing, required fields/types, schema version, local namespaced ID uniqueness, nonempty options/questions/states, unique option IDs/texts, exact single target membership, 2–6 option bounds, task family, split purity, frozen config group membership, four rows per group, cross-split group isolation, and teacher provenance all checked.

Duplicate scan: **zero normalized exact state duplicates**, **zero state pairs at token-set Jaccard >= 0.60**. This lexical heuristic cannot establish semantic uniqueness. Cross-shard uniqueness and similarity remain for the parent assembler.

Target positions (one-based):

| Split | Option count | Positions 1 / 2 / 3 / 4 |
|---|---:|---|
| Train | 3 | 30 / 30 / 30 / — |
| Train | 4 | 3 / 3 / 2 / 2 |
| Validation | 3 | 6 / 6 / 6 / — |
| Validation | 4 | 0 / 0 / 1 / 1 |

Author self-review inspected rendered train `g01` and validation `g29`/`g30` (12 rows), alongside authoring review of all fixed situations. It found the overly broad positive/negative wording and that wording was corrected before completion. This is **teacher self-review, not independent correctness verification**. SHA-256 hashes of final train and validation content are in `validation_report.json` for parent assembly.

## Usage, cost, and remaining risks

Original synthetic English situations, no external datasets or private real data. Existing provider terms apply; no separately asserted redistribution license and no independent terms review. **£0 additional spend; £0 pending spend**. Existing agent access was used; its subscription/serving cost is not estimated here.

Small, deliberately balanced and unusually explicit pilot. Neutral examples are factual snippets rather than rich natural reviews. Mixed cases often name both sides directly. Shared phrasing, candidate-set shortcuts, English-only coverage, and teacher errors can inflate apparent performance. No independent semantic audit, probability calibration, or model-quality claim is made.

The shard is complete and frozen for parent validation/immutable-manifest assembly. Do not rerun generation into this completed directory or modify finished JSONL files.
