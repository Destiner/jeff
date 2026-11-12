# E15 — stronger learning rate for the frozen-backbone readout

**The fixed 100× head-learning-rate contrast is not a rescue of agreement or order robustness.** M12 reduces new-case NLL/Brier versus original P3 and M8, but agreement falls to121/113 of240 in native/reversed order, both-order successes fall86→75 versus M8, and probes lose four previously both-correct pairs. TRAIN probability fit improves while TRAIN agreement also declines. Neither this outcome nor the larger update proves convergence or a feature/capacity limit.

## Prospective control and scope

The [E15 addendum](../../artifacts/evaluation/night-predeclared-v1/e15-head-lr-addendum.md) was adopted01:27UTC before M12 outcomes. The sole scientific change from [M8/E8](e8-readout-scope.md) is head LR **2e-6→2e-4**: fresh original P3, frozen494,032,768 original parameters, independent bias-free FP32 W6[6,896] with5,376 trainable scalars, fresh head/optimizer/RNG, identical seed42 schedule,1,500 TRAIN presentations/375updates/oneepoch, optimizer/clip1/prompt/readout/temperature and caps. No cache, closed-form solver, trained-start shortcut, extra epoch or retry. The full151,936×896 exported vocabulary table is a v2 deployment representation, **not a trained full-vocabulary arm**.

Primary controls are P3 and M8, not failed M6. Sixteen completed raw contexts are retained, including M7/M9 and actual M10/E11 and M11/E12; M12 is seventeenth. P12/E14 had not completed at binding time. The historical comparison files remain explicitly historical, not invented complete sixteen-model pairwise comparisons. Only M12 is newly scored.

Populations stay separate: inherited60cases/12groups; new240cases/170groups, including80rules/40policies/10mechanisms; probes12already-paired groups/24presentations. Reversals, source groups, policies, mechanisms and producers overlap. These are not624 independent observations. Teacher/reference agreement is not independent semantic truth; same-alias rule verification, unknown immutable reviewer revisions and reused development remain qualifications. No D3 pass belongs to this contrast.

## TRAIN and control evidence

[Independent saved-data review][train] passed92checks, including all3,000 START/FINAL vectors, exact TRAIN-shard/schedule/option joins, M8 comparison, canonical producer fingerprint/storage records, source/recipe and process/resource bindings. It did not read weights, replay parameter updates or run a model.

| Same1,500 TRAIN rows | Agreement | NLL | Summed Brier |
|---|---:|---:|---:|
| Original P3 START |805|1.357723628|.650797231|
| M8 FINAL, LR2e-6 |804|1.332200276|.640291|
| M12 FINAL, LR2e-4 |**786**|**1.135530838**|**.615579763**|

| Family /500 | START→M8→M12 agreement | M8→M12 NLL |
|---|---:|---:|
| Intent |442→441→430|.370048→.396181|
| Sentiment |179→179→173|1.997229→1.569388|
| Rules |184→184→183|1.629324→1.441023|

START is byte-identical to M8/M7's original-P3 prefit. Against START, M12 changes573 selections, with172 gains and191 losses; against M8 it gains162/loses180. First-position choices rise417→936/1500, without ties;426/500 rule and337/500 sentiment choices are first-slot. This is not an exact constant vector or proof of a particular learned mechanism.

Recorded head L2 movement is.186173528 versus M8's.005199586, **35.805×**, not100×; initial head L2 is1.150196433. All375 preclip norms exceed1, range12.243052–308.985718. These are producer-observed movement/gradient records, not independent tensor measurements or convergence evidence. Changing-head online CE1.322342 is distinct from fixed-final fit.

Original/fixed-buffer canonical fingerprints and frozen/no-gradient/no-optimizer-membership records agree. START and FINAL recorded projection differences are0logits/0probabilities with identical maximal sets within fixed1e-4/1e-6 limits. **FINAL compares W6 and the exported full-vocabulary head on the same hidden state**, not an independently rerun full pipeline on every development case. Fresh P13 reload evidence is separate.

## Raw development results

Natural-log NLL and summed multiclass Brier are lower-is-better. Existing validated roundoff normalization at1e-6 remains; no clipping, smoothing or imputation. All624 M12 presentations/2,390 values are valid, finite and untied, with no zero probabilities or missing/extra vectors.

| Population | Native / reversed agreement | NLL native / reversed | Brier native / reversed | Both correct | Flips |
|---|---:|---:|---:|---:|---:|
| Inherited /60 |34 /36|1.093545 /.922122|.579666 /.493781|26|33|
| New /240 |121 /113|1.172462 /1.235607|.627519 /.662124|75|142|
| Probes /12pairs |10 /6|.523827 /.877238|.299046 /.551094|5|6|

| New-case context | Native / reversed agreement | Both correct | NLL native / reversed | Brier native / reversed |
|---|---:|---:|---:|---:|
| P3 original |129 /118|82|1.312350 /1.410621|.633492 /.687402|
| M8 lower-head-LR |130 /119|86|1.300082 /1.380115|.630714 /.675376|
| M7 seed42 full-model |171 /170|138|.669211 /.618564|.352959 /.337570|
| M9 12-epoch encoder |165 /165|165|.699420 /.699420|.359766 /.359766|
| M10 seed7 full-model |182 /178|157|.525300 /.522373|.288286 /.282673|
| M11 30-epoch encoder |162 /162|162|.860175 /.860175|.411284 /.411284|
| **M12 stronger-head-LR** |**121 /113**|**75**|**1.172462 /1.235607**|**.627519 /.662124**|

The new M12 family agreements are73/70intent,26/25sentiment and22/18rules, each/80 in native/reversed order. Rules choose first input141/160presentations; the vectors are not exact constants. Raw rule NLL1.587937/1.671524 and Brier.867886/.937504 remain poor. Inherited agreement combines19/20intent,9/9sentiment and6/7rules, each/20.

Both-order retention/gain/loss on new cases is **67/8/19 versus M8**, and67/8/15 versus P3. The lower proper scores do not recover these lost choices. Inherited both-correct falls28→26 against either primary; choice flips rise18→33 versus M8. Full explicit source/family/arity/regression and probe membership evidence is retained in the [quality review][quality], not selected away by headline averages.

Probes are especially adverse:16/24 total agreement versus P3's20 and M8's19; both-correct5 versus9, retaining five/gaining zero/losing four against each primary. Native/reversed family agreement is4/2intent,3/3sentiment and3/1rules of4each. A favourable native10/12 headline does not describe reverse retention or overall probability quality. The separately fixed [M12 reversal mean](e16-m12-reversal-mean.md) is a distinct exploratory decision rule, not a redefinition of this raw contrast.

## Execution and independent verification

- M12 records4500 attempted/completed backbone calls:1500 START,1500 learning,1500 FINAL;375 attempted/completed updates, zero extra backwards. Audit2.965879s +train/export261.244038s =264.209917s, within Model590s of the total900s grant. The initial `failure-receipt.json` is an incomplete-start sentinel, not the terminal outcome; complete receipt/exits/closure establish success.
- P13 executes one actual v2 fresh reload, three established startup forwards and624 scored presentations:627 attempted/completed, zero extra START/D3/canary/retry/fallback. Conservative Runtime charge44s yields **308.209917/900s**, below its separate310s cap. Unused time grants no work.
- [P13 binding review][runtime] passed223checks. Actual four loading-diagnostic lists are empty; storage/profile/proof records bind the M12 v2 path. This is actual retained reload evidence, not an independent weight/tensor replay or full per-case small-head/stock equivalence proof.
- All624 saved prompt-token hashes, lengths and answer IDs match both original P3 and M8/P6,1248 comparisons, without another tokenizer run. The tokenizer warning is retained; exact correspondence on these inputs does not prove general harmlessness.
- Timing is approximately42.5s: the inspected saved outer-publication event is42.496176875s; Runtime's later handoff states42.496509959s, not located in the inspected receipts. Both use the same44s conservative charge; no controlled speed comparison is claimed. Recorded process groups were absent.
- Model lifetime RSS3,370,532,864B /sampled MPS driver2,772,107,264B /minimum recommended headroom16,297,558,016B satisfy its16GiB/16GiB/2GiB guards. Runtime separately satisfies8GiB RSS/driver and2GiB recommended headroom. These overlapping sampled scopes are nonadditive, not continuous peaks or free physical RAM.
- Independent quality review checks all17raw contexts,11,356 orientation units,5,678 pair units,10,688 contrasts and6,885 regression rows,144 retained bundle/report copies and163 preparation-copy records. All16old contexts remain unchanged. Exact covered/uncovered scopes are explicit; no substantive discrepancy was found.

Owner caught two descriptive `final-entrypoint-*` preparation metadata basenames conflicting with the unchanged reserved-path guard **before execution**. Byte-identical safe-name copies, a fresh191-pin integrity seal and `execute_e15_v2.py` changed only the selected seal filename; all800 scientific dependencies and original files remain. The copied seal's descriptive entrypoint text still names the earlier script, while actual execution and pinned v2 bytes are explicit. There was no failed scoring run or relaxed guard.

[Exact executed recipe](../../configs/evaluation/e15-m12-v1.json) · [publication index](../../manifests/evaluation/e15-m12-report-v1.json). No tests/lint, new dependency, extra inference, final/D7 access or additional actual/pending spend. Packaging checks establish buildability, not scientific correctness or software-test evidence.

[train]: ../../artifacts/evaluation/e15-m12-control-review-v1/findings.md
[quality]: ../../artifacts/evaluation/e15-quality-review-v1/findings.md
[runtime]: ../../artifacts/evaluation/e15-p13-binding-v1/findings.md
