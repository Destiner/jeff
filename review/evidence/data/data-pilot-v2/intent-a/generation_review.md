# intent-a r1 generation review

## Delivery

- 200 new train rows across the 20 assigned train domains; 40 new validation rows across the four assigned validation domains. Exactly ten singleton scenarios per domain, 240 groups total. Parent rows are not included.
- `group_assignments.json` was written before any case text, using the frozen namespace and ranges. No group changed split or domain.
- `source_cases.txt` holds 240 directly authored cases and teacher targets, not a Cartesian request-template expansion. `generate.py` only serializes, shuffles choices and validates. Its seed is 741903. Source-format targets are first; exported targets are shuffled and their option IDs are opaque.
- `authoring_record.json` captures the actual authoring-session `PI_PROVIDER=openai` and `PI_MODEL=gpt-sol`; regeneration preserves this identity rather than attributing old text to a future session. Immutable revision and sampling settings were unavailable.

## Semantic review (same teacher, not independent verification)

The requests cover booking, amendments, recovery, reporting, disputes, information-only enquiries, conditional pauses, limited cancellations and access assistance. Each target addresses the primary request. Specific boundaries checked include correcting a fault description without cancelling a visit (g032), requesting a refund only for an unused ferry ticket (g044), cancelling a single desk rather than a team booking (g073), withdrawing procedure consent while keeping a consultation (g098), declining mobile access while retaining bank accounts (g130), withdrawing sale consent but retaining appraisal (g216), and appealing a score rather than replacing a certificate (g229).

Information-only requests leave bookings unchanged when explicitly requested; contrastive negatives do not override an affirmative requested action. Urgent veterinary and equipment-safety requests are intent labels, not medical or engineering advice. Weather and climbing cases request information without claiming forecasts, anchors or routes are safe.

All cases were authored individually. Generic acts such as login recovery, rescheduling and invoice correction deliberately recur across domains; these are not held-out intent categories. The ten cases in a domain concern different customer situations rather than paraphrases of a single event. Scenario independence is a teacher authoring judgment, not independently established evidence.

## Local checks and shortcut audit

The stdlib CPU generator validates the saved JSONL: contract shape, required values, target membership, counts, ID uniqueness, exact canonical state/input duplicates, singleton groups, group isolation, frozen domain allocation and ten scenarios per domain. No exact duplicates or cross-split group overlap were found. All 240 states contain 21–32 words; options contain 2–8 words. This is **not** a tokenizer measurement.

Choice counts are mostly three/four (80% in each split), with five/six also represented. Target schedules are independently randomized and balanced within each split/choice-count stratum, differing by at most one per position. Which positions receive remainder rows is randomized too. Rival order uses separate per-row random streams.

Correct candidates are not always longest: unique-longest targets occur in 70/200 train and 11/40 validation rows; including ties gives 142/200 and 29/40. Mean target length is 4.667 words versus 4.091 for rivals. This residual length asymmetry is disclosed, not evidence that option-only shortcuts are absent. Correct and rival options use the same action-label style; no target markers or metadata appear in model-facing text.

A content-word Jaccard scan compared all 8,000 new train/validation state pairs. None reached 0.5; the highest was 0.3182 (g100/g217). The twelve reported top pairs were reviewed: they share generic account access, subscription pause/retrieval, invoice, amendment or complaint acts, but concern separate assigned domains and events. g013/g229 deliberately distinguish certificate-name correction from grade appeal. No pair is a reused source event or cosmetic paraphrase. This lightweight scan is not a semantic leakage guarantee.

## Boundaries and remaining parent gates

Only the producer's private artifact directory was written. No Git commands, repository edits, network/API calls, paid work, ML loads, tests or linting were performed. Historical tiny/v1 content and all evaluation data were not read. Reserved domains were taken only from the config; training domains were checked against all listed validation-domain reservations. No `passage_entailment` rows were produced.

Parent assembly must still check cross-producer/historical duplicates, run the CPU 256-token pair audit and arrange the required separate-session teacher review. Local structural validation and this same-session review do not establish independent label correctness. Original synthetic content is subject to existing provider terms; no independent redistribution licence is claimed. Additional and pending spend are both £0.

## Reproduction

Run `python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/intent-a/generate.py` with the captured source, assignments and authoring record intact. It uses stdlib Python only and reads only this directory plus the declared config and contract paths. Revision/hash records are in `metadata.json` and `validation_report.json`. Outputs are frozen at handoff; any later correction should receive a new artifact revision rather than modifying the delivered files.
