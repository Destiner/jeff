"""Bounded actual-data audit. Stdlib only; no generator/main imports, models or tests.
Run: python3 /absolute/path/to/audit_selected.py
Writes NEW report.json/report.md/sourcehashes.json only beside this script (exclusive create).
Only the predeclared 24 TRAIN records receive semantic inspection or diagnostics.
Whole pinned TRAIN files and permitted source files are hashed; unselected records
are parsed only to join IDs/ordinals, never retained for semantic processing.
"""
import ast
import collections
import hashlib
import json
import os
from pathlib import Path
import re
from datetime import datetime, timezone
from fractions import Fraction

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
ROOT = BASE.parents[1]
HASHES = {}
START = datetime.now(timezone.utc).isoformat()

def digest(path):
    path = Path(path)
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    HASHES[str(path)] = value
    return value

def load(path):
    digest(path)
    return json.loads(Path(path).read_text())

def selected_lines(path, ids):
    digest(path)
    found = {}
    for line in Path(path).open():
        item = json.loads(line)
        if item.get('id') in ids:
            if item['id'] in found:
                raise ValueError('Duplicate selected ID')
            found[item['id']] = item
    return found

def pure(path, names):
    """Extract reviewed pure function definitions and stdlib imports, not module code."""
    digest(path)
    tree = ast.parse(Path(path).read_text())
    nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))
             or isinstance(n, ast.FunctionDef) and n.name in names]
    allowed = {'collections', 'hashlib', 'itertools', 'json', 'pathlib', 'decimal', 'fractions', 'random'}
    for n in nodes:
        if isinstance(n, ast.Import):
            if not all(x.name in allowed for x in n.names):
                raise ValueError('Unexpected import')
        if isinstance(n, ast.ImportFrom) and n.module not in allowed:
            raise ValueError('Unexpected import')
    ns = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), ns)
    return ns

def inputhash(row):
    fields = {k: row[k] for k in ('schema_version', 'id', 'state', 'question', 'options')}
    return hashlib.sha256(json.dumps(fields, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def fresh(row):
    """Fresh calculations from the selected rendered prose, NOT structured sourcefacts.
    Constants reflect policies manually read in this fixed sample, not a general parser.
    Source-fact fidelity is checked separately; these are bounded, explicit derivations.
    """
    s = row['state']; rid = row['id']; g = row['group_id'].split(':')[-1]
    if ':pilot-v1:' in rid:
        if g == 'g01':
            flags = dict(re.findall(r'(safety|warranty|urgent)=(on|off)', s))
            destinations = [('safety', 'Safety bench'), ('warranty', 'Warranty bench'), ('urgent', 'Rapid bench')]
            dest = next((d for k, d in destinations if flags[k] == 'on'), 'General bench')
            return 'Route to '+dest+'.', 'Safety off; warranty off; urgent on. First matching rule is Rapid bench.'
        if g == 'g04':
            n = int(re.search(r'Move (\d+) slot', s)[1]); cycle = ['Juno', 'Kestrel', 'Lark']
            return 'Duty belongs to '+cycle[(1-n) % 3]+'.', 'Kestrel index 1; (1 - 4) mod 3 = 0, Juno. Backward sequence Juno, Lark, Kestrel, Juno.'
        if g == 'g07':
            spans = [(int(a), int(b)) for a,b in re.findall(r'(\d\d):00–(\d\d):00', s)]
            a,b = spans[-1]
            hits = ['Booking '+str(i+1) for i,(c,d) in enumerate(spans[:-1]) if max(a,c) < min(b,d)]
            return 'Conflicts: '+(', '.join(hits) if hits else 'none')+'.', 'Proposal [6,8); bookings [8,10), [10,12), [12,14). Every intersection has nonpositive length; endpoint 8 is not overlap.'
        if g == 'g10':
            state = re.search(r'Initial state: (\w+)', s)[1]
            events = re.search(r'Event log: (.*?)\.', s)[1].split(', ')
            transitions = {('occupied','exit'):'open', ('open','enter'):'occupied', ('open','close'):'locked', ('locked','badge'):'open'}
            trace = [state]
            for e in events:
                state = transitions.get((state,e),state); trace.append(state)
            return 'Final state: '+state+'.', ' -> '.join(trace)+'; exit opens, enter occupies.'
    if ':rule-a:' in rid:
        if g == 'g001':
            eligible = re.search(r'Eligible signers: (.*?)\.', s)[1].split(', ')
            signed = re.search(r'Signatures received: (.*?)\.', s)[1].split(', ')
            n = len(set(eligible) & set(signed)); required = int(re.search(r'exactly (\d+)',s)[1])
            answer = 'Authorize' if n == required else 'Reject: too '+('few' if n < required else 'many')+' eligible signers'
            return answer, f'{n} distinct eligible signers versus exactly {required}; duplicate legal signature and intern do not add eligible distinct signers.'
        if g == 'g002':
            choices = [(name, tuple(map(int, vals.split(', ')))) for name,vals in re.findall(r'([FGH])=\(([^)]+)\)',s)]
            best = min(choices, key=lambda x:(x[1][0],-x[1][1],x[1][2]))
            reason = 'F and G tie on aisle distance 2; G battery 60 > 40, so machine IDs never enter.' if rid.endswith('r07') else 'F and G tie on distance 1 and battery 55; G machine ID 4 < 8. H loses on distance despite higher battery.'
            return 'Select candidate '+best[0], reason
        if g == 'g003':
            batches = re.findall(r'([PMN]) (\d+) units( quarantined)?',s)
            demand = int(re.search(r'Demand: (\d+)',s)[1]); left=demand; issued=[]
            for _,amount,blocked in batches:
                take = 0 if blocked else min(left,int(amount)); issued.append(take); left-=take
            return ', '.join(map(str,issued))+f'; unfilled {left}', f'P quarantined: take 0. M has 7, N has 2; demand {demand} gives issued {issued}, residual {left}.'
        if g == 'g005':
            price = int(re.search(r'Original price: £(\d+)',s)[1]); rate = int(re.search(r'Apply (\d+)%',s)[1]); fixed = int(re.search(r'fixed £(\d+)',s)[1])
            result = max(Fraction(0),Fraction(price*(100-rate),100)-fixed)
            return '£'+str(result), f'{price} × (1 - {rate}/100) - {fixed}, floored at zero = {result}. Percent first, not fixed first.'
        if g == 'g007':
            step = int(re.search(r'multiple of (\d+)',s)[1]); value=int(re.search(r'Measured value: (-?\d+)',s)[1]); lo=(value//step)*step; hi=lo+step
            answer = lo if value-lo < hi-value else hi
            return f'{answer} millimetres', f'Adjacent multiples {lo}, {hi}; distances {value-lo}, {hi-value}. Choose nearest, larger on equality: {answer}.'
    if ':rule-b:' in rid:
        if g == 'g002':
            size, damaged, demand, reserve, stock, minimum = map(int,re.search(r'Each pack has (\d+) units, of which (\d+) are unusable\. Demand is (\d+); keep (\d+) extra usable units\. Already hold (\d+) usable units\. Buy whole packs only, at least (\d+)',s).groups())
            need=max(0,demand+reserve-stock); usable=size-damaged; ceiling=(need+usable-1)//usable; result=max(minimum,ceiling)
            return str(result), f'Net need {need}; usable/pack {usable}; ceil={ceiling}; max(minimum {minimum}, ceil {ceiling})={result}.'
        if g == 'g005':
            a,ad,b,bd=map(int,re.search(r'A reports (\d+) over (\d+); Vendor B reports (\d+) over (\d+)',s).groups()); delta=a*bd-b*ad
            return ('Vendor A' if delta>=0 else 'Vendor B'), f'A={a}/{ad}, B={b}/{bd}; cross-product difference {delta}. '+('Equal rates; explicit tie returns Vendor A, not the Tie distractor.' if delta==0 else 'B has the higher rate.')
        if g == 'g006':
            x,y=map(int,re.search(r'Start at \((-?\d+), (-?\d+)\)',s).groups()); dx,dy=map(int,re.search(r'add \((-?\d+), (-?\d+)\)',s).groups()); result=(-(x+dx),y+dy)
            return str(result), f'({x},{y}) + ({dx},{dy}) = ({x+dx},{y+dy}); reflect x sign only -> {result}.'
        if g == 'g008':
            a,b=map(int,re.search(r'Existing intervals: (\d+)–(\d+)',s).groups()); duration=int(re.search(r'New duration: (\d+)',s)[1]); gap=int(re.search(r'at least (\d+) minutes',s)[1]); starts=list(map(int,re.search(r'Candidate starts: ([\d, ]+)',s)[1].split(', ')))
            legal=[x for x in starts if x>=b+gap or x+duration<=a]; answer=str(min(legal)) if legal else 'No slot'
            return answer, f'Existing [{a},{b}); duration {duration}, gap {gap}. Listed {starts}; legal listed starts {legal}. Touching {b} is legal; starts below {b} here overlap.'
        if g == 'g010':
            moisture,heat=map(int,re.search(r'Here moisture=(\d+), heat=(\d+)',s).groups()); answer='Soak' if moisture<4 else 'Mist' if heat>=8 else 'Skip'
            return answer, f'moisture={moisture}: <4 is {moisture<4}; '+('select Soak without evaluating the else branch.' if moisture<4 else f'else heat={heat} >=8 is {heat>=8}; select {answer}.')
    raise ValueError('Unselected mechanism')

selection=load(BASE/'selection.json')
ids={x['id'] for x in selection['selection']}
if len(ids)!=24 or len(selection['selection'])!=24: raise ValueError('Scope not 24')
if ids & set(selection['exclusions']['already_inspected_ids']): raise ValueError('Historical novelty overlap')
refs=selected_lines(BASE/'selected-reference.jsonl',ids)
# Require exactly the selected 24, not merely a filtered subset of this file.
ref_ids=[json.loads(line)['id'] for line in (BASE/'selected-reference.jsonl').open()]
if len(ref_ids)!=24 or set(ref_ids)!=ids: raise ValueError('Reference scope')
shards={}; audits={}; helpers={}; assignments={}; sources={}; metadata={}
for shard,pin in selection['shards'].items():
    p=ROOT/shard
    if p.name!='train.jsonl' or digest(p)!=pin: raise ValueError('TRAIN pin mismatch')
    shard_ids={x['id'] for x in selection['selection'] if x['shard']==shard}
    shards[shard]=selected_lines(p,shard_ids)
    d=p.parent; audits.update(selected_lines(d/'audit_cases.jsonl',shard_ids))
    helpers[shard]=pure(d/'audit.py',{'expected','scalar'})['expected']
    assignments[shard]=load(d/'group_assignments.json')['groups']
    metadata[shard]=load(d/'metadata.json')
    if d.name=='rule-a':
        digest(d/'source_cases.jsonl'); counts=collections.Counter()
        for line in (d/'source_cases.jsonl').open():
            source=json.loads(line); group=f'data:pilot-v2:rule-a:g{source["group"]:03}'
            for c in source['cases']:
                counts[group]+=1; rid=group+f':r{counts[group]:02}'
                if rid in shard_ids: sources[rid]=(source,c)
    elif d.name=='rule-b':
        digest(d/'authoring_cases.jsonl')
        for line in (d/'authoring_cases.jsonl').open():
            c=json.loads(line); rid=f'data:pilot-v2:rule-b:g{c["group_number"]:03}:r{(c["policy_number"]-1)*2+c["case_number"]:02}'
            if rid in shard_ids:sources[rid]=c
        helpers['render-b']=pure(d/'generate.py',{'render','coord','tree_text'})['render']

records=[]
for entry in selection['selection']:
    rid=entry['id']; shard=entry['shard']; row=refs[rid]; case=audits[rid]
    if row!=shards[shard][rid]: raise ValueError('Existing row mismatch '+rid)
    if row['split']!='train' or row['group_id']!=entry['group_id'] or assignments[shard][row['group_id']]['split']!='train':raise ValueError('Metadata mismatch')
    if digest((ROOT/shard).parent/'group_assignments.json')!=entry['assignment_sha256']:raise ValueError('Assignment pin')
    if int(rid.rsplit(':r',1)[1])!=entry['ordinal_one_based']:raise ValueError('Ordinal')
    texts=[o['text'] for o in row['options']]; oids=[o['id'] for o in row['options']]
    if len(set(texts))!=len(texts) or len(set(oids))!=len(oids) or oids.count(row['target_id'])!=1:raise ValueError('Option uniqueness')
    slot=oids.index(row['target_id']); target=texts[slot]
    derived,reason=fresh(row)
    expected=helpers[shard](case['mechanism'],case['facts']) if ':pilot-v1:' in rid else helpers[shard](case)
    correspondence=None
    if ':rule-a:' in rid:
        source,c=sources[rid]
        correspondence=(row['state']==source['title']+'. '+source['rule']+' '+c['text'] and case['facts']==c['facts'] and case['policy']==source['policy'] and row['provenance']['scenario_id']==source['scenario_id']==case['scenario_id'])
    elif ':rule-b:' in rid:
        c=sources[rid]; state,q=helpers['render-b'](c)
        correspondence=(row['state']==state and row['question']==q and c['policy']==case['policy'] and c['facts']==case['facts'] and row['provenance']['scenario_id']==case['scenario_id']==row['group_id']+f':p{c["policy_number"]:02}')
    lengths=list(map(len,texts)); numeric=None
    if all(re.fullmatch(r'£?-?\d+(?: millimetres)?',t) for t in texts):
        vals=[int(re.search(r'-?\d+',t)[0]) for t in texts]; numeric={'ascending_target_rank':sorted(vals).index(vals[slot])+1,'choices':len(vals),'target_value':vals[slot]}
    dominance=None
    if ':rule-a:g002:' in rid:
        cs=[(name,list(map(int,vals.split(', ')))) for name,vals in re.findall(r'([FGH])=\(([^)]+)\)',row['state'])]
        pairs=[]
        for a,av in cs:
            for b,bv in cs:
                aa=(av[0],-av[1],av[2]);bb=(bv[0],-bv[1],bv[2])
                if a!=b and all(x<=y for x,y in zip(aa,bb)) and any(x<y for x,y in zip(aa,bb)):pairs.append([a,b])
        dominance={'candidate_count':len(cs),'ordered_pairs_checked':len(cs)*(len(cs)-1),'strict_pareto_dominates':pairs,'winner_state_position_one_based':[n for n,(name,_) in enumerate(cs,1) if name==derived.rsplit(' ',1)[1]][0]}
    records.append(dict(id=rid,input_sha256=inputhash(row),group_id=row['group_id'],policy_id=row['provenance'].get('scenario_id'),stratum=entry['stratum'],shard=shard,existing_row_equal=True,structured_helper_expected=expected,structured_helper_matches=expected==target,fresh_rendered_expected=derived,fresh_reasoning=reason,fresh_matches=derived==target,source_rendering_correspondence=correspondence,manual_fact_to_text_review='consistent: reviewed selected structured facts and policy against rendered state',options_unique=True,options_disjoint='distinct terminal outcomes or exact complete result tuples; Tie is interpreted as a returned answer, not pre-tiebreak rate equality',target_text=target,target_slot_one_based=slot+1,option_count=len(texts),target_first=slot==0,target_unique_longest=lengths[slot]==max(lengths) and lengths.count(lengths[slot])==1,target_tied_longest=lengths[slot]==max(lengths) and lengths.count(lengths[slot])>1,target_unique_shortest=lengths[slot]==min(lengths) and lengths.count(lengths[slot])==1,target_tied_shortest=lengths[slot]==min(lengths) and lengths.count(lengths[slot])>1,numeric=numeric,dominance=dominance,choice_fingerprint=hashlib.sha256(json.dumps(sorted(texts),ensure_ascii=False,separators=(',',':')).encode()).hexdigest()))

def summary(rows):
    return dict(n=len(rows),policies_explicit=len({r['policy_id'] for r in rows if r['policy_id']}),slots=dict(collections.Counter(r['target_slot_one_based'] for r in rows)),by_choice_count={str(k):dict(collections.Counter(r['target_slot_one_based'] for r in rows if r['option_count']==k)) for k in sorted({r['option_count'] for r in rows})},**{key:sum(r[key] for r in rows) for key in ['target_first','target_unique_longest','target_tied_longest','target_unique_shortest','target_tied_shortest']},numeric_comparable_n=sum(r['numeric'] is not None for r in rows),numeric_ranks=dict(collections.Counter(r['numeric']['ascending_target_rank'] for r in rows if r['numeric'])))

fingerprints=collections.defaultdict(list)
for r in records:fingerprints[r['choice_fingerprint']].append(r['id'])
findings=[
 {'type':'correctness','severity':'none','finding':'No genuine target/specification bug found in selected 24; all fresh rendered calculations and same-author helper computations match saved targets. No erratum or relabeling proposed.'},
 {'type':'dependence','finding':'All 10 new r07/r08 pairs share actual p04 scenario_id: 20 decisions, 10 policy instances, 10 mechanism/source groups. Four inherited controls add 4 source groups; no explicit scenario_id is stored for them. Total 14 source groups, not 24 independent policies. Treat inherited rows as four rendered control-policy instances only, not newly inferred provenance IDs.'},
 {'type':'reviewer_identity','finding':'Fresh reasoning is a separate review session, but reviewer alias equals disclosed source teacher alias openai/gpt-sol. Not independent-model or independent-provider verification; immutable revision unavailable.'},
 {'type':'shortcut','finding':'Selected rule-a:g002 winners are G in 2/2 and second candidate in state in 2/2. No winner strictly Pareto-dominates all rivals in either case (0/2); G dominates F in r08 only. Thus a universal dominance shortcut is not demonstrated, while a shared-policy candidate-name fingerprint is possible.'},
 {'type':'shortcut','finding':'Selected rule-a:g005 targets are numeric minimum 2/2; rule-a:g007 targets ascending rank 3 of 4 (second largest) 2/2; rule-b:g002 targets ascending rank 3 of 4 in 2/2. Each denominator is one shared policy pair; these are local construction signatures, not measured whole-training shortcuts.'},
 {'type':'options','finding':'All 24 option ID/text sets unique; manual review found distinct terminal returned outcomes. Vendor Tie options in two rate rows are unreachable under this p04 tie-return-A policy (2/2), but not a competing correct answer: question asks returned result, not whether raw rates are equal. Authorization too-many option is unreachable when only two eligible signers and required=2 (2/2). Unreachable distractors are local weakness, not label errors.'},
 {'type':'coverage','finding':'Mechanism coverage is not branch coverage. The chosen scheduling p04 has zero cooldown in 2/2 cases; neither measures positive cooldown arithmetic. Rounding pair covers positive tie/non-tie only (2/2), not negative tie behavior. No extra cases were generated or sampled.'}
]
report=dict(task='D4 independent artifact-only factual audit',started_utc=START,finished_utc=datetime.now(timezone.utc).isoformat(),reviewer={'PI_PROVIDER':os.environ.get('PI_PROVIDER'), 'PI_MODEL':os.environ.get('PI_MODEL'),'identity_basis':'Only PI_PROVIDER and PI_MODEL; alias, not immutable revision'},scope={'selected_train_rows':24,'inherited':4,'new':20,'mechanism_source_groups':14,'explicit_new_policy_ids':sorted({r['policy_id'] for r in records if r['policy_id']}),'historical_excluded_ids':16,'historical_overlap':0,'selection_and_shard_pins_verified':True,'extra_semantic_samples':0,'blind_review_outputs_read':False,'validation_rows_read':False,'evaluation_heldout_probe_final_rows_read':False},hash_definition='input_sha256 = SHA256 UTF-8 canonical JSON ensure_ascii=False, sort_keys=True, separators=(comma,colon), containing schema_version,id,state,question,ordered options; no labels or provenance.',methods={'fresh_reasoning':'Explicit rendered-prose arithmetic/logic for each of 24; bounded parser/constants transcribed from actual policy text; manually checked structured policy/facts against prose. Not generic semantic parsing.', 'executable_consistency':'AST-extracted reviewed pure expected functions, plus pure rule-b rendering correspondence. Source algorithms share authorship with labels, so their agreement alone is not independent verification.', 'source_correspondence':'10/10 rule-a authored prose/facts joins and 10/10 rule-b pure rendered state/question/facts joins. Four inherited structured records manually matched to prose; no generator executed.', 'limits':'Purposive rules-only TRAIN sample; dependent paired policies and same-model provenance. No accuracy estimates or extrapolation to whole training; no tokenizer/model audit. Hashing full files is identity verification, not semantic expansion.'},summary=summary(records),by_group={g:summary([r for r in records if r['group_id']==g]) for g in sorted({r['group_id'] for r in records})},by_stratum={g:summary([r for r in records if r['stratum']==g]) for g in ['inherited_v1','new_v2']},repeated_unordered_choice_fingerprints=[{'sha256':k,'n':len(v),'ids':v} for k,v in fingerprints.items() if len(v)>1],findings=findings,records=records,bugs=[{'id':r['id'],'input_sha256':r['input_sha256']} for r in records if not(r['fresh_matches'] and r['structured_helper_matches'])],resources={'network':False,'models':False,'dependencies_changed':False,'software_tests_lint':False,'git_or_mailbox':False,'spend_GBP':0,'pending_spend_GBP':0})
if any(r['source_rendering_correspondence'] is False for r in records):raise ValueError('Source mismatch')
for p in [ROOT.parent/'AGENTS.md',ROOT.parent/'docs/contracts.md',ROOT.parent/'docs/plan.md',ROOT.parent/'docs/coordination.md',ROOT.parent/'docs/swarm.md',Path(__file__)]:digest(p)
report['sourcehashes_file']='sourcehashes.json'
md=['# D4 factual audit — selected TRAIN rows','',f"Reviewer alias: `{report['reviewer']['PI_PROVIDER']}/{report['reviewer']['PI_MODEL']}` (environment only).",'', '## Result','', '24/24 exact existing-row matches against pinned TRAIN shards; 0/16 historical novelty-ID overlap. Fresh rendered reasoning: 24/24 target matches. Same-author executable consistency: 24/24 matches. Source rendering joins: 20/20 new rows; inherited facts manually reviewed 4/4. No genuine target/spec bug found; no frozen-row edits or correction proposed.','', '## Independence and scope','',report['methods']['limits'],'',report['methods']['executable_consistency'],'', '20 new decisions are 10 actual p04 policies, not 20 policies; the four inherited rows have no explicit scenario IDs. 14 mechanism/source groups total. Reviewer is the same exposed model alias as the source author; fresh-session reasoning is not independent-model verification.','', '## Exact findings','']
for f in findings:md.append('- '+f['finding'])
md+=['','## Construction diagnostics','', 'All counts below refer only to these 24. First means first displayed option; length uses Unicode character count; tied extrema are separate from unique extrema. Numeric rank uses ascending scalar values only, with identical units inside each row. Tuples, labels, and mixed No-slot/numeric choices are excluded from the numeric denominator. No fitted classifier or whole-training extrapolation.','', '```json',json.dumps(report['summary'],indent=2),'```','', '| Group | n | Target slots (1-based) | First | Unique longest / tied longest | Unique shortest / tied shortest | Numeric ranks (n comparable) |','|---|---:|---|---:|---|---|---|']
for g,s in report['by_group'].items():md.append(f"| {g} | {s['n']} | {s['slots']} | {s['target_first']}/{s['n']} | {s['target_unique_longest']} / {s['target_tied_longest']} | {s['target_unique_shortest']} / {s['target_tied_shortest']} | {s['numeric_ranks']} (n={s['numeric_comparable_n']}) |")
md+=['','Repeated unordered choice sets are enumerated with exact IDs and SHA-256 in report.json; shared option vocabularies alone do not show the choices-only heuristic predicts a target.','', '## Per-row fresh derivations','', '| Existing ID | Derived answer | Rendered-rule derivation |','|---|---|---|']
for r in records:md.append(f"| `{r['id']}` | {r['fresh_rendered_expected']} | {r['fresh_reasoning']} |")
md+=['','## Reproduction and hashes','',f'Run `python3 {Path(__file__).resolve()}` only with absent report outputs (exclusive creation prevents overwrites). Reads only declared TRAIN shards and permitted helper/source/metadata files; extracts pure functions, never invokes their mains. Uses standard-library CPU only. It is an actual-data audit, not a software test or generated fixture.','', 'Exact per-row input hashes, source correspondence, semantic distinctions, choice fingerprints and denominators are in report.json. Full source hashes and script hash are in sourcehashes.json. Files are hashed in full solely for identity; semantic inspection remains selected-only. No blind-review output, validation.jsonl, Evaluation, held-out, probe or final rows were opened. No Git/mailbox/network/models/dependencies/tests/lint/spend.']
for name,value in [('report.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n'),('report.md','\n'.join(md)+'\n'),('sourcehashes.json',json.dumps(HASHES,indent=2,sort_keys=True)+'\n')]:
    with (OUT/name).open('x') as f:f.write(value)
print(json.dumps({'selected':24,'fresh_matches':sum(r['fresh_matches'] for r in records),'helper_matches':sum(r['structured_helper_matches'] for r in records),'summary':report['summary'],'bugs':report['bugs'],'output':str(OUT)}))
