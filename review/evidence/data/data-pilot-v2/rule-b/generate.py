"""Deterministic rendering, target computation and position-balanced candidate assembly."""
import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SEED=761903
DAYS=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
def interval(a,b): return 'Empty' if a>b else f'{a} through {b}'
def coord(v): return f'({v[0]}, {v[1]})'
def allocation(v,names): return '; '.join(f'{k} {x}' for k,x in zip(names,v))
def transformed(point,ops):
    x,y=point
    for op in ops:
        if op[0]=='shift': x,y=x+op[1],y+op[2]
        elif op[0]=='ccw': x,y=-y,x
        elif op[0]=='cw': x,y=y,-x
        elif op[0]=='reflect_x': y=-y
        elif op[0]=='reflect_y': x=-x
        elif op[0]=='swap': x,y=y,x
        elif op[0]=='scale': x,y=x*op[1],y*op[1]
    return [x,y]
def solve(c):
    g,p,f=c['group_number'],c['policy'],c['facts']
    if g==1:
        d=f['start']; left=f['steps']
        if p['inclusive'] and d in p['active']: left-=1
        while left:
            d=(d+p['direction'])%7
            if d in p['active']: left-=1
        return DAYS[d]
    if g==2:
        need=max(0,f['demand']+p['reserve']-f['stock']); usable=p['size']-p['damaged']
        return str(max(p['minimum'],(need+usable-1)//usable))
    if g==3:
        w=p['weights']; total=f['total']; denom=sum(w)
        shares=[total*x//denom for x in w]; left=total-sum(shares)
        if p['mode']=='largest':
            order=sorted(range(len(w)),key=lambda i:(-(total*w[i]%denom),i if p['tie']=='forward' else -i))
            for i in order[:left]: shares[i]+=1
        else: shares[0 if p['mode']=='first' else -1]+=left
        return allocation(shares,p['names'])
    if g==4: return interval(max(f['lo'],p['lo']+(not p['lc'])),min(f['hi'],p['hi']-(not p['hc'])))
    if g==5:
        delta=f['a_num']*f['b_den']-f['b_num']*f['a_den']
        if delta==0: return p['tie']
        return 'Vendor A' if (delta>0)==(p['prefer']=='higher') else 'Vendor B'
    if g==6: return coord(transformed(f['point'],p['ops']))
    if g==7:
        return str(max(0,max(0,f['batches']-p['whole_loss'])*(p['gross']-p['per_loss']-p['retain'])-p['final_loss']))
    if g==8:
        def valid(s):
            for a,b in f['busy']:
                after=s-b>p['gap'] if p['strict'] else s-b>=p['gap']
                gap_before=a-(s+p['duration'])
                before=(gap_before>p['gap'] if p['strict'] else gap_before>=p['gap']) if p['both'] else gap_before>=0
                if not (after or before): return False
            return True
        choices=[s for s in f['candidates'] if valid(s)]
        return str(min(choices)) if choices else 'No slot'
    if g==9:
        def norm(s):
            s=s.replace(p['ignore'],'')
            return Counter(s.lower() if p['fold'] else s)
        return next(k for k,v in p['choices'].items() if norm(v)==norm(f['symbols']))
    if g==10:
        t=p['tree']
        while isinstance(t,list):
            var,op,num,a,b=t; value=f[var]
            yes={'<':value<num,'<=':value<=num,'>':value>num,'>=':value>=num,'==':value==num,'!=':value!=num}[op]
            t=a if yes else b
        return t
    if g==11:
        nums=[p['values'][s] for s in f['numeral']]
        return str(sum(-v if i+1<len(nums) and v<nums[i+1] else v for i,v in enumerate(nums)))
    if g==12:
        stack=[]
        for t in f['tokens']:
            if t in ['+','-','*','/']:
                b=stack.pop(); a=stack.pop()
                stack.append({'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a/b}[t]())
            else: stack.append(Fraction(t))
        return str(stack[0])
    if g==13:
        remaining=list(p['nodes']); result=[]
        while remaining:
            ready=[x for x in remaining if not any(b==x and a in remaining for a,b in f['edges'])]
            if p['tie'].startswith('alphabetically'): ready.sort()
            chosen=ready[-1] if p['tie'].endswith('last') else ready[0]
            result.append(chosen); remaining.remove(chosen)
        return ' → '.join(result)
    if g==14:
        book=p['codebook']; dist={k:sum(a!=b for a,b in zip(v,f['received'])) for k,v in book.items()}
        tied=[k for k,v in dist.items() if v==min(dist.values())]
        if p['tie'].startswith('alphabetically'): tied.sort()
        return tied[-1] if p['tie'].endswith('last') else tied[0]
    if g==15:
        vals=f['values']; k=p['width']; sums=[sum(vals[i:i+k]) for i in range(len(vals)-k+1)]
        tied=[i for i,v in enumerate(sums) if v==max(sums)]
        i=tied[0] if p['tie']=='earliest' else tied[-1]
        return f'Positions {i+1}–{i+k}'
    raise ValueError(g)
def tree_text(t):
    if isinstance(t,str): return t
    var,op,n,a,b=t
    return f'if {var} {op} {n} then ({tree_text(a)}) else ({tree_text(b)})'
def leaves(t): return [t] if isinstance(t,str) else leaves(t[3])+leaves(t[4])
def render(c):
    g,p,f=c['group_number'],c['policy'],c['facts']; ctx=c['context']
    if g==1:
        active=', '.join(DAYS[i] for i in p['active'])
        text=f'Active weekdays: {active}. Count {"forward" if p["direction"]==1 else "backward"} cyclically. {"Count the start as day 1 if active; otherwise start with the next active day in that direction." if p["inclusive"] else "Do not count the start; day 1 is the next active day in that direction."} Start {DAYS[f["start"]]}; count {f["steps"]} active days.'
        return ctx+': '+text,'Which weekday is reached?'
    if g==2:
        return (f'{ctx}: Each pack has {p["size"]} units, of which {p["damaged"]} are unusable. Demand is {f["demand"]}; keep {p["reserve"]} extra usable units. Already hold {f["stock"]} usable units. Buy whole packs only, at least {p["minimum"]} packs even if stock suffices.', 'What is the fewest packs to buy?')
    if g==3:
        weights=', '.join(f'{n}:{w}' for n,w in zip(p['names'],p['weights']))
        if p['mode']=='largest':
            remainder=f'Award remaining units one each by descending fractional remainder; ties favor {"earlier" if p["tie"]=="forward" else "later"} names in the listed order.'
        else: remainder=f'Give every leftover unit to the {p["mode"]} listed recipient.'
        return f'{ctx}: Split {f["total"]} indivisible units in weight ratio {weights}. First floor each exact proportional share. {remainder}','What is the final allocation?'
    if g==4:
        return (f'{ctx}: Only integer settings are valid. Allowed values are {">=" if p["lc"] else ">"} {p["lo"]} and {"<=" if p["hc"] else "<"} {p["hi"]}. Requested values are {f["lo"]} through {f["hi"]}, inclusive. Keep only values satisfying both ranges; report Empty if none.', 'What interval remains?')
    if g==5:
        return (f'{ctx}: Compare {p["unit"]}; {p["prefer"]} is preferred. Vendor A reports {f["a_num"]} over {f["a_den"]}; Vendor B reports {f["b_num"]} over {f["b_den"]}, in those units. Compare exact ratios without rounding. If equal, return {p["tie"]}.', 'Which result follows?')
    if g==6:
        descriptions=[]
        for op in p['ops']:
            if op[0]=='shift': desc=f'add ({op[1]}, {op[2]})'
            elif op[0]=='scale': desc=f'multiply both coordinates by {op[1]}'
            else: desc={'ccw':'replace (x,y) with (-y,x)','cw':'replace (x,y) with (y,-x)','reflect_x':'replace (x,y) with (x,-y)','reflect_y':'replace (x,y) with (-x,y)','swap':'replace (x,y) with (y,x)'}[op[0]]
            descriptions.append(desc)
        return f'{ctx}: Start at {coord(f["point"])}. Apply in this exact order: '+ '; then '.join(descriptions)+'. Each step uses the current coordinates.','What is the final coordinate?'
    if g==7:
        return (f'{ctx}: Start with {f["batches"]} batches of {p["gross"]} items each. First discard {p["whole_loss"]} whole batches (all if fewer). In each remaining batch, discard {p["per_loss"]} defective items and reserve {p["retain"]} other items. Then remove {p["final_loss"]} items from the combined output. Clamp output at zero.', 'How many items remain available?')
    if g==8:
        busy=', '.join(f'{a}–{b}' for a,b in f['busy'])
        gap=f'{"more than" if p["strict"] else "at least"} {p["gap"]} minutes'
        rule=f'Require {gap} after any earlier appointment ends.'
        if p['both']: rule+=f' Also require {gap} before any later appointment starts.'
        else: rule+=' No cooldown before later appointments.'
        return (f'{ctx}: Times are minute indices. Existing intervals: {busy}. New duration: {p["duration"]}. Overlap is forbidden; touching endpoints is not overlap. {rule} Candidate starts: {", ".join(map(str,f["candidates"]))}.', 'Which is the earliest legal listed start, or No slot?')
    if g==9:
        kits='; '.join(f'{k}="{v}"' for k,v in p['choices'].items())
        return (f'{ctx}: Match symbol multiplicities exactly; order is irrelevant. Ignore every {json.dumps(p["ignore"])} character. {"Treat uppercase and lowercase as identical." if p["fold"] else "Uppercase and lowercase are distinct."} Available kits: {kits}. Received string: "{f["symbols"]}".', 'Which kit matches exactly?')
    if g==10:
        vals=', '.join(f'{k}={v}' for k,v in f.items())
        return f'{ctx}: Evaluate this nested policy: {tree_text(p["tree"])}. Here {vals}. Only the selected branch applies.','Which output is selected?'
    if g==11:
        table=', '.join(f'{k}={v}' for k,v in p['values'].items())
        return (f'{ctx}: Symbol values: {table}. Scan left to right. Subtract a symbol if its value is less than the immediately following symbol; otherwise add it. Always add the last symbol. Parse {f["numeral"]}.', 'What value is obtained?')
    if g==12:
        return (f'{ctx}: Execute postfix tokens on an initially empty stack. A number pushes its value. An operator pops right operand b, then left operand a, and pushes a operator b. Division is exact rational division, not truncation. Tokens: {" ".join(f["tokens"])}.', 'What final stack value remains?')
    if g==13:
        edges=', '.join(f'{a} before {b}' for a,b in f['edges'])
        return (f'{ctx}: Tasks in listed order: {", ".join(p["nodes"])}. Constraints: {edges}. Repeatedly choose a task whose predecessors are already emitted, breaking ready-task ties by {p["tie"]}. Emit every task once.', 'What sequence is emitted?')
    if g==14:
        book='; '.join(f'{k}={v}' for k,v in p['codebook'].items())
        return (f'{ctx}: Codebook in listed order: {book}. Received bits: {f["received"]}. Hamming distance counts differing positions. Choose minimum distance; ties choose {p["tie"]}.', 'Which codeword label is selected?')
    if g==15:
        return (f'{ctx}: Readings in order: {", ".join(map(str,f["values"]))}. Consider every consecutive window of exactly {p["width"]} readings. Select the greatest arithmetic mean; tied means choose the {p["tie"]} start. Positions are numbered from 1.', 'Which window is selected?')

def candidates(c,target,rng):
    g,p,f=c['group_number'],c['policy'],c['facts']; pool=[]
    n=3 if c['policy_number']%2 else 4
    if g==1: pool=DAYS[:]
    elif g in (2,7,11,12):
        v=Fraction(target)
        pool=[str(v+d) for d in [-3,-2,-1,1,2,3]]
        if g!=12: pool=[x for x in pool if Fraction(x)>=0]
        if g==11: pool.extend([str(sum(p['values'][x] for x in f['numeral'])),str(abs(v-10)),str(v+10)])
    elif g==3:
        base=[int(t.rsplit(' ',1)[1]) for t in target.split('; ')]
        for i,j in itertools.permutations(range(3),2):
            if base[j]>0:
                v=base[:]; v[i]+=1; v[j]-=1; pool.append(allocation(v,p['names']))
        pool.append(allocation([f['total'],0,0],p['names']))
    elif g==4:
        a=max(f['lo'],p['lo']+(not p['lc'])); b=min(f['hi'],p['hi']-(not p['hc']))
        pool=['Empty', interval(f['lo'],f['hi']),interval(p['lo'],p['hi'])]
        if a<=b: pool.extend([interval(a-1,b),interval(a,b+1),interval(a+1,b),interval(a,b-1)])
        pool.extend([interval(p['lo'],p['lo']),interval(p['hi'],p['hi'])])
    elif g==5: pool=['Vendor A','Vendor B','Tie']; n=3
    elif g==6:
        x,y=transformed(f['point'],p['ops'])
        pool=[coord(f['point']),coord(transformed(f['point'],p['ops'][::-1])),coord([-x,y]),coord([x,-y]),coord([y,x]),coord([x+1,y]),coord([x,y-1])]
    elif g==8: pool=[str(v) for v in f['candidates']]+['No slot']; n=4
    elif g==9: pool=list(p['choices']); n=3
    elif g==10: pool=leaves(p['tree']); n=3
    elif g==13: pool=[' → '.join(t) for t in itertools.permutations(p['nodes'])]; n=4
    elif g==14: pool=list(p['codebook']); n=4
    elif g==15:
        pool=[f'Positions {i+1}–{i+p["width"]}' for i in range(len(f['values'])-p['width']+1)]
        n=min(n,len(pool))
    unique=list(dict.fromkeys(x for x in pool if x!=target)); rng.shuffle(unique)
    if len(unique)<n-1: raise ValueError(('insufficient distractors',c,n,unique))
    return unique[:n-1],n

def main():
    rng=random.Random(SEED)
    cases=[json.loads(s) for s in (ROOT/'authoring_cases.jsonl').read_text().splitlines()]
    assignments=json.loads((ROOT/'group_assignments.json').read_text())['groups']
    prepared=[]
    audit=[]
    for c in cases:
        group=f'data:pilot-v2:rule-b:g{c["group_number"]:03}'
        rownum=(c['policy_number']-1)*2+c['case_number']
        rid=group+f':r{rownum:02}'
        sid=group+f':p{c["policy_number"]:02}'
        answer=solve(c); state,q=render(c); wrong,n=candidates(c,answer,rng)
        prepared.append((c,group,rid,sid,answer,state,q,wrong,n,assignments[group]['split']))
        audit.append({'id':rid,'scenario_id':sid,'group_number':c['group_number'],'policy':c['policy'],'facts':c['facts']})
    # Assign positions independently of semantics after grouping by split and option count.
    buckets=defaultdict(list)
    for i,entry in enumerate(prepared): buckets[(entry[-1],entry[-2])].append(i)
    positions={}
    for (split,n),indices in sorted(buckets.items()):
        balanced=[i%n for i in range(len(indices))]; rng.shuffle(balanced)
        for index,pos in zip(indices,balanced): positions[index]=pos
    outputs=defaultdict(list)
    for index,(c,g,rid,sid,answer,state,q,wrong,n,split) in enumerate(prepared):
        rng.shuffle(wrong); texts=wrong[:]; texts.insert(positions[index],answer)
        option_ids=['o'+hashlib.sha256((rid+'|'+str(i)).encode()).hexdigest()[:12] for i in range(n)]
        row={'schema_version':'0.1','id':rid,'state':state,'question':q,
             'options':[{'id':k,'text':v} for k,v in zip(option_ids,texts)],
             'target_id':option_ids[positions[index]],'group_id':g,'task_family':'rule_application','split':split,
             'provenance':{'kind':'programmatic','source':'data-pilot-v2-rule-b-r1:original-policies-r1',
                           'label_basis':'rule_verified','scenario_id':sid,
                           'teacher_model':'openai/gpt-sol'}}
        outputs[split].append(row)
    # No rows are emitted as rule_verified unless the separate semantic implementation agrees.
    import audit as independent
    checked=0
    for split,rows in outputs.items():
        for row in rows:
            c=next(c for c in audit if c['id']==row['id'])
            expected=independent.expected(c)
            supplied=next(o['text'] for o in row['options'] if o['id']==row['target_id'])
            if expected!=supplied: raise ValueError(('audit mismatch',row['id'],expected,supplied))
            checked+=1
    for split,rows in outputs.items():
        (ROOT/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    (ROOT/'audit_cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in audit))
    print(f'Emitted {checked} audited rows; position buckets '+str({str(k):len(v) for k,v in buckets.items()}))
if __name__=='__main__': main()
