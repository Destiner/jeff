# Jeff

A small text decision model, trained with help from an agent swarm.

Give Jeff context, a question, and possible answers. The goal is to return probabilities over those answers, including for decisions not explicitly seen during training.

## Goals

- Fine-tune a small pretrained model rather than pretrain language understanding from scratch.
- Have a usable trained checkpoint by the end of day one; improve and evaluate it on day two.
- Prefer local training and inference on Apple silicon with 16–24 GB memory.
- Design contributions for tens or hundreds of agents working in the same codebase through isolated workspaces.
- Keep additional teacher-model and compute spending within £50.

Training and understanding the model are the primary deliverables. Applications and web demos are optional.

## What works

A ~22.7M-parameter MiniLM candidate scorer, full fine-tuning, self-contained inference checkpoints, and decision-only JSONL prediction. Local MPS training and fresh offline-process reloads have completed.

The 300-train/60-validation pilot improved reference-label agreement from 19/60 to 36/60. This mixes teacher and rule-verified labels, not wholly verified accuracy. Rule performance regressed, and some rule-validation questions were truncated at 128 tokens. See [the qualified results](docs/model/pilot-results.md).

Data-generation and evaluation tooling are still on separate worker branches. Checkpoints and datasets are local artifacts, not bundled with this repository.

## What's faked or mocked

No mocked model outputs. The starting scoring head is random; probabilities are not claimed to be calibrated. This small pilot does not establish broad generalization. No application demo is claimed.

## How to run

Use Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked                 # Shared package, without ML dependencies
uv sync --locked --extra model   # Model/training environment
uv build --no-sources            # Wheel and source distribution
```

Use separate environments per worktree. Run model commands with `uv run --locked --extra model` to retain their optional dependencies. [Model setup and commands](docs/model/README.md) cover training and local checkpoint inference. The recorded pilot uses 128 tokens; the approved follow-up uses 256 to avoid the measured input loss.

No software tests or linting. Model evaluation and dataset validation remain part of the training workflow.

## Project docs

- [Agent instructions](AGENTS.md)
- [Plan and decisions](docs/plan.md)
- [Swarm workflow](docs/swarm.md)
- [Worker assignments and launch order](docs/coordination.md)
- [Shared data and inference contracts](docs/contracts.md)
