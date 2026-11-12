# M12 — fixed frozen-readout learning-rate contrast

## Authority and scope

Lead authorization `31ea7bc0`: one fresh original-P3 frozen-backbone run, not a
continuation of M8/M7. This source preparation does not launch or reserve ML.
Runtime owns the new fixed accepted profile and P13; no Runtime files or model
proof schemas change here. M6/M7/M8/M10 remain available unchanged; readout CLI
defaults to M8.

`configs/model/m12-qwen-head-lr.json` (`m12.recipe.v1`) differs from M8 only in
schema, head learning rate `2e-6 -> 2e-4`, and operational run budget
`2700 -> 590` seconds. It is a fixed profile, not a free-form recipe interface.

- Original P3: 494032768 parameters, frozen FP32, eval, no original gradients or
  optimizer/weight-decay members. Fresh independent bias-free FP32 W6 `[6,896]`
  cloned from the original ordered A–F rows; only its 5376 scalars are trained.
- Fresh base, W6, empty AdamW and RNG; seed 42. No learned M8/M7 weights or moments.
- One epoch, 1500 presentations, microbatch 1, accumulation 4, 375 updates.
  AdamW betas `.9/.999`, epsilon `1e-8`, decay `.01`, preclip norm capture and
  clip `1`, `foreach=False`. Four torch threads, FP32 MPS, stock SDPA,
  maximum input 1024, cache disabled.
- Exact historical M8/M6 materialized TRAIN schedule:
  `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`.
  No feature cache, capacity probe, extra epoch, selection, refit or extra forwards.
- START retains 1500 backbone forwards bound to M7 `fit-before` original-P3
  reference rows, **not M7 trained weights**. TRAIN has 1500 backbone forwards;
  FINAL has 1500, comparing W6 with the actual untied full-vocabulary export
  on the same hidden states. Existing `1e-4` logit / `1e-6` probability bounds,
  identical probability/logit top sets, vectors, and all 375 preclip norms remain.
- Original backbone/fixed-buffer, non-answer row, dtype, storage, exact export
  config and tokenizer proofs remain unchanged. Checkpoint manifest remains v2;
  readout proof shape is unchanged. Learned-head preservation, durable pre-step
  ATTEMPT and publication-last behavior are retained.

## Budget and historical metadata reuse

The external controller must enforce **aggregate Model <=590 seconds**, including
all audits and failed/plumbing attempts, leaving P13 <=310 seconds of the 900-second
chain. Each process requires a matching `m12.supervisor.v1` attestation with fresh
process, external enforcement, no automatic retry, remaining aggregate <=590 and
process maximum <=remaining. The source's process monitor cannot independently
account for prior processes: the controller owns the aggregate ledger and deadline.
RSS/driver guards are 16 GiB each and recommended headroom >=2 GiB.
`maximum_capacity_seconds: 600` is an inert compatibility field; there is no
readout capacity command or M12 capacity execution.

Reuse only actual successful M8 scope/memory/control metadata:
`artifacts/model/m8-qwen-readout-20261111-01/training/receipt.json`, SHA256
`06f742a2bf8c3e2d6a33c9dd64bb8f02744f271e24f13f7289f021bc674542fa`.
The M12 helper validates original assets, schedule, fresh-start record, full frozen
scope, START/FINAL completion and historical memory observations. Its explicit
allowed recipe differences are schema, LR and operational run budget. It does
**not** rewrite M12 to an M7 recipe or assert that M12 used LR `2e-6`, and does not
reuse the old full-parameter capacity projection as an M12 performance guarantee.
Historical M8 measured process runtime was about 245 seconds; this is not a new
measurement or an M12 guarantee.

Raw environment equality is deliberately unchanged. The future launch wrapper
must reproduce the actual M8 unset controls, not inject defaults for
`PYTORCH_ENABLE_MPS_FALLBACK`, `TORCH_DEVICE_BACKEND_AUTOLOAD`, `OMP_NUM_THREADS`,
`MKL_NUM_THREADS` or `VECLIB_MAXIMUM_THREADS`. Actual M8 recorded those as unset;
`TOKENIZERS_PARALLELISM=false`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`.
The controller/model explicitly sets torch threads to four. Do not weaken raw
control equality to accommodate a wrapper (the M10 first-load failure).

## CLI for the authorized controller only

Use the existing locked model environment; preparation does not install it.
Both commands require their own unique output directory and supervisor receipt:

```sh
python -B -m jeff.training.qwen_readout audit --experiment m12 \
  --output-dir <new-audit-directory> --supervisor-receipt <audit-supervisor.json>
python -B -m jeff.training.qwen_readout train --experiment m12 \
  --audit-dir <completed-audit-directory> --output-dir <new-training-directory> \
  --supervisor-receipt <train-supervisor.json> \
  --comparison-freeze-sha256 <controller-frozen-comparison-sha256> \
  --authorize-run M12-ONE-original-P3-frozen-six-row-lr2e-4-1500-375-seed42
```

Scientific executable/config pins and operating-context separation follow M8's
source-identity pattern. Audit/revalidation require clean committed source;
training consumes the pinned audited schedule without reshuffling/tokenizing it.

## Actual backbone accounting

Only `m12.train.v1` receipts (and their existing durable status snapshots) add:

```json
{"backbone_forwards":{"maximum":4500,"attempted":0,"completed":0,"by_phase":{"START":{"attempted":0,"completed":0},"TRAIN":{"attempted":0,"completed":0},"FINAL":{"attempted":0,"completed":0}}}}
```

The attempt increments immediately before the actual `model.model` call, after
input/mask construction; completion increments only after successful return and
MPS synchronization. A failed dispatch/synchronization retains an unmatched
attempt in the failure receipt. Each phase fails closed at 1500, subsequent phases
require all preceding phases complete, and successful FINAL requires 4500 total.
Counts are instrumentation only: no hook dispatch approximation, extra forward,
tensor scan or RNG operation. Handled failures preserve partial counts in normal
receipt/status failure publication. SIGKILL cannot promise a final receipt; the
existing durable update-boundary snapshots remain the last persisted state.
Old M8 receipts do not gain retroactive counts.

## Preparation verification boundary

Source review and `uv build --no-sources` only. No project/ML imports, tokenizer or
weight loading, native execution, model forwards, software tests, lint or new
dependencies are performed by this preparation. Runtime acceptance and actual
M12/P13 evidence remain with their authorized owners.
