# Protected final reservation

Dataset `evaluation-final-v1`: 24 separately assigned final groups, one row each. Six cases each for `intent`, `sentiment`, `rule_application`, and the reserved unseen `passage_entailment` family. Options span 2–6 choices. Original teacher-authored fictional scenarios; no external dataset or company/customer content. Labels are teacher labels, not independently verified; the curator's exact model identity is unknown.

Small public manifest: `manifests/evaluation/final-v1.json`. Relative paths resolve against `JEFF_ARTIFACTS_DIR`. All content, compact source cases, labels, rationales, and metadata are private under `evaluation/final/`; do not inspect or distribute during tuning. No final examples live in source code, configs, or public docs.

## Freeze and release

- Curation delegated separately from validation discovery; returned to lead for serialized materialization. No validation examples were provided to the final curator.
- Assigned source groups before serialization. Contract validation performed during freezing: unique example IDs, option uniqueness/targets, provenance, split, reserved family. Frozen shard and source hashes recorded. This is structural validation, not independent label correctness.
- No final baselines, model inference, or scoring performed; no label-free final inputs exported.
- Before release, Lead freezes the selected checkpoint identity, model/configuration/code revision, and validation-based selection rationale. Evaluation authorizes one reporting pass, prepares label-free inputs inside the final subtree, and requests inference from Model's existing compute owner. Model should receive only the specific released input file, never labels, rationales, or neighboring content.
- Evaluate selected model, its starting baseline, and simple baselines on identical final examples, reporting all coverage/failures and teacher agreement by family. Report unseen family separately.
- Keep detailed final failures private while any tuning continues. If a final result influences training, data repair, hyperparameters, or model selection, it is no longer untouched final evidence. Freeze a new untouched set for a later claim.

## Limitations

Procedural isolation is not an OS security boundary. Distinct namespaced groups avoid ID/group collisions by construction, but do not establish semantic/template independence from every possible training example. Cross-shard contamination review is still needed at the final release gate; do not send final content to training/data workers for that review. Small synthetic family samples do not establish broad generalization. Teacher consistency and label ambiguity remain limitations; do not claim calibrated confidence or independently verified correctness.

Cost: £0 additional actual/pending. No paid APIs or model loads by Evaluation.
