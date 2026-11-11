"""Original authored policies and paired consequential cases. Run locally; no dependencies."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CASES = []
DAYS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
def add(g, p, context, policy, facts_pair):
    for n, facts in enumerate(facts_pair, 1):
        CASES.append({'group_number':g, 'policy_number':p, 'case_number':n,
                      'context':context, 'policy':policy, 'facts':facts})
# Weekday calendars: conventions, not absolute dates or external calendar knowledge.
calendars = [
 ('Dispatch desk', [0,1,2,3,4], 1, False, [('Fri',1),('Fri',2)]),
 ('Museum rota', [1,2,3,4,5,6], 1, True, [('Mon',1),('Tue',2)]),
 ('Night pharmacy', list(range(7)), -1, False, [('Mon',1),('Mon',7)]),
 ('Weekend repair crew', [5,6], 1, False, [('Fri',2),('Sun',1)]),
 ('Market collection', [0,2,4], 1, True, [('Wed',1),('Thu',1)]),
 ('Archive deadline', [0,1,2,3,4], -1, False, [('Mon',1),('Sun',2)]),
 ('Reservoir sampling', [1,3,5], -1, True, [('Sat',1),('Sun',2)]),
 ('Daily alarm', list(range(7)), 1, True, [('Sun',1),('Sun',7)]),
 ('Theatre delivery', [2,3,4,5], 1, False, [('Tue',1),('Sat',2)]),
 ('Clinic records', [0,3], -1, True, [('Thu',2),('Wed',2)]),
]
for p,(ctx,active,direction,inclusive,pair) in enumerate(calendars,1):
    pol={'active':active,'direction':direction,'inclusive':inclusive}
    add(1,p,ctx,pol,[{'start':DAYS.index(d),'steps':s} for d,s in pair])
# Packs: total demand, usable inventory, extra reserve and minimum buy (packs).
packs = [
 ('Catering trays',12,2,0,0,[(24,0),(25,0)]),
 ('Ceramic tile cartons',8,0,3,0,[(13,0),(14,0)]),
 ('Clinic glove boxes',20,1,0,0,[(10,10),(31,10)]),
 ('Art paper bundles',5,3,0,0,[(5,0),(16,0)]),
 ('Filter cartridges',4,0,0,1,[(9,1),(11,1)]),
 ('Festival wristbands',25,2,5,0,[(45,0),(46,0)]),
 ('Shipping labels',10,0,0,0,[(30,10),(31,10)]),
 ('Bike brake pads',2,1,1,0,[(3,0),(4,0)]),
 ('Lab sample tubes',6,0,0,0,[(0,0),(1,0)]),
 ('Plant pots',9,2,0,2,[(14,0),(15,0)]),
]
for p,(ctx,size,minimum,reserve,damaged,pair) in enumerate(packs,1):
    add(2,p,ctx,{'size':size,'minimum':minimum,'reserve':reserve,'damaged':damaged},
        [{'demand':d,'stock':s} for d,s in pair])
# Proportional floor shares; leftovers either Hamilton-style or explicitly all to one recipient.
allocations = [
 ('Exhibit lighting hours',['Hall','Loft','Wing'],[5,3,2],'largest','forward',[9,10]),
 ('Workshop grant',['Clay','Ink','Glass'],[1,1,1],'largest','reverse',[4,5]),
 ('Broadcast slots',['News','Arts','Sport'],[2,3,1],'last','forward',[7,8]),
 ('Community transport seats',['North','South','West'],[0,3,2],'largest','forward',[4,5]),
 ('Server task budget',['Red','Blue','Gold'],[4,2,2],'largest','reverse',[5,6]),
 ('Water tokens',['Oak','Elm','Ash'],[2,1,4],'first','forward',[8,10]),
 ('Studio time',['Audio','Video','Photo'],[3,0,1],'largest','forward',[6,7]),
 ('Printed programme pages',['Dance','Drama','Music'],[1,2,2],'largest','reverse',[3,4]),
 ('Instrument lockers',['Brass','Strings','Winds'],[2,5,3],'last','forward',[11,13]),
 ('Volunteer meal tickets',['Gate','Stage','Desk'],[2,2,1],'largest','forward',[7,8]),
]
for p,(ctx,names,weights,mode,tie,totals) in enumerate(allocations,1):
    add(3,p,ctx,{'names':names,'weights':weights,'mode':mode,'tie':tie},[{'total':v} for v in totals])
# Integer clipping; open endpoints are consequential.
clips = [
 ('Thermostat setpoints',10,25,True,True,[(5,10),(25,30)]),
 ('Admission ages',8,16,False,True,[(8,8),(8,9)]),
 ('Shelf positions',1,12,True,False,[(12,15),(11,15)]),
 ('Voltage settings',-3,4,False,False,[(-4,-3),(-3,0)]),
 ('Booking hour indices',0,23,True,True,[(-5,26),(7,7)]),
 ('Trial dosage units',2,8,False,False,[(3,7),(7,8)]),
 ('Parcel weights',1,20,True,True,[(21,24),(19,21)]),
 ('Signed offset limits',-8,-2,True,False,[(-4,0),(-10,-8)]),
 ('Page selection',4,9,False,True,[(1,5),(9,12)]),
 ('Oven dial notches',0,6,True,False,[(5,5),(6,6)]),
]
for p,(ctx,lo,hi,lc,hc,pair) in enumerate(clips,1):
    add(4,p,ctx,{'lo':lo,'hi':hi,'lc':lc,'hc':hc},[{'lo':a,'hi':b} for a,b in pair])
# Rate comparisons: two rates with equal dimensions, exact comparison only.
rates = [
 ('Document scanners','pages per minute','higher','Tie',[(30,2,44,3),(30,2,45,3)]),
 ('Paint quotes','pounds per panel','lower','Vendor B',[(18,3,35,5),(18,3,30,5)]),
 ('Fuel usage','litres per kilometre','lower','Tie',[(8,100,12,150),(9,100,12,150)]),
 ('Garden pumps','litres per minute','higher','Vendor A',[(20,4,30,6),(19,4,30,6)]),
 ('Print resolution','dots per millimetre','higher','Tie',[(72,6,60,5),(73,6,60,5)]),
 ('Material waste','grams per component','lower','Vendor A',[(7,4,14,8),(8,4,14,8)]),
 ('Battery endurance','hours per charge unit','higher','Vendor B',[(21,3,24,4),(18,3,24,4)]),
 ('Cleaning concentrate','pounds per litre','lower','Tie',[(11,2,16,3),(10,2,15,3)]),
 ('Typing service','characters per second','higher','Tie',[(100,7,99,7),(100,7,200,14)]),
 ('Packaging density','grams per parcel','lower','Vendor B',[(9,2,14,3),(8,2,12,3)]),
]
for p,(ctx,unit,prefer,tie,pair) in enumerate(rates,1):
    add(5,p,ctx,{'unit':unit,'prefer':prefer,'tie':tie},[dict(zip(['a_num','a_den','b_num','b_den'],v)) for v in pair])
# Ordered transformations. Tuples are operation then parameters; no unstated geometric conventions.
transforms = [
 ('Floor robot',[['shift',2,-1],['ccw']],[[-2,1],[0,0]]),
 ('Plotter calibration',[['cw'],['shift',-3,2]],[[1,3],[0,-2]]),
 ('Map overlay',[['reflect_x'],['shift',1,4]],[[2,-1],[-1,0]]),
 ('Sprite editor',[['shift',-2,3],['reflect_y']],[[2,-3],[3,1]]),
 ('Survey marker',[['scale',2],['shift',-1,1]],[[1,0],[-2,3]]),
 ('Image tile',[['shift',1,-2],['scale',3]],[[0,2],[-1,1]]),
 ('Warehouse cart',[['swap'],['reflect_x']],[[3,-2],[-1,4]]),
 ('Stage rig',[['reflect_y'],['cw']],[[2,1],[0,-3]]),
 ('Board token',[['ccw'],['shift',2,2],['reflect_x']],[[1,2],[-2,-1]]),
 ('Sensor frame',[['scale',-1],['swap'],['shift',0,3]],[[2,0],[-1,3]]),
]
for p,(ctx,ops,pair) in enumerate(transforms,1):
    add(6,p,ctx,{'ops':ops},[{'point':v} for v in pair])
# Fixed batch yields: distinctly ordered, explicitly stated loss stages.
yields = [
 ('Candle workshop',12,1,0,0,0,[2,3]),
 ('Biscuit kitchen',20,0,2,0,0,[2,3]),
 ('Resin casting',9,2,1,0,0,[2,4]),
 ('Soap cutting',10,0,0,3,0,[1,3]),
 ('Ceramic firing',15,1,0,4,0,[2,3]),
 ('Sticker sheets',8,0,1,2,0,[1,4]),
 ('Sample preparation',6,1,0,0,2,[1,3]),
 ('Thread spool packing',14,2,1,0,3,[1,2]),
 ('Concrete pavers',16,0,0,2,5,[1,2]),
 ('Chocolate moulding',11,1,2,1,4,[1,3]),
]
for p,(ctx,gross,per_loss,whole_loss,retain,final_loss,pair) in enumerate(yields,1):
    add(7,p,ctx,{'gross':gross,'per_loss':per_loss,'whole_loss':whole_loss,'retain':retain,'final_loss':final_loss},[{'batches':n} for n in pair])
# Appointment starts in minute indices; select earliest supplied legal candidate, not arbitrary minute.
schedules = [
 ('Massage room',10,False,False,[[[30,60]],[[30,60]]],[[69,70,80],[60,65,69]]),
 ('Dental chair',15,False,True,[[[20,50]],[[20,50]]],[[65,66,70],[50,64,65]]),
 ('Recording booth',5,True,False,[[[10,25],[60,75]],[[10,25],[60,75]]],[[30,35,40],[40,45,50]]),
 ('Training bay',0,False,False,[[[15,45]],[[15,45]]],[[45,46,60],[30,40,44]]),
 ('Photo studio',20,True,True,[[[0,30],[100,120]],[[0,30],[100,120]]],[[50,51,60],[65,70,80]]),
 ('Hearing clinic',8,False,False,[[[25,40],[90,110]],[[25,40],[90,110]]],[[48,50,60],[110,117,118]]),
 ('Vehicle inspection',12,True,False,[[[10,35],[85,105]],[[10,35],[85,105]]],[[47,48,50],[60,61,62]]),
 ('Practice room',1,False,True,[[[5,20]],[[5,20]]],[[21,22,25],[19,20,21]]),
 ('Consultation pod',30,False,False,[[[60,90]],[[60,90]]],[[110,119,120],[100,105,115]]),
 ('Equipment demo',6,True,False,[[[0,15],[55,70]],[[0,15],[55,70]]],[[21,25,30],[35,36,37]]),
]
for p,(ctx,gap,both,strict,busy,pair) in enumerate(schedules,1):
    # Vary duration meaningfully; both-side policies expose the next appointment boundary.
    duration = [20,10,20,15,25,25,25,5,15,15][p-1]
    add(8,p,ctx,{'gap':gap,'both':both,'strict':strict,'duration':duration},[{'busy':b,'candidates':c} for b,c in zip(busy,pair)])
# Symbol multisets: exact after explicit normalization, options are named kits with literal strings.
multisets = [
 ('Bead kits',False,'-',{'Amber':'aab','Birch':'abb','Cedar':'abc'},['a-b-a','b-b-a']),
 ('Stamp trays',True,' ',{'Tray K':'AaB','Tray L':'AbB','Tray M':'AbC'},['b a A','B b A']),
 ('Wire labels',False,'.',{'Coil P':'XXy','Coil Q':'Xyy','Coil R':'XYy'},['y.X.X','Y.y.X']),
 ('Tile bags',True,'_',{'Bag Red':'mmn','Bag Blue':'mnn','Bag Green':'mno'},['N_m_M','o_N_m']),
 ('Charm packets',False,' ',{'Pouch 1':'112','Pouch 2':'122','Pouch 3':'123'},['2 1 1','2 2 1']),
 ('Assembly tokens',False,'/',{'Set D':'++-','Set E':'+--','Set F':'+-='},['+/+/-','-/=/+']),
 ('Stencil bundles',True,'-',{'Bundle U':'pqQ','Bundle V':'ppQ','Bundle W':'pqr'},['q-P-q','Q-p-P']),
 ('Cable tags',False,'_',{'Rack A':'aAB','Rack B':'aaB','Rack C':'aBB'},['B_A_a','B_a_a']),
 ('Badge packs',False,':',{'Pack N':'778','Pack S':'788','Pack W':'789'},['8:7:7','9:8:7']),
 ('Pattern swatches',True,'.',{'Roll 1':'rss','Roll 2':'rrs','Roll 3':'rst'},['S.r.S','t.S.r']),
]
for p,(ctx,fold,ignore,choices,pair) in enumerate(multisets,1):
    add(9,p,ctx,{'fold':fold,'ignore':ignore,'choices':choices},[{'symbols':s} for s in pair])
# Nested conditional policies: expression trees, no external interpretation of labels.
def branch(var,op,threshold,yes,no): return [var,op,threshold,yes,no]
nested = [
 ('Parcel routing',branch('weight','>',10,'Freight',branch('distance','<=',5,'Local','Standard')),[{'weight':10,'distance':5},{'weight':11,'distance':2}]),
 ('Cooling response',branch('temperature','>=',30,branch('occupancy','>',0,'Ventilate','Idle'),'Standby'),[{'temperature':30,'occupancy':0},{'temperature':30,'occupancy':1}]),
 ('Publication queue',branch('errors','==',0,branch('pages','<',20,'Quick','Long'),'Revise'),[{'errors':0,'pages':20},{'errors':1,'pages':5}]),
 ('Watering programme',branch('moisture','<',4,'Soak',branch('heat','>=',8,'Mist','Skip')),[{'moisture':4,'heat':8},{'moisture':3,'heat':2}]),
 ('Scholarship tier',branch('score','>=',80,branch('income','<=',25,'Full','Half'),'None'),[{'score':80,'income':25},{'score':80,'income':26}]),
 ('Machine maintenance',branch('vibration','>',6,'Stop',branch('hours','>=',100,'Service','Run')),[{'vibration':6,'hours':100},{'vibration':7,'hours':10}]),
 ('Ticket desk',branch('age','<',16,'Junior',branch('visits','>=',4,'Member','Adult')),[{'age':16,'visits':4},{'age':15,'visits':0}]),
 ('Storage class',branch('fragility','==',1,branch('temperature','<',0,'Padded cold','Padded'),'Ordinary'),[{'fragility':1,'temperature':0},{'fragility':1,'temperature':-1}]),
 ('Exhibit access',branch('capacity','<=',0,'Wait',branch('pass','==',1,'Enter','Buy ticket')),[{'capacity':0,'pass':1},{'capacity':1,'pass':1}]),
 ('Release gate',branch('failures','!=',0,'Block',branch('approvals','>=',2,'Release','Hold')),[{'failures':0,'approvals':1},{'failures':0,'approvals':2}]),
]
for p,(ctx,tree,pair) in enumerate(nested,1): add(10,p,ctx,{'tree':tree},pair)
# Held-out mechanisms below are validation-only.
romans = [
 ('Inscription decoder',{'I':1,'V':5,'X':10},['XIV','XVI']),
 ('Clock plaque reader',{'I':1,'V':5,'X':10,'L':50},['XLIX','XLVI']),
 ('Archive volume marks',{'I':1,'V':5,'X':10,'L':50,'C':100},['XCIV','LXXXIX']),
 ('Medal date fragments',{'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000},['CDIX','CMXI']),
]
for p,(ctx,values,pair) in enumerate(romans,1): add(11,p,ctx,{'values':values},[{'numeral':s} for s in pair])
postfix = [
 ('Calculator register',['8 3 - 2 *','8 3 2 * -']),
 ('Meter formula',['12 3 / 2 -','12 3 2 - /']),
 ('Workshop arithmetic',['4 7 - 3 *','4 7 3 - *']),
 ('Lab stack machine',['5 2 + 3 1 - *','5 2 3 + * 1 -']),
]
for p,(ctx,pair) in enumerate(postfix,1): add(12,p,ctx,{},[{'tokens':s.split()} for s in pair])
topos = [
 ('Exhibit installation',['A','B','C','D'],'alphabetically first',[[['A','C'],['B','C'],['C','D']],[['B','A'],['A','D'],['C','D']]]),
 ('Publication stages',['Edit','Layout','Proof','Ship'],'alphabetically last',[[['Edit','Proof'],['Layout','Proof'],['Proof','Ship']],[['Layout','Edit'],['Edit','Ship'],['Proof','Ship']]]),
 ('Assembly stations',['Cut','Drill','Paint','Wrap'],'listed first',[[['Cut','Paint'],['Drill','Paint'],['Paint','Wrap']],[['Drill','Cut'],['Cut','Wrap'],['Paint','Wrap']]]),
 ('Data preparation',['Fetch','Clean','Index','Store'],'listed last',[[['Fetch','Index'],['Clean','Index'],['Index','Store']],[['Clean','Fetch'],['Fetch','Store'],['Index','Store']]]),
]
for p,(ctx,nodes,tie,pair) in enumerate(topos,1): add(13,p,ctx,{'nodes':nodes,'tie':tie},[{'edges':e} for e in pair])
hammings = [
 ('Radio tag decoder',{'A':'0000','B':'0011','C':'1111','D':'1100'},'alphabetically first',['0001','1110']),
 ('Parcel marker decoder',{'K':'10101','L':'01010','M':'11100','N':'00011'},'alphabetically last',['10100','01011']),
 ('Relay beacon',{'Red':'000000','Blue':'111000','Gold':'000111','Teal':'111111'},'listed first',['100000','111100']),
 ('Survey flag code',{'P':'0101','Q':'1010','R':'0000','S':'1111'},'listed last',['0011','0100']),
]
for p,(ctx,codebook,tie,pair) in enumerate(hammings,1): add(14,p,ctx,{'codebook':codebook,'tie':tie},[{'received':w} for w in pair])
windows = [
 ('Hourly output',2,'earliest',[[2,6,6,2],[6,2,6,2]]),
 ('Sensor trend',3,'latest',[[1,4,4,1,4],[-3,-1,-2,-1,-3]]),
 ('Daily footfall',4,'earliest',[[3,0,2,3,4,1],[2,2,2,2,1,3]]),
 ('Quality readings',2,'latest',[[-5,-1,-1,-5],[3,5,1,7,0]]),
]
for p,(ctx,width,tie,pair) in enumerate(windows,1): add(15,p,ctx,{'width':width,'tie':tie},[{'values':v} for v in pair])
if __name__ == '__main__':
    (ROOT/'authoring_cases.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in CASES))
    print(f'Authored {len(CASES)} cases across {len({(c["group_number"],c["policy_number"]) for c in CASES})} policies')
