"""Predeclare a 24-decision training audit without using labels or outcomes."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import random

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
OUT = ROOT / 'data/d4-20261111T144812Z'
MANIFEST = ROOT / 'data/data-pilot-v2/manifest.json'
EXPECTED = 'd97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac'
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(MANIFEST) == EXPECTED
manifest = json.loads(MANIFEST.read_text())
history_path = ROOT / 'data/data-d3-seen-rules-v1/review/review.json'
history = json.loads(history_path.read_text())['historical_train_comparison']
excluded = sorted({key for item in history for key in item['semantically_inspected_ids']})
plans = {
 'data/data-pilot-v1/rule_application/train.jsonl': [(f'data:pilot-v1:rule_application:g{g:02d}', [6]) for g in (1,4,7,10)],
 'data/data-pilot-v2/rule-a/train.jsonl': [(f'data:pilot-v2:rule-a:g{g:03d}', [6,7]) for g in (1,2,3,5,7)],
 'data/data-pilot-v2/rule-b/train.jsonl': [(f'data:pilot-v2:rule-b:g{g:03d}', [6,7]) for g in (2,5,6,8,10)],
}
selected, metadata, bindings = [], [], {}
for relative, groups in plans.items():
 entry = next(s for s in manifest['shards'] if s['path'] == relative)
 assert entry['split'] == 'train'
 path = ROOT / relative
 assert sha(path) == entry['sha256']
 bindings[relative] = entry['sha256']
 rows = [json.loads(line) for line in path.read_text().splitlines()]
 assert len(rows) == entry['rows']
 assignments_path = path.parent / 'group_assignments.json'
 assignments = json.loads(assignments_path.read_text())['groups']
 for group, positions in groups:
  ordered = sorted((r for r in rows if r['group_id'] == group), key=lambda r:r['id'])
  assert assignments[group]['split'] == 'train'
  for position in positions:
   row = ordered[position]
   assert row['split'] == 'train' and row['task_family'] == 'rule_application'
   assert row['id'] not in excluded
   selected.append(row)
   metadata.append({'id':row['id'], 'group_id':group, 'mechanism':assignments[group]['mechanism'],
                    'shard':relative, 'shard_sha256':entry['sha256'], 'ordinal_one_based':position+1,
                    'stratum':'inherited_v1' if 'data-pilot-v1' in relative else 'new_v2',
                    'assignment_sha256':sha(assignments_path)})
assert len(selected) == 24 and len({r['id'] for r in selected}) == 24
assert len({r['group_id'] for r in selected}) == 14
seed = 20261111144812
random.Random(seed).shuffle(selected)
selection = {
 'task':'D4', 'selected_at':datetime.now(timezone.utc).isoformat(), 'manifest':str(MANIFEST),
 'manifest_sha256':EXPECTED, 'selector_sha256':sha(Path(__file__)),
 'recipe':'4 inherited rows: ordinal7 from v1 groups01/04/07/10. 20 new rows: ordinals7/8 from rule-a groups001/002/003/005/007 and rule-b002/005/006/008/010. Metadata-only selection, no outcomes or target conditioning.',
 'reason':'Paired later-policy cases on eight D3-seen mechanisms plus authorization/conditional branches, with four inherited rule controls; avoids the16 earlier D3 novelty examples.',
 'decisions':24,'source_mechanism_groups':14,'inherited_decisions':4,'new_decisions':20,
 'exclusions':{'d3_review_sha256':sha(history_path),'already_inspected_ids':excluded,'overlap':0},
 'shards':bindings,'selection':metadata,'display_order_seed':seed,'display_order':[r['id'] for r in selected],
 'limits':'Purposive small rules-only sample; paired cases and shared teacher are dependent. Not a whole-dataset estimate or independent ground truth.'}
with (OUT/'selection.json').open('x') as stream:
 json.dump(selection,stream,indent=2);stream.write('\n')
# Freeze IDs before emitting any text for semantic judging.
with (OUT/'blind-inputs.jsonl').open('x') as stream:
 for row in selected:
  stream.write(json.dumps({k:row[k] for k in ('id','state','question','options')},ensure_ascii=False)+'\n')
with (OUT/'selected-reference.jsonl').open('x') as stream:
 for row in selected:
  stream.write(json.dumps(row,ensure_ascii=False)+'\n')
with (OUT/'observations.jsonl').open('a') as stream:
 stream.write(json.dumps({'at':datetime.now(timezone.utc).isoformat(),'event':'selection_frozen',
  'decisions':24,'groups':14,'previously_reviewed_overlap':0,'selection_sha256':sha(OUT/'selection.json'),
  'blind_inputs_sha256':sha(OUT/'blind-inputs.jsonl'),'note':'No targets used in selection; fresh reviewer has projection only.'})+'\n')
print(json.dumps({'selection_sha256':sha(OUT/'selection.json'),'blind_inputs_sha256':sha(OUT/'blind-inputs.jsonl'),'decisions':24,'groups':14,'ids':[r['id'] for r in selected]},indent=2))
