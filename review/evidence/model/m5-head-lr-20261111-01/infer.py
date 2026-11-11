"""Execute four authorized fresh offline M5 predictions and check its starting control."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
RUN = ROOT / 'model/m5-head-lr-20261111-01'
WORKTREE = Path('/Users/destiner/Code/jeff/.worktrees/model')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, data):
    with path.open('x') as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write('\n')

def inventory(path):
    return [{'path': str(p.relative_to(path)), 'sha256': sha(p), 'bytes': p.stat().st_size}
            for p in sorted(path.rglob('*')) if p.is_file()]

inputs = {name: item for name, item in zip(('original', 'probes'),
          json.loads((RUN / 'preflight.json').read_text())['inputs'])}
out = RUN / 'inference'
out.mkdir()
receipts = []
for stage in ('baseline', 'checkpoint'):
    checkpoint = RUN / 'training' / stage
    before = inventory(checkpoint)
    save(out / f'{stage}-checkpoint-before.json', before)
    for suite, item in inputs.items():
        source = Path(item['path'])
        if sha(source) != item['sha256']:
            raise ValueError('Input hash changed')
        name = f'{stage}-{suite}'
        destination = out / f'{name}-predictions.jsonl'
        cache = RUN / 'empty-reload-cache' / name
        cache.mkdir(parents=True)
        command = ['uv', 'run', '--locked', '--extra', 'model', 'python', '-m', 'jeff.model.predict',
                   '--checkpoint', str(checkpoint), '--input', str(source), '--output', str(destination),
                   '--device', 'mps', '--batch-size', '8']
        env = os.environ.copy()
        env.update(JEFF_ARTIFACTS_DIR=str(ROOT), HF_HOME=str(cache), HF_HUB_OFFLINE='1',
                   TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
        receipt = {'job': name, 'command': command, 'cwd': str(WORKTREE), 'input': item,
                   'checkpoint': str(checkpoint), 'checkpoint_inventory': str(out / f'{stage}-checkpoint-before.json'),
                   'checkpoint_inventory_sha256': sha(out / f'{stage}-checkpoint-before.json'),
                   'started_at': datetime.now(timezone.utc).isoformat(), 'fresh_process': True,
                   'initially_empty_hf_home': str(cache), 'offline_environment': True}
        save(out / f'{name}.invocation.json', receipt)
        started = time.monotonic()
        with (RUN / 'logs' / f'{name}.stdout.log').open('x') as stdout, (RUN / 'logs' / f'{name}.stderr.log').open('x') as stderr:
            result = subprocess.run(command, cwd=WORKTREE, env=env, stdout=stdout, stderr=stderr, timeout=120)
        receipt.update(exit_code=result.returncode, process_wall_seconds=time.monotonic()-started,
                       completed_at=datetime.now(timezone.utc).isoformat())
        if result.returncode == 0:
            receipt['output'] = {'path': str(destination), 'sha256': sha(destination),
                                 'rows': len(destination.read_bytes().splitlines())}
            if receipt['output']['rows'] != item['rows'] or sha(source) != item['sha256']:
                raise ValueError('Input/coverage mismatch')
        receipt['checkpoint_files_unchanged'] = inventory(checkpoint) == before
        save(out / f'{name}.receipt.json', receipt)
        if result.returncode or not receipt['checkpoint_files_unchanged']:
            raise SystemExit('Inference failed or checkpoint changed; retain evidence')
        receipts.append(receipt)
        print(json.dumps({'job': name, 'rows': receipt['output']['rows'], 'wall_seconds': receipt['process_wall_seconds']}), flush=True)

comparisons = {}
for suite in inputs:
    historical = ROOT / 'model/msmarco-256-inference-20261111-01' / f'baseline-{suite}-predictions.jsonl'
    current = out / f'baseline-{suite}-predictions.jsonl'
    def probabilities(path):
        return {r['id']: {o['option_id']: o['probability'] for o in r['probabilities']}
                for r in map(json.loads, path.read_text().splitlines())}
    left, right = probabilities(historical), probabilities(current)
    if left.keys() != right.keys() or any(left[k].keys() != right[k].keys() for k in left):
        raise ValueError('Starting prediction identity mismatch')
    delta = max(abs(left[k][o]-right[k][o]) for k in left for o in left[k])
    comparisons[suite] = {'historical': str(historical), 'historical_sha256': sha(historical),
                          'current': str(current), 'current_sha256': sha(current),
                          'byte_identical': historical.read_bytes() == current.read_bytes(),
                          'max_absolute_probability_difference': delta, 'rows': len(left)}
    if delta > 1e-6:
        raise ValueError('Fresh starting predictions not comparable; do not interpret intervention')
save(out / 'starting-prediction-comparison.json', comparisons)
save(out / 'receipt.json', {'script_sha256': sha(Path(__file__)), 'jobs': receipts,
                           'starting_predictions': comparisons, 'additional_spend_gbp': 0, 'active_jobs': 0})
print(json.dumps({'starting_predictions': comparisons}))
