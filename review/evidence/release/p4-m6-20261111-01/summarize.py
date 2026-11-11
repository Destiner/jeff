"""Summarize the actual P4 pass and validate only its label-free output contract."""
import hashlib
import json
import math
from pathlib import Path
import re

base = Path(__file__).resolve().parent

def read(name):
    return json.loads((base / name).read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

run = read('run/receipt.json')
process = read('process-receipt.json')
audit = read('audit/audit.json')['evidence']
if run['status'] != 'complete' or process['returncode'] != 0:
    raise ValueError('not a completed actual run')
validation = {'scope': 'Label-free output contract/identity validation only; no reference labels or quality scoring.', 'suites': []}
for suite in audit['suites']:
    entry = suite['input']
    source = Path(entry['path'])
    if sha(source) != entry['sha256']:
        raise ValueError('source input changed')
    output = base / 'run' / (entry['name'] + '.jsonl')
    inputs = [json.loads(line) for line in source.read_text().splitlines()]
    predictions = [json.loads(line) for line in output.read_text().splitlines()]
    if len(inputs) != len(predictions) or len(inputs) != entry['rows']:
        raise ValueError('coverage mismatch')
    count, maximum_error = 0, 0.0
    for row, prediction in zip(inputs, predictions):
        if (set(prediction) != {'schema_version', 'id', 'probabilities'} or
                prediction['schema_version'] != '0.1' or row['id'] != prediction['id']):
            raise ValueError('prediction schema/id mismatch')
        values = prediction['probabilities']
        if ([o['id'] for o in row['options']] != [v['option_id'] for v in values] or
                any(set(v) != {'option_id', 'probability'} for v in values)):
            raise ValueError('option identity mismatch')
        probabilities = [v['probability'] for v in values]
        if any(not math.isfinite(p) or not 0 <= p <= 1 for p in probabilities):
            raise ValueError('invalid probability')
        error = abs(sum(probabilities) - 1)
        if error > 1e-6:
            raise ValueError('probability sum mismatch')
        maximum_error = max(maximum_error, error)
        count += len(values)
    validation['suites'].append({'name': entry['name'], 'rows': len(inputs), 'options': count,
        'maximum_sum_error': maximum_error, 'input_sha256': entry['sha256'], 'output_sha256': sha(output)})
binding = audit['trained_checkpoint']
manifest = binding['manifest']
files = ['audit/audit.json', 'run/receipt.json', 'process-invocation.json', 'process-receipt.json',
         'process.stderr.log', 'launch.py'] + ['run/' + s['name'] + '.jsonl' for s in run['suites']]
result = {
    'schema_version': 'jeff.runtime.trained-checkpoint-result.v1',
    'status': 'fresh-process trained-checkpoint inference complete; independent scoring owned by E6',
    'frozen_runtime_code_revision': audit['git_revision'],
    'runtime_source_sha256': audit['source_sha256'],
    'runtime_validator_source_sha256': binding['validator_source_sha256'],
    'config_sha256': audit['config_sha256'], 'chat_template_sha256': audit['chat_template_sha256'],
    'trained_checkpoint_manifest_path': binding['manifest_path'],
    'trained_checkpoint_manifest_sha256': binding['manifest_sha256'],
    'checkpoint_id': manifest['checkpoint_id'], 'run_id': manifest['run_id'], 'kind': 'trained',
    'base_lineage': {'model_id': manifest['base_model_id'], 'revision': manifest['base_revision']},
    'trained_weights': manifest['files']['model.safetensors'],
    'training_code_revision': manifest['training_code_revision'],
    'training_data_manifest_sha256': manifest['training_data_manifest_sha256'],
    'training_recipe_sha256': manifest['training_recipe_sha256'],
    'training_schedule_sha256': manifest['training_schedule_sha256'],
    'source_run_receipt': binding['source_run_receipt'],
    'environment': audit['environment'], 'validation': validation,
    'presentations': sum(s['written_rows'] for s in run['suites']),
    'options': sum(s['options'] for s in validation['suites']),
    'process_wall_seconds': process['wall_seconds'], 'model_load_seconds': run['cold_load_seconds'],
    'startup': run['startup'], 'suite_wall_seconds': sum(s['elapsed_seconds'] for s in run['suites']),
    'suites': [{k: v for k, v in s.items() if k != 'forward_seconds'} for s in run['suites']],
    'cpu_lifetime_maxrss_bytes': run['cpu_lifetime_maxrss_bytes'],
    'mps_observed_samples': run['memory_samples'], 'memory_qualification': run['memory_qualification'],
    'completed_at': process['completed_at'], 'additional_spend_gbp': 0,
    'artifact_root': str(base),
    'artifacts': {name: {'bytes': (base / name).stat().st_size, 'sha256': sha(base / name)} for name in files},
}
footprint = re.search(r'(\d+)\s+peak memory footprint', (base / 'process.stderr.log').read_text())
if footprint:
    result['macos_peak_process_footprint_bytes'] = int(footprint[1])
    result['memory_qualification'] += '; native process footprint is separate OS accounting, not a true MPS/unified-memory peak; do not sum overlapping metrics.'
result['decisions_per_second'] = result['presentations'] / result['suite_wall_seconds']
for name, data in [('output-validation.json', validation), ('delivery-summary.json', result)]:
    with (base / name).open('x') as stream:
        json.dump(data, stream, indent=2); stream.write('\n')
print(json.dumps({k: result[k] for k in ('checkpoint_id', 'presentations', 'options', 'process_wall_seconds', 'model_load_seconds', 'decisions_per_second')}, indent=2))
