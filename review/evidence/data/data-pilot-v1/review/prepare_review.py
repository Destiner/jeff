"""Read-only published dataset selection; new review artifacts only."""
from pathlib import Path
import json, hashlib, collections
ROOT=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1')
OUT=ROOT/'review'
rows=[]
manifest=json.loads((ROOT/'manifest.json').read_text())
for e in manifest['shards']:
    p=ROOT/Path(e['path']).relative_to('data/data-pilot-v1')
    rows.extend(json.loads(x) for x in p.read_text().splitlines())
selected=[]
for family in ['intent','sentiment']:
    for split in ['train','validation']:
        pool=[r for r in rows if r['task_family']==family and r['split']==split]
        groups=sorted({r['group_id'] for r in pool})
        picks=[groups[round(i*(len(groups)-1)/5)] for i in range(6)]
        # Distinct scenarios, cycling through source row positions; no labels used.
        for i,g in enumerate(picks):
            candidates=sorted([r for r in pool if r['group_id']==g],key=lambda r:r['id'])
            selected.append(candidates[i%len(candidates)])
for g in sorted({r['group_id'] for r in rows if r['task_family']=='rule_application'}):
    candidates=sorted([r for r in rows if r['group_id']==g],key=lambda r:(len(r['state']),r['id']))
    selected.extend([candidates[0],candidates[-1]])
with (OUT/'selected_inputs.jsonl').open('x') as f:
    for r in selected:
        f.write(json.dumps({k:r[k] for k in ['schema_version','id','state','question','options']},ensure_ascii=False)+'\n')
with (OUT/'selection.json').open('x') as f:
    json.dump({'method':'intent/sentiment: six evenly spaced lexicographic groups per split; cyclic row positions 0,1,2,3,0,1. Rules: shortest and longest state per mechanism, ID tie break. Selection never uses target. Short/long is variation heuristic, not guaranteed boundary coverage.','ids':[r['id'] for r in selected]},f,indent=2)
print('Wrote 48 label-free inputs; target fields not printed.')
for i,r in enumerate(selected,1):
    print(f"\n{i}. {r['id']}\n{r['state']}\nQ: {r['question']}")
    print(' | '.join(f"{j}: {o['text']}" for j,o in enumerate(r['options'])))
