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

The repository currently contains project decisions and a swarm workflow. No model or training implementation exists yet.

## What's faked or mocked

No model outputs, benchmark results, or demos are presented.

## How to run

There is no executable setup yet. The first implementation milestone is a tiny end-to-end training, save, reload, and evaluation run.

## Project docs

- [Agent instructions](AGENTS.md)
- [Plan and decisions](docs/plan.md)
- [Swarm workflow](docs/swarm.md)
- [Worker assignments and launch order](docs/coordination.md)
- [Shared data and inference contracts](docs/contracts.md)
