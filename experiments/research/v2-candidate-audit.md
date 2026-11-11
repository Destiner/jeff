# R3 frozen candidate: execution and scope

Report: [v2 candidate audit](../../docs/research/pilot-v2-candidate-audit.md). This is an incremental use of R2 diagnostics and Data's existing quality findings, not a new dataset validator or repeated v1 investigation.

## Canonical actual execution

From `/Users/destiner/Code/jeff/.worktrees/research`:

```sh
uv run --locked python -B experiments/research/audit_v2_candidate.py \
  --artifacts-dir /Users/destiner/Code/jeff/artifacts \
  --output-dir /Users/destiner/Code/jeff/artifacts/research/r3-20261111T1124/reproduction
```

Succeeded on 1,800 rows, reproducing Data's **entire new/combined shortcut summaries exactly**, including 53/80 longest-character agreement on new intent validation. Standard library only, Python 3.12 via the existing base uv environment; no model extra, new dependency, network research, tokenizer or fitted model. Output: `reproduction/audit.json`. Use a new output directory for any further execution; existing directories are refused. The caller must keep `--output-dir` under shared `artifacts/research/`; the CLI does not enforce output ownership, and must not be pointed at another team's storage.

The script deliberately pins the first frozen pre-review-r2 manifest and Data receipt, not any eventual v2 release. All 18 shard hashes/counts/splits are verified; the six original v1 shard entries must be present unchanged. It rejects paths outside the pilot-v1/v2 data roots and non-train/validation splits, duplicate candidate IDs, inherited/added group overlap and candidate cross-split groups. It records source and script hashes. These guards protect the bounded analysis input; they do not certify labels or replace Data's validator.

It imports `shortcut_summary` from the unchanged `audit_pilot_shortcuts.py`; the helper hash must match Data's receipt. R2's complete audit main, sentiment wording decoder and full pair scan are **not** called. Inherited shortcut results are reused from the hash-pinned Data receipt; no new R2 investigation occurs.

## Definitions and comparability

- Fixed selectors: first/last option, longest/shortest characters, longest normalized words. Ties pick the first input option. Uniform expected agreement is mean `1/K`.
- Training priors use only the supplied stratum's training rows, pooled across its families. Producer summaries instead use producer-local training rows. Do not compare their count-prior scores as if their fitting populations matched. Fixed selectors themselves have no fitted counts.
- Training option-prior agreement is a resubstitution description, not held-out evidence. Validation labels never fit those counts. No threshold/model is tuned by the script.
- Publication-cycle statistics use family/split/choice-count counters in supplied order; pooled and producer counters have different boundaries. This is unavailable publication metadata for independent-example inference, not a model baseline or proof of permutation sensitivity.
- “New” means candidate shards absent from the original parent shard list; inherited entries are verified unchanged and current IDs are unique. It does not prove independent authorship or semantic novelty.
- Exact reproduction of Data's summary confirms consistent execution, not independent methodology. Counts share the reviewed R2 implementation.

## Other bounded evidence, not reexecuted by this companion

Artifact root: `/Users/destiner/Code/jeff/artifacts/research/r3-20261111T1124/`.

- `construction/report.md`, `producer-diagnostics.json`, `sentiment-availability-style.json`, selected-row receipts: fresh subagent inspected all six generators without executing them, all new shard hashes, option/style counts, and bounded published cases. Target classes were decoded from literal producer style tables via AST inspection; R2's v1-only sentiment decoder was not broadened speculatively.
- `breadth/report.md`, `bounded-evidence.json`, `policy-counts.json`: fresh subagent counted assignment/domain/mechanism/policy units, inspected selected published rows and structured specifications. Unique policy objects are within-group exact JSON configurations, not independent semantic policies.
- `lineage/findings.md`, `evidence.json`, `scope-and-audit-comparison.json`: fresh subagent independently verified candidate/v1/tiny hash and identity/split relationships, exact canonical input and state-only exclusion. It read Data's boundary implementation, did not execute the mutable Data checkout, and did not read Evaluation rows.
- Data `quality-audit/audit.json`: existing all-pairs lexical scan reused, not rerun. Data's tokenizer/label-review receipts remain explicitly Data-reported.

The manual analysis receipts are bounded evidence, not a generic rerunnable semantic validator. The companion reproduces the material fixed-selector counts; do not imply it reproduces all manual judgments or probe exclusion. No software test, lint, benchmark suite, dataset mutation or ML execution is involved.

## Integration evidence

Build the Research branch before the exact-commit merge:

```sh
uv build --no-sources \
  --out-dir /Users/destiner/Code/jeff/artifacts/research/r3-20261111T1124/branch-build
```

The branch build above succeeded, producing a wheel and source distribution (`branch-build.log`). A fresh read-only review found no blocker in the report, companion or evidence; its output-path caveat is documented above. The main integration additionally runs `uv build --no-sources` while holding only Research's atomically acquired shared merge lock. The final handoff and `integration-receipt.txt` record actual implementation/main commits and build outcomes; this command listing alone is not evidence of successful integration. No tests/linting are authorized.

Data's `006-v2-review-findings-and-revisions.md` announces new immutable option/wording revisions. If their shards change, this pinned companion intentionally fails rather than assigning old results to the new version. A narrowly scoped later delta audit may reuse the same R2 helpers on the new frozen identity; it is not a reason to rerun the entire investigation or delay publication for Research approval.
