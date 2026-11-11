# R3 — frozen v2 candidate shortcut and source audit

## Decision summary

**The first frozen v2 candidate broadens synthetic coverage and fixes deterministic choice-order construction, but a substantial intent answer-length shortcut survives.** Without state or question, longest-character selection matches **53/80 new intent validation labels (66.25%)**, versus **18/20 inherited labels (90%)**. It is an available construction cue, not evidence that a neural model uses it.

Data received these findings directly and independently measured the same counts. Its handoff `006-v2-review-findings-and-revisions.md` says immutable intent-a-r2 / intent-b-r2 option revisions and a sentiment-b-r2 wording correction are underway. **This report audits pre-review-r2, not those revisions or a training release.** Keep original evidence; do not transfer its results or hash to a superseding manifest. Research is advisory, not a publication gate.

The historical split checks found no v1/tiny validation reuse in training by identifiers, canonical full input or state. A separate published-validation-probe exclusion check was requested directly from Evaluation; this report does not claim all historical validation has been excluded semantically. No final-evaluation data was accessed.

## Frozen identity and evidence levels

- Candidate: `artifacts/data/data-pilot-v2/pre-review-r2/manifest.json`, SHA256 **`345e935b46ca3d1226dfd603208bf5d1e1e16982d425319f678e34447b0c9483`**.
- Parent: `artifacts/data/data-pilot-v1/manifest.json`, SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`.
- Data's existing CPU audit: `artifacts/data/data-pilot-v2/quality-audit/audit.json`, SHA256 `d044f6d2e55594962648a10344f441a8577cac598b523acff915c7b3c2fe2c17`.
- Research artifact root: `/Users/destiner/Code/jeff/artifacts/research/r3-20261111T1124/`.

Read current owner instructions, Data's findings and completed [R2](pilot-v1-generalization-audit.md) first. Adopted the existing clean Research workspace and safely fast-forwarded `36af3bb` → `5ee2b18`; no recreated/reset workspace or repeated R1/R2 investigation.

**Measured here:** all 18 candidate shard hashes/counts/splits; inherited identities; targeted R2 helper reproduction for new/combined strata and six producers; historical exact-boundary checks; bounded source/configuration counts. Three fresh read-only subagents covered construction, breadth and lineage. They inspected 48 construction-sample rows plus six targeted intent examples, and 61 breadth-sample rows (samples can overlap). Parent reviewed material evidence and reproduced the new/combined shortcut summaries exactly against Data's receipt.

**Reused, not rerun:** R2's inherited diagnostics; Data's full lexical scan, tokenizer audit, and separate-session label reviews. No producer program, model, tokenizer or full lexical scan was executed by Research in R3. The reproducible companion imports the unchanged R2 helper instead of rebuilding the diagnostics; [execution notes](../../experiments/research/v2-candidate-audit.md) define its scope.

## 1. Like-for-like construction diagnostics

Counts are agreement with supplied labels, not neural accuracy or independently verified correctness. Fixed selectors use the same R2 character/normalized-word definitions and first-input tie break. Uniform is mean `1 / choice_count`, not deterministic first-choice performance.

| Family / stratum | Train rows | Longest characters | Validation rows | Longest characters | Longest words, validation | Uniform expected, validation |
|---|---:|---:|---:|---:|---:|---:|
| Intent inherited v1 | 100 | 84 | 20 | 18 (90%) | 18 | 25.83% |
| Intent new v2 | 400 | 243 | 80 | **53 (66.25%)** | 35 | 27.50% |
| Intent combined | 500 | 327 | 100 | 71 (71%) | 53 | 27.17% |
| Sentiment inherited v1 | 100 | 25 | 20 | 6 | 5 | 25% |
| Sentiment new v2 | 400 | 100 | 80 | 21 | 20 | 25% |
| Sentiment combined | 500 | 125 | 100 | 27 | 25 | 25% |
| Rules inherited v1 | 100 | 25 | 20 | 7 | 6 | 25.33% |
| Rules new v2 | 400 | 122 | 80 | 21 | 24 | 27.40% |
| Rules combined | 500 | 147 | 100 | 28 | 30 | 26.98% |

### Intent: improvement does not remove the shortcut

Both new producers contribute: intent-a **138/200 train, 28/40 validation**; intent-b **105/200, 25/40**. **52/80** new validation targets are uniquely longest, so 52 of the 53 matches do not depend on ties. Shortest characters matches only **5/80** new validation labels. This is not one anomalous producer or an artifact of one tie rule.

Equal word counts are insufficient. Five validation rows per producer have equal whitespace-word counts across choices but a uniquely longest correct answer. For example, `data:pilot-v2:intent-a:g226:r01` offers “Recover candidate portal access” against “Register a new exam” and “Post a paper certificate”; all have four words. The individual options can be sensible while systematic relative specificity/character length remains exploitable.

The descriptive reduction from 90% to 66.25% is not a paired causal repair estimate: new domains, scenarios and choice-count mix differ. Nor does any length diagnostic identify how M2/M3/M4 predict. Existing and subsequent model comparisons need the corresponding state-free baselines and inherited/new strata.

### Ordering and sentiment: supported improvements, limited claims

Read-only inspection of all six new generators supports independently seeded balanced target schedules **and shuffled distractors**, rather than inserting the answer into a canonical rival list. New pooled publication-cycle matches fall to **23/80 intent**, **25/80 rules**, versus **20/20 each** in inherited v1. This diagnostic depends on publication order and shard boundaries; it is not an available independent-example feature or a permutation-invariance measurement.

All **480 new sentiment rows offer all four classes**. Each producer has five complete wording styles, each equally represented within target class and split; both training producers realize all 24 class-order permutations. V1's published sentiment-r2 already had complete availability, so do not claim v2 newly fixes the excluded original availability defect. New length selectors show no intent-sized effect, while finite answer paraphrase sets remain.

Residual rhetoric is narrower than raw group counts suggest. In sentiment-a, “though” appears in **23/50 mixed training and 7/10 mixed validation** rows, but no other-class rows. This can be legitimate contrast evidence, not an invalid cue to ban. Implicit sentiment remains a review issue: `sentiment-b:g134:r01` was sent to Data as an ambiguity question, **not** an established wrong label. Data separately identified a different wording error in `sentiment-b:g011` and is correcting it without changing its positive class.

Rules show no analogous global length effect. A local limitation remains in `rule-a:g011:r01–r04`: longest-common-substring choices prioritize whole input strings and a truncated target. They can permit filtering impossible strings and choosing the longer remaining common candidate, without challenging the stated optimum/tie rule. This is limited distractor difficulty, not demonstrated incorrect labels; it does not justify changing frozen examples in place.

## 2. Breadth: count the right units

| Stratum / family | Train rows / declared groups | Validation rows / declared groups | Additional unit |
|---|---:|---:|---|
| Inherited intent | 100 / 25 | 20 / 5 | Domain clusters, four cases each |
| Inherited sentiment | 100 / 25 | 20 / 5 | Domain clusters, four cases each |
| Inherited rules | 100 / 10 | 20 / 2 | Named mechanism groups |
| New intent | 400 / 400 | 80 / 80 | **40 / 8 named domains**, ten singleton scenarios each |
| New sentiment | 400 / 400 | 80 / 80 | **40 / 8 named domains**, ten singleton scenarios each |
| New rules | 400 / 20 | 80 / 10 | **200 / 40 authored policy instances**, two cases each |
| **Combined all families** | **1,500 / 880** | **300 / 182** | Heterogeneous grouping units, not iid samples |

Singleton scenario IDs do not turn eight validation domains into 80 domain holdouts. Group-count growth is not like-for-like independence growth: the grouping unit changed for intent/sentiment. Combined rule coverage is **30 training / 12 validation named mechanism groups**, still below the aspirational 100/20 group target; Data explicitly reports the shortfall rather than renaming policies as independent mechanisms.

The six new producer jobs identify the **same exposed teacher alias**, with immutable model revision unavailable. They are separate synthetic authoring streams, not six independently collected sources or diverse teacher models. New intent/sentiment labels remain teacher references; rules remain programmatic/rule-verified with same-author solver limitations. Data reports label-hidden review agreement of 40/40 intent, 40/40 sentiment and 60/60 rules, plus 480/480 same-author rule recomputation. Those are **Data-reported checks**, not independent ground truth or R3 label certification.

“Policy instances” is defensible; “240 independent specifications” is not. Exact within-group structured `policy` objects number **192 training / 29 validation**, versus 200/40 authored instances. This narrow object comparison is **not semantic deduplication**: wording/field labels can live outside the object and entity strings inside it can inflate uniqueness. Four postfix instances share one formal configuration; four bracket instances share two. Keep useful varied cases, but distinguish cases, configurations and named mechanisms.

New operations do meaningfully broaden coverage: rounding, permissions, coordinate composition, proportional allocation, string/stack operations and more. However, exact names do not establish computational novelty:

- Weekday progression includes all-seven-day subcases of inherited cyclic indexing.
- Cooldown scheduling reuses interval conflict; nested routing includes ordered-conditional subcases familiar from first-match routing.
- Held-out parity constraints reuse modular-sum arithmetic; bracket and postfix holdouts share stack primitives.

No full-task equivalence between new validation algorithms and training was established by the bounded review. These relationships are transfer opportunities, **not demonstrated source leakage**. Describe validation as **named-group-disjoint**, not universally unseen computations. Dedicated same-complete-mechanism/new-scenario validation remains absent; the set cannot by itself diagnose retention on trained algorithms.

## 3. Inherited versus added data and validation exclusion

- All **6/6 v1 shard entries and 360/360 inherited row objects** remain unchanged; hashes establish unchanged shard bytes.
- Combined **1,500 train / 300 validation** = inherited **300/60** + added **1,200/240**. Exactly 1,800 unique IDs; no inherited/added group overlap.
- “Added” or “new v2” describes shard/ID lineage, not proved semantic novelty or untouched evaluation. The **60 inherited validation rows are reused development evidence**, and this audit also makes the new candidate validation development-inspected.
- Across candidate plus tiny data: **0/1,071** group IDs and **0/240** nonempty policy-scenario IDs cross splits.

Independent lineage comparison found no current-train matches by ID, group, scenario, canonical full input or state alone against:

| Reference | Rows | Current-train comparison pairs | Matches |
|---|---:|---:|---:|
| Manifested v1 validation | 60 | 90,000 | 0 |
| Tiny validation | 3 | 4,500 | 0 |
| Current candidate validation | 300 | 450,000 | 0 |

These comparison populations overlap; do not add denominators as independent evidence. Canonical equality uses NFC and outer whitespace stripping, preserves signs/brackets/case/internal whitespace, and ignores option order for full-input comparison. It is not literal input byte equality or semantic derivative detection. No hash check can establish authors' historical exposure.

Data's existing lexical audit covers **1,809 candidate-plus-tiny rows**, not just 1,800 candidate rows: **473 raw / 1,507 number-masked** high-overlap pairs, all within groups; no cross-split pair even at 0.2 in **456,318** comparisons. Research reused this result rather than repeating the scan. Word-only normalization removes meaningful symbols: five normalized full-input collision clusters are **not** five exact duplicate clusters. Absence of these lexical matches is not semantic clearance.

**Published probe boundary:** Data's historical receipt lists v1/tiny only. Evaluation's separate **24 validation-probe presentations / 12 groups** are not covered by that receipt. Research asked Evaluation directly to compare those published probes against candidate training and record hashes/exclusion findings, without broadening Data access or inspecting reserved final storage. At this report's initial preparation, this was **unchecked coverage, not observed contamination**. See subsequent Evaluation/Research handoffs for its disposition; do not characterize a request as a completed check.

## 4. Actions delivered to owners

1. **Data:** retain immutable versions; revise relative intent answer specificity/length rather than only word counts or padding. Data already has bounded r2 repairs underway. Recheck both shortest/longest character/word selectors and hash lineage on the superseding freeze; these inspected diagnostics are not a shortcut-free benchmark or proof of model gains. Keep policy/domain/mechanism units honest.
2. **Model / Evaluation:** compare models on identical frozen references, retaining inherited/new/probe strata and length baselines. Report domain-level summaries for new intent/sentiment and mechanism-level summaries for rules where available; singleton-group macro scores alone conceal domain clustering. No model promotion, retraining order or new ML allocation is made by Research.
3. **Evaluation:** own the scoped published-probe exclusion comparison and qualify historical-isolation claims until recorded. Preserve the final-data boundary. No reason to wait for Research sign-off on unrelated authorized work.

Direct handoffs: `artifacts/handoffs/research/20261111T1124-R3-adopted-candidate-audit.md` and `20261111T1129-R3-material-findings-and-probe-exclusion-request.md`. Detailed evidence is in `construction/`, `breadth/`, `lineage/` and `reproduction/audit.json` under the Research artifact root. The final delivery handoff records actual integration/build receipts and any later candidate/probe status.

Scope: only Research-owned tracked paths; ignored immutable Research artifacts/handoffs. CPU-only, no dataset/label/producer edits, model jobs/downloads, paid services, final-evaluation access, tests or linting. £0 additional actual / pending. R3 is a bounded candidate investigation, not an ongoing survey or approval gate.
