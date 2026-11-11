#!/usr/bin/env python3
"""Deferred CPU E6 orchestration; requires real predictions and owner evidence."""
from __future__ import annotations
import argparse
from collections import defaultdict
from copy import deepcopy
from itertools import combinations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
WORKTREE = Path('/Users/destiner/Code/jeff/.worktrees/evaluation')
ARTIFACTS = Path('/Users/destiner/Code/jeff/artifacts')
PYTHON = WORKTREE / '.venv/bin/python'
CONFIG = WORKTREE / 'configs/evaluation/e5-p3-v1.json'
UNITS = ARTIFACTS / 'evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json'
BINDING = ARTIFACTS / 'evaluation/e6-predeclared-v1/inputs.json'
START, TRAINED, P3 = 'm6-qwen-fresh-start', 'm6-qwen-v2-trained', 'qwen25-05b-instruct-frozen'
STRATA = ('inherited-v1', 'new-v2', 'probes')


def safe(value):
    raw = Path(value).absolute()
    path = raw.resolve()
    for candidate in (raw, path):
        if any(p.lower() == 'final' or p.lower().startswith(('final-', 'final_', 'final.')) for p in candidate.parts):
            raise ValueError('Reserved final path refused')
    return path


def pin(value):
    path = safe(value)
    if not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError('Require a small real file, not a checkpoint/directory: ' + str(path))
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def load(path):
    return json.loads(safe(path).read_text())


def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def verify(pins):
    for expected in pins:
        if pin(expected['path']) != expected:
            raise ValueError('Pinned dependency changed: ' + expected['path'])


def supplement(output, config):
    # These are the actual existing APIs: compare exports paired_comparison, not paired.
    from jeff.evaluation.metrics import summarize
    from jeff.evaluation.compare import paired_comparison
    from jeff.evaluation.order import pair_summary
    from jeff.evaluation.common import records
    mapping = load(UNITS)['by_validation_id']
    summaries, numeric = {}, {}
    for stratum, spec in config['strata'].items():
        definitions = load(spec['order_pairs']['path'])
        anchors = {p[k]: p['original_id'] for p in definitions for k in ('original_id', 'reversed_id')}
        reports = {name: load(output / 'study' / stratum / (name + '-order-report.json')) for name in spec['predictors']}
        sample = next(iter(reports.values()))['prediction_report']['outcomes']
        by_id = {r['id']: r for r in sample}
        for identifier, anchor in anchors.items():
            metadata = mapping.get(anchor)
            if metadata and (metadata['stratum'] != stratum or metadata['group_id'] != by_id[identifier]['group_id'] or metadata['task_family'] != by_id[identifier]['task_family']):
                raise ValueError('Reviewed-unit identity mismatch: ' + identifier)
        def groups(row):
            metadata = mapping.get(anchors[row['id']], {})
            family = row['task_family']
            result = [('all',), ('family', family), ('family_label_basis', family, row['label_basis']),
                      ('source_group', family, row['group_id'])]
            for kind in ('producer', 'domain', 'mechanism', 'policy_instance'):
                result.append((kind, family, metadata.get(kind) or '<unknown>'))
            return result
        block = {'predictors': {}, 'orientations': {}, 'pair_definitions': definitions}
        for name, report in reports.items():
            grouped = defaultdict(list)
            for pair in report['pairs']:
                for key in groups(by_id[pair['original_id']]):
                    grouped[json.dumps(key)].append(pair)
            block['predictors'][name] = {
                'original': report['original'], 'reversed': report['reversed'],
                'paired_quality': report['paired_quality'],
                'both_order_groups': {key: {'metrics': pair_summary(rows), 'pairs': rows} for key, rows in grouped.items()},
                'diagnostics': {key: report['prediction_report'][key] for key in ('status', 'record_diagnostics', 'extra_prediction_ids', 'duplicate_prediction_ids', 'unidentifiable_records', 'roundoff')},
            }
        for orientation, ids in [('original', {p['original_id'] for p in definitions}), ('reversed', {p['reversed_id'] for p in definitions})]:
            population = [r for r in sample if r['id'] in ids]
            group_ids = defaultdict(set)
            for row in population:
                for key in groups(row):
                    group_ids[json.dumps(key)].add(row['id'])
            orientation_block = {}
            for key, members in group_ids.items():
                rows = {name: [r for r in report['prediction_report']['outcomes'] if r['id'] in members] for name, report in reports.items()}
                contrasts = []
                # Every family change for every retained E5 arm, plus the primary contrasts.
                for left, right in combinations(rows, 2):
                    a, b = {r['id']: r for r in rows[left]}, {r['id']: r for r in rows[right]}
                    paired = paired_comparison(rows[left], rows[right], len(members))
                    contributions = []
                    for identifier in sorted(members):
                        x, y = a[identifier], b[identifier]
                        item = {'id': identifier, 'anchor_id': anchors[identifier], 'left_status': x['status'], 'right_status': y['status']}
                        if x['status'] == y['status'] == 'valid':
                            finite = x['log_loss'] is not None and y['log_loss'] is not None
                            item.update(nll_delta_left_minus_right=x['log_loss'] - y['log_loss'] if finite else None,
                                        nll_status='finite' if finite else 'infinite_side; inspect raw outcomes',
                                        brier_delta_left_minus_right=x['brier'] - y['brier'],
                                        agreement_delta_left_minus_right=int(x['correct']) - int(y['correct']))
                        contributions.append(item)
                    common = [r for r in contributions if 'brier_delta_left_minus_right' in r]
                    paired['brier_delta_left_minus_right'] = sum(r['brier_delta_left_minus_right'] for r in common) / len(common) if common else None
                    contrasts.append({'left_name': left, 'right_name': right, **paired, 'case_contributions': contributions})
                orientation_block[key] = {'reference_ids': sorted(members), 'runs': {name: summarize(value) for name, value in rows.items()}, 'contrasts': contrasts}
            block['orientations'][orientation] = orientation_block
        if stratum == 'probes':
            # Twelve existing paired groups, not a new reversal dataset or 24 independent sources.
            block['probe_pair_macro'] = {}
            for name, report in reports.items():
                outcomes = {r['id']: r for r in report['prediction_report']['outcomes']}
                units = [summarize([outcomes[p['original_id']], outcomes[p['reversed_id']]]) for p in definitions]
                losses = [u['log_loss'] for u in units]
                status = 'positive_infinity' if any(v['status'] == 'positive_infinity' for v in losses) else 'undefined' if any(v['status'] != 'finite' for v in losses) else 'finite'
                block['probe_pair_macro'][name] = {'pair_count': len(units), 'pair_metrics': units,
                    'nll_status': status, 'nll_mean': sum(v['mean'] for v in losses) / len(units) if status == 'finite' else None,
                    'brier_mean': sum(u['brier']['mean'] for u in units) / len(units) if all(u['coverage']['numerator'] == 2 for u in units) else None,
                    'stable_correct': report['overall']['both_correct']}
        summaries[stratum] = block
        # Exact raw probabilities are retained separately from scorer roundoff normalization.
        raw = {}
        for name in (START, P3):
            path = output / 'study' / stratum / (name + '-order.jsonl')
            raw[name] = {row['id']: {p['option_id']: p['probability'] for p in row['probabilities']}
                         for _, row, error in records(path) if not error and isinstance(row, dict)
                         and any(o['id'] == row.get('id') and o['status'] == 'valid' for o in reports[name]['prediction_report']['outcomes'])}
        outcomes = {name: {r['id']: r for r in reports[name]['prediction_report']['outcomes']} for name in (START, P3)}
        cases = []
        for identifier in by_id:
            a, b = outcomes[START][identifier], outcomes[P3][identifier]
            item = {'id': identifier, 'start_status': a['status'], 'p3_status': b['status']}
            if a['status'] == b['status'] == 'valid':
                differences = {k: raw[START][identifier][k] - raw[P3][identifier][k] for k in raw[START][identifier]}
                item.update(option_probability_differences_start_minus_p3=differences,
                            start_tie_size=a['tie_size'], p3_tie_size=b['tie_size'],
                            start_choice=a['choice_id'], p3_choice=b['choice_id'],
                            new_tie=a['tie_size'] > 1 and b['tie_size'] == 1,
                            untied_choice_change=a['tie_size'] == b['tie_size'] == 1 and a['choice_id'] != b['choice_id'])
            cases.append(item)
        differences = sorted(abs(v) for c in cases for v in c.get('option_probability_differences_start_minus_p3', {}).values())
        complete = all('start_choice' in c for c in cases)
        numeric[stratum] = {'reference_presentations': len(cases), 'common_valid': sum('start_choice' in c for c in cases),
            'cases': cases, 'sorted_absolute_probability_differences': differences,
            'max_absolute_difference': max(differences, default=None),
            'exact_probability_equality_on_common_valid': all(v == 0 for v in differences) if differences else None,
            'full_coverage_numerical_reference_met': complete and bool(differences) and max(differences) <= 1e-6 and not any(c.get('new_tie') or c.get('untied_choice_change') for c in cases),
            'semantic_equivalence': 'NOT ATTESTED; owner must review actual evidence schema and semantic controls; hashes are not semantics'}
    write(output / 'grouped-both-order-summary.json', {'strata': summaries, 'direction': 'left minus right; inspect names, lower NLL/Brier better',
        'limits': 'No pooled strata or subgroup score; overlapping reviewed dimensions, unknown explicit. Shared summarize reliability fields are descriptive only, not a calibration claim.'})
    write(output / 'fresh-start-vs-p3-exact-differences.json', numeric)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ('start', 'trained'):
        for suite in ('original300', 'reversed300', 'probes24'):
            parser.add_argument('--' + role + '-' + suite, required=True)
    parser.add_argument('--evidence', required=True, action='append', help='Real small receipt/code/audit evidence; repeat, actual schemas reviewed by owner')
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    if Path(sys.executable).absolute() != PYTHON.absolute():
        raise ValueError('Use project interpreter: ' + str(PYTHON))
    output = safe(args.output_dir)
    if HERE not in output.parents or output.exists():
        raise ValueError('Require a NEW descendant of e6-analysis-preparation-v1; never overwrite')
    dependencies = load(HERE / 'preparation-lock.json')['dependencies']
    verify(dependencies)
    runtime = {role: {suite: pin(getattr(args, role + '_' + suite)) for suite in ('original300', 'reversed300', 'probes24')} for role in ('start', 'trained')}
    files = [p for arm in runtime.values() for p in arm.values()]
    if len({p['path'] for p in files}) != 6:
        raise ValueError('Require six distinct real prediction paths')
    evidence = [pin(p) for p in args.evidence]
    config = deepcopy(load(CONFIG))
    universes = {p['name']: p for p in load(BINDING)['inputs']}
    for stratum, spec in config['strata'].items():
        for role, name in [('start', START), ('trained', TRAINED)]:
            def source(suite, universe):
                return {'predictions': runtime[role][suite], 'source_inputs': universes[universe]}
            original = source('original300', 'v2-original')
            reverse = source('reversed300', 'v2-reversed')
            probes = source('probes24', 'probes-paired')
            spec['predictors'][name] = {'role': 'fresh-start' if role == 'start' else 'v2-trained',
                'role_detail': 'M6 pinned pretrained start, no Jeff updates' if role == 'start' else 'M6 final one-epoch v2 TRAIN checkpoint, P4 inference; owner reviews evidence',
                'sources': [probes] if stratum == 'probes' else [original],
                'order_sources': [probes] if stratum == 'probes' else [original, reverse]}
        if len(spec['predictors']) != 11:
            raise ValueError('Must preserve all nine E5 predictors plus two M6 arms')
    config['e6_evidence'] = evidence
    output.mkdir(parents=True, exist_ok=False)
    pins = dependencies + files + evidence + [pin(HERE / 'preparation-lock.json')]
    write(output / 'preflight.json', {'dependencies': pins, 'runtime': runtime, 'evidence': evidence, 'argv': sys.argv,
        'identity_review': 'Owner must bind actual input/output hashes, checkpoint lineage, tokenizer/template/readout/T1/cap1024/FP32-MPS/eval/batch/thread controls in actual evidence schema. No invented receipt fields or automatic semantic attestation.',
        'training_summaries': 'Separate later evidence; not consumed here'})
    write(output / 'recipe.json', config)
    env = dict(os.environ, PYTHONPATH=str(WORKTREE / 'src'), JEFF_ARTIFACTS_DIR=str(ARTIFACTS), PYTHONDONTWRITEBYTECODE='1')
    def execute(arguments):
        command = [str(PYTHON), *map(str, arguments)]
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        write(output / ('command-' + str(len(list(output.glob('command-*.json'))) + 1) + '.json'), {'command': command, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            raise ValueError('Execution failed; preserve partial namespace, never retry/overwrite it')
    execute(['-m', 'jeff.evaluation.study', '--config', output / 'recipe.json', '--output-dir', output / 'study'])
    for stratum in STRATA:
        directory = output / 'study' / stratum
        arguments = ['-m', 'jeff.evaluation.render', '--comparison', directory / 'comparison.json', '--title', 'E6 ' + stratum, '--output', output / ('E6-' + stratum + '.md')]
        for name in config['strata'][stratum]['predictors']:
            arguments += ['--order', name + '=' + str(directory / (name + '-order-report.json'))]
        execute(arguments)
    sys.path.insert(0, str(WORKTREE / 'src'))
    supplement(output, config)
    verify(pins)
    write(output / 'completion.json', {'dependencies': pins, 'model_loads': 0, 'cost_gbp': 0,
        'limitations': 'Development only, no automatic promotion/significance/calibration/semantics attestation; train fit separate.',
        'outputs': [pin(p) for p in sorted(output.rglob('*')) if p.is_file()]})


if __name__ == '__main__':
    main()
