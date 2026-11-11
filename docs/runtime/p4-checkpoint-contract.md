# P4 additive trained-checkpoint binding

Runtime implements Model's flat `c6ba7f97` contract, as confirmed in
`artifacts/handoffs/release/20261111T1533-P4-schema-convergence.md`. The concurrent
nested-training proposal is not used. No new loader or scoring recipe is added.

## Layout and manifest

Publish the complete HF directory and a **sibling**, not contained,
`checkpoint-manifest.json`. The CLI also accepts an explicit alternate sibling
filename. Freeze the source-run receipt before hashing it into the manifest.

Required manifest fields:

| Field | Constraint |
| --- | --- |
| `schema_version` | `jeff.qwen-trained-checkpoint.v1` |
| `status`, `kind` | `complete`, `trained` |
| `checkpoint_id`, `run_id` | Nonempty strings; producer assigns unique identities |
| `base_model_id` | `Qwen/Qwen2.5-0.5B-Instruct` |
| `base_revision` | `7ae557604adf67be50417f59c2c2f167def9a775` |
| `training_code_revision` | 40 hexadecimal characters |
| `training_data_manifest_sha256`, `training_recipe_sha256`, `training_schedule_sha256` | Each 64 hexadecimal characters |
| `p3_scoring_config_sha256` | `2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f`, also matching the actual runtime config bytes |
| `tokenizer_assets` | Exactly the four original filename/hash entries below |
| `files` | Every local HF filename mapped to exactly `{ "sha256": "…", "bytes": 0 }`; actual nonnegative integer sizes and SHA-256 hashes must match |
| `source_run_receipt` | Object with nonempty `path` and SHA-256 `sha256` |

Additional provenance fields are allowed and frozen by the whole manifest hash.
No mandatory `training` object, completed-update counter, or receipt-internal
schema is imposed. Hash hex is accepted case-insensitively except the exact
pinned scoring/tokenizer fields, which use the lowercase literals shown.

The directory must contain `model.safetensors`, `config.json`,
`generation_config.json`, and all four tokenizer files. Optional files are
`README.md` and `LICENSE`. No other files, symlinks, special files,
subdirectories, or caches are accepted. Inventory names must be flat and safe.
The existing asset validator still checks `qwen2` / `Qwen2ForCausalLM` architecture.

Original P3 tokenizer byte pins:

```text
merges.txt             599bab54075088774b1733fde865d5bd747cbcc7a547c5bc12610e874e26f5e3
tokenizer.json         c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539
tokenizer_config.json  5b5d4f65d0acd3b2d56a35b56d374a36cbc1c8fa5cf3b3febbbfabf22f359583
vocab.json             ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910
```

The source receipt may be absolute or relative to the manifest's parent. Runtime
hashes the exact existing file; it does not parse its contents. Existing
`safe_path` final/reference restrictions apply to resolved model, manifest, and
receipt paths. Runtime never follows training-data/recipe/schedule provenance
paths or opens training datasets or reference rows.

Model is responsible for completing 375 updates and final before/after TRAIN-fit
measurement before publishing `status: complete`. Runtime verifies identity,
not training labels, optimizer progress, training quality, or proof of learning.
IDs are checked for nonemptiness, not uniqueness across a global registry.
Base revision records **lineage**: trained tensor bytes are identified by their
own inventory hashes, not described as original upstream revision bytes.

## CLI and frozen evidence

From the repository root, when the trained checkpoint and authorized ML slot
are ready:

```sh
uv run --locked --extra model python -m jeff.runtime.qwen_challenger audit \
  --config configs/runtime/p3-qwen.json \
  --inputs /absolute/development-inputs.json \
  --model-dir /absolute/run/hf \
  --checkpoint-manifest /absolute/run/checkpoint-manifest.json \
  --audit-dir /absolute/new-trained-audit

uv run --locked --extra model python -m jeff.runtime.qwen_challenger predict \
  --audit-dir /absolute/new-trained-audit \
  --model-dir /absolute/run/hf \
  --output-dir /absolute/new-trained-predictions --device mps
```

`evidence(config_path, manifest_path, model_dir, checkpoint_manifest=None)` retains
its existing three positional arguments and adds one optional argument. Without
it, `trained_checkpoint` is **omitted**, not null; previous evidence fields and
P3 behavior remain. The adapter source digest continues to hash its current
source, so audits from an older adapter revision still require a fresh audit.

With it, audit evidence (and prediction receipt evidence) additionally contains:

```text
trained_checkpoint:
  manifest_path: resolved absolute path
  manifest_sha256: SHA-256 of exact manifest bytes
  manifest: complete parsed manifest, including optional provenance
  source_run_receipt:
    path: resolved absolute receipt path
    sha256: SHA-256 of exact receipt bytes
  validator_source_sha256: SHA-256 of qwen_checkpoint.py
```

Prediction has no manifest override flag. It retrieves the path from frozen
training binding, reruns the validator through `evidence`, and performs the
existing exact `current == frozen` comparison before loading weights. Manifest,
receipt, validator source, assets, and existing environment/config/input/code
bindings must therefore remain unchanged. Keep published artifacts immutable;
this is local hash binding, not authentication or protection against concurrent
filesystem mutation between validation and loading.

## Verification boundary

This implementation was source-reviewed and packaged with `uv build --no-sources`.
The trained checkpoint was not ready during implementation. No fabricated
checkpoint/fixture, software test, lint, tokenizer audit, model load, inference,
training, or extra original-weight scan was executed. Actual trained manifest
acceptance, fresh-process reload, 624-presentation development coverage, resource
measurements, and evaluation remain pending Model publication and scheduling.
