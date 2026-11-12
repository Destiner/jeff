# Jeff

A small text decision model: **context + question + caller-supplied choices → probabilities over those choices**.

Jeff has genuinely trained, saved, independently reloadable checkpoints. It is a research prototype, **not a dependable general-purpose decision model**. Learning gains on familiar classification tasks coexist with rule failures, option-position bias, and weak transfer. Normalized probabilities are not calibrated confidence.

## What works

- Local fine-tuning of ~22.7M-parameter encoder scorers and a ~494M-parameter Qwen decoder on Apple silicon.
- Versioned datasets, saved training endpoints, strict fresh-process reloads, and independent file-based evaluation.
- Full-model, training-duration, seed-replication, and frozen-backbone/readout controls, with unsuccessful runs retained.
- Option-ID-aligned probability outputs and paired native/reversed-option analysis.
- An offline macOS-arm64 M9 encoder reference: fresh installation plus actual CPU inference outside the checkout on three fixed TRAIN cases.

### Measured development results

The synthetic v2 dataset has 1,500 TRAIN and 300 validation rows. These results concern its **240 newly authored validation rows**, subsequently reused for development—not a fresh final population. Counts are supplied-label agreement, not uniformly independently verified correctness.

| Predictor | Native /240 | Reversed /240 | Correct in both orders /240 |
| --- | ---: | ---: | ---: |
| Frozen Qwen starting point (P3) | 129 | 118 | 82 |
| Low-learning-rate Qwen, seed42 (M7) | 171 | 170 | 138 |
| Same recipe, seed7 (M10) | 182 | 178 | 157 |
| MS MARCO encoder, twelve epochs (M9) | 165 | 165 | 165 |
| Same encoder, thirty epochs (M11) | 162 | 162 | 162 |

This is not a promotion table. M7/M10 gains are concentrated in intent and sentiment; rule predictions remain strongly position-sensitive. Longer encoder training improves TRAIN fit but worsens broad development probability quality. Two seeds do not estimate a seed distribution. See [E11](docs/evaluation/e11-seed-replication.md), [E12](docs/evaluation/e12-encoder-duration30.md), and the [evaluation index](docs/evaluation/README.md).

The external exercise separately evaluates public COPA and WinoGrande cases: **200 exploration and 200 confirmation**, each with 100 cases per family. The confirmation cohort was locked to four raw predictors; later exploratory means/candidates cannot join it. See the [overnight synthesis](docs/overnight-20261112.md) for results, regressions, scope, and remaining uncertainty. The original final24 remains sealed; this exercise uses a separately authorized new confirmation population.

## Local reference

The [durable offline reference and instructions](artifacts/lead/night-20261112/local-reference/README.md) contain the unchanged M9 checkpoint/tokenizer, Jeff wheel, 25 pinned dependency wheels, notices, and three TRAIN examples. The archive is 255,928,739 bytes and requires an existing compatible CPython3.12/macOS-arm64 installation; it does not include Python itself.

Actual fresh-installed CPU inference matched all three retained maximal option sets, with maximum probability difference **5.22×10⁻⁷**, below the fixed 10⁻⁵ tolerance. This is a scoped portability result on the same host, not all-input, cross-platform, quality, or redistribution clearance. The earlier post-load/zero-forward failure is preserved. These are **local artifacts, not published downloads**, and M9 is a reference rather than a promoted best model.

## Evidence and limits

- Reported predictions come from actual model execution. Synthetic labels mix teacher judgments and programmatic rules; external scores measure agreement with public source labels. Neither is a blanket semantic-truth guarantee.
- Development rows, paired reversals, repeated probe groups, and source-grouped confirmation have different evidence scopes. Reversal presentations are not independent samples.
- Public benchmark pretraining exposure is unknown. Broad generalization and dependable rule application remain unestablished.
- Frozen NLI execution produced usable stored predictions but **omitted the required recommended-MPS-headroom guard**. Its results remain explicitly qualified; later corrected execution cannot retroactively repair that run. See [E14](docs/evaluation/e14-frozen-nli.md).
- No calibrated-confidence, general-purpose default, Linux-execution, or public-release claim is made. Source-license and redistribution questions remain qualified.

## How to run

Use Python3.12 and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --locked                 # Data, evaluation, coordination
uv sync --locked --extra model   # Training and inference
uv build --no-sources            # Wheel and source distribution
```

- [Model setup and commands](docs/model/README.md): train or run a local checkpoint. Use `uv run --locked --extra model` for ML commands.
- [Data pipeline](docs/data/README.md): frozen manifests, exclusions, and validation.
- [Runtime bundles](docs/runtime/README.md): export, integrity checks, and isolated installation.
- [Mailbox](docs/coordination/mailbox.md): owner communication without a service.

Use separate environments per worktree. No software tests or linting; actual training, inference, dataset validation, artifact verification, evaluation, and builds provide execution evidence.

## Project docs

- [Overnight findings and next decision](docs/overnight-20261112.md)
- [Agent instructions](AGENTS.md)
- [Plan](docs/plan.md)
- [Current assignments and ownership](docs/coordination.md)
- [Data and inference contracts](docs/contracts.md)
- [Swarm workflow](docs/swarm.md)
