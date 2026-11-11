# Linux CPU install sidecar for the existing P1 M2 bundle

Prepared target: **CPython 3.12, Linux x86_64, glibc >= 2.28** (not Alpine/musl,
ARM, or another Python ABI). Use the existing immutable `p1-m2-20261111-01`
bundle; this sidecar does not rebuild, modify, or supersede it. Do not use the
bundle's macOS/universal requirements file for this installation.

## Prepared installation (not executed)

On that Linux target, with Python 3.12 and uv already available, work outside
any checkout. Set absolute paths to the copied existing bundle, this separate
sidecar directory, and a **new** environment. Before installing, hash the actual
bundle manifest against a separately trusted P1 receipt, then hash the wheel
against that verified manifest; merely comparing sidecar text is insufficient.
Follow the pre-install steps in `docs/runtime/README.md`. Hashes are integrity
checks, not publisher authentication.

```sh
BUNDLE=/absolute/path/to/p1-m2-20261111-01
RECIPE=/absolute/path/to/linux-cpu
ENV=/absolute/path/to/new-venv
uv --no-config venv --python 3.12 --no-python-downloads "$ENV"
uv --no-config pip install --python "$ENV/bin/python" --link-mode copy \
  --no-index --only-binary :all: --require-hashes -r "$RECIPE/requirements.txt"
uv --no-config pip install --python "$ENV/bin/python" --no-index --no-deps \
  "$BUNDLE/package/jeff-0.1.0-py3-none-any.whl"
"$ENV/bin/python" -I -m jeff.runtime.verify "$BUNDLE"
```

The first install retains dependency checking: it does **not** use `--no-deps`.
All 25 packages use exact wheel URLs and SHA256 hashes, with no index search,
source builds, global extra index, or CUDA fallback. The second install uses
`--no-deps` only for the existing Jeff wheel (its base dependencies are empty);
do not request `jeff[model]` or run `uv sync`, which would reselect the root
Linux CUDA stack. Downloads require public network access; there is no bundled
wheelhouse or fully offline installation claim. Use a fresh environment, not
one with unrelated packages already installed.

## Prepared inference (not executed)

Use the existing inference implementation and copied bundle unchanged:

```sh
RUN=$(mktemp -d)
mkdir "$RUN/home" "$RUN/hf" "$RUN/xdg" "$RUN/torch" "$RUN/tmp"
env -i PATH="$ENV/bin:/usr/bin:/bin" HOME="$RUN/home" TMPDIR="$RUN/tmp" \
  HF_HOME="$RUN/hf" HF_HUB_CACHE="$RUN/hf/hub" XDG_CACHE_HOME="$RUN/xdg" \
  TORCH_HOME="$RUN/torch" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_IMPLICIT_TOKEN=1 \
  TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 \
  "$ENV/bin/python" -I -m jeff.model.predict \
  --checkpoint "$BUNDLE/checkpoint" --input "$BUNDLE/demo/inputs.jsonl" \
  --output "$RUN/predictions.jsonl" --device cpu --batch-size 1
```

Offline model flags prevent remote model fetching, not arbitrary networking.
Keep original checkout/cache paths inaccessible for a future isolation run.
Demo scores are not accuracy or calibration evidence. Existing bundle licensing,
privacy and redistribution limitations still apply; no publication authorized.

## Evidence and remaining gap

The official CPU index advertises the exact `torch==2.15.0+cpu` CPython 3.12
manylinux_2_28_x86_64 wheel and SHA256. Its PEP 658 metadata digest matches the
index advertisement. Its complete `Requires-Dist` list is in `provenance.json`:
there are no CUDA, NVIDIA or Triton requirements, even before marker filtering.
Required filelock, typing-extensions, setuptools, sympy, networkx, jinja2 and
fsspec dependencies are retained. Unrequested Torch extras are not installed.

Every non-Torch version, wheel URL and wheel hash comes from unchanged root
`uv.lock`. Public wheel metadata for each selected wheel was retrieved and its
Python requirement and applicable dependency version constraints checked for
this target with no extras. This is a metadata closure check, **not** an executed
uv cross-resolution, installation, binary compatibility check or model run.
Wheel contents/hashes have not been downloaded/independently verified; future
installation enforces the advertised/locked hashes. No exact-version
availability or metadata gap was observed.

Raw public index/metadata, retrieval timestamps, digests and applicable
requirements are recorded under
`artifacts/release/p2-linux-cpu-20261111-01/recipe-investigation/` in the root
artifact store. No weights or full wheels were retrieved. The host and Tart
sandbox are Darwin, with no available authorized Linux runtime. Therefore
**Linux installation and inference remain unverified**; P1's executed macOS
results are not Linux evidence. The next bounded step is installation and one
Model-approved isolated CPU invocation on an authorized Linux target, recording
versions, coverage and comparison with the saved P1 demo probabilities (any
cross-platform numerical differences must be disclosed). No new bundle is needed.
