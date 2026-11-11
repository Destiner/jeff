# Worker: Training data

Create your own `worker/data` branch and `.worktrees/data` worktree from committed main before editing. Do not implement in the root checkout, overwrite an existing workspace, or create workspaces for other leads.

Read `AGENTS.md`, `docs/coordination.md`, and `docs/contracts.md`. Work on `worker/data` in `.worktrees/data`. Do not write or run software tests or linting. Dataset validation is part of your deliverable.

## Mission

Supply useful labeled examples early, then scale diversity and quality. Strong-model-generated labels are acceptable by default; do not build an elaborate multi-judge labeling platform.

## Ownership

Edit only `src/jeff/data/`, `configs/data/`, `manifests/data/`, and `docs/data/`. Store generated shards under the shared artifact root at `data/<dataset-or-shard-id>/`. Root packaging and contracts belong to the integrator.

Training families are `intent`, `sentiment`, and `rule_application`. Do not generate training examples for the reserved `passage_entailment` family or inspect final-evaluation content.

## First milestone

1. Deliver a tiny contract-valid shard immediately, before constructing a large dataset.
2. Aim for an initial pilot around 300 training and 60 validation examples across the three families. These are starting sizes, not quotas worth sacrificing correctness for.
3. Assign source/scenario groups to splits before paraphrasing or producing variants.
4. Include informative option descriptions, plausible distractors, varied option positions, and varied wording. Avoid ambiguous targets in the first pilot.
5. Validate structure, IDs, targets, group isolation, and duplicates. Publish a manifest and concise data-quality summary.
6. Record provenance and the actual teacher/source. Existing approved agent access may be used; separately billed API generation requires an allocation.
7. After the first model run, expand based on validation failures and missing coverage rather than generating more of the same examples.

Do not hand-write many near-identical templates merely to inflate counts. Programmatically verifiable rule examples are useful, but keep their generator families grouped to avoid leakage.

## Suggested subagents

- One generator per task family, each assigned its own shard paths and group namespace.
- One reviewer for structural quality, duplicates, and a small label spot check.
- The session lead owns dataset assembly and the immutable manifest.

No simultaneous appends to one dataset file. Review agents must not silently rewrite published shards.

## Handoff

Publish `artifacts/handoffs/data/<id>.md` in the shared root with branch/commit, manifest path, counts by family and split, quality findings, generation method, dependencies, and actual/pending cost. Notify Model as soon as the tiny first shard is available; do not wait for all subagents.
