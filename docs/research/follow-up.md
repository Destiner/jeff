# Follow-up: pilot question truncation and tiny-score regression

After the early backbone recommendation, Research inspected the active implementation boundary, audited actual tokenizer budgets, and decomposed the first published validation regression. No training, model inference, large-weight download, paid work, tests, or linting was performed by Research. Production fixes remain with Model.

## Action now

**Use `--max-length 256` for the approved all-MiniLM pilot, including its untouched baseline.** The measured 128-token preprocessing policy removes question tokens from **12/20 rule-validation decisions**; 256 fits every published pilot pair. This is an existing CLI setting, not an architecture/dependency change, and does not require delaying implementation.

Keep the completed all-MiniLM learning/save/reload loop. Do not select a new architecture from three tiny validation cases. Run the pilot from the same pretrained base plus fresh head as Model intends; preserve the tiny run as plumbing evidence only. If the full pilot remains near-uniform or repeats semantic errors after the token-budget correction, compare the recommended cross-encoder's retained pretrained scoring path on the exact same validation inputs before pursuing the decoder.

Two cheap observations explain what the tiny result does and does not mean:

- Its entire 6-train/3-validation dataset fits under the current 128-token pair cap; **truncation is not an explanation of these three errors**.
- Predictions are close to uniform before and after six optimizer steps. The 1/3 → 0/3 drop is one low-margin intent flip, not demonstrated catastrophic loss of a previously capable classifier. All three targets lose a little probability, so log loss genuinely worsens too. The cause of that drift is not identified by these observations.

## Measured here: saved-prediction failure decomposition

Inputs: published `data-tiny-v1/validation.jsonl` and Model's `tiny-20261111-01/{baseline,trained}-predictions.jsonl`. Both have complete 3/3 ID/option coverage. All labels remain teacher labels; this is **teacher agreement**, not independently verified correctness.

Research independently recomputed arithmetic on the saved probabilities using `experiments/research/inspect_validation_delta.py` (no model execution):

| Validation case | Target probability, before → after | Top choice before → after | Change in log loss |
| --- | --- | --- | ---: |
| Intent: rescheduling | 0.341829 → 0.338248 | correct → incorrect | +0.010532 |
| Sentiment: neutral description | 0.333210 → 0.330680 | incorrect → incorrect | +0.007622 |
| Rule: smoke takes priority | 0.326914 → 0.326287 | incorrect → incorrect | +0.001922 |
| Mean / total | Agreement **1/3 → 0/3** | Loss **1.096828 → 1.103520** | **+0.006692** |

Uniform three-choice log loss is `log(3) = 1.098612`. The baseline is only ~0.001784 better and the trained model ~0.004908 worse. Across all three distributions, the largest absolute deviation of any probability from 1/3 is 0.013040 before and 0.010083 after. The intent winner changes with an after-training top-two margin of just **0.000254**. No exact tie occurred in that case; this is a genuine but very small ranking change.

Do not infer calibration, statistical significance, overfitting, or a specific optimizer defect from three examples / six updates. In particular, the random-head baseline's one correct answer does not establish useful zero-shot decision ability. No independently held-out claim is made for any future change selected after this inspection.

Artifact: `/Users/destiner/Code/jeff/artifacts/research/validation-delta-20261111T1034/tiny-validation-delta.json`. It records complete per-example probabilities-of-target, margins, log losses, input hashes and script hash; no final-evaluation content was read.

## Measured here: token-budget audit rules out one suspected cause

The current scorer uses `(State: … Question: …, Candidate: …)` with right `longest_first` truncation. Research fetched only the **462,948-character tokenizer JSON**, pinned to the same all-MiniLM revision Model used: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`. The read-only CPU audit used `tokenizers==0.22.2`, without importing torch or loading weights.

| Dataset | Decisions | Candidate pairs | Full token length min / p50 / p95 / max | Overflow at caps 128 / 256 / 512 |
| --- | ---: | ---: | --- | --- |
| `data-tiny-v1` (6 train + 3 validation) | 9 | 25 | 36 / 40 / 59 / 59 | 0 / 0 / 0 |
| `data-pilot-v1` (300 train + 60 validation) | 360 | 1,412 | 41 / 62 / 114 / 169 | **45 / 0 / 0** |

The tiny data loses no question/candidate tokens at any cap. In the full pilot, all **45** over-budget pairs at 128 lose **1–11 question tokens**, affecting **12 unique validation/rule_application decisions**: 60% of the 20 rule-validation rows and 20% of all 60 validation rows. No train pairs overflow, and no candidate text is lost. At 256 and 512 every pilot pair fits and no question/candidate tokens are lost. This is exact tokenizer measurement, not a characters-to-tokens estimate or a model-accuracy result. Repeated budgets reuse the same data and do not increase the independent sample count.

**Concrete cause:** the question is at the end of the first sequence, so right truncation removes it before much of a long state. `longest_first` only considers sequence lengths, not semantic fields. The tokenizer's [v0.22.2 truncation source](https://github.com/huggingface/tokenizers/blob/v0.22.2/tokenizers/src/utils/truncation.rs) establishes the strategy; the current format and the actual affected-pair audit establish its impact. Because only rule validation is affected here, the policy also creates a train/validation preprocessing difference that could masquerade as weak rule generalization. We have **not** measured how much it changes model scores.

**Immediate fix proposal to Model:** use the existing `--max-length 256` for fresh pilot initialization, its baseline, training and checkpoint metadata; no need for 512. All pairs have at most 169 tokens. Do not change only inference length after training and call that an equivalent baseline comparison. The finding was published immediately in the shared `20261111T103800Z-pilot-question-truncation.md` handoff; Research did not change Model code or run the pilot.

For future longer inputs, reserve complete question/choice tokens and pair special tokens before budgeting state, and report affected IDs. Merely switching to `only_first` still permits losing a question at the end of the first sequence. A removed state rule or exception can invalidate the label; state truncation is not automatically safe.

Artifacts: `/Users/destiner/Code/jeff/artifacts/research/tokenizer-audit-20261111T1029/{tiny,pilot}-token-budget.json`. Tokenizer SHA256 `be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037`; pilot manifest SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`. Full executed commands are in [the experiment notes](../../experiments/research/README.md).

## Source finding: adopting the recommended head is not a model-ID-only change

At inspection, the approved pilot loads `AutoModel`, mean-pools token representations, creates a new linear scalar head, and explicitly resets that head before training. This is an honest implementation of the approved **embedding backbone + random head** pilot. Its trainer correctly computes external grouped cross-entropy and its scorer pads absent choices with negative infinity.

Changing only `--model-id` to `cross-encoder/ms-marco-MiniLM-L6-v2` would **not** preserve the advertised pretrained ranking baseline: the current path discards the classifier and changes the pooling/scoring path. A later comparison must use `AutoModelForSequenceClassification`, retain its BERT pooled-output/classifier weights, avoid head reset, and record/save/reload that architecture explicitly. Keep the old checkpoint valid rather than silently changing its format.

A second upstream trap applies to that later path: in [Transformers v4.48.3 `BertForSequenceClassification.forward`](https://github.com/huggingface/transformers/blob/v4.48.3/src/transformers/models/bert/modeling_bert.py), `num_labels == 1` selects regression and `MSELoss` when `labels` are passed and problem type is unset. That does not implement choosing one option among 2–6. Use raw candidate logits without built-in labels, group by example, and compute choice CE outside the backbone. Overriding to single-label classification with one class also does not create a choice axis. This is **source-confirmed library behavior**, not a reproduced current training bug.

### Draft integration mismatch: resolved, not an outstanding blocker

Research's 10:30 source snapshot found `.encoder` in the inference subagent and `.backbone` in the training subagent. The snapshots were uncommitted and actively changing; the finding was promptly published in the shared handoff. Model's integrated scorer now exposes a read-only `backbone` property returning `encoder`, and Model reports fixing the mismatch before the first run. Research confirmed the property in the integrated source. Do not count this as an executed training failure or imply Research made the production fix.

## Reported by Model: useful local compatibility evidence, not a cross-encoder benchmark

Source: `/Users/destiner/Code/jeff/artifacts/handoffs/model/20261111-1043-tiny-loop-ready.md` and the linked `tiny-20261111-01/run.json`. These figures were **reported by Model**, not remeasured by Research:

- Apple M5 with 24 GiB; torch 2.15.0 MPS, Transformers 4.57.6, no CPU fallback enabled.
- all-MiniLM backbone + new head, 6 optimizer steps / 12 presentations; full-backbone and head weights changed.
- 20.680 seconds including initialization/download/checkpoints, **not pure training throughput**.
- Process lifetime maximum RSS 767,492,096 bytes; end-point MPS current allocation 362,869,760 and driver allocation 1,178,599,424 bytes. **Neither MPS number is a peak; do not add these overlapping accounting measures or call them dedicated VRAM.**
- Saved baseline and trained checkpoints each reloaded in a separate offline process with an empty cache and produced all 3 predictions.

This supports the feasibility of a small BERT-family encoder on this machine. It does not establish the recommended cross-encoder's actual compatibility/quality, a 16 GB fit at larger batches, or the decoder's performance. The independent arithmetic above agrees with Model's reported quality degradation.

## Decoder bottleneck to avoid if the fallback is activated

Qwen's vocabulary has 151,936 entries. Full `[batch, sequence, vocabulary]` projection at batch 1, length 512 occupies **296.75 MiB FP32** (148.375 MiB in two-byte precision), before loss intermediates. These are tensor-size calculations, not measured peaks. Masking prompt labels after projection does not avoid this tensor.

[Transformers v4.48.3 Qwen2 source](https://github.com/huggingface/transformers/blob/v4.48.3/src/transformers/models/qwen2/modeling_qwen2.py) projects `hidden_states[:, -num_logits_to_keep:, :]` through `lm_head`; zero means all positions. Newer versions may call the parameter `logits_to_keep`: inspect the **installed** signature instead of copying a version-mismatched argument.

For verified single-token A–F continuations, a prompt ending at the assistant boundary needs only the last prompt position's logits and external CE over the allowed token columns. Use one unpadded example initially, or select each row's actual last non-padding position. No built-in full-sequence labels or training KV cache is needed. Verify exact chat-boundary tokenization; multi-token answers require correctly aligned continuation scoring and cannot be approximated by one arbitrary first token. Record logits shape/dtype and memory during Model's first actual step, not an independent research run.

## Completion and limitations

Research scripts executed successfully on published non-final data. `uv build --no-sources --out-dir /Users/destiner/Code/jeff/artifacts/research/build-20261111T1034` produced the shared scaffold's wheel and source distribution; this is packaging evidence, not model execution or verification of production changes in another worktree. No software tests or linters were written/run. No root dependencies, contracts, datasets or production files were modified. Additional spend: £0 actual / £0 pending. The full pilot comparison and any decoder experiment remain proposed Model-owned work, not completed research runs.
