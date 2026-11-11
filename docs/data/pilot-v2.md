# Data D2: immutable pilot v2

## Release

- Shared manifest: `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/manifest.json`.
- Committed manifest: `manifests/data/pilot-v2.json`.
- SHA256: `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`.
- Provenance: shared `data/data-pilot-v2/provenance.json`, committed `manifests/data/pilot-v2.provenance.json`.
- Final manifest is byte-identical to the reviewed `pre-review-r3/manifest.json`. Earlier candidates and producer r1 files are retained but not all included. **Read the manifest, never glob the directory.**

| Family | Train rows / serialized groups | Validation rows / serialized groups | New named domains or mechanisms, train / validation |
| --- | ---: | ---: | ---: |
| intent | 500 / 425 | 100 / 85 | 40 / 8 domains |
| sentiment | 500 / 425 | 100 / 85 | 40 / 8 domains |
| rule_application | 500 / 30 | 100 / 12 | 20 / 10 mechanisms |
| **Total** | **1,500 / 880** | **300 / 182** | Heterogeneous units; not iid samples |

The eighteen shards include **all six original v1 shards, unchanged**: 300 train / 60 validation. New content adds 1,200 / 240. Never concatenate v1 and v2; never describe all 300 validation rows as fresh. Label basis totals: **1,200 teacher, 600 rule_verified**. Use `label_basis`, not `kind`: one new rule producer records teacher kind with executable rule verification.

V1 was built, validated and self-integrated first at main `1a6350a`, under the user's explicit authorization. Later ownership commit `4019fa7` was incorporated safely after generation; D2's remaining integration follows its shared merge-lock/build protocol. Implementation and main merge hashes are in the final shared handoff.

## Source diversity and frozen boundaries

Six disjoint artifact producers, two per family, each supplied 200 train / 40 validation. No shared checkout editing. Namespaces, split ranges and domains/mechanisms were assigned before authoring; the original config is archived as `authoring-plan.json`, SHA256 `d3189d43a4de66574bf5a08776ad6d3f6020fa08c28814e4254cecb3b2a8499b`. The final config adds revision publication paths without changing assignments.

New intent and sentiment each have **480 separately authored situations**, one row per scenario, across 48 domains. Reviewers inspected source lists/generators after label-hidden judgments: they serialize authored cases, not a Cartesian product or runtime paraphrase multiplier. This does not establish statistical independence; common teacher, request schemas and wording styles remain. Review actual domain breadth alongside singleton group counts.

New rules have **200 train / 40 validation policy instances**, two consequential cases each, conservatively grouped into **20 / 10 named mechanism groups**. They add rounding, encoding, ranking, inventory, scheduling, arithmetic/geometry and additional held-out algorithms. Formal configurations sometimes repeat; broad conditional/cyclic/interval/counting primitives cross named mechanisms. Not every named group is a wholly unseen computation.

Rule serialized counts remain below the aspirational 100 train / 20 validation source-group target. We retained mechanism-conservative grouping rather than rename related cases to inflate the denominator. Counting policy instances separately is useful but not a substitute for independent mechanisms. **No dedicated seen-mechanism validation was added**; all mechanism groups remain split-pure. V1 reachability and Condorcet groups remain validation-only.

No old validation rows, groups or known policy scenarios moved into train. Direct audits verify all v1 row objects and shard entries, historical tiny/v1 boundaries, and exact canonical exclusion. Producers were not shown historical examples. Semantic non-derivation cannot be proved by hashes or lexical checks. Evaluation owns the separate exclusion comparison against public probes and prior evaluation presentations; Data never opened those rows or final-evaluation content.

## Research coordination and repairs

Read R2/R3 owner handoffs directly, sent candidate manifests/hashes and responded through Data handoffs 004–008. Research identified the longest-answer shortcut, publication-order cycles, heterogeneous group units and the public-probe exclusion coverage gap. We reused its reviewed CPU diagnostic helper with its hash recorded; no Research files were edited.

### Intent choice construction

Original new choice sets retained substantial specificity/length bias. Two bounded editors reauthored all 480 sets with more plausible neighboring actions and complete target scope, preserving states, questions, requested actions, groups/splits, arity, ordered option IDs and target slots. No labels changed to defeat a heuristic and no generic filler padding was used. New example IDs and parent lineage distinguish `intent-a-r2` and `intent-b-r2`.

Longest-character selector, ignoring context/question, with first-option ties:

| Stratum | Train matches | Validation matches |
| --- | ---: | ---: |
| Inherited v1 | 84/100 (84%) | 18/20 (90%) |
| New v2, before choice revision | 243/400 (60.75%) | 53/80 (66.25%) |
| **New v2, released** | **120/400 (30%)** | **32/80 (40%)** |
| Combined released v2 | 204/500 (40.8%) | 50/100 (50%) |

These are **authoring diagnostics, not neural performance or independent validation**. The new validation arity-based uniform expectation is 27.5%. Residual bias is material: intent-a-r2 validation longest-character still gets 21/40 (52.5%). Intent-b-r2 word-shortest gets 15/40 (37.5%, versus 28.8% arity chance). Full longest/shortest character/word, position, arity and group diagnostics remain in `quality-audit-r3/`. We did not keep rewriting to force one heuristic score to chance.

All new producers use seeded balanced shuffled target slots and independently shuffled distractors, not deterministic publication-index cycling. New sentiment always offers all four classes with class-balanced question/option wording. Shared styles and legitimate lexical sentiment cues remain.

### Sentiment wording

Separate reviewer found an unsampled wording error in `sentiment-b:g011`: “Not a crease survived” implies removing existing creases, not preventing them. Immutable `sentiment-b-r2` changes only that state's wording to “Every sheet arrived uncreased”; positive judgment is preserved. All other 239 states and all questions/options/targets/groups/splits are unchanged. The correction was explicitly reviewed non-blind. A shaded-bench mixed example flagged by Research was considered by the sentiment reviewer; it relies on implicit amenity approval plus a defect, remains somewhat subtle, and was not silently relabeled.

## Executed quality evidence

All relative paths below are under `JEFF_ARTIFACTS_DIR/data/data-pilot-v2/`.

| Evidence | Measured outcome |
| --- | --- |
| `validation.json` | 1,800 valid; zero structural, exact canonical duplicate, conflicting target or split/group errors; eighteen hashes/counts match |
| `quality-audit-r3/audit.json` | Six v1 shards/360 row objects preserved; tiny/v1 historical checks pass; inherited/new/combined diagnostics |
| Lexical historical scan | 473 raw and 1,507 number-masked trigram pairs at Jaccard >=0.65, all within groups; zero cross-group/cross-split candidates at that threshold |
| `pre-review-r3/token-budget.json` | 6,848 candidate pairs, min/median/p95/max 41/61/96/169 tokens; zero overflow/question/candidate loss at256 |
| Token budget at128 | Same45 inherited-v1 pairs lose question tokens; new rows do not add overflow |
| `review-revisions/review.json` | Final revised intent40/40 label-hidden agreements; full480-row lineage checks; 53 protected inputs unchanged |
| `review-sentiment/review.json` | Sentiment40/40 label-hidden agreements; all480 new source experiences inspected after freeze; full four-class/style/position checks |
| `review-rules/review.json` | Rules60/60 label-hidden agreements (two per new mechanism); all480 new targets recomputed; source/policy correspondence checked |
| Final correction review | One sentiment wording repair accepted non-blind; no unresolved sampled must-fix |

The final-content sample totals **140 target-hidden judgments** (40 intent, 40 sentiment, 60 rules), plus the non-blind correction. Earlier intent judgments covered superseded option sets and are not added as independent accuracy evidence. Reviewers and authors share the exposed `openai/gpt-sol` alias in separate sessions; immutable revisions are unavailable. Agreement is not independent ground truth or all-row semantic proof.

Rule audits recompute from structured facts using separately implemented producer functions. Same-author specifications/renderers/solvers can share mistakes. Sixty direct text assessments improve fidelity evidence but do not independently parse every policy.

The tokenizer audit used the exact saved all-MiniLM tokenizer revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, CPU-only; it is not a universal length guarantee for other tokenizers. No model was loaded or trained by Data.

### Corrected validator failure

The first expansion assembly was rejected because the old word-only canonicalizer erased negative-coordinate signs, bracket order and symbol strings, falsely merging distinct choices and cases. We inspected the affected rows and corrected exact comparison to Unicode NFC/outer stripping while preserving case, punctuation and internal spaces. Unchanged producer bytes then passed. Initial failed report is preserved in `pre-review/validation.json`; no bad rows were dropped or labels changed to make validation pass. Word-normalized collisions remain clearly labeled heuristic flags in the Research-derived overlap report.

## Reproduction and actual commands

From the data worktree; outputs must be new paths. Full release commands and integration evidence are in the final handoff.

```sh
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
uv run --locked python -m jeff.data.assemble \
  --config configs/data/pilot-v2.json \
  --manifest manifests/data/pilot-v2.json \
  --report "$JEFF_ARTIFACTS_DIR/data/data-pilot-v2/validation.json"

uv run --locked python -m jeff.data.audit \
  --manifest "$JEFF_ARTIFACTS_DIR/data/data-pilot-v2/pre-review-r3/manifest.json" \
  --parent-manifest "$JEFF_ARTIFACTS_DIR/data/data-pilot-v1/manifest.json" \
  --historical-manifest "$JEFF_ARTIFACTS_DIR/data/data-tiny-v1/manifest.json" \
  --artifacts-dir "$JEFF_ARTIFACTS_DIR" \
  --research-script /Users/destiner/Code/jeff/experiments/research/audit_pilot_shortcuts.py \
  --output "$JEFF_ARTIFACTS_DIR/data/data-pilot-v2/quality-audit-r3/audit.json"
```

Both succeeded on the actual data. Candidate generation/review, two choice revisions and the one wording revision are retained with authored sources and exact generation settings. Some producer replay scripts overwrite files: never run them in a published directory. Restore hashed source artifacts into a new root, retain their original teacher identities, and replay there. Git includes only small configs/manifests/code/docs, not the bulky training content.

## Costs and downstream use

**£0 actual additional / £0 pending / £0 allocated**, existing approved agent access only; token/subscription costs not separately metered. No API calls, rented compute, large model loads, software tests or linters. Original synthetic content under existing provider terms, no private records or external datasets; no independent blanket redistribution-license claim. Lead wording correction used exposed `openai/gpt-astra`; no invented immutable model versions.

Evaluation should freeze inputs against this final hash, keep inherited/new/probe strata explicit, report domain/mechanism breadth, and rebind its public-probe exclusion receipt after revision. Model's existing M4 scope and compute ownership are unchanged by this delivery. Preserve v1 and prior checkpoints. Further expansion should follow actual untruncated error evidence rather than add more of the same templates.
