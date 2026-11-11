# E6 — the single decoder-learning contrast

2026-11-11. Final M6 checkpoint versus its fresh starting control; independent Runtime P4 outputs. [Frozen analysis plan](e6-plan.md), [executed recipe](../../configs/evaluation/e6-m6-v1.json), [hash-linked evidence index](../../manifests/evaluation/e6-m6-report-v1.json).

## Conclusion

**Negative learning result for this bounded final-checkpoint recipe; no promotion or default change.** Relative to its fresh starting control, M6 loses agreement in both orientations of both broad strata, loses all both-order successes, and flips every paired choice. Intent and probe retention fail. This does not support successful learning under the demonstrated combined supervised-learning plus frozen TRAIN-permutation recipe on these development populations; it does not reject every decoder or permutation training in isolation. No causal diagnosis is identified. No best checkpoint, fitted score threshold, new conjunction, retuning or experiment is introduced.

Fresh start and preserved P3 are exactly equal on all saved case/option probabilities; every fresh contrast below is therefore also the P3 contrast. Strong saved-output/semantic-control comparability is supported by the existing start-control and P4-binding reviews, not independent historical loaded-tensor attestation. Prior E3/E4/E5 conclusions remain unchanged. Parallel Model/Data audits are not an approval gate.

## Populations, coverage and arithmetic

Inherited: 60 cases / 12 source groups; new: 240 / 170. Original and reverse reuse the same cases. Probes are separate: 24 presentations / 12 curated pairs, four pairs per family, teacher-only. Combined300 is not an independent sample or a pooled performance claim. Family, label-basis, domain, producer, mechanism, policy and source-group dimensions overlap. Even source-group/domain/producer grouping is coarse and leaves dependencies; no significance or independence assumption is made.

All 11 predictors are retained in each stratum: M4 MiniLM pretrained-encoder/random-head start and trained, M4 MS MARCO pretrained start/trained, M2, M3, uniform, lexical, preserved P3, M6 fresh, M6 final. Coverage of 33 quality and 33 order reports is complete. Every assembled presentation is valid; missing, invalid, duplicate, extra, malformed/unidentifiable record diagnostics are zero. All target probabilities are positive; no infinite NLL or dropped zero-target row. Valid and failures-as-unsuccessful agreement denominators coincide. The independent arithmetic review records 24,797 checks, zero discrepancies (actual-data analysis, not a software test suite).

NLL = mean natural-log −log p(target); Brier = mean sum over options of (p−onehot)², not divided by option count. Following the unchanged core, only already-valid roundoff-level sums are normalized for scoring; no output file is changed or probability repaired. Raw probabilities, rather than rounded report cells, determine choices/ties. Every independent per-case calculation agrees with core outcomes within 1e−12; aggregate comparisons use the same arithmetic tolerance, not a promotion threshold. Full precision and source JSON pointers are indexed below.

## Primary contrast, each orientation

| Population | Order | Predictor | Agreement | NLL | Brier |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | original | fresh = P3 | 35/60 | 1.194707 | 0.599128 |
| inherited-v1 | original | final | 17/60 | 1.442884 | 0.778014 |
| inherited-v1 | reversed | fresh = P3 | 34/60 | 0.966733 | 0.537541 |
| inherited-v1 | reversed | final | 13/60 | 1.472594 | 0.803253 |
| new-v2 | original | fresh = P3 | 129/240 | 1.312350 | 0.633492 |
| new-v2 | original | final | 65/240 | 1.413320 | 0.779200 |
| new-v2 | reversed | fresh = P3 | 118/240 | 1.410621 | 0.687402 |
| new-v2 | reversed | final | 65/240 | 1.407130 | 0.778134 |
| probes | original | fresh = P3 | 9/12 | 0.649621 | 0.317726 |
| probes | original | final | 4/12 | 1.175404 | 0.726504 |
| probes | reversed | fresh = P3 | 11/12 | 0.419398 | 0.251247 |
| probes | reversed | final | 4/12 | 1.172018 | 0.749054 |

The important exception is **new reversed NLL**, improving slightly from **1.4106206775423604 to 1.407130039288739** (Δ −0.0034906382536215), while Brier worsens **0.6874023517504078 → 0.7781339061775513**, agreement falls 118→65/240 and both-order success vanishes. It is incorrect to say every proper loss worsens. Smaller NLL or total variation alone is not ranking or robustness improvement.

## Choice robustness and retention

| Population | Predictor | Pairs | Flips | Both | Original only | Reverse only | Neither | Mean TV | Max Δp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| inherited-v1 | fresh = P3 | 60 | 19 | 28 | 7 | 6 | 19 | 0.244710 | 0.780268 |
| inherited-v1 | final | 60 | 60 | 0 | 17 | 13 | 30 | 0.190760 | 0.310205 |
| new-v2 | fresh = P3 | 240 | 122 | 82 | 47 | 36 | 75 | 0.330491 | 0.947695 |
| new-v2 | final | 240 | 240 | 0 | 65 | 65 | 110 | 0.206962 | 0.310961 |
| probes | fresh = P3 | 12 | 2 | 9 | 0 | 2 | 1 | 0.257527 | 0.987729 |
| probes | final | 12 | 12 | 0 | 4 | 4 | 4 | 0.319989 | 0.456414 |

All these final flips are untied flips. Direct joins of **actual P4 raw outputs to all 624 exact frozen label-free inputs** confirm the top choice is **input position 0 in 624/624**, with **zero ties**; output-list position was not assumed. See `direct-frozen-input-receipt.json` for each presentation and source hashes. This is a positional top-choice collapse, **not flat probabilities**. Across raw saved vectors, winning probability ranges 0.29401078820228577–0.7282788157463074; top-minus-second margin ranges 0.10249418020248413–0.45655760169029236. These are conditional allowed-symbol probabilities, not full-vocabulary probabilities or calibrated confidence.

Uniform has all-option ties; its input-order tie-break happens to produce the same final top-choice counts and flips, but uniform probabilities and proper losses differ. Its tie-free flip denominator is zero, not evidence of stable untied ranking. M6's untied positional collapse must not be equated with uniform's tie-breaking behavior.

New rules (80 cases / **40 explicit policies / 10 mechanisms**, not 80 independent policies):

| Predictor | Cases | Flips | Both correct | Original only | Reverse only | Neither | TV |
| --- | --- | --- | --- | --- | --- | --- | --- |
| m6-qwen-fresh-start | 80 | 65 | 4 | 21 | 18 | 37 | 0.392720 |
| m6-qwen-v2-trained | 80 | 80 | 0 | 23 | 21 | 36 | 0.210572 |

Intent retention, each broad stratum and probes (both-order agreement and each orientation’s losses/counts are fully shown in the appendix):

| Population | Predictor | Pairs | Both correct | Flips |
| --- | --- | --- | --- | --- |
| inherited-v1 | m6-qwen-fresh-start | 20 | 18 | 2 |
| inherited-v1 | m6-qwen-v2-trained | 20 | 0 | 20 |
| new-v2 | m6-qwen-fresh-start | 80 | 64 | 14 |
| new-v2 | m6-qwen-v2-trained | 80 | 0 | 80 |
| probes | m6-qwen-fresh-start | 4 | 4 | 0 |
| probes | m6-qwen-v2-trained | 4 | 0 | 4 |

## Family proper-loss changes and paired gains/losses

Final minus fresh (= final minus P3); negative proper-loss delta is improvement. Each common-valid denominator is shown; gains/losses mean newly correct/newly wrong reference agreements. Some sentiment/rule proper scores improve despite position collapse: these probability gains are retained, not misreported as robust rule learning.

| Population | Family | Order | Common valid | Agreement gains | Losses | ΔNLL | ΔBrier |
| --- | --- | --- | --- | --- | --- | --- | --- |
| inherited-v1 | intent | original | 20 | 0 | 14 | 1.403829 | 0.763663 |
| inherited-v1 | sentiment | original | 20 | 3 | 7 | -0.226584 | -0.053530 |
| inherited-v1 | rule_application | original | 20 | 6 | 6 | -0.432714 | -0.173474 |
| inherited-v1 | intent | reversed | 20 | 2 | 16 | 1.368927 | 0.725390 |
| inherited-v1 | sentiment | reversed | 20 | 1 | 6 | 0.147337 | 0.096612 |
| inherited-v1 | rule_application | reversed | 20 | 3 | 5 | 0.001321 | -0.024869 |
| new-v2 | intent | original | 80 | 5 | 57 | 1.199547 | 0.662531 |
| new-v2 | sentiment | original | 80 | 11 | 21 | -0.506492 | -0.112044 |
| new-v2 | rule_application | original | 80 | 17 | 19 | -0.390144 | -0.113362 |
| new-v2 | intent | reversed | 80 | 5 | 48 | 1.055076 | 0.584438 |
| new-v2 | sentiment | reversed | 80 | 11 | 20 | -0.691299 | -0.167547 |
| new-v2 | rule_application | reversed | 80 | 16 | 17 | -0.374249 | -0.144696 |
| probes | intent | original | 4 | 0 | 3 | 1.220838 | 0.781093 |
| probes | sentiment | original | 4 | 1 | 2 | -0.257308 | 0.088789 |
| probes | rule_application | original | 4 | 1 | 2 | 0.613819 | 0.356454 |
| probes | intent | reversed | 4 | 0 | 3 | 1.049433 | 0.679283 |
| probes | sentiment | reversed | 4 | 0 | 2 | 0.863415 | 0.485222 |
| probes | rule_application | reversed | 4 | 0 | 2 | 0.345012 | 0.328916 |

Reference basis matters: inherited teacher labels remain teacher agreement; new intent/sentiment are teacher-labelled. New `rule_verified` includes both programmatic and teacher-authored/executable-consistency evidence with the existing same-alias and natural-language limitations, not independent human truth. Probes remain teacher-only, including their rule family; they are not upgraded by sharing a family name. Family×label-basis and explicit reviewed policy membership are preserved in the granular appendix. No policy/group ancestry is inferred from case IDs.

## Uniform and M4 practical context, both orders

| Population | Order | Predictor | Agreement | NLL | Brier |
| --- | --- | --- | --- | --- | --- |
| inherited-v1 | original | m4-minilm-trained | 34/60 | 0.907554 | 0.478135 |
| inherited-v1 | original | m4-msmarco-trained | 42/60 | 0.712621 | 0.393343 |
| inherited-v1 | original | uniform | 17/60 | 1.378765 | 0.746111 |
| inherited-v1 | reversed | m4-minilm-trained | 34/60 | 0.907554 | 0.478135 |
| inherited-v1 | reversed | m4-msmarco-trained | 42/60 | 0.712621 | 0.393343 |
| inherited-v1 | reversed | uniform | 13/60 | 1.378765 | 0.746111 |
| new-v2 | original | m4-minilm-trained | 132/240 | 0.823115 | 0.460115 |
| new-v2 | original | m4-msmarco-trained | 141/240 | 0.917258 | 0.481392 |
| new-v2 | original | uniform | 65/240 | 1.333463 | 0.733681 |
| new-v2 | reversed | m4-minilm-trained | 132/240 | 0.823115 | 0.460115 |
| new-v2 | reversed | m4-msmarco-trained | 141/240 | 0.917258 | 0.481392 |
| new-v2 | reversed | uniform | 65/240 | 1.333463 | 0.733681 |
| probes | original | m4-minilm-trained | 6/12 | 1.025456 | 0.628466 |
| probes | original | m4-msmarco-trained | 5/12 | 1.876464 | 0.770313 |
| probes | original | uniform | 4/12 | 1.055008 | 0.645833 |
| probes | reversed | m4-minilm-trained | 6/12 | 1.025456 | 0.628466 |
| probes | reversed | m4-msmarco-trained | 5/12 | 1.876464 | 0.770313 |
| probes | reversed | uniform | 4/12 | 1.055008 | 0.645833 |

M6 final has worse NLL and Brier than current uniform in both orders of each broad stratum and on probes. M4 trained encoders are better on both broad strata in both orientations; probe comparisons are mixed (in particular MS MARCO NLL is worse than M6), not an across-the-board encoder victory. All 11 predictors, original/reverse family top-choice counts and proper scores, and all paired metrics remain in [appendix.md](../../artifacts/evaluation/e6-quality-review-v1/appendix.md). Different capacity/pretraining/rendering/training histories make this a practical systems comparison, **not a controlled architecture ablation**.

## Separate TRAIN evidence and process qualifications

The separate `e6-train-control-review-v1/report.md` reconstructs deterministic fixed-checkpoint TRAIN agreement **805→431/1500**, mean NLL **1.357723629→1.390592028**; 1,500 presentations, 375 updates, final one-epoch checkpoint, same frozen TRAIN permutation schedule. All after-fit argmax positions are 0, but **TRAIN ties are unknown** because saved fit rows lack probability vectors. Online changing-weight mean CE is not fixed-checkpoint fit or held-out performance. That review found no demonstrated rendering/reset/target/loss/loop bug and no causal diagnosis: optimization, inputs/labels, exposure and capacity remain unresolved. This review does not repeat large byte/weight audits or claim an independently observed training execution.

The owner preserved the v2 first-attempt failure before scoring, caused by two mutable policy pins (AGENTS and coordination). The v3 runner is reported byte-identical with 94 scientific pins unchanged; it is procedural recovery, not another learning attempt or a favorable checkpoint selection. The prior failure remains preserved. This synthesis checks actual v3 arithmetic, rather than treating a completed process receipt as proof of scores.

## Numerical receipts and complete appendix

- [Full unrounded recomputation](../../artifacts/evaluation/e6-quality-review-v1/numbers.json): all orientation × family/source-unit proper metrics and all pair metrics, plus signed paired contributions. Six-decimal display above is not the precision used for deltas.
- [Indexed appendix](../../artifacts/evaluation/e6-quality-review-v1/appendix.md): all 11 predictor tables; every family and granular source-group/domain/producer/mechanism/**individual policy** regression is accessible via linked CSVs; all private IDs stay there rather than in this main report.
- [Paired gains/losses](../../artifacts/evaluation/e6-quality-review-v1/paired-gains-losses.csv): each common-valid denominator and positive/negative NLL/Brier contribution sum; dimensions overlap and must not be pooled or summed as independent evidence.
- [Explicit reviewed unit mapping](../../artifacts/evaluation/e6-quality-review-v1/explicit-case-unit-mapping.csv): case→source group/domain/producer/mechanism/policy, unknowns retained. Pair membership uses frozen `recipe.json` → strata → `order_pairs`, not ID parsing.
- [Independent review receipt](../../artifacts/evaluation/e6-quality-review-v1/receipt.json), [source hashes](../../artifacts/evaluation/e6-quality-review-v1/source-pins.json), [direct raw-input binding](../../artifacts/evaluation/e6-quality-review-v1/direct-frozen-input-receipt.json), reproducible `review.py` and `synthesize.py`. Primary authoritative sources: `e6-analysis-preparation-v3/execution-01/{recipe.json,grouped-both-order-summary.json,study/*/comparison.json,study/*/*-order-report.json}`; exact file paths and SHA256s are in source-pins. Family/unit metadata ancestry is accepted from the existing E3 reviewed mapping; arithmetic is independently recomputed from actual raw vectors and reference records, not delegated to those summaries.

Evidence limits are historical tensor execution/weight attestation, unknown complete TRAIN tie counts, correlated development-only groups, same-alias label limitations and one combined recipe/seed; these constrain interpretation, not a new review gate. Evaluation used existing CPU scoring only: no ML load, new prediction, extra learning, final access, tests/lint, dependencies or paid calls. Additional actual/pending spend: £0.

### Probe all-pair macro probability scores (12 pairs, separate population)

| Predictor | Macro NLL | Macro Brier | Stable correct pairs |
| --- | --- | --- | --- |
| m6-qwen-fresh-start | 0.534509 | 0.284486 | 9 |
| qwen25-05b-instruct-frozen | 0.534509 | 0.284486 | 9 |
| m6-qwen-v2-trained | 1.173711 | 0.737779 | 0 |

## Bound controls and execution

The [original immutable declaration](../../artifacts/evaluation/e6-predeclared-v1/plan.md) and71-pin receipt predate M6/P4 outcomes; the declaration was integrated atcfbb25b. The reporting tolerance1e-6 was fixed for starting-control equivalence, not model success. Independent [starting-control review](../../artifacts/evaluation/e6-start-control-review-v1/findings.md) binds all624inputs and2390raw option probabilities to preserved P3, maximum difference0, no changed choices/top sets/ties. Model execution source isdafd5d2; the unchanged original P3 adapter was used for START. Local timestamps/receipts support sequence but are not cryptographic precommitment or loaded-tensor proof.

The sole full run used the released1500TRAIN rows, one materialized seed42 row/option schedule, one epoch/375updates, full-parameter FP32 AdamW2e-5, microbatch1/accumulation4 and clip1. A separate disposable longest-TRAIN capacity process exited before the fresh model/optimizer/RNG reset; its state was not reused. There was no development-best selection. The [TRAIN control review](../../artifacts/evaluation/e6-train-control-review-v1/report.md) independently replays schedule/target identity and recomputes880explicit source-group summaries. Counts are not880independent mechanisms.

[Actual P4 binding](../../artifacts/evaluation/e6-p4-binding-v1/receipt.json) ties the three trained prediction hashes to the exact completed M6 manifest1fe8f6d169301c76698b78b8d7b067c4b10868fb755324896352d1f61310960f. This exact manifest/path qualifies short producer IDs such as training-checkpoint; base Qwen lineage and trained weight identity are distinct. Runtime owns actual weight-byte validation and fresh load. Evaluation independently matches manifest/source-run hashes, audit/run equality, actual input/output hashes and complete P3-equivalent token audits/configuration/environment, without rereading giant tensors. Original tokenizer/chat/template, A–F complete continuation boundaries, conditional T1 scoring, cap1024/no truncation, FP32/MPS/SDPA, batch1/four threads/cache-disabled readout remain unchanged. No score-dependent comparator or prompt change.

| Recorded execution | External seconds | Scope |
|---|---:|---|
| Fresh starting624 control |38.361126|One fresh pass; byte-identical saved P3 outputs|
| Disposable TRAIN capacity |8.922245|One disposable optimizer step plus resident-state backwards; no checkpoint reused|
| Sole M6 full run |776.083240|1500training presentations/375updates plus deterministic before/after fits and final save; ≤2700s cap|
| P4 final624 inference |40.527824|One fresh local reload; load.709607s, full-pass36.818456s,16.948022decisions/s|

Full training CPU lifetimeRSS3,371,466,752B and observed MPSdriver maximum11,852,775,424B are different/overlapping scopes, **not additive**; MPS samples are not true peaks. Minimum observed recommended headroom7,216,889,856B. P4 reports CPU lifetimeRSS554,598,400B, native macOS peak process footprint3,143,828,608B and observed MPSdriver maximum2,777,350,144B. Safetensors/mmap and unflushed OS caches preclude cold-storage or comparative memory claims. No matched decoder/encoder speed or memory ratio is inferred. See [Model result](../model/m6-qwen-results.md) and [Runtime result](../runtime/p4-trained-checkpoint.md) for measurement scopes and offline/cache qualifications. Execution success is not learning success.

## Parallel diagnosis and R6 support

Model's later [source diagnosis](../model/m6-qwen-diagnosis.md) found no concrete defect in the scoped Python objective/autograd/update path; native kernel correctness, parameter-level causal effects and other causes remain unresolved. Data's D5 TRAIN-only audit independently confirms target-ID remapping and interleaved exposure. Under unsmoothed CE/recorded precision, after-fit target losses contradict exact uniformity on all1500rows; at least140rows have conditionally identifiable strict winners, but the remaining1360tiedness/full tie count and all full TRAIN vectors remain unknown. These qualified TRAIN deductions do not substitute for the directly retained development probabilities or change the frozen evaluation. Online changing-weight loss cannot establish a fixed-checkpoint learning curve. No extra run, repair or fallback follows from these audits.

Separately, Evaluation delivered Research an [anonymous P3 NEW-v2 export](../../manifests/evaluation/r6-probability-export-v1.json):240paired decisions/480vectors/1840raw probability values, no text/targets/correctness/private map, with explicit anonymous construction units. It contains only preserved P3, not trained E6 predictions; R6's frozen-base diagnostic is a separate authorized workstream and not a retrospective E6 ablation. The export's producer-held-out grouping does not establish independent sampling. Data received aggregate E6 conclusions only; a follow-up explicitly clarified that common-handoff artifact-root locators were not Data inputs or permission to open private Evaluation cases.

The v2 failed attempt and v3 policy-only rebinding are preserved in [previous-attempt.json](../../artifacts/evaluation/e6-analysis-preparation-v3/previous-attempt.json) and [policy diff](../../artifacts/evaluation/e6-analysis-preparation-v3/policy-changes.diff). Scientific criteria, all references/baselines/source units and runner bytes are unchanged. The first successful analysis has158hash-indexed output files, complete11-predictor coverage in all three separate strata, and no selection of a favorable execution. No automatic promotion, temperature diagnostic or further learning is authorized by E6.
