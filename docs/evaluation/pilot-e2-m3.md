# E2: corrected pilot and retained-head cross-encoder comparison

**M3 improves the pilot score, but substantially regresses on the separate validation probes. Preserve both models; this is not evidence for an unconditional replacement.** Evaluation independently scored Model's frozen prediction files. No model was loaded by Evaluation and no final data were inspected or scored.

Full machine/readable reports: `JEFF_ARTIFACTS_DIR/evaluation/e2-m3-v2/{comparison.json,report.md,probes-comparison.json,probes-report.md}`. `v2` is the report revision (adds explicit teacher/source provenance), **not Data pilot-v2**. All comparisons here use frozen `data-pilot-v1` plus the existing evaluation probes.

## Controls and coverage

- Pilot: **60 rows / 12 declared source groups**, not 60 independent tasks. Intent/sentiment have five groups of four rows each; rules have two groups of ten. Labels: 40 teacher, 20 programmatic `rule_verified`. Teacher aliases are `openai/gpt-sol` / `gpt-sol`, without immutable revision claims. Aggregate metric is **reference-label agreement**; teacher families measure teacher agreement.
- Probes: **24 presentations / 12 source groups**, each original plus exact reversed options. All teacher labels, including rule probes; teacher identity unknown. These are validation, not untouched final evidence.
- All eight predictors cover **60/60 pilot** and **24/24 probe** rows, with zero missing, invalid, duplicate, extra, or unidentifiable predictions. Conditional agreement therefore equals all-row success. All primary model reversal runs cover 120/120 presentations / 60/60 pairs.
- M2 uses `sentence-transformers/all-MiniLM-L6-v2@1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, a pretrained encoder with an initially **random** scalar head. Compared recorded 128/M2 configs independently: only token cap 128→256 and output directory differ; recorded model/trainer source hashes and dataset manifest hash match. Training stochasticity is not eliminated on MPS. Use the matching 256-token starting checkpoint to measure M2 training gains.
- M3 uses `cross-encoder/ms-marco-MiniLM-L6-v2@233902d25c440f23af6f7d6e94d2946bac0bee0a`, retaining its **pretrained MS MARCO relevance head**. Same data, cap256, seed42, three epochs, batch4, learning rates2e-5/5e-4, and225-step budget. Its base weights, pooling/scoring architecture, and training history differ: this is not a head-only causal ablation.
- Model owns training/save/fresh-process reload evidence. Evaluation independently compared recorded configuration/source/manifest metadata and scored every published prediction file; it did not rerun training, tokenizer audits, or weight-tensor comparisons. `control-audit.json` records that distinction.

## Pilot comparison

Log loss uses natural logarithms, no clipping; lower is better. Uniform chooses the first option on exact ties, not random sampling.

| Predictor | Reference-label agreement | Log loss |
| --- | --- | --- |
| Uniform | 17/60 (28.33%) | 1.378765 |
| Lexical overlap | 29/60 (48.33%) | 1.323710 |
| Random-head128 | 19/60 (31.67%) | 1.378223 |
| Trained128 | 36/60 (60.00%) | 0.843401 |
| Random-head256, M2 start | 20/60 (33.33%) | 1.378267 |
| Trained256, M2 | 35/60 (58.33%) | 0.855288 |
| Pretrained MS MARCO256, M3 start | 30/60 (50.00%) | 1.026878 |
| Trained MS MARCO256, M3 | 40/60 (66.67%) | 0.793701 |

M2 versus its starting checkpoint: **25 paired row wins / 10 losses**, net+15. M2 versus trained128: **2 wins / 3 losses**, net−1; mean loss worsens0.011887. Model/Research's token audit reports zero over-budget pairs at256 (maximum full pair169), correcting known question loss at128. Removing input loss did not fix the rule weakness; do not revert to truncated inputs merely to favor the earlier score.

M3 versus its starting checkpoint: **14 wins / 4 losses**, net+10; mean loss improves0.233177. M3 versus M2: **13 wins / 8 losses**, net+5; mean loss improves0.061587. These are descriptive paired counts on one seed and few correlated groups, not significance claims.

### Per family

Each cell is agreement count / mean log loss, with20 rows per family. Intent/sentiment measure teacher agreement; rule application uses Data's `rule_verified` labels.

| Family (groups) | Uniform | Lexical | M2 start | M2 trained | M3 start | M3 trained |
| --- | --- | --- | --- | --- | --- | --- |
| Intent (5) | 6 /1.370160 | 16 /1.216725 | 6 /1.373597 | 20 /0.067838 | 18 /0.381560 | 19 /0.211817 |
| Sentiment (5) | 5 /1.386294 | 5 /1.380693 | 6 /1.382234 | 11 /1.066200 | 7 /1.332485 | 14 /0.806437 |
| Rules (2) | 6 /1.379841 | 8 /1.373712 | 8 /1.378970 | 4 /1.431825 | 5 /1.366589 | 7 /1.362848 |

M3 still trails the lexical baseline in rule top-choice accuracy (7/20 versus8/20). Its overall advantage does not establish reliable rule execution.

### Every source group

IDs below omit `data:pilot-v1:`. The corrected sentiment-r2 shard retains the `sentiment` group namespace. Counts refer to correct choices. M3 loss is shown per group; full starting/trained/simple-baseline group losses and coverage appear in both complete reports. The source group, not its number of paraphrases/templates, is the useful unit for interpreting breadth.

| Source group | n | Uniform | Lexical | M2 start | M2 trained | M3 start | M3 trained | M3 log loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent:g26 — apiary | 4 | 3 | 3 | 1 | 4 | 4 | 4 | 0.000795 |
| intent:g27 — canal boat | 4 | 0 | 2 | 1 | 4 | 3 | 4 | 0.194188 |
| intent:g28 — seed library | 4 | 1 | 4 | 1 | 4 | 4 | 4 | 0.001515 |
| intent:g29 — makerspace | 4 | 1 | 3 | 2 | 4 | 3 | 3 | 0.857740 |
| intent:g30 — choir festival | 4 | 1 | 4 | 1 | 4 | 4 | 4 | 0.004845 |
| sentiment:g26 — pet boarding | 4 | 1 | 1 | 2 | 3 | 1 | 4 | 0.581017 |
| sentiment:g27 — observatory | 4 | 0 | 0 | 0 | 3 | 1 | 3 | 0.677976 |
| sentiment:g28 — luggage storage | 4 | 1 | 2 | 1 | 3 | 3 | 1 | 1.004299 |
| sentiment:g29 — hearing loop | 4 | 2 | 0 | 1 | 1 | 0 | 3 | 0.962462 |
| sentiment:g30 — seed swap | 4 | 1 | 2 | 2 | 1 | 2 | 3 | 0.806433 |
| rule_application:g11 — reachability | 10 | 3 | 3 | 2 | 2 | 2 | 2 | 1.427479 |
| rule_application:g12 — election | 10 | 3 | 5 | 6 | 2 | 3 | 5 | 1.298218 |

M3's largest net gain over M2 is election g12 (+3), but that contains five wins and two losses. Reachability remains2/10 despite two wins and two losses. Luggage-storage sentiment regresses3→1 while its log loss improves slightly: probability quality and chosen-answer quality can move in opposite directions. Neither changes the supplied label provenance.

## Probe regression: do not hide it behind the pilot gain

| Predictor | Teacher agreement | Log loss |
| --- | --- | --- |
| Uniform | 8/24 | 1.055008 |
| Lexical | 9/24 | 1.047044 |
| Random-head128 | 2/24 | 1.057107 |
| Trained128 | 16/24 | 0.710406 |
| Random-head256 | 2/24 | 1.057107 |
| Trained256, M2 | **16/24** | **0.710407** |
| Pretrained MS MARCO256 | 14/24 | 1.453783 |
| Trained MS MARCO256, M3 | **8/24** | **1.360701** |

M3's mean loss improves modestly versus its own start while agreement falls14→8. Against M2, both agreement and loss worsen substantially. Family counts M2→M3: intent6/8→4/8, sentiment6/8→0/8, rules4/8→4/8. M3 fails **all four sentiment probe groups**.

Every probe group (counts out of2 presentations; IDs omit `eval.validation.`):

| Group | M3 start | M2 trained | M3 trained |
| --- | --- | --- | --- |
| intent.01 | 2 | 2 | 2 |
| intent.02 | 0 | 2 | 0 |
| intent.03 | 0 | 0 | 0 |
| intent.04 | 2 | 2 | 2 |
| sentiment.01 | 0 | 2 | 0 |
| sentiment.02 | 0 | 0 | 0 |
| sentiment.03 | 2 | 2 | 0 |
| sentiment.04 | 2 | 2 | 0 |
| rule_application.01 | 0 | 0 | 0 |
| rule_application.02 | 2 | 2 | 0 |
| rule_application.03 | 2 | 2 | 2 |
| rule_application.04 | 2 | 0 | 2 |

Versus its start M3 loses three groups and gains none: rule precedence, quoted-positive sentiment attribution, and neutral sentiment with an embedded instruction. Versus M2 it loses five groups and gains one (inclusive boundary/injected rule replacement). The conjunction case stays wrong but becomes more confidently wrong (loss3.4184→7.1430); an unresolved-intent case stays wrong but becomes less confident (7.1181→1.1582), helping explain the mixed aggregate loss/accuracy movement.

These are validation-derived findings, not final-set discoveries. Any repairs must use genuinely separate new training scenarios; none of these cases or their variants may become training data.

## Option-order sensitivity

Exact reversed option objects preserve option IDs, text, targets, and source groups. Original predictions are reused from the same snapshots, not regenerated with another model. Probability differences are compared after the scorer's declared floating-point normalization.

| Predictor | Complete pilot pairs | Same choice | Tied pairs | Original→reversed agreement | Mean total variation |
| --- | --- | --- | --- | --- | --- |
| Uniform | 60/60 | 0/60 | 60 | 17/60→13/60 | 0 |
| Lexical | 60/60 | 46/60 | 14 | 29/60→31/60 | 0 |
| M2 start | 60/60 | 60/60 | 0 | 20/60→20/60 | 0 |
| M2 trained | 60/60 | 60/60 | 0 | 35/60→35/60 | 4.12e-11 |
| M3 start | 60/60 | 60/60 | 0 | 30/60→30/60 | 5.59e-10 |
| M3 trained | 60/60 | 60/60 | 0 | 40/60→40/60 | 3.27e-11 |

Maximum individual probability change across these model pilot runs is1.44e-8. Both M2/M3 snapshot pairs are also choice-consistent12/12 on the probes, without ties; maximum individual change there is6.91e-9. All 14 completed order reports expose coverage, consistency, transitions, and probability change **per family and source group** in JSON.

Uniform/lexical choice changes are entirely tie effects; probability distributions are unchanged. Reversal tests one permutation. Order consistency preserves wrong answers too and does not demonstrate broad invariance or reasoning. No 128-token full-pilot reversal inference was requested; its existing probe reversal predictions were processed and are reported separately.

## Limitations and recommended use

- Keep both existing trained models. M3 has the best pilot aggregate here, but its probe regression rules out an unqualified improvement claim. Model selection requires an explicit task trade-off, not just the highest aggregate or training-loss curve.
- Research's validation-selected longest-option diagnostic reaches18/20 intent targets without state/question. This qualifies both models' high intent scores; it does not prove either model uses that shortcut. The diagnostic is post-inspection analysis, not an independently held-out baseline. See the integrated [Research audit](../research/pilot-v1-generalization-audit.md) and delivery handoff `20261111T1110-R2-delivered.md`.
- Few synthetic source groups, only two rule-validation mechanisms, single-seed comparisons, teacher labels, and repeated use of validation limit generalization claims. Research found no validation cases for the ten trained rule mechanisms: these results do not measure retention on those mechanisms. Its lexical/manual audit found no demonstrated cross-split source leakage, but that is not comprehensive semantic clearance. Group IDs do not prove statistical independence. No confidence calibration is claimed.
- `passage_entailment` remains reserved. Final content was not opened, exported, scored, or used for any decision in E2/M3. Additional spend£0 actual/pending; Evaluation used CPU only.

## Reproduction and evidence

`evaluation/e2-m3-v2/recipe.json` pins every reference, prediction, pair-map, order-report, and comparison SHA-256. `prediction-bundles.json` under `e2-m3-v1/` records original/reversed concatenation sources. A compact tracked index is `manifests/evaluation/e2-m3-report-v1.json`. Never overwrite frozen outputs.

Actual successful operations: `compare` for both eight-way sets; `order` for six pilot predictors and all eight probe predictors; `render` for both final reports. `uv build --no-sources --out-dir /Users/destiner/Code/jeff/artifacts/evaluation/e2-final-build-v1/dist` produced wheel and source distribution. Installed that wheel with `uv pip install --no-deps` into a new Python3.12 environment at `evaluation/e2-final-build-v1/env`; from outside the checkout, with `PYTHONPATH` unset, it successfully re-scored and rendered both complete eight-way comparisons. Those reproduction reports are preserved beside the build. No optional ML dependencies were installed or loaded by Evaluation. The earlier128/probe files were consumed while awaiting Model's requested M2/M3 inference. All requested inference arrived through direct public handoffs, without a user relay.

To repeat scoring into a **new** directory using the recipe:

```sh
uv run --locked python - <<'PY'
import json, pathlib, subprocess, sys
root = pathlib.Path('/Users/destiner/Code/jeff/artifacts/evaluation')
recipe = json.loads((root/'e2-m3-v2/recipe.json').read_text())
output = root/'e2-m3-reproduction-new-id'
output.mkdir(exist_ok=False)
for filename, run in recipe['comparisons'].items():
    args = [sys.executable, '-m', 'jeff.evaluation.compare',
            '--examples', run['examples']['path'], '--output', str(output/filename)]
    for name, prediction in run['predictions'].items():
        args += ['--predictions', name+'='+prediction['path']]
    subprocess.run(args, check=True)
PY
```

Then render a new Markdown output with `python -m jeff.evaluation.render --comparison <new-comparison.json> --order <predictor>=<matching-order-report> ... --output <new-report.md>`. The renderer requires exact matching original probabilities and supports both60 original references/60 reversal pairs and24 paired presentations/12 probe pairs. Full per-group losses remain available even if a narrative table is shortened.

Focused read-only reviews covered metric denominators, multi-pair group handling, validation failures, and report provenance. Two renderer issues were fixed before final delivery: teacher/source identities now appear explicitly, and paired infinite/undefined loss status is not silently reduced to an unexplained dash. No software tests or linting were written or run.
