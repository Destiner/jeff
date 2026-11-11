# E5: frozen instruction decoder versus trained encoders

Independent CPU scoring of Runtime P3's frozen Qwen comparison. The decoder improves reused-probe agreement and loss, but both trained M4 encoders retain better inherited/new probability quality. Severe option-order sensitivity and sentiment failures prevent a general robustness claim. No default is promoted. Evidence paths are relative to `/Users/destiner/Code/jeff/` unless absolute.

## Recommendation
**One bounded decoder-learning experiment is worth proposing, not starting.** The frozen decoder shows strong reused-probe performance and some new-rule ranking signal, but does not demonstrate net better probability quality or robust rules. Preserve encoder candidates and the frozen decoder comparator. This recommendation is not authorization for another run.

The useful learning question is whether one fixed supervised-learning run can improve supplied-choice probability quality on independent training groups without sacrificing the observed probe/intent signal or aggravating reversal instability. Before execution, Model must choose and freeze one feasible learning recipe, obtain explicit compute and any new dependency authorization, and account for training memory (unmeasured here). Use existing authorized train data only; do not copy these validation failures, probes, or paraphrases into training. Retain this exact prompt/scoring recipe and references; evaluate with the existing scorer by stratum, family, source units, and both orders. Report costs and regressions for human review, not a newly tuned numerical pass threshold. No dynamic prompts, threshold search, architecture ablation, calibration or default change.

## Scope and provenance
| Stratum | Rows / declared groups | Label basis | Source units |
|---|---|---|---|
| Inherited-v1 | 60 / 12 | 40 teacher; 20 rule_verified | Intent/sentiment 5 groups each; rules 2 groups; related variants |
| New-v2 | 240 / 170 | 160 teacher; 80 rule_verified | Intent/sentiment 80 singleton groups each, 8 domains and 2 producers per family; rules 40 policies / 10 mechanisms |
| Reused probes | 24 / 12 | 24 teacher; curator model unknown | 12 original/reversed groups, 4 per family; NOT 24 independent cases |

Mapping is the explicit E3 reviewed `artifacts/evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json`, joined by exact row ID, never parsed from IDs. Rule policy IDs come from reviewed provenance and mechanism names from assignments. Teacher aliases gpt-sol/openai/gpt-sol have no immutable revision; agreement is not independently verified correctness. Rule_verified means executable structured checks, not independent authorship or proof of every natural-language interpretation. New rules are held-out named mechanisms, with shared logical primitives; this is not D3 seen-mechanism evidence. Fresh authorship and reused development probes are not untouched final evidence.

## All nine predictors: coverage and proper losses
Cells: **correct/valid; natural-log loss; summed-option Brier** (lower losses better). Every run has full valid coverage: 60/60, 240/240, 24/24, respectively; zero missing/invalid/duplicate/extra/unidentifiable records. Conditional agreement therefore equals all-row success.

| Predictor | Inherited-v1 | New-v2 | Probes |
|---|---|---|---|
| M4 MiniLM start (random head) | 20/60; 1.378267; 0.746036 | 66/240; 1.332467; 0.733140 | 2/24; 1.057107; 0.647165 |
| M4 MiniLM trained | 34/60; 0.907554; 0.478135 | 132/240; 0.823115; 0.460115 | 12/24; 1.025456; 0.628466 |
| M4 MARCO pretrained start | 30/60; 1.026878; 0.552223 | 99/240; 1.058568; 0.581492 | 14/24; 1.453783; 0.651840 |
| M4 MARCO trained | 42/60; 0.712621; 0.393343 | 141/240; 0.917258; 0.481392 | 10/24; 1.876464; 0.770313 |
| M2 retained | 35/60; 0.855288; 0.461543 | 107/240; 1.136427; 0.606945 | 16/24; 0.710407; 0.441728 |
| M3 retained | 40/60; 0.793701; 0.421937 | 110/240; 1.024844; 0.555299 | 8/24; 1.360701; 0.653598 |
| Uniform | 17/60; 1.378765; 0.746111 | 65/240; 1.333463; 0.733681 | 8/24; 1.055008; 0.645833 |
| Lexical | 29/60; 1.323710; 0.717805 | 99/240; 1.296868; 0.712801 | 9/24; 1.047044; 0.646289 |
| Qwen frozen | 35/60; 1.194707; 0.599128 | 129/240; 1.312350; 0.633492 | 20/24; 0.534509; 0.284486 |

MiniLM start has a random scoring head, not an equally meaningful pretrained decision head; MARCO start retains its pretrained head. M2/M3 are retained historical trained systems. Uniform uses first-option tie breaking, not a random draw. Qwen has no ties; baseline tie counts remain in the source comparisons.

## Family results

Cells: agreement count; natural-log loss; summed Brier. Intent/sentiment and all probes use teacher labels; inherited/new rules use published rule-verified labels, not independently established semantic truth. Complete results for all nine predictors remain in the comparison JSON.

| Stratum / family | M4 MiniLM trained | M4 MS MARCO trained | Qwen frozen |
|---|---|---|---|
| inherited-v1 / intent | 17/20; 0.500164; 0.236403 | 18/20; 0.251990; 0.158071 | 20/20; 0.025459; 0.006885 |
| inherited-v1 / rule_application | 4/20; 1.377048; 0.744755 | 7/20; 1.316504; 0.713169 | 6/20; 1.873184; 0.948396 |
| inherited-v1 / sentiment | 13/20; 0.845449; 0.453248 | 17/20; 0.569368; 0.308788 | 9/20; 1.685479; 0.842102 |
| new-v2 / intent | 74/80; 0.184336; 0.117682 | 77/80; 0.091450; 0.049058 | 74/80; 0.205688; 0.117439 |
| new-v2 / rule_application | 15/80; 1.343231; 0.745066 | 21/80; 1.411166; 0.765541 | 25/80; 1.765476; 0.882113 |
| new-v2 / sentiment | 43/80; 0.941779; 0.517597 | 43/80; 1.249159; 0.629578 | 30/80; 1.965885; 0.900924 |
| probes / intent | 6/8; 0.765721; 0.455262 | 2/8; 1.412754; 0.742417 | 8/8; 0.158820; 0.072295 |
| probes / rule_application | 2/8; 1.309512; 0.872190 | 4/8; 2.637630; 0.712874 | 6/8; 0.571991; 0.360356 |
| probes / sentiment | 4/8; 1.001136; 0.557945 | 4/8; 1.579008; 0.855648 | 6/8; 0.872717; 0.420808 |

### What matters
- Qwen is 35/60 inherited (loss 1.194707, Brier .599128), 129/240 new (1.312350, .633492), and 20/24 probe presentations (.534509, .284486). M4 MiniLM and MARCO both have better inherited/new probability quality; MARCO also has more agreeing new labels (141 vs 129).
- New rules: Qwen 25/80 vs MiniLM 15 and MARCO 21, but loss 1.765476 vs 1.343231 / 1.411166, even worse than uniform 1.303586. Ranking gain is weak evidence of useful rule signal, not reliable rule probabilities.
- New sentiment is a hard regression: Qwen 30/80 vs 43 for either M4; loss 1.965885 vs .941779 / 1.249159. Inherited sentiment also regresses (9/20 vs 13 / 17). Intent and probes do not cancel these failures.
- The observed probe advantage is on a reused development slice, not 20 independent wins: 9/12 groups are correct in BOTH orders, versus retained M2's 8/12 and trained M4 MiniLM/MS MARCO's 6/12 and 5/12. Four groups per family offer limited breadth. No significance or calibration claims.

## Exact reversal sensitivity
| Stratum | Qwen flips / complete pairs | Both correct | Original-only / reversed-only / neither | Mean TV | Max option probability delta |
|---|---|---|---|---|---|
| inherited-v1 | 19/60 | 28 | 7 / 6 / 19 | 0.244710 | 0.780268 |
| new-v2 | 122/240 | 82 | 47 / 36 / 75 | 0.330491 | 0.947695 |
| probes | 2/12 | 9 | 0 / 2 / 1 | 0.257527 | 0.987729 |

All Qwen pairs complete, with no ties. TV is half the sum of absolute probability changes aligned by option identity. These are paired presentation observations, not independent sources.

| Stratum / family | Orig correct | Rev correct | Both | Orig-only / rev-only / neither | Flips / pairs | Mean TV | Max delta |
|---|---|---|---|---|---|---|---|
| inherited-v1 / intent | 20 | 18 | 18 | 2 / 0 / 0 | 2/20 | 0.068672 | 0.622547 |
| inherited-v1 / rule_application | 6 | 6 | 3 | 3 / 3 / 11 | 10/20 | 0.336173 | 0.716424 |
| inherited-v1 / sentiment | 9 | 10 | 7 | 2 / 3 / 8 | 7/20 | 0.329284 | 0.780268 |
| new-v2 / intent | 74 | 67 | 64 | 10 / 3 / 3 | 14/80 | 0.190781 | 0.885970 |
| new-v2 / rule_application | 25 | 22 | 4 | 21 / 18 / 37 | 65/80 | 0.392720 | 0.910997 |
| new-v2 / sentiment | 30 | 29 | 14 | 16 / 15 / 35 | 43/80 | 0.407972 | 0.947695 |
| probes / intent | 4 | 4 | 4 | 0 / 0 / 0 | 0/4 | 0.154093 | 0.304032 |
| probes / rule_application | 3 | 3 | 3 | 0 / 0 / 1 | 0/4 | 0.208110 | 0.382657 |
| probes / sentiment | 2 | 4 | 2 | 0 / 2 / 0 | 2/4 | 0.410378 | 0.987729 |

New rules fall 25→22/80 under reversal, only 4/80 cases correct both ways, with 65/80 choice flips; new sentiment is 30→29 with 14/80 both correct and 43/80 flips. Neither set is 80 independent sources: rules share 40 policies and 10 mechanisms; sentiment shares producers/domains. By contrast all six stored encoder systems have zero untied flips in every stratum (probabilities stable to tiny numerical noise); this is consistency, not correctness. Uniform flips are tie-driven despite unchanged probabilities; lexical untied choices are stable. Exact-order margins are preserved in the source artifact, without imposing a new margin threshold.

## Source-unit results and hard regressions
Equal-unit macros below come directly from the completed shared-scorer supplement, not a new metric implementation. Dimensions overlap; no iid, confidence interval or significance interpretation. Unknown metadata is not a fabricated unit. Inherited policy metadata and probe producer/domain/mechanism/policy metadata are absent; new intent/sentiment mechanisms/policies and new-rule domains are absent.

| Stratum / family | Equal unit | Units | M4 MiniLM trained agreement; loss | M4 MARCO trained agreement; loss | Qwen frozen agreement; loss |
|---|---|---|---|---|---|
| inherited-v1 / intent | source_group | 5 | 0.8500; 0.500164 | 0.9000; 0.251990 | 1.0000; 0.025459 |
| inherited-v1 / rule_application | source_group | 2 | 0.2000; 1.377048 | 0.3500; 1.316504 | 0.3000; 1.873184 |
| inherited-v1 / sentiment | source_group | 5 | 0.6500; 0.845449 | 0.8500; 0.569368 | 0.4500; 1.685479 |
| new-v2 / intent | source_group | 80 | 0.9250; 0.184336 | 0.9625; 0.091450 | 0.9250; 0.205688 |
| new-v2 / intent | domain | 8 | 0.9250; 0.184336 | 0.9625; 0.091450 | 0.9250; 0.205688 |
| new-v2 / rule_application | source_group | 10 | 0.1875; 1.343231 | 0.2625; 1.411166 | 0.3125; 1.765476 |
| new-v2 / rule_application | policy_instance | 40 | 0.1875; 1.343231 | 0.2625; 1.411166 | 0.3125; 1.765476 |
| new-v2 / rule_application | mechanism | 10 | 0.1875; 1.343231 | 0.2625; 1.411166 | 0.3125; 1.765476 |
| new-v2 / sentiment | source_group | 80 | 0.5375; 0.941779 | 0.5375; 1.249159 | 0.3750; 1.965885 |
| new-v2 / sentiment | domain | 8 | 0.5375; 0.941779 | 0.5375; 1.249159 | 0.3750; 1.965885 |
| probes / intent | source_group | 4 | 0.7500; 0.765721 | 0.2500; 1.412754 | 1.0000; 0.158820 |
| probes / rule_application | source_group | 4 | 0.2500; 1.309512 | 0.5000; 2.637630 | 0.7500; 0.571991 |
| probes / sentiment | source_group | 4 | 0.5000; 1.001136 | 0.5000; 1.579008 | 0.7500; 0.872717 |

### All ten named new-rule mechanisms (8 cases / 4 policies each)
| Reviewed mechanism | Group | M4 MiniLM trained | M4 MARCO trained | Qwen frozen |
|---|---|---|---|---|
| longest common contiguous substring | data:pilot-v2:rule-a:g011 | 0/8; 1.552475; 0.830934 | 0/8; 1.491364; 0.804163 | 2/8; 2.188600; 1.082200 |
| bracket-stack validation | data:pilot-v2:rule-a:g012 | 1/8; 1.557083; 0.826566 | 1/8; 2.123043; 1.002021 | 3/8; 1.505422; 0.826523 |
| stable merge of sorted queues | data:pilot-v2:rule-a:g013 | 0/8; 1.398381; 0.756097 | 3/8; 1.385232; 0.749481 | 1/8; 2.062968; 1.085262 |
| bit-vector parity constraints | data:pilot-v2:rule-a:g014 | 1/8; 1.426493; 0.769431 | 1/8; 1.600959; 0.830603 | 3/8; 2.294756; 0.921903 |
| highest median measurement selection | data:pilot-v2:rule-a:g015 | 1/8; 1.106696; 0.672621 | 4/8; 1.094316; 0.663926 | 3/8; 1.864751; 0.871547 |
| subtractive Roman numeral parsing | data:pilot-v2:rule-b:g011 | 3/8; 1.227640; 0.700287 | 4/8; 1.241423; 0.707371 | 2/8; 1.569472; 0.857052 |
| postfix arithmetic stack execution | data:pilot-v2:rule-b:g012 | 3/8; 1.230084; 0.703611 | 1/8; 1.245580; 0.709993 | 1/8; 2.194044; 1.063633 |
| directed precedence topological ordering | data:pilot-v2:rule-b:g013 | 1/8; 1.396268; 0.755161 | 5/8; 1.379466; 0.745525 | 5/8; 0.876190; 0.448312 |
| nearest Hamming codeword | data:pilot-v2:rule-b:g014 | 2/8; 1.388008; 0.750753 | 0/8; 1.413877; 0.764017 | 1/8; 1.871353; 0.972066 |
| maximum consecutive-window mean | data:pilot-v2:rule-b:g015 | 3/8; 1.149183; 0.685198 | 2/8; 1.136398; 0.678306 | 4/8; 1.227204; 0.692637 |

### New sentiment domains: losses cannot be hidden by intent
| Reviewed domain | M4 MiniLM trained | M4 MARCO trained | Qwen frozen |
|---|---|---|---|
| community darkroom sessions | 5/10; 0.876366; 0.486340 | 5/10; 1.681164; 0.763623 | 3/10; 1.836965; 0.928866 |
| embroidery hoops | 5/10; 0.827982; 0.458748 | 5/10; 1.185559; 0.627704 | 5/10; 1.824844; 0.742605 |
| falconry demonstrations | 5/10; 1.003064; 0.552953 | 5/10; 1.171188; 0.624875 | 2/10; 1.661071; 0.975947 |
| folding picnic benches | 6/10; 0.921894; 0.510147 | 4/10; 1.578407; 0.729652 | 4/10; 2.066511; 0.915280 |
| kayak dry bags | 7/10; 0.935913; 0.502394 | 7/10; 1.088583; 0.551682 | 4/10; 2.543884; 0.970228 |
| orienteering map printing | 3/10; 1.033112; 0.565429 | 8/10; 1.002941; 0.527964 | 4/10; 1.940434; 0.912459 |
| violin shoulder rests | 3/10; 1.124546; 0.629811 | 6/10; 1.068726; 0.563231 | 4/10; 1.825656; 0.823887 |
| weaving loom rental | 9/10; 0.811354; 0.434956 | 3/10; 1.216704; 0.647895 | 4/10; 2.027716; 0.938120 |

Each domain has 10 singleton groups. Qwen sentiment loss is worse in **all 8/8 domains** than either trained M4. New-rule loss is worse in **8/10 mechanisms** than either M4: bracket-stack and directed-precedence ordering are the two exceptions. A concrete hard regression is stable queue merge: Qwen 1/8, loss 2.062968 versus MARCO 3/8, 1.385232. Conversely topological ordering matches MARCO 5/8 with much better loss .876190 versus 1.379466. Thus the rule signal is localized, not uniformly absent or generally robust. Full group/policy metrics, including all 40 policies and every inherited/probe group, remain in the cited supplement; no claim that the macro erases local regressions.

## Practical runtime and context trade-off (historical measurements only)

The analysis itself is CPU-only; the completed decoder inference was **FP32/MPS**, not CPU inference. Runtime's 14:42 handoff records 624/624 evaluated presentations plus 3 startup-only decisions, one successful frozen pass, slot returned. Full-suite throughput was 19.1438 / 18.2873 / 20.1463 decisions/s (original/reversed/probes); synchronized forward p50 was 51.1505 / 55.1386 / 49.0672 ms, with original p95 61.7346 ms. Total external process wall was 38.27065 s and model load 1.15714 s. Forward timing excludes tensor creation/probability extraction; suite wall includes those and output writes. Imports, hashing, tokenization and startup are also in process wall. No OS cache flush, matched benchmark, or fresh timing here.

CPU process-lifetime max RSS was **2,532,196,352 B (~2.53 GB)**. MPS current/driver observed maxima over load/startup/end samples were **2,013,552,384 / 2,768,961,536 B** (~2.01/2.77 GB), not true accelerator or unified-memory peaks; these quantities overlap and are **not additive**. Decoder **training** memory is unmeasured; inference fit is not a training-fit guarantee.

Existing encoder evidence qualifies, rather than quantifies, the trade-off:
- `artifacts/handoffs/model/20261111T1431-D3-predictions-ready.md` and `artifacts/model/m4-d3-inference-20261111-01/receipt.json`: four M4 original-only fresh processes on **96 different D3 cases each**, cap256/batch4/MPS, wall 2.928/1.959/1.961/1.950 s. This differs from decoder batch1, 624 presentations, prompt/scoring path and timing scope. **No matched speed ratio can be claimed.**
- `docs/runtime/p1-results.md`: historical CPU batch1/two-thread M2/M3 packaging runs on only **3 synthetic decisions / 8 options**, isolated walls 9.8904/1.3791 s, max RSS 421,396,480/378,372,096 B, internal load+predict .143/.066 s. These small CPU/isolation measurements are not E5 encoder-MPS memory or latency measurements, nor an M2/M3 benchmark. They illustrate that much smaller encoder deployments have measured lower process RSS in a different scope; they do not establish a same-profile memory ratio. No warehouse/environment search or benchmark was run.

Capacity is about **22.7M encoder vs 494M decoder parameters**. Qwen's frozen chat template/tokenizer cap1024 has observed full-prompt max220; encoder pair cap256 has observed max169. Both length audits show no input loss on their respective formats. This prevents a truncation explanation but does **not** control architecture, pretraining, capacity, context, tokenization or scoring. It is a practical systems comparison, not an architecture ablation. Qwen uses temperature1 softmax conditional on supplied single-token answer symbols, not calibrated full-vocabulary confidence.

## Execution history and review boundaries

The initial P3 attempt failed on an audit-envelope lookup **before model/tokenizer construction or predictions**. The original failure and source-control review that missed the bug remain preserved. Runtime changed only the lookup to `audit['evidence']`, refroze source at `49823af30d6b394a147c7b8a9f5c676526a439f3`, retained the config/prompt/input/model identities, and obtained a **new explicit Model grant** before run-02. The 14:36 refreeze and 14:42 success handoffs disclose this history. This is not a result-driven retry or evidence that the original review verified execution. This quality analysis does not replace the separate input/receipt/recipe control review in `artifacts/evaluation/e5-p3-execution-binding-v1/`.

Evaluation used CPU-only existing compare/order/render/source-unit tooling. Owner integrity review rechecked 228 hash declarations and all 27 quality plus 27 order reports, including independent natural-log loss/Brier arithmetic from actual scored probability maps. No final data, ML loads, training, new framework/dependency, tests/lint or paid service. £0 additional/pending spend.

## Evidence index and reproducibility

- Completed source: `artifacts/evaluation/e5-comparison-preparation-v1/execution-01/completion.json`, `recipe.json`, `study/receipt.json`; actual per-stratum `study/{inherited-v1,new-v2,probes}/comparison.json` and all nine `*-order-report.json` reports.
- `execution-01/source-units/summary.{json,md}` and the explicit E3 reviewed mapping cited above: shared-scored source groups/policies/mechanisms; this analysis extracts macros without rescoring.
- `execution-01/exact-order-margins.json`: original-choice anchored margins, TV and probability deltas; no new near-tie cutoff or order metric.
- `artifacts/evaluation/e5-p3-execution-binding-v1/` (receipt/control evidence), `artifacts/evaluation/e5-p3-input-binding-v1/` (reference/input identity), preserved separately from quality interpretation.
- Runtime: `artifacts/handoffs/release/20261111T1436-P3-corrected-freeze-renewed-slot-request.md`, `20261111T1442-P3-predictions-ready-slot-returned.md`; `artifacts/release/p3-qwen-20261111-01/{run-02/receipt.json,process-02-receipt.json,audit-02/audit.json}`. Historical encoder citations above are measurements only, not fresh runs.
- This directory: `analyze.py` is the stdlib-only extraction command, `input-receipt.json` pins the consumed quality inputs, `extracted-evidence.json` retains unrounded overall and decoder order summaries. The Markdown includes additional human interpretation and historical runtime citations; rerunning the extraction would replace those additions, so reproduce only into a new authorized namespace after adapting its output path. No frozen source artifact is edited.


Tracked recipe: `configs/evaluation/e5-p3-v1.json`; evidence index: `manifests/evaluation/e5-p3-report-v1.json`. The reusable study retains its historical `e3-study/1` schema; separately rendered E5 reports avoid changing completed artifacts. D3 is a [separate seen-mechanism diagnostic](e4-d3-seen-rules.md), not pooled here.
