# R2 pilot shortcut audit: execution and interpretation

`audit_pilot_shortcuts.py` is a standard-library data inspection script, not a model trainer, software test suite, or replacement dataset generator. It only reads the published `data-pilot-v1` train/validation manifest, six referenced shards and their group-assignment files. It refuses final/unknown splits and paths outside the pilot directory, checks shard hashes/counts before analysis, and creates a **new** output directory exclusively.

## Canonical command

Run from `/Users/destiner/Code/jeff/.worktrees/research`:

```bash
uv run --locked python -B experiments/research/audit_pilot_shortcuts.py \
  --manifest /Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/manifest.json \
  --artifacts-dir /Users/destiner/Code/jeff/artifacts \
  --output-dir /Users/destiner/Code/jeff/artifacts/research/pilot-shortcut-audit-20261111T1105
```

Use the base uv environment, **not** `--extra model`. No torch, Transformers, tokenizer, external API, or paid dependency is used. Never rerun with a completed output directory. Source data is not edited or copied into training.

Outputs:

- `audit.json`: input/script hashes; declared group/domain/mechanism details; position and choice-count distributions; fixed-selector and train-count lookup diagnostics; exact/template overlap and all-pairs scan summaries; sentiment label/style counts.
- `heuristic-rows.json`: per-row option lengths, target position, fixed-selector decisions/agreement and unseen-option flags. IDs locate existing data; these are **analysis records, not new labeled dataset rows**.

## Methods and limits

- All pairs: 360 choose 2 = 64,620; cross-split: 300 × 60 = 18,000. NFKC/casefold word trigrams of state, with question fallback only for empty state, match Data's original lexical method. Numeric masking replaces all-digit tokens with `NUM`; it intentionally discards meaningful numerical differences. It does not rename entities or establish semantic equivalence. The report stores the top 30 cross-split pairs even when similarity is low.
- Fixed selectors: first, last, longest/shortest characters, longest words. Ties always use input order. Uniform expected agreement is `mean(1/K)`, not the accuracy of deterministic first-option tie-breaking.
- Descriptive training priors pool **all training families**: choice-count-conditioned position frequency; normalized option-text rate `(correct + 1)/(offered + 2)`. No thresholds or fitted ML model. Unknown option texts tie at 0.5. Training rows participate in their own counts, so in-sample lookup scores are not independent predictive evidence. Validation labels never set lookup counts.
- Publication-cycle diagnostic: a counter starts at zero separately for family/split/choice-count and predicts position `counter mod K`. It sees file order; it is **not** a deployable independent-example baseline or an available input feature of the current pair scorer.
- Sentiment label mapping decodes the three published four-class wording sets. Mean state word count uses whitespace splitting; conjunction/mixed-word counts use normalized words. These are associations, not causal model explanations.
- Structural/hash checks protect the analysis input but do not duplicate Data's full validator, certify label correctness, or establish group independence.
- This is exploratory validation analysis. Do not call heuristic selection on the inspected validation data an independently held-out result. No model was loaded or evaluated by running inference.

## Execution history

Two preliminary invocations used the system `python3 -B` (Python 3.9.6), the same manifest/root, and new immutable directories:

1. `pilot-shortcut-audit-20261111T1055`: successful full counts; retained cross-split pairs only above 0.12, which yielded an empty candidate list.
2. `pilot-shortcut-audit-20261111T1058`: successful after retaining the top cross-split pairs without a floor, to permit bounded manual review even at low similarities. This changed reporting, not the counts/selectors. Maximum cross-split similarity is 0.076923.

The canonical command above successfully repeated the final script using the repository's approved Python **3.12.16** uv environment; results match the preliminary runs. Earlier artifacts are retained, not overwritten. Intermediate handoffs cite those earlier immutable reports; final delivery cites the canonical run.

## Package build

The worktree is built with:

```bash
uv build --no-sources \
  --out-dir /Users/destiner/Code/jeff/artifacts/research/pilot-shortcut-audit-20261111T1105/branch-build
```

The branch build above succeeded, producing wheel and source distribution. Integration additionally uses `uv build --no-sources` on the main tree under the shared merge lock, as required by `docs/coordination.md`. The final handoff records the actual integration outcome and commit hashes; the planned integration command here is not itself evidence that it succeeded. No software tests or linting are authorized or run.

Interpretation, source examples and exactly three prioritized data improvements: [R2 report](../../docs/research/pilot-v1-generalization-audit.md).
