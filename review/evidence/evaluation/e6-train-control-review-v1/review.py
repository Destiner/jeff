"""Bounded saved-evidence analysis; standard library only; no model imports."""
import collections
import datetime
import hashlib
import json
import math
import pathlib
import random
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path('/Users/destiner/Code/jeff/artifacts')
RUN = ROOT / 'model/m6-qwen-20261111-01'
REPO = pathlib.Path('/Users/destiner/Code/jeff/.worktrees/evaluation')
REV = 'dafd5d235b53af341fbf539e4bf32dcf09a399f2'
checks = []
pins = {}
def check(name, value, detail=None):
    checks.append({'name': name, 'ok': bool(value), 'detail': detail})
def digest(p):
    p = pathlib.Path(p)
    if p.stat().st_size > 30_000_000 or p.name in {'tokenizer.json','tokenizer_config.json','vocab.json','merges.txt'}:
        raise ValueError('forbidden weight/tokenizer read')
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    pins[str(p)] = {'sha256': h, 'bytes': p.stat().st_size}
    return h
def load(p):
    return json.loads(pathlib.Path(p).read_text())
def rows(p):
    return [json.loads(s) for s in pathlib.Path(p).read_text().splitlines() if s.strip()]
def save(name, obj):
    with (OUT/name).open('x') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')
def gitfile(name):
    return subprocess.check_output(['git','show',REV+':'+name], cwd=REPO)

receipt = load(RUN/'training/receipt.json')
audit = load(RUN/'train-audit/audit.json')
proof = audit['evidence']
freeze = load(RUN/'full-run-freeze.json')
manifest = load(RUN/'training/checkpoint-manifest.json')
capacity = load(RUN/'capacity/receipt.json')
process = load(RUN/'train-process.json')
cap_process = load(RUN/'capacity-process.json')
for p in ['training/receipt.json','train-audit/audit.json','full-run-freeze.json','training/checkpoint-manifest.json','capacity/receipt.json','train-process.json','capacity-process.json','training/fit-before.jsonl','training/fit-after.jsonl','training/online.jsonl','train-audit/schedule.jsonl','train-invocation.json','starting/receipt.json','control-audit/audit.json','control-inputs.json']:
    digest(RUN/p)
check('exact published checkpoint manifest SHA256',digest(RUN/'training/checkpoint-manifest.json')=='1fe8f6d169301c76698b78b8d7b067c4b10868fb755324896352d1f61310960f')
check('completed source-run receipt hash',digest(manifest['source_run_receipt']['path'])==manifest['source_run_receipt']['sha256'])
for name,p in freeze['receipt_pins'].items():
    check('full-run freeze pin '+name, digest(p['path'])==p['sha256'])
control_freeze=load(RUN/'comparison-freeze.json')
for k in ['e6_input_binding','e6_plan','p3_audit']:
    p=control_freeze[k];check('control freeze '+k,digest(p['path'])==p['sha256'])
source_checks=[]
for name, expected in proof['source']['tracked_files'].items():
    actual=hashlib.sha256(gitfile(name)).hexdigest()
    source_checks.append({'path':name,'expected':expected,'git_blob_sha256':actual,'matches':actual==expected})
check('all recorded tracked source byte pins match exact Git revision',all(x['matches'] for x in source_checks),len(source_checks))
check('source revision across freeze/audit/checkpoint',all(x==REV for x in [freeze['source_revision'],proof['source']['revision'],manifest['training_code_revision']]))
for name in ['src/jeff/training/qwen_decision.py','src/jeff/training/qwen_data.py','src/jeff/runtime/qwen_challenger.py']:
    check('source preserved in recorded tracked pins '+name,name in proof['source']['tracked_files'])
check('recipe Git bytes/hash',hashlib.sha256(gitfile('configs/model/m6-qwen.json')).hexdigest()==proof['recipe_sha256']==manifest['training_recipe_sha256'])
check('P3 config Git bytes/hash',hashlib.sha256(gitfile('configs/runtime/p3-qwen.json')).hexdigest()==proof['p3_scoring_config_sha256']==manifest['p3_scoring_config_sha256'])
check('training identity exactly matches capacity',receipt['identity']==capacity['identity'])
check('training identity binds audit',receipt['identity']['audit_sha256']==digest(RUN/'train-audit/audit.json') and receipt['identity']['evidence']==proof)
check('1500/375 complete without extra backward',receipt['status']=='complete' and (receipt['presentations'],receipt['optimizer_steps'],receipt['extra_backwards'])==(1500,375,0))
check('final all-parameter Adam step',receipt['adam_final_state']=={'state_tensors':290,'moment_bytes':3952262144,'step':375})
check('parameter inventory 290/494032768',receipt['parameters']['unique_tensors']==290 and receipt['parameters']['trainable']==receipt['parameters']['total']==494032768)
check('selected parameter fingerprints all changed',all(receipt['initial_parameter_fingerprints'][k]!=v for k,v in receipt['final_parameter_fingerprints'].items()),{'initial':receipt['initial_parameter_fingerprints'],'final':receipt['final_parameter_fingerprints']})
check('capacity separate process exited before training',cap_process['returncode']==0 and not cap_process['timeout'] and cap_process['child_pid']!=process['child_pid'] and cap_process['completed_at']<process['started_at'])
check('capacity disposable 1 step +4 extra backwards',capacity['status']=='complete' and (capacity['presentations'],capacity['optimizer_steps'],capacity['extra_backwards'])==(4,1,4))
check('process complete without retry/timeout',process['returncode']==0 and not process['timeout'] and not process['automatic_retry'])

# Read only authorized TRAIN shards; retain no copied cases or labels in output.
data_manifest=load(proof['data']['manifest_path'])
check('authorized data manifest bytes',digest(proof['data']['manifest_path'])==proof['data']['manifest_sha256']==manifest['training_data_manifest_sha256'])
train=[]
for shard in data_manifest['shards']:
    if shard['split']!='train':
        continue
    p=ROOT/shard['path']
    check('TRAIN shard bytes '+shard['path'],digest(p)==shard['sha256'])
    batch=rows(p)
    check('TRAIN shard count/split '+shard['path'],len(batch)==shard['rows'] and all(r['split']=='train' for r in batch))
    train.extend(batch)
check('1500 unique authorized TRAIN IDs',len(train)==len({r['id'] for r in train})==1500)
rng=random.Random(42)
rng.shuffle(train)
schedule=rows(RUN/'train-audit/schedule.jsonl')
check('schedule hash across freeze/audit/receipt/manifest',len({digest(RUN/'train-audit/schedule.jsonl'),audit['schedule_sha256'],freeze['schedule_sha256'],receipt['identity']['schedule_sha256'],manifest['training_schedule_sha256']})==1)
check('schedule length',len(schedule)==1500)
schedule_errors=[]
for i,(original,s) in enumerate(zip(train,schedule)):
    opts=list(original['options']);rng.shuffle(opts)
    expected={k:original[k] for k in ['schema_version','id','state','question']};expected['options']=[{'id':o['id'],'text':o['text']} for o in opts]
    good=(s['index']==i and s['id']==original['id'] and s['decision']==expected and s['target_id']==original['target_id'] and s['target_position']==[o['id'] for o in opts].index(original['target_id']) and s['option_ids']==[o['id'] for o in opts] and s['original_option_ids']==[o['id'] for o in original['options']] and s['family']==original['task_family'] and s['group_id']==original['group_id'] and s['provenance']==original['provenance'] and s['input_tokens']==len(s['prompt_tokens'])<=1024 and s['prompt_token_sha256']==hashlib.sha256(json.dumps(s['prompt_tokens']).encode()).hexdigest() and s['answer_ids']==list(range(32,32+len(opts))))
    if not good:schedule_errors.append(i)
check('exact seed42 row+option replay/identity/metadata/token inventory',not schedule_errors,{'mismatched_indices':schedule_errors,'tokenizer_not_executed':True})

def aggregate(rs):
    n=len(rs);return {'rows':n,'agreements':sum(r['agreement'] for r in rs),'mean_ce':sum(r['ce'] for r in rs)/n,'ce_sum':sum(r['ce'] for r in rs),'predicted_position_counts':dict(collections.Counter(str(r['predicted_position']) for r in rs)),'target_position_counts':dict(collections.Counter(str(r['target_position']) for r in rs))}
def grouped(rs,key):
    d=collections.defaultdict(list)
    for r in rs:d[key(r)].append(r)
    return {k:aggregate(v) for k,v in sorted(d.items())}
fit={}
for phase in ['before','after']:
    rs=rows(RUN/f'training/fit-{phase}.jsonl')
    check('fit '+phase+' complete same schedule metadata',len(rs)==1500 and all(r['index']==s['index'] and r['id']==s['id'] and r['option_ids']==s['option_ids'] and r['target_position']==s['target_position'] and r['family']==s['family'] and r['group_id']==s['group_id'] and r['source']==s['provenance']['source'] and type(r['agreement']) is bool and r['agreement']==(r['predicted_position']==r['target_position']) and 0<=r['predicted_position']<len(s['option_ids']) and math.isfinite(r['ce']) and r['ce']>=0 for r,s in zip(rs,schedule)))
    summary={'overall':aggregate(rs),'by_family':grouped(rs,lambda r:r['family']),'by_source_group':grouped(rs,lambda r:json.dumps([r['source'],r['group_id']])),'by_source':grouped(rs,lambda r:r['source']),'by_target_position':grouped(rs,lambda r:str(r['target_position'])),'by_family_target_position':grouped(rs,lambda r:json.dumps([r['family'],r['target_position']]))}
    for section in ['overall','by_family','by_source_group']:
        reported=receipt['fit_'+phase][section]
        buckets=[(summary[section],reported)] if section=='overall' else [(v,reported[k]) for k,v in summary[section].items()]
        check('fit '+phase+' independently reproduces receipt '+section,all(all(b[k]==v for k,v in a.items()) for a,b in buckets) and (section=='overall' or set(summary[section])==set(reported)))
    check('fit '+phase+' row pin',digest(RUN/f'training/fit-{phase}.jsonl')==receipt['fit_'+phase]['rows_sha256'])
    fit[phase]=summary
check('all post-training argmax position0',fit['after']['overall']['predicted_position_counts']=={'0':1500})
online=rows(RUN/'training/online.jsonl')
check('online schedule+375 groups of four',len(online)==1500 and all(r['index']==i and r['id']==schedule[i]['id'] and r['update']==i//4+1 and math.isfinite(r['ce']) for i,r in enumerate(online)))
check('online pin and mean',digest(RUN/'training/online.jsonl')==receipt['online_rows_sha256'] and sum(r['ce'] for r in online)/1500==receipt['online_mean_ce'])

controls=[]
for suite,p in control_freeze['p3_control_outputs'].items():
    new=RUN/f'starting/{suite}.jsonl'
    old_hash=digest(p['path']);new_hash=digest(new)
    a=rows(p['path']);b=rows(new)
    ai={r['id']:r for r in a};bi={r['id']:r for r in b}
    deltas=[];ties=[0,0];changes=0
    for case in ai.keys() & bi.keys():
        probs=[]
        for j,rr in enumerate([ai[case],bi[case]]):
            pp={p['option_id']:p['probability'] for p in rr['probabilities']};probs.append(pp)
            ties[j]+=sum(v==max(pp.values()) for v in pp.values())>1
        if probs[0].keys()!=probs[1].keys():raise ValueError('control option mismatch')
        deltas.extend(abs(v-probs[1][k]) for k,v in probs[0].items())
        changes+=({k for k,v in probs[0].items() if v==max(probs[0].values())}!={k for k,v in probs[1].items() if v==max(probs[1].values())})
    detail={'suite':suite,'rows':len(a),'unique_old':len(ai),'unique_new':len(bi),'bytes_equal':old_hash==new_hash==p['sha256'],'same_ids':ai.keys()==bi.keys(),'max_absolute_probability_delta':max(deltas),'changed_top_sets':changes,'ties_old_new':ties}
    controls.append(detail);check('independent control equality '+suite,detail['bytes_equal'] and detail['same_ids'] and len(a)==len(b)==len(ai)==len(bi),detail)
control_inputs=load(RUN/'control-inputs.json')
for d in control_inputs['datasets']:
    check('frozen label-free control input '+d['name'],digest(d['path'])==d['sha256'] and len(rows(d['path']))==d['rows'])

inventory=[]
for name,item in manifest['files'].items():
    p=RUN/'training/checkpoint'/name
    inventory.append({'path':name,'actual_bytes':p.stat().st_size,'published_sha256':item['sha256'],'content_not_read':True})
    check('checkpoint inventory size '+name,p.stat().st_size==item['bytes'] and receipt['checkpoint_files'][name]==item)
check('exact checkpoint file inventory',set(manifest['files'])=={p.name for p in (RUN/'training/checkpoint').iterdir() if p.is_file()})
check('tokenizer pins unchanged across source/receipt/manifest',proof['tokenizer_assets']==receipt['tokenizer_assets']==manifest['tokenizer_assets'])
resources={}
for label,d in [('training',receipt),('capacity',capacity)]:
    samples=d['memory_samples']; fields=['cpu_lifetime_rss_bytes','mps_current_bytes','mps_driver_bytes','mps_recommended_headroom_bytes']
    resources[label]={'process_runtime_seconds':d['process_runtime_seconds'],'sample_count':len(samples),'sample_stages':dict(collections.Counter(x['stage'] for x in samples))}
    for field in fields:
        vals=[x[field] for x in samples if field in x]
        resources[label][field]={'samples':len(vals),'min':min(vals) if vals else None,'max':max(vals) if vals else None}
    resources[label]['qualification']='MPS discrete observed samples, not peaks. CPU ru_maxrss is process-lifetime RSS, not an additive concurrent allocation. Never sum CPU RSS and MPS.'
resources['external_training_wall_seconds']=process['process_wall_seconds']
resources['external_capacity_wall_seconds']=cap_process['process_wall_seconds']
resources['capacity_projection']=capacity['projection']
save('fit-aggregates.json',fit)
save('source-pins.json',source_checks)
save('controls.json',controls)
save('resources.json',resources)
save('checkpoint-inventory.json',inventory)
save('receipt.json',{'schema_version':'e6.train-control-independent-review.v1','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python_executable':sys.executable,'source_revision':REV,'checks':checks,'failed_checks':[x for x in checks if not x['ok']],'input_pins':pins,'fit_ties':'unknown: fit rows save only CE/argmax, no probabilities/logits','probability_variance':'unknown: no per-option fixed-fit probabilities/logits saved','online_mean_ce':receipt['online_mean_ce'],'limits':'saved evidence and exact source review do not attest actual historical loaded tensor execution; no weight/tokenizer content reads, inference, network, final data, tests, lint, compilation or package build'})
print(json.dumps({'checks':len(checks),'failed':[x for x in checks if not x['ok']],'fit':{k:v['overall'] for k,v in fit.items()},'controls':controls,'resources':{k:{kk:vv for kk,vv in v.items() if kk!='sample_stages'} if isinstance(v,dict) else v for k,v in resources.items()}},indent=2))
