from pathlib import Path
import json,collections
R=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1'); O=R/'review'
def load(p):return json.loads(p.read_text())
def jl(p):return [json.loads(x) for x in p.read_text().splitlines()]
c=load(O/'checks.json'); rows=[r for d in ['intent','sentiment-r2','rule_application'] for s in ['train','validation'] for r in jl(R/d/f'{s}.jsonl')]; byid={r['id']:r for r in rows}
classes={
'P':{'Positive only: the writer expresses approval or satisfaction, with no stated criticism of the specified subject.','Favorable toward the named subject, with no stated criticism of that subject.','The stated attitude toward this subject is favorable only, not a combination of praise and criticism.'},
'N':{'Negative only: the writer expresses criticism or dissatisfaction, with no stated praise of the specified subject.','Unfavorable toward the named subject, with no stated praise of that subject.','The stated attitude toward this subject is unfavorable only, not a combination of praise and criticism.'},
'U':{'Neutral: the writer gives facts without expressing approval or disapproval of the specified subject.','Descriptive only: no evaluative attitude toward the named subject is stated.','No positive or negative attitude toward this subject is expressed.'},
'M':{'Mixed: the writer explicitly expresses both favorable and unfavorable views of the specified subject.','Both praise and criticism of the named subject are stated; neither side should be discarded.','The stated attitude combines satisfaction and dissatisfaction with this subject.'}}
def classify(t):return next((k for k,v in classes.items() if t in v),None)
revision=[]
for x in c['revision_checks']:
    r=byid[x['id']]
    revision.append({'id':r['id'],'parent_class_matches_map':classify(x['original_target_text'])==x['class'],'revision_class_matches_map':classify(x['revised_target_text'])==x['class'],'exactly_all_four_classes':collections.Counter(classify(o['text']) for o in r['options'])==collections.Counter('PNUM')})
facts={x['id']:x for x in jl(R/'rule_application/audit_cases.jsonl')}
pair_checks=[]
for p in c['validation']['likely_duplicates']:
    a,b=byid[p['left']],byid[p['right']]; fa,fb=facts[a['id']]['facts'],facts[b['id']]['facts']
    identical=fa==fb
    pair_checks.append({**p,'structured_facts_identical':identical,'mechanisms_equal':facts[a['id']]['mechanism']==facts[b['id']]['mechanism'],'same_fact_target_conflict':identical and next(o['text'] for o in a['options'] if o['id']==a['target_id'])!=next(o['text'] for o in b['options'] if o['id']==b['target_id'])})
a=jl(R/'sentiment/train.jsonl')[0];b=jl(R/'sentiment-r2/train.jsonl')[0]
metadata={d:load(R/d/'metadata.json') for d in ['intent','sentiment','sentiment-r2','rule_application']}
# Read source rows for explicitly noted cross-family scenario/domain risks.
pairs=[('intent','g09','sentiment','g26'),('intent','g17','sentiment','g27'),('intent','g28','sentiment','g30'),('intent','g06','sentiment','g16'),('intent','g22','sentiment','g25')]
scenarios=[]
for f,g,h,k in pairs:
    left=[r for r in rows if r['task_family']==f and r['group_id'].endswith(':'+g)]
    right=[r for r in rows if r['task_family']==h and r['group_id'].endswith(':'+k)]
    scenarios.append({'left_group':left[0]['group_id'],'right_group':right[0]['group_id'],'cross_split':left[0]['split']!=right[0]['split'],'left_states':[r['state'] for r in left],'right_states':[r['state'] for r in right]})
result={'revision_class_checks':revision,'revision_fields_pass_counts':{k:sum(x[k] for x in c['revision_checks']) for k in ['state_preserved','split_preserved','group_preserved','subject_in_original_question','revised_neutral_question','four_options']},'pair_checks':pair_checks,'provenance_example':{'parent':a['provenance'],'revision':b['provenance']},'metadata':metadata,'cross_family_scenario_examples':scenarios,'lead_duplicate_list_identical':c['validation']['likely_duplicates']==load(R/'validation.json')['likely_duplicates']}
with (O/'supplement.json').open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps({'revision_fields_pass_counts':result['revision_fields_pass_counts'],'revision_class_all_pass':all(all(x[k] for k in ['parent_class_matches_map','revision_class_matches_map','exactly_all_four_classes']) for x in revision),'facts_identical_pairs':sum(x['structured_facts_identical'] for x in pair_checks),'target_conflicts':sum(x['same_fact_target_conflict'] for x in pair_checks),'lead_duplicates_identical':result['lead_duplicate_list_identical'],'provenance_example':result['provenance_example'],'cross_family_scenario_examples':scenarios},indent=2))
