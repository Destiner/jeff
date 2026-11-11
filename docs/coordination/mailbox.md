# Markdown mailbox v1

A small, local lead ↔ owner channel, not a workflow engine or another task ledger.
Detailed artifacts and public peer handoffs remain the evidence; link to them.

## Board and participants

The live board is `/Users/destiner/Code/jeff/.coord/`, outside Git. From any
checkout/worktree, the CLI takes the parent of Git's absolute common `.git`
directory, **not the current worktree**, and appends `.coord`. There is no
worktree-local fallback. Outside Git or with a nonstandard Git layout, supply
`--board /absolute/path`; this override never consults the live board.

Only `lead`, `model`, `data`, `evaluation`, `research`, `release`, and
`infra` post. Owners post on behalf of their subagents. Each message has one
recipient. Routing is lead → one owner or one owner → lead only; team-to-team
artifact handoffs continue unchanged. To send one adoption direction to all
owners, the lead sends six individual messages, not a shared receipt.

```text
.coord/
  board.md                          # format marker; init does not import tasks
  messages/<uuidv4>.md               # immutable, sender-published
  receipts/<recipient>/<uuidv4>.md   # written exclusively by that recipient
  receipts/<recipient>/.lock         # permanent local receipt-write lock
```

## Everyday commands

Run from an up-to-date checkout with Python 3.12 and uv. No optional ML stack
or additional dependencies are needed. In an environment also used for ML,
uv's usual optional-extra retention rules still apply; prefer the owner's
isolated environment.

```sh
uv run --locked python -m jeff.coordination init
uv run --locked python -m jeff.coordination inbox --recipient infra
uv run --locked python -m jeff.coordination read MESSAGE_ID

# Only after actually reading the full message:
uv run --locked python -m jeff.coordination ack MESSAGE_ID --recipient infra

# Afterwards, choose the applicable disposition:
uv run --locked python -m jeff.coordination complete MESSAGE_ID --recipient infra \
  --note 'Delivered; [evidence](/absolute/path/to/handoff.md)'
uv run --locked python -m jeff.coordination block MESSAGE_ID --recipient infra \
  --note 'Need the existing allocation clarified; no paid work started.'
uv run --locked python -m jeff.coordination decline MESSAGE_ID --recipient infra \
  --note 'Outside the assigned scope; proposing a separate decision.'

uv run --locked python -m jeff.coordination inbox --recipient infra --all
```

The dispositions above are **alternatives**, not a command sequence.
`read` is read-only; it never acknowledges. `ack` is an explicit attestation
that the owner actually read the message, not evidence that a file exists.
It neither accepts new authority nor claims completion. The CLI cannot prove
human/agent comprehension.

```sh
# Body is a regular UTF-8 Markdown file; include request/report and evidence links.
uv run --locked python -m jeff.coordination send \
  --sender lead --recipient infra --kind task --task-id I2 \
  --subject 'A bounded follow-up' --body-file /absolute/path/to/request.md

uv run --locked python -m jeff.coordination send \
  --sender infra --recipient lead --kind report --task-id I2 \
  --subject 'Follow-up delivered' --reply-to MESSAGE_ID \
  --body-file /absolute/path/to/report.md
```

`send` prints only the new ID. Kinds are `task`, `direction`, `report`,
`update`, `blocker`; they describe content, not permissions.
Task IDs are optional labels, not managed tasks. `--reply-to ID` requires an
existing message with reversed endpoints. `--supersedes ID` requires the
same endpoints (a correction by the original sender). Both may be present
if each independently satisfies its rule. References stay within the chosen
board, must exist, and cannot be self-references or cycles.

Corrections and replies are new messages, never edits. Superseding a message
does not hide it, close its receipt, or transfer authority. If obsolete, its
recipient can acknowledge and decline it with a link to the correction.
Messages do not follow links, execute commands, load models, grant budgets,
or authorize overriding user/project rules.

## Inbox and receipt states

The default inbox lists `unread`, `acknowledged-outstanding`, and `blocked`.
`--all` also shows `completed` and `declined`. Results sort by creation time
then ID, not causal order; concurrent sends may appear on the next check.
Malformed records fail visibly with a nonzero exit rather than disappear.
All messages/references are validated even if addressed to another recipient.

| Current receipt | Allowed next states |
| --- | --- |
| None (`unread`) | `acknowledged` |
| `acknowledged` | `blocked`, `completed`, `declined` |
| `blocked` | `completed`, `declined` |
| `completed` / `declined` | No different state |

Same-state retries are no-ops and preserve times/notes. If a retry supplies a
different note it fails; send a follow-up message instead. A repeated `ack`
after blocking/completion/declining fails instead of regressing state.
Blocking remains outstanding; resumption can be reported in a message and
eventual completion recorded directly from blocked. Explanations/evidence
links are optional `--note` Markdown. Receipts do not send notifications;
for a consequential blocker or delivery, also send a concise message to lead.

Only the recipient writes its receipt, using an explicit `--recipient`.
A stable per-recipient `flock` serializes read/check/replace across concurrent
CLI processes. Do not delete `.lock`: the OS releases the lock when the process
exits. This local lock is unrelated to the project's main merge lock.

## Check-in discipline

Check your inbox:

- On starting/resuming work.
- Before substantial new work or an ML job.
- After subagents or long commands return.
- Before merging and before ending an assignment.
- Roughly every minute while actively waiting and able to check.

Read new messages, explicitly acknowledge them, and separately record outcomes.
Do not interrupt a running job merely to meet a polling deadline. There is no
background delivery, watcher, daemon, heartbeat, or wake-up tooling; finished
or idle sessions may need a manual nudge. Adoption requires owners to refresh
committed main and follow these instructions; installing a CLI does not make
existing sessions poll it.

Send tasks/directions and meaningful reports/updates/blockers, not routine
progress spam, per-subagent chatter, or training logs. Keep long reports in
existing artifacts. Never include credentials or protected final-evaluation
content. Existing allocations, objectives, peer handoffs, owner-transfer
rules, and self-merge rules remain authoritative and unchanged.

## File format

All records are UTF-8 Markdown beginning immediately with one JSON fence,
followed by a blank line and the Markdown body. Schema version is the string
`"1"`. Required keys, exact key sets, value types, timestamps, and references
are checked; optional keys are omitted, not null. Duplicate JSON keys,
nonfinite constants, and unknown versions/fields are rejected. Body Markdown
is opaque (it may contain more fences) and is never evaluated.

A message, shown with an illustrative ID:

````markdown
```json
{
  "schema_version": "1",
  "record_type": "message",
  "id": "e3fae680-de3a-43c7-84a3-89eef83921ed",
  "sender": "lead",
  "recipient": "infra",
  "kind": "direction",
  "created_at": "2026-11-11T12:00:00.000000Z",
  "subject": "Read the mailbox protocol",
  "task_id": "I1"
}
```

Read [the protocol](docs/coordination/mailbox.md) before posting.
````

Required message metadata: `schema_version`, `record_type`, `id`, `sender`,
`recipient`, `kind`, `created_at`, `subject`.
Optional: `task_id`, `reply_to`, `supersedes`.
IDs are canonical lowercase hyphenated UUIDv4 strings and match filenames.
Timestamps use UTC `YYYY-MM-DDTHH:MM:SS.ffffffZ`; wall-clock order is not
an integrity guarantee. Subject is nonempty, at most 240 characters and
single-line without ASCII controls; task ID has the same rules with an
80-character limit. Message bodies must contain non-whitespace text.

Receipt metadata: `schema_version: "1"`, `record_type: "receipt"`,
`message_id`, `recipient`, `status`, `acknowledged_at`, `updated_at`.
The acknowledgement time survives later dispositions; body is the optional
explanation/evidence. The board marker has only `schema_version: "1"` and
`record_type: "board"`, plus an informational body.

## Publication, safety, and limits

- `init` is idempotent, creates the marker/directories, and never replays old
  assignments. Other commands require an initialized board. No migration.
- Messages use UUIDv4 IDs for concurrent senders. A same-directory temporary
  file is flushed/fsynced, then hard-linked into place atomically with
  no-clobber semantics; collisions fail rather than overwrite.
- Receipt updates publish a complete same-directory temporary file via atomic
  replacement under the recipient lock; first receipts use no-clobber links.
  Directory fsync follows publication. If durability/cleanup fails after
  publication, inspect the named record before retrying. Reserved
  `.pending-*` files are ignored by inbox; a killed writer may leave one.
- Paths/IDs are validated. Symlink components and nonregular record/body files
  are rejected. Use physical paths for scratch boards (macOS `/tmp` and
  `/var` are symlinks). Links in message bodies are inert evidence, not
  filesystem paths the CLI traverses.
- This is a cooperative local POSIX filesystem design (macOS/Linux,
  `fcntl.flock`, hard links). Not Windows or a network-filesystem protocol.
  No defense against a malicious local writer racing path checks or editing
  files directly; immutability and recipient ownership are also conventions.
- Sender/recipient strings are **not authentication**. Anyone with board
  filesystem access can impersonate an identity or read messages. Do not
  treat the board as a security or final-evaluation isolation boundary.
- No automatic read detection, delivery guarantees, notifications, wake-ups,
  scheduling, retention, search, or receipt history. Inbox validation scans
  messages and their reference chains; suitable for this small experiment.
- The board is outside Git, with no backup service. Missing/deleted receipts
  can look unread; manual edits/deletions bypass CLI safeguards.

## Isolated demonstration

Use an explicit board, never fake live work:

```sh
scratch=$(mktemp -d)
scratch=$(cd "$scratch" && pwd -P)
uv run --locked python -m jeff.coordination --board "$scratch/board" init
# Put demonstration-only bodies in "$scratch", then add --board "$scratch/board"
# before each command. Do not replay these messages into the live board.
```

Actual I1 runs, IDs, outcomes, and the transcript are recorded in
[i1-demo.md](i1-demo.md).
