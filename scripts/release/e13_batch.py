"""E13 sequential parent. Run with .venv/bin/python -I -S; no project imports."""
import time
CLOCK = time.monotonic()
import os
import signal
import sys
PROCESS = None
PUBLISHED = None


def expired(signum, frame):
    if PROCESS is not None:
        try:
            os.killpg(PROCESS.pid, signal.SIGKILL)
            PROCESS.poll()
        except OSError:
            pass
    if PUBLISHED is not None:
        try:
            PUBLISHED.unlink(missing_ok=True)
        except OSError:
            pass
    os._exit(1)


signal.signal(signal.SIGALRM, expired)
signal.setitimer(signal.ITIMER_REAL, 1154)
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
NATIVE = Path('/Users/destiner/Code/jeff/.worktrees/release/.venv/bin/python')
ORDER = ['m10', 'm11', 'm12', 'p12-nli']
PRIOR = Path('/Users/destiner/Code/jeff/artifacts/release/e13-exploration-20261112-01/delivery-summary.json')
INPUT_ROOT = Path('/Users/destiner/Code/jeff/artifacts/evaluation/e13-exploration-inputs-v1')
INPUTS = {'native.jsonl': '1c8dca5c849faba518478c8676be37290d7722fde2f3edfe791d71e0ca23a074',
          'reversed.jsonl': '5e115753f7ee2bc6193c1c9758ddf59f05f2bae35a79eb975678afb8ce8ed2d1',
          'pairs.json': '7572cdb4b47273d877d803203d8ff38e74dcdbfb82cac2f1a63c01830a991c5f'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def now():
    return dt.datetime.now(dt.timezone.utc)


def stamp(s):
    value = dt.datetime.fromisoformat(s)
    require(value.tzinfo is not None, 'timezone required')
    return value


def load(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())


def alive(pid):
    try:
        os.killpg(pid, 0)
        return True
    except ProcessLookupError:
        return False


def send(pid, sig):
    try:
        os.killpg(pid, sig)
    except ProcessLookupError:
        pass


def check(pin, deadline):
    path = Path(pin['path'])
    require(path.is_absolute() and '..' not in path.parts and
            not any(p.is_symlink() for p in (path, *path.parents)), 'unsafe pin')
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            require(time.monotonic() < deadline, 'hash deadline')
            h.update(chunk)
    require(h.hexdigest() == pin['sha256'], 'pin mismatch')


def group_rss(pid):
    result = subprocess.run(['/bin/ps', '-axo', 'pgid=,rss='], text=True,
                            capture_output=True, timeout=.4, check=True)
    return sum(int(parts[1]) * 1024 for line in result.stdout.splitlines()
               if len(parts := line.split()) == 2 and int(parts[0]) == pid)


def main():
    global PROCESS, PUBLISHED
    p = argparse.ArgumentParser()
    p.add_argument('--operation', type=Path, required=True)
    p.add_argument('--output-root', type=Path, required=True)
    p.add_argument('--model-activation-confirmed', action='store_true', required=True)
    a = p.parse_args()
    require(sys.flags.isolated and sys.flags.no_site, 'parent requires -I -S')
    op = load(a.operation)
    for key in ('model_activation', 'reservation', 'renewed_window_message'):
        require(isinstance(op.get(key), str) and op[key].strip(), 'actual Model grant required')
    gs, ge = stamp(op['grant_start_utc']), stamp(op['grant_end_utc'])
    require(gs <= now() < ge <= stamp('2026-11-12T08:30:36+00:00'), 'grant window')
    require(now() < stamp('2026-11-12T08:00:00+00:00'), 'starts closed')
    require(op['candidate_order'] == ORDER and op['source_root'] == str(ROOT), 'frozen order/root')
    require(op['phase'] == 'exploration' and op['prior_delivery']['path'] == str(PRIOR), 'exploration ledger only')
    check(op['prior_delivery'], CLOCK + 30)
    prior = load(PRIOR)
    require(prior['status'] == 'complete' and prior['conservative_cumulative_charge_seconds'] == 46 and
            prior['remaining_from_1200_seconds'] == 1154 and prior['outer_exit_code'] == 0 and
            prior['all_native_groups_absent'] is True, 'prior exploration charge/return')
    end = min(CLOCK + 1154, time.monotonic() + (ge - now()).total_seconds())
    require(end - time.monotonic() >= 725, 'full four-job budget unavailable')
    signal.setitimer(signal.ITIMER_REAL, end - time.monotonic())
    out = a.output_root.absolute()
    out.mkdir(parents=True, exist_ok=False)
    records = []
    write(out / 'operation.json', op)
    for candidate in ORDER:
        start = time.monotonic()
        deadline = min(start + 180, end - .5)
        # The alarm covers hashes, imports, scoring, cleanup and publication alike.
        signal.setitimer(signal.ITIMER_REAL, max(.001, deadline - time.monotonic()))
        record = {'candidate': candidate, 'success': False, 'cleanup_complete': True}
        records.append(record)
        PROCESS = None
        try:
            require(now() < stamp('2026-11-12T08:00:00+00:00') and gs <= now() < ge,
                    'new candidate outside start window')
            ref = op['bindings'][candidate]
            check(ref, deadline - 2)
            b = load(ref['path'])
            require(b['candidate'] == candidate and b['source_root'] == str(ROOT), 'binding role/root')
            if candidate == 'p12-nli':
                require(b['schema_version'] == 'e13.nli.wrapper.v1' and
                        b['native_binding']['path'] != ref['path'], 'separate native NLI descriptor required')
            for key in ('model_activation', 'reservation', 'renewed_window_message'):
                require(b[key] == op[key], 'activation binding mismatch')
            for path, sha in b['executable_sources'].items():
                check({'path': path, 'sha256': sha}, deadline - 2)
            for key in ('input_manifest', 'config', 'checkpoint_manifest', 'download_manifest', 'native_binding'):
                if b.get(key) is not None:
                    check(b[key], deadline - 2)
            require(str(NATIVE.resolve()) == b['native_interpreter']['path'], 'native interpreter changed')
            check(b['native_interpreter'], deadline - 2)
            if candidate == 'p12-nli':
                native_binding = load(b['native_binding']['path'])
                require(native_binding['schema_version'] == 'e13.nli.binding.v1' and
                        native_binding['candidate'] == candidate and
                        native_binding['input_manifest'] == b['input_manifest'],
                        'native NLI input binding mismatch')
            manifest = load(b['input_manifest']['path'])
            require(manifest['release']['path'] == str(INPUT_ROOT / 'inference-handoff.json'), 'release scope')
            require(manifest['pair_map'] == {'path': str(INPUT_ROOT / 'pairs.json'), 'sha256': INPUTS['pairs.json']}, 'pair scope')
            for item, name in zip(manifest['datasets'], ('native.jsonl', 'reversed.jsonl'), strict=True):
                require(item['path'] == str(INPUT_ROOT / name) and item['sha256'] == INPUTS[name] and item['rows'] == 200, 'actual input scope')
            command = [str(NATIVE), '-I', '-B', str(ROOT / 'scripts/release/e13_worker.py'),
                       '--binding', ref['path'], '--output-dir', str(out / candidate)]
            env = {'PATH': '/usr/bin:/bin', 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
                   'HF_DATASETS_OFFLINE': '1', 'HF_HUB_DISABLE_IMPLICIT_TOKEN': '1',
                   'HF_HUB_DISABLE_TELEMETRY': '1', 'PYTORCH_ENABLE_MPS_FALLBACK': '0',
                   'TOKENIZERS_PARALLELISM': 'false', 'OMP_NUM_THREADS': '4',
                   'MKL_NUM_THREADS': '4', 'VECLIB_MAXIMUM_THREADS': '4'}
            record['command'] = command
            with (out / (candidate + '.stdout.log')).open('x') as stdout, (out / (candidate + '.stderr.log')).open('x') as stderr:
                PROCESS = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout,
                                           stderr=stderr, start_new_session=True)
                record['pid'] = PROCESS.pid
                write(out / (candidate + '.child-registration.json'),
                      {'candidate': candidate, 'pid': PROCESS.pid, 'pgid': PROCESS.pid,
                       'phase': 'exploration', 'command': command})
                while time.monotonic() < deadline - 2:
                    if PROCESS.poll() is not None and not alive(PROCESS.pid):
                        break
                    elapsed = time.monotonic() - start
                    if elapsed >= 170:
                        record['timeout'] = True
                        send(PROCESS.pid, signal.SIGTERM)
                    rss = group_rss(PROCESS.pid)
                    record['group_rss_observed_max_bytes'] = max(rss, record.get('group_rss_observed_max_bytes', 0))
                    require(rss <= 8 * 1024**3, 'group RSS guard')
                    time.sleep(.03)
            require(PROCESS.poll() == 0 and not record.get('timeout'), 'native failed or timed out')
            receipt = load(out / candidate / ('run/receipt.json' if candidate in ('m10', 'm12') else 'receipt.json'))
            require(receipt['status'] == 'complete', 'native receipt incomplete')
            if candidate in ('m10', 'm12'):
                require(receipt['forwards']['attempted'] == receipt['forwards']['completed'] ==
                        receipt['forwards']['maximum'] == 403 and
                        receipt['forwards']['expected_startup'] == 3 and
                        receipt['forwards']['expected_suite_rows'] == [200, 200] and
                        len(receipt['suites']) == 2 and
                        all(s['status'] == 'complete' and s['expected_rows'] == s['written_rows'] == 200
                            for s in receipt['suites']), 'Qwen forward coverage')
            elif candidate == 'p12-nli':
                require(receipt['schema_version'] == 'e13.nli.run.v1' and
                        receipt['expected_counts'] == {
                            'decisions': 400, 'candidate_pairs': 800, 'native_forwards': 100,
                            'startup_forwards': 0,
                            'suites': [{'name': name, 'decisions': 200, 'candidate_pairs': 400,
                                        'native_forwards': 50}
                                       for name in ('e13-native', 'e13-reversed')]} and
                        receipt['native_attempted'] == receipt['native_completed'] == 100 and
                        receipt['pairs_attempted'] == receipt['pairs_completed'] == 800 and
                        receipt['startup_forwards'] == 0 and
                        sum(s['written_rows'] for s in receipt['suites']) == 400 and
                        sum(s['written_probabilities'] for s in receipt['suites']) == 800,
                        'NLI coverage')
            else:
                require(receipt['native_forward_attempted'] == receipt['native_forward_completed'] == 100 and
                        receipt['written_decisions'] == 400 and
                        receipt['candidate_pairs_attempted'] == receipt['candidate_pairs_completed'] == 800,
                        'encoder coverage')
            record['outputs'] = []
            for item in manifest['datasets']:
                path = out / candidate / ('run' if candidate in ('m10', 'm12') else '') / (item['name'] + '.jsonl')
                raw = path.read_bytes()
                predictions = [json.loads(line) for line in raw.splitlines()]
                inputs = [json.loads(line) for line in Path(item['path']).read_bytes().splitlines()]
                require(len(predictions) == len(inputs) == 200, 'output row coverage')
                for pred, row in zip(predictions, inputs, strict=True):
                    require(pred['id'] == row['id'] and pred['schema_version'] == '0.1', 'output identity')
                    probabilities = pred['probabilities']
                    require(len(probabilities) == 2 and {v['option_id'] for v in probabilities} == {v['id'] for v in row['options']}, 'output option coverage')
                    values = [v['probability'] for v in probabilities]
                    require(all(type(v) in (int, float) and math.isfinite(v) and 0 <= v <= 1 for v in values) and abs(sum(values) - 1) <= 1e-5, 'invalid probabilities')
                record['outputs'].append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'rows': 200, 'probabilities': 400})
            record['success'] = True
        except BaseException as exc:
            record['failure_type'] = type(exc).__name__
            record['failure_message'] = str(exc)[:1000]
        finally:
            if PROCESS is not None:
                if alive(PROCESS.pid):
                    send(PROCESS.pid, signal.SIGKILL)
                while time.monotonic() < deadline - .3:
                    if PROCESS.poll() is not None and not alive(PROCESS.pid):
                        break
                    time.sleep(.01)
                record['returncode'] = PROCESS.poll()
                record['process_group_absent'] = not alive(PROCESS.pid)
                record['cleanup_complete'] = record['returncode'] is not None and record['process_group_absent']
            record['elapsed_seconds_before_publication'] = time.monotonic() - start
            record['success'] = record['success'] and record['cleanup_complete'] and time.monotonic() < deadline - .2
            pending = out / (candidate + '.pending.json')
            published = out / (candidate + '.process-receipt.json')
            write(pending, record)
            require(time.monotonic() < deadline, 'publication deadline')
            PUBLISHED = published
            os.replace(pending, published)
            require(time.monotonic() < deadline, 'post-publication deadline')
            write(out / (candidate + '.publication-receipt.json'),
                  {'elapsed_seconds_after_publication': time.monotonic() - start,
                   'phase': 'exploration'})
            signal.setitimer(signal.ITIMER_REAL, max(.001, end - time.monotonic()))
            PUBLISHED = None
        if not record['cleanup_complete']:
            break
    write(out / 'batch-receipt.json', {'phase': 'exploration', 'prior_charge_seconds': 46,
          'elapsed_seconds_before_publication': time.monotonic() - CLOCK, 'runs': records, 'success': len(records) == 4 and all(r['success'] for r in records),
          'qualification': 'Source-prepared harness; sampled group RSS, not continuous peak. Success also requires parent exit zero. No retries.'})
    require(time.monotonic() < end, 'aggregate publication deadline')
    return 0 if len(records) == 4 and all(r['success'] for r in records) else 1


if __name__ == '__main__':
    raise SystemExit(main())
