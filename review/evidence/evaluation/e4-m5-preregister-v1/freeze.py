"""Historical-only E4 receipt. Run once; no model imports or M5 inputs."""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from jeff.evaluation.common import load_examples
from jeff.evaluation.metrics import score_examples, summarize

ROOT = Path('/Users/destiner/Code/jeff')
A = ROOT / 'artifacts'
OUT = Path(__file__).parent
W = ROOT / '.worktrees/evaluation'

def load(p):
    return json.loads(Path(p).read_text())

def binding(p):
    p = Path(p)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def save(name, obj):
    with (OUT / name).open('x') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n')

recipe_path = A / 'evaluation/e2-m3-v2/recipe.json'
recipe = load(recipe_path)
verified = {}
def verify(entry):
    actual = binding(entry['path'])
    assert actual['sha256'] == entry['sha256'], entry
    verified[actual['path']] = actual['sha256']
    return Path(actual['path'])

# Reuse the complete E2 receipt, including existing group/order reports.
for section in ('comparisons', 'orders'):
    for spec in recipe[section].values():
        for key, value in spec.items():
            if key == 'predictions' and 'path' not in value:
                for entry in value.values(): verify(entry)
            elif isinstance(value, dict) and 'path' in value: verify(value)

pairs_spec = recipe['orders']['probe-order/trained-msmarco-256.json']['pairs']
pairs = load(verify(pairs_spec))
refs, reports, tables, inputs = {}, {}, {}, {}
for suite, filename, baseline_dir, n in (
    ('pilot', 'comparison.json', 'pilot-baselines-v1', 60),
    ('probes', 'probes-comparison.json', 'probes-baselines-v1', 24)):
    spec = recipe['comparisons'][filename]
    examples = load_examples(verify(spec['examples']))
    assert len(examples) == n and len({e['group_id'] for e in examples}) == 12
    assert all(e['split'] == 'validation' for e in examples)
    refs[suite] = {e['id']: e for e in examples}
    receipt_path = A / 'evaluation' / baseline_dir / 'input-receipt.json'
    receipt = load(receipt_path)
    verify(receipt['examples']); input_path = verify(receipt['inputs'])
    exported = [json.loads(line) for line in input_path.read_text().splitlines()]
    assert exported == [{k: e[k] for k in receipt['label_free_fields']} for e in examples]
    inputs[suite] = {'receipt': binding(receipt_path), **receipt}
    existing = load(verify(spec['output']))
    reports[suite] = {}
    for label, name in [('M3_start', 'pretrained-msmarco-256'), ('M3_trained', 'trained-msmarco-256')]:
        report = score_examples(examples, verify(spec['predictions'][name]))
        assert report['status'] == 'ok' and report['prediction_records'] == n
        assert report['outcomes'] == existing['runs'][name]['outcomes']
        reports[suite][label] = report

probe_refs = refs['probes']
ids = [p[k] for p in pairs for k in ('original_id','reversed_id')]
assert len(pairs) == 12 and len(set(ids)) == 24 and set(ids) == set(probe_refs)
assert len({p['group_id'] for p in pairs}) == 12
pair_identities = []
for pair in pairs:
    a,b = [probe_refs[pair[k]] for k in ('original_id','reversed_id')]
    assert a['options'] == list(reversed(b['options']))
    assert a['group_id'] == pair['group_id']
    assert all(a[k] == b[k] for k in ('state','question','target_id','group_id','task_family','provenance'))
    pair_identities.append({**pair, 'target_id': a['target_id'], 'original_option_ids': [o['id'] for o in a['options']], 'exact_reversal_verified': True})

def snapshot(o, e):
    ordered = sorted([x['id'] for x in e['options']], key=lambda k: -o['probabilities'][k])
    rival = max((k for k in ordered if k != e['target_id']), key=o['probabilities'].get)
    return {'target_rank': ordered.index(e['target_id'])+1, 'target_probability': o['target_probability'],
            'signed_target_minus_best_rival': o['target_probability']-o['probabilities'][rival],
            'best_rival_id': rival, 'choice_id': o['choice_id'], 'correct': o['correct'],
            'log_loss': o['log_loss'], 'loss_status': 'finite' if o['target_probability'] else 'positive_infinity'}

byrun = {name: {o['id']:o for o in report['outcomes']} for name,report in reports['probes'].items()}
for name, outcomes in byrun.items():
    tables[name] = []
    for p in pairs:
        a,b = [outcomes[p[k]] for k in ('original_id','reversed_id')]
        tables[name].append({'group_id':p['group_id'], 'original_id':a['id'], 'reversed_id':b['id'],
            'original':snapshot(a,probe_refs[a['id']]), 'reversed':snapshot(b,probe_refs[b['id']]),
            'pair_mean_loss':summarize([a,b])['log_loss'], 'both_orders_correct':a['correct'] and b['correct'],
            'same_choice':a['choice_id']==b['choice_id']})

lost = [p['group_id'] for p in pairs if byrun['M3_start'][p['original_id']]['correct'] and not byrun['M3_trained'][p['original_id']]['correct']]
assert set(lost) == {'eval.validation.sentiment.03','eval.validation.sentiment.04','eval.validation.rule_application.02'}
macro = {name: math.fsum(x['pair_mean_loss']['mean'] for x in rows)/12 for name,rows in tables.items()}
pilot_loss = reports['pilot']['M3_trained']['overall']['log_loss']['mean']
assert pilot_loss == 0.7937008119799213
run_path = A / 'model/msmarco-256-20261111-01/run.json'
run = load(run_path)
# Reuse R4's existing category definition, restricted to the two historical pilot mechanisms.
r4path = A / 'research/r4-20261111T1145/reproduction-final/diagnosis.json'
r4 = load(r4path)
no_result_text = {'data:pilot-v1:rule_application:g11':'Water reaches no other junctions.',
                  'data:pilot-v1:rule_application:g12':'Elect nobody under this rule.'}
rule_mapping = []
for e in refs['pilot'].values():
    if e['task_family'] != 'rule_application': continue
    matching = [o for o in e['options'] if o['text'].rstrip('.') == no_result_text[e['group_id']].rstrip('.')]
    assert len(matching) == 1
    rule_mapping.append({'id':e['id'], 'group_id':e['group_id'], 'no_result_option_id':matching[0]['id'],
                         'no_result_text':matching[0]['text'], 'target_is_no_result':e['target_id']==matching[0]['id']})
counts = {}
for name, report in reports['pilot'].items():
    outcomes = {o['id']:o for o in report['outcomes']}
    counts[name] = {}
    for group in no_result_text:
        rows = [r for r in rule_mapping if r['group_id']==group]
        counts[name][group] = {'rows':len(rows), 'no_result_targets':sum(r['target_is_no_result'] for r in rows),
            'no_result_choices':sum(outcomes[r['id']]['choice_id']==r['no_result_option_id'] for r in rows),
            'correct':sum(outcomes[r['id']]['correct'] for r in rows)}

save('historical-bindings.json', {'created_at':datetime.now(timezone.utc).isoformat(),
    'recipe':binding(recipe_path), 'verified_E2_files':verified, 'label_free_inputs':inputs,
    'run':binding(run_path), 'controls':{k:run[k] for k in ('config','code','environment','base_model','optimizer','seed_policy')},
    'training_budget':{k:run['training'][k] for k in ('steps','examples_seen','epochs_completed')},
    'data_manifest':binding(run['config']['dataset_manifest']), 'historical_dataset_record':run['dataset'],
    'starting_tensor_hashes_recorded_not_reloaded':run['weights']['before'],
    'pair_identities':pair_identities, 'lost_unique_groups':lost,
    'probe_macro_pair_loss':macro, 'probe_all12group_tables':tables,
    'pilot_metrics':{k:r['overall'] for k,r in reports['pilot'].items()},
    'pilot_rule_category_mapping':rule_mapping, 'pilot_rule_category_counts':counts,
    'R4_reuse':{'diagnosis':binding(r4path),'existing_diagnostic_key':'datasets.pilot.rule_choice_text_counts',
        'existing_counts':r4['datasets']['pilot']['rule_choice_text_counts'],
        'script':binding(W/'experiments/research/diagnose_m3_regression.py')},
    'scorer_source':binding(W/'src/jeff/evaluation/metrics.py')})

save('criterion.json', {'schema_version':'e4-m5-preregister/1', 'created_at':datetime.now(timezone.utc).isoformat(),
    'status':'frozen_before_any_M5_outcome_access; owner_scores_later',
    'hypothesis':'One scalar-head LR change 5e-4 -> 2e-5; encoder/native pooler stay 2e-5.',
    'historical_bindings':binding(OUT/'historical-bindings.json'),
    'all_required':True, 'criteria':{
        'recovery':{'eligible_groups':lost, 'minimum':1, 'definition':'target rank 1 in BOTH original and reversed presentation; count each source group once'},
        'no_newly_wrong_groups':{'maximum':0, 'definition':'no previously correct historical-trained presentation becomes wrong in either order; assess all 12 groups'},
        'probe_loss':{'operator':'strictly_less_than', 'historical_value':macro['M3_trained'],
            'definition':'arithmetic mean over all 12 source-group mean losses; each group mean includes its original and reversal losses, NOT loss of averaged probabilities'},
        'pilot_loss':{'operator':'less_than_or_equal', 'historical_exact':pilot_loss, 'allowance':0.05,
            'maximum':pilot_loss+0.05, 'definition':'all 60 original pilot decisions, row mean natural-log loss via existing scorer'}},
    'coverage_precondition':{'pilot':{'valid_rows':60,'source_groups':12},'probes':{'valid_rows':24,'complete_exact_reversal_pairs':12,'source_groups':12},
        'required':'exact frozen reference IDs and option sets; no missing, invalid, duplicate, extra, unidentifiable predictions; compare-bound reference and prediction hashes verified; no conditional-only success',
        'on_failure':'explicit coverage/control failure; success=false, do not score partial sets as success'},
    'control_precondition':'Owner verifies source/data/config/runtime controls and fresh retained-head starting-state identity against bound historical run before interpreting intervention. A mismatch is explicit noncomparable, never criterion success.',
    'ranking':'descending normalized probabilities, deterministic exact ties resolved using original reference option order for original ranks; reversed presentation uses its own frozen reference order as existing scorer requires; never average ranks or probabilities to claim recovery',
    'reporting':'show all 12 original ranks/p(target)/signed target-minus-best-rival margins/losses plus reversal and pair-loss diagnostics, even on failure; signed probability margins are not logits or top-two confidence',
    'nonfinite_loss':'zero target mass means positive infinity, not clipped; cannot pass lower finite probe or bounded pilot loss',
    'limitations':['Probe labels are all teacher labels, teacher identity unknown; agreement is not independently verified correctness.',
        'Pilot has 40 teacher and 20 rule-verified labels; no-result category diagnostic is descriptive, not an extra selection threshold.',
        'M2 is descriptive context only, not a causal comparator.', 'Single-seed historical comparison remains vulnerable to MPS/stochastic variation; no significance, calibration, final-data or causal proof claim.',
        'No thresholds/group exclusions may change in response to M5 outcomes.'],
    'receipt_method':{'script':binding(Path(__file__)), 'CPU_only':True,'M5_outcomes_read':False,'spend_GBP':0}})
print(json.dumps({'pilot_exact':pilot_loss,'probe_macro':macro,'lost':lost,'rule_counts':counts},indent=2))
