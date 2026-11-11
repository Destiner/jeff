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

## Current assignments — quality evidence and direct coordination

Keep all six owners; no organisational restructure is being made. Use spare agent capacity for bounded work that informs model decisions, not optional platform coverage. Zero spending is not a target, but paid work still needs an explicit bounded allocation within the aggregate £50 ceiling.

D2, M4, E3, R4, P1/P2, I1/I2, and M5/E4 Track A are delivered/self-integrated. M5 recovered one probe group (8→10/24 presentations) but worsened probe group-macro loss1.360701→1.384773, so its fixed criterion failed. No default is promoted. D3 publication and E4 Track B remain pending; do not describe those as complete.

Detailed directions: `artifacts/handoffs/lead/20261111-I3-peer-mailbox.md` and `artifacts/handoffs/lead/wave-20261111-1400/`. Earlier wave files remain historical evidence, not instructions to replay completed work.

- **Model:** M5 training/control is complete. Fulfill E4's D3 originals-only request with the four existing M4 snapshots once released. Handle Data's small nonblocking validation-only ingestion-marker guard in owned code without modifying historical experiment sources or retraining. Remain ML scheduler and grant P3 a bounded local slot; D3 has priority once ready, but an unpublished input must not indefinitely reserve idle compute.
- **Data D3:** finish the existing96-case/48-new-policy/8-seen-mechanism diagnostic repairs and immutable release. Fix demonstrated semantic/construction defects, preserve review history, verify reviewed-byte identities, and disclose residual hints. Do not make speculative publisher redesign or a guarantee of zero heuristic matches a release gate. No new authoring quota, training-data expansion, or lead approval gate.
- **Evaluation E4/E5:** E4 Track A is complete and Track B resumes on repaired D3 publication. In parallel, E5 exports/reuses exact frozen E3 label-free original/reversed development inputs for P3 and independently compares the frozen decoder with stored encoder/baseline outputs. Preserve inherited60/new240/probe24-over12groups strata, families, probability quality, coverage, and order sensitivity. Different capacity/pretraining/prompt/context mean this is a practical systems comparison, not an architecture ablation. No new framework, threshold tuning, automatic promotion, or final access.
- **Research:** R4 delivered and its control executed; remain available for a concrete follow-up. No repeated diagnosis, broad survey, model load or new assignment merely to keep busy. R1's existing pinned decoder recommendation is reused directly by P3.
- **Release/Runtime P3:** P2 preparation is complete; Linux remains explicitly unverified and is not a current goal. Execute ONE local frozen `Qwen/Qwen2.5-0.5B-Instruct` comparison at R1's pinned revision, using a small experimental adapter in Runtime-owned paths and the existing ML stack. Freeze one prompt/scoring recipe before outcomes, verify answer-token boundaries, audit lengths without silent truncation, and produce contract-compatible predictions for E5 under Model's scheduling. Measure actual load/warm-inference/memory cost with appropriate qualifications. Public model download is authorized; no training, PEFT/dependency change, backend migration, remote execution, paid service, upload or production serving. This is the narrow exception authorizing decoder exploration, not an unqualified model switch.
- **Infra I3:** implement direct owner-to-owner requests/notices/replies using existing immutable messages and recipient receipts. Peer posting stays OFF on the live board until compatible-client adoption is confirmed and lead explicitly enables it; current readers reject all peer records even if addressed elsewhere. Provide a verified canonical-current CLI invocation, scratch-board behavior, and adoption/enablement instructions. Preserve old records; no impersonation, fabricated live traffic, watcher, wake-up, dashboard, scheduler, service or task-ledger expansion.

Owners choose implementation/delegation and self-integrate within their bounds. Current paid allocations remain zero because these next executions use existing local resources, not because useful paid work is forbidden. Request a concrete costed allocation if it would remove a real critical-path blocker; do not halt unrelated work while waiting.

## Markdown mailbox experiment (Infra I1)

Infra owns the barebones [mailbox protocol and CLI](coordination/mailbox.md); see the [Infra brief](briefs/infra.md). The shared board is `/Users/destiner/Code/jeff/.coord/`, outside Git; all worktrees resolve to that same board. Explicit alternate boards support isolated demonstrations. No old assignments are imported or replayed.

Only lead and owners post. Until I3's explicit rollout enablement, routes remain lead ↔ team only: tasks/directions outbound, reports/meaningful updates/blockers inbound. I3 implementation/adoption is authorized, but peer posting is not yet enabled. Subagents report through their owner. Existing peer artifact handoffs, team objectives, shared contracts, ownership transfers, spending allocations, and the merge protocol below remain unchanged. Messages link evidence; they do not establish another task ledger or grant authority. Sender names are not authentication.

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
