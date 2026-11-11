# 04 — Next experiments and decision value

Independent Claude Fable review, prompt 04. Read-only; nothing was executed beyond CPU arithmetic on exported artifacts.

## 1. Scope and verdict

**Identity.** Checkout HEAD `e666c3a93c6a84a5d3a4f87d6b3ccb0e790b3780`. Tag `fable-review-20261111-v1` is an annotated tag on review commit `65e8429d68bd0542eac145758d707e149034fd62`, whose parent is the code base `91e09919bdf3b38370bf18c7bee0f6a2bbb26871` (matches `review/source-code-commit.txt`). HEAD differs from the tag only by three commits adding `review/reports/01–03`; I did not open those or the copies in the report directory. `resolve_path.py --verify`: 912 files, 97,901,520 bytes, no failures. Evidence cutoff 2026-11-11T16:53:50Z. No user-supplied hash was given to verify. M7/P5/E7 and R7 have no outcomes here and I assume none.

**Inspected.** The orientation documents; M4/M5/M6 results and diagnosis; E3, E4-D3, E5, E6; R6; executed M6 source at `dafd5d2`; raw M6 TRAIN logs, P3/P4/M4 prediction vectors, development references, D5 findings; then R5 and the wave-1635 authorizations.

**Recomputed.** From raw vectors I reproduce P3 129/240 (NLL 1.3123) and 118/240 (1.4106), MiniLM 132/240 (0.8231), MS MARCO 141/240 (0.9173), M6 65/240 (1.4133). New arithmetic: M6 input-dependence on development and TRAIN, per-update collapse timing, temperature-only comparators, ensemble and discordance counts, chance bands, encoder loss history. **Trusted, not recomputed:** E6's arithmetic review, D5's identity audit, the Python source review, token audits, all resource measurements, R6's fits.

**Bottom line.** The next step should not be another unobserved full decoder epoch, and not new data. Retained logs show M6 lost most of its input-dependence within its first few optimizer updates and all of it by about update 100, so at least 73% of the run trained a predictor that ignores its input. The encoders, the only line that learns, stopped while still under-fit. Three cheap experiments follow, all £0, all minutes of compute, all within 24 GiB. Compute is not the constraint: training wall time recorded in the run summaries totals about 17 minutes for every run to date (M6 is 776 s of it). Owner and authorization time is.

### Ranking before and after R5

Recorded at 20:50 UTC, before opening R5 or the M7 authorization text:

1. Decoder go/no-go: a short step-size ladder, checked on held-out TRAIN rows every few updates, instead of another one-shot epoch (F1–F2).
2. Encoder fit versus transfer: a training-duration curve with per-family TRAIN fit (F4).
3. A task-aligned pretrained backbone, screened zero-shot first.

**After R5: retained, with two revisions.** R5's first priority was executed as M6 with the same recipe (2e-5, no warm-up, no intermediate evaluation). R5's own cited counterevidence mentions an early-collapse run that changed LR, warm-up and batch; that fits F2, but I did not verify the source. R5's second priority (coverage data) states that TRAIN-fit summaries are needed first; that measurement still does not exist for any encoder, so my item 2 comes before it. R5's contingent temperature diagnostic is answered by arithmetic below and cannot change a promotion decision, so I do not rank it. Revisions: Experiment 1 adopts M7's frozen controls to stay comparable, and Experiment 3 is now conditional on Experiment 2.

## 2. Findings

### F1. M6's final checkpoint is a constant predictor, not a "first-position preference"

- **Category:** verified observation by recomputation; not a code defect.
- **Evidence:** `review/evidence/release/p4-m6-20261111-01/run/v2-{original,reversed}.jsonl` joined by ID to the frozen inputs in `evaluation/e3-v2-freeze-v1/` and the two reversed-input files. Log-odds of each displayed position against position 0, over 300 inputs (fewer for D–F):

| Position (letter) | Mean | SD across inputs |
|---|---:|---:|
| B | −0.982 | 0.0056 |
| C | −0.816 | 0.0074 |
| D | −0.439 | 0.0035 |
| E | −0.430 | 0.0024 |
| F | −1.270 | 0.0049 |

  The reversed file matches to the third decimal. Frozen P3 has SD 3.7–3.8 on the same inputs. On TRAIN, `training/fit-after.jsonl` field `ce` grouped by (K, `target_position`), where K is the number of options, has SD 0.001–0.006 per cell; the implied probabilities sum to 1.001 for K=3 and K=4 and give the same log-odds across K.
- **Reasoning:** the output is one letter-logit vector regardless of content, family or K. E6's reported probability and margin ranges are just K=2…6 applied to that vector. Because option order was randomized by seed, the TRAIN cells leave no realistic room for ties among the 1,360 rows D5 left open. The vector is not the label prior (K=4 output .406/.152/.180/.262 versus target prior .267/.264/.226/.243), which is why CE is worse than uniform.
- **Impact, confidence:** high confidence. R6's letter and slot analysis of the frozen model cannot explain M6. E6's family-level NLL improvements are what a content-free constant produces when the start was worse than uniform.
- **Counterevidence / falsifier:** residual variation of ~0.005 nat exists. M7's full TRAIN vectors will show whether the signature recurs.

### F2. The damage happened in the first updates

- **Category:** verified timing; cause is a hypothesis.
- **Evidence:** `training/online.jsonl` (`ce`, `update`) against `training/fit-before.jsonl` (`ce`), same schedule index.
  - Update 1 saw targets A, D, D, B with CE 2.19, 0.17, 0.02, 0.48, so its gradient was dominated by one target-A row.
  - After that single update: three target-A rows moved 1.13→0.26, 0.03→0.05, 2.77→0.09; the target-D row moved 2.70→**13.51**.
  - Rows in the same update with the same K and target position share weights, so their CE gap measures input-dependence (330 pairs). Median gap: about 1.2–2.0 before training; 0.04–0.8 over updates 2–100 (few pairs early); 0.002–0.008 from update 101 (233 pairs, maximum 0.08).
  - Intent rows at presentations 21–40: CE 0.07 before, 1.21 online.
- **Hypothesis (medium confidence):** the step was too large in function space from step one. Adam's bias-corrected first step is about `lr·sign(g)` on all 494M parameters; clipping to norm 1 does not bound it, as the M6 diagnosis itself notes. Pre-clip norms were 14–165, the accumulation was four rows, and there was no warm-up. The capacity receipt shows the same four rows' gradient norm falling 522→76 after one update. Early-step instability of adaptive optimizers without warm-up is documented externally ([Liu et al. 2020](https://arxiv.org/abs/1908.03265); [Mosbach et al. 2021](https://arxiv.org/abs/2006.04884)); that is context, not project evidence.
- **Counterevidence:** one run; MPS is not bitwise deterministic; weight displacement was not recorded; a native numerical fault is not excluded.
- **Falsifiers:** a replicate 2e-5 arm keeps input-dependence past 25 updates; or an arm at 2e-7 collapses as fast; or M7 shows a first-update swing as large as M6's.
- **Conditional expectation, not observation:** scaling the single-update swing linearly, 2e-6 still implies moves of about one nat on the first step. I cannot predict whether discrimination survives.

### F3. "Better than the fresh base" can be passed without learning, and the development sets cannot resolve small gains

- **Category:** evidence-qualified concern.
- **Evidence:**
  - TRAIN start CE 1.3577 is worse than uniform 1.3224 (D5).
  - One scalar temperature takes frozen P3 new-v2 NLL 1.312→1.079 out of fold (three group folds, T≈2.0–2.8; oracle 1.058). Ranks do not change.
  - On 240 cases, MS MARCO minus MiniLM is +9 with 73 discordant cases (SE about 8.5, about 9.4 clustered by group). Differences below roughly 17 net cases are noise.
  - Chance bands: new-v2 rules 21.9 ± 4.0 (every predictor scores 15–25/80); D3 25.9 ± 4.3 (observed 26–31/96).
- **Impact:** an NLL gain up to about 0.25 nat with flat agreement is flattening, not learning. M7/E7 should be read on ranking, both-order agreement and input-dependence. The NLL comparator should be the fresh base rescaled by one fitted temperature (the "temperature-matched start" below).
- **Counterevidence / falsifier:** E7 already reports those components and forbids a composite; this adds a comparator, not a threshold. It fails if a temperature fitted on TRAIN start vectors does not transfer to development.

### F4. The encoders are under-fit, and rules show no signal anywhere

- **Category:** evidence-qualified concern (under-fit); hypothesis (rules exceed single-pass capacity).
- **Evidence:** `model/m4-v2-20261111-01/{minilm,msmarco}/run.json`. Mean online loss over the last 100 steps is 0.887 and 0.886; `metrics.validation_after.loss` is 0.840 and 0.876. There is no train–development gap after three epochs, and epoch means were still falling (1.116→0.941→0.832). Development intent loss is 0.09–0.18, so the other two families' TRAIN loss must be about 1.2–1.3 against chance near 1.33 (inferred, not measured).
- Rules: 15–25/80 for every predictor and every ensemble I tried; at least one of three models is right on 44/80, against about 46 expected from independent guessing. The tasks are multi-step algorithms (longest common substring with tie-breaks, cyclic counting).
- Sentiment is different: MS MARCO moved 18→43/80 with training, and three models' errors are nearly independent (at least one right 70/80, all three right 11/80).
- **Impact:** D6's up-to-96 new rule examples and any data scale-up are premature. The effect of 96 added training rows cannot be resolved on an 80-case slice sitting at chance.
- **Counterevidence / falsifier:** online loss includes dropout. The concern fails if per-family TRAIN agreement at the existing checkpoints is already ≥90% on rules and sentiment.

### F5. Recombining existing models gives a small, unresolved gain

- **Category:** hypothesis; post hoc on reused development data.
- **Evidence (new-v2, fixed equal weights):**

| Predictor | Agreement | NLL |
|---|---:|---:|
| MS MARCO alone | 141/240 | 0.917 |
| MiniLM alone | 132/240 | 0.823 |
| MiniLM + MS MARCO | 147/240 | 0.833 |
| Both + two-order-averaged frozen P3 | 151/240 | 0.843 |

  Net gain over MS MARCO is +6 to +11 with SE 5.8–7.5. Sentiment rises to 50–52/80; rules do not move. I examined about eight variants.
- **Use:** a fallback candidate for the one-shot final evaluation if nothing else lands. It is not evidence of better learning.

## 3. Prioritized experiments

### Experiment 1 — Decoder step-size ladder with held-out checks (isolates one factor: peak LR)

- **Owner:** Model executes; Evaluation freezes the rule first. No checkpoint is saved, so Runtime is not needed.
- **Step 0, no compute:** apply the two paired statistics in F2 and the F1 statistic to M7's `online.jsonl` and full fit vectors. If M7 kept input-dependence and meets the full-epoch thresholds below, skip the ladder and replicate once with a second seed.
- **Held fixed:** pinned P3 base, prompt and readout; M6's materialized schedule and every optimizer setting except LR.
- **Arms:** 2e-5 (positive control, must reproduce the collapse), 6e-6, 2e-6, 6e-7, 2e-7. Each trains on the first 240 presentations (60 updates).
- **Check rows:** the last 96 schedule rows, which no arm trains on; TRAIN only. Save full allowed-logit vectors at updates 0, 1, 2, 4, 8, 16, 32, 60.
- **Measurements on the check rows:** input-dependence D (across-row SD of position log-odds; M6's end state is 0.006, frozen P3 is about 3.7 on development); agreement by family; CE against the temperature-matched start. Also pre-clip norm every update and weight displacement.
- **Decision rule:** an arm has collapsed if D falls below 25% of its start at any checkpoint, or intent agreement on the check rows drops by five or more. It is stable if D stays at or above 75% and intent stays within two rows.
  - Control arm does not collapse → the failure is not recipe-determined; stop tuning and reopen the numerical diagnosis.
  - No stable arm at or above 6e-7 → **stop full-parameter decoder fine-tuning for this deadline.** A second stage (warm-up alone at 2e-6, or a restricted trainable set) only if hours remain.
  - A largest stable LR exists → exactly one full epoch there (M7 itself if it is 2e-6), judged on E7's components sized to F3: new-v2 both-order agreement ≥99/240 (82 + 17), intent both-order ≥60/80, NLL below the temperature-matched start in both orders.
- **Bounds:** five arms, 60 updates each, abort an arm at its first collapse checkpoint, M6's memory guards.
- **Cannot support:** which parameters or mechanism fail. LR is confounded with total displacement, so "stable" at a tiny LR may mean "barely moved". Sixty updates do not certify a full epoch. One seed.
- **Why it changes a decision:** it is the go/no-go for the whole decoder line, and replaces a 13-minute blind epoch with a 2-minute observable.

### Experiment 2 — Encoder fit versus transfer (isolates one factor: number of updates)

- **Owner:** Model and Evaluation.
- **Step 0, inference only:** deterministic per-family TRAIN fit for both existing M4 checkpoints.
- **Step 1:** the unchanged M4 recipe from a fresh start at 6 and 12 epochs for both encoders; epoch 3 already exists as the control. At each endpoint: per-family TRAIN fit, plus new-v2, inherited, probes and D3 with the existing scorer.
- **Decision rules:**
  - TRAIN rules below 60% at 12 epochs → capacity or interface limit. Stop rule-data work; decide between dropping rules from the claim and Experiment 3.
  - TRAIN rules ≥90% but new-v2 rules below 30/80 and D3 below 35/96 → memorization without transfer. Small rule additions will not help.
  - New-v2 sentiment ≥54/80 with inherited and probe agreement not lower → adopt the longer schedule; confirm once with a second seed.
  - Development NLL rising more than 0.3 above TRAIN NLL → over-fitting reached. Only then is data volume, and spend, the lever.
  - Otherwise → Experiment 3.
- **Bounds:** four training runs, hard cap 12 epochs, no LR change.
- **Cannot support:** updates are confounded with cumulative step size; capacity is not separated from pretraining; development data is reused; one seed.
- **Optional, same budget:** train on two of the three TRAIN producers per family and score the third (TRAIN is 100 + 200 + 200 rows per family by producer). That gives a 600-row cross-producer read with no development exposure, instead of 12 probe groups.
- **Why it changes a decision:** it chooses among training longer, changing the backbone, buying data, and dropping rules.

### Experiment 3 — Task-aligned backbone screen (combined recipe; run only if Experiment 2 shows under-fit persists)

- **Change:** score each candidate with the entailment logit of one NLI or zero-shot cross-encoder, zero-shot first. Public model cards (not loaded by me) list `MoritzLaurer/roberta-base-zeroshot-v2.0-c` (125M, MIT), `MoritzLaurer/deberta-v3-base-zeroshot-v2.0` (184M, MIT) and `cross-encoder/nli-deberta-v3-small` (142M, Apache-2.0).
- **Held fixed:** the same 624 presentations, scorer and per-candidate scoring; one hypothesis template chosen in advance.
- **Screen rule:** continue only if zero-shot new-v2 sentiment ≥43/80 and intent ≥66/80 (MS MARCO fresh is 18 and 66). Otherwise stop.
- **Then:** one fine-tune with M4's recipe. Carry it to final evaluation only if it beats M4 MS MARCO by ≥17 net new-v2 agreements with lower NLL and no loss of inherited or probe agreement.
- **Cannot support:** whether size, pretraining objective or architecture caused any gain.
- **Why it changes a decision:** it picks the backbone for the final candidate; a failed screen closes the question in minutes.

### Costs

| | Realized (from receipts) | Projected (my estimate) |
|---|---|---|
| Experiment 1 | M6: 1.47 s/update, 0.06–0.08 s/eval row; MPS driver max 11.85 GB, minimum headroom 7.2 GB (non-additive samples) | ~2.5 min per arm, ~12 min total, ±30% (M6 slowed late in the run). Same memory shape. Owner effort perhaps 1–2 h for the extra logging and freeze. |
| Experiment 2 | M4: 74–77 s per 3 epochs; MPS driver ~2.3 GB | ~15 min training, under 1 min inference. Config values plus one TRAIN input file; I did not verify that no code change is needed. |
| Experiment 3 | none | 0.5–0.75 GB download; 1–2 min zero-shot; 8–20 min fine-tune, unmeasured; ~3 GB optimizer state by arithmetic. DeBERTa on MPS is a risk, so try the RoBERTa variant first. Needs approval for new weights. |
| Paid spend and data | £0 reported to cutoff | £0 for all three; no new data, labels or teacher calls. Only a data scale-up would touch the £50 ceiling. |

About 31 hours remained at the cutoff, about 27 when this was written.

## 4. Preserve / stop

**Preserve:** frozen comparators, byte-identical start controls, paired both-order evaluation and immutable receipts; they made every recomputation above possible. M7's single-factor design and full-vector logging. The sealed final set.

**Stop:**
- Full epochs with no intermediate fixed-snapshot evaluation.
- Judging decoder learning by CE against the fresh base alone.
- Using letter or position bias to explain M6.
- Go/no-go conjunctions on a 12-group probe slice.
- Authoring rule examples before TRAIN fit is measured.
- Treating compute as scarce.

## 5. Unknowns

- M7/E7's outcome, which selects the branch of Experiment 1.
- Owner and protocol hours per experiment, and working hours left. The packet has no per-task effort record; M6 took roughly 40 minutes from its 15:20 authorization wave to completion at 16:01 UTC for a 13-minute run. Experiment 1 is five short arms, which the current "exactly one attempt" practice would need to authorize as one job.
- Whether the product must execute algorithmic rules. If yes, single-pass models of this size are probably the wrong class, and that is a user decision rather than an experiment.
- When, and on which candidate, the one-shot final evaluation is spent.
