#!/usr/bin/env python3
"""Deterministically serialize private, teacher-authored sentiment scenarios; CPU only."""
import collections
import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/pilot-v2.json')
JOB = 'data-pilot-v2/sentiment-a'
REVISION = 'sentiment-a-generator-r1'
SEED = 271828
TEACHER = {'provider': 'openai', 'model_alias': 'gpt-sol', 'immutable_revision': None}
CLASSES = ['P', 'N', 'U', 'M']
CLASS_NAMES = {'P': 'positive-only', 'N': 'negative-only', 'U': 'neutral/no evaluation', 'M': 'mixed approval and criticism'}
OPTION_STYLES = [
    {
        'P': 'The writer expresses approval of the subject, without offering any criticism of it.',
        'N': 'The writer criticises the subject and offers no approval.',
        'U': 'The writer reports facts about the subject without evaluating it.',
        'M': 'The writer expresses both approval and criticism of the subject.',
    },
    {
        'P': 'Approval of the item, with no complaint about it.',
        'N': 'Criticism of the item, with no expression of approval for anything about it.',
        'U': 'Information about the item, without judging its merits.',
        'M': 'Praise for the item alongside a complaint about it.',
    },
    {
        'P': 'A favourable assessment without any expressed reservation about the item.',
        'N': 'An unfavourable assessment without anything commended about the item.',
        'U': 'A descriptive account of the item, without any judgement of its merits or shortcomings.',
        'M': 'An assessment that commends something and also finds fault with the item.',
    },
    {
        'P': 'The subject is praised, and no fault with it is expressed.',
        'N': 'The subject is faulted, and no praise for it is expressed.',
        'U': 'The subject is described without any praise or criticism of it.',
        'M': 'The writer conveys approval of the subject while also expressing criticism of it.',
    },
    {
        'P': 'Approval is expressed about the subject without any accompanying criticism.',
        'N': 'Criticism is expressed about the subject without any accompanying approval.',
        'U': 'The subject is described without any approval or criticism expressed.',
        'M': 'Approval and criticism are both expressed about the named subject.',
    },
]
QUESTIONS = [
    'What attitude does the writer express toward {subject}?',
    'How does the writer regard {subject}?',
    'What assessment is given of {subject}?',
    'How is {subject} evaluated in this account?',
    'What stance is conveyed toward {subject}?',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def word_count(text):
    return len(text.split())


def main():
    assignments_path = ROOT / 'group_assignments.json'
    assignment_hash_before = sha(assignments_path)
    assignment = json.loads(assignments_path.read_text())['groups']
    config = json.loads(CONFIG.read_text())
    reservation = next(x for x in config['assignments'] if x['producer'] == 'sentiment-a')
    domains = reservation['train_domains'] + reservation['validation_domains']
    records = []
    domain = None
    section_counts = collections.Counter()
    for line in (ROOT / 'source_cases.txt').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        if line.startswith('@'):
            domain = line[1:]
            assert domain in domains, domain
            continue
        code, subject, state = line.split('|', 2)
        assert code in CLASSES and subject and state and domain
        section_counts[domain] += 1
        n = len(records) + 1
        group = reservation['group_namespace'] + f'g{n:03d}'
        a = assignment[group]
        assert domain == a['domain'] == domains[(n - 1) // 10]
        assert a['split'] == ('train' if n <= 200 else 'validation')
        assert a['scenario_plan']
        records.append({'code': code, 'subject': subject, 'state': state,
                        'group_id': group, 'split': a['split'], 'domain': domain})
    assert len(records) == len(assignment) == 240
    assert section_counts == collections.Counter({d: 10 for d in domains})
    assert len(domains) == len(set(domains)) == 24
    assert not set(reservation['train_domains']) & set(config['avoid_new_training_domains'])

    positions = {}
    styles = {}
    questions = {}
    extras = [[0, 1], [2, 3], [0, 2], [1, 3]]
    for split, expected in [('train', 50), ('validation', 10)]:
        for c, code in enumerate(CLASSES):
            indices = [i for i, rec in enumerate(records) if rec['split'] == split and rec['code'] == code]
            assert len(indices) == expected
            ps = [p for p in range(4) for _ in range(expected // 4)] + extras[c]
            ss = list(range(5)) * (expected // 5)
            qs = list(range(5)) * (expected // 5)
            random.Random(f'{SEED}:position:{split}:{code}').shuffle(ps)
            random.Random(f'{SEED}:style:{split}:{code}').shuffle(ss)
            random.Random(f'{SEED}:question:{split}:{code}').shuffle(qs)
            for i, p, s, q in zip(indices, ps, ss, qs):
                positions[i], styles[i], questions[i] = p, s, q

    rows = []
    internal = []
    for i, rec in enumerate(records):
        rng = random.Random(f'{SEED}:distractors:{rec["group_id"]}')
        other_codes = [c for c in CLASSES if c != rec['code']]
        rng.shuffle(other_codes)
        ordered_codes = other_codes[:]
        ordered_codes.insert(positions[i], rec['code'])
        id_rng = random.Random(f'{SEED}:opaque-ids:{rec["group_id"]}')
        options = [{'id': f'c{id_rng.getrandbits(64):016x}', 'text': OPTION_STYLES[styles[i]][c]}
                   for c in ordered_codes]
        row = {
            'schema_version': '0.1', 'id': rec['group_id'] + ':r01',
            'state': rec['state'], 'question': QUESTIONS[questions[i]].format(subject=rec['subject']),
            'options': options, 'target_id': options[positions[i]]['id'],
            'group_id': rec['group_id'], 'task_family': 'sentiment', 'split': rec['split'],
            'provenance': {'kind': 'teacher', 'source': JOB + ':sentiment-a-authored-r1',
                           'label_basis': 'teacher', 'teacher_model': TEACHER['model_alias']},
        }
        rows.append(row)
        internal.append({'code': rec['code'], 'position': positions[i], 'style': styles[i],
                         'question_style': questions[i], 'domain': rec['domain']})

    ids = [r['id'] for r in rows]
    groups = [r['group_id'] for r in rows]
    assert len(set(ids)) == len(set(groups)) == 240
    states = [r['state'] for r in rows]
    normal_states = [' '.join(s.casefold().split()) for s in states]
    assert len(set(states)) == len(set(normal_states)) == 240
    canonical = [json.dumps([r['state'], r['question'], [o['text'] for o in r['options']]],
                            ensure_ascii=False) for r in rows]
    assert len(set(canonical)) == 240
    train_groups = {r['group_id'] for r in rows if r['split'] == 'train'}
    val_groups = {r['group_id'] for r in rows if r['split'] == 'validation'}
    assert not train_groups & val_groups
    forbidden = re.compile(r'\b(?:positive|negative|neutral|mixed)\b', re.I)
    all_option_ids = []
    for row, rec in zip(rows, records):
        assert row['schema_version'] == '0.1' and row['task_family'] == 'sentiment'
        assert row['state'] and isinstance(row['state'], str)
        assert row['question'].strip() and rec['subject'] in row['question']
        assert row['split'] in ('train', 'validation')
        assert len(row['options']) == 4
        option_ids = [o['id'] for o in row['options']]
        assert len(set(option_ids)) == 4 and all(option_ids)
        assert sum(o['id'] == row['target_id'] for o in row['options']) == 1
        assert all(o['text'].strip() for o in row['options'])
        assert not forbidden.search(row['state'])
        assert row['provenance']['kind'] == row['provenance']['label_basis'] == 'teacher'
        assert row['provenance']['source'].startswith(JOB)
        all_option_ids.extend(option_ids)
    assert len(set(all_option_ids)) == len(all_option_ids)

    split_stats = {}
    for split, expected_rows in [('train', 200), ('validation', 40)]:
        indices = [i for i, r in enumerate(rows) if r['split'] == split]
        assert len(indices) == expected_rows
        class_counts = collections.Counter(internal[i]['code'] for i in indices)
        position_counts = collections.Counter(internal[i]['position'] + 1 for i in indices)
        assert set(class_counts.values()) == {expected_rows // 4}
        assert set(position_counts.values()) == {expected_rows // 4}
        by_class = {}
        for code in CLASSES:
            ix = [i for i in indices if internal[i]['code'] == code]
            pc = collections.Counter(internal[i]['position'] + 1 for i in ix)
            sc = collections.Counter(internal[i]['style'] for i in ix)
            qc = collections.Counter(internal[i]['question_style'] for i in ix)
            assert max(pc.values()) - min(pc.values()) <= 1 and len(pc) == 4
            assert len(sc) == len(qc) == 5
            assert len(set(sc.values())) == len(set(qc.values())) == 1
            unique_longest = 0
            tied_longest = 0
            target_lengths = []
            for i in ix:
                lens = [word_count(o['text']) for o in rows[i]['options']]
                length = lens[internal[i]['position']]
                target_lengths.append(length)
                if length == max(lens):
                    if lens.count(length) == 1:
                        unique_longest += 1
                    else:
                        tied_longest += 1
            by_class[CLASS_NAMES[code]] = {
                'rows': len(ix), 'target_positions_1_based': dict(sorted(pc.items())),
                'option_style_counts': dict(sorted(sc.items())),
                'question_style_counts': dict(sorted(qc.items())),
                'target_unique_longest_words': unique_longest,
                'target_tied_longest_words': tied_longest,
                'mean_target_words': round(sum(target_lengths) / len(target_lengths), 3),
            }
        output_path = ROOT / (split + '.jsonl')
        output_path.write_text(''.join(json.dumps(rows[i], ensure_ascii=False, separators=(',', ':')) + '\n'
                                       for i in indices))
        split_stats[split] = {
            'rows': len(indices), 'groups': len(indices), 'independently_authored_scenarios': len(indices),
            'domain_counts': dict(sorted(collections.Counter(internal[i]['domain'] for i in indices).items())),
            'class_counts': {CLASS_NAMES[c]: class_counts[c] for c in CLASSES},
            'target_positions_1_based': dict(sorted(position_counts.items())), 'by_class': by_class,
        }

    stopwords = set('a an the of to in on and or is it its i my we our for with as at from that this by but so not no me have has had was were be been are into than them their they each then when which while through after before without only all one two'.split())
    def lexical_set(i):
        tokens = set(re.findall(r"[a-z]+", rows[i]['state'].casefold()))
        subject_tokens = set(re.findall(r'[a-z]+', records[i]['subject']))
        return tokens - stopwords - subject_tokens
    token_sets = [lexical_set(i) for i in range(len(rows))]
    pairs = []
    for i in range(200):
        for j in range(200, 240):
            union = token_sets[i] | token_sets[j]
            score = len(token_sets[i] & token_sets[j]) / len(union) if union else 0
            pairs.append((score, i, j))
    pairs.sort(reverse=True)
    threshold = 0.45
    candidates = [{'train_id': rows[i]['id'], 'validation_id': rows[j]['id'],
                   'content_word_jaccard': round(score, 4)} for score, i, j in pairs if score >= threshold]
    length_stats = {}
    for key in ['state', 'question']:
        lengths = [word_count(r[key]) for r in rows]
        length_stats[key + '_words'] = {'min': min(lengths), 'max': max(lengths),
                                       'mean': round(sum(lengths) / len(lengths), 3)}
    option_lengths = [word_count(o['text']) for r in rows for o in r['options']]
    length_stats['option_words'] = {'min': min(option_lengths), 'max': max(option_lengths)}
    pair_lengths = [word_count(r['state'] + ' ' + r['question'] + ' ' + o['text'])
                    for r in rows for o in r['options']]
    length_stats['max_state_question_single_option_words'] = max(pair_lengths)

    assert sha(assignments_path) == assignment_hash_before
    hashes = {name: sha(ROOT / name) for name in
              ['source_cases.txt', 'group_assignments.json', 'generate.py', 'train.jsonl', 'validation.jsonl']}
    hashes['pilot-v2.json'] = sha(CONFIG)
    metadata = {
        'schema_version': '0.1', 'shard_id': 'data-pilot-v2-sentiment-a-r1', 'teacher': TEACHER,
        'cost': {'currency': 'GBP', 'additional_spend': 0, 'pending_spend': 0},
        'generation_settings': {
            'job': JOB, 'method': 'Direct original synthetic scenario and label authoring by the active approved teacher; deterministic CPU-only serialization, candidate ordering and structural validation.',
            'seed': SEED, 'generation_revision': REVISION, 'source_revision': 'sentiment-a-authored-r1',
            'assignment_revision': 'sentiment-a-frozen-assignments-r1',
            'config_revision': 'data-pilot-v2', 'hash_algorithm': 'sha256', 'hashes': hashes,
            'teacher_identity_source': 'PI_PROVIDER=openai; PI_MODEL=gpt-sol observed in this session before authoring',
            'sampling': {'temperature': None, 'top_p': None, 'reason': 'Harness sampling settings unavailable; no new API calls were made.'},
            'immutable_revision_available': False,
            'rows_per_group': 1, 'options_per_row': 4,
            'class_names': CLASS_NAMES,
            'balancing': 'Per split/class: shuffled near-uniform target slots, independently shuffled exactly uniform option-style and question-style schedules; other candidates independently shuffled.',
            'position_numbering': 'one-based in reports; zero-based internal implementation',
            'source_format': 'Domain headers then class|subject|state; sequential lines bind to prewritten g001..g240 assignments.',
        },
        'usage_constraints': {
            'origin': 'Original synthetic text generated under the existing provider terms for this job.',
            'license': 'No independent redistribution-license claim; applicable provider terms and downstream obligations remain in force.',
            'privacy': 'No private records or real customer data; fictional everyday experiences.',
            'split_policy': 'Frozen groups and domain allocation; validation for held-out measurement, not training updates.',
            'features': 'Only state, question and option texts are model inputs; IDs, labels, group and provenance are not features.',
        },
        'row_counts': {'train': 200, 'validation': 40},
        'group_counts': {'train': 200, 'validation': 40},
        'limitations': [
            'All sentiment targets are teacher labels; author self-review is not independent correctness verification.',
            'Immutable teacher revision and sampling parameters were unavailable.',
            'No tokenizer or ML loads used; the parent CPU audit must verify the 256-token pair cap.',
            'Only this private shard was checked for duplicates and lexical candidates; no parent rows, other producer content or evaluation data were inspected.',
            'Independent scenario count refers to separately authored experiences, not statistically independent samples; all rows share one teacher and five candidate/question styles.',
            'Historical boundaries checked against config domain reservations only, without opening historical content.',
        ],
    }
    dump('metadata.json', metadata)
    report = {
        'schema_version': '0.1', 'job': JOB, 'validation_revision': REVISION,
        'status': 'passed_structural_checks', 'counts': split_stats,
        'checks': {
            'contract_fields_types_and_values': True, 'exact_requested_counts': True,
            'unique_namespaced_row_ids': True, 'unique_namespaced_singleton_groups': True,
            'opaque_option_ids_unique': True, 'exactly_one_supplied_target': True,
            'one_row_per_frozen_group': True, 'assignment_hash_unchanged_during_generation': True,
            'split_group_isolation': True, 'domain_allocation_matches_config': True,
            'no_reserved_training_domains': True, 'four_mutually_exclusive_categories_every_row': True,
            'balanced_classes': True, 'balanced_target_positions_per_class_split_option_count': True,
            'question_and_option_style_counts_independent_of_class': True,
            'exact_state_duplicates': 0, 'casefold_whitespace_normalized_state_duplicates': 0,
            'exact_canonical_input_duplicates': 0, 'forbidden_answer_label_words_in_states': 0,
            'provenance_job_and_teacher_present': True,
        },
        'hashes': {**hashes, 'metadata.json': sha(ROOT / 'metadata.json')},
        'lengths_whitespace_not_tokens': length_stats,
        'own_shard_cross_split_lexical_screen': {
            'method': 'Content-word set Jaccard excluding listed stopwords and each row subject words; all 8000 local train/validation pairs.',
            'threshold': threshold, 'candidate_count': len(candidates), 'candidates': candidates,
            'maximum_similarity': round(pairs[0][0], 4),
            'highest_pair': {'train_id': rows[pairs[0][1]]['id'], 'validation_id': rows[pairs[0][2]]['id']},
            'scope': 'This shard only. Lexical screening does not prove absence of semantic derivatives.',
        },
        'semantic_review': {
            'method': 'Same-teacher authoring review of all 240 cases against four-category definitions; no separate teacher call.',
            'independent_verification': False,
            'focus': ['Neutral rows make no evaluative claim about the question subject.',
                      'Mixed rows contain approval and a substantive complaint about the same subject.',
                      'Criticism of old/other products and rejected expectations are not transferred onto the named subject.',
                      'Removed an incidental capacity commendation from a negative bag case before serialization.',
                      'Revised the small-cup kettle complaint to condensation from its lid, keeping it distinct from the separate minimum-fill waste scenario.'],
        },
        'not_performed': ['Independent or separate-session label verification', 'Tokenizer-based 256-token audit',
                          'Cross-producer or parent-content duplicate audit', 'Model training or inference',
                          'Software tests or linting', 'Network/API requests or new ML loads'],
        'additional_spend_gbp': 0, 'pending_spend_gbp': 0,
    }
    dump('validation_report.json', report)
    review = f'''# Generation review — sentiment-a r1

## Deliverable
- **200 train + 40 validation**, all new: 240 singleton groups / 240 separately authored experiences.
- Exactly 20 assigned train domains and 4 assigned validation domains, 10 scenarios each.
- Frozen assignments were written before any cases and retained without split changes.
- Teacher: **openai / gpt-sol**, observed from PI_PROVIDER / PI_MODEL. Revision and sampling unavailable.
- Existing approved text generation only; additional and pending spend **£0**.

## Authoring and review
Each domain covers different uses or incidents rather than four sentiment rewrites of one event. Cases include indirect approval, ordinary complaints, factual records, rejected expectations, negation, and comparisons to other items. Questions retain the exact subject; all four mutually exclusive attitudes appear every time. Approval plus a real fault is labelled as both, not by whichever clause is stronger. Neutral cases do not evaluate the named item.

The same teacher reviewed all source cases. A bag case's incidental capacity commendation was removed so its criticism-only target is not ambiguous. The small-cup kettle scenario uses a lid-condensation complaint rather than repeating the separate minimum-fill scenario. This is **not independent label verification**. Subject comparisons concern other items or expectations, not hidden evidence that the current subject has both attitudes.

## Structural evidence
`python3 generate.py` reads only this private directory and the assignment config, uses Python's standard library, and regenerates the deliverables deterministically with seed {SEED}. Source cases, generator and assignment SHA-256 values are in `metadata.json` and `validation_report.json`.

Train classes are 50 each; validation classes are 10 each. Target slots total 50 each in train and 10 each in validation. Within each class the slots differ by at most one (12/13 train, 2/3 validation). Five question styles and five complete option styles have equal frequencies within every class/split; distractor order is independently shuffled. Full class/slot/style and target-length statistics are in the report. Across the five candidate styles, each category is uniquely longest in one style, and all categories tie in the fifth. Thus the target is uniquely longest on exactly 20% of rows in every class/split, not a class-dependent cue.

All contract, target membership, ID uniqueness, exact/normalized state duplicate, canonical-input duplicate, frozen-domain/group and split-isolation checks passed. Local cross-split content-word Jaccard screening found **{len(candidates)} pairs at threshold {threshold}** (maximum {pairs[0][0]:.4f}); this screen is not a semantic guarantee. State lengths are {length_stats['state_words']['min']}–{length_stats['state_words']['max']} whitespace words; longest state/question/single-option combination is {max(pair_lengths)} words. No tokenizer was used.

## Handoff boundaries
No historical examples, other producer content, evaluation data, Git, manifests, or model code were read or changed. Shared contracts and checkout instructions were read only; nothing in a checkout was edited. Reserved domains were respected using config boundaries. The parent still needs its tokenizer audit, full-dataset duplicate/boundary checks and separate-session teacher spot review. These outputs claim structural validation and teacher self-review only. Original synthetic text remains subject to existing provider terms; no independent redistribution licence is asserted.

Files: `group_assignments.json`, `source_cases.txt`, `generate.py`, `train.jsonl`, `validation.jsonl`, `metadata.json`, `validation_report.json`, and this review. Finished outputs are frozen at handoff.
'''
    (ROOT / 'generation_review.md').write_text(review)
    print(json.dumps({'status': report['status'], 'row_counts': metadata['row_counts'],
                      'group_counts': metadata['group_counts'], 'hashes': hashes,
                      'lexical_candidates': len(candidates), 'lengths': length_stats}, indent=2))


if __name__ == '__main__':
    main()
