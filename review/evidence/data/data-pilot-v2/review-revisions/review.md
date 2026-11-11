# Jeff v2 — final revision review

**ACCEPT WITH LIMITS. No sampled MUSTFIX, disagreements, or unresolved label ambiguities.**

Reviewer environment: `PI_PROVIDER=openai`, `PI_MODEL=gpt-sol`. Immutable revision unavailable. Teacher agreement is not independent ground truth.

## Intent: judgments frozen before labels

The reviewer saw only IDs for bookkeeping and state/question/options before freezing 40 choices. `prepare.py` emitted no targets or provenance. Parent content and generators were first inspected after `blind-judgments-frozen.json` was written. Its SHA-256 remains `9ab59724f0aa64b98f2dad278b89ccdf833b5cd2624b408520da3127d4df7d7a`.

Sampling: sort IDs in each producer/split and select `round(i*(n-1)/9)` for `i=0..9`. Per producer: 10 train (`g001,g023,g045,g067,g089,g112,g134,g156,g178,g200`) and 10 validation (`g201,g205,g210,g214,g218,g223,g227,g231,g236,g240`), covering 14 domains. Both producers use this fixed sample.

**40/40 frozen choices agree with r2 teacher targets.** Sampled parent target actions are semantically retained, with no over-trimming or equally supported synonym rival found. Revised rivals are plausible neighboring requests and distinguishable as primary intents.

| Producer | Rows compared | Choice sets changed | Target texts changed | Rival texts changed | Total option texts changed |
|---|---:|---:|---:|---:|---:|
| intent-a-r2 | 240 | 240 | 240 | 713 | 953 / 953 |
| intent-b-r2 | 240 | 240 | 239 | 606 | 845 / 846 |

All **480** states, questions, groups, splits, schema/family, arities, ordered option IDs, target IDs and target slots are identical to parents. All 480 IDs and provenance objects intentionally change. All 480 source mapping rows match parents and revision exports exactly; authored sources (including B’s 150 target-refinement entries) reproduce all 480 option sets by direct comparison, without running producer code. **Mechanical equality is not all-row semantic proof.**

### Close contrasts, not MUSTFIX

- `data:pilot-v2:intent-b-r2:g001:r01`: Belt service and motor replacement are narrower potential repair methods, not logically disjoint downstream actions. The state does not identify either component as faulty, so neither is an equally supported primary intent. Broad mechanical repair is the sole supported request. Accepted under the contracts primary-choice interpretation, not a claim of literal action incompatibility.
- `data:pilot-v2:intent-a-r2:g205:r01`: Resending a bulletin is workflow-adjacent but the rival specifies delivery failure; the actual complaint is stale content, making investigation the supported primary intent.

## Sentiment: non-blind correction

`data:pilot-v2:sentiment-b-r2:g011:r01` now says **“Every sheet arrived uncreased, so I could use them all for the drawing.”** This removes the old “Not a crease survived” implication of eliminating pre-existing creases. Successful protective packaging and usable sheets support implicit positive-only sentiment (`c20117`), with no criticism. Prior exposure to the positive target is explicitly acknowledged; this is not a blind result.

All 240 rows compared: **one state changed; 239 states unchanged**. Every question, complete ordered option set, target, group and split is unchanged. All 240 IDs and provenance sources intentionally change; parent IDs form a complete bijection, sources are the exact expected parent-source prefix, and other provenance fields/teacher metadata are retained. Class coverage remains P/N/U/M = **50 each train; 10 each validation**. This verifies coverage, not full provenance equality or independent semantic correctness.

## Integrity and scope

**28/28 recorded parent/artifact/script hash references match.** All three assignment files are byte-identical to parents, assignment splits agree, and within each revision there is no train/validation group overlap. All six revised shards match candidate `pre-review-r3/manifest.json` hashes, counts and splits. The other 12 candidate entries were not opened.

Before/after and final SHA snapshots preserve **53/53 input files**, with no changes. No producer files were modified or executed. New review files only were created under this directory.

## Per-row frozen choices and post-freeze parent comparison

| ID | Split | Frozen choice | Parent target → revised target | Agreement |
|---|---|---|---|---|
| `data:pilot-v2:intent-a-r2:g001:r01` | train | `o5c85050f0440cf` | Resolve a delayed broadband activation → Resolve the overdue service activation | yes |
| `data:pilot-v2:intent-a-r2:g023:r01` | train | `obbe25a4c5590a8` | Unsubscribe from recipe emails → Remove the subscriber from the recipe mailing list | yes |
| `data:pilot-v2:intent-a-r2:g045:r01` | train | `o462f081cbf5dc5` | Explain step-free boarding access → Confirm whether wheelchair boarding is step-free | yes |
| `data:pilot-v2:intent-a-r2:g067:r01` | train | `o6f9041c64e5bb0` | Request pedestrian diversion information → Explain the signed pedestrian diversion around the works | yes |
| `data:pilot-v2:intent-a-r2:g089:r01` | train | `o1c7b8aae5c5774` | Transfer an unused training session → Transfer the unused personal training session to the partner | yes |
| `data:pilot-v2:intent-a-r2:g112:r01` | train | `o9db21d8d8ed214` | Postpone the venue booking → Move the existing hall booking from March to May | yes |
| `data:pilot-v2:intent-a-r2:g134:r01` | train | `o2e9257b5062337` | Transfer the smartcard balance → Move remaining credit from the old card to the new one | yes |
| `data:pilot-v2:intent-a-r2:g156:r01` | train | `o2f3ed2777de2c2` | Request an energy tariff comparison → Compare available energy tariffs for the customer's usage | yes |
| `data:pilot-v2:intent-a-r2:g178:r01` | train | `oe14e1ac58b8fb0` | Dispute a late-return charge → Remove the late fee contradicted by the return receipt | yes |
| `data:pilot-v2:intent-a-r2:g200:r01` | train | `o31de3debacfd89` | Ask about signed-copy availability → Check whether signed copies of the biography will be available | yes |
| `data:pilot-v2:intent-a-r2:g201:r01` | validation | `oc311ea774914cf` | Change the bulletin coverage area → Switch future bulletins to the eastern shipping area | yes |
| `data:pilot-v2:intent-a-r2:g205:r01` | validation | `oabf9be7266941d` | Report an out-of-date weather bulletin → Investigate the bulletin containing yesterday's forecast timestamp | yes |
| `data:pilot-v2:intent-a-r2:g210:r01` | validation | `o3226de1c19d367` | Activate severe weather alerts → Add immediate severe-weather alerts alongside daily bulletins | yes |
| `data:pilot-v2:intent-a-r2:g214:r01` | validation | `o6c94803a74ea63` | Obtain a written appraisal report → Provide a written report from the completed chest appraisal | yes |
| `data:pilot-v2:intent-a-r2:g218:r01` | validation | `ob8362cfa894c5c` | Correct ownership details in the report → Correct the watch owner's attribution without changing value | yes |
| `data:pilot-v2:intent-a-r2:g223:r01` | validation | `o83bd8f5f26091e` | Verify a certificate's authenticity → Confirm whether the referenced certificate was genuinely issued | yes |
| `data:pilot-v2:intent-a-r2:g227:r01` | validation | `odf0f067c40cee6` | Update the certificate mailing address → Change the mailing address before certificate dispatch | yes |
| `data:pilot-v2:intent-a-r2:g231:r01` | validation | `o0e9b724da99cdf` | Ask about route difficulty → Explain the ridge route's technical climbing difficulty | yes |
| `data:pilot-v2:intent-a-r2:g236:r01` | validation | `o0f3bb0e3d154cd` | Ask about reported anchor condition → Provide recent reported condition information for the top anchors | yes |
| `data:pilot-v2:intent-a-r2:g240:r01` | validation | `oe271d27d29d3c9` | Request offline access to the route guide → Explain how to save the route guide for offline use | yes |
| `data:pilot-v2:intent-b-r2:g001:r01` | train | `o74ec4b1d20d59021` | Arrange a mechanical repair → Arrange repair of the jammed mechanism | yes |
| `data:pilot-v2:intent-b-r2:g023:r01` | train | `oa65669d34e0c5b0c` | Pause walks temporarily → Pause until the 18th, then resume walks | yes |
| `data:pilot-v2:intent-b-r2:g045:r01` | train | `od532681f0c3d6d6a` | Supply the compliance document → Supply the glazing compliance certificate | yes |
| `data:pilot-v2:intent-b-r2:g067:r01` | train | `o0a45ef2f70b59190` | Enrol in the advanced workshop → Book the advanced viennoiserie workshop | yes |
| `data:pilot-v2:intent-b-r2:g089:r01` | train | `o42bf5ff3c6c99672` | Change the delivery recipient → Change the delivery recipient to the neighbour | yes |
| `data:pilot-v2:intent-b-r2:g112:r01` | train | `o5b5e3fb91dd7025f` | Explain how to operate the alarm → Explain how to set the alarm's night mode | yes |
| `data:pilot-v2:intent-b-r2:g134:r01` | train | `o7ced76e729535f9e` | Explain the stairs surcharge → Explain the quoted stairs surcharge | yes |
| `data:pilot-v2:intent-b-r2:g156:r01` | train | `o31cbd29eea7ed239` | Report a conduct violation → Report the player's repeated abuse | yes |
| `data:pilot-v2:intent-b-r2:g178:r01` | train | `oc8e69f5fd19e71b4` | Disable automatic renewal → Stop auto-renewal, keeping current validity | yes |
| `data:pilot-v2:intent-b-r2:g200:r01` | train | `odc44fd7e84411790` | Change the reusable box size → Use a smaller reusable box next time | yes |
| `data:pilot-v2:intent-b-r2:g201:r01` | validation | `o2b67d8e59ddec3c6` | Begin a new operator registration → Start a first operator registration | yes |
| `data:pilot-v2:intent-b-r2:g205:r01` | validation | `o98dd241ee57745d8` | Cancel the duplicate application → Withdraw only the later duplicate application | yes |
| `data:pilot-v2:intent-b-r2:g210:r01` | validation | `o77c0c5a8667243fa` | Provide registration instructions → Explain operator details; leave submission to me | yes |
| `data:pilot-v2:intent-b-r2:g214:r01` | validation | `of4ef5f890b76bd88` | Explain the tour duration → Explain the old-town walk's total duration | yes |
| `data:pilot-v2:intent-b-r2:g218:r01` | validation | `oab3083f8c08df76d` | Arrange a private group tour → Book a private Tuesday tour for twelve | yes |
| `data:pilot-v2:intent-b-r2:g223:r01` | validation | `o887f87ee651298ef` | Check sharpening completion → Check whether tag 47 is ready to collect | yes |
| `data:pilot-v2:intent-b-r2:g227:r01` | validation | `ofb4cd46f057ba6eb` | Change the drop-off time → Move drop-off to 4 pm only | yes |
| `data:pilot-v2:intent-b-r2:g231:r01` | validation | `oe843e049277e1ff9` | Order an embossed copy → Order embossing of the correct transcription | yes |
| `data:pilot-v2:intent-b-r2:g236:r01` | validation | `o09265f26dc783214` | Cancel the unstarted order → Cancel transcription before work starts | yes |
| `data:pilot-v2:intent-b-r2:g240:r01` | validation | `o77296ea62c88d734` | Quote for braille transcription → Quote for braille; await production approval | yes |

Full blind reasons and post-freeze comparison are in `review.json`; immutable pre-comparison reasons are in `blind-judgments-frozen.json`.

## True limits

- Semantic review covers 40 deterministic intent rows (20 per producer, 10 train and 10 validation), not all 480. All-row structural equality and exact source mappings are not proof that all 479 revised target texts retain their intended meanings.
- Blind means target/metadata hidden from reviewer output before judgments were written. The projection script necessarily parsed labeled JSON rows in memory; only ID, state, question, options were emitted. No parent content or generator content was inspected until the freeze. IDs were retained as bookkeeping, not evidence.
- The systematic ID sample is not random or statistically representative. It covers 14 domains per producer (10 train domains and all four validation domains), not every domain or every possible ambiguity. No independent human judgments or immutable teacher-model revision are available.
- Agreement is reviewer/teacher agreement, not independently established ground truth; the current reviewer and original teachers expose the same model alias gpt-sol. No teacher or model calls were made.
- Explicit scope negations and state/option lexical overlap remain shortcuts; option-length residual bias is acknowledged, not measured afresh or claimed eliminated. No full length diagnostics, model/tokenizer budget audit, accuracy, calibration or order-sensitivity evaluation performed.
- Sentiment g011 review is knowingly label-exposed and not blind. The other 239 sentiment states were mechanically compared, not semantically relabeled. Class coverage uses parent source labels.
- Candidate manifest has 18 entries; only the six revised intent/sentiment shard files were opened and hash/count/split checked. Other 12 entries, inherited v1 data, unrelated producers and evaluation/final data were not opened. This is not a whole-manifest uniqueness or provenance audit.
- SHA preservation covers all 53 regular input files under the six specified producer/parent directories plus the candidate manifest as enumerated at start. It does not prove prior history, files outside that scope or filesystem atomicity during reads.
- Metadata sentiment revision_author records openai/gpt-astra as a historical author claim; this review cannot authenticate that earlier process. Current reviewer identity is only the actual PI_PROVIDER=openai and PI_MODEL=gpt-sol. Metadata teacher identity is retained from parent, not replaced by reviewer identity.
- No tests, lint, Git operations, checkout edits, producer execution/edits, builds, model loading, network/API calls, evaluation data access or additional/pending spend. Standard-library CPU file inspections only. The initial directory listing exposed filenames outside review scope, not their contents.

## Exact executed commands

The initial `ls` intentionally found no existing review directory (nonzero `ls` status; the combined command completed). One verbose inspection output was truncated by the tool; focused reads and the bounded `verification.json` provide the actual evidence. Producer generator files were read, never executed. The commands below are verbatim; reviewer script contents and SHA-256 are retained in this directory.

1.
```bash
pwd; find /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2 -maxdepth 2 -type f -not -path '*/review*/*' | sort; printenv PI_MODEL PI_PROVIDER
```

2.
```bash
wc -l /Users/destiner/Code/jeff/.worktrees/data/docs/{plan,coordination,swarm}.md; ls -ld /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/review-revisions; python3 - <<'PY'
import os
print({k:os.environ.get(k) for k in ['PI_MODEL','PI_PROVIDER']})
PY
```

3.
```bash
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/review-revisions/prepare.py
```

4.
```bash
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/review-revisions/freeze.py
```

5.
```bash
python3 - <<'PY'
import json
from pathlib import Path
b=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2')
for d in ['intent-a-r2','intent-b-r2','sentiment-b-r2']:
 for name in ['metadata.json','choice_mappings.json','source_mappings.json','target_refinements.json','revision.json','group_assignments.json']:
  p=b/d/name
  if not p.exists():continue
  x=json.loads(p.read_text()); print('\nFILE',p)
  if name in ['metadata.json','revision.json']:print(json.dumps(x,indent=2))
  else:
   print('type',type(x).__name__,'len',len(x));print(str(x)[:6500])
for d in ['intent-a','intent-b','sentiment-b']:
 p=b/d/'metadata.json';print('\nPARENT METADATA',p);print(p.read_text())
print('\nCANDIDATE MANIFEST');print((b/'pre-review-r3/manifest.json').read_text())
PY
```

6.
```bash
python3 - <<'PY'
import json
from pathlib import Path
b=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2')
x=json.loads((b/'intent-a-r2/choice_mappings.json').read_text());print('choice mapping type',type(x).__name__);print(str(x)[:4000])
for d in ['intent-a-r2','intent-b-r2','sentiment-b-r2']:
 r=json.loads((b/d/'train.jsonl').read_text().splitlines()[0]);print(d,'ROW SCHEMA',json.dumps(r))
for split in ['train','validation']:
 for line in (b/'sentiment-b-r2'/(split+'.jsonl')).read_text().splitlines():
  r=json.loads(line)
  if ':g011:' in r['id']:print('G011',json.dumps(r,indent=2))
PY
```

7.
```bash
python3 - <<'PY'
from pathlib import Path
b=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2')
for d,n in [('sentiment-b','source_cases.txt'),('intent-a-r2','choices.txt'),('intent-b-r2','authored_choices.txt')]:
 print(d,n); print('\n'.join((b/d/n).read_text().splitlines()[:6]))
PY
```

8.
```bash
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/review-revisions/verify.py
```

9.
```bash
python3 /Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/review-revisions/report.py
```

Read-tool operations (not shell commands):
- `/Users/destiner/Code/jeff/.worktrees/data/AGENTS.md`
- `/Users/destiner/Code/jeff/.worktrees/data/docs/contracts.md`
- `/Users/destiner/Code/jeff/.worktrees/data/docs/plan.md`
- `/Users/destiner/Code/jeff/.worktrees/data/docs/coordination.md`
- `/Users/destiner/Code/jeff/.worktrees/data/docs/swarm.md`
- `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/intent-a-r2/metadata.json`
- `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/intent-a-r2/apply.py`
- `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/intent-b-r2/apply_revision.py`
- `/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2/sentiment-b-r2/revise.py`
