"""Join already-frozen judgments to the selected existing training labels."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
judgment_path = ROOT / 'blind-review/judgments.json'
judgments = json.loads(judgment_path.read_text())['judgments']
rows = {r['id']:r for r in map(json.loads,(ROOT/'selected-reference.jsonl').read_text().splitlines())}
selection = json.loads((ROOT/'selection.json').read_text())
assert {r['id'] for r in judgments} == set(rows) and len(judgments) == 24
comparisons = []
for judgment in judgments:
 row = rows[judgment['id']]
 options = {o['id']:o['text'] for o in row['options']}
 comparisons.append({'id':row['id'],'group_id':row['group_id'],
  'chosen_option_id':judgment['chosen_option_id'],'target_id':row['target_id'],
  'agrees':judgment['chosen_option_id']==row['target_id'],
  'chosen_text_matches':options.get(judgment['chosen_option_id'])==judgment['chosen_option_text']})
assert all(c['chosen_text_matches'] for c in comparisons)
result = {'task':'D4','compared_at':datetime.now(timezone.utc).isoformat(),
 'selection_sha256':sha(ROOT/'selection.json'),'judgments_sha256':sha(judgment_path),
 'reference_sha256':sha(ROOT/'selected-reference.jsonl'),
 'decisions':24,'source_groups':len({r['group_id'] for r in rows.values()}),
 'agreement':sum(c['agrees'] for c in comparisons),'by_group':{},'comparisons':comparisons,
 'limits':'Target-hidden same-model-alias agreement on a purposive TRAIN slice. Not independent ground truth, not model performance, not a whole-dataset rate.'}
for group in sorted({r['group_id'] for r in rows.values()}):
 subset=[c for c in comparisons if c['group_id']==group]
 result['by_group'][group]={'decisions':len(subset),'agreement':sum(c['agrees'] for c in subset)}
with (ROOT/'target-comparison.json').open('x') as stream:
 json.dump(result,stream,indent=2);stream.write('\n')
with (ROOT/'observations.jsonl').open('a') as stream:
 stream.write(json.dumps({'at':result['compared_at'],'event':'audit_join_complete','decisions':24,
  'groups':result['source_groups'],'agreement':result['agreement'],'subagents_completed':3,
  'findings':'No target/spec bug in sample; unreachable options in4rows/2groups; paired policy degeneracy and local cues recorded. No correction or Data code change warranted.',
  'peer_report':'E4/E5 aggregate-only message received/ack/completed; all consumer predictions valid per Evaluation; no private evidence opened.'})+'\n')
print(json.dumps({'decisions':24,'groups':result['source_groups'],'agreement':result['agreement'],'judgments_sha256':result['judgments_sha256']}))
