# Worker: Time-boxed research

**LD004 ownership update:** you are the workstream owner, not a worker awaiting lead review. Self-review and self-merge completed changes within the paths below, using the shared lock/build protocol in `docs/coordination.md`. Current assignments in that file supersede the initial milestone below. Coordinate directly with other owners and continue bounded in-scope work without waiting for lead approval. No software tests or linting. Report final delivery with the main merge commit.

Create your own `worker/research` branch and `.worktrees/research` worktree from committed main before editing. Do not implement in the root checkout, overwrite an existing workspace, or create workspaces for other leads.

Read `AGENTS.md`, `docs/coordination.md`, and `docs/contracts.md`. Work on `worker/research` in `.worktrees/research`. Do not write or run software tests or linting.

## Mission

Reduce consequential uncertainty quickly. Advise the active implementation; do not become a prerequisite for the first training run or produce an exhaustive literature survey.

## Ownership

Edit only `docs/research/` and `experiments/research/`. No production model/trainer changes, root dependency changes, or unallocated ML runs. Generated research outputs use a unique `research/<id>/` directory under the shared artifact root.

## First milestone: 30–45 minutes

Recommend one starting backbone and one fallback. Compare:

- Pretrained text encoder plus candidate scorer versus a small decoder-style alternative.
- Actual Apple silicon backend support, required dependencies, and likely memory constraints on 16–24 GB.
- Whether a starting checkpoint already understands question/answer or semantic matching well enough to offer a useful baseline.
- Model/license terms, download size, tokenizer behavior, and checkpoint portability.
- A minimal supervised objective and the simplest viable trainable parameter strategy.

Use primary documentation and model cards. Cite sources and distinguish measured facts from estimates. Do not quote cloud training timings as laptop estimates.

Publish an actionable recommendation in the shared handoff directory as soon as available, without a separate intermediate chat report. If evidence is incomplete, give a provisional choice and a specific cheap experiment to resolve the uncertainty.

## Suggested subagents

- Encoder/candidate-scoring options.
- Small decoder and local training-backend options.
- Evaluation/generalization pitfalls and suitable public data sources.

Limit each investigation. Do not independently download several large models or run competing training jobs; request a compute slot.

## After the recommendation

Switch to the most valuable concrete follow-up: analyze published validation results, investigate a specific bottleneck, or propose one controlled improvement. Keep production changes with their owning worker. No UI work unless explicitly reassigned.

## Handoff

Publish `artifacts/handoffs/research/<id>.md` in the shared root with branch/commit, recommendation, supporting URLs, uncertainties, and suggested next experiment. Separately billed services require an allocation; no paid work is authorized initially.

Send one final chat report when the assigned time-boxed research task is complete. Report early only if genuinely blocked; do not report startup, delegation, or each individual finding as separate completed tasks.
