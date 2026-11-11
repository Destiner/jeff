# D4 factual audit — selected TRAIN rows

Reviewer alias: `openai/gpt-sol` (environment only).

## Result

24/24 exact existing-row matches against pinned TRAIN shards; 0/16 historical novelty-ID overlap. Fresh rendered reasoning: 24/24 target matches. Same-author executable consistency: 24/24 matches. Source rendering joins: 20/20 new rows; inherited facts manually reviewed 4/4. No genuine target/spec bug found; no frozen-row edits or correction proposed.

## Independence and scope

Purposive rules-only TRAIN sample; dependent paired policies and same-model provenance. No accuracy estimates or extrapolation to whole training; no tokenizer/model audit. Hashing full files is identity verification, not semantic expansion.

AST-extracted reviewed pure expected functions, plus pure rule-b rendering correspondence. Source algorithms share authorship with labels, so their agreement alone is not independent verification.

20 new decisions are 10 actual p04 policies, not 20 policies; the four inherited rows have no explicit scenario IDs. 14 mechanism/source groups total. Reviewer is the same exposed model alias as the source author; fresh-session reasoning is not independent-model verification.

## Exact findings

- No genuine target/specification bug found in selected 24; all fresh rendered calculations and same-author helper computations match saved targets. No erratum or relabeling proposed.
- All 10 new r07/r08 pairs share actual p04 scenario_id: 20 decisions, 10 policy instances, 10 mechanism/source groups. Four inherited controls add 4 source groups; no explicit scenario_id is stored for them. Total 14 source groups, not 24 independent policies. Treat inherited rows as four rendered control-policy instances only, not newly inferred provenance IDs.
- Fresh reasoning is a separate review session, but reviewer alias equals disclosed source teacher alias openai/gpt-sol. Not independent-model or independent-provider verification; immutable revision unavailable.
- Selected rule-a:g002 winners are G in 2/2 and second candidate in state in 2/2. No winner strictly Pareto-dominates all rivals in either case (0/2); G dominates F in r08 only. Thus a universal dominance shortcut is not demonstrated, while a shared-policy candidate-name fingerprint is possible.
- Selected rule-a:g005 targets are numeric minimum 2/2; rule-a:g007 targets ascending rank 3 of 4 (second largest) 2/2; rule-b:g002 targets ascending rank 3 of 4 in 2/2. Each denominator is one shared policy pair; these are local construction signatures, not measured whole-training shortcuts.
- All 24 option ID/text sets unique; manual review found distinct terminal returned outcomes. Vendor Tie options in two rate rows are unreachable under this p04 tie-return-A policy (2/2), but not a competing correct answer: question asks returned result, not whether raw rates are equal. Authorization too-many option is unreachable when only two eligible signers and required=2 (2/2). Unreachable distractors are local weakness, not label errors.
- Mechanism coverage is not branch coverage. The chosen scheduling p04 has zero cooldown in 2/2 cases; neither measures positive cooldown arithmetic. Rounding pair covers positive tie/non-tie only (2/2), not negative tie behavior. No extra cases were generated or sampled.

## Construction diagnostics

All counts below refer only to these 24. First means first displayed option; length uses Unicode character count; tied extrema are separate from unique extrema. Numeric rank uses ascending scalar values only, with identical units inside each row. Tuples, labels, and mixed No-slot/numeric choices are excluded from the numeric denominator. No fitted classifier or whole-training extrapolation.

```json
{
  "n": 24,
  "policies_explicit": 10,
  "slots": {
    "3": 6,
    "1": 8,
    "4": 3,
    "2": 7
  },
  "by_choice_count": {
    "3": {
      "1": 5,
      "2": 2,
      "3": 3
    },
    "4": {
      "3": 3,
      "4": 3,
      "2": 5,
      "1": 3
    }
  },
  "target_first": 8,
  "target_unique_longest": 2,
  "target_tied_longest": 14,
  "target_unique_shortest": 3,
  "target_tied_shortest": 15,
  "numeric_comparable_n": 6,
  "numeric_ranks": {
    "1": 2,
    "3": 4
  }
}
```

| Group | n | Target slots (1-based) | First | Unique longest / tied longest | Unique shortest / tied shortest | Numeric ranks (n comparable) |
|---|---:|---|---:|---|---|---|
| data:pilot-v1:rule_application:g01 | 1 | {3: 1} | 0/1 | 0 / 0 | 1 / 0 | {} (n=0) |
| data:pilot-v1:rule_application:g04 | 1 | {1: 1} | 1/1 | 0 / 0 | 0 / 1 | {} (n=0) |
| data:pilot-v1:rule_application:g07 | 1 | {4: 1} | 0/1 | 0 / 0 | 1 / 0 | {} (n=0) |
| data:pilot-v1:rule_application:g10 | 1 | {2: 1} | 0/1 | 1 / 0 | 0 / 0 | {} (n=0) |
| data:pilot-v2:rule-a:g001 | 2 | {3: 1, 2: 1} | 0/2 | 0 / 0 | 1 / 0 | {} (n=0) |
| data:pilot-v2:rule-a:g002 | 2 | {1: 2} | 2/2 | 0 / 2 | 0 / 2 | {} (n=0) |
| data:pilot-v2:rule-a:g003 | 2 | {3: 1, 2: 1} | 0/2 | 0 / 2 | 0 / 2 | {} (n=0) |
| data:pilot-v2:rule-a:g005 | 2 | {2: 2} | 0/2 | 0 / 1 | 0 / 2 | {1: 2} (n=2) |
| data:pilot-v2:rule-a:g007 | 2 | {1: 1, 4: 1} | 1/2 | 0 / 2 | 0 / 2 | {3: 2} (n=2) |
| data:pilot-v2:rule-b:g002 | 2 | {2: 2} | 0/2 | 0 / 2 | 0 / 2 | {3: 2} (n=2) |
| data:pilot-v2:rule-b:g005 | 2 | {1: 2} | 2/2 | 0 / 2 | 0 / 0 | {} (n=0) |
| data:pilot-v2:rule-b:g006 | 2 | {4: 1, 1: 1} | 1/2 | 0 / 1 | 0 / 1 | {} (n=0) |
| data:pilot-v2:rule-b:g008 | 2 | {3: 1, 1: 1} | 1/2 | 1 / 0 | 0 / 1 | {} (n=0) |
| data:pilot-v2:rule-b:g010 | 2 | {3: 2} | 0/2 | 0 / 2 | 0 / 2 | {} (n=0) |

Repeated unordered choice sets are enumerated with exact IDs and SHA-256 in report.json; shared option vocabularies alone do not show the choices-only heuristic predicts a target.

## Per-row fresh derivations

| Existing ID | Derived answer | Rendered-rule derivation |
|---|---|---|
| `data:pilot-v1:rule_application:g01:r07` | Route to Rapid bench. | Safety off; warranty off; urgent on. First matching rule is Rapid bench. |
| `data:pilot-v1:rule_application:g04:r07` | Duty belongs to Juno. | Kestrel index 1; (1 - 4) mod 3 = 0, Juno. Backward sequence Juno, Lark, Kestrel, Juno. |
| `data:pilot-v1:rule_application:g07:r07` | Conflicts: none. | Proposal [6,8); bookings [8,10), [10,12), [12,14). Every intersection has nonpositive length; endpoint 8 is not overlap. |
| `data:pilot-v1:rule_application:g10:r07` | Final state: occupied. | occupied -> open -> occupied; exit opens, enter occupies. |
| `data:pilot-v2:rule-a:g001:r07` | Authorize | 2 distinct eligible signers versus exactly 2; duplicate legal signature and intern do not add eligible distinct signers. |
| `data:pilot-v2:rule-a:g001:r08` | Reject: too few eligible signers | 1 distinct eligible signers versus exactly 2; duplicate legal signature and intern do not add eligible distinct signers. |
| `data:pilot-v2:rule-a:g002:r07` | Select candidate G | F and G tie on aisle distance 2; G battery 60 > 40, so machine IDs never enter. |
| `data:pilot-v2:rule-a:g002:r08` | Select candidate G | F and G tie on distance 1 and battery 55; G machine ID 4 < 8. H loses on distance despite higher battery. |
| `data:pilot-v2:rule-a:g003:r07` | 0, 5, 0; unfilled 0 | P quarantined: take 0. M has 7, N has 2; demand 5 gives issued [0, 5, 0], residual 0. |
| `data:pilot-v2:rule-a:g003:r08` | 0, 7, 2; unfilled 3 | P quarantined: take 0. M has 7, N has 2; demand 12 gives issued [0, 7, 2], residual 3. |
| `data:pilot-v2:rule-a:g005:r07` | £0 | 12 × (1 - 50/100) - 8, floored at zero = 0. Percent first, not fixed first. |
| `data:pilot-v2:rule-a:g005:r08` | £4 | 24 × (1 - 50/100) - 8, floored at zero = 4. Percent first, not fixed first. |
| `data:pilot-v2:rule-a:g007:r07` | 150 millimetres | Adjacent multiples 140, 150; distances 5, 5. Choose nearest, larger on equality: 150. |
| `data:pilot-v2:rule-a:g007:r08` | 140 millimetres | Adjacent multiples 140, 150; distances 4, 6. Choose nearest, larger on equality: 140. |
| `data:pilot-v2:rule-b:g002:r07` | 3 | Net need 5; usable/pack 5; ceil=1; max(minimum 3, ceil 1)=3. |
| `data:pilot-v2:rule-b:g002:r08` | 4 | Net need 16; usable/pack 5; ceil=4; max(minimum 3, ceil 4)=4. |
| `data:pilot-v2:rule-b:g005:r07` | Vendor A | A=20/4, B=30/6; cross-product difference 0. Equal rates; explicit tie returns Vendor A, not the Tie distractor. |
| `data:pilot-v2:rule-b:g005:r08` | Vendor B | A=19/4, B=30/6; cross-product difference -6. B has the higher rate. |
| `data:pilot-v2:rule-b:g006:r07` | (0, 0) | (2,-3) + (-2,3) = (0,0); reflect x sign only -> (0, 0). |
| `data:pilot-v2:rule-b:g006:r08` | (-1, 4) | (3,1) + (-2,3) = (1,4); reflect x sign only -> (-1, 4). |
| `data:pilot-v2:rule-b:g008:r07` | 45 | Existing [15,45); duration 15, gap 0. Listed [45, 46, 60]; legal listed starts [45, 46, 60]. Touching 45 is legal; starts below 45 here overlap. |
| `data:pilot-v2:rule-b:g008:r08` | No slot | Existing [15,45); duration 15, gap 0. Listed [30, 40, 44]; legal listed starts []. Touching 45 is legal; starts below 45 here overlap. |
| `data:pilot-v2:rule-b:g010:r07` | Mist | moisture=4: <4 is False; else heat=8 >=8 is True; select Mist. |
| `data:pilot-v2:rule-b:g010:r08` | Soak | moisture=3: <4 is True; select Soak without evaluating the else branch. |

## Reproduction and hashes

Run `python3 /Users/destiner/Code/jeff/artifacts/data/d4-20261111T144812Z/fact-audit/audit_selected.py` only with absent report outputs (exclusive creation prevents overwrites). Reads only declared TRAIN shards and permitted helper/source/metadata files; extracts pure functions, never invokes their mains. Uses standard-library CPU only. It is an actual-data audit, not a software test or generated fixture.

Exact per-row input hashes, source correspondence, semantic distinctions, choice fingerprints and denominators are in report.json. Full source hashes and script hash are in sourcehashes.json. Files are hashed in full solely for identity; semantic inspection remains selected-only. No blind-review output, validation.jsonl, Evaluation, held-out, probe or final rows were opened. No Git/mailbox/network/models/dependencies/tests/lint/spend.
