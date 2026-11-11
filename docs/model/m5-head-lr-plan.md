# M5: one historical-M3 scalar-head learning-rate control

Authorized by lead mailbox task `07ac3cf8-6dbf-4646-82f4-47091b0ff733`, after completed M4. This is a new single-factor control, not a replay of completed M3 or v2 training. Preserve all prior candidates and the default.

## Hypothesis and fixed criterion

Hypothesis: the historical retained pretrained head's25× learning-rate multiplier contributes to lost probe rankings. Change **only scalar classifier LR5e-4→2e-5**; encoder and native pooler remain2e-5. This does not isolate the broader data-construction/pretraining hypotheses.

Use Research R4 section4 and Evaluation E4's predeclared full conjunction:

1. Recover at least one of `eval.validation.sentiment.03`, `.sentiment.04`, `.rule_application.02` versus historical trained M3.
2. Introduce no new probe error relative to historical trained M3.
3. Reduce equal-source-group macro probe log loss, interpreting12unique groups rather than24presentations.
4. Pilot mean loss≤0.8437008119799213 (historical0.7937008119799213+0.05).

Report every group/rank/probability/margin and the whole criterion, including failure; no cherry-picking or automatic promotion. Tiny reused development references, teacher labels and single-seed MPS variation prevent a general or causal certainty claim.

## Frozen controls

- Historical implementation `e37b0f3e7f2e3162abca87a76883eb81300603e0`; fresh retained-head `cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`, unchanged tokenizer/format/pooling/dropout/temperature1.
- Frozen pilot-v1 manifest SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`;300train/60validation. No data or label change, no probes/derivatives in training.
- Seed42,batch4,cap256,3epochs/225updates/900presentations,full fine-tuning,AdamW decay.01,betas(.9,.999),eps1e-8; no warmup/scheduler/clipping/early stopping. Historical `max_steps` stays null.
- Same MPS/fourthreads, Python3.12.16,Torch2.15.0,Transformers4.57.6. Existing cache, offline flags; no new packages/model download or paid work.
- Relevant current trainer/model/package/lock source bytes equal historical M3. Run from the current clean owner checkout with newer Git provenance, retaining a source-equivalence receipt instead of resetting main or recreating the owner worktree. Matching metadata/lock cannot establish historical installed binary identity or deterministic MPS execution.
- Exactly **one training invocation**, fresh immutable `artifacts/model/m5-head-lr-20261111-01/training/`; failure preserved, no retry/sweep. Five-minute supervised bound given historical25second runtime. No additional optimization experiment authorized.

Before interpreting outcomes, compare all105 initial parameter-record hashes/retained-head provenance and fresh baseline predictions with historical M3. Pin checkpoint bytes before and after fresh-process inference. Use existing E4 label-free60pilot and24probe inputs; historical prediction batch8, fresh offline starts and trained snapshots. Evaluation owns independent scoring; historical M3/M2 predictions are reused, not rerun.

Actual source/environment/command/output records live under the run root. Reference settings: `configs/model/msmarco-pilot-256-low-head-lr.json` (not automatically CLI-loaded). No tests, linting, final-data access, new dependency, dataset repair or v2 training. £0 allocation/actual/pending additional spend.

## Subsequent inference-only queue

After M5, fulfill E4's frozen D3 label-free requests using the **four existing M4 snapshots**. D3 is validation-only, seen-mechanism/new-policy diagnostic data; no diagnostic training or mixing with unseen-mechanism v2 evidence. Release's bounded runtime work needs an explicit Model slot; M5 has priority. Self-review/build/integrate only owned files under the shared merge lock, then report through the mailbox.
