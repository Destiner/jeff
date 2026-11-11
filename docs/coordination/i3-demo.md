# I3 — actual peer-routing demonstration

**Live peer posting remains OFF.** All simulated roles, enablement, and peer
messages below used the separate scratch board; nothing was replayed live.

## Evidence

- [Actual CLI transcript](i3-cli.log), 2026-11-11 14:15–14:18 UTC.
- Scratch directory:
  `/Users/destiner/Code/jeff/.worktrees/infra/.scratch/i3-demo-J5TpK6/`.
- `board/` began as a copy of the actual I1 demonstration board, not a new live
  assignment. `legacy-client/` contains the original coordination source
  exported from committed pre-I3 `e7e60f3`. No owner workspace was reset/edited.
- Actual peer request: **`48fcbefc-82a3-4ee7-aa15-ed95025f02e8`**, Model → Data.
- Actual peer reply: **`97b61f4d-68d3-4004-b74b-e281b6c25727`**, Data → Model,
  referencing the request. Both bodies explicitly identify the scratch scenario.

## Observed behavior

1. The legacy and updated clients read the original v1 messages and completed/
   declined receipts. Updated `init`, `status`, `read`, and `inbox` did not alter
   any of the nine original board/message/receipt files: SHA-256 inventories
   matched. The first comparison stopped on a log-formatting difference (one
   versus two spaces introduced by awk); repeating the original inventory
   command showed no byte/digest differences. Both outcomes remain in the log.
2. Before enablement, status reported `peer_reading: true` and
   `peer_posting: false`. The attempted Model → Data send exited **1**, with
   `peer posting is disabled`; Data's inbox remained empty.
3. Scratch-only `enable-peers --sender lead --confirm-adoption` atomically
   created `peer-posting.md`. Status became enabled. The legacy client still
   read the original board because `board.md` was not changed.
4. Peer request was published/read, then explicitly acknowledged in a later
   invocation. Data's inbox distinguished `acknowledged-outstanding`; a reply
   was published/read and separately acknowledged/completed by simulated Model.
   The request moved through blocked → completed with explicit scratch notes.
5. After peer publication, the legacy client's **unrelated Infra inbox** exited
   **1**, `only lead ↔ team routing is allowed`. This reproduces the rollout
   hazard: do not publish live peers until every reader has adopted the new CLI.
6. The absolute launcher, run from `legacy-client/src` with stale `PYTHONPATH`
   and Model's `VIRTUAL_ENV`, selected the new Infra source, read the mixed
   legacy/peer board successfully, and resolved the default live board to the
   root `.coord/`. Read-only live status still reported posting disabled.

The isolation invocation used before integration was:

```sh
PYTHONPATH="$scratch/legacy-client/src" \
VIRTUAL_ENV=/Users/destiner/Code/jeff/.worktrees/model/.venv \
/Users/destiner/Code/jeff/.venv/bin/python -I -S \
  /Users/destiner/Code/jeff/.worktrees/infra/src/jeff/coordination/current.py \
  --board "$scratch/board" status
```

The [adoption command](i3-rollout.md) uses the **main** launcher path instead.
Post-integration verification of that exact canonical path, under the same
stale-path conditions, is retained in the scratch directory's
`canonical-main.log` and reported in the final mailbox delivery. That check is
read-only: it must not enable the live board. The launcher performs no package
sync/install, activation, or ML import; it requires isolated/no-site Python and
rejects inherited Git repository-selection overrides for default discovery.

## Review and bounds

Owner self-review and an independent read-only review found no blocking defect.
The review's inherited-Git-override caveat was addressed with a small fail-closed
check; evidence links were completed. `uv build --no-sources` succeeded and
produced the wheel and sdist. Integration builds again under the shared lock.

No software tests, linting, ML jobs, paid services, background polling, or
features beyond routing, a single enablement marker, read-only status, and the
source-pinned local launcher. Identity/adoption attestations remain conventions,
not authentication. Confirmations and live enablement belong to lead; I3 delivery
does not claim that other owners have adopted the new client.
