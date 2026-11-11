# Jeff v2 — rule review

No must-fix found within bounded review; retain limitations below. Not a certification of all rendered prose.

## Scope and evidence

- Candidate: `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/pre-review-r2/manifest.json`; SHA-256 `345e935b46ca3d1226dfd603208bf5d1e1e16982d425319f678e34447b0c9483`.
- 1800 declared total rows; reviewed **480 new rule rows**, not inherited v1 content or other producer rows.
- Actual reviewer: **openai / gpt-sol**, the same exposed alias as both producers. No immutable revision available.
- Prior exposure: manifest, first-row IDs/group/provenance and filenames only before sampling; no displayed labels or source solver/generator before decisions.
- Deterministic label-hidden selection: two rows per each of 30 mechanisms, rotated shortest/longest state quartiles; 60 rows (40 train, 20 validation). State lengths 141–324 characters. Outcomes varied naturally, not through target selection.
- `decisions-frozen.jsonl` was written and hashed before `targets-sealed.json` was read for comparison. All 60 blind choices match saved labels; no sampled ambiguity or must-fix identified. This is agreement, **not estimated accuracy or calibrated confidence**.
- After unblinding: imported each inspected pure **expected(case)** with its real dictionary shape (`mechanism_number` for rule-a; `group_number` for rule-b). All **480/480** recomputations match and have one exact supplied option. This reuses the same-author verifier, not a new independent solver.
- Audit IDs cover all rows exactly; policy/facts/source and scenario correspondence pass for 480 rows; assignment/config split checks pass; metadata-listed source artifact hashes match.
- Both combined: **200 train / 40 validation policy instances**, two rows each; **20 train / 10 validation mechanism groups**, not 240 independent mechanisms.

## Semantics, boundaries and rendering

- After decisions, read both audit.py and generate.py, metadata and mechanism plans; mechanically joined all 480 audit/source records and checked configured mechanism/split correspondence. No generator main or audit main/validate executed. rule-b render(case) only was imported/called after inspection for exact source/render join; rule-a source prose concatenation checked directly.
- No direct cross-producer train-to-validation reuse of the ten new held-out mechanisms found in these renderers/assignments. Train rule-a scheduling is deadline feasibility, not validation rule-b topological ordering; train lexicographic ranking differs from validation highest median; generic ordering, arithmetic, strings, and sets overlap intentionally.
- Read historical v1 rule metadata only, not historical rows: graph reachability and Condorcet are validation-only there. Neither new training renderer introduces those mechanisms. New topological graph ordering is also validation-only. This is mechanism/spec inspection, not proof that no semantic historical derivative exists.
- Rendering review found explicit direction, ordering, tie, boundary, units, sign and case conventions for sampled problems. rule-a prose is authored separately from structured facts: exact source joins do not semantically parse prose. rule-b uses shared structured renderer; re-render equality detects drift, not a shared renderer bug. Full independent prose review beyond 60 rows was not performed.

## Integration code (read-only)

- No material blocker identified for this candidate. Assembly retains parent shard entries, enforces allocation counts/splits/family and cost; validator rejects final/unknown manifest splits before shard reads, verifies hashes, detects duplicate IDs/groups and exact full inputs.
- Exact canonicalizer uses NFC and outer strip, preserving signs/brackets/case/internal whitespace. Trigram casefold/word normalization is heuristic only: lexical collisions are not label conflicts.
- Integration audit checks historical exact-input, group and scenario boundaries but cannot prove absence of semantic derivatives; appropriately qualified. It executes an external research script through runpy; that path was not accessed or executed in this review.
- Publication is not transactional: assembly writes candidate/report before all checks finish and multiple final files in sequence. Existing-file guards can leave partial outputs on retries; operational caveat, not evidence of a material data defect here.

## Existing claims versus executed checks

- User reports full structural checks passed and 256-token audit has zero overflow; neither full-manifest validator nor tokenizer audit rerun.
- Producer metadata claims original synthetic authorship, no forbidden producer data access, zero additional spend and same-author separate-algorithm verification. Review confirms declared metadata/hashes and target recomputation, not producer access history.
- 1800 total manifest rows include inherited v1 and other producers. Only manifest arithmetic and 480 new rule rows reviewed; other family and historical content not read.

## Qualifications

- Actual PI_MODEL=gpt-sol, PI_PROVIDER=openai; matches exposed producer alias. This is separate-session blind reasoning, not an independent model/teacher ground truth. Immutable identity unavailable.
- 60/60 is sample agreement with saved labels, not estimated dataset accuracy, calibrated confidence or validation performance.
- 480/480 is recomputation with reused same-author expected(case), not independent algorithms newly authored by reviewer. Both structured audits can share author/spec errors.
- No final/evaluation data, model loading, network/API, paid calls, tests, lint, Git or checkout edits. Existing session access only; zero additional/pending GBP spend.
- No historical content-level comparison or all-family cross-producer data review. Exact parent preservation and full token/structure audit are existing claims rather than reexecuted checks.

## Preservation and spend

- Before/after SHA-256: **25 files**, **0 changed**. Includes candidate manifest and all existing files under both rule producer directories; producer bytes and candidate preserved.
- No producer or checkout edits. Wrote only new files under `review-rules/`. Zero additional or pending paid spend.

## Row decisions (frozen before labels)

| Row ID | Chosen option | Reason | Ambiguity | Comparison | Must-fix |
|---|---|---|---|---|---|
| data:pilot-v2:rule-a:g001:r15 | Reject: too few eligible signers | Visitor is ineligible: zero distinct eligible signers, below one. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g001:r07 | Authorize | Two distinct eligible signers; duplicate legal signature ignored. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g002:r01 | Select candidate C | Urgency 3 ties A/C; C has smaller minutes 8. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g002:r15 | Select candidate Iris | Iris/Noor tie at 4 shifts; Iris travels 15 rather than 20 minutes. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g003:r04 | 3, 5, 1; unfilled 0 | FIFO exhausts Q=3,R=5 then S=1, totaling nine. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g003:r08 | 0, 7, 2; unfilled 3 | Quarantined P skipped; M=7,N=2 leaves demand three. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g004:r06 | 2700 seconds | 5 times 9 times 60 =2700 seconds. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g004:r09 | 140 millimetres | (4 times 3 +2) times 10 =140. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g005:r14 | £70 | (120-20) times .70=70. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g005:r06 | £121.5 | 150 qualifies; (150-15) times .90=121.5. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g006:r02 | 12 credits | Daily capped credits 2+0+10=12. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g006:r11 | 15 credits | 4+6+6=16 before final cap of 15. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g007:r14 | -4 units | -3.1 is .9 from -4 and 1.1 from -2. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g007:r18 | 4 centimetres | 4.12 is .12 from 4 and .13 from 4.25. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g008:r03 | 2X-1Y-3X | Adjacent runs XX,Y,XXX encode 2X-1Y-3X. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g008:r15 | G(2) A(2) G(1) | Runs GG,AA,G encode G(2) A(2) G(1). | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g009:r05 | Feasible: all jobs meet deadlines | Deadline order Y,Z,X completes at 2,5,9, all on time. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g009:r03 | Feasible: all jobs meet deadlines | Starting 5, setup-inclusive finishes 10,14,17 all permitted. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g010:r02 | Deny: requested permission vetoed | Export veto overrides custodian grant. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g010:r06 | Allow the full request | Engineer grants record; producer grants schedule; no veto. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g011:r02 | ABD | ABD is common contiguous length three; cannot extend to four. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g011:r08 | BABA | BABA occurs in both and is length four, maximal. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g012:r02 | Invalid: wrong closing type | After {[( the closing ] mismatches top (. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g012:r08 | Invalid: wrong closing type | After x{y[z](q), top opener is { but next closer is ]. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g013:r01 | A1 B1 A2 A3 B2 | Numeric merge puts A1,B1 then A2,A3 before tied B2. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g013:r03 | S1 N1 S2 S3 N2 | South wins equal keys at 1 and 4: S1 N1 S2 S3 N2. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g014:r03 | Pass all constraints | First set has one 1 (odd), second zero (even). | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g014:r08 | Fail constraints 2, 3 | Constraint 1 odd passes; constraint 2 zero fails odd; constraint 3 one fails even. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g015:r06 | Select candidate M | M and K medians are 9, L is 8; latest name M wins. | None identified | Matches saved target | None |
| data:pilot-v2:rule-a:g015:r07 | Select candidate Pine | Medians Yew 6.5, Oak 7, Pine 8. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g001:r07 | Sun | Next active days after Fri are Sat then Sun. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g001:r15 | Sun | Active starting Sun counts immediately as day one. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g002:r19 | 2 | Seven usable per pack; fourteen demand needs two and meets minimum. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g002:r11 | 2 | 45+5=50 usable, two 25-unit packs. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g003:r06 | News 2; Arts 4; Sport 2 | Floors 2,4,1 leave one for last Sport: 2,4,2. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g003:r15 | Dance 1; Drama 1; Music 1 | Exact .6,1.2,1.2; floor 0,1,1 leaves one awarded Dance by largest remainder. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g004:r18 | 9 through 9 | Integers 5..9 intersect 9..12 only at 9. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g004:r01 | 10 through 10 | 10..25 intersects 5..10 only at 10. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g005:r02 | Tie | 30/2=45/3=15; explicit Tie. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g005:r11 | Vendor A | 7/4=14/8; explicit equality rule selects A. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g006:r05 | (3, 5) | Reflect (2,-1) to (2,1); add (1,4) gives (3,5). | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g006:r20 | (-3, 4) | Negate to (1,-3), swap to (-3,1), translate to (-3,4). | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g007:r05 | 7 | One batch remains; 9-2=7. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g007:r15 | 0 | Discard the sole batch; subsequent removal clamped to zero. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g008:r15 | 22 | 21 is only one minute after 20, insufficient; 22 is two. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g008:r10 | No slot | 65 ends90 leaving10;70 ends95 leaving5;80 overlaps100..120. None has >20 gap before later appointment. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g009:r15 | Rack A | Ignoring underscore leaves B,A,a, matching case-sensitive aAB. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g009:r20 | Roll 3 | Ignoring dots and case leaves tsr, matching rst. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g010:r10 | Half | Score80 meets outer >=80; income26 fails <=25, yielding Half. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g010:r11 | Service | Vibration6 fails >6; hours100 meets >=100, yielding Service. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g011:r01 | 14 | X adds10, I subtracts1 before V, V adds5:14. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g011:r07 | 409 | C subtracts100 before D500; I subtracts1 before X10:409. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g012:r04 | 12 | 3-2=1;12/1=12. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g012:r08 | 24 | (2+3)*5-1=24. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g013:r01 | A → B → C → D | A before B by ready tie; then C after both, then D. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g013:r04 | Proof → Layout → Edit → Ship | Initially Proof and Layout ready; alphabetical last Proof, then Layout,Edit,Ship. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g014:r07 | S | All four codewords distance two from0011; listed last S wins. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g014:r06 | Blue | Distances Red4,Blue1,Gold5,Teal2; Blue unique minimum. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g015:r02 | Positions 1–2 | All two-reading means4; earliest start1. | None identified | Matches saved target | None |
| data:pilot-v2:rule-b:g015:r06 | Positions 1–4 | Four-reading sums8,7,8; earliest maximum start1. | None identified | Matches saved target | None |

## Supporting artifacts

- `blind-sample.jsonl`, `decisions-frozen.jsonl`, `freeze-record.json`, `comparison.jsonl` (option IDs and row reasoning).
- `recompute.json`, `recompute-rows.jsonl` (480 source/target comparisons).
- `hashes-before.json`, `hashes-after.json`, `exposure.json`; selection/freeze/recompute scripts retained for provenance.
- `review.json` contains full structured findings and all per-row records.
