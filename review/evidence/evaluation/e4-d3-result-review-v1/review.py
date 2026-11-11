"""Independent, bounded real-D3 delivery review; no model/tokenizer loads."""
import os, sys, json, math, hashlib, subprocess
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
ROOT=Path('/Users/destiner/Code/jeff'); W=ROOT/'.worktrees/evaluation'; A=ROOT/'artifacts/evaluation'; O=Path(__file__).resolve().parent
PY='/Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python'
def read(p): return json.loads(Path(p).read_text())
def pin(p): return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def save(n,d):
 with (O/n).open('x') as f: json.dump(d,f,indent=2,allow_nan=False); f.write('\n')
checks=[]; pins=[]
def check(ok,msg):
 checks.append({'claim':msg,'ok':bool(ok)})
 if not ok: raise ValueError(msg)
def verify(p):
 check(pin(p['path'])['sha256']==p['sha256'],'hash '+p['path']); pins.append(p)
C=A/'e4-d3-comparison-v1'; B=A/'e4-d3-released-boundary-v1'; M=ROOT/'artifacts/model/m4-d3-inference-20261111-01'
check(sys.version_info[:2]==(3,12),'actual project Python 3.12')
pins += [pin(W/'docs/evaluation/e4-d3-seen-rules.md'),pin(W/'configs/evaluation/e4-d3-v1.json')]
for f in ['comparison.json','report.json','receipt.json','execution-pins.json','source-recheck.json']:
 pins.append(pin(C/f))
for f in ['recipe.json','pins.json','bindings.json','prepare-receipt.json','delivery-receipt.json','score_d3.py']:
 pins.append(pin(A/'e4-d3-scoring-v2'/f))
original=read(C/'comparison.json'); report=read(C/'report.json'); boundary=read(B/'boundary.json'); units=read(B/'units.json')
for k in ['reference','inputs','units']: verify(boundary[k])
for p in boundary['pins']: verify(p)
rows=[json.loads(l) for l in (B/'reference/validation.jsonl').read_text().splitlines()]; inputs=[json.loads(l) for l in (B/'inputs.jsonl').read_text().splitlines()]
check(inputs==[{k:r[k] for k in ['schema_version','id','state','question','options']} for r in rows],'exact five-field label-free export')
cases={c['case_id']:c for c in units['cases']}; policies={p['policy_instance_id']:p['case_ids'] for p in units['policies']}; mechanisms={m:[c['case_id'] for c in units['cases'] if c['mechanism_id']==m] for m in units['mechanisms']}
check(len(rows)==len(cases)==96 and len(policies)==48 and len(mechanisms)==8,'96/48/8 explicit units')
check(all(len(v)==2 for v in policies.values()) and Counter(i for ids in policies.values() for i in ids)==Counter(r['id'] for r in rows),'all 48 two-case policies partition reference')
check(all(len(v)==12 for v in mechanisms.values()) and all(sum(p['mechanism_id']==m for p in units['policies'])==6 for m in mechanisms),'eight mechanisms each 12 cases and six policies')
check(all(r['group_id']==cases[r['id']]['policy_instance_id']==cases[r['id']]['group_id'] and r['split']=='validation' and r['provenance']['label_basis']=='rule_verified' for r in rows),'explicit reference policy and label-basis mapping')
commands=[]
env=os.environ.copy();env.update(PYTHONPATH=str(W/'src'),PYTHONDONTWRITEBYTECODE='1')
args=[PY,'-B','-m','jeff.evaluation.compare','--examples',str(B/'reference/validation.jsonl'),'--output',str(O/'comparison-reproduced.json')]
for n,r in original['runs'].items():
 verify(r['prediction_file']);args += ['--predictions',n+'='+r['prediction_file']['path']]
for argv in [args,[PY,'-B','-m','jeff.evaluation.render','--comparison',str(O/'comparison-reproduced.json'),'--output',str(O/'shared-report-reproduced.md'),'--title','D3 originals: six predictors']]: 
 p=subprocess.run(argv,cwd=W,env=env,capture_output=True,text=True);commands.append({'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}); check(p.returncode==0,'actual CLI '+argv[3])
reproduced=read(O/'comparison-reproduced.json');check(reproduced==original,'entire comparison exact object equality under Python 3.12');check((O/'shared-report-reproduced.md').read_text().replace(str(O/'comparison-reproduced.json'),str(C/'comparison.json'))==(C/'shared-report.md').read_text(),'render equality except required new comparison path footer')
# Arithmetic deliberately independent of shared scoring implementation.
computed={}
def summary(ids,data):
 v=[data[i] for i in ids]; bins=[[x for x in v if min(int(x['confidence']*5),4)==b] for b in range(5)]
 return {'agreement_valid':sum(x['correct'] for x in v)/len(v),'agreement_all':sum(x['correct'] for x in v)/len(v),'coverage':1.0,'log_loss':math.fsum(x['log_loss'] for x in v)/len(v),'brier':math.fsum(x['brier'] for x in v)/len(v),'ece':math.fsum(abs(math.fsum(x['confidence']-x['correct'] for x in b)) for b in bins)/len(v)}
def compare_summary(s,expected,label):
 actual={'agreement_valid':s['top_choice']['on_valid']['value'],'agreement_all':s['top_choice']['on_all_failure_as_unsuccessful']['value'],'coverage':s['coverage']['value'],'log_loss':s['log_loss']['mean'],'brier':s['brier']['mean'],'ece':s['reliability']['ece']}
 check(all(math.isclose(actual[k],expected[k],rel_tol=1e-12,abs_tol=1e-12) for k in actual),label)
for name,run in reproduced['runs'].items():
 pred=[json.loads(l) for l in Path(run['prediction_file']['path']).read_text().splitlines()]; pp={r['id']:r for r in pred};data={}
 check(len(pred)==len(pp)==96 and set(pp)==set(cases) and run['status']=='ok' and not run['record_diagnostics'] and not run['extra_prediction_ids'] and not run['duplicate_prediction_ids'] and run['unidentifiable_records']==0,'complete zero-error raw coverage '+name)
 for row in rows:
  vals=pp[row['id']]['probabilities']; probs={v['option_id']:v['probability'] for v in vals}; ids=[o['id'] for o in row['options']]; total=sum(probs.values())
  check(len(vals)==len(probs)==len(ids) and set(probs)==set(ids) and all(math.isfinite(p) and 0<=p<=1 for p in probs.values()) and abs(total-1)<=1e-6,'valid raw probabilities '+name+' '+row['id'])
  p=[probs[i]/total for i in ids]; chosen=max(range(len(ids)),key=lambda j:p[j]);correct=ids[chosen]==row['target_id']
  data[row['id']]={'correct':correct,'confidence':p[chosen],'log_loss':-math.log(p[ids.index(row['target_id'])]),'brier':math.fsum((p[j]-(i==row['target_id']))**2 for j,i in enumerate(ids))}
 compare_summary(run['overall'],summary(list(cases),data),'independent overall math '+name)
 for key,mapping,macrokey in [('per_policy',policies,'equal_policy_macro'),('per_mechanism',mechanisms,'equal_mechanism_macro')]:
  ss=[]
  for unit,ids in mapping.items():
   s=summary(ids,data);ss.append(s);compare_summary(report['runs'][name][key][unit],s,'independent '+name+' '+unit)
  for field in ss[0]:
   m=report['runs'][name][macrokey][field]
   check(m['units']==len(mapping) and m['finite_units']==len(mapping) and m['undefined_units']==m['positive_infinity_units']==0 and m['status']=='finite' and math.isclose(m['mean'],math.fsum(s[field] for s in ss)/len(mapping),abs_tol=1e-12),'all-unit macro '+name+' '+macrokey+' '+field)
 computed[name]={'overall':summary(list(cases),data),'correct':sum(x['correct'] for x in data.values()),'cases':data}
pairs={}
def pair(ids,a,b):
 return {'total_cases':len(ids),'common_valid':len(ids),'unpaired':0,'wins':sum(not a[i]['correct'] and b[i]['correct'] for i in ids),'losses':sum(a[i]['correct'] and not b[i]['correct'] for i in ids),'both_correct':sum(a[i]['correct'] and b[i]['correct'] for i in ids),'both_wrong':sum(not a[i]['correct'] and not b[i]['correct'] for i in ids)}
for start,trained in [('minilm_start','minilm_trained'),('msmarco_start','msmarco_trained')]:
 a=computed[start]['cases'];b=computed[trained]['cases']; claimed=report['paired_own_start_to_trained'][trained];full=Counter(wins=0,losses=0,both_correct=0,both_wrong=0,incomplete=0)
 check(pair(list(cases),a,b)==claimed['cases'],'paired case totals '+trained)
 for unit,ids in policies.items():
  x=all(a[i]['correct'] for i in ids);y=all(b[i]['correct'] for i in ids);v=pair(ids,a,b);v.update(start_full_2_of_2=x,trained_full_2_of_2=y)
  check(v==claimed['per_policy'][unit],'policy pair '+trained+' '+unit);full['wins' if y and not x else 'losses' if x and not y else 'both_correct' if x and y else 'both_wrong']+=1
 check(dict(full)==claimed['full_policy_2_of_2'] and claimed['total_policies']==48,'full 2/2 policy transitions '+trained)
 for m,ids in mechanisms.items():check(pair(ids,a,b)==claimed['per_mechanism'][m],'mechanism pairs '+trained+' '+m)
 pairs[trained]={'cases':pair(list(cases),a,b),'full_policy_2_of_2':dict(full),'start_complete':full['losses']+full['both_correct'],'trained_complete':full['wins']+full['both_correct']}
# Recheck published execution bindings without reading model weights or tokenizer assets.
pre=read(M/'preflight.json'); aggregate=read(M/'receipt.json');verify({'path':str(M/'execute.py'),'sha256':aggregate['script_sha256']})
check(pre['input']['sha256']==pin(B/'inputs.jsonl')['sha256'],'preflight frozen input')
for p in pre['release_receipts']:verify(p)
receipts=[];inventory_count=0
for name,item in read(A/'e4-d3-scoring-v2/bindings.json').items():
 verify(item['receipt']);r=read(item['receipt']['path']);check(r in aggregate['jobs'],'aggregate receipt '+name)
 for key in ['input','output','checkpoint_inventory']: verify(r[key])
 check(r['input']['path']==str(B/'inputs.jsonl') and r['input']['rows']==r['output']['rows']==96 and r['output']['path']==original['runs'][name]['prediction_file']['path'],'receipt original files '+name)
 check(r['fresh_process'] is True and r['exit_code']==0 and r['checkpoint_files_unchanged'] is True and math.isfinite(r['process_wall_seconds']) and r['process_wall_seconds']>=0,'published success claims '+name)
 cp=ROOT/'artifacts/model/m4-v2-20261111-01'/read(W/'configs/evaluation/e4-d3-v1.json')['checkpoint_directories'][name]
 check(r['checkpoint']==str(cp),'checkpoint directory identity '+name)
 for flag,value in [('--input',str(B/'inputs.jsonl')),('--output',r['output']['path']),('--checkpoint',str(cp))]:check(r['command'].count(flag)==1 and r['command'][r['command'].index(flag)+1]==value,'receipt command '+name+' '+flag)
 before=Path(r['checkpoint_inventory']['path']);after=M/(r['snapshot']+'-inventory-after.json');check(before.read_bytes()==after.read_bytes(),'inventory record equality '+name);pins.append(pin(after)); inv=read(before);inventory_count+=len(inv)
 for e in inv:check((cp/e['path']).stat().st_size==e['bytes'],'inventory current size '+name+' '+e['path'])
 meta=read(cp/'checkpoint.json');verify({'path':str(cp/'checkpoint.json'),'sha256':next(e['sha256'] for e in inv if e['path']=='checkpoint.json')});check(meta['max_length']==256,'metadata native cap '+name)
 audit=pre['token_audits'][r['snapshot']];check(audit['pairs']==361 and audit['full_pair_max']==129 and audit['over_budget_pairs']==0 and audit['native_cap']==256 and audit['tokenizer_sha256']==next(e['sha256'] for e in inv if e['path']=='tokenizer/tokenizer.json'),'published token audit binding '+name)
 check(datetime.fromisoformat(boundary['completed_at'])<datetime.fromisoformat(pre['created_at'])<=datetime.fromisoformat(r['started_at'])<datetime.fromisoformat(r['completed_at']),'pre-outcome boundary '+name);receipts.append(r)
check(inventory_count==30,'30 inventory file sizes, no tensor/tokenizer content reads')
save('independent-metrics.json',{'runs':computed,'pairs':pairs})
save('audit.json',{'completed_at':datetime.now(timezone.utc).isoformat(),'python':sys.version,'executable':sys.executable,'checks':checks,'pins':pins,'commands':commands,'receipts':receipts,'boundary_provenance':{k:boundary[k] for k in ['completed_at','exclusion','label_provenance','limitations','data_limitations']},'outputs':[pin(O/f) for f in ['comparison.json','shared-report.md','comparison-reproduced.json','shared-report-reproduced.md','independent-metrics.json']],'status':'no_blockers','tensor_bytes_attested':False,'tokenizer_loaded':False,'additional_spend_gbp':0})
print(json.dumps({'checks':len(checks),'all_ok':all(c['ok'] for c in checks),'counts':{n:r['correct'] for n,r in computed.items()},'pairs':pairs,'outputs':str(O)},indent=2))
