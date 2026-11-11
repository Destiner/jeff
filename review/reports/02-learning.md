# 02 — Learning path and failure identification

Independent Claude Fable review, prompt 02. Read-only; no model execution, tests, lint or installs.

## 1. Scope and verdict

**Identity.** `git rev-parse HEAD` = `ac4f744d62573db364bf493e522d89b0beb47217` (branch `review/fable-20261111`). Tag `fable-review-20261111-v1` → commit `65e8429d68bd0542eac145758d707e149034fd62`; HEAD is the tag plus one commit that only adds `review/reports/01-framing.md`, which I did not read. Code base `91e09919…` is an ancestor of the tag, and executed M6 source `dafd5d23…` is an ancestor of the code base. Evidence cutoff 2026-11-11T16:53:50Z. `resolve_path.py --verify`: 912 files / 97,901,520 B, ok. No user-supplied hash was given to verify.

**Inspected.** Protocol, README, brief, observations, evidence map, `AGENTS.md`, `docs/plan.md`; executed `qwen_decision.py`, `qwen_data.py`, `qwen_challenger.py` via `git show dafd5d23…`; `configs/model/m6-qwen.json`; M6 plan/results/diagnosis/run JSON; M6 receipts, schedule, `fit-before/after.jsonl`, `online.jsonl`, `events.jsonl`, capacity receipt; P3/P4 vectors; development labels; M4/M5 results; D5 findings; R5 memo; the M7 handoff.

**Recomputed here (stdlib arithmetic).** All 168 tracked-file hashes in `training/receipt.json` against Git blobs at `dafd5d23…`; schedule, audit, fit, online and capacity hashes; start-control byte identity with P3; target remapping for all 1,500 rows; uniform CE 1.322383; fit 805→431 and CE 1.357724→1.390592; online mean 1.400338; E6 agreement and NLL for inherited/new in both orders, base and trained; margin range .102494–.456558; D5's 140 certified winners. Everything in F1–F4 marked "computed" is new arithmetic on those files.

**Trusted, not recomputed.** Brier scores, probe macros, R6 fits, D4's label audit, library-source line citations, resource figures, M4/M5 numbers.

**Bottom line.** M6 is a genuine learning failure, and a more specific one than the reports state: **the final checkpoint is a constant function.** It returns the same letter probabilities whatever it is asked. That is a model state produced during training, so it is not a label, option-order, tie-breaking, save/reload or reporting artifact. Input dependence starts disappearing at the first optimizer step, is largely gone within roughly 40 updates and entirely gone by about update 160; the rest of the run only moves a content-free letter prior around.

The best-supported cause is the update rule: AdamW at 2e-5 with no warmup, on 494M parameters and 4-row batches, takes steps far larger than the pretrained function tolerates. The objective then offers a cheap way down that does not need the input, because the base model is confidently wrong on two of three families. I found no implementation defect, and the logs contain behavioural evidence that updates follow the analytic loss gradient. Exact native MPS gradient values remain unverified. M6 says nothing about whether this decoder and readout can learn the task.

## 2. Findings

### F1 — The M6 checkpoint ignores its input

*Category: verified by artifact arithmetic; an interpretation gap, not a code defect. Impact high. Confidence: high on development (full vectors), high-by-inference on TRAIN.*

Computed from `review/evidence/release/p4-m6-20261111-01/run/*.jsonl` (624 rows):

| K | Mean probabilities by letter position | Largest SD across inputs |
|---|---|---|
| 2 | .728 / .272 | .0006 |
| 3 | .551 / .206 / .244 | .0016 |
| 4 | .406 / .152 / .180 / .262 | .0010 |
| 5 | .321 / .120 / .143 / .207 / .209 | .0009 |

- These are renormalisations of one six-number vector. Relative logits A…F = [0, −0.982, −0.816, −0.439, −0.429, −1.270], with SD across inputs of 0.003–0.007 nats. On the same inputs the base model (P3) has SD 3.8–6.0 nats, so content-dependent variation shrank by about 550–2,300×. Correlation between trained and base centred logits is 0.07.
- That development-fitted vector predicts every one of the 1,500 TRAIN target probabilities `exp(−ce)` in `training/fit-after.jsonl` to within 0.0042 (mean error 0.0008), and implies TRAIN CE 1.39133 against the recorded 1.39059.

Consequences:

- **Ties.** The smallest implied top-two gap is 0.10 (K=6), about 25× the largest deviation. The 1,360 "unresolved" TRAIN rows are strict letter-A winners for every practical purpose. Row-level certification still stops at D5's 140.
- **Agreement counts are structural.** Every M6 agreement figure equals the number of targets sitting in position 0: TRAIN 431; development 17 and 65 (original), 13 and 65 (reversed).
- **The "exceptions" carry no signal.** 240/240 flips, zero both-order successes, TV .19–.21, max Δp .31, the new-reversed NLL gain (1.410621→1.407130) and the sentiment/rule CE gains all follow from a constant compared with an overconfident base. None is partial learning or an order effect.
- **"First-position preference" is incidental.** It is the letter prior at the moment training stopped. At update 356 the same run favoured B (p≈.34 at K=4).
- **Save and reload are faithful.** In-process `fit-after` and fresh-process P4 give the same vector.

Counterevidence: TRAIN full vectors were never saved, so TRAIN rests on one coordinate per row; residual variation is small but not zero. Falsifier: any TRAIN full vector from this checkpoint more than 0.01 from the constant.

### F2 — Input dependence is lost from the first optimizer step

*Category: timeline verified; causal reading is a hypothesis held with high confidence.*

`online.jsonl` and `fit-before.jsonl` score the same rows and prompts, so joining them by row shows how far the weights have moved from base when each row arrives. Computed:

| Presentations (updates) | Mean abs CE change vs base | corr(p_online, p_base) |
|---|---|---|
| 1–4 (1) | 0.000005 (max) | — |
| 5–8 (2) | 3.59 (max 10.81) | — |
| 5–40 (2–10) | 1.73 | 0.07 |
| 41–160 (11–40) | 1.23 | 0.30 |
| 161–640 (41–160) | 1.32 | 0.10 |
| 641–1500 (161–375) | 1.26 | 0.006 |

Within a single update, rows sharing the same K and target letter differ in probability by a median of 0.089 over updates 2–40, 0.0069 (max 0.21) over 41–160, and 0.0009 (max 0.006) over 161–375. Intent rows with p_target above 0.5 fall from 85% at base to 31% over updates 2–10, and to none after presentation 640.

- After **one** step, schedule index 7 (sentiment, target D) goes from CE 2.70 to 13.51, while indices 4–6 (target A) fall to 0.05–0.26. Update 1's gradient was dominated by index 0 (target A, base chose D at CE 2.19). One step therefore moved "A up, D down" by about 10 nats on unrelated inputs.
- `capacity/receipt.json`: gradient norm on the same four rows is 522.18 before and 76.50 after a single step.
- Mechanism (arithmetic, not measured): AdamW's first update is `−lr·sign(g)` per coordinate, since m̂/√v̂ = ±1. It does not depend on gradient scale, so clipping does not shrink it. Every weight with a non-negligible gradient moves 2e-5, a step of L2 length about 0.4, and the next several updates are similar because no averaging has built up. The recipe has no warmup or scheduler (`qwen_data.py:23-28`, `qwen_decision.py:151-153`, both at `dafd5d23…`). This is the usual reason warmup is paired with Adam (Kingma & Ba, arXiv:1412.6980; Liu et al., arXiv:1908.03265), and fine-tuning instability of this kind is typically an optimization problem (Mosbach et al., arXiv:2006.04884).
- A random perturbation of that size would be very unlikely to produce a 10-nat, directionally sensible shift. The step is coherent with the loss.

Counterevidence: M4 encoders trained successfully at 2e-5, batch 4, no warmup. They differ in having 22M parameters, a start at or below uniform CE, and per-option scoring. 2e-5 is conventional for full fine-tuning, though normally with warmup and larger batches. No counterfactual run exists.

Falsifier: M7 keeps the same schedule, so its first update has the same direction and one tenth the length. Presentations 5–8 (indices 4–7) should then move roughly 0.3–0.5 nats mean abs CE with the same signs. A multi-nat swing at 2e-6 would refute this account.

### F3 — The objective has a cheap content-free way down from this base

*Category: hypothesis. Confidence medium-high.*

- Base TRAIN CE by family: intent 0.396 (442/500), sentiment 2.020 (179/500), rules 1.657 (184/500). Uniform at K=4 is 1.386. On two of three families the base scores worse than a uniform guess.
- A uniform constant scores 1.3224 and the per-K label-marginal constant 1.3164 (computed). Both beat the starting 1.3577. Ignoring the input *lowers* the loss. M6 ended above its start only because its prior wanders: late online CE is 1.369 against 1.322 for uniform on the same rows.
- Sentiment and rule CE fell (2.02→1.44, 1.66→1.34) while the model became content-blind. CE alone cannot separate "less overconfident" from "learned something".
- Implication for M7: a lower LR can yield a slower flattening (CE down, agreement flat or down) or no collapse and no learning in 375 small steps. Neither is evidence of learning, and neither shows decoders cannot learn.
- Labels are not the driver. Base intent agreement is 88% under the same target mapping; four sentiment rows I read are sensibly labelled; M4 learned from this TRAIN set (new-v2 66→132/240). Rules are the exception: no trained model here has beaten the uniform tie-break baseline on new rules (encoders 15 and 21 of 80, against 23).

What would change this: with stable steps, agreement rises within one epoch and CE beats the calibrated-frozen reference (action 1d).

### F4 — No implementation defect found; updates follow the analytic gradient

*Category: scoped no-defect result with new behavioural evidence; telemetry is an evidence-qualified concern.*

Independent checks, all passing:

- Source, schedule, audit, fit, online and capacity hashes; start predictions byte-identical to P3.
- Target positions recomputed from option IDs for 1,500 rows. Answer tokens are always 32–37. Target positions are balanced (K=4: 276/273/234/252), so the data gives no position shortcut.
- Training and fit use the same `decision_loss` and targets (`qwen_decision.py:156-166`), under which the base scores 805/1500. The mapping is not scrambled.
- Update-1 online CE equals `fit-before` CE to 5e-6: clean reset, train and eval modes equivalent, no stale state.
- Loss/4 over four rows, one clip, one step, `zero_grad(set_to_none=True)` (`:338-361`); one parameter group of 290 tensors, all at Adam step 375.

Behavioural evidence (computed):

- The first step moves the readout in the direction the analytic gradient dictates (F2).
- In the content-blind phase (updates 161–375), the per-update change in a letter's log-probability correlates r = +0.69 (n = 243) with a β = 0.9 moving average of the analytic push (target frequency minus current probability), and +0.29 with the same-update push. Backward plus AdamW are moving the readout along the CE gradient.

Not established: numerical MPS gradient correctness across all tensors. The correlation covers the readout subspace only. No observation requires a backend bug.

Telemetry gaps: 15 of 375 pre-clip norms kept and update 1's not among them; no full vectors; no fixed probe set; the capacity run never logged same-batch loss before and after its one step.

### F5 — Ranking

| Hypothesis | Discriminating evidence | Status |
|---|---|---|
| Optimization (step size, no warmup) | F2: 3.6-nat mean shift after one step; Adam first-step arithmetic; capacity norm 522→76 | Sufficient to explain the collapse; high confidence. Not shown to be the only blocker. |
| Supervision / exposure (objective geometry, one pass) | F3: constant beats start; two families confidently wrong | Contributing attractor; medium. Learnability untested. |
| Architecture / readout | Letter readout has a content-free channel that per-option encoder scoring lacks (cf. Zheng et al., arXiv:2309.03882); base already letter-biased (rule K=4 picks by position 110/45/23/109) | Untested. M6 destroyed the function before this could be observed. |
| Implementation | F4 | Lowest. Native numerics unverified. |
| Label errors, option order, ties, reporting | F1, F3, F4 | Excluded as explanations of the constant output. Several reported M6 metrics are artifacts of it. |

## 3. Prioritized measurements

**1. Zero-compute reading of M7** — Evaluation with Model; about 20 minutes of CPU arithmetic on files M7 already writes; no extra forwards. Held fixed: schedule, rows, scoring.

- (a) Dose-response on presentations 5–8 (F2 falsifier).
- (b) Retention by update block: correlation with base and same-cell spread.
- (c) Constant-vector test on `fit-after` full vectors: per-K SD of relative logits (base ≈ 4–6, M6 ≈ 0.005).
- (d) Calibrated-frozen reference: fit one temperature, then temperature plus five letter offsets, on the base TRAIN vectors; report CE and agreement.

Outcomes: call it learning only if agreement rises *and* CE beats (d). Shrinking SD and spread means slow collapse. High retention with CE near base means under-training. A multi-nat move in (a) refutes F2: run action 2 before any further training.

**2. Pre-learning step-response and gradient check** — Model; needs lead authorization, since the M7 handoff excludes new disposable probes. Base weights, update 1's four rows, nothing saved.

- (i) FP32 gradient on MPS and on CPU: global and per-tensor cosine and norm ratio.
- (ii) Batch loss and a fixed 32-row TRAIN probe at θ − s·2e-5·sign(g) for s ∈ {0.01, 0.03, 0.1, 0.3, 1}.

Cost, estimated from M6 phase timings (0.08 s forward, 0.19 s backward per row): about 1 minute on MPS, plus an unmeasured CPU backward of perhaps 1–2 minutes and ~6 GB.

Outcomes: cosine below 0.99 on any large tensor is a backend defect, which is what M7's correctness-repair branch exists for. Loss falling only below some s* sets the initial step and warmup by measurement instead of convention. Loss rising at every s means the direction is wrong. Optional CPU-only addition: per-tensor weight change between the two safetensors files, to locate where the function moved.

**3. Overfit positive control** — Model; about 10 minutes on MPS (extrapolated, not measured); disposable. 32 fixed TRAIN rows balanced by family and target letter, 40 passes, step policy from action 2, full vectors each pass. Held fixed: base, readout, objective.

Outcomes: reaching ≥90% agreement and CE below 0.3 shows the learning path works, makes exposure and recipe the open question, and justifies one full run. Failing to memorise 32 rows is a reason to stop full-parameter decoder runs and put the time into the frozen decoder with calibration, or the encoders.

## 4. Preserve / stop

**Preserve.** Immutable receipts and source binding. Fixed-schedule fit before and after plus per-row online loss, which made this diagnosis possible. The byte-identical start control. The refusal to promote or to claim a backend bug. M7's same-schedule, single-factor design, which gives a clean dose-response.

**Stop.**
- Treating TRAIN tie status as an open question.
- Describing M6 as a first-position preference, or including it in order-effect analyses.
- Citing M6's NLL or family-CE gains as exceptions with content.
- Summarising online loss in 100–250-row windows; the event is in the first 40 presentations.
- Choosing a step size by convention, or launching full-epoch recipes before a positive control exists.

## 5. Unknowns

- Exact MPS gradient numerics (action 2).
- Where in the network input dependence was lost; this needs weights or activations.
- Whether stable steps produce learning within 375 updates, or whether exposure is the binding limit.
- Whether sentiment and rules are learnable through a letter readout from 1,500 rows. No trained model in this project has beaten the uniform baseline on held-out new rules.
- User decision: whether about 15 minutes of disposable diagnostic compute (actions 2–3) is acceptable before another full run, given the deadline.

External sources are cited inline for the Adam and warmup mechanics and for option-ID bias only. Public queries contained no repository content.
