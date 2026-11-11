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

## Current assignments — one decoder-learning contrast; bounded support continues

All six owners remain. Existing agent/token capacity is available; paid API/compute still needs a bounded allocation within the aggregate £50 ceiling. No new dependency or paid allocation is required for the current experiment.

E4/E5 and P3 are delivered: D3 shows weak transfer even for seen mechanisms, with both encoders worsening proper probability scores. Frozen Qwen is129/240 on new validation and20/24 on reused probe presentations, but flips122/240 new answers under reversal; new rules are correct in both orders only4/80. Neither architecture is promoted. Research R5 delivered in about28minutes, explicitly not a claimed full hour, and recommends the same narrow decision-learning contrast.

Current M6/P4/E6 directions: `artifacts/handoffs/lead/wave-20261111-1520/`. R5's exact primary proposal is in `docs/research/learning-strategies.md`. Data D4/Infra I4 support directions remain in `artifacts/handoffs/lead/wave-20261111-1440/` with their original stop times; historical tasks are not to be replayed.

- **Model M6:** one full-parameter Qwen0.5B grouped-choice CE run from P3's pinned start, on exact released1,500TRAIN decisions only; R5's fixed AdamW2e-5/oneepoch/microbatch1/accum4/375updates/seed42 recipe with one materialized training-only option permutation per presentation. Preserve prompt/readout/T1/cap1024/FP32-MPS controls. Audit inputs and measure train-only backward/optimizer capacity before commitment; any disposable probe state is discarded/restored and separately accounted. Freeze controls before outcomes; at most one full learning run under a45-minute scheduled cap. No automatic LoRA/dependency/cloud fallback. Produce fresh starting E5 predictions, deterministic before/after TRAIN-fit summaries and a reloadable final checkpoint; do not select by development score. No D3 extension. Model remains scheduler through P4's return.
- **Release/Runtime P4:** coordinate narrow P3 rendering/readout reuse and an additive HF-compatible trained-checkpoint handoff with Model. Preserve P3 pins/artifacts and avoid competing loaders. Prepare while M6 is implemented; own the one fresh-process trained-checkpoint624-presentation development inference pass under Model's grant, with offline reload, identity/coverage and measured resource evidence. Model owns starting predictions/train-fit; do not duplicate final inference. No new serving/framework/portability/bundle work.
- **Evaluation E6:** reuse E5's exact624 presentations, references and source units. Before new outcomes, freeze interpretation of both-order inherited/new proper scores, rule flip/both-order success, intent/probe retention and family regressions. Check fresh-start/P3 comparability and distinguish train-fit from held-out behavior. Report every component; no post-outcome combined score, significance/calibration assertion, automatic promotion, architecture/permutation-only causal claim, or temperature fallback. No new framework or final access.
- **Research R6:** investigate the observed Qwen order instability using saved target/text-free NEW-v2 paired outputs, with explicit identifiability limits, not another broad strategy survey. Prepare at most48 preselected TRAIN cases ×4 fixed order/letter-assignment conditions (≤192presentations) on the unchanged frozen P3 model if needed. One such inference-only pass is authorized under Model scheduling and Runtime execution, lower priority than ready M6/P4 work; no Research model load, new learning, prompt search, dependencies or modification of M6/E6. Publish a frozen packet before outputs and distinguish diagnostic execution from mere preparation. R5's contingent temperature alternative remains unauthorized.
- **Data D4:** continue the original bounded data-flow observation and training-only audit, then stop/report actual outcomes. Do not extend the hour or author training cases from E4/E5 failures. Published artifacts remain immutable; genuine frozen-data issues require hash-linked errata. Share aggregate/source-appropriate findings directly with owners, not private held-out cases.
- **Infra I4:** continue the original bounded operational experiment, then stop/report measured interventions and overhead. Peer posting is live and all owners use canonical current.py. Small justified owned fixes are allowed; no scheduler takeover, repeated weight scans, process interference, observer-service expansion or new review gate.

### One-hour experiment bounds and assessment

Each R5/D4/I4 owner records actual start/end and stops around60minutes from resume. This is an active owner session with normal check-ins, not a permanent or unattended watcher. If activity ends early, report actual coverage honestly. Use subagents where useful; no software tests/linting, model-load contention, external uploads, new services, wake-up tooling, dashboard, scheduler, or destructive intervention.

Self-review/build/self-merge small in-scope fixes under the existing short lock. Cross-owner patches require that owner's agreement and integration; do not become an approval gate. Observations stay in compact append-only artifact logs, not a second task ledger. Message concrete actionable findings, not each poll.

At the end, report useful findings, interventions, actual fixes and observed effects, unresolved issues, and overhead. Do not fabricate counterfactual time saved or require a patch to justify the hour. "No demonstrated benefit" is a valid result. No automatic extension or leftover monitoring process.

## Throughput and availability

Owners use the bounded continuation policy in `docs/owner-lifecycle.md`; active sessions poll about each minute after delivery for up to30 idle minutes and take already-authorized/in-scope follow-on work. This does not add automatic wake-up or extend observation deadlines.

Parallelize preparation, CPU analysis, input validation and evaluator work; serialize substantial model loads through Model. M6 remains the only learning run. R6 adds a small explicitly bounded frozen-model diagnostic, not an architecture/seed sweep. No new experiment scheduler, dependency or cloud allocation is authorized.

Infra's existing I4 now includes a requested interim view of real peer traffic/acknowledgements, actionable stalls/fixes, and known ML busy versus ready-waiting intervals. Treat acknowledgements as attention evidence, not transport latency, and missing activity telemetry as unknown. Do not assume compute is the bottleneck before measuring eligible work and its waits.

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
