# M12 — stronger frozen-backbone head learning rate

**The 100× head-learning-rate contrast improves aggregate TRAIN probability loss but reduces agreement and development order robustness.** M12 is complete and preserved, not promoted. Independent [E15](../evaluation/e15-head-learning-rate.md) and the separate [E16 mean](../evaluation/e16-m12-reversal-mean.md) are delivered. No extra epoch, numerical rescue, alternative endpoint or capacity claim follows.

## Fixed experiment

The sole scientific change from M8 is head LR **2e-6 → 2e-4**. One fresh original `Qwen/Qwen2.5-0.5B-Instruct@7ae557604adf67be50417f59c2c2f167def9a775` supplies the frozen494,032,768 original parameters. Only independent bias-free FP32 W6[6,896],5,376 scalars, learns. It starts from the original A–F output rows, not trained M7 or M8 weights.

Same v2 TRAIN manifest and materialized seed42 row/option schedule;1,500 presentations/375 updates/one epoch, microbatch1/accumulation4, AdamW betas(.9,.999), eps1e-8, decay.01, clip1, foreachFalse, FP32/MPS/four threads, complete1024-token cap, unchanged prompt/readout/T1. No feature cache, solver, new data, extra backwards or post-update restart. The full untied vocabulary export is a v2 deployment representation, not another trained arm or a tiny standalone model.

Execution uses clean `f75d72bd1487f9cf874aa48231233840881573fc`. M12-only counters record attempted calls immediately before the decoder backbone, completion after success/MPS synchronization: **4,500/4,500**, exactly1,500 START,1,500 TRAIN and1,500 FINAL. All375 updates completed. Instrumentation and supervision are operating changes, not additional scientific arms.

## Saved TRAIN fit

Same1,500 reference IDs,500 per family. These are teacher/reference agreements, not independent semantic truth. CE below is the producer's FP32-derived mean; saved-vector FP64/logit and raw-probability reconstructions differ slightly and are separately retained in the [run index](m12-head-lr-run.json) and first-look artifact. No clipping or fresh inference was used for the Model first look.

| TRAIN agreement | Original START | M8 | M12 |
|---|---:|---:|---:|
| Overall /1500 |805|804|786|
| Intent /500 |442|441|430|
| Sentiment /500 |179|179|173|
| Rules /500 |184|184|183|

| Producer mean CE | Original START | M8 | M12 |
|---|---:|---:|---:|
| Overall |1.357723629|1.332200274|1.135530835|
| Intent |.396152925|.370048039|.396181016|
| Sentiment |2.019891845|1.997228758|1.569388417|
| Rules |1.657126115|1.629324025|1.441023071|

Against M8, M12 gains162/loses180 agreements and changes526 choices;807 per-row CE and822 Brier values worsen despite aggregate proper-score improvement. Against START, gains172/losses191 accompany573 changed choices. All maxima are strict and all target probabilities positive. Final first-slot winners are936/1500, including426/500rules and337/500sentiment, versus417 START. This is not an exact constant vector or demonstrated content independence. Family×arity coordinate means, population SDs and position counts remain in the saved first look.

Producer-recorded W6 movement L2 is.18617352843284607, versus M8's.0051995856:35.805× movement, not100×. Maximum absolute coordinate change is.012136291712522507; initial/learned L2 norms1.1501964330673218/1.1495842933654785. All375 preclip norms exceed1 (12.243052–308.985718). A larger update and lower loss neither demonstrate convergence nor establish a frozen-feature capacity limit.

## Independent development follow-through

E15 retains all16 earlier raw contexts and scores only M12. Populations remain inherited60/12groups, new240/170groups (80rules/40policies/10mechanisms), and12already-paired probes/24presentations. Reversals are not independent cases; reused development is not untouched confirmation. No D3 pass belongs to M12.

| New240 | Original P3 | M8 | M12 |
|---|---:|---:|---:|
| Native / reversed agreement |129 /118|130 /119|121 /113|
| Both correct |82|86|75|
| Native / reversed NLL |1.312350 /1.410621|1.300082 /1.380115|1.172462 /1.235607|
| Native / reversed Brier |.633492 /.687402|.630714 /.675376|.627519 /.662124|

M8→M12 both-order retention/gain/loss is67/8/19. New family agreement is73/70intent,26/25sentiment,22/18rules, each/80 native/reversed;141/160rule presentations select first position. Inherited34/36 of60, both26,33flips. Probes total16/24 (10native/6reversed), both5/12: retain5/gain0/lose4 against both P3 and M8. Full family/source/arity and per-case regressions stay in Evaluation's report; lower proper scores do not cancel lost choices.

The pre-fixed aligned reversal mean is a **different, two-forward decision rule**, not a rewrite of raw M12. Its new agreement132/240 ties M8 mean132 but is below P3 mean134; NLL1.072924953/Brier.564642226. Native→mean gains27/loses16. Probe agreement10→9, with1gain/2losses and worse Brier. All means are untied; Jensen bounds compare against mean constituent loss, not the better orientation, correctness or calibration. No automatic confirmation slot follows.

## Proofs, actual execution and accounting

The original START file is byte-identical to M8/M7's original-P3 prefit. Original/fixed-buffer fingerprints, frozen/no-gradient/no-optimizer-membership records, nonaliasing, unchanged non-answer rows and normalized export/config links are retained. START/FINAL recorded projection differences are0logits/0probabilities, same maximal sets within1e-4/1e-6. **FINAL compares the heads on the same hidden state**, not an independent full-pipeline rerun for every case. Backend-specific storage evidence is not a generic external-Metal alias guarantee.

The parent checked all nine checkpoint-file hashes, manifest/receipt/proof links,1,500 START/FINAL/online records,375 norms and actual native/process/group return. Evaluation's separate92-check TRAIN/control review covers all3,000 START/FINAL vectors and exact joins/M8 controls without reading weights or replaying updates. Producer records, parent artifact consistency and independent saved-data review have different scopes.

- Sole audit:2.965878834016621s. Sole training/export:261.24403841700405s, completed2026-11-12T04:28:44.313876Z. Model subtotal **264.20991725102067s**.
- P13: one actual strict v2 fresh reload, **627 attempted/completed forwards =3 existing startup +624 scored**,2,390 probabilities; no extra START/D3/canary/retry/fallback. Both recorded loading-diagnostic locations have four empty lists. Output hashes/IDs/options/counts/finite normalization and actual group return were parent-checked;223 independent Runtime-binding checks followed.
- P13 timing is approximately42.5s. The inspected saved outer-publication event is42.496176875s; the later Runtime handoff quotes42.496509959s, not the same located receipt. Both give the unchanged conservative **44s** charge. No speed comparison is inferred.
- Aggregate **308.20991725102067/900s**; unused591.7900827489793s authorizes nothing. Model590s/Runtime310s sublimits also close.
- Model lifetime RSS3,370,532,864B, sampled MPS driver2,772,107,264B and minimum recorded recommended headroom16,297,558,016B satisfy its16GiB/16GiB/2GiB guards. P13 separately meets8GiB RSS/driver and2GiB recommended headroom. Samples/lifetime high-water/driver are different, overlapping, nonadditive scopes, not continuous physical-memory peaks. P12's separately reported headroom deviation does not amend these M12/P13 records.
- All624 saved prompt-token hashes/lengths/answer IDs match both P3 and M8 (1,248 comparisons), without retokenization. The frozen tokenizer warning remains; these inputs do not establish general harmlessness.

The initial `training/failure-receipt.json` explicitly says it is an incomplete-start sentinel, **not a completed zero-update failure**. Intermediate progress statuses do not override final completed native/external receipts. Controller originals and review history are retained: the last cancellation-gap source fix landed02:58:33,33seconds after the review tail, and was explicitly adopted by Lead; it is not retroactive independent approval. Pre-terminal cancellation invalidates success under the defined commit point, not an impossible guarantee after immediate terminal exit.

Root: `artifacts/model/m12-qwen-head-lr-20261112-01/`. Runtime: `artifacts/release/p13-m12-20261112-01/`. [Plan](m12-head-lr-plan.md) · [machine inventory](m12-head-lr-run.json) · [E15](../evaluation/e15-head-learning-rate.md) · [E16](../evaluation/e16-m12-reversal-mean.md). Preserve every endpoint, original controller and operational record. No tests/lint, new dependency, extra ML, original-final/D7 access or additional actual/pending spend. Builds establish packaging, not model quality.
