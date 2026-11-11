"""Original authored policy instances. CPU-only; writes only beside this script."""
import json
import random
from pathlib import Path
ROOT = Path(__file__).resolve().parent
policies = []

def add(g, title, rule, pairs, **policy):
    n = 1 + sum(p['group'] == g for p in policies)
    assert len(pairs) == 2
    policies.append(dict(group=g, scenario_id=f'data:pilot-v2:rule-a:g{g:03}:p{n:02}', title=title,
                         rule=rule, policy=policy, cases=[dict(text=t, facts=f) for t,f in pairs]))

# Exact-count authorization: membership is explicit; repeated names count once.
def auth(title, eligible, count, pairs):
    add(1,title,f'Authorize only when exactly {count} distinct eligible signers signed. Eligible signers: {", ".join(eligible)}. Ignore other signers and repeated signatures.',
        [(f'Signatures received: {", ".join(s)}.',dict(signed=s)) for s in pairs],eligible=eligible,required=count)
auth('Museum loan release',['curator','registrar','conservator'],2,[['curator','registrar'],['curator','registrar','conservator']])
auth('Bakery night-key issue',['owner','baker','supervisor'],1,[['baker','baker','courier'],['courier','visitor']])
auth('Field survey departure',['lead','navigator','medic','driver'],3,[['lead','navigator'],['lead','navigator','medic','visitor']])
auth('Archive destruction order',['records officer','legal officer'],2,[['records officer','legal officer','legal officer'],['records officer','intern']])
auth('Radio transmission release',['editor','producer','engineer'],1,[['editor','producer'],['engineer','announcer']])
auth('Apartment reserve withdrawal',['chair','treasurer','secretary','auditor'],3,[['chair','treasurer','secretary'],['chair','treasurer','secretary','auditor']])
auth('Workshop chemical delivery',['chemist','safety officer','stores lead'],2,[['chemist','chemist','porter'],['chemist','safety officer','porter']])
auth('Theatre prop disposal',['designer','stage manager','director'],1,[['visitor'],['designer','stage manager']])
auth('School excursion release',['head','deputy','trip lead','governor'],2,[['head','trip lead','visitor'],['head','deputy','trip lead']])
auth('Reservoir inspection entry',['inspector','engineer','warden','operator'],3,[['inspector','engineer','warden','warden'],['inspector','engineer','visitor']])

# Ranking policies explicitly specify all tie-breaks.
def rank(title, fields, directions, candidates):
    words=[f'{name} ({"smaller" if direction==1 else "larger"} wins)' for name,direction in zip(fields,directions)]
    add(2,title,'Choose by '+', then '.join(words)+'. Compare later fields only on ties. Each tuple follows that field order.',
        [('Candidates: '+ '; '.join(f'{name}={tuple(vals)}' for name,vals in group)+'.',dict(candidates=group)) for group in candidates],directions=directions)
rank('Emergency print queue',['urgency','minutes','ticket'],[-1,1,1],[[['A',[3,12,7]],['B',[2,4,1]],['C',[3,8,9]]],[['A',[4,6,8]],['B',[4,6,3]],['C',[4,9,1]]]])
rank('Orchard delivery assignment',['distance','capacity','van number'],[1,-1,1],[[['Oak',[8,20,4]],['Elm',[8,24,8]],['Ash',[9,30,1]]],[['Oak',[7,18,6]],['Elm',[7,18,2]],['Ash',[8,40,1]]]])
rank('Translation job allocation',['quality','load','bid'],[-1,1,1],[[['R',[9,4,70]],['S',[9,2,90]],['T',[8,1,20]]],[['R',[8,3,55]],['S',[8,3,45]],['T',[8,4,35]]]])
rank('Warehouse forklift dispatch',['aisle distance','battery','machine ID'],[1,-1,1],[[['F',[2,40,3]],['G',[2,60,9]],['H',[3,90,1]]],[['F',[1,55,8]],['G',[1,55,4]],['H',[2,80,2]]]])
rank('Poster award',['jury points','public points','entry number'],[-1,-1,1],[[['Blue',[8,30,4]],['Red',[9,5,7]],['Gold',[8,50,1]]],[['Blue',[9,20,8]],['Red',[9,25,6]],['Gold',[9,25,3]]]])
rank('Courier bid selection',['price','arrival hour','rating'],[1,1,-1],[[['North',[40,12,4]],['South',[40,11,3]],['West',[45,9,5]]],[['North',[38,10,3]],['South',[38,10,5]],['West',[39,8,5]]]])
rank('Instrument calibration queue',['overdue days','error','serial'],[-1,-1,1],[[['K',[3,6,2]],['L',[4,1,7]],['M',[3,9,1]]],[['K',[5,2,8]],['L',[5,3,9]],['M',[5,3,4]]]])
rank('Volunteer shift choice',['unfilled shifts','travel minutes','signup order'],[-1,1,1],[[['Iris',[4,20,2]],['Noor',[4,15,8]],['Pia',[3,5,1]]],[['Iris',[2,10,6]],['Noor',[2,10,3]],['Pia',[2,12,1]]]])
rank('Roof repair tender',['warranty years','cost','finish day'],[-1,1,1],[[['X',[5,800,9]],['Y',[6,950,12]],['Z',[5,700,6]]],[['X',[7,900,8]],['Y',[7,900,6]],['Z',[7,950,3]]]])
rank('Document retrieval station',['wait','accuracy','station number'],[1,-1,1],[[['Desk A',[6,99,2]],['Desk B',[5,95,9]],['Desk C',[6,100,1]]],[['Desk A',[4,98,7]],['Desk B',[4,98,3]],['Desk C',[4,97,1]]]])

# FIFO records use receipt order, not expiry or batch name.
def fifo(title, batches, demands, skip=None):
    skip=skip or []
    text='Issue units from the earliest received usable batch first; exhaust it before the next. '+('Quarantined batches are unusable. ' if skip else '')+'Report quantities taken from each batch in listed order, then unfilled demand.'
    desc='; '.join(f'{b} {q} units'+(' quarantined' if b in skip else '') for b,q in batches)
    add(3,title,text,[(f'Receipt order: {desc}. Demand: {d} units.',dict(demand=d)) for d in demands],batches=batches,skip=skip)
fifo('Clinic bandage issue',[['B7',4],['A2',6],['C5',3]],[4,7])
fifo('Cafe carton issue',[['Q',3],['R',5],['S',4]],[2,9])
fifo('Lab vial issue',[['D',6],['E',2],['F',5]],[7,14])
fifo('Print room paper issue',[['P',5],['M',7],['N',2]],[5,12],['P'])
fifo('Hotel soap issue',[['L',2],['J',8],['K',3]],[10,11])
fifo('Repair depot fuse issue',[['T',7],['V',4],['U',6]],[8,18],['V'])
fifo('Farm feed sack issue',[['H',3],['G',3],['I',7]],[6,8])
fifo('School chalk issue',[['Z',8],['X',4],['Y',5]],[3,13])
fifo('Florist ribbon issue',[['R3',4],['R1',5],['R2',6]],[4,10],['R1'])
fifo('Catering tray issue',[['W',6],['U',9],['V',2]],[15,19])

# Two stated conversion stages, including offsets in calibration contexts.
def conversion(title, rule, unit, first, second, values, input_unit='raw units'):
    add(4,title,rule+f' Report the result in {unit}.',[(f'Input: {v} {input_unit}.',dict(value=v)) for v in values],first=first,second=second,unit=unit)
# Each stage is multiply then add; this representation is not rendered as metadata.
conversion('Paint decanting','One crate holds 6 tins; each tin holds 750 millilitres. Convert crates to tins, then to millilitres.','millilitres',[6,0],[750,0],[2,3],input_unit='crates')
conversion('Survey tape calibration','Convert marks to metres by multiplying by 4. Convert metres to centimetres by multiplying by 100.','centimetres',[4,0],[100,0],[3,7],input_unit='marks')
conversion('Audio archive timing','One reel is 9 minutes. One minute is 60 seconds. Convert reels to minutes, then seconds.','seconds',[9,0],[60,0],[2,5],input_unit='reels')
conversion('Ceramics glaze mass','A scoop holds 125 grams. Convert scoops to grams, then divide grams by 1000 to obtain kilograms.','kilograms',[125,0],[0.001,0],[4,12],input_unit='scoops')
conversion('Conveyor sensor calibration','Multiply the raw reading by 3 and add 2 to obtain centimetres. Multiply centimetres by 10 to obtain millimetres.','millimetres',[3,2],[10,0],[4,9])
conversion('Water meter correction','Add 5 to the reading to obtain litres. Divide litres by 4 to obtain jug equivalents.','jug equivalents',[1,5],[0.25,0],[7,15])
conversion('Textile roll planning','One bolt contains 8 metres. Each metre yields 5 strips. Convert bolts to metres, then strips.','strips',[8,0],[5,0],[3,6],input_unit='bolts')
conversion('Thermal display calibration','Double the raw value and subtract 6 to get degrees A. Add 10 to degrees A to get degrees B.','degrees B',[2,-6],[1,10],[8,13])
conversion('Stone sample weighing','One block weighs 2.5 kilograms. Multiply kilograms by 1000 to obtain grams.','grams',[2.5,0],[1000,0],[3,8],input_unit='blocks')
conversion('Tank gauge translation','Divide the raw reading by 2 to obtain litres. Subtract 3 litres of unusable reserve, then multiply the remainder by 4 for cup units.','cup units',[0.5,0],[4,-12],[14,22])

# Fixed and percentage discounts: explicit ordering, caps, and floors.
def discount(title, fixed, percent, order, prices, threshold=0):
    fixed_rule=f'a fixed £{fixed} reduction'+(f' only if the original price is at least £{threshold}' if threshold else '')
    steps=(fixed_rule+f', then {percent}% off the remainder') if order=='fixed_first' else (f'{percent}% off the original price, then '+fixed_rule)
    add(5,title,'Apply '+steps+'. A reduction cannot make the price negative. No other charges or rounding apply.',
        [(f'Original price: £{p}.',dict(price=p)) for p in prices],fixed=fixed,percent=percent,order=order,threshold=threshold)
discount('Stationery voucher',10,20,'fixed_first',[50,60])
discount('Cinema concession',6,25,'percent_first',[24,40])
discount('Shoe outlet promotion',15,10,'fixed_first',[100,150],100)
discount('Laundry account offer',8,50,'percent_first',[12,24])
discount('Picture frame coupon',12,25,'fixed_first',[8,44])
discount('Lunch counter offer',5,20,'percent_first',[20,25],25)
discount('Curtain fabric sale',20,30,'fixed_first',[80,120])
discount('Bike light promotion',9,10,'percent_first',[30,50])
discount('Art supply club offer',4,50,'fixed_first',[10,18],15)
discount('Piano lesson credit',15,20,'percent_first',[50,75],60)

# Daily caps are applied before adding, with explicit exclusions/aggregate ceiling.
def accrual(title, rate, cap, days, eligible=None, ceiling=None):
    rule=f'Each eligible day earns {rate} credits per recorded unit, capped at {cap} credits that day. Add daily earnings.'
    if eligible is not None: rule+=f' Only days with at least {eligible} units are eligible.'
    else: rule+=' All listed days are eligible.'
    if ceiling is not None: rule+=f' Cap the final total at {ceiling} credits.'
    add(6,title,rule,[(f'Daily units, in order: {", ".join(map(str,d))}.',dict(days=d)) for d in days],rate=rate,cap=cap,eligible=eligible,ceiling=ceiling)
accrual('Reading challenge',2,10,[[4,5,6],[1,0,9]])
accrual('Recycling reward',3,12,[[3,4,5],[1,2,8]],eligible=2)
accrual('Staff walking credit',1,8,[[8,9,2],[7,7,7]],ceiling=20)
accrual('Practice diary',4,16,[[1,3,5],[2,4,6]],eligible=3)
accrual('Tree care points',5,20,[[4,6,2],[3,3,3]],ceiling=40)
accrual('Packaging return reward',2,6,[[2,3,5],[1,1,4]],eligible=2,ceiling=15)
accrual('Volunteer minute tokens',1,15,[[10,15,20],[16,16,2]])
accrual('Music rehearsal credits',3,9,[[0,2,4],[3,3,1]],ceiling=18)
accrual('Cycling commute points',4,12,[[1,2,3],[4,1,4]],eligible=2)
accrual('Water saving challenge',2,14,[[7,8,3],[5,5,5]],eligible=3,ceiling=30)

# Explicit half-up rounding; positive and negative values use ties toward +infinity.
def rounding(title, step, unit, values):
    add(7,title,f'Round to the nearest multiple of {step} {unit}. At an exact halfway tie choose the numerically larger multiple, including for negative inputs.',
        [(f'Measured value: {v} {unit}.',dict(value=v)) for v in values],step=step,unit=unit)
rounding('Parcel mass reporting',0.5,'kilograms',[2.25,2.24])
rounding('Delivery duration board',5,'minutes',[12.5,12.4])
rounding('Laboratory temperature log',1,'degrees',[-2.5,-2.6])
rounding('Timber length labels',10,'millimetres',[145,144])
rounding('Photographic exposure scale',0.2,'units',[1.1,1.09])
rounding('Market price display',0.1,'pounds',[3.25,3.24])
rounding('Lift level calibration',2,'units',[-3,-3.1])
rounding('Fuel delivery invoice',25,'litres',[62.5,62.4])
rounding('Pottery diameter tag',0.25,'centimetres',[4.125,4.12])
rounding('Competition distance board',100,'metres',[250,249])

# Codecs include symbol/count ordering and separators; streams are authored.
def rle(title, fmt, sep, streams):
    forms={'sc':'symbol followed by its count','cs':'count followed by its symbol','colon':'symbol, a colon, then count','bracket':'symbol followed by count in parentheses'}
    delimiter='no separator' if not sep else repr(sep)+' between encoded runs'
    add(8,title,f'Encode maximal adjacent runs, not total symbol frequencies. Write each run as {forms[fmt]}; use {delimiter}. Include count 1. Spaces shown around the stream are not part of it.',
        [(f'Stream: {s}.',dict(stream=s)) for s in streams],fmt=fmt,sep=sep)
rle('Badge ribbon logger','sc',' ',['AAABBAC','ABBAAA'])
rle('Camera trigger log','cs','-', ['XXYXXX','YXXYYX'])
rle('Packing lane event code','colon','|',['PPQQP','QPQQQ'])
rle('Textile stripe register','bracket',',',['RRRGR','GRRGG'])
rle('Heartbeat marker archive','sc','',['LLHLL','HLLHHH'])
rle('Access turnstile signal','cs',' ',['EEEXE','XEXXX'])
rle('Rain gauge pulse record','colon',',',['WWDWW','DDWWD'])
rle('Boarding light sequence','bracket',' ',['GGAAG','AGGAAA'])
rle('Tile inspection tape','sc','/',['MMNNNM','NMNN'])
rle('Assembly buzzer recording','cs','|',['TTSTT','SSTSSS'])

# EDF, no idle, no preemption, completion equality allowed, optional setup each job.
def edf(title, start, setup, a, b):
    rule=f'One worker starts at minute {start}. Process jobs without idle time in earliest-deadline order; ties use listed order. Each job takes its duration'+(f' plus {setup} minutes setup' if setup else '')+'. Completion at the deadline is allowed. All jobs must meet their deadlines.'
    add(9,title,rule,[(f'Jobs (duration, deadline): '+ '; '.join(f'{name}=({d}, {end})' for name,d,end in jobs)+'.',dict(jobs=jobs)) for jobs in [a,b]],start=start,setup=setup)
edf('Print finishing shift',0,0,[['A',3,3],['B',2,5],['C',4,10]],[['A',3,3],['B',3,5],['C',4,10]])
edf('Bakery oven queue',5,1,[['Loaf',4,10],['Roll',3,14],['Bun',2,17]],[['Loaf',4,10],['Roll',3,13],['Bun',2,17]])
edf('Microfilm digitisation',0,0,[['X',4,9],['Y',2,2],['Z',3,6]],[['X',5,9],['Y',2,2],['Z',3,6]])
edf('Costume pressing schedule',2,0,[['Cape',3,6],['Coat',4,9],['Vest',1,12]],[['Cape',4,6],['Coat',4,9],['Vest',1,12]])
edf('Machine inspection round',0,2,[['M',2,4],['N',1,7],['P',3,12]],[['M',2,4],['N',2,7],['P',3,12]])
edf('Translation desk deadlines',10,0,[['Memo',2,12],['Note',1,12],['Brief',3,17]],[['Memo',1,12],['Note',1,12],['Brief',3,17]])
edf('Photo lab jobs',0,1,[['Red',2,7],['Blue',1,2],['Gold',2,8]],[['Red',2,7],['Blue',1,2],['Gold',3,8]])
edf('Equipment cleaning queue',3,0,[['Saw',2,5],['Drill',4,9],['Sander',3,12]],[['Saw',2,5],['Drill',5,9],['Sander',3,12]])
edf('Parcel sealing station',0,1,[['Box',3,4],['Tube',2,7],['Bag',1,9]],[['Box',3,4],['Tube',2,7],['Bag',2,9]])
edf('Gallery label production',4,0,[['Room A',2,10],['Room B',3,7],['Room C',1,10]],[['Room A',3,10],['Room B',4,7],['Room C',1,10]])

# Union grants, any requested permission under veto rejects the entire request.
def permission(title, grants, vetoes, pairs):
    grants_text='; '.join(f'{r} grants {", ".join(ps)}' for r,ps in grants.items())
    rule='Combine all assigned role grants. '+grants_text+'. Any active veto overrides grants. Allow only if every requested permission is granted and none is vetoed.'
    add(10,title,rule,[(f'Roles: {", ".join(roles)}. Active vetoes: {", ".join(v) if v else "none"}. Request: {", ".join(req)}.',dict(roles=roles,vetoes=v,request=req)) for roles,v,req in pairs],grants=grants)
permission('Archive access',{'reader':['view'],'editor':['view','annotate'],'custodian':['export']},[],[(['reader','custodian'],[],['view','export']),(['editor','custodian'],['export'],['export'])])
permission('Warehouse console',{'picker':['locate','pick'],'dispatcher':['ship'],'auditor':['locate','audit']},[],[(['picker'],[],['ship']),(['picker','dispatcher'],[],['pick','ship'])])
permission('Broadcast desk',{'host':['speak'],'engineer':['record','transmit'],'producer':['schedule']},[],[(['host','engineer'],['transmit'],['speak','transmit']),(['engineer','producer'],[],['record','schedule'])])
permission('School resource portal',{'student':['read'],'tutor':['read','comment'],'clerk':['enrol']},[],[(['student','clerk'],[],['comment']),(['tutor'],['comment'],['read'])])
permission('Garden irrigation control',{'viewer':['inspect'],'gardener':['water'],'manager':['water','configure']},[],[(['viewer','gardener'],[],['inspect','water']),(['manager'],['configure'],['configure'])])
permission('Ticketing terminal',{'seller':['sell'],'supervisor':['refund'],'planner':['allocate']},[],[(['seller','planner'],[],['refund']),(['seller','supervisor'],[],['sell','refund'])])
permission('Audio production folder',{'listener':['play'],'mixer':['play','edit'],'publisher':['release']},[],[(['mixer','publisher'],['edit'],['release']),(['mixer','publisher'],['release'],['edit','release'])])
permission('Maintenance work board',{'technician':['inspect','repair'],'coordinator':['assign'],'reviewer':['close']},[],[(['technician','coordinator'],[],['repair','assign']),(['coordinator','reviewer'],[],['inspect','close'])])
permission('Donation ledger',{'recorder':['enter'],'reviewer':['view','approve'],'treasurer':['pay']},[],[(['reviewer','treasurer'],['approve'],['approve','pay']),(['recorder','reviewer'],[],['enter','view'])])
permission('Theatre cue console',{'operator':['trigger'],'designer':['edit'],'director':['approve']},[],[(['operator','designer'],[],['approve']),(['operator','director'],['edit'],['trigger','approve'])])

# Validation-only mechanisms follow; none feed training groups.
def substring(title, pairs, tie='asc'):
    add(11,title,'Choose the longest nonempty contiguous substring occurring in both strings. Substrings must keep adjacent symbols in order. If lengths tie, choose the alphabetically '+('earliest' if tie=='asc' else 'latest')+' substring.',
        [(f'First string: {a}. Second string: {b}.',dict(a=a,b=b)) for a,b in pairs],tie=tie)
substring('Stencil overlap',[('ABXCD','ABYCD'),('CABDE','ZABD')])
substring('Signal motif comparison',[('TATGC','ATGTA'),('GACTA','TACTG')],tie='desc')
substring('Fabric code overlap',[('LMNLM','QLMNR'),('PQRSP','RSPQT')])
substring('Crate marking comparison',[('HHJKL','MJKLN'),('ABABA','BABAC')],tie='desc')

def brackets(title, pairs, ignore):
    add(12,title,'Validate (), [] and {} with a last-opened, first-closed stack. '+('Ignore letters and digits. ' if ignore else 'Only bracket symbols occur. ')+'Classify as valid, wrong closing type, closing with no opener, or unclosed opener. Report the first closing error; otherwise report leftover openers.',
        [(f'Sequence: {s}.',dict(sequence=s)) for s in pairs],ignore=ignore)
brackets('Expression wrapper check',['{[()]}','{[(])}'],False)
brackets('Annotated path notation',['a(b[c]d)e','a(b[c]d'],True)
brackets('Packing bracket notation',['[]{}()','[]}{()'],False)
brackets('Label formula enclosure',['x{y[z](q)}','x{y[z](q)]'],True)

def merge(title, left, right, tie, pairs):
    add(13,title,f'Merge the two queues by ascending numeric key. Preserve order within each queue. On equal head keys take from {tie} first. Report item labels only.',
        [(f'{left}: '+', '.join(f'{label}({key})' for label,key in a)+f'. {right}: '+', '.join(f'{label}({key})' for label,key in b)+'.',dict(left=a,right=b)) for a,b in pairs],tie_left=(tie==left))
merge('Two scanner intake','A','B','A',[
([['A1',1],['A2',3],['A3',3]],[['B1',2],['B2',3]]),
([['A1',2],['A2',5]],[['B1',2],['B2',4],['B3',6]])])
merge('Ticket desk consolidation','North','South','South',[
([['N1',1],['N2',4]],[['S1',1],['S2',3],['S3',4]]),
([['N1',2],['N2',2],['N3',5]],[['S1',2],['S2',6]])])
merge('Sensor event reconciliation','Red','Blue','Red',[
([['R1',0],['R2',7]],[['B1',1],['B2',7],['B3',8]]),
([['R1',3],['R2',4]],[['B1',1],['B2',2],['B3',4]])])
merge('Dispatch docket union','East','West','West',[
([['E1',2],['E2',5]],[['W1',1],['W2',5],['W3',5]]),
([['E1',1],['E2',1],['E3',3]],[['W1',1],['W2',2]])])

def parity(title, constraints, vectors):
    rule='Bits are numbered from 1 at the left. '+ ' '.join('Positions '+','.join(map(str,pos))+f' must contain an {"even" if parity==0 else "odd"} number of 1 bits.' for pos,parity in constraints)+' A vector passes only if every constraint holds.'
    add(14,title,rule,[(f'Vector: {v}.',dict(vector=v)) for v in vectors],constraints=constraints)
parity('Packet check bits',[([1,2,4],0),([2,3,5],1)],['10110','10100'])
parity('Control-panel wiring',[([1,3],1),([2,4],0)],['1000','1010'])
parity('Storage stripe audit',[([1,2,3],0),([3,4,5,6],0)],['110011','110010'])
parity('Switch bank parity',[([1,4,6],1),([2,3,5],1),([1,2],0)],['110000','100000'])

def median(title, pairs, tie):
    add(15,title,'Select the candidate with the highest median measurement. Sort each candidate\'s measurements; for even counts average the two middle values. On tied medians choose the alphabetically '+('earliest' if tie=='asc' else 'latest')+' candidate name.',
        [('Measurements: '+'; '.join(f'{name}: '+','.join(map(str,vals)) for name,vals in cs)+'.',dict(candidates=cs)) for cs in pairs],tie=tie)
median('Coating thickness winner',[
[['A',[1,8,9]],['B',[7,7,20]],['C',[5,6,40]]],
[['A',[1,8,10]],['B',[8,8,8]],['C',[2,7,30]]]],'asc')
median('Acoustic trial selection',[
[['D',[2,4,10,12]],['E',[6,6,7,7]],['F',[1,5,8,50]]],
[['D',[2,4,6,10]],['E',[3,5,7,9]],['F',[1,6,6,40]]]],'desc')
median('Adhesive strength choice',[
[['K',[3,9,10,11,12]],['L',[8,8,8,30,40]],['M',[1,7,7,8,50]]],
[['K',[1,9,9]],['L',[9,9,50]],['M',[2,8,60]]]],'desc')
median('Optical reading selection',[
[['Oak',[2,6,8,20]],['Pine',[5,7,9,11]],['Yew',[1,3,10,40]]],
[['Oak',[4,6,8,10]],['Pine',[1,7,7,30]],['Yew',[2,5,6,50]]]],'asc')

if __name__ == '__main__':
    assert len(policies) == 120
    assert all(sum(p['group']==g for p in policies)==(10 if g<=10 else 4) for g in range(1,16))
    # Names and listed candidate order carry no intended ranking information.
    rng=random.Random(174031)
    for policy in policies:
        if policy['group'] not in (2,15):continue
        labels=[c[0] for c in policy['cases'][0]['facts']['candidates']]
        renamed=labels[:];rng.shuffle(renamed);mapping=dict(zip(labels,renamed))
        for case in policy['cases']:
            candidates=case['facts']['candidates']
            for candidate in candidates:candidate[0]=mapping[candidate[0]]
            rng.shuffle(candidates)
            if policy['group']==2:
                case['text']='Candidates: '+'; '.join(f'{name}={tuple(vals)}' for name,vals in candidates)+'.'
            else:
                case['text']='Measurements: '+'; '.join(f'{name}: '+','.join(map(str,vals)) for name,vals in candidates)+'.'
    (ROOT/'source_cases.jsonl').write_text(''.join(json.dumps(p,ensure_ascii=False,sort_keys=True)+'\n' for p in policies))
    print('Authored policies:',len(policies),'cases:',sum(len(p['cases']) for p in policies))
