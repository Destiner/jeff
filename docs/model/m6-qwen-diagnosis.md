# M6: bounded source and optimizer-receipt diagnosis

## Finding

**No concrete implementation defect was found in the scoped Python objective/autograd/update path.** The authorized recipe executed as recorded; the negative TRAIN fit and P4/E6 candidate remain unchanged. Source inspection does not prove native MPS numerical correctness or identify why useful discrimination was lost. No corrective patch or additional learning run is justified by this review alone.

Lead authorized a15–20minute CPU/source-only follow-up after [M6's negative result](m6-qwen-results.md). Two fresh narrow reviewers inspected executed source/library paths and actual optimization logs. There were **no model/tokenizer/weight loads, new inference/training, tests/lint or input/reference/final-case inspections**. Data D5 separately owns schedule/target/exposure-order and retained-fit probability identifiability; Model did not duplicate that diagnosis. P4 and the separately authorized R6 job proceeded independently without a review gate.

## Intended versus executed mechanics

Executed revision `dafd5d235b53af341fbf539e4bf32dcf09a399f2`; the two training-module hashes match the receipt. The reviewer read executed P3 rendering via Git, rather than assuming the subsequently amended Runtime module was identical. Recorded/installed metadata agrees on Torch2.15.0 and Transformers4.57.6, but the installed library binaries/source were not cryptographically pinned by the run receipt.

| Check | Evidence-supported finding |
| --- | --- |
| Assistant boundary and loss | Executed P3 `prepare` requires one distinct answer token after an identical prompt prefix. `qwen_decision.py:156–166` selects allowed last-token logits then CE. Qwen2 projects only the last hidden state (`modeling_qwen2.py:460–467`); its LM loss needs `labels`, which is never passed. No full-vocabulary denominator, shifted-label loss or prompt-token loss is added. |
| Gradient connection | Tensor indexing and `.float()` retain autograd. `.item()` is used for checks/logging, not as the backward loss. Mean-reduction CE on one target is one decision loss. |
| Accumulation / clipping / zeroing | Each of four rows contributes loss/4; one global L2 clip1 precedes one step, followed by `zero_grad(set_to_none=True)` (`qwen_decision.py:338–361`).1500divides exactly into375groups. No double averaging, per-row clip, premature zeroing, remainder or scheduler was found. |
| Tied input/output table | Original config enables tying; HF shares the parameter, and `model.parameters()` deduplicates it.290tensors/494032768parameters support one shared table, not duplicate optimization. Input-embedding and selected-output gradient routes combine before one update. Unselected output logits have no direct choice-CE gradient, but shared rows can receive input-route gradients and decay. |
| AdamW | `foreach=False` selects non-fused single-tensor Adam; decoupled decay, clipped-gradient moments, bias correction and epsilon follow installed AdamW source. The single parameter group also decays biases/norm weights/shared table: intended actual behavior, not a demonstrated defect. Final290states are atstep375; all three sampled fingerprints changed. |
| Fit / train mode | Scoped no-grad restores gradient mode; the trainer explicitly re-enters train mode. No inference-mode tensors are reused. Qwen has RMSNorm rather than running-stat normalization and configured attention dropout0. |

Global clipping bounds the accumulated gradient norm; it is not a direct bound on AdamW's parameter displacement or a guarantee of retained pretrained behavior. This follows from adaptive moment normalization, not from a measured causal explanation of M6.

Library source citations and exact qualifications are preserved in `artifacts/model/m6-diagnosis-20261111-01/source-review.md`. The trace cannot validate the actual native MPS SDPA/backward kernel. FP32 parameter/buffer checks override the base BF16 preference; HF passes causal attention, explicit scale and zero dropout to SDPA. There is **no evidence here supporting a backend-bug claim**.

## Actual online trajectory

These are retrospective contiguous log-order summaries, not a new outcome criterion. All1,500 online losses are finite; overall mean1.400338, median1.355179, populationSD.596858. Range.006389–13.505731; the maximum occurs at presentation8/update2 and remains included in every reported result. There are24losses>3, five>4 and one>5.

| Presentations | Online mean CE | Population SD | Losses >3 |
| --- | ---: | ---: | ---: |
|1–250|1.475757|1.1259|13|
|251–500|1.451593|.6619|9|
|501–750|1.377753|.3906|1|
|751–1000|1.348144|.2872|0|
|1001–1250|1.398505|.2992|0|
|1251–1500|1.350275|.3051|1|

Loss dispersion contracts and the mean declines modestly, nonmonotonically. This **does not establish improved fixed-snapshot fit**: each loss is measured under changing weights before later updates. The independent before/after fit remains805→431/1500 and CE1.357724→1.390592.

All15retained preclip-norm samples (one every25updates) exceed1, range14.349–164.572, so those sampled updates were clipped. The largest sampled norm is atupdate75, not the largest loss atpresentation8. Values for the other360updates, postclip norms, gradient directions and per-parameter norm trajectories were not retained. Completion supports finite/positive checks at every clip, not reconstruction of missing values or an all-update clipping rate.

Actual recorded TRAIN phase totals are approximately114.23s forward,292.12s backward,20.65s clipping and124.04s optimizer. From initial forward to completed375updates is about551.83s;100-presentation intervals take33.3–40.7s. Later intervals slow somewhat without a late loss explosion. Observed allocation/headroom and CPU lifetimeRSS do not identify thermal throttling, swapping or resource stress as a cause. Memory samples are not peaks or additive quantities.

Full100-row windows and sampled norms are in `artifacts/model/m6-diagnosis-20261111-01/timeline-review.md`, derived only from `online.jsonl`, `train.stdout`, `events.jsonl` and selected completed-receipt fields.

## What remains identifiable—and what does not

- Full-parameter adaptation can change representations and the shared readout, so optimization-induced loss of useful discrimination is plausible. Source establishes the pathways, **not which pathway caused the observed failure**.
- All final TRAIN argmax indices are0. Saved fit rows do not contain full probability/logit vectors or tie counts. Approximate target probability can be recovered from CE, but a target probability near1/K alone does not determine every other probability or establish a strict first-position preference. Data D5 owns that retained-artifact assessment; E6 owns complete development-vector/tie analysis.
- Sparse fingerprints and scalar losses cannot locate when or in which layer discrimination was lost. Native gradient correctness and counterfactual recipes were not tested. No new instrumentation run or weight inspection was authorized here.
- No schedule/label repair, LR/epoch/prompt change, temperature fallback, optimizer amendment or automatic rerun follows. A demonstrated future defect would require a new reviewed revision; historical code/receipts/checkpoints remain immutable and a new learning run still needs explicit authorization.

## Independent D5 clarification from retained TRAIN evidence

Data's separately bounded D5 report (`artifacts/data/d5-20261111T161610Z/`) subsequently found zero identity/permutation/target-remapping mismatches across all1500TRAIN rows and9pinned shards. The actual seed42 schedule is interleaved:375four-row updates,500rows/family, maximum family runs6/7/7;20/191/164updates contain1/2/3families. These facts reject a demonstrated remapping defect or whole-family-block schedule, not every ordering effect. Model did not repeat D5's audit or reopen the completed run.

D5's uniform reference is meanCE1.322382806 and expected random agreement404.1167/1500; deterministic first-tie agreement431/1500 is a different quantity. Final CE1.390592028 is worse than uniform, including within each family. Under the recorded unsmoothed-CE interpretation, **all1500final rows differ from ln(K) by more than.01nat**: this contradicts exact uniformity, despite the first-position argmax agreement equaling the first-tie baseline.

Target probability alone conditionally establishes at least140strict winners:139correct targets have derived probability>.5, and the sole binary row identifies a strict wrong first-position winner by complement. Full tiedness for the other1360rows remains unresolved; no full vector, Brier, entropy, margins or exact TRAIN tie count is retroactively reconstructed. Narrow position-conditioned target-score ranges across distinct inputs are not a common pooled probability vector or proof that input is ignored. Exact fit/receipt/schedule hashes and the binary derivation are in D5's fit/order/schedule reports and `binary-identifiability-addendum.json`. These are additional retained-artifact findings, not an extension of Model's source-review or Data's observation window.

E6 subsequently joined actual development inputs with all624trained probability vectors: every choice is input position0 with no ties and positive top-two margins.102494–.456558. This independently establishes a strict development first-position collapse, not flat/uniform development scores; it must not be substituted for missing full TRAIN vectors or its remaining1360unknown tie statuses. E6 still does not identify a causal implementation or optimization mechanism.

£0additionalactual/pending/allocation. This diagnosis is evidence about executed mechanics and limits, not a cosmetic repair of the negative E6 comparison or a general rejection of supervised decoders.
