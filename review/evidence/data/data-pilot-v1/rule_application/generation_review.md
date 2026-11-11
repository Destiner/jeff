# Rule application pilot shard r1

## Frozen handoff

Root: `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/rule_application/`

- `train.jsonl`: **100 rows**, g01–g10, 10 rows per group.
- `validation.jsonl`: **20 rows**, g11–g12, 10 rows per group.
- `group_assignments.json`: written before row authoring; full namespaced group IDs and frozen split/mechanism/domain assignments.
- `metadata.json`: teacher/source identity, settings, costs, constraints, limitations and shard hashes.
- `generate.py`: deterministic local CPU generator, including original explicit policies and curated cases.
- `audit_cases.jsonl`: 120 structured audit fact records, not model inputs.
- `audit.py`: separate rule recomputation plus structural dataset validation; does not import the generator.
- `validation_report.json`: executed audit findings, outcome/position counts and file hashes.

No checkout files, Git, manifests, model/evaluation code, external datasets, private real data, evaluation artifacts or final data were inspected or modified. This handoff creates no manifest; the parent owns assembly. Nothing was written outside this assigned artifact directory.

## Group plan

All groups use prefix `data:pilot-v1:rule_application:`.

| Groups | Split | Distinct mechanisms |
|---|---|---|
| g01 | train | Ordered first-match routing and precedence |
| g02 | train | Progressive marginal-band charge accumulation |
| g03 | train | Greedy capacity admission, skipping oversized requests |
| g04 | train | Signed cyclic indexing with wraparound |
| g05 | train | Signed weighted score and interval classification |
| g06 | train | Symmetric difference of entitlement sets |
| g07 | train | Half-open time interval intersections |
| g08 | train | Longest matching prefix routing |
| g09 | train | Position-weighted modular checksum |
| g10 | train | Finite-state transition execution |
| g11 | validation | Directed graph transitive reachability |
| g12 | validation | Strict pairwise-majority Condorcet selection |

Validation mechanisms are held out entirely, not renamed training thresholds. There are only **two independent validation generator mechanisms**: 20 rows must not be described as 20 independently sampled rule families. Within-group policy renderings are template-based; case parameters, boundaries, topology, ordering and outcomes vary meaningfully, but linguistic coverage is limited.

## Labels and source

Rules, cases, renderer and verifier were authored in this existing agent session. Actual exposed alias: **openai / gpt-sol**. Immutable model revision and temperature are **unknown**. No model was loaded and no additional model, network or API calls were used.

All rows use `provenance.kind = programmatic`, `label_basis = rule_verified`, and source `data-pilot-v1/rule_application/original-rule-job-r1`. This basis is supported by executed separate recomputation on **every row**. The verifier derives expected choice text from structured facts before checking the target option ID. Examples of algorithm separation: per-hour fee summation versus closed formula; modular indexing versus deque steps; endpoint overlap versus minute-set intersection; graph traversal versus all-pairs closure; direct ballot ranking comparisons versus a pairwise tally matrix.

The natural-language semantics and audit facts are teacher-created. The verifier is independently implemented, **not independently authored**. Self-review and two implementations do not independently prove the language-to-facts mapping. Audit facts, IDs, provenance, group IDs and targets are metadata, never substitutes for the full state text or model input.

## Commands actually executed

Both local commands succeeded twice during pre-publication refinement:

```sh
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/rule_application/generate.py
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/rule_application/audit.py
```

The second generation replaced the unreported draft to balance target positions and categorical outcomes; this is the frozen r1 handoff. No further shard edits after completion reporting.

Executed dataset checks: JSONL parsing; contract fields, types and schema/family/split; nonempty state/question/choice text; 2–6 unique meaningful supplied options; one target; namespaced unique row IDs; exact frozen group/split assignments; exactly 10 rows per group; no cross-split group overlap; no exact canonical-input duplicates ignoring option order; independent rule answer agreement on **120/120** rows. Observed option counts are 2–5. Target positions rotate deterministically within each split/choice-count stratum, with counts differing by at most one. Training four-choice rows have target counts 17/17/17/16; validation four-choice rows have 4/4/4/4.

Text spot review: the same agent read the full rendered states, questions, choices and marked targets for r01 and r10 of every group (**24 rows**), including zero rental hours, skipped cargo, signed wraparound, empty sets, touching endpoints, fallback prefixes, modular remainders, ignored controller events, a graph self-loop and election ties. No ambiguity or target mismatch was found in these reviewed rows; this is not an independent human/model review. No semantic embedding near-duplicate check was run; related rule cases are intentionally grouped.

Outcome balance: routing 2/3/3/2; score 3 reject / 3 hold / 4 release; controller 3 locked / 4 open / 3 occupied; election 5 elected / 5 nobody. Other mechanisms have several exact numeric, set, route or conflict results; full counts are in the report. Some distractors are easy and small option-count strata cannot cover every target position.

No software tests, test runners, linting, build, training or model evaluation were run. This artifact-only dataset task has no build deliverable.

## Usage and cost

Original synthetic content, generated through existing approved provider access; use is subject to applicable existing provider/account terms and project permissions. **No separately asserted redistribution license** or blanket independent clearance is claimed. No external datasets or private company/customer data were used.

**£0 additional spend; £0 pending spend.** Existing access was not separately metered. Local standard-library Python CPU generation and validation only.
