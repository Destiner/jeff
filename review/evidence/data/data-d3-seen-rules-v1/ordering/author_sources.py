"""Original policy/fact authoring; never reads historical examples."""
import json
from pathlib import Path
P=Path(__file__).resolve().parent
assign=json.loads((P/'group_assignments.json').read_text())['groups']
rows=[]
def add(mech,p,policy,cases):
    group=f'data:d3-seen-rules-v1:{mech}:p{p:02}'
    for i,facts in enumerate(cases,1):
        rows.append(dict(id=f'{group}:c{i:02}',group_id=group,mechanism_id=mech,policy_domain=assign[group]['policy_domain'],policy=policy,facts=facts))
# Ranking criteria are in precedence order, not a weighted score.
add('lexicographic',1,dict(context='A reef nursery must choose one shipment route.',criteria=[['survival','max'],['hours','min'],['cost','min']],units='survival points; hours; cost credits'),[
 {'candidates':[['Atoll',92,8,41],['Shoal',92,6,54],['Lagoon',91,3,19],['Cove',92,6,49]]},
 {'candidates':[['Atoll',94,9,70],['Shoal',93,4,20],['Lagoon',94,9,68],['Cove',94,10,30]]}])
add('lexicographic',2,dict(context='An archive chooses the next oral-history reel to digitise.',criteria=[['damage','max'],['consent_age','max'],['minutes','min']],units='damage grade; consent age in days; running minutes'),[
 {'candidates':[['Birch',3,80,44],['Elm',3,80,39],['Ash',3,79,12],['Yew',2,130,20]]},
 {'candidates':[['Birch',2,200,10],['Elm',4,18,60],['Ash',4,19,75],['Yew',4,19,72]]}])
add('lexicographic',3,dict(context='A mountain team selects one avalanche sensor for inspection.',criteria=[['days_offline','max'],['walk','min'],['asset','min']],units='days offline; walk minutes; asset number'),[
 {'candidates':[['Ridge',5,45,18],['Gully',5,45,12],['Spur',5,50,3],['Bowl',4,10,1]]},
 {'candidates':[['Ridge',0,10,18],['Gully',1,70,12],['Spur',1,60,3],['Bowl',1,60,8]]}])
add('lexicographic',4,dict(context='A community kiln has one firing reservation available.',criteria=[['deadline','min'],['shelf_use','max'],['request','min']],units='deadline day number; shelf-use percent; request number'),[
 {'candidates':[['Willow',12,85,31],['Ochre',12,85,28],['Slate',12,80,9],['Reed',13,100,1]]},
 {'candidates':[['Willow',9,70,31],['Ochre',10,95,28],['Slate',9,72,9],['Reed',9,72,11]]}])
add('lexicographic',5,dict(context='A ferry dispatcher assigns the only accessible ramp to one sailing.',criteria=[['unassisted','min'],['waiting','max'],['berth','min']],units='passengers able to board without ramp; waiting minutes; berth number'),[
 {'candidates':[['Heron',0,22,4],['Tern',0,22,2],['Gull',0,20,1],['Ibis',1,40,3]]},
 {'candidates':[['Heron',2,60,4],['Tern',1,8,2],['Gull',1,9,1],['Ibis',1,10,3]]}])
add('lexicographic',6,dict(context='A habitat trust awards one pollinator corridor planting bid.',criteria=[['native_species','max'],['gap','min'],['grant','min']],units='native species count; unplanted gap metres; grant credits'),[
 {'candidates':[['Meadow',14,30,800],['Hedge',14,30,790],['Brook',14,31,500],['Verge',13,0,300]]},
 {'candidates':[['Meadow',16,50,900],['Hedge',15,10,400],['Brook',16,49,950],['Verge',16,49,940]]}])
# Arrival numbers are explicit FIFO sequence, regardless of displayed order.
add('fifo',1,dict(context='A mosaic studio issues tessera stock.',unit='tiles',note='All listed batches are usable; issue whole tiles.'),[
 {'request':23,'batches':[['Amber',1,12],['Chalk',2,16],['Indigo',3,20]]},
 {'request':28,'batches':[['Amber',1,12],['Chalk',2,16],['Indigo',3,20]]}])
add('fifo',2,dict(context='A garden withdraws stored rainwater from its cistern batches.',unit='litres',note='All listed water is usable; partial withdrawals are allowed.'),[
 {'request':75,'batches':[['North',1,30],['East',2,45],['West',3,60]]},
 {'request':82,'batches':[['North',1,30],['East',2,45],['West',3,60]]}])
add('fifo',3,dict(context='A costume workshop issues reclaimed felt.',unit='metres',note='All rolls are usable; cutting a roll is allowed.'),[
 {'request':19,'batches':[['Moss',1,8],['Rust',2,15],['Ink',3,11]]},
 {'request':7,'batches':[['Moss',1,8],['Rust',2,15],['Ink',3,11]]}])
add('fifo',4,dict(context='A mural team issues bioluminescent paint stock.',unit='sealed tins',note='Every listed tin passed inspection; no expiry preference applies.'),[
 {'request':17,'batches':[['Glow',1,6],['Halo',2,10],['Spark',3,9]]},
 {'request':10,'batches':[['Glow',1,6],['Halo',2,10],['Spark',3,9]]}])
add('fifo',5,dict(context='A theatre issues stage counterweights.',unit='blocks',note='All blocks have equal mass and are usable; issue whole blocks.'),[
 {'request':18,'batches':[['Brass',1,9],['Steel',2,9],['Iron',3,14]]},
 {'request':20,'batches':[['Brass',1,9],['Steel',2,9],['Iron',3,14]]}])
add('fifo',6,dict(context='A cooling hub dispatches reusable ice packs.',unit='packs',note='All batches are frozen and ready; return date gives no priority.'),[
 {'request':14,'batches':[['Polar',1,5],['Frost',2,12],['Snow',3,16]]},
 {'request':4,'batches':[['Polar',1,5],['Frost',2,12],['Snow',3,16]]}])
# Ordered arithmetic deliberately uses differing credit placement and percentage bases.
add('discount',1,dict(context='A community planetarium invoices workshop places.',steps=[['fixed','12'],['percent','20']],note='The credit applies once per booking.'),[{'base':'90'},{'base':'140'}])
add('discount',2,dict(context='A print shop quotes restored map reproductions.',steps=[['percent','15'],['fixed','9']],note='The voucher is deducted after the trade reduction.'),[{'base':'120'},{'base':'200'}])
add('discount',3,dict(context='A cooperative quotes canopy shelter installation.',steps=[['fixed','40'],['percent','25'],['fixed','5']],note='The final credit is a separate site-reuse allowance.'),[{'base':'260'},{'base':'340'}])
add('discount',4,dict(context='A repairable toy kit supplier calculates an invoice.',steps=[['percent','10'],['fixed','6'],['percent','20']],note='Each percentage uses the subtotal at its own step.'),[{'base':'80'},{'base':'130'}])
add('discount',5,dict(context='A wildlife sketching school calculates course fees.',steps=[['fixed','15'],['percent','10'],['percent','20']],note='Membership and early-booking percentages are sequential, not added.'),[{'base':'115'},{'base':'165'}])
add('discount',6,dict(context='A gallery quotes reusable exhibition plinth hire.',steps=[['percent','25'],['fixed','8'],['percent','10']],note='The reuse credit falls between the two percentage reductions.'),[{'base':'96'},{'base':'176'}])
add('rounding',1,dict(context='A lab logs lichen sample mass.',unit='g',step='0.1',places=1),[{'value':'2.35'},{'value':'2.349'}])
add('rounding',2,dict(context='An embossing operator sets the pressure dial.',unit='kPa',step='5',places=0),[{'value':'42.5'},{'value':'47.4'}])
add('rounding',3,dict(context='A canal survey reports salinity.',unit='ppt',step='0.01',places=2),[{'value':'1.205'},{'value':'1.2149'}])
add('rounding',4,dict(context='A concert rig displays its load.',unit='kg',step='10',places=0),[{'value':'125'},{'value':'134.9'}])
add('rounding',5,dict(context='A conservator logs heritage tile thickness.',unit='mm',step='0.5',places=1),[{'value':'7.25'},{'value':'7.76'}])
add('rounding',6,dict(context='An orbital model receives distance labels.',unit='cm',step='2',places=0),[{'value':'19'},{'value':'20.99'}])
(P/'source_cases.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
print(f'Authored {len(rows)} source cases')
