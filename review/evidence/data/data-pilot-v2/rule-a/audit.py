"""Same-agent, separately implemented semantic and structural dataset audit.
expected() uses only structured policy/facts, never saved target or generator code.
Not a software test suite; invoke directly for CPU dataset validation.
"""
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def scalar(value):
    value=Decimal(str(value))
    return format(value.normalize(),'f')

def expected(case):
    g=case['mechanism_number'];p=case['policy'];f=case['facts']
    if g==1:
        counted=[]
        for signer in f['signed']:
            if signer in p['eligible'] and signer not in counted:counted.append(signer)
        if len(counted)<p['required']:return 'Reject: too few eligible signers'
        if len(counted)>p['required']:return 'Reject: too many eligible signers'
        return 'Authorize'
    if g==2:
        pool=f['candidates'][:]
        for index,direction in enumerate(p['directions']):
            best=(min if direction==1 else max)(candidate[1][index] for candidate in pool)
            pool=[candidate for candidate in pool if candidate[1][index]==best]
        if len(pool)!=1:raise ValueError('Ranking lacks unique winner')
        return 'Select candidate '+pool[0][0]
    if g==3:
        # Allocate individual demand units through a receipt-ordered inventory.
        inventory=[];issued=[0]*len(p['batches'])
        for index,(name,count) in enumerate(p['batches']):
            if name not in p['skip']:inventory.extend([index]*count)
        for index in inventory[:f['demand']]:issued[index]+=1
        shortage=max(0,f['demand']-len(inventory))
        return ', '.join(str(n) for n in issued)+f'; unfilled {shortage}'
    if g==4:
        # Compose the two affine maps algebraically rather than executing stages.
        a,b=map(lambda x:Decimal(str(x)),p['first']);c,d=map(lambda x:Decimal(str(x)),p['second'])
        result=Decimal(str(f['value']))*(a*c)+(b*c+d)
        return scalar(result)+' '+p['unit']
    if g==5:
        price=Decimal(str(f['price']));fixed=Decimal(str(p['fixed'])) if f['price']>=p['threshold'] else Decimal(0)
        rate=Decimal(str(p['percent']))/100
        # Account for each amount removed, explicitly clipping each removal.
        if p['order']=='percent_first':
            percentage_removed=price*rate
            fixed_removed=min(price-percentage_removed,fixed)
        else:
            fixed_removed=min(price,fixed)
            percentage_removed=(price-fixed_removed)*rate
        return '£'+scalar(price-percentage_removed-fixed_removed)
    if g==6:
        credits=[]
        for units in f['days']:
            amount=units*p['rate']
            if p['eligible'] is not None and units<p['eligible']:amount=0
            if amount>p['cap']:amount=p['cap']
            credits.append(amount)
        result=sum(credits)
        if p['ceiling'] is not None and result>p['ceiling']:result=p['ceiling']
        return str(result)+' credits'
    if g==7:
        x=Decimal(str(f['value']));step=Decimal(str(p['step']))
        lower=(x/step).to_integral_value(rounding=ROUND_FLOOR)*step;upper=lower+step
        answer=lower if x-lower<upper-x else upper
        return scalar(answer)+' '+p['unit']
    if g==8:
        segments=[]
        for ch in f['stream']:
            if segments and segments[-1][0]==ch:segments[-1][1]+=1
            else:segments.append([ch,1])
        encoded=[]
        for ch,count in segments:
            if p['fmt']=='sc':s=ch+str(count)
            elif p['fmt']=='cs':s=str(count)+ch
            elif p['fmt']=='colon':s=ch+':'+str(count)
            else:s=ch+'('+str(count)+')'
            encoded.append(s)
        return p['sep'].join(encoded)
    if g==9:
        remaining=list(enumerate(f['jobs']));elapsed=p['start']
        while remaining:
            selected=min(range(len(remaining)),key=lambda j:(remaining[j][1][2],remaining[j][0]))
            _,(label,duration,deadline)=remaining.pop(selected)
            elapsed=elapsed+duration+p['setup']
            if elapsed>deadline:return 'Infeasible: '+label+' first misses'
        return 'Feasible: all jobs meet deadlines'
    if g==10:
        missing=False
        for permission in f['request']:
            if permission in f['vetoes']:return 'Deny: requested permission vetoed'
            if not any(permission in p['grants'][role] for role in f['roles']):missing=True
        return 'Deny: requested permission ungranted' if missing else 'Allow the full request'
    if g==11:
        # Dynamic-programming suffix lengths of common contiguous runs.
        a,b=f['a'],f['b'];table=[[0]*(len(b)+1) for _ in range(len(a)+1)];best=''
        for i,x in enumerate(a,1):
            for j,y in enumerate(b,1):
                if x==y:
                    table[i][j]=table[i-1][j-1]+1
                    candidate=a[i-table[i][j]:i]
                    tie_better=(candidate<best) if p['tie']=='asc' else (candidate>best)
                    if len(candidate)>len(best) or (len(candidate)==len(best) and tie_better):best=candidate
        return best
    if g==12:
        # Stack of expected closers, not openers.
        closers=[];mapping={'(':')','[':']','{':'}'}
        for c in f['sequence']:
            if c in mapping:closers.append(mapping[c])
            elif c in ')]}':
                if not closers:return 'Invalid: closing with no opener'
                wanted=closers[-1]
                if c!=wanted:return 'Invalid: wrong closing type'
                del closers[-1]
        return 'Invalid: unclosed opener' if closers else 'Valid: balanced and properly nested'
    if g==13:
        left=f['left'][:];right=f['right'][:];result=[]
        while left or right:
            if not right:queue=left
            elif not left:queue=right
            elif left[0][1]<right[0][1]:queue=left
            elif left[0][1]>right[0][1]:queue=right
            else:queue=left if p['tie_left'] else right
            result.append(queue.pop(0)[0])
        return ' '.join(result)
    if g==14:
        failing=[]
        for i,(positions,required) in enumerate(p['constraints'],1):
            parity=0
            for pos in positions:parity^=int(f['vector'][pos-1])
            if parity!=required:failing.append(str(i))
        return 'Fail constraints '+', '.join(failing) if failing else 'Pass all constraints'
    if g==15:
        # Find middle order statistics by counting, without sorting samples.
        medians={}
        for name,values in f['candidates']:
            middle=[]
            for rank in [(len(values)-1)//2,len(values)//2]:
                for value in set(values):
                    below=sum(x<value for x in values);equal=sum(x==value for x in values)
                    if below<=rank<below+equal:middle.append(Decimal(str(value)));break
            medians[name]=sum(middle)/2
        winners=[name for name,value in medians.items() if value==max(medians.values())]
        return 'Select candidate '+(min if p['tie']=='asc' else max)(winners)
    raise ValueError(g)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def validate():
    rows=[];failures=[];counts={};assignments=json.loads((ROOT/'group_assignments.json').read_text())['groups']
    for split in ('train','validation'):
        subset=[json.loads(line) for line in (ROOT/(split+'.jsonl')).read_text().splitlines()];counts[split]=len(subset)
        rows+=subset
        if len(subset)!=(200 if split=='train' else 40):failures.append('Wrong split count '+split)
        if any(r['split']!=split for r in subset):failures.append('Split/file disagreement')
    cases=[json.loads(line) for line in (ROOT/'audit_cases.jsonl').read_text().splitlines()]
    audits={c['id']:c for c in cases}
    policies=[json.loads(line) for line in (ROOT/'source_cases.jsonl').read_text().splitlines()]
    source_by_id={};source_indexes=Counter()
    for policy in policies:
        group=f"data:pilot-v2:rule-a:g{policy['group']:03}"
        for case in policy['cases']:
            source_indexes[group]+=1
            source_by_id[group+f':r{source_indexes[group]:02}']=(policy,case)
    ids=set();states={};canonical={};group_splits=defaultdict(set);positions=defaultdict(Counter);lengths=defaultdict(Counter);matches=0;semantic_failures=[];scenario_rows=Counter();group_rows=Counter();word_counts=[]
    scenarios_by_split=defaultdict(set);answer_text_counts=defaultdict(Counter);candidate_state_positions=defaultdict(Counter);source_fidelity_matches=0
    for r in rows:
        rid=r['id'];group=r['group_id'];group_rows[group]+=1
        if rid in ids:failures.append('Duplicate ID '+rid)
        ids.add(rid)
        if r['schema_version']!='0.1' or r['task_family']!='rule_application':failures.append('Schema/family '+rid)
        if r['split'] not in ('train','validation'):failures.append('Unexpected split '+rid)
        if not isinstance(r['state'],str) or not r['question'].strip():failures.append('Missing text '+rid)
        if not 2<=len(r['options'])<=6:failures.append('Option count '+rid)
        option_ids=[o['id'] for o in r['options']]
        option_text=[o['text'] for o in r['options']]
        if any(not isinstance(x,str) or not x.strip() for x in option_ids+option_text):failures.append('Empty option '+rid)
        if len(set(option_ids))!=len(option_ids) or len(set(option_text))!=len(option_text):failures.append('Duplicate option '+rid)
        if option_ids.count(r['target_id'])!=1:failures.append('Target membership '+rid);continue
        if not rid.startswith(group+':r'):failures.append('ID namespace '+rid)
        if group not in assignments or assignments[group]['split']!=r['split']:failures.append('Assignment '+rid)
        group_splits[group].add(r['split'])
        if r['state'] in states:failures.append('Exact duplicate state '+rid+' '+states[r['state']])
        states[r['state']]=rid
        key=json.dumps([r['state'],r['question'],sorted(option_text)],ensure_ascii=False)
        if key in canonical:failures.append('Duplicate canonical input '+rid)
        canonical[key]=rid
        prov=r['provenance']
        if prov['kind']!='teacher' or prov['label_basis'] not in ('teacher','rule_verified') or prov['teacher_model']!='openai/gpt-sol' or 'data-pilot-v2-rule-a-r1' not in prov['source']:failures.append('Provenance '+rid)
        scenario_rows[prov['scenario_id']]+=1
        scenarios_by_split[r['split']].add(prov['scenario_id'])
        if not prov['scenario_id'].startswith(group+':p'):failures.append('Scenario namespace '+rid)
        index=option_ids.index(r['target_id']);actual=option_text[index]
        answer_text_counts[group][actual]+=1
        c=audits[rid]
        source,source_case=source_by_id[rid]
        if (r['state']==source['title']+'. '+source['rule']+' '+source_case['text'] and c['policy']==source['policy'] and c['facts']==source_case['facts'] and c['mechanism_number']==source['group']):source_fidelity_matches+=1
        else:failures.append('Source/text/fact join '+rid)
        if c['mechanism_number'] in (2,15):
            label=actual.removeprefix('Select candidate ')
            order=[candidate[0] for candidate in c['facts']['candidates']]
            candidate_state_positions[r['split']][order.index(label)+1]+=1
        if c['scenario_id']!=prov['scenario_id']:failures.append('Scenario audit join '+rid)
        answer=expected(c)
        if answer==actual:matches+=1
        else:semantic_failures.append(dict(id=rid,expected=answer,saved=actual))
        stratum=r['split']+':'+str(len(option_ids));positions[stratum][index+1]+=1
        sizes=[len(s) for s in option_text];target_len=sizes[index]
        lengths[r['split']]['target_unique_longest']+=int(target_len==max(sizes) and sizes.count(target_len)==1)
        lengths[r['split']]['target_tied_longest']+=int(target_len==max(sizes) and sizes.count(target_len)>1)
        lengths[r['split']]['target_unique_shortest']+=int(target_len==min(sizes) and sizes.count(target_len)==1)
        word_counts.append(len((r['state']+' '+r['question']+' '+max(option_text,key=len)).split()))
    if len(cases)!=len(rows) or set(audits)!=ids:failures.append('Audit coverage')
    if any(len(s)!=1 for s in group_splits.values()):failures.append('Group overlap')
    if set(group_rows)!=set(assignments):failures.append('Group set')
    for group,n in group_rows.items():
        if n!=(20 if assignments[group]['split']=='train' else 8):failures.append('Group row count '+group)
    if len(scenario_rows)!=120 or set(scenario_rows.values())!={2}:failures.append('True policy/variant counts')
    for k,c in positions.items():
        if max(c.values())-min(c.values())>1:failures.append('Target-position imbalance '+k)
    report=dict(schema_version='0.1',shard_id='data-pilot-v2-rule-a-r1',status='passed' if not failures and not semantic_failures else 'failed',
        row_counts=counts,group_counts=dict(Counter(next(iter(s)) for s in group_splits.values())),true_policy_counts={split:len(scenarios) for split,scenarios in scenarios_by_split.items()},
        source_rendering_fidelity={'compared':len(rows),'exact_source_state_and_structured_fact_matches':source_fidelity_matches,'limitation':'This joins authored prose and facts, not semantic parsing of prose; semantic fidelity remains same-agent review.'},
        target_answer_text_counts={g:dict(c) for g,c in answer_text_counts.items()},candidate_list_winner_positions={s:dict(c) for s,c in candidate_state_positions.items()},
        structural_failures=failures,semantic_audit={'compared':len(rows),'matches':matches,'failures':semantic_failures,'method':'Same-agent separate algorithms on structured facts; no generator import or target access inside expected(). Not independent authorship or text parsing.'},
        exact_state_duplicates=len(rows)-len(states),exact_canonical_input_duplicates=len(rows)-len(canonical),target_positions={k:dict(sorted(v.items())) for k,v in positions.items()},candidate_length_shortcuts={k:dict(v) for k,v in lengths.items()},
        pair_word_count_proxy={'max':max(word_counts),'mean':round(sum(word_counts)/len(word_counts),2),'tokenizer_used':False,'note':'Whitespace words are not tokens. Parent must perform actual 256-token audit.'},
        boundaries={'assignment_mechanisms_split_pure':True,'parent_or_other_producer_data_read':False,'evaluation_data_read':False,'cross_shard_duplicate_audit':'Not performed: private scope only.'},
        text_fact_fidelity='Same-agent review of all authored policy specifications and rendering; not independent correctness verification.',
        sha256={p.name:digest(p) for p in sorted(ROOT.iterdir()) if p.is_file() and p.name not in ('validation_report.json',)})
    (ROOT/'validation_report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:report[k] for k in ('status','row_counts','semantic_audit','structural_failures')},indent=2))
    return report

if __name__=='__main__':
    report=validate()
    raise SystemExit(0 if report['status']=='passed' else 1)
