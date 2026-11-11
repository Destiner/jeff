# I3 — adopt the current client before enabling peers

**Live peer posting is deliberately OFF at I3 delivery.** Infra does not enable
it or send adoption directions on lead's behalf. Lead collects confirmations
from all six owners and switches its own session before enabling.

## Canonical invocation (from any directory)

```sh
jeff_mail() {
  /Users/destiner/Code/jeff/.venv/bin/python -I -S \
    /Users/destiner/Code/jeff/src/jeff/coordination/current.py "$@"
}
jeff_mail status
jeff_mail inbox --recipient YOUR_TEAM
```

Expected status: `peer_reading: true`, `message_schema: "1"`,
`source: "/Users/destiner/Code/jeff/src/jeff/coordination/mailbox.py"`,
`board: "/Users/destiner/Code/jeff/.coord"`, and initially
`peer_posting: false`. Status is read-only; checking it does not enable anything.
Use this function for **all** mailbox operations, not just adoption.

The absolute interpreter/launcher paths select main's current source. Required
`-I -S` suppresses caller CWD/PYTHONPATH, site-packages, and editable-install
hooks; the launcher adds only its own source tree before loading the CLI.
It resolves the default board from the launcher's Git checkout, even when
called outside Git. Inherited `GIT_DIR`, `GIT_COMMON_DIR`, or `GIT_WORK_TREE`
overrides are rejected for default-board discovery: unset them or explicitly
select `--board`. No uv sync/install, environment activation, optional-dependency
removal, or owner-worktree update occurs. The existing main Python 3.12
interpreter and Git are required. This is not protection against malicious local
changes to main, the interpreter, or Git configuration. Main remains a shared
mutable checkout during its brief locked integrations; retry transient errors
after integration rather than changing another owner's workspace.

Explicit `--board PATH` before the operation still selects a scratch board.
Relative paths remain relative to the caller. Do not run a launcher from a
stale worktree and assume it is canonical; inspect `status.source`.

## Adoption direction for lead to send

> Use the canonical `jeff_mail` command in `docs/coordination/i3-rollout.md`
> for every mailbox operation, without changing an active ML environment.
> Run `status` and your `inbox`; confirm the main source path, shared board,
> and peer-reading capability in a reply to this direction. Read before ack.
> Continue lead↔owner posting only until lead enables peers. After enablement,
> peer requests remain in-scope proposals, not priority/ownership/compute/spend
> grants; Model schedules ML. Link artifacts and escalate consequential issues
> to lead, without copying every exchange. Manual check-ins still apply.

Owners send their own real adoption confirmations to lead using existing
lead↔owner routing. No fabricated receipts or automatic confirmation collection.
Lead ensures idle/parked/replacement sessions are covered: they must switch
before their next mailbox access too. A copied command alone does not prove
adoption, comprehension, or future polling.

## Lead enablement — only after confirmations

Using the same function, lead runs:

```sh
jeff_mail enable-peers --sender lead --confirm-adoption
jeff_mail status
```

Expected result: the board's `peer-posting.md` path, then
`peer_posting: true`. The command is an explicit procedural attestation, not
authentication; identity strings cannot enforce who actually invoked it.

The message/receipt schema remains v1. Updated clients read original records
unchanged and always understand peer routes. The new gate restricts **new peer
sends**, not reading or recipient dispositions. Lead↔owner sends keep working
while disabled. Self-messages remain invalid.

**Never revert to legacy readers once peer messages exist.** They validate all
messages, so even an unrelated inbox fails on a peer record. Removing the gate
file would not make existing peer records readable by those clients. There is
no rollback/migration/feature-management system; preserve immutable records
and keep compatible readers. If adoption is incomplete, leave posting OFF.
