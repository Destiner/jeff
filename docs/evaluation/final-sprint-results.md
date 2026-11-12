# Final-sprint results: retain M9

**Final scientific decision: M13 does not pass the fixed promotion conjunction; retain the existing M9 default.** M13 improves fresh primary choice agreement and both primary proper scores, but fails retained-task probability-quality limits. This is a scientific decision, not acceptance of every application or deployment requirement. Independent final-result arithmetic is complete: **608 saved vectors, 4,664 exact and 1,276 floating comparisons, maximum difference 0, no errors**. The [review](../../artifacts/evaluation/final-sprint-20261112-01/independent-final-review-v1/report.md) and [receipt](../../artifacts/evaluation/final-sprint-20261112-01/independent-final-review-v1/receipt.json) confirm all six gate values below.

The [saved result](../../artifacts/evaluation/final-sprint-20261112-01/final-result-v1/result.json) is the single v2 scoring outcome (exit 0), not a new scoring run by this publication. Admission passed; `scientific_pass=false`; `promotion=not_authorized`. The scorer's saved deployability-pending field is its execution-time snapshot: **M13 deployment is not pursued because its scientific conjunction failed**, not left as an implied export request. The [prospective plan summary](final-sprint-plan.md), [exact frozen rule](../../artifacts/evaluation/final-sprint-20261112-01/promotion-plan-v1.md), and [earlier exploratory diagnostics](final-sprint-diagnostics.md) remain unchanged. No export, retraining, fitted temperature, threshold change, additional recipe or diagnostic success can rescue this failed gate.

## Fresh reserved domains

Each domain has 16 choices evaluated. Proper-score denominators are 16/14/16/16: two ambiguous sentiment judgments remain in **all choice counts**, retaining their acceptable-set uncertainty, and are excluded **only** from proper scores. Primary means use routing + sentiment (32 choices, 30 proper references), not all 64. Values below are M9 → M13; gains/losses are matched preferred-choice transitions, not independent samples. Lower NLL and summed multiclass Brier are better.

| Domain (choice / proper n) | Preferred | Acceptable | Gains / losses | NLL | Brier | Fixed-gate interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Routing (16 / 16) | 12 → 12 | 12 → 12 | 0 / 0 | 1.050891 → .976917 | .460742 → .417256 | Primary domain nonloss and proper nonworsening pass |
| Sentiment (16 / 14) | 9 → 13 | 11 → 14 | 4 / 0 | 1.142487 → 1.013351 | .594688 → .275986 | Primary domain nonloss and proper nonworsening pass |
| **Primary (32 / 30)** | **21 → 25** | **23 → 26** | **4 / 0** | **1.093636 → .993920** | **.523250 → .351330** | All four primary booleans pass |
| Tickets (16 / 16) | 9 → 14 | 9 → 14 | 6 / 1 | 1.448066 → .595036 | .696671 → .282487 | Diagnostic improvement; cannot rescue retention |
| Novel taxonomy transfer (16 / 16) | 7 → 6 | 7 → 6 | 0 / 1 | 1.677480 → 1.864902 | .903686 → .947392 | Diagnostic regression in choice and both proper scores |

The primary gain is exactly the required +4/32 (12.5 percentage points), entirely in sentiment; routing choices are unchanged. Aggregate primary NLL improves by .099716 and Brier by .171921, exceeding the required .02 improvements, with neither primary domain worsening. These are useful bounded adaptation signals, not a broad transfer result. Tickets improve strongly but novel-taxonomy transfer worsens. Even primary aggregates conceal remaining boundary difficulty: routing boundary preferred stays 1/4 while NLL rises 2.909300 → 3.023350; sentiment boundary preferred rises 0 → 2/4 while its two singleton references have NLL 2.246954 → 3.003005. These subgroups are descriptive, not replacement gates.

## Retained tasks: choice tolerance passes, probability quality fails

This is the exact reused new240 **development** cohort, not fresh confirmation. Each family has 80 choice and proper-score cases; preferred equals acceptable throughout. The original saved M9 retention baseline is reused, not rerun.

| Family | Preferred = acceptable | Gains / losses | Net loss | NLL | Brier | Choice / proper gate |
| --- | --- | --- | --- | --- | --- | --- |
| Intent | 78 → 77 /80 | 0 / 1 | 1 | .099739 → .128661 | .036343 → .056908 | Pass / pass |
| Sentiment | 70 → 72 /80 | 4 / 2 | −2 | .399240 → .551815 | .180991 → .181286 | Pass / **fail NLL** |
| Rule application | 17 → 13 /80 | 2 / 6 | 4 | 1.599282 → 2.460728 | .861966 → 1.045416 | Pass / **fail NLL and Brier** |
| **Overall** | **165 → 162 /240** | **6 / 9** | **3** | **.699420 → 1.047068** | **.359766 → .427870** | **Pass / fail** |

Overall net loss 3 is within 6; every family is within 4, including rules exactly at that boundary. But overall NLL increases **+.347647 > .05**, and Brier **+.068104 > .03**. Sentiment's improved choice count does not prevent its **+.152575 NLL > .10** family failure (Brier +.000295 passes .05). Rules worsen **+.861446 NLL > .10** and **+.183450 Brier > .05**. Intent's +.028921 / +.020566 pass family limits. Thus modest choice retention masks consequential probability-quality deterioration; the observed tradeoff is sufficient to reject promotion without asserting a causal mechanism or calibration failure diagnosis.

### Exact six scientific gate booleans

| Saved field | Value | Frozen requirement |
| --- | --- | --- |
| primary_choice_gain | true | Preferred gain ≥4/32 |
| primary_domain_choice_nonloss | true | Preferred and acceptable nonloss in each primary domain |
| primary_proper_gain | true | Primary NLL and Brier each improve ≥.02 |
| primary_domain_proper_nonworsen | true | Neither score worsens in either primary domain (1e-12 comparison tolerance) |
| retention_choice | true | Net loss ≤6 overall and ≤4 per family |
| retention_proper | **false** | Overall increases ≤.05 NLL / .03 Brier; every family ≤.10 / .05 |

## Learning, reload and evidence strength

The sole M13 completed **three epochs, 360 updates, 1,440 presentations** on 480 released TRAIN rows (240 fresh: 80 each routing/sentiment/tickets; 240 original-TRAIN replay: 80 per old family). It warm-started the trained M9 backbone and head, full-model CPU FP32 with four threads, seed 42, batch 4, fresh AdamW, backbone LR 2e-5, head LR 5e-4, weight decay .01; no optimizer-state restore or endpoint selection. [Release binding](../../artifacts/evaluation/final-sprint-20261112-01/release-binding-v1.json) records byte identity to screened candidate shards. Qualified source-bound exclusion is not exhaustive semantic independence or zero-leakage proof.

[Learning review](../../artifacts/evaluation/final-sprint-20261112-01/m13-learning-binding-v1/report.md) and [receipt](../../artifacts/evaluation/final-sprint-20261112-01/m13-learning-binding-v1/receipt.json) support source/metadata consistency, including 105 initializer records matching M9's after records, not independent tensor reconstruction. The standalone run is completed; checkpoint-embedded run status remains stale **running**, explained by serialization order and not repaired. Tokenizer config gained seven serialization keys; other reviewed small assets match, but **not all tokenizer bytes are identical**, nor is universal behavioral equivalence established.

[Inference review](../../artifacts/evaluation/final-sprint-20261112-01/m13-inference-binding-v1/report.md) and [receipt](../../artifacts/evaluation/final-sprint-20261112-01/m13-inference-binding-v1/receipt.json) record a fresh M13 checkpoint load with **784 decisions / 196 native forwards** (480 TRAIN + 64 reserved + 240 retention), followed by a fresh M9 load with **64 / 16**; **zero startup forwards**, one saved-checkpoint load each. No extra/reverse cohort is asserted beyond that reviewed scope. Successful recorded process-group closure and sampled guards close the native ledger at **88/1200 charged seconds**; unused time is closed authority, not a new allowance. Learning sampled group RSS peaked at 1,854,930,944 bytes, native lifetime high-water at 1,864,335,360; pressure samples were [1], not continuous group-peak certification.

Online epoch TRAIN losses .696825 → .440790 → .299077 were accumulated while weights changed, not fixed-checkpoint fit. The separately adopted [Model fixed-TRAIN aggregate](../../artifacts/model/final-sprint-20261112-01/train-fit-summary.json) reports **466/480** final label agreements, NLL **.103207**, Brier **.054182**: fresh routing 80/80, sentiment 77/80, tickets 79/80; replay 230/240, including rules 70/80. No initial M9 fit on this exact 480-row mixture was run, so this is not a measured fit gain. These TRAIN results were not duplicated by Evaluation's independent held-out/retention arithmetic and cannot override its decision.

## Separate M9 SDK portability outcome

[Saved arithmetic](../../artifacts/evaluation/final-sprint-20261112-01/sdk-online-comparison-v1/report.md) ([result](../../artifacts/evaluation/final-sprint-20261112-01/sdk-online-comparison-v1/result.json)) passes six cases / 24 as-recorded values, six exact canonical tops, maximum absolute drift **8.866882e-7 ≤1e-4**, with finite/range/sum checks and **no normalization**. Three detailed calls match nine token matrices / **1,668 integers**; three plain calls remain token-unverified. This arithmetic alone is not execution proof.

The separate [functional review](../../artifacts/evaluation/final-sprint-20261112-01/sdk-functional-review-v1/report.md) ([receipt](../../artifacts/evaluation/final-sprint-20261112-01/sdk-functional-review-v1/receipt.json)) accepts retrospective saved **online packed `/sdk-proof/` M9-only** execution/closure. Actual release evidence root is [final-sdk-20261112-01](../../artifacts/release/final-sdk-20261112-01/); this is not a final app URL or uptime claim. The first preflight failed before browser contact with zero calls, charged 2 seconds; renewed online execution completed six public calls and disposal, charged 4 seconds: **6/300 total, grant closed**. Known worker/tab/control closure is supported, not OS-global process absence. Browser total/peak memory remains unknown.

Offline is **UNATTEMPTED** after late pickup of the stop notification; cache readiness is not offline execution or fresh-navigation proof. No new production queue/chat/playground dependency graph or runtime acceptance is certified; no M13 browser parity or promotion follows. Earlier B2 and other reports are preserved, not rescored or substituted.

### Final production-app phase: unattempted, not a parity failure

A separate six-case packet was [frozen](../../artifacts/evaluation/final-sprint-20261112-01/final-app-reference-v1/reference.json) at **20:02:51** and delivered **20:03:10**: two existing queue rows, two existing chat rows and two existing playground cases, preserving raw M9 references. Queue/chat would use their normal suggestion buttons; playground would use its existing explicit same-call diagnostic bridge. Three independent lazy engines, six calls total; no native-reference replay or offline phase. The comparator was prepared but **never executed**.

The [closure receipt](../../artifacts/evaluation/final-sprint-20261112-01/final-app-closure-v1/receipt.json) records the actual distinction: final capture source `b7de809bd01bdd58902c2ea4ea2bc468f26e7c2b` / manifest `19876c1858b65fc905679d25` was served around **20:11**, after the 20:05 readiness target. Runtime reported three cold, unused task pages and complete readiness at **20:13:30**. Model reported no inbox pickup between **20:07:50 and 20:15:09**, after its fixed **20:15** availability ended. **No activation was issued; no final-app inference occurred.** The tighter single-55-second controller proposal did not itself grant execution. The prepared refs, source and unused allowance do not justify a late launch or fabricated pass.

Final production-UI parity/inference is therefore **UNATTEMPTED / UNVERIFIED**, not a measured numerical failure. The earlier packed SDK online acceptance remains valid only in its demonstrated scope. Model's shared browser charge remains **6/300 seconds**, closed. The Infra-owned finite local static host and its configured **23:15 UTC** expiry are separate from Model/Evaluation availability; this report does not promise continuing uptime or monitoring.

## Interpretation and publication boundary

The [public freeze](../../artifacts/evaluation/final-sprint-20261112-01/reserved-freeze-v1.json) fixes 64 deliberately balanced synthetic cases, not 64 IID observations or verified human truth. AI-authored/reviewed agreement, retained ambiguity, scenario/taxonomy dependencies and small strata limit generalization. Quality arithmetic uses admitted vectors divided by actual sums, natural-log NLL and summed multiclass Brier on singleton targets; no clipping or repair. Both models have zero recorded ties and zero infinite NLL counts in these summaries. Threshold freeze followed S1 knowledge and preceded the owner's S2 review and new learning: not blind preregistration.

Scientific review is closed: the source/binding reviews and independent arithmetic support **retain M9**. The single actual scorer invocation and subsequent independent arithmetic are distinct saved-data operations; neither reran a model or changed producer bytes. The original source-only scorer v1, v2 preparation, failed inspection/locator attempts and earlier SDK pre-browser failure remain retained. No private cases, labels or probability vectors are published here.

Final production-app M9 acceptance closed **UNATTEMPTED**, not accepted by source equivalence. New SDK offline execution also remains **UNATTEMPTED**; M13 deployability is **NOT MEASURED / NOT PURSUED** after scientific failure. Package builds demonstrate packaging only, not numerical or browser acceptance. No software tests, lint, dependency changes, extra inference or spending were performed for this publication. Detailed evidence artifacts remain local and are not shipped in the source-only public repository; artifact links identify retained evidence, not downloadable public payloads. Locally they resolve from canonical main, not the worktree's stale artifact tree.
