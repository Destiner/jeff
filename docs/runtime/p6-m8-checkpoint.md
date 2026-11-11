# P6 — M8 untied export reload completed

**One fresh stock-HF reload passed strict identity/storage checks and produced624/624development predictions in36.246seconds.** Exactly627model forwards occurred:3existing unscored startup rows plus300original,300reversed and24already-paired presentations. All2390option probabilities passed the label-free output contract. No retry, extra canary or representation fallback occurred.

Model received the slot return immediately (`c42507ca`), and Evaluation received outputs directly (`0cff1986`) before this report/integration. **E8 owns independent quality conclusions; none were available at delivery.** Model's TRAINagreement805→804/1500 and CE1.357724→1.332200 show limited adaptation, not held-out success or failure of feature capacity. No default promotion follows.

## Actual execution

| Measurement | Recorded result |
|---|---:|
| Process UTC | 2026-11-11 22:23:59.859099–22:24:36.105443 |
| External monotonic wall / exit |36.245987792s /0; process group absent |
| Model load / storage and tensor proof |0.653115458s /1.437603250s |
| Startup / scored-suite elapsed |0.198490s /31.094693457s |
| Scored throughput |20.067733decisions/s |
| Maximum probability-sum error |1.271828296e-7 |
| Internal lifetime CPU RSS observation |484114432bytes |
| Native time-wrapper full-process maximum RSS |501563392bytes |
| Native peak process footprint |3145516232bytes |
| Observed MPS driver maximum |2768961536bytes |
| Observed MPS current allocation maximum |2567200512bytes |
| Minimum observed recommended MPS headroom |16300703744bytes |

The activation required8GiB separate RSS/driver guards and>=2GiB recommended headroom. The latter was added, built and frozen **before the first Runtime audit**, with no scoring/config/tolerance change. External supervision targeted TERM300/groupKILLby309 within310seconds, independent of the time-wrapper leader. These are OS scheduling targets, not real-time guarantees; actual completion was well inside them.

CPU/MPS/footprint scopes overlap and must not be summed. Internal RSS was observed before final receipt serialization; the native wrapper covers the full process. Recommended headroom is recommended MPS maximum minus sampled driver allocation, not system free memory. MPS observations are not true peaks. No cache flush, mapping trace or controlled performance comparison was made: the36.246second pass does not establish a speedup. The full untied output adds544538624bytes (519.3125MiB) of FP32 parameter payload regardless of allocator/sample totals.

## What was verified

The [v2 contract](p6-readout-contract.md) was implemented at preparation main`9b2ecf6`; actual execution used`9eeef9cea87fbd0bda7700127e88db95c7b97f9a`. Metadata/tokenizer audit completed in3.108246seconds without model construction or decoded tensors. Its Model-package import does import torch/scorer definitions; it is not torch-import-free.

Both serialized full tables, exact F32 geometry/state inventory, original tokenizer/config/scoring pins and all producer proof crosslinks passed. Fresh HF loading reported **zero missing, unexpected, mismatched or error keys**. Actual CPU byte ranges and allocator-owned MPS buffer identities were independent. All original290parameter and nonpersistent fixed-buffer identities matched Model's before/after/export maps; full output, ordered six learned rows and every non-answer row matched the export proof. Checks added no forwards. MPS handles are opaque Metal objects, not payload addresses.

Model's1500-row START and1500-row same-hidden-state FINAL bindings reported exact logits/probabilities/top sets within the frozen bounds. Runtime verifies the actual reloaded components; **this is not a fresh small-head-versus-stock numerical comparison on every development case**, and it does not independently replay historical optimizer/scope evidence.

## Artifacts and pins

Root: `/Users/destiner/Code/jeff/artifacts/release/p6-m8-20261111-01/`. Compact machine-readable evidence: [`manifests/releases/p6-m8-20261111-01.json`](../../manifests/releases/p6-m8-20261111-01.json).

| Artifact | SHA-256 |
|---|---|
| `audit/audit.json` |`968a709b472d1e492fae81a19f30ae5fee2fe86231a5edf9f347b760cbd8e219`|
| `run/receipt.json` |`c9171efb12e6c6501352a12fe16c20415c83b499f2b20c823030e29b5183e610`|
| `run/v2-original.jsonl` |`c3571534c9a2040829c2292f7c9b333541c9db40f840008f3c3d2f28fd2b6951`|
| `run/v2-reversed.jsonl` |`6e50885a7bb967c103defcc735d48a8c7292280654bd93aaf6d2a8b32cc2514d`|
| `run/probes-paired.jsonl` |`db1b6b869f245a93f5a8a4cc0e80b0fcd4d3ceec3808d3f6959e0a723d32af7c`|
| Model sibling manifest |`d558079b06d77b0245dfcc239afbd505b532f54d7506bbd31bf5f29a40eba43d`|
| Model readout proof |`8e5706c2b3c458bb28fc84d6f956936c639fb1363a5aacd30f34895e7b6d8260`|
|2520702368-byte trained safetensors |`419f8f96205b3b2bd76f58727562e637a4830bc1f13aa12133a4a2589548f80a`|

The root also retains process invocation/exit receipts, raw logs, one-shot launcher, output validation and delivery summary. Model checkpoint: `artifacts/model/m8-qwen-readout-20261111-01/training/checkpoint/`. Reservation`da3eabb7` was activated by actual checkpoint/process message`29d92b09` and consumed once. Input bridge`77c57b75...` and P3scoring config`2698ed67...` are unchanged.

Source review caught serialization normalization and incorrect MPS-address arithmetic before Model's first weight load; Model preserved its earlier tokenizer-only audit/refreeze. Runtime had no failed execution. Existing tokenizer-regex and torch_dtype-deprecation warnings are retained in stderr, not silently repaired. Fresh HOME/cache and offline/local-only flags do not establish OS network denial, fully offline installation, Linux support or publication rights. No tests/lint, dependencies, uploads or additional spending; £0actual/pending/allocation.
