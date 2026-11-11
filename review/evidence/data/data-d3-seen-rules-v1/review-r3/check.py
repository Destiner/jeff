import ast, collections, copy, hashlib, json, os
from pathlib import Path
B=Path('/Users/destiner/Code/jeff/artifacts/data/data-d3-seen-rules-v1'); O=B/'review-r3'
def J(p):return json.loads((B/p).read_text())
def L(p):return [json.loads(x) for x in (B/p).read_text().splitlines()]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for d in ['pre-review-r3','pre-review-r2','geometry-r3','geometry-r2','ordering-r2','review-r2']:
 files += [p for p in (B/d).rglob('*') if p.is_file() and '__pycache__' not in str(p)]
files += [B/'review/review.json']
before={str(p.relative_to(B)):H(p) for p in files}
fail=[]; counts=collections.Counter()
def check(ok,name,rid=None):
 counts[name]+=1
 if not ok:fail.append({'check':name,'id':rid})
# Only inspected imports and pure functions; all main/read/write helpers excluded.
def pure(path,names):
 tree=ast.parse((B/path).read_text()); nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)) or isinstance(n,ast.FunctionDef) and n.name in names]
 env={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),env);return env
G=pure('geometry-r3/audit.py',{'expected','correspondence'})
Q=pure('ordering-r2/audit.py',{'expected','stated','fixed'})
rows={}; old={};results=[];source={}
for shard,folder,solver in [('geometry','geometry-r3',G),('ordering','ordering-r2',Q)]:
 rr=L(f'pre-review-r3/shards/{shard}.jsonl'); prev=L(f'pre-review-r2/shards/{shard}.jsonl')
 rows.update({r['id']:r for r in rr});old.update({r['id']:r for r in prev})
 cases={c['id']:c for c in L(folder+'/audit_cases.jsonl')}; src={c['id']:c for c in L(folder+'/source_cases.jsonl')};source.update(src)
 assign=J(folder+'/group_assignments.json')['groups']
 check(len(rr)==48 and len(cases)==48 and len(src)==48,'48_per_shard')
 check({r['id'] for r in rr}==set(cases)==set(src),'exact_source_audit_row_ids')
 check((B/f'pre-review-r3/shards/{shard}.jsonl').read_bytes()==(B/folder/'validation.jsonl').read_bytes(),'snapshot_raw_bytes')
 for r in rr:
  i=r['id']; c=cases[i];s=src[i]; g=c['group_id'];p=r['provenance']; a=assign[g]
  check(c=={k:v for k,v in s.items() if k!='distractors'} if shard=='geometry' else {k:v for k,v in c.items() if k!='display_order'}==s,'source_audit_identity',i)
  ans=solver['expected'](c); texts=[o['text'] for o in r['options']]; ids=[o['id'] for o in r['options']];selected=[o['text'] for o in r['options'] if o['id']==r['target_id']]
  check(len(ids)==len(set(ids)) and len(texts)==len(set(texts)) and all(ids) and all(texts),'unique_options',i)
  check(texts.count(ans)==1 and selected==[ans],'unique_expected_target_id_text',i)
  try:
   if shard=='geometry':solver['correspondence'](c,r)
   else:check(solver['stated'](c)==(r['state'],r['question']),'ordering_stated',i)
  except Exception as e:fail.append({'id':i,'correspondence':str(e)})
  check(r['group_id']==g==p['policy_instance_id']==a['policy_instance_id'] and a['mechanism_id']==c['mechanism_id']==p['mechanism_id'] and a['policy_domain']==c['policy_domain'] and i in [g+':c01',g+':c02'],'group_mapping',i)
  check(r['split']==a['split']=='validation' and p['usage']=='validation_only_never_train' and r['schema_version']=='0.1' and r['task_family']=='rule_application','contract_usage',i)
  check(r['target_id']==old[i]['target_id'] and r['state']==old[i]['state'] and r['question']==old[i]['question'] and r['group_id']==old[i]['group_id'] and r['split']==old[i]['split'],'r2_state_question_target_group_split_preserved',i)
  results.append({'id':i,'expected_text':ans,'target_id':r['target_id'],'target_text':selected[0],'text_correspondence':True})
check(len(rows)==96 and len({r['group_id'] for r in rows.values()})==48,'96_decisions_48_policies')
check(set(collections.Counter(r['group_id'] for r in rows.values()).values())=={2},'two_cases_per_policy')
check(collections.Counter(c['mechanism_id'] for c in source.values())==dict.fromkeys(['packs','rates','coordinates','cooldown','lexicographic','fifo','discount','rounding'],12),'eight_mechanisms_twelve_each')
manifest=J('pre-review-r3/manifest.json')
for entry in manifest['shards']:
 p=B/'pre-review-r3/shards'/Path(entry['path']).name
 check(H(p)==entry['sha256'] and len(p.read_text().splitlines())==entry['rows'],'manifest_hash_rows')
freeze=J('review-r3/frozen-decisions.json'); blind=[]
for d in freeze['decisions']:
 r=rows[d['id']];check(d['answer']==r['target_id'],'new_blind_agreement',d['id']);blind.append(dict(d,target_id=r['target_id'],agreement=d['answer']==r['target_id']))
check(len(blind)==13 and sum(':cooldown:' in d['id'] for d in blind)==12,'exact_13_blind_scope')
# Strict revision scope, including each exact declared old/new string.
cm=J('geometry-r3/change-map.json'); changes={c['id']:c['replacements'] for c in cm['changes'] if c['file']=='validation.jsonl'}
check(len(changes)==7 and sum(len(x) for x in changes.values())==7,'seven_changes_declared')
actual=[]
for i,r in rows.items():
 prior=old[i]; expected=copy.deepcopy(prior)
 if i in changes:
  actual.append(i)
  for ch in changes[i]:
   slots=[o for o in expected['options'] if o['text']==ch['old']]
   check(len(slots)==1 and slots[0]['id']!=expected['target_id'],'changed_slot_not_target',i)
   slots[0]['text']=ch['new']
 check(expected==r,'r2_exact_row_except_seven_wrong_clocks',i)
for fname in ['source_cases.jsonl','audit_cases.jsonl']:
 prev={c['id']:c for c in L('geometry-r2/'+fname)}; now={c['id']:c for c in L('geometry-r3/'+fname)}
 check(set(prev)==set(now),'revision_source_id_sets')
 for i,c in now.items():
  expected=copy.deepcopy(prev[i])
  if i in changes:
   for ch in changes[i]:
    expected['facts']['starts']=[ch['new'] if t==ch['old'] else t for t in expected['facts']['starts']]
    if 'distractors' in expected:expected['distractors']=[ch['new'] if t==ch['old'] else t for t in expected['distractors']]
  check(expected==c,'only_starts_and_source_distractors_changed',i)
for f in ['group_assignments.json','audit.py']:
 check((B/'geometry-r2'/f).read_bytes()==(B/'geometry-r3'/f).read_bytes(),'geometry_helper_assignments_unchanged')
plan=J('geometry-r3/rank-plan.json');rank=collections.Counter();none=[]
for i,r in rows.items():
 if ':cooldown:' not in i:continue
 target=next(o['text'] for o in r['options'] if o['id']==r['target_id']); times=sorted(o['text'] for o in r['options'] if o['text']!='No listed start fits')
 value=None if target=='No listed start fits' else times.index(target)+1
 if value is None:none.append(i);check(r==old[i],'none_target_row_unchanged',i)
 else:rank[value]+=1
 check(value==plan['assignment'][i],'rank_plan_exact',i)
check(dict(rank)=={1:4,2:4,3:3} and len(none)==1,'known_rank_counts_only')
check(H(B/'geometry-r3/rank-plan.json')==cm['rank_plan_sha256'],'change_map_rank_plan_hash')
for f,h in plan['parent_hashes'].items():check(H(B/'geometry-r2'/f)==h,'rank_plan_parent_hash')
r2=J('review-r2/frozen-decisions.json')['decisions']; r2inputs={r['id']:r for r in L('review-r2/blind-inputs.jsonl')}
non=[]
for d in r2:
 i=d['id']; check(d['answer_id']==old[i]['target_id'],'r2_56_agreement',i)
 check(r2inputs[i]=={k:old[i][k] for k in ['id','state','question','options']},'r2_reviewed_input_snapshot_identity',i)
 if ':cooldown:' not in i:
  check(r2inputs[i]=={k:rows[i][k] for k in ['id','state','question','options']},'noncooldown_reviewed_input_unchanged',i);non.append(i)
combined=set(non)|{d['id'] for d in blind};policies={rows[i]['group_id'] for i in combined}
check(len(non)==52 and len(combined)==64 and len(policies)==40,'derived_final_content_coverage')
history=J('review/review.json');check(history['blind_agreement']['matches']==31 and history['blind_agreement']['n']==32,'initial_31_32_history_preserved')
after={str(p.relative_to(B)):H(p) for p in files};check(before==after,'inputs_unchanged_during_integrity_checks')
report={'verdict':'pass' if not fail else 'must_fix','must_fix_count':len(fail),'failures':fail,'reviewer':{k:os.environ.get(k) for k in ['PI_MODEL','PI_PROVIDER']},'immutable_model_revision':None,'additional_model_calls':0,'spend':0,'new_target_hidden':{'matches':sum(d['agreement'] for d in blind),'n':len(blind),'decisions':blind},'r2_target_hidden':{'matches':56,'n':len(r2),'noncooldown_unchanged':len(non)},'final_content_coverage':{'unique_decisions':len(combined),'unique_policies':len(policies),'ids':sorted(combined)},'initial_history':{'matches':31,'n':32,'ambiguity':'packs:p06:c02 reserve doubling; retained as history, not replaced'},'scope':'96 seen-mechanism development-only decisions / 48 policies / 8 mechanisms; never train; not final held-out evidence','limitations':['Same-model-alias agreement is not independent truth.','Pure author audit reuse corroborates consistency, not independent semantic proof.','Only 13 new hidden judgments; remaining coverage carries forward inspected unchanged r2 inputs.','Existing repaired diagnostic frozen; no additional heuristic search, generation or optimization.'],'recomputed':results,'checks_actually_executed':dict(counts),'geometry_changes':actual,'cooldown_rank_counts':dict(rank),'none_target_ids':none,'frozen_decisions_sha256':H(O/'frozen-decisions.json'),'input_hashes_before':before,'input_hashes_after':after,'execution':'Standard-library local Python; inspected pure functions extracted by AST, no module top level or mains executed; no bytecode writes. No tests/lint/Git/mailbox/network/model/tokenizer/Evaluation/probe/finaldata/training content. Writes only new review-r3 files.'}
(O/'review.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(O/'review.md').write_text(f'''# D3 r3 bounded semantic / integrity review

**Verdict: {report['verdict']}; must-fix count: {len(fail)}.** Existing repaired diagnostic remains frozen; no repair proposal.

- New target-hidden judgments: **{sum(d['agreement'] for d in blind)}/13**, all 12 cooldown plus packs p06:c02. Only id/state/question/options emitted before immutable answer/rationale freeze. All have one correct rendered answer under stated policy; no unsupported convention or ambiguity found.
- Full consistency: **96/96** target IDs/texts and exact rendered state/question correspondence recomputed with inspected pure `expected` and `correspondence` / ordering `stated`; no overwrite mains or generator executed.
- Exactly **7 incorrect clock alternatives across 7 cases** changed versus r2, with faithful facts.starts and source distractor updates. All other rows/fields, state/question, policy/booking facts, target IDs/texts/slots, groups/splits, provenance, and packing clarification preserved.
- Known cooldown ascending clock ranks **4/4/3** verified against frozen rank plan; the one none-target row is unchanged. No other heuristic search performed.
- Prior r2 **56/56** agreement corroborated against frozen decisions and reviewed input snapshot. Its **52 non-cooldown** inputs are unchanged. Actual ID union with these 13 decisions yields **64 unique final-content decisions / 40 policies**, not 65 (packs overlaps).
- Historical initial **31/32** reserve-doubling ambiguity remains history; no historical artifacts edited. Same-model-alias agreement is **not independent truth**.

## Scope and provenance
All **96 decisions / 48 policies / 8 seen mechanisms** are development-only and **never train**, not final held-out evidence. Reviewer environment: `PI_MODEL={os.environ.get('PI_MODEL')}`, `PI_PROVIDER={os.environ.get('PI_PROVIDER')}`; immutable revision unavailable. No extra model calls or spend.

Frozen answers SHA-256: `{report['frozen_decisions_sha256']}`.
Geometry snapshot: `{H(B/'pre-review-r3/shards/geometry.jsonl')}`.
Ordering snapshot: `{H(B/'pre-review-r3/shards/ordering.jsonl')}`.

`review.json` contains every answer/rationale, recomputed target, check count, actual coverage ID, and before/after SHA-256 for {len(before)} inspected-scope input files. Hashes unchanged over the post-freeze integrity-check interval; no claim of a pre-session baseline. Manifest shard hashes and raw snapshot bytes match. Rank-plan parent hashes match.

Actual actions: read instructions, manifest and target-hidden projection; create new output directory and freeze; inspect audit modules and revision/rank/history records; run this standard-library bounded integrity script once. Audit AST execution includes only inspected imports/pure functions, not top-level assignments/helpers/mains. No tests, lint, Git, mailbox, network, model/tokenizer runs, Evaluation/probe/finaldata access or training-content access. No candidate or historical inputs modified. All deliberate writes confined to new `review-r3/` files.
''')
print(json.dumps({'must_fix_count':len(fail),'failures':fail,'new_blind':sum(d['agreement'] for d in blind),'coverage':[len(combined),len(policies)],'checks':sum(counts.values()),'input_files':len(before)}))
