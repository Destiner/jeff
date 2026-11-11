# Jeff local inference bundle

A byte-preserving export of a trained Jeff checkpoint, not a newly selected best model. See `manifest.json` for candidate identity, hashes, package/version and provenance. Three synthetic demo decisions are runtime examples, not accuracy evidence. Outputs are normalized scores, not calibrated confidence.

## Install (network may be needed)

Executed target: Apple silicon macOS, Python 3.12. The pinned Torch macOS wheel requires macOS 14+. Python/uv and dependency wheels are not included. This is **not fully offline installation**. The requirements file is a universal uv-lock export retaining platform markers; this recipe is scoped to macOS arm64. Do not use it as a Linux CPU recipe: Linux markers select CUDA dependencies.

From outside any source checkout, set absolute paths:

```sh
BUNDLE=/absolute/path/to/copied-bundle
ENV=/absolute/path/to/new-venv
uv venv --python 3.12 "$ENV"
uv pip install --python "$ENV/bin/python" --link-mode copy --only-binary :all: \
  --require-hashes -r "$BUNDLE/requirements-macos-arm64-py312.txt"
uv pip install --python "$ENV/bin/python" --no-deps \
  "$BUNDLE/package/jeff-0.1.0-py3-none-any.whl"
"$ENV/bin/python" -I -m jeff.runtime.verify "$BUNDLE"
```

Compare `manifest.sha256` with a separately trusted release receipt before installing the wheel; verification detects corruption, not a maliciously replaced manifest/wheel. Keep the immutable bundle read-only. Put caches and outputs elsewhere.

## Run (no remote model fetch)

```sh
RUN=$(mktemp -d)
mkdir "$RUN/home" "$RUN/hf" "$RUN/xdg" "$RUN/torch" "$RUN/tmp"
env -i PATH="$ENV/bin:/usr/bin:/bin" HOME="$RUN/home" TMPDIR="$RUN/tmp" \
  HF_HOME="$RUN/hf" HF_HUB_CACHE="$RUN/hf/hub" XDG_CACHE_HOME="$RUN/xdg" \
  TORCH_HOME="$RUN/torch" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  HF_HUB_DISABLE_TELEMETRY=1 HF_HUB_DISABLE_IMPLICIT_TOKEN=1 \
  TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 \
  VECLIB_MAXIMUM_THREADS=2 \
  "$ENV/bin/python" -I -m jeff.model.predict \
  --checkpoint "$BUNDLE/checkpoint" --input "$BUNDLE/demo/inputs.jsonl" \
  --output "$RUN/predictions.jsonl" --device cpu --batch-size 1
```

The existing loader requires local safetensors/tokenizer files and disables remote custom code. `--device cpu` avoids automatic MPS selection. Missing required weights must fail, not download. These flags disable remote model fetching, not arbitrary networking; the separately documented P1 execution additionally denied all network and original-home reads using macOS sandbox-exec. No server or second inference implementation is included.

## Contents, rights and limitations

- `checkpoint/`: original file bytes; M2 has a separate scalar head, M3 retains its head in encoder weights. Max input 256 tokens; longest-first truncation can lose information. No model default changed; M3's pilot gain coexists with a probe regression.
- `package/`: Jeff wheel, not an editable checkout; dependency pins/hashes accompany it. Other platforms and accelerators are unverified here.
- `licenses/`: Apache-2.0 text, pinned upstream card, and Jeff modification/rights notice. Upstream model licensing is distinct from project code and data/provider rights. No Jeff project license grant or external redistribution clearance has been established. Local use only under this assignment; no publication authorized.
- `provenance.json`: completed-run receipt and training identity; no training rows. Original checkpoint metadata retains historical absolute project paths and a save-time `running` status snapshot. Paths are inert provenance, not runtime dependencies; the source run completed. Bytes are deliberately unchanged. Do not publish these local bundles without privacy and licensing review.
- Exported permissions (0444 files, 0555 directories) deter accidental writes but are reversible, not WORM storage. Never overwrite an existing bundle; give every new export a new ID. Copy the directory using normal file copying, not hard links. No archive extraction is needed.
