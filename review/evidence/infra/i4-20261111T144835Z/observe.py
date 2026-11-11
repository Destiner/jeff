"""One foreground I4 evidence capture per manual invocation; no polling loop."""

from datetime import datetime, timezone
import json
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT = Path('/Users/destiner/Code/jeff')
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from jeff.coordination import mailbox

started = datetime.now(timezone.utc).isoformat()
tick = time.perf_counter()
before = resource.getrusage(resource.RUSAGE_CHILDREN)
self_cpu = time.process_time()
command = [str(ROOT / '.venv/bin/python'), '-I', '-S',
           str(ROOT / 'src/jeff/coordination/current.py'), 'inbox', '--recipient', 'infra']
result = subprocess.run(command, text=True, capture_output=True)
record = {'started_at': started, 'operation': 'full' if '--full' in sys.argv else 'inbox',
          'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
print(result.stdout, end='')
if result.stderr:
    print(result.stderr, file=sys.stderr, end='')
if '--full' in sys.argv and result.returncode == 0:
    board = mailbox.board_path(ROOT / '.coord')
    previous_paths = sorted(OUT.glob('round-*.json'))
    previous = json.loads(previous_paths[-1].read_text())['messages'] if previous_paths else {}
    messages = {}
    for path in sorted((board / 'messages').glob('*.md')):
        meta, _ = mailbox.load_message(board, path.stem)
        receipt = mailbox.load_receipt(board, meta['recipient'], meta['id'])
        messages[meta['id']] = {'message': meta, 'receipt': receipt[0] if receipt else None}
    changed = {key: value for key, value in messages.items() if previous.get(key) != value}
    snapshot = {'observed_at': datetime.now(timezone.utc).isoformat(), 'messages': messages}
    name = 'round-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json'
    with (OUT / name).open('x') as stream:
        json.dump(snapshot, stream, indent=2)
    record.update({'snapshot': name, 'message_count': len(messages), 'changed_ids': list(changed)})
    print(f'Metadata: {len(messages)} messages; {len(changed)} changed since prior full round.')
    for key, item in changed.items():
        meta, receipt = item['message'], item['receipt']
        state = receipt['status'] if receipt else 'unread'
        print(f"{key} {meta['sender']}->{meta['recipient']} {state} {meta['kind']} {meta['subject']}")
after = resource.getrusage(resource.RUSAGE_CHILDREN)
record.update({'work_wall_seconds': time.perf_counter() - tick,
               'work_cpu_seconds': time.process_time() - self_cpu + after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime,
               'finished_at': datetime.now(timezone.utc).isoformat()})
with (OUT / 'checks.jsonl').open('a') as stream:
    stream.write(json.dumps(record) + '\n')
print(f"Observation work: {record['work_wall_seconds']:.3f}s wall, {record['work_cpu_seconds']:.3f}s CPU (excludes interpreter startup/final log append).")
raise SystemExit(result.returncode)
