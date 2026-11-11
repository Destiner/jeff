# Owner continuity and fresh threads

A workstream belongs to the project, not to one conversation. Fresh threads and compaction must preserve ownership, decisions, artifacts, and active-job state without replaying the entire chat.

## Starting or replacing an owner

1. Read current root `AGENTS.md`, `docs/coordination.md`, your owner brief, and the shared contracts. Do not treat historical launch prompts as current authority.
2. Read the latest explicit handover and your team's latest completed delivery. Follow artifact links only as needed; do not load the entire report/commit backlog into context.
3. Inspect actual branch/worktree status, recent main integrations, outstanding public handoff requests, and active-job records. Reports are snapshots; current code/artifacts outrank stale summaries.
4. A replacement adopts the existing owner branch/worktree, commits, environments, and artifacts. Do not create a duplicate owner branch, delete old workspaces, reset changes, or rerun completed milestones.
5. Take over only after the outgoing owner is parked/released, or Timur explicitly confirms the transfer. If active writers/subagents/jobs are unclear, remain read-only until clarified. A quiet chat is not proof a job ended.
6. Start the current bounded objective. Delegate fresh subagents with narrow scopes, decide within your authority, self-review/self-integrate, and report delivery. Do not wait for routine lead approval.

## Outgoing handover

At a natural milestone, finish or explicitly hand off active work. Stop creating new subtasks. Publish one concise append-only handover under `artifacts/handoffs/<team>/` containing:

- Branch, implementation/main commits, workspace and dirty/uncommitted state.
- Delivered result and exact key artifact paths.
- Current objective, next useful step, and consequential decisions with short rationale.
- Important failures/limitations, rejected approaches, and things not to repeat.
- Outstanding peer requests and their owners.
- Active processes/subagents, compute ownership, actual/pending spend.
- Whether the owner is released and whether any job still needs supervision.

Then park the old thread; only the replacement owns new work. Do not silently abandon running jobs or kill useful work just to reset context.

## Compaction and operating style

Keep durable rationale and current facts in owned project docs and immutable handoffs. The owner orchestrates; fresh, bounded subagents do most detailed investigation/implementation. Bring back results and evidence, not entire transcripts.

No scheduled reset is required just because a thread is long. Rotate when the role changes, context becomes confused, or a useful milestone provides a clean boundary. Safe continuity matters more than a perfectly fresh context.

No extra software tests, linting, orchestration service, or global mutable task board is needed.
