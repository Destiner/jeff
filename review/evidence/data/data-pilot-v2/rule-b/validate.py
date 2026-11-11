"""CPU-only shard validation and descriptive shortcut diagnostics, not a software test suite."""
import hashlib
import json
import os
import platform
from collections import Counter,defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from audit import expected
ROOT=Path(__file__).resolve().parent
CONFIG=Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/pilot-v2.json')
CONTRACT=Path('/Users/destiner/Code/jeff/.worktrees/data/docs/contracts.md')

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(name): return [json.loads(line) for line in (ROOT/name).read_text().splitlines()]
def main():
    assignments=json.loads((ROOT/'group_assignments.json').read_text())['groups']
    cfg=json.loads(CONFIG.read_text())
    reservation=next(a for a in cfg['assignments'] if a['producer']=='rule-b')
    rows=load('train.jsonl')+load('validation.jsonl')
    authored=load('authoring_cases.jsonl'); audit=load('audit_cases.jsonl')
    auditmap={c['id']:c for c in audit}
    failures=[]
    def check(value,message):
        if not value: failures.append(message)
    check(len(rows)==240,'total row count')
    check(Counter(r['split'] for r in rows)=={'train':200,'validation':40},'split counts')
    check(len({r['id'] for r in rows})==240,'unique row IDs')
    check(len(auditmap)==240,'unique audit IDs')
    check(set(auditmap)=={r['id'] for r in rows},'audit coverage')
    check(len(authored)==240,'source case count')
    groups=defaultdict(list); states=defaultdict(list); canonical=defaultdict(list)
    positions=defaultdict(Counter); option_counts=defaultdict(Counter); targets=defaultdict(Counter)
    length_diagnostics=defaultdict(Counter)
    compared=0
    for row in rows:
        rid=row['id']; group=row['group_id']; split=row['split']; options=row['options']
        check(row['schema_version']=='0.1',rid+': schema')
        check(row['task_family']=='rule_application',rid+': task family')
        check(isinstance(row['state'],str) and bool(row['state'].strip()),rid+': state')
        check(isinstance(row['question'],str) and bool(row['question'].strip()),rid+': question')
        check(2<=len(options)<=6,rid+': option count')
        check(all(isinstance(o['id'],str) and bool(o['id']) and isinstance(o['text'],str) and bool(o['text'].strip()) for o in options),rid+': option strings')
        check(len({o['id'] for o in options})==len(options),rid+': option IDs unique')
        check(len({o['text'] for o in options})==len(options),rid+': option texts unique')
        selected=[i for i,o in enumerate(options) if o['id']==row['target_id']]
        check(len(selected)==1,rid+': target membership')
        check(group in assignments,rid+': frozen group')
        check(assignments[group]['split']==split,rid+': frozen split')
        number=int(group.rsplit('g',1)[-1]); mechanism=assignments[group]['mechanism']
        mechanism_list=reservation['train_mechanisms'] if split=='train' else reservation['validation_mechanisms']
        check(mechanism in mechanism_list,rid+': reserved mechanism')
        check(group==reservation['group_namespace']+f'g{number:03}',rid+': namespace')
        check(rid.startswith(group+':r'),rid+': variant ID')
        provenance=row['provenance']
        check(provenance['kind']=='programmatic' and provenance['label_basis']=='rule_verified',rid+': provenance type')
        check(provenance['source'].startswith('data-pilot-v2-rule-b-r1:'),rid+': source job')
        check(provenance['scenario_id']==auditmap[rid]['scenario_id'],rid+': scenario link')
        output=expected(auditmap[rid]); compared+=1
        check(output==options[selected[0]]['text'],rid+': independent semantic comparison')
        groups[group].append(row); states[row['state']].append(rid)
        key=json.dumps([row['state'],row['question'],sorted(o['text'] for o in options)],ensure_ascii=False)
        canonical[key].append(rid)
        positions[(split,len(options))][selected[0]+1]+=1
        option_counts[split][len(options)]+=1
        targets[group][output]+=1
        sizes=[len(o['text']) for o in options]; correct_size=sizes[selected[0]]
        d=length_diagnostics[split]; d['rows']+=1
        d['correct_is_longest_including_ties']+=int(correct_size==max(sizes))
        d['correct_is_uniquely_longest']+=int(sizes.count(correct_size)==1 and correct_size==max(sizes))
        d['correct_is_shortest_including_ties']+=int(correct_size==min(sizes))
        d['all_options_equal_length']+=int(min(sizes)==max(sizes))
    for group,examples in groups.items():
        expected_count=20 if assignments[group]['split']=='train' else 8
        check(len(examples)==expected_count,group+': frozen group count')
        check(len({r['split'] for r in examples})==1,group+': split isolation')
        check({r['id'] for r in examples}=={group+f':r{i:02}' for i in range(1,expected_count+1)},group+': IDs')
        sc=Counter(r['provenance']['scenario_id'] for r in examples)
        check(all(n==2 for n in sc.values()) and len(sc)==expected_count//2,group+': paired policies')
    check(set(groups)==set(assignments),'all frozen groups used')
    for (split,n),counts in positions.items():
        check(max(counts.values())-min(counts.get(i,0) for i in range(1,n+1))<=1,f'{split}/{n}: position balance')
    duplicate_states=[ids for ids in states.values() if len(ids)>1]
    duplicate_inputs=[ids for ids in canonical.values() if len(ids)>1]
    check(not duplicate_states,'exact state duplication')
    check(not duplicate_inputs,'canonical input duplication')
    scenarios=defaultdict(set)
    for r in rows: scenarios[r['split']].add(r['provenance']['scenario_id'])
    check(not scenarios['train'].intersection(scenarios['validation']),'scenario isolation')
    source_map={}
    for c in authored:
        group=reservation['group_namespace']+f'g{c["group_number"]:03}'
        rid=group+f':r{(c["policy_number"]-1)*2+c["case_number"]:02}'
        source_map[rid]=c
    for rid,c in auditmap.items():
        check(c['policy']==source_map[rid]['policy'] and c['facts']==source_map[rid]['facts'],rid+': saved source facts')
    scenario_answers=defaultdict(set)
    for r in rows:
        scenario_answers[r['provenance']['scenario_id']].add(next(o['text'] for o in r['options'] if o['id']==r['target_id']))
    # This comparison is local only: no historical, external, other-producer or final data is read.
    train=[r for r in rows if r['split']=='train']; val=[r for r in rows if r['split']=='validation']
    lexical=[]
    for a in train:
        aa=set(a['state'].lower().split())
        for b in val:
            bb=set(b['state'].lower().split()); overlap=len(aa&bb)/len(aa|bb)
            lexical.append((overlap,a['id'],b['id']))
    lexical.sort(reverse=True)
    train_answer_frequency=Counter(o['text'] for r in train for o in r['options'] if o['id']==r['target_id'])
    shortcut_baselines={}
    for split,subset in [('train',train),('validation',val)]:
        correct=Counter()
        for r in subset:
            options=r['options']
            predictions={
                'first_position':options[0],
                'longest_characters_first_tie':max(options,key=lambda o:len(o['text'])),
                'shortest_characters_first_tie':min(options,key=lambda o:len(o['text'])),
                'train_target_text_frequency_first_tie':max(options,key=lambda o:train_answer_frequency[o['text']])}
            for method,option in predictions.items(): correct[method]+=int(option['id']==r['target_id'])
        shortcut_baselines[split]={'rows':len(subset),'correct':dict(correct)}
    hashes={name:digest(ROOT/name) for name in ['group_assignments.json','author.py','authoring_cases.jsonl','generate.py','audit.py','audit_cases.jsonl','train.jsonl','validation.jsonl','validate.py']}
    metadata={
        'schema_version':'0.1','shard_id':'data-pilot-v2-rule-b-r1',
        'teacher':{'provider':os.environ.get('PI_PROVIDER') or 'unknown','model_alias':os.environ.get('PI_MODEL') or 'unknown','immutable_revision':None},
        'cost':{'currency':'GBP','additional_spend':0,'pending_spend':0},
        'generation_settings':{
            'generation_revision':'rule-b-generator-r1','source_revision':'original-policies-r1','assignment_revision':'pilot-v2-rule-b-frozen-r1',
            'method':'Existing approved agent authors original explicit policies and facts; standard-library CPU functions render and compute labels; separate pure semantics compare every target before emission.',
            'seed':761903,'agent_sampling':{'temperature':None,'top_p':None,'sampling_seed':None},
            'position_method':'Independent deterministic shuffle of near-uniform target positions per split and option count, then independent distractor permutation.',
            'python_version':platform.python_version(),'artifact_sha256':hashes,
            'input_revisions':{'config_path':str(CONFIG),'config_sha256':digest(CONFIG),'contracts_sha256':digest(CONTRACT)},
            'no_network_no_ml':True,'source_job':'data-pilot-v2-rule-b-r1'},
        'usage_constraints':'Original synthetic examples produced under existing provider terms; no independent redistribution-license claim. No private records, external sources, historical examples or protected evaluation data used. IDs and all metadata are excluded from model features.',
        'row_counts':{'train':200,'validation':40},
        'group_counts':{'train':10,'validation':5,'unit':'one group per named generator mechanism'},
        'policy_instance_counts':{'train':100,'validation':20,'related_cases_per_policy':2,'independence_claim':'Independently specified synthetic policy instances, not independent real-world observations; shared mechanism renderers and author.'},
        'mechanism_assignments':assignments,
        'limitations':[
            'Same author specified policies, renderers and both semantic implementations. Agreement does not independently establish natural-language specification or rendering correctness.',
            'No separate-session teacher review performed; same-session text spot review only.',
            'No tokenizer or ML loaded; 256-token cap audit is deferred to parent CPU audit.',
            'No parent or other-producer rows inspected; historical duplicates, cross-producer overlap and parent integrity require parent integration checks.',
            'Fifteen mechanism groups, not 240 independent mechanisms; paired cases remain correlated.',
            'Finite hand-authored policies and short calculations do not establish broad mathematical reasoning or real-world calendar validity.',
            'Candidate numeric errors are mostly nearby values; nonuniform answer strings and lengths remain possible shortcuts and are quantified in validation_report.json.',
            'Teacher immutable revision and agent sampling settings were unavailable.'
        ]}
    (ROOT/'metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
    hashes['metadata.json']=digest(ROOT/'metadata.json')
    report={
        'schema_version':'0.1','shard_id':metadata['shard_id'],'status':'passed' if not failures else 'failed',
        'failures':failures,'rows':dict(Counter(r['split'] for r in rows)),
        'groups':{s:sum(a['split']==s for a in assignments.values()) for s in ['train','validation']},
        'policy_instances':{s:len(x) for s,x in scenarios.items()},
        'targets_compared':compared,'target_mismatches':sum('semantic comparison' in s for s in failures),
        'checks':{'contract':'passed' if not failures else 'see failures','unique_ids':len({r['id'] for r in rows}),
                  'group_split_isolation':True,'scenario_split_isolation':True,'frozen_reservations':True,
                  'duplicate_exact_states':duplicate_states,'duplicate_canonical_inputs':duplicate_inputs,
                  'option_id_uniqueness':'within row','no_external_or_final_data_access':True},
        'option_counts':{s:dict(c) for s,c in option_counts.items()},
        'target_positions_1based':{f'{s}/{n}_options':{str(i):c.get(i,0) for i in range(1,n+1)} for (s,n),c in positions.items()},
        'answer_text_frequency_by_group':{g:dict(c) for g,c in targets.items()},
        'paired_policy_outcomes':{'policies':len(scenario_answers),'policies_with_distinct_outputs':sum(len(a)==2 for a in scenario_answers.values())},
        'candidate_only_shortcut_baselines':shortcut_baselines,
        'character_length_shortcuts':{s:dict(c) for s,c in length_diagnostics.items()},
        'text_lengths':{'max_state_words':max(len(r['state'].split()) for r in rows),'max_question_words':max(len(r['question'].split()) for r in rows),
                        'max_option_words':max(len(o['text'].split()) for r in rows for o in r['options']),'tokenizer_used':False,'token_cap_status':'deferred to parent'},
        'within_shard_cross_split_lexical_top10':[{'word_set_jaccard':round(score,4),'train_id':a,'validation_id':b} for score,a,b in lexical[:10]],
        'lexical_review':'Top lexical candidates are shared arithmetic/choice vocabulary across distinct reserved mechanisms; no shared policies, codebooks, fact sets or source scenarios cross split. This is same-author review, not an independent leakage audit.',
        'text_spot_review':{'rows':30,'selection':'First paired policy in every mechanism (r01 and r02 in all 15 groups). Rendered state, question, choices and targets reviewed in this authoring session.',
                            'independent_reviewer':False,'result':'No ambiguity observed in sampled texts; residual specification risk remains.'},
        'deferred_checks':['Parent integrity and historical boundaries','Cross-producer and historical duplicates','256-token CPU tokenizer cap','Separate-session teacher spot review'],
        'artifact_sha256':hashes,
        'execution':'python3 author.py; python3 generate.py; python3 validate.py (standard library only; no software tests or linting)',
        'additional_spend_gbp':0,'pending_spend_gbp':0}
    (ROOT/'validation_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':report['status'],'failures':failures,'rows':report['rows'],'audited':compared,'length_shortcuts':report['character_length_shortcuts'],'top_lexical':report['within_shard_cross_split_lexical_top10'],'positions':report['target_positions_1based']},indent=2))
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
