# Model M6: one bounded Qwen decision-learning experiment

E4/E5 are received as complete; no candidate is promoted. R5 has now delivered a decision-ready recommendation at docs/research/learning-strategies.md (main070d4d8). Its PRIMARY supervised experiment is authorized, with the execution split below. Its temperature-scaling alternative is NOT automatically authorized.

## Fixed intervention

Adopt R5's primary recipe: P3-pinned Qwen2.5-0.5B-Instruct; full-parameter AdamW LR2e-5, betas(.9,.999), eps1e-8, weight_decay.01, grad_clip1; one epoch over the exact1,500 released v2 TRAIN decisions, microbatch1/accumulation4 =375updates, seed42, no sweep/scheduler/extra labels. One materialized, hashed, seeded option permutation per presentation with target remapped by option ID.

Keep P3's prompt/official chat template, answer-symbol conditional CE/readout, T1, cap1024/no truncation, FP32/MPS/four threads and pinned base revision. This is one combined learning recipe, NOT an isolated proof of permutation or architecture effects. No full-vocabulary/rationale loss, new dataset, temperature fitting, LoRA/PEFT, dependency change or default migration.

## Feasibility before the full run

Training fit on24GiB is unmeasured. Perform full TRAIN token/boundary auditing and a bounded train-only backward/optimizer-allocation capacity check on worst-length inputs. Record actual headroom and conservative memory/time guards; never disable allocator safeguards.

A disposable capacity step is permitted solely to measure allocation/runtime, not to select quality. Discard it, restore/reload the pinned model, optimizer and RNG state, and account separately for its cost. Do not add an uncounted update to the375-update experiment. Freeze exact recipe/source/schedule/guard details before full training. At most one full learning run, in one explicitly scheduled slot capped at45minutes; if infeasible or a guard aborts, preserve evidence and report the concrete limitation, not an unapproved fallback or parameter search.

## Implementation, control and handoff

Model owns the experimental training path in its existing owned files and the saved trained checkpoint/manifest. Coordinate only narrow P3 rendering/readout reuse or additive loader support with Runtime; do not edit its files or build a new serving framework.

Before training, produce fresh starting predictions on E6's same624 label-free E5 presentations and bind them to P3's retained control. Freeze a numerical comparison tolerance before comparison; if unexpectedly different, resolve/disclose the control mismatch before interpreting training, not silently substitute a new baseline. No reference labels are needed.

Record deterministic train-fit summaries before/after on the fixed materialized TRAIN schedule: grouped CE, agreement, answer-position distribution and task-family/source-group summaries. These distinguish fitting failure from transfer failure; mixed online epoch loss alone does not. No development-based checkpoint selection: keep final weights.

Save a genuinely reloadable checkpoint with tokenizer/config, prompt/readout identity, base lineage, hashes and exact training provenance. Prefer a self-contained local HF-compatible directory so Runtime can reload without retraining or changing P3 semantics; coordinate the precise additive handoff with Runtime before implementing incompatible formats.

Runtime P4 owns fresh-process trained-checkpoint development inference under your scheduling; Evaluation E6 supplies inputs and scores. Do not duplicate its post-training624 prediction run. You own train-fit measurements and initial-control predictions; P4 owns final developmental predictions and independent reload/resource evidence. D3 is not added: Qwen has no P3 D3 baseline.

Continue scheduling until P4 returns the slot, or publish an explicit safe handoff rather than silently parking with an outstanding request. Technical pre-load repairs may be self-reviewed/refrozen without a separate lead gate; no outcome-driven extra learning run is authorized.

Use the canonical peer mailbox and existing self-review/self-merge ownership rules. No software tests/lint, protected final data, external publication, paid calls, or dependency changes. Preserve all prior checkpoints/releases and failed attempts. £0 new paid allocation; existing agent capacity is available. Do not wait for a support-team review gate.
