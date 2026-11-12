# Fixed reversal-probability means: five completed exploratory candidates

**On 240 new development references, M7 agreement rose from 171 native / 170 reversed to 182 after averaging; M10 fell from 182 / 178 to 177.** The fixed mean therefore does not generally improve selected answers. Its proper-score advantage against the mean constituent score is mathematical, not evidence of new reasoning.

## Scope and chronology

This is the completed initial five-candidate slice: frozen P3, M7, M8, M9 and M10, each with the same fixed equal-weight rule. The [rule index](../../configs/evaluation/e16-reversal-mean-v1.json) and [publication manifest](../../manifests/evaluation/e16-reversal-mean-report-v1.json) bind the executed evidence. M12 and the E13 exploration extension have **not** been executed in this slice.
The [fixed plan][plan] was adopted at 03:01 UTC on 12 November 2026, after earlier component results and producer positional tendencies were known but before mean calculation; this is exploratory, not an unseen-outcome decision.
The [initial four completion][done4] records 03:07:45.600331 UTC. [M10 completion][done10] records 03:21:05.666066 UTC, after actual P9 outputs and E11 scoring completed at 03:19; the [append binding][binding] documents that ordering and unchanged arithmetic.
Both executions finished before the original 03:26 UTC, 25-minute bound. M10 was an append, not a retroactive replacement of the initial four.
The receipts record 15 new scoring calls and 1,560 native-derived candidate vectors, zero old scoring calls, zero model/tokenizer loads and zero extra forwards. Those are workload counts, not independent quality denominators.

Keep **60 inherited**, **240 new** and **12 unique probe** references separate throughout. Their recorded source-group counts are 12, 170 and 12, respectively; reversed presentations are paired observations, not additional independent cases.
Development data have been reused across decisions. Source labels are agreement targets, not independently verified truth; same-alias and related source/scenario groups remain dependent. Neither case counts nor candidate counts remove that dependence.

## Rule and mathematical comparator

For each complete explicit native/reversed pair, validate and normalize both vectors under the existing scorer, align by semantic option ID, and compute `m_i = (p_i + q_i)/2`. Score the native-reference mean once, without dropping pairs or changing criteria.
There is no fitted weight, temperature, log pooling, better-order oracle, extra permutation or imputation. Existing constituent outcomes are retained, not rescored.
For the same normalized vectors, target and case weights:

- Natural-log loss obeys `NLL(m) ≤ [NLL(p) + NLL(q)]/2`.
- Summed multiclass Brier obeys `[B(p) + B(q)]/2 − B(m) = ||p−q||²/4`; the gain against that comparator is independent of the label.
- Neither identity guarantees improvement against the **better order**, uniform, or either order's argmax agreement.
- A target uniquely maximal in both constituents remains uniquely maximal in their mean. Outside that intersection, gains and losses must be measured.

The mean distribution and maximal semantic-option set are reversal-invariant **by construction**. The selected semantic option is invariant only with a unique maximum: the existing first-input tie-break is not generally invariant.
For two choices, reversal covers all permutations; for more than two, this is only a reversal-orbit average. All actual candidate/stratum native, reversed and mean blocks report zero top ties; that observation does not remove the general tie qualification.
Serving the rule requires **two forward presentations per request**; reuse of saved outputs here does not imply free deployment or a latency saving. See the canonical [R13 interpretation][r13].

## Agreement and proper scores by population

Entries are agreement counts and `NLL / summed Brier` (lower losses are better), rounded to six decimals directly from saved aggregates. N/R/mean use identical references and complete coverage. No pooled quality headline is used.

| Population | Candidate | N / R / mean agreement | Native NLL / Brier | Reversed NLL / Brier | Mean NLL / Brier |
| --- | --- | ---: | ---: | ---: | ---: |
| Inherited (60) | P3 | 35 / 34 / 36 | 1.194707 / .599128 | .966733 / .537541 | .980299 / .525433 |
| Inherited (60) | M7 | 45 / 44 / 44 | .576872 / .314785 | .552224 / .297745 | .500429 / .270457 |
| Inherited (60) | M8 | 35 / 34 / 36 | 1.191182 / .594447 | .959838 / .532837 | .971040 / .517882 |
| Inherited (60) | M9 | 43 / 43 / 43 | .673346 / .354056 | .673346 / .354056 | .673346 / .354056 |
| Inherited (60) | M10 | 44 / 45 / 44 | .506410 / .276910 | .474389 / .254632 | .479169 / .258058 |
| New (240) | P3 | 129 / 118 / 134 | 1.312350 / .633492 | 1.410621 / .687402 | 1.171135 / .587258 |
| New (240) | M7 | 171 / 170 / 182 | .669211 / .352959 | .618564 / .337570 | .536661 / .291256 |
| New (240) | M8 | 130 / 119 / 132 | 1.300082 / .630714 | 1.380115 / .675376 | 1.165015 / .585362 |
| New (240) | M9 | 165 / 165 / 165 | .699420 / .359766 | .699420 / .359766 | .699420 / .359766 |
| New (240) | M10 | 182 / 178 / 177 | .525300 / .288286 | .522373 / .282673 | .498428 / .272313 |
| Probes (12) | P3 | 9 / 11 / 11 | .649621 / .317726 | .419398 / .251247 | .346243 / .214544 |
| Probes (12) | M7 | 10 / 11 / 10 | .325502 / .202114 | .275787 / .164804 | .264550 / .151366 |
| Probes (12) | M8 | 9 / 10 / 11 | .629560 / .285103 | .427066 / .254383 | .328785 / .203826 |
| Probes (12) | M9 | 8 / 8 / 8 | 1.362500 / .425304 | 1.362500 / .425304 | 1.362500 / .425304 |
| Probes (12) | M10 | 10 / 9 / 10 | .293618 / .175614 | .354217 / .239230 | .320836 / .199734 |

Sources: [initial-four aggregates][sum4] and [M10 aggregates][sum10]. M10's probe mean worsens both proper scores relative to native despite retaining 10/12 agreement; its inherited mean also trails reversed proper scores. M7 loses one inherited and one reversed-probe agreement. Such exceptions are not erased by convexity.
M8 is not identical to P3: new mean agreement is 132 versus 134, with slightly lower NLL/Brier (1.165015/.585362 versus 1.171135/.587258); inherited and probe mean agreements match, but losses differ.

## Family effects and native-answer retention

Within each population, families have equal case counts: inherited 20 each, new 80 each, probes 4 each. Family cells show **native → mean agreement**. The last column gives native-correct retained / newly gained / lost, across that population.

| Population | Candidate | Intent | Sentiment | Rules | Retained / gained / lost |
| --- | --- | ---: | ---: | ---: | ---: |
| Inherited | P3 | 20 → 20 | 9 → 9 | 6 → 7 | 32 / 4 / 3 |
| Inherited | M7 | 20 → 20 | 19 → 20 | 6 → 4 | 43 / 1 / 2 |
| Inherited | M8 | 20 → 20 | 9 → 9 | 6 → 7 | 32 / 4 / 3 |
| Inherited | M9 | 18 → 18 | 20 → 20 | 5 → 5 | 43 / 0 / 0 |
| Inherited | M10 | 19 → 20 | 20 → 20 | 5 → 4 | 42 / 2 / 2 |
| New | P3 | 74 → 76 | 30 → 34 | 25 → 24 | 112 / 22 / 17 |
| New | M7 | 78 → 80 | 70 → 78 | 23 → 24 | 160 / 22 / 11 |
| New | M8 | 74 → 75 | 31 → 34 | 25 → 23 | 113 / 19 / 17 |
| New | M9 | 78 → 78 | 70 → 70 | 17 → 17 | 165 / 0 / 0 |
| New | M10 | 79 → 80 | 75 → 77 | 28 → 20 | 166 / 11 / 16 |
| Probes | P3 | 4 → 4 | 2 → 4 | 3 → 3 | 9 / 2 / 0 |
| Probes | M7 | 4 → 4 | 4 → 4 | 2 → 2 | 9 / 1 / 1 |
| Probes | M8 | 4 → 4 | 2 → 4 | 3 → 3 | 9 / 2 / 0 |
| Probes | M9 | 2 → 2 | 4 → 4 | 2 → 2 | 8 / 0 / 0 |
| Probes | M10 | 4 → 4 | 4 → 4 | 2 → 2 | 10 / 0 / 0 |

M7 new intent retains 78, gains 2 and loses 0; sentiment retains 69, gains 9 and loses 1; rules retain 13, gain 11 and lose 10. M10 new rules retain 12, gain 8 and lose 16, outweighing its intent/sentiment improvements.
M7's unchanged probe-rule total conceals one gain and one loss. Both-raw-correct counts (inherited/new/probe) are P3 28/82/9, M7 39/138/9, M8 28/86/9, M9 43/165/8 and M10 41/157/9; receipts report zero failures to retain unique correctness in this intersection.

## Rule limitations and meaningful starting context

All 80 M7 new rule-mean choices remain native **first/last endpoints: 39/41**, with no ties. The [position supplement][pos4] records 23 distinct three-choice vectors across 23 cases and 57 distinct four-choice vectors across 57 cases, with nonzero coordinate variation within each arity.
These are not one exactly constant vector per arity, but that does not establish semantic reasoning: length, formatting, source or other cues can produce nonconstant vectors.
M7 rule-mean NLL/Brier is **1.359448/.752823**, worse than uniform **1.303586/.726042**. Agreement is 24/80 versus uniform's deterministic first-choice 23/80; uniform's probability-based expected agreement is **27.3958%**, a different quantity from deterministic tie-broken agreement. This is **not evidence of rule competence**. M10's rule mean also remains worse than uniform on NLL/Brier (1.313404/.732016) while agreement falls28→20/80; its proper-score gain versus its own constituents does not reverse that comparison.
A constant slot prior averaged with its reversal can create mirror-symmetric endpoints and unchanged odd-arity middle preferences, mimicking features of an invariant mean without case-specific semantic information.

| Native contextual baseline | Inherited: agreement; NLL / Brier | New: agreement; NLL / Brier | Probes: agreement; NLL / Brier |
| --- | ---: | ---: | ---: |
| Uniform | 17/60; 1.378765 / .746111 | 65/240; 1.333463 / .733681 | 4/12; 1.055008 / .645833 |
| Original MS MARCO pretrained start | 30/60; 1.026878 / .552223 | 99/240; 1.058568 / .581492 | 7/12; 1.453783 / .651840 |

The pretrained start is meaningful, not an invented random-head substitute. Its new intent/sentiment/rule agreements are 66/18/15; M9 means are 78/70/17. M9's native, reversed and mean agreement is unchanged in every population; displayed losses also match at six decimals, a numerical control rather than a claim of exact floating-point equality.
M9's remaining new rules (17/80) stay below uniform deterministic agreement (23/80); improved intent/sentiment does not generalize to rules. Baseline family details and provenance are in the [initial][pos4] and [M10][pos10] supplements.

## Evidence boundary and continuation

R13 independently reviewed mathematics and the initial-four source/receipts, **not an independent raw replay and not later M10**. Its [source-review qualification][review] distinguishes exact normalized study-prediction/old-report agreement from upstream release files that were hash-bound but not independently compared by that review.
Initial-four receipts report maximum Brier-identity residual 4.440892098500626e−16; M10 reports 3.1051550219984847e−16. Both report maximum pre-score mean-sum deviation 1.1102230246251565e−16 and zero recorded finite-constituent NLL, Brier or strict-retention violations.
All actual constituent and mean aggregate target-zero counts are zero. The implementation's finite-constituent NLL guard is therefore applicable here, but is not a general certification of infinite-loss handling; do not clip or discard future zero-target cases.
This publication summarizes those completed new-vector calculations without another scoring or model pass. It neither revises earlier criteria nor rescues old results, and supports no significance, calibration, promotion or controlled-architecture conclusion. Existing E8/E9 and E11 lineage reviews, not the R13 source review alone, bind upstream predictions to the retained study rows.
Any later completed E13 exploration checkpoint plus this rule is a **distinct candidate** consuming one of at most two optional slots if selected, not automatic confirmation admission. The 06:30 checkpoint/rule lock, four mandatory predictors and existing optional-slot cap remain unchanged; no unselected derived confirmation report or extra unselected underlying raw-model quality report is authorized.

[plan]: ../../artifacts/evaluation/e16-reversal-mean-v1/plan.md
[sum4]: ../../artifacts/evaluation/e16-reversal-mean-v1/execution-01/summary.json
[pos4]: ../../artifacts/evaluation/e16-reversal-mean-v1/execution-01/context-position-supplement.json
[done4]: ../../artifacts/evaluation/e16-reversal-mean-v1/execution-01/completion.json
[sum10]: ../../artifacts/evaluation/e16-m10-reversal-mean-v1/execution-01/summary.json
[pos10]: ../../artifacts/evaluation/e16-m10-reversal-mean-v1/execution-01/context-position-supplement.json
[done10]: ../../artifacts/evaluation/e16-m10-reversal-mean-v1/execution-01/completion.json
[binding]: ../../artifacts/evaluation/e16-m10-reversal-mean-v1/append-binding.json
[r13]: ../research/reversal-mean-interpretation.md
[review]: ../../artifacts/research/r13-20261112T025943Z/e16-source-review.md
