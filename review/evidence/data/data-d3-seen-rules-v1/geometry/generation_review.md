# Geometry: D3 seen rules, new policies

## Frozen delivery

48 validation-only decisions; 24 policy groups; 4 mechanisms, 12 rows each. Each mechanism has six policies in the config's exact domain order, with two source cases per policy. No training file or manifest was created. All writes were confined to this geometry directory; no Git, mailbox, checkout edits, old example inspection, network, API, model invocation, tests or lint were used.

`group_assignments.json` was written before authoring policies or source cases, directly from the frozen config. It records the validation split, mechanism, policy/domain, and named training group. Source groups use `data:d3-seen-rules-v1:<mechanism>:p01` through `p06`; rows append `:c01`/`:c02`. These are new groups, not reused training groups.

## Files

- `validation.jsonl`: the 48 contract-0.1 rows, now marked `rule_verified` after the successful audit.
- `group_assignments.json`: 24 pre-authoring assignments.
- `source_cases.jsonl`: original authored policies, structured case facts, contexts, and applicable distractors/listing order.
- `audit_cases.jsonl`: the same facts without authored distractors and without targets/answers.
- `generate.py`: deterministic original source definitions, rendering, computed labels and full choice shuffle; seed **704931**.
- `audit.py`: pure `expected(case)` plus post-generation comparisons and correspondence checks; no generator import. The pure function does not read labels, files, or saved targets.
- `semantic_review.json`: same-agent semantic notes and manually worked answers for **both cases in every policy**, after reading generated states, questions and options. This exceeds the required one-per-policy self-review.
- `validation_report.json`: actual checks, per-case computed answers and results, distributions, and correction history.
- `metadata.json`: provenance, constraints, source/config/assignment revisions, hashes, teacher alias and cost.

## Policy novelty versus mechanism familiarity

Mechanism overlap with the named v2 training groups is **intentional**. This is a seen-mechanism/new-policy development diagnostic, not an unseen-mechanism challenge or broad training expansion. The only training information consulted was the config's named mechanism/group identities; no historical row text, labels, probes, or final data were inspected. Original authorship is procedural evidence here, not a content-similarity certification against uninspected corpora.

- **Packs:** six domains use pack sizes 8/12/10/25/6/16 and minima 3/2/1/4/2/1. Policies distinguish deficit-only procurement from mandatory scheduled purchases. Cases include unusable returned inventory, protected reserves, zero shortage, exact multiples, one-unit-over thresholds, and a minimum overriding an otherwise sufficient smaller order. The reflector cases deliberately both require two packs for different deficit relationships.
- **Rates:** exact output/time, usable/input, time/output and intact-output/labour rates. Minimum-time and maximum-throughput conventions differ, as do earliest/latest-name tie breakers and three/four candidate sets. Cases contrast real ties with close unequal rates, raw-count traps and separate operational trials. Some policy pairs legitimately choose the same candidate for different reasons.
- **Coordinates:** six distinct ordered affine procedures use different translations, swaps, mirrors and turns, always expressed as explicit coordinate assignments. New anchors/cues/control points include axis crossings and exact-origin registration. Cases are paired within their own policy; operation order is never shuffled.
- **Cooldown:** new durations 12/20/7/18/25/10 minutes and reset gaps 8/5/13/12/15/6 minutes. Policies differ on whether reset must finish before closing or only the session must. Cases distinguish exact endpoints, unavailable one-minute-earlier starts, extended existing sessions, closing overruns and multiple feasible starts. One case has no listed feasible start.

Contexts and facts were authored for these source cases, not derived from old numerical substitutions or paraphrases. The paired coordinate cases necessarily share the policy's transformation sequence; likewise the other pairs intentionally share their policy. They must not be treated as independent policy samples.

## Actual audit and review

Successful invocation: `python3 audit.py` from this directory (or using its absolute path). All 48 targets match the separate-algorithm answer exactly; each expected answer occurs once among unique options. Final automated audit failures: **0**. All 24 policies have two rows, and all four mechanisms have 12.

Generator/auditor algorithm distinction:

| Mechanism | Generator | Pure audit |
| --- | --- | --- |
| packs | integer ceiling and minimum | repeated accumulation of pack units |
| rates | streaming cross-product comparison | exact `Fraction` sort, stable tie order |
| coordinates | sequential point updates | compose homogeneous matrices, then apply once |
| cooldown | candidate-wise interval compatibility | union forbidden integer start sets, subtract from operating window |

Full rendered state/question correspondence is checked against structured facts for all 48 rows, alongside option identity, source/audit equality, IDs, frozen groups, split, provenance and arity. Semantic review separately read policy wording against the facts and worked both cases per policy. That self-review found **four duration-scope problems** before verification: extended existing appointments conflicted with wording implying every appointment had the new-session duration. Those policies now explicitly give the fixed duration only to new bookings and honor existing stated end times. Numeric facts and computed answers did not change. Three pack distractor sets were also improved to permit maximum correct quantities rather than making every positive answer interior. A stock-count wording issue was tidied. These are authoring-stage corrections, not hidden successful audit claims.

### Shuffle and compactness

Target slots are balanced within each arity, then randomly assigned, not published in a cycle. Distractors and rate candidate listings use separate random shuffle calls. Ordered transformations and existing chronological bookings are preserved.

- 37 four-option rows: target-position counts **10, 9, 9, 9**.
- 11 three-option rows: target-position counts **4, 4, 3**.
- Rate winners appear in state-list positions 1/2/3 **3/4/5** times; they are not always first-listed.
- Maximum state length: **67 whitespace-separated words**. No tokenizer/model was run; the parent's 256-token input-pair audit remains required.
- Strictly shortest correct option: 5 rows; strictly longest: 2. Many equal-length choices tie for shortest/longest. There is no universal answer-length rule, but these small diagnostics cannot exclude every stylistic cue.

## Label, usage and cost limits

These are **same-agent separate-algorithm consistency checks**, not independent authorship, an external semantic audit, or real-world validation. The parent will separately review rendered text. Computed provenance is `kind: programmatic`, with `label_basis: rule_verified` set only after the successful post-generation audit. The actual exposed author alias is **openai / gpt-sol**; immutable model revision and harness temperature/top-p/sampling seed are unknown. No immutable revision is invented.

All content is original synthetic content under existing provider terms. No private records or additional redistribution license are asserted. **Additional spend £0; pending spend £0.** Only lightweight Python standard-library CPU work was used.

Permanently **validation only, never train**, including all related variants and derivatives. This is a development diagnostic with familiar mechanisms, newly authored policies, and paired dependence—not final evaluation evidence. Outputs are frozen at handoff; hashes of the delivered data, source, assignments, auditor, report and review are recorded in metadata. No further regeneration is planned.
