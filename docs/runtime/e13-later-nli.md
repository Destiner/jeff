# E13 later exploration: native P12 NLI adapter

Source-only preparation, reusing the prospective adapter from `release-e13`.
No model, tokenizer, tensor or target-module execution was performed. No tests,
lint, network, commit, or inference run. This is readiness, not execution evidence.

## Native interface (for the parent binding owner)

Invoke `python -m jeff.runtime.nli_challenger predict --binding <native-binding>
--output-dir <new-directory>` in the separately authorized offline ML process.
The parent/common binding wraps this native binding; it is not passed in its place.

Canonical preparation files:

- `artifacts/release/e13-later-exploration-20261112-01/bindings/p12-nli.native.binding.template.json`
- `artifacts/release/e13-later-exploration-20261112-01/bindings/p12-nli.inputs.json`

The native strict `e13.nli.binding.v1` object permits exactly `schema_version`,
`candidate` (`p12-nli`), `model_id`, `revision`, `model_dir`, `research_profile`,
`assets`, `input_manifest`, `sources`, and `versions`. It does not require or accept
outer authority fields. The scientific fields were copied from actual P12
`execution-01/binding.json`, not reconstructed from a different model or invented
Model authority. Four checkout source descriptors point at this worktree and its
current bytes. The two installed Transformers implementation-source pins retain
the actual P12 environment paths; the executor must match that environment or
explicitly refresh those source descriptors to the actual identical implementation.
Do not change scientific pins to accommodate a different environment.

The input descriptor uses `path` and `sha256` (no `bytes`). Its strict
`e13.exploration.inputs.v1` document has `candidate: p12-nli`,
`validation_only_never_train: true`, `release`, `pair_map`, and `datasets`.
Release binds only `inference-handoff.json`; pair map binds only `pairs.json`.
Datasets are `e13-native` and `e13-reversed`, exactly 200 rows each, K=2.
Only these four exploration files are hashed/read, under
`artifacts/evaluation/e13-exploration-inputs-v1`; paths and their frozen hashes
are enforced before opening. No reference, confirmation, final or sibling input
is consumed. Release and pair map are hashed, not interpreted as model inputs.

## Fixed execution and counters

Exactly 400 decisions, 800 candidate pairs, 100 native forwards, four decisions
per batch (eight pairs), zero startup forwards. Each suite has 200 decisions,
400 pairs and 50 forwards. Smaller partial exploration manifests are rejected.
There is no padding replay, warmup, extra canary, retry, generation or fallback.

`receipt.json` uses `e13.nli.run.v1`. Parent consumers should inspect:

- `status`, `failure`, `binding`, `pins`, `profile`, `exploration_inputs`;
- `expected_counts`: `decisions`, `candidate_pairs`, `native_forwards`,
  `startup_forwards`, plus per-suite expected counts;
- `native_attempted`, `native_completed`, `pairs_attempted`, `pairs_completed`,
  `startup_forwards`, and model/tokenizer load attempted/completed counters;
- `suites`: name/path/hash/rows, `written_rows`, `written_probabilities`, `status`;
- `tokens`: complete pair lengths, maximum, overflow and pair count;
- `recipe` (unchanged original 624-development recipe) versus `effective_profile`
  (actual 400/800/100 execution counts and corrected resource guard);
- `resources`, `outputs`, and elapsed timestamps.

Outputs are `e13-native.jsonl`, `e13-reversed.jsonl`, `journal.jsonl`, and
`receipt.json`; successful predictions remain contract `0.1`. Attempt/completion
counters are not interchangeable. On failure, retain the journal/receipt and
partial output; do not treat partial coverage as a completed exploration pass.

## Scientific and operational invariants

Original R10 model/revision/assets, renderer, native label 0 entailment / 1
not-entailment, score z0 minus z1 at T=1, FP32 MPS, four threads and complete
pair cap 512 with truncation false remain unchanged. All complete pairs must
pass token-cap validation before model loading/scoring. No weights were read in
this preparation; runtime retains the original pinned asset audit.

The corrected prospective headroom guard is
`torch.mps.recommended_max_memory() - torch.mps.driver_allocated_memory() >= 2 GiB`.
It runs after Torch import, immediately before MPS model allocation, before every
batch allocation and forward, after forwards, and at other resource checkpoints.
RSS (including recorded peak RSS) and MPS driver allocations have separate 8 GiB
ceilings. Before Torch import, MPS values are explicitly null/not checked, not
fabricated as zero. The cooperative wall bound remains 480 seconds; the parent
must separately supervise the authorized process.

The old frozen P12 development execution and its historical free-plus-inactive
headroom-guard deviation remain evidence as originally recorded. This prospective
fix does not retroactively qualify that execution. No 624-decision rerun is
requested or authorized here; old P12 artifacts have not been modified.

## Handoff state

Template hashes bind current uncommitted source bytes. Source/core preparation
is ready; the parent must refresh native source hashes and any enclosing binding
hashes after the later integration/commit. There is no commit or ML execution
claim. Actual execution still depends on the parent/common binding, the Model
scheduler's authority, the pinned offline environment and passing runtime guards.
