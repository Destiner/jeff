"""Original synthetic rules and cases, authored in existing agent session; no model calls.
Run from any cwd. All writes are restricted to this script's directory.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JOB = 'data-pilot-v1/rule_application/original-rule-job-r1'
PLAN = json.loads((ROOT / 'group_assignments.json').read_text())
ROWS, FACTS = [], []
POSITION_COUNTS = {}

def emit(g, j, state, question, correct, alternatives, facts):
    group = f'data:pilot-v1:rule_application:g{g:02d}'
    split = PLAN['groups'][group]['split']
    # Positions cycle globally within each group; IDs have no outcome meaning.
    choices = list(dict.fromkeys([correct] + alternatives))
    assert 2 <= len(choices) <= 6
    position_key = (split, len(choices))
    sequence = POSITION_COUNTS.get(position_key, 0)
    pos = sequence % len(choices)
    POSITION_COUNTS[position_key] = sequence + 1
    choices.remove(correct)
    choices.insert(pos, correct)
    rid = f'data:pilot-v1:rule_application:g{g:02d}:r{j+1:02d}'
    options = [{'id': hashlib.sha256(f'{rid}:{i}:opaque'.encode()).hexdigest()[:12], 'text': c}
               for i, c in enumerate(choices)]
    ROWS.append(dict(schema_version='0.1', id=rid, state=state, question=question,
                     options=options, target_id=options[pos]['id'], group_id=group,
                     task_family='rule_application', split=split,
                     provenance=dict(kind='programmatic', source=JOB, label_basis='rule_verified')))
    FACTS.append(dict(id=rid, mechanism=g, facts=facts))

# g01: Ordered routing: rule order varies, including priority inversions.
route_cases = [
(['safety','warranty','urgent'],True,True,True),
(['warranty','safety','urgent'],True,True,False),
(['urgent','safety','warranty'],True,False,True),
(['safety','urgent','warranty'],False,False,False),
(['warranty','urgent','safety'],False,True,True),
(['urgent','warranty','safety'],True,True,False),
(['safety','warranty','urgent'],False,False,True),
(['urgent','safety','warranty'],True,False,False),
(['warranty','safety','urgent'],False,False,False),
(['warranty','urgent','safety'],True,False,True)]
route_names = {'safety':'Safety bench', 'warranty':'Warranty bench', 'urgent':'Rapid bench'}
for j,(order,s,w,u) in enumerate(route_cases):
    active = dict(safety=s,warranty=w,urgent=u)
    result = next((route_names[k] for k in order if active[k]), 'General bench')
    rules = '; then '.join(f'if the {k} flag is on, use {route_names[k]}' for k in order)
    state = (f'Repair desk routing sheet {j+1}. Apply only the first matching rule: {rules}. '
             'If none matches, use General bench. Later matches never override an earlier match. '
             + 'Ticket flags: ' + ', '.join(f'{k}={"on" if v else "off"}' for k,v in active.items()) + '.')
    emit(1,j,state,'Which single bench receives this ticket?',f'Route to {result}.',
         [f'Route to {x}.' for x in list(route_names.values())+['General bench'] if x!=result],
         dict(order=order,active=active,routes=route_names,default='General bench'))

# g02: Marginal fees, not a single rate on the total; boundary and zero cases.
rental_cases = [(3,7,2,4,6,0),(3,7,2,4,6,3),(3,7,2,4,6,7),(3,7,2,4,6,8),
                (2,5,1,3,5,4),(4,6,3,5,8,9),(1,4,0,2,7,1),(2,8,4,4,9,8),
                (5,9,2,6,10,6),(2,3,3,7,11,5)]
for j,(a,b,r1,r2,r3,n) in enumerate(rental_cases):
    fee=sum(r1 if k<=a else r2 if k<=b else r3 for k in range(1,n+1))
    state=(f'A fictional rental counter bills whole hours marginally: hours 1 through {a} each cost {r1} credits; '
           f'hours {a+1} through {b} each cost {r2} credits; every later hour costs {r3} credits. '
           f'Add the charges for used hours only; there is no deposit, rounding, or minimum fee. This rental used {n} whole hours.')
    vals=[max(0,fee-2),fee+2,n*r3,n*r1,fee+5]
    emit(2,j,state,'What total charge follows this tariff?',f'Charge {fee} credits.',
         [f'Charge {v} credits.' for v in dict.fromkeys(vals) if v!=fee][:3],
         dict(first_end=a,second_end=b,rates=[r1,r2,r3],hours=n))

# g03: Sequential greedy allocation with skipped requests not ending the scan.
cargo_cases=[(7,[('Amber',5),('Birch',4),('Cedar',2)]),
(8,[('Dune',9),('Elm',3),('Flint',5)]),(5,[('Gale',6),('Haze',7),('Iris',8)]),
(9,[('Jade',2),('Kite',3),('Lime',4)]),(6,[('Moss',4),('Nook',3),('Opal',1)]),
(0,[('Pine',1),('Quay',2),('Reed',3)]),(10,[('Sage',6),('Tide',5),('Umber',4),('Vale',1)]),
(4,[('Wave',4),('Yarn',1),('Zinc',2)]),(11,[('Ash',3),('Bramble',8),('Cove',2)]),
(6,[('Dell',7),('Echo',2),('Fern',5),('Glow',4)])]
def load_text(names):
    return 'Load '+(', '.join(names) if names else 'nothing')+'.'
for j,(cap,items) in enumerate(cargo_cases):
    remaining=cap; chosen=[]
    for name,weight in items:
        if weight<=remaining:
            chosen.append(name); remaining-=weight
    allnames=[n for n,w in items]
    alternatives=[load_text(x) for x in [[],allnames,allnames[:1],allnames[-1:],allnames[1:]] if x!=chosen]
    state=(f'The cargo cart has capacity {cap} units. Inspect requests in this exact order: '+
           ', '.join(f'{n} ({w} units)' for n,w in items)+'. Load a request if its entire weight fits the remaining capacity; '
           'otherwise skip it and continue to later requests. Never unload an accepted request. All requests are indivisible.')
    emit(3,j,state,'Which requests end up on the cart, in inspection order?',load_text(chosen),list(dict.fromkeys(alternatives))[:3],dict(capacity=cap,items=items))

# g04: Signed movement around a cycle; index arithmetic with multiple wraps.
rota_cases=[(['Aster','Beryl','Cobalt'],0,0),(['Aster','Beryl','Cobalt'],2,1),
(['Dawn','Evening','Night','Noon'],0,-1),(['Dawn','Evening','Night','Noon'],3,6),
(['Elm','Fir','Gum','Holly','Ivy'],1,-7),(['Elm','Fir','Gum','Holly','Ivy'],4,10),
(['Juno','Kestrel','Lark'],1,-4),(['Maple','Nutmeg','Olive','Poppy'],2,9),
(['Quartz','Ruby','Slate','Topaz','Umber'],3,-10),(['Vega','Willow','Xenia'],0,5)]
for j,(cycle,start,shift) in enumerate(rota_cases):
    correct=cycle[(start+shift)%len(cycle)]
    state=(f'An observatory rotates duty in this repeating forward order: {" → ".join(cycle)} → back to {cycle[0]}. '
           f'The current duty is {cycle[start]}. Move {abs(shift)} slot(s) {"forward" if shift>=0 else "backward"}; '
           'one step changes to the adjacent slot, and zero steps leaves the duty unchanged. Wrap at either end as often as needed.')
    emit(4,j,state,'Who is on duty after the move?',f'Duty belongs to {correct}.',
         [f'Duty belongs to {x}.' for x in cycle if x!=correct],dict(cycle=cycle,start=start,shift=shift))

# g05: Additive signed scoring with changing weights, thresholds and inputs.
score_cases=[(2,3,1,0,0,1,3,7),(2,3,1,2,1,0,3,7),(2,3,1,2,2,1,3,7),
(4,1,2,1,0,2,0,4),(1,4,3,0,2,1,4,6),(3,2,2,3,0,0,2,8),
(2,5,4,1,0,2,-2,5),(1,2,1,1,1,1,5,9),(5,1,3,0,0,0,0,3),
(2,2,5,2,3,1,2,5)]
for j,(wa,wb,wc,a,b,c,lo,hi) in enumerate(score_cases):
    score=wa*a+wb*b-wc*c
    result='Reject batch' if score<lo else 'Hold batch for review' if score<hi else 'Release batch'
    state=(f'Seed grading uses score = {wa} × ripe samples + {wb} × dry samples − {wc} × damaged samples. '
           f'Count each listed category separately even if the same sample might qualify twice. '
           f'A score below {lo} means reject; a score from {lo} inclusive to {hi} exclusive means hold for review; '
           f'a score of {hi} or more means release. Batch counts: ripe {a}, dry {b}, damaged {c}.')
    emit(5,j,state,'What disposition does the score require?',result+'.',
         [x+'.' for x in ['Reject batch','Hold batch for review','Release batch'] if x!=result],
         dict(weights=[wa,wb,wc],counts=[a,b,c],low=lo,high=hi))

# g06: Symmetric difference; intersection members removed, not union.
set_cases=[(['amber','blue'],['blue','coral']),([],['dune','elm']),(['fern'],['fern']),
(['gold','hazel','iris'],['iris']),(['jade','khaki'],[]),(['lime','mauve'],['navy','ochre']),
(['pink','rose','silver'],['rose','silver','teal']),([],[]),
(['umber','violet','white'],['white','violet','umber']),(['yellow'],['yellow','zinc'])]
def set_text(vals):
    return 'Issue '+(', '.join(sorted(vals)) if vals else 'no badges')+'.'
for j,(a,b) in enumerate(set_cases):
    answer=sorted(set(a)^set(b)); universe=sorted(set(a)|set(b))
    distract=[set_text(set(a)&set(b)),set_text(universe),set_text(a),set_text(b),set_text(['reserve'])]
    state=(f'Exhibition desk reconciliation: issue exactly the badge names that occur on one of the two lists but not both. '
           'Treat the lists as sets; a badge on both is cancelled. Do not create names absent from the lists. '
           f'List East: {", ".join(a) or "empty"}. List West: {", ".join(b) or "empty"}.')
    emit(6,j,state,'Which badges should the desk issue?',set_text(answer),
         [x for x in dict.fromkeys(distract) if x!=set_text(answer)][:3],dict(east=a,west=b))

# g07: Half-open interval conflicts, endpoints touching are free.
interval_cases=[((9,11),[(7,9),(11,13)]),((9,12),[(8,10),(12,14)]),
((13,15),[(10,14),(14,17)]),((8,9),[(8,9),(10,11)]),((16,18),[(9,16),(17,19)]),
((10,13),[(9,12),(11,14),(12,13)]),((6,8),[(8,10),(10,12),(12,14)]),
((12,14),[(10,12),(12,13),(14,16)]),((15,17),[(14,16),(16,18),(19,20)]),
((7,10),[(6,7),(8,9),(9,10),(10,11)])]
for j,(request,slots) in enumerate(interval_cases):
    labels=[f'Booking {k+1}' for k in range(len(slots))]
    conflicts=[name for name,(s,e) in zip(labels,slots) if request[0]<e and s<request[1]]
    def fmt(x): return 'Conflicts: '+(', '.join(x) if x else 'none')+'.'
    choices=[[],labels,labels[:1],labels[-1:],labels[1:]]
    state=(f'Room times use a 24-hour clock on one day. Each booking includes its start and excludes its end. '
           'A conflict requires a positive duration of overlap; touching endpoints are not a conflict. '
           +'; '.join(f'{name}: {s:02d}:00–{e:02d}:00' for name,(s,e) in zip(labels,slots))+
           f'. Proposed booking: {request[0]:02d}:00–{request[1]:02d}:00.')
    emit(7,j,state,'Which existing bookings conflict with the proposal?',fmt(conflicts),
         list(dict.fromkeys(fmt(x) for x in choices if x!=conflicts))[:3],dict(request=request,slots=slots,labels=labels))

# g08: Prefix routing, exact character prefixes, not substring or first match.
prefix_cases=[([('a','Amber'),('ab','Birch'),('abc','Cedar')],'abcd'),
([('m','Moss'),('mn','Nook'),('mno','Opal')],'mx'),
([('s','Sage'),('st','Tide'),('sto','Umber')],'xsto'),
([('c','Cove'),('cat','Dell'),('ca','Echo')],'cat'),
([('r','Reed'),('ra','Ash'),('rab','Bramble')],'razz'),
([('p','Pine'),('pi','Quay'),('pin','Rock')],'pinwheel'),
([('v','Vale'),('va','Wave'),('val','Yarn')],'v'),
([('z','Zinc'),('ze','Elm'),('zen','Fern')],'zenith'),
([('l','Lime'),('lu','Gale'),('lux','Haze')],'lumen'),
([('k','Kite'),('ko','Iris'),('kor','Jade')],'okor')]
for j,(rules,message) in enumerate(prefix_cases):
    matches=[(p,r) for p,r in rules if message.startswith(p)]
    result=max(matches,key=lambda x:len(x[0]))[1] if matches else 'Fallback'
    state=('The message switchboard compares lowercase text exactly. A prefix must match from the first character. '
           'Use the destination attached to the longest matching prefix, regardless of listing order. If none matches, use Fallback. '
           +'Entries: '+ '; '.join(f'"{p}" → {r}' for p,r in rules)+f'. Message code: "{message}".')
    emit(8,j,state,'Which destination receives this message?',f'Send to {result}.',
         [f'Send to {x}.' for x in [r for p,r in rules]+['Fallback'] if x!=result],dict(rules=rules,message=message))

# g09: Explicit weighted modular checksum, ask the required digit, no external convention.
checksum_cases=[([1,2,3],[1,1,1],5),([0,0,0],[2,1,2],7),([9,1,4],[1,3,2],6),
([2,7,1,3],[1,2,1,2],4),([5,5],[3,1],5),([4,0,2],[2,3,4],7),
([8,3,6],[1,2,3],6),([1,9,0,2],[2,1,2,1],4),([3,3,3],[1,2,1],5),
([7,2],[2,3],7)]
for j,(digits,weights,mod) in enumerate(checksum_cases):
    total=sum(d*w for d,w in zip(digits,weights)); answer=total%mod
    state=(f'This parcel system defines its seal value as the remainder after dividing the weighted digit sum by {mod}. '
           f'Digits, left to right: {digits}. Corresponding weights, left to right: {weights}. '
           f'Multiply each digit by its corresponding weight, then add. The remainder is in 0 through {mod-1}; '
           'use that remainder directly, not its complement.')
    vals=[v for v in range(mod) if v!=answer]
    emit(9,j,state,'Which seal value must be printed?',f'Print seal value {answer}.',
         [f'Print seal value {v}.' for v in vals[:3]],dict(digits=digits,weights=weights,modulus=mod))

# g10: Explicit total transition systems; ignored events and repeated events matter.
fsm_cases=[('locked',['badge']),('locked',['badge','enter']),('open',['close','badge']),
('occupied',['badge','exit','close']),('locked',['enter','close']),
('open',['badge','enter','exit']),('occupied',['exit','enter']),
('locked',['badge','close','enter']),('open',['enter','exit','close','badge']),
('occupied',['close','exit','badge','enter'])]
transitions={'locked':{'badge':'open'},'open':{'enter':'occupied','close':'locked'},'occupied':{'exit':'open'}}
for j,(initial,events) in enumerate(fsm_cases):
    current=initial
    for event in events: current=transitions.get(current,{}).get(event,current)
    state=('Workshop controller states are locked, open, and occupied. In locked, badge changes the state to open. '
           'In open, enter changes it to occupied and close changes it to locked. In occupied, exit changes it to open. '
           'Every event not specified for the current state leaves that state unchanged. Process all events in order. '
           f'Initial state: {initial}. Event log: '+', '.join(events)+'.')
    emit(10,j,state,'What is the final controller state?',f'Final state: {current}.',
         [f'Final state: {x}.' for x in transitions if x!=current],dict(initial=initial,events=events,transitions=transitions))

# g11: Held-out graph reachability, not direct-neighbour lookup; cycles and empty sets.
graph_cases=[(['A','B','C','D'],[('A','B'),('B','C')],'A'),
(['E','F','G','H'],[('E','F'),('G','F'),('H','G')],'F'),
(['J','K','L','M'],[('J','K'),('K','J'),('K','L'),('L','M')],'K'),
(['N','P','Q','R'],[('P','N'),('P','Q'),('Q','R')],'N'),
(['S','T','U','V'],[('S','T'),('S','U'),('U','V')],'S'),
(['W','X','Y','Z'],[('W','X'),('X','Y'),('Y','W')],'X'),
(['A1','B1','C1','D1','E1'],[('A1','B1'),('C1','B1'),('C1','D1'),('D1','E1')],'C1'),
(['F1','G1','H1','J1'],[('G1','F1'),('H1','G1'),('J1','H1')],'J1'),
(['K1','L1','M1','N1'],[('K1','L1'),('L1','M1'),('N1','M1')],'L1'),
(['P1','Q1','R1','S1'],[('P1','P1'),('P1','Q1'),('R1','S1')],'P1')]
def graph_text(nodes):
    return 'Water reaches '+(', '.join(sorted(nodes)) if nodes else 'no other junctions')+'.'
for j,(nodes,edges,start) in enumerate(graph_cases):
    reached={start}; frontier=[start]
    while frontier:
        n=frontier.pop()
        for a,b in edges:
            if a==n and b not in reached: reached.add(b); frontier.append(b)
    answer=sorted(reached-{start})
    direct=sorted({b for a,b in edges if a==start}-{start})
    candidates=[[],sorted(set(nodes)-{start}),direct,sorted({a for a,b in edges if b==start}-{start}),[n for n in nodes if n!=start][:1]]
    alternatives=list(dict.fromkeys(graph_text(c) for c in candidates if c!=answer))[:3]
    state=('In this fictional irrigation network, every listed arrow is an open one-way pipe. Water may follow any number of arrows, '
           'branch into multiple pipes, and pass through cycles. Unlisted pipes do not exist. '
           f'Junctions: {", ".join(nodes)}. Pipes: '+', '.join(f'{a} → {b}' for a,b in edges)+
           f'. Water is introduced only at {start}. Exclude the starting junction from the reported set, even if a cycle leads back to it.')
    emit(11,j,state,'Which other junctions can water reach?',graph_text(answer),alternatives,dict(nodes=nodes,edges=edges,start=start))

# g12: Held-out pairwise majority, including cycles, equalities and weighted ballots.
election_cases=[
(['Ari','Bea','Cy'],[(3,[0,1,2]),(2,[1,2,0])]),
(['Dee','Eli','Fay'],[(2,[0,1,2]),(2,[1,2,0]),(2,[2,0,1])]),
(['Gus','Hal','Ida'],[(2,[0,1,2]),(2,[1,0,2])]),
(['Jen','Kai','Lou'],[(1,[0,1,2]),(4,[2,1,0]),(1,[1,0,2])]),
(['Mae','Nia','Oli'],[(3,[1,2,0]),(2,[0,1,2]),(1,[2,1,0])]),
(['Paz','Ren','Sol'],[(2,[0,2,1]),(4,[2,1,0]),(1,[1,0,2])]),
(['Tao','Una','Val'],[(1,[0,1,2]),(1,[1,2,0]),(1,[2,0,1])]),
(['Wes','Xiu','Yan'],[(3,[1,0,2]),(2,[2,1,0]),(2,[0,1,2])]),
(['Ada','Bo','Cal','Dom'],[(4,[3,0,2,1]),(3,[0,1,2,3]),(2,[2,3,1,0])]),
(['Em','Flo','Gil','Han'],[(2,[0,1,2,3]),(2,[1,2,3,0]),(2,[2,3,0,1]),(2,[3,0,1,2])])]
for j,(names,raw) in enumerate(election_cases):
    ballots=[(n,[names[k] for k in order]) for n,order in raw]
    winners=[]
    for candidate in names:
        if all(sum(n for n,order in ballots if order.index(candidate)<order.index(other))>
               sum(n for n,order in ballots if order.index(other)<order.index(candidate)) for other in names if other!=candidate):
            winners.append(candidate)
    result=f'Elect {winners[0]}.' if winners else 'Elect nobody under this rule.'
    state=('The club elects a candidate only if that candidate beats every other candidate in a separate head-to-head comparison. '
           'In each comparison, every voter supports whichever of the two appears earlier in their ranking. '
           'Beating requires strictly more votes; a tie is not a win. If nobody beats every rival, elect nobody. '
           'There is no elimination round or tie-break. Candidates: '+', '.join(names)+'. Ballot blocks: '+
           '; '.join(f'{n} voters rank '+ ' > '.join(order) for n,order in ballots)+'. Every ranking lists all candidates, best first.')
    emit(12,j,state,'Who, if anyone, is elected by this rule?',result,
         [x for x in [f'Elect {name}.' for name in names]+['Elect nobody under this rule.'] if x!=result],dict(names=names,ballots=ballots))

assert len(ROWS)==120
for split in ('train','validation'):
    path=ROOT/f'{split}.jsonl'
    path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in ROWS if r['split']==split))
(ROOT/'audit_cases.jsonl').write_text(''.join(json.dumps(f,ensure_ascii=False)+'\n' for f in FACTS))
print(json.dumps({'generation_job':JOB,'train':sum(r['split']=='train' for r in ROWS),'validation':sum(r['split']=='validation' for r in ROWS)}))
