# Final sprint — parallel delivery and one bounded improvement opportunity

Issued2026-11-12 after17:37UTC. User explicitly approved parallel SDK/demos, model comparison, research into poor transfer, and preparing our final improvement opportunity. Deadline remains **23:59 Europe/London today**. All times below UTC=London. Previous B1/B2/S1 grants and windows are closed; unused budgets do not carry over.

## Outcome and priorities
Ship a real local browser-first SDK plus small convincing demos, preserving an honest record of what the actual trained model does. Current main447272d is clean; trained M9 works in Safari/WASM, but S1 exposed weak new-task transfer. Do not present old synthetic scores as general capability. Working M9 package/router is the fallback regardless of experimental outcome.

Parallel tracks:
1. Runtime: extract private local `sdk/`, real package/types/worker/build/assets contract.
2. Infra: minimal dark Linear-inspired request-routing UI, Slack-like message/reaction UI, and generic playground; keep hosts thin.
3. Model: serialized diagnostic comparisons; prepare and potentially execute **at most ONE** new fixed-endpoint encoder learning run.
4. Research: focused source/data/literature diagnosis and ranked final recommendation, not a broad survey.
5. Data: fresh candidate TRAIN data plus supported-task replay, prepared independently of evaluation.
6. Evaluation: S2 direct-sentiment screen, analysis of comparisons, fresh sealed decision set, final acceptance.

Do not wait for research to build the SDK, or for training to build previews. Do not promote a guessed capability just because the interface exists.

## Schedule / decision
- On pickup: acknowledge actual start and concrete deliverables. Most owners are parked; posting does not wake them. User must resume all six.
- **18:00:** Evaluation's small S2 packet ready; Runtime/Infra agree package/API/asset interface directly.
- **18:20:** first comparison/research findings; UI previews and SDK skeleton should be usable around18:30–19:00.
- **18:45:** Model+Research publish one ranked decision and frozen candidate recipe/serving rule, or explicit no-go. Lead reviews consequential changes, but routine progression is not gated by acknowledgment.
- **19:15:** Data release and Evaluation's fresh private64-case freeze complete. No learning before both exist.
- **20:00:** hard latest start for the ONE learning attempt; **20:45** execution/evaluation target. Do not fill remaining time with searches/retries.
- **21:00:** model/serving selection freezes; retain current M9 if improvement is not supported or cannot be packaged.
- **22:00:** integrated package/demos/build/browser acceptance; **22:30** submission-ready handoff, leaving reserve before23:59.

If pickup is late, publish a shorter feasible plan rather than silently sliding all deadlines. No background attention or new overnight shift is implied. Follow ordinary30-idle-minute continuation and explicitly bounded known dependencies; report when parking.

## Scientific and compute rules
- Model is sole scheduler for native, tokenizer and browser model work. Source/data/UI work can run in parallel; no overlapping substantial ML.
- Diagnostic allocation: **600seconds aggregate local model process time**, finite per-child limits, four CPU threads preferred. <=8GiB sampled RSS; stop on concerning pressure. MPS, if used for the known Qwen path, also enforces <=8GiB driver and >=2GiB recommended headroom. No low-resource fallback that changes numerics silently.
- Planned new diagnostic decisions: M9 on16 S2; original MS MARCO START on96 S1+16 S2; actual trained M10 on those112 plus their112 reversals. **352new decisions**, no M9 S1 replay. Up to32 additional hypothesis-specific M9 decisions reserved for Research, one prospectively specified probe, no parameter search. Use existing artifacts/code/environments; reuse source/checkpoint bindings.
- At most ONE new learning attempt, only inside the compatible encoder envelope in Model brief; **20minutes aggregate** for its train/fit/evaluation native work. No hidden best checkpoint, second seed/LR/epoch arm, or post-update retry. Separate **5minutes** reserved for compatible encoder export and bounded browser acceptance, serialized by Model.
- The same <=8GiB RSS/driver caps apply to encoder learning/export; on MPS enforce >=2GiB recommended headroom, on CPU use pressure/RSS without calling a CPU free-memory estimate MPS headroom. Finite supervision and no overlapping substantial ML apply throughout.
- All actual/failed process time counts. Zero-forward wiring repair may retain/refreeze under its same cap; a run that has learned is the one attempt.
- **GBP0 new external spend** in this wave; no new paid teachers/cloud jobs, model downloads, public upload/deployment, Qwen browser/quantization retry or new architecture without one explicit scope decision. Research may browse public technical sources, never upload private cases/weights.
- No tests, test runners or lint. Builds, actual inference/training, dataset validation and saved-output arithmetic are allowed.
- No final24/D7/D3/D8/E13 reopening, use, training or case exposure. No S1/S2/new reserved evaluation examples or scenario paraphrases in training. Shared task definitions/taxonomies are allowed; copied scenarios are not.
- Keep failures, original artifacts, checkpoint/source distinctions and weak results. No probabilities-as-calibrated-confidence claims.

## Data/evaluation boundaries
Data prepares240 fresh examples:80 workspace routing,80 direct sentiment,80 software ticket intent; class/style/position variation, scenario-group split discipline. Add240 deterministic supported-task replay rows from released original v2 TRAIN only (120intent/120sentiment). No rule-learning expansion. This is candidate preparation, not permission to train or claim new labels are human truth.
Evaluation independently authors64 reserved cases (16 per each of those3 domains plus16 novel taxonomy/description-transfer cases); freezes content/preferences/grouping before learning. Model gets only exact decision-only exports, never the private reference directory. Data/Research get no new reserved cases. Evaluation checks exclusion against training and S1/S2; no hidden confirmation-driven selection/repair.
Evaluation freezes the comparison/promotion rule before new learning or fresh-set model outputs: primary routing+sentiment, ticket stretch and transfer/retention separately. Observe both top-choice and proper-score changes; no pooled headline that hides a regression. New reserved set is opened once for the prospectively fixed candidates/serving rules, not repurposed for tuning.
Existing S1/S2 are exploratory development. M10 reversal mean, if analyzed, is fixed arithmetic ID-aligned mean, a separately named two-forward rule, never a fitted rescue.

## Ownership and integration
Adopt existing worktrees/history; no resets, duplicate ownership or clobbering. Owners self-review/build/self-integrate under short shared lock; only abort a merge they started after verifying expected MERGE_HEAD. No routine Lead or publication gates.
- Runtime: `sdk/**`, existing `web/src/runtime/**`, ordinary Runtime code/docs/manifests. No SDK-specific lockfile.
- Infra: other `web/**`; narrowly owns NEW root JS workspace `package.json` and `bun.lock`, and migration of `web/bun.lock` to that single workspace lock. Preserve exact current dependency versions; no root Python packaging/environment changes. Root package is private with sdk/web workspaces; web consumes `@jeff/sdk` via workspace dependency. Coordinate dependency entries directly with Runtime, not simultaneous lock writers.
- Model/Data/Evaluation/Research retain their usual owned code/docs/artifact paths. Lead owns coordination/shared plans/final narrative.
- New heavyweight assets/dist/node_modules stay ignored. No new framework solely for UI preview; keep existing TS/Vite stack.

## UI and host rules
Read gallery skill for net-new screens: small isolated previews, not a design-system project. Use the agreed style, no invented menu clutter or prototype/audit banners in product UI. If a gallery is used, keep controls outside the product and obtain explicit user approval before promotion/removal. Mocked/precomputed behavior must be identified outside product UI; never pretend it is live inference. SDK work is independently authorized.
Route requests to Writing/Numbers/Design/Scheduling with the actually measured option descriptions. Do not keep advertising the failed Bug/Feature taxonomy as reliable. Reaction UI is a transcript + composer + model-selected sentiment-to-emoji mapping, gated on S2 results; no invented human reactor or real Slack/Linear integration. Generic editor remains available. Creature/mood scenes are out.
B2 host expired15:45 and is not presumed live. Infra may start one new loopback-only preview/final static host with explicit PID/log/command, no auto inference, finite **stop no later23:15**. Do not kill unknown user/owner processes or overwrite the B2 served worktree. Browser model execution still scheduled by Model.

## Key existing evidence
`artifacts/lead/demo-screen-20261112-01/{READY.json,inputs.jsonl,references.json,reviewed/,analysis-01/,decision.md,sdk-extraction-notes.md}`.
S1 input SHA6d9f9978928dbd9c0cb7a30270f38c182bdfca3ad839bfe885408054f59da20d; predictions `artifacts/model/demo-screen-20261112-01/run01/predictions.jsonl`, SHAecc3a1c8b0b88d88f295f74bb116085b311a750b6fc9fe37225bb862de54ebaf.
`docs/{runtime/browser-b2.md,evaluation/browser-b2.md,model/m9-msmarco-duration-results.md,model/m10-qwen-seed7-results.md,research/native-nli-adaptation-proposal.md}`; `web/README.md`.
Read current source and a few relevant records, not the entire historical audit backlog.


## Pre-execution boundary clarification

# Fresh reserved-set path clarification
The original task text used a private subdirectory outside the canonical final tree. Use:
- Evaluation-only private content: `artifacts/evaluation/final/final-sprint-20261112-01/private/`.
- Model-readable fresh-set exports OUTSIDE final: `artifacts/evaluation/final-sprint-20261112-01/inputs/{native.jsonl,reversed.jsonl,pairs.json,handoff.json}`.
- Any old-development retention exports are a SEPARATE explicit packet under `artifacts/evaluation/final-sprint-20261112-01/retention-inputs/`, not permission to browse original reference/private directories.
Evaluation provides exact filenames/hashes/allowed consumers. Model, Data, Research and Lead do not traverse the private set. No other scientific scope/row count changes. This is a pre-execution path correction, not a new experiment. The original immutable task messages remain retained.

Lead is also adding generic node_modules/ to root .gitignore for the authorized JS workspace; Infra need not race that file. Existing dist/build/artifacts ignores remain.

This document records the plan/authority, not completed executions. Six task messages were actually dispatched at17:45UTC; local briefs and dispatch IDs are under `artifacts/handoffs/lead/final-sprint-20261112-01/`. A read-only review found no additional material ownership/count/dependency conflict. The fresh private-path correction was separately sent before execution. Lead source work includes only this plan, the coordination pointer and a generic node_modules ignore.
