# E14: a frozen native NLI baseline

**Summary.** The fixed RoBERTa NLI baseline achieved 37/60 inherited, 126/240 new and 7/12 probe both-order successes, with exactly reversal-identical, untied probability vectors. It improves paired consistency over original P3 on the new population, but loses previously correct members and falls behind stronger trained contexts. This is a practical fresh-start baseline, not an architecture-controlled comparison, training result or calibrated NLI-truth estimate.

**Consequential resource qualification:** the REQUIRED recommended MPS headroom guard was **neither measured nor enforced**. The sampler used `vm_stat` free + inactive pages (minimum 8,559,722,496 bytes), not `torch.mps.recommended_max_memory() - torch.mps.driver_allocated_memory()`. Lead direction `b6de92` permits qualified interpretation of these stored outputs—not a P12 rerun, historical memory probe or claim of full contract compliance. The [owner resource follow-up](../../artifacts/evaluation/e14-resource-qualification-v1/receipt.json) supersedes any compliant-headroom reading of the earlier binding review. Separate observed RSS/driver caps do not repair the missing guard. Original source, receipts and failure evidence remain unchanged. Future NLI execution requires a prospective guard fix and an actual grant; this report grants no adaptation permission.

## Prospective controls and fixed method

Conditional E14 comparison criteria were adopted at 01:14 UTC before P12 outputs: same development presentations, component-wise agreement/proper scores, strict both-order success, ties, coverage, exact probe retention and every family/source regression. The single R10 source profile was adopted by 01:57 UTC (receipt timestamp 01:56:16), before execution; source eligibility was not a runtime-success claim. The [predeclared plan](../../artifacts/evaluation/night-predeclared-v1/plan.md), [source adoption receipt](../../artifacts/evaluation/e14-source-binding-v1/receipt.json) and [R10 declared profile](../research/frozen-nli-source-screen.md) retain these distinctions. The present retrospective synthesis makes no additional unseen-outcome claim.

Exactly one model was used: `MoritzLaurer/roberta-base-zeroshot-v2.0-c@d825e740e0c59881cf0b0b1481ccf726b6d65341`, retaining its pretrained two-class head, **0 = entailment; 1 = not_entailment**. Class 1 is not a separately trained contradiction class. Each native option was paired independently with the same context/question using:

```text
premise = 'Context:\n{state}\n\nQuestion:\n{question}'
hypothesis = 'The correct answer is:\n{option_text}'
```

Here `\n` denotes actual LF characters. Fields are verbatim, without stripping, normalization or paraphrase; the Context header remains for empty state. Premise is sequence 1 and hypothesis sequence 2. IDs, targets and source/family metadata do not enter the text. This fixed QA-to-NLI bridge is not the model card's topic template and is not established as optimal, especially for terse labels or numeric answers.

For option i, the score is native entailment minus logsumexp of native non-entailment logits: exactly `s_i = z_i,0 - z_i,1` for this head. Probabilities are stable **T=1 softmax across that decision's supplied choices**. They are not independently sigmoid-transformed entailment probabilities subsequently normalized. No prompt sweep, temperature fitting, replacement head or Jeff NLI training occurred. Cross-choice normalization forces a distribution even when no answer is well supported.

The producer used strict local builtin RoBERTa loading, safetensors, no remote code, FP32/MPS, four threads, eager attention, frozen eval/inference mode and four decisions per batch. Complete pairs include special tokens, with a 512-token cap and no truncation. Different architecture, scale, pretraining/NLI history, tokenizer, budget and readout prevent a causal architecture interpretation.

## Populations and results

P12 processed the same **624 presentations**: 300 native, 300 reversed and 24 already-paired probe presentations. These comprise separate **60 inherited, 240 new and 12 probe pair denominators**; probes were not reversed again. Source groups number 12 inherited, 170 new (80 intent, 80 sentiment, 10 rules) and 12 probes. Reversals and overlapping source dimensions are dependent, not independent replications. These repeatedly exposed development comparisons are not a new holdout or semantic re-verification of teacher labels.

NLL and summed Brier are lower-is-better. For P12 native and reversed results are identical, and each native correct member is also correct reversed:

| Population | Correct / both correct | NLL | Brier | Choice flips |
|---|---:|---:|---:|---:|
| Inherited | 37/60 | 0.954901939 | 0.529523529 | 0 |
| New | 126/240 | 1.134035080 | 0.598443984 | 0 |
| Probes | 7/12 | 0.684391412 | 0.437221452 | 0 |

All 312 pairs have exactly identical raw and normalized semantic-ID vectors and maximal sets: maximum absolute change and total variation are zero. All P12 maxima are unique; no zero probabilities occur. This establishes observed native/reversal invariance, not arbitrary-permutation invariance or a guarantee about future runtimes.

### Meaningful starts and stronger completed contexts

Original P3 and original MS MARCO are the primary fresh-start comparisons. The weaker random MiniLM head is not a substitute for them. The table gives new-population results; every historical context remains available in the [full 18-context review](../../artifacts/evaluation/e14-quality-review-v1/findings.md), including M2/M3, both M4 arms, M6, M8 and uniform/lexical controls. P3 and M6 fresh-start reuse the same outputs, not independent confirmations. No favourable context or orientation was selected.

| Context | Native / reversed correct (of 240) | Both correct | Native / reversed NLL | Native / reversed Brier |
|---|---:|---:|---:|---:|
| Original P3 | 129 / 118 | 82 | 1.312349631 / 1.410620678 | 0.633492030 / 0.687402352 |
| Original MS MARCO | 99 / 99 | 99 | 1.058567628 / 1.058567628 | 0.581492282 / 0.581492282 |
| M4 MS MARCO trained | 141 / 141 | 141 | 0.917258345 / 0.917258345 | 0.481392322 / 0.481392322 |
| M7 | 171 / 170 | 138 | 0.669211029 / 0.618563980 | 0.352958510 / 0.337569741 |
| M9 | 165 / 165 | 165 | 0.699420442 / 0.699420442 | 0.359766381 / 0.359766381 |
| M10 | 182 / 178 | 157 | 0.525299952 / 0.522372994 | 0.288286142 / 0.282673286 |
| M11 | 162 / 162 | 162 | 0.860174719 / 0.860174719 | 0.411283631 / 0.411283631 |
| M12 | 121 / 113 | 75 | 1.172462498 / 1.235607139 | 0.627519445 / 0.662124356 |
| P12 frozen NLI | 126 / 126 | 126 | 1.134035080 / 1.134035080 | 0.598443984 / 0.598443984 |

P12's paired gain over P3 coexists with fewer native correct choices. Against original MS MARCO it improves both-correct count but **worsens both proper scores**. M4-trained, M7, M9, M10 and M11 have stronger broad new-population quality. M12 illustrates why improved paired consistency cannot erase lost members.

### Retention, family, source and probe tradeoffs

Entries below are **retained / gained / lost / neither** both-correct members, P12 relative to each comparator, with populations kept separate:

| Comparator | Inherited (60) | New (240) | Probes (12) |
|---|---|---|---|
| P3 | 22 / 15 / 6 / 17 | 65 / 61 / 17 / 97 | 7 / 0 / 2 / 3 |
| Original MS MARCO | 24 / 13 / 6 / 17 | 77 / 49 / 22 / 92 | 5 / 2 / 2 / 3 |
| M7 | 26 / 11 / 13 / 10 | 99 / 27 / 39 / 75 | 5 / 2 / 4 / 1 |
| M9 | 26 / 11 / 17 / 6 | 107 / 19 / 58 / 56 | 4 / 3 / 4 / 1 |
| M10 | 25 / 12 / 16 / 7 | 107 / 19 / 50 / 64 | 5 / 2 / 4 / 1 |
| M11 | 25 / 12 / 17 / 6 | 108 / 18 / 54 / 60 | 5 / 2 / 4 / 1 |
| M12 | 22 / 15 / 4 / 19 | 66 / 60 / 9 / 105 | 3 / 4 / 2 / 3 |

| P12 family | Inherited correct; NLL; Brier | New correct; NLL; Brier | Probe correct; NLL; Brier |
|---|---|---|---|
| Intent | 20/20; .305024705; .116818538 | 72/80; .543778884; .274345092 | 3/4; .504564903; .272825345 |
| Sentiment | 6/20; 1.265307231; .769921210 | 37/80; 1.521868584; .778802491 | 1/4; 1.044755388; .709679962 |
| Rules | 11/20; 1.294373882; .701830839 | 17/80; 1.336457772; .742184368 | 3/4; .503853945; .329159049 |

Intent is relatively strong; sentiment and especially new rules remain weak. On new native rules P12 loses 22 P3-correct choices while gaining 14, despite better NLL/Brier. New native intent loses 8 and gains 6 against P3 with worse proper scores. Against original MS MARCO, new native sentiment gains 25 and loses 6 yet worsens NLL by .129354992 and Brier by .025757313. Choice gains and probability quality are distinct.

Source losses also survive aggregate gains: against P3, new native source units include 32 with gained choices and 30 with lost choices, but 111/170 have worse NLL and Brier; reversed counts are 40 gain-bearing and 31 loss-bearing units, with 104 worse NLL and 103 worse Brier. Against original MS MARCO, 44 new units contain gains and 19 losses, while 103 have worse NLL and 106 worse Brier in either orientation. Units can contain both gains and losses. Unknown probe source dimensions remain unknown, not inferred from IDs.

P12's seven correct probe pairs are a subset of P3/M8's nine: zero gained, with `eval.validation.intent.03.original` and `eval.validation.sentiment.01.original` lost. Comparator-specific probe gains do not cancel other losses. Every requested family contrast, source-unit gain/loss count and proper-score exception is retained separately by orientation in [tradeoffs](../../artifacts/evaluation/e14-quality-review-v1/tradeoffs.md); exact memberships and overlapping producer/domain/policy/mechanism dimensions remain in [focal tradeoffs](../../artifacts/evaluation/e14-quality-review-v1/focal-all-tradeoffs.json) and [both-order membership](../../artifacts/evaluation/e14-quality-review-v1/both-order-membership.json).

## Execution limits and evidence strength

The [actual binding review](../../artifacts/evaluation/e14-p12-binding-v1/report.md) supports exact source-semantic binding and 83 artifact-consistency checks. Native receipts record one tokenizer load, one model load, **156 batch-four forwards**, 2,390 candidate pairs and zero startup forwards. Saved complete-pair lengths range 52–177, total 188,734 unpadded tokens, with all pairs below 512. This is retained length evidence, not independent tokenization.

Parent recorded elapsed was 19.516261 seconds; external timing was 19.52 seconds, with conservative delivery charge 21/480 seconds. Recorded child cleanup and successful delivery support completion, but the receipt's end precedes final publication and is not an independent outer-process exit timestamp. Sampled current RSS max was 880,787,456 bytes, process peak RSS 1,130,102,784 bytes and MPS driver max 1,082,867,712 bytes. RSS/driver are nonadditive unified-memory views, driver sampling is not a continuous peak, and none establishes the missing recommended-headroom guard.

Recorded 249,318,428-byte F16 weights and 124,647,170 parameters come from retained acquisition/shape metadata, not Evaluation tensor reads; runtime FP32 conversion is a separate fact. The model card declares MIT, without a standalone LICENSE or blanket upstream-rights clearance. Attribution and supplied notices remain required.

Native logits/margins were **not saved**: exact source binding is not numerical raw-margin replay. Reviewer text hashes were newly reconstructed from pinned inputs and inspected rendering, not independently runtime-captured text/token traces. Producer load diagnostics were empty, but Evaluation did not independently load the model.

The [completed quality review and receipt](../../artifacts/evaluation/e14-quality-review-v1/final-receipt.json) independently checked all 18 contexts, 12,024 orientation rows, 6,012 pair rows, 11,356 contrasts and 7,180 regression rows, plus 153 retained byte-identical copies and 51 preserved predictor objects. No covered arithmetic, exact-join, validity or retention discrepancy was found. Only new P12 predictions were scored; **17 historical contexts were retained without rescoring**. The actual completed E14 recipe is [execution-01/recipe-all18.json](../../artifacts/evaluation/e14-scoring-preparation-v1/execution-01/recipe-all18.json), not an earlier preparation template. The preserved preparation `KeyError: source_inputs` was a historical `source_reference` alias error, not an actual execution failure.

This evidence does not establish runtime/full-resource compliance, semantic correctness of teacher labels, calibration, significance, architecture causality, candidate admission or promotion. It neither reports external-population results nor authorizes follow-on adaptation. The [executed new-only recipe](../../configs/evaluation/e14-p12-v1.json) is a byte-exact copy; the [publication manifest](../../manifests/evaluation/e14-p12-report-v1.json) binds execution, independent reviews and the resource correction. Evidence locators do not grant access to private references or per-case outputs. Packaging builds establish packaging only, not scientific correctness or software-test evidence.
