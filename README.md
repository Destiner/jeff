# Jeff

A small text decision model, trained with help from an agent swarm.

Give Jeff context, a question, and possible answers. It returns probabilities over those answers, rather than generating a response.

## What works

- Two ~22.7M-parameter encoder scorers: sentence-pretrained MiniLM with a new scalar head, and an MS MARCO cross-encoder retaining its pretrained head.
- Full local fine-tuning, self-contained inference checkpoints, and fresh offline-process reloads.
- Versioned synthetic datasets, independent file-based evaluation, source-group reporting, and option-order analysis.
- Portable local bundles for both architectures, demonstrated outside the development checkout on macOS CPU.
- A shared Markdown mailbox for agent coordination.

The latest dataset contains 1,500 training and 300 validation examples. On its 240 newly authored validation rows, trained MiniLM and MS MARCO achieve **55% and 58.75% supplied-label agreement**, versus a lexical baseline's 41.25%.

These gains coexist with regressions on historical examples and development probes. Rule performance remains weak, and no newer checkpoint is an unqualified replacement. See [the independent comparison](docs/evaluation/pilot-e3-m4.md).

## What's faked or mocked

No mocked model predictions. Data is synthetic; labels mix teacher judgments and programmatically verified rules, not uniformly independent ground truth. Probabilities are not claimed to be calibrated, and broad generalization is not established. Final evaluation remains sealed.

Runtime execution is demonstrated on macOS arm64 CPU only. Weights/datasets are local artifacts, not published downloads; installation may fetch Python dependencies. External redistribution/licensing questions remain unresolved.

## How to run

Use Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked                 # Data, evaluation, coordination
uv sync --locked --extra model   # Training and inference
uv build --no-sources            # Wheel and source distribution
```

- [Model setup and commands](docs/model/README.md): train or run a local checkpoint. Use `uv run --locked --extra model` for ML commands.
- [Data pipeline](docs/data/README.md): frozen manifests and validation.
- [Runtime bundles](docs/runtime/README.md): export, integrity checks, and isolated installation.
- [Mailbox](docs/coordination/mailbox.md): lead/owner communication without a service.

Use separate environments per worktree. No software tests or linting; actual training, inference, dataset validation, evaluation, and builds provide execution evidence.

## Project docs

- [Agent instructions](AGENTS.md)
- [Plan](docs/plan.md)
- [Current assignments and ownership](docs/coordination.md)
- [Data and inference contracts](docs/contracts.md)
- [Swarm workflow](docs/swarm.md)
