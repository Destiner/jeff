# E3 control / probability audit v1

Bounded fresh reviewer, CPU metadata/report inspection only. No source edits, software tests, lint, ML/model loads, scoring rebuild, package build, final-content access, paid services, tuning recommendation, new-run recommendation, or default selection. Read Evaluation AGENTS/brief, frozen M4 plan/reference config, Model 11:50/11:56/12:01 handoffs, and intermediate `20261111-e3-M4-independent-results.md`. Existing shared comparison and source-unit summaries supply all metrics below; arithmetic only compares those summaries.

## Evidence pins

`receipt.json` pins 134 distinct files, including both run records, all four checkpoint metadata files and available model/tokenizer configs, both final-release token audits, dataset-manifest copies, trainer/scorer source, frozen plan/config, input receipt, inference queue source, all 16 invocation/completion receipt pairs and logs, prediction/input bytes, actual E3 comparison reports and source-unit summary. Receipt SHA-256: `9b109b4771cdd963e71aa95c8aaa77d106da66e2daa21d312d4966dc1cb2d2b0`.

Released manifest: `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/manifest.json`, SHA-256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`. Both saved manifest copies match these exact bytes. This is not the pre-review candidate manifest. Run metadata records 1,500 train / 300 validation, 500 train rows per family. This review does not repeat the Data boundary validator or read/re-author dataset cases.

## Important run evidence — controls match

- Both completed run records report clean code and clean invocation cwd at `812a6557a559b82882b2a24a5c2f37fa9b74a163`. Every recorded trainer/dataset/scorer source digest matches both the committed Git blob at that revision and current source bytes. Historical clean status remains trainer-recorded evidence, not something today's Git status can independently prove.
- Initialization is fresh respective pinned pretrained source: all-MiniLM `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` with explicitly reset random scalar head; MS MARCO `233902d25c440f23af6f7d6e94d2946bac0bee0a` with retained pretrained ranking head. Pinned trainer source invokes `from_pretrained(model_id, revision)`, not an old candidate checkpoint. MS MARCO loaded/baseline head hashes are recorded unchanged. Both runs record changed backbone and head. These are metadata/source-backed findings, not independent tensor verification: no weights loaded or hashed. M2/M3 are historical trained comparators, not fresh starts.
- Shared seed 42, cap 256, batch 4 decisions, 3 full epochs, explicit 1,125-step cap, backbone/head LR 2e-5 / 5e-4, AdamW weight decay .01, betas .9/.999, eps 1e-8, MPS and 4 threads all match. All nine comparable CLI controls and full optimizer metadata are equal. Both loss histories contain 1,125 updates, each totals 4,500 presentations; all three epoch records report exactly 1,500 examples and complete=true. `stopped_by_max_steps=true` means the cap was reached at the end of epoch three, not a shortened exposure.
- Final token audits bind the released manifest and exact saved baseline tokenizer JSON hashes (both independently rehashed): 1,800 rows / 6,848 candidate pairs, max 169 complete tokens, p95 96, zero overflow, question loss or candidate loss at cap 256. No final-release audit was silently replaced by the earlier candidate audit. This is a recorded audit, not a rerun, and says nothing about unseen longer text.
- Recorded training intervals are sequential: MiniLM 11:56:25.865972–11:57:40.269000 UTC; MS MARCO 11:57:56.172265–11:59:12.794433. Elapsed 74.403 / 76.622 seconds, below the stated 15-minute bound. Supplied namespace shows one completed v2 run per architecture; this is not exhaustive machine-wide proof that no other process ever ran.
- Designed inequalities remain: mean-pool/random head versus native pooled-CLS/dropout/pretrained head, distinct pretraining objectives/tokenizers, possible padding/runtime differences. Matching recipe is not identical compute, a data-only causal ablation versus v1, or deterministic MPS replication. One seed provides no seed-variance estimate.

## Reload evidence versus owner assertion

The 12:01 public handoff is supported by actual saved invocation/completion records, not merely its prose. All 16 per-job receipts equal aggregate receipt entries, match their pre-execution invocation fields, record exit 0, and have rehashed exact input/output bytes and matching output row counts. Twelve jobs cover four M4 snapshots × combined (300), reversed (300), probes (24); four jobs reload historical M2/M3 on new and new-reversed (240 each).

The pinned queue script uses a fresh `subprocess.run` per job, creates a unique HF_HOME, sets HF_HUB_OFFLINE/TRANSFORMERS_OFFLINE, and records wall time plus stdout/stderr paths. This supports actual separate-process offline reload/inference in the owner checkout. It is not an independently witnessed process trace, isolated package installation, OS-network-denied sandbox, or independent portability demonstration. Inference receipts identify checkpoint **paths**, not hashes of weight bytes; today's metadata pins do not retroactively authenticate the exact weight bytes loaded. No weight verification is claimed here.

Metadata mismatch worth retaining: all saved checkpoint embedded `run.status` snapshots remain `running`, whereas standalone run.json is `completed`; the pinned trainer saves checkpoint metadata before setting final status. Run.json also retains generic text that fresh-process reload is a separate lead-owned step. These are stale snapshot/boilerplate fields, not evidence reload failed: the later dated 16-process receipts provide the actual reload evidence. No matched-budget mismatch found.

## Probability quality and descriptive gates

All eight predictors have full valid coverage in actual E3 reports, with no missing/invalid/duplicate predictions or extras. Counts below are supplied-label agreement; loss is natural-log loss. Combined 300-row results overlap inherited/new and are not additional evidence.

| Candidate | New 240: correct / loss | Inherited 60: correct / loss | Probes 24: correct / loss |
|---|---|---|---|
| M2 v1 trained | 107 / 1.136427 | 35 / .855288 | 16 / .710407 |
| M4 MiniLM fresh random-head start | 66 / 1.332467 | 20 / 1.378267 | 2 / 1.057107 |
| M4 MiniLM trained | 132 / .823115 | 34 / .907554 | 12 / 1.025456 |
| M3 v1 trained | 110 / 1.024844 | 40 / .793701 | 8 / 1.360701 |
| M4 MS MARCO fresh pretrained start | 99 / 1.058568 | 30 / 1.026878 | 14 / 1.453783 |
| M4 MS MARCO trained | 141 / .917258 | 42 / .712621 | 10 / 1.876464 |

**Both pass the frozen descriptive new-v2-versus-own-start gate; neither passes the frozen robustness gate versus its corresponding v1-trained predecessor.** No significance, final-evaluation, or promotion claim follows.

- MiniLM: inherited intent 20→17/20 and loss .067838→.500164. Probe agreement 16→12/24, loss .710407→1.025456 and Brier .441728→.628466. Every probe family has worse loss: intent .598436→.765721, rules .912532→1.309512, sentiment .620252→1.001136. New rules regress against M2 (19→15/80; loss 1.335358→1.343231) and own start (21→15/80; loss about 1.3020→1.3432).
- MS MARCO: inherited aggregate gain hides intent 19→18/20, loss .211817→.251990. Probes 8→10/24 hide loss 1.360701→1.876464 and Brier .653598→.770313; every probe family loss worsens, intent 4→2/8. Probe rules remain 4/8 but loss 2.084269→2.637630; sentiment 0→4/8 yet loss 1.078186→1.579008. Against own fresh start probe agreement falls 14→10 and loss rises 1.453783→1.876464. New rules improve 14→21/80 against M3 while loss worsens 1.405047→1.411166.
- Between trained M4 architectures MS MARCO gains nine new labels but has worse loss (.917258 vs .823115) and Brier (.481392 vs .460115). New sentiment is tied 43/80 but MS MARCO loss 1.249159 versus MiniLM .941779. Ranking and probability quality are consequentially different.
- New pooled ECE is .045960 MiniLM / .023151 MS MARCO; probe ECE is .218652 / .416654. MS MARCO probe ECE is numerically lower than M3's .442556 despite worse log loss/Brier. Sparse descriptive reliability bins/ECE do not establish calibrated confidence or override the proper-score regressions.

## Source-group / domain regressions from shared source-unit reports

All comparisons here are M4 trained versus corresponding historical M2/M3, not independent repeated samples. Receipt retains worst-three unit records and counts for every stratum/family, using existing shared metrics verbatim.

- Inherited MiniLM intent loss worsens in 4/5 domains/groups. `canal_boat_hire` / `data:pilot-v1:intent:g27` (4 rows): 4→2 correct, loss .163599→2.115364. `makerspace_laser` / g29: 4→3, .006365→.248637. Inherited MS MARCO's intent regression is concentrated in canal_boat_hire: 4→3, .194188→.501848. MiniLM inherited sentiment aggregate improves but Pet boarding/g26 remains 3/4 while loss worsens .683696→1.025966.
- New MiniLM: intent language-exam-certification domain remains 9/10 while loss rises .190081→.259997; 7/80 individual intent source groups worsen in loss despite family improvement. Sentiment improves in all eight domain losses but 16/80 one-row source groups worsen. New-rule loss worsens in 6/10 mechanism/source groups; rule-a:g011 (8 rows) goes 1→0 correct, 1.441992→1.552475.
- New MS MARCO: intent improves across all eight domain losses, but 5/80 individual source groups worsen. Sentiment worsens in 2/8 domains and 25/80 source groups despite aggregate gain: community darkroom sessions goes 4→5/10 while loss 1.374684→1.681164; folding picnic benches 1→4/10 while loss 1.414660→1.578407. Sentiment-b:g238 remains wrong with loss 1.732691→5.478944. New-rule loss worsens in 3/10 groups; rule-a:g012 remains 1/8 with loss 1.993223→2.123043.
- Probes have four source groups per family, each two existing original/reversed presentations, not two independent cases. MiniLM loss worsens in 1/4 intent, 3/4 sentiment and 3/4 rule groups; intent.01 changes 2→0 correct, .350200→2.722793; rule_application.03 changes 2→0, .713718→1.596698. MS MARCO worsens in 2/4 groups in each family: rule_application.01 remains 0/2 with loss 7.142956→9.418985, while rule_application.04 falls 2→0, .463546→1.042370.
- New rules comprise 80 rows / 40 policy instances / 10 mechanism groups; intent and sentiment each have 80 one-row source groups but only eight domains and two producers. Rule domain metadata is unknown; probe producer/domain/mechanism/policy metadata is unknown. Unknowns are not invented domains or evidence of zero regression. Equal-unit macros are descriptive, not iid confidence estimates. No seen-mechanism new-rule-validation comparator exists.

## Label and inference limits

New validation has 160 teacher / 80 rule_verified labels; inherited has 40 / 20; probes have 24 teacher labels with unknown teacher identity. Data008 reports full 480-new-rule recomputations passed and rules60/60 review, but same exposed teacher alias/author-review dependence is not independent ground truth. `rule_verified` identifies executable-rule checking rather than proof of independently correct policy construction/interpretation; kind=teacher may coexist with this basis. Teacher `gpt-sol` aliases do not establish an independently identified upstream model, and unknown probe identity stays unknown. Historical/probe development reuse, same-author labels/reviews, domain concentration and residual construction shortcuts remain qualifications. Hash/group identity checks cannot prove no semantic derivatives or unrecorded access.

## Packaging is separate

The 11:50 handoff reports recipe wheel/sdist build success; existing recipe-dist files are not this review's executed build or runtime-install evidence. This review did not build/install or change code, and needs no merge commit. Training completion and fresh-process local reload have concrete records above; package build claims do not replace them, and local owner-checkout reload does not prove external package portability. No default selected; no tuning or additional run proposed.
