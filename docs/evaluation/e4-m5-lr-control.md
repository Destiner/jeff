# E4 Track A — historical M3 scalar-head LR control

**The fixed conjunction fails.** M5 recovers one of three lost probe groups with
no new error, and preserves pilot loss within tolerance, but **all-group probe
macro log loss worsens**. This does not support lowering head LR as a sufficient
robustness repair under the declared criterion. No model/default is promoted.

This is the one authorized historical-M3 control, not a repeat of M4 training.
D3 seen-mechanism diagnostics are a separate E4 track and are not pooled here.
The intervention comparator is historical trained M3; M2 is descriptive context only.

## Frozen question and control evidence

Research [R4 section4](../research/m3-pilot-probe-diagnosis.md) and lead E4 fixed
one intervention: scalar-head LR **5e-4→2e-5**, encoder/native-pooler LR still
2e-5. Evaluation pinned the exact criterion before M5 outcome access at
2026-11-11T13:05:27Z in
`artifacts/evaluation/e4-m5-preregister-v1/criterion.json`.

A fresh independent reviewer passed 92 source/control/integrity checks:

- Historical relevant source at `e37b0f3` and recorded M5 source `4031e7e` are
  byte-equivalent for ten training/model/package/lock files. Entire repositories
  differ; no active checkout was reset to historical source.
- Same pilot-v1 manifest `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`
  and six shards, train order/seed42, pretrained retained-head model/revision,
  tokenizer/format/cap256, batch4, full tuning, three epochs/225updates/900
  presentations, AdamW/dropout/temperature1, MPS/four threads and recorded
  Torch2.15.0/Transformers4.57.6 runtime. No max-steps flag was added.
- Config differences are exactly head LR and new output path. All105 initial
  parameter-record hashes match; those were compared as records, not regenerated
  by Evaluation from tensor arrays. Initial metrics also match.
- Fresh starting predictions are **byte-identical** to historical M3 on pilot60
  and probe24. Four fresh offline inference invocation/completion receipts were
  rehashed, including input/output/command and complete checkpoint inventories
  recorded before and unchanged after each inference job.

The intervention is comparable with explicit qualifications: current rehashing
cannot retroactively observe a process's file reads, and a historical single-seed
MPS run remains vulnerable to stochastic/backend variation. No causal proof or
independently loaded-tensor claim. Model recorded one run; no extra runs authorized.

## Coverage and reference-label results

Pilot: **60 decisions/12groups**, 40teacher plus20rule_verified labels.
Probes: **24 presentations/12unique groups**, all teacher labels, unknown curator
model identity. Each pair is original plus exact reversal, not two independent
cases. These are repeatedly used development references, not untouched final data.

All seven predictors have full valid coverage on both references, with zero
missing/invalid/duplicate/extra/unidentifiable records. Existing historical
prediction files were reused, not reinferred. Table cells: correct/rows; mean
natural-log loss. For these equally sized probe pairs, row and group-macro loss
are numerically equal; the criterion explicitly averages pair losses across12groups.

| Predictor | Pilot60 | Probe24 / 12groups |
| --- | --- | --- |
| Uniform, deterministic first-option tie | 17/60;1.378765 | 8/24;1.055008 |
| Lexical | 29/60;1.323710 | 9/24;1.047044 |
| Historical M3 pretrained start | 30/60;1.026878 | 14/24;1.453783 |
| Historical M3 trained | 40/60;.793701 | 8/24;1.360701 |
| Fresh M5 pretrained start | 30/60;1.026878 | 14/24;1.453783 |
| **M5 low-head-LR trained** | **40/60;.794525** | **10/24;1.384773** |
| M2 trained, context only | 35/60;.855288 | 16/24;.710407 |

| Fixed condition | Outcome |
| --- | --- |
| Recover≥1 of sentiment.03, sentiment.04, rule_application.02 | **Pass:** sentiment.04 correct in both orders;1/3eligible groups |
| No newly wrong probe group versus historical M3 | **Pass:** zero; all four previously correct groups retained |
| Lower all12group macro probe loss | **Fail:**1.360701041→1.384773252 (+.024072211) |
| Pilot loss≤historical exact loss+.05 | **Pass:**.794524952≤.843700812 |
| Full coverage and comparable controls | **Pass**, with recorded historical/single-seed qualifications |
| **Full conjunction** | **Fail** |

Recovery requires each presentation to rank the target first under its own
deterministic tie-break; ranks/probabilities are never averaged to claim recovery.
Full input/pair coverage is a prerequisite, not a conditional
quality denominator. The exact pilot ceiling uses the stored normalized loss
.7937008119799213+.05; rounded .843701 is for display only. No criteria or group
exclusions changed after observing outcomes.

## All12 unique probe groups: rank and probability movement

Each cell is **target rank / p(target) / signed target-minus-best-rival margin /
loss**, on the original presentation. The JSON retains both presentations and
pair-mean loss. Signed margins are not raw logits or top-two confidence. Rank
uses the frozen input order to break exact ties; these neural cases have no ties.

| Group (`eval.validation.` prefix) | Historical M3 trained | M5 low-head-LR |
| --- | --- | --- |
| intent.01 | 1/.682845/+.366630/.381488 | 1/.717299/+.435303/.332263 |
| intent.02 | 2/.121467/−.727541/2.108112 | 2/.119893/−.731471/2.121156 |
| intent.03 | 3/.314050/−.056834/1.158204 | 3/.287107/−.102518/1.247900 |
| intent.04 | 1/.969682/+.948169/.030788 | 1/.968829/+.946879/.031667 |
| sentiment.01 | 2/.438294/−.018742/.824866 | 2/.463801/−.000852/.768300 |
| sentiment.02 | 3/.130976/−.354876/2.032744 | 3/.134177/−.346046/2.008595 |
| sentiment.03 | 2/.491150/−.012360/.711005 | 2/.471571/−.051546/.751686 |
| sentiment.04 | 2/.475148/−.024632/.744129 | **1/.493301/+.010877/.706636** |
| rule_application.01 | 2/.000790/−.998419/7.142956 | 2/.000570/−.998859/7.469238 |
| rule_application.02 | 2/.486317/−.010917/.720894 | 2/.492366/−.002837/.708532 |
| rule_application.03 | 1/.990366/+.984762/.009680 | 1/.991584/+.986714/.008452 |
| rule_application.04 | 1/.629049/+.258098/.463546 | 1/.629485/+.258970/.462853 |

Seven group losses improve, five worsen; all12remain included. The already-wrong
rule_application.01 becomes more confidently wrong, increasing loss by .326282nats; this
outweighs smaller gains. The recovered sentiment.04 has p(target)<.5 because it
wins among three choices. Near-zero negative margins on sentiment.01 and
rule_application.02 are still **wrong**, not partial recovery.

Probe-family agreement/loss, historicalM3→M5:
- Intent:4/8→4/8; .919648→.933246.
- Sentiment:0/8→2/8;1.078186→1.058804.
- Rules:4/8→4/8;2.084269→2.162269.

Probe Brier slightly improves .653598→.652062 while log loss worsens; different
proper scores emphasize different probability errors. Neither descriptive ECE
nor normalized probabilities certify calibration. Source-group tables and all
reliability bins remain in the generated reports; no significance claim.

All neural predictors preserve choice on12/12complete probe pairs without ties.
Baselines' tied-choice effects remain separate from probability movement. M5
pilot reversal inference was not requested; no pilot-order conclusion is invented.

## Pilot rule answer-category result

Reuse R4's preexisting category mapping, not new labels or a post-hoc gate:

| Pilot rule group | No-result targets | HistoricalM3→M5 no-result choices | Agreement |
| --- | ---: | ---: | ---: |
| Reachability g11,10rows | 2 | 9→9 | 2→2 |
| Election g12,10rows | 5 | 10→10 | 5→5 |

M5 retains the19/20no-result preference; all seven correct rule decisions are
no-result targets, **0/13nonempty/winner cases correct**. Lower head LR does not
remove this observed category pattern. Pilot family agreements remain19intent,
14sentiment,7rules, while small loss changes yield the reported total.

## Reproduction and artifacts

All paths below are under `/Users/destiner/Code/jeff/artifacts/evaluation/`:
- `e4-m5-preregister-v1/`: frozen criterion, historical references/predictions,
  starting controls, full historical group tables and rule-category bindings.
- `e4-m5-control-review-v1/`: independent92-check receipt and qualifications.
- `e4-m5-comparison-v1/{pilot,probes}/`: existing compare/render outputs; probes
  additionally have seven order reports. `receipt.json` pins sources/commands.
- `e4-m5-result-v1/{result.json,report.md}`: applied conjunction and every group.
- `e4-m5-execution-v1/{run.py,criterion.py}`: exact executed artifact scripts;
  exclusive output paths preserve this execution rather than overwrite reports.

Tracked criterion/report index: `configs/evaluation/e4-m5-criterion-v1.json` and
`manifests/evaluation/e4-m5-report-v1.json`. The criterion copy preserves the
pre-result artifact exactly. Reproduce the ordinary scorer with a new destination:

```sh
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
uv run --locked python -m jeff.evaluation.compare \
  --examples "$JEFF_ARTIFACTS_DIR/evaluation/probes-v1/validation.jsonl" \
  --predictions "m3=$JEFF_ARTIFACTS_DIR/model/msmarco-256-inference-20261111-01/checkpoint-probes-predictions.jsonl" \
  --predictions "m5=$JEFF_ARTIFACTS_DIR/model/m5-head-lr-20261111-01/inference/checkpoint-probes-predictions.jsonl" \
  --output "$JEFF_ARTIFACTS_DIR/evaluation/<new-E4-reproduction>/probes.json"
```

The execution receipt contains all seven-predictor pilot/probe commands, order
calls and renderer calls; use new output paths. Apply the fixed machine-readable
criterion to all12groups, not only the three recovery candidates. Existing
score/compare/order/render were reused; no new scorer or reporting framework.
Model run/reload evidence remains separate from package builds. Evaluation used
CPU only, £0additional/pending, no tests/lint, no final-data access, no training
or new default. This development result does not authorize a sweep.
