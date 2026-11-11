# E3 — released-v2 comparison protocol

E1/E2 are complete. E3 adds an identity boundary and a pinned execution recipe;
scoring, probability validation, group comparisons, order analysis and Markdown
rendering remain the existing pipeline. Final evaluation remains sealed.

## Pre-result interpretation

Primary evidence is **newly authored v2 validation**, separate from unchanged
inherited-v1 validation and existing independent probes. “Independent probes”
means separately authored source cases, not untouched final evidence: the probes
already influenced development. Combined v2 is a convenience summary, not a
second independent sample or a substitute for the strata.

Compare uniform, lexical, four fresh M4 starting/trained snapshots, and preserved
M2/M3 trained candidates where available. The all-MiniLM starting scalar head is
random and weak; the MS MARCO pretrained head is retained. Historical trained
checkpoints are not fresh starts. Match exact ordered input identities and
prediction hashes before reusing old inherited/probe inference. Ask Model only
for missing predictions; Evaluation runs no competing model job.

Follow Model's pre-result descriptive gate (`docs/model/m4-v2-plan.md`): a v2
candidate improves over its own start only if new-v2 agreement increases **and**
log loss decreases. A robustness improvement over its v1 predecessor additionally
requires no family-level agreement or log-loss regression on inherited/probe
strata. Otherwise expose the trade-off. This is not a significance test or an
automatic model-selection policy. No new default is selected by this study.

## Freeze and execution

1. Consume Data's immutable publication handoff, not a pre-review filename or
   stable example IDs. Revisions may change content while retaining ancestry.
2. Assemble validation using the existing assembler. Use
   [the identity freeze](e3-freeze.md) with complete v1 ancestry, published source
   provenance, explicit reviewed source allowlist and separately pinned probes.
3. Independently check released training against historical validation and probes
   for IDs, groups and exact decision content. Record scope/hashes; non-detection
   is not semantic-derivative clearance or proof of producer access history.
4. Export combined/inherited/new label-free inputs; prepare exact reversals of
   v2 originals. Existing probes already contain paired presentations. Publish
   hashes/paths directly to Model without source labels or a lead approval gate.
5. Bind returned prediction receipts to those inputs and checkpoint roles. Reuse
   valid old predictions rather than rerun E2. Execute the pinned
   [study recipe](e3-study.md), retaining missing, invalid, duplicate, unknown and
   unidentifiable predictions in reports. Known subset exclusions are audited.
6. Review numerical/narrative facts, build the package, and self-integrate owned
   paths using the current shared merge-lock protocol. Intermediate handoffs are
   append-only; one final assignment report follows completed delivery.

## Required evidence and limitations

- Full coverage/failure counts and denominators for each candidate and stratum;
  paired common-valid denominators cannot silently replace full coverage.
- Agreement, log loss, Brier and descriptive reliability diagnostics. Neither
  normalized probabilities nor a small descriptive ECE establishes calibration.
- Per-family and declared source-group results, explicit gains and regressions,
  plus named-domain/mechanism summaries where published assignments support them.
  Reversals, policy variants and singleton author IDs are not independent samples.
- Preserve actual label provenance: teacher agreement, source-label agreement,
  rule verification and human verification are not interchangeable. `label_basis`,
  not `kind`, defines interpretation. Same-alias teacher review is not independent
  ground truth; unknown probe teacher and unpinned model revisions stay explicit.
- Rule mechanism holdouts are not a seen-mechanism stratum. Shared primitives
  limit claims of wholly unseen computation. Report this missing coverage rather
  than deriving it from filenames or group counts.
- Include published residual construction shortcuts and revision lineage. Newly
  authored does not mean externally sampled, untouched, or shortcut-free.
- Same input/data/seed/update budgets do not make different pretrained models a
  head-only ablation. Versus v1, data mixture and update count change together.

## Resources and completed preparation

Timur explicitly transferred the parked owner's clean `worker/evaluation`
workspace. It was adopted, not recreated; E1/E2 and their artifacts are intact.
Fresh bounded agents inspected identity provenance and existing tooling, built
small freeze/study helpers in isolated task worktrees, and independently reviewed
both. Review fixes cover honest optional Git provenance for installed wheels and
full-row equality between comparison/order references.

A wheel installed without ML extras successfully assembled/froze revised
candidate `pre-review-r3` and ran its new-v2 uniform/lexical comparison, outside
an owning Git checkout. Evidence: `artifacts/evaluation/e3-packaging-v1/`,
`e3-r3-development-{assembly,freeze,study}-v1/`. These are explicitly candidate-only
preparation, not released M4 results. Source/receipt hashes distinguish revisions.
No software tests, linting, ML loads, separately billed services or final-data
access. Additional actual/pending spend £0; paid allocation £0.
