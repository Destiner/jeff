"""Bounded deterministic distractor repair. Standard library only; no audit main.
The fully inspected parent's expected/correspondence functions are the only audit calls.
"""
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

OUT = Path(__file__).resolve().parent
PARENT = OUT.with_name('geometry-r2')
PLAN_HASH = 'a95f2b13f047f993353e5dfa194e5e7f8ee5966b957fc88804be5848576de061'
# Replacement choices selected only after rank-plan.json was frozen.
REPLACEMENTS = {
    'p01:c01': {'10:00': ('09:12', 'Omit the preceding booking’s 8-minute cooldown; use its session end.')},
    'p02:c01': {'13:24': ('13:26', 'Treat allowed equality as strict and move one minute past reset; this misses reset before the next booking.')},
    'p03:c02': {'08:56': ('08:38', 'Omit the preceding survey’s 13-minute recovery and use its stated end.')},
    'p04:c01': {'10:29': ('10:31', 'Treat allowed equality as strict and move one minute later; this misses ventilation before the next booking.')},
    'p05:c01': {'16:00': ('15:25', 'Omit the preceding trial’s 15-minute cooldown and use its session end.')},
    'p05:c02': {'16:04': ('16:20', 'Use the latest legal start at closing minus duration minus cooldown; feasible but not earliest listed.')},
    'p06:c02': {'18:53': ('19:04', 'Subtract reset (6 minutes), rather than session duration (10 minutes), from closing.')},
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def dump(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def minutes(t):
    assert re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', t), t
    h,m=map(int,t.split(':'))
    return 60*h+m

def clock(n):
    return f'{n//60:02d}:{n%60:02d}'

def violations(case, text):
    """Explain constraints directly, separately from the imported set-based solver."""
    t=minutes(text);p=case['policy'];d=p['duration'];g=p['gap']
    issues=[]
    if t<minutes(p['opening']):
        issues.append('starts before opening '+p['opening'])
    finish=t+d+(g if p['close_mode']=='reset' else 0)
    if finish>minutes(p['closing']):
        issues.append(('session plus recovery' if p['close_mode']=='reset' else 'session')+
                      ' ends '+clock(finish)+' after closing '+p['closing'])
    for a,b in case['facts']['bookings']:
        if not (t>=minutes(b)+g or t+d+g<=minutes(a)):
            issues.append(f'conflicts with {a}–{b}: start must be at least {clock(minutes(b)+g)} after it, '
                          f'or session plus reset must finish by {a} before it (would finish {clock(t+d+g)})')
    return issues

def diagnostics(rows, cases):
    result={}
    for name, subset in [('all',rows)]+[(m,[r for r in rows if cases[r['id']]['mechanism_id']==m]) for m in ('packs','rates','coordinates','cooldown')]:
        slots=defaultdict(Counter);length=Counter();none_slots=Counter();none_targets=0
        for row in subset:
            opts=row['options'];texts=[o['text'] for o in opts]
            pos=next(i for i,o in enumerate(opts) if o['id']==row['target_id']);answer=texts[pos]
            slots[len(opts)][pos+1]+=1
            lens=list(map(len,texts))
            length['shortest_first_tie_hits']+=pos==min(range(len(opts)),key=lambda i:lens[i])
            length['longest_first_tie_hits']+=pos==max(range(len(opts)),key=lambda i:lens[i])
            length['shortest_including_ties']+=len(answer)==min(lens)
            length['longest_including_ties']+=len(answer)==max(lens)
            length['strict_shortest']+=all(len(answer)<len(t) for t in texts if t!=answer)
            length['strict_longest']+=all(len(answer)>len(t) for t in texts if t!=answer)
            for i,t in enumerate(texts):
                if t=='No listed start fits': none_slots[i+1]+=1
            none_targets+=answer=='No listed start fits'
        result[name]={'rows':len(subset),'target_slots_by_arity':{str(k):dict(v) for k,v in slots.items()},
                      'length':dict(length),'none_option_slots':dict(none_slots),'none_target_count':none_targets}
    cool=[r for r in rows if cases[r['id']]['mechanism_id']=='cooldown']
    ranks=Counter();hits=Counter();distances=[]
    for r in cool:
        answer=next(o['text'] for o in r['options'] if o['id']==r['target_id'])
        times=sorted([o['text'] for o in r['options'] if o['text']!='No listed start fits'],key=minutes)
        for rank,t in enumerate(times,1):
            hits[{1:'earliest',2:'second',3:'latest'}[rank]]+=t==answer
        if answer!='No listed start fits': ranks[times.index(answer)+1]+=1
        distances.append({'id':r['id'],'sorted_times':times,'target':answer,
                          'adjacent_minute_gaps':[minutes(b)-minutes(a) for a,b in zip(times,times[1:])]})
    result['cooldown'].update({'clock_prior_hits_of_12':dict(hits),'non_none_numerical_target_ranks':dict(ranks),
                              'clock_gap_details':distances,'always_none_hits_of_12':1})
    return result

def main():
    assert OUT.name=='geometry-r3' and PARENT.name=='geometry-r2'
    plan_bytes=(OUT/'rank-plan.json').read_bytes()
    assert sha(plan_bytes)==PLAN_HASH
    plan=json.loads(plan_bytes)
    parent={n:(PARENT/n).read_bytes() for n in plan['parent_hashes']}
    assert {n:sha(b) for n,b in parent.items()}==plan['parent_hashes']
    author={k:os.environ.get(k) for k in ('PI_MODEL','PI_PROVIDER')}
    assert author==plan['author']
    data={n:[json.loads(x) for x in parent[n].splitlines()] for n in ('source_cases.jsonl','audit_cases.jsonl','validation.jsonl')}
    old=deepcopy(data)
    changes=[]
    for name, rows in data.items():
        lines=parent[name].decode().splitlines(keepends=True)
        for i,r in enumerate(rows):
            suffix=r['id'].split(':cooldown:')[-1]
            replacements=REPLACEMENTS.get(suffix,{}) if ':cooldown:' in r['id'] else {}
            before=deepcopy(r)
            if name=='validation.jsonl':
                for opt in r['options']:
                    if opt['text'] in replacements:
                        assert opt['id']!=r['target_id']
                        opt['text']=replacements[opt['text']][0]
                restored=deepcopy(r);restored['options']=before['options']
                assert restored==before
            else:
                r['facts']['starts']=[replacements.get(t,(t,''))[0] for t in r['facts'].get('starts',[])] if replacements else r['facts'].get('starts',[])
                if 'starts' not in before['facts']: r['facts'].pop('starts',None)
                if replacements and 'distractors' in r:
                    r['distractors']=[replacements.get(t,(t,''))[0] for t in r['distractors']]
                restored=deepcopy(r);restored['facts']=before['facts']
                if 'distractors' in before: restored['distractors']=before['distractors']
                assert restored==before
                assert r['policy']==before['policy']
                if replacements: assert r['facts']['bookings']==before['facts']['bookings']
            if r!=before:
                assert replacements
                # Preserve each row's original JSON formatting; touch only quoted clock literals.
                for a,(b,reason) in replacements.items():
                    assert json.dumps(a) in lines[i]
                    lines[i]=lines[i].replace(json.dumps(a),json.dumps(b))
                assert json.loads(lines[i])==r
                changes.append({'file':name,'id':r['id'],'before_starts':before.get('facts',{}).get('starts'),
                                'after_starts':r.get('facts',{}).get('starts'),
                                'replacements':[{'old':a,'new':b,'construction':why} for a,(b,why) in replacements.items()]})
            else:
                assert r==before
        (OUT/name).write_bytes(''.join(lines).encode())
    for name in ('audit.py','group_assignments.json'):
        (OUT/name).write_bytes(parent[name])
        assert (OUT/name).read_bytes()==parent[name]
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('r3_inspected_pure_audit',OUT/'audit.py')
    audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    sources={r['id']:r for r in data['source_cases.jsonl']}
    cases={r['id']:r for r in data['audit_cases.jsonl']}
    rows=data['validation.jsonl'];checks=[];rationales=[]
    assert len(rows)==len(cases)==len(sources)==48
    assignments=json.loads(parent['group_assignments.json'])['groups']
    assert len(assignments)==24
    for i,row in enumerate(rows):
        prev=old['validation.jsonl'][i];c=cases[row['id']];source=sources[row['id']]
        assert row['id']==prev['id']
        assert c=={k:v for k,v in source.items() if k!='distractors'}
        answer=audit.expected(c)
        assert answer==next(o['text'] for o in prev['options'] if o['id']==prev['target_id'])
        assert [o['text'] for o in row['options'] if o['id']==row['target_id']]==[answer]
        assert sum(o['text']==answer for o in row['options'])==1
        assert len({o['text'] for o in row['options']})==len(row['options'])
        assert [o['id'] for o in row['options']]==[o['id'] for o in prev['options']]
        assert row['target_id']==prev['target_id']
        assert {k:v for k,v in row.items() if k!='options'}=={k:v for k,v in prev.items() if k!='options'}
        audit.correspondence(c,row)
        group=row['group_id'];a=assignments[group]
        assert c['group_id']==row['provenance']['policy_instance_id']==a['policy_instance_id']==group
        assert a['mechanism_id']==row['provenance']['mechanism_id']==c['mechanism_id']
        assert a['split']==row['split']=='validation' and a['policy_domain']==c['policy_domain']
        if 'distractors' in source: assert set(source['distractors'])=={o['text'] for o in row['options'] if o['id']!=row['target_id']}
        if c['mechanism_id']!='cooldown':
            for name in data: assert data[name][i]==old[name][i]
        else:
            times=c['facts']['starts'];assert len(times)==len(set(times))==3
            for t in times: minutes(t)
            rank=None if answer=='No listed start fits' else sorted(times,key=minutes).index(answer)+1
            assert rank==plan['assignment'][row['id']]
            assert (answer=='No listed start fits')==all(violations(c,t) for t in times)
            for opt in row['options']:
                if opt['id']==row['target_id']: continue
                t=opt['text']
                if t=='No listed start fits':
                    assert not violations(c,answer)
                    why='False: the offered '+answer+' satisfies all booking, reset and closing constraints.'
                    feasible=None
                else:
                    issues=violations(c,t);feasible=not issues
                    if not issues:
                        assert answer!='No listed start fits' and minutes(t)>minutes(answer)
                        why='Feasible but later than offered '+answer+'; the question asks earliest listed, not any feasible start.'
                    else: why='Infeasible: '+'; '.join(issues)+'.'
                replacement=REPLACEMENTS.get(row['id'].split(':cooldown:')[1],{})
                construction=next((v[1] for v in replacement.values() if v[0]==t),'Retained parent alternative; constraint rationale recomputed.')
                rationales.append({'id':row['id'],'option_id':opt['id'],'text':t,'feasible':feasible,'why_wrong':why,'construction':construction})
        checks.append({'id':row['id'],'expected_answer':answer,'target_match':True,'text_correspondence':True})
    groups=Counter(r['group_id'] for r in rows)
    assert len(groups)==24 and set(groups.values())=={2} and set(groups)==set(assignments)
    assert len(changes)==21
    before_d=diagnostics(old['validation.jsonl'],{c['id']:c for c in old['audit_cases.jsonl']})
    after_d=diagnostics(rows,cases)
    assert after_d['cooldown']['non_none_numerical_target_ranks']=={1:4,2:4,3:3}
    dump('change-map.json',{'revision':'geometry-r3','parent':str(PARENT),'rank_plan_sha256':PLAN_HASH,
         'scope':'Incorrect cooldown clock options and faithful corresponding facts.starts/source distractors only',
         'logical_cases_changed':7,'wrong_option_texts_changed':7,'changes':changes,
         'facts_delta_disclosure':'Offered starts are source facts and have changed in source_cases and audit_cases. Policy parameters, bookings, all other facts and contexts are fixed.',
         'preserved':'All state/question/target texts, target IDs/slots, IDs/groups/splits, arities, none text/slot, row provenance; all 36 non-cooldown rows and r2 packing clarification.',
         'byte_identical_helpers_and_assignments':['audit.py','group_assignments.json']})
    dump('distractor-rationales.json',{'coverage':'All 36 wrong cooldown options, including retained options and none choices','options':rationales})
    dump('diagnostics.json',{'definitions':'Character lengths; first displayed option breaks length ties. Clock priors ignore none and choose numerical rank 1/2/3. None-case counts as miss for every clock prior.','before':before_d,'after':after_d})
    limits=[
        'Same-agent pure solver and text reconstruction consistency, not independent verification or authorship.',
        'Known reviewer-exposed quality issue repaired before publication; this is not untouched validation. No model predictions informed repair.',
        'Balanced marginal clock ranks do not establish shortcut freedom; paired templates, boundary times, minute-neighbor cues, equal-length times versus long none text, target slots and rare none targets remain.',
        'Some later choices are feasible but wrong only because an earlier listed start works; rank-one choices at tight between-booking boundaries can have only infeasible later alternatives.',
        'No new cases, policy expansion, targets, model calls or generation after this bounded repair. Freeze is final for this task.',
        'No tests, lint, build, tokenizer, model inference, network, API calls, Git, mailbox or spending performed. Validation-only, never train.'
    ]
    dump('validation_report.json',{'schema_version':'0.1','revision':'geometry-r3','audit_kind':'same_agent_inspected_pure_functions_not_independent',
         'rows_checked':48,'target_checks_passed':48,'text_checks_passed':48,'policy_groups':24,
         'mechanisms':dict(Counter(c['mechanism_id'] for c in cases.values())),
         'failure_count':0,'failures':[],'cases':checks,'limitations':limits})
    (OUT/'generation_review.md').write_text(
        '# Geometry r3 — bounded final cooldown repair\n\n'
        'Rank assignment was frozen by ID in rank-plan.json before replacement selection (SHA-256 '+PLAN_HASH+'). '
        'Seven incorrect clock alternatives in seven cases changed; the other five cooldown cases retain their options. '
        'All 12 cooldown cases were checked, including the unchanged none-target case. '
        'Offered starts ARE source facts: matching facts.starts were changed in both source and audit records; there are no cooldown source distractor fields in this parent. '
        'The change map documents every delta. All policy/booking numerical facts, exact targets, state/context/question, option IDs, none slots, row provenance and all 36 other rows remain fixed. '
        'The r2 final-reserve packing clarification remains intact. Parent formatting is preserved outside the seven changed clock strings in each dataset.\n\n'
        'The fully inspected audit.py and group_assignments.json are byte-identical. Only pure expected and correspondence were called; overwrite main was never called. '
        '48/48 expected targets and 48/48 full rendered state/question correspondences passed. '
        'The additional direct interval constraint explanations cover all 36 wrong cooldown options, not just edited ones. '
        'No wrong earlier time is feasible; later feasible choices lose on earliest-listed wording.\n\n'
        '## Choice-only diagnostics\n\n'
        'Before: earliest/second/latest clock priors hit 0/11/0 of 12. After: **4/4/3 of 12** (the one none target loses under all clock priors). '
        'All 11 non-none numerical ranks are therefore 4/4/3. None is offered 12/12 and correct 1/12. '
        'All target-slot and length diagnostics are unchanged because every replacement remains a five-character clock. '
        'Per-mechanism and total length/slot/none distributions and adjacent clock gaps are in diagnostics.json.\n\n'
        '## Residual hints and limits\n\n'+'\n'.join('- '+s for s in limits)+'\n\n'
        'Actual session author: '+json.dumps(author)+'. Additional/pending cost: GBP 0/0. '
        'All allowed parent files are hashed before and after; freeze.json records new output digests. No independence or shortcut-free claim.\n')
    metadata=json.loads(parent['metadata.json'])
    metadata.update({'shard_id':'data-d3-seen-rules-v1-geometry-r3','job_id':'data-d3-seen-rules-v1-geometry-r3',
        'revision_author':author,'parent':str(PARENT),'parent_hashes':plan['parent_hashes'],
        'parent_lineage':{'direct_parent':'geometry-r2','inherited_parent':json.loads(parent['metadata.json'])['parent'],'review_trigger':'second-earliest clock prior hit 11/12 including all 11 non-none targets'},
        'reason':'Bounded incorrect cooldown offered-start repair; source starts facts explicitly updated; no relabeling.',
        'field_scope':{'validation.jsonl':'incorrect cooldown options[].text','audit_cases.jsonl':'cooldown facts.starts','source_cases.jsonl':'cooldown facts.starts and source distractors if present'},
        'cost':{'currency':'GBP','additional_spend':0,'pending_spend':0},
        'row_counts':{'validation':48},'group_counts':{'validation':24},'policy_count':24,'limitations':limits})
    outputs=[f.name for f in sorted(OUT.iterdir()) if f.is_file() and f.name not in ('metadata.json','freeze.json')]
    metadata['generation_settings']={'method':'Deterministic bounded repair from hashed r2 parents and preselected rank plan; no model predictions',
        'source_revision':'geometry-r3','script':'revise.py','hashes':{n:sha((OUT/n).read_bytes()) for n in outputs}}
    dump('metadata.json',metadata)
    assert {n:sha((PARENT/n).read_bytes()) for n in parent}==plan['parent_hashes']
    assert sha((OUT/'rank-plan.json').read_bytes())==PLAN_HASH
    files={f.name:sha(f.read_bytes()) for f in sorted(OUT.iterdir()) if f.is_file() and f.name!='freeze.json'}
    dump('freeze.json',{'revision':'geometry-r3','final':True,'sha256':files,'parent_files_unchanged':True,
         'additional_generation_permitted':False,'cost_GBP':{'additional':0,'pending':0},'independence_claim':False})
    for f in OUT.iterdir():
        if f.is_file(): f.chmod(0o444)
    OUT.chmod(0o555)
    print(json.dumps({'output':str(OUT),'rows':48,'policies':24,'changed_cases':7,'clock_rank_counts':{1:4,2:4,3:3},'parent_unchanged':True,'frozen':True}))

if __name__=='__main__':
    main()
