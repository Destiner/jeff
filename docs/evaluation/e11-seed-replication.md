# E11: a second seed retains broad learning and severe rule/order failures

**M10 seed7 improves broad development agreement/proper scores over M7 seed42, but new-rule both-order agreement is only4/80 and probe agreement falls21→19/24.** Its rule preference shifts from M7's first slot to a strong third-slot tendency. These are two realized seeds, not an estimate of seed variance, a better-seed selection policy or a promotion.

The [night criteria](night-comparisons.md) were adopted by Evaluation by01:03UTC on12November2026, before M10/P9 outcomes. Original P3 and M7 are primary controls; all14 retained contexts remain. The separately authorized [E16 mean rule](e16-reversal-mean.md) is exploratory post-processing, not E11's raw decision rule or a rewrite of its criteria.

## Controlled change and fixed TRAIN fit

M10 restarts original P3, not M7. The planned scientific change is seed42→7, including materialized row/option permutations and Python/CPU/MPS RNG. The same1500TRAIN/oneepoch/375updates,494032768trainable FP32 parameters,290unique tensors, AdamW LR2e-6,betas(.9,.999),eps1e-8,decay.01,clip1,microbatch1/accum4,foreachFalse and no scheduler remain. Operational Model cap2700→2400s and richer diagnostics/counters are not training treatments. Narrow source/control review supports these scoped conditions; it is not historical full-binary/full-tensor attestation.

The [independent TRAIN/control review][train] reconstructs every seed7 materialized presentation from nine exact TRAIN shards and reviews all1500START+1500FINAL vectors. Different option orders legitimately change START805→777 relative to seed42; neither identical vectors nor805 START is required.

| TRAIN population | Agreement START→FINAL | Logit CE START→FINAL | Summed Brier START→FINAL | Same-ID gains / losses |
|---|---:|---:|---:|---:|
| All1500 |777→1214|1.389727→.416055|.667489→.227461|514 /77|
| Intent500 |436→498|.355664→.020749|.177842→.007884|62 /0|
| Sentiment500 |174→483|2.093026→.123621|.952296→.057919|312 /3|
| Rules500 |167→233|1.720491→1.103793|.872330→.616581|140 /74|

All saved tops are singleton; coverage is complete.252rows worsen CE and242worsen Brier, including181/171rule rows. Final rule winners by one-based slot are26/83/388/3; third-slot dominance is not rule competence. M7's rule184→176/500 regression and first-slot472/500 remain historical evidence. Fixed TRAIN fit is neither held-out transfer nor the changing-weight online mean CE.817825. All375 preclip norms are finite/positive,360>1; these are not update bounds or a causal explanation.

## Unchanged evaluation population

Same624presentations:300native+300reversed+24already-paired probes,2390probabilities; probes are not reversed again. Native300 remain inherited60/12groups and new240/170groups. New rules80cases span40policies/10conservative mechanisms. Probe24 comprise12pairs. Dimensions and reversals overlap; none are IID sample-count multipliers.

All new predictions are valid, finite, complete and untied under the unchanged scorer's1e-6 sum-roundoff policy. Labels remain inherited40teacher/20rule_verified, new160teacher/80rule_verified, probes24teacher. Same-alias rule verification and unknown probe-curator revision are not independent human truth.

| Stratum | Native agreement | Reversed agreement | Native / reversed NLL | Native / reversed Brier | Both correct | Choice flips |
|---|---:|---:|---:|---:|---:|---:|
| Inherited60 |44|45|.506410 / .474389|.276910 / .254632|41|16|
| New240 |182|178|.525300 / .522373|.288286 / .282673|157|73|
| Probe12pairs |10|9|.293618 / .354217|.175614 / .239230|9|1|

P3→M7→M10 new both-order counts are82→138→157; inherited28→39→41. M10 versus M7 gains/loses30/19new native and31/23reversed agreements. Inherited native agreement45→44 falls despite better proper scores. M9 remains a useful contextual exception:165new both-order agreements, more than M10's157, despite lower single-order agreement165/165. Different architectures/training recipes do not constitute a controlled architecture comparison.

### Both-order agreement by family

Each entry is **P3 / M7 / M10**.

| Population | Intent | Sentiment | Rules |
|---|---:|---:|---:|
| Inherited,20each |18 /20 /19|7 /19 /20|3 /0 /2|
| New,80each |64 /75 /79|14 /63 /74|4 /0 /4|
| Probes,4pairs each |4 /4 /4|2 /4 /4|3 /1 /1|

M10 new-rule native/reversed agreements28/22 of80 conceal only4both-correct and69flips. Its new rule winners are native slots1:11,2:12,3:57 and reversed1:5,2:12,3:63: **120/160 third-slot choices**. Inherited rules choose slot3 on36/40presentations; across inherited+new rules,156/200. M7 chooses slot1 on all200. M10 is not an exactly constant-third decision rule, but neither does this repair rule transfer/order sensitivity.

### All retained contexts

These are descriptive reused-development measurements, not a pooled ranking or endpoint selector. Both-order successes and probe totals have different denominators.

| Predictor | New native / reversed, /240 | New both, /240 | New flips | Probe agreement, /24 | Probe both, /12 |
|---|---:|---:|---:|---:|---:|
| M4 MiniLM random start |66 /66|66|0|2|1|
| M4 MiniLM trained |132 /132|132|0|12|6|
| Original M4 MS MARCO start |99 /99|99|0|14|7|
| M4 MS MARCO three epochs |141 /141|141|0|10|5|
| M2 retained |107 /107|107|0|16|8|
| M3 retained |110 /110|110|0|8|4|
| Uniform |65 /65|0|240|8|0|
| Lexical |99 /99|70|121|9|3|
| Original P3 |129 /118|82|122|20|9|
| M6 fresh START |129 /118|82|122|20|9|
| M6 trained |65 /65|0|240|8|0|
| M7 seed42 |171 /170|138|101|21|9|
| M8 readout |130 /119|86|113|19|9|
| M9 twelve epochs |165 /165|165|0|16|8|
| M10 seed7 |182 /178|157|73|19|9|

Uniform's choices use deterministic first-input tie-breaking, not random expected1/K. Its identical maximal sets are not discrimination; lexical ties also remain explicit in full reports. Mean-rule results are deliberately absent from this raw-model table.

## Retention and source regressions

Against P3, M10 retains7probe both-correct pairs, gains2sentiment and loses2rule pairs. Against M7 it retains the same9both-correct pairs with no pair gain/loss, yet loses two reversed-only rule successes: **19/24 versus21/24**. Equal9/12totals therefore do not establish equal probe quality.

All source regressions are retained in the [review][quality] and [complete contrasts][contrasts]. Examples versus M7 include two sentiment source groups losing agreement in both orders; the sentiment-b-r2 producer worsens reversed NLL by.119190 and Brier by.025358 despite broad gains. Reversed longest-common-contiguous-substring rules worsen NLL by.168670/Brier by.018394 with one lost agreement over8cases. Policy/source/mechanism views overlap and must not be added as independent evidence. Exact mappings, not ID substrings, establish these dimensions.

## Actual execution, repair and evidence limits

M10's one learning process lasted718.695154s. Aggregate728.150536/2400s includes two audits and a preserved2.812403s pre-load environment-pin failure. No post-update restart or new development START run occurred. Sampled MPS driver max11886329856B, CPU lifetime RSS3377381376B and minimum sampled recommended headroom7183335424B satisfy their separate guards; overlapping counters are nonadditive and samples are not continuous peaks.

P9's first attempt failed at `transformers` import using the lightweight coordination interpreter: **zero tokenizer/model loads or forwards**. Its supervisor exited after.802366s, but the full309.808853250s outer wait remains charged. Lead explicitly granted an additional310s, total allowance619.808853250s. The repaired immutable attempt uses the existing full Runtime environment and narrowly corrected early-failure closure, not changed scientific inputs or software dependencies.

The actual successful P9 pass records627forwards=3existingstartup+624decisions, all groups returned, and40.756467s final watchdog observation conservatively charged41s. Combined P9 charge350.808853250s stays within the renewed allowance. Predict runtime36.349304s; CPU lifetime RSS553697280B, sampled MPS driver2768977920B and minimum sampled recommended headroom16300687360B have distinct scopes, not a controlled speedup.

The [125-check P9 binding review][runtime] supports successful **fresh v1 reload** and matching Runtime/Model manifest inventories. It does **not** establish four-empty-list loading-diagnostic verification: that explicit check is on the separate v2 path. Both actual phases emitted a tokenizer-regex warning; frozen bytes were not changed. A subsequent [saved-token comparison][tokens] independently confirms all624per-case prompt-token-list hashes, lengths and answer-token IDs match preserved P3 and M7 audits (1248comparisons). This supports exact token correspondence on these inputs, not general harmlessness of the warning or other texts. Weight bytes were not redundantly rehashed by Evaluation. Actual emitted predictions, declared runtime conditions and these qualifications—not an invented stricter loader contract—are the evaluated evidence.

## Reproducibility and publication

Successful new-only scoring is [night-scoring-preparation-v2/e11-execution-01][execution], completed03:19UTC. [Executed recipe](../../configs/evaluation/e11-m10-v1.json) and [report index](../../manifests/evaluation/e11-m10-report-v1.json) bind actual outputs. All14old contexts are byte-reused, not passed to the scorer again.

Two Evaluation pre-scoring failures remain intact: a9.8MB producer receipt exceeded the existing2MiB binding guard, then an actual import exposed one unmatched closing parenthesis in previously unexecuted preparation. A new preparation version fixes exactly that one source byte;165original pins were verified unchanged, and actual small Runtime/control receipts replace the oversized binding argument. No criteria, probability, guard or old artifact was rewritten.

Independent quality review covers9360raw presentation records across15predictors,4680pairs,10020orientation units,5010pair units,9352grouped contrasts,8736case contributions,168probe-retention rows,2160position cells and126byte-identical retained copies. Its explicit uncovered fields and preserved reviewer-only mistakes remain in the receipt. TRAIN/control review has65checks; Runtime binding125. No substantive arithmetic discrepancy was found within those stated scopes.

All helpers finished; branch/integrated packaging builds are publication checks, not scientific/software-test evidence. Additional actual/pending spending£0; no new inference, protected-final/D7 access, dependency, test/lint or promotion follows. E12/E14/E15/E13 remain their own authorized workstreams.

[train]: ../../artifacts/evaluation/e11-m10-control-review-v1/findings.md
[quality]: ../../artifacts/evaluation/e11-quality-review-v1/findings.md
[runtime]: ../../artifacts/evaluation/e11-p9-binding-v1/findings.md
[contrasts]: ../../artifacts/evaluation/night-scoring-preparation-v2/e11-execution-01/grouped-contrasts.csv
[execution]: ../../artifacts/evaluation/night-scoring-preparation-v2/e11-execution-01/completion.json
[tokens]: ../../artifacts/evaluation/e11-owner-integrity-v1/token-correspondence.json
