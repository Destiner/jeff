# Model origin, modifications and rights

Jeff notice, not an upstream NOTICE. Base and tokenizer:
cross-encoder/ms-marco-MiniLM-L6-v2 at 233902d25c440f23af6f7d6e94d2946bac0bee0a.
Pinned card: https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2/raw/233902d25c440f23af6f7d6e94d2946bac0bee0a/README.md
Existing P1 source evidence records Apache-2.0 and no upstream LICENSE/NOTICE
at that pin. The verbatim pinned card and canonical Apache-2.0 text accompany
this bundle. No upstream endorsement or trademark permission is implied.

M9 run m9-msmarco-duration-20261111-01 completed 2026-11-11: 12 epochs,
4500 updates, 18000 presentations on data-pilot-v2. Encoder and retained
pretrained scalar classifier were fine-tuned in encoder/model.safetensors.
No separately initialized head.safetensors exists. Configuration/tokenizer files
were re-saved by Transformers; checkpoint.json is Jeff provenance/settings.
All seven source checkpoint files must be preserved byte-for-byte. Adjacent
notices identify modifications without rewriting immutable checkpoint files.
Only three authorized decision-only TRAIN examples are bundled, not the corpus.
Metadata contains historical local paths;
completed run provenance supersedes its save-time running snapshot. Those paths
are not execution dependencies, but require review before any distribution.

Apache-2.0 for the upstream model is not a blanket Jeff code, synthetic-data,
provider/account or corpus license. No project license grant is recorded and
provider redistribution/training rights are not independently cleared.
No external publication is authorized. Dependency wheels retain their own
embedded licenses/notices; the outer offline kit must inventory these separately.
This notice does not assert a complete dependency-license audit. Apache AS-IS
limitations apply. M9 is a working reference with known rule weaknesses, not a
promoted general decision model or a calibrated-confidence system.
