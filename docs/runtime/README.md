# Portable local Jeff runtime

P1 exports the existing **M2** checkpoint without changing its weights, tokenizer, settings, loader or probabilities. The same exporter also handles **M3**, separately identified; neither packaging nor the demo selects a better model. No UI, model server or new framework is introduced.

## Deliverables

- `python -m jeff.runtime.export`: standard-library, allowlisted copy into a new read-only directory bundle. M2 has eight checkpoint files, M3 seven. Unexpected files, links, special files, overwrites and source changes during copying are rejected.
- `python -m jeff.runtime.verify BUNDLE`: exact inventory, size and SHA-256 verification, checkpoint/package metadata consistency, and manifest sidecar verification. No model imports.
- `scripts/release/prepare_support.py`: explicit local sidecars from a completed pinned M2/M3 run and checked-in runtime assets; no network/model loading.
- `scripts/release/cold_start.py`: macOS evidence harness invoking the **existing** `jeff.model.predict` CLI. Requires a prior explicit Model slot, an externally installed Python/environment, copied bundles and a UTC start deadline. It is not an inference implementation or a software test suite.
- [`BUNDLE-README.md`](BUNDLE-README.md): short macOS CPU install/run instructions included in each delivered bundle.
- [`p1-results.md`](p1-results.md): executed evidence, hashes, qualifications and failures. `manifests/releases/` stores the small inventory/runtime receipts; large bundles are ignored artifacts, never Git objects.

## Linux CPU follow-up (P2)

A separate [pinned Linux CPU recipe](../../configs/runtime/linux-cpu/README.md)
uses the existing M2 bundle without its CUDA-heavy universal requirements.
Target: CPython 3.12, Linux x86_64, glibc ≥2.28; official Torch 2.15.0+cpu,
all other package versions retained from the root lock. This is
**metadata-checked preparation, not executed Linux support**: no authorized
local Linux runtime was found. See [P2 status/evidence](p2-linux-cpu.md).
P1 bundles and macOS runtime evidence remain unchanged.

## Reproduce an export

Use Python 3.12. Run at a clean committed revision and record its actual full hash. The P1 wheel was built from `82c327a7ba6def23e77123f3e768b31255feb2b5`; the later delivery adds support/docs/evidence without changing that wheel's inference/runtime code.

```sh
uv build --no-sources
# Only needed when deliberately refreshing dependency pins from the owned root lock:
uv export --frozen --offline --no-cache --extra model --no-emit-project \
  --no-editable --format requirements.txt --no-header \
  --output-file /absolute/path/to/new-requirements.txt

# Use a new OUTPUT_PARENT and never overwrite a prior release.
mkdir -p "$OUTPUT_PARENT"
uv run --locked python scripts/release/prepare_support.py \
  --run-dir "$SOURCE_RUN" --output-dir "$OUTPUT_PARENT/support"
uv run --locked python -m jeff.runtime.export \
  --checkpoint "$SOURCE_RUN/checkpoint" \
  --wheel dist/jeff-0.1.0-py3-none-any.whl \
  --support-dir "$OUTPUT_PARENT/support" \
  --output-dir "$OUTPUT_PARENT/bundle" --bundle-id "$NEW_ID" \
  --code-revision "$(git rev-parse HEAD)"
uv run --locked python -m jeff.runtime.verify "$OUTPUT_PARENT/bundle"
```

`SOURCE_RUN` is the existing M2 `pilot-256-20261111-01` or M3 `msmarco-256-20261111-01` directory. Prepare-support currently supports exactly those pinned model identities; the exporter supports their present complete local layouts, not arbitrary future sharded checkpoints. Source runs must not be modified concurrently. The manifest records source runtime hashes, wheel metadata/hash, training revision/config, original model revision, dataset identity/hash, notices, demo and dependency requirements. Build from a trusted clean checkout; `--code-revision` is an operator assertion, not a signature or an independent Git verification.

The bundle is a directory, not an archive; ordinary copying preserves its bytes. Do not hard-link it or copy extra workspace/cache files. Export failure removes only its newly created output; an abrupt kill can leave an explicitly incomplete directory that will not verify. Read-only permissions protect against accidents, not deliberate owner changes. Filesystem durability against power loss and hostile concurrent writers is not promised.

## Verify before trusting/installing

The sidecar is not authentication. Obtain the expected manifest hash through an independently trusted receipt (for P1, the committed results below), hash **the actual manifest**, and then hash the wheel against that verified manifest **before installing or executing bundle code**. For example, from a trusted Python installation:

```sh
python3 - "$BUNDLE" "$EXPECTED_MANIFEST_SHA256" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
manifest_bytes = (root / 'manifest.json').read_bytes()
if hashlib.sha256(manifest_bytes).hexdigest() != sys.argv[2]:
    raise SystemExit('manifest hash mismatch')
manifest = json.loads(manifest_bytes)
wheel = manifest['package']['path']
path = pathlib.PurePosixPath(wheel)
if path.is_absolute() or '..' in path.parts or path.parts[0] != 'package':
    raise SystemExit('unsafe package path')
actual = hashlib.sha256((root / wheel).read_bytes()).hexdigest()
if actual != manifest['files'][wheel]['sha256']:
    raise SystemExit('wheel hash mismatch')
print('trusted receipt matches actual manifest and wheel')
PY
```

After installation, run the full inventory verifier in the bundled instructions. A trusted source checkout can also run the verifier before installation. This local tool is not a hardened hostile-file/TOCTOU security service.

## Scope and rights

Demonstrated only on macOS arm64 / Python 3.12 / CPU. Hash-pinned requirements preserve universal platform markers; do **not** treat this file as a Linux CPU installation recipe because its Linux branch includes CUDA packages. No dependency wheelhouse or Python installer is bundled. Installations can download packages; empty model caches and offline inference do not imply fully offline installation.

The Apache-2.0 text and pinned upstream cards are checked in under `configs/runtime/licenses/`; provenance identifies the source URLs. Neither upstream pinned repository supplied a LICENSE/NOTICE file. Our adjacent notice describes fine-tuned weights/generated configuration without changing source checkpoint bytes. Jeff code/new head licensing and synthetic-data provider/account rights are not cleared for redistribution, and dependency-license auditing is not complete. No upload/publication is authorized.

Existing checkpoint provenance contains local project paths and a save-time `running` snapshot; the separately hashed completed run receipt explains both. No training rows, credentials, author cache, protected final data or workspace dump is included. Historical paths remain inert metadata, demonstrated inaccessible during inference. Preserve bytes and disclose this local-only privacy limitation; external distribution needs an owner-approved privacy/licensing resolution.
