# Jeff v2 — sentiment review

**Disposition: one wording must-fix before semantic sign-off.** No target mismatch among 40 frozen blind judgments. This is agreement with producer labels, **not independent ground-truth accuracy**.

## Scope and independence

Reviewed **sentiment-a and sentiment-b: 480 new rows**, not the historical sentiment rows included in the 1,800-row manifest. Actual environment: `PI_PROVIDER=openai`, `PI_MODEL=gpt-sol`; immutable revision unavailable. Both producers expose this same provider/alias. Separate-session target hiding reduces anchoring but does not create an independent teacher.

Prior exposure before freezing: user instructions/audit assertions, `AGENTS.md`, `docs/contracts.md`, manifest paths/counts/hashes only. The selection script handled labels mechanically and stored them separately in `sealed-targets.json`; it displayed only state/question/options plus row IDs. I did not read labels, source annotations, metadata or generators before writing `frozen-judgments.json`. Targets were first inspected after that freeze. Subsequent full-source scanning was label-visible and is explicitly weaker evidence.

## Executed checks versus existing claims

**Executed here:** deterministic 40-row blind sample; post-freeze reading of all 480 source experiences; actual-row/source-label alignment; complete four-class option coverage; class, question-style, option-style, target-position and domain counts; exact/whitespace-only state uniqueness; scoped SHA-256 before/after comparison. `audit.py` interprets static generator constants using AST; it does not import or execute producer generators. Detailed counts are in `post-freeze-audit.json` and `review.json`.

**Not rerun:** user-reported full structural checks, tokenizer audit, and canonicalizer correction. No model loads, network/API calls, tests/lint, Git, checkout edits, historical examples, evaluation data, or final content. Additional paid spend: £0. No confidence or calibration estimate.

## Sampling and coverage

For each producer/split, selected zero-based indices `round(i*(n-1)/9)`, i=0…9, without inspecting labels. Train indices: 0,22,44,66,88,111,133,155,177,199. Validation: 0,4,9,13,17,22,26,30,35,39. Ten train and ten validation rows per producer; 40 total. Each producer's sample covers 10 train domains and all 4 validation domains, and all four target classes in each split after unsealing. This is systematic coverage, not a random representative accuracy sample.

| Producer/split | Positive | Negative | Neutral | Mixed |
|---|---:|---:|---:|---:|
| sentiment-a/train | 3 | 2 | 2 | 3 |
| sentiment-a/validation | 2 | 3 | 3 | 2 |
| sentiment-b/train | 2 | 2 | 1 | 5 |
| sentiment-b/validation | 3 | 2 | 2 | 3 |

## Full 480-row balance and semantic scan

- **480/480** have exactly one of each semantic option: approval only, criticism only, no evaluation, both approval and criticism. All ten option-style dictionaries were read semantically, not inferred solely from opaque IDs.
- Per producer: train **50/class**, validation **10/class**. Target-position totals: **50/slot** train, **10/slot** validation.
- Within every producer/split/class: target positions differ by at most one (12–13 train; 2–3 validation). Each of five question forms and each of five option styles occurs **10 times/class** train and **2 times/class** validation. Thus these marginal styles do not disclose targets. This does not establish absence of every possible joint or lexical shortcut.
- Actual targets match source annotations for **480/480**; this is serialization consistency, not an external truth check. Questions exactly instantiate a subject-preserving form. All are label-neutral; words such as “evaluate” also appear with neutral accounts.
- **480 exact distinct states**, also distinct under whitespace-only normalization preserving case, signs and punctuation. No trigram collision was treated as a label conflict.
- I read **48 domain blocks, 10 separately described experiences each**. They use different attributes, incidents or purposes rather than repeated four-polarity versions of one event. **480 described events; zero identified four-polarity rewrite sets.** This is a qualitative scenario count, not 480 statistically independent observations. Common synthetic scaffolds and same-teacher dependence remain.

Semantic focus: factual storage/inventory is neutral, not mixed; genuine benefit plus defect is mixed even when the closing judgment is strongly negative. Avoided fears and defects of other products are not criticism of the question subject. Negated defects can convey praise; reporting a safety-negation omission can imply criticism without an explicit adjective. The kayak bag's “top closure is not the problem” narrows its leak diagnosis rather than adding affirmative praise. Willow Park's shaded bench provides mild implied approval alongside its faulty support; see recorded ambiguity.

## Must-fix finding F1 — wording, not established wrong class

**`data:pilot-v2:sentiment-b:g011:r01`**, found in the post-freeze source scan (not in the blind sample), source class **positive**:

> Quill Parcel sandwiched my tracing sheets between rigid boards. Not a crease survived the journey, so I could use every sheet for the drawing.

“Not a crease survived” says existing creases disappeared; it does not say the sheets arrived without new creasing. This is a negation/verb reversal in the evidence, despite a plausible intended positive target. Rigid packing does not explain crease removal. **Re-author to describe uncreased arrival unambiguously in a new producer revision.** Do not automatically flip the target. No blinded chosen option exists for this unsampled row; positive remains plausible on a literal crease-removal reading. I found no further confirmed incorrect class or forced ambiguous positive/negative target in the annotated scan; that is not a guarantee of corpus-wide correctness.

## Frozen row decisions

Positions are one-based. Every comparison below agrees with the producer target after unsealing. All 40 have no individual label must-fix. Opaque chosen option IDs, complete option texts, comparison targets and explicit ambiguity fields are retained in `review.json`.

| Row ID | Choice | Reason | Ambiguity | Comparison |
|---|---|---|---|---|
| data:pilot-v2:sentiment-a:g001:r01 | 1 — positive | Quiet shutoff and one-handed pouring benefit the parent; no kettle fault. | none material | agrees |
| data:pilot-v2:sentiment-a:g023:r01 | 4 — neutral | Inventory and contents order only; no judgment of the puzzle book. | none material | agrees |
| data:pilot-v2:sentiment-a:g045:r01 | 1 — positive | Reach under sofa avoids lifting; grateful back implies approval, not criticism of vacuum. | none material | agrees |
| data:pilot-v2:sentiment-a:g067:r01 | 2 — neutral | Packing locations do not evaluate the sleep mask. | none material | agrees |
| data:pilot-v2:sentiment-a:g089:r01 | 4 — positive | Accessible raised switch is valued; no lamp defect. | none material | agrees |
| data:pilot-v2:sentiment-a:g112:r01 | 1 — mixed | Head support praised; leaking and interrupted sleep criticised. | none material | agrees |
| data:pilot-v2:sentiment-a:g134:r01 | 4 — negative | Tray access is worse than bags; no praise for insert. | none material | agrees |
| data:pilot-v2:sentiment-a:g156:r01 | 2 — mixed | Cleanability explicitly appreciated; collapsed perch criticised. Negative overall conclusion does not erase praise. | none material | agrees |
| data:pilot-v2:sentiment-a:g178:r01 | 3 — negative | Bleed-through ruins pages and makes notebook unusable for these pens. | none material | agrees |
| data:pilot-v2:sentiment-a:g200:r01 | 3 — mixed | Cooling appreciated; drooping hinge requires readjustment. | none material | agrees |
| data:pilot-v2:sentiment-a:g201:r01 | 1 — positive | Dry contents after immersion earn trust; prior expectation of dampness is not an actual bag fault. | none material | agrees |
| data:pilot-v2:sentiment-a:g205:r01 | 1 — positive | Clear sleeve avoids unpacking; expected inconvenience was avoided, not a criticism. | none material | agrees |
| data:pilot-v2:sentiment-a:g210:r01 | 4 — negative | Seam leaks and double-bagging required. Saying closure is not the problem localises defect rather than praising closure. | Low: absence of closure defect is not an affirmative commendation; negative preferred over mixed. | agrees |
| data:pilot-v2:sentiment-a:g214:r01 | 2 — negative | Heavy rim causes wrist pain and interrupts sewing; no benefit asserted. | none material | agrees |
| data:pilot-v2:sentiment-a:g218:r01 | 2 — negative | Distortion spoils geometry and prevents intended use. | none material | agrees |
| data:pilot-v2:sentiment-a:g223:r01 | 4 — neutral | Leg settings and diary record only. | none material | agrees |
| data:pilot-v2:sentiment-a:g227:r01 | 3 — neutral | Routine storage and folding feet are not approval. | none material | agrees |
| data:pilot-v2:sentiment-a:g231:r01 | 3 — neutral | Seating and other chairs reported without judging capacity or comfort. | none material | agrees |
| data:pilot-v2:sentiment-a:g236:r01 | 3 — mixed | Level adjustment praised; splinters criticised despite negative overall conclusion. | none material | agrees |
| data:pilot-v2:sentiment-a:g240:r01 | 2 — mixed | Compact fit welcomed; finger pinching criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g134:r01 | 1 — mixed | Afternoon shade implies useful comfort; sunken support causes sliding. Both concern park amenity. | Low: shade is implicit amenity approval rather than explicit praise; mixed preferred. | agrees |
| data:pilot-v2:sentiment-b:g178:r01 | 1 — mixed | Moisture checks explicitly valued; unlatched door is criticism of service. | none material | agrees |
| data:pilot-v2:sentiment-b:g004:r01 | 2 — mixed | Useful explanation praised; dismissed question criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g094:r01 | 1 — mixed | Reliable early delivery praised; bent crossword handling criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g027:r01 | 4 — neutral | Track receipt and file identification without quality judgment. | none material | agrees |
| data:pilot-v2:sentiment-b:g125:r01 | 2 — positive | Assistant found missing volume and checked rather than guessing; implied service praise. | none material | agrees |
| data:pilot-v2:sentiment-b:g020:r01 | 1 — mixed | Accurate tracking praised; crushed presentation folders criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g192:r01 | 3 — negative | Omitted negation reverses safety instruction; serious implied criticism, not neutral transcription facts. | none material | agrees |
| data:pilot-v2:sentiment-b:g049:r01 | 2 — positive | Storm resistance and careful bracing earn confidence; neither/nor negate defects, not praise. | none material | agrees |
| data:pilot-v2:sentiment-b:g070:r01 | 3 — negative | Unidentified allergen forced abandoned meal; implied criticism of provider. | none material | agrees |
| data:pilot-v2:sentiment-b:g208:r01 | 1 — mixed | Crisp symbol reproduction praised; missing north arrow criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g222:r01 | 1 — negative | Dismissed welfare question overshadows visit; desire to watch flight does not praise provider. | none material | agrees |
| data:pilot-v2:sentiment-b:g239:r01 | 3 — neutral | Hours changed and other facilities unchanged; no expressed appraisal of longer session. | none material | agrees |
| data:pilot-v2:sentiment-b:g209:r01 | 2 — positive | Retained fine detail enables discrimination; blurred OTHER proofs are not criticism of Contour Press. | none material | agrees |
| data:pilot-v2:sentiment-b:g235:r01 | 2 — positive | Instruction finally enables clear comparison; previous blurred edges not attributed as provider fault. | none material | agrees |
| data:pilot-v2:sentiment-b:g211:r01 | 3 — positive | Instruction enables weaving; feared uneven warp is avoided, not actual fault. | none material | agrees |
| data:pilot-v2:sentiment-b:g224:r01 | 2 — mixed | Clear handling demonstration praised; banner obstructs landings. | none material | agrees |
| data:pilot-v2:sentiment-b:g228:r01 | 1 — mixed | Close feather observation is valued opportunity; loud microphone criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g212:r01 | 2 — negative | Cracked rental part damages thread; inspection failure criticised. | none material | agrees |
| data:pilot-v2:sentiment-b:g233:r01 | 4 — neutral | Booking time/equipment/access only; availability not independently praise. | none material | agrees |

## Byte preservation and files

SHA-256 before/after of `pre-review-r2/manifest.json` and the four sentiment JSONL files is unchanged; all four shard hashes match the candidate manifest. This preservation claim is scoped to those five files, not to unread unrelated shards. See `before-hashes.json` and `hash-preservation.json`. No candidate manifest or producer artifact was written.

New files exist only under `review-sentiment/`: `review.json`, this report, blind input sample, sealed targets, frozen judgments, protocol, preservation evidence, post-freeze audit and its read-only script. Do not reuse the annotated findings as a blind holdout.
