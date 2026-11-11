# Validation-only failure discovery

Dataset `evaluation-probes-v1` has 12 distinct source groups, 4 per training family. Each is presented with original and reversed option order: 24 rows, **not 24 independent observations**. Stable option IDs/text and target IDs are preserved under reversal; example IDs differ. No `passage_entailment` examples occur here.

The separate validation curator designed negation, rejected distractors, explicit clarification, mixed-versus-neutral sentiment, attribution, rule precedence, missing information, thresholds, and answer-selection instructions embedded as task data. These are original AI-teacher labels (`teacher_model: unknown`), not human or rule-verified labels.

## Actual simple-baseline results

All 24 predictions valid for each baseline; no missing/invalid/duplicate/extra/unidentifiable predictions. Pair coverage 12/12.

| Baseline | Teacher agreement | Log loss | Intent | Sentiment | Rule application |
| --- | --- | --- | --- | --- | --- |
| Uniform | 8/24 (33.33%) | 1.055008 | 2/8 | 3/8 | 3/8 |
| Lexical | 9/24 (37.50%) | 1.047044 | 2/8 | 3/8 | 4/8 |

Uniform original/reversed scores are both 4/12; lexical scores are 4/12 and 5/12. Probabilities by option ID are invariant under reversal for both baselines (mean total variation 0). Uniform choices change in all 12 pairs due solely to deterministic first-option tie-breaking. Lexical choices are consistent in 8/12 pairs; all four inconsistent pairs have ties. Untied lexical choices are consistent 8/8. This is not evidence of a learned model's order robustness.

Artifacts: `evaluation/probes-v1/` (manifest, validation rows, source-group pair map), `evaluation/probes-baselines-v1/` (label-free inputs, simple predictions, comparison and order reports). Source cases/rationales remain artifact data, not software tests.

## Reproduction

`curate` freezes compact teacher-authored cases; it is not a teacher API. For these artifacts:

```sh
uv run --locked python -m jeff.evaluation.curate \
  --source "$JEFF_ARTIFACTS_DIR/evaluation/validation-probes-source-v1/cases.json" \
  --dataset-id evaluation-probes-v1 --split validation --reverse-pairs \
  --output-dir "$JEFF_ARTIFACTS_DIR/evaluation/<new-dataset-id>"
uv run --locked python -m jeff.evaluation.order \
  --examples "$JEFF_ARTIFACTS_DIR/evaluation/probes-v1/validation.jsonl" \
  --pairs "$JEFF_ARTIFACTS_DIR/evaluation/probes-v1/pairs.json" \
  --predictions "<prediction-file>" --output "<new-order-report.json>"
```

Order analysis requires exact reversed options, same content/target/provenance, complete unique pair definitions, and validation-only rows. It reports complete-pair coverage, missing/invalid members, choice consistency with/without ties, probability variation, and both/one/neither-correct outcomes by family. Initial curation and both simple-baseline order analyses were executed successfully. Use a new dataset ID/output path for regeneration; do not overwrite or silently revise a frozen shard.

## Interpretation boundaries

Clarification and missing-value cases have explicit policies; they do not establish resolution of genuinely ambiguous tasks. Mixed sentiment follows the supplied options, not an assumed universal taxonomy. Injection cases clearly mark attributed content and probe only basic separation. Sarcasm/implicit preferences and broad adversarial robustness are not covered by this validation set.

## Actual tiny-model probe comparison

Model completed the optional inference request on these exact label-free inputs using the **tiny-trained** checkpoint and its starting random-head checkpoint, not a pilot-selected model. Evaluation independently scored the returned files without loading any models.

| Predictor | Valid / total | Teacher agreement | Log loss | Intent | Sentiment | Rule application |
| --- | --- | --- | --- | --- | --- | --- |
| Pretrained encoder + random head | 24/24 | 2/24 (8.33%) | 1.057107 | 2/8 | 0/8 | 0/8 |
| Tiny-trained | 24/24 | 2/24 (8.33%) | 1.059969 | 2/8 | 0/8 | 0/8 |

No prediction failures/extras or ties. Both snapshots correctly select only `eval.validation.intent.01`, in both orders; all other 11 source groups disagree with the teacher in both orders. These are wrong answers against references, not inference failures. Tiny training worsens probability quality without improving top-choice agreement here. No comparisons on final data occurred.

Choice consistency is 12/12 for both snapshots. Mean total variation under reversal is 0 for the starting head and 1.65e-9 for trained (maximum individual probability change 1.94e-8). These near-numerical differences show order consistency on these pairs, **not correctness or broad robustness**. Artifacts: `evaluation/probes-trained-comparison-v1/comparison.json`, `baseline-order.json`, `trained-order.json`; model files under `model/tiny-probes-20261111-01/`.

Validation-only next hypotheses: train the first actual pilot before changing architecture; add matched validation controls to separate negation/conjunction/injected-text effects; distinguish probability-order sensitivity from tie changes. The earlier validation analyst's lexical findings are not attributed to Model; trained conclusions above use actual returned model probabilities.
