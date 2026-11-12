Jeff local browser notices

M9 is Jeff's fine-tuned twelve-epoch encoder, based on
cross-encoder/ms-marco-MiniLM-L6-v2 at revision
233902d25c440f23af6f7d6e94d2946bac0bee0a, converted to FP32 ONNX.
The exported model is modified trained software, not untouched upstream weights.
Retained: m9-APACHE-2.0.txt, m9-upstream-model-card.md, m9-Jeff-NOTICE.md.
The last notice is Jeff-authored, not an upstream NOTICE.

Browser packages: @huggingface/transformers3.8.1 (Apache-2.0),
@huggingface/jinja0.5.12 (MIT), onnxruntime-web/common
1.22.0-dev.20250409-89f8206ba4 (MIT). Complete license texts are adjacent.
ORT source texts are unchanged captures from:
https://raw.githubusercontent.com/microsoft/onnxruntime/89f8206ba4/LICENSE
https://raw.githubusercontent.com/microsoft/onnxruntime/89f8206ba4/ThirdPartyNotices.txt
The ORT collection is project-wide, not a verified list of shipped WASM components.

Potential JavaScript transitive notices are retained for flatbuffers25.9.23,
long5.3.2, platform1.3.6, protobufjs7.6.6 and its protobufjs subpackages.
Their actual tree-shaken bundle membership is not established; inclusion of
these notices does not assert every named component ships. guid-typescript's
full local permission text was not located in the bounded source inventory.
This is not an exhaustive dependency or native-binary attribution audit.

These source texts are served alongside local assets and retained in the
repository; they are not part of the fixed fourteen-file M9 offline cache.
Build tools and native exporter dependencies remain separate environments.
The isolated M10 Qwen prototype is not included in the normal M9 demo.

Jeff first-party redistribution terms were not established. Component grants
do not clear all underlying training corpora, teacher output or demo-row rights.
No public distribution or legal clearance is claimed. Original source mapping:
artifacts/research/b2-notices-20261112T121139Z/inventory.md.
