"""Same-agent separate-algorithm dataset audit; no generator import.
expected(case) is pure and consumes structured facts only, never saved labels.
This is not independent authorship, a test suite, or an external verification.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent


def expected(case):
    p=case['policy']; f=case['facts']; mechanism=case['mechanism_id']
    if mechanism=='packs':
        # Count packs by accumulating available units, not division/ceiling.
        available=f['stock']-f['rejected']
        required=f['demand']+f['reserve']
        if available>=required and not p['always']:
            count=0
        else:
            count=p['minimum']
            available+=count*p['size']
            while available<required:
                count+=1
                available+=p['size']
        return str(count)+(' pack' if count==1 else ' packs')
    if mechanism=='rates':
        # Exact rational sort, rather than generator's streaming cross products.
        candidates=sorted(f['candidates'],key=lambda a:a['name'],reverse=p['tie']=='reverse_alphabetical')
        ranked=sorted(candidates,key=lambda a:Fraction(a['numerator'],a['denominator']),reverse=p['direction']=='max')
        return ranked[0]['name']
    if mechanism=='coordinates':
        # Compose homogeneous transforms before applying to the input point.
        total=[[1,0,0],[0,1,0],[0,0,1]]
        for step in p['ops']:
            a,b=step['matrix'];tx,ty=step['offset']
            matrix=[a+[tx],b+[ty],[0,0,1]]
            total=[[sum(matrix[i][k]*total[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        point=f['point']+[1]
        result=[sum(row[k]*point[k] for k in range(3)) for row in total[:2]]
        return '('+','.join(map(str,result))+')'
    if mechanism!='cooldown':
        raise ValueError(mechanism)
    def minutes(text):
        return sum(int(x)*scale for x,scale in zip(text.split(':'),(60,1)))
    # Existing sessions forbid integer starts in open intervals; endpoints allowed.
    blocked=set()
    for start,end in f['bookings']:
        blocked.update(range(minutes(start)-p['duration']-p['gap']+1,minutes(end)+p['gap']))
    closing=minutes(p['closing'])-p['duration']-(p['gap'] if p['close_mode']=='reset' else 0)
    allowable=set(range(minutes(p['opening']),closing+1))-blocked
    listed={minutes(t):t for t in f['starts']}
    feasible=sorted(allowable & set(listed))
    return listed[feasible[0]] if feasible else 'No listed start fits'


def correspondence(case,row):
    """Independently reconstruct every rendered state/question from source facts."""
    p=case['policy'];f=case['facts'];m=case['mechanism_id']
    prefix=p['text']+' '+case['context']
    if m=='packs':
        text=prefix+' Demand {}; reserve {}; stock {}; rejected {}.'.format(f['demand'],f['reserve'],f['stock'],f['rejected'])
        question='How many packs must be purchased?'
    elif m=='rates':
        by_name={a['name']:a for a in f['candidates']}
        assert set(case['candidate_order'])==set(by_name)
        assert len(case['candidate_order'])==len(by_name)
        parts=[]
        for name in case['candidate_order']:
            a=by_name[name]
            parts.append(name+': '+str(a['numerator'])+'/'+str(a['denominator']))
        text=prefix+' Values are '+p['numerator']+' / '+p['denominator']+': '+'; '.join(parts)+'.'
        question='Which candidate should be selected?'
        assert {o['text'] for o in row['options']}==set(by_name)
    elif m=='coordinates':
        x,y=f['point']
        assert f'({x},{y})' in case['context']
        text=prefix
        question='What are the final coordinates?'
        assert all(re.fullmatch(r'\(-?\d+,-?\d+\)',o['text']) for o in row['options'])
    else:
        text=prefix+' Existing sessions: '+'; '.join('–'.join(b) for b in f['bookings'])+'.'
        question='Which listed start is earliest feasible? If none works, choose “No listed start fits”.'
        assert {o['text'] for o in row['options']}==set(f['starts']+['No listed start fits'])
        assert f['bookings']==sorted(f['bookings'])
    assert row['state']==text,'state/facts mismatch'
    assert row['question']==question,'question/facts mismatch'


def read_lines(name):
    return [json.loads(s) for s in (ROOT/name).read_text().splitlines()]


def digest(name):
    return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()


def main():
    cases=read_lines('audit_cases.jsonl')
    originals=read_lines('source_cases.jsonl')
    rows=read_lines('validation.jsonl')
    assignments=json.loads((ROOT/'group_assignments.json').read_text())['groups']
    errors=[]
    checked=[]
    def check(ok,message):
        if not ok:
            errors.append(message)
    check(len(cases)==len(rows)==len(originals)==48,'48 rows in all files')
    check(len({r['id'] for r in rows})==48,'unique row IDs')
    check(len(assignments)==24,'24 assigned groups')
    row_index={r['id']:r for r in rows}
    source_index={c['id']:c for c in originals}
    check(set(row_index)=={c['id'] for c in cases}==set(source_index),'same row ID coverage')
    slots=defaultdict(Counter);group_counts=Counter();mech_counts=Counter()
    length_ranks=Counter();rate_listing_positions=Counter()
    for c in cases:
        try:
            row=row_index[c['id']]
            source=source_index[c['id']]
            check(c=={k:v for k,v in source.items() if k!='distractors'},c['id']+' original/audit fact equality')
            answer=expected(c)
            option_text=[o['text'] for o in row['options']]
            ids=[o['id'] for o in row['options']]
            check(option_text.count(answer)==1,c['id']+' exactly one expected answer')
            # This is the first point at which saved labels are accessed.
            selected=[o['text'] for o in row['options'] if o['id']==row['target_id']]
            check(selected==[answer],c['id']+' target mismatch')
            check(2<=len(ids)<=6 and len(set(ids))==len(ids) and len(set(option_text))==len(option_text),c['id']+' unique options/arity')
            check(all(isinstance(x,str) and x.strip() for x in ids+option_text),c['id']+' nonempty options')
            check(row['schema_version']=='0.1' and row['split']=='validation' and row['task_family']=='rule_application',c['id']+' contract')
            g=c['group_id'];a=assignments[g]
            check(row['group_id']==g==row['provenance']['policy_instance_id']==a['policy_instance_id'],c['id']+' group')
            check(c['id'] in (g+':c01',g+':c02'),c['id']+' case namespace')
            check(a['mechanism_id']==c['mechanism_id']==row['provenance']['mechanism_id'] and a['policy_domain']==c['policy_domain'] and a['split']=='validation',c['id']+' assignment')
            prov=row['provenance']
            check(prov['kind']=='programmatic' and prov['usage']=='validation_only_never_train' and bool(prov['source']) and prov['teacher_model']=='openai/gpt-sol',c['id']+' provenance')
            correspondence(c,row)
            if c['mechanism_id']=='packs':
                f=c['facts'];p=c['policy']
                check(all(isinstance(v,int) and v>=0 for v in f.values()) and f['stock']>=f['rejected'] and p['size']>0 and p['minimum']>0,c['id']+' valid stock facts')
            if c['mechanism_id']=='rates':
                check(all(x['denominator']>0 for x in c['facts']['candidates']),c['id']+' positive rate denominators')
                rate_listing_positions[c['candidate_order'].index(answer)+1]+=1
            if 'distractors' in source:
                check(set(source['distractors'])==set(option_text)-{answer},c['id']+' distractor correspondence')
            position=option_text.index(answer)
            slots[len(option_text)][position+1]+=1
            lengths=[len(t) for t in option_text]
            length_ranks['shortest_including_ties']+=len(answer)==min(lengths)
            length_ranks['longest_including_ties']+=len(answer)==max(lengths)
            length_ranks['strict_shortest']+=all(len(answer)<len(t) for t in option_text if t!=answer)
            length_ranks['strict_longest']+=all(len(answer)>len(t) for t in option_text if t!=answer)
            group_counts[g]+=1;mech_counts[c['mechanism_id']]+=1
            checked.append(dict(id=c['id'],expected_answer=answer,matched=selected==[answer],text_fact_correspondence=True))
        except Exception as exc:
            errors.append(c['id']+': '+repr(exc))
    check(set(group_counts)==set(assignments) and set(group_counts.values())=={2},'two rows per policy')
    check(mech_counts==dict(packs=12,rates=12,coordinates=12,cooldown=12),'12 rows per mechanism')
    for arity,counter in slots.items():
        counts=[counter[i+1] for i in range(arity)]
        check(max(counts)-min(counts)<=1,'target positions balanced at arity '+str(arity))
    # Explicit, same-agent semantic review notes are written only after reading
    # actual generated text, not fabricated as independent review evidence.
    review_path=ROOT/'semantic_review.json'
    if review_path.exists():
        review=json.loads(review_path.read_text())
        check(set(review['policies'])==set(assignments),'semantic review covers 24 policies')
        check(all(v['case_id'] in row_index and v['reviewed_rendered_text'] and v['verdict']=='consistent' for v in review['policies'].values()),'semantic review records')
        case_index={c['id']:c for c in cases}
        for group,note in review['policies'].items():
            check(note['case_ids']==[group+':c01',group+':c02'],group+' semantic review case IDs')
            check(note['manual_answer_texts']==[expected(case_index[key]) for key in note['case_ids']],group+' manual semantic answers versus separate algorithm')
    else:
        errors.append('semantic_review.json missing')
    report=dict(schema_version='0.1',audit_kind='same_agent_separate_algorithm_consistency_not_independent_authorship',
        rows_checked=len(checked),policy_groups=len(group_counts),mechanisms=dict(mech_counts),
        checks=['Exact targets versus pure expected(case), after generation','Unique expected option and all distinct options',
                'Full rendered state/question correspondence to structured facts','Source and audit fact equality',
                'Contract, namespace, provenance, split and frozen group assignment checks',
                'Balanced randomized target positions within arity','Positive denominators and valid stock',
                'Same-agent semantic reading of rendered text: at least one case per policy'],
        failure_count=len(errors),failures=errors,
        authoring_self_review_corrections=['Four scheduling policies initially implied fixed durations for existing bookings while their second cases used extended existing sessions. Before label verification, wording was corrected to scope the fixed duration to new sessions and explicitly honor stated existing end times. No numeric facts or answers changed.','Three pack distractor sets were revised before audit to include legitimate maximum answers rather than making every positive answer an interior quantity.','Stock rendering changed to a count label to avoid singular/plural mismatch.'],
        target_position_counts={str(k):dict(v) for k,v in slots.items()},
        answer_length_diagnostics=dict(length_ranks),rate_winner_candidate_listing_positions=dict(rate_listing_positions),
        max_state_words=max(len(r['state'].split()) for r in rows),
        tokenizer_check='Not run; parent owns 256-token pair audit.',cases=checked)
    if not errors:
        for r in rows:
            r['provenance']['label_basis']='rule_verified'
        (ROOT/'validation.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
        report['label_basis']='rule_verified'
    else:
        report['label_basis']='not_verified'
    (ROOT/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
    if not errors:
        metadata=json.loads((ROOT/'metadata.json').read_text())
        metadata['generation_settings']['hashes'].update({name:digest(name) for name in ['validation.jsonl','audit.py','validation_report.json','semantic_review.json','generation_review.md']})
        metadata['limitations']=[s.replace('Labels pending same-agent separate-algorithm consistency audit','Labels passed same-agent separate-algorithm consistency audit') for s in metadata['limitations']]
        (ROOT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
    if errors:
        raise SystemExit(1)

if __name__=='__main__':
    main()
