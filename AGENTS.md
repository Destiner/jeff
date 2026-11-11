# Jeff

A small, text-based decision model: context + question + caller-supplied choices → probabilities.

## Project constraints

- The model is the project. Prioritize training, evaluation, and improvement; applications and UI are optional.
- Deliver a saved, reloadable trained model and held-out evaluation by the end of day one. Improve it on day two.
- Start from pretrained weights. Use Python with uv; the backbone, ML backend, and training method remain open.
- Target Apple silicon with 16–24 GB unified memory. Prefer local training and inference; cloud training is a fallback.
- Additional teacher-model and compute spending has a combined £50 ceiling. Estimate and track aggregate spend before scaling.
- Strong-model-generated labels are acceptable by default. Use lightweight quality checks; distinguish teacher agreement from independently verified correctness.
- Probabilities are not automatically calibrated. Measure reliability before claiming calibrated confidence.
- The user confirmed the coding window is open on 2026-11-11. Deadline: 2026-11-12 at 23:59 Europe/London. Pre-start commits are flagged by the rubric.

## Working in a swarm

- Read [the plan](docs/plan.md), [the active assignments](docs/coordination.md), and [the shared contracts](docs/contracts.md) before taking work. Follow [the swarm workflow](docs/swarm.md).
- Use isolated branches/worktrees and bounded tasks with explicit ownership. Never share a mutable checkout or training output directory.
- Agree on versioned data, inference, and evaluation contracts before scaling contributions. Coordinate shared-contract changes through the integration owner.
- Parallelize dataset shards, validation failure analysis, and controlled experiments; keep core implementation ownership narrow.
- Keep final test data out of training and tuning. Split related examples together, before generating paraphrases or variants.
- Queue training jobs against measured memory capacity; agent count is not compute capacity.
- Put generated data, checkpoints, caches, and run outputs under ignored `artifacts/`, with unique IDs. Commit small provenance manifests and configurations, not bulky artifacts.
- Never overwrite another worker's outputs. Submit a small reviewable change and report checks, artifact IDs, and costs.

## No tests or linting

- Do not write or run software tests, add test suites or test runners, or configure or run linters. This is an explicit project rule, including before commits.
- Model evaluation, dataset validation, and actual training/inference runs remain essential; they are not software test suites.

## Verification

- This starts as a documentation-only scaffold. Do not invent successful builds or model runs.
- When introducing the toolchain, document its setup and build/package commands. Verify a real build when implementation exists; do not add test or lint steps.
- Model handoff requires saved weights, a fresh-process reload, working inference, and a comparison with the starting baseline.
