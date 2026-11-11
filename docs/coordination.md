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
| Infra | `worker/infra`, `.worktrees/infra` | `src/jeff/coordination/`, `docs/coordination/`, `docs/briefs/infra.md`; I1-only narrow mailbox additions to `.gitignore`, `AGENTS.md`, and this document |

Create/manage your own isolated workspaces. Do not edit other owners' files or share a mutable checkout between subagents. Subagents return bounded contributions to their owner; only workstream owners merge to main.

Root dependencies and shared interfaces still need the lead; cross-team implementation changes need the affected owner's agreement. Neither is permission to halt unrelated useful work. Coordinate routine inputs, predictions, and findings directly through public handoff files.

## Current assignments — focused wave after the first complete build

D2, M4, E3, R4, P1, and I1 are delivered/self-integrated. Training/save/reload, data, independent evaluation, portable local bundles, and the live mailbox work. Neither v2-trained candidate passes the predeclared robustness gate; no default is promoted. Final data remains sealed and reported additional spending remains zero.

The detailed directions are immutable files under `artifacts/handoffs/lead/wave-20261111-1247/`, delivered through the live mailbox. Owners read/acknowledge their own inbox on resume. Idle sessions still need a manual nudge.

- **Model M5:** execute exactly one fresh historical-M3 control from R4 section 4, lowering only scalar-head LR from5e-4 to2e-5 while retaining encoder/pooler2e-5, pilot-v1, source/seed/format/cap/budget/runtime controls. Preserve all prior artifacts, verify starting-state comparability, and provide fresh pilot/probe predictions for E4. No sweep, data change, new architecture/dependency, or v2 retraining. Historical source use must not reset main/the active owner workspace. Afterwards fulfill E4's label-free D3 requests with the four existing M4 snapshots; no diagnostic training.
- **Data D3:** create a small separate validation-only rule diagnostic (roughly60–120 cases over6–10 already-trained mechanisms) with genuinely new policy instances, not copied/paraphrased old cases. Plan before authoring, verify executable targets and rendered text, counterbalance options, and freeze before predictions. Mechanism overlap is intentional and explicitly reported; independent policy/source units remain separate. Preserve all old group IDs/splits; do not claim mechanism-disjoint/iid evidence or put these cases/derivatives into training. Coordinate metadata with Evaluation; no broad training-data expansion.
- **Evaluation E4:** reuse current tooling for two bounded questions. Independently score M5 versus historical M3 under R4's existing criterion, with source-group ranks/probabilities/losses and all failures visible. Separately freeze/export D3, request the two M4 starts and two trained checkpoints, and compare on seen-mechanism/new-policy instances with simple baselines. Keep this diagnostic separate from v2's unseen-mechanism validation and existing probes. No new scorer/reporting framework or final evaluation.
- **Research:** R4 delivered; standby rather than invent another investigation. M5 now executes the single recommended control and E4 applies the criterion. No new research task or ML authority. Acknowledge availability and park until a concrete follow-up is assigned.
- **Release P2:** P1 is delivered. Lead cannot yet locate a P2 completion receipt: first report existing P2 evidence if already done, without rerunning. If unstarted, continue the previously authorized30–45-minute Linux CPU recipe/runtime mission; if blocked, report the precise execution gap. Existing local runtime only, no new engine/VM/remote host, paid service, root dependency change, or upload. Model M5 has compute priority. No repeat of P1 or unrequested bundle proliferation.
- **Infra I2:** observe one bounded10–15-minute active window of this first real dispatch/receipt round. Report actual adoption friction, acknowledgement/outstanding states, and observed failures; idle-session delays are not transport bugs. Fix only an actually observed blocking defect within owned tooling if needed. No fabricated traffic/receipts, impersonation, new feature, dashboard, daemon, watcher, wake-up, or orchestration layer. If no blocker appears, deliver a concise operational note and stop.

These are current objectives, not a requirement to wait for lead approval after each internal subtask. Owners retain their file boundaries, short self-merge lock, peer coordination, and zero paid allocations. Do not open arbitrary work merely to keep every team busy.

## Markdown mailbox experiment (Infra I1)

Infra owns the barebones [mailbox protocol and CLI](coordination/mailbox.md); see the [Infra brief](briefs/infra.md). The shared board is `/Users/destiner/Code/jeff/.coord/`, outside Git; all worktrees resolve to that same board. Explicit alternate boards support isolated demonstrations. No old assignments are imported or replayed.

Only lead and owners post, initially lead ↔ team only: tasks/directions outbound, reports/meaningful updates/blockers inbound. Subagents report through their owner. Existing peer artifact handoffs, team objectives, shared contracts, ownership transfers, spending allocations, and the merge protocol below remain unchanged. Messages link evidence; they do not establish another task ledger or grant authority. Sender names are not authentication.

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

Use `JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts`. Data writes under `data/`, Model under `model/`, Evaluation under `evaluation/`, Research under `research/`, Release under `release/`; use unique IDs.

Publish intermediate outputs and nonblocking requests in append-only `handoffs/<team>/<id>.md`. Check relevant public handoffs when inputs are needed. Files are not automatically monitored, and Timur is not expected to relay routine milestones.

Final content stays under `evaluation/final/` and must not reach training/data/research workers or tuning decisions. This is procedural, not OS-enforced isolation.

## Reporting

Send one concise final chat report per completed assignment, after eligible self-integration. Early chat is only for a genuine blocker preventing useful progress or required authorization. Do not stop/report merely because a worktree, environment, tiny shard, or subagent delegation is ready.

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
