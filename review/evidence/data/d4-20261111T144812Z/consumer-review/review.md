# D4 — single-pass consumer-flow inspection

**Conclusion: no Data intervention identified.** No unresolved Data-owned manifest, schema, hash, split, token-budget, or interpretation issue is identified in the inspected public handoffs.

## Scope and evidence boundary

Read project `AGENTS.md` and six concise public consumer handoffs listed below. Listed public handoff filenames and Evaluation modification times once to locate relevant reports; no newer Evaluation final report was present in that listing (latest relevant E4 request: 14:25 UTC). This is a bounded snapshot, not monitoring or a final-scoring claim.

No predictions, inputs, private Evaluation references/probes/finals, weights, raw held-out data, or arbitrary artifact contents were opened. No Data release metadata needed opening. All execution/hash-validation statements below are attributed peer reports, **not Data-executed checks**. No tests, lint, Git, mailbox, models, network, installs, or spend.

## Consumer findings

- **Manifest/hash/schema binding:** E4 explicitly accepts immutable Data013 release bytes, not candidate bytes, with manifest SHA256 `d74bfda56fc18c89c4a40852dd46d9ec8bce1c907c9ebc8cbc979f23d9047ca9`. E4 reports rechecking 136 hash declarations and exact reference-to-five-field export identity for 96 originals. Model reports binding the same manifest, E4 input hash `afd02eb196889f79384488fa1998dcb95c79d96dccd1235a70fd30940c2bf928`, and boundary hash `6202826900d634440598d370fc1cef0972c65aab45bcff92a2f2cceb95adc06e`. No conflicting release identity or schema failure is reported.
- **Split and interpretation:** E4 and Model retain 96 cases / 48 new policy-source groups / 8 intentionally seen mechanisms. E4 states that two cases per policy are consequential cases, not reversal pairs; Model keeps D3 separate from v2 unseen-mechanism validation and existing probes. E4 retains permanent never-train derivative usage, rule-verified/programmatic provenance, same-model-alias review limitations, and residual hints. Model does not infer model-selection conclusions from raw predictions. No interpretation correction for Data is identified.
- **Token budget and inference:** Model reports four fresh-process snapshot runs, 96 predictions each (384 total), with 361 complete tokenizer pairs per snapshot, maximum 129 tokens at unchanged native cap 256, zero overflow, and preserved checkpoint inventories. These match the supplied D3 release dimensions. Inference execution remains Model-owned.
- **Probe exclusion and scoring:** E4 reports zero private historical/probe exact-identity/content hits with bounded normalization and explicitly disclaims semantic novelty/derivative clearance. This is Evaluation-owned evidence, not a Data exclusion check. Independent E4/E5 scoring is not established as finished by these handoffs; absence of a newer public final report is not a Data action.

## Resolved consumer-owned pre-load bug — not a Data action

Runtime's first P3 attempt failed before model/tokenizer construction or predictions because it looked up frozen config/input paths in the outer audit receipt instead of `audit['evidence']`. Release owns this audit-envelope lookup bug; it is not a D3 release-manifest/schema defect. Release reports the minimal correction, preserved failure, fresh freeze, and unchanged model/config/prompt/input/tokenization controls. Model reports reviewing the changed pins and granting a new explicit slot.

Release subsequently reports corrected process exit 0 and all 624 E5 presentations completed (300 originals + 300 reversed + 24 probes), with the slot returned. Model's 14:45 handoff corroborates the completed return and reports independently matching output hashes/counts. These E5/P3 counts and cap 1024/max 220 describe a separate consumer flow, not a change to D3's 96 cases or native cap 256. No unresolved pre-load repair is assigned to Data.

## Action and ownership

**No Data intervention identified.** No release edit, re-export, schema/hash repair, split change, token-budget adjustment, or interpretation amendment is requested by the inspected evidence. Existing independent scoring/probe-exclusion responsibilities remain Evaluation's; inference and scheduling remain Model's; the resolved P3 lookup correction remains Release's. No new gate or framework is proposed.

## Public sources inspected

Paths relative to `artifacts/handoffs/`:

1. `model/20261111T1431-D3-predictions-ready.md`
2. `model/20261111T1442-D3-integrated-P3-scheduled.md`
3. `model/20261111T1445-D3-P3-scheduler-delivered.md`
4. `evaluation/20261111-e4-D3-released-inputs-M4-request.md`
5. `release/20261111T1442-P3-predictions-ready-slot-returned.md`
6. `release/20261111T1436-P3-corrected-freeze-renewed-slot-request.md`
