#!/usr/bin/env python3
"""Deferred CPU-only E5 orchestration. Requires real Runtime outputs; never infers."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
WORKTREE = Path('/Users/destiner/Code/jeff/.worktrees/evaluation')
ARTIFACTS = Path('/Users/destiner/Code/jeff/artifacts')
CONFIG = WORKTREE / 'configs/evaluation/e3-m4-v1.json'
BINDING = ARTIFACTS / 'evaluation/e5-p3-input-binding-v1/inputs.json'
STRATA = {'inherited-v1': 60, 'new-v2': 240, 'probes': 24}
DECODER = 'qwen25-05b-instruct-frozen'


def safe(value):
    raw = Path(value).absolute()
    path = raw.resolve()
    for candidate in (raw, path):
        if any(p.lower() == 'final' or p.lower().startswith(('final-', 'final_', 'final.')) for p in candidate.parts):
            raise ValueError('Reserved final path refused')
    return path


def pin(value):
    path = safe(value)
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return {'path': str(path), 'sha256': digest.hexdigest(), 'bytes': path.stat().st_size}


def load(path):
    return json.loads(safe(path).read_text())


def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def source(prediction, universe):
    return {'predictions': pin(prediction), 'source_inputs': universe}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original300', required=True)
    parser.add_argument('--reversed300', required=True)
    parser.add_argument('--probes24', required=True)
    parser.add_argument('--frozen-recipe', required=True)
    parser.add_argument('--execution-receipt', required=True)
    parser.add_argument('--evidence', action='append', default=[], help='Additional immutable runtime code/audit/failure evidence file; repeatable')
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    output = safe(args.output_dir)
    if HERE not in output.parents or output.exists():
        raise ValueError('Require a NEW descendant of the exclusive preparation directory')
    lock_path = HERE / 'preparation-lock.json'
    lock = load(lock_path)
    pins = {p['path']: p for p in lock['dependencies']}
    for expected in pins.values():
        if pin(expected['path']) != expected:
            raise ValueError('Preparation dependency changed: ' + expected['path'])
    pins[str(lock_path)] = pin(lock_path)
    runtime = {'original300': pin(args.original300), 'reversed300': pin(args.reversed300),
               'probes24': pin(args.probes24), 'frozen_recipe': pin(args.frozen_recipe),
               'execution_receipt': pin(args.execution_receipt), 'additional_evidence': [pin(p) for p in args.evidence]}
    if len({runtime[k]['path'] for k in ('original300', 'reversed300', 'probes24')}) != 3:
        raise ValueError('Require three distinct real prediction files')
    for item in [runtime[k] for k in ('original300', 'reversed300', 'probes24', 'frozen_recipe', 'execution_receipt')] + runtime['additional_evidence']:
        pins[item['path']] = item
    config = deepcopy(load(CONFIG))
    config['strata'] = {k: config['strata'][k] for k in STRATA}
    # Stored simple baselines are reused byte-for-byte, not regenerated.
    config['baselines'] = []
    universes = {row['name']: row for row in load(BINDING)['inputs']}
    original = source(args.original300, universes['v2-original'])
    reversed_ = source(args.reversed300, universes['v2-reversed'])
    probes = source(args.probes24, universes['probes-paired'])
    for stratum, spec in config['strata'].items():
        for baseline in ('uniform', 'lexical'):
            root = ARTIFACTS / 'evaluation/e3-m4-v1' / stratum
            spec['predictors'][baseline] = {
                'role': 'historical-retained',
                'role_detail': 'Stored deterministic non-neural E3 baseline, not a checkpoint',
                'sources': [{'predictions': pin(root / f'{baseline}.jsonl'), 'source_reference': spec['examples']}],
                'order_sources': [{'predictions': pin(root / f'{baseline}-order.jsonl'), 'source_reference': spec['order_examples']}],
            }
        spec['predictors'][DECODER] = {
            'role': 'fresh-start',
            'role_detail': 'Pretrained instruction model untouched by Jeff learning; NOT random or untrained pretraining',
            'sources': [probes] if stratum == 'probes' else [original],
            'order_sources': [probes] if stratum == 'probes' else [original, reversed_],
        }
    config['e5_runtime_evidence'] = runtime
    config['e5_input_binding'] = pin(BINDING)
    config['e5_preparation_lock'] = pin(lock_path)
    config['e5_interpretation'] = 'Practical systems comparison, not an architecture ablation. Normalized conditional answer-symbol probabilities, not calibrated confidence. No automatic promotion or preregistered threshold.'
    # All original sources, runtime inputs and executing code are hashed before outputs exist.
    output.mkdir(parents=True, exist_ok=False)
    write(output / 'preflight.json', {'dependencies': list(pins.values()), 'runtime': runtime,
                                     'argv': sys.argv, 'python': sys.version,
                                     'attestation': 'Hashes establish byte identity, not freeze chronology, checkpoint identity or inference authenticity. Owner must review Runtime evidence.'})
    write(output / 'recipe.json', config)
    env = dict(os.environ, JEFF_ARTIFACTS_DIR=str(ARTIFACTS), PYTHONPATH=str(WORKTREE / 'src'), PYTHONDONTWRITEBYTECODE='1')
    commands = []

    def execute(arguments):
        command = [sys.executable, *map(str, arguments)]
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        receipt = {'command': command, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        commands.append(receipt)
        write(output / f'orchestration-command-{len(commands):02d}.json', receipt)
        if result.returncode:
            raise ValueError('Command failed; retain partial output and receipt; do not overwrite/retry this directory')

    study = output / 'study'
    execute(['-m', 'jeff.evaluation.study', '--config', output / 'recipe.json', '--output-dir', study])
    supplement = ['--units', ARTIFACTS / 'evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json']
    for stratum in STRATA:
        directory = study / stratum
        # Keep completed study outputs immutable; create a separate E5-named rendering.
        render = ['-m', 'jeff.evaluation.render', '--comparison', directory / 'comparison.json',
                  '--title', f'E5 frozen decoder comparison: {stratum} ({STRATA[stratum]} presentations)',
                  '--output', output / f'E5-{stratum}.md']
        for predictor in config['strata'][stratum]['predictors']:
            render += ['--order', f'{predictor}={directory / (predictor + "-order-report.json")}']
        execute(render)
        supplement += ['--comparison', f'{stratum}={directory / "comparison.json"}']
    execute([ARTIFACTS / 'evaluation/e3-source-unit-analysis-v1/summarize.py', *supplement, '--output-dir', output / 'source-units'])
    # Derive exact flip/margin diagnostics from shared-scorer outcomes, never raw re-scoring.
    margins = {}
    for stratum in STRATA:
        margins[stratum] = {}
        for predictor in config['strata'][stratum]['predictors']:
            report = load(study / stratum / f'{predictor}-order-report.json')
            outcomes = {r['id']: r for r in report['prediction_report']['outcomes']}
            pairs = []
            for pair in report['pairs']:
                item = dict(pair)
                if pair['status'] == 'valid':
                    left, right = outcomes[pair['original_id']], outcomes[pair['reversed_id']]
                    anchor = left['choice_id']
                    def margin(row, option):
                        p = row['probabilities']
                        return p[option] - max(v for k, v in p.items() if k != option)
                    item.update(choice_flip=not pair['same_choice'],
                                original_choice_margin_original=margin(left, anchor),
                                original_choice_margin_reversed=margin(right, anchor),
                                target_margin_original=margin(left, left['target_id']),
                                target_margin_reversed=margin(right, right['target_id']))
                pairs.append(item)
            margins[stratum][predictor] = {'coverage_and_tv': report['overall'], 'pairs': pairs}
    write(output / 'exact-order-margins.json', {'definition': 'Margin is probability of specified option minus max probability of another option. Original-choice anchor preserved across reversal; ties are separately reported. Incomplete pairs have no invented margin.', 'strata': margins})
    for expected in pins.values():
        if pin(expected['path']) != expected:
            raise ValueError('Dependency changed during run; no completion receipt')
    write(output / 'completion.json', {'schema_version': 'e5-orchestration/1', 'dependencies': list(pins.values()),
          'commands': commands, 'outputs': [pin(p) for p in sorted(output.rglob('*')) if p.is_file()],
          'cost_gbp': 0, 'model_loads': 0,
          'limitations': 'Evidence files are pinned claims, not checkpoint or chronology attestation. Coverage gaps do not prevent reporting. No combined headline, calibrated confidence, architecture attribution, automatic recommendation or promotion.'})


if __name__ == '__main__':
    main()
