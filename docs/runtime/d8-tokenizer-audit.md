# D8 tokenizer audit — closed execution record

## Result and scope

Attempt **07** completed the tokenizer-only audit: all **800 pairs fit**, across
1,600 presentations, 2,400 audit records, 3,200 encoder candidate pairs and
1,600 decoder prompts. Maximum encoder/decoder lengths were **54 / 89** tokens
against frozen caps **256 / 1,024**. These are runtime token-fit facts, not model
quality, population selection, confirmation eligibility or promotion evidence.
Data/Evaluation, not Runtime, select the population.

The successful parent took **6.101216292008758 seconds**; cumulative charged
actual parent time was **20.819555623922497 / 180 seconds**, including
14.71833933191374 seconds from five earlier executed attempts. Exit was zero
and the process group was absent. No model construction, weight read, forward
or GPU execution occurred. **Torch definitions were imported**; do not describe
this as a no-Torch-import run.

## All attempts remain closed

| Attempt | Parent seconds | Outcome retained |
| --- | ---: | --- |
| 01 | 0.0461804578 | Exit 71 before audit entry; stderr discarded, cause unknown. |
| 02 | 0.046074875 | SIGABRT before audit entry. |
| 03 | 4.415010666 | Scratch-access denial after Torch import. |
| 04 | 4.942871250 | Vocabulary false positive. |
| 05 | — | Never executed; not a zero-time successful attempt. |
| 06 | 5.2682020827 | Directory-listing denial during local-file discovery, before tokenizer construction. |
| 07 | 6.101216292008758 | Complete; all 800 pairs fit. |

Earlier failures are not erased by 07. Prior executed attempts tokenized zero
presentations. Attempt 06 entered the tokenizer-loading API but failed before
`_from_pretrained` / the tokenizer class constructor; that is not a universal
statement about every imported definition. Rounded per-attempt display values
do not replace the retained cumulative timer.

## Access and measurement qualifications

The 07 policy added exactly two literal directory-listing allowances:

- `/Users/destiner/Code/jeff/artifacts/release/p3-qwen-20261111-01/download/model`
- `/Users/destiner/Code/jeff/artifacts/model/m4-v2-20261111-01/msmarco/baseline/tokenizer`

These are **not recursive asset or weight access**. Actual access scope is the
retained Seatbelt policy, including its runtime/system/library allowances,
literal authorized files and fresh output tree. Python file-access logs do
**not** cover all native opens; they are not the access enforcement boundary.
Network was denied by Seatbelt. Raw private stderr is not publishable.

Sampled process-group RSS peaked at 466,944,000 bytes; native child lifetime RSS
high-water was 477,200,384 bytes. These different measurements are not additive
and are not a kernel allocation hard limit or a continuous group peak.

## Canonical evidence

All paths below are relative to `/Users/destiner/Code/jeff/artifacts/release/`;
no evidence was regenerated for this publication.

- `d8-token-pass-20261112-07/delivery-summary.json`
- `d8-token-pass-20261112-07/parent-receipt.json`
- `d8-token-pass-20261112-07/audit/status.json`
- `d8-token-parent-20261112-07/policy.diff` and `offline.sb`
- `d8-token-parent-20261112-07/final-binding.json` (pin only; not a request to open protected inputs)

Small provenance record: [D8 manifest](../../manifests/releases/d8-token-pass-20261112-07.json).
This documentation authorizes no replay or further access.
