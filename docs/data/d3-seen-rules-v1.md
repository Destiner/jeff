# D3: seen-mechanism, new-policy diagnostic

## Frozen release

- Manifest: `/Users/destiner/Code/jeff/artifacts/data/data-d3-seen-rules-v1/release/manifest.json`.
- SHA-256: `d74bfda56fc18c89c4a40852dd46d9ec8bce1c907c9ebc8cbc979f23d9047ca9`.
- Committed mirror: `manifests/data/d3-seen-rules-v1.json`; provenance mirror alongside it.
- **0 training / 96 developmental validation decisions, 48 policy/source groups, eight intentionally seen mechanisms.** Six new policies per mechanism, two dependent cases per policy.
- **Never train on these rows or derivatives.** Keep this diagnostic separate from v2, earlier probes and final evaluation. Do not concatenate it into a training manifest or count it as mechanism-disjoint evidence.

The fixed preauthoring plan is archived at `data/data-d3-seen-rules-v1/authoring-plan.json`, SHA-256 `c622b1d943f02d38dd66561dd63d663f6c4f4f314f5bef0d831bb2617cee3132`. The committed config preserves every original allocation/constraint and adds publication-revision locations. D2's 1,500/300 release and all historical IDs/splits remain untouched; v2 manifest SHA-256 remains `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`.

## Exposure and grouping

| Mechanism | Named v2 training group | Decisions / new policies |
| --- | --- | ---: |
| Lexicographic | `data:pilot-v2:rule-a:g002` | 12 / 6 |
| FIFO | `data:pilot-v2:rule-a:g003` | 12 / 6 |
| Discount composition | `data:pilot-v2:rule-a:g005` | 12 / 6 |
| Rounding | `data:pilot-v2:rule-a:g007` | 12 / 6 |
| Packs | `data:pilot-v2:rule-b:g002` | 12 / 6 |
| Rates | `data:pilot-v2:rule-b:g005` | 12 / 6 |
| Coordinates | `data:pilot-v2:rule-b:g006` | 12 / 6 |
| Cooldown scheduling | `data:pilot-v2:rule-b:g008` | 12 / 6 |

`release/case-metadata.json` maps each decision to policy/source group, domain, mechanism and its actual training shard/group/hash. Assignment hashes are also bound. `group_id` is the new policy instance, not the trained mechanism. Per-case fields expose `stratum=seen_mechanism_new_policy`, intentional mechanism overlap and permanent training exclusion. These are 48 declared policy units, not 48 independently invented algorithms; common authors and paired cases remain.

All row provenance has `usage=validation_only_never_train` and `label_basis=rule_verified`. The Data validator rejects that usage marker on a train row. Model owns its separate ingestion-boundary guard; Data did not edit training code. Current validation-only shards do not enter training. A marker cannot detect arbitrary untracked paraphrases: derivative exclusion is also a durable procedural constraint.

## Quality and corrections

Final structure: 96 valid rows, no exact canonical duplicates, conflicting exact-input targets or cross-split group overlap. Eighteen within-policy lexical pairs are expected paired variants. Against 1,809 historical Data rows (v2/v1/tiny deduplicated by ID): no exact ID/group/input/state matches and no raw or numeric-masked state-trigram candidates at Jaccard ≥0.3. Separate bounded semantic comparison inspected 16 matching historical **training** cases. This does not establish semantic independence or clear Evaluation-owned probes; Evaluation must supply its own final-hash exclusion receipt. Data read no Evaluation/probe/final rows.

Two isolated producers authored the planned policies. Structured recomputation passes **96/96**, including exact rendered state/question correspondence. The initial target-hidden review agreed **31/32**, finding a packing reserve-doubling ambiguity despite all structured solvers agreeing. A new geometry revision explicitly says the listed reserve is the final requirement; no numerical fact or target changed.

Final-content target-hidden agreement covers **64/64 decisions across 40 policies**: 52 unchanged non-cooldown r2 inputs plus all 12 final cooldown inputs. The r3 review also rechecked the clarified packing case, which overlaps rather than increasing the unique denominator. These are separate-session teacher agreements using the same exposed `openai/gpt-sol` alias, immutable revision unknown—not independent model-family or human ground truth. Rule recomputation likewise establishes consistency, not independently authored proof.

Before any prediction request, 87 incorrect ordering options were revised across 36 cases. Policy facts, states/questions, labels, target texts/slots, IDs and splits remained unchanged. A later geometry revision changed seven incorrect offered clock alternatives and matching source `facts.starts` entries; policies, bookings, states/questions and correct targets remained unchanged. All initial and intermediate artifacts remain preserved.

| Descriptive construction diagnostic | Original | Released |
| --- | ---: | ---: |
| Discount unique `v+1, v−2` option fingerprint | 12/12 | 0/12 |
| Rounding target at interior numeric rank | 12/12 | 4/12 |
| FIFO most-zero allocation, first tie | 9/12 | 3/12 |
| Cooldown second-earliest clock choice | 11/12 | 4/12 |

Residual hints remain: FIFO fewest-zero selection hits 6/12; rates target slot two occurs 6/12; 11/12 scheduling targets are not the none choice; some boundary cases are easy. Released clock-rank hits are 4/4/3 for earliest/second/latest, plus one none target. Authoring diagnostics are descriptive, not held-out shortcut estimates, model improvements or proof of shortcut-free content. No further heuristic-driven authoring is planned for this release.

Exact pinned all-MiniLM tokenizer audit: **361 candidate pairs, maximum 129 tokens; zero overflow/question/candidate loss at 256**. At 128, one pair loses question content. Preserve the intended 256-token/native-run prediction profile.

## Evidence and publication

All paths below are relative to `/Users/destiner/Code/jeff/artifacts/data/data-d3-seen-rules-v1/`:

- `release/manifest.json`, `case-metadata.json`, `provenance.json`, `exclusion.json`, `validation.json`, `freeze.json` and `shards/`.
- `release-path-validation.json`: actual validation through the final published paths.
- `review/review.{json,md}`: preserved first-pass findings; `review-r2/` and `review-r3/`: frozen judgments, executable consistency checks and final coverage.
- `ordering-r2/`, `geometry-r3/`: published source revisions, assignments, audit inputs/helpers, deterministic revision recipes, metadata and change maps; originals remain alongside them.
- `token-budget-r3.json`; `code-review/` and `code-review-r2/`.

The bounded `jeff.data.freeze_diagnostic` command captures producer shard bytes into a new publisher-owned staging directory. It verifies preauthoring allocations, exact claimed training-shard membership, historical exclusions, costs, counts and the captured rows. With `--review-manifest`, published shard hashes/counts must equal the reviewed candidate's bindings. `freeze.json` indexes every bundle file plus helper-source and supplied external-evidence hashes. A completed directory is atomically renamed into a previously nonexistent destination under the cooperative single-publisher workflow. Failed staging is not a release. Existing versions are never overwritten.

`validation-input.json` is the recorded staging validation input; its old temporary paths are evidence, not the consumer manifest. Consumers use only **`release/manifest.json`**, never directory globs. Reviewed r3 candidate and release manifest hashes differ because snapshot paths differ; both contain exactly the same two shard payloads.

For a future explicit publication/reproduction, use new output/report paths, the fixed config, `--review-report`, `--review-manifest`, and repeated `--evidence` paths. Do not rerun producer/repair mains in published directories: some historical scripts overwrite outputs. Plain `python -m jeff.data.validate --manifest ... --artifacts-dir ... --output <new-report>` needs no ML stack. Token auditing uses Research's separately hashed tokenizer/helper; no model weights are loaded.

No software tests/lint, training, ML slot, protected-data access, external upload or separately billed generation. Additional actual/pending spend: **£0/£0**. Existing provider terms apply; no independent redistribution-license claim.
