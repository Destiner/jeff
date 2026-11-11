# Active coordination

## Recommended topology

Four worker sessions plus the main session as integrator. Start with 2–4 subagents per worker; expand independent data and evaluation jobs after the first pipeline works. Do not create parallel work merely to maximize agent count.

Each worker lead creates its own branch/worktree from committed main before editing. The integrator does not provision worker workspaces. Start by reading the root instructions, then move to your isolated checkout; do not implement in the root checkout. If the named branch or path already exists, inspect it and coordinate rather than overwriting it.

| Session | Branch / worker-created workspace | Owns | First task completion |
| --- | --- | --- | --- |
| Integrator | `main`, repository root | Root configuration, packaging, contracts, integration, resource allocations | Minimal Python/uv package setup; dependency requests resolved |
| Model | `worker/model`, `.worktrees/model` | `src/jeff/model/`, `src/jeff/training/`, `configs/model/`, `docs/model/` | Small actual training run, checkpoint, fresh-process predictions |
| Data | `worker/data`, `.worktrees/data` | `src/jeff/data/`, `configs/data/`, `manifests/data/`, `docs/data/` | Roughly 300 train + 60 validation examples, manifest, validation summary |
| Evaluation | `worker/evaluation`, `.worktrees/evaluation` | `src/jeff/evaluation/`, `configs/evaluation/`, `manifests/evaluation/`, `docs/evaluation/` | Baseline metrics and a prediction-file evaluator; reserved final-evaluation design |
| Research | `worker/research`, `.worktrees/research` | `docs/research/`, `experiments/research/` | Within 30–45 minutes: two candidate backbones, one recommendation, concrete compatibility risks |

Paths are ownership reservations, not claims that implementation already exists. Worker briefs are in [briefs/](briefs/model.md): [model](briefs/model.md), [data](briefs/data.md), [evaluation](briefs/evaluation.md), [research](briefs/research.md).

The integrator alone edits root files, `src/jeff/__init__.py`, shared contracts, and shared packaging. Workers report dependency requirements rather than racing to edit `pyproject.toml` or the lockfile. While waiting for packaging, research and dataset preparation can proceed; keep any temporary environment isolated.

## Launch order and gates

1. **Immediately:** launch all four workers against [contracts v0.1](contracts.md). Research does not gate data or evaluator implementation.
2. **First 30–45 minutes:** model selects a provisional backbone; data produces a tiny first shard before the full pilot; evaluation produces file-based scoring. Integrator supplies packaging.
3. **First complete run:** model trains on the pilot, saves, reloads, and writes predictions. Evaluation scores the same validation inputs for baselines and the trained model.
4. **After the loop works:** expand data, run hypothesis-driven improvements, and assign additional adversarial validation work.
5. **Day-one cutoff:** preserve the best usable checkpoint and its provenance, even if a later experiment is unfinished.

Do not wait for a perfect dataset or a definitive architecture survey. A small real run is the critical path.

## Lead decision LD002: research accepted; correct input loss first

Research commits through `59f70cf` are integrated into main. Lead independently reran both research scripts on published non-final artifacts and built the integrated package. The pilot audit reproduces 45 question-truncated pairs at 128 tokens and zero at 256, covering 360 decisions / 1,412 pairs. Review artifacts: `artifacts/lead/research-review-FjOJ4y/`. The tiny 1/3 → 0/3 result also reproduces but cannot select an architecture.

- **Model M2:** preserve the existing all-MiniLM architecture and all prior artifacts. Run one fresh `data-pilot-v1` comparison at `--max-length 256`, changing no other experimental factor: same base revision, initialization seed, data, epochs, learning rates, and batch size as `pilot-20261111-01`. Save the matching pre-training baseline, trained checkpoint, and fresh-process predictions on the same validation inputs. Publish artifacts for Evaluation; report once the bounded run and comparison are complete. The old 128-token result is retained with its truncation limitation, not overwritten.
- **Evaluation:** use the same labels and examples for the corrected baseline/trained comparison, report per-family changes and reference-label provenance, and keep final evaluation untouched. This remains within the existing evaluation remit.
- **Research R2:** next bounded task is a 30–45-minute generalization/shortcut audit of published `data-pilot-v1` train/validation data. Quantify independent source groups versus rows, template/near-duplicate overlap, answer-position or option-text shortcuts, and rule-mechanism coverage. Identify concrete limitations in what pilot gains can establish. Recommend at most three prioritized data improvements. Do not generate a replacement dataset or change labels, production code, shared contracts, or task-family reservations. Existing research-owned paths remain the only allowed edits; CPU-only, no ML jobs, no paid spend, no final-evaluation access.
- **Architecture:** retained-head MS MARCO cross-encoder is a candidate for a later controlled experiment, not an adopted replacement. No Qwen implementation, new dependencies, or extra training runs are authorized by this decision.

Model retains the local ML slot; Research uses lightweight CPU analysis only. All paid allocations remain zero. Workers incorporate the latest lead-approved main commit at a safe point and report completed tasks only, except genuine blockers.

## Initial task reservation

- Training families: `intent`, `sentiment`, `rule_application`.
- Validation: new source groups within those families.
- Unseen-family final evaluation: reserve `passage_entailment` for evaluation only.
- Evaluation also holds private in-family final cases with independently assigned source groups.
- These are initial experiment boundaries, not a claim that the model supports those tasks well.
- Changing these reservations requires coordination before generating more data.

## Compute and budget

- Model owns the initial local ML compute slot, including model downloads, GPU/MPS training, and model inference.
- Other sessions may run lightweight CPU data processing and metric computation. They must request a slot before loading a large model or starting competing ML work.
- Research can suggest runs but cannot independently launch training.
- Shared additional-spend ceiling: £50. Initial paid allocations: £0 for every worker. Existing approved agent access may be used; separately billed API calls, GPU rentals, or services require an explicit allocation.
- The integrator records allocations and actual/in-flight spend here or in a dedicated ledger before authorizing paid work. No paid jobs are launched by this scaffold.

## Artifact sharing and handoffs

All sessions use `JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts`. This is shared storage, not a shared checkout. Use team-specific, uniquely named directories; never mutate a completed artifact.

- Data writes under `data/`; model under `model/`; evaluation under `evaluation/`.
- Final evaluation stays under `evaluation/final/`. Training workers must not inspect or consume it. This is procedural isolation, not an OS security boundary.
- Each worker publishes append-only notes at `handoffs/<team>/<handoff-id>.md` under the artifact root. Put intermediate outputs and nonblocking requests here, not in chat reports. Other workers may inspect these public notes for inputs when needed; final-evaluation content remains private to Evaluation.
- Include branch and commit, deliverables, commands actually executed, metrics or failures, artifact paths, dependency requests, and costs. Distinguish proposed commands from successful executions.
- Commit logical changes on your worker branch. Do not merge or cherry-pick other workers' changes yourself; request integration.
- The integrator merges ready changes and tells workers which integration commit to incorporate. Do not continuously rebase active subagents.

No software tests or linting. Use actual builds, training/inference runs, dataset validation, and model evaluation for evidence.

## Reporting and decisions

The main session is project lead and integrator. Timur manually copies final worker reports into that session and relays decisions back. Writing an intermediate handoff file does not automatically notify the lead, and Timur is not expected to relay each milestone.

Send one final chat report when the assigned task is complete. Creating a worktree, installing dependencies, delegating subagents, or publishing the first tiny shard is an intermediate step, not task completion. Continue through your brief's acceptance criteria rather than returning control after each substep. Keep the final report concise (roughly 150–250 words); put longer evidence in the handoff artifact.

An early chat report is justified only by a genuine blocker that prevents further useful in-scope work, or a necessary authorization you cannot proceed without. Record nonblocking questions in shared handoff files and continue independent work. Do not send routine startup/progress/first-output reports.

Publish intermediate artifacts promptly so the pipeline can proceed without chat relays. When an input is needed, inspect the relevant team's public handoff directory instead of asking Timur to forward routine status. Do not inspect final-evaluation content or assume anyone is monitoring files continuously.

Use this format:

```text
TEAM / TASK:
STATUS: done | blocked
RESULT: what actually exists or changed
EVIDENCE: actual invocation and outcome; metrics with dataset/version and sample count
CODE: branch, commit, workspace, and any uncommitted changes
ARTIFACTS: absolute manifest/checkpoint/report/handoff paths
RESOURCES: compute running or released; actual and pending additional spend
DECISION NEEDED: question, options, and recommendation; or "none"
NEXT: proposed bounded next task
```

Do not include credentials, private final-evaluation examples, or invented measurements. Distinguish a claimed result from a result you reproduced.

Workers may make reversible implementation choices within their assigned scope and resources. Shared-contract changes, root dependencies, ownership/scope changes, access to another team's compute slot, and unallocated paid work still require coordination. Record nonblocking requests in files; escalate in chat only when blocked. Do not treat the absence of a reply as permission. Describe the smallest decision that would unblock you and continue independent in-scope work where possible.

The lead inspects the report and relevant code/artifacts, then responds with:

- **Disposition:** integrate, request a change, or hold.
- **Decision:** chosen option and short rationale, including remaining uncertainty.
- **Next task:** owner, objective, allowed paths, and concrete completion evidence.
- **Resources:** compute ownership and any spending allocation.
- **Sync:** integration commit to incorporate, if applicable.

Prefer evidence that advances the day-one training/save/reload/evaluation loop. Use comparisons on the same data; do not select models solely on training loss or unverifiable claims. Keep the working checkpoint while considering alternatives.

The lead records decisions affecting shared contracts, ownership, or resources in the relevant project docs and sends copyable instructions back through Timur. Model-specific rationale belongs with the model workstream. No orchestration service, shared writable task board, or automatic monitoring is required.

## If the number of sessions changes

- **Three workers plus integrator:** fold research into a time-boxed subagent under Model.
- **Five workers plus integrator:** add a validation/failure-analysis worker after Evaluation has a working pipeline. Give it a disjoint directory and validation-only data; do not add a second trainer or an early UI workstream.
- **Three sessions total:** integrator also handles evaluation; one worker owns model plus research; one owns data.

Within each session, subagents need disjoint tasks and edit scopes. Use additional isolated worktrees for independent code-writing subagents, or serialize integration through the session lead. Never let several subagents edit the same mutable files concurrently.
