"""Deterministic CPU-only application and lineage audit; never overwrite frozen files.
Run: python3 apply_revision.py
After publication: python3 apply_revision.py --verify
No model, tokenizer, external package, network, or test runner is used.
"""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'intent-b'
OLD = 'data:pilot-v2:intent-b:'
NEW = 'data:pilot-v2:intent-b-r2:'
SHARD = 'data-pilot-v2-intent-b-r2'
VERIFY = sys.argv[1:] == ['--verify']
assert not sys.argv[1:] or VERIFY


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def publish(name, data):
    path = ROOT / name
    if VERIFY:
        assert path.read_bytes() == data, f'Frozen bytes differ: {name}'
    else:
        with path.open('xb') as handle:
            handle.write(data)


def save(name, value):
    publish(name, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode())


def words(text):
    return re.findall(r"\w+(?:['’\-]\w+)*", text.lower())


def diagnostics(rows):
    result = {}
    for split in ('train', 'validation'):
        subset = [r for r in rows if r['split'] == split]
        buckets = {'all': subset}
        buckets.update({str(n): [r for r in subset if len(r['options']) == n]
                        for n in sorted({len(r['options']) for r in subset})})
        result[split] = {}
        for arity, bucket in buckets.items():
            entry = {'rows': len(bucket), 'arity_chance': sum(1 / len(r['options']) for r in bucket) / len(bucket)}
            entry['target_slots_zero_based'] = dict(sorted(collections.Counter(
                next(i for i, o in enumerate(r['options']) if o['id'] == r['target_id']) for r in bucket).items()))
            entry['lengths'] = {}
            for unit, measure in [('characters', len), ('words', lambda t: len(words(t)))]:
                counts = collections.Counter()
                ranks = collections.Counter()
                ascending = collections.Counter()
                by_arity_rank = collections.Counter()
                target_sizes, rival_sizes = [], []
                for row in bucket:
                    lengths = [measure(o['text']) for o in row['options']]
                    slot = next(i for i, o in enumerate(row['options']) if o['id'] == row['target_id'])
                    value = lengths[slot]
                    counts['first_max_target'] += slot == lengths.index(max(lengths))
                    counts['first_min_target'] += slot == lengths.index(min(lengths))
                    counts['unique_max_target'] += value == max(lengths) and lengths.count(value) == 1
                    counts['unique_min_target'] += value == min(lengths) and lengths.count(value) == 1
                    counts['among_max_target'] += value == max(lengths)
                    counts['among_min_target'] += value == min(lengths)
                    counts['max_tie_rows'] += lengths.count(max(lengths)) > 1
                    counts['min_tie_rows'] += lengths.count(min(lengths)) > 1
                    rank = 1 + sum(n > value for n in lengths)
                    ranks[str(rank)] += 1
                    ascending[str(1 + sum(n < value for n in lengths))] += 1
                    by_arity_rank[f'{len(lengths)}_options/rank_{rank}'] += 1
                    target_sizes.append(value)
                    rival_sizes.extend(n for i, n in enumerate(lengths) if i != slot)
                entry['lengths'][unit] = {
                    **dict(counts), 'target_rank_descending_competition': dict(sorted(ranks.items())),
                    'target_rank_ascending_competition': dict(sorted(ascending.items())),
                    'arity_and_descending_rank': dict(sorted(by_arity_rank.items())),
                    'mean_target': sum(target_sizes) / len(target_sizes),
                    'mean_rival': sum(rival_sizes) / len(rival_sizes),
                }
            result[split][arity] = entry
    return result


def main():
    parent_names = ['train.jsonl', 'validation.jsonl', 'metadata.json', 'group_assignments.json', 'source_cases.txt', 'generate.py']
    parent_hashes = {name: sha(PARENT / name) for name in parent_names}
    original = [json.loads(line) for split in ('train', 'validation')
                for line in (PARENT / f'{split}.jsonl').read_text().splitlines()]
    parent_metadata = json.loads((PARENT / 'metadata.json').read_text())
    choices = [line.split(' | ') for line in (ROOT / 'authored_choices.txt').read_text().splitlines()
               if line.strip() and not line.startswith('#')]
    refinements = json.loads((ROOT / 'target_refinements.json').read_text())
    for group, target in refinements.items():
        choices[int(group) - 1][0] = target
    assert len(choices) == len(original) == 240
    source_cases = [line.split(' | ') for line in (PARENT / 'source_cases.txt').read_text().splitlines()
                    if line.strip() and not line.startswith(('#', '@'))]
    assert len(source_cases) == 240
    teacher = {'provider': os.environ['PI_PROVIDER'], 'model_alias': os.environ['PI_MODEL'], 'immutable_revision': None}
    assert all(teacher[k] for k in ('provider', 'model_alias'))
    rows, mappings = [], []
    for index, (parent, texts, source) in enumerate(zip(original, choices, source_cases), 1):
        assert parent['group_id'] == OLD + f'g{index:03}'
        assert parent['state'] == source[0]
        assert {o['text'] for o in parent['options']} == set(source[1:])
        assert next(o['text'] for o in parent['options'] if o['id'] == parent['target_id']) == source[1]
        assert len(texts) == len(parent['options']) and all(t.strip() == t and t for t in texts)
        assert len(set(t.casefold() for t in texts)) == len(texts)
        row = json.loads(json.dumps(parent))
        row['id'] = NEW + parent['id'][len(OLD):]
        rivals = iter(texts[1:])
        for option in row['options']:
            option['text'] = texts[0] if option['id'] == row['target_id'] else next(rivals)
        row['provenance'] = {
            **parent['provenance'], 'kind': 'teacher', 'label_basis': 'teacher',
            'source': SHARD + '/source-mappings-r2', 'parent_id': parent['id'],
            'teacher_model': teacher['model_alias'], 'teacher_provider': teacher['provider'],
        }
        for field in ('state', 'question', 'split', 'group_id', 'task_family', 'schema_version', 'target_id'):
            assert row[field] == parent[field], field
        assert [o['id'] for o in row['options']] == [o['id'] for o in parent['options']]
        assert len(row['options']) == len(parent['options'])
        assert row['id'] != parent['id'] and row['id'].startswith(NEW)
        mappings.append({
            'parent_id': parent['id'], 'id': row['id'], 'group_id': row['group_id'], 'split': row['split'],
            'target_id': row['target_id'], 'parent_target_text': source[1],
            'options': [{'id': new['id'], 'parent_text': old['text'], 'text': new['text']}
                        for old, new in zip(parent['options'], row['options'])],
        })
        rows.append(row)
    assert len({r['id'] for r in rows}) == 240
    assert not ({r['id'] for r in rows} & {r['id'] for r in original})
    assert collections.Counter(r['split'] for r in rows) == {'train': 200, 'validation': 40}
    groups = {s: {r['group_id'] for r in rows if r['split'] == s} for s in ('train', 'validation')}
    assert not groups['train'] & groups['validation']
    exact_state_duplicates = len(rows) - len({r['state'] for r in rows})
    normalized_state_duplicates = len(rows) - len({' '.join(words(r['state'])) for r in rows})
    canonical = [encode([r['state'], r['question'], sorted(o['text'] for o in r['options'])]) for r in rows]
    canonical_duplicates = len(canonical) - len(set(canonical))
    ordered_duplicates = len(rows) - len({encode([r['state'], r['question'], r['options']]) for r in rows})
    assert exact_state_duplicates == normalized_state_duplicates == canonical_duplicates == ordered_duplicates == 0
    save('source_mappings.json', {'schema_version': '0.1', 'source_revision': 'intent-b-r2', 'rows': mappings})
    publish('group_assignments.json', (PARENT / 'group_assignments.json').read_bytes())
    for split in ('train', 'validation'):
        publish(f'{split}.jsonl', ''.join(encode(r) + '\n' for r in rows if r['split'] == split).encode())
    output_hashes = {n: sha(ROOT / n) for n in ('train.jsonl', 'validation.jsonl', 'group_assignments.json')}
    source_hashes = {n: sha(ROOT / n) for n in ('authored_choices.txt', 'target_refinements.json', 'source_mappings.json', 'apply_revision.py')}
    metadata = {
        'schema_version': '0.1', 'shard_id': SHARD, 'teacher': teacher,
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
        'generation_settings': {
            'method': 'Existing approved agent directly authored all 240 option sets and semantic target refinements; deterministic CPU application only.',
            'source_revision': 'intent-b-r2', 'sampling_parameters': None,
            'immutable_sampling_details': 'Unavailable from agent environment.',
            'option_order': 'Parent ordered option IDs and target slots retained exactly; authored rivals assigned in parent non-target slot order.',
            'source_and_script_sha256': source_hashes, 'output_sha256': output_hashes,
            'regenerate': 'In a fresh sibling output directory containing the three authored/script inputs, run python3 apply_revision.py; verify an existing freeze with --verify.',
            'parent_rows_read': 240,
        },
        'usage_constraints': parent_metadata['usage_constraints'],
        'row_counts': {'train': 200, 'validation': 40}, 'group_counts': parent_metadata['group_counts'],
        'parent': {'path': str(PARENT), 'metadata_path': str(PARENT / 'metadata.json'), 'sha256': parent_hashes},
        'revision_purpose': 'Replace weak and length-revealing choices with concise targets and plausible same-workflow alternatives.',
        'semantic_scope': 'Only option text, example namespace, and provenance revised. Every original teacher requested action is intended to remain unchanged. State, question, schema, family, split, group IDs, arities, ordered option IDs, target IDs and slots are byte/value-preserved. No real-world factual assertions added to state. Alternative options are hypothetical actions, not asserted events.',
        'limitations': [
            'Semantic preservation is author judgment, not independently verified correctness; parent must separately inspect all revised labels.',
            'Immutable teacher revision and sampling settings unavailable; alias records actual current environment.',
            'No tokenizer/model loaded; no token budget certification.',
            'Only this parent shard and read-only review-intent/review.md inspected; no historical or cross-producer global uniqueness certification.',
            'Length and state-word overlap may remain predictive; no shortcut-free claim. Explicit parent scope cues remain unchanged.',
        ],
    }
    save('metadata.json', metadata)
    report = {
        'schema_version': '0.1', 'shard_id': SHARD, 'status': 'cpu_lineage_and_structural_checks_passed',
        'row_counts': metadata['row_counts'], 'group_counts': metadata['group_counts'],
        'checks': {
            'parent_source_export_state_and_target_match': 240,
            'parent_states_questions_splits_groups_arities_ordered_option_ids_targets_slots_preserved': 240,
            'revised_ids_correctly_namespaced_and_unique_within_parent_plus_revision': 240,
            'teacher_label_basis_and_parent_id_recorded': 240,
            'exact_state_duplicates': exact_state_duplicates, 'normalized_state_duplicates': normalized_state_duplicates,
            'exact_ordered_input_duplicates': ordered_duplicates, 'exact_option_order_invariant_input_duplicates': canonical_duplicates,
            'within_row_duplicate_option_texts': 0, 'cross_split_group_overlap': 0,
            'group_assignments_byte_identical': sha(ROOT / 'group_assignments.json') == parent_hashes['group_assignments.json'],
            'all_option_sets_changed': all(a['options'] != b['options'] for a, b in zip(original, rows)),
            'parent_bytes_unchanged_at_end': all(sha(PARENT / name) == value for name, value in parent_hashes.items()),
        },
        'diagnostic_definitions': {
            'characters': 'Python len(text), Unicode codepoints.',
            'words': r"Lowercase Unicode regex \w+(?:['’\-]\w+)*; hyphenated/apostrophized words retained.",
            'first_extremum': 'First supplied option wins ties, matching parent review convention.',
            'rank': 'Competition rank: 1 + number of options strictly longer (descending) or shorter (ascending). Ties share ranks.',
            'chance': 'Mean reciprocal arity for the applicable subset. Not a fitted null or significance claim.',
        },
        'original': diagnostics(original), 'revision': diagnostics(rows),
        'output_sha256': output_hashes, 'metadata_sha256': sha(ROOT / 'metadata.json'),
        'source_and_script_sha256': source_hashes, 'parent_sha256': parent_hashes,
        'limitations': metadata['limitations'], 'additional_spend_gbp': 0, 'pending_spend_gbp': 0,
    }
    assert all(report['checks'][k] for k in ('group_assignments_byte_identical', 'all_option_sets_changed', 'parent_bytes_unchanged_at_end'))
    save('validation_report.json', report)
    print(json.dumps({'mode': 'verify' if VERIFY else 'freeze', 'row_counts': metadata['row_counts'], 'output_sha256': output_hashes,
                      'length_summary': {s: {v: {u: {k: report[v][s]['all']['lengths'][u][k] for k in ('first_max_target', 'first_min_target')}
                          for u in ('characters', 'words')} for v in ('original', 'revision')} for s in ('train', 'validation')}}, indent=2))


if __name__ == '__main__':
    main()
