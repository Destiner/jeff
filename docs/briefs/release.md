# Release / Runtime workstream owner

## Role and mission

Make an existing Jeff checkpoint straightforward to package, obtain locally, install, and run outside the development checkout. You own portable delivery and honest runtime evidence, not model selection, training, a UI, or a second inference implementation.

Read current root `AGENTS.md`, `docs/coordination.md`, `docs/contracts.md`, and `docs/owner-lifecycle.md`. Create your own `worker/release` branch and `.worktrees/release` worktree from committed main if absent; if they already exist, inspect and adopt them without resetting someone else's work. This is a new team, not a replacement for another active owner.

## Code boundary

Allowed tracked edits:
- `src/jeff/runtime/`
- `configs/runtime/`
- `scripts/release/`
- `manifests/releases/`
- `docs/runtime/`

Use unique immutable `artifacts/release/<id>/` outputs and `artifacts/handoffs/release/<id>.md` notes. Do not change Model's scorer/checkpoint format, trainer, Data/Evaluation code, labels, root packaging/lockfile, or shared contracts. Coordinate necessary changes with their owners. Root README changes can be proposed to the lead without blocking your owned documentation.

## Initial mission P1

Deliver one reusable local checkpoint-export path plus an actual cold-start execution:

1. Package the existing M2 all-MiniLM 256-token trained checkpoint first, without modifying its source artifact. This is a known working reference, not a declaration that it is the best model.
2. Produce an immutable bundle and a small manifest with architecture/model revision, exact checkpoint file inventory/hashes, code/package version, dependency requirements, provenance, and applicable license notices. Keep loading semantics and model probabilities unchanged. Include the project wheel or an explicit reproducible package-install recipe.
3. Reuse the existing inference CLI/loader. Prefer standard-library export/inventory tooling; do not introduce a server, alternate model framework, or unnecessary dependency.
4. Copy/unpack the bundle into a fresh directory outside the repository. Install in an isolated environment and run real inference with original checkout paths and original model cache unavailable. Use an empty model cache and offline model-loading flags. Coordinate this model-loading run with Model first.
5. Record the actual invocation, platform/Python/dependency versions, bundle size, cold-start duration, prediction coverage, and any measured memory with clear scope. Compare the same input's probabilities with the source checkpoint when feasible; do not invent portability or equivalence claims.
6. Exercise the same export path for the existing M3 retained-head architecture if it fits the bounded assignment, so the bundle is not hardcoded to one layout. Keep the two candidates separately identified.
7. Document short portable install/run commands and meaningful limitations under `docs/runtime/`. Build, self-review, and self-integrate the owned changes.

The distinction matters: package installation may download Python dependencies; inference must not silently fetch missing model weights or depend on the author's caches. Do not claim fully offline installation or unexecuted platform support. Prefer a CPU deployment recipe where practical, without accidentally requiring a large CUDA stack.

## Inputs already available

Consult current Model public handoffs for exact checkpoints and code revisions. At assignment creation:
- M2 checkpoint: `/Users/destiner/Code/jeff/artifacts/model/pilot-256-20261111-01/checkpoint`.
- M3 checkpoint: `/Users/destiner/Code/jeff/artifacts/model/msmarco-256-20261111-01/checkpoint`.
- Existing inference entry point: `python -m jeff.model.predict`.
- Operational reference: `docs/model/README.md`.

Use small explicitly synthetic demonstration inputs or existing approved label-free development inputs, not protected final data. Do not present demonstration outputs as accuracy evidence. The reported M3 pilot gain coexists with a probe regression; do not pick or switch the default model on pilot score alone.

## Packaging safety and distribution boundaries

Only include intended checkpoint/package/license/demo files. Do not sweep entire workspaces, caches, environment files, credentials, training data, private paths, or protected evaluation artifacts into a bundle. Keep bulky weights/archives outside Git; commit only small code/docs/manifests. Refuse overwrite of completed bundles. Handle archive extraction paths safely if implementing an extractor.

Do not upload to Hugging Face, a registry, cloud storage, a public repository, or hosting service without explicit authorization. Local release preparation is authorized; external publication is not. Preserve upstream model license obligations and distinguish model licensing from the training-data/provider terms; do not declare all artifacts public domain.

## Authority and resources

You own bounded planning/delegation, review, and in-scope self-merges under the shared lock/build protocol. Delegate separate export, runtime-install, and documentation investigations if useful, but only one owner integrates.

Lightweight CPU packaging/hashing is allowed. Model owns substantial inference/model loading: request a short cold-start verification slot directly; Model can execute the run or explicitly grant a bounded slot. Do not load a second model unannounced or start training.

Paid allocation is £0. No software tests or linting. Actual export/install/inference and package builds are delivery evidence. No final-evaluation access.

## Delivery

Publish useful intermediate artifacts and requests in shared handoff files. Send one final concise report with main merge commit, bundle/manifest paths, executed cold-start evidence, licensing/runtime qualifications, resources, and next bounded step. Early chat only for a genuine blocker. Do not require routine lead approval to complete owned work.
