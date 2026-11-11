# 01 — Problem framing and feasibility

Independent, read-only review of the frozen Jeff snapshot. Prompt 01 (`review/prompts/01-framing.md`).

## 1. Scope and verdict

**Identity, verified**

- Review commit (detached HEAD): `65e8429d68bd0542eac145758d707e149034fd62`. The annotated tag `fable-review-20261111-v1` resolves to it. Its parent is the code base `91e09919bdf3b38370bf18c7bee0f6a2bbb26871`, matching `review/source-code-commit.txt` and `review/manifest.json`. No user-supplied hash was given to check.
- Evidence cutoff `2026-11-11T16:53:50Z`. `review/resolve_path.py --verify` passed: 912 files, 97,901,520 bytes, no failures.
- Outside `review/`, the packaging commit changes two lines of `README.md` and nothing else.

**Read.** Stage 1: protocol, review README, `brief.md`, `AGENTS.md`. Stage 2: plan, observations, evidence map, contracts; E3, both E4 tracks, E5, E6, P3; M4 and M6 plans and results; R1, R5, the head of R6, D4, D5; final design and probes; the 16:35 authorization wave; model and training source at HEAD and at the executed revisions `812a655` (M4) and `dafd5d2` (M6). Not read: prompts 02–05, other reviews (none existed), coordination state.

**Recomputed here** (CPU, standard library, retained artifacts; Appendix B): new-v2 agreement and loss by family for six predictors, matching E3/E5/E6; sentiment confusion by class; group-bootstrap intervals; confidence versus correctness; per-family training loss for M4 from a replay of its batch order; M6 output vectors by option count and position; M6 loss in the first updates. **Taken on trust:** label correctness, hash and binding audits, timings, memory samples, R6's fits.

**Verdict**

The interface is sound and the day-one milestone is met. What the snapshot lacks is any test of the mission's central claim, that learning transfers across task families.

Learning has not yet been achieved on two of the three families, so transfer could not be tested. The encoders were stopped after about 75 seconds. At that point their loss on the sentiment training rows had only just left chance and was still falling, and their loss on the rule training rows had not moved. The one decoder run turned the model into a constant that ignores its input, starting with the first update. Neither result shows that a small model cannot do this. Both show that the recipes have not been made to work.

Resources are not the limit. The eight recorded learning runs used 17 minutes of training in the 6.6 hours after the first commit, and £0 of the £50 ceiling. Runs are authorized one at a time, with no retry.

The benchmark could not confirm transfer even if it happened. Development has no unseen family. The sealed final has 24 rows, six of them for the one unseen family.

One gain is resolved: trained MS MARCO beats its own pretrained start on new-v2 by 17.5 points (group-bootstrap 95% interval 10.9 to 24.5). Trained-encoder confidence also ranks its own errors well on in-distribution rows.

## 2. Stage 1 judgments, revised

The Stage 1 memo is Appendix A, frozen before I read any plan, result or diagnosis.

| Stage 1 judgment | Status | Evidence that decided it |
|---|---|---|
| The interface is useful; "arbitrary options" names a domain, not a learning target; a softmax over options is relative to the option set | Retained | `src/jeff/model/scorer.py:161-178` scores each option alone; P3 probabilities are conditional on the allowed letters; `docs/plan.md` says accepting arbitrary text proves nothing |
| P1. Compute is not binding; data diversity is; fitting seen templates will be easy | Half wrong | Compute is idle (1,031 s of training, £0). Fitting was not easy (findings 1, 2). The binding limit is fit and run count, ahead of data diversity |
| P2. Self-authored benchmark, few independent clusters, no external anchor | Retained, sharper | Finding 3 |
| P3. Headline will be trained versus own start; a strong cheap baseline will be missing | Mostly withdrawn | E3 and E5 include lexical, a pretrained-head start and a frozen 0.5B model, and flag the random head as weak. Remaining gaps: the frozen decoder was scored through one letter readout that R6 shows is order-unstable, and no surface model was trained on TRAIN |
| P4. Probabilities normalized; reliability in-distribution at best | Retained, with a positive | Finding 5 |
| P5. The objective rewards template fit | Revised | Cross-entropy over the supplied options suits the interface. The narrowness is in what was learned (finding 3), and "template fit" is premature while the templates are not yet fit (finding 1) |
| P6. Process cost is material | Retained | Eight runs in 6.6 hours; M7 is again "exactly ONE" attempt (`review/evidence/handoffs/lead/wave-20261111-1635/model-M7.md`) |

## 3. Findings

Terms: cross-entropy (CE) is the loss, lower is better; a uniform guess over four options scores 1.39. "Fit" is how well a model does on the rows it was trained on.

### 1. Encoder training stopped before two of three families were fit, so transfer has not been tested

*Evidence-qualified concern. Impact high. Confidence medium-high for rules, medium for sentiment.*

`812a655:src/jeff/training/train.py:211,309` seeds Python's `random` and shuffles once per epoch, so the batch order can be replayed. I joined it to `training.loss_history` in `review/evidence/model/m4-v2-20261111-01/{minilm,msmarco}/run.json` and regressed each batch loss on its family mix.

| Training-time CE on TRAIN, epoch 1 → 2 → 3 | Intent | Sentiment | Rules |
|---|---|---|---|
| MiniLM | 0.64 → 0.20 → 0.10 | 1.45 → 1.39 → 1.15 | 1.26 → 1.24 → 1.25 |
| MS MARCO | 0.38 → 0.18 → 0.09 | 1.43 → 1.36 → 1.22 | 1.31 → 1.27 → 1.26 |
| Uniform guess | 1.31 | 1.39 | 1.27 |

Rule loss never left chance on the rows being trained on. Sentiment loss stayed near chance through epoch 2 and was still falling when training ended. The new-rule results (15 and 21 of 80) and the D3 seen-mechanism results (31 and 26 of 96) therefore describe a model that never learned rules, not one that failed to transfer them. R5 noted that train-fit summaries were "still needed"; the data to estimate them was already on disk.

*Counterevidence.* These are estimates from changing weights with dropout on (R² 0.60–0.67; single-family batches agree, 2–7 per cell). MiniLM's development sentiment loss after training is 0.94, so its final state is better than the epoch-3 average.

*Falsifier.* Eval-mode CE by family on the 1,500 TRAIN rows for the existing M4 checkpoints. If rule CE is well below 1.27, or sentiment CE on TRAIN is far below development, the limit is transfer and this finding is wrong.

### 2. M6 is a constant function; it is evidence about one recipe, not about decoders or feasibility

*Verified observation (constant output); hypothesis (cause). Impact high. Confidence high for the observation, medium for the cause.*

I joined the P4 outputs (`review/evidence/release/p4-m6-20261111-01/run/*.jsonl`) to their frozen inputs. The probability at each option count and position is the same for every input: standard deviation at most 0.0015 across 624 presentations. Four options always receive 0.406, 0.152, 0.180, 0.262. The ratio p(B)/p(A) is 0.373–0.375 at every option count from two to six, so this is one fixed letter preference, renormalized.

TRAIN shows the same vector: in `training/fit-after.jsonl`, CE within each (option count, target position) cell varies by at most 0.006, and exp(−CE) gives the same four values. D5 §3 recorded these narrow ranges and drew no conclusion. They imply position 0 wins strictly on every TRAIN row, which D5 left unresolved for 1,360 rows.

The collapse began at the first update (`training/online.jsonl` against `fit-before.jsonl`). Of the four rows scored after one optimizer step, the three with target A have p(target) of 0.77–0.95. The one with target D has CE 13.5, where the starting weights gave 2.70. Intent rows seen after 6–10 updates average CE 1.01 (n=9); at the starting weights the same rows average 0.07.

*Hypothesis.* The step was too large. Adam's early steps move each parameter by about the learning rate whatever the gradient's size, so clipping at 1.0 did not bound the step (`dafd5d2:src/jeff/training/qwen_decision.py:151-171`; constant 2e-5, no warmup, `qwen_data.py:23-25`). Mosbach et al. (Appendix C) attribute failed fine-tuning runs to optimization rather than data.

*Counterevidence.* 2e-5 is a conventional rate, and Model's source review found no Python-path defect. The swing toward A matches the first batch's largest-loss target, which fits overshoot better than a corrupt gradient, but MPS gradient correctness is unverified.

*Falsifier.* M7 at 2e-6 still yields input-independent outputs. Suspicion then moves to the backend.

### 3. The benchmark cannot measure the mission claim

*Verified design limit (final size, no unseen family in development); evidence-qualified concern (where the signal sits). Impact high. Confidence high.*

- `manifests/evaluation/final-v1.json` has 24 rows. `docs/evaluation/final-design.md` assigns six per family, with `passage_entailment` the only unseen one. A 12/24 result has a 95% interval of 31–69%. On six rows, a two-sided sign test reaches p = 0.03 only at six wins and no losses.
- Development contains no unseen family.
- On new-v2 the families behave completely differently (recomputed from `review/evidence/evaluation/e3-v2-freeze-v1/new-v2/validation.jsonl`):

| Correct of 80 | Intent | Sentiment | Rules |
|---|---|---|---|
| Random expectation | 22.0 | 20.0 | 21.9 |
| MS MARCO, untrained | 66 | 18 | 15 |
| Qwen 0.5B, frozen | 74 | 30 | 25 |
| MiniLM, trained | 74 | 43 | 15 |
| MS MARCO, trained | 77 | 43 | 21 |

Intent is near ceiling and largely solvable by matching: lexical overlap gets 63 (E3) and the untrained reranker 66. Rules are within noise of random for every predictor. Nearly all discriminating signal is therefore 80 sentiment rows from two producers and one teacher alias.

Sentiment is a fixed four-class task with reworded labels: every row has exactly one positive-only, negative-only, mixed and neutral option, drawn from 40 distinct strings. MiniLM's gain from 18 to 43 is mostly one boundary. The neutral class goes from 0 to 19 of 20. The three polarity classes go from 18 to 24 of 60, where chance is 20.

Group bootstrap over the 170 declared groups: trained MS MARCO minus its start is +17.5 points [10.9, 24.5]; minus trained MiniLM, +3.7 [−3.7, 11.3]; minus frozen Qwen, +5.0 [−2.1, 12.6]. Only the first is resolved. Groups share producers and domains, so these intervals are optimistic.

*Counterevidence.* Held-out rule mechanisms are a real held-out design. Reporting is by stratum and group throughout, and the project never claims transfer.

*What would change this.* A development stratum of unseen families with several hundred independently labelled rows.

### 4. The rules family is multi-step computation, and no candidate fits it

*Hypothesis (capability mismatch) and strategic preference (re-scope). Impact medium-high. Confidence medium.*

TRAIN rules include a weighted digit sum modulo 4 and chained coordinate transforms. Development mechanisms include postfix evaluation, nearest Hamming codeword and longest common substring (E5 mechanism table). The encoder scores each option alone through a six-layer mean-pooled model, so it must compute the answer internally with no working space. Its rule loss is flat in training (finding 1). The frozen 0.5B model gets 25 of 80 and flips 65 of 80 choices when the options are reversed.

A third of every training epoch and a third of every aggregate is therefore noise. The README's 55% and 58.75% blend one solved family, one half-learned and one unlearned. D6 designs up to 96 new rule examples (`wave-20261111-1635/data-D6.md`); that preparation is aimed at the least tractable family.

*Counterevidence.* Rules carry the only executable labels. Applying a supplied policy is central to a decision model. Some policies, such as role grants with a veto, are closer to lookup than arithmetic and may be learnable.

*Falsifier.* After longer training, rule CE on TRAIN falls clearly below 1.27 and D3 rises above chance.

### 5. The probabilities support in-distribution selective prediction, not confidence under shift

*Evidence-qualified concern, with one useful positive. Impact medium. Confidence medium.*

On new-v2, when a trained encoder's top probability is at least 0.8, it agrees with the label 96–97% of the time: MiniLM 80 of 83, MS MARCO 75 of 77. The chance that a correct answer carries higher confidence than a wrong one (AUROC) is 0.89 and 0.85. Frozen Qwen manages 83 of 106 and 0.78. A caller could act on about a third of these decisions and escalate the rest. This is the closest thing to useful decision behavior in the snapshot, and no report states it.

It does not survive the probes: 6 of 10 and 10 of 16 at the same threshold. That is the usual pattern under shift (Ovadia et al., Appendix C). Much of the in-distribution signal is the model recognising the easy family (intent mean confidence 0.94–0.95). Within sentiment, AUROC is 0.76 and 0.70.

The two readouts fail in opposite ways. The encoder is order-invariant by construction (zero flips), but options never see each other, so it cannot express "none of these" and splits mass across near-duplicates. The decoder sees all options, but through letters: 122 of 240 choices flip on reversal (E5), a known weakness of letter readouts (Zheng et al., Appendix C).

*Counterevidence.* The probes are 12 hand-built hard pairs, not a sample of shifted inputs, and n is small.

*What would change this.* A risk–coverage curve on an unseen-family stratum.

## 4. Next actions

### A1. Run a fit ladder on the encoder (Model runs, Evaluation scores)

- **Step 0, no training.** Eval-mode CE by family on the 1,500 TRAIN rows for both existing M4 checkpoints.
- **Step 1.** The M4 MS MARCO recipe with one change: 3 epochs → 30. Log eval-mode TRAIN and development CE by family each epoch. Keep the final checkpoint; do not pick an epoch from the curve for a claim.
- **Step 2.** Step 1 without the rule rows.
- **Held fixed.** Data release, seed 42, learning rates, batch 4, cap 256, the development strata and the reversal check.
- **Cost.** At most 25 s per epoch measured (74–77 s for three, including saves), so about 15 minutes per run with per-epoch evaluation, estimated. A small logging change. £0.
- **Outcomes.**
  - Sentiment falls on TRAIN and development together: the recipe was undertrained, and longer training is the day-two improvement.
  - TRAIN falls and development does not: a real transfer problem. Go to A3, not more epochs.
  - Rule CE on TRAIN stays near 1.27: this scorer cannot represent the rules. Re-scope them and do not take the D6 design forward to authoring.
  - Step 2 beats step 1 on intent and sentiment: the rule rows are harmful noise.

### A2. Make the decoder result interpretable before spending more on it (Model, Evaluation)

- **E7, no compute.** Report the spread of probability within each (option count, position) cell, on M7's saved TRAIN vectors and on P5 outputs. Near-zero spread means a constant model, whatever the accuracy.
- **Overfit check.** 32 fixed TRAIN rows, 50 updates at M7's settings, CE on those rows logged after updates 1, 2, 4, 8, 16, 32 and 50. Repeat the first 8 updates on CPU.
- **Held fixed.** Base weights, prompt, readout, seed.
- **Cost.** About 2 minutes on MPS, estimated from M6's capacity measurement of ~2 s per update on its longest rows. CPU time is unmeasured. £0.
- **Outcomes.**
  - The model cannot drive 32 rows toward zero loss: the defect is in optimization or the backend. Stop decoder training until it is found.
  - CPU and MPS diverge: the backend.
  - The model fits 32 rows with input-dependent outputs: the path is sound and M6 was step size. A multi-epoch run with warmup is then justified.

### A3. Give development an unseen-family stratum with independent labels (Data builds, Evaluation freezes)

- **Change.** Convert public human-labelled classification or multiple-choice sets into the v0.1 contract: at least three families absent from TRAIN, at least 150 rows each, original labels, original short label strings as options. Never train on them. Keep `passage_entailment` out so the sealed final stays unseen. Score the existing checkpoints: both M4 starts, both trained, and P3. Published unseen-task transfer came from training on many public families (Sanh et al., Appendix C), not three.
- **Cost.** A licence check per source, a conversion script, an estimated 1–2 hours. Inference takes seconds. £0.
- **Outcomes.**
  - Trained scores below its start on unseen families: fine-tuning narrowed the model, and the claim must be "in-family".
  - Trained scores at or above its start: the first transfer evidence.
  - Either way, the project gains rows whose labels do not come from the teacher alias.
- Report the 24-row sealed final as a smoke check, or enlarge it before it is opened.

## 5. Preserve / stop

**Preserve**

- Reporting by stratum, family and source group.
- The baseline set: uniform, lexical, pretrained-head start, frozen decoder, byte-identical start controls.
- The honest language: teacher agreement, no calibration claim, negative results kept.
- The sealed final and the train/development exclusion rules.
- The encoder scorer's order invariance, and reversal pairs as a standing check.
- Trained MS MARCO as the working reference. It holds the only resolved gain.

**Stop**

- Rationing learning runs to one per wave, with no retry, when a run costs 75 seconds to 13 minutes. Keep predeclaration for the final pass. More runs will wear out a 240-row development set faster, which is a further reason for A3.
- Reading M6 as a position-bias or decoder result.
- Quoting one number across families.
- Designing or authoring more rule data before any model fits the existing rule rows.
- Withholding an inference that the retained numbers support, as in D5 §3.

## 6. Unknowns

1. **Which claim is day two for?** (a) Better than cheap alternatives on seen families, with usable confidence, or (b) evidence of unseen-family transfer. (a) is within reach on current data. (b) needs A3 first. This is a user decision.
2. **What "small" and the 16 GB floor mean.** Full fine-tuning of the 0.5B model sampled about 11.9 GB of MPS driver memory (not a true peak). That fits 24 GiB and is doubtful on 16.
3. **Whether computation-style rules are in scope.**
4. **What a caller does with the number:** take the top option, apply a threshold, or weigh costs.
5. **Whether public human-labelled data is acceptable** to the user.
6. **Not observed:** M7; eval-mode TRAIN fit for M4; MPS gradient correctness; any second seed.

---

## Appendix A — Stage 1 memo (frozen)

Written at 2026-11-11T18:38Z, before Stage 2. Reproduced unchanged apart from heading levels. SHA-256 of the original file: `b3890b467d6ca38269f7758a9bc40f6bcc0ab0e2c9ee4201aa852484e685629b`.

### Stage 1 provisional framing memo (frozen before Stage 2)

Written 2026-11-11T18:38Z after reading only `review/protocol.md`, `review/README.md`, `review/manifest.json` (identity fields), `review/brief.md` and `AGENTS.md`. No plan, contract, observation, evidence-map, result or code read yet.

#### Reconstruction

- **Achievement.** A small pretrained text model, fine-tuned locally, exposing one primitive: (context/state, question, caller-supplied options) -> a distribution over those options. Single-choice incl. yes/no. Day one: a real trained, saved, reloadable checkpoint with a held-out comparison against its starting point. Day two: make it better. The stated ambition is learning that "transfers across more than one task family"; the stated higher goal is "useful decision behavior".
- **Users / decisions.** None is named. The implied caller is a program or agent wanting a cheap, local, non-generative decision primitive (route, gate, classify, yes/no check) plus a number it can threshold. The real near-term decision-makers are the user (what to do with ~30 remaining hours; what may honestly be claimed) and hackathon judges (ambition, novelty, usefulness, working software).
- **Success criteria, in increasing strength.** (1) infrastructure works; (2) trained beats its own starting point and trivial baselines on held-out rows; (3) the gain survives held-out templates / option wordings / families; (4) probabilities are reliable, not just normalized; (5) a caller's decision is better with it than with the cheapest alternative. Only (1) and a weak form of (2) are fixed by the brief. Nothing quantitative is agreed for (3)-(5).
- **Hard constraints.** Python 3.12/uv; pretrained start; local Apple silicon (24 GiB measured); £50 ceiling; deadline 2026-11-12 23:59 London; no software tests/lint; sealed final set; immutable artifacts; no eval/diagnostic case or paraphrase into training; teacher agreement is not correctness; probabilities not assumed calibrated.
- **Preferences (challengeable).** Full fine-tuning, backbone, objective, synthetic task mix, data volume, prompt/readout, experiment sequence, six-team swarm.

#### Is "probabilities over arbitrary caller-supplied options" a useful target?

As an **interface**, yes: it subsumes classification, NLI, multiple choice and routing, and any shared-weight option scorer gives it for free. Flexibility is therefore an architectural property and is not evidence of anything learned.

As a **learning target**, no, not by itself. "Arbitrary" names the function's domain, not a distribution. A target needs (a) a distribution over (context, question, option set) and (b) a labelling rule. Unrestricted, it is general language understanding, which two days of fine-tuning cannot create; the realistic ceiling is the backbone's existing competence, exposed and sharpened on a few families without being damaged elsewhere. That makes the pretrained backbone under its best cheap readout the baseline that matters, and forgetting/negative transfer the main risk.

As a **probability**, a softmax over supplied options means "P(option i | exactly one supplied option is right)". It is set-relative (not comparable across option sets), splits mass across near-duplicate options, has no "none of these" mass unless the caller adds it, and for tasks whose answer is determined by the context its ideal value is 0/1, so the number only expresses model uncertainty. Yes/no is the one case where it is an absolute proposition probability. What a caller can actually use is ranking plus selective prediction (does low confidence predict error on unseen inputs?), which is weaker than, and should be claimed instead of, "calibrated probability".

#### Evidence that would separate semantic competence from template fitting

1. A ladder of held-out distance, reported separately: unseen rows of seen templates; unseen templates; unseen option vocabularies / relabelled options; unseen families; human-authored external items not produced by the project's generator or teacher.
2. Paired comparison on the same items against: uniform, prior/majority, position and length heuristics, lexical overlap, an option-only and a context-removed model, a bag-of-words classifier trained on the same TRAIN set, and the untouched backbone with its best cheap readout. If a surface baseline matches the trained model, the gain is template fit.
3. Interventions: option permutation and paraphrase invariance; minimal context edits that should flip the answer versus irrelevant edits that should not; cloned or added distractor options; undetermined contexts, where mass should spread.
4. Dose-response: more independent families/templates in training should raise unseen-family performance; more rows of the same templates should not.
5. Statistics by independent cluster (template/family/source), not by row, order or paraphrase; more than one seed; a metric fixed before looking.

#### What the reconstructed brief does not establish

- Any workload, so "useful" has no referent; what "small" means; latency; cost of a wrong decision.
- Whether "transfers across more than one task family" means multi-task fit on several seen families (weak) or zero-shot transfer to unseen ones (strong). These differ by an order of difficulty and the brief permits either reading.
- Whether tasks are determined by the context or genuinely uncertain, hence what the probability is a probability of; whether exactly one option is always right.
- Whether labels are programmatically verifiable or teacher opinion.
- Which baseline defines "improvement". "Starting baseline" could be a near-chance untrained readout, which makes any training look good.
- What the probabilities are for: argmax only, thresholding, abstention, or expected-value arithmetic.
- The brief is the project's own reconstruction, so it may already encode project choices as user intent.

#### Provisional judgments to confirm or revise in Stage 2

- **P1.** Compute is not the binding constraint; the number of independent task sources and label quality are. Expect easy in-template fit and small, noisy unseen-family transfer.
- **P2.** Expect a self-authored synthetic benchmark with few independent clusters, so wide intervals and no external anchor.
- **P3.** Expect the headline comparison to be trained-vs-own-start under one readout, with the stronger "best cheap alternative" baseline missing or weak.
- **P4.** Expect normalized probabilities with reliability measured in-distribution at best.
- **P5.** Expect the objective (cross-entropy to one teacher label per row) to reward template fit, not the decision use.
- **P6.** With many numbered stages on day one and six teams, expect process cost to be material relative to a two-day window. (Execution is another reviewer's remit; noted only as a feasibility factor.)

Each of these is a prior, not a finding. Any may be wrong.

---

## Appendix B — Recomputation notes

All paths are under `review/evidence/` unless stated. Python 3.12 standard library only; nothing was written inside the checkout.

- **New-v2 by family.** References `evaluation/e3-v2-freeze-v1/new-v2/validation.jsonl`. Predictions `model/m4-v2-20261111-01/inference/{minilm,msmarco}-{baseline,checkpoint}-combined.jsonl`, `release/p3-qwen-20261111-01/run-02/v2-original.jsonl`, `release/p4-m6-20261111-01/run/v2-original.jsonl`. Top choice with first-position tie-break. Totals reproduce the reports: 66, 132, 99, 141, 129, 65 of 240.
- **Sentiment classes.** Option strings mapped to four classes by keyword rules. Check: all 80 rows have exactly one option per class, and targets are 20 per class.
- **Group bootstrap.** 4,000 resamples of the 170 `group_id` values, fixed seed, percentile interval on the accuracy difference.
- **Confidence.** Top probability against correctness. AUROC over all correct/incorrect pairs, ties counted as half. Probes from `evaluation/e3-v2-freeze-v1/probes/validation.jsonl` and the matching `*-probes` predictions.
- **M4 training loss by family.** TRAIN rows loaded in manifest shard order from `model/m4-v2-20261111-01/minilm/dataset-manifest.json`. `random.seed(42)`, then one `random.shuffle` of `range(1500)` per epoch, batches of four. Least squares of recorded batch loss on the batch's family fractions, per epoch. The replay validates itself: a wrong order would give equal family estimates, and it gives 0.09 against 1.26.
- **M6 vectors.** P4 outputs joined by `id` and `option_id` to `evaluation/e3-v2-assembly-v1/inputs.jsonl`, `evaluation/e3-v2-order-v1/reversed-inputs.jsonl` and `evaluation/e3-v2-freeze-v1/probes/inputs.jsonl`. Mean and standard deviation per (option count, input position).
- **M6 early updates.** `model/m6-qwen-20261111-01/training/online.jsonl` row *i* was scored with weights after ⌊*i*/4⌋ updates. Compared by `id` with `fit-before.jsonl`. Gradient norms from `training/events.jsonl`.
- **Run times.** `docs/model/*-run.json`: 20.7 + 20.5 + 19.3 + 25.0 + 74.4 + 76.6 + 18.3 + 776.1 = 1,031 s. M6's figure includes two 1,500-row evaluation passes and the save. First commit `1bf5236` at 10:17 UTC.

## Appendix C — External sources

These are external claims, not project evidence. Search queries contained no repository content.

- Mosbach, Andriushchenko, Klakow. *On the Stability of Fine-tuning BERT: Misconceptions, Explanations, and Strong Baselines.* ICLR 2021. https://arxiv.org/abs/2006.04884. Failed fine-tuning runs are an optimization problem; small learning rates with bias correction and training for more iterations avoid them.
- Sanh et al. *Multitask Prompted Training Enables Zero-Shot Task Generalization.* ICLR 2022. https://arxiv.org/abs/2110.08207. Unseen-task transfer obtained by training on many public task families and scoring answer options by rank classification.
- Zheng et al. *Large Language Models Are Not Robust Multiple Choice Selectors.* ICLR 2024. https://proceedings.iclr.cc/paper_files/paper/2024/hash/54dd9e0cff6d9214e20d97eb2a3bae49-Abstract-Conference.html. Option-letter token bias drives order sensitivity in letter readouts.
- Ovadia et al. *Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift.* NeurIPS 2019. https://arxiv.org/abs/1906.02530. Calibration measured in-distribution degrades under shift.
