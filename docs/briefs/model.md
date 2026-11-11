# Worker: Model and training

Create your own `worker/model` branch and `.worktrees/model` worktree from committed main before editing. Do not implement in the root checkout, overwrite an existing workspace, or create workspaces for other leads.

Read `AGENTS.md`, `docs/coordination.md`, and `docs/contracts.md`. Work on `worker/model` in `.worktrees/model`. Do not write or run software tests or linting.

## Mission

Deliver the earliest real trained checkpoint: train, save, reload in a fresh process, and write probabilities for new inputs. Do not wait for the complete dataset, an exhaustive model search, or UI.

## Ownership

Edit only `src/jeff/model/`, `src/jeff/training/`, `configs/model/`, and `docs/model/`. Generated outputs belong under the shared artifact root at `model/<run-id>/`. Root packaging and shared contracts belong to the integrator; send dependency requests promptly.

You own the initial local ML compute slot. Do not launch paid/cloud jobs without a separate budget allocation. Hardware target is Apple silicon with 16–24 GB memory; inspect the actual machine before sizing a run.

## First milestone

1. Select a provisional small pretrained backbone after a short compatibility check. The research worker will advise but must not block you.
2. Prefer the simplest genuine candidate scorer that consumes question, state, and option text. Record any simplifications.
3. Start with a tiny real training run as soon as Data has a shard. If you need a few hand-authored bootstrapping examples earlier, label them as development-only and do not report them as held-out performance.
4. Confirm that weights changed through training and save everything needed to reload.
5. Produce fresh-process predictions using the shared input/output format. Publish the checkpoint and input/prediction paths for Evaluation.
6. Once the full pilot arrives, run the first meaningful training/validation comparison.

Do not mistake decreasing training loss or memorizing a tiny development batch for generalization. Preserve the first working checkpoint.

## Suggested subagents

- One short model/backend compatibility investigation; coordinate with Research to avoid duplication.
- One inference and checkpoint implementation under `src/jeff/model/`.
- One training implementation under `src/jeff/training/`.
- The session lead integrates these and alone schedules ML runs.

Parallelize edits only in isolated workspaces or strictly disjoint scopes. Subagents must not independently load competing models or start training.

## Handoff

Publish `artifacts/handoffs/model/<id>.md` in the shared root, with branch/commit, dependency requirements, actual commands, dataset ID, checkpoint and prediction paths, runtime/memory, failures, and cost. Use the absolute shared root specified in coordination, not a private worktree artifact directory.
