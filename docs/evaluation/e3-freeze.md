# E3 validation identity freeze

`python -m jeff.evaluation.freeze` partitions **validation development evidence**,
not final evaluation. It reuses the existing contract validators, exclusive
writers, and `input_only`; it does not load models, change labels, or generate
another set of reversals.

## Inputs and invocation

Run from the evaluation checkout with `PYTHONPATH=src` and the shared
`JEFF_ARTIFACTS_DIR`. First use `jeff.evaluation.assemble` to assemble validation
from the chosen source manifest. Supply the **complete Data v1 manifest**, e.g.
`manifests/data/pilot-v1.json`, not the validation-only
`manifests/evaluation/data-pilot-v1.json`: historical train IDs, groups and
content are necessary ancestry exclusions.

```sh
python -m jeff.evaluation.freeze \
  --examples /absolute/assembled/validation.jsonl \
  --v1-manifest manifests/data/pilot-v1.json \
  --source-manifest /absolute/published/manifest.json \
  --provenance /absolute/published/manifest.provenance.json \
  --new-sources /absolute/released-new-sources.json \
  --probes "$JEFF_ARTIFACTS_DIR/evaluation/probes-v1/validation.jsonl" \
  --publication-status released \
  --output-dir "$JEFF_ARTIFACTS_DIR/evaluation/e3-<unique-revision>"
```

`--new-sources` is a JSON array of **exact** `provenance.source` values, not
prefixes, filenames, or regexes. Alternatively repeat `--new-source VALUE`.
The combined allowlist must exactly cover the newly authored validation sources;
unused entries also fail. Obtain the list from the released authoring/provenance
handoff; this is an explicit caller attestation, not inferred publication status.
The provenance file must identify the source dataset and pin the supplied full
v1 parent manifest hash and dataset ID. The helper pins the provenance bytes but
does not recursively verify every artifact cited inside that document.

For unreleased preparation use `--publication-status candidate`. Neither the
flag nor the resulting evaluation manifests publish a Data release. A release
requires Data's own publication handoff. Do not silently reuse a candidate freeze
when a successor changes rows under stable IDs: assemble and freeze the released
bytes into another unique directory and compare canonical row/input identities.

## Checks and classification

- Explicit input/output paths are screened for reserved final components before
  reads. Every manifest shard declaration is screened before its shards are
  opened. Final splits and the reserved final family are rejected. Output must
  be a new direct child of `artifacts/evaluation/`; existing destinations fail
  before input reading. No final override exists.
- All v1 train **and** validation shard bytes, hashes, counts, splits, unique IDs,
  reference fields and group/split consistency are checked. Train is read using
  strict JSON records and `validate_input`, never `load_examples`, and its split
  is not rewritten to pass an evaluation reader.
- Source v2 validation shard hashes/counts/splits are verified. The combined
  source references must exactly match assembled full canonical rows by ID.
  Row permutation is allowed and recorded; option order and all metadata must
  match. Frozen subsets preserve assembled order. V2 train declarations are
  screened, but their content is intentionally not read or verified here.
- **inherited-v1:** historical ID plus identical full canonical labeled row,
  including its validation split. Every old validation row must remain present.
  A changed historical ID or historical train ID is an error, never fresh data.
- **new-v2:** no historical ID, group, or order-independent decision-content
  collision against *all* v1 rows and existing probes, plus exact source
  allowlist membership. A new ID in an old group/content is an error, not an
  implicitly excluded derivative. Every assembled row must be classified.
- **probes:** separately pinned, nonempty validation reference, copied as-is.
  Parent/probe overlap and candidate/probe overlap fail. Existing presentation
  variants remain variants; no re-reversal or additional independent cases are
  claimed. `identities.jsonl` retains group and content identities for pairing.

Order-independent content means exact state, exact question, and the sorted
multiset of option texts, ignoring option IDs and order. No lexical normalization
removes punctuation, signs, brackets, case, or whitespace. This catches exact
identity reuse, not semantic derivatives or unrecorded access history.

## Outputs and receipt

Each of `inherited-v1/`, `new-v2/`, and `probes/` contains:

- `validation.jsonl`: immutable-by-exclusive-creation labeled references;
- `inputs.jsonl`: allowlisted label-free model inputs;
- `manifest.json`: validation-only shard path/hash/count (not a Data release).

Root `identities.jsonl` records every emitted row's stratum, split, group, family,
raw provenance, source shard/file hash and line, canonical full-row hash,
canonical full-input hash and order-free content hash. `parent-identities.jsonl`
also records the complete train+validation ancestry. Canonical hashes use UTF-8
JSON with sorted keys, compact separators, `ensure_ascii=False`, and
`allow_nan=False`; JSON object key order is irrelevant, array order is not.

`receipt.json` pins manifests, provenance, allowlist file if supplied, assembled
examples, probes, consumed shards and helper source, plus the Git revision and
tracked-dirty flag. Inputs are fingerprinted again before output creation. It
records classification/order/hash policy, publication status, output hashes,
row/group counts and distributions by family, **label_basis** and exact source.
The receipt is written last; a directory without it is incomplete, not a freeze
to reuse. Failed/partial output directories are never overwritten on retry.

Interpret metrics by **label_basis**, not provenance `kind`: a teacher-authored
rule can still carry `rule_verified`. Mixed aggregates are supplied-label
agreement, not uniformly independently verified accuracy. Unknown teacher
identity stays unknown. Historical validation and probes are reused development
evidence; newly authored v2 is not untouched final evidence. Source groups and
original/reversed presentations are not independent rows. Semantic exclusion,
assignment/authoring verification, training-boundary validation and release
approval remain with Data; final build and integration remain with the owner.

## Executed candidate preparation

Executed CPU-only from isolated branch `task/evaluation-e3-freeze`, based on
`17e9e0ae35ee492913e846c213826911408bc416`, against:

- `artifacts/data/data-pilot-v2/pre-review-r2/manifest.json`, SHA-256
  `345e935b46ca3d1226dfd603208bf5d1e1e16982d425319f678e34447b0c9483`;
- its `manifest.provenance.json`, SHA-256
  `6dfefde6fa272fb1d4c893d544be81f3a65ecaaeae4aae46c28d42bcdf6012e4`;
- complete `manifests/data/pilot-v1.json` and existing
  `artifacts/evaluation/probes-v1/validation.jsonl`.

Actual workflow: ran the existing assembler into
`artifacts/evaluation/e3-freeze-development-assembly-v1/`; serialized the 84
observed exact new-source values after excluding parent IDs into its
`candidate-new-sources.json`; then invoked this helper with those paths,
`--publication-status candidate`, and output
`artifacts/evaluation/e3-freeze-development-v1/`. This observed-source list is
**candidate-only**, not a released-source attestation. The receipt pins 19 files.

| Partition | Rows | Groups | Rows by intent / sentiment / rules |
| --- | ---: | ---: | --- |
| inherited-v1 | 60 | 12 | 20 / 20 / 20 |
| new-v2 | 240 | 170 | 80 / 80 / 80 |
| probes | 24 | 12 | 8 / 8 / 8 |

Inherited labels: 40 teacher / 20 rule-verified. New labels: 160 teacher / 80
rule-verified. Probes: 24 teacher, teacher identity unknown. Existing probes
already include original/reversed presentations; no new reversals were made.

This is an actual **candidate development freeze, never a published release**.
The consulted Data handoff `006-v2-review-findings-and-revisions.md` still awaits
superseding intent/sentiment revisions; no final Data publication is claimed.
Identity-review evidence consulted:
`artifacts/evaluation/e3-identity-review-v1/findings.md`.
No tests, lint, syntax-check substitutes, dependency installation, ML loads,
paid calls, final-data access, main merges or owner-workspace edits were run.
Package build and integration are explicitly left to the owner.
