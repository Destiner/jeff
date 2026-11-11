#!/usr/bin/env python3
"""CPU-only lineage, exact-duplicate and choice-length audit; never writes row files."""
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'intent-a'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return [json.loads(x) for x in p.read_text().splitlines()]


def canon(s):
    return ' '.join(s.casefold().split())


def words(s):
    return len(re.findall(r"\b\w+(?:['’\-]\w+)*\b", s.lower()))


def lengths(rows):
    out = {}
    for metric, measure in [('chars', len), ('words', words)]:
        max_first = min_first = any_max = any_min = unique_max = unique_min = max_ties = min_ties = 0
        ranks = collections.Counter()
        by_arity = {}
        ledger = []
        for r in rows:
            values = [measure(o['text']) for o in r['options']]
            target = [o['id'] for o in r['options']].index(r['target_id'])
            t, n = values[target], len(values)
            hi, lo = max(values), min(values)
            mx, mn = values.index(hi) == target, values.index(lo) == target
            max_first += mx; min_first += mn
            any_max += t == hi; any_min += t == lo
            unique_max += t == hi and values.count(hi) == 1
            unique_min += t == lo and values.count(lo) == 1
            max_ties += values.count(hi) > 1; min_ties += values.count(lo) > 1
            rank_min = 1 + sum(v > t for v in values)
            rank_max = sum(v >= t for v in values)
            rank = f'{rank_min}-{rank_max}'
            ranks[rank] += 1
            a = by_arity.setdefault(str(n), {'rows': 0, 'first_max_matches': 0, 'first_min_matches': 0, 'target_descending_rank_interval_counts': collections.Counter()})
            a['rows'] += 1; a['first_max_matches'] += mx; a['first_min_matches'] += mn
            a['target_descending_rank_interval_counts'][rank] += 1
            ledger.append({'id': r['id'], 'arity': n, 'option_lengths': values, 'target_slot_1_based': target + 1,
                           'target_descending_rank_interval': [rank_min, rank_max]})
        out[metric] = {'rows': len(rows), 'first_max_matches': max_first, 'first_min_matches': min_first,
                       'first_max_rate': max_first / len(rows), 'first_min_rate': min_first / len(rows),
                       'target_among_max': any_max, 'target_among_min': any_min,
                       'target_unique_max': unique_max, 'target_unique_min': unique_min,
                       'max_tie_rows': max_ties, 'min_tie_rows': min_ties,
                       'target_descending_rank_interval_counts': ranks, 'by_arity': by_arity, 'rows_detail': ledger}
    return out


def main():
    meta = json.loads((ROOT / 'metadata.json').read_text())
    frozen = {name: sha(ROOT / name) for name in ['train.jsonl', 'validation.jsonl']}
    assert all(sha(PARENT / n) == h for n, h in meta['parent']['sha256'].items())
    assert (PARENT / 'group_assignments.json').read_bytes() == (ROOT / 'group_assignments.json').read_bytes()
    for name, expected in meta['generation_settings']['artifact_sha256'].items():
        assert sha(ROOT / name) == expected, name
    mappings = json.loads((ROOT / 'choice_mappings.json').read_text())['rows']
    mapping = {m['parent_id']: m for m in mappings}
    assert len(mapping) == 240
    new_all, old_all = [], []
    audits, counts, positions, changed = {}, {}, {}, collections.Counter()
    for split, expected in [('train', 200), ('validation', 40)]:
        old, new = load(PARENT / (split + '.jsonl')), load(ROOT / (split + '.jsonl'))
        assert len(old) == len(new) == expected
        for a, b in zip(old, new):
            assert a.keys() == b.keys()
            assert all(a[k] == b[k] for k in a if k not in ('id', 'options', 'provenance'))
            assert b['id'] == a['id'].replace('data:pilot-v2:intent-a:', 'data:pilot-v2:intent-a-r2:', 1)
            assert [o['id'] for o in a['options']] == [o['id'] for o in b['options']]
            assert 3 <= len(b['options']) <= 6
            assert all(o['text'].strip() and o['text'] == o['text'].strip() for o in b['options'])
            assert len({o['id'] for o in b['options']}) == len(b['options'])
            assert len({canon(o['text']) for o in b['options']}) == len(b['options'])
            p = b['provenance']
            assert p['parent_id'] == a['id'] and p['kind'] == p['label_basis'] == 'teacher'
            assert p['teacher_model'] == meta['teacher']['provider'] + '/' + meta['teacher']['model_alias']
            assert p['source'] == 'jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#' + a['group_id'].rsplit(':', 1)[-1]
            m = mapping[a['id']]
            assert m['id'] == b['id'] and m['group_id'] == b['group_id'] and m['split'] == split
            assert m['target_id'] == b['target_id']
            assert m['options'] == [{'id': x['id'], 'parent_text': x['text'], 'text': y['text']} for x, y in zip(a['options'], b['options'])]
            assert [o['id'] for o in b['options']].count(b['target_id']) == 1
            pos = [o['id'] for o in b['options']].index(b['target_id']) + 1
            assert pos == m['target_slot_1_based']
            key = f'{split}/{len(b["options"])}'
            positions.setdefault(key, collections.Counter())[str(pos)] += 1
            for x, y in zip(a['options'], b['options']):
                changed['options_changed'] += x['text'] != y['text']
                if y['id'] == b['target_id']:
                    changed['target_texts_changed'] += x['text'] != y['text']
            assert any(x['text'] != y['text'] for x, y in zip(a['options'], b['options']))
        counts[split] = {'rows': len(new), 'groups': len({r['group_id'] for r in new}),
                         'arity_counts': collections.Counter(str(len(r['options'])) for r in new),
                         'arity_chance': sum(1 / len(r['options']) for r in new) / len(new)}
        audits[split] = {'original': lengths(old), 'revision': lengths(new)}
        old_all.extend(old); new_all.extend(new)
    assert len({r['id'] for r in new_all}) == 240
    assert not {r['id'] for r in new_all} & {r['id'] for r in old_all}
    train_groups = {r['group_id'] for r in new_all if r['split'] == 'train'}
    val_groups = {r['group_id'] for r in new_all if r['split'] == 'validation'}
    assert not train_groups & val_groups
    duplicate_counts = {}
    for name, key in [
        ('raw_state', lambda r: r['state']),
        ('canonical_state', lambda r: canon(r['state'])),
        ('canonical_input_unordered_options', lambda r: (canon(r['state']), canon(r['question']), tuple(sorted(canon(o['text']) for o in r['options'])))),
        ('raw_input_ordered_options', lambda r: (r['state'], r['question'], tuple(o['text'] for o in r['options']))),
    ]:
        counter = collections.Counter(key(r) for r in new_all)
        duplicate_counts[name] = sum(v - 1 for v in counter.values())
        assert duplicate_counts[name] == 0
    assignments = json.loads((ROOT / 'group_assignments.json').read_text())['groups']
    assert set(assignments) == {r['group_id'] for r in new_all}
    assert all(assignments[r['group_id']]['split'] == r['split'] for r in new_all)
    assert frozen == {name: sha(ROOT / name) for name in frozen}
    report = {
        'schema_version': '0.1', 'shard_id': meta['shard_id'], 'status': 'passed_cpu_lineage_and_structural_validation',
        'checks': {'all_240_lineages_checked': True, 'all_states_questions_splits_groups_arities_preserved': True,
                   'ordered_option_ids_target_ids_and_slots_preserved': True, 'group_assignments_byte_identical': True,
                   'parent_protected_hashes_unchanged': True, 'new_ids_unique_and_disjoint_from_parent': True,
                   'mapping_matches_every_exported_option': True, 'teacher_provenance_and_parent_ids_valid': True,
                   'cross_split_group_overlap': 0, 'all_choice_sets_reauthored': True},
        'exact_duplicate_counts': duplicate_counts, 'row_and_group_counts': counts,
        'target_positions_1_based_by_split_arity': positions, 'text_changes': changed,
        'length_definition': {'chars': 'Python len, Unicode codepoints', 'words': "Unicode word sequences, retaining internal apostrophes/curly apostrophes/hyphens; regex in validate.py",
                              'ties': 'first supplied option wins max/min; rank interval is 1-based descending, all tie positions retained',
                              'chance': 'Mean reciprocal arity; descriptive uniform-choice reference, not a significance test'},
        'length_audit': audits, 'frozen_output_sha256': frozen,
        'parent_sha256': meta['parent']['sha256'], 'metadata_sha256': sha(ROOT / 'metadata.json'),
        'semantic_review': {'basis': 'Direct teacher authoring after reading all 240 parent source requests; same-session self-review only.',
                            'independent_correctness': False, 'parent_semantic_label_inspection': 'pending'},
        'limitations': meta['limitations'] + ['No final/evaluation or other-producer data opened. No global deduplication or tokenization audit.',
                                            'Length diagnostics are descriptive; no relabeling, state edits or reshuffling to optimize them.'],
    }
    with (ROOT / 'validation_report.json').open('x') as f:
        f.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for s, audit in audits.items():
        print(s, 'chance', round(counts[s]['arity_chance'], 4))
        for revision, values in audit.items():
            print(revision, {metric: {k: v[k] for k in ('first_max_matches', 'first_min_matches', 'target_unique_max', 'target_unique_min')} for metric, v in values.items()})
    print('Text changes:', dict(changed))
    print('Frozen SHA256:', frozen)


if __name__ == '__main__':
    main()
