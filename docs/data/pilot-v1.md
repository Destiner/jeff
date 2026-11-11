# Pilot v1: quality and provenance

## Frozen outputs

Manifest: `manifests/data/pilot-v1.json` (SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`). Shared copy: `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/manifest.json`.

Provenance sidecar: `manifests/data/pilot-v1.provenance.json`; the shared `provenance.json` references and hashes individual producer metadata, assignments, generator code and reports. Generator seeds/authored cases are retained outside Git, not buried in this summary.

| Family | Train rows / groups | Validation rows / groups | Label basis |
| --- | ---: | ---: | --- |
| intent | 100 / 25 | 20 / 5 | Teacher |
| sentiment | 100 / 25 | 20 / 5 | Teacher, formatting-corrected r2 |
| rule_application | 100 / 10 | 20 / 2 | Programmatic, rule-verified |
| **Total** | **300 / 60** | **60 / 12** | **240 teacher / 120 rule-verified** |

Options span 2–5 choices across the pilot. Intent uses 3–5; corrected sentiment always uses four; rules 2–5. Positions vary and are balanced within applicable split/choice-count strata to within one where producer subset size permits. Tiny subsets cannot cover every position. Sentiment has 25 train and 5 validation rows per positive-only, negative-only, neutral, and mixed class; class balance is intentional, not a natural frequency estimate.

## Production and split isolation

Three separate high-intelligence subagents produced independent family directories; a fourth reviewed finished files without edits. They were artifact producers, not concurrent checkout/code editors. The lead alone changed the data checkout and assembled manifests.

`configs/data/pilot-v1.json` assigned group namespaces and splits before generation. Each producer wrote its domain/mechanism map before content. Intent/sentiment groups contain four substantively different cases in one scenario/domain cluster. Rule groups contain ten varied parameter/boundary cases per generator mechanism, never split across train/validation.

Rule training includes first-match routing, marginal fees, greedy capacity, cyclic indexing, weighted scoring, set symmetric difference, interval overlap, longest-prefix routing, checksums, and state-machine transitions. Validation reserves entire graph-reachability and Condorcet-selection mechanisms. It measures only two held-out mechanisms, not all trained rule types or 20 independent domains.

No reserved final family was generated, and no final-evaluation data was inspected. Namespaces/source groups do not overlap across splits. **This is not topic-disjoint validation across all task families**: e.g. intent training includes pet boarding while sentiment validation includes different pet-boarding events. Reviewer found no shared source event or copied content in these overlaps.

## Provenance and verification level

- Pilot text/teacher labels: actual exposed `openai/gpt-sol` alias for each producer; immutable model revision and sampling parameters unavailable. Tiny text/labels: `openai/gpt-astra` exposed lead alias.
- Lead formatting correction: `openai/gpt-astra`; no new sentiment judgments. All 120 source→revision mappings preserve state, subject, teacher class, split, and group. New IDs distinguish revised rows; groups retain lineage.
- Rule labels: generator computes results; a separately implemented `audit.py` recomputes them from retained facts. The same producer authored rules, facts, generator, and verifier. This is executable rule verification, **not independent authorship or independently parsed text correctness**.
- Reviewer used a separate session with the same exposed `openai/gpt-sol` alias. Its agreement is not independent ground truth or proof of a distinct underlying model.
- Original synthetic data; no external source dataset or private real records. Existing provider/account terms apply; no independently reviewed blanket redistribution permission claimed.
- Additional/pending spend **£0/£0**, no separately billed generation. Existing-session tokens/cost not separately metered. Local lightweight CPU only.

## Quality results

Detailed evidence under `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/`:

| Evidence | Result |
| --- | --- |
| `validation.json`, `assembly-validation.json` | 360/360 structurally valid; all six hashes/counts match; no duplicate IDs, exact normalized inputs, conflicting targets, repeated state/question warnings, or group leakage |
| Lexical scan | 163 pairs at state word-trigram Jaccard >=0.65; all within rule groups; zero cross-group or cross-split candidates at that threshold |
| `review/review.json`, `review/review.md` | 48/48 teacher spot-review agreements, no unresolved ambiguity; 24 rule, 12 intent, 12 sentiment |
| Reviewer protocol | 47 target-label-hidden judgments frozen before comparison; one sentiment class already exposed, honestly recorded as ordinary review |
| Rule recomputation | 120/120 targets matched the retained audit helper; reproduced by reviewer without executing its report-overwriting main |
| Sentiment lineage | 120/120 classes/states/subjects/groups/splits preserved; all four classes supplied |
| Independent integrity pass | Six shard hashes and 17 provenance artifact hashes verified; producer files unchanged |

The reviewer examined strongest/weakest lexical pairs across nine flagged groups (17 unique pairs). Distinct structured facts and meaningful boundaries support retaining these rows; template redundancy remains, particularly routing, set reconciliation and state-machine groups (135 of 163 pairs). Do not treat related cases as independent samples. No semantic-deduplication completeness claim.

### Corrected before publication

The original sentiment producer's question templates perfectly tracked the target class; the mixed candidate was also mostly available only when correct. The lead created `sentiment-r2` instead of changing the frozen originals. It uses one neutral subject-specific question, all four classes on every row, and shuffled class-balanced target positions. Original rows are excluded from the manifest. Explicit cues such as “delighted”, “mixed”, and factual neutral descriptions remain; this is a clean synthetic pilot, not a hard natural-language benchmark.

### Code review follow-up

Reviewer reported no observed must-fix current-data issue and flagged two reuse risks: assembler hardcoded provenance/cost and incomplete guards for child paths. Both were corrected before the final commit: metadata-derived identity/costs checked against config, and guarded/contained source/published paths before reads. Reassembling all 360 actual rows under a new artifact root succeeded with byte-identical manifest and equivalent provenance. Original published files/reviewer findings were not overwritten.

### Execution history and build

Successful: tiny publication; `uv sync --locked`; sentiment correction; pilot assembly; full tiny and pilot validation; actual-source reassembly; `uv build --no-sources`. The built wheel was also installed into an isolated uv environment and its validator executed from `/tmp` against all 360 rows: valid, zero errors, same 163 within-group candidates (`installed-wheel-validation.json`). This verifies packaged execution rather than only source-tree imports. One initial assembly attempt failed on different producer group-map wrappers (`KeyError: groups`); normalized wrapped/direct maps, then reran successfully before publishing the manifest. No failed examples were dropped to obtain success. No software tests/linting, ML model loading, or final-data access.

## Known limits and next task

Only 72 source groups, English-only synthetic content, teacher-style correlations, explicit sentiment cues, and uneven rule difficulty. Four sentiment candidates trade away option-count diversity within that family to remove a concrete shortcut. Teacher labels can be wrong despite the 48-row review; rule rendering/specification errors can survive algorithmic agreement. No calibrated-confidence claim.

Model's public `20261111-1040-pilot-complete.md` reports using this exact manifest, 36/60 aggregate target agreement after training, and **45 rule-validation candidate pairs truncated at 128 tokens, losing question text**. These are Model-reported results, not reproduced by Data. All 1,412 pairs would fit at 256 per its token audit. Preserve v1; recommend correcting/controlling the input budget on the same validation rows before interpreting rule errors or generating replacements. Subsequent data expansion should respond to untruncated validation failures and missing coverage, not inflate this pilot with more templates.
