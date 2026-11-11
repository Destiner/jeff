"""Close this bounded observation; no polling, sleep, model or data changes."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ARTIFACTS = OUT.parent.parent
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
session = json.loads((OUT/'session.json').read_text())
start = datetime.fromisoformat(session['started_at'].replace('Z','+00:00'))
deadline = datetime.fromisoformat(session['deadline'].replace('Z','+00:00'))
now = datetime.now(timezone.utc)
if now < deadline:
    raise SystemExit('Original observation window has not ended; do not close or invent coverage.')
events = [json.loads(line) for line in (OUT/'observations.jsonl').read_text().splitlines()]
last_check = max(datetime.fromisoformat(e['at']) for e in events if e['event']=='inbox_check')
initial = json.loads((OUT/'flow-integrity-check-01.json').read_text())
checks = {name:sha(ARTIFACTS/name)==item['sha256'] for name,item in initial['checks'].items()}
comparison = json.loads((OUT/'target-comparison.json').read_text())
checks['selection.json'] = sha(OUT/'selection.json')==comparison['selection_sha256']
checks['selected-reference.jsonl'] = sha(OUT/'selected-reference.jsonl')==comparison['reference_sha256']
checks['blind-review/judgments.json'] = sha(OUT/'blind-review/judgments.json')==comparison['judgments_sha256']
blind = json.loads((OUT/'blind-review/judgments.json').read_text())
checks['blind-inputs.jsonl'] = sha(OUT/'blind-inputs.jsonl')==blind['input_sha256']
closing = {
 'task':'D4','started_at':session['started_at'],'original_deadline':session['deadline'],
 'last_observation_check_at':last_check.isoformat(),'closure_recorded_at':now.isoformat(),
 'elapsed_minutes':round((last_check-start).total_seconds()/60,3),
 'timing_note':'Coverage ends at the last actual observation check before the original deadline. Closure validation/reporting is administrative, not an extension of D4.',
 'integrity_checks':checks,'integrity_valid':all(checks.values()),
 'inbox_checks_lower_bound':max(e.get('check_number',0) for e in events),
 'inbox_accounting_limit':'One early selection-metadata inbox check is unnumbered; numbered count is a conservative lower bound, not complete telemetry.',
 'requested_foreground_wait_seconds':sum(e.get('foreground_wait_seconds',0) for e in events),
 'completed_subagents':4,'active_data_subagents':0,'active_data_jobs':0,'background_observers_created':0,
 'outbound_peer_reports':{'research':'0b69e467-8c31-4232-b936-93a43e568222','model':'0e29a37c-4f37-430c-bdf1-adb26937dd4b'},
 'decision_sample':24,'source_groups':14,'blind_agreement':comparison['agreement'],
 'demonstrated_label_spec_defects':0,'production_code_fixes':0,'frozen_dataset_changes':0,
 'additional_spend_gbp':0,'pending_spend_gbp':0,
 'limits':['Procedural target hiding, not OS isolation','Same exposed reviewer/source model alias, not independent ground truth',
           'Paired purposive TRAIN slice, not whole-dataset semantic clearance','No causal model improvement or counterfactual time-saved estimate',
           'Observation stops now; no extension or background monitoring promise']}
with (OUT/'closure.json').open('x') as stream:
    json.dump(closing,stream,indent=2);stream.write('\n')
with (OUT/'observations.jsonl').open('a') as stream:
    stream.write(json.dumps({'at':now.isoformat(),'event':'closed','last_observation_check_at':last_check.isoformat(),'elapsed_minutes':closing['elapsed_minutes'],
       'integrity_valid':closing['integrity_valid'],'checks':len(checks),'note':'Original support window ended. No observer process or subagent retained; reporting only follows.'})+'\n')
print(json.dumps(closing,indent=2))
if not closing['integrity_valid']:
    raise SystemExit('Actual frozen-data/audit integrity mismatch: report explicitly; do not silently repair.')
