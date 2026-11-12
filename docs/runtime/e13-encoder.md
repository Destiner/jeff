# E13 encoder — source-only handoff

Prepared against lead minimal E13 preparation d02118e6. No imports, model execution, tokenizer invocation, weight reads, tests, lint, network, build, or commit performed during implementation. This is not a successful native run or a supervision grant.

## Child interface

`src/jeff/runtime/external_encoder.py --binding ABSOLUTE_JSON --output-dir NEW_ABSOLUTE_DIRECTORY`

One invocation loads exactly one of `msmarco-start`, `m9`, or `m11`. No arbitrary candidate/checkpoint, alternate backend, fallback, startup forward, training, or retries. Reuses the authenticated frozen P10 `predict.py` helper API (`decode`, `same`, `CHECKPOINT_FILES`), without modifying or invoking its `main`. Loads through existing `load_checkpoint` and predicts through existing `_rows` / `_write_batch` and unchanged retained scorer.

Controls are FP32/MPS, four Torch threads, temperature 1, decision batch 4 including final short batch, token cap 256. Before **each** scorer batch the same loaded tokenizer encodes complete pairs from source-owned `cross_encoder._FORMAT`, with special tokens and `truncation=False`. Any pair over 256 stops before scorer/native forward. Admitted pairs therefore lose nothing under the scorer's unchanged `longest_first` setting. Native pre-hook also checks attention-mask lengths against complete lengths. Receipt distinguishes configured truncation from zero actual truncated pairs; there is no claim that the native scorer has been changed to disable truncation.

## Frozen identities

All paths below are under `/Users/destiner/Code/jeff/artifacts/`. Metadata hashes and helper hash are frozen in source. Exact seven-file hash/size inventories are read from authenticated existing metadata and all actual checkpoint bytes are validated only during a later authorized execution.

| Role | Checkpoint | Existing inventory source |
| --- | --- | --- |
| msmarco-start | `model/m4-v2-20261111-01/msmarco/baseline` | `model/m4-v2-20261111-01/checkpoint-inventory.json`, `checkpoints['msmarco-baseline']` |
| m9 | `model/m9-msmarco-duration-20261111-01/training/checkpoint` | `release/p11-m9-20261112-01/preparation/checkpoint-plan.json`, `checkpoint_files` |
| m11 | `model/m11-msmarco-duration30-20261112-01/training/checkpoint` | `release/p10-m11-20261112-01/binding.json`, `checkpoint_files` |

Original M4 weight hash is `a6e1fd85181a93a58bc33f65700f2ba34da3af2667f85cc57bcdf0f9f0092200`. Its historical inventory explicitly says **post-inference inventory, not pre-load attestation**; that qualification is retained in the receipt. Nothing here upgrades that historical evidence.

## Binding and input manifest

`configs/runtime/e13-encoder.json` is intentionally non-runnable: grant, deadline ceiling, actual counts, executable pins, supervisor and input manifest references remain null. Select one fixed role per child. Actual `max_seconds` must be positive and <=600; the external owner may impose a shorter remaining budget. Actual grant context IDs must be nonempty. These strings do not themselves grant compute.

`executable_sources` maps absolute paths to actual SHA256 values. Required paths: this child, frozen P10 helper, separate supervisor, worktree `pyproject.toml` / `uv.lock`, and `src/jeff/{__init__.py,model/__init__.py,model/scorer.py,model/predict.py,model/cross_encoder.py}`. Additional executable pins may be supplied. Imported model module origins and their bytes are rechecked.

Input manifest exact fields:

```json
{
  "schema_version": "e13.exploration.inputs.v1",
  "candidate": "msmarco-start",
  "validation_only_never_train": true,
  "release": {"path": null, "sha256": null},
  "pair_map": {"path": null, "sha256": null},
  "datasets": [
    {"name": "e13-native", "path": null, "sha256": null, "rows": null},
    {"name": "e13-reversed", "path": null, "sha256": null, "rows": null}
  ]
}
```

Nulls above are documentation placeholders and fail. Dataset hashes must match actual bytes; decision-only rows pass existing native schema validation. Exactly two suites, equal positive actual row counts <=200, unique IDs within each suite. No matching-ID assumption across orientations: explicit pair-map bytes/hash are retained and Evaluation owns the join. Final/reference/unreleased paths and all symlink paths are rejected, including ancestor symlinks.

`expected` is populated from released actual inputs: `calls=sum(ceil(suite_rows/4))`, `decisions=sum(suite_rows)`, `pairs=sum(len(row.options))`. No startup calls. Count binding is checked before load.

## Evidence and remaining owner interface

`receipt.json` records binding/source/metadata/input identities, verified checkpoint inventory, controls, per-batch complete lengths, attempted/completed native calls and candidate pairs, completed writes, and output hashes/physical lines including partials. Output files are `e13-native.jsonl` and `e13-reversed.jsonl`; existing prediction schema is unchanged. Failed writes are not equated with completed native forwards. No cleanup/retry hides partial evidence.

RSS <=8 GiB and sampled MPS driver <=8 GiB are separate limits. Required headroom is `recommended_max_memory - driver >=2 GiB`, not physical free RAM. Pre-Torch phases sample RSS only; MPS telemetry starts only after Torch import. Samples are not continuous peaks. Guards are cooperative, including per-file checkpoints during hash verification; they cannot kill a hung load/forward or enforce a process-tree ceiling.

**Blockers before use:** Data/Evaluation must release actual manifest/dataset/pair-map bytes; Model must provide a fresh exact role/remaining-time grant; external owner must freeze executable/source pins, fill actual counts and supervisor binding, and implement full process-group supervision/deadline/partial collection. No supervisor is supplied or executed in this bounded task. No native behavior, build, or source syntax execution has been verified; subsequent authorized owner review/run remains necessary.
