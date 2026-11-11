# E5 frozen-decoder comparison — deferred CPU preparation

**Prepared, not executed.** No Runtime predictions have been scored. No model/tokenizer load, inference, download, network call, training, build, test or lint command was performed. Only existing development artifact/code reading, SHA-256 hashing and reference/mapping counts were performed. Everything new is confined to this directory; no tracked edits or source exports.

## Deliverables

- `run.py`: standard-library orchestration of existing `study`, `compare`, `order`, `render` and the existing source-unit supplement. Requires three explicit real prediction files and both frozen recipe and execution receipt evidence files. There are no default prediction paths, synthetic data or execution on import.
- `preparation-lock.json`: 84 preparation-time dependency hashes: original E3 config and its declared references, encoder predictions, label-free sources and receipts; stored baselines; current Evaluation code; reviewed unit mapping; original supplement and E3 summary; orchestration script and inventory. Every pin is rechecked **before creating a run directory** and again before completion. The study also checks its own dependencies before/after scoring.
- `reuse-inventory.json`: exact reference counts, family/label-basis/group counts, reviewed mapping coverage and unit counts; all three exact input universes from `e5-p3-input-binding-v1/inputs.json`. This is an inventory, not an outcome report or checkpoint attestation.

## Future exact invocation

Only after Runtime publishes its immutable real outputs, substitute the actual absolute paths below. This command is intentionally **not run** during preparation. Use the already installed Evaluation Python; no uv sync, dependency installation or network is needed.

```bash
cd /Users/destiner/Code/jeff/.worktrees/evaluation
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  /Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/run.py \
  --original300 "$RUNTIME_ORIGINAL300_PREDICTIONS" \
  --reversed300 "$RUNTIME_REVERSED300_PREDICTIONS" \
  --probes24 "$RUNTIME_PROBES24_PREDICTIONS" \
  --frozen-recipe "$RUNTIME_FROZEN_RECIPE_EVIDENCE" \
  --execution-receipt "$RUNTIME_EXECUTION_RECEIPT" \
  --output-dir /Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01
```

All five variables must identify existing **real files**. Add repeatable `--evidence /absolute/path` arguments for actual immutable prompt/scorer code, token-boundary/length audits, error logs or runtime measurements not contained in the two mandatory evidence files. The wrapper hashes these files without interpreting their claims; it never opens model/tokenizer artifacts. Do not pass weight/tokenizer files as evidence.

Before invocation, the Evaluation owner must review Runtime's actual recipe publication and receipt: R1-pinned model/tokenizer revision, prompt/chat template and answer-symbol mapping, conditional scoring/normalization, code hash, label-free token-boundary/length audit, no silent truncation, chosen cap and explicit overflow/failure records; exact three input/output hashes; evidence the recipe was frozen before predictions. Attach available load/warm inference/backend/memory observations with qualifications. A byte hash or mtime is **not** proof of pre-outcome chronology, an untouched checkpoint, execution authenticity or complete file dependency provenance. This wrapper does not manufacture such attestation, require a new attestation schema, or make cosmetic timing completeness a quality-scoring gate.

The output must be a new descendant of this exclusive directory. Nothing is created by `run.py` until required paths exist and all frozen preparation hashes match. Any fatal command leaves immutable partial outputs and command receipts; use a new execution directory after resolving the cause. Dependency drift is a reason for owner review and a separately versioned preparation, not bypassing pins or rewriting completed reports.

## Exact reuse and private mapping

| Existing stratum key | Report population | Reference rows | Source groups | Order pairs |
|---|---|---:|---:|---:|
| `inherited-v1` | inherited60 |60|12|60|
| `new-v2` | new240 |240|170|240|
| `probes` | probes24 |24|12|12|

These **only three** strata retain E3 keys because the reviewed mapping binds those keys. There is no combined300 quality report or combined headline. Original300 and reversed300 are source universes, not additional quality strata. The inventory records family counts without inventing policy/mechanism membership from IDs.

The six encoder predictors remain exactly those in E3: M4 MiniLM random-head start/trained, M4 MS-MARCO pretrained start/trained, retained M2 and M3. All neural source lists, source-universe bindings and historical-reuse evidence are copied unchanged from `configs/evaluation/e3-m4-v1.json`. No old encoder inference is requested. Both **stored** E3 `uniform`/`lexical` prediction and order files are reused byte-for-byte, not regenerated; their schema-compatible `historical-retained` role means non-neural artifact reuse, not a checkpoint claim. The decoder uses schema role `fresh-start`: pretrained and instruction-tuned but untouched by Jeff learning, **not random/untrained pretraining**.

The wrapper binds original300 predictions to exactly `v2-original` and reversed300 predictions to exactly `v2-reversed` from the existing input-binding document, then lets study filter by known private reference identities and use existing exact pair definitions. It does not derive reversal IDs from suffixes or export labels. Probes24 already has 12 reversal pairs: its same single prediction source is used for both quality and order; **never reverse it again**.

Study bundles raw prediction records, retains unidentifiable/malformed records and unknown extras, and audits every known-universe exclusion in `subsets.json`. Missing, invalid, duplicate, extra and failed predictions remain visible. No perfect coverage requirement: the existing study accepts comparison/order status 1 when a report was produced. Raw files remain authoritative; shared scoring only applies its existing tiny sum-tolerance normalization, not temperature fitting or error repair. Fatal invalid references/IO failures are not treated as ordinary coverage gaps.

## Future outputs and report plan

1. `preflight.json` hashes all supplied real evidence/predictions plus locked dependencies before scoring; `recipe.json` uses the existing **`e3-study/1`** schema honestly. Existing study emits cosmetic E3 titles in its completed `study/*/report.md`; those files are never changed. Separate `E5-*.md` reports are rendered with the existing renderer and explicit E5 titles.
2. Each stratum comparison includes nine predictors; per-family, source-group and label-basis results; supplied teacher/source provenance and family/group denominators; conditional agreement and all-row failure-as-unsuccessful agreement; natural-log loss, sum-over-options Brier, ties, coverage/failure counts and raw outcome diagnostics. Teacher agreement remains distinct from rule-verified correctness. The current renderer does not display Brier in Markdown; cite the existing comparison JSON's `overall.brier` and grouped Brier in the owner's synthesis, rather than claiming the Markdown already includes it.
3. Exact order reports include complete-pair denominators, choice consistency including/without ties, original/reversed quality, TV and per-pair maximum probability change. `exact-order-margins.json` supplements **the same shared-scored outcomes** with exact flip identities, original-choice-anchored probability margin on each presentation and target margin on each presentation. Incomplete pairs have no invented margins; tied flips are not mistaken for probability changes. Reversals are repeated measurements, not independent observations.
4. The unmodified `e3-source-unit-analysis-v1/summarize.py` consumes the three newly saved comparisons and exactly `e3-release-identity-review-v1/validation-source-units-reviewed.json`. Its policy-instance/mechanism/domain/producer/source-group breakdowns reuse per-case outcomes through shared `metrics.summarize`, with equal-known-unit agreement/loss macros, Brier and coverage inside JSON unit metrics. Unknown mapping rows are explicit, not inferred from case IDs; wholly absent expected units and undefined/infinite losses remain visible. Overlapping dimensions are not added together. `e3-m4-source-units-v1/summary.json` is pinned reference evidence only, not modified or mislabeled as a fresh execution.
5. Owner synthesis should describe where the frozen decoder helps/fails across the three populations, families, reviewed policies/mechanisms and label provenance; qualify reused development data, correlated rows, incomplete coverage and unknown metadata. Include actual P3 runtime observations with measurement limits. Answer whether another **bounded future decoder learning experiment** appears warranted on this evidence, without a preregistered numeric threshold (none exists), post-outcome success criterion, default promotion or claim that learning has occurred. The script deliberately does not automate this recommendation.

## Interpretation and limits

- Probabilities are normalized conditional probabilities over supplied answer symbols/options, subject to Runtime's actual frozen scoring recipe; they are **not calibrated confidence**. Descriptive reliability bins are not calibration evidence.
- Different capacity, pretraining, instruction tuning, prompt, context budget and runtime make this a **practical systems comparison, not an architecture ablation**. The MiniLM random head is explicitly weaker/different from a pretrained reranker or instruction model.
- This is existing development/validation only. No final data access, fresh inference, new exports, prompt search, learning, framework changes, new dependencies or external spending. D3/E4 is independent and not blocked by this preparation.
- This script has been read/reviewed but **not executed or tested**. There is no `execution-*`, generated scoring recipe, decoder outcome, completion receipt or inference result in this preparation. An actual run can still expose IO/schema/reporting limitations; preserve the evidence and report them honestly.
