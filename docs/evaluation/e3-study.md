# E3 pinned CPU study recipe

`python -m jeff.evaluation.study` orchestrates the existing **compare → order
(optional) → render** CLIs. It implements no metrics, inference, training, or
candidate selection. Each named stratum has its own exact validation reference;
use `combined`, `inherited-v1`, `new-v2`, and `probes` as separate strata after
[identity freezing](e3-freeze.md). Names do not establish ancestry: consume the
freeze's identities/receipt and Data's publication handoff. Overlapping combined
and inherited/new rows are intentionally not additional independent evidence.

## Minimal recipe

Use the owner's existing CPU environment; no dependency installation is needed.
Set absolute paths and create a new config/output namespace, never reuse one:

```sh
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
export PYTHONPATH=/Users/destiner/Code/jeff/.worktrees/evaluation-e3-report/src
PY=/Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python

# config.json is prepared with the schema below and actual SHA-256 pins.
"$PY" -m jeff.evaluation.study \
  --config "$JEFF_ARTIFACTS_DIR/evaluation/e3-study-unique/config.json" \
  --output-dir "$JEFF_ARTIFACTS_DIR/evaluation/e3-study-unique/run"
```

Every file declaration is `{"path": "/absolute/path", "sha256": "64 lowercase hex characters"}`.
Create pins with `jeff.evaluation.common.fingerprint(path)` after freezing the
source bytes. File paths are absolute, not relative to config, cwd, or artifact
root. The minimal config is:

```json
{
  "schema_version": "e3-study/1",
  "status": "candidate-only",
  "baselines": ["uniform", "lexical"],
  "strata": {
    "new-v2": {
      "examples": {"path": "/absolute/new-v2/validation.jsonl", "sha256": "<actual sha256>"},
      "predictors": {}
    }
  }
}
```

This baseline-only recipe is useful for a **new development question**, not a
reason to repeatedly rescore completed E2 references. `released-validation` is
the other supported status; it is a caller assertion, not publication approval.
Candidate-only results must never be presented as released M4 results.

Baselines default to uniform and lexical; an explicit list may contain either,
both, or neither, without duplicates. Each stratum needs at least two predictors
in total because the existing comparison CLI requires them. Baselines call only
`baseline.predict(input_only(row), method)`: only stripped input fields and
stripped option id/text reach baseline code, never labels or provenance. This
uses the existing baseline definitions, including input-order tie breaking.

## Candidate sources and optional order evidence

Add named predictors inside each stratum. A predictor has:

- `role`: exactly `fresh-start`, `v2-trained`, or `historical-retained`.
  Retained M2/M3 candidates are **historical-retained**, never fresh pretrained
  controls. Use unambiguous predictor names too; the stock Markdown renderer
  displays names, while roles remain in config/receipt.
- `sources`: nonempty array of source declarations. Each has a required
  `predictions` file pin, and optionally **one** of `source_reference` or
  `source_inputs`, also file pins. These define the declared source universe.
- Optional `order_sources`: another nonempty source array for order analysis.
- Optional `reference` and `inputs` pins on each source: caller-provided
  reference/input fingerprint attestations. They do not prove checkpoint
  identity or that inference really consumed those bytes. `reference` files
  are validated as nonempty validation-only references; an `inputs` attestation
  alone does not establish an exclusion universe.

For example, a predictor entry (replace every pin with actual values) is:

```json
"m4-minilm-trained": {
  "role": "v2-trained",
  "sources": [{
    "predictions": {"path": "/absolute/model/order-bundle.jsonl", "sha256": "<actual sha256>"},
    "source_reference": {"path": "/absolute/order/validation.jsonl", "sha256": "<actual sha256>"},
    "inputs": {"path": "/absolute/order/inputs.jsonl", "sha256": "<actual sha256>"}
  }],
  "order_sources": [{
    "predictions": {"path": "/absolute/model/order-bundle.jsonl", "sha256": "<same actual sha256>"},
    "source_reference": {"path": "/absolute/order/validation.jsonl", "sha256": "<same actual sha256>"}
  }]
}
```

At stratum level supply **both** `order_examples` and `order_pairs` pins to
request order analysis. Before scoring, the study requires each comparison row
to equal the corresponding full order-reference row, including state, question,
option text/order and provenance. The existing order CLI validates exact reversal
pairs, group consistency and full pair coverage; the existing renderer requires
comparison IDs to equal originals or all presentations, with exactly matching
predictor probabilities/statuses. Prefer reusing a same-snapshot order bundle
for comparison originals and order sources as above: the split is audited and
does not perform fresh inference. If separate comparison and order snapshots
disagree, rendering fails, rather than presenting mismatched evidence.

A simple alternative is to provide **already exact per-stratum prediction
files** in `sources`, with no source universe. No preprocessing convention or
new model output format is required. Optional attestations remain independently
pinned. Multiple raw source files are concatenated in declaration order, not
joined into a dictionary or deduplicated.

### Exclusion and failure policy

For each comparison/order bundle, retain every raw source line unless its
strictly parsed, nonempty string ID is outside the target reference **and is
inside the explicitly declared source universe**. Universe IDs come only from
validated pinned `source_reference` rows or validated pinned `source_inputs`.
The latter must have only allowlisted label-free top-level fields and stripped
option fields, valid inputs, and unique IDs. Never supply an arbitrary ID list
as the universe. A source declaration attests which complete reference/input
universe its predictions cover; the helper cannot authenticate the producer.

- Duplicate target rows, invalid probabilities, malformed JSON, non-object
  records, missing IDs, and unknown extra IDs remain visible to the scorer.
- Known out-of-stratum rows may be excluded even if their probability payload
  is invalid, but only if their ID is strictly identifiable. Parse failures
  cannot justify exclusion. Every excluded source line/ID is recorded.
- Raw bytes/probabilities are never normalized or JSON-reserialized. A missing
  final line terminator gets a newline when concatenating, to preserve record
  separation. Duplicate JSON keys/nonfinite constants remain invalid records.
- No missing predictions are filled in. Comparison exit 1 (prediction issues)
  is reportable and rendering continues; order exit 1 is likewise reportable
  if it emitted its report. Exit 2, unexpected exits, or absent output are
  fatal. The helper itself returns success for a completed issue-bearing study;
  inspect command return codes and scorer coverage/issues, not just helper exit.
- Unsupported byte encodings or underlying CLI failures may be fatal, with a
  command receipt and incomplete directory rather than a misleading result.

`subsets.json` records source declarations/hashes, kept/unidentifiable counts,
each excluded known line/ID and each retained unknown-extra line/ID. Scorer JSON
and Markdown retain missing/invalid/duplicate denominators and issue counts.
An unknown extra is never quietly assumed to belong to another stratum.

## Boundaries and receipts

Output must be a new directory under `$JEFF_ARTIFACTS_DIR/evaluation/`, outside
reserved final paths. Use exclusive immutable namespaces such as
`e3-study-<revision>/run`. Existing destinations fail before config reads.
Explicit paths and resolved symlinks with `final`, `final-…`, `final.…`, or
`final_…` components are rejected; all file declarations in the config are
screened before any target file is hashed/opened. No `--allow-final` exists.
All actual references must be nonempty validation-only; misleading filenames
cannot authorize final splits. This is procedural protection, not a filesystem
sandbox or recursive verification of arbitrary documents cited by a config.

The recipe saves config, exclusive prediction bundles, comparison/order JSON,
Markdown, command stdout/stderr/exit receipts, and subset audit. It invokes the
same Python executable with this checkout's `src` first on `PYTHONPATH`.
`receipt.json`, written **last**, records commands and output hashes, config and
source pins, and hashes of the helper/baseline/common/metrics/CLI implementations.
All input pins, including code/config, are rechecked immediately before that
completion receipt. A directory without it is incomplete; retry in a new
namespace, never patch an old study. External mutation after completion is not
prevented by filesystem permissions; hashes make it detectable.

This is one explicit recipe, not a scheduler or M4 readiness detector. Omitted
predictors/strata are **not evaluated**, not zero coverage; provide prediction
files (including genuinely empty files) for intended-but-missing predictions
to get scorer coverage. Omitted order sources mean **no order conclusion**.
No inference, reverse generation, training-boundary verification, publication
approval, statistical independence claim, calibration claim, default promotion,
or validation-to-final upgrade is implied. Per-family/group metrics and paired
valid denominators come directly from the existing tools.

## Executed development evidence

Executed CPU-only using the owner Python above, against the frozen candidate
`artifacts/evaluation/e3-freeze-development-v1/new-v2/validation.jsonl`, SHA-256
`24af789c76500be252d81e0e294f32dd54fac08c059971044866ad328e6b1fc9`.
The config was created with `common.fingerprint` and `common.write_json` under
`artifacts/evaluation/e3-study-development-v1/config.json`; it is the minimal
baseline-only schema above with the actual absolute reference/pin.

Exact completed final-code invocation:

```sh
cd /Users/destiner/Code/jeff/.worktrees/evaluation-e3-report
JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts PYTHONPATH="$PWD/src" \
  /Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python \
  -m jeff.evaluation.study \
  --config /Users/destiner/Code/jeff/artifacts/evaluation/e3-study-development-v1/config.json \
  --output-dir /Users/destiner/Code/jeff/artifacts/evaluation/e3-study-development-v1/run-v2
```

The earlier `run/` directory is an immutable initial execution before tightening
role/reference-attestation validation; its pinned source hashes distinguish it.
The final-code `run-v2/receipt.json` records compare/render commands and hashes.

| Predictor | Valid / rows | Supplied-label agreement | Natural-log loss |
| --- | ---: | ---: | ---: |
| Uniform | 240 / 240 | 65 / 240 | 1.333463 |
| Lexical | 240 / 240 | 79 / 240 | 1.314932 |

These are **candidate-only baseline results, not M4 results**: 240 new-v2 rows,
170 declared source groups; 160 teacher / 80 rule-verified labels. No inherited
or probe rescore, no M4/preserved model predictions, no order evidence, and no
claim about a released Data successor. Merged-model filtering and order paths
are supported but not exercised by this bounded baseline execution. No tests,
lint, syntax checks, build/dependency installation, ML/model loads, spending,
final-data reads, or main merge were performed. Packaging/integration remains
with the owner.
