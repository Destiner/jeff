# B2 trained M10 browser export

## Native result

The actual M10 seed7 endpoint was exported successfully to a single FP16 ONNX
six-logit decision scorer. This is not pretrained Qwen, M7, or the frozen-base
M8/M12 head-only model. All 494,032,768 trained backbone/embedding parameters
remain represented; the projection copies the actual trained A–F head rows.
The native tied embedding/head were the same parameter and storage before and
after precision conversion. Four strict loading diagnostics were empty.

| Recorded item | Result |
| --- | --- |
| Execution source | `c99cc5d480017896d4a8302ac66e5ee3e84d9fbd`, clean |
| Exporter SHA256 | `c43249ee0ceff07ce19aaf1b869c54acda70f3ee48f0db8342aee25b297ff860` |
| Native interval | 2026-11-12 12:16:43.868888–12:17:02.366230 UTC |
| External parent duration | 18.53 s; conservative charge 20/1200 s |
| Execution | CPU, four intra-op/inter-op threads |
| Native reference | Three FP32/SDPA calls; frozen before conversion |
| Export trace | One FP16/eager backbone call on the first same input |
| Outputs | Three cases, eleven native probabilities; prompt lengths 93/142/154 |
| Answer token IDs | A–F = 32–37, actual suffix-boundary checks |
| Graph | 989,080,308 bytes; IR8, opset17, 291 initializers, no external data |
| Graph SHA256 | `501bc4abe0c7ee66a885508992c61b4e75663a3d2776bf35942b7a1e498bbacd` |
| Lifetime RSS | 4,078,387,200 bytes |
| Maximum sampled process-group RSS | 3,996,909,568 bytes |
| Parent/child result | Exit0, complete receipt, PID/group47514 absent |
| Additional actual/pending spend | £0/£0 |

RSS scopes are nonadditive, not a continuous system-wide memory measurement.
The supervising parent sampled group RSS and enforced12GiB/300s; the child
also checked lifetime RSS and its deadline. The global/user browser state is
unknown. This closure concerns agent-owned task processes, not unrelated user
sessions. No original native checkpoint, tokenizer or historical environment
was modified. A new isolated exporter environment and exact package freeze are
retained.

## Contract and evidence

One int64 `input_ids` tensor `[1,L]` supplies an unpadded full prompt; positions
and additive causal mask are internal. The graph returns float32 `logits` for
A–F. Its ONNX batch output dimension is symbolically named
`Castlogits_dim_0`; execution is restricted to batch1 and the browser must check
the actual `[1,6]` result. Slice to the original K options **before** stable T1
softmax. FP16 rounding and SDPA→eager lowering require actual browser parity;
casting outputs to FP32 does not restore discarded precision. RoPE frequencies,
normalization variance and attention softmax retain their source FP32 islands.

All artifact paths below are relative to repository root:

- `artifacts/model/browser-b2-20261112-01/export01/receipt.json`:
  source/checkpoint assets, counters, load/tie metadata, actual graph schema/operators.
- `export01/native-references.json` under that root: frozen complete FP32
  reference, SHA256 `a0cf43e9143981839b6ddb664548dcff72eab2ad77c556f519a03dc87ce66fc4`.
- `export01/export-contract.json`: SHA256
  `f7577e3143814f03a534262e41c5c1598ccdb1d3e9ca69721f8cccfdc8c75ad9`.
- `export01/model.onnx` and `export01/assets/`: graph and exact original small
  tokenizer/config/license assets; do not serve a partial attempt.
- `export01-parent/process.json`, `rss.jsonl`, `stderr.log`: actual parent,
  memory samples and retained warnings.
- `preparation/`: supervising source, frozen source/environment, build logs,
  activation timing and external parent time log.
- `native-return.json`: Model's bounded native closure record.

The native2GB weight identity reuses its existing pinned checkpoint manifest
and stat; it was not redundantly rehashed. The newly produced graph was hashed
once. Read-only permissions are not WORM. Historical tokenizer-regex warning,
`torch_dtype` deprecation and legacy ONNX-export deprecation remain in stderr;
no tokenizer repair, precision ladder, extra cases or reference replay occurred.

## Browser attempt: stopped on sampled memory pressure

The actual Safari27 FP16/WebGPU attempt used combined source
`cd1507c80fe7364bed045106a11e7a9087a364b0` and the unchanged exported graph.
The engine initialized successfully, exposing a device with `shader-f16` and
2,147,483,644-byte buffer/binding limits. One prediction request was in flight
when sampled macOS memory pressure changed from level1 to level2. The controller
aborted the owned operation and disposed its worker. There were **zero completed
requests and zero returned probabilities**. This does not mean zero model load
or prove that no physical forward work occurred; no completed-forward counter
was returned.

| Browser fact | Recorded result |
| --- | --- |
| Browser interval | 2026-11-12 12:57:05.046–12:57:09.512 UTC |
| Model-load-through-disposal interval | 4.35822 s |
| Whole bridge / external controller | 4.46656 / 4.9651232907 s |
| Worker initialization | 3589.74 ms |
| ONNX session creation | 2807.88 ms, excluding model fetch684.6 ms |
| Browser charge | 6 s |
| Closed Qwen chain | Native20 + browser6 = **26/1200 s** |
| Closure observation | 12:58:40.924168 UTC: disposed, not busy, null engine metadata |
| Browser total/peak memory | Unavailable |
| Decision | No parity result, no normal-demo Qwen exposure or retry |

Pressure was sampled before and during the attempt, not continuously. Its rise
does not establish Qwen-alone causation, a browser memory peak, a numerical
failure or general model incapacity. Global/user browser state remains unknown.
The successful native export/reference and partial browser evidence are retained;
no precision/backend ladder, native reference replay or further Qwen attempt
was authorized by unused seconds. The normal demo remains M9.

Exact browser evidence is under
`artifacts/release/browser-b2-20261112-01/qwen-01/`:
`receipt-after-abort.json`, `controller-return.json`, `closure-observation.json`.
Model's small closure record is
`artifacts/model/browser-b2-20261112-01/qwen-return.json`.

## Prospective gate and remaining limitations

The prospective route is Safari/WebGPU with shader-f16, pinned ORT-Web
1.22.0-dev.20250409-89f8206ba4 and Transformers.js3.8.1. A no-model adapter
capability check advertised2,147,483,644-byte buffer/binding limits, exceeding
the272,269,312-byte FP16 embedding. This is not an operator/device/model pass.

The stopped browser attempt produced no output for numerical acceptance; the
fixed gate was **not evaluated**, rather than passed or numerically failed.
Do not expose Qwen in the ordinary demo based on export/initialization success.
The unchanged gate uses exactly the three original P11 short TRAIN inputs: exact
prompts/tokens/option coverage, finite probabilities, sums within1e-6,
maximum absolute FP32-native/browser probability difference≤0.01 and identical
top choices on all three. No changed reference, clipping, renormalization,
threshold relaxation or baseline substitution. M9 remains primary/default and
has its separate600-second browser allowance: its initial and server-unavailable
phases returned at6 seconds total, with independent numerical passes reported
separately. Qwen's26-second chain is closed; unused seconds grant no new
experiment. Its task worker was disposed before the13:10UTC cutoff.

Three portability examples do not establish wider quality, calibration,
long-input behavior, all-input equivalence, another browser, browser peak memory,
offline Qwen operation or public redistribution clearance. Later publication
revisions are not retroactive executed-source revisions.
