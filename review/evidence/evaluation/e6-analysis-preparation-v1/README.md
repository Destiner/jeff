# E6 deferred analysis preparation

Prepared without reading M6 start/training or P4 trained outcomes. `run.py` has **not been executed**, imported, syntax-tested, linted, or exercised with fixtures. Only actual frozen metadata/pin/count collection was executed with the project interpreter. No tracked changes, model/tokenizer loads, weight scans, network, mailbox, or final access.

## Future invocation — only after real outputs and evidence exist

Replace each shell variable below with an absolute real file path. Evidence may be repeated for actual Model and Runtime receipts, immutable recipe/code/audit/lineage evidence; no invented receipt schema is required. Do not supply weight files or TRAIN rows. Keep training-fit summaries separate for later reporting.

```sh
PYTHONDONTWRITEBYTECODE=1 \
/Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python \
  /Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v1/run.py \
  --start-original300 "$M6_START_ORIGINAL" \
  --start-reversed300 "$M6_START_REVERSED" \
  --start-probes24 "$M6_START_PROBES" \
  --trained-original300 "$P4_TRAINED_ORIGINAL" \
  --trained-reversed300 "$P4_TRAINED_REVERSED" \
  --trained-probes24 "$P4_TRAINED_PROBES" \
  --evidence "$MODEL_REAL_EVIDENCE" \
  --evidence "$RUNTIME_REAL_EVIDENCE" \
  --output-dir /Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v1/execution-01
```

The output must be a **new descendant** of this E6 namespace. Use `execution-02` rather than retrying a partial directory. Files are created exclusively. Dependencies are checked before outcome files are read/hashed and again before completion. Pin mismatch stops the run: preserve and explain it, do not silently repin after outcomes. Small-file limit 16 MiB prevents accidental checkpoint hashing; no directory or weight inventory scan.

## Reuse and outputs

- Copies the already-configured `configs/evaluation/e5-p3-v1.json`, preserving all nine E5 arms (P3 Qwen, both encoder starts/trained arms, M2/M3, stored uniform/lexical), plus M6 fresh start (`fresh-start`) and P4-trained M6 (`v2-trained`): **11 predictors in each of the same three strata**. No baseline regeneration.
- Uses exactly frozen original300/reversed300/probes24, total624, with no inference export, new reference contents, or new probe reversal. Strata remain inherited60/new240/probes24; no combined300 headline.
- Existing `study.py` owns raw-record bundling, known-universe out-of-stratum exclusions, malformed/unknown/duplicate/extra audit, shared scoring, comparison, order, and rendering. See `study/subsets.json`, command receipts, comparisons and order reports. Failures remain unsuccessful in all-reference agreement denominators; proper losses remain valid-only with explicit coverage. No complete-case-only headline.
- Existing `order.py` already emits `original`, `reversed`, `paired_quality`, `prediction_report.outcomes`, family/group pair metrics and per-pair stability/correctness. The supplement consumes these; no new scorer or reversal dataset. All original/reversed outcomes remain authoritative in order reports.
- `grouped-both-order-summary.json`: every predictor by orientation/family/family×label-basis/source group and reviewed producer/domain/mechanism/policy, plus every pairwise predictor change, including start→trained and both versus P3. Actual API is `compare.paired_comparison` (imported from metrics), **not** a `compare.paired` function. Reuses `metrics.summarize` and `order.pair_summary`. Delta signs are left-minus-right; inspect names. Exact case contributions include NLL/Brier/agreement, status and common-valid denominators; infinite-side NLL is explicit rather than subtracted as a finite number. Groups and orientations are never pooled.
- Reversal metadata is mapped through frozen pair definitions to original IDs and reviewed E3 units, never ID suffixes. New rules retain40policy/10mechanism units and new intent8domains; unknown metadata is explicit, not inferred. Dimensions overlap and are not independent. Both-order pair metrics include flips (complete pairs minus same-choice numerator), tied/untied stability, TV and original-only/reversed-only/both/neither correct. Inspect intent and every family, not only new rules. Probe macro retains all12paired groups and24presentations with per-pair coverage/proper scores and stable-correct counts; no iid assertion.
- `fresh-start-vs-p3-exact-differences.json`: raw option-ID probability differences for all common-valid cases, full sorted absolute-difference distribution/max, choices/ties/new ties and coverage. No gap is converted to equality. Existing shared scoring accepts and normalizes sum roundoff within1e-6 (reported by existing scorer); exact equivalence differences use **raw** accepted output probabilities, not normalized outcomes. The new script never repairs predictions.
- `E6-*.md`: existing renderer for all three strata. Detailed orientation/source-unit contributions are in the JSON supplement and order reports, not a replacement scoring framework.

## Identity binding and limitations

Evidence file bytes are pinned, **not semantic or loaded-weight attestation**. Owner must inspect their actual schemas and bind all six files to exact input IDs/hashes, intended checkpoint/output identities, start-weight lineage and saved-checkpoint evidence. Review actual tokenizer/environment/code, official prompt/chat template, complete A–F boundary-token mapping, allowed-symbol T1 normalization, cap1024/no truncation, FP32/MPS/eval/no-gradient/batch1/four-thread controls. Code hashes alone cannot establish equivalent scoring semantics. Incomplete/mismatched evidence qualifies comparisons; it is not a reason to drop bad outcomes or substitute controls.

Numerical reference is max absolute probability difference≤1e-6, unchanged untied choices and no new ties, with full coverage. It is only a reporting reference; semantic equivalence always remains owner-reviewed. Exact equality is separate. Diagnostics including unknown/unidentifiable records must accompany this reference; a probability comparison does not erase them.

Training summaries are deliberately not consumed, created or diagnosed. Later keep fixed-checkpoint before/after TRAIN-fit summaries separate from changing-weight averages and held-out behavior; verify final checkpoint/375updates/1500presentations/permutation recipe/reset evidence from provided summaries without opening TRAIN rows here.

No formal pass score, significance, calibration, architecture/permutation-only causal claim, automatic promotion, temperature fallback or new evaluation data. Shared summarize includes descriptive reliability fields; their presence is not a calibration conclusion. A narrow probability improvement is not necessarily ranking or transfer improvement. Preparation is unexecuted code, not an execution-success claim; partial failures retain their namespace and receipts.
