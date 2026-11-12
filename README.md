# Jeff

**Context + question + caller-supplied choices → probabilities over those choices.**

Jeff is a small, fine-tuned text decision model with saved, independently reloadable checkpoints. Its trained encoder also runs directly in a browser: tokenization and inference happen on the device, without a Python or remote inference backend.

## Browser demo

The current browser model is **M9**, a ~22.7M-parameter encoder exported to a ~91 MB FP32 ONNX file. Actual Safari/WASM execution matched Python's top choices on three fixed TRAIN examples, with maximum probability difference **6.78×10⁻⁷** and identical tokenization.

About 104 MB of app/model/runtime assets can be prepared for offline use. A new page load and three inferences succeeded with the static server stopped; host networking remained on. Inputs and results are not persisted by the asset cache.

This establishes a short-input demo, not all-input compatibility or a new quality benchmark. Model files are local artifacts, not included in Git or published downloads. See [setup and launch instructions](web/README.md), [initial port evidence](docs/runtime/browser-b1.md), and [offline/Qwen results](docs/evaluation/browser-b2.md).

The larger trained Qwen export initialized on WebGPU, but a memory-pressure safeguard stopped its first prediction request before any result returned. Its browser parity remains unverified; the demo stays M9.

With retained model assets and Bun:

```sh
cd web
bun install --frozen-lockfile --ignore-scripts
bun run demo
```

## Recorded learning

Fine-tuning substantially improved the corresponding pretrained models on our synthetic development distribution:

| Candidate | Agreement before → after (of 240) | Log loss before → after |
| --- | ---: | ---: |
| Qwen ~494M, seed 7 (M10) | 129 → 182 | 1.312 → 0.525 |
| Encoder, twelve epochs (M9) | 99 → 165 | 1.059 → 0.699 |

These are native-runtime results on 240 new synthetic validation examples, subsequently reused during development—not browser benchmarks or an untouched final population. Training used 1,500 examples. Labels mix teacher judgments and programmatic rules; agreement is not uniformly verified correctness.

Improvements are concentrated in intent and sentiment. Rule failures, Qwen option-position sensitivity and weak external transfer remain. Longer encoder training improved TRAIN fit but worsened development log loss. **Normalized scores are not calibrated confidence or dependable general reasoning.**

See [Qwen learning](docs/evaluation/e11-seed-replication.md), [encoder learning](docs/evaluation/e9-encoder-duration.md), [duration regression](docs/evaluation/e12-encoder-duration30.md), and the [evaluation index](docs/evaluation/README.md). Successful and unsuccessful experiments remain recorded. The separate external exploration/locked-confirmation exercise is summarized in the [overnight report](docs/overnight-20261112.md); the original 24-case final set remains sealed.

## Native use

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked --extra model
uv build --no-sources
```

[Model instructions](docs/model/README.md) cover training and local inference. The [offline macOS-arm64 reference](docs/runtime/p11-portable-m9.md) includes M9, dependency wheels and a three-case fresh-installed CPU proof. It requires an existing compatible Python installation.

Portability evidence is scoped to the recorded executions; other platforms, broad quality and public redistribution clearance are not implied. Source terms and notices remain relevant.

## Project documentation

[Contracts](docs/contracts.md) · [Runtime](docs/runtime/README.md) · [Data](docs/data/README.md) · [Plan](docs/plan.md) · [Coordination](docs/coordination.md) · [Agent instructions](AGENTS.md)

No software tests or linting. Actual inference, model/data evaluation, artifact validation and builds provide execution evidence.
