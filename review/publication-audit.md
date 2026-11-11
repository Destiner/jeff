# Jeff — private publication safety audit

**Audited repository:** `/Users/destiner/Code/jeff`  
**Pin:** `91e09919bdf3b38370bf18c7bee0f6a2bbb26871`  
**Authorized audience:** PRIVATE GitHub repository and external LLM review; not public release.

## Verdict

**The full history reachable from the pin is suitable for the authorized private code review, subject to the boundaries below. No security finding currently requires a clean/squashed export.** Preserve the original commits: they retain useful execution-source provenance. This is a bounded risk assessment, not a guarantee of secret absence or legal clearance.

**No credential, private raw-chat dump, sealed final dataset rows, model binary, committed environment/worktree, symlink, or unusually large file was identified in the audited tree/history.** Ordinary author identity and local-path metadata remain; these are acceptable private-review metadata, not a basis for public release.

## Scope and method

- Read-only Git/Python inspection of the pinned tree and **all 135 reachable commits**, including historical blob versions and commit metadata: **190 distinct paths, 320 unique blobs, 2,693,118 bytes** of unique blob content. No history-only/deleted paths were found. Repository is not shallow; no replace refs or graft file were present.
- Inspected modes, sizes, names, UTF-8/binary characteristics, credential/key/auth patterns, opaque-string candidates, URLs, privacy/final-data indicators, JSON structures, provenance, `.gitignore`, and selected documentation/source. All blobs were valid UTF-8, with no NUL-containing blobs. Targeted semantic review supplemented automated screening.
- No project commands, tests, lint, builds, training, model loads, dependency installation, network requests, or uploads were performed. No repository/worktree/team artifact edits were made. Sealed artifact contents were **not opened, copied, hashed, or verified**. Only ignored-directory names at repository root were observed, not their contents. This report is the only requested deliverable.

## Findings

| Category | Path / commit evidence | Redacted finding and disposition |
|---|---|---|
| Credentials / secrets | Entire pinned reachable history | No matching private keys, common provider tokens, credential literals, authenticated URLs, or long encoded payloads identified. Opaque-string candidates resolved to answer-symbol alphabets, not secrets. **No blocker found.** |
| Personal metadata | `docs/coordination.md` (from `1bf5236e`); `docs/model/*-run.json`, `configs/evaluation/*.json`, `manifests/releases/*.json`, coordination CLI logs (at pin and historical versions); commit metadata | Absolute paths contain a local account identifier **[REDACTED]**; Git records one author/committer identity, including a non-noreply email **[REDACTED]**. Paths, run IDs, timestamps, hashes, hardware/cost and team workflow details are provenance, not access credentials. **Acceptable for this private review; retain restricted access.** |
| Transcripts / raw records | `docs/coordination/i1-cli.log` @ `b6bf12f8`; `docs/coordination/i3-cli.log` @ `296908ce` | These are committed coordination CLI/demo transcripts, not an absence of all transcripts. They contain command/output and mailbox demonstration metadata. No private user/LLM raw-chat export or customer records identified. Training docs describe synthetic data; this is not independent verification of ignored datasets. |
| Sealed final evaluation | `manifests/evaluation/final-v1.json`, `docs/evaluation/final-design.md` @ `9afbe7ab` (unchanged through pin) | Manifest includes a relative shard path under `evaluation/final/`, row count and digest; design includes aggregate family/split/release-policy metadata. **References, not included rows.** No final shard, source-case array, per-example final labels/rationales, or final predictions identified in tracked history. Generic curation/guard code is not the final dataset. Keep actual sealed storage excluded. |
| Other included examples | `src/jeff/data/bootstrap.py`; `configs/runtime/demo-inputs.jsonl` @ pin | Tiny synthetic seed examples and three runtime demo decisions are included intentionally. These are not sealed-final examples. Development evaluation results/failure analysis and hashes are also included; do not describe the repository as containing no evaluation information. |
| Binaries / large files / links | All reachable trees | No model/pretrained/checkpoint binaries, archives, dependency environments, gitlinks/submodules or symlinks identified. Maximum blob: `uv.lock`, **75,980 bytes**. Model inventories/hashes are text references, not included weights or LFS payloads. |
| Third-party material | `configs/runtime/licenses/APACHE-2.0.txt`, `m2-model-card.md`, `m3-model-card.md` @ `209e7136`; `scripts/release/prepare_support.py`; release manifests | Copied Apache license text and upstream MiniLM model cards are present intentionally. Cards declare Apache-2.0; manifests/support code retain pinned source provenance. Preserve those notices and attribution. No vendored third-party implementation or corpus dump identified. **Not a blanket license grant for Jeff, teacher outputs, dependencies, or future weight bundles.** |

## Blockers and exposure boundaries

**Pinned-history blockers: none identified for the specifically authorized private review.** The following remain publication gates, not reasons to rewrite this clean history:

1. **Do not upload/copy the working directory wholesale.** Root contains ignored `artifacts/`, `.worktrees/`, `.venv/`, `.coord/`, and `dist/`. Their contents were not audited. Do not mirror/push all refs: other branches, later commits, tags and unreachable/reflog objects are outside this pin's scope. Publish only the intended pinned lineage/ref through a separate authorized operation.
2. **Selected review artifacts require a separate allowlisted audit.** No blanket approval for checkpoints, wheels, archives, handoffs, raw sessions, logs or datasets outside Git. Do not include `evaluation/final/` or its derivatives while sealed. Model/provider licensing and redistribution rights remain unresolved; neither this audit nor private-repository authorization clears every future artifact.
3. **Public release is not authorized.** Existing README/runtime notices correctly warn that external redistribution/licensing is unresolved. The user's newer authorization permits this private review only; it does not select a project license or permit public hosting. Review-only access does not authorize training on the repository; use appropriate external-review retention/training settings.

## Ignore rules and public-ish docs

`.gitignore` at the pin excludes `.env`, `.env.*` (except `.env.example`), `.worktrees/`, `/.coord/`, `.scratch/`, `.venv/`, caches, build/dist and `artifacts/`. Read-only ignore checks confirmed the sensitive directory exclusions. No excluded environments/worktrees are tracked in any reachable version.

**Residual hazard:** ignore rules do not prevent forced additions or filesystem archives. Credentials such as PEM files, model weights or wheels placed elsewhere are not comprehensively ignored; `.env.example` is intentionally trackable. Future additions need review. README, plan, workflow and runtime docs expose internal schedules, budget, limitations, local-path provenance and a rubric link—not credentials. Do not remove honest limitations or treat Apache model notices as the project's license.

## Preserve execution provenance

Recorded source revisions are reachable ancestors, including M2 `2f856242`, M3 `e37b0f3e`, M4 `812a6557`, M5 `4031e7e9`, M6 `dafd5d23`, P1 wheel/runtime `82c327a7`, and P4 runtime `264c4434`. Keeping reachable history is preferable to a clean export for reviewing those snapshots. **Qualification:** `docs/model/tiny-run.json` records a dirty source tree at `1f64aead`; retaining that commit alone cannot establish the exact uncommitted execution bytes. This is a reproducibility qualification, not a secret finding.

## Limitations

Pattern/entropy screening cannot detect every secret, obfuscated value or subtle personal/confidential fact; not every narrative line received independent semantic review. No credential validity checks, upstream license verification, provider-contract review, malware audit or execution validation was attempted. No ignored/untracked artifact contents, other refs, later changes, remote settings/auth configs, environment dump or SSH material were inspected. Counts and verdict apply only to the stated pin and its reachable history. A different publication set requires renewed inspection.
