# Generation review — sentiment-a r1

## Deliverable
- **200 train + 40 validation**, all new: 240 singleton groups / 240 separately authored experiences.
- Exactly 20 assigned train domains and 4 assigned validation domains, 10 scenarios each.
- Frozen assignments were written before any cases and retained without split changes.
- Teacher: **openai / gpt-sol**, observed from PI_PROVIDER / PI_MODEL. Revision and sampling unavailable.
- Existing approved text generation only; additional and pending spend **£0**.

## Authoring and review
Each domain covers different uses or incidents rather than four sentiment rewrites of one event. Cases include indirect approval, ordinary complaints, factual records, rejected expectations, negation, and comparisons to other items. Questions retain the exact subject; all four mutually exclusive attitudes appear every time. Approval plus a real fault is labelled as both, not by whichever clause is stronger. Neutral cases do not evaluate the named item.

The same teacher reviewed all source cases. A bag case's incidental capacity commendation was removed so its criticism-only target is not ambiguous. The small-cup kettle scenario uses a lid-condensation complaint rather than repeating the separate minimum-fill scenario. This is **not independent label verification**. Subject comparisons concern other items or expectations, not hidden evidence that the current subject has both attitudes.

## Structural evidence
`python3 generate.py` reads only this private directory and the assignment config, uses Python's standard library, and regenerates the deliverables deterministically with seed 271828. Source cases, generator and assignment SHA-256 values are in `metadata.json` and `validation_report.json`.

Train classes are 50 each; validation classes are 10 each. Target slots total 50 each in train and 10 each in validation. Within each class the slots differ by at most one (12/13 train, 2/3 validation). Five question styles and five complete option styles have equal frequencies within every class/split; distractor order is independently shuffled. Full class/slot/style and target-length statistics are in the report. Across the five candidate styles, each category is uniquely longest in one style, and all categories tie in the fifth. Thus the target is uniquely longest on exactly 20% of rows in every class/split, not a class-dependent cue.

All contract, target membership, ID uniqueness, exact/normalized state duplicate, canonical-input duplicate, frozen-domain/group and split-isolation checks passed. Local cross-split content-word Jaccard screening found **0 pairs at threshold 0.45** (maximum 0.1724); this screen is not a semantic guarantee. State lengths are 23–37 whitespace words; longest state/question/single-option combination is 59 words. No tokenizer was used.

## Handoff boundaries
No historical examples, other producer content, evaluation data, Git, manifests, or model code were read or changed. Shared contracts and checkout instructions were read only; nothing in a checkout was edited. Reserved domains were respected using config boundaries. The parent still needs its tokenizer audit, full-dataset duplicate/boundary checks and separate-session teacher spot review. These outputs claim structural validation and teacher self-review only. Original synthetic text remains subject to existing provider terms; no independent redistribution licence is asserted.

Files: `group_assignments.json`, `source_cases.txt`, `generate.py`, `train.jsonl`, `validation.jsonl`, `metadata.json`, `validation_report.json`, and this review. Finished outputs are frozen at handoff.
