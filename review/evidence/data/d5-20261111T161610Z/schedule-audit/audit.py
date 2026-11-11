#!/usr/bin/env python3
"""Bounded actual-TRAIN artifact audit; stdlib only, no model/code imports.
Run: python3 /absolute/path/to/schedule-audit/audit.py
Creates report.json/md exclusively beside this new script; refuses overwrite.
"""
import collections
import hashlib
import json
import math
from pathlib import Path
import random

ROOT = Path('/Users/destiner/Code/jeff/artifacts')
OUT = ROOT / 'data/d5-20261111T161610Z/schedule-audit'
MODEL = ROOT / 'model/m6-qwen-20261111-01'
MANIFEST = ROOT / 'data/data-pilot-v2/manifest.json'
PIN = 'd97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac'
NAMES = ['train-audit/schedule.jsonl', 'train-audit/audit.json',
         'training/fit-before.jsonl', 'training/fit-after.jsonl',
         'training/online.jsonl', 'training/receipt.json', 'full-run-freeze.json']


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    for name in ['report.json', 'report.md']:
        if (OUT / name).exists():
            raise SystemExit('Refusing to overwrite ' + str(OUT / name))
    raw = {MANIFEST: MANIFEST.read_bytes()}
    if sha(raw[MANIFEST]) != PIN:
        raise SystemExit('Pinned manifest hash mismatch; no shards read')
    manifest = json.loads(raw[MANIFEST])
    shards = [s for s in manifest['shards'] if s['split'] == 'train']
    # Only paths explicitly declared TRAIN by the pinned manifest may be opened.
    paths = [ROOT / s['path'] for s in shards] + [MODEL / n for n in NAMES]
    for p in paths:
        raw[p] = p.read_bytes()
    before = {str(p): sha(b) for p, b in raw.items()}
    mismatches = []
    checks = collections.Counter()

    def check(ok, kind, location, expected=None, actual=None):
        checks[kind] += 1
        if not ok:
            mismatches.append(dict(kind=kind, location=location, expected=expected, actual=actual))

    def equal(actual, expected, kind, location):
        check(type(actual) is type(expected) and actual == expected, kind, location, expected, actual)

    def lines(p):
        result = []
        for line_number, line in enumerate(raw[p].splitlines(), 1):
            if not line.strip():
                check(False, 'blank_jsonl_line', f'{p}:{line_number}')
                continue
            result.append(json.loads(line))
        return result

    def schema(rows):
        counts = collections.Counter(tuple(sorted(r)) for r in rows)
        return [dict(fields=list(k), rows=v) for k, v in sorted(counts.items())]

    originals = []
    shard_counts = []
    origin_path = {}
    for s in shards:
        p = ROOT / s['path']
        rows = lines(p)
        equal(before[str(p)], s['sha256'], 'manifest_train_hash', s['path'])
        equal(len(rows), s['rows'], 'manifest_train_count', s['path'])
        shard_counts.append(dict(path=s['path'], rows=len(rows), sha256=before[str(p)]))
        for row in rows:
            equal(row.get('split'), 'train', 'original_split', row.get('id'))
            origin_path[row['id']] = s['path']
        originals.extend(rows)
    equal(len(originals), 1500, 'original_total', 'TRAIN')
    ids = collections.Counter(r['id'] for r in originals)
    check(all(v == 1 for v in ids.values()), 'original_unique_ids', 'TRAIN', {}, {k:v for k,v in ids.items() if v != 1})
    source = {r['id']: r for r in originals}
    schedule = lines(MODEL / NAMES[0])
    audit = json.loads(raw[MODEL / 'train-audit/audit.json'])
    receipt = json.loads(raw[MODEL / 'training/receipt.json'])
    freeze = json.loads(raw[MODEL / 'full-run-freeze.json'])
    by_id = {r['id']: r for r in schedule}

    def coverage(rows, name):
        counts = collections.Counter(r['id'] for r in rows)
        missing = sorted(set(ids) - set(counts))
        unknown = sorted(set(counts) - set(ids))
        duplicate = {k:v for k,v in counts.items() if v != 1}
        equal(len(rows), 1500, 'row_count', name)
        equal(missing, [], 'missing_ids', name)
        equal(unknown, [], 'unknown_or_nontrain_ids', name)
        equal(duplicate, {}, 'duplicate_ids', name)
        indices = [r.get('index') for r in rows]
        equal(indices, list(range(1500)), 'index_coverage_and_file_order', name)
        return dict(rows=len(rows), unique_ids=len(counts), missing_ids=missing,
                    unknown_or_nontrain_ids=unknown, duplicate_ids=duplicate,
                    index_coverage_and_order=indices == list(range(1500)))

    coverage_report = {'schedule': coverage(schedule, 'schedule')}
    slots = []
    transitions = collections.Counter()
    arities = collections.Counter()
    original_slots = collections.Counter()
    permuted_slots = collections.Counter()
    # Replay precisely the algorithm declared in allowed binding metadata.
    equal(audit['evidence']['schedule_algorithm'], 'Random(42): shuffle rows then options once per row', 'declared_algorithm', 'audit')
    rng = random.Random(42)
    replay = list(originals)
    rng.shuffle(replay)
    for i, row in enumerate(schedule):
        loc = f'schedule:{i + 1}:{row["id"]}'
        if row['id'] not in source:
            continue
        original = source[row['id']]
        decision = row['decision']
        for field in ['id', 'state', 'question', 'schema_version']:
            equal(decision.get(field), original[field], 'decision_' + field, loc)
        equal(row['family'], original['task_family'], 'retained_family', loc)
        equal(row['group_id'], original['group_id'], 'retained_group_id', loc)
        equal(row['provenance'], original['provenance'], 'retained_provenance', loc)
        orig_ids = [o['id'] for o in original['options']]
        dec_ids = [o['id'] for o in decision['options']]
        equal(len(set(orig_ids)), len(orig_ids), 'original_option_id_uniqueness', loc)
        equal(row['original_option_ids'], orig_ids, 'original_option_order', loc)
        equal(row['option_ids'], dec_ids, 'decision_option_order', loc)
        equal(collections.Counter(dec_ids), collections.Counter(orig_ids), 'option_bijection', loc)
        equal(len(set(dec_ids)), len(dec_ids), 'permuted_option_id_uniqueness', loc)
        original_map = {o['id']: o['text'] for o in original['options']}
        for o in decision['options']:
            equal(o.get('text'), original_map.get(o['id']), 'option_id_exact_text', loc + ':' + o['id'])
        target = original['target_id']
        check(target in orig_ids, 'original_target_membership', loc, True, target in orig_ids)
        equal(row['target_id'], target, 'target_id_from_original_label', loc)
        if target in orig_ids and target in dec_ids:
            a, b = orig_ids.index(target), dec_ids.index(target)
            equal(row['target_position'], b, 'target_position_from_id', loc)
            arities[len(orig_ids)] += 1
            original_slots[a] += 1
            permuted_slots[b] += 1
            transitions[(a,b)] += 1
            slots.append(dict(id=row['id'], index=row['index'], shard=origin_path[row['id']],
                              target_id=target, original_target_slot=a, permuted_target_slot=b,
                              changed=a != b, option_arity=len(orig_ids)))
        if i < len(replay):
            expected = replay[i]
            opts = list(expected['options'])
            rng.shuffle(opts)
            equal(row['id'], expected['id'], 'replayed_row_order', loc)
            equal(decision['options'], opts, 'replayed_option_order_and_content', loc)
        equal(row['input_tokens'], len(row['prompt_tokens']), 'prompt_token_count', loc)
        check(all(type(t) is int and t >= 0 for t in row['prompt_tokens']), 'prompt_token_integer_domain', loc)
        equal(len(row['answer_ids']), len(orig_ids), 'answer_token_arity', loc)
        check(all(type(t) is int and t >= 0 for t in row['answer_ids']) and len(set(row['answer_ids'])) == len(row['answer_ids']), 'answer_token_integer_uniqueness', loc)

    fit_summary = {}
    schemas = {'original_train': schema(originals), 'schedule': schema(schedule),
               'decision': schema([r['decision'] for r in schedule]),
               'original_options': schema([o for r in originals for o in r['options']])}
    for name in ['fit-before', 'fit-after', 'online']:
        rows = lines(MODEL / ('training/' + name + '.jsonl'))
        schemas[name] = schema(rows)
        coverage_report[name] = coverage(rows, name)
        agreements = 0
        ces = []
        for i, row in enumerate(rows):
            loc = f'{name}:{i+1}:{row["id"]}'
            sch = by_id.get(row['id'])
            if sch is None:
                continue
            equal(row['index'], sch['index'], 'joined_index', loc)
            ce = row.get('ce')
            finite = type(ce) in (int,float) and math.isfinite(ce)
            check(finite, 'finite_ce', loc, 'finite number', ce)
            if finite:
                ces.append(ce)
                check(ce >= 0, 'nonnegative_ce', loc, '>=0', ce)
            if name == 'online':
                # No option IDs, predictions, targets, agreement or source fields exist here.
                equal(row.get('update'), i // 4 + 1, 'online_update_sequence', loc)
                continue
            original = source[row['id']]
            equal(row['option_ids'], sch['option_ids'], 'fit_option_ids', loc)
            for field in ['family', 'group_id', 'target_position']:
                equal(row[field], sch[field], 'fit_' + field, loc)
            equal(row['source'], original['provenance']['source'], 'fit_source', loc)
            for field in ['target_position', 'predicted_position']:
                valid = type(row[field]) is int and 0 <= row[field] < len(sch['option_ids'])
                check(valid, 'valid_' + field, loc, 'integer in option range', row[field])
            pred = row['predicted_position']
            if type(pred) is int and 0 <= pred < len(sch['option_ids']):
                agrees = sch['option_ids'][pred] == original['target_id']
                equal(row['agreement'], agrees, 'agreement_from_mapped_original_target_id', loc)
                agreements += agrees
        fit_summary[name] = dict(rows=len(rows), finite_ce_rows=len(ces),
                                 mean_ce=sum(ces)/len(ces) if ces else None)
        if name != 'online':
            fit_summary[name]['agreements_from_original_target_id'] = agreements

    bindings = []
    def binding(location, actual, expected):
        equal(actual, expected, 'binding_metadata', location)
        bindings.append(dict(location=location, declared=actual, observed=expected,
                             matches=type(actual) is type(expected) and actual == expected))

    sched_hash = before[str(MODEL / 'train-audit/schedule.jsonl')]
    audit_hash = before[str(MODEL / 'train-audit/audit.json')]
    binding('audit.schedule_sha256', audit['schedule_sha256'], sched_hash)
    binding('receipt.identity.schedule_sha256', receipt['identity']['schedule_sha256'], sched_hash)
    binding('receipt.identity.audit_sha256', receipt['identity']['audit_sha256'], audit_hash)
    binding('freeze.schedule_sha256', freeze['schedule_sha256'], sched_hash)
    for name in ['train-audit/audit.json', 'train-audit/schedule.jsonl']:
        pin = freeze['receipt_pins'][name]
        binding('freeze.receipt_pins.' + name + '.sha256', pin['sha256'], before[str(MODEL / name)])
        binding('freeze.receipt_pins.' + name + '.path', pin['path'], str(MODEL / name))
    for name, key in [('fit-before', 'fit_before'), ('fit-after', 'fit_after')]:
        p = MODEL / ('training/' + name + '.jsonl')
        binding('receipt.' + key + '.rows_sha256', receipt[key]['rows_sha256'], before[str(p)])
        binding('receipt.' + key + '.path', receipt[key]['path'], str(p))
        binding('receipt.' + key + '.overall.rows', receipt[key]['overall']['rows'], fit_summary[name]['rows'])
        binding('receipt.' + key + '.overall.agreements', receipt[key]['overall']['agreements'], fit_summary[name]['agreements_from_original_target_id'])
    binding('receipt.online_rows_sha256', receipt['online_rows_sha256'], before[str(MODEL / 'training/online.jsonl')])
    binding('receipt.presentations', receipt['presentations'], len(schedule))
    binding('freeze.recipe.train_rows', freeze['recipe']['train_rows'], len(originals))
    for label, evidence in [('audit', audit['evidence']), ('receipt.identity', receipt['identity']['evidence'])]:
        d = evidence['data']
        for field, expected in [('manifest_path', str(MANIFEST)), ('manifest_sha256', PIN),
                                ('dataset_id', manifest['dataset_id']), ('rows', len(originals)),
                                ('unique_ids', len(ids)), ('unique_groups', len({r['group_id'] for r in originals})),
                                ('families', dict(collections.Counter(r['task_family'] for r in originals)))]:
            binding(label + '.evidence.data.' + field, d[field], expected)
        expected_shards = [dict(s, resolved_path=str(ROOT / s['path'])) for s in shards]
        binding(label + '.evidence.data.train_shards', d['train_shards'], expected_shards)
    # Re-read only the exact allowlist already read, never metadata-referenced files.
    after = {str(p): sha(p.read_bytes()) for p in raw}
    for p in before:
        equal(after[p], before[p], 'input_unchanged', p)
    changed = sum(r['changed'] for r in slots)
    conclusion = ('This specific mapping/coverage defect is NOT demonstrated. '
                  'This is not a finding that training code is correct.' if not mismatches else
                  'Artifact mismatches were found; see row-level mismatch records. No training-code correctness claim is made.')
    report = dict(schema_version='d5.bounded-train-schedule-audit.v1', conclusion=conclusion,
                  scope='CPU stdlib inspection of actual TRAIN and named artifact files only; no execution of model/training code, semantic relabeling, optimizer review, private path traversal, network, tests, lint or weight access.',
                  manifest_pin=PIN, train_shards=shard_counts, original_rows=len(originals),
                  original_unique_ids=len(ids), original_unique_groups=len({r['group_id'] for r in originals}),
                  coverage=coverage_report, observed_schemas=schemas,
                  check_counts=dict(sorted(checks.items())), mismatch_count=len(mismatches), mismatches=mismatches,
                  option_arity_distribution=dict(sorted(arities.items())),
                  target_slots=dict(zero_based=True, changed=changed, unchanged=len(slots)-changed,
                                    original_slot_counts=dict(sorted(original_slots.items())),
                                    permuted_slot_counts=dict(sorted(permuted_slots.items())),
                                    transitions=[dict(original_slot=a, permuted_slot=b, rows=n) for (a,b),n in sorted(transitions.items())],
                                    per_row=slots),
                  fit_and_online=fit_summary, binding_checks=bindings,
                  file_hashes=[dict(path=p, sha256_before=before[p], sha256_after=after[p], unchanged=before[p]==after[p]) for p in sorted(before)],
                  inputs_unchanged=before == after,
                  limitations=[
                      'Online actual schema is ce,id,index,qualification,update; ID/index and CE checked. It does not record option IDs, positions, agreements, family, group or source, so these cannot be independently joined/verified for online rows.',
                      'Original targets are accepted as labels; no semantic correctness review or label inference from slot positions.',
                      'Prompt token counts/domain checked, but no tokenizer/model executed; prompt_token_sha256 serialization and token-to-text semantics are not independently established.',
                      'Only hashes of allowed files are verified; other freeze receipt pins and all model/weight/private paths are not followed.',
                      'Input immutability compares bytes at this script run entry with bytes at exit; no earlier-history claim.'
                  ])
    md = ['# D5 bounded TRAIN schedule audit', '', conclusion, '',
          f'- Original TRAIN: **{len(originals)} rows / {len(ids)} unique IDs / {len(shards)} manifest shards**.',
          f'- Row-level and binding mismatches: **{len(mismatches)}**.',
          f'- Original-target slot → permuted-target slot: **{changed} changed / {len(slots)-changed} unchanged** (zero-based; labels taken only from original target IDs).',
          f'- Option arities: `{json.dumps(dict(sorted(arities.items())))}`.',
          f'- Input hashes unchanged at audit exit: **{before == after}**.', '',
          '## Coverage', '', '| File | Rows | Unique IDs | Missing | Unknown/nontrain | Duplicate IDs | Index coverage/order |',
          '|---|---:|---:|---:|---:|---:|---|']
    for n,c in coverage_report.items():
        md.append(f'| {n} | {c["rows"]} | {c["unique_ids"]} | {len(c["missing_ids"])} | {len(c["unknown_or_nontrain_ids"])} | {len(c["duplicate_ids"])} | {c["index_coverage_and_order"]} |')
    md += ['', 'Verified exact decision ID/state/question/schema, original option order, bijective option ID→text preservation, target ID and remapped target position, retained family/group/provenance. Replayed declared Random(42) row shuffle and per-row option shuffle. Both fit files are joined by ID/index/option IDs and checked against original targets, source/group/family, valid positions, finite CE and recorded agreement.', '', '## Actual schema limitation', '', report['limitations'][0], '', '## Source shards', '', '| TRAIN shard | Rows | SHA-256 |', '|---|---:|---|']
    for s in shard_counts:
        md.append(f'| `{s["path"]}` | {s["rows"]} | `{s["sha256"]}` |')
    md += ['', '## Target slot transitions', '', '| Original slot | Permuted slot | Rows |', '|---:|---:|---:|']
    for (a,b),n in sorted(transitions.items()):
        md.append(f'| {a} | {b} | {n} |')
    md += ['', '## Exact input hashes', '', 'All below are SHA-256 of complete allowed input bytes. Before/after comparison is recorded per file in `report.json`.', '', '| Input | SHA-256 | Unchanged |', '|---|---|---|']
    for p in sorted(before):
        md.append(f'| `{p}` | `{before[p]}` | {before[p] == after[p]} |')
    md += ['', '## Mismatches', '', json.dumps(mismatches, indent=2) if mismatches else 'None.', '', '## Reproduction and boundaries', '', f'`python3 {OUT / "audit.py"}`', '', 'Stdlib only. Refuses existing report files: for reproduction preserve/move the two generated reports within the authorized output directory first. No fixtures or software tests. `report.json` includes observed schemas, all check counts, binding comparisons, all 1,500 row-level original/permuted target slots and every mismatch.', '']
    md += ['- ' + s for s in report['limitations']]
    with (OUT / 'report.json').open('x') as f:
        json.dump(report, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')
    with (OUT / 'report.md').open('x') as f:
        f.write('\n'.join(md) + '\n')
    print(json.dumps(dict(mismatches=len(mismatches), rows=len(originals), shards=len(shards), slot_changed=changed, slot_unchanged=len(slots)-changed, arities=dict(arities), inputs_unchanged=before == after, conclusion=conclusion)))


if __name__ == '__main__':
    main()
