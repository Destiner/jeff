# E3 released identity review v1

## Receipt

**Identity/provenance rebind complete; zero unresolved errors. Not semantic clearance.**

- Released manifest: `artifacts/data/data-pilot-v2/manifest.json`, SHA256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`.
- Released provenance SHA256: `a55a3bc0ba76958e6e2b81ef8288c4d2fa008f18bd2ff106a8cb8b0321a4c5e3`.
- 18 released shards; 1,800 rows / unique IDs: 1,500 train, 300 validation. Train 880 groups; validation 182 groups; zero cross-split group intersections.
- Six exact parent shard entries retained, with published/tracked v1 row equality. Inherited 300 train / **60 validation**; new 1,200 train / **240 validation**. Each family has 500 train / 100 validation, including 80 new validation rows.
- All 1,440 new rows join released source metadata, hash-linked assignment metadata, source family/label basis/teacher alias, and matching group split. Output hashes in producer metadata additionally bind five producers. The sixth producer is fully byte-reconstructed as described below. Classification is not based on filenames alone.
- 123 expected-hash comparisons passed: release pin, parent manifest, 33 shard reads (some inherited reads repeated), **75 published source/revision artifacts**, 13 revision-parent artifacts. Zero hash mismatches. Five manifest reads and two independently hashed historical references are additionally recorded.
- **720 revised rows** join exact parent IDs: intent-a 240, intent-b 240, sentiment-b 240. Intent mapping options and parent option texts agree; state/question/group/split/target/order invariants preserved. Sentiment full reconstruction preserves labels, options, question, groups and splits; exactly the documented train-state correction is applied. Full row hashes and raw provenance remain in evidence.

## Exclusion scope

168 zero-hit checks: new-v2 train (1,200) and all released train (1,500), each against pilot-v1 validation (60), tiny validation (3), superseded sentiment validation (20), existing independent probes (24), existing pilot order variants (120), and released validation (300).

For each pairing: IDs, groups, exact ordered decision content, exact order-free decision content; ordered/order-free content with NFC, outer-strip, and combined NFC+outer-strip; and state-only exact/NFC/outer-strip/combined checks. Option IDs are deliberately excluded from decision-content keys. No semantic/near-duplicate clearance or access-history verification is implied. Reused probes remain development evidence, not fresh untouched data.

## Source-label and teacher interpretation

Overall label basis is **1,200 teacher / 600 rule_verified** (validation 200 / 100); do not infer basis from provenance.kind. New rule-a retains `kind=teacher`, `label_basis=rule_verified`; rule-b uses programmatic kind. Same-author rule checking is not independently verified natural-language correctness.

Exact row teacher strings (`gpt-sol` versus `openai/gpt-sol`, provider where present), source aliases, full generation settings, and revised provenance.parent_id/source strings are preserved. Published metadata resolves author/teacher provider to openai and model alias gpt-sol, with immutable revision unavailable. Inherited programmatic rule rows have no row teacher_model; published author identity does not turn these into teacher labels. Sentiment-b revision_author is separately `openai/gpt-astra (exposed alias, immutable revision unknown)`; original teacher judgments remain gpt-sol.

## Explicit metadata qualification and reconciliation

Initial review imposed a redundant direct-output-hash requirement that sentiment-b-r2 metadata does not promise: its settings contain parent hashes and a revision specification, not released output hashes. This produced 240 repeated row diagnostics for one metadata shape. Initial `evidence.json` and execution remain unchanged.

`reconcile.py` independently reconstructs both complete released sentiment-b-r2 JSONL byte streams, including IDs and all provenance, from the hash-verified parent plus the published single-state revision. It does not execute producer code. Reconstructed hashes exactly equal released train `0c2d5441102fb0623dec43265f3d9dc44b025c92b788138344cdc1447ac1ab20` and validation `b739a2e7c56e6d8ec28aa0450276d339e4f53936c71e6b27436a2e5d22ff409e`. All 240 initial diagnostics are resolved; **zero unresolved errors** in `reconciled-evidence.json`. Frozen Data artifacts were not changed. An immediate public caveat handoff was published when this surfaced.

## Per-validation-ID source-unit mapping

Use **`validation-source-units-reviewed.json`**: `by_validation_id` contains all 300 released validation IDs (240 new / 60 inherited), with published producer shard_id, exact assignment group attributes, domain, mechanism, policy instance, source and assignment paths/hashes, exact label basis/provenance, teacher resolution, method, revision author, and binding basis.

No missing unit is fabricated: null plus absent_units is explicit. **80 validation rows lack assignment domain; 160 lack assignment mechanism; 220 lack policy-instance provenance.** Policy instance is the released provenance.scenario_id, not guessed from filenames. Intent/sentiment scenario_plan is retained but is not silently promoted to a named mechanism or policy instance. Inherited rule rows have no policy-instance metadata and remain null.

New rule validation has 80 cases, **40 policy instances within 10 conservative mechanism groups**; training has 400 cases / 200 instances / 20 mechanism groups. Inherited rules add 20 validation cases / 2 mechanism groups and 100 train cases / 10 mechanism groups. There is no exact named rule-mechanism overlap across train/validation. This supports a published held-out-mechanism stratum, not broad unseen-reasoning certification, and does not supply a seen-mechanism rule-validation comparison. Intent/sentiment new validation uses four domains per producer; their mechanism fields are absent. Across all published assignment metadata there are 28 validation domains and 22 named validation mechanisms (including domain-specific v1 intent/sentiment names), none exactly shared with training labels; these heterogeneous names are not interchangeable independent observations.

Producer/method/domain dependence persists: shared teacher aliases, authoring approaches, renderers, style schedules and related policy cases. Group-balanced summaries must preserve these dependencies and inherited/new strata; do not treat 300 rows, 182 groups, named mechanisms and policy instances as iid equivalent sample sizes. Assignment-name nonintersection does not establish semantic mechanism separation.

## Execution and boundaries

Executed from read-only Evaluation worktree using standard-library Python:

```
python3 /Users/destiner/Code/jeff/artifacts/evaluation/e3-release-identity-review-v1/review.py
python3 /Users/destiner/Code/jeff/artifacts/evaluation/e3-release-identity-review-v1/reconcile.py
```

Scripts refuse evidence overwrite; initial and reconciled outputs are separate. Original earlier review/artifacts untouched. Only exclusive new review artifacts and unique public handoffs were written. Worktree remains clean. No source edits, tests, lint, ML, tokenizer, build, spending, final-data reads, commits or main merges. No new default/promotion authorized.
