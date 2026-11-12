# Jeff

**Context + question + caller-supplied choices → probabilities over those choices.**

[Watch the 85-second demo](https://github.com/Destiner/jeff/releases/download/m9-browser-v1/jeff-actual-demo.mp4) · [Download M9](https://github.com/Destiner/jeff/releases/tag/m9-browser-v1)

Pretrained models were fully fine-tuned on Apple silicon, saved and reloaded for native inference:

- **M9:** ~23M-parameter MS MARCO/MiniLM encoder and ranking head. Grouped-choice cross-entropy trains scores for context/question/candidate pairs; softmax normalizes across choices.
- **M10:** ~494M-parameter `Qwen2.5-0.5B-Instruct` decoder. It reads choices jointly and normalizes next-token answer-symbol scores.

## Use it

The browser-first `@jeff/sdk` runs M9 tokenization and single-thread WASM inference in a Web Worker, with a ~91 MB FP32 ONNX model. Model/tokenizer sizes and SHA-256 hashes are checked. No inference server, API key or telemetry.

```ts
import { createEngine } from '@jeff/sdk';

const engine = await createEngine({
  assetBaseUrl: '/models/m9/', ortBaseUrl: '/ort/',
});
try {
  const result = await engine.predict({
    state: 'Book a team meeting for next week.',
    question: 'Which workspace should receive this request?',
    options: ['Tasks', 'Calendar', 'Notes'],
  });
  console.log(result.probabilities);
} finally {
  await engine.dispose();
}
```

A routing queue, sentiment-to-emoji chat and editable playground use the SDK. [API documentation](sdk/README.md).

## Measured learning

Both models trained on 1,500 examples. Native, original-order results use 240 synthetic validation examples subsequently reused during development. Labels combine teacher judgments and programmatic rules.

| Model | Label agreement before → after, /240 | Log loss before → after |
| --- | ---: | ---: |
| [M9: twelve epochs](docs/evaluation/e9-encoder-duration.md) | 99 → 165 | 1.059 → 0.699 |
| [M10: one epoch, seed 7](docs/evaluation/e11-seed-replication.md) | 129 → 182 | 1.312 → 0.525 |

Later adaptation M13 improved fresh routing/sentiment agreement 21/32 → 25/32, but worsened retained-development log loss 0.699 → 1.047. It failed predeclared retention limits; **M9 remains selected**. [Results](docs/evaluation/final-sprint-results.md).

## Execution and limits

Six actual Chromium app-button predictions matched saved native top choices; maximum probability difference **1.69×10⁻⁶**. Queue routing worked. The edited recording retains a negative message ranked **Mixed**. Earlier packed-SDK Safari parity also passed. [Execution, interrupted attempts and setup evidence](docs/runtime/submission-delivery.md).

Scores are uncalibrated. Rules/external transfer remain weak; Qwen is order-sensitive. Qwen native inference works; its browser attempt stopped without a prediction. New-app offline inference remains unverified. Encoded pairs exceeding 256 tokens are rejected.

Messages/requests are authored examples. State is local; there is no Slack/workspace integration. Emoji mapping is fixed. Predictions are computed, not canned.

## Run locally

Requires **Bun 1.4.4**. Download the release archive/checksum, verify SHA-256 and extract into `artifacts/m9`, then:

```sh
bun install --frozen-lockfile --ignore-scripts
ASSETS="$(cd artifacts/m9 && pwd -P)"
bun run demo --model-dir "$ASSETS" --descriptor "$ASSETS/model.json"
```

Open **http://127.0.0.1:4174/**. [Complete download/setup commands](web/README.md). [Python training/native inference](docs/model/README.md) requires Python 3.12 and uv.
