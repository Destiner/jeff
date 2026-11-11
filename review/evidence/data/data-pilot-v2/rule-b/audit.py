"""Pure second semantic implementation. No generator, targets, rendering or output imports."""
from fractions import Fraction

def expected(case):
    mechanism=case['group_number']; rules=case['policy']; data=case['facts']
    if mechanism==1:
        # Enumerate eligible days on an unbounded integer line, then index.
        eligible=[]
        first=0 if rules['inclusive'] else 1
        for distance in range(first,7*(data['steps']+2)):
            day=(data['start']+distance*rules['direction'])%7
            if day in rules['active']: eligible.append(day)
        return ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][eligible[data['steps']-1]]
    if mechanism==2:
        purchased=rules['minimum']
        while data['stock']+purchased*(rules['size']-rules['damaged']) < data['demand']+rules['reserve']:
            purchased+=1
        return str(purchased)
    if mechanism==3:
        exact=[Fraction(w*data['total'],sum(rules['weights'])) for w in rules['weights']]
        awarded=[int(x) for x in exact]
        remaining=data['total']-sum(awarded)
        if rules['mode']=='largest':
            priority=list(range(len(exact)))
            if rules['tie']=='reverse': priority.reverse()
            priority.sort(key=lambda j:exact[j]-awarded[j],reverse=True)
            for j in priority:
                if remaining==0: break
                awarded[j]+=1; remaining-=1
        elif rules['mode']=='first': awarded[0]+=remaining
        else: awarded[-1]+=remaining
        return '; '.join(name+' '+str(value) for name,value in zip(rules['names'],awarded))
    if mechanism==4:
        valid=[]
        for value in range(data['lo'],data['hi']+1):
            lower=value>=rules['lo'] if rules['lc'] else value>rules['lo']
            upper=value<=rules['hi'] if rules['hc'] else value<rules['hi']
            if lower and upper: valid.append(value)
        return f'{valid[0]} through {valid[-1]}' if valid else 'Empty'
    if mechanism==5:
        a=Fraction(data['a_num'],data['a_den']); b=Fraction(data['b_num'],data['b_den'])
        if a==b: return rules['tie']
        best=max(a,b) if rules['prefer']=='higher' else min(a,b)
        return 'Vendor A' if best==a else 'Vendor B'
    if mechanism==6:
        # Compose homogeneous matrices first, then apply to the original point.
        def multiply(a,b): return [[sum(a[i][k]*b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        matrix=[[1,0,0],[0,1,0],[0,0,1]]
        fixed={'ccw':[[0,-1,0],[1,0,0],[0,0,1]],'cw':[[0,1,0],[-1,0,0],[0,0,1]],
               'reflect_x':[[1,0,0],[0,-1,0],[0,0,1]],'reflect_y':[[-1,0,0],[0,1,0],[0,0,1]],
               'swap':[[0,1,0],[1,0,0],[0,0,1]]}
        for action in rules['ops']:
            if action[0]=='shift': step=[[1,0,action[1]],[0,1,action[2]],[0,0,1]]
            elif action[0]=='scale': step=[[action[1],0,0],[0,action[1],0],[0,0,1]]
            else: step=fixed[action[0]]
            matrix=multiply(step,matrix)
        point=data['point']+[1]
        out=[sum(a*b for a,b in zip(line,point)) for line in matrix]
        return f'({out[0]}, {out[1]})'
    if mechanism==7:
        # Explicitly realize batches, remove whole batches, then individual items.
        batches=[list(range(rules['gross'])) for _ in range(data['batches'])]
        batches=batches[rules['whole_loss']:]
        usable=[]
        for batch in batches:
            usable.extend(batch[rules['per_loss']+rules['retain']:])
        return str(max(0,len(usable)-rules['final_loss']))
    if mechanism==8:
        for candidate in sorted(data['candidates']):
            end=candidate+rules['duration']; legal=True
            for start_old,end_old in data['busy']:
                if candidate>=end_old:
                    distance=candidate-end_old
                    if distance<rules['gap'] or (rules['strict'] and distance==rules['gap']): legal=False
                elif end<=start_old:
                    if rules['both']:
                        distance=start_old-end
                        if distance<rules['gap'] or (rules['strict'] and distance==rules['gap']): legal=False
                else: legal=False
            if legal: return str(candidate)
        return 'No slot'
    if mechanism==9:
        def signature(symbols):
            normalized=[]
            for char in symbols:
                if char==rules['ignore']: continue
                normalized.append(char.casefold() if rules['fold'] else char)
            return sorted(normalized)
        hits=[label for label,symbols in rules['choices'].items() if signature(symbols)==signature(data['symbols'])]
        if len(hits)!=1: raise ValueError('Nonunique exact match')
        return hits[0]
    if mechanism==10:
        def visit(node):
            if type(node)==str: return node
            field,operator,cutoff,yes,no=node
            value=data[field]
            if operator=='<': result=value<cutoff
            elif operator=='<=': result=value<=cutoff
            elif operator=='>': result=value>cutoff
            elif operator=='>=': result=value>=cutoff
            elif operator=='==': result=value==cutoff
            elif operator=='!=': result=value!=cutoff
            else: raise ValueError(operator)
            return visit(yes) if result else visit(no)
        return visit(rules['tree'])
    if mechanism==11:
        # Add everything, correcting each immediately ascending pair by twice its first value.
        values=[rules['values'][char] for char in data['numeral']]
        result=sum(values)
        for small,big in zip(values,values[1:]):
            if small<big: result-=2*small
        return str(result)
    if mechanism==12:
        # Reverse recursive parsing of postfix is independent of a forward stack evaluator.
        tokens=data['tokens'][:]
        def read():
            token=tokens.pop()
            if token not in ('+','-','*','/'): return Fraction(token)
            right=read(); left=read()
            if token=='+': return left+right
            if token=='-': return left-right
            if token=='*': return left*right
            return left/right
        value=read()
        if tokens: raise ValueError('Trailing stack items')
        return str(value)
    if mechanism==13:
        # Enumerate all valid orders and choose the lexicographically best under tie priority.
        from itertools import permutations
        names=rules['nodes']
        priority=sorted(names) if rules['tie'].startswith('alphabetically') else names[:]
        if rules['tie'].endswith('last'): priority.reverse()
        valid=[]
        for order in permutations(names):
            if all(order.index(a)<order.index(b) for a,b in data['edges']): valid.append(order)
        chosen=min(valid,key=lambda order:tuple(priority.index(x) for x in order))
        return ' → '.join(chosen)
    if mechanism==14:
        names=list(rules['codebook'])
        if rules['tie'].startswith('alphabetically'): names.sort()
        if rules['tie'].endswith('last'): names.reverse()
        # XOR bit-count rather than character comparisons.
        received=int(data['received'],2)
        distances={n:bin(int(rules['codebook'][n],2)^received).count('1') for n in names}
        winner=min(names,key=lambda n:distances[n])
        return winner
    if mechanism==15:
        averages={}
        for start in range(len(data['values'])-rules['width']+1):
            averages[start]=sum(Fraction(data['values'][start+j],rules['width']) for j in range(rules['width']))
        indices=list(averages)
        if rules['tie']=='latest': indices.reverse()
        chosen=max(indices,key=lambda i:averages[i])
        return f'Positions {chosen+1}–{chosen+rules["width"]}'
    raise ValueError(mechanism)
