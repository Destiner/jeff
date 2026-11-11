"""Bind released reference identities to existing inference without model loads."""
from pathlib import Path
from jeff.evaluation.common import fingerprint, input_only, load_examples, parse_json, write_json

root = Path('/Users/destiner/Code/jeff/artifacts')
e = root / 'evaluation'
recipe_path = e / 'e2-m3-v2/recipe.json'
recipe = parse_json(recipe_path.read_text())
pins = [fingerprint(recipe_path)]

def verify(pin):
    actual = fingerprint(pin['path'])
    if actual != pin:
        raise ValueError(f'Historical source changed: {pin["path"]}')
    pins.append(actual)
    return Path(pin['path'])

def refs(path):
    rows = load_examples(path)
    if not rows or any(r['split'] != 'validation' for r in rows):
        raise ValueError('Validation only')
    pins.append(fingerprint(path))
    return {r['id']: r for r in rows}

old = refs(verify(recipe['comparisons']['comparison.json']['examples']))
inherited = refs(e / 'e3-v2-freeze-v1/inherited-v1/validation.jsonl')
if old != inherited:
    raise ValueError('Inherited references differ from historical full rows')
old_order = refs(e / 'pilot-order-v1/validation.jsonl')
full_order = refs(e / 'e3-v2-order-v1/validation.jsonl')
if any(full_order.get(k) != r for k, r in old_order.items()):
    raise ValueError('Inherited order reference mismatch')
old_probes = refs(verify(recipe['comparisons']['probes-comparison.json']['examples']))
probes = refs(e / 'e3-v2-freeze-v1/probes/validation.jsonl')
if old_probes != probes:
    raise ValueError('Probe reference mismatch')

inputs = {}
for key, old_path, current_path in [
    ('inherited', e/'pilot-baselines-v1/inputs.jsonl', e/'e3-v2-freeze-v1/inherited-v1/inputs.jsonl'),
    ('probes', e/'probes-baselines-v1/inputs.jsonl', e/'e3-v2-freeze-v1/probes/inputs.jsonl'),
]:
    old_rows = [parse_json(line) for line in old_path.read_text().splitlines()]
    current_rows = [parse_json(line) for line in current_path.read_text().splitlines()]
    if old_rows != current_rows or any(r != input_only(r) for r in current_rows):
        raise ValueError('Ordered label-free input mismatch')
    inputs[key] = {'historical': fingerprint(old_path), 'current': fingerprint(current_path),
                   'canonical_ordered_inputs_equal': True, 'bytes_equal': old_path.read_bytes() == current_path.read_bytes()}

candidates = {}
for label, old_name in [('m2-v1-trained', 'trained-256'), ('m3-v1-trained', 'trained-msmarco-256')]:
    original = recipe['comparisons']['comparison.json']['predictions'][old_name]
    probe = recipe['comparisons']['probes-comparison.json']['predictions'][old_name]
    paired = recipe['orders'][f'order/{old_name}.json']['predictions']
    for pin in (original, probe, paired):
        verify(pin)
    candidates[label] = {'role': 'historical-retained', 'inherited_original': original,
                         'inherited_paired': paired, 'probes': probe,
                         'basis': 'Existing E2 hashed snapshots; unchanged full labeled references and ordered decision inputs. Not fresh M4 starts.'}
write_json(e/'e3-v2-assembly-v1/historical-reuse.json', {
    'schema_version':'evaluation/e3-historical-reuse/1', 'source_pins':pins,
    'input_identity': inputs, 'candidates':candidates,
    'checks': {'unchanged_full_inherited_rows':len(inherited), 'unchanged_inherited_paired_presentations':len(old_order),
               'unchanged_full_probe_rows':len(probes)},
    'scope':'No inference or rescoring. No final access. Full rows/ordered inputs checked; old checkpoint authenticity remains existing Model/E2 evidence.'})
print('Bound retained M2/M3 existing original/paired/probe predictions to identical released inherited/probe references.')
