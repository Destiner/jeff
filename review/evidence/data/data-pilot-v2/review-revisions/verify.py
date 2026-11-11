import json,hashlib,collections
from pathlib import Path
B=Path('/Users/destiner/Code/jeff/artifacts/data/data-pilot-v2'); O=B/'review-revisions'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):
 with (O/n).open('x') as f:json.dump(x,f,indent=2);f.write('\n')
def rows(d):return [json.loads(s) for split in ['train','validation'] for s in (B/d/(split+'.jsonl')).read_text().splitlines()]
def target(r):return next(o['text'] for o in r['options'] if o['id']==r['target_id'])
E={'producers':{},'sample_comparison':[],'hash_checks':[],'manifest_checks':[]}; allnew={}; allold={}
def checkhash(p,expected,origin):E['hash_checks'].append({'path':str(p),'expected':expected,'actual':sha(p),'match':sha(p)==expected,'origin':origin})
for d in ['intent-a','intent-b','sentiment-b']:
 new=d+'-r2'; oldrows=rows(d); newrows=rows(new); old={r['id']:r for r in oldrows}; idx={r['id']:r for r in newrows};allold.update(old);allnew.update(idx)
 counts=collections.Counter();bad=[]; statechanges=[]; changedfields=collections.Counter(); changes=[]
 for r in newrows:
  pid=r['provenance']['parent_id'];p=old[pid]
  counts['rows']+=1
  for k in set(p)|set(r):
   if p.get(k)!=r.get(k):changedfields[k]+=1
  for k in ['state','question','group_id','split','schema_version','task_family','target_id']:
   if r[k]==p[k]:counts[k+'_identical']+=1
   elif k!='state' or d!='sentiment-b':bad.append([r['id'],k])
  ids=lambda x:[o['id'] for o in x['options']]
  for label,ok in [('arity',len(r['options'])==len(p['options'])),('ordered_option_ids',ids(r)==ids(p)),('target_slot',ids(r).index(r['target_id'])==ids(p).index(p['target_id']))]:
   if ok:counts[label+'_identical']+=1
   else:bad.append([r['id'],label])
  if r['state']!=p['state']:statechanges.append({'id':r['id'],'parent_id':pid,'old':p['state'],'new':r['state']})
  if r['options']!=p['options']:counts['option_sets_changed']+=1
  if target(r)!=target(p):counts['target_texts_changed']+=1
  for a,b in zip(p['options'],r['options']):
   counts['option_texts_total']+=1
   if a['text']!=b['text']:
    counts['option_texts_changed']+=1
    counts['target_option_texts_changed' if b['id']==r['target_id'] else 'rival_option_texts_changed']+=1
  if r['id']!=pid.replace(':'+d+':',':'+new+':'):bad.append([r['id'],'namespace'])
  if r['provenance'].get('kind')!='teacher' or r['provenance'].get('label_basis')!='teacher':bad.append([r['id'],'teacher provenance'])
  if not r['provenance'].get('source') or not r['provenance'].get('teacher_model'):bad.append([r['id'],'source/teacher missing'])
  allowed={'id','provenance','options'} if d.startswith('intent') else {'id','provenance','state'}
  if any(p.get(k)!=r.get(k) for k in set(p)|set(r) if k not in allowed):bad.append([r['id'],'unexpected field change'])
 meta=load(B/new/'metadata.json');gs=meta['generation_settings']
 for name,expected in meta.get('parent',{}).get('sha256',{}).items():checkhash(B/d/name,expected,new+' parent.sha256')
 for key in ['artifact_sha256','source_and_script_sha256','output_sha256']:
  for name,expected in gs.get(key,{}).items():checkhash(B/new/name,expected,new+' generation_settings.'+key)
 for name,expected in gs.get('parent_hashes',{}).items():checkhash(B/d/name,expected,new+' parent_hashes')
 if 'script_sha256' in gs:checkhash(B/new/gs['script'],gs['script_sha256'],new+' script_sha256')
 mappingchecks=collections.Counter();mappingbad=[]
 if d.startswith('intent'):
  mapping=load(B/new/('choice_mappings.json' if d=='intent-a' else 'source_mappings.json'))['rows']
  for m in mapping:
   r=idx[m['id']];p=old[m['parent_id']]
   expected=[{'id':a['id'],'parent_text':a['text'],'text':b['text']} for a,b in zip(p['options'],r['options'])]
   ok=m['options']==expected and all(m[k]==r[k] for k in ['group_id','split','target_id']) and m['parent_id']==r['provenance']['parent_id']
   if 'target_slot_1_based' in m:ok &= m['target_slot_1_based']==[a['id'] for a in r['options']].index(r['target_id'])+1
   if 'parent_target_text' in m:ok &= m['parent_target_text']==target(p)
   if ok:mappingchecks['exact_mapping_rows']+=1
   else:mappingbad.append(m['id'])
  if len({m['id'] for m in mapping})!=len(idx):mappingbad.append('mapping coverage')
  if d=='intent-a':
   authored={a[0]:a[1:] for a in [l.split('|') for l in (B/new/'choices.txt').read_text().splitlines() if l.strip()]}
   source={a[0]:a[1:] for a in [l.split('|') for l in (B/d/'source_cases.txt').read_text().splitlines() if l.strip()]}
   for r in newrows:
    p=old[r['provenance']['parent_id']];g=r['group_id'].split(':')[-1];sc=source[g];bytext={a['text']:a['id'] for a in p['options']};expected={bytext[t]:nt for t,nt in zip(sc[1:],authored[g])}
    ok=p['state']==sc[0] and target(p)==sc[1] and len(authored[g])==len(r['options']) and all(expected[a['id']]==a['text'] for a in r['options'])
    if ok:mappingchecks['authored_source_rows']+=1
    else:mappingbad.append(r['id'])
  else:
   authored=[l.split(' | ') for l in (B/new/'authored_choices.txt').read_text().splitlines() if l.strip() and not l.startswith('#')];refs=load(B/new/'target_refinements.json')
   source=[l.split(' | ') for l in (B/d/'source_cases.txt').read_text().splitlines() if l.strip() and not l.startswith(('#','@'))]
   for k,t in refs.items():authored[int(k)-1][0]=t
   for r in newrows:
    p=old[r['provenance']['parent_id']];i=int(r['group_id'].split(':g')[-1])-1;ts=authored[i];actual=[target(r)]+[a['text'] for a in r['options'] if a['id']!=r['target_id']]
    ok=actual==ts and p['state']==source[i][0] and target(p)==source[i][1] and {a['text'] for a in p['options']}==set(source[i][1:])
    if ok:mappingchecks['authored_source_rows']+=1
    else:mappingbad.append(r['id'])
   mappingchecks['target_refinement_entries']=len(refs)
 assignments=load(B/new/'group_assignments.json')['groups']; train={r['group_id'] for r in newrows if r['split']=='train'}; val={r['group_id'] for r in newrows if r['split']=='validation'}
 E['producers'][new]={'counts':dict(counts),'changed_fields':dict(changedfields),'structural_violations':bad,'state_changes':statechanges,'mapping_checks':dict(mappingchecks),'mapping_violations':mappingbad,'group_assignments_byte_identical':sha(B/new/'group_assignments.json')==sha(B/d/'group_assignments.json'),'group_assignment_rows_match':all(assignments[r['group_id']]['split']==r['split'] for r in newrows),'cross_split_group_overlap':len(train&val),'row_counts':dict(collections.Counter(r['split'] for r in newrows)),'metadata_row_counts_match':meta['row_counts']==dict(collections.Counter(r['split'] for r in newrows)),'id_unique':len(idx)==len(newrows),'parent_ids_bijective':set(r['provenance']['parent_id'] for r in newrows)==set(old)}
 if d=='sentiment-b':
  src=[l.split('|',1) for l in (B/d/'source_cases.txt').read_text().splitlines() if l and not l.startswith(('#','@'))]
  classes={};classbad=[]
  for r in newrows:
   i=int(r['group_id'].split(':g')[-1])-1;label,state=src[i];p=old[r['provenance']['parent_id']]
   if state!=p['state']:classbad.append(r['id'])
   classes.setdefault(label,set()).add(target(r))
  distribution={split:dict(collections.Counter(src[int(r['group_id'].split(':g')[-1])-1][0] for r in newrows if r['split']==split)) for split in ['train','validation']}
  E['sentiment_class_coverage']={'counts':distribution,'source_states_match_parent':not classbad,'class_to_target_texts':{k:sorted(v) for k,v in classes.items()},'note':'Class mappings are checked for coverage and unchanged options/targets, not relabeled independently.'}
  E['sentiment_g011']=[r for r in newrows if ':g011:' in r['id']][0]
  E['sentiment_provenance_checks']={'all_parent_source_prefixed':all(r['provenance']['source']=='data-pilot-v2-sentiment-b-r2/from/'+old[r['provenance']['parent_id']]['provenance']['source'] for r in newrows),'all_other_provenance_fields_retained':all({k:v for k,v in r['provenance'].items() if k not in ['source','parent_id']}=={k:v for k,v in old[r['provenance']['parent_id']]['provenance'].items() if k not in ['source','parent_id']} for r in newrows),'teacher_metadata_retained':meta['teacher']==load(B/d/'metadata.json')['teacher']}
for j in load(O/'blind-judgments-frozen.json')['judgments']:
 r=allnew[j['id']];p=allold[r['provenance']['parent_id']]
 E['sample_comparison'].append({**j,'target_id':r['target_id'],'agrees':j['chosen_option_id']==r['target_id'],'parent_target_text':target(p),'revised_target_text':target(r),'split':r['split'],'domain':load(B/r['id'].split(':')[2]/'group_assignments.json')['groups'][r['group_id']]['domain']})
manifest=load(B/'pre-review-r3/manifest.json')
for s in manifest['shards']:
 p=Path('/Users/destiner/Code/jeff/artifacts')/s['path']
 if p.parent.name not in ['intent-a-r2','intent-b-r2','sentiment-b-r2']:continue
 rs=[json.loads(l) for l in p.read_text().splitlines()]
 E['manifest_checks'].append({'path':s['path'],'hash_matches':sha(p)==s['sha256'],'rows_match':len(rs)==s['rows'],'split_matches':all(r['split']==s['split'] for r in rs)})
E['candidate_scope']={'shards_total':len(manifest['shards']),'revised_shards_checked':len(E['manifest_checks']),'other_shards_not_opened':True,'only_train_validation_entries':all(s['split'] in ['train','validation'] for s in manifest['shards'])}
before=load(O/'sha-before.json');after={p:sha(Path(p)) for p in before};save('sha-after.json',after);E['preservation']={'files':len(before),'all_unchanged':before==after,'changed_paths':[p for p in before if before[p]!=after[p]],'frozen_judgments_sha256':sha(O/'blind-judgments-frozen.json')}
save('verification.json',E)
print(json.dumps({k:v for k,v in E.items() if k not in ['sample_comparison','hash_checks','sentiment_g011','sentiment_class_coverage']},indent=2))
print('HASH REFERENCES',len(E['hash_checks']),'FAILURES',[c for c in E['hash_checks'] if not c['match']])
print('SENTIMENT CLASSES',json.dumps(E['sentiment_class_coverage']))
for s in E['sample_comparison']: print(s['id'],s['agrees'],repr(s['parent_target_text']),'->',repr(s['revised_target_text']))
