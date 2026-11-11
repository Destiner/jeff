# D3 r2 — final read-only semantic review

**Verdict: pass with residual limits. No must-fix semantic, target, correspondence, mapping, revision-scope, or hash findings.** This is developmental validation evidence for **96 rows, 48 paired policies, 8 intentionally seen mechanisms**, not iid, unseen-mechanism, or final evidence.

## Blind decisions, then verification

The target-hidden projection emitted only `id`, `state`, `question`, and `options`. An initial broad projection exposed input text for additional rows, but no labels or source facts; the exact 56-row projection was then saved as `blind-inputs.jsonl`. Direct judgments covered all 36 FIFO/discount/rounding rows, plus `p01:c01`, `p02:c02`, `p04:c01`, and `p06:c02` for lexicographic and each of the four geometry mechanisms. No producer source, solver, generator, or target was inspected before freezing.

All **56 decisions and individual rationales** are preserved verbatim in `frozen-decisions.json` and embedded in `review.json`. Frozen file SHA-256:

`4f01a433131b05dc2798d165e05c8a213b7bf71bb9496aba8235fc94cab3082f`

After freeze, **56/56** selected option IDs agreed with the candidate labels. No sampled row supported multiple choices, omitted a necessary rule, or had an incorrect numerical target. Examples of consequential details explicitly honored:

- Packs `p06:c02`: reserve 10 is explicitly the final requirement after doubling; accepted stock is 20, deficit 32, hence **2 packs**, not a second doubling.
- Packs `p04:c01`: the explicit demand/reserve/stock counts produce a three-pack deficit, overridden by the four-pack minimum. The contextual repair narrative does not override the counts.
- Rates: exact fractions and the specified earliest/latest alphabetical tie directions determine Aster, Ivo, Birch, and Blue in the sampled rows.
- Scheduling: resets are required on both sides; final reset overrun is permitted only in the policies that explicitly permit it. Earliest **listed**, not earliest imaginable, start is chosen.
- Rounding: decimal halfway values are exact; higher multiple is selected at equality. No binary-float interpretation was substituted.

The remaining 40 rows received structured arithmetic and exact text-correspondence checks, **not a claim of 96 blind human-like semantic decisions**. Matching the same teacher alias is not independent groundtruth.

## Full 96-row verification and revision scope

`check.py` imports the fully inspected audit modules with bytecode disabled. It calls only pure `expected` and geometry `correspondence`, or ordering's equivalent `stated`. **Neither audit main was run**: those mains can overwrite producer artifacts and retain obsolete original distractor assumptions.

Results: **96/96** unique exact expected options and matching selected targets; **96/96** exact state/question correspondence; **96/96** source/audit correspondence and case → policy group → mechanism mappings. Group assignments, source domains, row provenance mapping, validation split, and intentional-seen/training-excluded metadata correspond. Each policy has two cases. All ordered option IDs, selected IDs and selected texts remain unchanged.

Parent-versus-revision checks found:

- Ordering: exactly **87 changed distractor texts**, confined to FIFO, discount, and rounding. All source/audit policy facts and rendering order are unchanged. Only the allowed provenance source/teacher representation fields additionally differ. Lexicographic choices are unchanged.
- Geometry: one logical context clarification, packs `p06:c02`, appears in source context, audit context, and the corresponding state substring. No policies, numeric facts, options, labels, or other rows change.
- Both pure audit helpers and group-assignment files are byte-identical to their respective parents. No mechanism drift was found.

### All 36 revised choice sets

After the blind freeze, every **96 wrong slot** across these 36 rows was checked against its saved construction and reviewed for semantic plausibility. `review.json → distractor_review` preserves every exact option string, error program, rationale, and result. The 96 constructions exceed 87 text changes because some reconstructed wrong slots retain their old text.

- FIFO alternatives exhaust a different batch priority; all obey capacities, nonnegativity and requested totals. They are feasible allocations but violate the stated FIFO rule.
- Discount alternatives reflect reversed steps, omitted/repeated credits or percentages, original-base percentages, additive percentages, or cash/percent confusion. Values match these descriptions and none is another correct interpretation of the explicit sequence.
- Rounding alternatives reflect wrong grids, floor/ceiling, or lower-halfway mode. All retain the displayed unit and precision. Some coarse grids are less compelling distractors than nearby errors, and off-grid values can be rejected without completing the calculation; these are residual difficulty limits, not additional supported answers.

The inspected pure construction functions were extracted from the revision script's AST and called without executing any revision top-level code. This corroborates construction arithmetic, not independent authorship. No generator or revision main was executed.

## Recomputed choice-only diagnostics

First-option tie-break applies to first/length/zero-count heuristics. Lengths count exact characters, including symbols/case; fractional tie credit is also recorded in JSON. No answer or option was optimized or rewritten.

| Mechanism (12 rows each) | First option | Shortest, first tie | Longest, first tie | Numeric ranks, ascending |
|---|---:|---:|---:|---|
| Packs | 4 | 0 | 6 | 1:1, 2:5, 3:5, 4:1 |
| Rates | 2 | 5 | 1 | Not scalar option values |
| Coordinates | 3 | 2 | 3 | Not imposed on coordinate pairs |
| Cooldown | 5 | 6 | 1 | 2:11, 4:1 |
| Lexicographic | 4 | 4 | 1 | Not scalar option values |
| FIFO | 4 | 4 | 5 | Not imposed on allocation vectors |
| Discount | 2 | 1 | 2 | 1:3, 2:2, 3:5, 4:2 |
| Rounding | 3 | 3 | 3 | 1:3, 2:2, 3:2, 4:5 |

Across all 96 rows, first-option selection hits **27/96**. Ranks are descriptive, not an assertion that arbitrary vector/name options have a canonical numerical ordering. For cooldown only, “No listed start fits” is ordered after listed times for this diagnostic; **second-earliest listed time** selects the target in **11/12** rows. This is a substantial residual scheduling prior and should be disclosed rather than generalized as rule competence. First displayed candidate hits lexicographic **4/12**, rates **3/12**.

Specific disclosed fingerprints were independently recomputed from the allowed original and revised producer rows:

- Discount unique `v+1` / `v−2` candidate: **original 12/12 present and correct; revised 0/12 present, 0/12 correct**.
- FIFO most zeros: original **9/12**, revised **3/12**; fewest zeros: original **1/12**, revised **6/12**.
- Rounding interior target: original **12/12**, revised **4/12**. Revised maximum numeric choice still hits **5/12**; minimum hits **3/12**.
- Revised discount numeric ranks remain uneven: third-smallest **5/12**, interior **7/12**. Rates shortest-first hits **5/12**, with strictly shortest target **4/12**.

These tiny descriptive counts do not establish absence of broader shortcuts. Low-demand FIFO necessarily leaves depleted/unused-batch signatures. Target slots are preserved, not newly randomized. Common templates, paired policies, repeated mechanisms and authoring dependence remain. The r2 candidate has already been revised following exposed weaknesses and is not untouched validation.

## Hashes and read-only preservation

- Candidate geometry snapshot SHA-256: `8699ef69adf504a4b8b9e58031431614db699999680c756ec2f8c4258603e1a2`.
- Candidate ordering snapshot SHA-256: `dad4cfb15b36898068413241e1589dd2a235cb77381a7b3537f39d4c7b289252`.
- Both snapshots match the manifest and raw revised `validation.jsonl` bytes.
- All **23** raw-revision hashes in snapshot provenance match; all **17** recorded parent references match; **40** explicit local metadata/manifest/freeze hash references match.
- **53 allowed input files** were hashed before and after the post-freeze audit, with **no changes**. Exact paths/digests are in `input-hashes-before.json` and `input-hashes-after.json`. This preservation interval starts after blind freeze; no claim of a pre-session historical baseline is made.
- The final audit records **1,342 check instances**, zero failures. The first audit run over-broadly rebased embedded *parent* hashes into revision directories, producing spurious hash failures. The reviewer-only script was corrected to use explicit local hash maps and separately validated parent references; no candidate file changed.

## Commands, boundaries, historical record

Actual local actions: `read` on the requested instructions/contracts and manifest; `mkdir -p review-r2`; standard-library `python3` input projection; `python3 review-r2/freeze.py` once before source inspection; bounded `find` file listing after freeze; `read` of revised audit/revision/construction/provenance files; and `python3 -B review-r2/check.py` twice (second stdout in `check-output.json`). `review.json` contains the command ledger and per-check counts; scripts are retained for inspection, not as a test suite.

No tests, lint, Git, mailbox, network, model/tokenizer execution, spend, Evaluation/probe/final content, or training-shard content was used. All writes are confined to new files under this `review-r2/` directory. No candidate inputs or historical review artifacts were edited.

**Historical record:** the original initial-review finding remains **31/32**, as supplied in the request. No historical review content was opened. The present r2 result does not erase, overwrite, or retroactively replace that finding.
