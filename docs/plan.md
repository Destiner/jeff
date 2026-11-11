# Plan and decisions

## Objective

Train a small, Jev-like text decision model during a two-day internal hackathon. The model itself is the achievement; product applications are secondary.

The developer knows LLM and coding-agent fundamentals but has not trained a model before. Explain consequential ML choices plainly and preserve their rationale.

## Agreed direction

| Area | Decision |
| --- | --- |
| Starting point | Fine-tune pretrained weights; no language pretraining from scratch. |
| Tooling | Python 3.12 with uv and Hatchling packaging. Optional `model` dependencies: PyTorch, Transformers, safetensors. Data/evaluation need no third-party runtime dependencies initially. |
| Software checks | No software tests, test runners, or linting. Build and execute the actual pipeline; keep model evaluation and dataset validation. |
| Interface | Context + question + caller-supplied choices → probabilities over those choices. |
| Initial output | Single-choice classification; yes/no is a two-choice case. Defer richer scoring and generated explanations. |
| Scope | Train across several task families, aiming for generalization rather than a single fixed label set. |
| Data | Use strong-model-generated examples and labels, supplemented by suitable existing datasets. Inheriting some teacher mistakes and biases is acceptable. |
| Hardware | Apple silicon, 16–24 GB unified memory. Exact chip and memory capacity remain to be confirmed. |
| Deployment | Prefer local training and local inference. Cloud training is an optional fallback. |
| Budget | At most £50 additional spend across teacher calls and rented compute, beyond existing access. This is a ceiling, not a target. |
| Collaboration | Swarm-first from the outset, with isolated workspaces and stable contracts. |
| Priority | Working checkpoint on day one; model improvement and evaluation on day two. UI is optional. |

This borrows the decision-model interface and purpose, not Jev's proprietary architecture or training algorithm. Do not claim equivalent capabilities or calibration.

## First technical decisions

Resolve these with a small pilot rather than a lengthy architecture exercise:

1. **Backbone and training approach.** Initial pilot approved: `sentence-transformers/all-MiniLM-L6-v2` (roughly 22M parameters), loaded through Transformers with a shared scalar candidate head and full fine-tuning. This is smaller than the original 100–300M suggestion to prove the loop sooner. The Model worker must record the exact model revision and actual backend behavior. Larger encoders or small decoders remain later candidates, not parallel mandatory builds.
2. **Trainable parameters.** Try full fine-tuning for the small initial backbone, subject to measured memory use. Consider head-only or adapter alternatives if that reveals a concrete need.

   **Pilot input-budget decision (LD002):** the next controlled baseline/trained comparison uses 256 tokens rather than 128. A reproduced tokenizer audit found that 128 removed question tokens from 45 candidate pairs in 12 rule-validation decisions; every pilot pair fits at 256. This fixes a measured input-loss problem, not a demonstrated accuracy problem. Keep the current architecture until the corrected comparison is available; the retained-head cross-encoder recommendation remains an unmeasured alternative.
3. **Contracts.** Follow [the v0.1 contracts](contracts.md) for training examples, predictions, and artifacts. Propose changes through the integrator.
4. **Task mix and splits.** Choose a small initial mix and reserve validation and final-test groups before producing variants.
5. **Teacher access and cost.** Check existing access, model terms, and pilot costs before expanding generation. Do not assume existing subscriptions provide programmatic API access.

Verify Apple GPU backend compatibility, model licensing, inference packaging, peak memory, and measured training speed before adopting a stack.

## Day one: a complete learning loop

1. Freeze the minimal contracts and choose initial task families.
2. Establish the strongest practical untrained baseline using the starting model where comparable.
3. Build a small, checked dataset and run training immediately.
4. Save weights and all configuration needed to reproduce inference.
5. Reload in a fresh process and run held-out evaluation.
6. Expand data and experiments only after this loop works.

### Checkpoint acceptance

- Weights were actually updated through training.
- A saved artifact can be loaded outside the training process.
- New context, questions, and choice descriptions produce valid probabilities.
- A report compares the trained model with the baseline on the same held-out examples, including failures.
- Dataset version, base-model revision, training configuration, and artifact locations are recorded.
- Any external training or inference dependencies are explicit.

The first checkpoint may be weak. Preserve it as a working reference.

## Day two: measurable improvement

Use validation failures to guide new data and controlled experiments. Investigate accuracy, unfamiliar task families, option-order sensitivity, ambiguity, confidence reliability, latency, and memory.

Keep successful checkpoints and compare every candidate against the current reference. A simple demo is useful only if it does not displace core model work.

## Training mental model

A pretrained backbone supplies language representations. Our decision model scores the supplied choices. Supervised training compares predictions with target answers, computes a loss, and adjusts trainable weights through backpropagation.

Cross-entropy is a reasonable initial objective. Strong-model labels make this a form of distillation. Reinforcement learning is not required for the initial model.

A candidate scorer is a proposal, not a guarantee of generalization. Merely accepting arbitrary option text does not prove the model understands unfamiliar tasks.

## Data and evaluation

- Start with a few families such as intent selection, passage-based questions, and applying supplied rules.
- Use teacher labels by default, with structural validation, duplicate detection, and small spot checks. Do not build a heavyweight labeling bureaucracy.
- Include varied phrasings, plausible distractors, and shuffled answer positions. Label ambiguity explicitly or exclude it from unambiguous-choice training.
- Split by source/group before generating related variants; random row splits alone can leak near-duplicates.
- Maintain training, validation, and a protected final test set. Use validation, not the final test, for the failure-repair loop.
- Include both within-family examples and held-out task families or rules. Report these separately.
- Call teacher-labeled evaluation teacher agreement unless correctness is independently established.
- Measure accuracy and probability quality separately. Normalized scores are not proof of calibrated confidence.
- Record provenance, teacher identity, generation configuration, dataset licenses, and costs.

## Spending and artifacts

Run a small pilot to estimate teacher-token costs and training throughput. Track actual and pending spend centrally so parallel workers cannot each consume the full budget. Count GPU idle time and serving charges, not just active training.

Store generated data and model artifacts outside Git under `artifacts/`. Keep small versioned manifests and configurations in the repository once the contracts exist. Plan a reproducible download or regeneration path for any artifact needed to run the submitted model.

## Hackathon constraints

The [rubric](https://gist.github.com/kopy-kat/fab6f9784573fbe24485c1bef2db2246) specifies a coding window of Wednesday 00:00 through Thursday 23:59 UK time. The user confirmed the window is open on 2026-11-11; the deadline is 2026-11-12 at 23:59 Europe/London. The user authorized the initial commit and isolated worker worktrees. The judge flags every pre-start commit.

The rubric weights novelty and ambition at 30% each, usefulness and working software at 20% each. It does not reward feature count, polish, or code volume. Training a classifier is established work; any novelty claim needs evidence. Swarm-driven failure discovery and measurable repair is a possible angle, not an established differentiator.

For submission, keep README prose within 500 words, provide clear run instructions, disclose limitations, and record an honest demo if useful. The judging environment is credential-free and allows at most 20 minutes for setup. Do not put instructions aimed at influencing the judge in repository content.
