# E6 independent fresh-start control review

## Verdict

**No blocking finding for starting-control artifact comparability.** All three actual M6 starting prediction files are byte-identical to the preserved P3 **run-02** files. Independently checked **624/624 presentations and 2,390 raw option probabilities**. No changed choices, top sets, ties or tie presence; neither predictor has a tie. No fresh-control substitution, probability repair or normalization was used. This is a starting-control review only, not a trained-performance conclusion or an approval gate. Model owns ongoing training independently.

Evidence: `receipt.json` contains complete SHA256 source/artifact pins, runtime claims and filesystem chronology; `check.py` is the independent CPU artifact verifier. Executed successfully with `/Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python -B`, without models, tokenizers, weight reads, references, quality scoring, tests, lint, syntax-check commands, network or paid calls. No subagents or background processes were launched. Only these three new review files were written; owner control receipts and any prior failures were not modified.

## Actual prediction and input checks

| Suite | Rows | Option probabilities | Byte equality to P3 run-02 | Max raw absolute delta | Choice/top-set/tie changes |
|---|---:|---:|---|---:|---:|
| v2-original | 300 | 1,160 | Exact | 0 | 0 / 0 / 0 |
| v2-reversed | 300 | 1,160 | Exact | 0 | 0 / 0 / 0 |
| probes-paired | 24 | 70 | Exact | 0 | 0 / 0 / 0 |
| **Total** | **624** | **2,390** | **All exact** | **0** | **0 / 0 / 0** |

Every raw difference is zero: min, mean, all quantiles and max are zero (2,390 comparisons). This is stronger than merely meeting the frozen absolute tolerance **1e-6**. Both sets contain zero ties. Deterministic input-order tie-broken choices were independently derived, not taken from a handoff.

Strict JSON parsing rejects duplicate object keys. All inputs have exactly the decision-only fields, valid ordered options and globally unique IDs across these suites. Both prediction sets have complete, unique ID coverage, correct schemas, exactly the expected option IDs without duplication, finite numeric non-boolean values in [0,1], and valid probability sums. No missing, extra, duplicate, malformed or invalid rows/options were observed. Comparisons join by case/option ID; token evidence also matches all case IDs.

The existing independent shared `jeff.evaluation.metrics.validate_prediction` validated both prediction sets using label-free inputs. Its normalized return was **discarded**; all comparisons and choices used the original stored probabilities. Maximum sum deviations are 1.3131648302078247e-7 / 1.341104507446289e-7 / 6.151094567030668e-8 respectively, not grounds to modify these outputs.

Prediction SHA256s, each shared by fresh and P3:

- original: `a9fe8f71e9194f269ec2ae926adebad1d45fed3618e0d4e10b83c19d5b3a14f5`
- reversed: `533ccb206619c9fb9e0a2a8067a5a463386d025500e43ad11540977215609d78`
- probes: `5d53748678ad63ec0910a54fea18965e4e4e0fe938fd3caf58474a742bd09058`

Actual input byte hashes match the E6 input binding, Model control manifest, both audits and retained E6 freeze pins:

- original: `2103447bf8fbca3b43c09b0506b943179e96f7e774d7ae8363eddbf940970917`
- reversed: `ba266b3b77896d77a453b095da485b569f0cde2238d94493e0a4bcfb704c92f1`
- probes: `051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6`

## Semantic, source and lineage checks

The actual `starting/receipt.json` embeds exactly the new control audit evidence and hashes that audit correctly. Its evidence matches retained P3 audit evidence for config, config/source bytes, asset inventory, official chat-template hash, package/environment versions, input manifest and **all 624 per-presentation full prompt token hashes, token lengths and answer-token mappings**. Recorded complete statuses, suite output hashes, token totals and counts reconcile with actual files and both run receipts.

- Base: `Qwen/Qwen2.5-0.5B-Instruct`, revision `7ae557604adf67be50417f59c2c2f167def9a775`.
- Recorded base `model.safetensors` SHA256: `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe`, identical across retained P3/new audits and comparison freeze. **Not rehashed in this review.** Starting process points directly to retained P3 `download/model`, not a trained checkpoint. The recorded inventory contains base assets and one base weight file, no trained adapter inventory.
- P3 code commit: `49823af30d6b394a147c7b8a9f5c676526a439f3`; fresh Model code commit: `dafd5d235b53af341fbf539e4bf32dcf09a399f2`; both record clean trees. Evaluation review HEAD: `518251d11086f3358eb559cd8c1e7b85aee743bf`.
- Actual adapter blobs at both commits, and current Model adapter file, match SHA256 `325d3a6b8e5577bba3b885fe8b61d5551305b456e2586d3949b2c45c649438d5`. Git diff for `src/jeff/runtime/qwen_challenger.py` is empty. This is the unchanged original P3 base adapter, not a newly invented baseline implementation.
- Config SHA256: `2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f`; template SHA256: `cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f`.
- Exact system prompt: `You are a decision assistant. Choose exactly one of the listed options. Reply with only its letter.` User layout: `State:\n{state}\n\nQuestion:\n{question}\n\nOptions:\n{options}`, each option rendered as `A. text` etc. IDs/metadata are not prompt features. Official system/user chat template with generation prompt; no extra special tokens on encoding.
- Source explicitly checks complete appended-answer tokenization has the identical full prompt prefix plus exactly one distinct answer token. Every observed option mapping is the A–F prefix of `[32,33,34,35,36,37]`, matching P3 for every presentation.
- Cap **1024**, `truncation=False`; recorded full lengths 94–220 original/reversed and 98–124 probes. Token totals **39,949 + 39,949 + 2,638 = 82,536**, all audit/run totals agree. **Zero overflow**, no partial/failed suite. This confirms retained token-audit evidence, not a fresh tokenizer recomputation.
- Source loads local safetensors, disallows remote code and automatic MPS fallback, checks parameter FP32/device, sets four CPU threads, disables gradients, selects eval mode and runs under inference mode. Each forward is batch one, MPS FP32, SDPA, no cache, last-token-only projection. T=1 softmax over supplied answer-symbol logits only; not a full-vocabulary or calibrated confidence. All these config/environment pins match P3.
- Recorded environment: Python 3.12.16, macOS 26.7.1 arm64, torch 2.15.0, transformers 4.57.6, safetensors 0.8.0, tokenizers 0.22.2. No ML packages were loaded by this review.

Read the actual owner `compare-start.py` rather than executing it (it exclusively creates an owner receipt). Its comparison uses raw option probabilities, checks pinned retained outputs, and reports maximum difference/top-set/tie-presence changes without labels. This independent verifier adds strict duplicate-key/ID/option checks, validates **both** prediction sets and derives deterministic choices. The owner's `starting-comparison.json` agrees with the independently reproduced findings and binds freeze SHA256 `5c24a089e3cb4025fb9fcdf4e10effb838d3fb7394eab96493d41b8598908e10`.

## Actual chronology and its limits

All times UTC, 2026-11-11:

| Evidence | Time |
|---|---|
| E6 plan filesystem creation/mtime | 15:30:22.010902 / 15:30:22.011138 |
| E6 receipt declaration | 15:31:06.064609 |
| E6 public input/plan handoff filesystem creation | 15:31:38.828974 |
| Model comparison freeze creation/mtime | 15:43:20.024806 / 15:43:20.024920 |
| Control audit process | 15:44:03.587896–15:44:06.684103 |
| Starting-control process | 15:44:06.703240–15:44:45.064244 |
| Model `20261111T1546-M6-start-control-ready.md` actual creation/mtime | 15:47:00.763142 / 15:47:00.763237 |

E6 plan hash `7b99168342b23cdec9685a357f9aef88c917e88cc4506dd109b1b0690d52928d` and E6 input-binding hash `a73f53c41537b25e831349b649b3649950cdd721d2ab9492ca902a366b3b8d1e` still match the actual files and Model comparison freeze. The E6 handoff says it froze before start/trained outcome inspection; actual local timestamps are consistent with plan/freeze preceding this starting run. The Model handoff filename says 15:46 but actual filesystem creation is 15:47; no inference of exact publication time is made from its filename. Starting process and invocation fields agree; process reports exit 0, no timeout, no automatic retry, wall time **38.36112583428621s**. Audit process also reports exit 0.

**Qualifications, not blocking mismatches:** local timestamps, handoff statements, hashes and receipts are not a cryptographically authenticated precommitment, remote asset authentication, or independent observation of actual tensors loaded into that process. Byte equality alone cannot prove execution was fresh rather than copied. Source review plus consistent metadata establishes supported scoring semantics and recorded lineage, not live tensor attestation. Weight content and tokenizer computations were deliberately not re-executed. Visible complete control receipts disclose no failed starting attempt; this bounded review cannot rule out unrecorded attempts elsewhere. No receipts, failed attempts or historical P3 evidence were replaced or removed. No training outcomes/training data were inspected, and no quality or learning-effect conclusions are drawn.
