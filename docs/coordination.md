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

Create/manage your own isolated workspaces. Do not edit other owners' files or share a mutable checkout between subagents. Subagents return bounded contributions to their owner; only workstream owners merge to main.

Root dependencies and shared interfaces still need the lead; cross-team implementation changes need the affected owner's agreement. Neither is permission to halt unrelated useful work. Coordinate routine inputs, predictions, and findings directly through public handoff files.

## Current assignments

- **Data D2:** self-review and integrate completed pilot-v1 tooling first. Then build immutable `data-pilot-v2`, aiming for roughly 1,500 train / 300 validation rows across the existing three families. Prioritize genuinely different scenarios, domains, rule mechanisms, and less obvious sentiment/intent wording over multiplying templates. Aim for at least 100 training and 20 validation source groups per family if achievable without lowering quality. Record actual counts and limitations rather than filling quotas with weak variants. Keep v1 unchanged; no prior validation examples or their variants may become training data. Consult Research directly, without waiting for its full audit. Deliver validated shards, manifests/provenance, and concise quality findings.
- **Evaluation E2:** self-review and integrate existing tooling first. Own the repeatable comparison report for the 256-token pilot and subsequent M3. Reuse the existing scoring/ordering tools rather than rebuilding them. Compare uniform, lexical, starting, and trained predictions on identical references; report coverage, label provenance, per-family and source-group results, log loss, and option-order behavior. Distinguish 60 rows from 12 independent groups. Request inference directly from Model; process already-available 128-token/pilot-probe predictions while waiting. Do not use reserved final data.
- **Model M3:** finish/publish the assigned M2 256-token comparison and self-integrate completed work. Then implement and run one retained-pretrained-head `cross-encoder/ms-marco-MiniLM-L6-v2` comparison on frozen `data-pilot-v1`, with 256 tokens, the same seed, and the same training-step budget. Preserve its initial head; compute grouped choice cross-entropy externally rather than built-in one-label regression. Keep the existing all-MiniLM path/checkpoints working and the decision interface unchanged. Record necessary architecture-specific settings explicitly. No Qwen, data changes, new dependencies, paid jobs, or final-data access. Publish initial/trained checkpoints and fresh-process predictions; coordinate scoring directly with Evaluation.
- **Research R2:** continue the assigned 30–45-minute pilot generalization/shortcut audit. Read Data's quality findings first. Examine source-group independence, template/near-duplicate overlap, answer-position/option-text shortcuts, and rule-mechanism coverage; recommend at most three prioritized improvements. Send actionable findings directly to Data/Model via files. Do not edit datasets, labels, production code, contracts, or task-family reservations.

These are current objectives, not a requirement to wait for lead approval after each internal subtask. Complete, self-review, merge eligible changes, and report delivery. If an objective is exhausted and no useful in-scope follow-up exists, ask for direction rather than inventing unrelated features.

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
- Other owners may run lightweight CPU data processing/scoring. Do not independently load large models or launch competing ML jobs.
- Shared extra-spend ceiling is £50. Current paid allocations remain £0 per owner. Existing approved agent access is available; separately billed API calls/services or rented compute need a lead allocation.
- Owners cannot each treat the £50 total as their personal budget. Track actual and pending spend in handoffs.
- All prior checkpoint/data artifacts remain immutable. Preserve a working version while experimenting.

## Artifact sharing

Use `JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts`. Data writes under `data/`, Model under `model/`, Evaluation under `evaluation/`, Research under `research/`; use unique IDs.

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
- Historical LD002/LD003 centralized integration rules are superseded by LD004 above. Their experiment findings remain valid; M3 is now explicitly authorized.
