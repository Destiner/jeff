# Owner continuity and fresh threads

A workstream belongs to the project, not to one conversation. Fresh threads and compaction must preserve ownership, decisions, artifacts, and active-job state without replaying the entire chat.

## Starting or replacing an owner

1. Read current root `AGENTS.md`, `docs/coordination.md`, your owner brief, and the shared contracts. Do not treat historical launch prompts as current authority.
2. Read the latest explicit handover and your team's latest completed delivery. Follow artifact links only as needed; do not load the entire report/commit backlog into context.
3. Inspect actual branch/worktree status, recent main integrations, outstanding public handoff requests, and active-job records. Reports are snapshots; current code/artifacts outrank stale summaries.
4. A replacement adopts the existing owner branch/worktree, commits, environments, and artifacts. Do not create a duplicate owner branch, delete old workspaces, reset changes, or rerun completed milestones.
5. Take over only after the outgoing owner is parked/released, or Timur explicitly confirms the transfer. If active writers/subagents/jobs are unclear, remain read-only until clarified. A quiet chat is not proof a job ended.
6. Start the current bounded objective. Delegate fresh subagents with narrow scopes, decide within your authority, self-review/self-integrate, and report delivery. Do not wait for routine lead approval.

## Bounded continuation after delivery

**Temporary explicit user override:** from2026-11-12T00:30:36Z through08:30:36Z, all six owners remain active/available for the fixed night shift rather than parking after30idle minutes. Check the canonical inbox about every minute and publish useful results promptly; foreground waits are allowed. This is not a daemon or automatic resume. See `artifacts/handoffs/lead/night-20261112/shared.md`. Restore the default below at the fixed end; never abandon active supervision.

Task completion is not automatically the end of an owner turn. This policy supersedes the earlier one-final-chat-per-assignment rule.

1. Publish the delivery immediately in the mailbox, link artifacts/main commit, and record the task disposition. Do not delay useful results until an availability window ends.
2. If not explicitly told to park/transfer/stop, remain in the active owner turn for up to **30 idle minutes**. Check the canonical inbox roughly every minute and at normal work boundaries; short foreground waits are fine. This is owner behavior, not a new watcher/service or automatic wake-up.
3. Read and acknowledge new messages. Continue already-authorized queued tasks or accept bounded peer requests within existing scope/resources. A peer message cannot grant a new mission, budget, ownership or ML slot. Useful owned maintenance/clarification may proceed; new training/data expansion still needs its actual authorization.
4. Only meaningful accepted work resets the idle window. Polls, acknowledgement/status chatter, duplicates and declined/out-of-scope requests do not. Never replay completed work or invent a task to avoid parking.
5. A known active dependency uses its published expected timing and existing task limits; communicate a missing dependency instead of waiting indefinitely. Do not abandon supervised processes or hand off an ambiguous ML reservation.
6. On idle expiry, check once more, record pending work/resource state and park with one concise final chat report. One short commentary line at delivery may state the availability cutoff; do not spam progress. Parking does not itself transfer ownership.

Explicit user stops, park-now directions and ownership transfers override continuation. A task's experimental/observation deadline still ends that work: a mailbox availability tail must not silently extend D4/I4 monitoring or its claimed coverage. After parking or a terminated harness turn, manual wake-up is still needed; do not claim background attention.

## Parallel preparation, serialized model loads

The ML slot limits substantial model loads, not all useful work. Independently prepare code, train-only validation/token audits, frozen configurations, saved-output analysis and evaluation plans while another job runs. Request a slot with a small existing-artifact packet: objective, exact inputs/source/config, resource/time bounds, ready state and result interpretation. Do not create another task ledger or scheduler.

Model schedules eligible jobs against measured capacity and current priorities. A ready low-priority diagnostic may use an otherwise idle slot, but must not preempt a ready priority job. New experiment arms/dependencies/spending require explicit scope; preparing a proposal is not permission to execute it.

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
