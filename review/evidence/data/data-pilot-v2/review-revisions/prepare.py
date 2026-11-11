import hashlib,json,os
from pathlib import Path
B=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2'); O=B/'review-revisions'
def save(n,x):
 p=O/n
 with p.open('x') as f: json.dump(x,f,indent=2); f.write('\n')
paths=[]
for d in ['intent-a','intent-a-r2','intent-b','intent-b-r2','sentiment-b','sentiment-b-r2']:
 paths += sorted(p for p in (B/d).rglob('*') if p.is_file())
paths += [B/'pre-review-r3/manifest.json']
save('sha-before.json',{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
save('environment.json',{k:os.environ.get(k) for k in ['PI_MODEL','PI_PROVIDER']})
blind=[]
for producer in ['intent-a-r2','intent-b-r2']:
 for split in ['train','validation']:
  rows=[json.loads(s) for s in (B/producer/(split+'.jsonl')).read_text().splitlines()]
  rows.sort(key=lambda r:r['id'])
  indices=[round(i*(len(rows)-1)/9) for i in range(10)]
  for i in indices:
   r=rows[i]
   blind.append({'id':r['id'],'state':r['state'],'question':r['question'],'options':r['options']})
save('blind-inputs.json',blind)
save('sampling.json',{'method':'Per producer, sort IDs within each split; select round(i*(n-1)/9), i=0..9. Exactly 10 train and 10 validation per producer. No label or metadata output; no parent/generator content inspected before freeze.','count':len(blind)})
for r in blind: print(json.dumps(r,ensure_ascii=False))
