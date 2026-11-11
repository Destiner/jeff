# Worker: Model evaluation

**LD004 ownership update:** you are the workstream owner, not a worker awaiting lead review. Self-review and self-merge completed changes within the paths below, using the shared lock/build protocol in `docs/coordination.md`. Current assignments in that file supersede the initial milestone below. Coordinate directly with other owners and continue bounded in-scope work without waiting for lead approval. No software tests or linting. Report final delivery with the main merge commit.

Create your own `worker/evaluation` branch and `.worktrees/evaluation` worktree from committed main before editing. Do not implement in the root checkout, overwrite an existing workspace, or create workspaces for other leads.

Read `AGENTS.md`, `docs/coordination.md`, and `docs/contracts.md`. Work on `worker/evaluation` in `.worktrees/evaluation`. Do not write or run software tests or linting. Model evaluation is your primary deliverable, not a software test suite.

## Mission

Make it possible to tell whether training helps, independently of the trainer's loss graph. Build file-based evaluation before a trained model is available.

## Ownership

Edit only `src/jeff/evaluation/`, `configs/evaluation/`, `manifests/evaluation/`, and `docs/evaluation/`. Generated outputs belong under the shared artifact root at `evaluation/<run-or-dataset-id>/`.

Final-evaluation data belongs under `evaluation/final/`. Do not send its examples, labels, or detailed failure cases to training/data workers during tuning. This is procedural isolation; filesystem permissions do not enforce it.

## First milestone

1. Implement scoring of contract-format prediction files against labeled rows, joining by IDs.
2. Report coverage, invalid/missing predictions, accuracy or teacher agreement, log loss, and per-family results. Show denominators and failures.
3. Produce simple baseline predictions, including uniform probabilities with clearly identified tie handling. Ask Model for a pre-training model baseline; do not independently load a second large model.
4. Consume Data's validation shard and publish baseline metrics before the trained model arrives.
5. Produce label-free inference inputs and score Model's trained predictions on the same examples.
6. Reserve a modest final-evaluation set: new in-family groups plus the unseen `passage_entailment` family. Do not use it for iterative failure analysis or score it repeatedly while tuning.

Use validation for option-order changes, negation, ambiguity, and adversarial failure discovery. Include probability-quality diagnostics when useful, but avoid claiming calibration from a tiny sample. Teacher labels measure teacher agreement unless independently verified.

## Suggested subagents

- Metrics and report generation.
- Final-evaluation curation, isolated from workers producing validation repairs.
- Validation-only adversarial cases and option-order analysis.

Keep ownership disjoint. CPU metric computation is allowed; request Model's compute slot for any substantial model inference. Paid teacher calls need an explicit allocation.

## Handoff

Publish `artifacts/handoffs/evaluation/<id>.md` in the shared root with branch/commit, commands, report and input paths, baseline comparisons, failure counts, dependencies, and costs. Intermediate handoffs must not reveal reserved final-evaluation content.

Keep startup updates, inference requests, and early baseline results in these files. Discover Data/Model inputs through their public handoff files when needed. Send one final chat report when the assigned evaluation task is complete; report early only if genuinely blocked. Do not end the task merely because you delegated work or published an input request.
