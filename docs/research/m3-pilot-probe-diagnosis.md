# R4 — why M3's pilot gain does not transfer to the development probes

## Bottom line

**The consequential pattern is selective ranking deterioration hidden by aggregate probability improvements—not uniform loss of confidence.** M3 training loses three previously correct probe groups and gains none. Two losses are sentiment, leaving all four sentiment probe groups wrong; a third loses an explicit rule-precedence decision. All three finish close to the decision boundary. Meanwhile, one still-wrong intent group accounts for more than the entire apparent probe log-loss improvement.

Pilot gains are real against supplied labels but narrower than they look: sentiment accounts for 75% of its mean-loss improvement, while **all seven correct trained-M3 pilot rule decisions are no-result cases**. M3 picks the no-result choice in 19/20 rule rows. That is an observed answer-category preference, not proof of successful rule execution or proof of the internal feature causing it.

**Best-supported explanation:** fine-tuning adapts the scorer unevenly to a narrow pilot construction; the probes change wording, candidate descriptions and semantic scope together. **Cause not isolated:** pretrained source, representation/pooling, encoder adaptation and fast scalar-head updates are confounded. The one recommended subsequent control is to lower only M3's scalar-head learning rate, leaving the historical experiment otherwise fixed. **Nothing here changes, delays or authorizes another run alongside frozen M4.**

## Evidence and units

Reused Evaluation's `artifacts/evaluation/e2-m3-v2/` grouped reports and normalized per-row outcomes, not a replacement scorer. Report revision `v2` still evaluates **Data pilot-v1**, not Data-v2. The companion verified recipe/report/reference hashes, all eight selected saved-prediction files, and exact agreement between those normalized predictions and Evaluation outcomes.

- Pilot: **60 decisions / 12 source groups**; 40 teacher labels, 20 Data rule-verified labels. Different rows in a group are related cases, not duplicates or independent sources.
- Probes: **24 presentations / 12 unique source groups**, original plus exact option reversal; all teacher labels, teacher identity unknown. Tables below use originals once. Both orders retain the same choices in all four snapshots, maximum probability difference `6.91e-9`.
- M2 start: pretrained sentence encoder, **random scalar head**. M3 start: retrieval-pretrained encoder and **retained pretrained relevance head**. Their starts are not comparable head-only controls.
- Observational development analysis, not untouched final evidence, independent correctness, calibrated confidence or causal identification. No new labels, cases, paraphrases or Data authoring requests.

Three fresh bounded subagents covered probability/rank transitions, task semantics and historical recipe/source. Parent reproduced the key arithmetic and reviewed source. Artifacts: `/Users/destiner/Code/jeff/artifacts/research/r4-20261111T1145/`; [execution notes](../../experiments/research/m3-regression-diagnosis.md).

## 1. Rank reversals, not just aggregate scores

`m = p(target) − max p(rival)` is the **signed probability margin**, not top-two confidence or a raw logit. Positive means the target wins. Rank uses descending probability with input-order tie-breaking; none of these model cases ties. Compact IDs identify existing probe groups under `eval.validation.*`, not training-generation instructions.

| Probe group / diagnostic | M3 target rank, start→trained | M3 p(target), start→trained | M3 margin m, start→trained | M2 trained p(target) / rank |
|---|---:|---:|---:|---:|
| sentiment.03 — attribution | **1→2** | **.4872→.4912** | **+.0047→−.0124** | .5105 / 1 |
| sentiment.04 — neutral/scope | **1→2** | .8246→.4751 | +.6692→−.0246 | .6592 / 1 |
| rule_application.02 — precedence | **1→2** | .7780→.4863 | +.5729→−.0109 | .3573 / 1 |
| sentiment.01 — negated affect | 2→2 | .2047→.4383 | −.5494→−.0187 | .6098 / 1 |
| sentiment.02 — mixed affect | 4→3 | .2329→.1310 | −.0573→−.3549 | .4076 / 2 |
| intent.03 — clarification | 3→3 | .000810→.31405 | −.5241→−.0568 | .2248 / 3 |
| rule_application.01 — conjunction | 2→2 | .03277→.000790 | −.9345→−.9984 | .3112 / 2 |

**Three lost groups, zero recovered groups:** M3 goes 7→4 correct unique probes; M2 goes 1→8, gaining seven and losing none from its weak start. Trained M3 versus trained M2 loses five groups and gains one. These are descriptive changes, not independent-trial significance estimates.

The attribution case is especially informative: target probability improves, but the competing answer improves more, reversing rank. Mixed affect shows the reverse distinction: rank improves 4→3 while target probability falls and loss worsens. M3's four trained sentiment errors have different wrong directions; it is not one universal sentiment-label inversion. Two errors existed before fine-tuning, two are new.

The three new failures have trained **top-two probability margins .0124, .0246 and .0109**. Their target-to-best-rival log probability ratios change respectively **+.0098→−.0249**, **+1.6686→−.0505**, **+1.3333→−.0222**. With the actual temperature-one choice softmax these are relative raw-score gaps; absolute logits cannot be reconstructed. The latter two lose substantial initial separation even though their final margins are small. These movements are orders of magnitude larger than saved reversal roundoff.

### Why probe loss improves while decisions deteriorate

M3's mean probe loss improves **1.453783→1.360701**, a `+0.093082` improvement. But:

- The still-wrong clarification group improves **7.118072→1.158204** nats. With one of 12 equally weighted groups, its contribution is **+0.496656**—over five times the net improvement. It stays target rank 3 and chooses the same wrong action.
- Across the **other 11 groups**, mean loss worsens **0.938848→1.379110** (`+0.440262` worse). This exclusion explains the average; it is **not a proposed replacement benchmark** or permission to drop the outlier.
- The still-wrong conjunction group worsens **3.418378→7.142956**, contributing `−0.310382` to mean improvement. Five groups improve loss; seven worsen.

There is no contradiction: log loss rewards increased mass on the target even without a correct decision and is highly sensitive to initially tiny target mass. A positive scalar temperature adjustment preserves within-example order and cannot repair the observed rank reversals. No temperature was fitted here.

## 2. What the pilot gain actually contains

M3 pilot training yields **14 wrong→correct and four correct→wrong decisions**; all four losses are sentiment. Mean-loss improvement `0.233177` decomposes into sentiment **0.175349 (75.2%)**, intent **0.056581 (24.3%)**, rules **0.001247 (0.5%)**. Ten groups improve loss, two worsen—more distributed than the probe improvement, but not uniformly better decisions.

### Rule gains track answer category, not demonstrated execution

| Pilot rule group | M2 start→trained no-result choices | M3 start→trained no-result choices | Actual no-result targets | M3 agreement start→trained |
|---|---:|---:|---:|---:|
| Reachability, 10 cases | 9→0 | 10→9 | 2 | 2→2 |
| Election, 10 cases | 8→0 | 8→10 | 5 | 3→5 |

“No result” refers to the existing “Water reaches no other junctions” / “Elect nobody” options. Trained M3 misses **all 13 nonempty/winner cases**, while getting all seven no-result cases right. Its entire two-decision rule gain over its own start comes from the remaining two election choices becoming “nobody.” Conversely, M2 never picks no-result after training, missing those seven but solving four nonempty/winner cases. The category preference is present in the starting models too; do not describe it as wholly created by M3 training.

This makes M3's 7/20 versus M2's 4/20 a different trade-off between errors, not a demonstrated improvement in applying supplied rules. Only two pilot rule mechanisms are evaluated, with no dedicated held-out examples of the ten trained mechanisms.

### Sentiment learns some familiar contrasts, not all constructions

M3 pilot negative-class agreement goes **0/5→5/5**: all five starting predictions were neutral. Other classes change positive **2→3/5**, mixed **1→3/5**, neutral **4→3/5**. Its improved sentiment aggregate is therefore partly the correction of a strong starting neutral preference, not transferable mastery of every polarity/scope distinction.

Pilot luggage-storage group g28 is a within-pilot counterexample: agreement **3→1/4** while loss improves **1.24454→1.00430**. One negative row's target probability rises `.2387→.9503`, outweighing three lost correct ranks. Thus the decision/probability divergence is not exclusive to probes.

Pilot sentiment supplies four full mutually exclusive class descriptions, three recurring wording sets, and the same subject-question template. The inspected training sample already contains ordinary negation and mixed sentiment—“training never contained these” is false. Probe sentiment changes question wording, description wording/length, candidate count and attribution/scope simultaneously. Three groups offer three short choices; the four-choice mixed group also fails. Important counterexamples:

- Pilot positive/neutral rank failures occur without quotation or injected instructions.
- M3 retains correct answers on other negation and injected-instruction probe groups; a blanket “ignores negation” or “follows injected instructions” account fails.
- Familiar pilot candidate wording sometimes succeeds and sometimes fails; explicit mixed wording can fail in either suite. Neither candidate count alone nor fixed vocabulary inversion explains the pattern.
- The earlier longest-intent-option finding qualifies high pilot intent scores, but no saved intervention demonstrates that M3 used length to cause these probe errors.

## 3. Ranked explanations

| Rank | Explanation / status | Supporting observations | Counterevidence and identification limit |
|---|---|---|---|
| **1** | **Uneven adaptation to pilot task/answer construction plus a development-distribution shift.** Best-supported explanatory hypothesis, not an isolated cause. | Familiar sentiment contrasts improve; all rule wins concentrate on no-result targets; new probe ranking losses involve scope/precedence. Probe wording, candidate semantics and choice counts differ together. | Pilot has analogous failures; some challenging probes survive; mixed probe has four choices and still fails. No same-content one-factor construction control exists. Cannot attribute the effect to wording, count, length or scope separately. |
| **2** | **Pretrained scalar-head adaptation is too aggressive under the inherited random-head recipe.** Most economical controllable recipe risk. | Only classifier weight/bias get **5e-4**, 25× the **2e-5** used for all BERT parameters, including pooler. The head starts pretrained and then changes; three previously correct probe rankings are lost. | The same multiplier is reasonable to question, not evidence it is excessive. M3's head moves less in absolute L2 than M2's; pilot improves; encoder/pooler also change. No head-only causal comparison or gradient history exists. |
| **3** | **Pretrained retrieval/source and representation mismatch, including encoder/pooler drift.** Plausible inherited and co-adapting contribution. | Several probe errors predate fine-tuning. M3 changes retrieval-pretrained weights, pooled-CLS/tanh representation and native head dropout versus M2's sentence-pretrained mean pooling; all 105 M3 parameter tensors change. | No attribution to one component is possible. M3 starts stronger overall; M2 also fails shared cases and loses pilot rule performance. Scalar-head, encoder, pretraining and task-construction effects are not separable in these observations. |

**No demonstrated implementation bug:** historical-source/hash review supports retaining the pretrained M3 head, exhaustive disjoint optimizer groups, raw scalar candidate logits, external grouped-choice cross-entropy, and one softmax—not Hugging Face regression or sigmoid-then-softmax. Pilot token audits show no truncation at 256; those are reused Model evidence, not new tokenization or a fresh probe-length audit. Saved order consistency argues against an option-order artifact, not broad reasoning robustness.

AdamW uses weight decay `.01`, betas `(.9,.999)`, epsilon `1e-8`; no warmup, schedule or clipping. These are actual recipe choices, not demonstrated causes. M3 epoch train loss falls **1.0712→.9227→.8477**; no intermediate held-out history supports picking a supposedly better epoch. A shared scalar bias cancels from choice softmax; its changed hash is not evidence of meaningful ranking change. Single-seed, MPS nondeterminism, tiny purposeful probes and teacher labels limit all causal/generalization claims.

## 4. Exactly one recommended subsequent experiment

**One fresh M3 run changing only scalar-head LR: `5e-4 → 2e-5`.** Keep encoder **and native pooler** LR `2e-5`. This tests explanation 2's fast-head preservation risk; it does not pretend to isolate the broader construction hypothesis. No freeze, new architecture, data repair, seed sweep, schedule or extra change. The existing CLI already supports this one-factor change.

**Fixed controls:** historical M3 source `e37b0f3e7f2e3162abca87a76883eb81300603e0`; fresh retained pretrained `cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`, same tokenizer, no head reset; frozen pilot-v1 manifest SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`; same train order/seed42, pair formatting, cap256, batch4, three epochs/225 updates/900 presentations, full fine-tuning, MPS/four threads, Torch2.15.0/Transformers4.57.6, AdamW settings above, dropout and temperature1 unchanged. Use a new immutable output; verify the fresh start matches the original M3 start before interpreting training differences.

**Comparators/data:** reuse the historical 5e-4 M3 run and M3 start; M2 trained is descriptive context, not another intervention. Evaluation should use the same recipe-bound pilot60/12 groups and probes24/12 groups, with complete grouped decisions, target ranks/probabilities, signed margins and loss. Count probe pairs once for interpretation, preserve all groups, and separately show the rule answer-category counts. No new cases/labels, no probe-derived training, no final evaluation.

**Result supporting the hypothesis:** lower-LR M3 recovers at least one of the three lost unique probe groups without creating a new probe error relative to historical trained M3, lowers probe group-macro loss, and keeps pilot mean loss within **+0.05** of `0.793701`. This is a proposed practical retention/adaptation criterion, not a significance threshold. Smaller head-weight movement alone, or merely softer probabilities with the same wrong ranks, is insufficient. No recovered lost group or unchanged/worse probe macro loss weakens this intervention; a large pilot deterioration instead demonstrates a retention/adaptation trade-off. Report every outcome even if the criterion fails.

This single new run against a historical comparator remains vulnerable to stochastic/backend variation and cannot prove a head-only causal mechanism. **Recommendation only, for a later Model/lead decision after M4; no run is launched or authorized by R4, and frozen M4 controls/allocation remain untouched.**

## Delivery boundary

Research synchronized cleanly to requested main `0b372aa`. Only `docs/research/` and `experiments/research/` tracked files changed; analysis receipts are immutable Research artifacts. No model loading/inference/training, new dataset/labels, final-data access, paid work, tests or linting. Findings were sent directly to Model/Evaluation/Lead, not as Data authoring prompts. £0 additional actual/pending. The final public handoff records review, build, integration commit and released Research work.
