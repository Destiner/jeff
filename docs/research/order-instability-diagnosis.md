# R6: order instability is not one universal answer-letter preference

**Finding:** a shared mirror-position/letter component describes part of frozen Qwen's reversal behavior, especially three-option rules, but it is not a general explanation or a justified correction. The executed four-condition TRAIN diagnostic shows substantial **condition-dependent interactions**: changing letters alone and moving content while preserving its letter both change decisions. Neither residual identifies a particular reasoning mechanism.

**Decision:** do not treat E5's122/240 flips as a single global letter prior to subtract, and do not change M6/E6 or launch another correction/prompt search. Retain their predeclared both-order/family probability comparisons. R6's one diagnostic is **executed and complete**, not pending. No accuracy, calibrated-confidence, promotion or new learning claim follows.

## 1. Two separate evidence populations

| Evidence | Scope and actual work |
| --- | --- |
| Saved P3 NEW-v2 | Evaluation supplied **240 anonymous paired cases /480 vectors /1,840 probability values**: no text, targets, correctness, raw IDs, probes, D3 or final data. Six construction producers, two/family;170 declared groups,16 domains,40 rule policies/10 mechanisms. Existing development evidence, not a new untouched benchmark. |
| Frozen four-cell packet | **48 preselected TRAIN cases /192 presentations /740 probability values**,16/family,4inherited+6each of two new producers.48 declared groups/roots,12 explicit new-rule policy instances; unknown inherited policy IDs stay unknown. Selection used metadata/hash stratification before outcomes, not labels or known failures. K3/4/5/6 counts11/34/2/1; no K2. |

Research predeclared descriptives, one source-heldout antisymmetric fit and the four-cell contrasts before inspecting the public export or receiving new outputs. Evaluation's anonymous construction clusters are the broadest **recorded** source units, not independent teacher samples. Shared authors/renderers and correlated policies remain. The two populations must not be pooled into an accuracy or generalization score.

## 2. Saved reversal: rules are more slot/letter-stable than semantic-stable

No argmax ties or zero probabilities. Identity means the same supplied option; letter/slot means the same displayed position and its standard A–F symbol. Those last two are inseparable in ordinary P3 reversal.

| NEW-v2 family | Cases | Same option identity | Same letter/slot | Mean TV by identity | Mean TV by letter/slot |
| --- | ---: | ---: | ---: | ---: | ---: |
| Intent | 80 | 66 | 17 | .190781 | .767466 |
| Rules | 80 | **15** | **53** | .392720 | .267370 |
| Sentiment | 80 | 37 | 15 | .407972 | .687784 |
| All | 240 | 118 | 85 | .330491 | .574207 |

Thus rules exhibit a repeatable positional/symbol pattern, while intent is much more content-identity-stable. This does **not** show that rules ignore content: neither53/80 slot retention nor marginal slot frequencies identify why the model selected those positions. Events may overlap at an unmoved odd middle.

Concrete marginal signature: among23 three-option rule cases, original/reversed winner counts for slots A/B/C are **1/6/16 and2/5/16**. Among57 four-option rules they are **18/7/4/28 and18/2/8/29**. The similar end preference is descriptive, not a ground-truth ranking or causal token-prior estimate. Full transition matrices, per-slot probabilities and source/K summaries remain in the machine result.

### What reversal identifies

Under the working assumption `p[order,i] ∝ exp(u[i]+b[K,slot])`, with semantic utility u invariant to presentation, center `log(p_original[i]/p_reversed[i])` across options. The resulting y can identify only

`gamma[K,j] = b[K,j] − b[K,K−1−j]`.

Gamma is mirror-antisymmetric; an odd middle is zero under this model. It is **not** the complete bias vector (its antisymmetric part is gamma/2). Mirror-symmetric end-versus-middle preferences can be absorbed into u and are invisible to reversal. Changes in content/order utility also enter y. A good fit therefore supports a compact description, not a proven neural mechanism. Conditional probabilities cannot recover full-vocabulary allowed-answer mass.

### One frozen producer-heldout fit

One producer per family was assigned FIT and the other HOLDOUT using a predeclared metadata-only hash: **120/120 cases, three producers per side**. Domains/mechanisms and related cases remained with their producer. Within K, weights balance producers, broad domains/mechanisms within producer, then cases; option loss is divided by K. One shared gamma per K was fitted across FIT families, with no alternate split, per-family fit, epsilon or temperature. All cases had positive probabilities and passed the1e-6 sum tolerance without renormalization.

| K | FIT/HOLDOUT cases | Heldout log RMSE | Reduction in squared log residual vs gamma=0 | Modeled paired TV / unchanged-semantic TV |
| --- | ---: | ---: | ---: | ---: |
| 3 | 35/20 | 1.125938 | **78.2%** | .194357 / .415462 |
| 4 | 83/92 | 1.466827 | **11.5%** | .283012 / .303617 |
| 5 | 1/4 | 2.696967 | **−11.0%** | .243507 / .256219 |
| 6 | 1/4 | 2.414795 | **−46.3%** | .454945 / .443046 |

Modeled TV predicts each paired change from the other observed probability vector using the fitted contrast; it is **not a question-to-answer predictor or a corrected accuracy score**. Three-option relative improvement is substantial, but absolute residual remains nontrivial. Four-option transfer is mixed:

- Heldout rules: squared-residual reduction31.1%, TV.433717→.315059.
- Heldout sentiment: squared residual **worsens50.4%**, TV.381366→.430448.
- Heldout intent: log residual improves29.4%, but TV worsens.095769→.103530.

Rare K5/6 each have only **one fitting case** and show no convincing transfer. The recorded equal-K macro gives each rare K25% weight and must not replace these support-qualified results. No p-values, independent-source guarantee or post-outcome success threshold is asserted.

## 3. Actual four-cell diagnostic: letter assignment changes the order response

[The frozen packet](order-diagnostic-packet.md) crossed text order O with ascending/descending letter assignment L. Let j be an option's original index and r(j)=K−1−j:

| Cell | Option position | Its actual letter index |
| --- | --- | --- |
| O0L0 | j | j |
| O0L1 | j | r(j) |
| O1L0 | r(j) | r(j) |
| O1L1 | r(j) | j |

Runtime executed the **unchanged frozen P3 model**, not M6, under Model's single-use grant after M6/P4 completed. Exactly192 attempted/completed/written forwards, no discarded startup or retry. Token audit:95–199tokens, cap1024, no truncation. External audit+predict wall **13.867752s**; prediction-process wall12.979705s. CPU lifetime RSS3.36GB and observed MPS-driver maximum2.77GB are overlapping/nonadditive measures, not a unified-memory peak. See [Runtime's executed report](../runtime/r6-order-diagnostic.md).

The same48 cases appear in every comparison below. TV averages use equal source weight, then domain/mechanism, then case; integer retention counts are unweighted. Each pair has48 unique argmax comparisons.

| Contrast | Same semantic choice, raw | Source-balanced semantic retention | Source-balanced semantic TV |
| --- | ---: | ---: | ---: |
| Change letters, original order:00↔01 | 20/48 | 42.6% | .423244 |
| Change letters, reversed order:11↔10 | 22/48 | 45.4% | .402534 |
| Move content, preserve its letter:00↔11 | 22/48 | 47.2% | .411236 |
| Move content, preserve its letter:01↔10 | 19/48 | 40.7% | .436849 |
| Reverse with standard letters:00↔10 | **30/48** | **63.9%** | **.263245** |
| Reverse with descending letters:01↔11 | **9/48** | **20.4%** | **.599693** |

Under descending letters, actual-letter/slot choice is retained in **38/48**, versus12/48 under standard letters (source-balanced76.9% versus23.1%). The very different responses rule out an exact invariant-content-only or single pure fixed-letter/slot-only account of all four conditions. They do not separate alphabet-sequence familiarity, symbol binding, context or internal reasoning.

For condition-centered log probabilities x aligned by semantic identity, the predeclared contrasts are:

- `alpha=((x00−x01)+(x11−x10))/2`: label-assignment-associated.
- `beta=((x00−x11)+(x01−x10))/2`: position/**order**-associated.
- `R=x00−x01+x10−x11`: zero under the invariant-content additive model.

Source-balanced RMS(alpha/beta/R) is **1.363607 /1.793570 /3.307742 natural-log units**. R is a differently scaled four-term contrast, **not** an explained-variance fraction or comparable fitted residual. Its family RMS is4.931440 intent,2.401221 sentiment,1.654847 rules; no family was dropped. Nonzero mirror-symmetric and odd-middle contrasts also violate the exact additive restrictions. K6 has one case: its mechanically zero across-case SD is not homogeneity evidence.

### Allowed-token mass was high, not inferred

The diagnostic saved actual allowed-letter full-vocabulary mass. Source-balanced means range **.998682–.999052** across cells; condition medians are.999740–.999805, overall minimum.958810. Instability therefore coexists with high allowed-token mass **in this TRAIN packet**. This does not establish accuracy, calibration or free-generation validity, and cannot retrospectively supply the missing mass for E5. Low mass, had it occurred, would not alone invalidate a conditional classifier.

## 4. What changes—and what does not

**Changed understanding:** there is a transferable mirror preference in some strata, especially K3, but the globally shared account fails important strata. Separate letter-assignment manipulation exposes substantial interactions that ordinary reversal cannot identify. A universal “remove the letter bias” remedy is not supported.

**Unchanged execution:** M6 already uses training-only option permutations; R6 neither amends that recipe nor replaces E6's evaluation criteria. Do not infer that arbitrary descending-letter augmentation would help merely because it exposes weakness. No further experiment, corrective predictor, temperature fit or default promotion is proposed by this delivery.

Remaining unknowns include complete symmetric biases, pure token versus position effects, general label×position interactions, why descending lettering changes behavior, accuracy of any putative correction, and transfer beyond these authored sources. Position changes alter surrounding content order; letter changes alter alphabet naturalness. No residual proves a particular reasoning failure.

## 5. Sources, reproduction and verification

Two focused primary sources, not another survey:

- [Zheng et al., ICLR2024](https://arxiv.org/html/2309.03882), §§2.4,3.1–3.2: IDs and positions are naturally bound; shuffled IDs affect prompt naturalness; prior/content decomposition needs invariance assumptions. Their cyclic permutations cover more pairings than our mirror reversal. We did not adopt PriDe correction or its evaluation-data procedure.
- [Robinson et al., ICLR2023](https://arxiv.org/html/2210.12353), §§3–4: symbol binding is model-dependent, and order consistency is independent of task correctness. Our two/four-cell measures are not their exhaustive-permutation PPA.

Evidence root: `/Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/`:

- `analysis-predeclaration-v1.md`, `method/{findings.md,source-ledger.json}`; primary predeclaration supersedes optional method suggestions.
- Public export `artifacts/evaluation/r6-new-v2-probabilities-v1/public/paired.jsonl` SHA256 `ca9d0f47401b753be87ef9c12648c771ef62783d1f8e646af89e1b55404f792d`; no private mapping followed.
- Canonical saved-output reproduction: `saved-analysis-py312-final/{input-binding.json,results.json,report.md}`. [`analyze_order_bias.py`](../../experiments/research/analyze_order_bias.py) supports `bind` then `analyze`, explicit `--task-root` and new `--output-dir`. Original subagent usedPython3.9.6; projectPython3.12 reproduction yields **exactly equal scientific result objects**. Original artifacts remain; no method/split change.
- Runtime output `artifacts/release/r6-order-20261111-01/run/predictions.jsonl` SHA256 `c9068e41915629f9419066941124c74fd7f181e93c840ca05e807d9e0056494d`. Canonical four-cell reproduction: `four-cell-reproduction/{input-receipt.json,results.json,report.md}` via [`analyze_four_cell.py`](../../experiments/research/analyze_four_cell.py), explicit `--task-root`, `--runtime-root`, new `--output-dir`. All scientific objects exactly match the initial completed analysis.
- **Analysis failure/provenance limit:** the first four-cell analyzer attempt stopped before metrics on semantic-order versus display-order binding. Its standalone initial input receipt was overwritten with an embedded previous-attempt summary; original failed-script bytes are not retained. This was not fully immutable failure preservation. The final tracked analyzer refuses any existing output directory; the correction/hardening did not alter the estimator or require another model pass. Producing and hardened/reproducing script hashes remain separately recorded.
- `packet-review.md`, `analysis-review.md`, `four-cell-review.md`: source/packet checks and independent actual-data arithmetic. Saved key metrics agree within8.88e-16; four-cell key metrics within4.44e-16. Reviews are not claims of complete semantic correctness or exhaustive runtime verification.

Research used stdlib analysis/preparation, source review and package builds only: no model load, new labels, training, dependency, tests/lint, paid work or protected-final access. Runtime alone performed the authorized model pass and returned its slot; all Research subagents finished. Package builds establish integration, not scientific validity. Exact commits, actual coverage and bounded availability are recorded in the delivery handoff.
