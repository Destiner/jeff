"""Verify published inference bindings, then pin the four-stratum E3 recipe."""
from pathlib import Path
from jeff.evaluation.common import fingerprint, load_examples, input_only, parse_json, write_json

root = Path('/Users/destiner/Code/jeff/artifacts')
e = root / 'evaluation'
m = root / 'model/m4-v2-20261111-01'
receipt_path = m/'inference/receipt.json'
receipt = parse_json(receipt_path.read_text())
inputs = {
    'combined': e/'e3-v2-assembly-v1/inputs.jsonl',
    'reversed': e/'e3-v2-order-v1/reversed-inputs.jsonl',
    'probes': e/'e3-v2-freeze-v1/probes/inputs.jsonl',
    'new': e/'e3-v2-freeze-v1/new-v2/inputs.jsonl',
    'new-reversed': e/'e3-v2-new-order-v1/reversed-inputs.jsonl',
}
input_rows = {k: [parse_json(line) for line in p.read_text().splitlines()] for k,p in inputs.items()}
combined_rows = load_examples(e/'e3-v2-assembly-v1/validation.jsonl')
new_rows = load_examples(e/'e3-v2-freeze-v1/new-v2/validation.jsonl')
order_rows = load_examples(e/'e3-v2-order-v1/validation.jsonl')
new_order_rows = load_examples(e/'e3-v2-new-order-v1/validation.jsonl')
probe_rows = load_examples(e/'e3-v2-freeze-v1/probes/validation.jsonl')
for suite, refs in [('combined',combined_rows),('reversed',order_rows[len(combined_rows):]),('new',new_rows),('new-reversed',new_order_rows[len(new_rows):]),('probes',probe_rows)]:
    if input_rows[suite] != [input_only(row) for row in refs]:
        raise ValueError('Input/reference mismatch: '+suite)

jobs = {}
for job in receipt['jobs']:
    key=job['job'];suite=job['suite']
    if key in jobs or suite not in inputs or job['exit_code'] != 0 or not job['fresh_process']:
        raise ValueError('Bad or duplicate inference job')
    for field in ('input','output'):
        pin=job[field]
        if fingerprint(pin['path'])['sha256'] != pin['sha256']:
            raise ValueError('Inference hash mismatch '+key+' '+field)
        if len(Path(pin['path']).read_bytes().splitlines()) != pin['rows']:
            raise ValueError('Inference row count mismatch '+key+' '+field)
    if job['input']['path'] != str(inputs[suite]) or job['input']['sha256'] != fingerprint(inputs[suite])['sha256']:
        raise ValueError('Wrong input suite '+key)
    if Path(job['output']['path']) != m/'inference'/f'{key}.jsonl':
        raise ValueError('Unexpected prediction destination')
    expected_checkpoint = str(m / key.split('-')[0] / key.split('-')[1]) if key.startswith(('minilm-', 'msmarco-')) else str(root/'model'/('pilot-256-20261111-01' if key.startswith('m2-') else 'msmarco-256-20261111-01')/'checkpoint')
    if job['checkpoint'] != expected_checkpoint:
        raise ValueError('Wrong checkpoint role '+key)
    jobs[key] = job
required={f'{a}-{s}-{u}' for a in ('minilm','msmarco') for s in ('baseline','checkpoint') for u in ('combined','reversed','probes')} | {f'{a}-{u}' for a in ('m2','m3') for u in ('new','new-reversed')}
if set(jobs)!=required:raise ValueError('Incomplete requested job set')

def source(key):
    job=jobs[key]
    return {'predictions':fingerprint(job['output']['path']), 'source_inputs':fingerprint(job['input']['path'])}

historical_path=e/'e3-v2-assembly-v1/historical-reuse.json'
historical=parse_json(historical_path.read_text())
for pin in historical['source_pins']:
    if fingerprint(pin['path']) != pin:raise ValueError('Historical source mutated')
strata={}
for stratum, reference, order_reference, pairs in [
    ('combined',e/'e3-v2-assembly-v1/validation.jsonl',e/'e3-v2-order-v1/validation.jsonl',e/'e3-v2-order-v1/pairs.json'),
    ('inherited-v1',e/'e3-v2-freeze-v1/inherited-v1/validation.jsonl',e/'pilot-order-v1/validation.jsonl',e/'pilot-order-v1/pairs.json'),
    ('new-v2',e/'e3-v2-freeze-v1/new-v2/validation.jsonl',e/'e3-v2-new-order-v1/validation.jsonl',e/'e3-v2-new-order-v1/pairs.json'),
    ('probes',e/'e3-v2-freeze-v1/probes/validation.jsonl',e/'probes-v1/validation.jsonl',e/'probes-v1/pairs.json'),
]:
    predictors={}
    for arch in ('minilm','msmarco'):
        for snapshot in ('baseline','checkpoint'):
            name = 'm4-'+arch+('-random-start' if arch=='minilm' else '-pretrained-start') if snapshot=='baseline' else 'm4-'+arch+'-trained'
            orig=source(f'{arch}-{snapshot}-'+('probes' if stratum=='probes' else 'combined'))
            order_sources=[orig] if stratum=='probes' else [orig,source(f'{arch}-{snapshot}-reversed')]
            predictors[name]={'role':'fresh-start' if snapshot=='baseline' else 'v2-trained','sources':[orig],'order_sources':order_sources}
    for short,label in [('m2','m2-v1-trained'),('m3','m3-v1-trained')]:
        old=historical['candidates'][label]
        if stratum=='probes':
            originals=[{'predictions':old['probes'],'source_reference':fingerprint(e/'probes-v1/validation.jsonl')}]
            ordered=originals
        else:
            original_old={'predictions':old['inherited_original'],'source_reference':fingerprint(e/'data-pilot-v1/validation.jsonl')}
            paired_old={'predictions':old['inherited_paired'],'source_reference':fingerprint(e/'pilot-order-v1/validation.jsonl')}
            originals=([original_old] if stratum!='new-v2' else [])+([source(short+'-new')] if stratum!='inherited-v1' else [])
            ordered=([paired_old] if stratum!='new-v2' else [])+([source(short+'-new'),source(short+'-new-reversed')] if stratum!='inherited-v1' else [])
        predictors[label]={'role':'historical-retained','sources':originals,'order_sources':ordered}
    strata[stratum]={'examples':fingerprint(reference),'order_examples':fingerprint(order_reference),'order_pairs':fingerprint(pairs),'predictors':predictors}
config={'schema_version':'e3-study/1','status':'released-validation','baselines':['uniform','lexical'],
        'source_manifest':fingerprint(root/'data/data-pilot-v2/manifest.json'),
        'freeze_receipt':fingerprint(e/'e3-v2-freeze-v1/receipt.json'),
        'model_inference_receipt':fingerprint(receipt_path),'historical_reuse':fingerprint(historical_path),
        'release_identity_review':fingerprint(e/'e3-release-identity-review-v1/reconciled-evidence.json'),
        'strata':strata}
write_json(e/'e3-v2-assembly-v1/m4-study.json',config)
write_json(e/'e3-v2-assembly-v1/inference-binding.json',{'recipe':fingerprint(e/'e3-v2-assembly-v1/m4-study.json'),'model_receipt':fingerprint(receipt_path),'jobs_verified':len(jobs),'input_identities':'All ordered reference inputs equal exported suite bytes; per-job paths/hashes/counts and checkpoint roles match requested frozen snapshots. Receipts are Model execution evidence, not an Evaluation rerun.','builder':fingerprint(__file__)})
print('Verified all 16 jobs; pinned eight-predictor recipe across combined/inherited/new/probe strata.')
