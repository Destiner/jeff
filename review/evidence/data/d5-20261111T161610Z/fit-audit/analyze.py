#!/usr/bin/env python3
"""Bounded saved-TRAIN statistics only. Python stdlib; no model execution.
Reproduce into a NEW directory under fit-audit: python3 analyze.py --output ...
All thresholds below are descriptive, fixed before the full calculation.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import statistics
import struct

ROOT = Path('/Users/destiner/Code/jeff/artifacts/data/d5-20261111T161610Z/fit-audit')
MODEL = Path('/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01')
INPUTS = {'before': MODEL/'training/fit-before.jsonl',
          'after': MODEL/'training/fit-after.jsonl',
          'receipt': MODEL/'training/receipt.json',
          'schedule': MODEL/'train-audit/schedule.jsonl'}
CE_THRESHOLDS = (1e-6, 1e-4, 1e-3, 1e-2, 0.1)
P_THRESHOLDS = (1e-6, 1e-4, 1e-3, 1e-2, 0.05)
RECONCILE_ATOL = 1e-10


def sha(b):
    return hashlib.sha256(b).hexdigest()


def mean(xs):
    return math.fsum(xs)/len(xs)


def spread(xs):
    s = sorted(xs)
    def quantile(q):
        t = (len(s)-1)*q
        i = int(t)
        return s[i] + (s[min(i+1, len(s)-1)]-s[i])*(t-i)
    return {'min': s[0], 'max': s[-1], 'range': s[-1]-s[0],
            'mean': mean(xs), 'population_sd': statistics.pstdev(xs),
            'q05': quantile(.05), 'median': quantile(.5), 'q95': quantile(.95),
            'unique_exact_saved_float_values': len(set(xs))}


def summary(rows):
    n = len(rows)
    ce = [r['ce'] for r in rows]
    ps = [math.exp(-r['ce']) for r in rows]
    ks = [len(r['option_ids']) for r in rows]
    dc = [c-math.log(k) for c, k in zip(ce, ks)]
    dp = [p-1/k for p, k in zip(ps, ks)]
    correct = [r['predicted_position'] == r['target_position'] for r in rows]
    return {
        'rows': n, 'agreements': sum(correct), 'agreement': sum(correct)/n,
        'ce_sum': math.fsum(ce), 'mean_ce': mean(ce),
        'stored_agreement_mismatches': sum(r['agreement'] != c for r, c in zip(rows, correct)),
        'predicted_position_counts': dict(collections.Counter(str(r['predicted_position']) for r in rows)),
        'target_position_counts': dict(collections.Counter(str(r['target_position']) for r in rows)),
        'ce': spread(ce), 'ce_derived_target_p': spread(ps),
        'baseline': {'mean_ce': mean([math.log(k) for k in ks]),
                     'mean_brier_sum_over_classes': mean([1-1/k for k in ks]),
                     'expected_random_agreements': math.fsum(1/k for k in ks),
                     'expected_random_agreement': mean([1/k for k in ks]),
                     'deterministic_first_tie_agreements': sum(r['target_position'] == 0 for r in rows),
                     'deterministic_first_tie_agreement': sum(r['target_position'] == 0 for r in rows)/n},
        'ce_minus_uniform': spread(dc), 'target_p_minus_uniform': spread(dp),
        'ce_exact_comparison_to_math_log_k': {'below': sum(x < 0 for x in dc), 'equal': sum(x == 0 for x in dc), 'above': sum(x > 0 for x in dc)},
        'target_p_exact_comparison_to_one_over_k': {'below': sum(x < 0 for x in dp), 'equal': sum(x == 0 for x in dp), 'above': sum(x > 0 for x in dp)},
        'ce_threshold_counts': {str(t): {'below_minus_threshold': sum(x < -t for x in dc), 'within_inclusive': sum(abs(x) <= t for x in dc), 'above_threshold': sum(x > t for x in dc)} for t in CE_THRESHOLDS},
        'target_p_threshold_counts': {str(t): {'below_minus_threshold': sum(x < -t for x in dp), 'within_inclusive': sum(abs(x) <= t for x in dp), 'above_threshold': sum(x > t for x in dp)} for t in P_THRESHOLDS},
        'conditional_strict_winner_certificate': {
            'target_p_gt_half_and_correct': sum(p > .5 and c for p, c in zip(ps, correct)),
            'target_p_gt_half_but_incorrect': sum(p > .5 and not c for p, c in zip(ps, correct)),
            'correct_without_this_certificate': sum(c and p <= .5 for p, c in zip(ps, correct))},
        'stored_ce_exactly_binary32_representable': sum(struct.unpack('f', struct.pack('f', c))[0] == c for c in ce),
        'actual_brier': None, 'actual_entropy': None, 'actual_top2_margin': None,
        'actual_tie_count': None,
    }


GROUPS = {
    'family': lambda r: r['family'],
    'target_position': lambda r: str(r['target_position']),
    'option_arity': lambda r: str(len(r['option_ids'])),
    'source': lambda r: r['source'],
    'source_group': lambda r: json.dumps([r['source'], r['group_id']]),
    'arity_target_position': lambda r: json.dumps([len(r['option_ids']), r['target_position']]),
}


def grouped(rows, key):
    buckets = collections.defaultdict(list)
    for r in rows:
        buckets[key(r)].append(r)
    return dict(sorted(buckets.items()))


def reconcile(actual, official, path, issues):
    for k, v in official.items():
        if k not in actual:
            issues.append({'path': path+'.'+k, 'error': 'missing recomputed field'})
        elif isinstance(v, dict):
            reconcile(actual[k], v, path+'.'+k, issues)
        elif isinstance(v, (int, float)):
            if not math.isclose(actual[k], v, rel_tol=0, abs_tol=RECONCILE_ATOL):
                issues.append({'path': path+'.'+k, 'actual': actual[k], 'official': v})
        elif actual[k] != v:
            issues.append({'path': path+'.'+k, 'actual': actual[k], 'official': v})
    if path.endswith('position_counts') and set(actual) != set(official):
        issues.append({'path': path, 'error': 'different count keys'})


def example(r):
    k = len(r['option_ids'])
    return {'train_id': r['id'], 'option_arity': k, 'target_position': r['target_position'],
            'predicted_position': r['predicted_position'], 'ce': r['ce'],
            'ce_derived_target_p': math.exp(-r['ce']), 'uniform_target_p': 1/k,
            'ce_minus_uniform': r['ce']-math.log(k)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT)
    out = parser.parse_args().output.resolve()
    if out != ROOT and ROOT not in out.parents:
        raise SystemExit('Output must be within authorized fit-audit directory')
    out.mkdir(parents=True, exist_ok=True)
    for name in ('report.json', 'report.md', 'SHA256SUMS'):
        if (out/name).exists():
            raise SystemExit('Refusing to overwrite '+str(out/name))
    raw = {k: p.read_bytes() for k, p in INPUTS.items()}
    provenance = {k: {'path': str(INPUTS[k]), 'sha256': sha(v), 'bytes': len(v)} for k, v in raw.items()}
    rows = {k: [json.loads(x) for x in raw[k].splitlines() if x.strip()] for k in ('before', 'after', 'schedule')}
    receipt = json.loads(raw['receipt'])
    # Schedule labels, identity and arity only; no prompts are interpreted or emitted.
    schedule = rows['schedule']
    if not all(len(v) == 1500 for v in rows.values()):
        raise ValueError('Expected exactly 1500 records in each input')
    if any(len({r['id'] for r in rs}) != 1500 for rs in rows.values()):
        raise ValueError('Duplicate TRAIN IDs')
    for i, s in enumerate(schedule):
        if s['index'] != i or s['decision']['id'] != s['id']:
            raise ValueError('Schedule identity mismatch')
        if [x['id'] for x in s['decision']['options']] != s['option_ids']:
            raise ValueError('Schedule option ordering mismatch')
        if s['option_ids'][s['target_position']] != s['target_id']:
            raise ValueError('Schedule label mismatch')
        for phase in ('before', 'after'):
            r = rows[phase][i]
            for key in ('id', 'index', 'family', 'group_id', 'option_ids', 'target_position'):
                if r[key] != s[key]:
                    raise ValueError('Join mismatch '+key)
            if r['source'] != s['provenance']['source']:
                raise ValueError('Source mismatch')
            if not (0 <= r['predicted_position'] < len(r['option_ids']) and math.isfinite(r['ce']) and r['ce'] >= 0):
                raise ValueError('Invalid saved fit fields')
    result = {
        'scope': 'Exactly 1500 paired saved TRAIN records; no inference, learning, source review or held-out data.',
        'inputs': provenance,
        'analyzer': {'path': str(Path(__file__).resolve()), 'sha256': sha(Path(__file__).read_bytes())},
        'thresholds_defined_before_computation': {'absolute_ce_nats': CE_THRESHOLDS, 'absolute_target_probability': P_THRESHOLDS, 'receipt_absolute_tolerance': RECONCILE_ATOL, 'purpose': 'Descriptive sensitivity summaries, not a tuned acceptance or selection criterion.'},
        'join': {'rows_per_file': 1500, 'unique_train_ids': 1500, 'ordered_identity_label_arity_source_matches': True,
                 'unique_schedule_prompt_hashes': len({s['prompt_token_sha256'] for s in schedule}),
                 'label_basis_counts': dict(collections.Counter(s['provenance'].get('label_basis') for s in schedule))},
        'limitations': [
            'Full probabilities and logits were not retained. Actual Brier, entropy, top-two margin and exact ties cannot be computed.',
            'Target p is approximately exp(-stored CE), conditional on the recorded unsmoothed categorical CE interpretation. It is not a separately retained probability.',
            'Stored decimal CE precision and binary32 representability do not establish precision or tiedness of unretained internal logits.',
            'Exact saved-float comparisons are arithmetic facts, not infinite-precision or internal-logit equality tests.',
            'Different target p from 1/k rules out exact uniformity for that row under the CE interpretation; equality would not prove full uniformity for k>2.',
            'No probabilities from different TRAIN records are combined into a reconstructed vector. Equal target p never implies equal non-target probabilities.',
            'Position-zero argmax alone does not prove ties. A correct argmax with target p > 0.5 certifies a strict winner under the CE interpretation, not the remaining tie count.',
            'TRAIN fit is descriptive agreement with saved labels, including teacher labels; not independent correctness, generalization, calibration or a causal account of performance/ranking.',
        ],
        'phases': {},
    }
    issues = []
    if sha(raw['schedule']) != receipt['identity']['schedule_sha256']:
        issues.append({'path': 'identity.schedule_sha256', 'error': 'hash mismatch'})
    for phase in ('before', 'after'):
        rs = rows[phase]
        block = {'overall': summary(rs), 'by_'+ 'family': {}}
        for name, key in GROUPS.items():
            block['by_'+name] = {k: summary(v) for k, v in grouped(rs, key).items()}
        for key, cell in block['by_arity_target_position'].items():
            ids = {r['id'] for r in rs if GROUPS['arity_target_position'](r) == key}
            cell['unique_input_prompt_hashes'] = len({s['prompt_token_sha256'] for s in schedule if s['id'] in ids})
        ordered = sorted(rs, key=lambda r: (r['ce']-math.log(len(r['option_ids'])), r['id']))
        block['record_examples_by_train_id_only'] = {'min_ce_minus_uniform': example(ordered[0]), 'max_ce_minus_uniform': example(ordered[-1]),
            'nearest_ce_to_uniform': example(min(rs, key=lambda r: (abs(r['ce']-math.log(len(r['option_ids']))), r['id']))),
            'first_correct_target_p_gt_half': next((example(r) for r in rs if r['predicted_position'] == r['target_position'] and math.exp(-r['ce']) > .5), None)}
        result['phases'][phase] = block
        official = receipt['fit_'+phase]
        if sha(raw[phase]) != official['rows_sha256']:
            issues.append({'path': 'fit_'+phase+'.rows_sha256', 'error': 'hash mismatch'})
        for key in ('overall', 'by_family', 'by_source_group'):
            reconcile(block[key], official[key], 'fit_'+phase+'.'+key, issues)
            if key != 'overall' and set(block[key]) != set(official[key]):
                issues.append({'path': 'fit_'+phase+'.'+key, 'error': 'different grouping keys'})
    before, after = rows['before'], rows['after']
    transitions = collections.Counter()
    for b, a in zip(before, after):
        transitions[('correct' if b['predicted_position'] == b['target_position'] else 'incorrect')+' -> '+('correct' if a['predicted_position'] == a['target_position'] else 'incorrect')] += 1
    result['paired'] = {'agreement_transitions': dict(transitions), 'ce_after_minus_before': spread([a['ce']-b['ce'] for b, a in zip(before, after)]),
                        'ce_decreased_rows': sum(a['ce'] < b['ce'] for b, a in zip(before, after)),
                        'ce_unchanged_rows': sum(a['ce'] == b['ce'] for b, a in zip(before, after)),
                        'ce_increased_rows': sum(a['ce'] > b['ce'] for b, a in zip(before, after))}
    result['receipt_reconciliation'] = {'status': 'match' if not issues else 'mismatch', 'issues': issues,
        'coverage': 'Input SHA256s, schedule SHA256, every official overall/family/source-group statistic; counts exact and numeric absolute tolerance 1e-10.',
        'official_fit_before_overall': receipt['fit_before']['overall'], 'official_fit_after_overall': receipt['fit_after']['overall'],
        'official_source_group_cells_per_phase': {p: len(receipt['fit_'+p]['by_source_group']) for p in ('before', 'after')},
        'online_mean_ce_not_same_estimand': receipt.get('online_mean_ce'),
        'note': 'Online mean CE describes a different recorded aggregate, not the paired frozen before/after fit. No optimizer or gradient implementation reviewed.'}
    (out/'report.json').write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n', encoding='utf-8')
    (out/'report.md').write_text(markdown(result), encoding='utf-8')
    files = [Path(__file__).resolve(), out/'report.json', out/'report.md']
    with (out/'SHA256SUMS').open('x', encoding='utf-8') as f:
        for p in files:
            f.write(sha(p.read_bytes())+'  '+str(p)+'\n')
        for entry in provenance.values():
            f.write(entry['sha256']+'  '+entry['path']+'\n')
    for p in files+[out/'SHA256SUMS']:
        p.chmod(0o444)
    print(json.dumps({'output': str(out), 'receipt_reconciliation': result['receipt_reconciliation']['status'], 'before': result['phases']['before']['overall']['mean_ce'], 'after': result['phases']['after']['overall']['mean_ce']}))


def markdown(r):
    b, a = (r['phases'][p]['overall'] for p in ('before', 'after'))
    base = b['baseline']
    lines = ['# D5 bounded TRAIN fit audit', '',
        '## Scope and method', '',
        'Exactly **1,500 paired TRAIN IDs**, each joined in order to the same schedule for identity, label, option ordering, arity and source. No frozen manifest/shard join was needed: the independently read schedule supplies every baseline label and arity. No protected data, weights, model execution, new learning, optimizer/gradient source, network, dependencies, Git, tests or lint were used.', '',
        'Thresholds were declared in `analyze.py` before computation: absolute CE deviations in nats = '+str(list(CE_THRESHOLDS))+'; absolute target-p deviations = '+str(list(P_THRESHOLDS))+'. All are descriptive, not tuned criteria. Exact comparisons use parsed stored floats against Python `math.log(k)` / `1/k`; threshold membership is inclusive. SD is population SD; quantiles use linear interpolation. All aggregates are record-weighted, not equal-weighted across groups.', '',
        'Agreement is recomputed as predicted_position == target_position, with zero-based positions. Brier uses the sum-over-classes convention. The uniform comparator is a mathematical same-schedule baseline, not generated model output. Random choice and deterministic first-tie choice are distinct comparators.', '',
        '## Overall results', '',
        '| Metric | Before | After | Same-schedule uniform baseline |',
        '|---|---:|---:|---:|',
        f"| Agreement | {b['agreements']}/1500 ({b['agreement']:.9%}) | {a['agreements']}/1500 ({a['agreement']:.9%}) | Random expected {base['expected_random_agreement']:.9%}; first-tie {base['deterministic_first_tie_agreement']:.9%} |",
        f"| Mean CE (nats) | {b['mean_ce']:.12f} | {a['mean_ce']:.12f} | {base['mean_ce']:.12f} |",
        f"| Mean CE − uniform | {b['ce_minus_uniform']['mean']:.12f} | {a['ce_minus_uniform']['mean']:.12f} | 0 |",
        f"| Mean CE-derived target p | {b['ce_derived_target_p']['mean']:.12f} | {a['ce_derived_target_p']['mean']:.12f} | {base['expected_random_agreement']:.12f} |",
        f"| Actual mean Brier | Missing vectors | Missing vectors | {base['mean_brier_sum_over_classes']:.12f} |", '',
        f"Stored agreement mismatch counts: before {b['stored_agreement_mismatches']}, after {a['stored_agreement_mismatches']}. Expected random agreement count is {base['expected_random_agreements']:.12f}; deterministic first-tie count is {base['deterministic_first_tie_agreements']}. These are not interchangeable.", '',
        f"Predicted-position counts: before `{json.dumps(b['predicted_position_counts'], sort_keys=True)}`; after `{json.dumps(a['predicted_position_counts'], sort_keys=True)}`. Target counts: `{json.dumps(a['target_position_counts'], sort_keys=True)}`.", '',
        'Paired transitions: `'+json.dumps(r['paired'], sort_keys=True)+'`.', '',
        '## Stratified agreement and CE', '',
        'Complete exact-source and all 880 (source, group_id) cells per phase, including each cell’s same-schedule baseline and CE/target-p statistics, are in `report.json`. Source-group means are descriptive, often based on few rows, not independent causal evidence. The tables below do not relabel or normalize source identities.', '']
    for group in ('family', 'option_arity', 'target_position'):
        lines += ['### '+group, '', '| Cell | n | Before agreement | After agreement | Before CE | After CE | Uniform CE | Random agreement | First-tie agreement |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for k, x in r['phases']['before']['by_'+group].items():
            y = r['phases']['after']['by_'+group][k]
            u = x['baseline']
            lines.append(f"| {k} | {x['rows']} | {x['agreement']:.6%} | {y['agreement']:.6%} | {x['mean_ce']:.9f} | {y['mean_ce']:.9f} | {u['mean_ce']:.9f} | {u['expected_random_agreement']:.6%} | {u['deterministic_first_tie_agreement']:.6%} |")
        lines.append('')
    lines += ['## Uniformity sensitivity and justified certificates', '']
    for phase in ('before', 'after'):
        x = r['phases'][phase]['overall']
        lines += ['### '+phase, '', 'Exact stored CE versus ln(k): `'+json.dumps(x['ce_exact_comparison_to_math_log_k'])+'`.',
            'CE-derived target p versus 1/k: `'+json.dumps(x['target_p_exact_comparison_to_one_over_k'])+'`.', '',
            '| Absolute CE threshold | Below −threshold | Within ±threshold (inclusive) | Above threshold |', '|---:|---:|---:|---:|']
        for t, c in x['ce_threshold_counts'].items():
            lines.append(f"| {t} | {c['below_minus_threshold']} | {c['within_inclusive']} | {c['above_threshold']} |")
        lines += ['', '| Absolute target-p threshold | Below −threshold | Within ±threshold (inclusive) | Above threshold |', '|---:|---:|---:|---:|']
        for t, c in x['target_p_threshold_counts'].items():
            lines.append(f"| {t} | {c['below_minus_threshold']} | {c['within_inclusive']} | {c['above_threshold']} |")
        lines += ['', 'Conditional strict-winner certificate counts: `'+json.dumps(x['conditional_strict_winner_certificate'])+'`.',
            f"CE values exactly representable as binary32: {x['stored_ce_exactly_binary32_representable']}/1500. This characterizes saved scalars only, not unretained logits.", '']
    lines += ['## Within-(arity, target position) across-input spread', '',
        'Each row of this table describes separate TRAIN inputs, never entries of one reconstructed probability vector. Unique counts are exact parsed CE / CE-derived-p float counts, not rounded bins. Input counts use the schedule’s prompt hashes. Full means, SDs and quantiles are in JSON.', '',
        '| Phase | [k, target position] | n / unique inputs | CE min … max | CE SD | Unique CE / p | Target-p min … max | Target-p SD |', '|---|---|---:|---:|---:|---:|---:|---:|']
    for phase in ('before', 'after'):
        for k, x in r['phases'][phase]['by_arity_target_position'].items():
            c, p = x['ce'], x['ce_derived_target_p']
            lines.append(f"| {phase} | {k} | {x['rows']} / {x['unique_input_prompt_hashes']} | {c['min']:.12g} … {c['max']:.12g} | {c['population_sd']:.9g} | {c['unique_exact_saved_float_values']} / {p['unique_exact_saved_float_values']} | {p['min']:.12g} … {p['max']:.12g} | {p['population_sd']:.9g} |")
    lines += ['', '## Actual-record examples (TRAIN ID only)', '', 'The examples are deterministically selected extrema, closest-to-uniform CE, and first strict-winner certificate; they are not additional model outputs. No question, context or option text is reproduced.', '']
    for phase in ('before', 'after'):
        lines += ['### '+phase, '', '```json', json.dumps(r['phases'][phase]['record_examples_by_train_id_only'], indent=2), '```', '']
    lines += ['## Official receipt reconciliation', '',
        '**'+r['receipt_reconciliation']['status'].upper()+'**: both fit-row hashes and the schedule hash match the official receipt. Every official overall, family and source-group statistic was recomputed. Integer counts are exact; numeric comparisons use absolute tolerance 1e-10.', '',
        'Issues: `'+json.dumps(r['receipt_reconciliation']['issues'])+'`. Official online mean CE = '+str(r['receipt_reconciliation']['online_mean_ce_not_same_estimand'])+'; it is not the same aggregate as either frozen fit pass. No implementation-level cause is inferred.', '',
        '## Scientifically bounded conclusion', '',
        f"The recorded agreement changes from {b['agreement']:.6%} to {a['agreement']:.6%}; mean CE changes from {b['mean_ce']:.9f} to {a['mean_ce']:.9f}. All 1500 after rows select position zero, which numerically matches the deterministic first-choice baseline’s agreement on this schedule. This does **not** establish tied logits or uniform probability vectors. The CE-derived target probabilities and per-cell variation must be assessed separately from the argmax positions.", '',
        'Under unsmoothed categorical CE, target p ≈ exp(−CE). A target p differing materially from 1/k rules out an exactly uniform vector for that row, subject to stored-CE precision. A correct target with p > 0.5 is necessarily a strict winner because all non-target mass sums to less than p. Neither statement identifies other probabilities. No all-non-target-equal assumption or cross-record vector reconstruction is used.', '',
        '**Unresolved evidence gap:** actual Brier, entropy, top-two margin and exact tie counts require the missing vectors/logits. The strict-winner certificates provide only a lower bound on strict winners, not a count of ties among the remaining rows. First-position argmax is not evidence of ties by itself. Saved decimal digits and observed binary32 representability do not expose internal-logit precision. This audit makes no generalization, causal, ranking-quality or calibration claim.', '',
        '## Provenance and reproduction', '',
        'Inputs and output files are SHA-256-addressed below / in `SHA256SUMS`; the local deliverables are set read-only (not an append-only or external authenticity guarantee). Input contents are not modified. `analyze.py` refuses to overwrite reports and permits output only inside the authorized audit directory. Reproduce with stdlib Python into a fresh child directory:', '',
        '```sh', 'python3 '+str(ROOT/'analyze.py')+' --output '+str(ROOT/'reproduction-new'), '```', '',
        '| Input | Bytes | SHA-256 |', '|---|---:|---|']
    for k, e in r['inputs'].items():
        lines.append(f"| {k}: `{e['path']}` | {e['bytes']} | `{e['sha256']}` |")
    lines += ['', 'Analyzer SHA-256: `'+r['analyzer']['sha256']+'`.', '',
        'All detailed limitations:', *['- '+x for x in r['limitations']], '']
    return '\n'.join(lines)


if __name__ == '__main__':
    main()
