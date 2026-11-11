# Bounded research experiments

## Token-budget data audit (CPU only)

`audit_token_budget.py` audits published **train/validation** rows against the active pilot's text-pair format, without loading a model or importing torch. This is dataset validation, not a software test suite. It rejects final shards, verifies published shard hashes/counts/splits, and reports actual combined token lengths plus question/candidate tokens lost to right `longest_first` truncation. It does not change datasets or production code. Existing outputs are never overwritten.

Requirements: Python >=3.10 and `tokenizers`. No root dependency addition is requested: the approved Model environment already contains `tokenizers` through Transformers. The completed invocation below used that environment read-only, with bytecode writing disabled. Do not install packages into another worker's environment.

### Executed invocation

From `/Users/destiner/Code/jeff/.worktrees/research`:

```bash
/Users/destiner/Code/jeff/artifacts/model/env-20261111/bin/python -B \
  experiments/research/audit_token_budget.py \
  --manifest /Users/destiner/Code/jeff/artifacts/data/data-tiny-v1/manifest.json \
  --artifacts-dir /Users/destiner/Code/jeff/artifacts \
  --tokenizer /Users/destiner/Code/jeff/artifacts/research/tokenizer-audit-20261111T1029/tokenizer.json \
  --tokenizer-source https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/tokenizer.json \
  --max-length 128 256 512 \
  --output /Users/destiner/Code/jeff/artifacts/research/tokenizer-audit-20261111T1029/tiny-token-budget.json
```

The tokenizer JSON was fetched from that exact public URL using the fetch tool, then saved under the unique research artifact directory. Only 462,948 characters of tokenizer metadata were fetched: **no model weights**. Script and tokenizer SHA256 values, runtime tokenizer version, dataset identity/hash and sample counts are in the report.

Observed: `tokenizers==0.22.2`; 9 rows / 25 candidate pairs; full lengths min 36, p50 40, p95 59, max 59. None exceeded 128, 256 or 512; no question/candidate loss. This establishes nothing about model quality or longer data.

### Full pilot: executed after publication

The same script/executable/tokenizer command was successfully executed with:

```text
--manifest /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/manifest.json
--output /Users/destiner/Code/jeff/artifacts/research/tokenizer-audit-20261111T1029/pilot-token-budget.json
```

All remaining arguments were identical to the tiny invocation above. Observed on 300 train + 60 validation decisions / 1,412 pairs: full length min 41, p50 62, p95 114, max 169. At 128, **45 pairs lose question tokens across 12 rule-validation decisions**; none lose candidate text. No train pairs overflow. At 256 and 512, zero loss/overflow. Use the existing Model CLI `--max-length 256` for the untouched pilot baseline and training. This is a measured token-budget failure, not a measured accuracy effect.

Future dataset versions need their own immutable output path and the exact Model tokenizer revision. No ML slot is needed for this CPU data operation. Do not inspect `evaluation/final` or use final labels for this workstream.

## Saved-prediction validation analysis (CPU only)

`inspect_validation_delta.py` performs standard-library arithmetic on already-produced prediction files. It requires exact full ID/option coverage and validation-only labels, reports per-case target probability, top-two margin and log-loss change, and refuses final data. It is a diagnostic, not a replacement for Evaluation's report schema. It neither runs inference nor trains a model.

Executed from the same research worktree:

```bash
python3 -B experiments/research/inspect_validation_delta.py \
  --examples /Users/destiner/Code/jeff/artifacts/data/data-tiny-v1/validation.jsonl \
  --baseline /Users/destiner/Code/jeff/artifacts/model/tiny-20261111-01/baseline-predictions.jsonl \
  --trained /Users/destiner/Code/jeff/artifacts/model/tiny-20261111-01/trained-predictions.jsonl \
  --output /Users/destiner/Code/jeff/artifacts/research/validation-delta-20261111T1034/tiny-validation-delta.json
```

Observed on three teacher-labeled validation cases: full coverage; target agreement 1/3 → 0/3; mean log loss 1.096827785789081 → 1.1035198087248328. The only top-choice flip is an intent example, with an after-training winning margin of 0.0002539158. All distributions remain near uniform. See [the follow-up analysis](../../docs/research/follow-up.md) for the interpretation and limits.

## Packaging execution

```bash
uv build --no-sources \
  --out-dir /Users/destiner/Code/jeff/artifacts/research/build-20261111T1034
```

Succeeded: `jeff-0.1.0.tar.gz` and `jeff-0.1.0-py3-none-any.whl`. This builds the inherited shared package scaffold, not another worker's unmerged model implementation. It does not prove model execution. No software tests or linting were run.

## Owner-run experiments (not launched by Research)

1. **Encoder first loop:** untouched vs trained predictions on the same validation inputs; record backend/dtype, memory (including whether point-in-time or peak), time, truncation, coverage, per-family label agreement and log loss; save/reload in a new process.
2. **One controlled format fix if real overflow appears:** preserve question and choice tokens, cap only state, keep the same data/seed/training budget. Save the format/truncation revision with the checkpoint. A rule removed from state still changes the task: report overflow rather than calling it harmless.
3. **Decoder only if needed:** one frozen-base rank-8 q/v LoRA run on the same training/validation data, with allowed-symbol choice scoring. Project only the actual answer position when supported by the installed Qwen API; verify symbol tokenization and record logits shape/memory during the real step. No generation/JSON parser or quantization stack is needed to start.

The experiments remain with Model, which owns compute. Temperature fitting, new families, paid generation, and final-evaluation access are not authorized by this note.
