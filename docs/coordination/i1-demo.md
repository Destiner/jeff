# I1 actual mailbox demonstration

Run on 2026-11-11 at 11:57 UTC from `worker/infra`, based on committed main
`97d032433cf94e5647b664f578f4237613f9b500`, with the I1 implementation in the
working tree. These are actual CLI executions, not sample output.

## Evidence

- [Full command/output transcript](i1-cli.log), including the body displayed by
  each `read`, inbox transitions, and successful dispositions.
- Retained isolated board:
  `/Users/destiner/Code/jeff/.worktrees/infra/.scratch/i1-demo-HXYQus/board`.
- Demo-only body files: `request.md`, `report.md`, `disposition.md` in that
  board's parent directory. They explicitly identify the scratch scenario.
- Every demo invocation used `uv run --locked python -m jeff.coordination
  --board <scratch-board> ...`. No live messages/assignments were created by
  the demonstration, and none are to be replayed.
- The local scratch directory is ignored; the committed transcript preserves
  the evidence if the directory is later removed.

| Actual message ID | Direction | Observed lifecycle |
| --- | --- | --- |
| `bb5317ad-e0eb-4cfe-9d8c-be73eccc962e` | lead → infra | unread → read → acknowledged-outstanding → completed |
| `a94cc73f-8792-4f68-8893-dc4f60e771aa` | infra → lead, reply to preceding direction | unread → read → acknowledged-outstanding → completed |
| `cd163f4a-df5f-41b6-89fa-bf2eb258f8ac` | lead → infra | read → acknowledged → blocked (visible as outstanding) → completed |
| `ece6f9ae-2237-4971-b1d3-a750a6cf1f11` | lead → infra | read → acknowledged → declined |

The last two sends ran concurrently and produced distinct files/UUIDs.
Completed/declined items disappeared from the default inbox and remained
visible under `--all`. Read and acknowledgement were separate CLI commands.
All demonstration commands succeeded.

The first direction's receipt retained acknowledgement time
`2026-11-11T11:57:16.626006Z` when completed at
`2026-11-11T11:57:16.888796Z`. The reply's receipt similarly retained
`2026-11-11T11:57:16.787086Z` when completed at
`2026-11-11T11:57:16.852439Z`. Both receipt bodies link the corresponding
scratch message IDs; neither claims another team's project work.

## Build and review

`uv build --no-sources` succeeded in the Infra worktree and produced:

- `dist/jeff-0.1.0.tar.gz`
- `dist/jeff-0.1.0-py3-none-any.whl`

Owner self-review plus an independent read-only source review covered shared
board resolution, strict metadata/reference/path validation, no-clobber atomic
message publication, stable receipt locking, and non-regressing dispositions.
The reviewer found no blockers. Concurrency of sends was demonstrated above;
receipt-race/crash/hostile-filesystem behavior was not runtime-stress-tested.
No software tests, test runner, linting, ML jobs, model loads, paid services,
or background processes were used. Root dependencies and ML contracts stayed
unchanged.

Live initialization and default-board inbox checks are performed after the
main integration so the root ignore rule is installed first. The final report
records the main merge hash and live-board outcome; this scratch transcript
does not pretend to prove delivery or adoption by other owners.
