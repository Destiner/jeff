# Local model descriptor

`m9.json` is the small publisher-declared descriptor for M9, not a model download or an asset registry. Stage it as `model.json` alongside the three literal assets named in its `files` map. See [the SDK setup](../README.md#stage-local-assets) for a non-overwriting manual copy example.

Identity and pins come from the agreed handoff at root `artifacts/handoffs/release/final-sdk-20261112-01/skeleton-and-assets.md` and the retained B1 export inventory at root `artifacts/release/browser-b1-20261112-01/export-01/asset-inventory.json`. Export tokenizer files live under `tokenizer/`; the served copies live directly beside `model.onnx` and `model.json`.

The descriptor identifies trained source `m9-msmarco-duration-20261111-01` and its declared checkpoint JSON SHA-256. This is the FP32 scalar encoder/scorer, using the existing BERT state/question–candidate pair formatter, a 256-token pair cap, and softmax at T=1. It is not Qwen. The SDK rejects overlength pairs; it does not redesign truncation or calibrate probabilities.

Initialization checks the byte length and SHA-256 of all three model/tokenizer assets against this same-origin descriptor before using each asset. The descriptor itself is publisher-declared provenance: these checks are not a trusted signature, independent authentication, or verification/reconstruction of a full training checkpoint. ORT runtime files are separate and are not pinned by this descriptor.

`metadata.model` reports the selected descriptor. `expectedModelId`, when supplied, verifies its ID; it cannot relabel the model. Another compatible export needs its own truthful identity, checkpoint declaration and asset pins, not an M9 alias. The package does not contain weights or WASM, and this descriptor does not establish public redistribution permission.
