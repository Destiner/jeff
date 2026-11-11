"""Compare only label-free probabilities under the pre-outcome tolerance."""
from pathlib import Path
import hashlib
import json
import math

root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((root/'comparison-freeze.json').read_text())
manifest=json.loads((root/'control-inputs.json').read_text())
reports=[]
for entry in manifest['datasets']:
    old=Path(freeze['p3_control_outputs'][entry['name']]['path'])
    if sha(old)!=freeze['p3_control_outputs'][entry['name']]['sha256']:
        raise ValueError('P3 frozen output changed')
    new=root/'starting'/f"{entry['name']}.jsonl"
    inputs=[json.loads(l) for l in Path(entry['path']).read_text().splitlines()]
    a=[json.loads(l) for l in old.read_text().splitlines()]
    b=[json.loads(l) for l in new.read_text().splitlines()]
    if len(a)!=len(b) or len(b)!=entry['rows']:raise ValueError('Control row coverage mismatch')
    max_delta=0.0;choices=0;ties=0
    for row, first, second in zip(inputs,a,b):
        if row['id']!=first['id'] or row['id']!=second['id']:raise ValueError('Control ID mismatch')
        expected={o['id'] for o in row['options']}
        p={o['option_id']:o['probability'] for o in first['probabilities']}
        q={o['option_id']:o['probability'] for o in second['probabilities']}
        if set(p)!=expected or set(q)!=expected or len(second['probabilities'])!=len(expected):
            raise ValueError('Control option coverage mismatch')
        if not all(math.isfinite(x) and 0<=x<=1 for x in q.values()) or abs(sum(q.values())-1)>1e-6:
            raise ValueError('Invalid starting probabilities')
        max_delta=max(max_delta,max(abs(p[k]-q[k]) for k in p))
        old_top={k for k in p if p[k]==max(p.values())}; new_top={k for k in q if q[k]==max(q.values())}
        choices+=old_top!=new_top;ties+=(len(old_top)>1)!=(len(new_top)>1)
    reports.append({'suite':entry['name'],'rows':len(b),'old_sha256':sha(old),'new_sha256':sha(new),
                    'byte_identical':old.read_bytes()==new.read_bytes(),'max_absolute_delta':max_delta,
                    'changed_top_sets':choices,'changed_tie_presence':ties,
                    'passes':max_delta<=freeze['tolerance_absolute_probability'] and choices==0 and ties==0})
report={'schema_version':'m6.start-comparison.v1','freeze_sha256':sha(root/'comparison-freeze.json'),
        'suites':reports,'passes':all(r['passes'] for r in reports),
        'qualification':'Numerical probability equivalence only; semantic/config/assets bound separately; no labels/scoring.'}
with (root/'starting-comparison.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(report,indent=2))
if not report['passes']:raise SystemExit('Control mismatch: stop before full training')
