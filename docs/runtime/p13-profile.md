# P13: named M12 readout profile

This is a source-only extension of the [P6 readout contract](p6-readout-contract.md), not executed compatibility evidence or permission to run. No model, tokenizer or weights were loaded; no ML imports, tests, lint, dependency installation or network access were used. Package builds are a separate integration gate, not executed model compatibility evidence.

## Exact profile dispatch

`src/jeff/runtime/qwen_readout.py` dispatches only these named recipe profiles and crosslinks each to its source receipt schema:

| Recipe profile | Required receipt schema | Learning rate | Maximum run seconds |
| --- | --- | --- | --- |
| `m8.recipe.v1` | `m8.train.v1` | `2e-6` | `2700` |
| `m12.recipe.v1` | `m12.train.v1` | `0.0002` | `590` |

The original M8 `RECIPE` remains unchanged. M12 inherits every M8 recipe field except `schema_version`, `learning_rate` and `maximum_run_seconds`. Unknown profiles, any other learning rate, changed fixed fields, and receipt/profile mismatches fail closed; in particular an M8 receipt cannot claim the M12 recipe. The referenced recipe file, receipt evidence and manifest recipe hash still crosslink. This is not a generic learning-rate allowance.

Both profiles retain `maximum_capacity_seconds: 600` as an inert recipe field, **not a compute grant**. The authorized aggregate is 900 seconds: Model at most 590 seconds including all audits and export; Runtime P13 at most 310 seconds and no more than the actual aggregate remainder. Model remains the scheduler. The recipe does not implement or expand that external execution authorization.

## Unchanged acceptance boundaries

The v2 manifest and existing proof field tree are unchanged. Historical v1 and no-manifest paths are untouched. Both named profiles retain all existing checks: 1,500 presentations, 375 optimizer attempts/completions, fixed schedule and retained original M7 control, frozen original scope, AdamW betas/epsilon/decay/clipping/foreach, FP32 shapes and aliases, unchanged non-answer rows, controlled config, headroom/resource guards, and START/FINAL coverage and tolerances. No cache, backend, scoring path or additional execution is introduced. Existing M8 exact recipe/receipt acceptance is preserved in source; no executed compatibility claim is made.

## Exact producer backbone counters

For `m12.train.v1` only, the source receipt must contain exactly this type-correct `backbone_forwards` value, agreed with Model in `447df2b2-756d-49fd-a96a-e9b51a525482`:

```json
{"maximum":4500,"attempted":4500,"completed":4500,"by_phase":{"START":{"attempted":1500,"completed":1500},"TRAIN":{"attempted":1500,"completed":1500},"FINAL":{"attempted":1500,"completed":1500}}}
```

The completed receipt is already hash-bound to the v2 manifest and crosslinked to the unchanged proof tree. Missing, partial, extra or bool-coerced counters fail closed. Historical M8 receipts do not acquire a retroactive counter requirement. These fields bind the producer's actual-call evidence; Runtime does not independently replay training or prove historical optimizer correctness.
