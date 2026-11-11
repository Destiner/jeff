# Execution evidence

No software tests, test suites, test runners, linters, or paid calls were used. Evidence consists of actual dataset validation/assembly, prediction-file evaluation, build, and installed-wheel execution. Error handling was source-reviewed, not fault-injected as a software test suite.

## Environment and build

- Started from committed main `1bf5236` in a new `worker/evaluation` branch / `.worktrees/evaluation` worktree before edits.
- Safely incorporated Lead-authorized `1f64aea` after read-only subagents completed; merge commit `1780121`. Did not merge to main or incorporate other worker branches.
- `uv sync --locked` succeeded with Python 3.12.16, no ML extras. Initial tiny baseline executions before packaging used Python 3.9.6 via `PYTHONPATH=src`.
- Before the setup sync, a staged evaluation-only wheel build succeeded using a copy of integrator packaging at `evaluation/build-20261111T1034/`. This was not an integrated project build.
- After final implementation, the following commands succeeded from the evaluation worktree:

```sh
uv build --no-sources --out-dir /Users/destiner/Code/jeff/artifacts/evaluation/build-final-v1/dist
uv venv --python 3.12 /Users/destiner/Code/jeff/artifacts/evaluation/build-final-v1/env
uv pip install --python /Users/destiner/Code/jeff/artifacts/evaluation/build-final-v1/env/bin/python --no-deps /Users/destiner/Code/jeff/artifacts/evaluation/build-final-v1/dist/jeff-0.1.0-py3-none-any.whl
```

Actual installed-wheel execution from outside the source checkout:

```sh
cd /Users/destiner/Code/jeff/artifacts/evaluation/build-final-v1
env -u PYTHONPATH ./env/bin/python -m jeff.evaluation.compare \
  --examples /Users/destiner/Code/jeff/artifacts/evaluation/data-pilot-v1/validation.jsonl \
  --predictions uniform=/Users/destiner/Code/jeff/artifacts/evaluation/pilot-baselines-v1/uniform.jsonl \
  --predictions lexical=/Users/destiner/Code/jeff/artifacts/evaluation/pilot-baselines-v1/lexical.jsonl \
  --output /Users/destiner/Code/jeff/artifacts/evaluation/build-final-v1/pilot-wheel-comparison.json
```

It scored 60/60 examples for both predictors successfully. Wheel and source distribution are both available under that build directory. This package contains Evaluation and the shared package scaffold, not the other workers' unmerged code.

## Executed model-evaluation/data operations

- `prepare`, `baseline` (uniform and lexical), `score`, `compare` on Data tiny-v1 validation: completed with zero prediction failures.
- `curate` on the separate validation curator's source cases: froze 24 presentations / 12 groups and pair map; original teacher labels retained.
- Final curation: structurally validated and froze 24 separate final groups, recorded hashes. No final label-free export, baseline predictions, model inference, or scores. No final content in public handoffs.
- `assemble` on Data pilot-v1 manifest: verified 3 validation shard hashes, counts, splits; froze 60 unchanged references / 12 groups with source receipt. No training shards read by assembly.
- `prepare`, two `baseline` calls, and `compare` on the assembled pilot: completed, 60/60 valid each.
- `compare` on Model tiny baseline/trained outputs with simple baselines: completed on the same 3 tiny references.
- `compare` and `order` on Model tiny-probe baseline/trained outputs: completed on the same 24 probe presentations / 12 reversal pairs. Model, not Evaluation, performed all inference.
- `order` on both simple probe baselines: completed, explicitly distinguishing tie-driven choice changes from probability changes.

Frozen outputs are never overwritten. Unique identifiers containing clock-like strings are artifact IDs, not claimed precise timestamps. All final source data remain separate from validation-derived findings.

## Review and remaining boundaries

Metrics specification, validation failure discovery, and final curation were delegated separately, with serialized lead edits. Follow-up metrics source review identified two low-severity issues, now fixed: fatal comparisons return exit 2 rather than the report-written issues code 1; curation validates rows before publishing its shard. No software test execution is claimed.

Data's reported cross-split/group/duplicate validation is referenced, not reproduced by the single-file scorer. Final release still requires checkpoint/configuration freeze and an isolation-preserving contamination review. No trained pilot result exists in this handoff; label-free pilot inputs are ready for Model's next task. Synthetic teacher labels, few source groups, a random initial scoring head, and tiny training are major limitations.
