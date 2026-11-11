# D5 TRAIN presentation-order audit

Scope: recorded 1,500 TRAIN presentations and 375 consecutive four-presentation updates only. No loss values, optimizer/gradient analysis, other splits, model execution, or causal inference. Indices below are zero-based and endpoints inclusive; updates are one-based.

## Identity and pins

All schedule indices are 0–1499 in file order: True. All online IDs/indices match position-for-position: True. Every online update equals floor(index/4)+1: True; 375 updates each have four rows. Receipt reports 1500 presentations / 375 updates, status `complete`. Schedule matches frozen SHA-256; online bytes match receipt SHA-256.

The recorded order is analyzed directly, not reconstructed from manifest order. Interleaving is observed; no claim is made about how the pinned permutation was generated or whether it is random.

## Family exposure

| Family | Count | First–last | Runs | Maximum run: index range(s) |
|---|---:|---|---:|---|
| intent | 500 | 1–1497 | 346 | 6: [[985, 990], [1018, 1023]] |
| rule_application | 500 | 0–1499 | 335 | 7: [[1134, 1140]] |
| sentiment | 500 | 7–1489 | 320 | 7: [[504, 510], [944, 950], [994, 1000]] |

## Source-group contiguous exposure (separate from example groups)

Source group means the first three colon-separated components of `group_id` (pilot version + source namespace), not an asserted original file shard. Revision aliases remain exact in `source-aliases.json`; these labels are not silently merged with original-shard counts. No manifest or additional rows were needed/read.

| Source group | Family | Count | First–last | Runs | Maximum run: index range(s) |
|---|---|---:|---|---:|---|
| data:pilot-v1:intent | intent | 100 | 22–1497 | 91 | 2: [[143, 144], [154, 155], [166, 167], [291, 292], [415, 416], [621, 622], [973, 974], [1119, 1120], [1485, 1486]] |
| data:pilot-v1:rule_application | rule_application | 100 | 10–1498 | 93 | 2: [[561, 562], [893, 894], [1013, 1014], [1136, 1137], [1139, 1140], [1307, 1308], [1492, 1493]] |
| data:pilot-v1:sentiment | sentiment | 100 | 7–1489 | 94 | 2: [[125, 126], [393, 394], [596, 597], [1186, 1187], [1197, 1198], [1277, 1278]] |
| data:pilot-v2:intent-a | intent | 200 | 1–1494 | 178 | 3: [[29, 31], [581, 583]] |
| data:pilot-v2:intent-b | intent | 200 | 3–1496 | 180 | 4: [[987, 990]] |
| data:pilot-v2:rule-a | rule_application | 200 | 5–1490 | 170 | 4: [[127, 130]] |
| data:pilot-v2:rule-b | rule_application | 200 | 0–1499 | 165 | 5: [[1330, 1334]] |
| data:pilot-v2:sentiment-a | sentiment | 200 | 12–1487 | 166 | 4: [[1252, 1255]] |
| data:pilot-v2:sentiment-b | sentiment | 200 | 17–1481 | 164 | 4: [[692, 695]] |

## Transitions and runs

- `family`: 1000 changes / 1499 adjacent pairs; 499 same-label adjacent pairs; 1001 runs, maximum 7; run-length histogram {1: 697, 2: 187, 3: 69, 4: 30, 5: 10, 6: 4, 7: 4}.
- `source_group`: 1300 changes / 1499 adjacent pairs; 199 same-label adjacent pairs; 1301 runs, maximum 5; run-length histogram {1: 1132, 2: 147, 3: 15, 4: 6, 5: 1}.
- `source`: 1358 changes / 1499 adjacent pairs; 141 same-label adjacent pairs; 1359 runs, maximum 5; run-length histogram {1: 1239, 2: 106, 3: 8, 4: 5, 5: 1}.
- `group_id`: 1495 changes / 1499 adjacent pairs; 4 same-label adjacent pairs; 1496 runs, maximum 2; run-length histogram {1: 1492, 2: 4}.

Full directed transition counts (including self-transitions), per-label first/last occurrences and all tied maximum locations are in `summary.json`; every contiguous run is in `runs.json`.

## Fixed windows

| Window (indices) | Family counts | Source-group counts |
|---|---|---|
| prefix100 (0–99) | intent=38, rule_application=32, sentiment=30 | pilot-v1:intent=2, pilot-v1:rule_application=4, pilot-v1:sentiment=5, pilot-v2:intent-a=20, pilot-v2:intent-b=16, pilot-v2:rule-a=15, pilot-v2:rule-b=13, pilot-v2:sentiment-a=13, pilot-v2:sentiment-b=12 |
| suffix100 (1400–1499) | intent=34, rule_application=38, sentiment=28 | pilot-v1:intent=7, pilot-v1:rule_application=5, pilot-v1:sentiment=9, pilot-v2:intent-a=16, pilot-v2:intent-b=11, pilot-v2:rule-a=12, pilot-v2:rule-b=21, pilot-v2:sentiment-a=12, pilot-v2:sentiment-b=7 |
| prefix250 (0–249) | intent=83, rule_application=69, sentiment=98 | pilot-v1:intent=16, pilot-v1:rule_application=8, pilot-v1:sentiment=18, pilot-v2:intent-a=36, pilot-v2:intent-b=31, pilot-v2:rule-a=35, pilot-v2:rule-b=26, pilot-v2:sentiment-a=37, pilot-v2:sentiment-b=43 |
| suffix250 (1250–1499) | intent=78, rule_application=92, sentiment=80 | pilot-v1:intent=15, pilot-v1:rule_application=15, pilot-v1:sentiment=21, pilot-v2:intent-a=35, pilot-v2:intent-b=28, pilot-v2:rule-a=33, pilot-v2:rule-b=44, pilot-v2:sentiment-a=30, pilot-v2:sentiment-b=29 |
| prefix500 (0–499) | intent=163, rule_application=148, sentiment=189 | pilot-v1:intent=35, pilot-v1:rule_application=22, pilot-v1:sentiment=33, pilot-v2:intent-a=68, pilot-v2:intent-b=60, pilot-v2:rule-a=66, pilot-v2:rule-b=60, pilot-v2:sentiment-a=75, pilot-v2:sentiment-b=81 |
| suffix500 (1000–1499) | intent=171, rule_application=180, sentiment=149 | pilot-v1:intent=31, pilot-v1:rule_application=36, pilot-v1:sentiment=36, pilot-v2:intent-a=70, pilot-v2:intent-b=70, pilot-v2:rule-a=71, pilot-v2:rule-b=73, pilot-v2:sentiment-a=60, pilot-v2:sentiment-b=53 |
| decile1 (0–149) | intent=54, rule_application=46, sentiment=50 | pilot-v1:intent=6, pilot-v1:rule_application=6, pilot-v1:sentiment=12, pilot-v2:intent-a=26, pilot-v2:intent-b=22, pilot-v2:rule-a=23, pilot-v2:rule-b=17, pilot-v2:sentiment-a=17, pilot-v2:sentiment-b=21 |
| decile2 (150–299) | intent=48, rule_application=36, sentiment=66 | pilot-v1:intent=14, pilot-v1:rule_application=4, pilot-v1:sentiment=9, pilot-v2:intent-a=19, pilot-v2:intent-b=15, pilot-v2:rule-a=17, pilot-v2:rule-b=15, pilot-v2:sentiment-a=28, pilot-v2:sentiment-b=29 |
| decile3 (300–449) | intent=44, rule_application=52, sentiment=54 | pilot-v1:intent=10, pilot-v1:rule_application=10, pilot-v1:sentiment=11, pilot-v2:intent-a=18, pilot-v2:intent-b=16, pilot-v2:rule-a=20, pilot-v2:rule-b=22, pilot-v2:sentiment-a=24, pilot-v2:sentiment-b=19 |
| decile4 (450–599) | intent=52, rule_application=40, sentiment=58 | pilot-v1:intent=11, pilot-v1:rule_application=11, pilot-v1:sentiment=12, pilot-v2:intent-a=18, pilot-v2:intent-b=23, pilot-v2:rule-a=14, pilot-v2:rule-b=15, pilot-v2:sentiment-a=20, pilot-v2:sentiment-b=26 |
| decile5 (600–749) | intent=49, rule_application=61, sentiment=40 | pilot-v1:intent=10, pilot-v1:rule_application=15, pilot-v1:sentiment=9, pilot-v2:intent-a=19, pilot-v2:intent-b=20, pilot-v2:rule-a=24, pilot-v2:rule-b=22, pilot-v2:sentiment-a=11, pilot-v2:sentiment-b=20 |
| decile6 (750–899) | intent=53, rule_application=60, sentiment=37 | pilot-v1:intent=12, pilot-v1:rule_application=10, pilot-v1:sentiment=4, pilot-v2:intent-a=22, pilot-v2:intent-b=19, pilot-v2:rule-a=24, pilot-v2:rule-b=26, pilot-v2:sentiment-a=18, pilot-v2:sentiment-b=15 |
| decile7 (900–1049) | intent=51, rule_application=39, sentiment=60 | pilot-v1:intent=8, pilot-v1:rule_application=12, pilot-v1:sentiment=8, pilot-v2:intent-a=15, pilot-v2:intent-b=28, pilot-v2:rule-a=11, pilot-v2:rule-b=16, pilot-v2:sentiment-a=29, pilot-v2:sentiment-b=23 |
| decile8 (1050–1199) | intent=54, rule_application=55, sentiment=41 | pilot-v1:intent=12, pilot-v1:rule_application=13, pilot-v1:sentiment=10, pilot-v2:intent-a=19, pilot-v2:intent-b=23, pilot-v2:rule-a=24, pilot-v2:rule-b=18, pilot-v2:sentiment-a=19, pilot-v2:sentiment-b=12 |
| decile9 (1200–1349) | intent=48, rule_application=53, sentiment=49 | pilot-v1:intent=8, pilot-v1:rule_application=10, pilot-v1:sentiment=13, pilot-v2:intent-a=24, pilot-v2:intent-b=16, pilot-v2:rule-a=23, pilot-v2:rule-b=20, pilot-v2:sentiment-a=15, pilot-v2:sentiment-b=21 |
| decile10 (1350–1499) | intent=47, rule_application=58, sentiment=45 | pilot-v1:intent=9, pilot-v1:rule_application=9, pilot-v1:sentiment=12, pilot-v2:intent-a=20, pilot-v2:intent-b=18, pilot-v2:rule-a=20, pilot-v2:rule-b=29, pilot-v2:sentiment-a=19, pilot-v2:sentiment-b=14 |

`windows.json` also supplies exact provenance.source counts, with explicit zero counts, for each fixed prefix/suffix and decile.

## Update mixtures and group distinction

- Distinct families per update: {1: 20, 2: 191, 3: 164}; family multiplicity patterns: {'2+1+1': 164, '2+2': 71, '3+1': 120, '4': 20}.
- Distinct source groups per update: {1: 2, 2: 39, 3: 183, 4: 151}; distinct exact group IDs: {3: 8, 4: 367}.
- 8 updates repeat an exact group ID; 8 presentations beyond the first of their group within those updates. Update IDs: [21, 124, 150, 172, 175, 204, 274, 345].
- Observed group-size histogram (size → number of groups): {1: 800, 4: 50, 10: 10, 20: 20}.
- A named rule/mechanism group can have multiple presentations; a singleton scenario group contributes only one presentation in this schedule. These are not comparable counts of independent mechanisms. Repeated non-rule groups are kept separate; their semantics are not inferred from count alone. `groups.json` records every group, its classification, indices, and update IDs.
- `updates.json` records every update’s four IDs, ordered family/source-group/group sequences, exact-source and family/group compositions, and repeated-group multiplicities. `summary.json` includes every family composition frequency.

## Reproduction and evidence

Run `python3 /Users/destiner/Code/jeff/artifacts/data/d5-20261111T161610Z/order-audit/analyze.py`. Python standard library only. Reads exactly the four pinned input paths listed below; writes only this directory. Does not inspect loss fields semantically, fit summaries, weights, or any other rows. Source strings containing per-case fragments are retained verbatim; exact-source contiguity can therefore differ substantially from source-group contiguity.

| Input | SHA-256 |
|---|---|
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/train-audit/schedule.jsonl` | `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8` |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/online.jsonl` | `66cc8fbcf2a041472c5705f8d76073a13be83d8160e6d97db011d256e1c59cb6` |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/receipt.json` | `893c6a1b154734133d49ce41036a05bef2b5830c3615070b3547d56aebff1657` |
| `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/full-run-freeze.json` | `13f2e6f88f6e99323645a748ecaffdc7aa709cc43cb19fb35fd6a63e435b9ed9` |

These are descriptive exposure facts for Model/Evaluation interpretation, not an optimization diagnosis, evaluation result, recommendation to reshuffle, or authorization for another run.
