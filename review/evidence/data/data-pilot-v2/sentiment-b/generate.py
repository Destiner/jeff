"""Deterministic, standard-library-only artifact assembly and structural validation.
Run with: python3 generate.py
Never reads parent examples, evaluation data, or network resources.
"""
import collections
import hashlib
import json
import os
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parent
REVISION = 'sentiment-b-generation-r1'
SOURCE_REVISION = 'sentiment-b-source-s1'
ASSIGNMENT_REVISION = 'sentiment-b-assignments-a1'
SHARD = 'data-pilot-v2-sentiment-b-r1'
SEED = 670129
CLASSES = ('P', 'N', 'U', 'M')
CLASS_NAMES = dict(zip(CLASSES, ('positive-only', 'negative-only', 'neutral/no evaluation', 'mixed praise and criticism')))
STYLES = [
    dict(zip(CLASSES, ('Praise for the named subject, with no criticism expressed.', 'Criticism of the named subject, with no praise expressed.', 'Facts about the named subject, with no judgment expressed.', 'Praise and criticism of the named subject are expressed.'))),
    dict(zip(CLASSES, ('The writer approves of the subject and voices no objections.', 'The writer objects to the subject and offers no praise.', 'The writer reports information without any judgment about the subject.', 'The writer appreciates certain aspects and also objects to others.'))),
    dict(zip(CLASSES, ('Only favourable judgments about the named subject are given.', 'Only unfavourable judgments about the named subject are given.', 'Factual information about the named subject, with judgment withheld.', 'Favourable and unfavourable judgments about the named subject appear.'))),
    dict(zip(CLASSES, ('An approving assessment without any complaints about the subject.', 'A critical assessment without any compliments about the subject.', 'A factual account without any judgments about the subject.', 'An assessment with compliments and complaints about the subject.'))),
    dict(zip(CLASSES, ('The subject is praised, not criticised.', 'The subject is criticised, not praised.', 'The subject is described, not evaluated.', 'The subject receives praise and criticism.'))),
]
QUESTIONS = (
    'How does the writer evaluate {subject}?',
    'What attitude does the writer express toward {subject}?',
    'Which description fits the account of {subject}?',
    'How is {subject} assessed in this account?',
    'What evaluation of {subject} appears here?',
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def canonical(text):
    return ' '.join(text.casefold().split())


def main():
    provider, model = os.environ.get('PI_PROVIDER'), os.environ.get('PI_MODEL')
    if not provider or not model:
        raise ValueError('Actual PI_PROVIDER and PI_MODEL are required; no guessed teacher identity')
    assignments = json.loads((ROOT / 'group_assignments.json').read_text())['groups']
    assert len(assignments) == 240
    cases = []
    subjects = []
    subject = None
    for line in (ROOT / 'source_cases.txt').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            subject = line[1:]
            subjects.append(subject)
            continue
        label, state = line.split('|', 1)
        assert label in CLASSES and subject and subject in state
        n = len(cases) + 1
        gid = f'data:pilot-v2:sentiment-b:g{n:03d}'
        a = assignments[gid]
        assert a['split'] == ('train' if n <= 200 else 'validation')
        assert state.strip() == state
        assert not re.search(r'\b(positive|negative|neutral|mixed)\b|both sides', state, re.I)
        cases.append({'group_id': gid, 'label': label, 'state': state, 'subject': subject, **a})
    assert len(cases) == 240 and len(subjects) == 24
    assert [len({c['domain'] for c in cases if c['split'] == s}) for s in ('train', 'validation')] == [20, 4]
    assert set(collections.Counter(c['domain'] for c in cases).values()) == {10}
    assert set(c['domain'] for c in cases[:200]).isdisjoint(c['domain'] for c in cases[200:])

    source_hash = digest(ROOT / 'source_cases.txt')
    assignment_hash = digest(ROOT / 'group_assignments.json')
    artifacts, diagnostics = {}, {}
    case_by_id = {}
    # Position, question, and style schedules are independently seeded within each label/split.
    for si, split in enumerate(('train', 'validation')):
        rows = []
        for ci, label in enumerate(CLASSES):
            selected = [c for c in cases if c['split'] == split and c['label'] == label]
            count = 50 if split == 'train' else 10
            assert len(selected) == count
            positions = [p for p in range(4) for _ in range(count // 4)] + [ci, (ci + 1) % 4]
            styles = [i % len(STYLES) for i in range(count)]
            questions = [i % len(QUESTIONS) for i in range(count)]
            random.Random(SEED + si * 100 + ci).shuffle(positions)
            random.Random(SEED + 1000 + si * 100 + ci).shuffle(styles)
            random.Random(SEED + 2000 + si * 100 + ci).shuffle(questions)
            for c, position, style, question in zip(selected, positions, styles, questions):
                rng = random.Random(f'{SEED}:{c["group_id"]}:options')
                other = [x for x in CLASSES if x != label]
                rng.shuffle(other)
                order = other[:position] + [label] + other[position:]
                # Opaque option IDs are freshly shuffled and carry no semantic category.
                opaque = rng.sample(range(10000, 99999), 4)
                options = [{'id': f'c{x}', 'text': STYLES[style][cl]} for x, cl in zip(opaque, order)]
                row = {
                    'schema_version': '0.1', 'id': c['group_id'] + ':r01',
                    'state': c['state'], 'question': QUESTIONS[question].format(subject=c['subject']),
                    'options': options, 'target_id': options[position]['id'],
                    'group_id': c['group_id'], 'task_family': 'sentiment', 'split': split,
                    'provenance': {
                        'kind': 'teacher',
                        'source': f'{SHARD}/{SOURCE_REVISION};source_sha256={source_hash};case={c["group_id"]}',
                        'label_basis': 'teacher', 'teacher_model': model,
                    },
                }
                case_by_id[row['id']] = {**c, 'position': position, 'style': style, 'question_form': question}
                rows.append(row)
        random.Random(SEED + 3000 + si).shuffle(rows)
        artifacts[split] = rows

    all_rows = artifacts['train'] + artifacts['validation']
    assert len({r['id'] for r in all_rows}) == 240
    assert len({r['group_id'] for r in all_rows}) == 240
    assert len({canonical(r['state']) for r in all_rows}) == 240
    assert len({(canonical(r['state']), canonical(r['question']), tuple(sorted(o['text'] for o in r['options']))) for r in all_rows}) == 240
    assert set(r['group_id'] for r in artifacts['train']).isdisjoint(r['group_id'] for r in artifacts['validation'])
    assert all(r['id'] == r['group_id'] + ':r01' for r in all_rows)
    for r in all_rows:
        assert r['schema_version'] == '0.1' and isinstance(r['state'], str) and r['state']
        assert r['task_family'] == 'sentiment' and r['question'].strip()
        assert r['split'] == assignments[r['group_id']]['split']
        assert len(r['options']) == 4
        assert len({o['id'] for o in r['options']}) == 4
        assert len({o['text'] for o in r['options']}) == 4
        assert all(isinstance(o['id'], str) and o['id'] and o['text'].strip() for o in r['options'])
        assert sum(o['id'] == r['target_id'] for o in r['options']) == 1
        assert set(r['provenance']) == {'kind', 'source', 'label_basis', 'teacher_model'}
        assert r['provenance']['kind'] == r['provenance']['label_basis'] == 'teacher'
        assert case_by_id[r['id']]['subject'] in r['question']
        assert set(o['text'] for o in r['options']) == set(STYLES[case_by_id[r['id']]['style']].values())
        assert len({len(o['text'].split()) for o in r['options']}) == 1

    for split, rows in artifacts.items():
        path = ROOT / f'{split}.jsonl'
        path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))
        cls = collections.Counter(case_by_id[r['id']]['label'] for r in rows)
        positions = {}
        lengths = {}
        for label in CLASSES:
            rr = [r for r in rows if case_by_id[r['id']]['label'] == label]
            positions[CLASS_NAMES[label]] = [sum(case_by_id[r['id']]['position'] == p for r in rr) for p in range(4)]
            unique_longest = 0
            among_longest = 0
            for r in rr:
                lens = [len(o['text'].split()) for o in r['options']]
                pos = case_by_id[r['id']]['position']
                among_longest += lens[pos] == max(lens)
                unique_longest += lens[pos] == max(lens) and lens.count(max(lens)) == 1
            lengths[CLASS_NAMES[label]] = {'rows': len(rr), 'uniquely_longest_correct': unique_longest, 'tied_or_unique_longest_correct': among_longest}
            assert max(positions[CLASS_NAMES[label]]) - min(positions[CLASS_NAMES[label]]) <= 1
        total_positions = [sum(case_by_id[r['id']]['position'] == p for r in rows) for p in range(4)]
        assert len(set(total_positions)) == 1
        diagnostics[split] = {
            'rows': len(rows), 'groups': len(rows), 'domains': len({case_by_id[r['id']]['domain'] for r in rows}),
            'class_counts': {CLASS_NAMES[k]: cls[k] for k in CLASSES},
            'target_positions_by_class_1_based_columns': positions, 'target_position_totals': total_positions,
            'option_count': 4, 'correct_option_length_diagnostics_words': lengths,
            'candidate_style_counts_by_class': {CLASS_NAMES[k]: dict(sorted(collections.Counter(case_by_id[r['id']]['style'] for r in rows if case_by_id[r['id']]['label'] == k).items())) for k in CLASSES},
            'question_form_counts_by_class': {CLASS_NAMES[k]: dict(sorted(collections.Counter(case_by_id[r['id']]['question_form'] for r in rows if case_by_id[r['id']]['label'] == k).items())) for k in CLASSES},
        }

    # Lexical candidates are diagnostic only; similarity does not certify semantic independence.
    candidates = []
    for a in artifacts['train']:
        aa = set(re.findall(r'\w+', a['state'].lower()))
        for b in artifacts['validation']:
            bb = set(re.findall(r'\w+', b['state'].lower()))
            overlap = len(aa & bb) / len(aa | bb)
            candidates.append((overlap, a['id'], b['id']))
    candidates.sort(reverse=True)
    hashes = {name: digest(ROOT / name) for name in (
        'plan_groups.py', 'group_assignments.json', 'source_cases.txt', 'generate.py', 'train.jsonl', 'validation.jsonl')}
    metadata = {
        'schema_version': '0.1', 'shard_id': SHARD,
        'teacher': {'provider': provider, 'model_alias': model, 'immutable_revision': None},
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
        'generation_settings': {
            'generation_revision': REVISION, 'source_revision': SOURCE_REVISION,
            'assignment_revision': ASSIGNMENT_REVISION, 'seed': SEED,
            'method': 'Existing approved agent authored 240 standalone synthetic experiences and teacher labels; deterministic standard-library Python assembly only.',
            'sampling_parameters': None, 'sampling_parameters_status': 'Not exposed by the existing agent session.',
            'group_namespace': 'data:pilot-v2:sentiment-b:', 'rows_per_group': 1,
            'assignment_frozen_before_source_authoring': True,
            'configuration': 'configs/data/pilot-v2.json; exact sentiment-b entry',
            'hashes_sha256': hashes,
            'option_order': 'Independent seeded per-class schedules; class positions differ by at most one; split totals exactly balanced.',
            'candidate_and_question_styles': 'Five complete styles and five question forms, independently scheduled; equal frequencies within every class and split.',
            'teacher_identity_environment': ['PI_PROVIDER', 'PI_MODEL'],
        },
        'usage_constraints': 'Original synthetic content under existing provider terms; no independent redistribution-license claim. No private records or external source text. Train rows for training; validation rows held out from weight updates. IDs, provenance, and metadata are not model features.',
        'row_counts': {'train': 200, 'validation': 40},
        'group_counts': {'train': 200, 'validation': 40, 'total': 240},
        'limitations': [
            'Labels are teacher judgments; author self-review is not independent correctness verification.',
            'The environment exposes an alias, not an immutable model revision; sampling parameters are unavailable.',
            'No tokenizer or ML stack was loaded. Parent must audit the 256-token cap.',
            'No parent, other producer, or evaluation examples were read; historical overlap checks are limited to configured reserved domains.',
            'Independent events are author-designed synthetic scenarios, not independently collected real-world observations.',
        ],
    }
    save(ROOT / 'metadata.json', metadata)
    report = {
        'schema_version': '0.1', 'shard_id': SHARD, 'status': 'passed_structural_checks',
        'checks': {
            'required_row_counts': True, 'teacher_provenance_only': True, 'schema_and_target_membership': True,
            'global_namespaced_unique_ids_within_shard': True, 'one_row_per_frozen_group': True,
            'frozen_group_split_compliance': True, 'exact_state_duplicates': 0,
            'canonical_input_duplicates': 0, 'cross_split_group_overlap': 0,
            'all_four_categories_always_available': True, 'forbidden_label_words_in_states': 0,
            'named_subject_in_every_question': True, 'ten_cases_per_domain': True,
        },
        'splits': diagnostics,
        'word_counts': {
            'state_min': min(len(r['state'].split()) for r in all_rows),
            'state_max': max(len(r['state'].split()) for r in all_rows),
            'question_max': max(len(r['question'].split()) for r in all_rows),
            'option_max': max(len(o['text'].split()) for r in all_rows for o in r['options']),
        },
        'cross_split_lexical_method': 'Lowercase word-set Jaccard over states; top eight diagnostic candidates, not an independence guarantee.',
        'cross_split_lexical_candidates': [{'jaccard': round(score, 5), 'train_id': a, 'validation_id': b} for score, a, b in candidates[:8]],
        'hashes_sha256': {**hashes, 'metadata.json': digest(ROOT / 'metadata.json')},
        'not_performed': ['Independent label review', 'Historical corpus content comparison (prohibited)', 'CPU tokenizer cap audit (parent responsibility)', 'Model evaluation', 'Software tests or linting'],
    }
    save(ROOT / 'validation_report.json', report)
    print(json.dumps({'rows': metadata['row_counts'], 'groups': metadata['group_counts'], 'word_counts': report['word_counts'], 'lexical_candidates': report['cross_split_lexical_candidates']}, indent=2))


if __name__ == '__main__':
    main()
