"""Deterministic renderer and provisional programmatic labels. Run audit.py afterwards."""
import hashlib,json,os,random
from collections import defaultdict
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
P=Path(__file__).resolve().parent
SEED=731904
JOB='data-d3-seen-rules-v1-ordering-original-731904'
R=random.Random(SEED)
def money(v): return f'£{v:.2f}'
def allocation(batches,takes):
    return '; '.join(f'{b[0]} {takes.get(b[0],0)}' for b in sorted(batches))
def compute(c):
    p,f,m=c['policy'],c['facts'],c['mechanism_id']
    if m=='lexicographic':
        winner=min(f['candidates'],key=lambda x:tuple((-x[i+1] if d=='max' else x[i+1]) for i,(_,d) in enumerate(p['criteria'])))
        return winner[0],[x[0] for x in f['candidates'] if x!=winner]
    if m=='fifo':
        remaining=f['request']; take={}
        for n,_,q in sorted(f['batches'],key=lambda x:x[1]):
            take[n]=min(remaining,q);remaining-=take[n]
        good=allocation(f['batches'],take)
        # Other feasible issue patterns, not impossible or padded options.
        b=f['batches']; alternatives=set()
        for x in range(b[0][2]+1):
            for y in range(b[1][2]+1):
                z=f['request']-x-y
                if 0<=z<=b[2][2]:
                    s=allocation(b,{b[0][0]:x,b[1][0]:y,b[2][0]:z})
                    if s!=good: alternatives.add(s)
        distract=sorted(alternatives);R.shuffle(distract)
        return good,distract[:2]
    if m=='discount':
        v=Decimal(f['base'])
        for op,a in p['steps']:
            a=Decimal(a);v=v-a if op=='fixed' else v*(1-a/100)
        good=money(v)
        rev=Decimal(f['base'])
        for op,a in reversed(p['steps']):
            a=Decimal(a);rev=rev-a if op=='fixed' else rev*(1-a/100)
        # Include the reversed-order result and nearby erroneous invoice totals.
        alts=[]
        for a in [rev,v+Decimal('1.00'),v-Decimal('2.00'),v+Decimal('3.00')]:
            s=money(a)
            if s!=good and s not in alts: alts.append(s)
        return good,alts[:3]
    step=Decimal(p['step']);v=Decimal(f['value']);n=(v/step).quantize(Decimal('1'),rounding=ROUND_HALF_UP)
    fmt=lambda x:f'{x:.{p["places"]}f} {p["unit"]}'
    offsets=R.choice([[-1,1,2],[-2,-1,1]])
    return fmt(n*step),[fmt((n+d)*step) for d in offsets]
def render(c):
    p,f,m=c['policy'],c['facts'],c['mechanism_id']
    if m=='lexicographic':
        order=list(f['candidates']);R.shuffle(order);c['display_order']=[x[0] for x in order]
        rules='; then '.join(f'{k} {"highest" if d=="max" else "lowest"}' for k,d in p['criteria'])
        state=f'{p["context"]} Rank by {rules}. Compare a later field only when all earlier fields tie. Fields: {p["units"]}. '+ ' | '.join(x[0]+': '+', '.join(map(str,x[1:])) for x in order)+'.'
        return state,'Which candidate receives priority?'
    if m=='fifo':
        order=list(f['batches']);R.shuffle(order);c['display_order']=[x[0] for x in order]
        state=f'{p["context"]} {p["note"]} Issue {f["request"]} {p["unit"]} by FIFO: exhaust the smallest arrival number before using the next. Batches (arrival number, available {p["unit"]}): '+ ' | '.join(f'{n}: {a}, {q}' for n,a,q in order)+'.'
        return state,'How many units should be issued from each batch?'
    if m=='discount':
        steps='; then '.join('subtract £'+a if op=='fixed' else 'reduce the current subtotal by '+a+'%' for op,a in p['steps'])
        return f'{p["context"]} Starting charge: £{f["base"]}. In order: {steps}. {p["note"]} No tax or other charge applies. Keep exact arithmetic until the final amount in pounds and pence.','What is the final charge?'
    return f'{p["context"]} Measured value: {f["value"]} {p["unit"]}. Record the nearest multiple of {p["step"]} {p["unit"]}, using multiples anchored at zero. At an exact halfway point, choose the higher multiple.','What value should be recorded?'
def main():
    sources=[json.loads(s) for s in (P/'source_cases.jsonl').read_text().splitlines()]
    grouped=defaultdict(list)
    for c in sources: grouped[3 if c['mechanism_id']=='fifo' else 4].append(c['id'])
    slots={}
    for arity,ids in grouped.items():
        positions=[i%arity for i in range(len(ids))];R.shuffle(positions)
        slots.update(zip(ids,positions))
    rows=[];audit=[]
    for original in sources:
        c=json.loads(json.dumps(original));good,bad=compute(c);R.shuffle(bad)
        texts=list(bad);texts.insert(slots[c['id']],good)
        state,question=render(c)
        options=[{'id':f'o{i+1}','text':s} for i,s in enumerate(texts)]
        rows.append(dict(schema_version='0.1',id=c['id'],state=state,question=question,options=options,target_id=options[slots[c['id']]]['id'],group_id=c['group_id'],task_family='rule_application',split='validation',provenance=dict(kind='programmatic',source=JOB,label_basis='teacher',teacher_model={'provider':os.environ['PI_PROVIDER'],'model_alias':os.environ['PI_MODEL']},mechanism_id=c['mechanism_id'],policy_instance_id=c['group_id'],usage='validation_only_never_train')))
        audit.append(c)
    for name,data in [('validation.jsonl',rows),('audit_cases.jsonl',audit)]:
        (P/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in data))
    print('Generated',len(rows),'provisional rows; verification pending')
if __name__=='__main__': main()
