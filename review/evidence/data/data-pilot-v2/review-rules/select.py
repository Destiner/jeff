import json, hashlib, os
from pathlib import Path
from collections import defaultdict
ROOT=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2')
OUT=ROOT/'review-rules'
files=[ROOT/'pre-review-r2'/'manifest.json']+[p for name in ['rule-a','rule-b'] for p in (ROOT/name).rglob('*') if p.is_file()]
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(OUT/'hashes-before.json').write_text(json.dumps(hashes,indent=2)+'\n')
groups=defaultdict(list); targets={}
for name in ['rule-a','rule-b']:
 for split in ['train','validation']:
  for line in (ROOT/name/(split+'.jsonl')).read_text().splitlines():
   r=json.loads(line); groups[r['group_id']].append(r); targets[r['id']]=r['target_id']
selected=[]
for i,(group,rows) in enumerate(sorted(groups.items())):
 rows=sorted(rows,key=lambda r:(len(r['state']),hashlib.sha256(r['id'].encode()).hexdigest()))
 # Short and long states, rotate within extreme quartiles to vary policy/boundary cases without consulting labels.
 for r in [rows[i%max(1,len(rows)//4)],rows[-1-i%max(1,len(rows)//4)]]:
  selected.append({k:r[k] for k in ['id','state','question','options']})
(OUT/'blind-sample.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in selected))
(OUT/'targets-sealed.json').write_text(json.dumps(targets,indent=2)+'\n')
(OUT/'exposure.json').write_text(json.dumps({'PI_MODEL':os.getenv('PI_MODEL'),'PI_PROVIDER':os.getenv('PI_PROVIDER'),'previous_exposure':'No prior session context or source/target exposure. Before selection saw manifest, first-row IDs/group/provenance and file names only; labels parsed by selection script but never displayed. No generators/audit code read before decisions.','selection':'Two per mechanism group: rotated shortest/longest quartiles, deterministic length/hash sort; no target-based outcome selection.'},indent=2)+'\n')
print('groups',len(groups),'sample',len(selected))
