"""Actual bounded process supervisor; never retries or launches another model."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
name, seconds = sys.argv[1], int(sys.argv[2])
command = sys.argv[3:]
worktree = Path('/Users/destiner/Code/jeff/.worktrees/model')
home = root / f'{name}-home'
home.mkdir(exist_ok=False)
env = {'PATH': os.environ['PATH'], 'HOME': str(home), 'LANG': 'en_US.UTF-8',
       'JEFF_ARTIFACTS_DIR': '/Users/destiner/Code/jeff/artifacts',
       'HF_HOME': str(home / 'hf'), 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
       'TOKENIZERS_PARALLELISM': 'false', 'PYTHONDONTWRITEBYTECODE': '1'}
receipt = {'command': command, 'cwd': str(worktree), 'maximum_seconds': seconds,
           'started_at': datetime.now(timezone.utc).isoformat(),
           'env_keys': sorted(env), 'initially_empty_home': str(home), 'automatic_retry': False}
with (root / f'{name}-invocation.json').open('x') as f: json.dump(receipt, f, indent=2)
start = time.monotonic()
with (root / f'{name}.stdout').open('x') as stdout, (root / f'{name}.stderr').open('x') as stderr:
    child = subprocess.Popen(command, cwd=worktree, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
    receipt.update(wrapper_pid=os.getpid(), child_pid=child.pid, timeout=False)
    try:
        child.wait(timeout=max(1, seconds-10))
    except subprocess.TimeoutExpired:
        receipt['timeout'] = True
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()
    receipt.update(returncode=child.returncode, process_wall_seconds=time.monotonic()-start,
                   completed_at=datetime.now(timezone.utc).isoformat())
with (root / f'{name}-process.json').open('x') as f: json.dump(receipt, f, indent=2)
print(json.dumps(receipt, indent=2))
raise SystemExit(1 if receipt['timeout'] else child.returncode)
