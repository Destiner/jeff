# Model and training

## The first genuine loop

A ~22.7M-parameter pretrained BERT encoder, `sentence-transformers/all-MiniLM-L6-v2` at revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, supplies language representations. A new shared scalar head scores each candidate. AdamW updates both the pretrained backbone and head using cross-entropy over the supplied options.

This deliberately small provisional model proves training/save/reload before a larger architecture search. The base is Apache-2.0 and originally trained for sentence embeddings, **not** decision correctness. M3 adds a separately selectable retained-pretrained-head MS MARCO cross-encoder; see `msmarco-pilot-results.md` and `configs/model/msmarco-pilot-256.json`. Its native pooled-CLS/dropout/classifier path preserves the pretrained ranking head, uses raw scalar logits and external choice cross-entropy, and has its own self-contained checkpoint architecture. The existing mean-pool path and checkpoints remain supported and remain the CLI default.

## Latest control: scalar-head learning rate

M5 changed only the retained MS MARCO classifier's learning rate, with byte-identical fresh starting predictions. It recovered one previously lost probe group without a new group error, but **failed the predeclared criterion because probe log loss worsened**. Pilot agreement stayed40/60; no default promotion or further training. See [M5 results](m5-head-lr-results.md), [plan](m5-head-lr-plan.md), and [run/provenance index](m5-head-lr-run.json).

## Frozen-v2 comparison

M4 completed one fresh-pretrained v2 run per supported architecture under matched controls, with saved baselines/checkpoints and fresh offline inference. Both improve on newly authored validation versus their own starts, but **neither passes the predeclared inherited/probe robustness gate**. Preserve M2/M3 and the new candidates; no default promotion. See [M4 results](m4-v2-results.md), [frozen plan](m4-v2-plan.md), and [run/provenance index](m4-v2-run.json).

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

- `baseline/`: all-MiniLM has a pretrained encoder plus an explicitly **random-initialized scoring head**, a weak baseline; MS MARCO instead retains its pretrained ranking head.
- `checkpoint/`: trained encoder and head. Both checkpoint directories include safetensors, tokenizer files, exact original base revision, formatting, truncation, and probability settings.
- `dataset-manifest.json`: frozen manifest; shards remain separately referenced by verified hashes.
- `run.json`: arguments, seed, dataset identity, code revision/dirty flag and source hashes, environment/device, optimizer configuration, train losses, validation agreement/log loss, before/after parameter hashes and representative L2 changes, elapsed time, memory and spend.
- `failure.json` for an unsuccessful run when the output directory could be reserved.

Reload uses local files only and rejects pickle fallback and custom remote code. A checkpoint is self-contained for inference, **not optimizer-resumable**. Software dependencies still require the shared Python environment.

First executed evidence: `docs/model/tiny-run.json` and `first-results.md`. Tiny data establishes plumbing only; validation degraded. The subsequent 300-train/60-validation pilot improved aggregate reference-label agreement from 19/60 to 36/60, but rule performance fell and a truncation audit found lost question tokens in rule-validation inputs. See `pilot-results.md` and `pilot-run.json` for the qualified comparison. Lead-authorized LD002 repeated the same setup at 256 tokens: input loss disappeared, but trained agreement was 35/60 and rules remained weak; see `pilot-256-results.md` and `pilot-256-run.json` for the matching-baseline comparison. Both runs have fresh offline-process predictions; the tiny run records a dirty checkout, while the pilot executed clean committed code.

Memory records distinguish CPU lifetime high-water RSS from point-in-time MPS allocator/driver usage, which is not a GPU peak. All runs were local with £0 additional spend. No software tests or linters are part of this project; verification is package building and actual training/inference/evaluation.
