# D4 predeclared TRAIN audit — bounded findings for learning decisions

Proactive audit finished; the one-hour observation window remains open until15:48:12UTC. Frozen v2 and D3 are unchanged. No training/inference or new data authoring is authorized by this finding.

## What was actually checked

Predeclared selection (`selection.json`, SHA256 `b599a661fabb38a5703d8393c6dc9f9ac96e4901aa16fff1bdd9a08fb614d99d`):24 existing TRAIN decisions from v2, spanning14 source/mechanism groups. Four inherited controls plus20 new decisions in10 paired p04 policies. Zero overlap with the16 D3-novelty training examples previously reviewed. IDs were fixed before semantic review; choice order shuffled with a fixed seed, without using labels or model outcomes.

Fresh reviewer received only state/question/options and opaque IDs. Frozen judgment hash `792ed9d238e7f2a00c74397b6fbf7df3d642dda59454a4ea7678c97dfcc65303`; parent subsequently compared saved labels: **24/24 agreement**,0 unresolved/multiple-defensible judgments. Separate factual auditor found24/24 exact pinned TRAIN-row matches,24/24 rendered-rule derivations matching labels and24/24 same-author executable recomputations. Four inherited controls lack explicit policy-instance IDs; do not invent them. There are14 source groups, not24 independent sources.

Both reviewers expose `openai/gpt-sol`, as do the relevant source authors. This is fresh-session consistency, not independent human/model-family ground truth. The purposive rules-only sample cannot establish that all1500training rows are correct.

## Concrete supervision weaknesses, not label defects

- Archive authorization p04 (`rule-a:g001:r07/r08`): “too many eligible signers” is impossible because only two identities are eligible, duplicates ignored and required count is two. 2/2decisions in1sharedpolicy/sourcegroup.
- Pump rate p04 (`rule-b:g005:r07/r08`): `Tie` is an unreachable returned result because the stated equality rule returns VendorA. 2/2decisions in1sharedpolicy/sourcegroup. This is NOT an ambiguous equality label.
- Appointment p04 (`rule-b:g008:r07/r08`): cooldown is zero in2/2cases; one offers only feasible starts, the other only overlapping starts. This pair supplies no positive-cooldown arithmetic supervision.
- Coordinate p04 (`rule-b:g006:r07/r08`): zero intermediate point makes reflection inert inonecase; in the other the correct option alone has negative x, allowing sign-based elimination without fullcoordinate arithmetic.
- Other local signatures: selected discount targets are smallest numeric option2/2; rounding targets are third of four2/2; packing targets third of four2/2. Each is justonepairedpolicy, not a whole-training shortcut estimate. First-option agreement8/24; no universal options-only solver was demonstrated.

The source labels still unambiguously implement their stated tasks. Easy/boundary examples are legitimate; these findings limit what correct selections demonstrate about full-rule learning. They do not prove that any trained model exploits these cues or explain the measured regressions causally.

## Recommendation / boundaries

**No actionable target/specification correction or frozen-data erratum demonstrated in this sample.** Do not block a separately authorized learning experiment on speculative relabeling. Do not alter D3 targets based on model disagreement.

If a future training-data improvement is explicitly assigned, the concrete opportunity is stronger within-TRAIN policy/branch contrast and plausible reachable distractors—not another broad quota, blanket relabeling or diagnostic-derived training cases. Preserve historical releases and training/held-out exclusions; any correction is a separate versioned proposal. No new Data code fix, generation or consumer change is requested now.

Detailed evidence in `blind-review/`, `target-comparison.json`, and `fact-audit/`. E4's aggregate-only notice was received; no private Evaluation artifacts or held-out examples were opened. Consumer handoff inspection found no unresolved Data-owned identity/schema/split/token issue; downstream coverage/scoring claims remain attributed to their owners.
