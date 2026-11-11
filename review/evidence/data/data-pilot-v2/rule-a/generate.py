"""Deterministic rendering and candidate assembly; no network or ML dependencies."""
import hashlib
import itertools
import json
import random
from collections import Counter
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SEED=813502
JOB='data-pilot-v2-rule-a-r1'
D=lambda x: Decimal(str(x))

def num(x):
    return format(D(x).normalize(),'f')

def encode(runs,p):
    f=p['fmt']
    return p['sep'].join((s+str(n) if f=='sc' else str(n)+s if f=='cs' else f'{s}:{n}' if f=='colon' else f'{s}({n})') for s,n in runs)

def runs_of(s):
    return [(k,len(list(v))) for k,v in itertools.groupby(s)]

def fifo_text(v):
    return ', '.join(map(str,v[:-1]))+f'; unfilled {v[-1]}'

def reference(g,p,f):
    if g==1:
        n=len(set(f['signed']) & set(p['eligible']))
        return ['Reject: too few eligible signers','Authorize','Reject: too many eligible signers'][(n>p['required'])+ (n>=p['required'])]
    if g==2:
        return 'Select candidate '+min(f['candidates'],key=lambda c:tuple(v*d for v,d in zip(c[1],p['directions'])))[0]
    if g==3:
        left=f['demand']; result=[]
        for name,qty in p['batches']:
            take=0 if name in p['skip'] else min(left,qty)
            result.append(take);left-=take
        return fifo_text(result+[left])
    if g==4:
        x=D(f['value'])*D(p['first'][0])+D(p['first'][1])
        return num(x*D(p['second'][0])+D(p['second'][1]))+' '+p['unit']
    if g==5:
        x=D(f['price']); fixed=D(p['fixed']) if x>=D(p['threshold']) else D(0); factor=1-D(p['percent'])/100
        out=max(0,x-fixed)*factor if p['order']=='fixed_first' else max(0,x*factor-fixed)
        return '£'+num(out)
    if g==6:
        out=sum(min(x*p['rate'],p['cap']) for x in f['days'] if p['eligible'] is None or x>=p['eligible'])
        if p['ceiling'] is not None: out=min(out,p['ceiling'])
        return str(out)+' credits'
    if g==7:
        step=D(p['step']); q=(D(f['value'])/step+D('.5')).to_integral_value(rounding=ROUND_FLOOR)
        return num(q*step)+' '+p['unit']
    if g==8:
        return encode(runs_of(f['stream']),p)
    if g==9:
        now=p['start']
        for name,t,deadline in sorted(f['jobs'],key=lambda j:j[2]):
            now+=t+p['setup']
            if now>deadline:return 'Infeasible: '+name+' first misses'
        return 'Feasible: all jobs meet deadlines'
    if g==10:
        allowed=set().union(*(set(p['grants'][r]) for r in f['roles']))
        if set(f['request']) & set(f['vetoes']): return 'Deny: requested permission vetoed'
        if not set(f['request'])<=allowed:return 'Deny: requested permission ungranted'
        return 'Allow the full request'
    if g==11:
        common={f['a'][i:j] for i in range(len(f['a'])) for j in range(i+1,len(f['a'])+1) if f['a'][i:j] in f['b']}
        longest=[s for s in common if len(s)==max(map(len,common))]
        return (min if p['tie']=='asc' else max)(longest)
    if g==12:
        stack=[];pairs={')':'(',']':'[','}':'{'}
        for c in f['sequence']:
            if c in '([{':stack.append(c)
            elif c in pairs:
                if not stack:return 'Invalid: closing with no opener'
                if stack.pop()!=pairs[c]:return 'Invalid: wrong closing type'
        return 'Invalid: unclosed opener' if stack else 'Valid: balanced and properly nested'
    if g==13:
        combined=[(key,0 if p['tie_left'] else 1,i,name) for i,(name,key) in enumerate(f['left'])]+[(key,1 if p['tie_left'] else 0,i,name) for i,(name,key) in enumerate(f['right'])]
        return ' '.join(x[3] for x in sorted(combined))
    if g==14:
        fail=[str(i) for i,(positions,parity) in enumerate(p['constraints'],1) if sum(int(f['vector'][x-1]) for x in positions)%2!=parity]
        return 'Fail constraints '+', '.join(fail) if fail else 'Pass all constraints'
    if g==15:
        ordered=sorted(f['candidates'],key=lambda c:c[0],reverse=p['tie']=='desc')
        def med(c):
            a=sorted(c[1]);return (D(a[(len(a)-1)//2])+D(a[len(a)//2]))/2
        return 'Select candidate '+max(ordered,key=med)[0]
    raise ValueError(g)

QUESTIONS={1:'What is the authorization outcome?',2:'Which candidate wins?',3:'What quantities are issued in batch order?',4:'What is the converted result?',5:'What is the final price?',6:'How many credits accrue?',7:'What rounded value is reported?',8:'What is the encoded stream?',9:'Which scheduling outcome applies?',10:'Which access decision applies?',11:'Which substring is selected?',12:'How is the sequence classified?',13:'What is the merged label order?',14:'Which parity constraints fail?',15:'Which candidate is selected?'}

def choices(g,p,f,target):
    if g==1:return ['Authorize','Reject: too few eligible signers','Reject: too many eligible signers']
    if g in (2,15):return ['Select candidate '+c[0] for c in f['candidates']]
    if g==3:
        q=f['demand']; capacities=[v for _,v in p['batches']]
        vectors=[]
        # Realistic wrong orders: LIFO, smallest batch first, ignore quarantine.
        for indices,respect in [(range(2,-1,-1),True),(sorted(range(3),key=lambda i:capacities[i]),True),(range(3),False)]:
            rem=q;v=[0,0,0]
            for i in indices:
                k=0 if respect and p['batches'][i][0] in p['skip'] else min(rem,capacities[i]);v[i]=k;rem-=k
            vectors.append(fifo_text(v+[rem]))
        # Alternative partial allocations remain arithmetically conservative.
        for i in range(3):
            v=[0,0,0];v[i]=min(q,capacities[i]);vectors.append(fifo_text(v+[q-v[i]]))
        for i in range(3):
            v=[0,0,0];v[i]=max(0,min(q,capacities[i])-1);vectors.append(fifo_text(v+[q-v[i]]))
        return unique_candidates(target,vectors,4)
    if g in (4,5,6,7):
        if g==4:
            val=D(target.split(' ')[0]);unit=' '+p['unit'];prefix='';delta=max(D(1),abs(val)/4)
            wrong=[D(f['value'])*D(p['first'][0])+D(p['first'][1]),D(f['value'])*D(p['second'][0])+D(p['second'][1])]
        elif g==5:
            val=D(target[1:]);unit='';prefix='£';delta=D(2)
            x=D(f['price']);fixed=D(p['fixed']) if x>=p['threshold'] else D(0);factor=1-D(p['percent'])/100
            wrong=[max(0,x*factor-fixed) if p['order']=='fixed_first' else max(0,x-fixed)*factor,x*factor,max(0,x-fixed)]
        elif g==6:
            val=D(target.split()[0]);unit=' credits';prefix='';delta=D(2)
            wrong=[D(sum(f['days'])*p['rate']),D(min(sum(f['days'])*p['rate'],p['cap'])),D(sum(min(x*p['rate'],p['cap']) for x in f['days']))]
        else:
            val=D(target.split()[0]);unit=' '+p['unit'];prefix='';delta=D(p['step']);wrong=[val-delta,val+delta,val-2*delta,val+2*delta]
        wrong += [val+delta,val+2*delta,val-delta,val+3*delta,val+4*delta]
        return unique_candidates(target,[prefix+num(x)+unit for x in wrong if g==7 or x>=0],4)
    if g==8:
        stream=f['stream'];runs=runs_of(stream)
        bad=[encode(list(Counter(stream).items()),p),encode(list(reversed(runs)),p),encode([(s,1) for s,_ in runs],p),encode([(s,n+1) for s,n in runs],p),encode(runs[:-1],p)]
        return unique_candidates(target,bad,4)
    if g==9:return ['Feasible: all jobs meet deadlines']+['Infeasible: '+j[0]+' first misses' for j in f['jobs']]
    if g==10:return ['Allow the full request','Deny: requested permission vetoed','Deny: requested permission ungranted']
    if g==11:
        a,b=f['a'],f['b']
        wrong=[a,b,target[:-1],target[1:],target[::-1]]+[a[i:i+2] for i in range(len(a)-1)]+list(dict.fromkeys(a))
        return unique_candidates(target,[s for s in wrong if s],4)
    if g==12:return ['Valid: balanced and properly nested','Invalid: wrong closing type','Invalid: closing with no opener','Invalid: unclosed opener']
    if g==13:
        a=[x[0] for x in f['left']];b=[x[0] for x in f['right']];out=target.split()
        bad=[' '.join(a+b),' '.join(b+a),' '.join(out[::-1]),' '.join(out[1:]+out[:1])]
        # Opposite stable tie priority is a consequential distractor.
        tagged=[(key,1 if p['tie_left'] else 0,i,name) for i,(name,key) in enumerate(f['left'])]+[(key,0 if p['tie_left'] else 1,i,name) for i,(name,key) in enumerate(f['right'])]
        bad.insert(0,' '.join(v[3] for v in sorted(tagged)))
        return unique_candidates(target,bad,4)
    if g==14:
        subsets=['Fail constraints '+', '.join(str(i+1) for i in range(len(p['constraints'])) if mask&(1<<i)) for mask in range(1,2**len(p['constraints']))]
        return unique_candidates(target,['Pass all constraints']+subsets,4)
    raise ValueError(g)

def unique_candidates(target,wrong,n):
    out=[target]
    for x in wrong:
        if x not in out:out.append(x)
        if len(out)==n:return out
    raise ValueError(('Not enough options',target,out))

def main():
    assignments=json.loads((ROOT/'group_assignments.json').read_text())['groups']
    policies=[json.loads(s) for s in (ROOT/'source_cases.jsonl').read_text().splitlines()]
    rows=[];audits=[];indices=Counter()
    for s in policies:
        g=s['group'];group=f'data:pilot-v2:rule-a:g{g:03}';split=assignments[group]['split'];p=s['policy']
        for case in s['cases']:
            indices[group]+=1;rid=group+f':r{indices[group]:02}';f=case['facts'];target=reference(g,p,f)
            opts=choices(g,p,f,target)
            state=s['title']+'. '+s['rule']+' '+case['text']
            rows.append(dict(schema_version='0.1',id=rid,state=state,question=QUESTIONS[g],options=opts,_target=target,group_id=group,task_family='rule_application',split=split,
                provenance=dict(kind='teacher',source=JOB+':source_cases-r1',label_basis='teacher',teacher_model='openai/gpt-sol',scenario_id=s['scenario_id'])))
            audits.append(dict(id=rid,scenario_id=s['scenario_id'],mechanism=assignments[group]['mechanism'],mechanism_number=g,policy=p,facts=f))
    rng=random.Random(SEED)
    # A separately shuffled target-slot multiset for each split/option-count stratum.
    for split,n in sorted({(r['split'],len(r['options'])) for r in rows}):
        subset=[r for r in rows if r['split']==split and len(r['options'])==n]
        slots=[i%n for i in range(len(subset))];rng.shuffle(slots)
        for r,pos in zip(subset,slots):
            answer=r.pop('_target');wrong=[x for x in r['options'] if x!=answer];rng.shuffle(wrong);wrong.insert(pos,answer)
            options=[dict(id=hashlib.sha256((r['id']+':'+str(i)+':option').encode()).hexdigest()[:14],text=x) for i,x in enumerate(wrong)]
            r['options']=options;r['target_id']=options[pos]['id']
    for split in ['train','validation']:
        (ROOT/(split+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows if r['split']==split))
    (ROOT/'audit_cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False,sort_keys=True)+'\n' for c in audits))
    print('Generated',dict(Counter(r['split'] for r in rows)))

if __name__=='__main__':main()
