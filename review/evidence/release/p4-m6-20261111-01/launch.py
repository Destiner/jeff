"""One externally supervised P4 pass, only after Model's explicit grant."""
import argparse
import datetime
import json
import os
from pathlib import Path
import signal
import subprocess
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--model-dir', required=True, type=Path)
parser.add_argument('--audit-dir', required=True, type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent
worktree = Path('/Users/destiner/Code/jeff/.worktrees/release')
python = worktree / '.venv/bin/python'
command = ['/usr/bin/time', '-l', str(python), '-m', 'jeff.runtime.qwen_challenger',
           'predict', '--audit-dir', str(args.audit_dir.resolve()), '--model-dir', str(args.model_dir.resolve()),
           '--output-dir', str(base / 'run'), '--device', 'mps']
for name in ('run-home', 'empty-hf-cache'):
    (base / name).mkdir(exist_ok=False)
env = {'PATH': '/usr/bin:/bin', 'HOME': str(base / 'run-home'),
       'HF_HOME': str(base / 'empty-hf-cache'), 'HF_HUB_OFFLINE': '1',
       'TRANSFORMERS_OFFLINE': '1', 'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1',
       'HF_HUB_DISABLE_TELEMETRY': '1', 'TOKENIZERS_PARALLELISM': 'false',
       'OMP_NUM_THREADS': '4', 'MKL_NUM_THREADS': '4', 'VECLIB_MAXIMUM_THREADS': '4'}
record = {'command': command, 'environment': env, 'cwd': str(worktree),
          'started_at': datetime.datetime.now(datetime.UTC).isoformat(), 'wrapper_pid': os.getpid(),
          'timeout_seconds': 300, 'termination_grace_seconds': 10,
          'timing_scope': 'External wall includes interpreter/import/hash-tokenization preflight/model load/startup/full pass/output.'}
with (base / 'process-invocation.json').open('x') as f:
    json.dump(record, f, indent=2); f.write('\n')
start = time.perf_counter()
with (base / 'process.stdout.log').open('x') as out, (base / 'process.stderr.log').open('x') as err:
    process = subprocess.Popen(command, cwd=worktree, env=env, stdout=out, stderr=err, start_new_session=True)
    record['child_pid'] = process.pid
    try:
        record['returncode'] = process.wait(timeout=300)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        record['returncode'] = process.returncode
        record['timeout'] = True
record['wall_seconds'] = time.perf_counter() - start
record['completed_at'] = datetime.datetime.now(datetime.UTC).isoformat()
record['cache_files_after'] = [str(p.relative_to(base / 'empty-hf-cache')) for p in (base / 'empty-hf-cache').rglob('*') if p.is_file()]
with (base / 'process-receipt.json').open('x') as f:
    json.dump(record, f, indent=2); f.write('\n')
print(json.dumps({'returncode': record['returncode'], 'wall_seconds': record['wall_seconds']}))
