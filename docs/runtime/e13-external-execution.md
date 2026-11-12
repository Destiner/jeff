# E13 external execution — 2026-11-12

E13 native execution is closed. This is a retrospective runtime publication from existing release metadata, not a quality assessment, calibration claim, promotion, replay authorization, or whole-native-binary certification. No new scoring or native execution was performed for this report.

## Executed phases

| Phase | Frozen source | Predictors | Whole outer wall | Conservative charge |
| --- | --- | --- | ---: | ---: |
| First exploration | `490277de5b40f3c275ec7b3ba427722b1a006257` | P3, M7, MSMARCO-START, M9 | 44.02 s | 46 s |
| Locked confirmation | `f1fee32df63ac4bb359e09e63c93fb7f358b82f1` | P3, M7, MSMARCO-START, M9 | 43.46 s | 45 s |
| Later exploration | `0d2edfe499ed1d45c5835efae54b95655c3a8771` | M10, M11, M12, p12-nli | 50.66 s | 52 s |

Each four-predictor batch reports 1,600 scored presentations, 3,200 probabilities, six startup forwards, and 1,006 physical native calls. The exploration population comprises 200 cases (100 COPA and 100 Wino), paired native/reversed order with K=2. All eight exploration predictors total 3,200 presentations, 6,400 probabilities, 12 startup forwards, and 2,012 physical native calls. Confirmation uses a **separate** 200-case population; do not pool its cases with exploration or treat presentations as independent cases.

Delivery summaries and batch receipts report exit zero, successful members, cleanup complete, native process groups absent, and exact parent/worker argv absent. These are historical receipt assertions, not a new process inspection. Each predictor had one fresh process/load, without retries. Member elapsed values are scoped around publication and are not summed as whole-batch duration. Group RSS is sampled, not a continuous peak.

## Cohort and timing qualifications

All times below are UTC on 2026-11-12. The confirmation cutoff was 06:30; the FOUR RAW / ZERO OPTIONAL lock record was written at 06:32:54. No Evaluation quality had been received by the cutoff. The later exploration quality could not change that cohort. There were no means, optional confirmation predictors, retries, or unselected confirmation outputs.

First-four source readiness was recorded at 06:18:49, but actual handoff was 06:21:24. That gap remains; the M9 batch notice arrived after return because of a polling gap. First exploration delivery metadata is timestamped 06:29:15.726481.

Confirmation source `aa98527e085b3f4871f4dbbf29f666fb43fd6e8d` was ready awaiting approved inputs at 06:55:27. Registering the four approved literal descriptors produced `f1fee32df63ac4bb359e09e63c93fb7f358b82f1`, ready at 07:00:59, without executable code changes. Actual activation was `35408451-4b31-4dee-85b1-ddac0e586dbc`. Actual execution ended around 07:08 and direct delivery preceded quality at 07:33; the persisted delivery summary is timestamped 07:09:26.742955. Do not equate readiness, execution end, direct delivery, and summary publication.

Later exploration readiness was recorded at 07:21:17; its delivery summary is timestamped 07:32:35.223679. Earlier preparation readiness still lists then-open blockers; those historical records are not rewritten as uninterrupted readiness.

## Authority, resources, and source boundaries

Exploration consumed a conservative 98/1,200 seconds, leaving 1,102 unused. Confirmation consumed 45/900 seconds separately, leaving 855 unused. Unused time confers **no further authority**. Actual outer wall durations are separate from conservative charges. All paid spend is £0.

The supplied source-preparation bounds/accounting are 30 initial minutes spent, 10 first-four minutes spent, 20 confirmation minutes allocated, and approximately 15 later-exploration minutes spent. This is not a fabricated minute-by-minute log or evidence of uninterrupted attention. Actual handoff/polling gaps remain disclosed.

Each phase used its exact four-file allowlist. Confirmation approval covered only the four approved final consumer files, not directories, sibling files, references, or any other final access. This publication read release summaries/readiness/receipts only, not confirmation inputs, prediction files, references, private folders, model weights, or tokenizer assets.

Exploration consumer source versions were being integrated into main; the distinct frozen `f1fee32` confirmation worktree remains retained, not unified or replayed. This report changes neither executed source nor evidence. The later native NLI path has prospective correct 308 guard checks; that does not retrospectively repair the old P12 missing recommended-headroom guard. Old P12's 624-presentation evidence remains qualified.

## Canonical evidence and quality boundary

Canonical root: `/Users/destiner/Code/jeff/artifacts/release/`. For each phase, the manifest links the existing `delivery-summary.json`, `execution-01/batch-receipt.json`, member `*.process-receipt.json`, and readiness records:

- `e13-exploration-20261112-01/`
- `e13-confirmation-20261112-01/`
- `e13-later-exploration-20261112-01/`

The [small publication manifest](../../manifests/releases/e13-external-20261112.json) records source pins, counts, authority limits, and closure digests. Model closure digests below are supplied provenance, not newly verified closure-file hashes:

- `e13-confirmation-return.json`: SHA-256 `6bfcfd29410d45eda94b4ea741d1d88d87e30941659f8c086ce355b8426bd44e`
- Later-exploration closure: SHA-256 `d9491962b360a1cd4850376a71bae247ab2551a8651b073feca37d1faeb0d567`

Quality belongs to Evaluation: `artifacts/evaluation/e13-confirmation-public-v1/report.md` and `artifacts/evaluation/e13-confirmation-public-v1/summary.json` are the only explicitly permitted aggregate-quality links. Neither was read for this runtime publication. Arithmetic review was pending at the supplied 07:33 snapshot; no later public resolution was checked. Runtime success does not resolve quality failures, establish generalization/calibration, or authorize promotion. All earlier failures and qualifications remain.

## Publication verification

Only this document and the named small manifest are owned by this publication. Packaging is checked with `UV_OFFLINE=1 uv build --no-sources`; a successful build is packaging evidence only. No tests, lint, network, imports of ML/tokenizer/model code, new experiment, source engineering, or main merge is part of this work.
