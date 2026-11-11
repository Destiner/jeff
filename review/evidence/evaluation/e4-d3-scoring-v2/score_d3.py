"""Bounded D3 artifact recipe; standard library plus existing Evaluation modules only."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path('/Users/destiner/Code/jeff')
WORK = ROOT / '.worktrees/evaluation'
HERE = Path(__file__).resolve().parent
BOUND = ROOT / 'artifacts/evaluation/e4-d3-released-boundary-v1'
OWNER = ROOT / 'artifacts/evaluation/e4-d3-owner-binding-v1/receipt.json'
OUT = ROOT / 'artifacts/evaluation/e4-d3-comparison-v1'
NAMES = ('minilm_start', 'minilm_trained', 'msmarco_start', 'msmarco_trained')
CHECKPOINTS = dict(zip(NAMES, ('minilm/baseline', 'minilm/checkpoint', 'msmarco/baseline', 'msmarco/checkpoint')))
sys.path.insert(0, str(WORK / 'src'))
from jeff.evaluation.common import load_examples
from jeff.evaluation.metrics import summarize
from jeff.evaluation.render import table, ratio, loss


def read(path):
    return json.loads(Path(path).read_text())


def fp(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def verify(pin):
    actual = fp(pin['path'])
    if actual['sha256'] != pin['sha256']:
        raise ValueError('Hash mismatch: ' + str(pin['path']))
    return actual


def write(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def now():
    return datetime.now(timezone.utc).isoformat()


def command(args, log):
    env = __import__('os').environ.copy()
    env['PYTHONPATH'] = str(WORK / 'src')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run([sys.executable, '-B', *args], cwd=WORK, env=env, capture_output=True, text=True)
    log.append({'argv': [sys.executable, '-B', *args], 'returncode': result.returncode,
                'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode not in (0, 1) or (result.returncode == 1 and args[1] != 'jeff.evaluation.compare'):
        raise RuntimeError('Command failed: ' + str(log[-1]))


def validate_units():
    examples = load_examples(BOUND / 'reference/validation.jsonl')
    units = read(BOUND / 'units.json')
    cases = {r['case_id']: r for r in units['cases']}
    policies = {p['policy_instance_id']: p for p in units['policies']}
    if len(cases) != len(units['cases']) or len(policies) != len(units['policies']):
        raise ValueError('Duplicate units')
    if len(examples) != 96 or set(cases) != {r['id'] for r in examples} or len(policies) != 48 or len(units['mechanisms']) != 8:
        raise ValueError('Unexpected D3 denominator')
    inputs = [json.loads(line) for line in (BOUND / 'inputs.jsonl').read_text().splitlines()]
    exported = [{k: r[k] for k in ('schema_version', 'id', 'state', 'question', 'options')} for r in examples]
    if inputs != exported:
        raise ValueError('Input is not exact label-free export')
    for row in examples:
        c = cases[row['id']]
        if row['group_id'] != c['group_id'] or row['group_id'] != c['policy_instance_id'] or row['split'] != 'validation':
            raise ValueError('Case/group mapping mismatch')
        if row['provenance']['label_basis'] != 'rule_verified' or row['provenance']['kind'] != 'programmatic':
            raise ValueError('Unexpected label provenance')
    seen = []
    for key, p in policies.items():
        if len(p['case_ids']) != 2 or len(set(p['case_ids'])) != 2:
            raise ValueError('Policy must contain exactly two distinct cases')
        for identifier in p['case_ids']:
            c = cases[identifier]
            if c['policy_instance_id'] != key or c['mechanism_id'] != p['mechanism_id']:
                raise ValueError('Policy mapping mismatch')
        seen.extend(p['case_ids'])
    if Counter(seen) != Counter(cases.keys()) or Counter(p['mechanism_id'] for p in policies.values()) != Counter({m: 6 for m in units['mechanisms']}):
        raise ValueError('Mechanism/policy coverage mismatch')
    return examples, units


def prepare():
    boundary_pin = {'path': str(BOUND / 'boundary.json'), 'sha256': '6202826900d634440598d370fc1cef0972c65aab45bcff92a2f2cceb95adc06e'}
    verify(boundary_pin)
    b = read(boundary_pin['path'])
    pins = [boundary_pin, fp(OWNER), fp(__file__)]
    for key in ('reference', 'inputs', 'units'):
        pins.append(verify(b[key]))
    owner = read(OWNER)
    verify(owner['boundary'])
    verify(owner['supplement'])
    examples, units = validate_units()
    for name, suffix in CHECKPOINTS.items():
        path = ROOT / 'artifacts/model/m4-v2-20261111-01' / suffix / 'checkpoint.json'
        metadata = read(path)
        if metadata['max_length'] != 256:
            raise ValueError('Not native 256 profile: ' + name)
        pins.append(fp(path))
    for module in ('baseline', 'compare', 'metrics', 'render', 'common', 'score'):
        pins.append(fp(WORK / 'src/jeff/evaluation' / (module + '.py')))
    write(HERE / 'pins.json', {'created_at': now(), 'files': pins})
    write(HERE / 'recipe.json', {
        'created_at': now(), 'predictors': list(NAMES) + ['uniform', 'lexical'],
        'checkpoint_directories': CHECKPOINTS, 'input': fp(BOUND / 'inputs.jsonl'),
        'counts': {'cases': 96, 'policies': 48, 'mechanisms': 8, 'cases_per_policy': 2, 'policies_per_mechanism': 6},
        'mapping': 'Explicit units.json only; no parsing IDs',
        'probability_quality': 'Shared metrics.summarize: unclipped natural log loss, summed multiclass Brier, 5 fixed reliability bins/ECE',
        'macros': 'Equal policy and equal mechanism; report defined/undefined/+infinity counts. Missing units not silently removed. ECE macro averages unit ECE, not pooled ECE.',
        'paired': 'Own start to trained: common-valid case wins/losses/both-correct/both-wrong and complete 2/2-policy outcomes; full denominators and incomplete groups retained',
        'selection': 'No threshold, tuning, promotion, reversal, inference, final access, or pooling with v2/probes',
        'receipt_requirements': 'Exactly four original paths; actual published receipt input/output(path,sha256,rows), checkpoint_inventory(path,sha256), checkpoint directory, command list, fresh_process, exit_code, process_wall_seconds, checkpoint_files_unchanged. Saved metadata and before/after inventory records separately verified. No fabricated execution max_length/argv/returncode fields. No prediction prefiltering. CPU metrics only; published inference uses MPS. Loaded tensors not independently attested.',
    })
    write(HERE / 'prepare-receipt.json', {'completed_at': now(), 'status': 'ready_not_scored', 'examples': len(examples), 'mechanisms': sorted(units['mechanisms']), 'commands': [sys.argv], 'errors': [], 'pins': fp(HERE / 'pins.json'), 'recipe': fp(HERE / 'recipe.json')})


def pointer(doc, path):
    for key in path.strip('/').split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        doc = doc[int(key)] if isinstance(doc, list) else doc[key]
    return doc


def bindings(path):
    data = read(path)
    if set(data) != set(NAMES):
        raise ValueError('Require exact four M4 bindings')
    model = ROOT / 'artifacts/model/m4-d3-inference-20261111-01'
    preflight = read(model / 'preflight.json')
    aggregate = read(model / 'receipt.json')
    source_pins = [fp(path), fp(model / 'preflight.json'), fp(model / 'receipt.json'), fp(model / 'execute.py')]
    if fp(model / 'execute.py')['sha256'] != aggregate['script_sha256']:
        raise ValueError('Model execution script changed')
    for pin in preflight['release_receipts']:
        source_pins.append(verify(pin))
    boundary = read(BOUND / 'boundary.json')
    for pin in boundary['pins']:
        source_pins.append(verify(pin))
    if {k: preflight['input'][k] for k in ('path', 'sha256')} != fp(BOUND / 'inputs.jsonl'):
        raise ValueError('Preflight input mismatch')
    examples, _ = validate_units()
    pairs = sum(len(e['options']) for e in examples)
    files, evidence, inventory_count = {}, {}, 0
    for name in NAMES:
        item = data[name]
        receipt = read(verify(item['receipt'])['path'])
        source_pins.append(verify(item['receipt']))
        if receipt not in aggregate['jobs']:
            raise ValueError('Aggregate/individual receipt mismatch')
        snapshot = receipt['snapshot']
        checkpoint = ROOT / 'artifacts/model/m4-v2-20261111-01' / CHECKPOINTS[name]
        if receipt['checkpoint'] != str(checkpoint):
            raise ValueError('Checkpoint directory mismatch')
        for key in ('input', 'output'):
            source_pins.append(verify(receipt[key]))
            if receipt[key]['rows'] != len(Path(receipt[key]['path']).read_bytes().splitlines()):
                raise ValueError('Receipt physical row count mismatch')
        if {k: receipt['input'][k] for k in ('path', 'sha256')} != fp(BOUND / 'inputs.jsonl') or receipt['input']['rows'] != 96:
            raise ValueError('Receipt binds a different input')
        before_pin = verify(receipt['checkpoint_inventory'])
        after_pin = fp(model / (snapshot + '-inventory-after.json'))
        source_pins += [before_pin, after_pin, fp(model / (snapshot + '-invocation.json'))]
        before, after = read(before_pin['path']), read(after_pin['path'])
        if before != after or before_pin['sha256'] != after_pin['sha256']:
            raise ValueError('Inventory records changed')
        inventory = {r['path']: r for r in before}
        if len(inventory) != len(before) or 'checkpoint.json' not in inventory or not any(p.endswith('.safetensors') for p in inventory):
            raise ValueError('Incomplete inventory')
        inventory_count += len(before)
        metadata_pin = fp(checkpoint / 'checkpoint.json')
        if metadata_pin['sha256'] != inventory['checkpoint.json']['sha256'] or read(metadata_pin['path'])['max_length'] != 256:
            raise ValueError('Saved metadata not pinned native 256')
        source_pins.append(metadata_pin)
        for rel, entry in inventory.items():
            if (checkpoint / rel).stat().st_size != entry['bytes']:
                raise ValueError('Current file size differs from inventory')
            if not rel.endswith('.safetensors'):
                current = fp(checkpoint / rel)
                if current['sha256'] != entry['sha256']:
                    raise ValueError('Current non-tensor bytes differ from inventory')
                source_pins.append(current)
        audit = preflight['token_audits'][snapshot]
        if not (audit['pairs'] == pairs == 361 and audit['full_pair_max'] == 129 and audit['over_budget_pairs'] == 0 and audit['native_cap'] == 256 and audit['tokenizer_sha256'] == inventory['tokenizer/tokenizer.json']['sha256']):
            raise ValueError('Unexpected published token audit')
        if receipt['exit_code'] != 0 or receipt['fresh_process'] is not True or receipt['checkpoint_files_unchanged'] is not True or not math.isfinite(receipt['process_wall_seconds']) or receipt['process_wall_seconds'] < 0:
            raise ValueError('Missing successful fresh-process receipt evidence')
        argv = receipt['command']
        for flag, expected in (('--input', str(BOUND / 'inputs.jsonl')), ('--output', receipt['output']['path']), ('--checkpoint', str(checkpoint))):
            if argv.count(flag) != 1 or argv[argv.index(flag) + 1] != expected:
                raise ValueError('Explicit command binding mismatch: ' + flag)
        if not (datetime.fromisoformat(boundary['completed_at']) < datetime.fromisoformat(preflight['created_at']) <= datetime.fromisoformat(receipt['started_at']) < datetime.fromisoformat(receipt['completed_at'])):
            raise ValueError('Frozen boundary does not precede prediction execution')
        if str(Path(item['prediction_path']).resolve()) != receipt['output']['path']:
            raise ValueError('Original prediction path mismatch')
        files[name] = receipt['output']['path']
        evidence[name] = {'receipt': item['receipt'], 'metadata': metadata_pin, 'inventory_before': before_pin, 'inventory_after': after_pin, 'inventory_files': len(before), 'token_audit': audit, 'published_process_wall_seconds': receipt['process_wall_seconds'], 'command': argv, 'fresh_process_reported': True}
    if len(set(files.values())) != 4 or inventory_count != 30:
        raise ValueError('Require four original outputs and 30 inventoried files')
    return files, source_pins, evidence


def macro(summaries):
    fields = {
        'agreement_valid': lambda s: s['top_choice']['on_valid']['value'],
        'agreement_all': lambda s: s['top_choice']['on_all_failure_as_unsuccessful']['value'],
        'coverage': lambda s: s['coverage']['value'], 'brier': lambda s: s['brier']['mean'],
        'ece': lambda s: s['reliability']['ece'], 'log_loss': lambda s: s['log_loss']['mean'],
    }
    result = {}
    for key, get in fields.items():
        vals = [get(s) for s in summaries]
        infinite = sum(s['log_loss']['status'] == 'positive_infinity' for s in summaries) if key == 'log_loss' else 0
        defined = [v for v in vals if v is not None]
        undefined = len(vals) - len(defined) - infinite
        result[key] = {'units': len(vals), 'finite_units': len(defined), 'undefined_units': undefined, 'positive_infinity_units': infinite,
                       'status': 'undefined' if undefined else 'positive_infinity' if infinite else 'finite',
                       'mean': math.fsum(defined) / len(vals) if not undefined and not infinite and vals else None,
                       'finite_only_mean': math.fsum(defined) / len(defined) if defined else None}
    return result


def paired(a, b, ids):
    common = [i for i in ids if a[i]['status'] == b[i]['status'] == 'valid']
    return {'total_cases': len(ids), 'common_valid': len(common), 'unpaired': len(ids) - len(common),
            'wins': sum(not a[i]['correct'] and b[i]['correct'] for i in common),
            'losses': sum(a[i]['correct'] and not b[i]['correct'] for i in common),
            'both_correct': sum(a[i]['correct'] and b[i]['correct'] for i in common),
            'both_wrong': sum(not a[i]['correct'] and not b[i]['correct'] for i in common)}


def score(path):
    OUT.mkdir(exist_ok=False)
    log, errors = [], []
    status = 'failed'
    try:
        for pin in read(HERE / 'pins.json')['files']:
            verify(pin)
        files, source_pins, evidence = bindings(path)
        _, units = validate_units()
        source_pins += read(HERE / 'pins.json')['files'] + [fp(HERE / 'recipe.json'), fp(HERE / 'prepare-receipt.json')]
        write(OUT / 'execution-pins.json', {'created_before_scoring': now(), 'bindings': fp(path), 'sources': source_pins, 'evidence': evidence, 'qualification': 'CPU scoring only. Model receipts report fresh-process MPS inference, not independently observed here. Saved metadata max_length=256 and published token audits verified without model/tokenizer loads. Before/after inventory record bytes identical; all 30 current file sizes checked, non-tensor bytes hashed. Current tensor byte hashes and loaded tensors NOT independently attested.'})
        for method in ('uniform', 'lexical'):
            output = OUT / (method + '.jsonl')
            command(['-m', 'jeff.evaluation.baseline', '--input', str(BOUND / 'inputs.jsonl'), '--method', method, '--output', str(output), '--receipt', str(OUT / (method + '-receipt.json'))], log)
            files[method] = str(output)
        args = ['-m', 'jeff.evaluation.compare', '--examples', str(BOUND / 'reference/validation.jsonl'), '--output', str(OUT / 'comparison.json')]
        for name, file in files.items():
            args += ['--predictions', name + '=' + file]
        command(args, log)
        command(['-m', 'jeff.evaluation.render', '--comparison', str(OUT / 'comparison.json'), '--output', str(OUT / 'shared-report.md'), '--title', 'D3 originals: six predictors'], log)
        comparison = read(OUT / 'comparison.json')
        report = {'runs': {}, 'paired_own_start_to_trained': {}, 'mechanisms': units['mechanisms'], 'limitations': read(BOUND / 'boundary.json')['limitations']}
        for name, run in comparison['runs'].items():
            outcomes = {r['id']: r for r in run['outcomes']}
            policies = {p['policy_instance_id']: summarize([outcomes[i] for i in p['case_ids']]) for p in units['policies']}
            mechanisms = {m: summarize([outcomes[c['case_id']] for c in units['cases'] if c['mechanism_id'] == m]) for m in units['mechanisms']}
            report['runs'][name] = {'status': run['status'], 'overall': run['overall'], 'record_diagnostics': run['record_diagnostics'], 'per_policy': policies, 'per_mechanism': mechanisms, 'policy_case_outcomes': {p['policy_instance_id']: [outcomes[i] for i in p['case_ids']] for p in units['policies']}, 'mechanism_case_outcomes': {m: [outcomes[c['case_id']] for c in units['cases'] if c['mechanism_id'] == m] for m in units['mechanisms']}, 'equal_policy_macro': macro(list(policies.values())), 'equal_mechanism_macro': macro(list(mechanisms.values()))}
        for start, trained in ((NAMES[0], NAMES[1]), (NAMES[2], NAMES[3])):
            a = {r['id']: r for r in comparison['runs'][start]['outcomes']}
            b = {r['id']: r for r in comparison['runs'][trained]['outcomes']}
            policy_pairs = {}
            full = Counter(wins=0, losses=0, both_correct=0, both_wrong=0, incomplete=0)
            for p in units['policies']:
                ids = p['case_ids']
                value = paired(a, b, ids)
                value['start_full_2_of_2'] = all(a[i]['correct'] for i in ids) if all(a[i]['status'] == 'valid' for i in ids) else None
                value['trained_full_2_of_2'] = all(b[i]['correct'] for i in ids) if all(b[i]['status'] == 'valid' for i in ids) else None
                if value['common_valid'] != 2:
                    full['incomplete'] += 1
                else:
                    x, y = value['start_full_2_of_2'], value['trained_full_2_of_2']
                    full['wins' if y and not x else 'losses' if x and not y else 'both_correct' if x and y else 'both_wrong'] += 1
                policy_pairs[p['policy_instance_id']] = value
            report['paired_own_start_to_trained'][trained] = {'start': start, 'cases': paired(a, b, list(a)), 'full_policy_2_of_2': dict(full), 'total_policies': 48, 'per_policy': policy_pairs, 'per_mechanism': {m: paired(a, b, [c['case_id'] for c in units['cases'] if c['mechanism_id'] == m]) for m in units['mechanisms']}}
        write(OUT / 'report.json', report)
        lines = ['# D3 seen-mechanism / new-policy diagnostic', '', '96 cases, 48 correlated two-case policies, eight intentionally seen mechanisms; originals only, native 256. Never pooled with v2/probes. No threshold or promotion.', '', 'All labels: rule_verified/programmatic. Same openai/gpt-sol author/reviewer alias (immutable revision unknown), not independent ground truth. Initial review 31/32; final-content review 64/64 across 40 policies only. Residual hints are a separate authoring quality: FIFO fewest-zero 6/12; rates slot-two 6/12; scheduling non-none 11/12; easy boundary cases. These are not measured model improvements.', '', 'Exact metrics, all 48 policy results, reliability bins, macro undefined/infinity accounting and paired results: report.json. Raw record diagnostics and all pairwise comparisons: comparison.json. Coverage/conditional quality definitions: shared-report.md.', '']
        for heading, select in [('Overall', lambda r: {'all': r['overall']}), ('All eight mechanisms (12 cases / 6 policies each)', lambda r: r['per_mechanism'])]:
            lines += ['## ' + heading, '']
            rows = []
            for name, run in report['runs'].items():
                for unit, s in select(run).items():
                    rows.append([name, unit, ratio(s['coverage']), ratio(s['top_choice']['on_valid']), loss(s['log_loss']), s['brier']['mean'], s['reliability']['ece'], s['failures']])
            lines += table(['Predictor', 'Unit', 'Coverage', 'Agreement', 'Loss', 'Brier', 'ECE', 'Failures'], rows)
        lines += ['## Equal-unit macros', '', 'Strict mean is null when any unit is undefined; positive-infinite loss is separately flagged. Finite-only means are explicitly conditional, not the headline macro.', '']
        for name, run in report['runs'].items():
            lines += ['### ' + name, '```json', json.dumps({k: run[k] for k in ('equal_policy_macro', 'equal_mechanism_macro')}, indent=2), '```', '']
        lines += ['## Paired own-start → trained', '']
        for name, pair in report['paired_own_start_to_trained'].items():
            lines += ['### ' + name, '```json', json.dumps({k: v for k, v in pair.items() if k != 'per_policy'}, indent=2), '```', '']
        with (OUT / 'report.md').open('x') as f:
            f.write('\n'.join(lines) + '\n')
        for pin in source_pins:
            verify(pin)
        write(OUT / 'source-recheck.json', {'completed_at': now(), 'files': source_pins, 'all_unchanged': True, 'tensor_bytes_rehashed': False})
        status = 'completed' if all(r['status'] == 'ok' for r in comparison['runs'].values()) else 'completed_with_prediction_issues'
    except Exception as exc:
        errors.append(type(exc).__name__ + ': ' + str(exc))
        raise
    finally:
        write(OUT / 'receipt.json', {'completed_at': now(), 'status': status, 'commands': log, 'errors': errors, 'outputs': [fp(p) for p in sorted(OUT.iterdir()) if p.is_file()], 'cost_gbp': 0, 'inference': False})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prepare', action='store_true')
    group.add_argument('--bindings', type=Path)
    args = parser.parse_args()
    prepare() if args.prepare else score(args.bindings)
