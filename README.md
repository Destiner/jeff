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

Shared Python packaging, project decisions, and a swarm workflow. Model, data, and evaluation implementations are in parallel worker branches and are not integrated yet. No trained checkpoint is claimed.

## What's faked or mocked

No model outputs, benchmark results, or demos are presented.

## How to run

Use Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked                 # Shared package, without ML dependencies
uv sync --locked --extra model   # Model/training environment
uv build --no-sources            # Wheel and source distribution
```

Use separate environments per worktree. Run model commands with `uv run --locked --extra model` to retain their optional dependencies. Training and inference commands will be documented when the worker implementations are integrated.

No software tests or linting. Model evaluation and dataset validation remain part of the training workflow.

## Project docs

- [Agent instructions](AGENTS.md)
- [Plan and decisions](docs/plan.md)
- [Swarm workflow](docs/swarm.md)
- [Worker assignments and launch order](docs/coordination.md)
- [Shared data and inference contracts](docs/contracts.md)
