# D5 bounded TRAIN schedule audit

This specific mapping/coverage defect is NOT demonstrated. This is not a finding that training code is correct.

- Original TRAIN: **1500 rows / 1500 unique IDs / 9 manifest shards**.
- Row-level and binding mismatches: **0**.
- Original-target slot → permuted-target slot: **1096 changed / 404 unchanged** (zero-based; labels taken only from original target IDs).
- Option arities: `{"2": 1, "3": 394, "4": 1035, "5": 56, "6": 14}`.
- Input hashes unchanged at audit exit: **True**.

## Coverage

| File | Rows | Unique IDs | Missing | Unknown/nontrain | Duplicate IDs | Index coverage/order |
|---|---:|---:|---:|---:|---:|---|
| schedule | 1500 | 1500 | 0 | 0 | 0 | True |
| fit-before | 1500 | 1500 | 0 | 0 | 0 | True |
| fit-after | 1500 | 1500 | 0 | 0 | 0 | True |
| online | 1500 | 1500 | 0 | 0 | 0 | True |

Verified exact decision ID/state/question/schema, original option order, bijective option ID→text preservation, target ID and remapped target position, retained family/group/provenance. Replayed declared Random(42) row shuffle and per-row option shuffle. Both fit files are joined by ID/index/option IDs and checked against original targets, source/group/family, valid positions, finite CE and recorded agreement.

## Actual schema limitation

Online actual schema is ce,id,index,qualification,update; ID/index and CE checked. It does not record option IDs, positions, agreements, family, group or source, so these cannot be independently joined/verified for online rows.

## Source shards

| TRAIN shard | Rows | SHA-256 |
|---|---:|---|
| `data/data-pilot-v1/intent/train.jsonl` | 100 | `119ef093712012886ddc66f02e2635e082bf9b905fb79aaf7440c2547692c589` |
| `data/data-pilot-v1/sentiment-r2/train.jsonl` | 100 | `4c1b9513186ef8a7749b67450e890f9d9bd7e44b74c160c7576f0607eac6256b` |
| `data/data-pilot-v1/rule_application/train.jsonl` | 100 | `24c9b8684c1d35589d44a00685ce53b33f6bf0da4f7dc9a28e3a1f1fddb41a5d` |
| `data/data-pilot-v2/intent-a-r2/train.jsonl` | 200 | `77cb6b5436415aee55bd0449590f9586a73a148f3270b9ac116348cbba79cae9` |
| `data/data-pilot-v2/intent-b-r2/train.jsonl` | 200 | `d551a90e504b7ad6ab0a535c953514edbf9bfc87a91d536f8dcd8b6958a3385c` |
| `data/data-pilot-v2/sentiment-a/train.jsonl` | 200 | `0d0cdced2810ba68bbd1d1a672d65f940ee8f0e5798ce7967bd522fd577a549b` |
| `data/data-pilot-v2/sentiment-b-r2/train.jsonl` | 200 | `0c2d5441102fb0623dec43265f3d9dc44b025c92b788138344cdc1447ac1ab20` |
| `data/data-pilot-v2/rule-a/train.jsonl` | 200 | `5716c4c263fc82607ecae10eede1bdd5dad3d884ef650c89de0d264f8eb01a9f` |
| `data/data-pilot-v2/rule-b/train.jsonl` | 200 | `549b1cfe8a3b3981c18b26f003cf9699881227c51b10ed7daa60068603ad7669` |

## Target slot transitions

| Original slot | Permuted slot | Rows |
|---:|---:|---:|
| 0 | 0 | 122 |
| 0 | 1 | 119 |
| 0 | 2 | 104 |
| 0 | 3 | 58 |
| 0 | 4 | 2 |
| 1 | 0 | 128 |
| 1 | 1 | 112 |
| 1 | 2 | 101 |
| 1 | 3 | 63 |
| 1 | 4 | 2 |
| 2 | 0 | 109 |
| 2 | 1 | 120 |
| 2 | 2 | 100 |
| 2 | 3 | 71 |
| 2 | 4 | 4 |
| 3 | 0 | 69 |
| 3 | 1 | 71 |
| 3 | 2 | 60 |
| 3 | 3 | 68 |
| 3 | 4 | 1 |
| 4 | 0 | 2 |
| 4 | 1 | 1 |
| 4 | 2 | 1 |
| 4 | 3 | 5 |
| 4 | 4 | 2 |
| 4 | 5 | 1 |
| 5 | 0 | 1 |
| 5 | 2 | 2 |
| 5 | 3 | 1 |

## Exact input hashes

All below are SHA-256 of complete allowed input bytes. Before/after comparison is recorded per file in `report.json`.

| Input | SHA-256 | Unchanged |
|---|---|---|
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/intent/train.jsonl` | `119ef093712012886ddc66f02e2635e082bf9b905fb79aaf7440c2547692c589` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/rule_application/train.jsonl` | `24c9b8684c1d35589d44a00685ce53b33f6bf0da4f7dc9a28e3a1f1fddb41a5d` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1/sentiment-r2/train.jsonl` | `4c1b9513186ef8a7749b67450e890f9d9bd7e44b74c160c7576f0607eac6256b` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/intent-a-r2/train.jsonl` | `77cb6b5436415aee55bd0449590f9586a73a148f3270b9ac116348cbba79cae9` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/intent-b-r2/train.jsonl` | `d551a90e504b7ad6ab0a535c953514edbf9bfc87a91d536f8dcd8b6958a3385c` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/manifest.json` | `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/rule-a/train.jsonl` | `5716c4c263fc82607ecae10eede1bdd5dad3d884ef650c89de0d264f8eb01a9f` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/rule-b/train.jsonl` | `549b1cfe8a3b3981c18b26f003cf9699881227c51b10ed7daa60068603ad7669` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/sentiment-a/train.jsonl` | `0d0cdced2810ba68bbd1d1a672d65f940ee8f0e5798ce7967bd522fd577a549b` | True |
| `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/sentiment-b-r2/train.jsonl` | `0c2d5441102fb0623dec43265f3d9dc44b025c92b788138344cdc1447ac1ab20` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/full-run-freeze.json` | `13f2e6f88f6e99323645a748ecaffdc7aa709cc43cb19fb35fd6a63e435b9ed9` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/train-audit/audit.json` | `16a5dd978f47e22ec4e0c0b71f99fd6d6ed4e9cb0698e3d2fe25b6ca274cb1e5` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/train-audit/schedule.jsonl` | `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/fit-after.jsonl` | `a099822f30a234b0b3d2ff588888d712897bf5b1af4cbb878369cc23e619ca84` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/fit-before.jsonl` | `d13d8602294732339056781f1148426be1ef3003b9b8ce9bc833142ecdd83312` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/online.jsonl` | `66cc8fbcf2a041472c5705f8d76073a13be83d8160e6d97db011d256e1c59cb6` | True |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/receipt.json` | `893c6a1b154734133d49ce41036a05bef2b5830c3615070b3547d56aebff1657` | True |

## Mismatches

None.

## Reproduction and boundaries

`python3 /Users/destiner/Code/jeff/artifacts/data/d5-20261111T161610Z/schedule-audit/audit.py`

Stdlib only. Refuses existing report files: for reproduction preserve/move the two generated reports within the authorized output directory first. No fixtures or software tests. `report.json` includes observed schemas, all check counts, binding comparisons, all 1,500 row-level original/permuted target slots and every mismatch.

- Online actual schema is ce,id,index,qualification,update; ID/index and CE checked. It does not record option IDs, positions, agreements, family, group or source, so these cannot be independently joined/verified for online rows.
- Original targets are accepted as labels; no semantic correctness review or label inference from slot positions.
- Prompt token counts/domain checked, but no tokenizer/model executed; prompt_token_sha256 serialization and token-to-text semantics are not independently established.
- Only hashes of allowed files are verified; other freeze receipt pins and all model/weight/private paths are not followed.
- Input immutability compares bytes at this script run entry with bytes at exit; no earlier-history claim.
