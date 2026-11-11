# R6 frozen order-packet review

## Decision

**The actual packet is structurally consistent; no deterministic audit→predict schema/equality failure was found by inspection. Conditional GO for Runtime only after the two launch gates below. The runner alone is not a complete frozen-packet / hard-deadline enforcement mechanism.** No diagnostic was executed in this review, and no model or tokenizer was imported.

### Launch gates / minimal fixes

1. **Bind the preselected packet, not merely whichever files happen to be present at audit time.** `run_order_packet.py:182–201` hashes the directory but does not compare `packet.json`'s declared input/config/selection hashes to the files, require its presence/schema/status/counts, or pin its digest independently. Lines 234–241 validate selection schema, manifest digest and case-ID coverage, not exact frozen selection contents. `read_rows` accepts any 1–48 cases, not necessarily this packet's 48. Thus a replacement/subset packet with matching coverage can pass audit and subsequent equality. The present packet does have all correct bindings, 48 cases and 192 rows (verified below); this is a pre-audit substitution gap, not an observed corrupt packet.
   - **Smallest operational closure:** Runtime must compare the runner and all four packet file hashes against the independent values below immediately before audit, then keep those files unchanged through predict. Do not regenerate the packet or silently accept a different digest. Audit→predict equality and the post-inference small-file recheck then protect subsequent drift.
   - **Smallest code closure, if preferred:** pin the expected `packet.json` digest independently, require its schema/48/192/conditions, verify its three file bindings, and pin the runner at launch. No resampling or source-shard reread is needed. A self-consistent packet without an independent expected digest is insufficient.
2. **Provide an external wall-clock stop and single-use Model grant.** `check()` at lines 410–412 is cooperative. There is no timer alarm or subprocess supervisor in the runner; imports, asset hashing, tokenizer construction, model loading, MPS synchronization and fsync can exceed 300 seconds before control returns. SIGTERM/SIGINT handlers are not deadlines and cannot guarantee prompt interruption inside native code. Final receipt hashing/writing is also outside a hard bound.
   - Runtime should use its existing bounded process supervisor: deadline covers command startup, verification/tokenization/load/forwards/output; terminate at the authorized deadline and kill if necessary, without relaunch. Record supervisor exit/deadline evidence separately. If the grant means 300 seconds for audit **plus** predict rather than per command, share one remaining-time budget; the script currently resets 300 seconds for each command.
   - There is no durable once-only execution claim: separate fresh output directories permit another full pass. Record/consume the grant before launching predict; any nonzero attempts or incomplete evidence means stop and report, not resume/retry. No framework or new dependency is necessary.

These are launch/protocol gates, not a request for more research or another model run. This review did not modify either script or any existing artifact.

## What was actually checked

Read root `AGENTS.md`, `docs/coordination.md`, `docs/plan.md`, `docs/contracts.md`, `docs/swarm.md`; both new scripts in full; current `src/jeff/runtime/qwen_challenger.py` in full; and historical P3 source directly from Git revision `49823af30d6b394a147c7b8a9f5c676526a439f3`. Examined only approved P3 audit metadata (status, configuration, source/config/template pins, asset inventory, environment); did not follow its input/suite paths. The scripts were not imported or run.

Used stdlib JSON/hash/count/identity arithmetic on the four permitted TRAIN packet files, without printing decision text. No TRAIN source shards or allocation files were reopened, so source-to-packet provenance is supported by preparer inspection and frozen metadata, not independently replayed selection. No Evaluation/probe/D3/final content was opened. No tokenization, model-stack import, weight scan/load/inference/training, new dependency, software test, lint, build, commit, merge, mailbox activity, or background job occurred.

### Actual packet arithmetic

- 48 selected cases, 192 unique presentations; each of O0L0/O0L1/O1L0/O1L1 occurs 48 times.
- Each family has inherited/new_a/new_b quotas 4/6/6; all nine declared source paths end in `/train.jsonl` and have `split=train`. Selection case coverage equals presentation case coverage. Zero recorded uniqueness fallbacks.
- Every new-rule selected policy is non-null. Preparer assigns `policy=scenario_id` for new rules (not mechanism group), and greedy freshness checks root, source group and policy. This is a preference with explicit fallback, not an unconditional global uniqueness promise; counters reset per bucket.
- K distribution over presentations: K3=44, K4=136, K5=8, K6=4; all within K2..6. Selection does not rank by K or targets. Preparer validates schema/options on all candidate TRAIN rows before selection, so invalid source data causes failure rather than hidden quota reduction.
- All actual rows have exactly the runner's nine expected fields; options have exactly `id,text,letter,original_position`. For every actual case, verified condition flags/ID suffix, unchanged state/question across conditions, original-position permutation, letter assignment, and identical `(option_id,text)` identity after restoring original positions. No decision text was emitted.
- Packet's declared input/config/selection hashes equal actual bytes. Packet's preparer and current-runtime hashes match the corresponding current files. Packet config equals the original audit config with **only** `maximum_run_seconds` changed to 300.

## Control and compatibility findings

### Four conditions and readout — PASS by source/packet inspection

For original index `j` and K choices:

| Condition | Display order | Letter attached to original j |
|---|---|---|
| O0L0 | original | A+j |
| O0L1 | original | A+(K−1−j) |
| O1L0 | reversed | A+(K−1−j) |
| O1L1 | reversed | A+j |

The last row preserves identity→letter mapping while reversing display order; the middle two share identity→letter mapping but differ in display order. Runner validates both flags and all identities, renders supplied letters rather than regenerating ascending letters, indexes logits by the corresponding answer tokens, and restores output probabilities/scores to original positions with opaque option IDs. Ties select the first displayed maximum and explicitly list displayed tied IDs, consistent with an input-order tie break. Reversing letters changes visible prompt tokens as well as readout identity: results cannot identify an isolated intrinsic letter prior or semantic reasoning mechanism.

### Schema / actual prediction controls — PASS by inspection, not execution

- This is an explicit diagnostic adapter, **not** stock P3's three-suite input manifest. Its inputs deliberately omit per-row `schema_version`; its own strict reader accepts them. Feeding it to stock P3 would fail and, if adapted improperly, could repeat P3's extra startup forwards. Use only the new runner.
- Original historical P3 source hash was independently computed from Git and equals the receipt. Current runtime contains the P4 checkpoint extension; the R6 runner does not import it or its checkpoint helper, and does not accept a trained-checkpoint path/override.
- Compared actual historical P3 `prepare` and `predict`, not tests: system/user strings, official chat template, untruncated encode without added special tokens, identical-prefix-plus-one-answer-token validation, letter-token conditional softmax, FP32/MPS, batch one, four threads, SDPA, eval/no gradients, inference_mode, attention mask, use_cache=False, logits_to_keep=1 all match for L0. Full prompt cap is 1024. R6 additionally validates finite scores/full-vocabulary mass and records logits; these do not change allowed-token probabilities.
- Unlike historical P3's three repeated startup forwards, R6 has only one model call inside its row loop. The first records' predictions are retained, not rerun. At most 192 attempts per invocation; attempted/completed/written counts must match for pass. There is no generation, learning, prompt search, exception retry, or alternate backend path.
- Output includes the contract's schema_version/id/probabilities and additional diagnostic fields. Joins must use IDs; a consumer requiring exactly the three base fields needs a decision-only projection, not the stock input reader. No consumer execution was reviewed.

### Audit `USE_TORCH=0` → predict equality — logically compatible, operationally unproven

Audit sets `USE_TORCH=0`, loads only AutoTokenizer, and requires torch absent from `sys.modules`. Predict sets `USE_TORCH=1`, recomputes evidence and demands exact equality **before constructing the model**. The proof records package versions, Python/platform, rendered/token hashes, answer tokens, paths, source/config/selection/packet bindings and assets; it does not record the intentionally different USE_TORCH value or imported-module state. Audit attests weight identity from the approved receipt; predict hashes the actual weight once and requires the same identity. Both proofs report the same expected asset hashes, so this difference is not itself an equality blocker.

Whether the installed Transformers/tokenizer stack stays torch-free during audit and produces identical tokens with its backend enabled remains unexecuted. If either guard fails, stop; do not weaken equality or change tokenizer/backend as a fallback. Use fresh processes and the same interpreter/environment/path arguments for both commands. Environment proof is not exhaustive (e.g. every MPS environment flag is not recorded); Runtime should preserve and record its normal P3 execution environment, with fallback disabled.

### Pins / leakage / failures

- Model ID and revision are fixed to Qwen/Qwen2.5-0.5B-Instruct at `7ae557604adf67be50417f59c2c2f167def9a775`. Original audit digest, historical source/config/template and model.safetensors digest are hardcoded and checked. Predict requires the exact original asset inventory/hashes, offline local loading and trust_remote_code=False; M6 weights cannot satisfy those hashes. Local asset equality is not an independent remote authenticity proof.
- Preparer reads the released TRAIN shards and group-allocation metadata only; validation entries are manifest metadata, never opened. It drops target fields by whitelisting and never accesses their values. IDs/provenance/domain/mechanism influence preselection, never prompt rendering. Runtime opens packet files, approved audit metadata, and model assets only; it does not follow manifest/source/evaluation references. Path restrictions are procedural guards, not an adversarial filesystem sandbox. Actual packet text was not independently audited for semantic label hints or prompt injection; tokenizer special-token checks remain pending.
- After output directory creation, caught failures normally yield content-free failure receipt, counters, resource samples, output hashes and read-only partial files. Existing-directory/setup failures before the try block, abrupt death/SIGKILL, OOM or failure while finalizing may leave no receipt. Supervisor evidence must then be authoritative; do not treat a predictions file alone as success or authorize a rerun. CPU RSS is process-lifetime high-water, MPS values are observed samples, **not** peaks or additive memory budgets.

## Runtime execution path

1. Obtain the Model slot/grant and record one authorized attempt; preserve packet-v1 unchanged. Do not run preparer again. Independently verify hashes below and ensure the two new receipt directories are outside packet-v1 and do not already exist.
2. In Runtime's existing Python 3.12 model environment, under the bounded supervisor, invoke the reviewed absolute `run_order_packet.py` with command `audit` and all of:
   - `--inputs /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/packet-v1/inputs.jsonl`
   - `--config` and `--selection` pointing to the sibling config.json and selection.json
   - `--model-dir` Runtime's existing original pinned P3 asset directory (not a trained checkpoint)
   - `--p3-audit /Users/destiner/Code/jeff/artifacts/release/p3-qwen-20261111-01/audit-02/audit.json`
   - `--audit-dir` a NEW Runtime-owned receipt directory
   - `--train-only-confirmed`
3. Only after audit exits zero with status=pass, launch **once** in a fresh process with command `predict`, the identical six path arguments and confirmation flag, plus `--output-dir` a NEW Runtime-owned run directory. Do not use stock `python -m jeff.runtime.qwen_challenger`; do not perform warmups or additional startup forwards. No retry, even for a partial pass, without a new explicit decision against the cumulative ≤192 budget.
4. Accept only supervisor-success plus receipt status=pass and expected_rows=written_rows=completed_forwards=forward_attempts=192, cases=48, and complete ID/option coverage. Preserve partial/error evidence otherwise. This review grants no compute and does not claim any actual predictions.

Operational unknowns remaining: actual Model grant/slot, original asset-directory availability, existing environment/import behavior, token lengths/boundaries/special-token rejection, installed model signature/MPS availability, wall-clock/resource fit including the one prediction-time weight scan, and durable supervisor/failure evidence. None was exercised here.

## Reviewed SHA-256 identities

| Item | SHA-256 |
|---|---|
| `.worktrees/research/experiments/research/prepare_order_packet.py` | `0b674aa2f07f48e62df4b47181987f5d75e0ab5a0b18a569b2c1d72c644ec2a1` |
| `.worktrees/research/experiments/research/run_order_packet.py` | `02c32c812ae9d9e1d6a61af4a68ba902fe2f9194cf72b05cf239999da4d2c36f` |
| `packet-v1/packet.json` | `7598451302c5389e62476c88e7c2489fa355e0c40611e91cfbd6da1d9dc35e03` |
| `packet-v1/selection.json` | `8e008f2c39e37529d32942b15eaba5e5b13cc0b9b3766f6d9b12722f15304a8f` |
| `packet-v1/config.json` | `128d550e355af4772a8f996ccb1f49675e5ba6bdc61d2ed7a1c84e11c4b6090f` |
| `packet-v1/inputs.jsonl` | `178708cd6a620c395d29131a0eb0bad65f66f8a71e608950f7282a4e9e2ed061` |
| Approved original P3 audit | `8e0dc65beb1c9dd5a21b2c4170853bc78bf14116429a9311c28e568c129d870a` |
| Historical P3 source at receipt revision | `325d3a6b8e5577bba3b885fe8b61d5551305b456e2586d3949b2c45c649438d5` |
| Current root runtime source (P4 extension present) | `cb07ceaf8af6cf1b06b08d11aff7a234031877428eb0aa27e37ad609eef731a5` |
| Root `configs/runtime/p3-qwen.json` | `2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f` |

All review commands completed synchronously; no jobs remain running. Only this new review artifact was written.
