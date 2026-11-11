"""CPU-only release rebind of e3-identity-review-v1/review.py's identity algorithm.
No project imports, model loads, final content, network, tests or source edits.
Run once: refuses to overwrite evidence.
"""
import collections
import hashlib
import json
import unicodedata
from pathlib import Path

ROOT = Path('/Users/destiner/Code/jeff')
ART = ROOT / 'artifacts'
OUT = Path(__file__).resolve().parent
EXPECTED = 'd97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac'
errors, receipts = [], []


def digest(b):
    return hashlib.sha256(b).hexdigest()


def safe(p):
    p = Path(p).resolve()
    if 'final' in p.parts or not p.is_relative_to(ROOT):
        raise ValueError('Refusing protected/outside path')
    return p


def load(p):
    return json.loads(safe(p).read_bytes())


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def check(ok, context):
    if not ok:
        errors.append(context)
    return ok


def hash_check(p, expected, role):
    p = safe(p)
    actual = digest(p.read_bytes())
    receipts.append({'path': str(p.relative_to(ROOT)), 'role': role, 'sha256': actual,
                     'expected_sha256': expected, 'matches': check(actual == expected, 'hash: ' + str(p))})
    return actual


def manifest_rows(p):
    m = load(p)
    records = []
    receipts.append({'path': str(p.relative_to(ROOT)), 'role': 'manifest', 'sha256': digest(p.read_bytes())})
    for s in m['shards']:
        if s['split'] not in ('train', 'validation'):
            raise ValueError('Refusing non-development manifest')
        path = safe(ART / s['path'])
        hash_check(path, s['sha256'], 'shard')
        rows = [json.loads(line) for line in path.read_bytes().splitlines() if line.strip()]
        check(len(rows) == s['rows'], 'row count: ' + s['path'])
        check(all(r['split'] == s['split'] for r in rows), 'split: ' + s['path'])
        records.extend((r, s['path']) for r in rows)
    return m, records


# Same decision key as earlier review: option IDs deliberately excluded.
def decision(r, mode='exact', ordered=False):
    def text(s):
        if mode in ('nfc', 'nfc_outerstrip'):
            s = unicodedata.normalize('NFC', s)
        return s.strip() if mode in ('outerstrip', 'nfc_outerstrip') else s
    opts = [text(o['text']) for o in r['options']]
    return canonical([text(r['state']), text(r['question']), opts if ordered else sorted(opts)])


v2p = ART / 'data/data-pilot-v2/manifest.json'
provp = v2p.with_name('provenance.json')
hash_check(v2p, EXPECTED, 'release-pin')
v2, current = manifest_rows(v2p)
prov = load(provp)
v1p = ROOT / '.worktrees/evaluation/manifests/data/pilot-v1.json'
v1provp = v1p.with_name('pilot-v1.provenance.json')
v1, old = manifest_rows(v1p)
_, published_old = manifest_rows(ART / prov['parent']['manifest'])
hash_check(ART / prov['parent']['manifest'], prov['parent']['sha256'], 'parent-manifest')
check(old == published_old, 'published parent differs from tracked v1')
retained = sum(s in v2['shards'] for s in v1['shards'])
check(retained == 6, 'six inherited shards not retained exactly')
_, tiny = manifest_rows(v1p.with_name('tiny-v1.json'))
_, probes = manifest_rows(ART / 'evaluation/probes-v1/manifest.json')
old_ids = {r['id']: r for r, _ in old}
old_groups = {r['group_id'] for r, _ in old}
classified = []
for r, path in current:
    inherited = r['id'] in old_ids
    if inherited:
        check(r == old_ids[r['id']], 'changed inherited row: ' + r['id'])
    else:
        check(r['group_id'] not in old_groups, 'new row in inherited group: ' + r['id'])
    classified.append((r, path, 'inherited-v1' if inherited else 'new-v2'))
check(len({r['id'] for r, _ in current}) == len(current), 'duplicate release IDs')
train_groups = {r['group_id'] for r, _ in current if r['split'] == 'train'}
val_groups = {r['group_id'] for r, _ in current if r['split'] == 'validation'}
check(not train_groups & val_groups, 'cross-split release groups')

prior = {
    'pilot-v1-validation': [(r,p) for r,p in old if r['split']=='validation'],
    'tiny-v1-validation': [(r,p) for r,p in tiny if r['split']=='validation'],
    'existing-probes': probes,
    'released-validation': [(r,p) for r,p in current if r['split']=='validation'],
}
for name, p in [('superseded-sentiment-validation', ART/'data/data-pilot-v1/sentiment/validation.jsonl'),
                ('pilot-order-variants', ART/'evaluation/pilot-order-v1/validation.jsonl')]:
    rows = [json.loads(line) for line in safe(p).read_bytes().splitlines() if line.strip()]
    check(all(r['split']=='validation' for r in rows), 'non-validation historical reference')
    receipts.append({'path':str(p.relative_to(ROOT)), 'sha256':digest(p.read_bytes()), 'role':'historical-reference', 'rows':len(rows)})
    prior[name] = [(r, str(p.relative_to(ART))) for r in rows]
checks = []
funcs = {'id': lambda r:r['id'], 'group_id':lambda r:r['group_id']}
for mode in ('exact', 'nfc', 'outerstrip', 'nfc_outerstrip'):
    for ordered in (True, False):
        funcs['decision_' + mode + ('_ordered' if ordered else '_order_free')] = lambda r,m=mode,o=ordered:decision(r,m,o)
    def state(r, m=mode):
        s = unicodedata.normalize('NFC', r['state']) if m in ('nfc','nfc_outerstrip') else r['state']
        return s.strip() if m in ('outerstrip','nfc_outerstrip') else s
    funcs['state_' + mode] = state
for label in ('new-v2-train', 'all-v2-train'):
    train = [r for r,_,st in classified if r['split']=='train' and (label=='all-v2-train' or st=='new-v2')]
    for name, records in prior.items():
        hits = {}
        for key, f in funcs.items():
            refkeys = {f(r) for r,_ in records}
            hits[key] = [r['id'] for r in train if f(r) in refkeys]
            check(not hits[key], 'overlap: ' + label + '/' + name + '/' + key)
        checks.append({'train':label, 'reference':name, 'train_rows':len(train), 'reference_rows':len(records), 'hits':hits})

# Bind every row to released source metadata AND its assignment group. Filename
# proximity only selects candidates; full metadata output hashes bind the rows.
sources = []
row_bindings = {}
lineage = []
for source in prov['sources'] + load(v1provp)['sources']:
    mp = ART / source['metadata_path']
    meta = load(mp)
    for path, expected in source['artifact_sha256'].items():
        hash_check(ART/path, expected, 'published-source-artifact')
    check(source['metadata_path'] in source['artifact_sha256'], 'metadata not hash-linked')
    ap = mp.with_name('group_assignments.json')
    check(str(ap.relative_to(ART)) in source['artifact_sha256'], 'assignments not hash-linked')
    a = load(ap)
    groups = a.get('groups', a)
    records = [(r,p,st) for r,p,st in classified if (ART/p).parent == mp.parent]
    check(bool(records), 'source with no released rows: ' + str(mp))
    settings = meta['generation_settings']
    output_hashes = {}
    def gather_hashes(x):
        if isinstance(x, dict):
            for k,v in x.items():
                if k in ('train.jsonl','validation.jsonl') and isinstance(v,str) and len(v)==64:
                    output_hashes.setdefault(k, set()).add(v)
                elif 'parent' not in k:
                    gather_hashes(v)
    gather_hashes(settings)
    teacher = meta.get('teacher', {})
    si = {'metadata_path':source['metadata_path'], 'metadata_sha256':digest(mp.read_bytes()),
          'assignment_path':str(ap.relative_to(ART)), 'assignment_sha256':digest(ap.read_bytes()),
          'producer':meta['shard_id'], 'task_family':source['task_family'],
          'published_teacher_alias':source['teacher_alias'], 'teacher':teacher,
          'generation_settings':settings, 'label_basis':source['label_basis'],
          'revision_author':meta.get('revision_author'), 'rows':len(records)}
    # Inherited sources sometimes lack explicit output hashes; their exact shards
    # are already pinned by the parent manifest. New rows must have both bindings.
    for r,p,st in records:
        if st=='new-v2':
            check(digest((ART/p).read_bytes()) in output_hashes.get(Path(p).name,set()), 'metadata output hash missing: '+p)
        g = groups.get(r['group_id'])
        check(isinstance(g,dict), 'missing assignment: '+r['id'])
        if not isinstance(g,dict):
            g = {}
        check(g.get('split')==r['split'], 'assignment split: '+r['id'])
        check(source['task_family']==r['task_family'], 'source family: '+r['id'])
        check(source['label_basis']==r['provenance']['label_basis'], 'label basis: '+r['id'])
        raw_teacher = r['provenance'].get('teacher_model')
        if raw_teacher:
            check(raw_teacher.split('/')[-1]==teacher.get('model_alias'), 'teacher resolution: '+r['id'])
        binding = {**si, 'id':r['id'], 'group_id':r['group_id'], 'stratum':st,
                   'source_shard':p, 'assignment':g, 'provenance':r['provenance'],
                   'domain':g.get('domain'), 'mechanism':g.get('mechanism'),
                   'policy_instance':r['provenance'].get('scenario_id'),
                   'absent_units':[k for k,v in [('domain',g.get('domain')),('mechanism',g.get('mechanism')),('policy_instance',r['provenance'].get('scenario_id'))] if v is None]}
        check(r['id'] not in row_bindings, 'ambiguous source binding: '+r['id'])
        row_bindings[r['id']] = binding
    sources.append(si)
    if meta.get('parent'):
        parent = meta['parent']
        parentdir = safe(Path(parent['path']))
        for path, expected in parent['sha256'].items():
            hash_check(parentdir/path, expected, 'revision-parent')
    elif settings.get('parent_metadata'):
        parentdir = safe((mp.parent/settings['parent_metadata']).parent)
        for path, expected in settings['parent_hashes'].items():
            hash_check(parentdir/path, expected, 'revision-parent')
    else:
        continue
    if not any(st=='new-v2' for _,_,st in records):
        continue
    parents = {}
    for split in ('train','validation'):
        for line in safe(parentdir/(split+'.jsonl')).read_bytes().splitlines():
            if line.strip():
                pr=json.loads(line); parents[pr['id']]=pr
    mappings = {}
    mapping_name = settings.get('source_mapping')
    if not mapping_name and 'source_mappings.json' in settings.get('source_and_script_sha256',{}):
        mapping_name='source_mappings.json'
    if mapping_name:
        mappings={x['id']:x for x in load(mp.with_name(mapping_name))['rows']}
    for r,p,st in records:
        pr = parents.get(r['provenance'].get('parent_id'))
        check(pr is not None, 'missing parent ID: '+r['id'])
        if pr is None:
            continue
        fields = ['question','group_id','split','task_family','target_id']
        if r['task_family']=='intent':
            fields.append('state')
            mm=mappings.get(r['id'],{})
            check(all(mm.get(k)==r[k] for k in ('id','group_id','split','target_id')), 'choice mapping fields: '+r['id'])
            check(mm.get('parent_id')==pr['id'], 'choice mapping parent: '+r['id'])
            check([{'id':o['id'],'text':o['text']} for o in mm.get('options',[])]==r['options'], 'choice mapping options: '+r['id'])
            check([o['parent_text'] for o in mm.get('options',[])]==[o['text'] for o in pr['options']], 'choice mapping prior text: '+r['id'])
        else:
            fields.append('options')
            revision=load(mp.with_name('revision.json'))
            expected_state=revision['new_state'] if pr['id']==revision['parent_id'] else pr['state']
            check(r['state']==expected_state, 'sentiment revision state: '+r['id'])
        check(all(r[k]==pr[k] for k in fields), 'revision invariant: '+r['id'])
        check([o['id'] for o in r['options']]==[o['id'] for o in pr['options']], 'revision option ID order: '+r['id'])
        lineage.append({'id':r['id'],'parent_id':pr['id'],'parent_row_sha256':digest(canonical(pr).encode()),
                        'released_row_sha256':digest(canonical(r).encode()),'source':r['provenance']['source']})

check(len(row_bindings)==1800, 'incomplete source binding')
validation = {r['id']:row_bindings[r['id']] for r,_,_ in classified if r['split']=='validation'}
summary=[]
for st in ('inherited-v1','new-v2'):
    for family in ('intent','sentiment','rule_application'):
        for split in ('train','validation'):
            rows=[r for r,_,s in classified if s==st and r['task_family']==family and r['split']==split]
            summary.append({'stratum':st,'family':family,'split':split,'rows':len(rows),
                            'groups':len({r['group_id'] for r in rows}),
                            'provenance':dict(collections.Counter(canonical(r['provenance'] | {'source':None,'parent_id':None,'scenario_id':None}) for r in rows))})
coverage=[]
for s in sources:
    rows=[b for b in row_bindings.values() if b['metadata_path']==s['metadata_path']]
    for unit in ('domain','mechanism','policy_instance'):
        tr={b[unit] for b in rows if b['assignment'].get('split')=='train' and b[unit] is not None}
        va={b[unit] for b in rows if b['assignment'].get('split')=='validation' and b[unit] is not None}
        coverage.append({'producer':s['producer'],'unit':unit,'train_units':sorted(tr),'validation_units':sorted(va),
                         'shared_units':sorted(tr & va),'validation_units_absent_from_same_producer_train':sorted(va-tr),
                         'absent_validation_rows':sum(b[unit] is None for b in rows if b['assignment'].get('split')=='validation')})
result={'released_manifest_sha256':digest(v2p.read_bytes()),'released_provenance_sha256':digest(provp.read_bytes()),
        'algorithm_parent_path':'artifacts/evaluation/e3-identity-review-v1/review.py',
        'algorithm_parent_sha256':digest((ART/'evaluation/e3-identity-review-v1/review.py').read_bytes()),
        'script_sha256':digest(Path(__file__).read_bytes()),'parent_shards_retained_exactly':retained,
        'rows':len(current),'unique_ids':len(row_bindings),'summary':summary,'overlap_checks':checks,
        'sources':sources,'coverage':coverage,'revision_lineage':lineage,'receipts':receipts,'errors':errors,
        'limitations':['Exact identity checks are not semantic clearance, derivative exclusion, or producer access-history verification.',
                       'Named unseen mechanisms are assignment units, not proof of semantically unrelated algorithms.',
                       'Groups, policy instances, domains and producers are heterogeneous and method/teacher dependent; not iid observations.',
                       'No semantic correctness, tokenizer audit, ML, tests, lint, spending or protected final-data reads.']}
for name, content in [('evidence.json',result),('validation-source-units.json',{'manifest_sha256':EXPECTED,'provenance_sha256':result['released_provenance_sha256'],'by_validation_id':validation})]:
    with (OUT/name).open('x') as f:
        json.dump(content,f,indent=2,ensure_ascii=False); f.write('\n')
with (OUT/'row-identities.jsonl').open('x') as f:
    for r,p,st in classified:
        f.write(canonical({'id':r['id'],'group_id':r['group_id'],'split':r['split'],'stratum':st,
                           'row_sha256':digest(canonical(r).encode()),'provenance':r['provenance']})+'\n')
print(json.dumps({'rows':len(current),'validation_ids_mapped':len(validation),'revision_rows_joined':len(lineage),
                  'hash_receipts':len(receipts),'errors':errors,'summary':summary},indent=2))
