# D5 — verified TRAIN schedule/fit findings; no inferred root cause

## 1. Recorded identity and remapping are correct

Independently joined all **1,500 original TRAIN rows from9hash-pinned v2shards** to the materialized schedule, both fit files and online IDs/indices. Every TRAIN ID occurs exactly once; no missing/duplicate/unknown/nontrain row or index mismatch. Original state/question/schema and option ID→text maps are unchanged; each option order is a bijection. Saved target IDs equal original labels and remapped positions equal lookup **by option ID**. Retained family/group/provenance also match. **Zero mismatches.**

Target slot changed for1,096rows and stayed for404. Actual arities:2→1row,3→394,4→1,035,5→56,6→14. Declared Random(42) row/option shuffle replay matches. Both fit files' recorded agreements reconcile with original remapped targets. Online rows retain ID/index/update/CE only: no independently recorded online option mapping to verify. This audits materialized records, not all training implementation semantics or original label truth. Prompt token-to-text semantics were not independently reconstructed.

## 2. Exposure is interleaved, not contiguous family blocks

All375updates contain exactly4recorded presentations. Families each have500rows; maximum contiguous runs are intent6/rules7/sentiment7. First100 family counts(intent,rules,sentiment)=38/32/30; last100=34/38/28. Updates contain1/2/3distinct families in20/191/164cases. Eight updates repeat an exact group ID;367contain4distinct groups. Exact-group maximum run is2. There are880declared group IDs, with heterogeneous singleton/scenario/mechanism meanings—not880independent mechanisms.

Producer-namespace prefixes (nine, not exact provenance.source identities) have maximum run5; their definition and all exact source aliases/early-late windows are retained in `order-audit/`. These observations neither prove ordering harmless nor establish an ordering cause. No reshuffle or rerun is proposed as a repair on this evidence.

## 3. Saved CE/argmax do NOT identify full ties or probability vectors

Model confirmed, and Data inspected, that fit files retain CE/target position/argmax/option IDs—not full probabilities or logits. Thus aggregate actual Brier/entropy/top-two margins and exact TRAIN tie counts are unavailable. First-position argmax for1,500rows is not itself evidence of ties.

| Same1,500TRAIN presentations | Before | After | Uniform comparator |
|---|---:|---:|---:|
| Agreement |805(53.6667%)|431(28.7333%)|Random expected404.1167(26.9411%)|
| Mean CE |1.357723629|1.390592028|1.322382806=mean ln(k)|
| Mean Brier |Not retained|Not retained|0.730588889=mean(1−1/k)|

Deterministic uniform **first-tie** agreement is separately431/1,500, identical to after's agreement because after always selects position0. That numerical equality is not a tie finding. Official receipt statistics and relevant file hashes reconcile; owner independently cross-checked the headline arithmetic.

Under the recorded **unsmoothed CE** interpretation, targetp≈exp(−savedCE). All1,500after rows have |CE−ln(k)|>0.01nat, so their saved target scores contradict exact uniformity, subject to this interpretation/precision. This does not recover other probabilities. Across distinct4-choice inputs, after target-position0 probabilities range about0.403916–0.408514 and position1 about0.150577–0.154238; these are narrow position-conditioned target-score ranges, **not a reconstructed common vector or proof that input is ignored**.

At least **140after rows are conditionally certified strict winners**:139correct targets have derivedp>0.5; the sole binary row additionally has targetp≈0.2707995 and its other optionp≈0.7292005, so its wrong first-position winner is strict (derived margin≈0.4584009). Binary complement is identifiable from that same row; no cross-row vector pooling was used. Tiedness of the other1,360rows remains unresolved; no exact tie count is claimed. See `binary-identifiability-addendum.json` for the sole binary TRAIN ID and conditional derivation.

## 4. Family patterns matter

Each family has500rows:

| Family | Agreement before→after | Mean CE before→after |
|---|---:|---:|
| Intent |442→140|0.396153→1.391938|
| Rules |184→154|1.657126→1.335713|
| Sentiment |179→137|2.019892→1.444126|

Agreement falls in allthree. CE worsens forintent while improving forrules/sentiment; allthree after-family CE means still exceed their appropriate uniform baselines. Overall CE increases0.0328684. Detailed source/group/arity/position cells,18arity-position spread tables and fixed exposure windows are preserved. These are TRAIN label-agreement statistics, not held-out quality/calibration or causal attribution.

## Exact bindings and evidence

Root: `/Users/destiner/Code/jeff/artifacts/data/d5-20261111T161610Z/`

- `schedule-audit/report.{json,md}` +`audit.py`: all1,500row-level mapping evidence,17input hashes unchanged before/after, source manifest/shard bindings.
- `fit-audit/report.{json,md}`,`analyze.py`,`SHA256SUMS`: retained-scalar analysis and official receipt reconciliation.
- `order-audit/`: reproducible order/update analysis and complete runs/windows/groups/updates evidence.
- `owner-crosscheck.json`;`binary-identifiability-addendum.json`.

Authoritative Model files under `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/`:

- `train-audit/schedule.jsonl`: `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`
- `training/fit-before.jsonl`: `d13d8602294732339056781f1148426be1ef3003b9b8ce9bc833142ecdd83312`
- `training/fit-after.jsonl`: `a099822f30a234b0b3d2ff588888d712897bf5b1af4cbb878369cc23e619ca84`
- `training/receipt.json`: `893c6a1b154734133d49ce41036a05bef2b5830c3615070b3547d56aebff1657`
- Original v2manifest: `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`.

## Bounded recommendation / unresolved questions

No recorded TRAIN coverage/remapping defect or whole-family-block schedule is demonstrated. Do not relabel, change data or silently repair the schedule based on this result. “Everyargmax is0” must not be reported as “allties/uniform”; retained CE supplies contrary evidence to exactuniformity, but not full TRAIN-vector characterization.

Optimizer/gradient/executed-readout diagnosis remains Model-owned; Data did not duplicate that source review. Preserve the negative run, keep P4/E6 unchanged, and let Evaluation report its own aggregate development ties/margins from already-retained outputs if relevant—not as a substitute for missing TRAIN vectors. No new model call, training repair or evaluation gate is requested. Any future authorized run could retain full TRAIN candidate scores to close the telemetry gap; do not fabricate them retroactively.

No weights/model loads, training, dataset/label/frozen-artifact edits, private validation/probe/final content, tests/lint, dependencies, paid calls or uploads. Three bounded Data subagents completed. £0additionalactual/£0pending. D4 remains closed; this is the separately authorized D5 diagnosis.
