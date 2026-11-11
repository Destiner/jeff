"""Original authored policies/facts; deterministic, standard-library-only rendering.
Run here with python3 generate.py, then python3 audit.py. No external row inputs.
"""
import hashlib
import json
import os
from pathlib import Path
import random
from collections import Counter

ROOT = Path(__file__).resolve().parent
SEED = 704931
JOB = 'data-d3-seen-rules-v1-geometry-original-20261112-704931'
CONFIG = Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/d3-seen-rules-v1.json')

def dump(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def lines(name, rows):
    (ROOT / name).write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# These policy groups were assigned and written before this source was authored.
assignments = json.loads((ROOT / 'group_assignments.json').read_text())['groups']
sources = []

def add(mechanism, p, policy, cases):
    group = f'data:d3-seen-rules-v1:{mechanism}:p{p:02d}'
    for n, case in enumerate(cases, 1):
        sources.append(dict(id=f'{group}:c{n:02d}', group_id=group,
                            mechanism_id=mechanism, policy_domain=assignments[group]['policy_domain'],
                            policy=policy, **case))

# Pack conventions intentionally vary: unconditional orders versus deficit-only,
# stock acceptance, protected reserves, and independently chosen pack/minimum sizes.
add('packs', 1, dict(size=8, minimum=3, always=False,
    text='Trail markers come in packs of 8. Cover the installation demand plus the reserve, using only accepted stock. If stock covers both, order nothing; otherwise buy the fewest whole packs covering the shortfall, at least 3 packs.'), [
    dict(context='A new marsh spur needs markers; the reserve must remain for later repairs.', facts=dict(demand=19, reserve=5, stock=8, rejected=0), distractors=['2 packs','1 pack','0 packs']),
    dict(context='After a storm, replacements and a rebuilt emergency reserve are needed; water-damaged markers cannot be used.', facts=dict(demand=31, reserve=7, stock=9, rejected=4), distractors=['3 packs','6 packs','4 packs'])])
add('packs', 2, dict(size=12, minimum=2, always=True,
    text='Mallet sleeves come in packs of 12. Required stock is the fitting demand plus reserve. Accepted stock excludes rejected sleeves. Every scheduled order must buy at least 2 packs, even with no shortfall; otherwise round the shortfall up to whole packs.'), [
    dict(context='The touring percussion case already has enough sleeves, but its scheduled replenishment order is mandatory.', facts=dict(demand=14,reserve=4,stock=23,rejected=1), distractors=['0 packs','1 pack','3 packs']),
    dict(context='A school loan programme must sleeve newly accepted mallets; split sleeves from the returned kit are rejected.', facts=dict(demand=37,reserve=6,stock=20,rejected=2), distractors=['2 packs','4 packs','5 packs'])])
add('packs', 3, dict(size=10, minimum=1, always=False,
    text='Sampler filters are sold in packs of 10. Maintain the run demand plus reserve after rejecting contaminated stock. Buy no packs if accepted stock suffices; otherwise buy the smallest whole-pack quantity covering the deficit, with a minimum of 1 pack.'), [
    dict(context='A cancelled river survey leaves enough sealed filters for the shorter replacement run and its reserve.', facts=dict(demand=17,reserve=3,stock=24,rejected=4), distractors=['1 pack','2 packs']),
    dict(context='A roadside pollution episode adds a second sampling shift; exposed filters are contaminated and unavailable.', facts=dict(demand=32,reserve=8,stock=25,rejected=6), distractors=['1 pack','2 packs'])])
add('packs', 4, dict(size=25, minimum=4, always=False,
    text='Mosaic spacers come in packs of 25. Keep the work demand plus reserve, counting stock only after removing rejected spacers. Order zero if enough remain. For a positive deficit, order the fewest whole packs that cover it, but never fewer than 4 packs.'), [
    dict(context='A small repair uses existing stock, while a separate teaching reserve must remain untouched.', facts=dict(demand=94,reserve=16,stock=40,rejected=5), distractors=['3 packs','5 packs','1 pack']),
    dict(context='A reopened mural section needs more spacers; warped returns fail inspection.', facts=dict(demand=143,reserve=21,stock=70,rejected=7), distractors=['4 packs','6 packs','7 packs'])])
add('packs', 5, dict(size=6, minimum=2, always=False,
    text='Windsock clips are sold in packs of 6. The target is installation demand plus reserve; rejected stock is unusable. If accepted stock meets the target, buy none. Otherwise buy the fewest whole packs covering the missing clips, subject to a 2-pack minimum.'), [
    dict(context='A replacement windsock frame can reuse most clips, but two corroded clips have been rejected.', facts=dict(demand=13,reserve=4,stock=7,rejected=2), distractors=['1 pack','3 packs','4 packs']),
    dict(context='A second weather mast is commissioned with a larger emergency reserve; several stored clips have cracked.', facts=dict(demand=16,reserve=8,stock=16,rejected=5), distractors=['2 packs','1 pack'])])
add('packs', 6, dict(size=16, minimum=1, always=True,
    text='Costume reflectors come in packs of 16. Desired stock equals show demand plus reserve, excluding rejected stock from what is available. Each scheduled purchase buys at least 1 pack. Above that minimum, buy only enough whole packs to cover the deficit.'), [
    dict(context='A night parade needs replacement reflectors and a small backstage reserve; delaminated pieces are rejected.', facts=dict(demand=29,reserve=4,stock=20,rejected=4), distractors=['1 pack','3 packs','4 packs']),
    dict(context='A touring show doubles its reserve before dispatch; only the unopened returned reflectors pass inspection.', facts=dict(demand=42,reserve=10,stock=25,rejected=5), distractors=['1 pack','3 packs','4 packs'])])

# Rate candidates are authored independently of option and listing order.
def cand(name, n, d):
    return dict(name=name, numerator=n, denominator=d)
add('rates',1,dict(direction='max',numerator='water collected (ml)',denominator='trial time (minutes)',tie='alphabetical',
    text='Select the collector with the greatest water collected per minute. Compare exact fractions, without rounding. If rates tie, choose the alphabetically earliest collector name.'),[
    dict(context='Choose a collector for the ridge station using these first field trials.',facts=dict(candidates=[cand('Bracken',81,9),cand('Clover',64,8),cand('Aster',54,6)])),
    dict(context='For a short coastal deployment, use these replacement-mesh trials rather than the earlier ridge results.',facts=dict(candidates=[cand('Aster',103,12),cand('Bracken',94,11),cand('Clover',77,9)]))])
add('rates',2,dict(direction='max',numerator='accepted corrections',denominator='editing time (minutes)',tie='reverse_alphabetical',
    text='Select the editor with the most accepted caption corrections per minute. Rejected edits are already excluded from the counts. Use exact fractions; on a tie, choose the alphabetically latest editor name.'),[
    dict(context='Allocate the live-event caption backlog using the timed rehearsal.',facts=dict(candidates=[cand('Dara',70,12),cand('Ivo',41,7),cand('Nuri',35,6)])),
    dict(context='An archival batch contains more specialist terms; use its separate timed sample.',facts=dict(candidates=[cand('Dara',18,4),cand('Ivo',27,6),cand('Nuri',40,9)]))])
add('rates',3,dict(direction='max',numerator='usable offcut area (square cm)',denominator='input area (square cm)',tie='alphabetical',
    text='Select the cutting layout with the largest usable-offcut fraction: usable offcut area divided by input area. Do not compare raw areas alone. Use exact fractions; tied layouts are resolved by alphabetically earliest name.'),[
    dict(context='Choose the layout for reclaimed sailcloth with the measured batch areas.',facts=dict(candidates=[cand('Arc',48,80),cand('Bay',66,100),cand('Cove',39,60),cand('Dune',84,140)])),
    dict(context='A narrow-roll consignment requires a fresh layout comparison.',facts=dict(candidates=[cand('Arc',35,50),cand('Bay',49,70),cand('Cove',68,100),cand('Dune',81,120)]))])
add('rates',4,dict(direction='min',numerator='elapsed time (minutes)',denominator='filtered water (litres)',tie='reverse_alphabetical',
    text='Select the filter with the least elapsed time per litre filtered. A lower minutes/litre fraction is better. Compare exactly; on a tie choose the alphabetically latest filter name.'),[
    dict(context='Choose a filter for the first snowmelt delivery.',facts=dict(candidates=[cand('Ash',14,8),cand('Birch',19,11),cand('Cedar',7,4)])),
    dict(context='After a sediment surge, compare these new trials only.',facts=dict(candidates=[cand('Ash',12,8),cand('Birch',18,12),cand('Cedar',23,15)]))])
add('rates',5,dict(direction='max',numerator='air cleared (cubic metres)',denominator='fan time (minutes)',tie='reverse_alphabetical',
    text='Choose the vent with greatest cleared-air volume per minute. Compare exact fractions; if equal, choose the alphabetically latest vent name. Trials already exclude startup time.'),[
    dict(context='Select a vent for the humid seedling shelter from full-speed measurements.',facts=dict(candidates=[cand('East',117,13),cand('North',80,9),cand('South',91,10)])),
    dict(context='Night noise limits require these separate low-speed measurements.',facts=dict(candidates=[cand('East',35,5),cand('North',49,7),cand('South',62,9)]))])
add('rates',6,dict(direction='max',numerator='intact tiles recovered',denominator='crew-hours',tie='alphabetical',
    text='Select the crew with the greatest intact tiles recovered per crew-hour. Crew-hours are already total labour, not clock time. Compare exact fractions, and break ties by alphabetically earliest crew name.'),[
    dict(context='Choose a crew for careful salvage from a stairwell.',facts=dict(candidates=[cand('Amber',55,8),cand('Blue',48,7),cand('Copper',62,9),cand('Dove',83,12)])),
    dict(context='For a roof removal, use the separate scaffold-access trial.',facts=dict(candidates=[cand('Amber',40,6),cand('Blue',54,8),cand('Copper',81,12),cand('Dove',65,10)]))])

# Transforms are explicit assignments of coordinates, not assumed geometric lore.
def op(a,b,c,d,tx=0,ty=0):
    return dict(matrix=[[a,b],[c,d]],offset=[tx,ty])
add('coordinates',1,dict(ops=[op(1,0,0,1,3,-2),op(-1,0,0,1)],
    text='To register loom coordinates, first translate (x,y) to (x+3,y-2); then reflect that result to (-x,y). Apply each rule to the current coordinates, in that order.'),[
    dict(context='The first anchor on a wide tapestry panel is at (2,5).',facts=dict(point=[2,5]),distractors=['(5,3)','(1,3)','(-5,7)']),
    dict(context='A repair motif starts left of the loom origin at (-4,2).',facts=dict(point=[-4,2]),distractors=['(7,0)','(-1,0)','(1,4)'])])
add('coordinates',2,dict(ops=[op(0,1,1,0),op(1,0,0,1,-2,4)],
    text='For follow-spot calibration, first swap coordinates: (x,y) becomes (y,x). Then translate the result to (x-2,y+4). Each operation uses the preceding result.'),[
    dict(context='A balcony cue is recorded at (4,-1).',facts=dict(point=[4,-1]),distractors=['(3,2)','(-1,4)','(2,3)']),
    dict(context='A floor cue after the stage reset is at (-2,6).',facts=dict(point=[-2,6]),distractors=['(10,-4)','(6,-2)','(-4,10)'])])
add('coordinates',3,dict(ops=[op(0,1,-1,0),op(1,0,0,1,5,1),op(1,0,0,-1)],
    text='Orient the relief map by applying these steps in order: (x,y) becomes (y,-x); then becomes (x+5,y+1); then becomes (x,-y). Every step uses the current coordinates.'),[
    dict(context='The ridge marker is originally at (3,2).',facts=dict(point=[3,2]),distractors=['(7,-2)','(3,8)','(7,4)']),
    dict(context='A new valley inset uses the original marker (-1,-4).',facts=dict(point=[-1,-4]),distractors=['(1,2)','(1,0)','(9,2)'])])
add('coordinates',4,dict(ops=[op(1,0,0,1,-3,2),op(0,-1,1,0)],
    text='Align a kite-camera overlay by first translating (x,y) to (x-3,y+2), then turning the result using (x,y) to (-y,x). Do not reverse these steps.'),[
    dict(context='A beach control point has original coordinates (5,4).',facts=dict(point=[5,4]),distractors=['(-7,7)','(6,-2)','(2,6)']),
    dict(context='A later inland flight uses a control point at (3,-2).',facts=dict(point=[3,-2]),distractors=['(-1,5)','(0,2)','(2,0)'])])
add('coordinates',5,dict(ops=[op(1,0,0,-1),op(0,1,1,0),op(1,0,0,1,2,-3)],
    text='Place the ceramic decal by first mapping (x,y) to (x,-y), then swapping coordinates to (y,x), then translating to (x+2,y-3). Apply operations to the current result.'),[
    dict(context='A rim decal has source position (7,4).',facts=dict(point=[7,4]),distractors=['(6,-10)','(-4,7)','(-4,9)']),
    dict(context='A handle decal on the next mould has source position (1,-2).',facts=dict(point=[1,-2]),distractors=['(0,-4)','(2,1)','(-1,0)'])])
add('coordinates',6,dict(ops=[op(-1,0,0,1),op(1,0,0,1,4,-1),op(-1,0,0,-1)],
    text='Convert railway-grid coordinates in order: reflect (x,y) to (-x,y), translate to (x+4,y-1), and finally map to (-x,-y). Each step uses the result of the last.'),[
    dict(context='A signal at (4,1) is being assigned to the new control display.',facts=dict(point=[4,1]),distractors=['(8,2)','(-8,0)','(0,-2)']),
    dict(context='An added siding turnout has source coordinates (1,-3).',facts=dict(point=[1,-3]),distractors=['(5,-2)','(-5,4)','(3,-4)'])])

# Booked intervals are chronological schedules, never randomized queues.
def schedule(context, bookings, starts):
    return dict(context=context, facts=dict(bookings=bookings, starts=starts))
add('cooldown',1,dict(duration=12,gap=8,opening='09:00',closing='10:20',close_mode='reset',
    text='A new curing booking lasts 12 minutes; existing bookings have the stated end times. Every booking requires 8 minutes of exclusive cooldown afterward. Endpoints may touch. Work opens at 09:00; both the new session and its cooldown must finish by 10:20.'),[
    schedule('Find a slot for a varnished panel between existing booth jobs.',[['09:00','09:12'],['09:40','09:52']],['09:19','09:20','10:00']),
    schedule('An urgent replacement panel needs a slot after a long curing run.',[['09:00','09:45']],['09:52','10:01','10:08'])])
add('cooldown',2,dict(duration=20,gap=5,opening='13:00',closing='14:30',close_mode='session',
    text='A new oral-history session lasts 20 minutes; existing sessions have their stated end times. Leave at least 5 minutes between any two sessions for booth reset. Exact boundary contact after reset is allowed. Sessions must lie within 13:00–14:30; the last reset may extend beyond closing.'),[
    schedule('Place a returning narrator between previously booked interviews.',[['13:00','13:20'],['13:50','14:10']],['13:24','13:25','14:15']),
    schedule('An interpreter-assisted interview must follow the afternoon recording.',[['13:00','13:40']],['13:44','14:10','14:11'])])
add('cooldown',3,dict(duration=7,gap=13,opening='08:00',closing='09:15',close_mode='reset',
    text='A new scanner appointment lasts 7 minutes; existing scans have the stated end times. After each scan the scanner is unavailable for 13 minutes. Every booking must respect recovery on both sides; touching recovery endpoints is allowed. Open 08:00–09:15; the new scan and its recovery must both finish within that window.'),[
    schedule('Fit a calibration scan between two thermographic surveys.',[['08:00','08:07'],['08:40','08:47']],['08:19','08:20','09:00']),
    schedule('After an extended survey, fit a diagnostic scan if any listed start works.',[['08:00','08:38']],['08:50','08:55','08:56'])])
add('cooldown',4,dict(duration=18,gap=12,opening='10:00',closing='12:00',close_mode='session',
    text='Spray-room sessions last 18 minutes, with at least 12 minutes of ventilation between sessions. Existing sessions have their stated durations. Equality at the ventilation boundary is valid. Sessions must be within 10:00–12:00; ventilation after the last session may run later.'),[
    schedule('Find a spray slot for a small glaze batch.',[['10:00','10:18'],['11:00','11:18']],['10:29','10:30','11:30']),
    schedule('A delayed glaze delivery arrives after an extended earlier spray run.',[['10:00','11:12']],['11:23','11:25','11:42'])])
add('cooldown',5,dict(duration=25,gap=15,opening='15:00',closing='17:00',close_mode='reset',
    text='A new sail trial lasts 25 minutes; existing trials use their stated end times. Every trial requires 15 minutes of tunnel cooldown afterward. Any consecutive trials must have that separation. Exact equality is allowed. Open 15:00–17:00; the new trial plus its cooldown must finish by closing.'),[
    schedule('Schedule a reefed-sail trial between two wind-tunnel reservations.',[['15:00','15:25'],['16:20','16:45']],['15:39','15:40','16:00']),
    schedule('Following a full-rig trial, try to fit the storm-sail check before shutdown.',[['15:00','15:50']],['16:04','16:05','16:21'])])
add('cooldown',6,dict(duration=10,gap=6,opening='18:00',closing='19:10',close_mode='session',
    text='Acoustic dome sessions last 10 minutes. Require at least 6 minutes of empty dome time between any two sessions. Existing sessions use their stated end times. Equality is allowed. Sessions must fit within 18:00–19:10, but the final reset may finish later.'),[
    schedule('Find the earliest slot for a chamber ensemble measurement.',[['18:00','18:10'],['18:40','18:50']],['18:15','18:16','18:56']),
    schedule('A late soloist must follow a longer ensemble recording.',[['18:00','18:48']],['18:53','19:00','19:01'])])


def minute(t):
    h,m=map(int,t.split(':'))
    return h*60+m

def time_text(t):
    return f'{t//60:02d}:{t%60:02d}'

def generated_answer(c):
    p,f,m=c['policy'],c['facts'],c['mechanism_id']
    if m=='packs':
        deficit=max(0,f['demand']+f['reserve']-(f['stock']-f['rejected']))
        count=max(p['minimum'],(deficit+p['size']-1)//p['size']) if deficit or p['always'] else 0
        return f'{count} '+('pack' if count==1 else 'packs')
    if m=='rates':
        best=None
        for a in f['candidates']:
            if best is None:
                best=a
                continue
            delta=a['numerator']*best['denominator']-best['numerator']*a['denominator']
            better=delta>0 if p['direction']=='max' else delta<0
            tied=delta==0 and ((a['name']<best['name']) if p['tie']=='alphabetical' else (a['name']>best['name']))
            if better or tied:
                best=a
        return best['name']
    if m=='coordinates':
        x,y=f['point']
        for step in p['ops']:
            a,b=step['matrix'];tx,ty=step['offset']
            x,y=a[0]*x+a[1]*y+tx,b[0]*x+b[1]*y+ty
        return f'({x},{y})'
    feasible=[]
    for t in map(minute,f['starts']):
        end=t+p['duration']
        finish=end+(p['gap'] if p['close_mode']=='reset' else 0)
        if t<minute(p['opening']) or finish>minute(p['closing']):
            continue
        if all(t>=minute(b)+p['gap'] or end+p['gap']<=minute(a) for a,b in f['bookings']):
            feasible.append(t)
    return time_text(min(feasible)) if feasible else 'No listed start fits'


def render(c,rng):
    p,f,m=c['policy'],c['facts'],c['mechanism_id']
    if m=='packs':
        state=f"{p['text']} {c['context']} Demand {f['demand']}; reserve {f['reserve']}; stock {f['stock']}; rejected {f['rejected']}."
        return state,'How many packs must be purchased?',c['distractors']
    if m=='rates':
        candidates=list(f['candidates']);rng.shuffle(candidates)
        c['candidate_order']=[a['name'] for a in candidates]
        detail='; '.join(f"{a['name']}: {a['numerator']}/{a['denominator']}" for a in candidates)
        state=f"{p['text']} {c['context']} Values are {p['numerator']} / {p['denominator']}: {detail}."
        ans=generated_answer(c)
        return state,'Which candidate should be selected?',[a['name'] for a in candidates if a['name']!=ans]
    if m=='coordinates':
        return f"{p['text']} {c['context']}",'What are the final coordinates?',c['distractors']
    detail='; '.join(a+'–'+b for a,b in f['bookings'])
    state=f"{p['text']} {c['context']} Existing sessions: {detail}."
    ans=generated_answer(c)
    return state,'Which listed start is earliest feasible? If none works, choose “No listed start fits”.',[t for t in f['starts']+['No listed start fits'] if t!=ans]


def main():
    rng=random.Random(SEED)
    prepared=[]
    for c in sources:
        state,question,distractors=render(c,rng)
        answer=generated_answer(c)
        assert answer not in distractors
        assert len(set(distractors))==len(distractors)
        prepared.append((c,state,question,answer,distractors))
    # Balance within each arity, then assign the multiset at random, not in a cycle.
    slots={}
    for arity in sorted({len(x[4])+1 for x in prepared}):
        ids=[i for i,x in enumerate(prepared) if len(x[4])+1==arity]
        positions=list(range(arity))*(len(ids)//arity)
        positions+=rng.sample(list(range(arity)),len(ids)%arity)
        rng.shuffle(positions)
        slots.update(zip(ids,positions))
    rows=[]
    for i,(c,state,question,answer,distractors) in enumerate(prepared):
        alternatives=list(distractors);rng.shuffle(alternatives)
        alternatives.insert(slots[i],answer)
        options=[dict(id=f'o{j+1}',text=t) for j,t in enumerate(alternatives)]
        rows.append(dict(schema_version='0.1',id=c['id'],state=state,question=question,options=options,
            target_id=f'o{slots[i]+1}',group_id=c['group_id'],task_family='rule_application',split='validation',
            provenance=dict(kind='programmatic',source=JOB,label_basis='teacher',
                teacher_model=os.environ.get('PI_PROVIDER','unknown')+'/'+os.environ.get('PI_MODEL','unknown'),
                mechanism_id=c['mechanism_id'],policy_instance_id=c['group_id'],usage='validation_only_never_train')))
    lines('source_cases.jsonl',sources)
    # No saved answers or target IDs in the audit input.
    lines('audit_cases.jsonl',[{k:v for k,v in c.items() if k!='distractors'} for c in sources])
    lines('validation.jsonl',rows)
    dump('metadata.json',dict(schema_version='0.1',shard_id='data-d3-seen-rules-v1-geometry',
        teacher=dict(provider=os.environ.get('PI_PROVIDER','unknown'),model_alias=os.environ.get('PI_MODEL','unknown'),immutable_revision=None),
        cost=dict(currency='GBP',additional_spend=0,pending_spend=0),
        generation_settings=dict(seed=SEED,method='Existing agent original authoring; deterministic Python arithmetic, rendering and shuffle; separate-algorithm same-agent audit',
            source_revision='geometry-original-v1',assignment_revision=sha(ROOT/'group_assignments.json'),config_revision=sha(CONFIG),
            harness_sampling=dict(temperature='unknown',top_p='unknown',seed='unknown'),
            hashes={name:sha(ROOT/name) for name in ['generate.py','source_cases.jsonl','audit_cases.jsonl','group_assignments.json']},
            config_path=str(CONFIG),old_rows_inspected=False),
        usage_constraints=dict(usage='validation_only_never_train',permanently_training_excluded=True,
            origin='Original synthetic content authored under existing provider terms; no private records used; no additional redistribution license asserted.'),
        row_counts=dict(validation=48),group_counts=dict(validation=24),mechanism_count=4,policy_count=24,
        limitations=['Development diagnostic, not protected final evaluation.','Mechanism overlap with v2 training is intentional; policies and source cases are newly authored.',
                    'Two cases per policy are dependent; 48 rows are not 48 independent policies.','Never use these cases or derivatives for training or weight updates.',
                    'Labels pending same-agent separate-algorithm consistency audit, not independent authorship or external verification.',
                    'No tokenizer run; parent must audit the 256-token pair budget.']))

if __name__=='__main__':
    main()
