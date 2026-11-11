# Swarm workflow

Design for tens or hundreds of contributors without requiring hundreds of simultaneous writers or training jobs. Workstream owners own their implementation, review, and in-scope integration. The project lead steers shared decisions rather than gating routine delivery.

This is a workflow specification, not a request to build a general-purpose orchestration platform. Current roles and launch order are in [coordination.md](coordination.md); payload formats are in [contracts.md](contracts.md).

Do not write or run software tests or linting. Verification below means actual builds, training/inference runs, and model/data evaluation, not test suites.

## Workstreams

| Workstream | Parallel work | Shared boundary |
| --- | --- | --- |
| Core model | Backbone trials, trainer, inference, save/reload | Small explicit ownership areas |
| Data | Task families, domains, phrasings, difficulty levels | Versioned example schema and split policy |
| Data review | Structural checks, duplicates, label spot checks | Independent shard reports |
| Evaluation | Baselines, validation cases, failure analysis | Versioned metrics and evaluation inputs |
| Experiments | Controlled changes to data or training | Resource queue and immutable run records |
| Packaging | Reproducible setup, artifact loading, optional demo | Stable inference contract |

## Task contract

Before starting, each worker needs:

- A unique task ID and one concrete objective.
- An owner, isolated workspace, and allowed edit scope.
- Input versions and expected output paths or artifact IDs.
- Acceptance checks and any dependencies.
- A time limit, compute allowance, and spending allocation if relevant.

Keep task assignments in one shared coordination record once work starts. Claim work before editing. Avoid having all workers rewrite the assignment document or append to one results file; let the coordinator maintain shared state.

## Workspace and integration rules

- Use one branch/worktree per coding task. Never share a mutable checkout between agents.
- Git worktrees need an initial commit. Until a rules-compliant initial commit exists, stay in planning mode rather than creating conflicting ad hoc implementations.
- Prefer disjoint edit scopes. Shared files, dependencies, and contracts have an integration owner.
- Workstream owners self-review and self-merge bounded changes in their owned paths, using the shared merge lock and build protocol in `docs/coordination.md`. Subagents do not merge to main. Every main-checkout writer, including the project lead, obeys the lock.
- Keep reviews small. Include checks performed, known failures, artifact IDs, provenance, and costs in the handoff.
- If a shared contract must change, propose the change centrally and version it. Do not silently update downstream assumptions.
- Recheck the combined system after integration; passing isolated checks does not prove compatibility.

## Data production

Parallelize by assigned task family or shard, not by having every agent generate unrestricted examples.

Each shard needs an immutable ID, schema version, source/teacher provenance, generation settings, split assignment, and validation results. Store bulky content under `artifacts/`; commit only small manifests and reproducible configuration where appropriate.

Validate and deduplicate before including a shard in a training dataset. Assemble a versioned dataset manifest rather than letting workers append to a shared training file.

Generate paraphrases and related variants only after their source group has a split assignment. Protected final-test content must not be passed to training-data or tuning workers.

## Experiments and compute

- One coordinator owns resource scheduling. Begin with one local training job at a time; increase concurrency only after measuring memory and throughput.
- Every run has a unique output directory and fixed dataset/model/configuration versions. Record seeds, metrics, elapsed time, hardware, and cost.
- Start with a clear hypothesis and a limited change. More runs are useful only if their results are interpretable.
- Workers may propose experiments without being permitted to launch them.
- Allocate portions of the shared £50 ceiling centrally and account for in-flight charges. Never assign the full ceiling independently to multiple agents.
- Stop or clean up paid resources when no longer needed. Record partial or failed runs rather than presenting only successes.

## Evaluation isolation

Use validation data for adversarial discovery and the train–evaluate–repair loop. Keep the final test set separate until reporting; once its failures guide training, it is no longer an untouched test set.

Distinguish teacher agreement, verified correctness, and calibration measurements. Independent teacher reviews can help find errors, but agreement between models is not proof of correctness.

## Scale only after the pilot

Start with enough workers to establish the core contracts and one complete run. Then increase independent data and evaluation tasks broadly. The number of active agents should follow useful parallel work, not become a goal in itself.
