# R5 evidence and experiment rationale

Companion to the [decision memo](../../docs/research/learning-strategies.md), researched2026-11-11. **The memo selects exactly one primary experiment and one contingent alternative.** The independent strands' candidate menus are research inputs, not additional instructions or experiments. None ran a model, authored a dataset or changed a frozen recipe.

## Evidence hierarchy and provenance

1. Jeff's published, versioned aggregate results determine the local problem: [E4/M5](../../docs/evaluation/e4-m5-lr-control.md), [D3](../../docs/evaluation/e4-d3-seen-rules.md), [E5](../../docs/evaluation/e5-frozen-decoder.md), [P3 runtime](../../docs/runtime/p3-frozen-challenger.md). These are **measurements attributed to their owners**, not fresh Research scoring.
2. Original papers/official technical documents support the method distinctions below. Three independent bounded strands read method/result/limitation passages, not only abstracts. Their exact quotations, locators, scales, counterevidence and failed/irrelevant retrievals are retained under the shared artifact root.
3. Proposed thresholds, resource caps, training choices and costs are **engineering judgments**. Published effect sizes are not Jeff predictions. No prior literature proves the cause of our regressions or the efficacy of our next recipe.

Artifact root: `/Users/destiner/Code/jeff/artifacts/research/r5-20261111T144821Z/`:

- `decision/{findings.md,source-ledger.json}`: five papers plus two official implementation READMEs, approximately14:48–14:56UTC.
- `composition/{findings.md,source-ledger.json}`: five papers, including negative findings and split/scale limitations.
- `probability/{findings.md,source-ledger.json}`: five papers, one overlapping the decision strand; proper scores, calibration, selection and order semantics.
- `jev-sources.md`: owner-read public Jev/analogue evidence and exact retrieved passage locators.
- `evidence-log.md`: append-only operational coverage; final review/build/integration evidence is colocated.

Thus the three strands cover **14 distinct research papers**, not15 independent confirmations. They returned before the new E4/E5 aggregates; their “outcomes unknown” language is historical and superseded by the owner memo. No raw probe/final cases or diagnostic-derived training examples were requested or shared. A later D4 TRAIN-only audit is a bounded consistency observation, not whole-release certification.

## Public Jev evidence

### J1 — official TypeSafe material: disclosed interface, undisclosed reproducible training

- [Introduction](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [models](https://docs.typesafe.ai/models).
- The company describes a specialized architecture, parallel sampler and **Reinforcement Learning for Calibrated Decisions (RLCD)**. The primer says it “trains Jev to return decisions and calibrated probabilities instead of generated text.” These are vendor descriptions, not a released loss equation, data recipe, optimizer, weights or independent demonstration of calibration.
- The blog distinguishes guaranteed output/schema matching from empirical capability claims; its workflow references are averages of other models, not independently known correct probabilities. The phrase “can't hallucinate” must not become a claim that a type-valid decision cannot be factually wrong.
- Public details inspected here do **not** justify reconstructing RLCD, buying teacher access or asserting reinforcement learning is necessary. No Jev API was called, weight loaded, or price/capability claim independently reproduced.
- [Hugging Face's decision-model overview](https://huggingface.co/blog/decision) illustrates a shared typed interface and a toy choice-CE training example. It is explanatory documentation, not controlled evidence for sample efficiency or a reason to migrate Jeff's pinned Transformers stack. Its model names/code were not adopted or executed.

### J2 — *LLMs Are Already Jev-Style Decision Models—When and How to Fine-Tune Them*

[Li & Wagle, arXiv2610.02076v2](https://arxiv.org/html/2610.02076v2), a public preprint, not local evidence.

- **Method:** bracketed numeric candidate suffixes, joint candidate prompting, suffix likelihood/tree-factorized listwise loss, full tuning or LoRA, shuffled option order. Auxiliary KL anchors preserve non-choice/text-generation behavior; single epoch. Our A–F one-token choice CE is a simpler related interface, **not** reproduction of the suffix-tree method.
- **Scale:** Qwen3.5-4B and Qwen3-0.6B. Main data configurations range9k–95,461 examples, with12k/375-step Reason+Long; a3,000-example/100-step arm is4B-only. AppendixB reports four A10080GB GPUs for most training; Reason-9k takes11minutes for0.6B on that setup. This does not predict Apple MPS training time or memory. Public human/source labels differ from Jeff's mostly teacher-authored1,500 decisions.
- **Positive:** §4.3.4 reports smaller-model benefits in decision format/calibration/high-cardinality tasks; targeted adaptation is plausible at roughly our model scale. §3.3 states candidates are randomly shuffled during training; consistency improvements are reported on multimodal rotations, not a controlled Jeff-specific permutation effect.
- **Counterevidence:** §4.3.2 reports4B JevBench accuracy81.4% frozen→77.5% at100steps→74.9% after intent-only training, even while in-distribution loss decreases. More short-context data can worsen long-context performance. §4.4 shows generation behavior can deteriorate despite reasonable decision scores. Its early collapse run also changed LR/warmup/batch, so missing anchors alone is not an established cause.
- **Leakage/selection limitation:** §3.5 explicitly says later data mixtures were motivated by public JevBench error analysis and treats the relevant evaluation as exploratory, even though examples were excluded and hyperparameters/checkpoints were not selected on that set. We do not copy its case-driven data process into Jeff's protected diagnostic boundary.
- **Use:** motivation for a narrowly declared choice-learning comparison, with strong negative-transfer caveats. Not proof our old Qwen2.5 variant will learn from a much smaller mixture. The paper's word “calibrated” does not certify Jeff.

### J3 — *Releasing the Inner Jev: A Simple Recipe for Open Decision Models*

[arXiv2610.17205](https://arxiv.org/html/2610.17205), another public preprint. Its released models named “Jeff” are **not this repository's artifacts**.

- **Method/scale (§4):** pretrained answer-letter readout plus zero-initialized affine correction; rank32 LoRA on attention/MLP projections, choice CE against hard or soft targets, shuffled options;4B–31B models. Pool417,825 questions, about76k presentations/400steps, approximately190 questions/step.31B training takes78minutes on four H200s; even4B takes23minutes on that hardware. This is not a1,500-example laptop recipe.
- **Ablation (§5.4/Table5):** on31B, head-only scores78.9 versus79.6 calibrated frozen, while LoRA with the original head frozen scores84.9 versus84.4 jointly trained. Hard instead of soft labels gives84.1, a difference within the reported uncertainty. Useful contrary evidence to claiming a new head or paid soft targets are essential; one-seed variants and an outcome-selected recipe limit causality.
- **Scale counterexample (§5.2):** the same recipe fails to improve4B (63.0 versus63.6); gains require three additional changes, including teacher-target mixing and format changes.12B's reported change (−0.4±1.8) is within noise. Do not export31B's headline to0.5B or22M.
- **Evaluation/selection caveats (§§4–5):** authors used OpenDecisions to select the recipe, report the better of original/recalibrated competitor outputs based on that score, and restrict fitted temperatures to≥1 after observing harmful sharpening there. Separate public evaluation sets are reported, but the principal score is not untouched. Their leaderboard submission also moves binary probabilities out of an abstention interval; **that score-specific adjustment is not a probability-reliability recipe to copy**.
- **Use:** simple supervised choice learning is a credible alternative to proprietary RLCD. This source does not establish that its teacher soft labels are genuine option logits from the passages inspected, nor that soft targets materially help our regime. No code/weights/dataset downloaded or run.

## Decision learning: strongest support and important gaps

| Source / relevant passage | What is supported | What is not |
| --- | --- | --- |
| [Hinton et al.,2015](https://arxiv.org/html/1503.02531), §§1–3; decisionS1/probabilityS5 | Actual softened teacher class vectors can convey alternatives; match temperatures and account for T² when mixing with hard CE. Centered-logit matching is a high-T special case. | Generated verbal confidence is not that vector; fixed-class MNIST60k and speech~700M frames do not establish gains on1,500 changing-choice language decisions. Weak teachers propagate errors. |
| [Hsieh et al.,2023](https://arxiv.org/html/2305.02301), §§3.2,4.4; decisionS2 | Separate label/rationale-generation multitask training can improve data efficiency. Official [implementation](https://raw.githubusercontent.com/google-research/distilling-step-by-step/main/README.md) confirms separate losses. | T5 students220M+ and PaLM540B are far from22M scalar scoring. Rationale generation is needed during training, **not necessarily deployment**. Putting oracle rationale in training input and removing it at inference is not this method. Naive rationale+label concatenation can hurt. |
| [Robinson et al.,2023](https://arxiv.org/html/2210.12353), §§3–5; decisionS3 | Allowed answer-symbol scores are a plausible decoder readout; symbol binding and order consistency are model-dependent. | Symbols are a **proxy** for correctness probability; invariance does not imply accuracy. Main studied models are1.5B–178B, not0.5B. |
| [Wei et al.,2021/22](https://arxiv.org/html/2109.01652), §4.2; [Longpre et al.,2023](https://arxiv.org/html/2301.13688), §§3.3,3.5; decisionS4–S5 | Instruction-transfer benefits depend on scale, mixture and recipe. Early FLAN has negative≤8B results; later Flan Collection has smaller-T5 gains and mixture-weighting effects. | No universal8B minimum, no proof that formatting instructions creates capability, no validation of equal weighting of Jeff's heterogeneous group IDs. Most later method ablations use3B T5. |

**Mathematical distinction:** Jeff already trains `−log softmax(s)[target]`. Instructions describe inputs/training distribution; they are not a competing probability objective. For a decoder, `−log P_vocab(answer_symbol)` additionally optimizes the probability mass on allowed symbols; choice-normalized CE does not. Choosing CE over allowed symbols is intentional for a non-generative API, not evidence that unrestricted text generation remains intact.

## Rules: fit, policy transfer, composition, algorithms

These are distinct claims: fitting presented training mechanisms; applying a familiar mechanism to a new policy; composing known primitives in unseen structures; executing a genuinely new algorithm. D3 measures the second. Neither new policy constants nor a fresh mechanism name certify the third/fourth.

- [Lake & Baroni,2018/SCAN](https://proceedings.mlr.press/v80/lake18a.html), compositionS1: >99.5% training fit can coexist with very poor held-out jump/length transfer. Synthetic non-pretrained recurrent generation differs from Jeff; even SCAN primitives have very different transfer outcomes.
- [Keysers et al.,2020/CFQ](https://arxiv.org/html/1912.09713), compositionS2: compound-divergence splits while controlling atoms expose a large random-split/generalization gap. This requires derivation structure; Jeff's group labels are not automatic atom/compound annotations.
- [Andreas,2020/GECA](https://aclanthology.org/2020.acl-main.676/), compositionS3: controlled shared-environment fragment substitution can help low-resource composition. Counterexamples include ill-typed outputs, no Scholar improvement, and synthesis of5%/1% of evaluation examples in two SCAN settings despite train-only generation. Do not interpret arbitrary paraphrasing or blindly retained labels as equivalent.
- [Nye et al.,2021](https://arxiv.org/html/2112.00114), compositionS4: intermediate-state generation helps bounded addition extrapolation with100k examples; low-data MBPP scratchpads give~5% versus~10% direct accuracy. Task traces require computation at inference. An encoder auxiliary-state task would be a new hypothesis, not reproduction of scratchpads.
- [Zaremba & Sutskever,2014](https://arxiv.org/html/1410.4615), compositionS5: mixed/combined curricula retain hard cases; naive easy-to-hard can underperform baseline. Reported digit accuracy is teacher-forced, not autonomous full-program output correctness.

**Deferred data principle:** if assigned later, choose mechanisms/policies from TRAIN metadata/fit only, split policy roots before variants, independently recompute labels after semantic changes, include reachable distractors and varied active branches. Hold presentation budgets explicit. Do not mine D3/probe failures or claim repeated views are new sources. A rational next data choice depends on train fit and label quality, which aggregate development failure alone does not resolve.

## Probability quality and action

- [Gneiting & Raftery,2007](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf), probabilityS1, §3.1: logarithmic and quadratic/Brier scores are strictly proper in expectation for categorical outcomes. Top-1 does not identify the whole probability distribution. Proper objectives do not guarantee optimization, calibration, valid target labels or representative assessment.
- [Guo et al.,2017](https://proceedings.mlr.press/v70/guo17a.html), probabilityS2, §§4–5: one positive temperature often helps fixed-label, matched-distribution classification; Reuters does not improve. Their calibration sets are roughly872–25,000 examples. The proposed source-cross-fitting and bounded search are **our design**, not their tiny-data guarantee.
- [Zheng et al.,2024](https://arxiv.org/html/2309.03882), probabilityS3: answer-ID token and position biases across20LLMs/three benchmarks; ID removal often hurts. This motivates measurement, not changing P3's frozen prompt or claiming a Qwen0.5B effect from7B+ models.
- [Geifman & El-Yaniv,2017](https://proceedings.neurips.cc/paper_files/paper/2017/file/4a8423d5e91fda00bb7e46540e2b0cf1-Paper.pdf), probabilityS4: risk–coverage selection requires IID labels and threshold-selection controls; their calibration sets use thousands of examples. Twelve reused correlated groups cannot support transferring a risk certificate.

**Architectural deductions, not new measurements:** deterministic independent candidate scores are permutation-equivariant, yet adding an option changes every denominator and duplicate meanings can split mass. Joint decoder prompts permit comparing alternatives but introduce order/symbol effects. Allowed-token normalization conditions on the allowed-symbol event, not truth. Positive temperature preserves each decision's ranking; it need not preserve maximum-confidence ordering **between** different multiclass decisions. Abstention is an action requiring costs/coverage semantics, not an automatically discovered “none of the above.”

## Cost, scope and reproducibility

The primary proposal's494M×16-byte model-state estimate includes weights, gradients and two FP32 Adam moments, **not** activations/extra copies/peak unified memory. Runtime's inference measurements cannot fill that gap. Full tuning is proposed to avoid assuming an installed adapter stack; it is not claimed superior to LoRA. A fixed45-minute slot is a resource cap subject to Model, not a performance estimate. The contingent scalar fit uses saved probabilities and needs no ML slot; no calibrated deployment artifact is authorized.

R5 performed literature/source review and aggregate synthesis only. No model operations, new labels, dependency installations, paid API/compute, protected-final access, software tests or linting. Source-review ledgers preserve scope gaps and discarded guesses instead of presenting every retrieval as evidence. Package builds verify integration only; they do not validate the proposed learning effect. Actual session timing, peer receipts, focused review and merge hash are in the final Research handoff, not fabricated as measured research benefit.
