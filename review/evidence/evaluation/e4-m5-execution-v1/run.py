"""E4 Track A: exact-input existing compare/order/render workflow; no model loads."""
import os
from pathlib import Path
import subprocess
import sys
from jeff.evaluation.common import fingerprint, input_only, load_examples, parse_json, write_json

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
E = ROOT/'evaluation'
M = ROOT/'model/m5-head-lr-20261111-01'
OUT = E/'e4-m5-comparison-v1'
OUT.mkdir(exist_ok=False)
old_recipe = parse_json((E/'e2-m3-v2/recipe.json').read_text())
preregister = parse_json((E/'e4-m5-preregister-v1/receipt.json').read_text())
model_receipt = parse_json((M/'inference/receipt.json').read_text())
print('Model receipt keys:', list(model_receipt))
pins = []
commands = []


def verify(spec):
    actual = fingerprint(spec['path'])
    if actual['sha256'] != spec['sha256']:
        raise ValueError('Input hash changed: '+spec['path'])
    pins.append(actual)
    return Path(actual['path'])


def run(module, args):
    command = [sys.executable, '-m', 'jeff.evaluation.'+module, *map(str,args)]
    result = subprocess.run(command, env=os.environ.copy(), capture_output=True, text=True)
    receipt = {'command':command,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
    commands.append(receipt)
    write_json(OUT/f'command-{len(commands):02d}.json',receipt)
    if result.returncode not in ((0,1) if module in ('compare','order') else (0,)):
        raise ValueError('Workflow failed; receipt retained')


for suite,old_key in [('pilot','comparison.json'),('probes','probes-comparison.json')]:
    historical = old_recipe['comparisons'][old_key]
    ref = verify(historical['examples'])
    rows = load_examples(ref)
    inputs = E/('pilot-baselines-v1/inputs.jsonl' if suite=='pilot' else 'probes-baselines-v1/inputs.jsonl')
    if [parse_json(line) for line in inputs.read_text().splitlines()] != [input_only(row) for row in rows]:
        raise ValueError('Historical input content mismatch')
    pins.append(fingerprint(inputs))
    predictions = {}
    for name,old_name in [('uniform','uniform'),('lexical','lexical'),('m3-pretrained-start','pretrained-msmarco-256'),('m3-historical-trained','trained-msmarco-256'),('m2-context','trained-256')]:
        predictions[name] = verify(historical['predictions'][old_name])
    for snapshot,label in [('baseline','m5-pretrained-start'),('checkpoint','m5-low-head-lr')]:
        path = M/'inference'/f'{snapshot}-{"original" if suite=="pilot" else "probes"}-predictions.jsonl'
        predictions[label] = path
        pins.append(fingerprint(path))
    if predictions['m5-pretrained-start'].read_bytes() != predictions['m3-pretrained-start'].read_bytes():
        raise ValueError('Fresh baseline differs from historical baseline')
    directory=OUT/suite
    directory.mkdir()
    args=['--examples',ref,'--output',directory/'comparison.json']
    for name,path in predictions.items():args+=['--predictions',f'{name}={path}']
    run('compare',args)
    render=['--comparison',directory/'comparison.json','--output',directory/'report.md','--title',f'E4 M5 LR control — {suite}']
    if suite=='probes':
        for name,path in predictions.items():
            order=directory/f'{name}-order.json'
            run('order',['--examples',ref,'--predictions',path,'--pairs',E/'probes-v1/pairs.json','--output',order])
            render+=['--order',f'{name}={order}']
    run('render',render)
for path in [E/'e4-m5-preregister-v1/criterion.json',E/'e4-m5-preregister-v1/historical-bindings.json',E/'probes-v1/pairs.json',M/'inference/receipt.json',Path(__file__)]:pins.append(fingerprint(path))
for pin in list(pins):
    if fingerprint(pin['path'])!=pin:raise ValueError('Changed execution source')
write_json(OUT/'receipt.json',{'study':'E4 M5 LR control','commands':commands,'pins':pins,'outputs':[fingerprint(p) for p in sorted(OUT.rglob('*')) if p.is_file()],'baseline_predictions_byte_identical':True,'scope':'Actual CPU comparison of saved predictions; no training/inference/final-data access. Recorded controls verified separately.'})
print('Completed immutable M5 pilot/probe comparison:',OUT)
