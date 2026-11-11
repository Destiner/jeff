"""Foreground one-attempt R6 audit/predict supervision; no model work on import."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('phase', choices=('audit', 'predict'))
parser.add_argument('--grant-id')
args = parser.parse_args()
base = Path(__file__).resolve().parent
repo = Path('/Users/destiner/Code/jeff')
worktree = repo / '.worktrees/release'
runner = repo / 'experiments/research/run_order_packet.py'
packet = repo / 'artifacts/research/r6-20261111T155310Z/packet-v1'
p3 = repo / 'artifacts/release/p3-qwen-20261111-01'
pins = {
    runner: '1f3bb7bb6d652121813692db5899c434ddaba9feed9fdbfb26ade26c5a6e8599',
    packet / 'packet.json': '7598451302c5389e62476c88e7c2489fa355e0c40611e91cfbd6da1d9dc35e03',
    packet / 'inputs.jsonl': '178708cd6a620c395d29131a0eb0bad65f66f8a71e608950f7282a4e9e2ed061',
    packet / 'selection.json': '8e008f2c39e37529d32942b15eaba5e5b13cc0b9b3766f6d9b12722f15304a8f',
    packet / 'config.json': '128d550e355af4772a8f996ccb1f49675e5ba6bdc61d2ed7a1c84e11c4b6090f',
    p3 / 'audit-02/audit.json': '8e0dc65beb1c9dd5a21b2c4170853bc78bf14116429a9311c28e568c129d870a',
}
for path, expected in pins.items():
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise RuntimeError('independent source/packet/P3 audit pin mismatch: ' + str(path))
used = 0.0
if args.phase == 'predict':
    if not args.grant_id:
        raise RuntimeError('explicit Model single-use grant required')
    previous = json.loads((base / 'audit-process.json').read_text())
    audit = json.loads((base / 'audit/audit.json').read_text())
    if previous['returncode'] != 0 or previous.get('timeout') or audit['status'] != 'pass':
        raise RuntimeError('audit did not complete; no predict or retry permitted')
    used = previous['wall_seconds']
budget = 300.0 - used
if budget <= 10:
    raise RuntimeError('combined audit+predict execution budget exhausted')
command = ['/usr/bin/time', '-l', str(worktree / '.venv/bin/python'), str(runner), args.phase,
           '--inputs', str(packet / 'inputs.jsonl'), '--config', str(packet / 'config.json'),
           '--selection', str(packet / 'selection.json'), '--model-dir', str(p3 / 'download/model'),
           '--p3-audit', str(p3 / 'audit-02/audit.json'), '--audit-dir', str(base / 'audit'),
           '--train-only-confirmed']
if args.phase == 'predict':
    command.extend(['--output-dir', str(base / 'run')])
home, cache = base / (args.phase + '-home'), base / (args.phase + '-hf-cache')
home.mkdir(exist_ok=False)
cache.mkdir(exist_ok=False)
env = {'PATH': '/usr/bin:/bin', 'HOME': str(home), 'HF_HOME': str(cache),
       'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1', 'HF_DATASETS_OFFLINE': '1',
       'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1', 'HF_HUB_DISABLE_TELEMETRY': '1',
       'TOKENIZERS_PARALLELISM': 'false', 'OMP_NUM_THREADS': '4',
       'MKL_NUM_THREADS': '4', 'VECLIB_MAXIMUM_THREADS': '4', 'PYTORCH_ENABLE_MPS_FALLBACK': '0'}
record = {'phase': args.phase, 'command': command, 'cwd': str(worktree), 'environment': env,
          'grant_id': args.grant_id, 'independent_pins': {str(p): h for p, h in pins.items()},
          'wrapper_pid': os.getpid(), 'started_at': datetime.datetime.now(datetime.UTC).isoformat(),
          'previous_audit_wall_seconds': used, 'remaining_process_budget_seconds': budget,
          'term_after_seconds': budget - 5.0, 'kill_deadline_seconds': budget,
          'budget_scope': 'Sum of actual audit and predict externally supervised process wall times; queue wait excluded.',
          'supervisor_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (base / (args.phase + '-invocation.json')).open('x') as stream:
    json.dump(record, stream, indent=2); stream.write('\n')
start = time.perf_counter()
deadline = start + budget
with (base / (args.phase + '.stdout.log')).open('x') as out, (base / (args.phase + '.stderr.log')).open('x') as err:
    process = subprocess.Popen(command, cwd=worktree, env=env, stdout=out, stderr=err, start_new_session=True)
    record['child_pid'] = process.pid
    try:
        record['returncode'] = process.wait(timeout=max(0, deadline - 5.0 - time.perf_counter()))
    except subprocess.TimeoutExpired:
        record['timeout'] = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=max(0, deadline - time.perf_counter()))
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        record['returncode'] = process.returncode
record['wall_seconds'] = time.perf_counter() - start
record['combined_audit_predict_wall_seconds'] = used + record['wall_seconds']
record['completed_at'] = datetime.datetime.now(datetime.UTC).isoformat()
record['cache_files_after'] = [str(p.relative_to(cache)) for p in cache.rglob('*') if p.is_file()]
with (base / (args.phase + '-process.json')).open('x') as stream:
    json.dump(record, stream, indent=2); stream.write('\n')
print(json.dumps({k: record[k] for k in ('phase', 'returncode', 'wall_seconds', 'combined_audit_predict_wall_seconds')}))
