# R12: one conditional native NLI adaptation, not a new experiment grant

**Native reuse is technically coherent; reserve one modest full-parameter recipe, but defer an execution decision until actual P12/E14 and exploration evidence makes it useful.** Do not begin implementation or learning from this note. If the original P12 adapter is not already usable, this is not permission to build a second inference backend or delay M10/M11/M12/P12/D8.

The alternative is the exact initialized NLI model, not a pure architecture ablation: pretraining, native classification head, parameter count, tokenizer, context budget and QA bridge all differ from the22M encoders and P3. A short negative result would not establish NLI/encoder capacity limits or adequate optimization.

## Fixed base, interface and objective

Keep `MoritzLaurer/roberta-base-zeroshot-v2.0-c`, revision **`d825e740e0c59881cf0b0b1481ccf726b6d65341`**, with all original native `RobertaForSequenceClassification` parameters and its **two-class head**. Preserve R10's affirmative MIT/source attribution qualification; actual P12 weight/load verification remains the authority for local assets. Do not override `num_labels=1`, reset the head, tolerate mismatched classifier weights or substitute another model.

Unchanged [R10 profile](frozen-nli-source-screen.md): premise `"Context:\n" + state + "\n\nQuestion:\n" + question`; hypothesis `"The correct answer is:\n" + option_text`, with actual LF, verbatim fields and no IDs/targets in text. Same native fast tokenizer, pair order/special tokens, complete512token cap, no truncation, FP32/MPS/fourthreads, native attention implementation, and output mapping. TRAIN overflow blocks the recipe; no dropping rows or new wording.

For each decision with K native choices, let its differentiable pair logits be z[i,0:2]. Use **s[i]=z[i,0]−z[i,1]** and **grouped-choice cross-entropy on s**, with the target's current option index. This is the exact binary form of entailment minus logsumexp(non-entailment); inference stays stable **T1 softmax across that decision's choices**.

- Both native logits remain in the graph: gradients are `dL/dz[i,0]=q[i]−1[i=target]`, `dL/dz[i,1]=−dL/dz[i,0]`. No `.item()`, detachment, Python/NumPy conversion, inference mode or cached features in the training path.
- Call native HF **without `labels`** and compute the group loss externally. HF's built-in binary per-pair loss would optimize a different objective. Do not flatten all decisions into one softmax, treat each negative pair as another decision, normalize sigmoid probabilities, or use only entailment logits.
- Variable K remains attached to its decision; padding, if used, must be excluded from the group denominator. Each decision has equal loss weight, not weight proportional to K. Option identity mapping survives the fixed schedule's permutations.
- The final two-class projection's shared/logit-common component is not identified by this choice objective. In particular, the candidate-independent margin bias cancels across choices. Both rows can participate in gradients without independently learning calibrated entailment/non-entailment truth. No new NLI calibration or preserved general NLI ability is claimed.

## Ordinary native train/eval semantics

The published config has hidden and attention dropout0.1, with `classifier_dropout=null`. Native HF falls back to hidden dropout, and its head is first-token→dropout→dense→tanh→dropout→two logits. **Retain these layers and probabilities.** `train()` enables ordinary encoder/head dropout and gradients; `eval()` disables dropout, while no-grad/inference mode is applied separately for measurement. LayerNorm does not require BatchNorm-style running-statistics adaptation.

Do not call a P12 inference convenience function that hardwires eval/no-grad from the training loss. Share the same tokenizer/rendering/native model factory and differentiable pair-logit computation; retain one inference backend. Deterministic eval fits need not equal noisy online training losses, and varying candidate dropout masks do not establish learned order dependence.

## Exactly one prospective recipe

| Item | Fixed proposal |
| --- | --- |
| Start | Fresh exact original P12 base; new optimizer and seed42 RNG state, not a trained M7/M9 checkpoint or saved P12 scores |
| Data | Released v2 **1500TRAIN only**,500per family; manifest `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac` |
| Schedule | Reuse existing materialized1500row/option schedule, SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`; exact identity/target bindings, no reshuffle/new permutation arm |
| Adaptation | All native parameters trainable, including original classification head; no head reset, detached readout, adapters or cache |
| Optimizer | AdamW **LR1e−5 for every parameter**, betas(.9,.999),eps1e−8,weight decay.01,`foreach=False`; global norm clip1 after accumulation; no scheduler |
| Batch/update | One decision's K≤6pairs per learning forward; accumulate four equally weighted decision losses (`loss/4`); **one epoch /1500presentations /375updates** |
| Endpoint | Fixed final endpoint only; no best-checkpoint selection, extra epoch, LR rescue, early-success selector or second arm |
| Precision/device | Native FP32/MPS, fourthreads, same attention implementation as admitted P12; no precision/CPU/attention fallback |

The rate is a **preservation-oriented engineering choice**, half the prior encoder backbone2e−5 and far below its5e−4head rate. The native NLI head already supplies a meaningful pretrained contrast; there is no evidence for a special high head LR here. This does **not** establish1e−5 optimal, equally effective across architectures, or one epoch sufficient. R11's incomplete rule fit reinforces reporting the actual fit rather than interpreting under-optimization as incapacity. Changing the one recipe requires a new decision, not an automatic fallback.

Use the existing seed42 protocol and record the pre-learning RNG state after initialization and before updates; the full-TRAIN pre-fit must not perturb the declared learning RNG state. The saved schedule is architecture-neutral identity/order data, not reused features or M7's optimizer. If it cannot be consumed unchanged with complete TRAIN token coverage, **defer**, rather than regenerate a superficially equivalent schedule tonight.

## Measurements and meaningful starting comparison

Within the prospective producer chain, run all1500TRAIN **once before and once after** in eval mode, fixed four-decision batches, no startup/canary/capacity update. Save the fixed final checkpoint, release the optimizer/old model, then perform the sole post-fit on its strict native reload; this replaces, rather than adds to, an in-memory post-fit. The producer's two loads plus Runtime's later load all count toward the aggregate budget; do not keep duplicate models resident. Retain full vectors/logits, target mapping, CE/agreement, exact ties, margins and positions, family/source summaries and already-computed pre-clip norms. Online stochastic loss is not the deterministic before/after comparison. No per-step whole-model hash/feature scan is required.

The meaningful development baseline is **the original frozen P12/E14**, with exact model/profile/population bindings, not just M6/M7's collapse. Reuse its624saved outputs when valid; do not repeat the frozen screen. A separately authorized fresh Runtime reload of the fixed final native checkpoint may produce the same624development presentations once, using unchanged readout/batching. Evaluation retains per-family proper scores/agreement, coverage/ties, rule order flips/both-correct and probe retention, alongside M9 and the existing baselines. TRAIN fit is measured on TRAIN, not compared numerically with a nonexistent frozen-P12 TRAIN cache.

A better TRAIN fit with worse development suggests this recipe's transfer mismatch, not a unique cause; improvements on both support practical adaptation under this bridge; minimal fit change remains an optimization-limited negative. Shared increases in output confidence are not calibration. No D3/probe/held-out/D8/D7 rows, labels or derivatives enter training. D8 exploration is decision context only; no new exploration pass or confirmation candidate follows from this note, and a locked cohort is never reopened for this candidate.

## Native save/reload and narrow admission work

Use native **`save_pretrained(..., safe_serialization=True)`** for the complete two-class model and the same tokenizer assets; save the fixed final endpoint, not intermediate candidates. FP32 output weights will be roughly499MB, not the original249MBF16 file. Preserve native semantic config/label maps plus explicit dtype and provenance; no custom detached head or alternate predictor format.

A **separate exact trained profile** must bind original-base asset pins, existing data/schedule, renderer/readout, native architecture/class map, optimizer/dropout/dtype,375updates, actual final files and process receipts. Runtime reloads local native HF assets strictly: no missing/unexpected/reinitialized head, remote code, arbitrary classifier admission or dependence on live optimizer memory. Original frozen P12 admission remains unchanged. Loaded final TRAIN measurement and fresh Runtime final outputs must refer to the same saved endpoint; no extra three-case inference proof is implied.

Current general encoder code is **not CLI-ready reuse**: its scalar/BERT adapter rejects this native two-label RoBERTa model; its trainer uses separate head LR, no accumulation, epoch shuffling, validation before/after and baseline+final saves. Those defaults cannot silently replace this recipe. Existing bundle assumptions include `vocab.txt`, whereas RoBERTa requires its native vocabulary/merges/JSON inventory. After P12 already supplies a working native adapter, the narrow remaining work is mode-safe differentiable reuse, grouped accumulation/fixed schedule, TRAIN reporting, native checkpoint metadata and an explicit trained-profile/export branch—not a second inference implementation.

Static planning estimate **Model45–90min + Runtime20–45min**, potentially overlapping, with source review/build included: **65–135owner-minutes**, not measured readiness. Actual P12 implementation availability was unknown during this source-only review; absence of an NLI-named file on inspected main is not proof no peer implementation exists. No owner audit or approval was requested to prepare this proposal.

## Resource planning and when to defer tonight

API-advertised124,647,170parameters ×16bytes for FP32 weights, gradients and two Adam moments ≈**1.994GB /1.857GiB**, before activations, workspaces, allocator caches, serialization copies and runtime overhead. One decision/≤6pairs per learning microbatch reduces activation demand relative to four-decision/≤24pair inference batching, but adds backward state. A rough **3–6GiB per observed process/driver counter** planning envelope assumes ordinary native attention, length≤512 and no duplicate model; it is unmeasured and the scopes overlap, not an additive physical-memory peak.

Propose separate **8GiB RSS and MPS-driver guards**,≥2GiB recommended headroom, and **20minutes aggregate producer+fresh624Runtime process time** including load, pre/post fits, learning, save/reload and output work. These are prospective hard bounds, not an authorization or feasibility result. Any semantic/numerical/resource failure stops; no learning retry, disposable capacity update, new precision, cloud or dependency fallback.

Existing TRAIN option-count metadata has K2/3/4/5/6 counts **1/394/1035/56/14**, giving5688pairs per complete pass. Pre-fit+one learning pass+post-fit are4500decision presentations /17064candidate pairs; the future624development pass adds2390pairs: **19,454total pair presentations**. Learning is1500native calls and375optimizer updates; fixed batch4pre/post fits are375calls each and Runtime156, **2406native classifier calls** total, zero startup. Pair presentations are not native-call counts.

If backward costs about twice forward, the chain is roughly **13 frozen624-pass forward-work equivalents**, before microbatch throughput, loading/saving and other overhead; that is not a measured wall-time multiplier. Existing actual P12 timings may inform planning without another probe. For illustration only, a20–40s comparable frozen pass suggests about4–9min forward/backward-equivalent work plus overhead; a≥90s pass already consumes about19.5min before overhead and makes the20min chain unattractive. Actual training memory/throughput remain unknown.

**Not worth doing tonight if any applies:**

1. P12 is not already a stable, bound native implementation, requires a second backend/library, or the remaining change exceeds the65–135owner-minute planning envelope.
2. Actual P12/E14 and exploration leave no decision-relevant complementary signal relative to the already available quality/latency alternatives. This is night-queue triage, not evidence that adaptation could never help.
3. Existing timing/resource information cannot support the20min chain conservatively, the unchanged1500TRAIN schedule cannot be admitted/tokenized completely, or strict native export/reload is uncertain within the bound. Do not buy clarity with an ungranted probe.
4. Preparation, one bounded chain and independent scoring cannot finish before the night cutoff without displacing already authorized work; or usefulness would depend on reopening sealed confirmation/candidate selection.

**Current disposition: proposal delivered, no implementation/learning/download/spend or candidate authority.** Evidence: `artifacts/research/r12-20261112T023205Z/native-reuse.md` and final review/build/handoff receipts. R12 began02:32:05UTC with02:52:05cap; fixed foreground availability remains through08:30:36UTC independently of this proposal.
