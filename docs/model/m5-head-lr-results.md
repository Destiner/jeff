# M5: historical-M3 scalar-head LR control

## Result

Exactly one fresh retained-head run lowered scalar-head LR from5e-4 to2e-5; encoder and native pooler stayed2e-5. **The predeclared R4 conjunction fails: probe group-macro log loss worsens**, despite higher probe agreement and acceptable pilot loss. This does not establish the broader cause of M3's failure or rule out all head-adaptation effects. No retry, sweep or default promotion; M2, M3, M4 and M5 candidates remain preserved.

Independent E4 comparison uses the same pilot60/12source groups and probes24presentations/12unique groups. Cells are reference-label agreement / log loss, not wholly independently verified accuracy.

| Snapshot | Pilot60 | Probes24 |
| --- | --- | --- |
| Historical M3 / M5 fresh pretrained start |30 /1.026878|14 /1.453783|
| Historical M3 trained, head LR5e-4 |40 /0.793701|8 /1.360701|
| **M5 trained, head LR2e-5** |**40 /0.794525**|**10 /1.384773**|
| M2 trained (descriptive context only) |35 /0.855288|16 /0.710407|

All seven compared predictors have complete valid coverage. E4's full criterion result:

- **Recovery passes:** `eval.validation.sentiment.04` recovers in both orders; 1 of 3 eligible lost groups recovered.
- **No-new-error passes:** zero newly wrong probe groups relative to historical trained M3.
- **Probe-loss condition fails:** all 12 groups retained; macro loss rises from 1.360701041245408 to 1.3847732520228302 (+0.024072211).
- **Pilot-loss condition passes:** 0.7945249517640895 is below the fixed ceiling 0.8437008119799213; agreement remains 40/60.

Probe agreement improves from 4 to 5 of 12 unique groups (8 to 10 of 24 presentations), but one recovered rank is insufficient for the conjunction. E4 displays both presentations, ranks, target probabilities and signed margins for every group in `artifacts/evaluation/e4-m5-result-v1/{result.json,report.md}`. Criterion and fixed controls were recorded before outcomes in [the M5 plan](m5-head-lr-plan.md).

## Historical equivalence, without resetting the workspace

- Historical implementation: `e37b0f3e7f2e3162abca87a76883eb81300603e0`; actual clean execution revision: `4031e7e9d371f15a53c3bae9d5db14478ace6fdb` in the adopted `.worktrees/model`.
- Ten relevant model/training/package/lock files are byte-identical to historical source. All four source hashes in the original run match. Current Git provenance differs through unrelated repository changes and the preregistration; no active workspace or main reset was needed.
- Frozen pilot-v1 manifest SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`, all6shards verified:300train/60validation. No data/label change.
- Model/tokenizer `cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`, native pooler/dropout/pretrained scalar head retained, no head reset. Historical cap256, batch4, seed42,3complete epochs/225updates/900presentations; `max_steps=null` unchanged.
- AdamW backbone/pooler LR2e-5, scalar-head LR2e-5, decay.01, betas(.9,.999),eps1e-8,temperature1; no scheduler/clipping/early stopping. Config differs only in head LR and required output directory. Optimizer record differs only in head LR.
- All105initial parameter-record hashes, base metadata, retained-head provenance and initial trainer validation metrics match historical M3. These are recorded hashes, not an independent tensor decode.
- **Fresh baseline predictions are byte-identical** to historical M3 on all60pilot and24probe inputs, with maximum per-option difference0.0. Original prediction SHA256 `cef650f002f9a7850c9f913b1e1d8dc169cc1b03db4a08ae10fafdf0a4935eb0`; probes `263276ab7578cf62a363b6e4aec8f7510f532d30840b84d5cfc1cdb8bf12ef95`.

Python3.12.16, Torch2.15.0, Transformers4.57.6, tokenizers0.22.2, safetensors0.8.0 and huggingface-hub0.36.2 match recorded historical versions; MPS/fourthreads/AppleM5/24GiB unchanged. Matching sources, lock and metadata do not prove historical installed-binary identity or bitwise deterministic MPS training. A single new run versus a historical control is not causal certainty.

## Execution and preservation

Run root `R=/Users/destiner/Code/jeff/artifacts/model/m5-head-lr-20261111-01/`:

- `training/{baseline,checkpoint}/`: complete local safetensors/tokenizer snapshots; `training/run.json` contains exact argv, hashes, configuration, changed weights and resources. All105parameter tensors changed.
- Head-weight L2 movement0.007149 versus historical0.158269; embedding-weight movement0.244028 versus0.245790. Smaller head movement is expected and **not itself the success criterion**.
- `preflight.json`, `initial-control-comparison.json`: source/data/runtime and starting-state checks.
- `inference/{baseline,checkpoint}-{original,probes}-predictions.jsonl`: four separate fresh offline processes, historical inference batch8,168total output rows, all exit0.
- `inference/receipt.json`, per-job invocation/completion receipts and `starting-prediction-comparison.json`: exact input/output hashes, initially empty unique HF_HOME, commands and start comparison. Before-inference inventories pin7files per checkpoint; recorded equality checks and read-only review confirm unchanged bytes afterward. No separate post-inference inventory snapshots are claimed.
- `prior-preservation.json`:69inventoried prior files remain unchanged (39M2/M3 complete-run files plus30M4 checkpoint files). Original M4 inventory was post-inference; this verifies subsequent preservation.
- `infer.py` and `logs/`: actual fixed queue and execution output. [Compact record](m5-head-lr-run.json) pins the above evidence. These are records, not authorization to repeat the completed run.

Training elapsed18.326s through checkpoint saves, before run-record write. CPU process-lifetime high-water RSS1,369,014,272bytes; endpoint MPS current370,411,008 /driver2,256,502,784bytes. These are **not accelerator peaks**, and must not be added into a peak unified-memory claim. Four prediction process walls total7.106s, including startup; not per-example latency.

E4 independent pipeline outputs: `artifacts/evaluation/e4-m5-comparison-v1/{pilot,probes}/comparison.json`, adjacent reports and probe-order reports. Model supplied exact existing Evaluation inputs, did not rebuild a scorer, and did not rerun old comparison snapshots. Pilot labels40teacher/20rule_verified; probes24teacher with unknown curator. Reused development groups, one seed, narrow constructions and correlated pairs limit generalization/calibration claims. Final data remains sealed; no tests/lint, new dependencies, dataset edits or additional spending. £0actual/pending/allocation.

## Inference-only follow-through

D3 is a separate validation-only seen-mechanism/new-policy diagnostic. E4's released label-free request is now delivered:96 original cases through each of the four **existing M4** snapshots, with fresh-process receipts and unchanged checkpoint inventories. See [D3 inference](d3-inference.md). No new training or diagnostic-based tuning; keep its results separate from v2 unseen-mechanism validation and these probes. The M5 training allocation remains exhausted.
