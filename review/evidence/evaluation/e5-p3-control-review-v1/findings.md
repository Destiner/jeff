# E5 independent P3 frozen-control review v1

## Disposition

**No blocking factual defect identified in the reviewed frozen control.** This is a bounded CPU/read-only review, not an execution/compatibility certification, promotion, compute grant, or new release gate. Runtime owns source/execution; Model owns compute scheduling. No decoder quality outputs, labels, reference files or final data were inspected.

**Nonblocking qualifications:** token-boundary evidence is the owner's recorded audit plus independently inspected source, not an independent tokenizer replay; freeze chronology is a contemporaneous claim, not cryptographic proof; resource guards are sampled/cooperative; latency/memory scopes are limited; hard process death can prevent the inner receipt. All are detailed below.

## Exact freeze and input binding

Reviewed `/Users/destiner/Code/jeff/.worktrees/release` at clean Git HEAD **8b03a390d2164cf9495aabcffe0f993b7a4fa9c0**. Worktree source/config bytes equal the committed blobs and audit hashes:

- `src/jeff/runtime/qwen_challenger.py`: `08e02641c25ef5afd6c51cc82dbdc4c9c2c8d35ebd345016e34d4119b2ecb833`.
- `configs/runtime/p3-qwen.json`: `2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f`.
- Runtime `inputs.json`: `77c57b75b64a0b306c8c851bb2d3a023bddd5d237334cd288316013c26d2927a`.
- `audit/audit.json`: `d90446114a51af995db436d69362714d904cb641d50b3d993ddaf997a99db8e4`.
- `download/manifest.json`: `7741a686ef6f0cc211438961223fb089e5f3a62da17c582cca27b021ce6191b5`.

Runtime's three dataset entries match E5's binding field-for-field on name/path/hash/rows. Independently read/hash-checked **300 + 300 + 24 = 624 presentations**, unique IDs within each suite, exactly decision fields `schema_version,id,state,question,options`, and option fields `id,text` only.

| Suite | Rows | Input SHA256 | Recorded full-prompt min/max/p50/p95 |
|---|---:|---|---|
| v2-original |300|`2103447bf8fbca3b43c09b0506b943179e96f7e774d7ae8363eddbf940970917`|94/220/133/171|
| v2-reversed |300|`ba266b3b77896d77a453b095da485b569f0cde2238d94493e0a4bcfb704c92f1`|94/220/133/171|
| probes-paired |24|`051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6`|98/124/107/124|

All 300 reversals preserve state/question/text and reverse complete option records exactly, with the expected `.evaluation-reversed-v1` decision-ID suffix. They do **not** retain identical decision IDs; the receipt intentionally records that strict unchanged-ID comparison as false and the correct suffix-aware comparison as true. Probes independently group into 12 exact original/reversed pairs by task text and option records. No extra probe reversal is needed. The inherited60/new240 partition remains Evaluation-owned: its claimed strata were read in the E5 handoff, not rejoined against private/reference identities here. Reversals are repeated measurements, not independent cases.

## Pinned model, template, boundaries and context

R1's local recommendation names `Qwen/Qwen2.5-0.5B-Instruct` at **7ae557604adf67be50417f59c2c2f167def9a775**, matching code/config/download receipt and saved public API metadata. Nine downloaded assets and 999,602,607 total recorded bytes are consistent. Independently verified the eight non-weight files' SHA256, Git blob identities and sizes against the saved upstream metadata and audit. No model or tokenizer package was imported or loaded.

**Weight verification boundary:** only stat size and the owner's published download/audit records were inspected for the 988,097,824-byte safetensors. Published LFS SHA256 `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe` matches the download attestation and audit; owner records `lfs_sha256_verified=true`. This reviewer did not read/hash weight bytes or independently contact upstream. The CDN response has no repo-commit header; revision-specific saved API/LFS metadata supplies that binding. Saved metadata/receipts are local evidence, not independently authenticated remote provenance.

The downloaded tokenizer configuration's official chat template hashes to `cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f`, matching audit. It declares the assistant generation boundary. `prepare()` uses that template with `add_generation_prompt=True`, encodes with `add_special_tokens=False,truncation=False`, and then checks **each allowed continuation at the actual boundary**: encoding `rendered + letter` must equal the complete unchanged prompt-token prefix plus exactly one additional distinct token. It is not a first-token approximation of a multi-token answer.

All 624 audit rows align with actual input IDs and supplied option counts; their recorded answer IDs are A–F = 32–37 as applicable, distinct and one per option, with per-prompt token hashes. All recorded lengths fit the frozen **1024** cap, maximum 220. The source rejects overflow rather than truncating; no recorded input loss. Input special-token-string exclusion is present and independently checked against downloaded added-token metadata. This review did not independently tokenize or reconstruct prompt token hashes; the owner's successful audit plus the inspected exact-prefix assertions are the evidence for tokenizer behavior.

Only state/question/option **text** enters the user prompt; fixed system instructions, headings and positional letters are added by the recipe. IDs only map external outputs; metadata/labels are rejected by the input allowlist. State remains untrusted task text, not a privileged system message. Structural isolation does not guarantee semantic resistance to task-text instructions.

## Exact scoring/runtime control

- One fixed system/user recipe, no generation, prompt sweep, training, fitting, or label-dependent branch.
- For unpadded batch size 1, the final prompt hidden state predicts the next answer token. Installed local Transformers Qwen2 source explicitly supports `logits_to_keep` and slices `hidden_states[:, -1:, :]` **before** the vocabulary projection when set to 1. Adapter additionally checks the loaded forward signature and resulting logits shape `(1,1,...)`.
- Exact implementation: `softmax(result.logits[0,0,answers].float(), dim=0)`. The fixed temperature is 1, so no division is needed. This is conditional normalization over supplied symbols, mathematically `exp(z_i)/sum_allowed exp(z_j)`, not full-vocabulary confidence, generated-answer likelihood, or calibration. It does not measure total probability mass of the permitted letters.
- Explicit `torch.float32`, MPS device, SDPA attention, 4 threads, batch1, `use_cache=False`; parameter dtype/device checked after transfer. `requires_grad_(False).eval()` plus `torch.inference_mode()` provides eval/no-gradient execution (stronger than merely `no_grad`). No autocast. MPS fallback environment must be unset/0, availability is checked, and CPU CLI selection is rejected by the frozen config. Unsupported operations fail rather than silently migrate backend.
- `predict()` regenerates evidence and requires exact equality with the audit, including source/config/assets/input/tokenization/environment/Git revision/status. Clean frozen Git is enforced before loading weights. This is not protection against arbitrary concurrent file mutation after checks.
- First three existing workload rows run as startup-only performance checks in the same process; probabilities are discarded, no quality labels inspected, then all 624 rows are processed once into outputs. These repeats are not tuning scores or extra independent examples. Three rows cannot warm every shape.

## Output, coverage and failure accounting

Predictions map each input option ID in supplied order to one finite [0,1] probability, sum checked within 1e-6, contract schema 0.1, original decision ID. Ties remain for the evaluator's documented input-order tie-break. Each suite records expected/written rows, coverage, status, token counts, timing distribution and output SHA256; exclusive creation and read-only final files avoid overwrite. Each row is flushed. A row failure preserves partial output, active input ID and failed/partial suite status; later suites remain not_started. Top-level errors record type/message and `retry=false`; no outcome-driven retry path.

Qualification: if evidence validation fails before suite initialization, the inner receipt has an empty suite list rather than per-suite expected counts; E5's immutable binding still defines the denominator. Abrupt kill/OOM/native crash can bypass Python `finally`, leaving partial output without the normal inner receipt. This is a reporting limitation, not evidence such a failure occurred. The inspected owner launch wrapper has a 1300-second process-group timeout, TERM/KILL escalation, waits for child exit, captures stdout/stderr and writes an outer process receipt; it does not itself guarantee inner per-row accounting after hard termination. Launcher is not part of the frozen adapter Git hash; execution binding, if produced, must identify the actual invocation.

## Resource and measurement qualifications

8 GiB CPU process-lifetime RSS, 8 GiB MPS driver allocation and 1200-second adapter lifetime are checked at boundaries, not hard OS memory limits or interruptible in-flight load/forward limits. They cannot prevent transient peaks or overshoot; no allocation-limit overrides are installed. The additional 1300-second wrapper bounds a hung process, subject to its own successful supervision.

Cold-load time excludes interpreter/import/preflight; process runtime includes evidence reconstruction (including owner's repeated weight hashing), import/audit/load/startup/full pass/output work; outer wrapper wall additionally covers interpreter/process overhead. Synchronized forward timings begin **after input tensor construction** and end **before probability extraction/CPU transfer**. Suite wall/throughput includes those omitted operations plus output writes; no apples-to-apples pure-kernel claim. CPU `ru_maxrss` is process-lifetime RSS; MPS current/driver samples and their sampled maxima are **not true peaks** or directly additive unified-memory measurements. Row guards observe driver allocation but only selected stages are persisted as samples. No hardware/runtime compatibility or measured performance was established by this review.

## Interpretation risks and chronology

Letter-token priors, absolute option positions, recency/ordering and token choice can affect predictions. Original/reversed presentation analysis can expose some sensitivity but not all permutations/token biases. Conditional choice probabilities may look confident even if the model places little full-vocabulary mass on any allowed answer; normalized output is not calibrated confidence.

This is a practical systems comparison against stored encoder/baseline predictions, **not a causal architecture ablation**: roughly 494M instruction-pretrained decoder versus roughly 22.7M fine-tuned cross-encoder differs in capacity, pretraining, instruction tuning, prompt/context and runtime. Retain inherited60/new240/probe24-over12groups, families and repeated-presentation accounting in downstream analysis; no thresholds, automatic promotion or claims of independent correctness are introduced here.

The 2026-11-11 14:22 Runtime handoff claims a clean committed recipe, cap1024 and successful tokenizer audit **before model loading/outcomes**; E5's earlier handoff requests exactly this freeze. Those contemporaneous handoffs and matching artifact hashes support the claimed chronology procedurally. Git/content hashes establish byte identity, not when execution/outcomes became available; no cryptographic timestamp proof is claimed.

At the receipt snapshot (14:28:46 UTC), no `run/receipt.json` existed. Execution remains unbound by this review unless a receipt is explicitly added to this review's receipt before return; no prediction content or quality outcome has been inspected. Absence is not a runtime failure or a new gate.

## Reviewer resources and deliverables

Only new files in `artifacts/evaluation/e5-p3-control-review-v1/`: this report and `receipt.json`. Used read-only Git/source inspection and bounded Python-standard-library hashing/JSON/data checks. No tracked edits, merges, mailbox, dependency changes, model/tokenizer loads, inference, software tests/lint/syntax tests, network, paid services, or large-weight hashing. No reviewer background/resource jobs started; all reviewer commands finished. Additional actual/pending spend £0.
