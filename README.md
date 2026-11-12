# Jeff

**Context + question + caller-supplied choices → probabilities over those choices.**

Jeff fine-tunes pretrained language models for text decisions without a fixed label taxonomy. Two model families were fully fine-tuned locally on Apple silicon, saved and reloaded in fresh processes for inference.

## What works

- **MiniLM encoder (M9, ~23M parameters):** starts from `cross-encoder/ms-marco-MiniLM-L6-v2`. Each context/question/candidate pair receives a scalar score, normalized across choices. Grouped-choice cross-entropy trains both the encoder and existing ranking head.
- **Qwen2.5 decoder (M10, ~494M parameters):** starts from `Qwen/Qwen2.5-0.5B-Instruct`. It reads all choices together and normalizes next-token answer-symbol scores over the supplied choices.
- **Browser SDK:** `@jeff/sdk` runs M9 tokenization and single-thread WASM inference in a Web Worker using a ~91 MB FP32 ONNX model. No inference server, API key or telemetry. Model/tokenizer buffers are checked against recorded sizes and SHA-256 hashes.
- **Applications:** a request-routing queue, sentiment-to-emoji chat and editable decision playground consume the SDK.

Browser usage with staged assets ([SDK documentation](sdk/README.md)):

```ts
import { createEngine } from '@jeff/sdk';

const engine = await createEngine({
  assetBaseUrl: '/models/m9/',
  ortBaseUrl: '/ort/',
});
try {
  const prediction = await engine.predict({
    state: 'Book a team meeting for next week.',
    question: 'Which workspace should receive this request?',
    options: ['Tasks', 'Calendar', 'Notes'],
  });
  console.log(prediction.probabilities);
} finally {
  await engine.dispose();
}
```

## Measured learning

Both models trained on 1,500 examples. These native, original-option-order results use 240 synthetic validation examples subsequently reused during development. Labels combine teacher judgments and programmatic rules.

| Model | Label agreement before → after, /240 | Log loss before → after |
| --- | ---: | ---: |
| [M9: twelve epochs](docs/evaluation/e9-encoder-duration.md) | 99 → 165 | 1.059 → 0.699 |
| [M10: one epoch, seed 7](docs/evaluation/e11-seed-replication.md) | 129 → 182 | 1.312 → 0.525 |

A later encoder adaptation, M13, improved fresh routing/sentiment agreement from 21/32 to 25/32, but increased retained-development log loss from 0.699 to 1.047. It failed predeclared retention limits; **M9 remains selected**. [Results and decision](docs/evaluation/final-sprint-results.md).

## Execution evidence and limits

The packed SDK completed six Safari 27/WASM predictions: all top choices matched native references; maximum probability difference was **8.87×10⁻⁷**. Final production-app acceptance and new-app-graph offline inference were not run.

Qwen's browser attempt stopped at the memory-pressure guard before returning a prediction; its native inference completed. [Browser results](docs/evaluation/browser-b2.md).

Scores are uncalibrated. Rule application and external transfer remain weak; Qwen is option-order sensitive. The SDK rejects encoded pairs exceeding 256 tokens. [Evaluation reports](docs/evaluation/README.md).

## What's faked or mocked

Example messages are authored. Queue/chat state is local, with no external workspace or Slack integration. Emoji selection is a fixed mapping from sentiment labels. Model predictions are not canned.

## How to run

Requires **Bun 1.4.4 and the M9 asset export**. Weights are not in Git; no public asset download is available. A fresh clone alone cannot run inference. From the repository root, with retained assets:

```sh
bun install --frozen-lockfile --ignore-scripts
bun run demo
```

Open **http://127.0.0.1:4174/**. [Asset placement, overrides and launcher details](web/README.md). [Python training/native inference](docs/model/README.md) requires Python 3.12 and uv.
