"""Lightweight local dataset validation, not a software test suite or semantic audit."""
import collections
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent
plan = json.loads((root / 'group_assignments.json').read_text())['groups']
config = json.loads(Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/pilot-v1.json').read_text())
reservation = next(item for item in config['assignments'] if item['task_family'] == 'sentiment')
errors = []
rows = []
files = {}
positions = {}
required = {'schema_version', 'id', 'state', 'question', 'options', 'target_id', 'group_id', 'task_family', 'split', 'provenance'}
for split, expected_count in [('train', 100), ('validation', 20)]:
    path = root / f'{split}.jsonl'
    content = path.read_bytes()
    selected = [json.loads(line) for line in content.decode().splitlines()]
    files[path.name] = {'rows': len(selected), 'sha256': hashlib.sha256(content).hexdigest()}
    if len(selected) != expected_count:
        errors.append(f'{split}: unexpected row count')
    positions[split] = collections.defaultdict(collections.Counter)
    for row in selected:
        rid = row.get('id', '<missing>')
        def check(condition, message):
            if not condition:
                errors.append(f'{rid}: {message}')
        check(set(row) == required, 'row fields')
        check(row['schema_version'] == '0.1', 'schema version')
        check(isinstance(row['state'], str) and bool(row['state'].strip()), 'state string')
        check(isinstance(row['question'], str) and bool(row['question'].strip()), 'question')
        check(isinstance(rid, str) and rid.startswith('data:pilot-v1:sentiment:'), 'namespaced ID')
        check(row['task_family'] == 'sentiment', 'family')
        check(row['split'] == split, 'split purity')
        group = row['group_id']
        check(group in plan and plan[group]['split'] == split, 'frozen group allocation')
        suffix = group.rsplit(':', 1)[-1]
        check(suffix in reservation[f'{split}_groups'], 'reservation membership')
        opts = row['options']
        check(isinstance(opts, list) and 2 <= len(opts) <= 6, 'option count')
        check(all(set(opt) == {'id', 'text'} and isinstance(opt['id'], str) and opt['id'].strip() and isinstance(opt['text'], str) and opt['text'].strip() for opt in opts), 'option structure')
        ids = [opt['id'] for opt in opts]
        check(len(ids) == len(set(ids)), 'unique option IDs')
        check(len({opt['text'] for opt in opts}) == len(opts), 'unique option texts')
        check(ids.count(row['target_id']) == 1, 'single valid target')
        if row['target_id'] in ids:
            positions[split][len(opts)][ids.index(row['target_id']) + 1] += 1
        provenance = row['provenance']
        check(provenance.get('kind') == 'teacher' and provenance.get('label_basis') == 'teacher', 'honest teacher label basis')
        check(provenance.get('source') == 'jeff-data-pilot-v1-sentiment-agent-r1', 'generation-job source')
        check(bool(provenance.get('teacher_model')), 'teacher identity')
    rows.extend(selected)
if len({row['id'] for row in rows}) != len(rows):
    errors.append('duplicate row IDs')
groups = collections.defaultdict(list)
for row in rows:
    groups[row['group_id']].append(row)
if set(groups) != set(plan):
    errors.append('missing or extra groups')
for group, group_rows in groups.items():
    if len(group_rows) != 4 or len({row['split'] for row in group_rows}) != 1:
        errors.append(f'{group}: group size or isolation')
normalize = lambda text: ' '.join(re.findall(r"[a-z0-9]+", text.lower()))
normalized_states = [normalize(row['state']) for row in rows]
exact_duplicates = [text for text, count in collections.Counter(normalized_states).items() if count > 1]
if exact_duplicates:
    errors.append('normalized exact state duplicates')
near = []
for i, row in enumerate(rows):
    left = set(normalized_states[i].split())
    for j in range(i):
        right = set(normalized_states[j].split())
        similarity = len(left & right) / len(left | right)
        if similarity >= 0.60:
            near.append({'left': rows[j]['id'], 'right': row['id'], 'token_set_jaccard': round(similarity, 4)})
report = {
    'scope': 'Only this sentiment shard plus its preassigned config; no other shards or final/evaluation content inspected',
    'status': 'pass' if not errors else 'fail',
    'errors': errors,
    'checks': ['JSONL parsing', 'contract fields and types', 'row counts', 'local namespaced ID uniqueness', '2-6 unique informative nonempty options', 'one supplied target per row', 'split-pure files', '30 reserved groups with four rows each', 'group isolation and frozen allocation', 'teacher provenance fields', 'normalized exact state duplicate scan', 'pairwise token-set Jaccard state similarity at 0.60 threshold', 'target-position distributions', 'SHA-256 of completed shards'],
    'files': files,
    'rows': len(rows), 'groups': len(groups),
    'target_positions_by_split_and_option_count': {split: {str(count): dict(hist) for count, hist in values.items()} for split, values in positions.items()},
    'normalized_exact_state_duplicates': len(exact_duplicates),
    'near_duplicate_candidates': near,
    'semantic_status': 'No independent semantic validation; target sentiment is teacher-authored. Duplicate heuristic is lexical, not semantic.',
    'global_uniqueness_limit': 'Uniqueness checked within this shard only; parent must check combined shards.',
}
(root / 'validation_report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if errors:
    raise SystemExit(1)
