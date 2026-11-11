# R6 focused method review: what paired reversal can identify

**Status:** mathematical/source review and prospective analysis recommendation only. No predictions, labels, case text, Evaluation export, private Evaluation/probe/D3/final data, model weights or tokenizer were accessed. No inference, training, downloads of model assets, dependencies, paid work, tests/lint, mailbox activity, commits or merges. The parent has requested an Evaluation-owned text-free export; its availability/content is not assumed here. This document is not an executed diagnostic or a frozen case packet.

**Scope:** preserve frozen M6/P4/E6 unchanged. One separately authorized frozen-P3 diagnostic may later contain at most 48 preselected TRAIN cases × four conditions (at most 192 presentations), scheduled by Model and executed by Runtime, never Research. No prompt search, correction deployment, calibration exercise or second inference pass is proposed. Public paper text alone was retrieved for the focused source review.

## 1. Decision in brief

1. Standard ordinal letters and display position are confounded. Original/reversed conditional probabilities, aligned by opaque **option identity**, identify only mirror-antisymmetric contrasts of a fixed additive slot/letter bias, conditional on content invariance. They do not identify a complete bias vector or a causal label effect.
2. Fit the antisymmetric component once on a source-disjoint fitting partition; describe fidelity on one untouched source partition. Do not subtract an arbitrary full bias vector and call the result corrected, accurate or calibrated.
3. The four-cell packet can distinguish mirror-antisymmetric **label-associated** and **position/order-associated** changes under additivity. It cannot hold the entire content sequence fixed when moving an option between positions. Order/context effects and label-sequence familiarity remain plausible explanations.
4. Use labels neither for selection nor for these descriptive computations. Conditional distributions suffice for own per-case log-odds changes, but cannot recover total probability assigned to valid answer tokens in the full vocabulary.

## 2. Paired original/reverse: derivation and non-identifiability

Let case c have K options indexed by semantic identity i. Its original slot is j(i), with mirror r(j)=K−1−j. Slots are zero-based. Standard rendering assigns A to slot 0, B to slot 1, …, up to the supported K (A…K if K≤11). These **rendered letters are not opaque contract option IDs**. Join all outputs by the latter, not array order or letter.

The proposed working model is

`p[c,O,i] = softmax_i(u[c,i] + b[K,slot(O,i)])`,

where `u[c,i]` is case-specific invariant content utility, and `b[K,j]` is fixed across cases with K choices. This is a substantive assumption, not a consequence of softmax. With standard letters, b combines letter, position and any repeatable correlated rendering effects.

For positive probabilities, define

`d[c,i] = log p[c,original,i] − log p[c,reverse,i]`,

`y[c,i] = d[c,i] − mean_h d[c,h]`.

The normalizer difference is constant across i and centering removes it. Under the working model,

`y[c,i] = gamma[K,j(i)]`, where `gamma[K,j] = b[K,j] − b[K,r(j)]`.

Consequences:

- `gamma[K,r(j)] = −gamma[K,j]`; the odd-K middle contrast is exactly zero under the model.
- There are only floor(K/2) identifiable bias contrasts for each K, not K−1 independent bias coordinates. The antisymmetric part of b is `gamma/2`, **not gamma**.
- A nonzero centered middle contrast in observed odd-K data is model lack-of-fit, not evidence for an identified middle bias.
- For any mirror-symmetric vector s (`s[j]=s[r(j)]`), replacing `b[j]` by `b[j]+s[j]` and `u[c,i]` by `u[c,i]−s[j(i)]` leaves both distributions unchanged. Even imposing sum(b)=0 generally leaves symmetric nonconstant degrees of freedom. An overall constant is always irrelevant. For K=2 only the ordinary constant remains, but label and position are still confounded.
- Only mirror pairs are exchanged. An end-versus-middle symmetric preference is invisible to this design. With K=3, b=(a,−2a,a) produces zero reversal contrast despite nonconstant bias.
- If u changes with presentation, `y` also contains centered `u[original]−u[reverse]`. A good fit supports a compact description of these outputs, not a proof that the model used a token prior or ignored content.

An unconstrained observed vector y need not be antisymmetric across mirror slots. Its mirror-symmetric component, and any nonzero odd middle, must remain in reported residuals; do not force the observed data to obey the hypothesis before assessing it.

### Conditional probabilities and unlabeled log odds

For any two semantic options i,h, one can compute without targets:

`Delta[c,i,h] = log(p_orig_i/p_orig_h) − log(p_rev_i/p_rev_h) = y[c,i]−y[c,h]`.

If p is obtained by normalizing next-token probabilities q over just the K allowed letters, then `p_i=q_i/M`, where `M=sum_allowed q`. Any compatible 0<M≤1 gives the same p. Thus p identifies within-set odds, not M, full-vocabulary entropy, probability of producing a valid letter, free-generation validity or calibrated correctness. No statement about those quantities follows from this export alone.

## 3. One frozen source-held-out descriptive fit

**Before outputs:** freeze exact input/export hashes, identity maps, K, provenance source units, group membership, source split, eligibility/zero rules, weights and summaries. Use no outcomes, target labels, high-flip selection, confidence screening or prompt tuning. Existing paired outputs may already have been observed by their producer: then call this a prospectively specified analysis of existing outputs, not a pre-outcome experiment.

Use one deterministic split of whole `provenance.source` units (or Evaluation-supplied stable text-free equivalents), with all related `group_id` variants kept together. Choose the split from metadata only; put roughly one third of source units in the descriptive holdout and the rest in fit, while retaining fit coverage of K where feasible. Record the actual split rather than promising balanced strata that may not exist. Do not substitute a random row split. If there is only one independent source, a genuine source-held-out claim is unavailable: report that limitation and do not silently rename groups as sources. This is **one fit and one holdout**, not a source sweep or outcome-selected split.

Within each K fit constrained weighted least squares:

`min_gamma sum_c w[c] * (1/K) * sum_i (y[c,i]−gamma[K,j(i)])²`,

with mirror antisymmetry and zero odd middle. The closed-form mirror contrast is the weighted average of `(y[c,j]−y[c,r(j)])/2`; use that value for gamma[j] and its negative for gamma[r(j)]. No full b is estimated. Freeze the fit and apply it unchanged to holdout sources. Unsupported holdout K is explicitly unscored, never filled using its outcomes or borrowed from another K.

**Weights:** to avoid repeated variants and large K dominating, give each source equal total weight within a K, each independent group within that source/K equal weight, each case within that group/K equal weight, and each option its case weight divided by K. Equivalently case weight is proportional to `1/(S_K * G_source,K * n_group,K)`. Report per-K results first; a macro average gives each supported K equal weight. State that this is a declared balanced-source estimand, not deployment prevalence. Also show counts of sources/groups/cases/options, raw coverage and per-source summaries. A group spanning K is never split across partitions. If source membership cannot be exported safely, use group-balanced weights but label the missing source-held-out requirement unresolved.

### Fidelity summaries, not task-quality metrics

Freeze these outputs, without an outcome-dependent pass/fail threshold:

- Weighted holdout RMSE and MAE of `y−gamma`, in natural-log units; signed residual means by K/slot/source, and descriptive median/90th percentile of case RMS residual.
- Compare with the fixed-content-only prediction `y=0` using heldout SSE reduction `1−SSE_fit/SSE_zero`; allow negative values. If SSE_zero=0, this ratio is undefined, not perfect explained variation. No post-hoc alternate metric or split selection.
- Show fitted gamma with fit source/group support; show holdout residual mirror-symmetric versus antisymmetric energy and odd-middle residual explicitly. These diagnose violations rather than repair them.
- Optional paired distribution fidelity is fully specified: predict reverse from original via `p_hat_rev_i ∝ p_orig_i * exp(−gamma[K,j(i)])`; compare with observed reverse using case-balanced total variation. For symmetry also predict original from reverse using +gamma, then average the two directional TV values. This is a descriptive transform using heldout case probabilities, **not** standalone prediction from question text or a verified correction. It uses only the identifiable contrast; hidden symmetric biases remain.

“Compatible with a shared antisymmetric description” means modest residuals and improvement over zero that persist across reported holdout sources, with numerical magnitudes shown. It does not mean causal identification, accuracy gain, correction, calibration, or even that the invariant latent utility is semantically right. Report conflicting sources, unsupported K and failures directly. No inferential p-values or independence claims from numerous within-case option pairs.

### Zeros, invalidity and selection

Reject and count nonfinite/negative values, missing or duplicate options, broken identity joins, and sums outside the existing contract tolerance; do not silently repair malformed records. Keep raw outputs immutable. Use log probabilities from the **same frozen readout** if already available/exportable; do not infer new logits from weights.

For exact p=0, log contrasts are undefined (including 0/0). Primary log analysis uses only pairs with all K probabilities strictly positive in both presentations, with exclusions/coverage reported by K/source/group and weight renormalization declared. This is a positive-support subset, not all cases. Keep zero-containing cases in defined probability-space summaries where feasible. Separately report a predeclared sensitivity analysis flooring each probability at epsilon=1e−12 and renormalizing within condition; report the number of altered entries, affected cases and whether conclusions change. Do not describe floored numbers as measured probabilities, treat zeros as tiny known probabilities, or choose epsilon after inspecting favorable fit. A source/group disappearing through exclusion is a coverage limitation.

## 4. Four-condition order × letter-assignment packet

Use exactly the same TRAIN cases and semantic option identities in every cell. Let O=0 original semantic sequence, O=1 reversed sequence. Let L=0 standard letters by displayed slot, L=1 reversed letters by displayed slot. For option i originally at j:

`slot = O ? r(j) : j`

`actual_letter_index = L ? K−1−slot : slot`

`actual_letter = chr(ord('A') + actual_letter_index)`.

| Cell | Semantic slot | Actual letter index | Displayed letter sequence |
|---|---:|---:|---|
| 00 | j | j | A,B,… |
| 01 | j | r(j) | …,B,A |
| 10 | r(j) | r(j) | A,B,… |
| 11 | r(j) | j | …,B,A |

Runtime must bind probabilities to the **actual rendered letters** and then restore semantic IDs. Merely reversing option arrays while retaining a slot-index readout does not implement the L intervention. The full permitted letter set is unchanged. Preserve P3 prompt/readout/T1/cap/model pins; alter only the authorized order/letter assignment. Freeze rendering and handling of truncation or invalid runs before results, and report failures, not replacements. If arbitrary letter assignment cannot be expressed without an unapproved readout/prompt change, stop at packet preparation and disclose that incompatibility rather than silently changing frozen P3.

Let `x[OL,i]=log p[OL,i]−mean_h log p[OL,h]` (semantic alignment). An additive descriptive model is

`x[OL,i] = U[c,i] + centered_i(a[K,letter(OL,i)] + t[K,slot(O,i)])`,

with fixed letter a, fixed position t, and invariant per-case content U. Define mirror contrasts `alpha[j]=a[j]−a[r(j)]`, `beta[j]=t[j]−t[r(j)]`.

### What comparisons actually change

- **00 vs 01**, and **11 vs 10**: same semantic order and same option position; actual letter changes. Under additivity, both `x00−x01` and `x11−x10` equal alpha[j]. These are the cleanest label-assignment comparisons, but they also change the entire displayed letter sequence and alphabet familiarity.
- **00 vs 11**, and **01 vs 10**: actual letter for each semantic option is held fixed; its position **and the entire content order change**. Under additivity, `x00−x11` and `x01−x10` equal beta[j]. These do not isolate pure position from order/context effects.
- **00 vs 10**: standard-letter reversal changes both letter and position; expected contrast alpha+beta. **01 vs 11**: reversed-letter reversal changes both with opposing letter direction; expected contrast beta−alpha.

Two equivalent descriptive estimates are

`alpha_hat[c,i] = ((x00−x01)+(x11−x10))/2`,

`beta_hat[c,i] = ((x00−x11)+(x01−x10))/2`.

They can also be obtained as half the difference/sum of the two reversal contrasts. They are finite-difference contrasts of these prompts, not identified neural mechanisms. Center within each condition before combining to remove softmax normalizers.

A necessary additive residual contrast is

`R[c,i] = (x00−x01)−(x11−x10) = x00−x01+x10−x11`.

It should vanish under the additive invariant-content model. The sign pattern matters because a semantic option's letter mapping reverses when O reverses. Nonzero R flags nonadditivity/invariance failure; it does not uniquely identify a letter×position mechanism. Also fit/report cross-case heterogeneity of alpha and beta, mirror-symmetry violations and odd-middle contrasts. Zero R alone is insufficient: nonstatic effects may cancel.

### Fixed-content, static-letter, static-position and residual accounts

Use these as transparent descriptive accounts, not outcome-selected corrected models:

- **Fixed-content-only:** each semantic option keeps the same conditional probability in all four cells; alpha=beta=0 and all cell differences vanish. This can be consistently wrong without labels.
- **Static-letter-only (strict):** within K a single distribution follows actual letters across cases, regardless of content/slot. It predicts beta=0, R=0 and shared alpha, but these contrast restrictions alone do not establish the strict account: an invariant content contribution is invisible in differences. The more permissive **fixed content + static letter** account has those same contrast restrictions and permits case-specific U.
- **Static-position-only (strict):** within K a single distribution follows displayed slots across cases, regardless of actual letters/content. It predicts alpha=0, R=0 and shared beta. Again contrast agreement supports at most **fixed content + static position**, unless absolute distributions also match the strict slot-only distribution.
- **Additive content + letter + position:** both shared alpha and beta may be nonzero; compare its heldout difference residuals with the three restrictions above using the same fixed weights/metrics, without selecting a promoted model. Residual includes case-dependent content/order response, source heterogeneity, label binding problems, nonadditivity, numeric/readout issues and other omissions; never name it “reasoning failure” by default.

The one source-held-out fit can estimate both alpha and beta in this additive diagnostic, if executed, using the same mirror-constrained weighted averages; restricted accounts are fixed zero-component comparisons, not separate prompt searches or new inference arms. Do not fit per-case U on all four heldout cells and then advertise a heldout prediction of those same cells. Direct contrast fidelity avoids that leakage.

## 5. What remains unidentified even with four cells

- Only j and r(j) are visited by a given semantic option. Mirror-symmetric components of a and t can still be absorbed into U. Complete K-letter and K-position preference vectors are not recovered by these four cells.
- Moving semantic content also changes predecessors, successors, recency and question–option context. Beta is position/**order-associated**, not position-only causal bias.
- A fully general label×position interaction is not estimable from only mirror pairings. Additive contrasts can absorb some interaction effects; R may detect other violations but cannot attribute them uniquely. Most label/slot pairings are never observed when K>2.
- Reversing letters changes a familiar ascending alphabet sequence into descending order. Label effects, sequence familiarity, symbol-binding difficulty and label/context interactions are not independently randomized. A degraded reversed-letter condition is not proof of a static letter preference.
- For odd K, the middle option has the same slot and letter in all four cells. Any change in its probability may reflect normalization or context; its **centered log** change under the additive invariant-content hypothesis is zero. Raw middle p need not stay fixed because other logits change normalizers.
- Case freezing prevents outcome-conditioned sampling, but this small TRAIN sample is not new heldout task evidence. Source-held-out here means transfer of a descriptive bias account between sources, not unseen-model-training data. No claim of broad generality or causal exclusivity is warranted.

## 6. Targeted primary-source grounding (two sources only)

**Zheng et al., ICLR 2024, _Large Language Models Are Not Robust Multiple Choice Selectors_ [Z24].** §2.4 explicitly identifies the natural binding between option IDs and positions, uses ID shuffling/removal as ablations, and warns that shuffled IDs impair prompt naturalness. §3.2, equations (2)–(3), makes the independence/permutation-invariance assumptions needed for multiplicative prior/content decomposition; it explicitly says its prior combines token and position bias. §3.1 uses cyclic permutations covering every ID/content pairing, unlike reversal's mirror-only coverage. These motivate our assumption checks, not a claim that PriDe or token bias has been established for this Qwen/P3 setup. Our stronger cross-case fixed b is an R6 assumption, not something this paper proves. We do not authorize their correction method or their use of test examples.

**Robinson, Rytting & Wingate, ICLR 2023, _Leveraging Large Language Models for Multiple Choice Question Answering_ [R23].** §3 distinguishes symbol-token MC prompting from text-likelihood cloze scoring. §4 defines multiple-choice symbol binding and explicitly says its order-invariance metric PPA is independent of task ability: consistent answers can be wrong. This supports separating descriptive fidelity from accuracy. Our two/four-cell packet is not their exhaustive-permutation PPA and should not be named PPA. Their model findings do not establish Qwen0.5B behavior or calibration.

Exact URLs, section anchors and quoted evidence are in `source-ledger.json`. The identifiability derivations, weights, zero rule and proposed fit/criteria above are original mathematical analysis/recommendations, not empirical conclusions borrowed from either paper.

## Handoff boundary

Parent/Runtime may use this method to freeze the separate TRAIN packet and analysis manifest before outputs. This review neither selects cases nor certifies a packet exists. Research should wait for the permitted Evaluation-owned text/target-free paired export rather than traverse private paths. No additional data/export access is requested or performed here. No M6/P4/E6 control, result interpretation freeze, model or artifact was changed.
