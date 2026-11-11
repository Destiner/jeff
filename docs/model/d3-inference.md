# D3: inference-only seen-mechanism diagnostic

Completed Evaluation E4's four original-only prediction requests using the **existing M4** MiniLM and retained-head MS MARCO starting/trained snapshots. No new training, tuning, checkpoints, default selection or option-reversal replay.

## Frozen inputs and scope

- Data release: `artifacts/data/data-d3-seen-rules-v1/release/manifest.json`, SHA256 `d74bfda56fc18c89c4a40852dd46d9ec8bce1c907c9ebc8cbc979f23d9047ca9`.
- E4 label-free input: `artifacts/evaluation/e4-d3-released-boundary-v1/inputs.jsonl`, SHA256 `afd02eb196889f79384488fa1998dcb95c79d96dccd1235a70fd30940c2bf928`.
- E4 release boundary: `artifacts/evaluation/e4-d3-released-boundary-v1/boundary.json`, SHA256 `6202826900d634440598d370fc1cef0972c65aab45bcff92a2f2cceb95adc06e`.
- **96 original cases / 48 new policy-source groups / 8 intentionally seen training mechanisms**. Each mechanism has six policies and two distinct cases per policy; these are not option-order pairs or 96 independent sources. All examples and derivatives are permanently excluded from training.
- Only five decision fields and option ID/text were supplied to inference. Model did not read neighboring labeled references. Evaluation owns identity/exclusion, independent scoring and mechanism/policy breakdowns.

Use this as a separate seen-mechanism/new-policy diagnostic, not a combined headline with v2 unseen-mechanism validation or existing probes. Explicit training-mechanism overlap is intentional; exact historical/probe exclusion is not semantic-derivative clearance. Data's executable rule labels and same-alias bounded semantic review are not independent truth verification; repaired ambiguities and residual option hints remain qualifications.

## Executed queue and evidence

Root `R=/Users/destiner/Code/jeff/artifacts/model/m4-d3-inference-20261111-01/`.

Existing checkpoints under `artifacts/model/m4-v2-20261111-01/`:

| Snapshot | Output under R | Rows | Process wall seconds |
| --- | --- | ---: | ---: |
| minilm/baseline | minilm-baseline-predictions.jsonl | 96 | 2.928 |
| minilm/checkpoint | minilm-checkpoint-predictions.jsonl | 96 | 1.959 |
| msmarco/baseline | msmarco-baseline-predictions.jsonl | 96 | 1.961 |
| msmarco/checkpoint | msmarco-checkpoint-predictions.jsonl | 96 | 1.950 |

Four sequential fresh processes, all exit0, **384 prediction rows**, approximately8.799seconds summed process wall including interpreter/load/inference. No per-example latency or accelerator-peak claim. Native cap256, temperature1, MPS, decision batch4; separate initially empty HF_HOME per job and offline flags, no dependency changes/model downloads.

Before loading, each saved tokenizer audited all **361 complete formatted candidate pairs**, truncation/padding disabled:56–129tokens, zero overflow at256. No cap change or silent truncation. All30checkpoint files match both persisted before/after inventories and the original M4 inventory; no extra checkpoint files or changed weights. The original M4 inventory itself was post-inference, not retroactively a pre-load attestation.

- `preflight.json`: exact input/release/boundary pins, four token audits, predictor source hash and execution revision `2d344c75c62740966362386535c954bfd5b3818e`.
- `receipt.json`, per-snapshot `*-invocation.json` and `*-receipt.json`: commands, times, exits, input/output/checkpoint hashes and coverage.
- `*-inventory-before.json`, `*-inventory-after.json`: independently inspectable checkpoint preservation.
- `execute.py`, `logs/`: fixed queue and actual execution output.
- [Compact evidence index](d3-inference-run.json). Prediction integrity was reviewed with CPU-only hashing/parsing; no duplicate inference or model/tokenizer load by the reviewer. All option probabilities are finite, normalized, and cover exactly the requested IDs/options.

E4 was notified directly with artifact links before Model integration; scoring does not wait for this merge. The release-bound inputs are not candidate data. The diagnostic-marker ingestion guard was already integrated at `c996916` after M5, without changing historical source commits/artifacts or training anything.

## Queue and resource handoff

D3 received the next available slot before Runtime P3. After all four processes exited, Runtime received a separate exclusive bounded grant for its authorized frozen challenger; no overlapping Model load was allowed. P3 is Runtime/E5-owned practical comparison evidence, not an encoder migration or additional training authority.

£0additional actual/pending/allocation. No software tests, linters, final-data access, paid service, data edits, training or default promotion. M5's completed lower-head-LR control and failed criterion remain unchanged; its D3 inference follow-through is now delivered.
