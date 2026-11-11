# data-pilot-v1 — independent-session dataset review

**Disposition:** no observed must-fix dataset-integrity or label issue. **7 findings; 0 must-fix; 0/48 label disagreements.** No label disagreements need resolution before handoff. This is teacher review and consistency validation, not independent correctness proof.

Reviewer: PI_PROVIDER=`openai`, PI_MODEL=`gpt-sol`; actual exposed aliases only, immutable revision unknown. **£0 additional; £0 pending.** No model/API/network calls, tests, lint, Git or checkout edits. No evaluation/final data inspected. All new artifacts are under `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/review/`.

## Integrity and scope

- Recomputed six manifest shard hashes and 17 provenance artifact hashes: all match. 360 rows: each family 100 train / 20 validation; total 300 / 60.
- 72 preassigned groups: 60 train / 12 validation. Intent and sentiment: 25 train / 5 validation groups each, four rows/group. Rules: 10 train / 2 validation groups, ten rows/group. Every row matches its published group allocation; no cross-split group overlap.
- No duplicate example IDs, normalized full-input duplicates, target conflicts on exact inputs, or repeated state/question warnings. Normalization is NFKC/casefold word normalization with order-independent option text; no semantic completeness claim.
- 163 state-trigram Jaccard ≥0.65 pairs reproduced exactly against lead validation.json: all within rule groups; no cross-family or cross-split flagged pairs. See findings for redundancy versus legitimate variation.
- Producer files were hashed before/after CPU checks and again at finalization: unchanged. External assignment-config hash was not recomputed because its source is outside the allowed input roots. No optional tiny data used.

## Spot review protocol and results

- Wrote label-free `selected_inputs.jsonl`, then froze all choices/rationales in `precomparison_decisions.json`, then compared with published targets. Selection is deterministic and target-independent: six spaced groups per split and cyclic row positions for intent/sentiment; shortest/longest state per rule mechanism, with ID tie breaks.
- 48 rows: intent 6 train + 6 validation; sentiment-r2 6 + 6; rules two per each of 12 mechanisms (20 train + 4 validation). All 48 preferred answers match targets; supplied alternatives are mutually exclusive under each question’s stated scope, with no unresolved ambiguity found in this sample.
- **Not fully blind:** sentiment-r2 g01:r01 class P had already been exposed in the revision-map excerpt. That one row is ordinary teacher review. The other 47 were target-label-hidden at assessment, but audit semantics were known. Same model alias as original teacher, independent session, unknown immutable revisions: no claim of independent model or ground truth.
- Rule shortest/longest selection covers several boundaries but missed some outcome variety (both score examples reject; both symmetric-difference examples issue nothing). Confidence is high for explicit sampled text, not a correctness confidence interval.

## Sentiment lineage and rule reproduction

- All 120 source→revision mappings preserve parent teacher class, state, split, group and subject. Parent shard hashes match. Every revised row has exactly all four sentiment classes and the neutral question. Full provenance objects differ because source gains revision lineage; teacher_model and label_basis retain the original teacher judgment. Excluded original sentiment is not treated as the published shard.
- Reproduced **120/120** programmatic rule targets by importing the inspected audit file with `runpy.run_path` (not `__main__`) and calling its actual pure `expected()` function. Required exactly one answer-text match and matching target ID; verified 120 unique audit IDs covering the published rule rows. Never ran the producer main, which would overwrite its validation report.
- This checks published target/options against teacher-authored structured facts and teacher-authored audit logic. It does not independently parse facts from statements or independently establish the rules. The 24 direct rule text assessments improve fidelity evidence, not prove all 120 statements correct.

## Findings

### F1. Legitimate parameter variation, but substantial template redundancy — quality_risk

163 trigram-Jaccard >= .65 pairs reproduced exactly; all within rule groups, none cross-split. All 163 pairs have distinct structured facts and the same mechanism; no identical-fact target conflicts. Read strongest/weakest flagged pairs per each of 9 groups (18 displays, 17 unique pairs). Priority changes, zero/boundary tariffs, modular wraps, score thresholds, empty symmetric differences, endpoint overlaps, weighted remainders, ignored events and voting ties are meaningful cases. Same outcome on different facts is not a conflict. 135 pairs come from routing, set reconciliation and state-machine groups alone. No clear quota-only filler found in sampled pairs, but redundancy lowers effective diversity; motive and semantic nonredundancy of every pair are not established.

### F2. Cross-family domain overlap is real; copied source scenarios not established — quality_risk

No exact normalized full-input duplicate, no repeated state/question warning, no cross-family trigram pair >= .65; maximum cross-family state similarity .035714. Manual scenario comparison found intent train dog boarding g09 versus sentiment validation boarding g26, and intent train astronomy g17 versus sentiment validation observatory g27. Events differ (extend booking or borrow telescope versus lost blanket or queue criticism); no shared named source/entity/event is established. Seed desk, bike workshop and pottery also recur across families. Current group isolation is source-group isolation, not topic-disjoint isolation. Do not claim cross-family domain-disjoint validation or semantic deduplication completeness.

### F3. Sentiment revision fixes published template/candidate shortcuts; explicit cues remain — quality_risk

All 120 revisions preserve original state, split, group, subject and teacher target class; source-to-revision map covers 120 unique published IDs. Each revised row has exactly all four semantic classes and the neutral subject-specific question. Parent hashes match. Original sentiment shards are excluded from manifest and reviewed only as parent lineage, not as published data. Revised states still often say delighted, disappointed, mixed, or explicitly state both views; neutral examples are strongly factual. Clean synthetic English and limited candidate paraphrases remain easy lexical shortcuts. Provenance source strings intentionally change to revision lineage, while original teacher identity and label basis remain; full provenance-object equality is therefore false, not a class-preservation failure.

### F4. Validation is small and mechanism-held-out, not coverage-complete — scope_limit

72 isolated groups: 60 train and 12 validation. Rule groups 1–10 train; 11–12 validation (reachability and pairwise voting). Therefore rule validation does not measure held-out examples of all trained mechanisms. Forty-eight selected rows agree with published targets, but only two per mechanism; shortest/longest heuristic selected two rejects in score group and two empty results in symmetric-difference group. Boundary examples include zero hours, exact capacity, wraparound, overlap endpoints, zero remainder and pairwise ties; no comprehensive boundary coverage claim.

### F5. Assembler hardcodes teacher identity and zero accounting — code_risk

Read-only source inspection: assemble.py sets teacher_alias=openai/gpt-sol and additional/pending spend to zero instead of deriving/checking producer metadata. This can materially misattribute later producers and hide later paid generation. Current manifest metadata/provenance identify those aliases and zero spend, so no demonstrated current dataset mismatch. Recommend deriving/validating those fields before using assembler with other producers. No tests or runtime assembly executed.

### F6. Assembler storage guard is incomplete for assignment subpaths — code_risk

assemble.py protects artifact_prefix through shard_path(), but directly joins assignment artifact_directory and published_directory afterward. Absolute or traversal subpaths can bypass prefix containment and evaluation/final guards before producer files are opened. Current published files are inside the allowed pilot directory and were independently checked; no exploit or forbidden read attempted. Enforce the same containment/excluded-storage guard on every resolved source/published path before accepting less-trusted configs. validate.py itself checks manifest shard paths before reads; no material bug found for the current valid dataset.

### F7. Label-hidden teacher review is not independent correctness evidence — scope_limit

Label-free selected_inputs.jsonl was written first and 48 rationales frozen in precomparison_decisions.json before target comparison. Sentiment g01:r01 class P had already appeared in the revision-map excerpt, so row 13 is ordinary teacher review, not blind. Other 47 selected target labels had not been displayed when assessed; audit semantics were already read. Same exposed model alias as original teacher, different session; immutable revisions unknown. All 120 rule targets reproduced using the published expected() helper (the script has no expected_result symbol), not an independently authored solver or independently parsed text. Text spot-check helps fidelity assessment but proves neither generator nor facts correct.

## Per-row decisions

Indices are zero-based. All rows: target agreement, high teacher confidence, one preferred option under stated scope. Row 13 is prior-label-exposed; others were label-hidden. Full fields are in `review.json`.

| # | Row ID | Choice | Rationale |
|---|---|---:|---|
| 1 | `data:pilot-v1:intent:g01:r01` | 0 | Keeping the same loan longer requests renewal, not reservation or a fine payment. |
| 2 | `data:pilot-v1:intent:g06:r02` | 2 | Repair already happened; the question asks collection readiness rather than initial repair or price. |
| 3 | `data:pilot-v1:intent:g11:r03` | 0 | User reports third-party dumped tyres, explicitly denying ownership; removal reporting fits. |
| 4 | `data:pilot-v1:intent:g15:r04` | 1 | The request is for meeting date and joining details, not casting a vote. |
| 5 | `data:pilot-v1:intent:g20:r01` | 2 | Offering time and asking to sign up is volunteer registration, not paid employment or donation. |
| 6 | `data:pilot-v1:intent:g25:r02` | 0 | Compare larger data allowances while retaining number; cancellation and number change contradict request. |
| 7 | `data:pilot-v1:intent:g26:r01` | 0 | A novice explicitly requests the beginner session; no purchase, cancellation or swarm report. |
| 8 | `data:pilot-v1:intent:g27:r02` | 2 | A prebooking question asks whether dogs are allowed aboard, explicitly not kennelling. |
| 9 | `data:pilot-v1:intent:g28:r03` | 2 | Unopened mistaken pea packet should be exchanged for broad beans, not diagnosed as a failed crop. |
| 10 | `data:pilot-v1:intent:g28:r04` | 1 | Remove only the dated shift; cancel-all and membership-ending options violate the limited scope. |
| 11 | `data:pilot-v1:intent:g29:r01` | 0 | The explicit request is the required induction, not unrestricted access or equipment purchase. |
| 12 | `data:pilot-v1:intent:g30:r02` | 1 | Needs step-free accommodation information before choosing lodging, not a medical appointment. |
| 13 | `data:pilot-v1:sentiment-r2:g01:r01` | 1 | Creamy, enjoyed every sip, would reorder: positive only. Parent-map P class previously exposed; not blind. |
| 14 | `data:pilot-v1:sentiment-r2:g06:r02` | 0 | Machine number, duration and card payment are factual; no expressed evaluative stance. |
| 15 | `data:pilot-v1:sentiment-r2:g11:r03` | 1 | Delighted with noise cancellation and no discomfort is praise of the asked subject; no stated criticism. |
| 16 | `data:pilot-v1:sentiment-r2:g15:r04` | 3 | Seat is broken and uncomfortable; excellent film refers to a different subject and must not turn seat sentiment mixed. |
| 17 | `data:pilot-v1:sentiment-r2:g20:r01` | 3 | Asked about overall family swim: enjoyable activities and uncomfortable crowding explicitly coexist. |
| 18 | `data:pilot-v1:sentiment-r2:g25:r02` | 3 | Untraceable lost bowl and very disappointed collection system express only dissatisfaction. |
| 19 | `data:pilot-v1:sentiment-r2:g26:r01` | 0 | Lost blanket, no attempt to find it and upset handling: negative only for belongings handling. |
| 20 | `data:pilot-v1:sentiment-r2:g27:r02` | 1 | Overall talk experience includes praised content and criticised room temperature; both must count. |
| 21 | `data:pilot-v1:sentiment-r2:g28:r03` | 2 | Early closure and explicit unhappiness are criticism of desk reliability with no praise. |
| 22 | `data:pilot-v1:sentiment-r2:g28:r04` | 2 | Storage duration and ticket details express no evaluation. |
| 23 | `data:pilot-v1:sentiment-r2:g29:r01` | 2 | Clear hearing-aid audio, no buzz and delighted clarity: favorable only. |
| 24 | `data:pilot-v1:sentiment-r2:g30:r02` | 3 | Packet quantities and venue describe the exchange without approval or criticism. |
| 25 | `data:pilot-v1:rule_application:g01:r01` | 0 | All flags on; first listed safety rule wins regardless of later warranty/urgent matches. |
| 26 | `data:pilot-v1:rule_application:g01:r09` | 0 | Every flag off triggers no rule, so default General bench. |
| 27 | `data:pilot-v1:rule_application:g02:r01` | 0 | Zero used hours, explicitly no minimum, so zero credits. |
| 28 | `data:pilot-v1:rule_application:g02:r10` | 2 | Marginal charge: 2*3 + 1*7 + 2*11 = 35, not a single-rate charge. |
| 29 | `data:pilot-v1:rule_application:g03:r02` | 0 | Skip overweight Dune 9; Elm 3 plus Flint 5 exactly fits capacity 8. |
| 30 | `data:pilot-v1:rule_application:g03:r07` | 1 | Accept Sage 6; skip Tide 5; accept Umber 4; no capacity for Vale 1. |
| 31 | `data:pilot-v1:rule_application:g04:r10` | 1 | Five forward steps in a three-person cycle equals two: Vega to Xenia. |
| 32 | `data:pilot-v1:rule_application:g04:r09` | 2 | Ten backward steps in five slots makes two complete wraps, leaving Topaz. |
| 33 | `data:pilot-v1:rule_application:g05:r01` | 2 | Score -1 is below reject threshold 3. |
| 34 | `data:pilot-v1:rule_application:g05:r07` | 2 | Score 2*1 + 5*0 - 4*2 = -6, below -2, so reject. |
| 35 | `data:pilot-v1:rule_application:g06:r03` | 1 | Fern appears on both sets, hence symmetric difference empty. |
| 36 | `data:pilot-v1:rule_application:g06:r09` | 0 | Lists contain the same set in reverse order, so no badges survive. |
| 37 | `data:pilot-v1:rule_application:g07:r01` | 1 | Proposal touches both existing endpoints only; positive overlap is explicitly required. |
| 38 | `data:pilot-v1:rule_application:g07:r10` | 2 | 07–10 overlaps 08–09 and 09–10, but only touches 06–07 and 10–11. |
| 39 | `data:pilot-v1:rule_application:g08:r07` | 1 | Single-character message v matches only prefix v, routed to Vale. |
| 40 | `data:pilot-v1:rule_application:g08:r06` | 0 | pinwheel matches p, pi and pin; longest pin routes to Rock. |
| 41 | `data:pilot-v1:rule_application:g09:r05` | 1 | Weighted sum 5*3+5*1=20; remainder mod 5 is zero, not its complement. |
| 42 | `data:pilot-v1:rule_application:g09:r08` | 0 | Weighted sum 1*2+9*1+0*2+2*1=13; remainder mod 4 is one. |
| 43 | `data:pilot-v1:rule_application:g10:r01` | 1 | Badge takes locked directly to open. |
| 44 | `data:pilot-v1:rule_application:g10:r10` | 1 | Occupied ignores close; exit opens; badge is ignored in open; enter returns to occupied. |
| 45 | `data:pilot-v1:rule_application:g11:r01` | 0 | From A follow A to B to C; D is disconnected. |
| 46 | `data:pilot-v1:rule_application:g11:r07` | 1 | From C1 reach B1 and D1 then E1; A1 cannot be reached by reversing its arrow. |
| 47 | `data:pilot-v1:rule_application:g12:r01` | 0 | Ari beats Bea and Cy by 3 votes to 2 in both comparisons. |
| 48 | `data:pilot-v1:rule_application:g12:r10` | 1 | Cyclic equal ballot blocks provide no candidate beating every rival strictly; opposite pairs tie, so elect nobody. |

## Exact shell commands executed

No other shell commands were executed. File contents were also read using the read tool (listed in review.json); script contents and all new supporting outputs are retained here.

```bash
printf 'PI_MODEL=%s\nPI_PROVIDER=%s\n' "$PI_MODEL" "$PI_PROVIDER"; find /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1 -maxdepth 3 -type f | sort
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/review/prepare_review.py
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/review/validate_review.py
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/review/supplement.py
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/review/finalize_review.py
```

## Handoff

No observed label disagreement requires resolution. Accept only with the documented scope: teacher agreement and programmatic consistency, not verified ground truth or topic-disjoint generalization. Code risks F5/F6 merit follow-up before broader producer/config reuse; no current pilot failure demonstrated.
