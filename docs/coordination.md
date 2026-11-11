# Workstream ownership and coordination

## LD004: delegated ownership, effective now

Timur identified lead review as the bottleneck. Workstream owners now own their implementation, review, delivery, and in-scope merges to main. This supersedes earlier prompts/rules requiring lead approval for every merge or next task.

The main session owns cross-workstream direction, shared contracts, root packaging, and budget. It reviews by exception or spot-check, not as a routine delivery gate. Owners choose and delegate bounded next steps within their assigned objective and resources without waiting for the lead.

## Ownership boundaries

| Owner | Branch / workspace | Allowed tracked edits |
| --- | --- | --- |
| Lead | `main`, repository root | Root files/configuration, `src/jeff/__init__.py`, shared contracts, coordination, budget |
| Model | `worker/model`, `.worktrees/model` | `src/jeff/model/`, `src/jeff/training/`, `configs/model/`, `docs/model/` |
| Data | `worker/data`, `.worktrees/data` | `src/jeff/data/`, `configs/data/`, `manifests/data/`, `docs/data/` |
| Evaluation | `worker/evaluation`, `.worktrees/evaluation` | `src/jeff/evaluation/`, `configs/evaluation/`, `manifests/evaluation/`, `docs/evaluation/` |
| Research | `worker/research`, `.worktrees/research` | `docs/research/`, `experiments/research/` |
| Release / Runtime | `worker/release`, `.worktrees/release` | `src/jeff/runtime/`, `configs/runtime/`, `scripts/release/`, `manifests/releases/`, `docs/runtime/` |
| Infra | `worker/infra`, `.worktrees/infra` | `src/jeff/coordination/`, `docs/coordination/`, `docs/briefs/infra.md`; I1 narrow mailbox additions to `.gitignore`; I1/I3 narrow mailbox/adoption updates to `AGENTS.md` and this document |

Create/manage your own isolated workspaces. Do not edit other owners' files or share a mutable checkout between subagents. Subagents return bounded contributions to their owner; only workstream owners merge to main.

Root dependencies and shared interfaces still need the lead; cross-team implementation changes need the affected owner's agreement. Neither is permission to halt unrelated useful work. Coordinate routine inputs, predictions, and findings directly through public handoff files.

## Current assignments — advance work continues during strategy

All six owners remain. Existing agent/token capacity is available; paid API/compute still needs a bounded allocation within the aggregate £50 ceiling. No new dependency or paid allocation is required for the current experiment.

E4/E5 and P3 are delivered: D3 shows weak transfer even for seen mechanisms, with both encoders worsening proper probability scores. Frozen Qwen is129/240 on new validation and20/24 on reused probe presentations, but flips122/240 new answers under reversal; new rules are correct in both orders only4/80. Neither architecture is promoted. Research R5 delivered in about28minutes, explicitly not a claimed full hour, and recommends the same narrow decision-learning contrast.

Latest authorization: `artifacts/handoffs/lead/wave-20261111-1635/shared.md` and its six owner directions. The lead/user strategy discussion is NOT a pause or approval gate. M6/P4 execution and the R6 frozen pass are delivered; remaining E6/R6/D5 analyses continue. Prior directions are historical, not instructions to replay completed work.

- **Model M7:** one new controlled learning attempt is authorized now. Default: original P3 base and exact M6 data/materialized row+option schedule/recipe, changing only AdamW LR2e-5→2e-6. If a concrete learning-path correctness defect is established before learning, the SAME one-attempt budget may instead minimally repair it at the original LR; freeze branch/evidence before execution, never combine both changes or switch after a failed attempt. Preserve45min/16GiB/>=2GiB-headroom guards, reset weights/optimizer/RNG, reuse measured capacity. Save full TRAIN-fit vectors/ties and already-computed gradient norms. No extra epoch, new data, sweep, retry or automatic promotion. Hand the checkpoint directly to P5 and schedule its pass; do not wait for lead, strategy, Research or documentation integration.
- **Release/Runtime P5:** P4 and R6 execution are complete. Prepare the existing checkpoint-binding path for M7 concurrently; own one fresh-process offline final624-presentation pass under Model's grant and existing8GiB/<=310s bounds. Preserve original rendering/readout/identities; deliver directly to E7 and return compute promptly. No repeat R6/P4 or new framework/portability work.
- **Evaluation E6→E7:** deliver E6 independently now, without waiting for the new run. Freeze E7 interpretation before M7trained outcomes using the same624presentations/references/source units. Compare original P3, failed M6, M7 and retained encoders on both-order proper scores, coverage/ties/stability, rule both-order correctness and intent/probe/source/family retention. Distinguish TRAIN fitting from held-out transfer; outperforming failed M6 alone is insufficient. Coordinate directly with Model/P5; no final access, new cases, post-outcome composite, calibration/significance claim or automatic promotion.
- **Research R6→R7:** finish interpretation of the already completed192-presentation R6 frozen pass and saved NEW-v2 analysis within the existing R6 substantive window, with identifiability limits. Then up to25minutes to DESIGN one evidence-based next intervention/confirmation experiment using available R6/diagnosis/D6 information. M7 does not wait for it; pending M7 outcomes can remain conditional. No more model calls, broad survey, active-experiment prompt changes, new labels/dependencies or live rescue arm.
- **Data D5→D6:** finish D5's independent TRAIN target/schedule/exposure audit and report the missing-full-vector limitation; raise real validity problems directly, not a document gate. Then up to25minutes to quantify D4's specific TRAIN rule/output/branch coverage gaps and propose a ranked design for <=96genuinely new TRAIN examples/policies addressing one or two measured gaps. DESIGN only: no authoring/release, altered v2, insertion into M7, private held-out/final access, model calls or new labels/spend.
- **Infra I5:** I4 and its availability tail are finished; Infra parked at16:21:57UTC and needs an initial manual resume. I5 is now ready: one15–20-minute retrospective of existing continuation-policy traffic/handoffs, using a fixed snapshot and documented follow-on pickups, comparable waits, censoring and limitations. No further monitoring hour, automatic extension, telemetry framework or patch quota. Supersedes the earlier unactivated I5 draft's E6/lead wait.

### M6 regression diagnosis — no extra learning

M6 completed its sole1,500-presentation/375-update run in776seconds. Deterministic TRAIN agreement fell805→431/1500 and every recorded argmax position was0; tie/flat-distribution status and cause are not yet established. Keep the failed candidate; P4 is delivered and E6 scores it unchanged.

Directions in `artifacts/handoffs/lead/wave-20261111-1610/` add a15–20-minute Model source/receipt diagnosis and independent Data D5 audit. Those audits do not themselves authorize retraining or frozen-artifact changes. M7 above is the separately authorized next experiment, not an amendment to M6. These audits are parallel support, not a scoring or delivery gate.

### One-hour experiment bounds and assessment

Each R5/D4/I4 owner records actual start/end and stops around60minutes from resume. This is an active owner session with normal check-ins, not a permanent or unattended watcher. If activity ends early, report actual coverage honestly. Use subagents where useful; no software tests/linting, model-load contention, external uploads, new services, wake-up tooling, dashboard, scheduler, or destructive intervention.

Self-review/build/self-merge small in-scope fixes under the existing short lock. Cross-owner patches require that owner's agreement and integration; do not become an approval gate. Observations stay in compact append-only artifact logs, not a second task ledger. Message concrete actionable findings, not each poll.

At the end, report useful findings, interventions, actual fixes and observed effects, unresolved issues, and overhead. Do not fabricate counterfactual time saved or require a patch to justify the hour. "No demonstrated benefit" is a valid result. No automatic extension or leftover monitoring process.

## Throughput and availability

Owners use the bounded continuation policy in `docs/owner-lifecycle.md`; active sessions poll about each minute after delivery for up to30 idle minutes and take already-authorized/in-scope follow-on work. This does not add automatic wake-up or extend observation deadlines.

Parallelize preparation, CPU analysis, input validation and evaluator work; serialize substantial model loads through Model. M6 and R6 execution are complete; M7 adds exactly one explicitly bounded learning attempt, not an architecture/seed sweep. No new experiment scheduler, dependency or cloud allocation is authorized.

I4's observation and availability windows are closed. I5 uses a retrospective snapshot, not an extension. Treat acknowledgements as attention evidence, not transport latency, and missing activity telemetry as unknown; measure eligible work and waits before alleging a compute bottleneck.

## Markdown mailbox experiment (Infra I1)

Infra owns the barebones [mailbox protocol and CLI](coordination/mailbox.md); see the [Infra brief](briefs/infra.md). The shared board is `/Users/destiner/Code/jeff/.coord/`, outside Git; all worktrees resolve to that same board. Explicit alternate boards support isolated demonstrations. No old assignments are imported or replayed.

Only lead and owners post. The live board now has peer posting enabled after canonical-client confirmations from all six owners and lead; evidence is in `artifacts/handoffs/lead/i3-adoption/enablement.json`. New/scratch boards still default OFF and require explicit adoption before enablement. Follow the [canonical current CLI and rollout instructions](coordination/i3-rollout.md) so an active ML worktree/environment need not be updated. Legacy readers reject peer records even when addressed elsewhere; do not use them after enablement. Once enabled, owners can send direct in-scope requests/notices/replies/blockers, without assigning priorities, changing ownership, or granting compute/spend. Model remains ML scheduler; lead receives consequential deliveries/escalations, not every exchange by default. Subagents report through their owner. Existing peer artifact handoffs, team objectives, shared contracts, ownership transfers, spending allocations, and the merge protocol below remain unchanged. Messages link evidence; they do not establish another task ledger or grant authority. Sender names are not authentication.

Check at work boundaries and roughly every minute while actively waiting and able to check, as specified in `AGENTS.md` and the protocol. Explicit acknowledgement follows reading and is distinct from completion; blocked items remain outstanding. There is no watcher, wake-up tooling, background delivery, or automatic polling. Idle/finished sessions may need a manual nudge. No progress spam, credentials, or protected final content.

## Owner-thread rotation pilot

Model, Research, and Evaluation are transitioning to fresh owner threads at completed milestones; Data continues uninterrupted. Their outgoing delivery reports say all jobs/subagents finished and work was integrated. Timur must park old owner threads before assigning replacements. New owners follow [the owner lifecycle](owner-lifecycle.md), adopt existing workspaces, and follow the current assignments rather than replaying completed tasks. Owner briefs: [Model](briefs/model.md), [Research](briefs/research.md), [Evaluation](briefs/evaluation.md).

## Safe self-merge protocol

Every writer to the main checkout, including the lead, follows this protocol. Only the short integration step is serialized; implementation, review, data generation, and experiments remain parallel.

1. In your isolated worktree, review the change (delegate a focused review where useful), run the relevant actual workflow, and build the package. No software tests or linting. Commit a bounded change and record its exact hash. Check that changes not already on main stay inside your ownership boundary.
2. Acquire the shared lock atomically: `mkdir /Users/destiner/Code/jeff/.git/jeff-merge.lock`. Write an `owner` file inside it with your team, purpose, and start time. If it exists, continue independent work or retry later; never delete another owner's lock.
3. Verify the main checkout is clean with no merge/rebase in progress. If it is dirty, do not stash, reset, or overwrite anyone's work. Release your lock and coordinate.
4. From main, merge the exact reviewed commit with `git -c core.hooksPath=/dev/null merge --no-ff --no-commit <commit>`. Already-integrated commits need no merge. If conflicts occur, abort the merge; resolve them in your isolated branch, involving affected owners, before retrying.
5. Run `uv build --no-sources` on the integrated tree. Do not hold the lock during training, model downloads, or long analysis. If the build fails, abort the uncommitted merge and fix your branch.
6. Commit the successful merge with a conventional message and no test/lint hooks. Record the resulting main commit. Release only your own lock, including its owner file, on success or after a safely aborted attempt. Do not leave main with an unfinished merge.
7. Publish the integration hash and evidence in your handoff. Other owners may incorporate committed main at safe points without asking the lead. Do not rebase active subagents.

Do not force-push, rewrite main history, merge another owner's unapproved feature branch, or widen your edit scope. Failed/non-merged work remains on the owner branch. For a stale lock, coordinate with its recorded owner; do not guess that it is abandoned.

## Shared contracts and task reservations

Follow [contracts v0.1](contracts.md). Training families remain `intent`, `sentiment`, `rule_application`; validation uses separate source groups. `passage_entailment` remains reserved for unseen-family final evaluation. Final in-family groups are also isolated. Do not change these reservations unilaterally.

Group before generating variants. Never put validation failures or their paraphrases into training. For repairs, create genuinely separate training scenarios while keeping the evaluated cases as validation.

## Compute and spending

- Model owns and schedules the local ML slot. Other owners send it inference requests directly; no lead relay needed.
- Other owners may run lightweight CPU data processing/scoring and release packaging/hashing. Do not independently load models or launch competing ML jobs. Release requests its cold-start inference slot directly from Model; Model may execute it or grant a bounded slot explicitly.
- Shared extra-spend ceiling is £50. Current paid allocations remain £0 per owner. Existing approved agent access is available; separately billed API calls/services or rented compute need a lead allocation.
- Owners cannot each treat the £50 total as their personal budget. Track actual and pending spend in handoffs.
- All prior checkpoint/data artifacts remain immutable. Preserve a working version while experimenting.

## Artifact sharing

Use `JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts`. Data writes under `data/`, Model under `model/`, Evaluation under `evaluation/`, Research under `research/`, Release under `release/`, Infra under `infra/`; use unique IDs.

Publish intermediate outputs and nonblocking requests in append-only `handoffs/<team>/<id>.md`. Check relevant public handoffs when inputs are needed. Files are not automatically monitored, and Timur is not expected to relay routine milestones.

Final content stays under `evaluation/final/` and must not reach training/data/research workers or tuning decisions. This is procedural, not OS-enforced isolation.

## Reporting

Publish each completed assignment promptly through the mailbox after eligible self-integration; do not wait for user relay or the end of an idle window. Then follow the [bounded continuation policy](owner-lifecycle.md#bounded-continuation-after-delivery): up to30 idle minutes of active inbox check-ins and already-authorized/in-scope follow-on work. Final chat is for actually parking or a genuine blocker, not an automatic stop after every delivery. Do not stop/report merely because a worktree, environment, tiny shard, or subagent delegation is ready.

```text
TEAM / TASK:
STATUS: delivered | blocked
RESULT: what actually exists or changed
EVIDENCE: actual commands/outcomes; metrics with dataset and sample/group count
CODE: branch, implementation commit, main merge commit (or why unmerged)
ARTIFACTS: absolute relevant paths
RESOURCES: compute running/released; actual and pending spend
DECISION NEEDED: consequential question and recommendation, or none
NEXT: bounded next step within scope, or requested direction
```

The lead uses these reports to steer priorities and resolve cross-team tradeoffs; its response is not a prerequisite for routine in-scope progress. No credentials or reserved final examples in reports. Distinguish measured evidence from recommendations and teacher agreement from verified correctness.

## Integration history

- Research through `59f70cf` was integrated; Lead reproduced the 128-token truncation finding and tiny validation arithmetic. Review artifacts: `artifacts/lead/research-review-FjOJ4y/`.
- Initial Model through `2f85624` was integrated at `fb916bc`; package build succeeded. Lead independently rescored the 60 saved validation outputs (19/60 → 36/60; rule regression retained), not a new ML run. Evidence: `artifacts/lead/model-evaluation-2f85624-SEE0Za/`.
- M2 is integrated at `33442f1`; M3 at `f62ab73`; Research R2 at `36af3bb`. M3 improved pilot agreement to 40/60 versus M2's 35/60 but regressed on independent validation probes to 8/24 versus 16/24. Both candidates stay available; no across-the-board replacement is selected.
- Evaluation E2's final delivery is integrated at `8ac7d79`. Grouped/order tooling and independent M2/M3 reports are complete. `artifacts/evaluation/e2-m3-v2/` is report revision 2 over pilot-v1, not a Data-v2 evaluation.
- Research R3's candidate audit is integrated at `bbc0916`; revised data remains Data-owned and the next research objective is R4, not a repeated publication gate.
- Historical LD002/LD003 centralized integration rules are superseded by LD004 above. M1–M3/R1–R3/E1–E2 are completed; current objectives are listed above.
