# P13 — M12 strict v2 checkpoint runtime

**Completed and Model-verified closed, not promoted.** This publication indexes existing metadata for `artifacts/release/p13-m12-20261112-01/`. The [release manifest](../../manifests/releases/p13-m12-20261112-01.json) preserves exact receipt/output SHA-256 descriptors, without rereading prediction payloads or weights or performing new scoring.

## Actual Runtime pass, separate from training

The retained execution comprises **one audit and one strict M12 v2 fresh reload**: **627 attempted/completed native calls = 3 established startup forwards + 624 scored decisions**, producing **2,390 probabilities**. Original/reversed development each contain 300 presentations; already-paired probes contain 24. There is **no D3**, extra START pass, canary, retry or fallback. Recorded loading diagnostics contain four empty lists; these are actual retained reload evidence, not independent tensor replay or proof of per-case full-pipeline equivalence.

Runtime source is `f75d72bd1487f9cf874aa48231233840881573fc`, profile **m12**, head LR **2e-4**, with Model **590s** and Runtime **310s** sublimits. The producer separately records **4,500 attempted/completed backbone calls**: 1,500 START, 1,500 TRAIN and 1,500 FINAL, with 375 updates. Those producer calls are not P13 calls. The original M8 endpoint remains unchanged; M12 is a fresh original-P3 frozen-backbone independent-head contrast, not a continuation or replacement of M8.

| Accounting scope | Seconds |
|---|---:|
| Runtime handoff outer duration | 42.49650995898992 |
| Saved outer-publication event | 42.496176874730736 |
| Conservative Runtime charge | 44 |
| Producer audit + training/export | 264.20991725102067 |
| Charged chain / ceiling | 308.20991725102067 / 900 |

**Timing qualification:** the handoff and located publication event are different recorded values; Model/E15 explicitly retain that discrepancy. Both support the unchanged conservative 44s charge, not a controlled speed comparison. All supervisor/audit/predict groups are recorded absent, with zero exit and a returnable slot. Model closure reports maximum normalization error `1.257285475730896e-07`. Unused time authorizes nothing.

## Interpretation and preserved qualifications

[Model M12](../model/m12-head-lr-results.md) and [independent E15](../evaluation/e15-head-learning-rate.md) own scientific interpretation. Stronger head LR improves aggregate TRAIN probability loss but reduces agreement; development proper-score gains coexist with worse choice retention and order robustness. New native/reversed agreement is 121/113 of240, with both-correct 86→75 versus M8; probes lose four previously both-correct pairs. This is **not an LR rescue**, convergence proof, capacity verdict, calibration result or promotion. E16's reversal mean is a separate two-forward decision rule, not a rewrite of raw M12/P13.

The initial producer failure receipt is an incomplete-start sentinel, not a completed zero-update terminal failure. Original controllers, review timing and later adopted cancellation-gap fix remain qualified in Model's report; completed receipts do not retroactively establish independent approval. The tokenizer warning remains: matching saved prompt hashes/lengths/answer IDs on these cases does not prove general harmlessness. FINAL projection comparisons share a hidden state, not an independent full-pipeline rerun. Backend-specific nonaliasing evidence is not a generic Metal storage guarantee.

Runtime's recorded 8GiB RSS/driver and 2GiB recommended-headroom guards are distinct from Model's guards. Sampled driver, lifetime RSS and recommended headroom are overlapping, nonadditive scopes, not continuous peaks or physical free RAM. Reused development, teacher/reference agreement, same-alias rule checks and unknown reviewer revisions remain qualifications. E15 retains all family/source/arity/retention regressions and preparation-copy history.

## Canonical evidence

- Root: `/Users/destiner/Code/jeff/artifacts/release/p13-m12-20261112-01/`.
- Terminal closure: `/Users/destiner/Code/jeff/artifacts/model/m12-qwen-head-lr-20261112-01/p13-return.json`, resolved from public Model metadata rather than the suggested `night-20261112` directory.
- Manifest pins packet, delivery summary, process receipt, outer receipt/publication, audit receipt, native run receipt and three prediction output descriptors. Old pending/preparation records do not override terminal closure and are not removed.

Source review and the publication package build alone are not proof of native execution or quality. This task changes only the named new documents/manifests; no evidence/executed-tree changes, ML/tokenizer imports, weight reads, protected final/reference/input access, new scoring, tests/lint, network or experiment.
