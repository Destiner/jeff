# R13: what the fixed reversal-probability mean can establish

**The rule may expose useful residual ranking information, but its proper-score advantage over the mean constituent score is mathematical, not evidence of new reasoning.** Reversal invariance applies to the resulting probability vector and maximal-option set; the existing first-input tie-break can still change the chosen semantic option on exact ties.

This reviews lead's single frozen E16 rule, not another aggregation arm, correction fit, training experiment or approval gate. Evaluation owns actual derivation/scoring and retains all raw results unchanged.

## Exact rule and source checks

For a complete native/reversed pair, validate and normalize each probability vector exactly as the existing scorer, align by the existing **explicit example/option identity maps**, then compute for each semantic option i:

`m[i] = (p_native[i] + p_reversed_aligned[i]) / 2`.

Do not average display slots, raw logits, unnormalized masses, selected answers or independent binary probabilities. No weight fitting, temperature, log/geometric pooling, better-order oracle, extra permutation or fallback is introduced. Missing/mismatched pairs stop that candidate's derivation; do not silently restrict the population.

`src/jeff/evaluation/metrics.py::validate_prediction` requires schema0.1, exact option-ID sets, no repeated IDs, finite non-boolean numeric probabilities in[0,1], and sum error≤1e−6. It divides by the observed sum without clipping. `score_examples` selects `max` in **reference input order**, counts exact ties, records zero-target loss as positive-infinity status, and sums Brier over options.

The existing `order.py` source verifies explicit original/reversed example IDs, group/reference consistency, exact reversed option objects with preserved IDs and complete nonrepeated pair coverage. Reading this source does **not** authenticate the actual E16 input maps or files. The same tuple of checkpoint, source predictions, maps, references and normalization rule must be bound in Evaluation's receipt.

## Two proper-score identities, with the correct comparator

For target y and normalized p,q, natural-log loss is `L(p) = −ln(p[y])`. Convexity gives:

`L((p+q)/2) ≤ (L(p)+L(q))/2`.

This is against the **mean of the two losses**, not the better order or uniform. If one target mass is zero, the right side is infinite; if both are zero, both sides are infinite. Preserve the scorer's status, never clip to epsilon or subtract infinity from infinity.

For summed multiclass Brier `B(p)=Σ_i(p[i]−1[i=y])²`, expansion gives the exact identity:

`(B(p)+B(q))/2 − B((p+q)/2) = Σ_i(p[i]−q[i])² / 4`.

The Brier gain against this comparator depends only on the vectors' disagreement, **not the target**. Highly inconsistent answers can therefore produce an impressive mechanical gain without improved choice information.

Both statements carry through identical nonnegative normalized case/source weights. They do not apply to comparisons that change cases, coverage, arity/reference mappings or weighting. Floating-point mean construction and the scorer's second accepted-roundoff normalization can introduce tiny numerical residuals; record them honestly rather than present a rounded tolerance violation as a new phenomenon. No new clipping/normalization arm is needed.

There is no general top-choice accuracy guarantee. If the same correct option is uniquely maximal in both inputs, it remains uniquely maximal in the mean; outside that intersection, measured gains and regressions matter. Report agreement, proper scores, ties and retention against the native baseline, meaningful starts and uniform, with inherited/new/probe and family effects kept separate. Do not substitute the Jensen inequality for measured success.

## Invariance and the consequential tie exception

Reversing the request swaps the two aligned summands. Thus **m and its maximal-option set are invariant under reversal by construction**, assuming the two fixed constituent vectors. If the maximum is unique, the semantic choice is invariant too.

On exact top ties, however, reapplying the existing “first option in reference input order” policy to the reversed reference can select a different semantic option. Holding the native reference fixed yields one deterministic tie choice, not learned order robustness. **Do not claim unconditional selected-choice invariance or zero semantic flips from the distribution identity.** Keep existing tie semantics; this review proposes no new tie-break arm.

For K2, identity/reversal enumerate all permutations. For K>2, this is only a **reversal-orbit average**, not arbitrary-permutation invariance. Copying the derived vector into another order does not create an independently observed successful prediction or another independent case.

## Constant prior versus useful rank information

If a model emits an exactly constant K-slot prior b for every content item in both orders, averaging gives, in zero-based indexing:

`m_at_native_slot[j] = (b[j] + b[K−1−j]) / 2`.

This is a mirror-symmetric positional prior, with an odd-K middle coordinate unchanged. It contains no new case-specific semantic information and can create exact mirror ties. Agreement can still reflect target-slot/source composition and tie-breaking. Conversely, nonconstant retained probabilities are **necessary but not sufficient** evidence of useful case-dependent ranking; variation may follow length, formatting, source or policy cues rather than reasoning.

Actual E16 agreement changes can show useful residual ranking on these exposed cases, including where raw dominant-slot choices hide differences. They cannot establish a causal mechanism, algorithm mastery, independent calibration or arbitrary-task generalization. Do not fit another prior/weighting rule to make this contrast favorable.

## Populations, costs and confirmation

The stipulated existing development population is **60inherited +240new +12probe pairs =312unique native references**, derived from624raw presentations. Preserve each stratum and its current source/group units. No duplicated624derived-score population; probe pairs are not24independent cases. Actual counts and coverage belong in Evaluation's execution receipt, not a source-only certification here.

E16 may use existing paired outputs for P3/M7/M8 and only actually completed authorized M10/M12 outputs. M9 can be a numerical order-invariant control, not an assumed exact floating-point-equality certificate. No raw output is overwritten and no missing pair is recreated with inference. Existing paired artifacts make this analysis **zero extra forwards**, but a deployed request requires **two inference presentations/forwards**, not one; batching does not make the extra work free and no latency saving follows.

The identical fixed rule may later be applied once to completed E13 **exploration** decoder outputs, without extra inference or selecting cases. Every checkpoint+rule is a distinct exposed candidate. If chosen at0630, it consumes one of the existing **at-most-two optional slots** alongside four mandatory predictors, and its checkpoint/rule are frozen. Reuse only its already-authorized paired raw confirmation pass; no unselected derived confirmation scores, extra raw-model quality report, sealed-cohort reopening or new pooled promotion score. Until actual selection and execution grants, confirmation remains sealed.

## Review provenance and boundary

Start2026-11-12 02:59:43UTC; R13 cap03:14:43. Independent mathematics/source review: `artifacts/research/r13-20261112T025943Z/math-review.md`. Direct non-gating coordination and the material tie qualification went to Evaluation at the start. No raw held-out prose/labels, protected-final payload, prediction scoring, model/tokenizer/weights, learning, extra forward, new data, dependencies, tests/lint, spend or upload was used by Research.

Actual E16 `plan.md`, `derive.py` and approved label-free completion/summary were reviewed within this bound. Completion03:07:45UTC records four candidates×312=1248 candidate-case checks,12new/zero old scoring calls, zero extra forwards, zero recorded convexity/strict-retention failures, maximum Brier-identity residual4.44e−16 and mean sum deviation1.11e−16. This is source/receipt review, not an independently rerun scoring certification. Parent inspected all36native/reversed/mean aggregate NLL blocks: zero target-zero counts everywhere, so the source's finite-constituent Jensen guard covers these actual outputs; it is not a general infinite-case validator. The source exactly matches retained study predictions to old normalized report probabilities, while upstream release files are only hash-bound, not independently compared to study rows here. Any stronger upstream-lineage claim must cite existing authorized evidence rather than infer it from these pins. Detailed scope/qualifications are in `e16-source-review.md`; no private paths were followed. Actual review status is not inferred from package builds or the mathematical proof. No reinterpretation rescues E7–E15 criteria or grants promotion. Foreground night availability continues independently through08:30:36UTC.
