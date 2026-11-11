# E6 independent M6 TRAIN-fit/control review

## Finding

The saved evidence consistently records the single authorized M6 run completing 1,500 TRAIN presentations and 375 AdamW updates, but deterministic TRAIN fit **regresses**. No demonstrated implementation bug was identified in the reviewed rendering, target mapping, reset, loss, gradient or training-loop code. This is a failed fitting outcome, not evidence identifying its cause: optimization, inputs/labels, exposure and capacity remain unresolved. It is neither held-out performance nor a decoder-wide or permutation-only causal result.

**No new review gate or blocking action. P4 proceeds independently.** Preserve the candidate, failures and planned final-checkpoint evaluation; no retuning, retry or alternative inference was performed or requested.

## Independently reconstructed fixed-checkpoint fit

Joined the actual fit rows to the explicit TRAIN schedule and then to the nine authorized TRAIN shards. No case-ID parsing supplied family, source, group, target or policy ancestry. Each phase covers all 1,500 rows with finite saved CE, correct metadata and internally consistent agreement/argmax; the same schedule is used in both phases.

| TRAIN population | Rows | Before agreement | After agreement | Before mean CE | After mean CE |
|---|---:|---:|---:|---:|---:|
| Overall | 1,500 | 805 (53.6667%) | 431 (28.7333%) | 1.357723629 | 1.390592028 |
| Intent | 500 | 442 | 140 | 0.396152925 | 1.391937832 |
| Sentiment | 500 | 179 | 137 | 2.019891845 | 1.444125607 |
| Rule application | 500 | 184 | 154 | 1.657126115 | 1.335712646 |

Intent and overall proper scores worsen; sentiment/rule CE improves despite lower agreement. Teacher-labelled intent/sentiment are teacher agreement, not independently verified correctness. Rules retain their existing `rule_verified` interpretation and qualifications. The authorized TRAIN inventory has 1,000 teacher-labelled and 500 rule-verified rows, 880 source groups; correlated rows are not independent observations.

All **1,500 after-fit argmax positions are 0**, including 500/500 in each family. Overall before argmax counts at positions 0–5 are `[417,384,411,278,7,3]`; after counts are `[1500,0,0,0,0,0]`.

| Target position (zero-based) | Rows, unchanged | Before agreements | After agreements | Before CE | After CE |
|---|---:|---:|---:|---:|---:|
| 0 | 431 | 229 | 431 | 1.412589134 | 0.812336753 |
| 1 | 423 | 231 | 0 | 1.231813667 | 1.790865680 |
| 2 | 368 | 210 | 0 | 1.286381888 | 1.626891939 |
| 3 | 266 | 127 | 0 | 1.590883211 | 1.352821204 |
| 4 | 11 | 7 | 0 | 0.869043760 | 1.563803814 |
| 5 | 1 | 1 | 0 | 0.579394817 | 2.486203194 |

`fit-aggregates.json` preserves full independently computed overall/family/source/source-group/target-position/family×position aggregates, including all 880 explicit source groups, counts, CE sums and distributions. The overall, family and source-group aggregates exactly reproduce the receipt.

**TRAIN ties are unknown.** Saved fit rows contain CE and argmax only, not per-option probabilities or logits. An argmax of 0 does not establish an untied maximum. Full within-vector/across-case per-option probability variance is likewise not available from these fit files; no runtime variability diagnostic was run or invented. Variation in CE is not a substitute for the missing option distributions.

The saved **online changing-weight mean CE is 1.4003377714039138** over 1,500 rows. It independently reproduces the receipt and follows 375 four-row update groups, but is not a fixed-checkpoint before/after fit score and is not held-out evidence.

## TRAIN boundary, schedule and recipe

- Exact authorized manifest SHA256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`; all nine TRAIN shard hashes/counts verified. Only TRAIN shard contents were opened. No validation, D3, final or diagnostic label files were opened.
- Independent `random.Random(42)` replay, shuffling TRAIN rows and then options once per row, reproduces all 1,500 schedule decisions, option identities/texts, original option order, target identity/position and explicit metadata. Exactly 1,500 unique authorized IDs. This excludes extra or substituted D3/dev/probe/final rows from the saved training/fit schedule; it is not independent historical process-I/O attestation.
- Schedule SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8` agrees across actual schedule, frozen plan, audit, training identity and checkpoint manifest.
- Recipe SHA256 `61b43e043bb11f3fa25cb39bf4c09bc80040da802a0eeb617d4ec1378787a624`: one epoch, microbatch1, accumulation4, 375 updates, AdamW LR2e-5, betas(.9,.999), epsilon1e-8, weight decay.01, clipping1, foreach=false, seed42. Exact committed config bytes match the published pin.
- Recorded completed stages independently count 1,500 forwards/backwards, 375 clips/optimizer steps, 1,500 before-fit and 1,500 after-fit forwards, one final optimizer-state check and one checkpoint save. No additional full-run backwards are recorded. These are saved stage records, not a live tensor trace.
- Audited prompt token inventory is 89–220 tokens under cap1024. Every saved token-list digest/length and A–F answer-ID sequence agrees. No tokenizer was loaded or executed by this review, so tokenization was not freshly reproduced.

## Exact-source review and historical execution limit

Reviewed `src/jeff/training/qwen_decision.py`, `qwen_data.py` and the imported Runtime P3 implementation from Git **`dafd5d235b53af341fbf539e4bf32dcf09a399f2`**, not a later unpinned trainer. `source-pins.json` compares every recorded tracked-file SHA256 against that exact Git revision; all match. Frozen E6 artifact plan bytes equal `docs/evaluation/e6-plan.md`.

- Rendering calls unchanged P3 `prepare`: state/question/option text only, official system/user chat template and generation prompt, no label/provenance/opaque option-ID features, no truncation, complete rendered-prefix-plus-one-symbol boundary check.
- Training reads the final-position logits restricted to the row's allowed symbol IDs, FP32 CE against the permuted target position. This corresponds to P3's T=1 allowed-symbol softmax, not full-vocabulary next-token CE. No target answer is appended to the input.
- Training model is all-parameter FP32/MPS, SDPA, batch1, four threads, cache disabled. The loop divides each loss by4, clips once per accumulated update, steps once and zeros gradients; saved CE is unscaled. Allowed logits and loss must be finite; gradient presence and a finite nonzero global norm are checked with `error_if_nonfinite=True`. Adam per-parameter moments/step counters are checked at the end. These checks do not claim every historical intermediate tensor was independently inspected.
- Before/after fit explicitly uses `eval()` and `torch.no_grad()`, the identical materialized schedule and same loss/readout; training mode is restored afterward. After-fit follows the final update and optimizer disposal, then the final model is saved. There is no development score input, epoch selection or alternate checkpoint path in this code.
- Capacity is a separate process, exercising the four longest TRAIN prompts: one optimizer step and four additional backwards with resident moments, with no second step and no saved weights. Its child PID differs and its recorded successful exit precedes full training. Full training separately reloads pinned original assets, reseeds Python/torch CPU/MPS42 and creates a new AdamW; no capacity optimizer/checkpoint is consumed. Matching identity and capacity-receipt hash checks bind the two processes.

**Source review, byte pins, process records and selected fingerprints do not prove actual historical loaded-tensor execution.** No such attestation is claimed. No giant weights were hashed or read; no model/tokenizer was constructed. In particular, the three small selected fingerprint changes establish what the receipt reports, not an independent all-tensor execution audit.

## Starting control

Independent hash and case/option-probability joins establish byte-for-byte equality for fresh-start vs preserved P3 outputs: original300, reversed300 and paired probes24. Max absolute probability delta **0**, changed top sets **0**, ties **0 in both controls** on all three suites (these tie counts are supported by saved control probabilities, unlike TRAIN fit). Byte equality also implies zero score differences for any identical reference joins; no held-out labels were needed here.

The starting receipt's scoring config, asset inventory, official chat-template hash and package environment match preserved P3; training uses the same recorded config/assets/template. The runtime source hash matches the exact committed imported implementation. The recorded controls are T1 conditional allowed-symbol probabilities, cap1024/no truncation, FP32/MPS, eval/no gradient, batch1/four threads. This is strong saved-output and semantic-control comparability, **not proof that particular historical weight tensors were loaded**. No new control or outcome-driven substitution was run.

## Checkpoint lineage

The actual sibling checkpoint manifest hashes to the required SHA256:

`1fe8f6d169301c76698b78b8d7b067c4b10868fb755324896352d1f61310960f`

Its `source_run_receipt` hash independently matches the complete receipt:

`893c6a1b154734133d49ce41036a05bef2b5830c3615070b3547d56aebff1657`

The manifest binds exact source, TRAIN manifest, recipe, schedule, P3 config and tokenizer pins. Receipt inventory: **290 unique tensors, 494,032,768 trainable parameters**, final Adam state290/step375 with 3,952,262,144 moment bytes. All three published selected small-parameter fingerprints change (exact pairs in `receipt.json`). Nine checkpoint files have the published sizes, and manifest/receipt inventories match. Model file size **1,976,163,472 bytes**; its published, not independently recomputed, SHA256 is `ecbeb36556281cf00e9175603aecefd83f2ce3fc8a610e4b2cf056b7a4a926fb`. Tokenizer files are inventoried and their reported pins match unchanged source assets; their contents were not opened here.

## Runtime and capacity scope

Training external wall **776.083240292s**, internal **774.789562833s**, within the2,700s cap; recorded return0, no timeout or automatic retry. Capacity external wall **8.922245125s**, internal **8.398579750s**, within600s. Its conservative longest-input projection **2,100.337583437s** is an extrapolation, not measured full-run duration or a guaranteed bound.

| Scope | CPU lifetime RSS max (bytes) | Observed MPS current max | Observed MPS driver max | Minimum observed recommended headroom |
|---|---:|---:|---:|---:|
| Full training | 3,371,466,752 | 8,740,772,096 | 11,852,775,424 | 7,216,889,856 |
| Disposable capacity | 2,898,182,144 | 8,730,074,368 | 10,191,831,040 | 8,877,834,240 |

Training receipt has24,768 memory samples,21,765 with MPS fields; capacity has3,084 samples,81 with MPS fields. Stages and exact scopes are in `resources.json`. MPS values are discrete observed samples **not peaks**; CPU is process-lifetime `ru_maxrss`. **Do not add RSS and MPS.** These measurements do not identify the fitting-failure cause.

## Preserved failures and boundaries

Initial immutable `failure-receipt.json` sentinels in training/capacity/audit remain untouched and are hash-inventoried in `supplemental-checks.json`. Source shows they are written before work as incomplete-unless-complete markers, not evidence of additional failed learning attempts. The poor completed fit remains visible without repair or selection.

Only new files under `artifacts/evaluation/e6-train-control-review-v1/` were written. No tests/lint/syntax checks/fixtures/package build, model or tokenizer loads, training, inference, network, paid calls, new datasets, diagnostic labels, final data, mailbox, tracked edits, commits or merges. Final `git status --short` was empty. £0 new spend. This report does not build or modify production code.

## Commands and receipts

Primary actual saved-evidence analysis command (exit0, **82 checks, zero mismatches**):

```sh
cd /Users/destiner/Code/jeff/.worktrees/evaluation
PYTHONDONTWRITEBYTECODE=1 /Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python -B /Users/destiner/Code/jeff/artifacts/evaluation/e6-train-control-review-v1/review.py
```

Read-only source review used:

```sh
git show dafd5d235b53af341fbf539e4bf32dcf09a399f2:src/jeff/training/qwen_decision.py
git show dafd5d235b53af341fbf539e4bf32dcf09a399f2:src/jeff/training/qwen_data.py
```

Runtime P3 source and all recorded tracked source blobs were read with `git show <revision>:<path>` by the same exact project Python. A supplementary standard-library-only inline invocation of that Python compared P3/start/training attestations, frozen plan and recorded completed stage counts (**15 additional checks, all match**), inventoried failure sentinels and ran final `git status --short`. Its actual results are `supplemental-checks.json`; it was not another ML run. `receipt.json` contains the primary exact input hashes, check outcomes and selected fingerprint pairs; `review.py` is the saved reproducible primary analysis. No test suite was created or executed.

**Blockers:** none for this bounded review or independent P4 work. Unknown TRAIN ties/probability variance and historical tensor attestation are evidence limits, not a new gate. Held-out conclusions remain E6/P4's separate task.
