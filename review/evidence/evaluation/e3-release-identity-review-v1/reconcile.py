"""Resolve absent redundant output hashes by full released-byte reconstruction.
Never executes producer code or changes any previous evidence.
"""
import copy
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ART = OUT.parent.parent

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load(p):
    return json.loads(p.read_bytes())

e = load(OUT/'evidence.json')
mapping = load(OUT/'validation-source-units.json')
base = ART/'data/data-pilot-v2/sentiment-b-r2'
meta = load(base/'metadata.json')
rev = load(base/'revision.json')
reconstruction = []
errors = []
for split in ('train','validation'):
    parent_bytes = (base.parent/'sentiment-b'/(split+'.jsonl')).read_bytes()
    if sha(parent_bytes) != meta['generation_settings']['parent_hashes'][split+'.jsonl']:
        errors.append('sentiment parent hash mismatch')
    rows = [json.loads(line) for line in parent_bytes.splitlines() if line.strip()]
    for row in rows:
        parent_id = row['id']
        if parent_id == rev['parent_id']:
            if row['state'] != rev['old_state']:
                errors.append('revision old state mismatch')
            row['state'] = rev['new_state']
        row['id'] = parent_id.replace('data:pilot-v2:sentiment-b:', 'data:pilot-v2:sentiment-b-r2:')
        row['provenance']['parent_id'] = parent_id
        row['provenance']['source'] = 'data-pilot-v2-sentiment-b-r2/from/' + row['provenance']['source']
    reconstructed = ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows).encode()
    released = (base/(split+'.jsonl')).read_bytes()
    ok = reconstructed == released
    if not ok:
        errors.append('full sentiment revision reconstruction mismatch: '+split)
    reconstruction.append({'split':split,'rows':len(rows),'released_sha256':sha(released),
                           'reconstructed_sha256':sha(reconstructed),'byte_identical':ok})
resolved = [x for x in e['errors'] if x.startswith('metadata output hash missing: data/data-pilot-v2/sentiment-b-r2/')]
unresolved = [x for x in e['errors'] if x not in resolved] + errors
if len(resolved) != 240:
    unresolved.append('unexpected initial diagnostic count')
for b in mapping['by_validation_id'].values():
    b['source_binding_basis'] = ('pinned released manifest + hashed metadata/assignments + byte-identical full parent revision reconstruction'
        if b['producer']=='data-pilot-v2-sentiment-b-r2' else
        'pinned released manifest + hashed metadata/assignments + exact inherited parent shard'
        if b['stratum']=='inherited-v1' else
        'pinned released manifest + hashed metadata/assignments + metadata output hash')
    b['unit_basis'] = {'producer':'published metadata shard_id', 'domain':'assignment.domain, null if absent',
                       'mechanism':'assignment.mechanism, null if absent',
                       'policy_instance':'released row provenance.scenario_id, null if absent; not inferred from a filename'}
    b['source_label_basis_exact'] = b['provenance']['label_basis']
    b['row_teacher_model_exact'] = b['provenance'].get('teacher_model')
    b['teacher_resolution'] = {'provider':b['teacher'].get('provider'), 'alias':b['teacher'].get('model_alias'),
                               'immutable_revision':b['teacher'].get('immutable_revision'),
                               'qualification':'published source/author identity; not an independent label verifier'}
    b['published_method'] = b['generation_settings'].get('method')
final = {'initial_evidence_sha256':sha((OUT/'evidence.json').read_bytes()),
         'reconciliation_script_sha256':sha(Path(__file__).read_bytes()),
         'manifest_sha256':e['released_manifest_sha256'],'provenance_sha256':e['released_provenance_sha256'],
         'initial_diagnostics':len(e['errors']),'resolved_redundant_output_hash_diagnostics':len(resolved),
         'reconstruction':reconstruction,'unresolved_errors':unresolved,
         'qualifications':['sentiment-b-r2 metadata has parent hashes, not redundant output hashes; complete frozen output bytes reproduced without executing producer code.',
                           'Initial diagnostics and artifacts preserved, not silently erased.',
                           'No semantic clearance or independent teacher revision/correctness verification.']}
mapping['review_reconciliation'] = final
for name,obj in [('reconciled-evidence.json',final),('validation-source-units-reviewed.json',mapping)]:
    with (OUT/name).open('x') as f:
        json.dump(obj,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps(final,indent=2))
