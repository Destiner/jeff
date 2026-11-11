# D4 target-hidden review

## Outcome

Frozen judgments cover **24/24** supplied TRAIN decision projections. Under the exact rendered policies, I find **24 uniquely defensible listed answers**, **0 unresolved**, **0 multiple-defensible**, and **0 confirmed contradictions**. These are reviewer judgments, not ground truth, target agreement, or independent verification. No saved targets were accessible or requested. Each judgment records its option ID and verbatim text, calculation, uniqueness assessment, alternatives, missing conventions, and construction note in `judgments.json`.

The main finding is **limited discrimination of full-policy execution**, not ambiguous labels. Several rows can be solved using a subset of the policy, and some distractors are structurally impossible. This bounded review does not establish how often shortcuts work outside these 24 projections or whether any trained model uses them.

## Specification and notation

The rendered tasks supply the conventions that matter: strict versus inclusive comparisons, lexicographic field priority, deduplicated eligibility, nonnegative reductions and operation order, explicit rounding ties, controller no-ops, rotation direction/step counting, quarantine and batch reporting order, and scheduling endpoint/cooldown behavior. Tuple and coordinate notation are sufficiently specified here. No missing convention changes a selected answer.

In particular:

- Equal pump ratios **return Vendor A**, not the offered `Tie`. The question asks which result follows from a policy that resolves equality. Raw equality does not create a second defensible policy output.
- The timber tie at 145 selects 150 by explicit instruction. External half-even or other rounding conventions do not introduce ambiguity.
- Endpoint-touching bookings do not overlap under these policies. An inclusive-end external scheduling convention is overridden.
- Repeated legal-officer signatures do not increase the distinct eligible count. Three raw signatures do not justify rejection as too many.
- Candidate labels and opaque IDs were used only to record the selected answer, not to infer it. No answer was inferred from row or option order.

## Choice construction and policy shortcuts

### Confirmed structural weaknesses in these rendered choices

1. **Impossible signer distractor** — both archive rows (`data:pilot-v2:rule-a:g001:r07`, `...:r08`) offer “Reject: too many eligible signers,” but only two signer identities are eligible and duplicates are ignored. The count cannot exceed two. This removes one choice without evaluating the received signature list. It does not by itself identify the answer between authorization and too few.
2. **Impossible final tie output** — both pump rows (`data:pilot-v2:rule-b:g005:r07`, `...:r08`) offer `Tie`, although the stated return rule resolves every equality to Vendor A. That option can always be eliminated. The equal-ratio row still requires recognizing equality to apply the tie-break; the unequal row also happens to favor B when comparing numerators alone.
3. **Weak coordinate distractors** — for the zero-coordinate row (`data:pilot-v2:rule-b:g006:r07`), addition already produces the final answer and reflection has no effect. For `...:r08`, the correct answer is the only option with negative x; determining the post-reflection sign can eliminate all others without calculating both coordinates. Its addition-only result is offered, but reverse-operation result (−5,4) is not.
4. **Minimum-pack row omits the natural capacity-only answer** — `data:pilot-v2:rule-b:g002:r07` needs one pack for demand but requires at least three. Options are 2, 3, 6, 0. Two options immediately violate the minimum, and three is visibly sufficient. This checks a simple minimum constraint more than the full stock/reserve/unusable-unit policy.

None of these makes the chosen answer ambiguous or inconsistent. They weaken what a correct multiple-choice selection demonstrates.

### Degenerate or easy states, not specification defects

- `data:pilot-v1:rule_application:g01:r07`: only urgent is on. Active-flag lookup works; first-match precedence is not exercised.
- `data:pilot-v1:rule_application:g10:r07`: the controller returns to its initial state. Ignoring events happens to yield the same answer, although the two-step trace is unambiguous.
- `data:pilot-v2:rule-a:g003:r08`: demand exceeds all usable stock. Taking all usable units determines the answer without FIFO priority. By contrast, `...:r07` genuinely distinguishes earlier-batch issue from taking later stock first.
- `data:pilot-v2:rule-b:g008:r07`: every listed start is legal; choosing the smallest listed start succeeds without checking overlap/cooldown. In `...:r08`, every start is inside the existing appointment, so rejecting all of them needs no endpoint or cooldown reasoning.
- `data:pilot-v2:rule-a:g007:r08`: 144 is not a tie. Distant rounding distractors are easy to reject; this does not undermine the unique nearest-multiple result.
- Pack cases have zero unusable units, reserve, and starting stock. Those components of the general calculation are inert in these rows.

Thus the answer to “can choices give away the answer without implementing the stated policy?” is **partly yes**: subset-of-policy reasoning and option elimination suffice for some supplied instances. There is no demonstrated universal options-only solver, and these observations do not show label leakage. Easy cases and redundant distractors should not be promoted into claims of ambiguity. No new rows, generators, or broad survey were produced.

## Freeze, identity, timing, and scope

- Actual environment identity: `PI_PROVIDER=openai`; `PI_MODEL=gpt-sol`. No other environment values were dumped. This reports the actual alias, not a guessed underlying model version.
- Start: **2026-11-11T14:53:33Z**.
- Judgment freeze and post-judgment input-hash checkpoint: **2026-11-11T14:55:40Z**, **127 seconds** after start. This duration covers bounded inspection and frozen judgments; report composition follows that checkpoint, within the approximately eight-minute timebox.
- `judgments.json` was written first, made read-only (mode 0444), and not revised. Read-only permissions provide a local freeze, not cryptographic append-only storage; its digest below identifies the frozen bytes.
- Frozen judgments SHA-256: `792ed9d238e7f2a00c74397b6fbf7df3d642dda59454a4ea7678c97dfcc65303`.
- Input SHA-256 before inspection, at 14:53:33Z: `c550b997ccfd352cf3844b6411bc10c0f4b13d1693826bbd6b5123acfd32920d`.
- Input SHA-256 after judgment freeze, at 14:55:40Z: `c550b997ccfd352cf3844b6411bc10c0f4b13d1693826bbd6b5123acfd32920d`.
- **Input hashes match.** The input was not modified.

Only `/Users/destiner/Code/jeff/AGENTS.md`, `/Users/destiner/Code/jeff/docs/contracts.md`, and the explicitly supplied `blind-inputs.jsonl` were read. The only data input was that JSONL. Instruction cross-references were not followed into excluded project material. No parent references, selections, provenance, reviews, datasets, generators, prior conversations, or Evaluation/held-out/probe/final content were read. No directory survey was performed.

No network requests, additional model/API calls, tests, lint, Git, mailbox operations, dependency installations, or paid compute were invoked. Local shell operations were limited to identity/timestamps, hashes, creation of the new review directory, and making the new judgment file read-only. Only new files under this `blind-review/` directory were written. No build was run because this was a data-only frozen review, not a code change.

**Independence limit:** a fresh target-hidden judgment under the same model alias is not independent human or model-family verification. No correctness percentage, ground-truth certification, or agreement with hidden targets is claimed.
