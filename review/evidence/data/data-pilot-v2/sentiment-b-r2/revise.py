"""Immutable single-wording correction from the separate sentiment review."""
import hashlib
import json
from pathlib import Path
import shutil

output = Path(__file__).resolve().parent
source = output.parent / 'sentiment-b'
old = 'Quill Parcel sandwiched my tracing sheets between rigid boards. Not a crease survived the journey, so I could use every sheet for the drawing.'
new = 'Quill Parcel sandwiched my tracing sheets between rigid boards. Every sheet arrived uncreased, so I could use them all for the drawing.'
changed = []
parent_hashes = {}
for split in ('train', 'validation'):
    path = source / (split + '.jsonl')
    parent_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    for row in rows:
        parent_id = row['id']
        if parent_id == 'data:pilot-v2:sentiment-b:g011:r01':
            if row['state'] != old:
                raise ValueError('Source state differs from reviewed wording')
            row['state'] = new
            changed.append(parent_id)
        row['id'] = parent_id.replace('data:pilot-v2:sentiment-b:', 'data:pilot-v2:sentiment-b-r2:')
        row['provenance']['parent_id'] = parent_id
        row['provenance']['source'] = 'data-pilot-v2-sentiment-b-r2/from/' + row['provenance']['source']
    with (output / (split + '.jsonl')).open('x') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
if changed != ['data:pilot-v2:sentiment-b:g011:r01']:
    raise ValueError('Expected one reviewed correction')
shutil.copyfile(source / 'group_assignments.json', output / 'group_assignments.json')
parent_metadata = json.loads((source / 'metadata.json').read_text())
metadata = {
    'schema_version': '0.1', 'shard_id': 'data-pilot-v2-sentiment-b-r2',
    'teacher': parent_metadata['teacher'],
    'revision_author': 'openai/gpt-astra (exposed alias, immutable revision unknown)',
    'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
    'generation_settings': {'method': 'One reviewed negation/verb wording correction, no new labels',
        'revision': 'r2', 'sampling': None, 'parent_hashes': parent_hashes,
        'parent_metadata': '../sentiment-b/metadata.json', 'script': 'revise.py',
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'option_order': 'Unchanged seeded parent order', 'changed_parent_ids': changed},
    'usage_constraints': parent_metadata['usage_constraints'],
    'row_counts': {'train': 200, 'validation': 40},
    'group_counts': {'train': 200, 'validation': 40},
    'limitations': ['Teacher judgments retained, not independently verified correctness',
        'All other 239 states and every question, option, target, group and split unchanged']}
with (output / 'metadata.json').open('x') as stream:
    json.dump(metadata, stream, indent=2)
    stream.write('\n')
with (output / 'revision.json').open('x') as stream:
    json.dump({'parent_id': changed[0], 'old_state': old, 'new_state': new,
               'reason': 'Describe uncreased arrival, not unexplained removal of existing creases',
               'target': 'Unchanged positive-only teacher judgment'}, stream, indent=2)
    stream.write('\n')
print('Published 240 lineage-preserved rows; one wording correction, no label changes.')
