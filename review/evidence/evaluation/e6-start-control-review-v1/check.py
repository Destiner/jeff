"""CPU-only actual artifact verification; no model/tokenizer/reference access."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, hashlib, math, subprocess
from datetime import datetime, timezone
ROOT = Path('/Users/destiner/Code/jeff')
WT = ROOT / '.worktrees/evaluation'
sys.path.insert(0, str(WT / 'src'))
from jeff.evaluation.metrics import validate_prediction
from jeff.evaluation.common import validate_input
OUT = ROOT / 'artifacts/evaluation/e6-start-control-review-v1'
M = ROOT / 'artifacts/model/m6-qwen-20261111-01'
E = ROOT / 'artifacts/evaluation/e6-predeclared-v1'
pins = {}
def sha(p):
    p = Path(p)
    assert p.stat().st_size < 5_000_000, 'bounded reads only'
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    pins[str(p)] = h
    return h
def unique(pairs):
    d = {}
    for k,v in pairs:
        assert k not in d, 'duplicate JSON key'
        d[k] = v
    return d
def load(p):
    sha(p)
    return json.loads(Path(p).read_text(), object_pairs_hook=unique)
def rows(p):
    sha(p)
    return [json.loads(s, object_pairs_hook=unique) for s in Path(p).read_text().splitlines()]
f = load(M/'comparison-freeze.json'); declared = load(E/'receipt.json')
for pin in [f['e6_plan'], f['e6_input_binding'], f['p3_audit'], declared['plan'], declared['inputs']]:
    assert sha(pin['path']) == pin['sha256']
manifest = load(M/'control-inputs.json'); einputs = load(E/'inputs.json')
audit = load(M/'control-audit/audit.json'); fresh = load(M/'starting/receipt.json')
old_audit = load(f['p3_audit']['path']); old_receipt = load(ROOT/'artifacts/release/p3-qwen-20261111-01/run-02/receipt.json')
a = audit['evidence']; b = old_audit['evidence']
assert audit['status'] == fresh['status'] == old_audit['status'] == old_receipt['status'] == 'complete'
assert fresh['evidence'] == a
assert fresh['audit_sha256'] == sha(M/'control-audit/audit.json')
for key in ['config','config_sha256','source_sha256','model_assets','chat_template_sha256','environment','suites','input_manifest','input_manifest_sha256']:
    assert a[key] == b[key], key
assert a['model_assets'] == f['p3_model_assets']
assert a['git_status'] == b['git_status'] == ''
assert sha(a['config_path']) == a['config_sha256']
assert sha(M/'control-inputs.json') == a['input_manifest_sha256']
assert a['config']['max_input_tokens'] == 1024
assert old_receipt['evidence'] == b
source_path = 'src/jeff/runtime/qwen_challenger.py'
source = subprocess.check_output(['git','show',a['git_revision']+':'+source_path],cwd=WT)
assert hashlib.sha256(source).hexdigest() == a['source_sha256']
old_source = subprocess.check_output(['git','show',b['git_revision']+':'+source_path],cwd=WT)
assert source == old_source
source_diff = subprocess.check_output(['git','diff',b['git_revision'],a['git_revision'],'--',source_path],cwd=WT,text=True)
assert source_diff == ''
assert sha(ROOT/'.worktrees/model'/source_path) == a['source_sha256']
reports=[]; seen=set()
for entry, frozen_input, sa, sb, run, oldrun in zip(manifest['datasets'], einputs['inputs'], a['suites'], b['suites'],fresh['suites'],old_receipt['suites'],strict=True):
    name=entry['name']; assert entry == {k:frozen_input[k] for k in entry}
    assert sha(entry['path']) == entry['sha256']
    inputs=rows(entry['path']); oldpath=Path(f['p3_control_outputs'][name]['path']); newpath=M/'starting'/f'{name}.jsonl'
    old=rows(oldpath); new=rows(newpath)
    assert len(inputs)==len(old)==len(new)==entry['rows']
    assert sha(oldpath)==f['p3_control_outputs'][name]['sha256']
    assert sha(newpath)==run['output_sha256']==oldrun['output_sha256']
    assert len({r['id'] for r in inputs})==len(inputs)
    assert len({r['id'] for r in old})==len(old) and len({r['id'] for r in new})==len(new)
    om={r['id']:r for r in old}; nm={r['id']:r for r in new}
    assert set(om)==set(nm)=={r['id'] for r in inputs}
    assert sa==sb and sa['input']==entry
    tokens={r['id']:r for r in sa['rows']}; assert set(tokens)==set(om) and len(tokens)==len(sa['rows'])
    deltas=[]; changed_top=changed_choice=ties_old=ties_new=changed_ties=0; deviations=[]
    for row in inputs:
        assert set(row)=={'schema_version','id','state','question','options'}
        validate_input(row)
        assert row['id'] not in seen; seen.add(row['id'])
        probs=[]
        for pred in [om[row['id']],nm[row['id']]]:
            assert set(pred)=={'schema_version','id','probabilities'}
            # Shared validator's normalized return is deliberately discarded.
            _, deviation=validate_prediction(pred,row); deviations.append(deviation)
            probs.append({p['option_id']:p['probability'] for p in pred['probabilities']})
        p,q=probs
        deltas.extend(abs(p[k]-q[k]) for k in p)
        pt={k for k in p if p[k]==max(p.values())};qt={k for k in q if q[k]==max(q.values())}
        changed_top+=pt!=qt; changed_ties+=(len(pt)>1)!=(len(qt)>1)
        ties_old+=len(pt)>1;ties_new+=len(qt)>1
        ordered=[o['id'] for o in row['options']]
        changed_choice+=next(k for k in ordered if k in pt)!=next(k for k in ordered if k in qt)
        token=tokens[row['id']]
        assert token['answer_token_ids']==list(range(32,32+len(ordered)))
        assert 0<token['input_tokens']<=1024
        assert len(token['prompt_token_sha256'])==64
    assert sum(t['input_tokens'] for t in sa['rows'])==run['input_tokens']==run['expected_input_tokens']
    assert run['status']=='complete' and run['written_rows']==len(inputs) and run['coverage']==1
    report=dict(suite=name,rows=len(inputs),option_probabilities=len(deltas),input_sha256=entry['sha256'],prediction_sha256=sha(newpath),byte_identical=oldpath.read_bytes()==newpath.read_bytes(),max_absolute_raw_delta=max(deltas),mean_absolute_raw_delta=math.fsum(deltas)/len(deltas),nonzero_deltas=sum(d!=0 for d in deltas),changed_top_sets=changed_top,changed_input_order_tiebroken_choices=changed_choice,p3_ties=ties_old,fresh_ties=ties_new,changed_tie_presence=changed_ties,max_sum_deviation=max(deviations),token_lengths=sa['lengths'],input_tokens=run['input_tokens'],full_token_audit_rows=len(tokens),overflows=0)
    assert report['byte_identical'] and max(deltas)<=f['tolerance_absolute_probability'] and changed_top==changed_choice==changed_ties==0
    reports.append(report)
assert len(seen)==624
process=load(M/'starting-process.json'); invocation=load(M/'starting-invocation.json'); ap=load(M/'control-audit-process.json')
assert all(process[k]==v for k,v in invocation.items())
assert process['returncode']==ap['returncode']==0 and not process['timeout'] and not process['automatic_retry']
assert declared['declared_at'] < ap['started_at'] < ap['completed_at'] < process['started_at'] < process['completed_at']
comparison=load(M/'starting-comparison.json');assert comparison['passes'] and comparison['freeze_sha256']==sha(M/'comparison-freeze.json')
for r,c in zip(reports,comparison['suites'],strict=True):
    assert r['suite']==c['suite'] and r['rows']==c['rows'] and r['prediction_sha256']==c['new_sha256']==c['old_sha256']
sha(M/'compare-start.py')
handoffs=[ROOT/'artifacts/handoffs/evaluation/20261111-e6-predeclared-M6-P4-inputs.md',ROOT/'artifacts/handoffs/model/20261111T1546-M6-start-control-ready.md']
for p in handoffs: sha(p)
chronology={}
for p in [E/'plan.md',E/'receipt.json',M/'comparison-freeze.json',M/'control-audit/audit.json',M/'starting/receipt.json',*handoffs]:
    stat=p.stat();chronology[str(p)]={'mtime_utc':datetime.fromtimestamp(stat.st_mtime,timezone.utc).isoformat(),'birthtime_utc':datetime.fromtimestamp(stat.st_birthtime,timezone.utc).isoformat()}
sha(Path(__file__));sha(WT/'src/jeff/evaluation/metrics.py');sha(WT/'src/jeff/evaluation/common.py')
result={'schema_version':'e6-start-control-independent-review/1','checked_at':datetime.now(timezone.utc).isoformat(),'interpreter':sys.executable,'evaluation_git_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=WT,text=True).strip(),'blocking_findings':[],'verdict':'No blocking finding for starting-control artifact comparability; runtime attestation limits apply. Not a training gate.','suites':reports,'total_rows':len(seen),'total_option_probabilities':sum(r['option_probabilities'] for r in reports),'raw_probabilities_used':True,'normalization_for_comparison':False,'model_loads':0,'tokenizer_loads':0,'reference_rows_read':0,'weight_files_read':0,'network_calls':0,'source':{'p3_git_revision':b['git_revision'],'fresh_git_revision':a['git_revision'],'sha256':a['source_sha256'],'git_diff':source_diff,'source_bytes_identical':True},'semantic_pins':{k:a[k] for k in ['config','config_sha256','chat_template_sha256','model_assets','environment']},'chronology':{'declared_at':declared['declared_at'],'audit_started_at':ap['started_at'],'audit_completed_at':ap['completed_at'],'starting_started_at':process['started_at'],'starting_completed_at':process['completed_at'],'starting_wall_seconds':process['process_wall_seconds'],'filesystem':chronology,'qualification':'Mutable local timestamps and owner handoff claims, not cryptographic precommitment or proof of loaded tensors.'},'qualifications':['Artifact equality does not independently attest fresh execution, actual loaded tensor identity, or remote authenticity of base assets. Recorded weight hash compared only; no weight rehash.','Recorded complete prompt token hashes/boundaries compared across all 624 rows; no fresh tokenizer computation.','Shared validator validates both sets, but its normalized return is discarded. Raw stored numbers alone determine equivalence.','Only visible control attempt evidence reviewed; no global proof that no unrecorded attempts exist. Existing owner receipts remain untouched.','No trained outcomes, training data, labels, quality scores, final references or mailbox accessed. Model owns independent ongoing training; no review gate.'],'artifact_sha256':pins}
with (OUT/'receipt.json').open('x') as stream: json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
print(json.dumps({'rows':result['total_rows'],'option_probabilities':result['total_option_probabilities'],'suites':reports,'chronology':result['chronology']},indent=2))
