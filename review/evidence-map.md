# Evidence map

Paths below are relative to repository root. Start with the short reports; inspect raw files only where they bear on your question. All copied scientific files retain their original bytes/hashes. Use `python3 review/resolve_path.py ORIGINAL_PATH` for references from old reports; `--list PREFIX` discovers included artifacts without dumping JSON.

## Mission, interface and choices
- review/brief.md; docs/plan.md; docs/contracts.md; AGENTS.md.
- docs/coordination.md and docs/owner-lifecycle.md describe active authority at cutoff, not duties for external reviewers.
- The root README is an earlier pilot overview, not the latest experiment report.

## Encoder/data progression
- docs/evaluation/pilot-e3-m4.md, e4-m5-lr-control.md, e4-d3-seen-rules.md.
- docs/model/*-run.json, configs/model/, src/jeff/model/, src/jeff/training/.
- review/evidence/data/data-pilot-v1/ and data-pilot-v2/: released TRAIN/development manifests/shards and selected authoring/revision evidence. Never treat development rows as new training examples.
- review/evidence/evaluation/e3-v2-freeze-v1/{inherited-v1,new-v2,probes}/validation.jsonl: exact development strata.
- review/evidence/evaluation/e3-v2-order-v1/ and e3-v2-new-order-v1/: paired/reversed inputs and identity mappings.
- review/evidence/data/data-d3-seen-rules-v1/release/ and review/evidence/evaluation/e4-d3-released-boundary-v1/: validation-only D3 and source-unit boundaries.

## Frozen decoder and M6 learning
- docs/runtime/p3-frozen-challenger.md; docs/evaluation/e5-frozen-decoder.md.
- src/jeff/runtime/qwen_challenger.py and configs/runtime/p3-qwen.json.
- docs/model/m6-qwen-plan.md, m6-qwen-results.md, m6-qwen-diagnosis.md, m6-qwen-run.json.
- **Executed M6 source:** `git show dafd5d235b53af341fbf539e4bf32dcf09a399f2:src/jeff/training/qwen_decision.py`, with `src/jeff/training/qwen_data.py` and the runtime adapter at that same revision. Do not assume later source is the executed revision.
- review/evidence/model/m6-qwen-20261111-01/: freeze, audit/schedule, starting controls, discarded-capacity evidence, training/fit-before.jsonl, fit-after.jsonl, online.jsonl, events.jsonl, receipt.json and checkpoint-manifest.json.
- review/evidence/model/m6-diagnosis-20261111-01/{source-review.md,timeline-review.md}.
- review/evidence/release/p3-qwen-20261111-01/run-02/ and p4-m6-20261111-01/run/: actual original/reversed/probe vectors. The initial P3receipt failure is also preserved where selected.
- No weights/tokenizer assets are exported. Their manifests/hashes are provenance, not present binaries.

## Independent E6
- docs/evaluation/e6-plan.md and e6-decoder-learning.md.
- review/evidence/evaluation/e6-analysis-preparation-v3/execution-01/: recipe, exact starting differences, completion, E6-{inherited-v1,new-v2,probes}.md and study inputs.
- review/evidence/evaluation/e6-quality-review-v1/: CSV scalar/source/order evidence, independent arithmetic results and qualifications.
- Source evaluators: src/jeff/evaluation/. The exported recipes retain original absolute paths; do not execute them unchanged. Resolve inputs first or inspect/arithmetic-check them in scratch space.
- E6's initial pre-metric preparation stopped after operational policy hashes changed; its revised scientific dependencies stayed unchanged. This procedural event is not a second model prediction or learning run.

## R5/R6
- docs/research/learning-strategies.md and experiments/research/learning-strategies-evidence.md: earlier proposal, not established success.
- docs/research/order-instability-diagnosis.md and order-diagnostic-packet.md.
- review/evidence/research/r6-20261111T155310Z/: predeclaration, fixed packet, saved-output analysis, four-cell reproduction and independent review.
- review/evidence/release/r6-order-20261111-01/: completed one-pass192presentation execution and probabilities.
- Review identifiability and sampling assumptions, not just fitted bias coefficients.

## Data diagnosis and coordination
- review/evidence/data/d4-20261111T144812Z/training-quality-summary.md and closure.json.
- review/evidence/data/d5-20261111T161610Z/findings.md, owner-crosscheck.json, binary-identifiability-addendum.json and audit subdirectories.
- review/evidence/infra/i4-20261111T144835Z/report.md, final-stats.json, closing snapshot, events.md, checks.jsonl and overhead.jsonl.
- review/evidence/handoffs/infra/20261111T162157Z-infra-parked.md and infra/continuation-20261111T155157Z/parking-message.md.
- review/evidence/handoffs/lead/wave-20261111-{1520,1540,1610,1635}/: explicit pre-execution authority, continuation rules and next work.
- These are selected operational records, NOT a complete raw conversation/mailbox or continuous activity trace. I5's later readout is outside the cutoff.

## Intentional absences
Sealed final shards/labels/predictions; all model/checkpoint/tokenizer asset bytes; dependency environments; live mailbox; raw sessions; some redundant report fans and intermediate author reviews. Manifests can mention these absent files. Actual execution-source history is retained, but one early tiny run reports a dirty working tree: its commit does not reconstruct uncommitted bytes.
