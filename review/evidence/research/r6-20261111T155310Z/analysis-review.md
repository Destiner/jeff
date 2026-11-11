# Independent R6 saved-output results review

## Verdict

**No numerical or estimator-implementation error found in the reviewed key metrics.** The headline is fair **as a descriptive, source-heldout account of paired frozen-P3 output changes**, with two qualifications: “one fixed bias” means **one shared mirror-contrast vector per K**, not one vector across K; and rare K=5/6 show **no convincing transfer**, rather than weak affirmative evidence. Their heldout centered-log SSE worsens versus zero, and K=6 TV also worsens. K=4 transfer is modest in aggregate and heterogeneous: heldout sentiment fails both comparisons, and heldout intent improves log fidelity but slightly worsens TV.

Recommended wording:

> A single source-fitted mirror-antisymmetric contrast per option count describes heldout K=3 reversal changes strongly and K=4 changes modestly in aggregate, but fails on the heldout sentiment source. Rare K=5/6 have only one fitting case each and show no convincing transfer. This is descriptive fidelity of paired conditional probabilities, not a pure causal bias estimate, task-accuracy improvement, calibration result, or deployed correction.

## Scope and independent execution

Read repository `AGENTS.md`, coordination/plan/contracts/swarm, and the requested R6 predeclaration, supporting `method/findings.md`, saved script, binding, results and report. Evaluation input access was confined to **`artifacts/evaluation/r6-new-v2-probabilities-v1/public/{paired.jsonl,README.md,receipt.json,delivery.json}`**. No private/raw case, probe, D3, final, identity mapping, model, tokenizer or weight paths were opened or followed. Upstream provenance hashes were treated as receipt assertions, not invitations to inspect upstream files.

Performed a synchronous, independently written inline **stdlib-only actual-data re-evaluation** using `python3 -B` (Python **3.9.6**). Did not import or execute the saved analysis script. Independently derived the frozen split, verified metadata membership, rebuilt hierarchical weights and gamma, and recalculated full-population retention/TV and per-K/per-source heldout RMSE, MAE, SSE reduction, symmetric-energy fraction and bidirectional TV. Largest absolute difference from saved gamma/key metrics was **8.881784197001252e-16**. This is independent implementation agreement on the same runtime family, **not** the parent's separate Python 3.12 reproduction; that directory was not reviewed.

Only this new review file was written. No existing artifacts or tracked files changed; no dependencies, ML, inference, training, tests, lint, builds, alternate fits, split selection, epsilon, temperature or correction were run. All commands finished synchronously; **no jobs remain**.

## Identification and implementation

For invariant per-case semantic utility under the working additive model, centering `log(p_orig)-log(p_rev)` removes the softmax normalizer difference and identifies `gamma[j]=b[j]-b[K-1-j]`. The constrained weighted least-squares estimate is the weighted mean of `(y[j]-y[mirror])/2`. The saved implementation computes exactly this, imposes opposite mirror entries and zero odd middle, and **does not remove the observed symmetric component before scoring**. The antisymmetric part of b is gamma/2, not gamma; complete b is not recovered.

Semantic option identity alignment and one-based position reversal are correct. Reverse predictions use original-identity probabilities multiplied by `exp(-gamma)` and renormalized; the opposite direction uses `+gamma`. Signs and bidirectional averaging are correct. The fixed-slot comparator mirrors semantic indices, whereas semantic-copy leaves option identities unchanged. Observed probabilities are not silently normalized. Only model-generated softmax predictions normalize, as specified.

Standard answer letters remain confounded with display position and repeatable rendering effects. Presentation-dependent semantic/order responses can enter y. Neither reversal nor good fidelity proves static token priors, content neglect or a causal neural mechanism. Conditional allowed-symbol probabilities do not identify full-vocabulary answer mass or calibrated correctness. The saved report respects these boundaries. The TRAIN four-cell diagnostic was not executed in these artifacts and supplies no empirical evidence here; its formulas were reviewed mathematically only.

## Source partition, freeze and weighting

- Public metadata has six producer/construction units, two per family, with construction_cluster equal to producer. Every observed source_group/domain/policy_instance/mechanism nests within one producer; no released related unit crosses the partition. These are the broadest **recorded** units, not guaranteed independent sources or teachers.
- Recomputed the exact predeclared SHA256 ordering using `R6/source-split/v1\n<family>\n<producer>`: first of two sources per family FIT, other HOLDOUT. It agrees with the binding, as does every saved case-metadata field. Each side has 120 cases. FIT producers are `b817637a…` (rules), `cd5a16c8…` (intent), `f9a95b74…` (sentiment); HOLDOUT producers are `2130e39a…`, `96cbb91d…`, `3f9deab4…`, respectively. Cross-family source-merging logic is not needed for this actual export because each producer belongs to exactly one family.
- Per K, weights give equal total mass to each represented producer, equal mass to its represented broad domain/mechanism groups, then equal rows within each group, with option loss divided by K. Per-source summaries rebalance groups within that source. This correctly implements the declared balanced-source estimand, **not row prevalence**. Quantiles are explicitly unweighted descriptives; equal-K macro averages per-K metrics, not pooled RMSE or pooled SSE reduction.
- All seven input byte hashes in the binding match current permitted inputs, predeclaration, method and script. Binding SHA256 is `1f3af31c73cb91df902131d1585c1387bf242e4448ac1bf19d7dbec903b7208d`; script SHA256 is `0d3b1bf6c0a9aadeb89f4aa1cbb045d04a94c3a06d372b4fee805305e4d99146`. Binding timestamp is **16:19:37.126001 UTC**, before analysis **16:19:42.851116 UTC**. The script separates metadata binding from probability computations and refuses overwrite/rerun in place.
- Freeze evidence supports the recorded sequence and unchanged artifacts; hashes/read-only files alone cannot independently prove nobody previously inspected probabilities. The primary predeclaration describes prospective analysis of existing outputs, not an untouched model experiment. Its approximately 16:06 predeclaration time postdates export creation at 16:04 but precedes delivered-at 16:07; creation is not proof of Research access. No stronger chronology claim is independently certified here.
- Supporting method recommendations differ (roughly one-third holdout, epsilon sensitivity, possible second diagnostic fit). The primary predeclaration and binding explicitly supersede them with half-source holdout, no epsilon and no second learned diagnostic model. The implementation follows that declared precedence; these are not hidden outcome-dependent deviations in the reviewed artifacts.

## Verified population arithmetic

240 complete pairs / 480 vectors / 920 semantic option identities / 1,840 probability entries; 80 pairs per family. No exact zero or one probabilities, no log exclusions, no unsupported heldout K, and no argmax ties. Maximum probability-sum error is **1.341104507446289e-07**, within 1e-6; 470/480 vectors have nonzero floating-point sum error. Receipt, report and independent evaluation agree.

| K | All pairs | Identity retained | Displayed letter/slot retained |
|---|---:|---:|---:|
| 3 | 55 | 28 | 36 |
| 4 | 175 | 82 | 49 |
| 5 | 5 | 4 | 0 |
| 6 | 5 | 4 | 0 |

Overall identity retention is **118/240 = 49.1667%** (122 flips); slot retention **85/240 = 35.4167%**. Odd-middle retention can belong to both coordinate systems; these are not disjoint categories. Mean raw aligned TV is **0.33049127639754755** by option identity versus **0.5742068356288068** by displayed slot. Greater identity-space stability does not establish task ability.

## Verified heldout headline metrics

Values below independently reproduce saved results to rounding. SSE reduction is against centered-log gamma=0; TV comparator is unchanged semantic probabilities.

| K | FIT / HOLDOUT cases | RMSE | MAE | SSE reduction | Symmetric energy fraction | TV model | TV semantic copy |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3 | 35 / 20 | 1.125938 | 0.902020 | 0.782182 | 0.048691 | 0.194357 | 0.415462 |
| 4 | 83 / 92 | 1.466827 | 1.077667 | 0.115156 | 0.139791 | 0.283012 | 0.303617 |
| 5 | 1 / 4 | 2.696967 | 1.914028 | -0.110429 | 0.493822 | 0.243507 | 0.256219 |
| 6 | 1 / 4 | 2.414795 | 1.729087 | -0.462677 | 0.374552 | 0.454945 | 0.443046 |

K=3 explains **78.2182%** of the declared heldout centered-log energy and reduces TV by about **53.22%**; both heldout rules and intent show strong relative improvement. Absolute residual RMSE remains nontrivial, so “strong” is relative fidelity improvement, not near-perfect fit.

K=4 explains **11.5156%** in aggregate and reduces TV about **6.79%**. Per-source qualifications are consequential:

| Heldout family, K=4 | Cases | SSE reduction | TV model | TV semantic copy |
|---|---:|---:|---:|---:|
| Rules | 32 | 0.310835 | 0.315059 | 0.433717 |
| Sentiment | 40 | **-0.503862** | **0.430448** | **0.381366** |
| Intent | 20 | 0.293698 | **0.103530** | **0.095769** |

Thus sentiment's modeled SSE is about **1.503862×** its zero-baseline SSE; its TV worsens too. Intent's K=4 log improvement does not imply probability-space improvement. K=5 has a small TV improvement despite worse log SSE; K=6 worsens both. Each rare-K fit rests on **one case from one producer and one broad group**, evaluated on four cases from one heldout intent producer. Equal-K macro gives each rare K 25% weight; it must not replace these support-qualified results with a broad success claim.

## Errors, limitations and disposition

**Numerical errors found: none in independently recalculated key metrics or rounded headline tables. Method implementation errors found: none material for these actual inputs.** The saved report discloses Python 3.9.6 rather than the project's requested 3.12; this is a reproducibility/process qualification, not evidence of wrong arithmetic. The parent's separately scoped unchanged-method 3.12 reproduction remains separate work.

This review did not independently reproduce every transition-matrix cell, every available-unit descriptive, signed residual, or RMS quantile; their alignment/weighting/quantile implementation was inspected. Public receipt claims of exact upstream probability preservation and original model provenance were not independently re-audited against prohibited upstream paths. No accuracy, pure causal, IID generalization, significance, calibration or training-intervention conclusion is justified. Within this precise scope, the restrained conclusions are supported and require no artifact rewrite or new method.
