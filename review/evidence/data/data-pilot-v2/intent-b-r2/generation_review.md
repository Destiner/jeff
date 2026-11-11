# Intent-b r2 — choice-construction revision

## Handoff

**240 revised rows frozen: 200 train + 40 validation.** All requests in the parent's source cases were read and their choice sets directly reauthored by the existing approved agent. Teacher identity from this session: provider `openai`, model alias `gpt-sol`; immutable revision unavailable. Additional and pending spend: **£0**.

This is a bounded option-text revision, **not independent semantic verification**. Each original teacher action is intended to remain the correct answer; the parent must separately inspect the revised semantic labels. Structural lineage checks cannot establish that every rival is semantically wrong.

## Inputs and boundaries

Read the assigned data-worktree `AGENTS.md` and `docs/contracts.md`. Row/source inputs came only from `../intent-b/`: train, validation, source cases, generator, metadata and group assignments. `../review-intent/review.md` was read only. The parent generator was inspected, not executed. No other producer rows, historical shards, final/evaluation data, hidden samples or review targets were opened.

All writes are new files under `intent-b-r2/`. No checkout/Git/shared edit, network call, paid call, model/tokenizer load, training, inference, software test, lint or package installation was performed. The only execution was standard-library CPU data application and validation. Parent source/export/support hashes are recorded and checked unchanged at completion.

## Authorship and semantic scope

- `authored_choices.txt`: 240 manually authored sets, in parent group order. Each line has target first, then alternatives in the **parent's non-target slot order**. This is authoring notation, not the model's supplied ordering.
- `target_refinements.json`: explicit, directly authored compact target formulations. These remove redundant identifiers where the unchanged request already fixes them, while preserving action and consequential scope. No algorithm truncates a target, generates a rival, pads text or changes labels. Both authoring stages remain available for inspection.
- `source_mappings.json`: final ID-keyed old/new texts for every option, parent example IDs, unchanged group/split/target IDs and parent target text. This is the definitive expanded revision mapping.
- `apply_revision.py`: deterministic expansion, application, structural/lineage validation, hashing and length diagnostics. It has no third-party dependencies or randomization. Existing files are opened exclusively for initial publication; `--verify` recomputes expected bytes without writing them.

Targets cover the original requested actions, including scoped cancellation versus postponement, refund versus account credit, warranty versus a new paid job, retrieval versus modification, inquiry versus execution, and changing one booking dimension while keeping the others. Choices use hypothetical action details, not new facts about the unchanged state. For example: battery progress rivals concern receipt, dispatch, specification, diagnostics and approval; skate-hollow rivals concern depth, edge alignment, edge damage, holder position and blade profile, rather than unrelated rink access. Administrative requests contrast nearby document types or record operations rather than unrelated purchases.

A preliminary in-memory diagnostic of the first authoring pass showed targets still too often longest. The explicit target refinements were then authored for semantic concision; no automated length quota or label reassignment was used. Final diagnostics were inspected for both extremes, words, characters, ranks and arities. **The frozen JSONL files have not been modified after reporting.**

## Executed lineage and duplicate checks

`python3 apply_revision.py` published the freeze. A subsequent `python3 apply_revision.py --verify` recomputed and matched frozen source mappings, assignments, outputs, metadata and report bytes without writing any file.

Checked across all 240 rows:

- Parent source-case state, full option set and source target match the parent exports.
- State, question, schema, task family, split, group ID, arity, ordered option IDs, target ID and target slot are exactly preserved.
- Every option set changes; rows remain 200 train / 40 validation.
- Example IDs replace only `data:pilot-v2:intent-b:` with `data:pilot-v2:intent-b-r2:`. **Group IDs retain the original intent-b namespace.** No row IDs collide within the revision or with its parent. Global uniqueness outside these permitted inputs is not certified.
- Each revised row has teacher kind/basis, r2 provenance source, the actual rewriting teacher alias/provider and `provenance.parent_id` equal to its original ID.
- `group_assignments.json` is byte-identical to the parent.
- Exact and normalized state duplicates: **0**. Exact ordered inputs and option-order-invariant full inputs duplicated within the revision: **0**. Within-row duplicate option text sets: **0**. Cross-split group overlap: **0**.
- Unchanged states intentionally overlap their parent counterparts: this is a replacement revision, **not an additive set of independent examples**. Do not train on parent and r2 together as if they were unrelated.

Metadata records parent paths and hashes, authoring and application source hashes, output hashes, constraints, purpose, semantic scope, row/group counts and limitations. Groups are 240 singleton storage groups across 24 broad domains, not proof of 240 independently sampled reasoning problems.

## Longest AND shortest priors

Characters are Python Unicode-codepoint `len(text)`. Words are lowercased Unicode `\w+(?:['’\-]\w+)*`, preserving internal apostrophes/hyphens. Ties select the first supplied option. These are no-state teacher-target match counts, not model accuracy or independently grounded correctness.

| Split | Rows | Arity chance | Parent char max | r2 char max | Parent char min | r2 char min |
|---|---:|---:|---:|---:|---:|---:|---:|
| Train | 200 | 29.10% | 105 (52.5%) | 49 (24.5%) | 26 (13.0%) | 67 (33.5%) |
| Validation | 40 | 28.83% | 25 (62.5%) | 11 (27.5%) | 2 (5.0%) | 10 (25.0%) |

| Split | Rows | Parent word max | r2 word max | Parent word min | r2 word min |
|---|---:|---:|---:|---:|---:|---:|
| Train | 200 | 78 (39.0%) | 50 (25.0%) | 42 (21.0%) | 65 (32.5%) |
| Validation | 40 | 14 (35.0%) | 9 (22.5%) | 5 (12.5%) | 15 (37.5%) |

**Residual bias:** shortest choices now exceed reciprocal-arity chance by 4.4 percentage points for train characters, 3.4 points for train words and 8.7 points for validation words. Longest train choices are below chance. This is not a claim that length has become irrelevant or that all priors are at chance. The validation-word minimum is the largest remaining aggregate simple-extremum prior (15/40), with only 40 rows and substantial word ties. No significance claim is made. Means alone would conceal these differences: revised target/rival means are 38.98/39.63 train characters, 40.52/40.69 validation characters, 6.00/6.14 train words and 5.92/6.22 validation words.

### r2 arity breakdown

Cells are first-extremum target matches. Arity chance is 1/arity; singleton high-arity buckets are not useful evidence of neutrality.

| Split | Arity | Rows | Char max | Char min | Word max | Word min |
|---|---:|---:|---:|---:|---:|---:|
| Train | 3 | 100 | 31 | 37 | 30 | 34 |
| Train | 4 | 98 | 17 | 29 | 20 | 31 |
| Train | 5 | 1 | 1 | 0 | 0 | 0 |
| Train | 6 | 1 | 0 | 1 | 0 | 0 |
| Validation | 3 | 20 | 6 | 5 | 4 | 7 |
| Validation | 4 | 18 | 4 | 4 | 4 | 8 |
| Validation | 5 | 1 | 0 | 1 | 0 | 0 |
| Validation | 6 | 1 | 1 | 0 | 1 | 0 |

Target positions were not reshuffled. The parent's per-split/per-arity slot counts remain balanced to within one, but a single row necessarily occupies only one position in a singleton arity bucket.

### Target length ranks

Descending competition rank is 1 + number of strictly longer options; ascending is 1 + number of strictly shorter options. Ties share ranks. Consequently rank-one counts differ from first-max/min wins. Full original and revised rank histograms, tie counts, unique/among-extremum counts, target/rival means and target-slot counts appear by split **and arity** in `validation_report.json`.

| Split / unit | Descending rank counts (rank: rows) | Ascending rank counts (rank: rows) |
|---|---|---|
| Train / chars | 1:56, 2:57, 3:58, 4:28, 6:1 | 1:76, 2:58, 3:49, 4:16, 5:1 |
| Train / words | 1:91, 2:51, 3:40, 4:18 | 1:103, 2:51, 3:34, 4:12 |
| Validation / chars | 1:12, 2:14, 3:9, 4:4, 5:1 | 1:10, 2:14, 3:12, 4:3, 6:1 |
| Validation / words | 1:12, 2:17, 3:6, 4:5 | 1:23, 2:10, 3:5, 4:1, 6:1 |

In particular, words have many ties: being among the shortest is much more common than actually winning a first-min tie break. Do not interpret shared rank one as unique-shortest accuracy.

## Freeze hashes

| File | SHA256 |
|---|---|
| `train.jsonl` | `d551a90e504b7ad6ab0a535c953514edbf9bfc87a91d536f8dcd8b6958a3385c` |
| `validation.jsonl` | `b622e9fe28ada680e847f0b183d9cc32ac3e5a6272905f7d09a060a26e932b14` |
| `group_assignments.json` | `95081b403116ef3ddf0f1124e673c036db7bfbf987afe44d054f8404c45f84ac` |

## Limitations and parent review

Semantic quality takes priority over length balance. Nearby workflow alternatives are still often rejected by the parent's explicit scope wording; that wording was deliberately not changed. Context copying, recurring administrative schemas and residual length/rank signals may remain predictive. No state-overlap classifier, tokenizer or model was run. No independent factual, regulatory or label verification is claimed. The parent should inspect all revised target/rival semantics, perform its separate token audit and historical/cross-producer duplication checks, and reference this r2 freeze instead of silently overwriting or co-training the parent version.
