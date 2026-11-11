import sys
sys.dont_write_bytecode=True
import json,hashlib,pathlib,importlib.util,collections,ast
from fractions import Fraction as F
B=pathlib.Path(__file__).resolve().parent; R=B.parent; A=R.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
lines=lambda p:[json.loads(l) for l in p.read_text().splitlines()]
# Explicit allowed input trees only; no historical, training, probe, or final files.
paths=[p for d in ['pre-review-r2','ordering','geometry','ordering-r2','geometry-r2'] for p in (R/d).rglob('*') if p.is_file() and '__pycache__' not in str(p)]
before={str(p):sha(p) for p in paths}; (B/'input-hashes-before.json').write_text(json.dumps(before,indent=2)+'\n')
fail=[]; checks=collections.Counter(); result=[]; mappings=[]; diffs=[]
def ck(ok,name,id=None):
 checks[name]+=1
 if not ok:fail.append(dict(check=name,id=id))
manifest=load(R/'pre-review-r2/manifest.json'); prov=load(R/'pre-review-r2/provenance.json'); meta={r['id']:r for r in load(R/'pre-review-r2/case-metadata.json')['cases']}
for s in manifest['shards']:
 p=A/s['path'];ck(sha(p)==s['sha256'],'snapshot_manifest_hash',str(p));ck(len(lines(p))==s['rows']==48,'snapshot_row_count',str(p))
for src in prov['sources']:
 for name,h in src['sha256'].items():ck(sha(A/name)==h,'raw_revision_provenance_hash',name)
allrows=[]; oldrows=[]; caseidx={}
for producer in ['geometry','ordering']:
 new=R/(producer+'-r2');old=R/producer
 spec=importlib.util.spec_from_file_location(producer+'_pure',new/'audit.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 rows=lines(R/'pre-review-r2/shards'/f'{producer}.jsonl'); orig=lines(old/'validation.jsonl'); cases=lines(new/'audit_cases.jsonl'); sources=lines(new/'source_cases.jsonl');groups=load(new/'group_assignments.json')['groups']
 ck((new/'validation.jsonl').read_bytes()==(R/'pre-review-r2/shards'/f'{producer}.jsonl').read_bytes(),'snapshot_raw_byte_identity',producer)
 ck((new/'audit.py').read_bytes()==(old/'audit.py').read_bytes(),'pure_helper_parent_identity',producer)
 ck((new/'group_assignments.json').read_bytes()==(old/'group_assignments.json').read_bytes(),'assignments_parent_identity',producer)
 for fn in ['source_cases.jsonl','audit_cases.jsonl']:
  aa=lines(old/fn);bb=lines(new/fn)
  for a,b in zip(aa,bb):
   changed=[k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)]
   if changed:diffs.append(dict(producer=producer,file=fn,id=b['id'],fields=changed))
   ck(not changed if producer=='ordering' else (not changed or (b['id'].endswith(':packs:p06:c02') and changed==['context'])),'structured_source_change_scope',b['id'])
 for row,prior,c,src in zip(rows,orig,cases,sources):
  rid=row['id']; caseidx[rid]=c;g=groups[row['group_id']];cm=meta[rid]
  answer=mod.expected(c); texts=[o['text'] for o in row['options']]; chosen=next(o['text'] for o in row['options'] if o['id']==row['target_id'])
  ck(texts.count(answer)==1 and chosen==answer,'pure_expected_unique_target',rid)
  if producer=='geometry':mod.correspondence(c,row);ok=True
  else:ok=(row['state'],row['question'])==mod.stated(c)
  ck(ok,'pure_rendered_correspondence',rid)
  ck(c=={k:v for k,v in src.items() if k!='distractors'} if producer=='geometry' else {k:v for k,v in c.items() if k!='display_order'}==src,'source_audit_correspondence',rid)
  ck(rid==c['id']==src['id'] and rid in [c['group_id']+':c01',c['group_id']+':c02'] and row['group_id']==c['group_id']==g['policy_instance_id']==cm['group_id']==cm['policy_instance_id']==row['provenance']['policy_instance_id'] and c['mechanism_id']==g['mechanism_id']==cm['mechanism_id']==row['provenance']['mechanism_id'] and c['policy_domain']==g['policy_domain']==cm['policy_domain'],'case_policy_mechanism_mapping',rid)
  ck(row['split']==g['split']==cm['split']=='validation' and cm['intentional_mechanism_overlap'] and cm['permanently_training_excluded'] and row['provenance']['usage']=='validation_only_never_train','seen_validation_usage',rid)
  ck(row['target_id']==prior['target_id'] and chosen==next(o['text'] for o in prior['options'] if o['id']==prior['target_id']),'labels_preserved',rid)
  ck([o['id'] for o in row['options']]==[o['id'] for o in prior['options']],'ordered_option_ids_preserved',rid)
  changed=[k for k in row if row[k]!=prior[k]]
  if producer=='ordering':
   ck(set(changed)<=set(['options','provenance']),'row_change_scope',rid)
   ck({k:v for k,v in row['provenance'].items() if k not in ['source','teacher_model']}=={k:v for k,v in prior['provenance'].items() if k not in ['source','teacher_model']},'provenance_only_optional_fields',rid)
  else:ck(not changed or (rid.endswith(':packs:p06:c02') and changed==['state']),'row_change_scope',rid)
  for o,po in zip(row['options'],prior['options']):
   if o['text']!=po['text']:diffs.append(dict(producer=producer,file='validation.jsonl',id=rid,option_id=o['id'],old=po['text'],new=o['text']));ck(o['id']!=row['target_id'] and c['mechanism_id'] in ['fifo','discount','rounding'],'changed_only_wrong_options',rid)
  result.append(dict(id=rid,expected_text=answer,target_text=chosen,text_correspondence=ok));mappings.append(dict(id=rid,policy_group=c['group_id'],mechanism=c['mechanism_id']))
 allrows+=rows;oldrows+=orig
 if producer=='ordering':
  refs=load(new/'parent_refs.json')['file_sha256']
 else:refs=load(new/'revision_map.json')['parent_hashes']
 for name,h in refs.items():ck(sha(old/name)==h,'recorded_parent_hash',producer+'/'+name)
freeze=load(B/'frozen-decisions.json');idx={r['id']:r for r in allrows}
for d in freeze['decisions']:ck(d['answer_id']==idx[d['id']]['target_id'],'frozen_blind_target_agreement',d['id'])
ck(len(allrows)==len(idx)==96 and len({r['group_id'] for r in allrows})==48 and len({c['mechanism_id'] for c in caseidx.values()})==8,'96_rows_48_policies_8_seen')
ck(set(collections.Counter(r['group_id'] for r in allrows).values())=={2},'two_cases_per_policy')
ck(len([d for d in diffs if d['file']=='validation.jsonl'])==87,'87_changed_distractor_texts')
# Pure selected construction functions from the fully inspected revision script;
# no top-level generation/revision/main is executed. Independently compare every
# result to the saved wrong slot, feasibility and stated error description.
tree=ast.parse((R/'ordering-r2/revise.py').read_text()); ns={'F':F}
for name in ['discount_value','rounded','allocation']:
 node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
 exec(compile(ast.Module(body=[node],type_ignores=[]),'<inspected-pure-construction>','exec'),ns)
distr=[]
for d in load(R/'ordering-r2/distractor_constructions.json'):
 c=caseidx[d['id']];r=idx[d['id']];m=c['mechanism_id'];err=d['rule_error'];t=d['text']
 if m=='discount':value=ns['discount_value'](c,err);ok=value==F(t[1:])
 elif m=='rounding':value=ns['rounded'](c['facts']['value'],err['grid'],err['mode']);ok=value==F(t.split()[0]) and t.split()[1]==c['policy']['unit']
 else:
  ok=ns['allocation'](c,err['priority'])==t
  take={x.rsplit(' ',1)[0]:int(x.rsplit(' ',1)[1]) for x in t.split('; ')};stock={b[0]:b[2] for b in c['facts']['batches']}
  ok=ok and sum(take.values())==c['facts']['request'] and all(0<=take[n]<=stock[n] for n in stock)
 ck(ok and next(o['text'] for o in r['options'] if o['id']==d['option_id'])==t and d['option_id']!=r['target_id'],'per_distractor_rationale_and_value',d['id']+'/'+d['option_id'])
 distr.append(dict(**d,construction_matches=ok,semantic_assessment='Plausible explicit rule misapplication, not an additional supported answer.'))
ck(len(distr)==96 and len({d['id'] for d in distr})==36,'all_36_choice_sets_96_wrong_slots')
# Choice-only descriptive priors. All ties resolve to first supplied option.
def stats(rows):
 out={}
 for m in sorted({r['id'].split(':')[2] for r in rows}):
  ss=[r for r in rows if r['id'].split(':')[2]==m];z=collections.Counter();ranks=collections.Counter();slots=collections.Counter();details=[]
  for r in ss:
   ts=[o['text'] for o in r['options']];i=next(j for j,o in enumerate(r['options']) if o['id']==r['target_id']);ls=list(map(len,ts));slots[i+1]+=1
   z['first']+=i==0
   for fn,key in [(min,'shortest'),(max,'longest')]:
    ties=[j for j,x in enumerate(ls) if x==fn(ls)];z[key+'_first_tie']+=i==ties[0];z[key+'_fractional']+=1/len(ties) if i in ties else 0;z[key+'_strict']+=ties==[i]
   detail={'id':r['id'],'target_slot':i+1,'lengths':ls}
   if m in ['packs','discount','rounding','cooldown']:
    nums=[F(t[1:]) if m=='discount' else F(t.split()[0]) if m!='cooldown' else F(10**6) if t=='No listed start fits' else F(int(t[:2])*60+int(t[3:])) for t in ts]
    rank=sorted(nums).index(nums[i])+1;ranks[rank]+=1
    z['numeric_min']+=i==nums.index(min(nums));z['numeric_max']+=i==nums.index(max(nums));z['numeric_interior']+=1<rank<len(nums);z['numeric_lower_median']+=nums[i]==sorted(nums)[(len(nums)-1)//2]
    detail['numeric_rank']=rank
    if m=='discount':
     cand=[j for j,v in enumerate(nums) if v+1 in nums and v-2 in nums];z['v_plus1_minus2_unique']+=len(cand)==1;z['v_plus1_minus2_correct']+=cand==[i]
   if m=='fifo':
    zeros=[sum(int(x.rsplit(' ',1)[1])==0 for x in t.split('; ')) for t in ts];z['most_zeros']+=i==zeros.index(max(zeros));z['fewest_zeros']+=i==zeros.index(min(zeros));detail['zeros']=zeros
   if m in ['rates','lexicographic']:
    c=caseidx[r['id']];order=c.get('candidate_order',c.get('display_order'));z['first_displayed_candidate']+=ts[i]==order[0]
   details.append(detail)
  out[m]=dict(rows=len(ss),counts=dict(z),target_slots=dict(slots),numeric_ranks=dict(ranks),per_row=details)
 return out
newstats=stats(allrows);oldstats=stats(oldrows)
# Hash refs in metadata, revision manifest, freeze: report bounded local refs only.
hashrefs=[]
for p in [R/'ordering-r2/manifest.json',R/'ordering-r2/metadata.json',R/'geometry-r2/metadata.json',R/'pre-review-r2/freeze.json']:
 obj=load(p)
 def walk(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if isinstance(v,str) and len(v)==64 and all(c in '0123456789abcdef' for c in v) and (p.parent/k).is_file():
     ok=sha(p.parent/k)==v;ck(ok,'local_metadata_hash',str(p.parent/k));hashrefs.append(dict(record=str(p),file=k,match=ok))
    else:walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 # Parent hashes and parent_generation_settings refer to the ORIGINAL directory,
 # not this revision. They were checked separately above; do not rebase them.
 if p.name=='manifest.json':walk(obj['files'])
 elif p.name=='metadata.json':walk(obj['generation_settings']['hashes'])
 else:walk(obj['files_sha256'])
after={str(p):sha(p) for p in paths};ck(before==after,'read_only_input_hash_preservation');(B/'input-hashes-after.json').write_text(json.dumps(after,indent=2)+'\n')
report=dict(status='pass_with_residual_limits' if not fail else 'must_fix',counts=dict(rows=96,policies=48,mechanisms=8,blind_rows=56,blind_agreement=sum(d['answer_id']==idx[d['id']]['target_id'] for d in freeze['decisions'])),checks=dict(checks),failures=fail,must_fix_findings=fail,frozen_decisions_sha256=sha(B/'frozen-decisions.json'),frozen_decisions=freeze,expected_and_correspondence=result,mappings=mappings,field_changes=diffs,distractor_review=distr,choice_only=dict(original=oldstats,revised=newstats,tie_rule='First supplied option; length fractional credit also reported. Cooldown No listed start fits ordered after times for numeric-rank diagnostics only.'),hash_references=hashrefs,input_hashes_preserved=before==after,input_file_count=len(before),historical_record='Original initial review finding remains 31/32 (as supplied by user); no historical review data opened. This r2 pass does not overwrite or retrospectively erase it.',limitations=['56 direct target-hidden judgments, not 96 independent text judgments; remaining 40 receive structured expected/correspondence checks.','Same teacher alias agreement is not independent groundtruth; pure helper recomputation is separate-algorithm consistency, not independent authorship.','96 rows / 48 paired policies / 8 intentionally seen mechanisms; not iid, unseen-mechanism, or final evidence.','Revised developmental candidate after exposed shortcut diagnostics; not untouched validation.','Wrong rounding grids are valid distractors but often eliminable by grid membership; coarse grids can be less attractive than neighboring-grid errors.','FIFO low-demand depletion signatures and discount numeric-rank priors remain. No optimization or rewriting performed.'],commands=['Read AGENTS.md and docs/contracts.md with read tool.','python3 target-hidden projection (id/state/question/options only); broad initial projection followed by exact 56-row blind-inputs.jsonl.','python3 review-r2/freeze.py (run once before source/target inspection).','find candidate base -maxdepth 3 -type f (listing only after freeze).','read revised audit.py, revise.py, revision.py, distractor_constructions.json, provenance.json and case metadata.','python3 -B review-r2/check.py (two runs; first over-broad metadata recursion misresolved embedded parent hashes as revision hashes; reviewer script corrected to check explicit local maps, with parent refs separately checked. No input changed. Pure expected/stated/correspondence and extracted pure distractor functions only; no mains).'],boundaries=dict(tests=False,lint=False,git=False,mailbox=False,network=False,models=False,additional_spend_gbp=0,evaluation_probe_final_data_access=False,writes='New review-r2 files only'))
(B/'review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],failures=fail,checks=dict(checks),blind=report['counts'],new={m:{k:v for k,v in s.items() if k!='per_row'} for m,s in newstats.items()},old_discount=oldstats['discount']['counts'],hash_preserved=before==after),indent=2))
