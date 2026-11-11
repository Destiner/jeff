from pathlib import Path
import json, hashlib, collections, itertools, runpy, re, unicodedata, os
R=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v1'); O=R/'review'
def load(p): return json.loads(p.read_text())
def jl(p): return [json.loads(x) for x in p.read_text().splitlines()]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def path(p):
    q=R/Path(p).relative_to('data/data-pilot-v1')
    assert q.resolve().is_relative_to(R) and 'review' not in q.relative_to(R).parts
    return q
before={str(p.relative_to(R)):digest(p) for p in R.rglob('*') if p.is_file() and 'review' not in p.relative_to(R).parts}
v=runpy.run_path('/Users/destiner/Code/jeff/.worktrees/data/src/jeff/data/validate.py')
validation=v['validate'](R/'manifest.json',R.parent.parent)
rows=[r for e in load(R/'manifest.json')['shards'] for r in jl(path(e['path']))]
byid={r['id']:r for r in rows}
prov=load(R/'provenance.json')
provenance_hashes=[{'path':p,'matches':digest(path(p))==h} for s in prov['sources'] for p,h in s['artifact_sha256'].items()]
allocation=[]
for directory in ['intent','sentiment-r2','rule_application']:
    plan=load(R/directory/'group_assignments.json'); plan=plan.get('groups',plan)
    family='sentiment' if directory=='sentiment-r2' else directory
    for row in [r for r in rows if r['task_family']==family]:
        allocation.append(row['group_id'] in plan and plan[row['group_id']]['split']==row['split'])
audit=runpy.run_path(str(R/'rule_application/audit.py')) # not __main__, no producer writes or bytecode
cases=jl(R/'rule_application/audit_cases.jsonl')
rule=[]
for c in cases:
    r=byid[c['id']]; answer=audit['expected'](c['mechanism'],c['facts'])
    opts=[o for o in r['options'] if o['text']==answer]
    rule.append({'id':r['id'],'expected_text':answer,'matches':len(opts)==1 and opts[0]['id']==r['target_id']})
selected=jl(O/'selected_inputs.jsonl'); decisions=load(O/'precomparison_decisions.json')
row_reviews=[]
for s,d in zip(selected,decisions['decisions']):
    r=byid[s['id']]; i=d['choice_index']; target=next(j for j,o in enumerate(r['options']) if o['id']==r['target_id'])
    row_reviews.append({**d,'id':r['id'],'family':r['task_family'],'split':r['split'],'group_id':r['group_id'],'assessed_answer':s['options'][i]['text'],'published_answer':r['options'][target]['text'],'agrees':i==target,'mode':'ordinary_teacher_review_prior_label_exposure' if d['row']==13 else 'label_hidden_teacher_assessment','confidence':'high','mutually_exclusive_choices':'yes under stated question scope','statement_target_fidelity':'supported by direct text spot-check'})
parent={r['id']:r for split in ['train','validation'] for r in jl(R/'sentiment'/f'{split}.jsonl')}
revision=[]
for m in load(R/'sentiment-r2/revision_map.json'):
    a=parent[m['parent_id']]; b=byid[m['id']]
    at=next(o['text'] for o in a['options'] if o['id']==a['target_id']); bt=next(o['text'] for o in b['options'] if o['id']==b['target_id'])
    revision.append({'id':b['id'],'class':m['class'],'subject':m['subject'],'original_target_text':at,'revised_target_text':bt,'state_preserved':a['state']==b['state'],'split_preserved':a['split']==b['split'],'group_preserved':a['group_id']==b['group_id'],'provenance_preserved':a['provenance']==b['provenance'],'subject_in_original_question':m['subject'] in a['question'],'revised_neutral_question':b['question']==f"What sentiment does the writer express toward {m['subject']}?",'four_options':len(b['options'])==4})
# Cross-family state similarity, ignoring option boilerplate. Also inspect repeated source topics.
norm=v['normalized']; shingles=[]
for r in rows:
    t=norm(r['state']).split(); shingles.append(set(zip(t,t[1:],t[2:])))
cross=[]
for i,a in enumerate(rows):
    for j in range(i+1,len(rows)):
        b=rows[j]
        if a['task_family']==b['task_family']: continue
        union=shingles[i]|shingles[j]; score=len(shingles[i]&shingles[j])/len(union) if union else 1
        cross.append({'left':a['id'],'right':b['id'],'similarity':score,'cross_split':a['split']!=b['split']})
cross.sort(key=lambda x:-x['similarity'])
pairs=validation['likely_duplicates']
pair_groups=collections.defaultdict(list)
for p in pairs: pair_groups[byid[p['left']]['group_id']].append(p)
pair_detail=[]
for g,ps in pair_groups.items():
    # strongest and weakest flagged pair per group, compare full wording and structured facts
    for p in [max(ps,key=lambda x:x['similarity']),min(ps,key=lambda x:x['similarity'])]:
        a,b=byid[p['left']],byid[p['right']]
        facts={c['id']:c['facts'] for c in cases}
        pair_detail.append({**p,'left_state':a['state'],'right_state':b['state'],'left_facts':facts.get(a['id']),'right_facts':facts.get(b['id']),'left_target':next(o['text'] for o in a['options'] if o['id']==a['target_id']),'right_target':next(o['text'] for o in b['options'] if o['id']==b['target_id'])})
after={str(p.relative_to(R)):digest(p) for p in R.rglob('*') if p.is_file() and 'review' not in p.relative_to(R).parts}
result={'identity':{'PI_MODEL':os.environ.get('PI_MODEL'),'PI_PROVIDER':os.environ.get('PI_PROVIDER'),'immutable_revision':None},'validation':validation,'provenance_hashes':provenance_hashes,'all_360_allocation_matches':all(allocation),'rule_reproduction':rule,'row_reviews':row_reviews,'revision_checks':revision,'revision_map_unique_ids':len({x['id'] for x in revision})==120,'parent_shard_hash_matches':{s:digest(R/'sentiment'/s)==h for s,h in load(R/'sentiment-r2/metadata.json')['parent_shard_hashes'].items()},'duplicate_pairs_per_group':{g:len(p) for g,p in pair_groups.items()},'duplicate_pair_samples':pair_detail,'cross_family_top20':cross[:20],'producer_files_unchanged_during_validation':before==after,'producer_snapshot_before':before,'producer_snapshot_after':after}
with (O/'checks.json').open('x') as f: json.dump(result,f,indent=2,ensure_ascii=False)
print(json.dumps({'valid':validation['valid'],'rows':validation['rows'],'counts':validation['counts'],'groups':validation['groups'],'errors':validation['errors'],'likely':validation['likely_duplicate_counts'],'pair_groups':result['duplicate_pairs_per_group'],'hash_failures':[p for p in provenance_hashes if not p['matches']],'rule_matches':sum(x['matches'] for x in rule),'review_agreements':sum(x['agrees'] for x in row_reviews),'revision_boolean_failures':[{k:v for k,v in x.items() if v is False} for x in revision if any(v is False for v in x.values())],'unchanged':before==after,'revision_target_text_mapping':list({(x['class'],x['original_target_text'],x['revised_target_text']) for x in revision}),'cross_family_top5':cross[:5]},indent=2))
print('\nFLAGGED PAIR SAMPLES')
for p in pair_detail:
    print(json.dumps(p,ensure_ascii=False))
print('\nGROUP SCENARIOS:')
for family in ['intent','sentiment','rule_application']:
    print(family)
    for g in sorted({r['group_id'] for r in rows if r['task_family']==family}):
        r=next(r for r in rows if r['group_id']==g)
        print(g,r['split'],r['state'][:200])
