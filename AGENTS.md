# Jeff

A small, text-based decision model: context + question + caller-supplied choices → probabilities.

## Project constraints

- The model is the project. Prioritize training, evaluation, and improvement; applications and UI are optional.
- Deliver a saved, reloadable trained model and held-out evaluation by the end of day one. Improve it on day two.
- Start from pretrained weights. Use Python 3.12 with uv; current pilot decisions are in `docs/plan.md`.
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
- Workstream owners self-review and self-merge bounded changes within their owned paths; routine delivery does not wait for lead approval. Subagents do not merge to main.
- Every main-checkout writer, including the lead, must use the short shared merge-lock protocol in `docs/coordination.md`. Never edit or merge into a dirty main checkout or remove another owner's lock.
- Never overwrite another worker's artifacts. Coordinate routine inputs/inference directly through public handoffs; the lead handles shared contracts, root dependencies, budget, and cross-team priorities.
- Send one final chat report per completed assignment, including the main merge commit. Interrupt only for a genuine blocker. Keep intermediate updates in shared files and continue bounded in-scope work without waiting for the lead.

## No tests or linting

- Do not write or run software tests, add test suites or test runners, or configure or run linters. This is an explicit project rule, including before commits.
- Model evaluation, dataset validation, and actual training/inference runs remain essential; they are not software test suites.

## Verification

- `uv sync --locked` installs the shared package; `uv sync --locked --extra model` includes the ML stack. Keep environments isolated per worktree.
- `uv build --no-sources` builds the package. No software test or lint steps.
- Use `uv run --locked --extra model` for model commands so uv retains the optional ML dependencies. Worker implementation and model-run evidence must be reported separately from packaging.
- Model handoff requires saved weights, a fresh-process reload, working inference, and a comparison with the starting baseline.
