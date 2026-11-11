#!/usr/bin/env python3
"""Serialize authored teacher cases and validate only this private shard (stdlib CPU)."""
import collections
import hashlib
import json
from pathlib import Path
import random
import re
import statistics

ROOT = Path(__file__).resolve().parent
CONFIG = Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/pilot-v2.json')
CONTRACT = Path('/Users/destiner/Code/jeff/.worktrees/data/docs/contracts.md')
SHARD = 'data-pilot-v2-intent-a-r1'
JOB = 'jeff/data-pilot-v2/intent-a/r1'
SEED = 741903


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def canonical(text):
    return ' '.join(text.casefold().split())


def words(text):
    return re.findall(r"\b[\w'-]+\b", text.casefold())


def main():
    authoring = json.loads((ROOT / 'authoring_record.json').read_text())
    provider = authoring['teacher']['provider']
    model = authoring['teacher']['model_alias']
    if not provider or not model:
        raise RuntimeError('Captured authoring teacher identity is required.')
    config = json.loads(CONFIG.read_text())
    assignment = next(a for a in config['assignments'] if a['producer'] == 'intent-a')
    groups = json.loads((ROOT / 'group_assignments.json').read_text())['groups']
    cases = []
    for line in (ROOT / 'source_cases.txt').read_text().splitlines():
        if not line.strip():
            continue
        short, state, *choices = [s.strip() for s in line.split('|')]
        n = int(short[1:])
        gid = assignment['group_namespace'] + short
        split = 'train' if n <= 200 else 'validation'
        domain = (assignment['train_domains'] + assignment['validation_domains'])[(n - 1) // 10]
        assert groups[gid]['split'] == split
        assert groups[gid]['domain'] == domain
        assert 3 <= len(choices) <= 6
        assert state and all(choices)
        cases.append({'group_id': gid, 'state': state, 'choices': choices, 'split': split})
    assert len(cases) == len(groups) == 240
    assert {c['group_id'] for c in cases} == set(groups)
    assert len({c['group_id'] for c in cases}) == 240

    # Balanced target schedules are drawn independently within each split/choice-count stratum.
    buckets = collections.defaultdict(list)
    for i, case in enumerate(cases):
        buckets[(case['split'], len(case['choices']))].append(i)
    placements = {}
    rng = random.Random(SEED)
    for (split, count), indices in sorted(buckets.items()):
        rng.shuffle(indices)
        cycle = rng.sample(range(count), count)
        positions = [cycle[j % count] for j in range(len(indices))]
        rng.shuffle(positions)
        placements.update(zip(indices, positions))

    rows = []
    for i, case in enumerate(cases):
        correct, *rivals = case['choices']
        # Use an independent per-row random stream for rival order, unrelated to semantics.
        row_rng = random.Random(f'{SEED}:rivals:{case["group_id"]}')
        row_rng.shuffle(rivals)
        rivals.insert(placements[i], correct)
        options = []
        for j, text in enumerate(rivals):
            opaque = hashlib.sha256(f'{JOB}:{case["group_id"]}:{j}:option'.encode()).hexdigest()[:14]
            options.append({'id': 'o' + opaque, 'text': text})
        row = {
            'schema_version': '0.1',
            'id': case['group_id'] + ':r01',
            'state': case['state'],
            'question': 'What is the primary intent of this request?',
            'options': options,
            'target_id': options[placements[i]]['id'],
            'group_id': case['group_id'],
            'task_family': 'intent',
            'split': case['split'],
            'provenance': {
                'kind': 'teacher',
                'source': JOB + '/source_cases.txt@r1#' + case['group_id'].rsplit(':', 1)[-1],
                'label_basis': 'teacher',
                'teacher_model': provider + '/' + model,
            },
        }
        assert options[placements[i]]['text'] == correct
        rows.append(row)
    for split in ('train', 'validation'):
        selected = [r for r in rows if r['split'] == split]
        (ROOT / (split + '.jsonl')).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in selected))

    # Validate the serialized bytes, not only the in-memory source objects.
    loaded = []
    for split, expected in [('train', 200), ('validation', 40)]:
        loaded_split = [json.loads(s) for s in (ROOT / (split + '.jsonl')).read_text().splitlines()]
        assert len(loaded_split) == expected
        assert all(r['split'] == split for r in loaded_split)
        loaded.extend(loaded_split)
    ids, gids, states, inputs = set(), set(), set(), set()
    positions = collections.defaultdict(collections.Counter)
    lengths = collections.defaultdict(list)
    domains = collections.defaultdict(collections.Counter)
    longest = collections.defaultdict(collections.Counter)
    for r in loaded:
        assert r['schema_version'] == '0.1' and r['task_family'] == 'intent'
        assert r['id'] == r['group_id'] + ':r01'
        assert r['group_id'].startswith(assignment['group_namespace'])
        assert r['id'] not in ids and r['group_id'] not in gids
        ids.add(r['id']); gids.add(r['group_id'])
        assert isinstance(r['state'], str) and isinstance(r['question'], str) and r['question'].strip()
        assert len(r['options']) in range(3, 7)
        option_ids = [o['id'] for o in r['options']]
        texts = [o['text'] for o in r['options']]
        assert len(set(option_ids)) == len(option_ids)
        assert all(isinstance(x, str) and x.strip() for x in option_ids + texts)
        assert len(set(map(canonical, texts))) == len(texts)
        assert option_ids.count(r['target_id']) == 1
        assert r['provenance']['kind'] == r['provenance']['label_basis'] == 'teacher'
        assert r['provenance']['source'].startswith(JOB)
        assert r['provenance']['teacher_model'] == provider + '/' + model
        state_key = canonical(r['state'])
        assert state_key not in states
        states.add(state_key)
        input_key = (state_key, canonical(r['question']), tuple(sorted(map(canonical, texts))))
        assert input_key not in inputs
        inputs.add(input_key)
        g = groups[r['group_id']]
        assert g['split'] == r['split']
        domains[r['split']][g['domain']] += 1
        pos = option_ids.index(r['target_id'])
        stratum = f'{r["split"]}/{len(option_ids)}'
        positions[stratum][pos + 1] += 1
        counts = [len(words(t)) for t in texts]
        lengths['state_words'].append(len(words(r['state'])))
        lengths['question_words'].append(len(words(r['question'])))
        lengths['option_words'].extend(counts)
        lengths['target_words'].append(counts[pos])
        lengths['rival_words'].extend(c for j, c in enumerate(counts) if j != pos)
        is_longest = counts[pos] == max(counts)
        is_unique_longest = is_longest and counts.count(counts[pos]) == 1
        longest[r['split']]['target_tied_or_unique_longest'] += int(is_longest)
        longest[r['split']]['target_unique_longest'] += int(is_unique_longest)
        longest[r['split']]['rows'] += 1
    assert set(domains['train']) == set(assignment['train_domains'])
    assert set(domains['validation']) == set(assignment['validation_domains'])
    assert all(n == 10 for counts in domains.values() for n in counts.values())
    forbidden = set(config['avoid_new_training_domains'])
    for a in config['assignments']:
        forbidden.update(a.get('validation_domains', []))
    assert not (set(domains['train']) & forbidden)
    train_groups = {r['group_id'] for r in loaded if r['split'] == 'train'}
    validation_groups = {r['group_id'] for r in loaded if r['split'] == 'validation'}
    assert not train_groups & validation_groups
    for stratum, counter in positions.items():
        n = int(stratum.split('/')[1])
        all_counts = [counter[p] for p in range(1, n + 1)]
        assert max(all_counts) - min(all_counts) <= 1

    # Lexical candidates are advisory and restricted to this new shard.
    lexical = []
    train = [r for r in loaded if r['split'] == 'train']
    validation = [r for r in loaded if r['split'] == 'validation']
    stop = set('a an the i my me to for and but is it in on of that this not please could you can do have with'.split())
    for t in train:
        tw = set(words(t['state'])) - stop
        for v in validation:
            vw = set(words(v['state'])) - stop
            overlap = len(tw & vw) / len(tw | vw)
            lexical.append((overlap, t['id'], v['id']))
    lexical.sort(reverse=True)
    file_names = ['group_assignments.json', 'authoring_record.json', 'source_cases.txt', 'generate.py', 'generation_review.md', 'train.jsonl', 'validation.jsonl']
    hashes = {name: digest(ROOT / name) for name in file_names}
    revisions = {
        'generation_revision': 'intent-a-r1',
        'source_revision': 'source-cases-r1',
        'assignment_revision': 'pilot-v2.json/intent-a frozen g001-g240',
        'assignment_config_sha256': digest(CONFIG),
        'contract_sha256': digest(CONTRACT),
        'artifact_sha256': hashes,
    }
    limitations = [
        'Teacher-authored labels and same-session semantic review are not independently verified correctness.',
        'Immutable teacher revision and provider sampling parameters were not exposed.',
        'No tokenizer or ML was loaded; the parent must audit the 256-token pair budget.',
        'Historical shards and other producer data were not inspected; global deduplication remains a parent gate.',
        'Domains and singleton scenario plans are distinct; generic request categories intentionally recur.',
    ]
    metadata = {
        'schema_version': '0.1', 'shard_id': SHARD,
        'teacher': {'provider': provider, 'model_alias': model, 'immutable_revision': None},
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
        'generation_settings': {
            **revisions,
            'method': 'Direct agent-authored independent requests and rival intents; CPU serialization and shuffled choices only.',
            'seed': SEED,
            'sampling': {'temperature': None, 'top_p': None, 'note': 'Harness settings unavailable; no API calls made.'},
            'source_format': 'One authored group per line: short group ID|state|teacher target text|rival texts. Correct source choice is first; exported positions are balanced and randomized.',
            'question': 'What is the primary intent of this request?',
            'position_method': 'Seeded shuffled balanced schedules independently within split and option count; independently shuffled rivals.',
            'rows_per_group': 1,
            'parent_rows_included': 0,
        },
        'usage_constraints': {
            'origin': 'Original synthetic text generated using existing approved agent access under existing provider terms.',
            'redistribution': 'No independent redistribution-license claim; subject to applicable provider terms.',
            'privacy': 'No private customer or company records used.',
            'features': 'Only state, question and option text are model inputs. IDs, targets, provenance and assignments are metadata.',
            'validation': 'Validation labels are for validation only, not weight updates.',
        },
        'row_counts': {'train': 200, 'validation': 40},
        'group_counts': {'train': 200, 'validation': 40},
        'limitations': limitations,
    }
    save('metadata.json', metadata)
    report = {
        'schema_version': '0.1', 'shard_id': SHARD, 'status': 'passed_local_structural_checks',
        'row_counts': {'train': 200, 'validation': 40},
        'group_counts': {'train': 200, 'validation': 40},
        'independent_scenarios': {'train': 200, 'validation': 40, 'basis': '240 individually authored singleton source cases and prewritten scenario plans, no variants.'},
        'domain_counts': {s: dict(c) for s, c in domains.items()},
        'checks': {
            'schema_required_fields': True, 'targets_present_exactly_once': True,
            'unique_row_ids': True, 'unique_option_ids_per_row': True,
            'singleton_groups_unique': True, 'cross_split_group_overlap': 0,
            'exact_canonical_state_duplicates': 0, 'exact_canonical_input_duplicates': 0,
            'frozen_group_domain_and_split_assignments': True,
            'ten_scenarios_per_assigned_domain': True, 'training_reserved_domain_overlap': [],
            'positions_balanced_within_split_and_option_count': True,
            'no_parent_rows_included': True,
        },
        'target_position_counts_1_based': {k: {p: v[p] for p in range(1, int(k.split('/')[1]) + 1)} for k, v in positions.items()},
        'option_count_distribution': {s: dict(collections.Counter(len(r['options']) for r in loaded if r['split'] == s)) for s in ('train', 'validation')},
        'target_length_shortcuts': {s: dict(c) for s, c in longest.items()},
        'word_length_summary_not_token_counts': {k: {'min': min(v), 'max': max(v), 'mean': round(statistics.mean(v), 3)} for k, v in lengths.items()},
        'cross_split_state_lexical_scan': {
            'method': 'Content-word set Jaccard, this shard only; no historical data read.',
            'pairs_scanned': len(lexical),
            'pairs_at_or_above_0_5': sum(x[0] >= 0.5 for x in lexical),
            'top_candidates': [{'jaccard': round(score, 4), 'train_id': t, 'validation_id': v} for score, t, v in lexical[:12]],
        },
        'teacher_semantic_review': {'kind': 'same_session_self_review', 'independently_verified': False, 'details_file': 'generation_review.md'},
        'tokenizer_audit': 'Not performed: prohibited ML/tokenizer loads; parent CPU audit pending.',
        'cost': metadata['cost'],
        'revisions': revisions,
        'metadata_sha256': digest(ROOT / 'metadata.json'),
        'limitations': limitations,
    }
    save('validation_report.json', report)
    print(json.dumps({'rows': report['row_counts'], 'groups': report['group_counts'], 'positions': report['target_position_counts_1_based'], 'lengths': report['word_length_summary_not_token_counts'], 'longest': report['target_length_shortcuts'], 'lexical': report['cross_split_state_lexical_scan']}, indent=2))


if __name__ == '__main__':
    main()
