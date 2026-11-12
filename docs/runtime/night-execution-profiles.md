# Internal P8/P9 execution-input profiles

These are narrow Runtime orchestration inputs, not new shared checkpoint or
scoring contracts. They do not grant execution authority. Model schedules loads;
the owner must freeze real assets, provenance, source/environment and a fresh
audit after integration, then obtain the Model execution grant.

## Exact inputs

Use the existing input-manifest shape: `schema_version` and `datasets`; each
entry has only `name`, `path`, `sha256`, `rows`. Paths resolve against the manifest.
The existing `read_inputs` decision-only parser validates every row and physical
row count. Missing/extra suites, changed order, names, counts or hashes fail.
Unknown profiles fail. No labels, padding, alternate parser or free-form row cap.

| Profile | Suite (in order) | Rows | SHA-256 |
| --- | --- | ---: | --- |
| `p8.inputs.v1` | `d3-seen-rules` | 96 | `afd02eb196889f79384488fa1998dcb95c79d96dccd1235a70fd30940c2bf928` |
| `p9.inputs.v1` | `v2-original` | 300 | `2103447bf8fbca3b43c09b0506b943179e96f7e774d7ae8363eddbf940970917` |
| `p9.inputs.v1` | `v2-reversed` | 300 | `ba266b3b77896d77a453b095da485b569f0cde2238d94493e0a4bcfb704c92f1` |
| `p9.inputs.v1` | `probes-paired` | 24 | `051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6` |

## Checkpoint and evidence boundaries

P8 permits original P3 without a checkpoint manifest, or a trained v1 manifest.
The owner separately pins actual original assets and M7 v1 inventory; absence of
a manifest does not prove original weights. P9 requires a trained v1 manifest;
the owner separately freezes actual M10 seed-7 full-parameter receipt provenance.
Runtime validates existing v1 identity/receipt bindings, not the truth of training.
Neither profile accepts v2. Original P3 configuration bytes are required; the
training scoring pin, loader, prompt/tokenization and conditional T=1 scorer stay
unchanged. Input-manifest bytes/profile already enter full evidence equality;
non-v2 still requires an exact fresh audit and the clean unchanged Git revision.

## Bounded execution and remaining external authority

The same prediction loop repeats the first three existing encoded rows for
startup: P8 has exactly 99 attempted/completed stock-HF calls per decoder arm;
P9 has exactly 627. Attempts increment immediately before the actual model call,
with the maximum checked first; completions increment after synchronized return.
Failures retain partial counters. No extra warmup, canary, START624, retry or fallback.
New profiles enforce 8 GiB CPU lifetime RSS / sampled MPS driver limits and at
least 2 GiB recommended-minus-driver headroom before/after CPU construction,
MPS transfer and every forward. Resource observations are samples, not MPS peaks.
The frozen cooperative 1200-second recipe is unchanged. An external whole-group
supervisor must later enforce P8's aggregate 600 seconds across all authorized
arms and P9's <=310 seconds, including verification/load/startup/cleanup; these
shorter deadlines are not enforced here. Encoder orchestration is outside this change.

## Legacy compatibility

`p3.inputs.v1` still requires exactly three nonempty suites. Its original/no-manifest
and v1 receipts gain no counters or headroom rule. Existing v2 behavior remains
restricted to its legacy 300/300/24 inputs and 627-forward maximum; no v2 expansion.
