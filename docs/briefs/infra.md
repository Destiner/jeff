# Infra owner brief

## Objective and ownership

I1/I2 are delivered. I3 adds direct owner-to-owner messaging with peer posting
OFF until lead confirms compatible-client adoption and enables it. See
[protocol/usage](../coordination/mailbox.md), [rollout](../coordination/i3-rollout.md),
and [I3 demonstration evidence](../coordination/i3-demo.md).

- Branch/worktree: `worker/infra`, `.worktrees/infra`, created from committed
  main `97d032433cf94e5647b664f578f4237613f9b500`; adopt rather than recreate.
- Owned paths: `src/jeff/coordination/`, `docs/coordination/`, this brief.
- I1 narrowly authorizes `/.coord/` in root `.gitignore`, mailbox/check-in
  instructions in `AGENTS.md`, and Infra ownership/mailbox registration in
  `docs/coordination.md`. I3 separately authorizes narrow mailbox/check-in and
  adoption wording in `AGENTS.md` and `docs/coordination.md`. Other teams'
  objectives and merge rules are unchanged.
- No model, training, data, evaluation, or release/runtime edits; no dependency,
  `pyproject.toml`, budget, or shared ML-interface changes.
- No tests/lint, model loading/training, paid services, database, web UI,
  network service, watcher, harness extension, wake-up, heartbeat, or integrations.

## Operating decisions

The live board is `/Users/destiner/Code/jeff/.coord/`. Git common-directory
resolution shares it across worktrees; `--board` selects an isolated alternative.
Messages are immutable JSON-fenced Markdown with UUIDv4 IDs and validated
participant routing/references. Updated readers understand peer records;
new peer sends require the board's explicit lead enablement marker. Per-recipient receipts distinguish read
acknowledgement from disposition and cannot regress closed work. Atomic
publication and a local per-recipient file lock handle cooperating processes.

Only owners/lead post; subagents report through the owner. Existing artifacts
remain detailed evidence and team-to-team handoffs remain unchanged.
No assignments are imported/replayed. Sender strings are not authentication
or authority. Poll at the boundaries in `AGENTS.md`; idle/finished sessions
may need a manual nudge. Do not promise background delivery.

## Delivery and continuity

Self-review, exercise the real CLI on a separate scratch board, build with
`uv build --no-sources`, and self-merge using the existing short shared merge
lock. Only a genuine blocker warrants an early report. No automatic adoption
messages are sent on behalf of lead; offer the concise adoption text in the
delivery report for lead to send.

Follow [owner lifecycle](../owner-lifecycle.md) for replacement. After I1,
request direction rather than expand this into an orchestration platform.
For I3, leave live enablement and adoption collection to lead; use the absolute
main-checkout launcher without changing an active ML environment.
No ML slot or paid allocation is needed; no background process is installed.
