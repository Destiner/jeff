"""Compile explicitly teacher-authored cases; CPU-only structural/data audit, no model calls."""
import collections
import hashlib
import json
import os
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parent
CONFIG = Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/pilot-v2.json')
SEED = 731947
JOB = 'data-pilot-v2-intent-b-r1'
REVISION = 'intent-b-generator-r1'
SOURCE_REVISION = 'intent-b-source-r1'
ASSIGNMENT_REVISION = 'intent-b-assignment-r1'


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def words(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def main():
    config = json.loads(CONFIG.read_text())
    assignment = next(a for a in config['assignments'] if a['producer'] == 'intent-b')
    groups = json.loads((ROOT / 'group_assignments.json').read_text())['groups']
    domains = assignment['train_domains'] + assignment['validation_domains']
    provider = os.environ.get('PI_PROVIDER')
    model = os.environ.get('PI_MODEL')
    assert provider and model, 'Actual teacher identity must be available'
    cases = []
    domain = None
    for line in (ROOT / 'source_cases.txt').read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        if line.startswith('@ '):
            domain = line[2:]
            continue
        parts = [x.strip() for x in line.split('|')]
        assert domain in domains and 4 <= len(parts) <= 7, line
        assert all(parts) and len(set(parts[1:])) == len(parts[1:])
        cases.append({'domain': domain, 'state': parts[0], 'choices': parts[1:]})
    assert len(cases) == 240
    assert list(dict.fromkeys(c['domain'] for c in cases)) == domains
    assert collections.Counter(c['domain'] for c in cases) == {d: 10 for d in domains}
    buckets = collections.defaultdict(list)
    for i, case in enumerate(cases, 1):
        group_id = assignment['group_namespace'] + f'g{i:03}'
        planned = groups[group_id]
        split = 'train' if i <= 200 else 'validation'
        assert planned['split'] == split and planned['domain'] == domains[(i - 1) // 10]
        assert case['domain'] == planned['domain']
        case.update(group_id=group_id, split=split)
        buckets[(split, len(case['choices']))].append(case)
    assert len(groups) == 240
    position_rng = random.Random(SEED)
    distractor_rng = random.Random(SEED + 1)
    id_rng = random.Random(SEED + 2)
    rows = []
    for (split, n), bucket in sorted(buckets.items()):
        cycles, remainder = divmod(len(bucket), n)
        positions = list(range(n)) * cycles + position_rng.sample(range(n), remainder)
        position_rng.shuffle(positions)
        for case, position in zip(bucket, positions):
            correct, *distractors = case['choices']
            distractor_rng.shuffle(distractors)
            texts = distractors[:]
            texts.insert(position, correct)
            options = [{'id': 'o' + f'{id_rng.getrandbits(64):016x}', 'text': text} for text in texts]
            rows.append({
                'schema_version': '0.1', 'id': case['group_id'] + ':r01',
                'state': case['state'], 'question': 'What does the customer want?',
                'options': options, 'target_id': options[position]['id'],
                'group_id': case['group_id'], 'task_family': 'intent', 'split': split,
                'provenance': {
                    'kind': 'teacher', 'source': JOB + '/' + SOURCE_REVISION,
                    'label_basis': 'teacher', 'teacher_model': model,
                },
            })
    rows.sort(key=lambda row: row['group_id'])
    split_counts = collections.Counter(row['split'] for row in rows)
    assert split_counts == {'train': 200, 'validation': 40}
    assert len({r['id'] for r in rows}) == len(rows)
    assert len({r['group_id'] for r in rows}) == len(rows)
    assert len({r['state'] for r in rows}) == len(rows)
    assert len({' '.join(words(r['state'])) for r in rows}) == len(rows)
    canonical_inputs = set()
    for row in rows:
        assert row['task_family'] == 'intent' and row['schema_version'] == '0.1'
        assert isinstance(row['state'], str) and row['state'].strip()
        assert row['question'].strip() and row['split'] in {'train', 'validation'}
        assert 2 <= len(row['options']) <= 6
        ids = [o['id'] for o in row['options']]
        assert len(ids) == len(set(ids)) and all(ids)
        assert sum(o['id'] == row['target_id'] for o in row['options']) == 1
        assert all(o['text'].strip() for o in row['options'])
        assert row['id'] == row['group_id'] + ':r01'
        p = row['provenance']
        assert p['kind'] == p['label_basis'] == 'teacher'
        assert JOB in p['source'] and p['teacher_model'] == model
        canonical = encoded([row['state'], row['question'], sorted(o['text'] for o in row['options'])])
        assert canonical not in canonical_inputs
        canonical_inputs.add(canonical)
    train = [r for r in rows if r['split'] == 'train']
    validation = [r for r in rows if r['split'] == 'validation']
    assert not ({r['group_id'] for r in train} & {r['group_id'] for r in validation})
    avoided = set(config['avoid_new_training_domains'])
    avoided.update(d for a in config['assignments'] for d in a.get('validation_domains', []))
    assert not (set(assignment['train_domains']) & avoided)
    position_counts = {}
    shortcut_metrics = {}
    for (split, n) in sorted(buckets):
        subset = [r for r in rows if r['split'] == split and len(r['options']) == n]
        counts = [0] * n
        longest = shortest = overlap_max = 0
        target_lengths = []
        distractor_lengths = []
        for row in subset:
            pos = next(i for i, o in enumerate(row['options']) if o['id'] == row['target_id'])
            counts[pos] += 1
            lengths = [len(words(o['text'])) for o in row['options']]
            longest += lengths[pos] == max(lengths) and lengths.count(max(lengths)) == 1
            shortest += lengths[pos] == min(lengths) and lengths.count(min(lengths)) == 1
            sw = set(words(row['state']))
            overlaps = [len(sw & set(words(o['text']))) for o in row['options']]
            overlap_max += overlaps[pos] == max(overlaps) and overlaps.count(max(overlaps)) == 1
            target_lengths.append(lengths[pos])
            distractor_lengths.extend(v for j, v in enumerate(lengths) if j != pos)
        assert max(counts) - min(counts) <= 1
        key = f'{split}/{n}_options'
        position_counts[key] = counts
        shortcut_metrics[key] = {
            'rows': len(subset), 'unique_longest_target': longest, 'unique_shortest_target': shortest,
            'target_unique_max_state_word_overlap': overlap_max,
            'mean_target_words': round(sum(target_lengths) / len(target_lengths), 3),
            'mean_distractor_words': round(sum(distractor_lengths) / len(distractor_lengths), 3),
        }
    # Diagnostic lexical comparison only; no final or parent content is opened.
    stop = set('the a an to of and is for in my i it this that me be on with not rather than want need please can could you'.split())
    def vocabulary(row):
        return set(words(row['state'])) - stop
    train_vocab = [(r, vocabulary(r)) for r in train]
    similarities = []
    for v in validation:
        vs = vocabulary(v)
        for t, ts in train_vocab:
            score = len(vs & ts) / len(vs | ts)
            similarities.append((score, t['id'], v['id']))
    top = sorted(similarities, reverse=True)[:10]
    for split in ['train', 'validation']:
        text = ''.join(encoded(r) + '\n' for r in rows if r['split'] == split)
        (ROOT / f'{split}.jsonl').write_text(text)
    revisions = {
        'generation_revision': REVISION, 'source_revision': SOURCE_REVISION,
        'assignment_revision': ASSIGNMENT_REVISION,
        'sha256': {name: sha(ROOT / name) for name in ['generate.py', 'source_cases.txt', 'group_assignments.json']},
        'config_sha256': sha(CONFIG),
    }
    output_hashes = {name: sha(ROOT / name) for name in ['train.jsonl', 'validation.jsonl']}
    metadata = {
        'schema_version': '0.1', 'shard_id': JOB,
        'teacher': {'provider': provider, 'model_alias': model, 'immutable_revision': None},
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
        'generation_settings': {
            **revisions, 'method': 'Existing approved agent authors every scenario and teacher label; deterministic CPU compilation only.',
            'seed': SEED, 'sampling_parameters': None, 'immutable_sampling_details': 'Unavailable from agent environment',
            'option_order': 'Balanced per split and option count; shuffled target slots independent of case content; distractors shuffled separately.',
            'option_ids': 'Independent deterministic opaque 64-bit identifiers',
            'question': 'What does the customer want?', 'task_family': 'intent',
            'rows_per_group': 1, 'parent_rows_read': 0, 'output_sha256': output_hashes,
        },
        'usage_constraints': {
            'origin': 'Original synthetic requests and labels generated under existing provider terms.',
            'redistribution': 'No independent redistribution-license claim; subject to applicable provider terms.',
            'privacy': 'No private records or real customer documents used.',
            'features': 'Only state, question, and option texts are model inputs; exclude IDs and provenance.',
        },
        'row_counts': dict(split_counts),
        'group_counts': {'train': 200, 'validation': 40, 'total': 240, 'independent_scenarios': 240, 'by_domain': dict(collections.Counter(c['domain'] for c in cases))},
        'limitations': [
            'All labels are teacher-authored; same-session review is not independent correctness verification.',
            'Teacher immutable revision and sampling configuration unavailable.',
            'No tokenizer or model loaded; parent must perform the 256-token audit.',
            'No historical examples or evaluation data inspected; parent must check historical overlap and aggregate uniqueness.',
            'Lexical overlap and explicit scope phrases may remain predictive; this is not a claim of shortcut-free data.',
            'Ten scenarios per domain provide limited coverage of that domain.',
        ],
    }
    save('metadata.json', metadata)
    report = {
        'schema_version': '0.1', 'shard_id': JOB, 'status': 'structural_checks_passed',
        'scope': 'This private shard only; teacher labels not independently verified.',
        'row_counts': dict(split_counts), 'group_counts': {'train': 200, 'validation': 40},
        'domain_counts': {'train': 20, 'validation': 4}, 'independent_scenarios': 240,
        'checks': {
            'contract_fields_and_targets': 'pass', 'unique_row_and_option_ids': 'pass',
            'one_row_per_frozen_group': 'pass', 'frozen_domain_order_and_split': 'pass',
            'exact_state_duplicates': 0, 'normalized_state_duplicates': 0,
            'exact_canonical_input_duplicates': 0, 'cross_split_group_overlap': 0,
            'reserved_domain_assignments_absent_from_training': 'pass',
            'balanced_positions_by_split_option_count': 'pass',
        },
        'target_position_counts_zero_based': position_counts,
        'length_and_overlap_diagnostics': shortcut_metrics,
        'max_words': {
            'state': max(len(words(r['state'])) for r in rows),
            'question': max(len(words(r['question'])) for r in rows),
            'option': max(len(words(o['text'])) for r in rows for o in r['options']),
            'state_question_single_option': max(len(words(r['state'] + ' ' + r['question'] + ' ' + o['text'])) for r in rows for o in r['options']),
        },
        'cross_split_lexical_top10': [{'jaccard': round(s, 4), 'train_id': t, 'validation_id': v} for s, t, v in top],
        'deferred_to_parent': ['256-token audit', 'historical and cross-producer duplicate/split audit', 'separate-session teacher spot review'],
        'revisions': revisions, 'output_sha256': output_hashes,
        'metadata_sha256': sha(ROOT / 'metadata.json'),
        'additional_spend_gbp': 0, 'pending_spend_gbp': 0,
    }
    save('validation_report.json', report)
    print(json.dumps({'rows': dict(split_counts), 'positions': position_counts, 'shortcuts': shortcut_metrics, 'max_words': report['max_words'], 'lexical_top10': report['cross_split_lexical_top10']}, indent=2))


if __name__ == '__main__':
    main()
