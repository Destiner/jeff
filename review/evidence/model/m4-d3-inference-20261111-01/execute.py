"""Frozen E4 D3 original-only inference on four preserved M4 snapshots."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
from tokenizers import Tokenizer

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
OUT = ROOT / 'model/m4-d3-inference-20261111-01'
WORKTREE = Path('/Users/destiner/Code/jeff/.worktrees/model')
SOURCE = ROOT / 'evaluation/e4-d3-released-boundary-v1/inputs.jsonl'
EXPECTED = 'afd02eb196889f79384488fa1998dcb95c79d96dccd1235a70fd30940c2bf928'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')

def inventory(path):
    return [{'path': str(p.relative_to(path)), 'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(path.rglob('*')) if p.is_file()]

if sha(SOURCE) != EXPECTED:
    raise ValueError('Released input changed')
rows = [json.loads(line) for line in SOURCE.read_text().splitlines()]
if len(rows) != 96 or len({r['id'] for r in rows}) != 96:
    raise ValueError('Released row/ID count mismatch')
for row in rows:
    if set(row) != {'schema_version', 'id', 'state', 'question', 'options'}:
        raise ValueError('Non-decision fields in inference input')
    if any(set(option) != {'id', 'text'} for option in row['options']):
        raise ValueError('Non-decision option fields')

boundaries = []
for path, expected in (
    (ROOT / 'data/data-d3-seen-rules-v1/release/manifest.json', 'd74bfda56fc18c89c4a40852dd46d9ec8bce1c907c9ebc8cbc979f23d9047ca9'),
    (ROOT / 'evaluation/e4-d3-released-boundary-v1/boundary.json', '6202826900d634440598d370fc1cef0972c65aab45bcff92a2f2cceb95adc06e'),
):
    if sha(path) != expected:
        raise ValueError('Release/boundary receipt hash mismatch')
    boundaries.append({'path': str(path), 'sha256': expected})

queue = []
audits = {}
for architecture in ('minilm', 'msmarco'):
    for stage in ('baseline', 'checkpoint'):
        name = f'{architecture}-{stage}'
        checkpoint = ROOT / 'model/m4-v2-20261111-01' / architecture / stage
        tokenizer_file = checkpoint / 'tokenizer/tokenizer.json'
        tokenizer = Tokenizer.from_file(str(tokenizer_file))
        tokenizer.no_padding()
        tokenizer.no_truncation()
        lengths = [len(tokenizer.encode(f"State:\n{row['state']}\nQuestion:\n{row['question']}",
                                        f"Candidate:\n{option['text']}").ids)
                   for row in rows for option in row['options']]
        if max(lengths) > 256:
            raise ValueError('D3 exceeds native cap256; do not silently truncate')
        audits[name] = {'tokenizer_sha256': sha(tokenizer_file), 'pairs': len(lengths),
                        'full_pair_min': min(lengths), 'full_pair_max': max(lengths),
                        'native_cap': 256, 'over_budget_pairs': 0}
        queue.append((name, checkpoint))

save(OUT / 'preflight.json', {'created_at': datetime.now(timezone.utc).isoformat(),
                             'input': {'path': str(SOURCE), 'sha256': EXPECTED, 'rows': 96},
                             'release_receipts': boundaries, 'token_audits': audits,
                             'code_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=WORKTREE, text=True).strip(),
                             'predictor_sha256': sha(WORKTREE / 'src/jeff/model/predict.py')})
(OUT / 'logs').mkdir()
receipts = []
for name, checkpoint in queue:
    before = inventory(checkpoint)
    inventory_file = OUT / f'{name}-inventory-before.json'
    save(inventory_file, before)
    output = OUT / f'{name}-predictions.jsonl'
    cache = OUT / 'empty-reload-cache' / name
    cache.mkdir(parents=True)
    env = os.environ.copy()
    env.update(JEFF_ARTIFACTS_DIR=str(ROOT), HF_HOME=str(cache), HF_HUB_OFFLINE='1',
               TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
    command = ['uv', 'run', '--locked', '--extra', 'model', 'python', '-m', 'jeff.model.predict',
               '--checkpoint', str(checkpoint), '--input', str(SOURCE), '--output', str(output),
               '--device', 'mps', '--batch-size', '4']
    receipt = {'snapshot': name, 'checkpoint': str(checkpoint), 'input': {'path': str(SOURCE), 'sha256': EXPECTED, 'rows': 96},
               'checkpoint_inventory': {'path': str(inventory_file), 'sha256': sha(inventory_file)},
               'command': command, 'cwd': str(WORKTREE), 'fresh_process': True,
               'initially_empty_hf_home': str(cache), 'offline_environment': True,
               'started_at': datetime.now(timezone.utc).isoformat()}
    save(OUT / f'{name}-invocation.json', receipt)
    started = time.monotonic()
    with (OUT / 'logs' / f'{name}.stdout').open('x') as stdout, (OUT / 'logs' / f'{name}.stderr').open('x') as stderr:
        result = subprocess.run(command, cwd=WORKTREE, env=env, stdout=stdout, stderr=stderr, timeout=120)
    receipt.update(exit_code=result.returncode, process_wall_seconds=time.monotonic()-started,
                   completed_at=datetime.now(timezone.utc).isoformat())
    after = inventory(checkpoint)
    save(OUT / f'{name}-inventory-after.json', after)
    receipt['checkpoint_files_unchanged'] = before == after
    if result.returncode == 0:
        receipt['output'] = {'path': str(output), 'sha256': sha(output), 'rows': len(output.read_bytes().splitlines())}
        if receipt['output']['rows'] != 96 or sha(SOURCE) != EXPECTED:
            raise ValueError('Input/coverage mismatch')
    save(OUT / f'{name}-receipt.json', receipt)
    if result.returncode or not receipt['checkpoint_files_unchanged']:
        raise SystemExit('Inference failed or checkpoint changed; preserve all evidence')
    receipts.append(receipt)
    print(json.dumps({'snapshot': name, 'rows': 96, 'process_wall_seconds': receipt['process_wall_seconds']}), flush=True)

save(OUT / 'receipt.json', {'jobs': receipts, 'script_sha256': sha(Path(__file__)),
                           'scope': 'Four original-only inference jobs; no training, labels, tuning or reversal replay',
                           'additional_spend_gbp': 0, 'active_jobs': 0})
