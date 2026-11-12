# Model and training

- [M12 stronger frozen-backbone head-LR results](m12-head-lr-results.md).
- [M11 thirty-epoch results and evidence inventory](m11-msmarco-duration30-results.md).
- [M10 seed7 results and E11/E16 follow-through](m10-qwen-seed7-results.md).

## The first genuine loop

A ~22.7M-parameter pretrained BERT encoder, `sentence-transformers/all-MiniLM-L6-v2` at revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, supplies language representations. A new shared scalar head scores each candidate. AdamW updates both the pretrained backbone and head using cross-entropy over the supplied options.

This deliberately small provisional model proves training/save/reload before a larger architecture search. The base is Apache-2.0 and originally trained for sentence embeddings, **not** decision correctness. M3 adds a separately selectable retained-pretrained-head MS MARCO cross-encoder; see `msmarco-pilot-results.md` and `configs/model/msmarco-pilot-256.json`. Its native pooled-CLS/dropout/classifier path preserves the pretrained ranking head, uses raw scalar logits and external choice cross-entropy, and has its own self-contained checkpoint architecture. The existing mean-pool path and checkpoints remain supported and remain the CLI default.

## Latest contrast: stronger frozen-backbone head learning rate

M12 changes only M8 head LR2e-6→2e-4. TRAIN CE improves1.332200→1.135531 but agreement declines804→786/1500; first-slot choices reach936/1500. [E15](../evaluation/e15-head-learning-rate.md) finds new native/reversed121/113 versus M8's130/119, both-correct86→75 and four lost both-correct probe pairs despite lower aggregate proper scores. The separate two-forward reversal mean reaches132, no better than M8 mean and below P3 mean134. M12/P13 is complete at308.209917/900seconds; no rescue, capacity verdict or promotion. See [results](m12-head-lr-results.md) and [run index](m12-head-lr-run.json).

## Fit diagnostic: fresh thirty-epoch MS MARCO

M11's fresh original-base30-total-epoch endpoint improves M9 TRAIN agreement1314→1414/1500 and rules314→414/500, with130rule gains/30losses. But [E12](../evaluation/e12-encoder-duration30.md) finds new-development165→162/240 and worse NLL/Brier. D3 gains26→29/96 while both proper scores worsen. Three small mapped TRAIN mechanism sets are now completely fitted without strong new-policy transfer. M11/P10 is closed; no promotion, further duration arm or architecture-limit claim. See [results](m11-msmarco-duration30-results.md) and [run index](m11-msmarco-duration30-run.json).

### Prior twelve-epoch contrast

M9 first measured both preserved M4 encoders on full TRAIN, then activated the predeclared fresh-original-base12-epoch MS MARCO arm. TRAIN agreement improves985→1314/1500, CE.726023→.2890573; rules remain incomplete at314/500, including32lost prior agreements. P7 is closed and [E9](../evaluation/e9-encoder-duration.md) complete: new-development165/240 in both orders, but rule-fit gains do not establish rule transfer. No promotion or architectural-capacity inference. See [M9 results](m9-msmarco-duration-results.md) and [pinned run index](m9-msmarco-duration-run.json).

## Prior executed contrast: frozen-base Qwen readout

M8 completed one 1,500-presentation/375-update six-row-readout run: TRAIN teacher agreement 805 → 804 and CE 1.357724 → 1.332200. P6 strict fresh reload completed (627 forwards including 3 startup rows); [independent E8](../evaluation/e8-readout-scope.md) is complete and finds limited change (new130/119 versus P3's129/118), not default promotion or feature-incapacity evidence. See [M8 results](m8-qwen-readout-results.md) and [pinned run index / positional appendix](m8-qwen-readout-run.json). The [readiness note](m8-readout-readiness.md) is preserved as a historical assessment, preceding execution under the lead grant.

## Prior learning contrast: full-parameter Qwen

M7 reset to original P3 and changed only AdamW LR 2e-5 → 2e-6 on the exact M6 schedule. Its one completed run improved TRAIN agreement 805 → 1,130/1,500 and CE 1.357724 → 0.530299, but rule agreement fell 184 → 176/500 with 472 final rule selections at position 0. P5 completed the fresh-process 624-presentation reload/inference pass. Independent [E7](../evaluation/e7-low-lr-learning.md) is **mixed**: substantive intent/sentiment and broad proper-score gains against original P3, but new-rule both-order successes fall 4 → 0/80 and all 80 rule pairs flip. Probe both-correct stays 9/12 while losing two old rule successes. This is correlated, reused development evidence, not untouched-final generalization, calibrated confidence, a root-cause diagnosis or automatic promotion. See [M7 results](m7-qwen-low-lr-results.md), [frozen plan](m7-qwen-low-lr-plan.md), and [run index](m7-qwen-low-lr-run.json).

### Historical M6 contrast

M6 completed its one authorized1500-TRAIN/375-update run, but fixed-schedule TRAIN fit regressed:805→431agreements/1500, CE1.357724→1.390592, with every final recorded argmax at position0. Preserve the negative final checkpoint; no retry, default promotion or causal claim. Fresh starting624predictions are byte-identical to frozen P3. Runtime P4 completed independent final-checkpoint reload; E6 finds all624development choices strictly select input position0, with no both-order success. A small new-reversed NLL improvement does not offset the broad failure; full exceptions remain in the report. See [M6 results](m6-qwen-results.md), [frozen plan](m6-qwen-plan.md), and [run/evidence index](m6-qwen-run.json).

## Historical control: scalar-head learning rate

M5 changed only the retained MS MARCO classifier's learning rate, with byte-identical fresh starting predictions. It recovered one previously lost probe group without a new group error, but **failed the predeclared criterion because probe log loss worsened**. Pilot agreement stayed40/60; no default promotion or further training. See [M5 results](m5-head-lr-results.md), [plan](m5-head-lr-plan.md), and [run/provenance index](m5-head-lr-run.json).

## Seen-mechanism inference follow-through

D3's released 96 original cases /48 new policy-source groups /8 intentionally seen mechanisms now have predictions from all four preserved M4 snapshots. Inference only, unchanged cap256, no training or default change; Evaluation scores this separately from unseen-mechanism v2 evidence. See [D3 inference delivery](d3-inference.md) and [hashed run index](d3-inference-run.json).

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

Rows carrying `provenance.usage="validation_only_never_train"` are rejected from training shards even if both manifest and row splits have been relabeled to `train`. They remain eligible for validation-only use; removing the marker or making untracked derivatives is a procedural exclusion, not something this guard can recognize. This safeguard was added after M5; historical experiment sources and artifacts remain unchanged.

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
