"""Dataset-only structural and rule audit; does not import generation code.
Reconstructs the semantic answer from structured facts without reading target_id
until after expected option text has been computed. No model or external data.
"""
import collections
import hashlib
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def expected(g,f):
    if g==1:
        eligible=[(f['order'].index(flag),destination) for flag,destination in f['routes'].items() if f['active'][flag]]
        return 'Route to '+(min(eligible)[1] if eligible else f['default'])+'.'
    if g==2:
        n=f['hours']; a=f['first_end']; b=f['second_end']; x,y,z=f['rates']
        total=min(n,a)*x+max(0,min(n,b)-a)*y+max(0,n-b)*z
        return f'Charge {total} credits.'
    if g==3:
        def admit(items,accepted):
            if not items: return [x[0] for x in accepted]
            item,*rest=items
            used=sum(x[1] for x in accepted)
            return admit(rest,accepted+[item] if used+item[1]<=f['capacity'] else accepted)
        names=admit(f['items'],[])
        return 'Load '+(', '.join(names) if names else 'nothing')+'.'
    if g==4:
        ring=collections.deque(f['cycle'])
        ring.rotate(-f['start'])
        for _ in range(abs(f['shift'])): ring.rotate(-1 if f['shift']>0 else 1)
        return 'Duty belongs to '+ring[0]+'.'
    if g==5:
        terms=[]
        for i,(w,n) in enumerate(zip(f['weights'],f['counts'])):
            terms.extend([(-w if i==2 else w)]*n)
        total=sum(terms)
        if total>=f['high']: label='Release batch'
        elif total>=f['low']: label='Hold batch for review'
        else: label='Reject batch'
        return label+'.'
    if g==6:
        names=sorted({x for x in f['east']+f['west'] if (x in f['east'])!=(x in f['west'])})
        return 'Issue '+(', '.join(names) if names else 'no badges')+'.'
    if g==7:
        proposed=set(range(f['request'][0]*60,f['request'][1]*60))
        hits=[]
        for name,(a,b) in zip(f['labels'],f['slots']):
            if proposed.intersection(range(a*60,b*60)): hits.append(name)
        return 'Conflicts: '+(', '.join(hits) if hits else 'none')+'.'
    if g==8:
        table=dict(f['rules']); message=f['message']
        result='Fallback'
        for size in range(len(message),0,-1):
            if message[:size] in table:
                result=table[message[:size]]; break
        return 'Send to '+result+'.'
    if g==9:
        residue=0
        for digit,weight in zip(f['digits'],f['weights']):
            for _ in range(weight):
                residue+=digit
                while residue>=f['modulus']: residue-=f['modulus']
        return f'Print seal value {residue}.'
    if g==10:
        # Explicit branching separately transcribed from the natural-language policy.
        state=f['initial']
        for event in f['events']:
            if state=='locked' and event=='badge': state='open'
            elif state=='open' and event=='enter': state='occupied'
            elif state=='open' and event=='close': state='locked'
            elif state=='occupied' and event=='exit': state='open'
        return 'Final state: '+state+'.'
    if g==11:
        nodes=f['nodes']; n=len(nodes)
        matrix=[[False]*n for _ in nodes]
        for a,b in f['edges']: matrix[nodes.index(a)][nodes.index(b)]=True
        for k in range(n):
            for a in range(n):
                for b in range(n): matrix[a][b]=matrix[a][b] or (matrix[a][k] and matrix[k][b])
        source=nodes.index(f['start'])
        result=sorted(nodes[i] for i in range(n) if matrix[source][i] and i!=source)
        return 'Water reaches '+(', '.join(result) if result else 'no other junctions')+'.'
    if g==12:
        names=f['names']; counts={(a,b):0 for a,b in itertools.permutations(names,2)}
        for multiplicity,ranking in f['ballots']:
            for i,a in enumerate(ranking):
                for b in ranking[i+1:]: counts[a,b]+=multiplicity
        undefeated=[a for a in names if all(counts[a,b]-counts[b,a]>0 for b in names if a!=b)]
        assert len(undefeated)<=1
        return 'Elect '+undefeated[0]+'.' if undefeated else 'Elect nobody under this rule.'
    raise ValueError(g)

def main():
    plan=json.loads((ROOT/'group_assignments.json').read_text())['groups']
    audit=[json.loads(line) for line in (ROOT/'audit_cases.jsonl').read_text().splitlines()]
    facts={x['id']:x for x in audit}
    assert len(facts)==len(audit)==120
    ids=set(); canonical=set(); group_counts=collections.Counter(); positions={}; outcomes={}; rows=[]
    for split,quota in [('train',100),('validation',20)]:
        shard=[json.loads(line) for line in (ROOT/f'{split}.jsonl').read_text().splitlines()]
        assert len(shard)==quota
        for r in shard:
            assert set(r)=={'schema_version','id','state','question','options','target_id','group_id','task_family','split','provenance'}
            assert r['schema_version']=='0.1' and r['task_family']=='rule_application'
            assert r['split']==split==plan[r['group_id']]['split']
            assert r['id'].startswith(r['group_id']+':') and r['id'] not in ids
            ids.add(r['id'])
            assert isinstance(r['state'],str) and r['state'].strip()
            assert isinstance(r['question'],str) and r['question'].strip()
            options=r['options']; assert 2<=len(options)<=6
            assert all(set(o)=={'id','text'} and isinstance(o['id'],str) and o['id'] and isinstance(o['text'],str) and o['text'].strip() for o in options)
            assert len({o['id'] for o in options})==len(options)
            assert len({o['text'] for o in options})==len(options)
            canonical_input=(r['state'],r['question'],tuple(sorted(o['text'] for o in options)))
            assert canonical_input not in canonical
            canonical.add(canonical_input)
            item=facts[r['id']]
            answer=expected(item['mechanism'],item['facts'])
            matching=[o for o in options if o['text']==answer]
            assert len(matching)==1, (r['id'],answer,options)
            assert matching[0]['id']==r['target_id'],(r['id'],answer)
            assert sum(o['id']==r['target_id'] for o in options)==1
            assert r['provenance']=={'kind':'programmatic','source':'data-pilot-v1/rule_application/original-rule-job-r1','label_basis':'rule_verified'}
            group_counts[r['group_id']]+=1
            key=f'{split}:{len(options)}_choices'
            positions.setdefault(key,collections.Counter())[str(next(i for i,o in enumerate(options) if o['id']==r['target_id']))]+=1
            outcomes.setdefault(r['group_id'],collections.Counter())[answer]+=1
        rows.extend(shard)
    assert set(ids)==set(facts)
    assert set(group_counts)==set(plan) and set(group_counts.values())=={10}
    assert {r['group_id'] for r in rows if r['split']=='train'}.isdisjoint({r['group_id'] for r in rows if r['split']=='validation'})
    report={
      'schema_version':'0.1','status':'passed','rows_checked':len(rows),'rule_verified_rows':120,
      'counts':{'train':100,'validation':20},'group_counts':dict(group_counts),
      'target_positions_zero_based_by_choice_count':{k:dict(v) for k,v in positions.items()},
      'outcome_counts':{k:dict(v) for k,v in outcomes.items()},
      'exact_input_duplicates':0,'cross_split_group_overlap':0,
      'checks':['JSONL parse; exact contract fields; schema/family/split; nonempty text; 2–6 distinct choices; opaque unique per-row option IDs; target membership; namespaced unique row IDs; frozen group allocation; 10 cases per group; exact canonical-input duplicate detection; independent rule recomputation on all 120 rows'],
      'audit_scope':'Independent algorithmic implementations, not an independent author or model. Facts and original natural-language semantics are teacher-created. Audit does not independently prove natural-language-to-fact fidelity.',
      'file_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['train.jsonl','validation.jsonl','group_assignments.json','audit_cases.jsonl','generate.py','audit.py']}
    }
    (ROOT/'validation_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'passed','rule_checked':120,'train':100,'validation':20,'target_positions':report['target_positions_zero_based_by_choice_count']}))

if __name__=='__main__': main()
