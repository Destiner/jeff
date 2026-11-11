# intent-a-r2 — choice-construction revision

## Scope and disposition

New, frozen replacement shard: **200 train + 40 validation rows**. All **240 targets and 713 rivals** have new text. Parent artifacts remain immutable. Use this revision **instead of**, not alongside, the parent: group IDs deliberately remain identical.

The author read all 240 requests in the parent's source cases, authored every complete choice set directly in `choices.txt`, and performed same-session semantic self-review. Revisions use concise complete requested actions and workflow-adjacent alternatives rather than unrelated topics or length-padding. This is **teacher authoring/self-review, not independent correctness verification**; the parent's separate revised-label inspection remains pending.

Actual rewriting teacher: **openai / gpt-sol**, captured from `PI_PROVIDER` and `PI_MODEL`. Immutable revision and harness sampling parameters are unavailable. No separate model/API invocation, network, paid call, tokenizer, ML load, tests, lint, Git command, checkout edit, or final/evaluation-data access. Additional and pending spend: **£0**. Writes are confined to this new directory. No packaging/build work was applicable to this dataset-only assignment.

## Semantic scope

Only option texts, the example ID prefix and provenance change. State, question, requested correct action, split, group ID, task family, schema, arity, ordered option IDs, target ID and target slot are retained. The new prefix is `data:pilot-v2:intent-a-r2:`; group IDs still use `data:pilot-v2:intent-a:`. Provenance identifies `intent-a-r2/choice_mappings.json`, retains teacher label basis, records the rewriting teacher, and includes the original example ID as `parent_id`.

The authored targets retain consequential distinctions, including:

- g003: relocate the existing connection, not add another subscription.
- g007: basic speed from the next billing date.
- g014: explain a hypothetical mid-course refund, not execute withdrawal.
- g037: decline replacement while leaving repair open.
- g073: remove one of three desks, not the whole reservation.
- g082: cancel tonight's class, retaining other bookings.
- g098: withdraw only dental-cleaning consent and retain consultation.
- g128: stop spending summaries but retain fraud alerts.
- g131: replace a lost registered card and protect its credit.
- g155: change the closing reading date while still moving out.
- g170: text on arrival rather than ring; no appointment reschedule.
- g185: remove highlights and retain the haircut.
- g195: cancel only the second duplicate preorder.
- g202/g210: distinguish SMS-only cessation and additive severe-weather alerts from replacing the subscription.
- g215/g216: retain the specified specialist / retain appraisal despite withdrawing sale permission.
- g225/g228/g230: track dispatch before replacement / provide accessible format without a result change / record verification consent rather than issue a certificate.
- g236/g239: request reported anchor information, not a safety certification / ask about the walk-in, not ascent difficulty.

Rivals vary genuine workflow dimensions: timing versus location changes, amount versus collection-date changes, records versus receipts, permission versus execution, add versus replace, repair versus exchange, and inquiry versus reservation. They are alternative requested actions, **not assertions of additional real facts**. For example, g179 distinguishes adding office delivery from modifying an already scheduled delivery or arranging return collection. g139 contrasts surname correction with ownership transfer, contact updates and card replacement. g239 contrasts approach access with descent, technical ascent, guiding and approach reporting. The original requests still explicitly exclude some alternatives; choice-only rewriting cannot remove that underlying ease. Some inquiry/execution rivals also remain straightforward. No claim of uniformly hard distractors or independent absence of ambiguity is made.

## Deterministic lineage and CPU validation

`apply.py` reads only parent train/validation, metadata/source cases and group assignments; it does not execute the parent generator. It maps target-first `choices.txt` through the parent's source-case order to the original opaque option IDs, preserving exported order. `choice_mappings.json` records every original/new text pair, parent/new example ID, unchanged group/split/target and target slot. `group_assignments.json` is copied byte-for-byte. The script refuses to overwrite frozen outputs.

Executed once:

```text
python3 .../intent-a-r2/apply.py
python3 .../intent-a-r2/validate.py
```

`validate.py` reads the frozen outputs back and publishes `validation_report.json`. It never writes train/validation. Its report creation is exclusive as well, to avoid silently replacing a published audit. This is dataset validation, not a software test suite.

Checked across all 240 paired rows:

- All original non-choice fields except example IDs/provenance are exactly equal.
- Ordered option IDs, arities, target IDs and slots are identical; every target appears once.
- Every mapping agrees with every serialized old/new option pair.
- All 240 example IDs are unique and disjoint from the parent IDs within the permitted source scope.
- All provenance records identify r2 and the original `parent_id`, with teacher labels.
- 200/40 singleton groups, unchanged assignment file, zero cross-split group overlap.
- Zero raw or whitespace/case-canonical state duplicates; zero raw ordered-input or canonical unordered-choice-input duplicates within this revision; zero duplicate canonical options within any row. Canonicalization preserves punctuation/signs, changing only case and whitespace.
- SHA256 of parent train, validation, metadata, source cases and assignments is unchanged from generation capture. Local mappings, source, scripts, assignments and frozen output hashes match metadata.
- All 953 option texts changed; all 240 choice sets and target texts changed. This does not itself verify semantic equivalence.

Parent-equivalent states/questions across revisions are intentional lineage, not new independent examples. No global duplicate claim is made: other producer, historical and final data were not opened. SHA256 and metadata identity are in `metadata.json` and `validation_report.json`; source/script hashes allow the exact authoring and CPU transformations to be inspected.

## Original versus revised no-state length priors

Characters are Unicode codepoints (`len`). Words are Unicode word sequences retaining internal straight/curly apostrophes and hyphens. Both first-maximum and first-minimum choose the **first supplied option on ties**, without state/question access. These are descriptive teacher-target match rates, not model performance or independently grounded accuracy.

| Split | Metric | Parent first-max | r2 first-max | Parent first-min | r2 first-min |
|---|---|---:|---:|---:|---:|
| train (200) | chars | 138 (69.0%) | 71 (35.5%) | 8 (4.0%) | 62 (31.0%) |
| train (200) | words | 96 (48.0%) | 58 (29.0%) | 27 (13.5%) | 55 (27.5%) |
| validation (40) | chars | 28 (70.0%) | 21 (52.5%) | 3 (7.5%) | 7 (17.5%) |
| validation (40) | words | 20 (50.0%) | 13 (32.5%) | 5 (12.5%) | 12 (30.0%) |

Uniform arity chance is **26.28% train**, **26.17% validation**. Word priors are relatively close to that reference, but **character length remains a substantial validation shortcut: 21/40 targets are uniquely longest**. Train character longest is still above chance, and shortest also reaches 31%. This is an improvement in the measured longest-choice prior, **not a shortcut-free result**. It has not simply become universally “shortest wins,” but neither extremum is neutral. No option padding, diagnostic-driven relabeling, target-slot shuffling, or state changes were used. No post-audit revisions were made to the frozen outputs.

### Arity and rank inspection

Arity counts are identical to the parent: train 3/4/5/6 choices = **60/100/27/13**; validation = **12/20/4/4**. Existing target positions remain balanced within each split/arity as far as sample size permits. The four validation five-choice cases occupy positions 1, 2, 4, 5; the four six-choice cases occupy 1, 2, 3, 6. This sparse coverage is inherited, not repaired by moving labels.

| Split / arity | Rows | r2 char first-max / first-min | r2 word first-max / first-min | Uniform chance |
|---|---:|---:|---:|---:|
| train / 3 | 60 | 23 / 24 | 18 / 22 | 33.3% |
| train / 4 | 100 | 32 / 32 | 28 / 26 | 25.0% |
| train / 5 | 27 | 9 / 5 | 6 / 6 | 20.0% |
| train / 6 | 13 | 7 / 1 | 6 / 1 | 16.7% |
| validation / 3 | 12 | 7 / 1 | 4 / 4 | 33.3% |
| validation / 4 | 20 | 12 / 4 | 6 / 5 | 25.0% |
| validation / 5 | 4 | 1 / 1 | 2 / 2 | 20.0% |
| validation / 6 | 4 | 1 / 1 | 1 / 1 | 16.7% |

Descending target rank uses an interval for ties (e.g. `1–3` means the target shares ranks 1 through 3). For **r2 character length**, train interval counts are: 1–1:68, 1–2:10, 1–3:2, 2–2:26, 2–3:8, 3–3:35, 3–4:3, 3–5:1, 4–4:37, 4–5:3, 5–5:6, 6–6:1. Validation: 1–1:21, 1–2:2, 2–2:7, 3–3:3, 4–4:5, 5–5:1, 6–6:1. Original and revised rank distributions for **both characters and words**, by split and arity, plus every row's option lengths and target rank interval, are published in `validation_report.json`.

The small six-choice train stratum remains notably long-target-biased (7/13 character first-max, 6/13 word first-max). Tiny validation strata are unstable. Consequential partial-action and conditional targets sometimes still require more words than their alternatives. Semantic scope takes priority over forcing a numerical quota. No token-budget claim follows from character/word counts.

## Frozen deliverables and limits

- `choices.txt`: all directly authored target-first choice sets.
- `choice_mappings.json`: complete option-ID and parent lineage mappings.
- `apply.py`, `validate.py`: deterministic serializer and CPU-only audit.
- `train.jsonl`, `validation.jsonl`: frozen outputs.
- `group_assignments.json`: unchanged parent bytes.
- `metadata.json`, `validation_report.json`, this review.

Frozen SHA256:

```text
train.jsonl       77cb6b5436415aee55bd0449590f9586a73a148f3270b9ac116348cbba79cae9
validation.jsonl  14035d90219ea2c5d687a6736d4b3a0c8d2a41ddd7b8b2bc94c2d34f575b6cca
```

Outputs were frozen before diagnostics and have not been modified after reporting. Remaining gates: separate parent semantic label inspection, tokenizer/budget checking, downstream assembly/global deduplication, and model evaluation. Same teacher identity as the original and review is not an independent source of correctness evidence.
