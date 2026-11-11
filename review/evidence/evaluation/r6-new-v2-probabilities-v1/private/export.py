"""Bounded real saved-probability export. No inference, targets, or scorer imports."""
import collections
import hashlib
import json
import math
from pathlib import Path
import secrets
import struct
import sys
import uuid
from datetime import datetime, timezone

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
WORK = Path('/Users/destiner/Code/jeff/.worktrees/evaluation')
OUT = ROOT / 'evaluation/r6-new-v2-probabilities-v1'
PUB = OUT / 'public'
PRIV = OUT / 'private'
PINS = {}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p, expected=None):
    p = Path(p)
    h = sha(p)
    if expected is not None:
        assert h == expected, 'source pin mismatch'
    PINS[str(p)] = h
    return json.loads(p.read_text())

def pinned(spec):
    p = Path(spec['path'])
    assert sha(p) == spec['sha256'], 'source pin mismatch'
    PINS[str(p)] = spec['sha256']
    rows = [json.loads(line) for line in p.read_text().splitlines()]
    return rows

def index(rows):
    result = {r['id']: r for r in rows}
    assert len(result) == len(rows), 'duplicate IDs'
    return result

def dump(p, value):
    with p.open('x') as f:
        f.write(json.dumps(value, indent=2, allow_nan=False) + '\n')

def bits(v):
    return struct.pack('>d', v)

def uid():
    return str(uuid.uuid4())

assert sys.version_info[:2] == (3, 12)
assert not PUB.exists(), 'fresh export only'
PUB.mkdir()
cfg = load(WORK / 'configs/evaluation/e5-p3-v1.json')
new = cfg['strata']['new-v2']
q = new['predictors']['qwen25-05b-instruct-frozen']['order_sources']
assert q[0]['predictions']['path'] == str(ROOT / 'release/p3-qwen-20261111-01/run-02/v2-original.jsonl')
assert q[1]['predictions']['path'] == str(ROOT / 'release/p3-qwen-20261111-01/run-02/v2-reversed.jsonl')
manifest = load(cfg['source_manifest']['path'], cfg['source_manifest']['sha256'])
assert cfg['source_manifest']['sha256'] == 'd97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac'
pairs = load(new['order_pairs']['path'], new['order_pairs']['sha256'])
units_doc = load(ROOT / 'evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json')
assert units_doc['manifest_sha256'] == cfg['source_manifest']['sha256']
units = units_doc['by_validation_id']
orig_all = index(pinned(q[0]['source_inputs']))
rev_all = index(pinned(q[1]['source_inputs']))
pred_o = index(pinned(q[0]['predictions']))
pred_r = index(pinned(q[1]['predictions']))
small_o_spec = new['predictors']['m2-v1-trained']['sources'][0]['source_inputs']
small_r_spec = new['predictors']['m2-v1-trained']['order_sources'][1]['source_inputs']
orig_new = index(pinned(small_o_spec))
rev_new = index(pinned(small_r_spec))
assert len(orig_all) == len(rev_all) == len(pred_o) == len(pred_r) == 300
assert set(orig_all) == set(pred_o) and set(rev_all) == set(pred_r)
assert len(pairs) == len(orig_new) == len(rev_new) == 240
assert {p['original_id'] for p in pairs} == set(orig_new)
assert {p['reversed_id'] for p in pairs} == set(rev_new)
assert len({p['pair_id'] for p in pairs}) == 240
assert all(orig_all[k] == v for k, v in orig_new.items())
assert all(rev_all[k] == v for k, v in rev_new.items())
# Complete development membership is established from preserved pair records, not ID parsing.
inherited_spec = cfg['strata']['inherited-v1']['order_pairs']
inherited_pairs = load(inherited_spec['path'], inherited_spec['sha256'])
all_pairs = pairs + inherited_pairs
assert len(all_pairs) == 300
assert {p['original_id'] for p in all_pairs} == set(orig_all)
assert {p['reversed_id'] for p in all_pairs} == set(rev_all)
for rows in (orig_all, rev_all, orig_new, rev_new):
    for r in rows.values():
        assert set(r) == {'schema_version', 'id', 'state', 'question', 'options'}
        assert r['schema_version'] == '0.1'
        assert isinstance(r['state'], str) and isinstance(r['question'], str)
        assert len(r['options']) >= 2
        assert len({o['id'] for o in r['options']}) == len(r['options'])
        assert all(set(o) == {'id', 'text'} and isinstance(o['id'], str) and isinstance(o['text'], str) for o in r['options'])
for p in all_pairs:
    a, b = orig_all[p['original_id']], rev_all[p['reversed_id']]
    assert a['state'] == b['state'] and a['question'] == b['question']
    assert a['options'][::-1] == b['options'], 'not exact reversal'
for predictions, inputs in ((pred_o, orig_all), (pred_r, rev_all)):
    for k, r in predictions.items():
        assert set(r) == {'schema_version', 'id', 'probabilities'}
        ps = r['probabilities']
        assert all(set(p) == {'option_id', 'probability'} for p in ps)
        assert len(ps) == len(inputs[k]['options'])
        assert {p['option_id'] for p in ps} == {o['id'] for o in inputs[k]['options']}
        assert all(type(p['probability']) in (float, int) and math.isfinite(p['probability']) and 0 <= p['probability'] <= 1 for p in ps)

kinds = ['source_group', 'domain', 'policy_instance', 'mechanism', 'producer']
maps = {k: {} for k in kinds}
option_map = {}
case_map = {}
raw_records = []
public = []
for p in pairs:
    oid, rid = p['original_id'], p['reversed_id']
    u = units[oid]
    assert u['stratum'] == 'new-v2' and u['assignment']['split'] == 'validation'
    assert u['id'] == oid and u['group_id'] == p['group_id']
    family = u['task_family']
    assert family in {'intent', 'sentiment', 'rule_application'}
    raw = {'source_group': u['group_id'], **{k: u.get(k) for k in kinds[1:]}}
    assert raw['producer'] is not None
    r = {'case_id': uid(), 'task_family': family}
    for kind in kinds:
        value = raw[kind]
        assert value is None or isinstance(value, str)
        if value is not None:
            maps[kind].setdefault(value, uid())
        r[kind] = maps[kind].get(value)
    r['construction_cluster'] = r['producer']
    options = [o['id'] for o in orig_new[oid]['options']]
    for option in options:
        option_map.setdefault(option, uid())
    a = {p['option_id']: p['probability'] for p in pred_o[oid]['probabilities']}
    b = {p['option_id']: p['probability'] for p in pred_r[rid]['probabilities']}
    rev_options = [o['id'] for o in rev_new[rid]['options']]
    r.update(K=len(options), option_ids=[option_map[o] for o in options], original_p=[a[o] for o in options], reversed_p=[b[o] for o in options], original_positions=list(range(1, len(options)+1)), reversed_positions=[rev_options.index(o)+1 for o in options])
    case_map[r['case_id']] = {'original_id': oid, 'reversed_id': rid, 'pair_id': p['pair_id'], 'option_ids': options}
    raw_records.append({'task_family': family, **raw})
    public.append(r)
secrets.SystemRandom().shuffle(public)
assert [case_map[r['case_id']]['original_id'] for r in public] != [p['original_id'] for p in pairs]

def grouping(records):
    stats = {}
    for kind in kinds:
        vals = [r[kind] for r in records]
        stats[kind] = {'distinct_nonnull': len(set(vals)-{None}), 'null_rows': vals.count(None)}
    nesting = {}
    for child, parent in [(k, 'producer') for k in kinds[:-1]] + [('policy_instance', 'mechanism')]:
        edges = collections.defaultdict(set)
        unknown = 0
        for r in records:
            if r[child] is None or r[parent] is None:
                unknown += 1
            else:
                edges[r[child]].add(r[parent])
        nesting[child+'->'+parent] = {'observed_child_units': len(edges), 'violating_child_units': sum(len(v)>1 for v in edges.values()), 'excluded_null_rows': unknown, 'functional_on_observed': all(len(v)==1 for v in edges.values())}
    return {'units': stats, 'nesting': nesting}

groups = grouping(public)
assert groups == grouping(raw_records)
assert all(n['functional_on_observed'] for n in groups['nesting'].values())
assert groups['units']['producer']['distinct_nonnull'] == 6
by_family = {f: {'rows': sum(r['task_family']==f for r in public), **grouping([r for r in public if r['task_family']==f])} for f in sorted({r['task_family'] for r in public})}
assert all(x['units']['producer']['distinct_nonnull'] == 2 for x in by_family.values())
public_keys = {'case_id', 'task_family', *kinds, 'construction_cluster', 'K', 'option_ids', 'original_p', 'reversed_p', 'original_positions', 'reversed_positions'}

def validate_row(r):
    assert type(r) is dict and set(r) == public_keys
    assert r['task_family'] in by_family
    for k in ['case_id', *kinds, 'construction_cluster']:
        assert r[k] is None and k in kinds or type(r[k]) is str and str(uuid.UUID(r[k])) == r[k] and uuid.UUID(r[k]).version == 4
    assert type(r['K']) is int and r['K'] >= 2
    for k in ['option_ids', 'original_p', 'reversed_p', 'original_positions', 'reversed_positions']:
        assert type(r[k]) is list and len(r[k]) == r['K']
    assert all(type(v) is str and str(uuid.UUID(v)) == v and uuid.UUID(v).version == 4 for v in r['option_ids'])
    assert len(set(r['option_ids'])) == r['K']
    for k in ['original_p', 'reversed_p']:
        assert all(type(v) in (int,float) and math.isfinite(v) and 0<=v<=1 for v in r[k])
    assert all(type(v) is int for k in ['original_positions','reversed_positions'] for v in r[k])
    assert r['original_positions'] == list(range(1,r['K']+1))
    assert r['reversed_positions'] == list(range(r['K'],0,-1))
    assert r['construction_cluster'] == r['producer']

for r in public:
    validate_row(r)
with (PUB/'paired.jsonl').open('x') as f:
    for r in public:
        f.write(json.dumps(r, allow_nan=False, separators=(',', ':'))+'\n')
roundtrip = [json.loads(line) for line in (PUB/'paired.jsonl').read_text().splitlines()]
assert len(roundtrip) == 240 and len({r['case_id'] for r in roundtrip}) == 240
bitwise_count = 0
for r in roundtrip:
    validate_row(r)
    m = case_map[r['case_id']]
    u = units[m['original_id']]
    assert r['task_family'] == u['task_family']
    for kind in kinds:
        raw = u['group_id'] if kind == 'source_group' else u.get(kind)
        assert r[kind] == maps[kind].get(raw)
    assert r['option_ids'] == [option_map[o] for o in m['option_ids']]
    for key, predictions, rawid in [('original_p',pred_o,m['original_id']), ('reversed_p',pred_r,m['reversed_id'])]:
        rawp = {p['option_id']:p['probability'] for p in predictions[rawid]['probabilities']}
        for option, value in zip(m['option_ids'],r[key]):
            assert bits(value) == bits(rawp[option]), 'raw probability changed'
            bitwise_count += 1
assert grouping(roundtrip) == groups
for kind, table in {**maps, 'option':option_map}.items():
    assert len(table) == len(set(table.values()))

# Compare every public string leaf against all input text/IDs and explicit raw unit IDs.
forbidden = set()
for rows in (orig_all,rev_all):
    for r in rows.values():
        forbidden.update([r['id'],r['state'],r['question']])
        for o in r['options']:
            forbidden.update([o['id'],o['text']])
for p in all_pairs:
    forbidden.update(p.values())
for r in raw_records:
    forbidden.update(v for k,v in r.items() if k!='task_family' and v is not None)
forbidden.discard('')

def leaves(v):
    if isinstance(v, dict):
        for x in v.values():
            yield from leaves(x)
    elif isinstance(v,list):
        for x in v:
            yield from leaves(x)
    elif isinstance(v,str):
        yield v

def no_leak(v):
    for s in leaves(v):
        assert s not in forbidden, 'raw string leaf leakage'
        assert not any(x in s for x in forbidden if len(x)>=12), 'raw identifier/text substring leakage'

no_leak(roundtrip)
errors = [abs(math.fsum(r[k])-1) for r in roundtrip for k in ['original_p','reversed_p']]
zeros = sum(v==0 for r in roundtrip for k in ['original_p','reversed_p'] for v in r[k])
coverage = {'pairs':240, 'rows':240, 'vectors':480, 'original_presentations':240, 'reversed_presentations':240, 'option_identities':sum(r['K'] for r in roundtrip), 'probability_values':bitwise_count, 'missing_pairs':0, 'missing_options':0, 'family_rows':{f:x['rows'] for f,x in by_family.items()}, 'K_rows':dict(sorted(collections.Counter(str(r['K']) for r in roundtrip).items()))}
normalization = {'convention':'Raw saved conditional answer-symbol probabilities, Python JSON number to binary64 to shortest round-trip JSON number; exact binary64 bit patterns preserved, including zeros. No scorer renormalization.', 'renormalized':False, 'epsilon_added':False, 'clipped':False, 'zero_values':zeros, 'max_absolute_sum_error_fsum':max(errors), 'mean_absolute_sum_error_fsum':math.fsum(errors)/len(errors), 'vectors_with_nonzero_sum_error':sum(e!=0 for e in errors), 'full_vocabulary_mass':'not available; not inferred'}
readme = '''# Anonymous paired probability export

240 NEW-v2 development decisions, two preserved P3 presentations per decision. No new inference or learning. Each row contains a random UUID case identity, task family, explicit anonymous scientific grouping units, K, ordered anonymous option identities and two probability vectors aligned to the ORIGINAL option identities. Position arrays are one-based positions of those same identities in each presentation; exact full reversal was checked against frozen label-free inputs before export. Public rows are randomly shuffled.

All kind-specific UUIDs are stable within this export, not across exports. Null means not explicitly recorded; no identities are parsed from names. construction_cluster equals producer: the broadest observed recorded construction unit (6 overall, 2 per family). Distinct units and functional nesting, including null exclusions, are in receipt.json. These are explicit scientific grouping variables, not evidence of independent sampling. All producers share teacher/common-renderer dependence. Held-out producer is a conservative observed-cluster split, NOT guaranteed independence.

Probabilities are the exact saved conditional answer-symbol values before any scorer normalization. JSON round trips preserve Python binary64 bit patterns; decimal spelling need not reproduce the source spelling. No epsilon, clipping, renormalization or invented full-vocabulary mass. These are not calibrated confidences. No text, targets, correctness, labels, rationales, raw identifiers or auxiliary scores are included.

Pseudonymization is procedural, not an OS-security or non-reidentifiability guarantee. Join structure, family, option counts and probability fingerprints remain observable. Owner review is required before onward Research delivery. receipt.json is written last as the completion marker. Only this public directory is intended for onward delivery.
'''
with (PUB/'README.md').open('x') as f:
    f.write(readme)
no_leak(readme)
export_hash = sha(Path(__file__))
receipt = {'schema_version':'anonymous-paired-probabilities/1', 'status':'complete-awaiting-owner-review', 'created_utc':datetime.now(timezone.utc).isoformat(), 'coverage':coverage, 'grouping':groups, 'by_family':by_family, 'construction_cluster_kind':'producer', 'exact_reversal_verified_pairs':240, 'full_development_input_presentations_verified':600, 'normalization':normalization, 'source_sha256':{'original_predictions':q[0]['predictions']['sha256'], 'reversed_predictions':q[1]['predictions']['sha256'], 'released_manifest':cfg['source_manifest']['sha256']}, 'exporter_sha256':export_hash, 'paired_sha256':sha(PUB/'paired.jsonl'), 'readme_sha256':sha(PUB/'README.md'), 'limitations':['Shared teacher/common renderer dependence; held-out producer is not guaranteed independence.', 'Procedural pseudonymization only; structure and probability fingerprints remain observable.', 'Conditional answer-symbol probabilities only; not calibration or full-vocabulary mass.'], 'privacy_validation':{'recursive_row_allowlist':True,'input_string_and_raw_unit_leakage_checks':True,'raw_probability_bitwise_equality':True,'mapping_and_nesting_roundtrip':True,'random_uuid_v4_ids':True,'random_row_order':True}, 'owner_review_required':True}
# Recursively freeze the exact allowed receipt structure and scalar types before serialization.
def schema(v):
    if isinstance(v,dict): return {k:schema(x) for k,x in v.items()}
    if isinstance(v,list): return [schema(x) for x in v]
    return type(v).__name__
receipt_schema = schema(receipt)
assert schema(json.loads(json.dumps(receipt,allow_nan=False))) == receipt_schema
no_leak(receipt)
for s in leaves(receipt):
    assert '/' not in s or s == 'anonymous-paired-probabilities/1' or s in receipt['limitations']
dump(PRIV/'mapping.json', {'cases':case_map,'kind_maps_raw_to_anonymous':maps,'options_raw_to_anonymous':option_map})
dump(PRIV/'public-schema.json', {'row_keys':sorted(public_keys),'receipt_exact_structure_and_types':receipt_schema})
dump(PRIV/'source-pins.json', {'sha256_by_absolute_path':PINS,'exporter_sha256':export_hash,'reviewed_source_units_pin_basis':'SHA256 captured before processing; manifest identity matched pinned E5 released manifest; explicit reviewed metadata used without target/reference access.','authorization':['Leader R6support7ea66844','Research request e013187a']})
dump(PRIV/'validation-receipt.json', {'status':'passed', 'coverage':coverage,'grouping':groups,'source_pins':PINS,'exporter_sha256':export_hash,'mapping_sha256':sha(PRIV/'mapping.json'),'public_schema_sha256':sha(PRIV/'public-schema.json'),'paired_sha256':receipt['paired_sha256'],'readme_sha256':receipt['readme_sha256'],'raw_bitwise_values_checked':bitwise_count,'forbidden_distinct_strings_checked':len(forbidden),'exact_reversal_all_development_pairs':300,'strict_label_free_full_inputs':True,'read_targets_or_labeled_references':False,'validation_kind':'actual export data/privacy validation; no software tests or lint','python_executable':sys.executable,'python_version':sys.version,'public_receipt_content_sha256':hashlib.sha256((json.dumps(receipt,indent=2,allow_nan=False)+'\n').encode()).hexdigest()})
# No writes follow this completion marker.
dump(PUB/'receipt.json',receipt)
print(json.dumps({'status':'complete-awaiting-owner-review','paired_sha256':receipt['paired_sha256'],'receipt_sha256':sha(PUB/'receipt.json'),'coverage':coverage,'grouping':groups,'zero_values':zeros,'max_sum_error':max(errors)},indent=2))
