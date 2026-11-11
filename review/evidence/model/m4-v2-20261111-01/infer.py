"""Execute the fixed M4 fresh-process inference queue; no training or scoring."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
RUN = ROOT / 'model/m4-v2-20261111-01'
WORKTREE = Path('/Users/destiner/Code/jeff/.worktrees/model')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')

inputs = {
    'combined': ROOT / 'evaluation/e3-v2-assembly-v1/inputs.jsonl',
    'reversed': ROOT / 'evaluation/e3-v2-order-v1/reversed-inputs.jsonl',
    'probes': ROOT / 'evaluation/e3-v2-freeze-v1/probes/inputs.jsonl',
    'new': ROOT / 'evaluation/e3-v2-freeze-v1/new-v2/inputs.jsonl',
    'new-reversed': ROOT / 'evaluation/e3-v2-new-order-v1/reversed-inputs.jsonl',
}
pins = {item['path']: item for item in json.loads((RUN / 'input-receipt.json').read_text())['inputs']}
for path in inputs.values():
    if digest(path) != pins[str(path)]['sha256']:
        raise ValueError(f'Input changed: {path}')

out = RUN / 'inference'
out.mkdir()
queue = []
for architecture in ('minilm', 'msmarco'):
    for stage in ('baseline', 'checkpoint'):
        for suite in ('combined', 'reversed', 'probes'):
            queue.append((f'{architecture}-{stage}-{suite}', RUN / architecture / stage, suite))
for name, checkpoint in (
    ('m2', ROOT / 'model/pilot-256-20261111-01/checkpoint'),
    ('m3', ROOT / 'model/msmarco-256-20261111-01/checkpoint'),
):
    for suite in ('new', 'new-reversed'):
        queue.append((f'{name}-{suite}', checkpoint, suite))

receipts = []
for name, checkpoint, suite in queue:
    destination = out / f'{name}.jsonl'
    cache = RUN / 'empty-reload-cache' / name
    cache.mkdir(parents=True)
    command = ['uv', 'run', '--locked', '--extra', 'model', 'python', '-m', 'jeff.model.predict',
               '--checkpoint', str(checkpoint), '--input', str(inputs[suite]),
               '--output', str(destination), '--device', 'mps', '--batch-size', '4']
    env = os.environ.copy()
    env.update(JEFF_ARTIFACTS_DIR=str(ROOT), HF_HOME=str(cache), HF_HUB_OFFLINE='1',
               TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
    receipt = {'job': name, 'suite': suite, 'command': command, 'cwd': str(WORKTREE),
               'checkpoint': str(checkpoint), 'input': pins[str(inputs[suite])],
               'started_at': datetime.now(timezone.utc).isoformat(),
               'fresh_process': True, 'initially_empty_hf_home': str(cache),
               'offline_environment': True, 'timeout_seconds': 120}
    save(out / f'{name}.invocation.json', receipt)
    started = time.monotonic()
    with (RUN / 'logs' / f'{name}.stdout.log').open('x') as stdout, (RUN / 'logs' / f'{name}.stderr.log').open('x') as stderr:
        result = subprocess.run(command, cwd=WORKTREE, env=env, stdout=stdout, stderr=stderr, timeout=120)
    receipt.update(exit_code=result.returncode, process_wall_seconds=time.monotonic()-started,
                   completed_at=datetime.now(timezone.utc).isoformat())
    if result.returncode == 0:
        receipt['output'] = {'path': str(destination), 'sha256': digest(destination),
                             'rows': len(destination.read_bytes().splitlines())}
        if receipt['output']['rows'] != receipt['input']['rows']:
            raise ValueError(f'Coverage mismatch: {name}')
        if digest(inputs[suite]) != receipt['input']['sha256']:
            raise ValueError(f'Input changed during inference: {name}')
    save(out / f'{name}.receipt.json', receipt)
    if result.returncode:
        raise SystemExit(result.returncode)
    receipts.append(receipt)
    print(json.dumps({'job': name, 'rows': receipt['output']['rows'],
                      'process_wall_seconds': receipt['process_wall_seconds']}), flush=True)

save(out / 'receipt.json', {'created_at': datetime.now(timezone.utc).isoformat(),
                           'script_sha256': digest(Path(__file__)), 'jobs': receipts,
                           'additional_spend_gbp': 0, 'active_jobs': 0})
