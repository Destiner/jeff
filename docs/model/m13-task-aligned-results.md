# M13: task-aligned M9 warm-start

## Decision

The sole fixed endpoint and its fresh-process scoring are complete. Independent reserved-set/retention acceptance is pending; **M9 remains the serving default**. Training fit is not the promotion criterion. No further training, alternative initializer, checkpoint selection or retry is authorized.

The [frozen plan](m13-task-aligned-plan.md) and [Research diagnosis](../research/final-transfer-diagnosis.md) distinguish task coverage from a proven scoring bug. M9 was selected for the declared workspace-routing/direct-sentiment tasks, despite original START's ticket/pooled diagnostic advantages and M9's S2 negative-class weakness. The joint decision was frozen at **18:36:52 UTC**, before the reserved64 freeze at18:50:56 and learning at19:21:06 on2026-11-12.

## Exact treatment and initialization

One full-parameter warm-start from the actual trained twelve-epoch M9 checkpoint, not original pretrained START. All105 initial parameter hashes matched the pinned M9 run's **weights.after** before updates. The retained ranking head was not reset; its architecture's `head_initialization=pretrained` describes historical origin, not untrained current weights.

Fresh AdamW, with no optimizer-state resume: backbone LR2e-5, head LR5e-4, weight decay.01, betas(.9,.999), epsilon1e-8. CPU FP32, four intra/inter-op threads, seed42, decision batch4, exactly3 epochs/1,440 presentations/360 updates. No clipping, scheduler, accumulation, early-best selection or numerical rescue. Existing paired actual-LF renderer, pooled scalar classifier, tokenizer, cap256 and T1 remain unchanged.

The final [480-row Data release](../data/final-sprint-v1.md), manifest SHA256 `4c41158e48c5546b6489bc4887ddedcd0dcbf8c8af36ed744fa8d41f7efb9634`, contains:

- 240 fresh TRAIN examples:80 workspace routing,80 direct sentiment,80 software-ticket intent.
- 240 exact original-v2 TRAIN replay rows:80 intent,80 sentiment,80 rule_application, selected by the frozen family/ID hash rule.
- 294 recorded groups, not294 independently sampled mechanisms;400 teacher-based and80 rule-verified labels. Same-family AI review agreement is not human truth. Qualified exclusion screening is not proof of zero semantic leakage.

Earlier120/120 replay candidates and exposed-ID/class-cycle review histories remain preserved. Model used only the selected release. Its sole tokenizer-only preflight loaded one tokenizer and checked480 decisions/1,858 untruncated pairs, **42–113 tokens including special tokens**, all within256. No weight load or model forward occurred in that stage; no candidate/repeated cap pass was performed.

## Training and fixed TRAIN fit

Learning ran19:21:06.344479–19:22:11.521488 UTC, parent/child exit0, with exactly360 updates and three complete epochs. All105 parameter tensors' hashes changed. The durable first-update-attempt marker was retained. Online training mean cross-entropy was.6968250153/.4407898995/.2990772142 across the three epochs; these changing-model/dropout observations are not fixed-endpoint validation scores.

A single subsequent fresh-process reload scored the fixed480 TRAIN rows once, alongside separately exported reserved and retention suites. Saved TRAIN vectors were validated before arithmetic and divided by their own sums for NLL/Brier. Ties choose the first input option.

| TRAIN subset | Target agreement | Mean NLL | Summed multiclass Brier |
|---|---:|---:|---:|
| All480 |466/480|.103207|.054182|
| Fresh workspace |80/80|.012053|.001466|
| Fresh sentiment |77/80|.091456|.046127|
| Fresh tickets |79/80|.141184|.063630|
| Original replay |230/240|.124849|.071289|
| Combined intent family |239/240|.051994|.021763|
| Combined sentiment family |157/160|.046538|.023160|
| Replayed rule family |70/80|.370182|.213480|

Family rows and shard rows are overlapping summaries, not independent samples. There was **no initial M9 pass on this480-row mixture**, so this table does not establish a before/after fit gain. Fourteen TRAIN errors remain. Neither fit nor declining training loss establishes transfer, calibration or mastery.

## Fixed evaluation and current acceptance

The prospective rule is [Evaluation's final-sprint plan](../evaluation/final-sprint-plan.md):32 primary choices/30 single-acceptable proper-score cases, with two uncertain sentiments retained; tickets and transfer remain separate. Both primary domains, both proper scores, the240-row reused-development retention guard and compatible deployment must satisfy the unchanged conjunction.

- One fresh M13 load:480 TRAIN +64 reserved native +240 retention native =784 decisions,3,034 probabilities,196 batch4 BERT forwards.
- One fresh M9 load:64 reserved native,256 probabilities,16 forwards. Its saved240-row retention baseline is reused, not rerun.
- Zero startup/canary/reversed calls. All suite boundaries are multiples of4; the original reserved/retention byte blocks are preserved, IDs are unique and outputs are split without reserialization or repair.
- Exact ordered input/options/output coverage and finite[0,1] values passed. Maximum raw sum deviations: M13 `1.2548571248771623e-7`; M9 `8.940696716308594e-8`.

Evaluation-only case-level outputs were delivered at19:28:53. Model did not inspect private references or duplicate held-out quality arithmetic. Operational completion is not yet a scientific or deployment pass.

## Source, artifacts and operating evidence

Actual execution source: **`3cc10dbaea93592841e28fafe126f97f73145dc1`**, clean `.worktrees/model-final-sprint`. Initializer source/plan integrated as `a0c22164065e6ed3a3fbf24598926e3db306b8be`; later reporting commits are not retroactive execution provenance. The scoped trainer change preserves the default original-START path and binds explicit M13 initialization to the actual M9 reference. Artifact-local CPU guards preserve the existing durable marker/finish interface; a metadata-only environment adapter avoids explicit MPS telemetry. Numerical training and prediction code otherwise remains unchanged.

Canonical root: `artifacts/model/final-sprint-20261112-01/`. Public operational records are `learning-return.json`, each stage's `return.json`, `endpoint-ready.md`, and `train-fit-summary.json`. Private-case locators embedded in receipts do not extend access permissions. Final checkpoint: `learning-01/run01/training/checkpoint/`:

- `checkpoint.json`: SHA256 `e8fa2393137263f40c984149eff6b86a1fcae581a5e06bfbe207c6cb01f57e20`.
- `encoder/model.safetensors`:90,866,412 bytes; SHA256 `5433cde7023f25fbda2cc6e7ff59149c4e8ba1e5a296a514b4dd5fb12bd8f629`.

Encoder config, vocabulary, tokenizer.json and special-token bytes match M9. Serialization added explicit right-padding/right-truncation, stride0, pad-token-type0, longest-first and max_length256 fields to tokenizer_config.json. Do not claim all checkpoint files are byte-identical or general tokenizer equivalence. Embedded checkpoint `metadata.run.status=running` remains historical; standalone run/native/parent receipts and actual fresh reload establish separate completion evidence. No tensor/update replay was performed.

| Native stage | External seconds | Conservatively charged |
|---|---:|---:|
| Final tokenizer preflight |5.29|7|
| Sole learning |65.19|67|
| M13 fixed fresh-load scoring |8.97|10|
| M9 reserved64 |2.14|4|
| **Total** |**81.59**|**88/1,200 closed**|

All parent/child PIDs and process groups were independently checked absent before successors. Maximum training lifetime RSS1,864,335,360 bytes and sampled group RSS1,854,930,944 bytes are distinct, nonadditive scopes; every observed pressure sample was1. These are sampled limits, not continuous peaks or real-time guarantees. Child/parent deadlines, TERM/KILL cleanup and partial/failure preservation remain in the frozen scripts. No native failure/retry occurred. The initial packaging command used a nonexistent uv location and exited127 before a build; the corrected existing uv path produced passing offline branch/integrated wheel and sdist builds. No dependency, tests/lint, external spend or old protected-data access was added.

## Separate SDK context

The actual packed M9 SDK online proof completed six calls with independent saved-output parity:24 probabilities, max drift `8.8668822495474586e-7`, six matching choices, three detailed cases/1,668 exact token integers. Plain-call token matrices are unavailable. A pre-browser timer-budget wiring failure was retained and narrowly repaired before any model contact; total6/300 seconds charged. The optional new-graph server-unavailable phase was **unattempted** after late stop-notification pickup missed its fixed start cutoff. Cache readiness, a stopped server and historical B2 evidence do not repair that gap. This proves the packed proof-consumer scope, not automatic production queue/chat or M13 deployment acceptance.
