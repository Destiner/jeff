import sys,json,hashlib,importlib.util
from pathlib import Path
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent.parent; OUT=ROOT/'review-rules'
def load(path):return [json.loads(x) for x in path.read_text().splitlines()]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
config=json.loads(Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/pilot-v2.json').read_text())
report={}; details=[]
for producer in ['rule-a','rule-b']:
 p=ROOT/producer; audit=module(producer.replace('-','_')+'_audit',p/'audit.py')
 rows=load(p/'train.jsonl')+load(p/'validation.jsonl'); cases=load(p/'audit_cases.jsonl'); byid={c['id']:c for c in cases}
 assignments=json.loads((p/'group_assignments.json').read_text())['groups']; failures=[]
 if len(cases)!=len(byid) or set(byid)!={r['id'] for r in rows}:failures.append('audit coverage')
 sources={}
 if producer=='rule-a':
  counters=Counter()
  for s in load(p/'source_cases.jsonl'):
   g=f'data:pilot-v2:rule-a:g{s["group"]:03}'
   for c in s['cases']:
    counters[g]+=1;sources[g+f':r{counters[g]:02}']=(s,c)
 else:
  renderer=module('rule_b_renderer',p/'generate.py')
  for s in load(p/'authoring_cases.jsonl'):
   rid=f'data:pilot-v2:rule-b:g{s["group_number"]:03}:r{(s["policy_number"]-1)*2+s["case_number"]:02}';sources[rid]=s
 config_assignment=next(a for a in config['assignments'] if a['producer']==producer)
 policies=defaultdict(set); groups=defaultdict(set); scenario_splits=defaultdict(set); scenarios=Counter();matches=0;unique=0
 for r in rows:
  c=byid[r['id']];expected=audit.expected(c); target=next(o['text'] for o in r['options'] if o['id']==r['target_id']);hits=[o['id'] for o in r['options'] if o['text']==expected]
  matches+=expected==target;unique+=len(hits)==1
  if expected!=target or len(hits)!=1:failures.append('target '+r['id'])
  gnum=c['mechanism_number' if producer=='rule-a' else 'group_number']; split='train' if gnum<=10 else 'validation'
  mechanism=config_assignment['train_mechanisms' if split=='train' else 'validation_mechanisms'][(gnum-1) if split=='train' else (gnum-11)]
  a=assignments[r['group_id']]
  if r['split']!=split or a['split']!=split or a['mechanism']!=mechanism:failures.append('assignment '+r['id'])
  if c['scenario_id']!=r['provenance']['scenario_id']:failures.append('scenario '+r['id'])
  if producer=='rule-a':
   s,sc=sources[r['id']]; source_ok=c['policy']==s['policy'] and c['facts']==sc['facts'] and c['mechanism_number']==s['group'] and c['scenario_id']==s['scenario_id'] and r['state']==s['title']+'. '+s['rule']+' '+sc['text']
  else:
   s=sources[r['id']]; state,q=renderer.render(s);source_ok=c['policy']==s['policy'] and c['facts']==s['facts'] and c['group_number']==s['group_number'] and r['state']==state and r['question']==q
  if not source_ok:failures.append('source fidelity '+r['id'])
  policies[split].add(c['scenario_id']);groups[split].add(r['group_id']);scenarios[c['scenario_id']]+=1;scenario_splits[c['scenario_id']].add(split)
  details.append({'id':r['id'],'expected_text':expected,'target_text':target,'matches':expected==target,'unique_expected_option':len(hits)==1,'source_correspondence':source_ok})
 if set(sources)!=set(byid):failures.append('source coverage')
 if set(scenarios.values())!={2} or any(len(x)!=1 for x in scenario_splits.values()):failures.append('paired policy split')
 meta=json.loads((p/'metadata.json').read_text()); hashes=meta['generation_settings'].get('source_and_script_sha256',meta['generation_settings'].get('artifact_sha256',{})); mismatched=[name for name,h in hashes.items() if hashlib.sha256((p/name).read_bytes()).hexdigest()!=h]
 report[producer]={'rows':len(rows),'audit_records':len(cases),'matches':matches,'unique_expected_options':unique,'policy_instances':{s:len(v) for s,v in policies.items()},'mechanism_groups':{s:len(v) for s,v in groups.items()},'failures':failures,'metadata_hash_mismatches':mismatched,'method':'Imported existing pure expected(case), dictionary argument, no main/validate invoked. Reused same-author solver, not independent correctness verification.'}
(OUT/'recompute.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'recompute-rows.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in details)); print(json.dumps(report,indent=2))
