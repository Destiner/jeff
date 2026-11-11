# 05 — Execution and information throughput

Independent review, prompt 05. Evidence cutoff 2026-11-11T16:53:50Z. All times UTC.

## 1. Scope and verdict

**Identity.** Tag `fable-review-20261111-v1` (tag object `a00f393`) → review commit `65e8429d68bd0542eac145758d707e149034fd62`; its parent is the code base `91e09919bdf3b38370bf18c7bee0f6a2bbb26871`, matching the prompt, `review/source-code-commit.txt` and `manifest.json`. No other hash was supplied. `git rev-parse HEAD` was `e666c3a93c6a84a5d3a4f87d6b3ccb0e790b3780` at start and `1dab5278a3e76ba406340a4bb6334b8f06acca74` at completion (a concurrent session committed its report). HEAD differs from the tag only by files under `review/reports/`; I did not open them. `resolve_path.py --verify`: 912 files / 97,901,520 bytes, no failures.

**Inspected.** The prescribed docs; lead waves 1520/1540/1610/1635; I4 (report, events, final stats, closing board snapshot, P3 reconstruction); D4 summary/closure/observation log; D5 findings; Infra parking records; M6 process receipts, freezes, reviews and fit files; P3/P4/R6 process receipts and P4 vectors; E6 preparation v1–v3, integrity and train-control records; R6 evidence log; Git history.

**Recomputed.** I4 acknowledgement statistics (match); statistics over the 128-record board snapshot; the day's timeline from Git and process receipts; recorded ML wall time; M6 TRAIN fit (805→431/1500, CE 1.357724→1.390592, uniform 1.322383); P4's 624/624 first-position winners with no ties; per-position dispersion of M6 output vectors. **Trusted, not recomputed:** E6 development scores, R6 analysis, D4 label audit, source reviews. No public research, model loads, tests or lint.

**Not assessable from this packet.** Merge-lock hold times and contention (one I4 acquisition plus commit timestamps only); whether resumes needed manual nudges; the owner-rotation pilot; token and attention cost; board traffic after 15:48:44; most owner handoff files; anything requiring raw sessions. The continuation policy has one plausible pickup and one empty tail on record (F4); I5 is outside the cutoff.

**Bottom line.** The process is honest and it protected the experiment: the final set stayed sealed, E6's plan was declared (15:31:06) before training started (15:48:30), failures were preserved, and nothing unsupported was promoted. Its information rate is low and fell through the day. On the record, the limit was not compute, merging or message delivery. It was (a) each learning experiment waiting for a lead-authored wave, (b) a three-owner serial path wrapped around sub-minute jobs, and (c) verification effort re-confirming provenance rather than extracting or measuring what separates hypotheses. M6 took 81 minutes from authorization to an integrated independent score (two hours counting the research step that defined it) for under 15 minutes of compute, and 31 hours remain. Cycle time is the scarce quantity, more than the choice of next recipe.

| Learning lane (Model) | Time | Interval |
|---|---|---|
| M4 reported → M5 task issued | 12:13:21 → 12:58:06 | 45 min, no authorized learning run |
| M5 executed and integrated | → 13:16:28 | 18 min |
| M5 → M6 authorized | → 15:24:57 | 128 min, no authorized learning run |
| M6 prepared and trained | → 16:01:26 | 36 min (training 776 s) |
| M6 TRAIN fit known → M7 authorized | → 16:39:42 | 38 min |

## 2. Findings

### F1. Authorization, not compute or merging, set the pace

*Category: verified timings; avoidability is an evidence-qualified concern. Confidence: high on numbers, medium on avoidability.*

- Recorded ML process wall time for every known job totals 1,189 s (19.8 min) of a 396-minute day, 5.0%; after M5, 15.6 of 217 minutes (`docs/model/*-run.json`; `review/evidence/model/m6-qwen-20261111-01/*-process.json`; `review/evidence/release/*/process*-receipt.json`, `predict-process.json`). This is a lower bound on slot use, not proof the remainder was idle.
- Training results landed at 10:32, 10:40, 10:51, 11:07, 12:08, 13:07 and 16:01 (result commits; M5 and M6 from the board and process receipts): gaps of 8, 11, 16, 61, 59 and 174 minutes.
- Between 12:13:21 and 16:39:42 Model held an authorized learning experiment for about 55 of 266 minutes (table). The 14:46 direction to Model reads "No new training or changed experimental controls."
- Board snapshot (`review/evidence/infra/i4-20261111T144835Z/round-20261111T154844204161Z.json`, 128 records from 12:01): owner→lead acknowledgement median 600 s, p90 2,904 s, 14 of 35 over 20 minutes, arriving in batches (five at 12:48, seven at 14:04). Lead→owner median is 147 s and peer median 151 s. Unacknowledged items are excluded, so these understate. No commit reachable from the snapshot falls in 12:16:57–12:57:54 or 13:18:04–14:04:09.

LD004 removed lead approval of merges. It did not remove lead authorship of each learning experiment: M5, M6 and M7 were each issued as a single attempt. With runs costing 18–776 s, that rations the cheapest resource.

*Counterevidence:* the gaps may be human breaks; acknowledgements measure attention, not activity; later experiments needed new data and a new trainer; holding for P3/D3/R5 and diagnosing M6 before M7 were deliberate, defensible choices; Model did useful non-learning work. *Falsifier:* session logs showing Model blocked on implementation rather than direction, or a pre-authorized queue (A1) that fails to shorten result→next-start.

### F2. Sub-minute jobs sit inside multi-minute gates; two E6 stops were self-inflicted

*Category: verified defect (policy-document pinning); evidence-qualified concern (grant ceremony). Confidence: high / medium.*

| Job | Compute | Wall-clock around it |
|---|---|---|
| P3 frozen inference | 38.3 s | frozen 14:21:04, explicit READY 14:28:48 → predictions 14:41:30, 12.7 min; a 0.04 s pre-load `KeyError` consumed the grant and forced a regrant |
| P4 trained inference | 40.5 s | training exit 16:01:26 → start 16:10:47, 9.4 min |
| E6 scoring | CPU arithmetic | P4 outputs 16:11:27 → headline to peers about 16:34 → on main 16:45:49, 34.4 min |
| R6 diagnostic | 13.9 s | about 1 min after its ready request |

- Across P3 (both attempts), P4 and R6, the waits between a job being ready and starting total about 18 minutes for about 96 s of inference. A recorded process occupied the slot for 9 s of those waits (D3 inference, 14:30:27–14:30:36).
- E6's first scoring attempt stopped at 16:24:55 with `Pinned dependency changed: …/AGENTS.md` (`review/evidence/evaluation/e6-analysis-preparation-v3/previous-attempt.json`). The lead's continuation-policy edit changed two operating documents; all 94 scientific pins were unchanged. `docs/coordination.md` was committed 21 times that day, so pinning it guarantees collisions. A second stop followed when a 50 KB tool preview was saved as the tracked recipe copy (`e6-owner-integrity-v1/failure.json`).
- Model was the recipient of 11 of 31 I4 peer messages, with the slowest median acknowledgement (523 s) among recipients of five or more. That is consistent with, not proof of, scheduling duty competing with critical-path work.

**Necessary freezes (keep):** data and schedule hashes, checkpoint hash, label-free input identity, plan declared before outcomes, fresh-process reload, Evaluation's independence. **Procedural gates (drop):** an exclusive-grant message exchange for sub-minute inference on an empty slot; forfeiting a grant on a crash that produced no model output; pinning mutable operating documents; byte-copy checks of executed recipes.

*Counterevidence:* R6 shows the grant path can be fast; serialization protects timing and memory measurements; three jobs is a small sample. *Falsifier:* a binding error (wrong checkpoint or inputs scored) that only a dropped step would have caught.

### F3. After M6 failed, three owners re-verified the same provenance while the decisive fact went unextracted

*Category: verified by recomputation. Confidence: high for development, high-conditional for TRAIN.*

- The same seed-42 schedule and target-remapping replay, with fit aggregates, was performed by Model's reviewer (`m6-qwen-20261111-01/execution-review.md`), Evaluation (`e6-train-control-review-v1`, 16:12:18) and Data D5 (16:16:10–16:35:08). The training loop was source-reviewed three times. All found no defect.
- All three carry forward that TRAIN ties are unresolved (1,360 rows; the manifest's first known evidence limit). D5 and Model's diagnosis add that the narrow ranges are "not … proof that input is ignored". I found no report in the packet stating that the outputs are input-independent.
- My arithmetic on retained files settles it. P4's 624 development vectors are constant for each option count and position: for four options .406/.152/.180/.262, with SD ≤ .0015 and range ≤ .005 in every cell. From `training/fit-after.jsonl`, exp(−CE) grouped by option count and target position gives the same constants (.4063/.1525/.1799/.2620) and they sum to 1.0006 (three options), 1.0006 (four) and 1.0010 (five), against 1.76/1.80/4.20 before training. In plain terms: the trained model returns one fixed preference over answer letters whatever the question says, on TRAIN and development alike. Every option count has a fixed strict first-position winner, so the tie question is moot. This needed about 20 lines and was available from 16:11:27.
- M6 retained 24,768 resource samples (6.9 MB of its receipt) and 15 of 375 gradient norms, but no probability vectors and no mid-run fit. The capacity projection was 2,100 s against 776 s actual. Guards targeted the failure that did not happen.

*Hypothesis for why it was missed:* ownership walls (Data may not see development vectors; Evaluation was told not to substitute development for TRAIN), a diagnosis scoped to "no new inference or weight load", and a reporting norm that rewards listing what cannot be claimed.

*Counterevidence:* D5's exclusion of data and remapping defects is real uncertainty reduction; cross-owner replication has integrity value; my TRAIN inference assumes unsmoothed CE (the source review confirms it) and is exact only for development. *Falsifier:* re-scoring the saved checkpoint on TRAIN and finding input-dependent vectors.

### F4. Observation and availability lanes had recorded low yield

*Category: verified records; what to do about it is a strategic preference. Confidence: high on records.*

- D4's 24-case audit and consumer check finished by 15:06:34, 18 minutes in. From 15:09:20 to 15:47:59 its log holds 18 inbox checks, 765 s of requested foreground waiting and no new measurement (`review/evidence/data/d4-20261111T144812Z/observations.jsonl`, `closure.json`).
- I4 shipped one read-only `receipt` command by 14:59:26 and reports no further useful patch in the remaining 49 minutes. A 30-minute availability tail accepted no work, and I5 needs a manual resume.
- 38 of 128 board records, by task ID, concern the coordination mechanism itself (a traffic indicator, not a throughput measure). The 18-record I3 adoption exchange (14:24:31–14:32:04) overlaps P3's READY wait; that is temporal overlap only.
- Continuation: D5 began 26.4 minutes after D4 closed (a plausible pickup, nudge status unknown); Infra's tail was empty; Research started R6 by explicit resume at 15:53:10.

*Counterevidence:* D4 found supervision-coverage gaps that feed D6; I4's "no demonstrated benefit" is itself honest and useful; the mailbox replaced user relay and there is no baseline. *Falsifier:* I5 showing several un-nudged pickups and shorter comparable waits.

### F5. Six owners: independence paid off, lead span of control is the cost

*Category: strategic preference.*

- **Benefit on record.** Independent Evaluation caught M3's probe regression (16/24→8/24) and has blocked every unsupported promotion since. Contracts v0.1 are unchanged since 10:17:54 across every training run of the day. The merge lock shows no contention (three main commits within 25 s at 16:14). E6's plan and P4's binding were prepared in parallel before training began. Self-review let through a 0.04 s wiring error and a truncated recipe copy; both surfaced at first real execution and cost minutes, and I found no self-merged change that corrupted a result.
- **Cost on record.** The lead authored 16 direction files (about 4,500 words) between 15:20 and 16:39 and, as human plus main session, is the slowest-acknowledging node. 19 of 31 I4 peer messages sit inside the Model–Runtime–Evaluation triangle. At 13:36:50 five of six owners' latest record was delivered, parked or blocked; the next directions came at 13:58:22 and 14:04:22.
- **Within the user's preference:** keep six, but leave a lane parked when it has no decision-relevant work instead of assigning observation. `docs/swarm.md` already says agent count "should follow useful parallel work".
- **Beyond it:** four owners (Model+Runtime, Evaluation, Research+Data, lead absorbing Infra) would remove one handoff per run. It loses other-owner reload evidence and spare capacity for submission packaging. I would not reorganize mid-hackathon; the actions below capture most of the gain without it.

## 3. Prioritized actions

**A1. Pre-authorize a conditional queue (Lead; Research, Model, Evaluation).** Before each result, write the next arm for each outcome class and let Model start it without a new wave. Arms that miss a predeclared TRAIN-fit criterion are recorded and stop there; only arms that meet it go to Runtime and Evaluation. *Held fixed:* one factor changed from a frozen base, the same 624 development presentations and scorer, the final set sealed. *Cost:* about 20–30 minutes of design (estimated); 776 s per full Qwen arm and 18–77 s per encoder arm (measured). *Decides:* result→next-start under 10 minutes (baseline 38 and 128) confirms authorization was binding. If it stays above 30, preparation is the constraint and owners should be moved onto building arms.

**A2. Slim the per-run path (Model, Runtime, Evaluation; rule text only).** Inference under five minutes starts without a message when no training process holds the slot, reusing the existing `mkdir` lock pattern. A crash with no model output may relaunch under the same freeze. Experiment locks pin scientific dependencies only. Evaluation posts headline numbers first and the appendix afterwards. *Held fixed:* every "necessary freeze" in F2. *Cost:* about 15 minutes (estimated), no compute. *Decides:* training-end→headline under 10 minutes (M6 baseline: 9.4 minutes to start inference, about 23 more to a headline) with no binding error makes it permanent; a real mis-binding restores the specific gate that would have caught it.

**A3. First-look extraction and onset telemetry (Model; one named first-look owner).** Within 10 minutes of any run, post per-position mean and SD of output vectors and agreement against the base, from files already saved. From the run after M7, score a fixed 48-row TRAIN probe every 25 updates. *Held fixed:* recipe, data and schedule; observation only. *Cost:* about 3 s per probe at P4's measured ~17 rows/s, roughly 45 s or 6% of a 776 s run (estimated). *Decides:* collapse within the first updates points at update scale or the gradient path; gradual drift points at optimization dynamics. Either way no three-owner audit is needed to find out.

## 4. Preserve / stop

**Preserve:** independent Evaluation with plans declared before outcomes; the byte-identical start control; the sealed final set and immutable artifacts; preserved failures and plain negative reporting; stable contracts; the short merge lock; hard time boxes (R5 took 28 minutes, D5 took 19); preparation in parallel with training.

**Stop:** observation hours and mailbox feature or adoption rounds during an armed run; pinning operating documents into experiment locks; grant exchanges for sub-minute inference; assigning the same replay to a second and third owner; barring a seconds-long measurement during diagnosis; counting availability or acknowledgements as progress; long qualified reports ahead of the headline.

## 5. Unknowns

1. **User decision:** may Model launch predeclared arms without a lead wave (A1)? This is the largest lever and it is a governance choice, not a technical one.
2. **User decision:** may a text-free, label-free export of development probability vectors be shared across owners for first-look arithmetic, as was done once for R6?
3. Whether the 12:17–12:58 and 13:18–14:04 gaps were human breaks. If so, part of F1's waiting is not a process cost.
4. M7's outcome and I5's readout, both outside this snapshot.
5. Submission path: at `91e0991` no data or weights are tracked (`artifacts/` is ignored) and the README says they are not published. I found no evidence of a credential-free, 20-minute route to a runnable model for the judges. If Release keeps a lane, this looks like its highest-value work; confirm whether it is already planned.
