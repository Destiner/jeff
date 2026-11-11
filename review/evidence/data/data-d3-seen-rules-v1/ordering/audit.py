"""Dataset audit, not a software test suite. No generator imports.
expected(case) is pure and operates only on structured source facts.
Fraction arithmetic, pairwise dominance, and cumulative interval overlap differ
from the generator's Decimal, tuple sorting, and stock-depletion algorithms.
"""
import hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent
def fixed(v,places):
    scale=10**places
    scaled=v*scale
    if scaled.denominator!=1: raise ValueError('Not exactly representable at stated precision')
    n=scaled.numerator
    if not places:return str(n)
    return f'{n//scale}.{n%scale:0{places}d}'
def expected(case):
    p,f=case['policy'],case['facts'];m=case['mechanism_id']
    if m=='lexicographic':
        def beats(a,b):
            for i,(_,direction) in enumerate(p['criteria'],1):
                if a[i]!=b[i]:return a[i]>b[i] if direction=='max' else a[i]<b[i]
            return False
        winners=[a for a in f['candidates'] if all(a==b or beats(a,b) for b in f['candidates'])]
        if len(winners)!=1:raise ValueError('Nonunique rank winner')
        return winners[0][0]
    if m=='fifo':
        # Each batch owns an interval on the cumulative stock axis.
        takes={}
        for name,arrival,qty in f['batches']:
            start=sum(b[2] for b in f['batches'] if b[1]<arrival)
            end=start+qty
            takes[name]=max(0,min(end,f['request'])-start)
        if sum(takes.values())!=f['request']:raise ValueError('Insufficient inventory')
        return '; '.join(f'{name} {takes[name]}' for name in sorted(takes))
    if m=='discount':
        # Compose affine transforms before evaluating the original base.
        slope=F(1);intercept=F(0)
        for op,a in p['steps']:
            if op=='fixed':intercept-=F(a)
            else:
                multiplier=(100-F(a))/100
                slope*=multiplier;intercept*=multiplier
        value=slope*F(f['base'])+intercept
        return '£'+fixed(value,2)
    if m=='rounding':
        value=F(f['value']);step=F(p['step'])
        floor=value//step
        low=floor*step;high=low+step
        answer=low if value-low<high-value else high
        return fixed(answer,p['places'])+' '+p['unit']
    raise ValueError(m)
def stated(case):
    # Exact textual correspondence: every authored rule/fact and displayed item.
    p,f=case['policy'],case['facts'];m=case['mechanism_id']
    if m=='lexicographic':
        indexed={a[0]:a for a in f['candidates']}
        rules='; then '.join(k+' '+('highest' if d=='max' else 'lowest') for k,d in p['criteria'])
        records=' | '.join(name+': '+', '.join(str(x) for x in indexed[name][1:]) for name in case['display_order'])
        return p['context']+' Rank by '+rules+'. Compare a later field only when all earlier fields tie. Fields: '+p['units']+'. '+records+'.','Which candidate receives priority?'
    if m=='fifo':
        indexed={a[0]:a for a in f['batches']}
        records=' | '.join(name+': '+str(indexed[name][1])+', '+str(indexed[name][2]) for name in case['display_order'])
        return p['context']+' '+p['note']+' Issue '+str(f['request'])+' '+p['unit']+' by FIFO: exhaust the smallest arrival number before using the next. Batches (arrival number, available '+p['unit']+'): '+records+'.','How many units should be issued from each batch?'
    if m=='discount':
        instructions=[]
        for op,a in p['steps']:
            instructions.append('subtract £'+a if op=='fixed' else 'reduce the current subtotal by '+a+'%')
        return p['context']+' Starting charge: £'+f['base']+'. In order: '+'; then '.join(instructions)+'. '+p['note']+' No tax or other charge applies. Keep exact arithmetic until the final amount in pounds and pence.','What is the final charge?'
    return p['context']+' Measured value: '+f['value']+' '+p['unit']+'. Record the nearest multiple of '+p['step']+' '+p['unit']+', using multiples anchored at zero. At an exact halfway point, choose the higher multiple.','What value should be recorded?'
def load(name):return [json.loads(x) for x in (P/name).read_text().splitlines()]
def main():
    sources=load('source_cases.jsonl');cases=load('audit_cases.jsonl');rows=load('validation.jsonl')
    assignments=json.loads((P/'group_assignments.json').read_text())['groups']
    failures=[];checks=Counter();results=[];position=defaultdict(Counter);first=Counter();lengths=Counter()
    def check(ok,description,row='shard'):
        checks[description]+=1
        if not ok:failures.append({'id':row,'check':description})
    check(len(rows)==len(cases)==len(sources)==48,'exact_48_rows')
    check(len(assignments)==24,'exact_24_assignments')
    check(len({r['id'] for r in rows})==48,'unique_row_ids')
    check(len({r['group_id'] for r in rows})==24,'exact_24_groups')
    check(Counter(r['mechanism_id'] for r in cases)==dict.fromkeys(['lexicographic','fifo','discount','rounding'],12),'mechanism_counts')
    check(Counter(r['group_id'] for r in rows)==dict.fromkeys(assignments,2),'two_cases_each_policy')
    for src,c,r in zip(sources,cases,rows):
        rid=r['id'];g=assignments[r['group_id']]
        check({k:v for k,v in c.items() if k!='display_order'}==src,'audit_source_identity',rid)
        check(rid==c['id'] and r['group_id']==c['group_id'],'id_correspondence',rid)
        check(rid in [c['group_id']+':c01',c['group_id']+':c02'],'case_namespace',rid)
        check(g['split']=='validation' and g['policy_instance_id']==c['group_id'] and g['mechanism_id']==c['mechanism_id'] and g['policy_domain']==c['policy_domain'],'assignment_correspondence',rid)
        check(r['schema_version']=='0.1' and r['split']=='validation' and r['task_family']=='rule_application','contract_fields',rid)
        options=r['options'];texts=[o['text'] for o in options];ids=[o['id'] for o in options]
        check(2<=len(options)<=6 and len(set(ids))==len(ids) and len(set(texts))==len(texts) and all(ids) and all(texts),'options_unique_nonempty',rid)
        answer=expected(c)
        check(texts.count(answer)==1,'unique_exact_expected_option',rid)
        selected=next((o['text'] for o in options if o['id']==r['target_id']),None)
        check(selected==answer,'computed_target_agreement',rid)
        state,question=stated(c)
        check(r['state']==state and r['question']==question,'complete_text_fact_correspondence',rid)
        if c['mechanism_id'] in ('fifo','lexicographic'):
            name='batches' if c['mechanism_id']=='fifo' else 'candidates'
            check(sorted(c['display_order'])==sorted(a[0] for a in c['facts'][name]),'display_permutation',rid)
            if c['mechanism_id']=='lexicographic':first[str(c['display_order'][0]==answer)]+=1
        prov=r['provenance']
        check(prov['kind']=='programmatic' and prov['source']=='data-d3-seen-rules-v1-ordering-original-731904' and prov['teacher_model']=={'provider':'openai','model_alias':'gpt-sol'} and prov['mechanism_id']==c['mechanism_id'] and prov['policy_instance_id']==c['group_id'] and prov['usage']=='validation_only_never_train','provenance_correspondence',rid)
        pos=ids.index(r['target_id']);position[len(options)][pos]+=1
        n=len(answer);lengths['tied_length' if sum(len(t)==n for t in texts)>1 else ('unique_shortest' if n==min(map(len,texts)) else 'unique_longest' if n==max(map(len,texts)) else 'interior_length')]+=1
        # Validate every distractor's domain, not merely the selected answer.
        if c['mechanism_id']=='fifo':
            stock={b[0]:b[2] for b in c['facts']['batches']}
            for text in texts:
                take={s.rsplit(' ',1)[0]:int(s.rsplit(' ',1)[1]) for s in text.split('; ')}
                check(set(take)==set(stock) and sum(take.values())==c['facts']['request'] and all(0<=q<=stock[n] for n,q in take.items()),'feasible_allocation_option',rid)
        if c['mechanism_id']=='lexicographic':check(set(texts)=={a[0] for a in c['facts']['candidates']},'all_candidate_options',rid)
        if c['mechanism_id']=='rounding':
            check(all(F(t.split()[0])%F(c['policy']['step'])==0 and t.split()[1]==c['policy']['unit'] for t in texts),'rounding_options_on_grid',rid)
        if c['mechanism_id']=='discount':check(all(t.startswith('£') and F(t[1:])>=0 for t in texts),'currency_options_valid',rid)
        results.append({'id':rid,'expected_text':answer,'target_text':selected,'text_fact_match':r['state']==state and r['question']==question,'agreement':selected==answer})
    for arity,hist in position.items():check(max(hist.values())-min(hist.values())<=1 and len(hist)==arity,'balanced_target_slots_arity_'+str(arity))
    report=dict(schema_version='0.1',audit_type='same_agent_separate_algorithm_consistency',rows=len(rows),groups=len(assignments),checks=dict(checks),check_count=sum(checks.values()),failures=failures,failure_count=len(failures),target_positions_by_arity={str(k):dict(v) for k,v in position.items()},lexicographic_first_displayed_winner=dict(first),correct_option_character_lengths=dict(lengths),max_state_words=max(len(r['state'].split()) for r in rows),tokenizer_audit='not performed; parent owns 256-token audit',semantic_self_review={'policies_reviewed':24,'cases_reviewed':24,'record':'generation_review.md','independent_authorship':False},case_results=results,rule_verified=not failures)
    if not failures:
        for r in rows:r['provenance']['label_basis']='rule_verified'
        (P/'validation.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    (P/'validation_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:report[k] for k in ['rows','groups','check_count','failure_count','target_positions_by_arity','lexicographic_first_displayed_winner','correct_option_character_lengths','max_state_words','rule_verified']}))
    if failures:raise SystemExit(1)
if __name__=='__main__':main()
