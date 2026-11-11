# R4 saved-prediction diagnosis: reproduction

Report: [M3 pilot/probe diagnosis](../../docs/research/m3-pilot-probe-diagnosis.md). CPU arithmetic and source inspection only; no inference, model loading, training, labels/data generation, final access, tests or linting.

## Actual canonical command

From `/Users/destiner/Code/jeff/.worktrees/research`:

```sh
uv run --locked python -B experiments/research/diagnose_m3_regression.py \
  --artifacts-dir /Users/destiner/Code/jeff/artifacts \
  --output-dir /Users/destiner/Code/jeff/artifacts/research/r4-20261111T1145/reproduction-final
```

Succeeded using the existing Python 3.12 base uv environment. Output `diagnosis.json` contains 60 pilot rows and 12 original probe rows, all four snapshots, margin/rank evidence, copied Evaluation grouped metrics, M3 group loss attribution, pilot sentiment confusion counts and rule choice-text counts. Output directories must be new children of shared `artifacts/research/`; existing paths are never overwritten.

An earlier successful `reproduction/` run is retained. The final version adds source hashes for the reused helpers; calculations are unchanged. All immutable inputs retain their hashes.

## Reuse, not a second evaluator

- Pins Evaluation's `e2-m3-v2/recipe.json` SHA256 `a456847c240dec875822df8672676ebdee4614c765363405e228c1569887b805` and verifies its recorded report, reference, pair-map and eight M2/M3 start/trained prediction hashes. Only explicitly allowlisted development/reference/prediction directories can be read; `final` path components are rejected.
- Reuses Research's `inspect_validation_delta.read_rows` for unique-ID reading and Evaluation's `metrics.validate_prediction` for the exact accepted-roundoff normalization. Requires complete matching prediction/reference/outcome IDs and exact equality with Evaluation's saved normalized probabilities. No dropped rows or independent replacement scoring policy.
- Reuses Evaluation's existing `overall`, `per_family`, `per_source_group`, correctness and per-row log loss. Adds arithmetic for target rank, signed probability margin, top-two margin and target/rival log ratio; does not reimplement scoring/coverage/grouping machinery or fit a probability transform.
- Reuses the reviewed R2 `sentiment_class` decoder only for the three known **pilot-v1** wording sets, not for unknown probe paraphrases. Pilot rule choices are counted by their existing texts; this is descriptive outcome analysis, not new ground-truth labels.
- Collapses probes using their published pair map, verifying exact reversed option objects and unchanged state/question/target/group/family. Records same-choice counts and maximum probability changes; does not treat reversal presentations as independent cases. Pilot variants remain separate decisions and retain group identity.

## Definitions

For saved normalized probabilities `p`, target `t`, and best rival `r`:

- Target rank: position in descending `p`, using reference option order for ties. None of the four model snapshots ties here.
- Signed target margin: `p[t] - p[r]`; negative means a rival wins.
- Top-two margin: highest minus second-highest probability, always nonnegative; distinct from target margin when target is not top-two.
- Relative score-gap equivalent: `log(p[t] / p[r])`. This equals the raw scalar score difference for these temperature-one softmax snapshots; absolute logits cannot be recovered. The bounded script rejects zero probabilities rather than silently clipping undefined ratios.
- Group contribution to M3 mean-loss improvement: `group_presentations / all_presentations * (starting_group_loss - trained_group_loss)`, using Evaluation's existing group means. Positive is improvement; the contributions sum to the published mean-loss improvement.

Probe groups each have two presentations, so group-macro and presentation-weighted loss coincide up to rounding. Pilot group sizes differ (4 or 10), so its displayed attribution is presentation-weighted, not equal-group macro. Excluding one probe group is explicitly an explanatory decomposition, **not a revised scoring set**.

Parent independently joined pilot rule outcomes to existing reference choices: 7/7 no-result targets correct and 0/13 nonempty/winner targets correct for trained M3. The two newly correct election cases are existing g12:r09/r10. These conclusions can be recovered from the verified reference and saved per-row choices; no new labels were authored.

## Bounded review/source artifacts

Root: `/Users/destiner/Code/jeff/artifacts/research/r4-20261111T1145/`.

- `probability-transitions/`: independent subagent margin/rank tables, complete original-probe and pilot rows, grouped loss contributions and input receipts. Snapshot CSV/JSON are analysis outputs, not training shards.
- `semantics/`: diagnosis against published references, construction counterexamples, and bounded first-12-row training sentiment inspection. No cases/paraphrases were sent to Data; do not use these findings as generation material.
- `recipe/`: historical source hash verification, configuration/optimizer mapping and saved training statistics. Source was read, not imported/executed; no tensor files/model were loaded. `derive_evidence.py` is the subagent's retained stdlib evidence derivation.
- `reproduction-final/diagnosis.json`: canonical owner reproduction with raw-prediction equality and helper/source hashes.

These receipts distinguish Research's arithmetic/qualitative observations from reused Model tokenizer/weight-retention audits and Evaluation metrics. The companion does not reproduce manual semantic judgments or identify causal components.

## Package and integration

Build the branch, then the exact reviewed integration under the shared merge lock:

```sh
uv build --no-sources \
  --out-dir /Users/destiner/Code/jeff/artifacts/research/r4-20261111T1145/branch-build
# Under Research's short owned merge lock, on clean main:
uv build --no-sources
```

The branch build above succeeded, producing wheel and source distribution (`branch-build.log`). A fresh read-only reviewer found no material issue in the numerical claims, duplicate handling, code reuse or one-factor recommendation. Its caution—one new MPS run against a historical control cannot isolate stochastic variation—is already explicit in the report. The final handoff and `integration-receipt.txt` record actual integrated build and exact implementation/main commits; command listings alone are not execution evidence. No tests/linting or hooks that run them are permitted. All tracked edits remain Research-owned.

Exactly one later experiment is specified in the report: change only M3 scalar-head LR under historical frozen-v1 controls. It is a recommendation requiring a subsequent decision, not code or authorization to launch training. Frozen M4 is untouched.
