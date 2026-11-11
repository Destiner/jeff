# M4: frozen-v2 robustness comparison

## Question and decision rule

Does training on Data's broader v2 scenarios improve each existing candidate beyond its own fresh pretrained start, without concealing regressions on inherited validation or independent development probes? Compare the already-supported all-MiniLM mean-pool/random scalar head and retained-head MS MARCO cross-encoder. Neither architecture is presumed the winner. Preserve M2/M3 weights and predictions and leave the CLI default unchanged.

The primary stratum is **newly authored v2 validation**, with reference-label agreement and log loss, per-family and source-group breakdowns. Report inherited-v1 validation and independent probes separately; do not mix them into one headline. A candidate improves against its own start only if new-v2 agreement increases and log loss decreases. Call it a robustness improvement over its corresponding v1-trained predecessor only if that improvement also has no family-level agreement or log-loss regression on inherited/probe strata; otherwise describe the trade-off explicitly. This is a descriptive gate, not a statistical significance or promotion claim. One seed, synthetic source dependence, teacher labels, and repeatedly used development sets prevent broad generalization/calibration claims.

M3 previously scored40/60 on the pilot but8/24 on probes, versus M2's35/60 and16/24. It must not be promoted by pilot score alone. No training examples or derivatives may be created from these evaluated cases.

## Input release gate

Data owns immutable training/validation release and historical-exclusion evidence. Evaluation owns stripping labels and validating inherited/new identities. Research advice is useful, not a required sign-off gate.

As of initial preparation, `data/data-pilot-v2/pre-review-r2/manifest.json` is **candidate-only, not training authorization**; manifest SHA256 `345e935b46ca3d1226dfd603208bf5d1e1e16982d425319f678e34447b0c9483`. It has1500 train/300 validation:300/60 inherited and1200/240 new. These counts must be rechecked against Data's final release; no candidate is silently substituted for it.

Before the first training run:

1. Record Data's published final manifest/hash and validator, quality-review, historical tiny/v1 validation-exclusion receipts. Require unchanged inherited validation; group/hash checks cannot prove all semantic derivatives absent. Preserve any uncertainty.
2. Check full serialized candidate-pair lengths with **both exact tokenizers** on the released bytes. Use one common supported cap that loses no text; fail/coordinate rather than silently truncate. Existing Research CPU audit is reused, with no neural model load.
3. Freeze recipe, input hashes and artifact IDs in a public Model handoff. Require a clean committed code revision. Validate actual steps and exposure after each run.
4. Obtain Evaluation's frozen decision-only v2 validation/order inputs and existing probe inputs. Never inspect reserved final content.

Candidate-only audits were actually executed on both saved baseline tokenizers:6848 pairs, max169 complete tokens, p95=96, zero overflow/question/candidate loss at256. Reports: `artifacts/model/m4-readiness-20261111-01/{minilm,msmarco}-candidate-token-budget.json`. This supports a tentative256 cap, **not permission to skip the final-release audit**.

## Matched bounded recipe

Reference settings are in `configs/model/m4-v2-comparison.json`; this is not a CLI-loaded config.

- Fresh original pinned pretrained sources, not M2/M3 fine-tuned weights. all-MiniLM explicitly resets the scalar head; MS MARCO retains its pretrained head.
- Same final split, seed42, decision batch4, three full epochs, explicit shared update cap `3 * ceil(train_rows / 4)` (1125 if1500 train rows), 4500 presentations if1500 rows.
- Same AdamW backbone/head learning rates2e-5/5e-4, weight decay0.01, no scheduler/calibration/early stopping. Four Torch CPU threads, local MPS. Fail rather than silently fall back to CPU.
- Same audited cap; tokenizer/formatting differences and realized padding cost remain recorded. Mean pooling versus native pooled-CLS/dropout, head initialization, and pretraining objective differ by design. Same seed does not guarantee identical dropout or deterministic MPS kernels.
- At most **one v2 training invocation per architecture**, sequentially under Model's sole local ML queue. Failed runs remain preserved; no automatic retry, tuning sweep, or recipe change after seeing results. Fifteen-minute supervision limit per training process; expected runtime materially below that from prior measured throughput. Stop on nonfinite/OOM rather than scaling resources.
- No new dependencies, architectures, dataset edits, paid calls/jobs, software tests or linting. £0 allocated/actual/pending additional spend.

M4 is not a pure data-only causal ablation versus v1: the data mixture, groups and number of updates all change. Matching budgets between architectures does not make their pretraining or compute identical.

## Delivery and independent review

Each run preserves its own baseline, trained checkpoint, manifest copy and `run.json` (code/source hashes, revisions, dataset hashes, optimizer, changed weights, metrics, resource measurements). Complete local safetensors/tokenizer artifacts must reload in fresh offline processes. Report CPU high-water RSS separately from point-in-time MPS allocation, never as a measured GPU peak.

Publish hashed predictions for each M4 baseline/trained snapshot on Evaluation's full v2 validation, requested reversal inputs, and independent probes. Full-v2 predictions can be subset by IDs into inherited/new strata by Evaluation; do not independently rebuild its labeled reference files. Existing M2/M3 pilot/probe predictions are reused; infer preserved v1-trained models on new validation only if requested/useful for same-reference comparison. This is not a repeat of training M1–M3.

Evaluation reuses its compare/order/report pipeline for uniform, lexical, pretrained/random-head starts, both trained M4 candidates, and optional historical references. Model records actual pipeline evidence separately from package builds. No new default is selected automatically. Self-review and integrate only owned paths using the atomic main merge lock and integrated build; final handoff includes exact implementation/main hashes, artifacts, outcomes, limitations and released queue.

## Initial preparation evidence

Existing clean `worker/model` / `.worktrees/model` adopted after Timur explicitly transferred ownership. Fast-forwarded f8c90c6→5ee2b18, then17e9e0a. No active ML processes found and old subagent worktrees retained. Fresh narrowly scoped read-only subagents assessed trainer controls and candidate readiness; no trainer changes needed. Main's current M4/E3 direction governs direct coordination. Public request: `artifacts/handoffs/model/20261111T1123-M4-owner-adopted-and-input-request.md`.
