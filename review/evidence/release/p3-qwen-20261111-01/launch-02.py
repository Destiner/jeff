"""One supervised, explicitly scheduled P3 process; no retries."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import time

BASE = Path(__file__).resolve().parent
WORKTREE = Path('/Users/destiner/Code/jeff/.worktrees/release')
PYTHON = WORKTREE / '.venv/bin/python'
command = ['/usr/bin/time', '-l', str(PYTHON), '-m', 'jeff.runtime.qwen_challenger',
           'predict', '--audit-dir', str(BASE / 'audit-02'), '--model-dir', str(BASE / 'download/model'),
           '--output-dir', str(BASE / 'run-02'), '--device', 'mps']
env = {'PATH': '/usr/bin:/bin', 'HOME': str(BASE / 'run-home-02'),
       'HF_HOME': str(BASE / 'empty-hf-cache'), 'HF_HUB_OFFLINE': '1',
       'TRANSFORMERS_OFFLINE': '1', 'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1',
       'HF_HUB_DISABLE_TELEMETRY': '1', 'TOKENIZERS_PARALLELISM': 'false',
       'OMP_NUM_THREADS': '4', 'MKL_NUM_THREADS': '4', 'VECLIB_MAXIMUM_THREADS': '4'}
(BASE / 'run-home-02').mkdir(exist_ok=False)
start = time.perf_counter()
record = {'command': command, 'environment': env, 'cwd': str(WORKTREE),
          'started_at': datetime.datetime.now(datetime.UTC).isoformat(),
          'wrapper_pid': os.getpid(), 'timeout_seconds': 1300,
          'timing_scope': 'Includes time wrapper/interpreter/import/preflight/model load/startup/steady pass/output.'}
with (BASE / 'process-02-invocation.json').open('x') as f:
    json.dump(record, f, indent=2); f.write('\n')
with (BASE / 'process-02.stdout.log').open('x') as out, (BASE / 'process-02.stderr.log').open('x') as err:
    proc = subprocess.Popen(command, cwd=WORKTREE, env=env, stdout=out, stderr=err, start_new_session=True)
    try:
        record['child_pid'] = proc.pid
        record['returncode'] = proc.wait(timeout=1300)
    except subprocess.TimeoutExpired:
        import signal
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
        record['returncode'] = proc.returncode
        record['timeout'] = True
record['wall_seconds'] = time.perf_counter() - start
record['completed_at'] = datetime.datetime.now(datetime.UTC).isoformat()
with (BASE / 'process-02-receipt.json').open('x') as f:
    json.dump(record, f, indent=2); f.write('\n')
print(json.dumps({'returncode': record['returncode'], 'wall_seconds': record['wall_seconds']}))
