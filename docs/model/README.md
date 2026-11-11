# Model and training

## The first genuine loop

A ~22.7M-parameter pretrained BERT encoder, `sentence-transformers/all-MiniLM-L6-v2` at revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, supplies language representations. A new shared scalar head scores each candidate. AdamW updates both the pretrained backbone and head using cross-entropy over the supplied options.

This deliberately small provisional model proves training/save/reload before a larger architecture search. The base is Apache-2.0 and originally trained for sentence embeddings, **not** decision correctness. Research recommends later comparing a pretrained MS MARCO relevance head; the first loop does not claim that stronger baseline.

## Formatting and probabilities

For each candidate, encode this text pair:

```text
State:
{state}
Question:
{question}
```

```text
Candidate:
{option text}
```

Use tokenizer special tokens, batch padding, and `longest_first` truncation to 128 total tokens in the pilot (configurable up to the backbone position limit). Attention-mask mean pooling feeds the scalar head; there is no sentence-embedding L2 normalization. A softmax across candidate logits gives probabilities, with temperature 1.0 and no calibration claim. Padded candidate slots receive negative infinity.

IDs, target labels, and all metadata are excluded from text. Option IDs only map output probabilities back to the caller. Candidate scoring is shared and independent of option order; ties are resolved by the evaluator in input order. Any number of options >=2 is supported, subject to available memory. Longest-first truncation can discard state, question, or candidate details; this is a known limitation, not instruction-hierarchy enforcement.

## Setup and commands

From the integrated package or this worktree:

```sh
uv sync --locked --extra model
uv build --no-sources
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
export HF_HOME="$JEFF_ARTIFACTS_DIR/model/hf-cache-20261111"
export TOKENIZERS_PARALLELISM=false
```

Use a **new** run directory on every execution. The reference settings are in `configs/model/minilm-pilot.json`; it documents CLI flags and is not automatically loaded.

```sh
uv run --locked --extra model python -m jeff.training.train \
  --dataset-manifest "$JEFF_ARTIFACTS_DIR/data/data-tiny-v1/manifest.json" \
  --output-dir "$JEFF_ARTIFACTS_DIR/model/YOUR-UNIQUE-RUN" \
  --revision 1110a243fdf4706b3f48f1d95db1a4f5529b4d41 \
  --device mps --epochs 3 --batch-size 4 --max-length 128 \
  --learning-rate 2e-5 --head-learning-rate 5e-4 --seed 42 --threads 4
```

Use `--device cpu` without Apple MPS. `auto` chooses MPS when available, CPU otherwise. Explicit MPS requests fail if unavailable, rather than silently switching.

Inference must receive decision-only JSONL, exported by Evaluation. Run baseline and trained checkpoints on the **same** inputs in separate processes:

```sh
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
uv run --locked --extra model python -m jeff.model.predict \
  --checkpoint "$JEFF_ARTIFACTS_DIR/model/YOUR-UNIQUE-RUN/checkpoint" \
  --input /absolute/path/to/inputs.jsonl \
  --output /absolute/path/to/new-predictions.jsonl --device mps
```

Repeat with `baseline` and a different output path. Output parents must already exist; existing prediction files are never overwritten. Invalid/duplicate inputs or nonfinite probabilities fail the entire invocation, with no success-looking partial output.

## Dataset and isolation safeguards

The trainer independently verifies manifest/shard hashes and row counts, decision fields, target membership, allowed task families, provenance fields, global ID uniqueness, and group isolation. It reports exact content duplicates. It rejects final shards in a whole-manifest preflight, refuses paths into protected `evaluation/final`, and rejects artifact-root traversal. Validation labels are used only for before/after metrics; only train rows reach optimizer updates.

These checks do not prove semantic label correctness or catch every paraphrase leak. Data owns broader validation. Final evaluation remains outside this workstream.

## Saved artifacts and evidence

Each immutable run contains:

- `baseline/`: pretrained encoder plus **random initialized scoring head**, explicitly a weak baseline.
- `checkpoint/`: trained encoder and head. Both checkpoint directories include safetensors, tokenizer files, exact original base revision, formatting, truncation, and probability settings.
- `dataset-manifest.json`: frozen manifest; shards remain separately referenced by verified hashes.
- `run.json`: arguments, seed, dataset identity, code revision/dirty flag and source hashes, environment/device, optimizer configuration, train losses, validation agreement/log loss, before/after parameter hashes and representative L2 changes, elapsed time, memory and spend.
- `failure.json` for an unsuccessful run when the output directory could be reserved.

Reload uses local files only and rejects pickle fallback and custom remote code. A checkpoint is self-contained for inference, **not optimizer-resumable**. Software dependencies still require the shared Python environment.

First executed evidence: `docs/model/tiny-run.json`. Tiny data establishes plumbing only; validation degraded, so it is not evidence of generalization. Both baseline/trained predictions were produced in fresh offline processes with a separate empty Hugging Face cache. Run records honestly mark this initial implementation checkout dirty.

Memory records distinguish CPU lifetime high-water RSS from point-in-time MPS allocator/driver usage, which is not a GPU peak. All runs were local with £0 additional spend. No software tests or linters are part of this project; verification is package building and actual training/inference/evaluation.
