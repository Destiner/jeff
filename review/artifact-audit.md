# Exported-artifact private-publication audit

## Verdict

**No blocker identified in the inspected 912-file export for the owner-authorized PRIVATE repository / LLM review.** This is not authorization for public release, a license grant, or a guarantee that every secret or confidential fact is absent. Preserve restricted access and appropriate external-review retention/training settings.

All exported files match the publication manifest. The original 883 selected files also match the separate original-source selection hash records. The 29 explicitly added operational/handoff files match the publication manifest, but lack an independent earlier hash record in the original 883-item selection; see provenance qualification below. No files were removed or altered by this audit.

## Exact scope and boundaries

- Export root: `/Users/destiner/Code/jeff-review/review/evidence/`.
- Inventory: `review/manifest.json`, schema `jeff.private-review-snapshot/1`; **912 files, 97,901,520 bytes** (approximately 98 MB decimal).
- Source pin recorded in manifest: `91e09919bdf3b38370bf18c7bee0f6a2bbb26871`.
- Evidence cutoff: **2026-11-11T16:53:50Z**.
- Read the separately completed source-history audit, `/tmp/jeff-fable-publication-audit.md`. Its private-publication conclusion applies to the pinned reachable source history, not automatically to these artifacts. This audit does not redo that history audit.
- Also read `/tmp/jeff-fable-evidence-selection.json` (original source hash records) and `/tmp/jeff_prepare_review.py` (copy/extra-selection implementation; read, not executed). Read repository `AGENTS.md` and `review/protocol.md` for constraints.
- **No live original artifact contents were opened or hashed.** In particular, no inspection of live `artifacts/evaluation/final/`, excluded model/cache/environment/worktree/mailbox/session roots, or later workstream outputs. Original absolute paths inside exported records were treated only as text and resolved against the export inventory, never followed into live storage.
- Packaging README/brief/protocol/observations/evidence-map, prompts, and resolver/helper are **not comprehensively audited** here; the parent is writing them concurrently. Reading the protocol or copy helper is not clearance of all packaging materials.

## Method and integrity results

Used local standard-library Python and bounded filesystem inspection only. No project code was executed; no tests, lint, builds, installs, model loads, training/inference, downloads, credential validation, network calls, or uploads occurred. The only file written by this audit is this report.

1. Parsed the manifest and enumerated the export tree without following directory symlinks. Checked allowlisted path containment, path traversal, symlink components, inventory agreement, byte counts, and SHA-256 of every selected copy.
2. Scanned all 97,901,520 bytes for UTF-8 validity, NULs, private-key headers, common provider credentials, credential assignments, authenticated/signed URL patterns, JWT-like strings, unusually long opaque payloads, LFS pointers, conversation/session structures, sealed-final indicators, copyright/licensing language, and timestamps. Matches were reported as categories/paths/line locations rather than suspected credential values.
3. Parsed **450 JSON files and 57,775 nonempty JSONL records** across 142 JSONL files, with no parse failures. Examined structural split/session/message fields and selected provenance records.
4. Supplemented automated screening with targeted semantic reads: final-related matches; D5 delivery timestamp; I4 report and metadata snapshot structure; representative synthetic-data provenance/usage constraints; R6 source ledger, runner prompt construction, development export documentation/source pins, and finalized saved-analysis report.

| Integrity check | Result |
|---|---|
| Copy sizes and SHA-256 versus manifest | **912/912 match** |
| Actual export inventory versus manifest | No missing or unmanifested files |
| Total bytes and count versus manifest | Exact match |
| Original-source selection records | **883/883 sizes and hashes match** |
| Additional coordination/handoff selection | **29 files**, all match publication manifest |
| Embedded historical hash maps keyed by exact selected source path | **378 matching occurrences, 374 distinct containing-file/target-file pairs; zero mismatches** |
| UTF-8 / NUL check | All files valid UTF-8; no NUL-containing files |
| Symlinks in export or selected path components | None identified |

The embedded-hash check covered exact source-path-to-SHA256 map entries, including R6 source pins; it is **not** a claim to have resolved every relative filename, every historical hash field, or every omitted dependency. It used exported manifest hashes already verified against copied bytes, without reading original live paths.

### Provenance qualification for the 29 additions

The original `/tmp/jeff-fable-evidence-selection.json` records 883 files. The additional 29 comprise 10 I4 files, three other operational/parking handoffs, and 16 lead wave handoffs. Their paths are explicitly enumerated by the copy helper and correspond to the user-authorized additions. The helper records original-source hashes and checks source bytes while copying; the current publication manifest and copies agree. **There is no independent pre-copy hash record for these 29 in the original selection file.** Inspection of the helper is evidence of intended procedure, not independent attestation that it ran exactly as written. No historical-byte or filesystem-mtime attestation is claimed.

## Findings and dispositions

### 1. Secrets, authenticated URLs, and private keys — no blocker found

No matching private-key material, common provider token, suspicious credential literal, JWT, authenticated/signed URL, or long opaque encoded payload was identified by these scans. Observed HTTP(S) hostnames concern research papers, public source repositories, model references, and documentation; no authenticated URL was identified. Model/provider names and aliases are not credentials. No credential values were printed or checked for validity.

Pattern checks are not an exhaustive credential detector: unusual token formats, short opaque secrets, encoded/fragmented values, and semantic confidentiality can escape them.

### 2. Private conversations versus deliberate operational evidence — acceptable private metadata

No unexpected raw agent-session or private customer-conversation dump was identified. The broad session-marker scan mostly matched `cwd` in invocation/run receipts. Structured `role` fields in evaluation recipes represent model/control roles; the R6 runner's `system`/`user` messages are **input prompt construction**, not a recorded agent conversation (`research/r6-20261111T155310Z/runner/run_order_packet.py:164`). Synthetic requests, targets, options, and teacher-authored review judgments are deliberately included evidence, not automatically raw private sessions.

The I4 export does contain deliberate operational communication metadata. `infra/i4-20261111T144835Z/round-20261111T154844204161Z.json` has **128 entries** with sender/recipient, subject, task IDs, message/reply IDs, timestamps and acknowledgement/status metadata. Its message objects have no message-body field; receipt objects have no note/body field. This is not an absence of all communications: `events.md`, operational reports, reviews and handoffs also recount selected coordination exchanges. Their intentional inclusion is consistent with the authorized I4 scope, not permission to export a live mailbox or raw agent sessions.

Local account/path identifiers, provider aliases, UUIDs, source/run hashes, PIDs, schedules, coordination subjects, resource/cost summaries and team workflow details remain. These are **acceptable private-review provenance/operational metadata**, not public-release clearance. Pseudonymous R6 rows are linkable through the deliberately included private development mapping; do not claim non-reidentifiability or complete anonymity.

### 3. Sealed-final data versus development evidence — no sealed-final payload identified

All 15 matches from the targeted sealed-final/reference scan were reviewed in context. They concern exclusion policy, statements that final rows were not read, or **hash references to `manifests/evaluation/final-v1.json`** in source inventories. They do not expose final dataset rows, source cases, per-example labels/rationales or predictions.

Structured split fields observed were `train`, `validation`, and the R6 analytical `FIT`/`HOLDOUT` partition names; no `final`/`test` split value was found by that structural check. FIT/HOLDOUT here are subdivisions of the included development diagnostic, not proof of a sealed-final dataset. The export intentionally includes TRAIN/dev/probe inputs, labels, predictions, D3 cases and **R6 development private mappings**. Those are not findings of accidental final leakage.

Examples of harmless finalized-development naming:
- `research/r6-20261111T155310Z/saved-analysis-py312-final/` analyzes 240 NEW-v2 frozen P3 development pairs.
- `data/data-pilot-v2/review-revisions/sha-final.json` is a revision hash record.
- `infra/i4-20261111T144835Z/final-stats.json` closes the I4 observation window.
- `finalize*.py` files are recipes, not sealed-final shards.

No live sealed content was opened for comparison. Therefore absence of covertly relabeled final examples cannot be cryptographically established by this audit; the conclusion rests on export structures, visible provenance and targeted content checks.

### 4. Temporal scope — no post-cutoff scientific outcome identified

Full-file timestamp screening found one explicit ISO-style timestamp later than the review cutoff: `data/d5-20261111T161610Z/delivery.json:19`, `continuation_cutoff`. Semantic inspection establishes that this is a **future availability deadline**, not a scientific result: the same record states delivery at 16:35:08Z, before the 16:53:50Z cutoff.

The I4 observation closes at 15:48:44.204149Z. Its own earlier planned observation cutoff and small overrun are distinct from the later publication cutoff. Lead handoffs authorize/predeclare later M7/P5/E7/D6/R7/I5 work; authorization is not evidence of its eventual outcome. No imported post-cutoff scientific result was identified. Timestamp screening cannot detect undated later edits, forged timestamps, or every natural-language time expression. Copy mtimes are not historical execution proof.

### 5. Model assets, binaries and symlinks — no blocker found

The 912 manifest items have text-oriented extensions: 450 JSON, 142 JSONL, 120 Markdown, 89 Python, 76 log, nine each TXT/stderr/stdout, six CSV, one diff and one extensionless `SHA256SUMS`. All decoded as UTF-8 and lacked NUL bytes; no model/asset suffix or LFS payload marker was identified. The largest file is a structured D5 fit-audit JSON report (**12,479,831 bytes**), not weights. Checkpoint/model/tokenizer path names and hashes inside text receipts are inventories/references, not included assets. No symlinks were identified. Text-only screening is not a malware audit and does not rule out arbitrary executable behavior in included recipes; do not execute them merely because publication screening passed.

### 6. Third-party material and rights — bounded, not a license grant

Targeted provenance checks describe original synthetic requests/labels under provider terms, with no independent redistribution-license claim (for example `data/data-pilot-v2/intent-b-r2/metadata.json`, `usage_constraints`). Research notes retain public-paper citations and short attributed quotations, including `research/r6-20261111T155310Z/method/source-ledger.json`. Public URLs/source references are not downloaded assets. No unexpected wholesale third-party corpus, paper copy, vendored model payload or private third-party conversation dump was identified.

This is not exhaustive rights clearance, upstream verification, or confirmation of provider contractual permissions. Preserve attribution, source links and existing usage/redistribution qualifications. The separate source-history audit already identifies intentional upstream license/model-card notices; those must not be interpreted as a project-wide license. Private owner-requested LLM review does not authorize public hosting, onward redistribution, or training on this material.

## Publication gates and limitations

**Current exported-artifact blockers: none identified.** Do not replace this scoped conclusion with a guarantee, and do not treat it as clearance of omitted roots or future additions.

- Recheck manifest/export integrity immediately before the parent's publication operation; concurrent writers and packaging edits can change the publication set after this scan. This audit itself did not upload or publish anything.
- Packaging documents/helper/prompts need the parent's final scope check, including truthful treatment of missing assets, development versus final evidence, cutoff and restricted access.
- Preserve the qualification that the 29 additions have no separate earlier selection-file hash record. If an independently timestamped historical attestation is required, current hashes alone do not supply it.
- Automated scans covered every exported byte, but semantic review was targeted rather than line-by-line across 98 MB. No independent check against excluded final datasets, original live source files, third-party originals or provider contracts was attempted. Unknown patterns, subtle private facts, synthetic text resembling real records, obfuscated secrets, and relabeled/undated later material may evade detection.
- This review establishes no experimental correctness, calibration, causality, scientific independence, reproducibility of absent model assets, or license rights beyond the stated owner-authorized private-review context.
