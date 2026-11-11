# 03 — Data, scoring and evaluation validity

Independent Fable review, prompt `review/prompts/03-data-evaluation.md`.

## 1. Scope and verdict

**Identity.** Checkout HEAD `ac4f744d62573db364bf493e522d89b0beb47217`. Tag `fable-review-20261111-v1` resolves to `65e8429d68bd0542eac145758d707e149034fd62`; HEAD is that commit plus one post-tag commit whose only change is `review/reports/01-framing.md`, which I did not open. Code base `91e09919bdf3b38370bf18c7bee0f6a2bbb26871`; cutoff `2026-11-11T16:53:50Z`. `review/resolve_path.py --verify`: 912 files, 97,901,520 bytes, no failures. No user-supplied hash was given to check. No model loads, tests, lint, installs or uploads; CPU arithmetic on copied artifacts only, with scratch files outside the checkout.

**Recomputed from raw artifacts (all matched the reports exactly):**
- v2 manifest: 18 shard hashes, 1,500/300 rows, 880/182 groups, zero cross-split group overlap, label-basis totals.
- An independent scorer written from the contract, not importing `src/jeff/evaluation`: agreement, NLL, Brier, ties, flips and both-order counts for the four M4 snapshots, frozen Qwen (P3) and M6 (P4) on inherited-60, new-240 (both orders) and probes; D3 for the four M4 snapshots; the lexical baseline (99/240).
- Reversal mapping: 300/300 v2 pairs and 12/12 probe pairs are exact reversals with identical option IDs, text and target.
- M6 TRAIN fit 805→431/1,500 and CE 1.357724→1.390592, from `fit-before.jsonl` / `fit-after.jsonl`.

**New analysis (mine, not in the packet):** domain/mechanism-cluster bootstrap intervals; within-family reliability; a train↔development lexical scan; the M6 probability-vector structure; text-level rule-label checks and a blind sentiment/probe label check.

**Trusted, not recomputed:** tokenisation and prompt rendering, weight identity, M2/M3/M5 scores, predeclaration timing, internals of the same-alias reviews.

**Terms.** NLL/CE is log loss: lower is better, and a uniform guess over k options scores ln k. ECE is the gap between stated confidence and observed agreement. Arity is the number of options. Trigram-Jaccard is the share of three-word sequences two texts have in common.

**Bottom line.** The data and evaluation machinery is sound: clean splits, exact arithmetic, honest denominators, labels that survive independent checking. The weakness is in what the numbers are taken to mean:

1. The pooled and probe headlines are dominated by a lexically solvable family and by a 12-group reused set.
2. No model is distinguishable from chance on rules in new-v2, D3 or inherited validation.
3. Model-versus-model contrasts are mostly inside cluster noise.
4. M6 is a *content-blind constant predictor*, a stronger and simpler fact than the reports state.
5. There is no untouched set large enough to confirm anything.

## 2. Findings

### F1. M6's final checkpoint ignores its input: output depends only on option count

*Category: evidence-qualified concern — the reports understate a fact that is recomputed on development vectors and strongly inferred on TRAIN. Confidence: high. Impact: high for diagnosis and for how E6/E7 are read.*

Evidence: `review/evidence/release/p4-m6-20261111-01/run/{v2-original,v2-reversed,probes-paired}.jsonl`, field `probabilities`.

- Every one of the 2,390 saved probabilities lies within 0.0027 of its arity×position mean.

| Options | Position vector (mean) | Largest per-position SD |
|---|---|---|
| 3 | .551 / .206 / .244 | .0015 |
| 4 | .406 / .152 / .180 / .262 | .0010 |

- Position-aligned total variation between a case and its reversal: mean 0.0002, max 0.0007. Frozen P3 on the same pairs: mean 0.585.
- `review/evidence/model/m6-qwen-20261111-01/training/fit-after.jsonl`: for all 1,500 rows, exp(−`ce`) matches that same vector at (arity, `target_position`) within 0.004. The training process's own fit pass and Runtime's separate reload agree, so this is a property of the weights, not a reload or scoring artifact.

Consequences:
- E6's "position-0 top-choice collapse, not flat" understates it. The per-family NLL "improvements" and the new-reversed NLL exception are the cross-entropy of a fixed vector against the target-position distribution, not partial learning.
- The "140 certified strict winners / 1,360 unresolved ties" caveat is in practice closed: the vector's top-two margin is ≥0.10 at every arity.
- No development population carries information about this checkpoint beyond "collapsed". This one statistic says what E6's 158 output files and 24,797 arithmetic checks say.
- The collapse was visible in TRAIN telemetry alone. In `training/online.jsonl`, intent rows with p(target)>0.5 fall from 87% before training to 39% in updates 1–25 and to 0% by update ~176. Rows with pre-training CE near 0 are at CE 1–2 by updates 5–8.

Counterevidence: full TRAIN vectors were not saved, and two (arity, position) cells are unobserved in TRAIN. Falsifier: M7's saved vectors, or any re-inference of M6, showing within-arity SD well above 0.003.

This says nothing about cause. Early-step damage is consistent with the step-size hypothesis M7 tests, but does not establish it.

### F2. No predictor is above chance on rules in any population large enough to tell; the headlines are family mixture

*Category: evidence-qualified concern. Confidence: high on the arithmetic, moderate on the intervals. Impact: high.*

New-v2, original order, correct of 80 per family. Expected uniform-random accuracy is 22.0 / 20.0 / 21.9.

| Predictor | Intent | Sentiment | Rules | Rules minus chance (mechanism-cluster 95%) |
|---|---|---|---|---|
| Lexical overlap, no training | 63 | 19 | 17 | — |
| MS MARCO pretrained start | 66 | 18 | 15 | −6.9 [−11.9, −1.2] |
| M4 MiniLM trained | 74 | 43 | 15 | −6.9 [−13.0, −0.6] |
| M4 MS MARCO trained | 77 | 43 | 21 | −0.9 [−10.7, +9.6] |
| Qwen frozen | 74 | 30 | 25 | +3.1 [−4.3, +11.3] |

Other rule populations agree:
- D3: 26–31/96 against chance 25.9; all four policy-cluster intervals include zero; no NLL beats uniform by more than 0.001.
- Inherited rules: 4–7/20 against chance 5.1.
- The one descriptive exception is frozen Qwen on probes: 3 of 4 rule groups correct in both orders. Four simple groups cannot carry a claim.

So "55%" and "58.75%" are roughly intent near ceiling, sentiment at 54%, and rules at chance. Intent is 75–80% solvable by token overlap in both TRAIN and validation. E5's "some new-rule ranking signal" (25/80) is inside chance noise.

Model-versus-model contrasts, percentile bootstrap over 8 domains per family and 10 mechanisms:

| Contrast on new-v2 | Difference | Approx. 95% interval |
|---|---|---|
| MS MARCO − MiniLM, all 240 | +9 | [−12, +30] |
| Qwen − MS MARCO, all 240 | −12 | [−27, +3] |
| Qwen − either encoder, sentiment | −13 | [−22, −4] and [−24, −2] |
| Trained − own start, all 240 | +66 / +42 | clearly positive |

Probes: Qwen 9/12 groups correct in both orders against 5–8/12 for the encoder systems; exact sign tests on discordant groups, for the three encoder snapshots I recomputed, give p = 0.22–0.69. The decoder's development-set case therefore rests on 12 reused groups. On 240 new rows it is not better than the encoders, and it is distinguishably worse on sentiment.

Aggregate reliability also hides family structure. MiniLM's overall ECE of .046 coexists with rules at mean confidence .31 against accuracy .19. Frozen Qwen is overconfident: sentiment .72 against .375, rules .60 against .31.

Counterevidence: the reports already hedge most of these statements and promote nothing. With so few clusters the intervals are, if anything, too narrow; I would not read the two rule intervals just below zero as real below-chance behaviour. Falsifier: seed replicates or a larger set showing these gaps are stable.

### F3. The ladder has no bottom rung, so "failed to transfer" cannot be told from "never fit"

*Category: hypothesis, with a direct falsifier. Confidence: moderate. Impact: high for D6 and any rule-data work.*

- `docs/model/m4-v2-run.json`, `runs.*.training.epoch_history`: final-epoch online TRAIN loss is 0.8315 (MiniLM) and 0.8536 (MS MARCO). New-v2 validation NLL is 0.823 and 0.917. The earlier v1-trained encoder runs (M2, M3, M5) all end at 0.848–0.849, against inherited validation NLL of 0.79–0.86.
- A near-zero train/validation gap, far from both zero and uniform (1.32), means under-fitting. It is consistent with intent fitted, sentiment half-fitted and rules at ln k *on TRAIN itself*.
- Per-family TRAIN fit was never saved for the encoders.
- Every rule development population is lexically disjoint from TRAIN renderings. My scan gives D3→TRAIN state trigram-Jaccard max 0.11, median 0.00; new-v2 rules max 0.02. TRAIN rule groups, by contrast, are template clusters of 10–20 rows per mechanism.

So D3's null cannot separate "mechanism not learned" from "learned but bound to one renderer". D6's design for at most 96 new TRAIN rule rows presumes a supervision gap that has not been shown to be the binding constraint.

Counterevidence: online loss is a changing-weight average with dropout, so the true final fit is somewhat lower. Falsifier: per-family TRAIN CE on the existing M4 checkpoints. If rules sit well below ln k there, this hypothesis is wrong and the question becomes transfer.

### F4. Labels are not the bottleneck, but only independent checks can show that

*Category: no defect found in the samples checked (scoped), plus evidence-qualified concern on what the data can support. Confidence: high for those samples.*

Existing reviews (48/48, 140/140, 64/64, 24/24) all use reviewer alias `gpt-sol` against a `gpt-sol` author, on deterministic or purposive samples. The rule "recompute" reuses the author's solver: `review/evidence/data/data-pilot-v2/review-rules/recompute.json`, field `method`, says "Reused same-author solver". They bound self-consistency, not error.

My checks, from a different model family, working only from the rendered text. Rule answers were recomputed from the prose (targets were visible during the hand checks). Sentiment and probe judgements were fixed before I looked at targets.

| Population | Method | Agreement |
|---|---|---|
| New-v2 rule validation (census) | Parsers I wrote from the prose for all 10 mechanisms | 80/80 |
| Inherited rule validation (census) | By hand | 20/20 |
| D3 (3 per mechanism) | By hand | 24/24 |
| TRAIN rules (1 per mechanism) | By hand | 30/30 |
| New-v2 sentiment validation (every second row: 15 neutral, 14 positive, 6 mixed, 5 negative) | Blind judgement | 40/40 |
| Probes (12 groups) | Blind judgement | 12/12 |

Label noise is therefore an unlikely explanation for any failure, and sentiment headroom is real: a careful reader scores about 100%, the trained encoders 54%.

What the data cannot support:
- **Graded confidence.** Every item is unambiguous by construction, so the ideal output is one-hot. NLL and Brier measure sharpness when right and overconfidence when wrong. Nothing here tests probabilities on genuinely uncertain decisions.
- **Arbitrary choice text, for sentiment.** Sentiment is a closed four-class task with 40 option phrasings in the new data; 320/320 new validation option texts occur verbatim in TRAIN. All 80 intent validation questions are also verbatim in TRAIN.
- **880 independent sources.** The count is 800 singletons in 80 domains, 50 four-row v1 scenario groups, and 30 rule mechanisms holding 500 rows: roughly 160 domain or mechanism clusters.

### F5. Splits are clean, but development evidence is adaptively used and there is nothing left to confirm with

*Category: evidence-qualified concern. Confidence: high. Impact: high at the deadline.*

Clean: zero group overlap. My scan finds no near-duplicate between TRAIN and any development population (max state trigram-Jaccard 0.19, medians ≤0.03).

Adaptive use:
- The 12 probe groups have been scored for about ten systems. Three are named in M5's success criterion (`configs/evaluation/e4-m5-criterion-v1.json`, `criteria.recovery.eligible_groups`); they also sit in the E3 gate and motivate the E5 decoder recommendation.
- New-v2 intent choice sets were rewritten after shortcut diagnostics computed on the validation rows themselves.
- E7 reuses the same 624 presentations (`review/evidence/handoffs/lead/wave-20261111-1635/evaluation-E7.md`).

The sealed final set is 24 rows, six per family (`docs/evaluation/final-design.md`; `manifests/evaluation/final-v1.json`, `rows: 24`). Six rows cannot distinguish 2/6 from 5/6 (Fisher exact p = 0.24).

Counterevidence: nothing has been promoted, so selection bias so far is small. This is a capacity problem, not contamination.

Controlled versus not:

| Comparison | Status |
|---|---|
| M5 vs M3 | Controlled as reported: one change, byte-identical start predictions |
| M6 start vs P3 | Controlled as reported: byte-identical |
| Trained vs own start (M4, D3, M6) | Controlled as a recipe contrast |
| M7 as planned | Controlled: learning rate only |
| M4 vs M2/M3 | Not controlled: data mixture and update count both change |
| MiniLM vs MS MARCO | Not controlled: pretraining and head initialisation differ |
| Qwen vs encoders | Not controlled: practical comparison only |
| D3 "seen mechanism" | Confounded with new authorship and prose (F3) |

Every result is one seed.

## 3. Next actions

**A1. Fit-and-sensitivity preflight before any development scoring.** Owner: Model, with Evaluation reading the output.
- Change: (a) deterministic per-family TRAIN fit with full vectors on the existing M4 MiniLM and MS MARCO checkpoints; (b) for M7 or any later run, a collapse sentinel: within-arity SD of per-position probability. If M7 has already run, compute it from its saved TRAIN vectors before reading E7. A no-cost version exists in today's logs: online CE on intent rows against the same rows in `fit-before.jsonl`. M6 would have tripped it within about ten updates.
- Held fixed: checkpoints, schedule, prompt, data.
- Cost: inference only on 1,500 rows. Estimated under a minute per encoder, from the measured 2–3 s per 96-row D3 pass. The sentinel is arithmetic on outputs already saved.
- Outcomes: encoder TRAIN rule CE near ln k → stop D3-style diagnostics and D6 rule authoring until some model fits TRAIN rules. Good TRAIN fit with chance D3 → add a same-template, new-parameter rung. M7 sentinel SD below ~0.01 → skip P5/E7 and save a development look.

**A2. Re-declare how E7 is read, before outcomes.** Owner: Evaluation. Zero model compute, roughly an hour.
- Change: per-family reporting against chance and the lexical baseline, with cluster intervals; state minimum detectable differences (roughly ±10–17 rows for sentiment and rules); rules reported as "versus chance" only; probes demoted to a regression sentinel and removed from success criteria.
- M7 success reads as: not collapsed, and intent and sentiment not below P3 outside noise in both orders.
- Add two extra seeds of M4 MiniLM (measured 74 s training each; needs a Model slot) as a noise floor.
- Outcome: if seed spread on new-v2 is ±9 rows or more, close encoder-versus-encoder and M5-type contrasts as unresolvable at this size.

**A3. Freeze a larger untouched confirmation set now.** Owner: Data and Evaluation; needs user authorisation.
- Change: at least 240 rows from new domains and mechanisms, plus a trained-template/new-parameter rule stratum. Authors do not see development failure analyses. Labels get a cross-family blind pass and text-level scripted rule checks, as in F4. Never trained on; one reporting pass.
- Cost: estimated 1–2 agent-hours, £0, no model compute.
- Outcome: without it, the submission must call every result development evidence. With it, one clean per-family claim is possible.

## 4. Preserve / stop

**Preserve:** hashed immutable manifests and the stratum separation; the coverage-aware scorer and exact reversal pairs; predeclared criteria (E4, E6); kept negative results; the honest `label_basis` language.

**Stop:**
- Pooled 240-row and 24-presentation probe headlines.
- Describing within-chance rule counts as "signal".
- Using probes in success criteria.
- Aggregate ECE without the per-family view.
- Exhaustive per-unit breakdowns of collapsed checkpoints.
- New rule data or diagnostics before per-family TRAIN fit is known.

## 5. Unknowns

- Per-family TRAIN fit of the encoder checkpoints (decides F3).
- Seed and backend variance; nothing has been replicated.
- What the output probabilities are for. No item in any population has a non-degenerate correct distribution, so "reliable confidence" is currently untestable, not merely untested.
- Allowed-token mass on development inputs for Qwen; it was measured on 48 TRAIN cases only.
- Label quality and usefulness of the 24-row sealed final set (not included, correctly).
- User decision: whether a held-out claim is wanted at the deadline. If so, A3 has to start before further tuning.
