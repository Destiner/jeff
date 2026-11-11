# P2 — Linux CPU installation preparation, execution unavailable

**Outcome:** a separate pinned CPU recipe for the existing P1 M2 bundle is prepared and metadata-checked. **Linux installation, binary compatibility and inference are unexecuted/unverified.** This is the explicitly permitted fallback, not a claim of Linux runtime support. P1 remains unchanged and was not replayed; no new model bundle was produced.

## Resume and local-runtime finding

On 2026-11-11 the same Release owner resumed its clean `worker/release` worktree, fast-forwarding `209e713` to committed main `5e782fb` without reset or history rewrite. Read the current mailbox protocol and lead message `d66a1c69-5672-44e9-bd4e-39270fe4df4d`, explicitly acknowledged it, and reported that P2 had not previously started. Existing P1 artifacts were adopted, not regenerated.

Read-only discovery at 13:07:47 UTC found:

- Host: macOS 26.7.1 arm64, not Linux.
- No `docker`, `podman`, `colima`, `limactl`, Apple `container`, `nerdctl`, `qemu-system-aarch64` or `qemu-system-x86_64` executable on PATH.
- No Docker, OrbStack or UTM application in the conventional `/Applications` locations.
- Tart exists; `tart list` showed local `sandbox` and a cached macOS Tahoe image. `tart get sandbox --format json` explicitly reports `OS: darwin` (already running), not Linux.

This records the inspected local paths/tools, not an exhaustive search of arbitrary files or a claim about remote hosts. No guest login, remote-machine access, guest/daemon start, engine/VM installation or infrastructure change was made. There is **no available authorized Linux runtime for this bounded mission**. We did not seek an ML slot or compete with Model M5 for a run that cannot execute.

Raw commands/results and inspection scope: `artifacts/release/p2-linux-cpu-20261111-01/local-runtime-availability.json` in the root artifact store.

## Prepared recipe and why it avoids CUDA

Files: [`configs/runtime/linux-cpu/`](../../configs/runtime/linux-cpu/README.md).

| Item | Pin / scope |
| --- | --- |
| Target | CPython 3.12, Linux **x86_64**, glibc ≥2.28 |
| Torch | **2.15.0+cpu**, official CPU-index wheel, `cp312-cp312-manylinux_2_28_x86_64` |
| Transformers | 4.57.6, unchanged from project lock |
| Safetensors | 0.8.0, unchanged from project lock |
| Complete closure | 25 exact wheel URLs with SHA-256 hashes; no extras |
| Root inputs | `pyproject.toml` and `uv.lock` unchanged |

The official CPU index provides a distinct Torch build variant, not a silent downgrade of the project's 2.15.0 stack. Its advertised PEP 658 metadata hash matched the retrieved metadata. Complete `Requires-Dist` contains filelock, typing-extensions, setuptools, sympy, networkx, jinja2, fsspec and optional extras; **no CUDA, NVIDIA or Triton requirement**. Every mandatory dependency is retained. Other selected versions, wheel URLs and hashes come from the existing root lock, with target-compatible wheel tags. Their public wheel metadata's `Requires-Python` and applicable dependency constraints were checked against the selected versions for Linux x86_64 / Python 3.12 / no extras.

The install command uses explicit URLs, `--no-index`, binary-only and hash enforcement, while **retaining dependency resolution/checking**. It does not rely on `CUDA_VISIBLE_DEVICES`, trim CUDA dependencies from a CUDA wheel, add a global extra index, or silently fall back to the generic root Torch package. The separate Jeff wheel install alone uses `--no-deps`. Do not substitute `uv sync` or the P1 bundle's universal requirements, whose Linux branch still selects CUDA packages.

This is metadata closure inspection, **not** an executed cross-platform resolver, package installation, native-library load or inference run. Full wheels were not downloaded; advertised/locked wheel hashes have not been independently checked against wheel bytes. Installation must enforce them later. No exact-version metadata/availability gap was observed. ARM, musl/Alpine, other Python ABIs and platform matrices were deliberately not added.

## Artifacts and integrity

Root artifact directory:

`/Users/destiner/Code/jeff/artifacts/release/p2-linux-cpu-20261111-01/`

- `linux-cpu-support/{README.md,requirements.txt,provenance.json}` — small separate support snapshot, no checkpoint or new bundle.
- `recipe-investigation/` — official CPU index, 25 retrieved wheel metadata files, URLs/timestamps/content digests, applicable requirements, preparation driver and package build log.
- `local-runtime-availability.json` — concrete execution gap above.
- `preparation-receipt.json` — support/evidence inventory and explicit zero install/inference counts; committed copy at `manifests/releases/p2-linux-cpu-20261111-01.json`.

Requirements SHA-256: `f2df19722404e0750e5e3b1a18b95fb5f5c96131e1d54b0951c4de5ce2778eb6`.

Torch CPU wheel URL and SHA-256 are in `configs/runtime/linux-cpu/provenance.json`; all package URLs/hashes are in its requirements file. The index selects `download-r2.pytorch.org` as the wheel host; this is the link supplied by the official `download.pytorch.org/whl/cpu/torch/` page, not a new unofficial index.

Existing M2 bundle remains at `artifacts/release/p1-20261111-01/m2-bundle/`, with trusted manifest SHA-256 `1c1fc4bc742beb7ec396e5b6b51550df216d38a097b467b9ce3fe0aa4f190e59`. The sidecar README contains prepared install/inference commands using its original wheel, demo and existing CLI. Before installation, hash the actual bundle manifest and wheel against the trusted P1 receipt; a matching sidecar string alone is insufficient.

## What was and was not executed

Executed: read-only runtime discovery; public index/metadata retrieval; dependency metadata analysis; package builds; focused review and owned integration. No software tests or linting.

Not executed: Linux package installation, Linux interpreter/model load, inference, source/bundle probability comparison, or measured Linux latency/memory. Therefore there are **zero new predictions**, no Linux coverage figure, and no Linux install/runtime performance result. P1's macOS evidence is not borrowed as Linux evidence.

A future actual run needs an authorized Linux x86_64/glibc target with Python 3.12/uv, only the existing bundle and sidecar staged, original checkout/cache unavailable, empty model caches, remote model fetching disabled and a Model-approved slot. Installation may download wheels; no fully offline installation or wheelhouse is claimed. Compare its outputs with saved P1 demo probabilities while exposing cross-platform numerical differences. Do not install new infrastructure or use a remote host under this completed assignment's authority.

No model/default promotion, training, root dependency/checkpoint change, final-evaluation access, upload or licensing decision. Existing Jeff/provider redistribution and checkpoint-provenance privacy limitations remain unresolved. No model resource reserved/used, no paid allocation consumed: **£0 actual / £0 pending**. The bounded preparation is complete; the precise execution gap is recorded rather than hidden behind a successful package build.
