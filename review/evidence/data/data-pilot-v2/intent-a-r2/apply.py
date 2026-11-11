#!/usr/bin/env python3
"""Deterministically serialize directly authored choices; refuse to overwrite frozen outputs."""
import copy
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'intent-a'
PREFIX = 'data:pilot-v2:intent-a:'
NEW_PREFIX = 'data:pilot-v2:intent-a-r2:'
SOURCE = 'jeff/data-pilot-v2/intent-a-r2/choice_mappings.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, obj):
    with (ROOT / name).open('x') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def main():
    for name in ('train.jsonl', 'validation.jsonl', 'choice_mappings.json', 'metadata.json', 'group_assignments.json'):
        if (ROOT / name).exists():
            raise RuntimeError('Frozen output already exists: ' + name)
    protected = ['train.jsonl', 'validation.jsonl', 'metadata.json', 'source_cases.txt', 'group_assignments.json']
    parent_hashes = {name: sha(PARENT / name) for name in protected}
    authored = {}
    for line in (ROOT / 'choices.txt').read_text().splitlines():
        key, *choices = line.split('|')
        assert key not in authored and all(x.strip() == x and x for x in choices)
        authored[key] = choices
    source = {}
    for line in (PARENT / 'source_cases.txt').read_text().splitlines():
        if not line.strip():
            continue
        key, state, *choices = line.split('|')
        source[key] = (state, choices)
    assert set(authored) == set(source) and len(authored) == 240
    provider, model = os.environ['PI_PROVIDER'], os.environ['PI_MODEL']
    mappings = []
    for split in ('train', 'validation'):
        result = []
        for line in (PARENT / (split + '.jsonl')).read_text().splitlines():
            old = json.loads(line)
            key = old['group_id'].rsplit(':', 1)[-1]
            state, original_choices = source[key]
            new_choices = authored[key]
            assert state == old['state'] and len(new_choices) == len(old['options']) == len(original_choices)
            by_text = {o['text']: o['id'] for o in old['options']}
            assert set(by_text) == set(original_choices)
            assert by_text[original_choices[0]] == old['target_id']
            replacements = {by_text[a]: b for a, b in zip(original_choices, new_choices)}
            assert old['id'].startswith(PREFIX)
            new = copy.deepcopy(old)
            new['id'] = NEW_PREFIX + old['id'][len(PREFIX):]
            for option in new['options']:
                option['text'] = replacements[option['id']]
            new['provenance'] = {
                'kind': 'teacher', 'source': SOURCE + '#' + key,
                'label_basis': 'teacher', 'teacher_model': provider + '/' + model,
                'parent_id': old['id'],
            }
            mappings.append({
                'parent_id': old['id'], 'id': new['id'], 'group_id': old['group_id'],
                'split': split, 'target_id': old['target_id'],
                'target_slot_1_based': [o['id'] for o in old['options']].index(old['target_id']) + 1,
                'options': [{'id': a['id'], 'parent_text': a['text'], 'text': b['text']}
                            for a, b in zip(old['options'], new['options'])],
            })
            result.append(new)
        with (ROOT / (split + '.jsonl')).open('x') as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + '\n' for r in result)
    save('choice_mappings.json', {
        'schema_version': '0.1', 'revision': 'intent-a-r2',
        'authoring_format': 'choices.txt: group|target|rivals; rival slots follow parent source-case order, not exported order',
        'rows': mappings,
    })
    with (ROOT / 'group_assignments.json').open('xb') as f:
        f.write((PARENT / 'group_assignments.json').read_bytes())
    metadata = {
        'schema_version': '0.1', 'shard_id': 'data-pilot-v2-intent-a-r2',
        'teacher': {'provider': provider, 'model_alias': model, 'immutable_revision': None},
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
        'parent': {'path': str(PARENT), 'metadata_path': str(PARENT / 'metadata.json'), 'sha256': parent_hashes},
        'revision_purpose': 'Replace length-revealing and remote choices with concise, workflow-adjacent contrasts without changing requested actions.',
        'semantic_scope': 'All 240 choice sets reauthored directly. Original states, questions, split, group_id, task_family, arity, ordered option IDs, target ID and target slot are unchanged. Targets express the same requested action, retaining consequential timing, conditions and partial-action scope; no new facts are asserted about the scenario. Only choice texts, example ID prefix and provenance change.',
        'generation_settings': {
            'method': 'Direct approved-agent teacher authoring of each complete choice set; stdlib CPU mapping and serialization only.',
            'sampling': {'temperature': None, 'top_p': None, 'note': 'Harness sampling settings unavailable; no additional model/API calls.'},
            'option_order': 'Parent order unchanged; no diagnostic-driven reshuffling or relabeling.',
            'source_mapping': 'choice_mappings.json', 'authored_source': 'choices.txt',
            'generation_scripts': ['apply.py', 'validate.py'],
            'artifact_sha256': {name: sha(ROOT / name) for name in [
                'choices.txt', 'choice_mappings.json', 'apply.py', 'validate.py',
                'train.jsonl', 'validation.jsonl', 'group_assignments.json']},
        },
        'usage_constraints': {
            'origin': 'Synthetic parent scenarios and direct revision through existing approved agent access; applicable provider terms remain in force.',
            'privacy': 'No private company or customer records used.',
            'features': 'Only state, question and option text are model inputs; all lineage and labels are metadata.',
            'validation': 'Validation rows are for validation only, never weight updates.',
            'replacement': 'Use this revision instead of the parent, not alongside its same-group rows.',
        },
        'row_counts': {'train': 200, 'validation': 40},
        'group_counts': {'train': 200, 'validation': 40},
        'limitations': ['Same-teacher semantic self-review, not independent correctness verification.',
                        'No immutable teacher revision or sampling parameters exposed.',
                        'No model/tokenizer load; downstream token-budget audit remains necessary.',
                        'Deduplication scope is this shard and its parent lineage only.'],
    }
    assert parent_hashes == {name: sha(PARENT / name) for name in protected}
    save('metadata.json', metadata)
    print('Frozen 200 train + 40 validation rows; parent hashes unchanged.')


if __name__ == '__main__':
    main()
