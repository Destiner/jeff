# E6 deferred CPU analysis v2

Preserves unused `../e6-analysis-preparation-v1/`. Before inspecting new M6/P4 outcomes, removes an arbitrary 16 MiB report-hash limit (streaming hashes; tensor files refused) and limits repeated per-case contribution tables to five named contrasts: trained−fresh, trained−P3, fresh−P3, trained−M4 MiniLM and trained−M4 MS MARCO. All eleven predictor/orientation/family/source-unit metrics remain; the existing comparer still supplies its complete original-order comparisons. Frozen plan/populations/metrics/tolerance are unchanged.

Not executed; no readiness or outcome claim. `preparation-lock.json` pins the current script and inherited dependencies; `prior-preparation.json` binds the original. Use project Python only:

```sh
cd /Users/destiner/Code/jeff/.worktrees/evaluation
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python /Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v2/run.py \
  --start-original300 "$START_ORIGINAL" --start-reversed300 "$START_REVERSED" --start-probes24 "$START_PROBES" \
  --trained-original300 "$TRAINED_ORIGINAL" --trained-reversed300 "$TRAINED_REVERSED" --trained-probes24 "$TRAINED_PROBES" \
  --evidence "$ACTUAL_START_RECEIPT" --evidence "$ACTUAL_TRAINED_RECEIPT" \
  --output-dir /Users/destiner/Code/jeff/artifacts/evaluation/e6-analysis-preparation-v2/execution-01
```

Require published real files and owner-reviewed actual receipt schemas/semantic controls. Additional `--evidence` files bind source/recipe/tokenization/training evidence; do not pass tensor files. No fake receipt, invented execution fields or automatic semantic equivalence. Failures remain in exclusive output namespaces. Preserve all frozen raw input/prediction bytes; no prefiltering malformed records. Train-fit evidence is separate, not consumed as development performance. No models, tests/lint, network, spending, final access, new framework or promotion.
