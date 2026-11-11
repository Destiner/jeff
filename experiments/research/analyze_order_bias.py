#!/usr/bin/env python3
"""R6 frozen, stdlib-only descriptive analysis. Run bind, then analyze once."""
import argparse
import sys
import os
import json
import math
import hashlib
import platform
import datetime
from pathlib import Path
from collections import defaultdict, Counter

HERE = ROOT = PUBLIC = PRE = METHOD = None
FIELDS = 'case_id task_family source_group domain policy_instance mechanism producer construction_cluster K option_ids original_p reversed_p original_positions reversed_positions'.split()
UNITS = 'source_group domain policy_instance mechanism producer construction_cluster'.split()
EXPECTED = {'paired.jsonl': 'ca9d0f47401b753be87ef9c12648c771ef62783d1f8e646af89e1b55404f792d', 'receipt.json': '1b312883376325a045c27ff691e949c5ba3260f8fde29600461373f1f70f948e'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(name, obj):
    with (HERE / name).open('x') as f:
        json.dump(obj, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')

def rows():
    return [json.loads(line) for line in (PUBLIC / 'paired.jsonl').read_text().splitlines()]

def broad(r):
    field = 'domain' if r['task_family'] in ('intent', 'sentiment') else 'mechanism'
    return r[field] or r['source_group'] or 'unknown'

def inventory(rs):
    return {'cases': len(rs), 'options': sum(r['K'] for r in rs), 'families': dict(Counter(r['task_family'] for r in rs)), 'K': dict(Counter(str(r['K']) for r in rs)), 'units': {u: {'observed': len({r[u] for r in rs if r[u] is not None}), 'null_rows': sum(r[u] is None for r in rs)} for u in UNITS}, 'producer_broad_groups': len({(r['producer'], broad(r)) for r in rs})}

def bind():
    assert not (HERE / 'input-binding.json').exists()
    hashes = {str(p): sha(p) for p in [PRE, METHOD, Path(__file__).resolve()] + [PUBLIC / n for n in ['README.md', 'receipt.json', 'delivery.json', 'paired.jsonl']]}
    for n, h in EXPECTED.items():
        assert hashes[str(PUBLIC / n)] == h, n
    rs = rows()  # Metadata only here: probability arrays are not inspected.
    assert len(rs) == 240 and len({r['case_id'] for r in rs}) == 240
    assert all(set(r) == set(FIELDS) for r in rs)
    families = defaultdict(set)
    nesting = {u: defaultdict(set) for u in UNITS if u != 'producer'}
    for r in rs:
        assert r['construction_cluster'] == r['producer']
        families[r['producer']].add(r['task_family'])
        for u in nesting:
            if r[u] is not None:
                nesting[u][r[u]].add(r['producer'])
    assert len(families) == 6 and all(len(v) == 1 for v in families.values())
    assert all(len(v) == 1 for d in nesting.values() for v in d.values())
    split = {}
    for family in sorted({r['task_family'] for r in rs}):
        ps = sorted({r['producer'] for r in rs if r['task_family'] == family}, key=lambda p: hashlib.sha256(('R6/source-split/v1\n' + family + '\n' + p).encode()).hexdigest())
        assert len(ps) == 2
        for i, p in enumerate(ps):
            subset = [r for r in rs if r['producer'] == p]
            split[p] = {'family': family, 'partition': 'FIT' if i < math.ceil(len(ps)/2) else 'HOLDOUT', 'split_digest': hashlib.sha256(('R6/source-split/v1\n' + family + '\n' + p).encode()).hexdigest(), 'inventory': inventory(subset)}
    binding = {'version': 'R6/saved-analysis/1', 'frozen_utc': now(), 'hash_scope': 'Exact bytes of script, primary predeclaration, supporting method and four permitted public files; no upstream files accessed.', 'sha256': hashes, 'field_roles': {'identity': 'case_id and per-case option_ids', 'family': 'task_family', 'source': 'producer; construction_cluster must equal producer', 'broad_group': 'domain for intent/sentiment; mechanism for rule_application; fallback source_group then explicit unknown', 'other_observed_units': UNITS, 'K': 'number of options, 2..6', 'probabilities': 'original_p/reversed_p aligned to original option_ids, raw saved binary64 values', 'positions': 'original_positions/reversed_positions, ONE-based slots of those same identities; exact reversal'}, 'partition': split, 'case_metadata': [{k: r[k] for k in FIELDS if k not in ('original_p', 'reversed_p')} | {'broad_group': broad(r)} for r in sorted(rs, key=lambda r: r['case_id'])], 'inventory': inventory(rs), 'estimator': 'One gamma[K] across all FIT producers: per K equal producer, equal broad group within producer, equal eligible rows within group, options 1/K. Center log(original)-log(reverse) per case then average mirror contrast (y[j]-y[K-1-j])/2. No epsilon, second model, alternate split, family fit, or outcome-driven revision.', 'eligibility': 'All valid raw pairs retained in descriptives; sums within 1e-6, no normalization. Log fits require every p>0 in both orders. Fail on malformed input, retain failed artifacts.', 'summaries': 'Per-K source/group-balanced heldout metrics; macro supported K equally. Per-source/K metrics rebalance groups within source. Case RMS quantiles are unweighted linear-interpolated descriptive quantiles. Probability descriptives unweighted rows within each displayed stratum; tied cases excluded from unique-argmax transitions. TV uses raw sums, only modeled softmax normalizes.', 'manual_review': 'Full script read before binding; checked original-identity alignment, ONE-based reversal mapping, source split/nesting, hierarchical weights, centered mirror fit, bidirectional predictions, raw TV and zero handling. No outcome statistics inspected before freeze.', 'commands': [f'{sys.executable} -I -S {Path(__file__).resolve()} {phase} --task-root {ROOT} --output-dir {HERE}' for phase in ('bind', 'analyze')], 'python': sys.version, 'platform': platform.platform(), 'precedence': 'Primary predeclaration overrides method epsilon sensitivity, alternate split, or second learned model. No TRAIN diagnostic executed.'}
    save('input-binding.json', binding)
    os.chmod(HERE / 'input-binding.json', 0o444)
    os.chmod(Path(__file__), 0o444)
    print('Frozen binding:', sha(HERE / 'input-binding.json'))

def fmt(value):
    return 'undefined' if value is None else f'{value:.6f}'

def avg(xs):
    return math.fsum(xs) / len(xs) if xs else None

def tv(a, b):
    return math.fsum(abs(x-y) for x, y in zip(a, b))/2

def slotvec(r, field, positions):
    out = [None] * r['K']
    for p, j in zip(r[field], r[positions]):
        out[j-1] = p
    return out

def winner(p):
    m = max(p)
    hits = [i for i, v in enumerate(p) if v == m]
    return hits[0] if len(hits) == 1 else None

def describe(rs):
    byk = {}
    for k in sorted({r['K'] for r in rs}):
        sub = [r for r in rs if r['K'] == k]
        identity = [[0]*k for _ in range(k)]
        slots = [[0]*k for _ in range(k)]
        kept_i = kept_s = eligible = 0
        per_order = {}
        for field, pos in [('original_p', 'original_positions'), ('reversed_p', 'reversed_positions')]:
            vs = [slotvec(r, field, pos) for r in sub]
            ws = [winner(v) for v in vs]
            per_order[field] = {'mean_p_by_slot_1_based': [avg([v[j] for v in vs]) for j in range(k)], 'unique_winners_by_slot_1_based': [ws.count(j) for j in range(k)], 'tied_argmax_vectors': ws.count(None)}
        for r in sub:
            a, b = winner(r['original_p']), winner(r['reversed_p'])
            if a is not None and b is not None:
                eligible += 1
                ja, jb = r['original_positions'][a]-1, r['reversed_positions'][b]-1
                ia, ib = r['original_positions'][a]-1, r['original_positions'][b]-1
                identity[ia][ib] += 1
                slots[ja][jb] += 1
                kept_i += a == b
                kept_s += ja == jb
        byk[str(k)] = {'pairs': len(sub), 'strict_unique_pairs': eligible, 'identity_retained': kept_i, 'letter_slot_retained': kept_s, 'identity_retention_rate': kept_i/eligible if eligible else None, 'letter_slot_retention_rate': kept_s/eligible if eligible else None, 'identity_transition_original_slot_rank_to_original_slot_rank': identity, 'letter_slot_transition_original_to_reversed': slots, 'orders': per_order}
    return {'inventory': inventory(rs), 'mean_TV_option_identity': avg([tv(r['original_p'], r['reversed_p']) for r in rs]), 'mean_TV_displayed_slot': avg([tv(slotvec(r, 'original_p', 'original_positions'), slotvec(r, 'reversed_p', 'reversed_positions')) for r in rs]), 'zero_entries': sum(p == 0 for r in rs for f in ('original_p', 'reversed_p') for p in r[f]), 'one_entries': sum(p == 1 for r in rs for f in ('original_p', 'reversed_p') for p in r[f]), 'zero_containing_pairs': sum(any(p == 0 for f in ('original_p', 'reversed_p') for p in r[f]) for r in rs), 'K': byk}

def weights(rs):
    groups = defaultdict(lambda: defaultdict(list))
    for r in rs:
        groups[r['producer']][broad(r)].append(r)
    return [(r, 1/len(groups)/len(gs)/len(gr)) for gs in groups.values() for gr in gs.values() for r in gr]

def quantile(xs, q):
    xs = sorted(xs)
    z = (len(xs)-1)*q
    i = int(z)
    return xs[i] + (xs[min(i+1, len(xs)-1)]-xs[i])*(z-i)

def softmax(logits):
    m = max(logits)
    es = [math.exp(v-m) for v in logits]
    total = math.fsum(es)
    return [v/total for v in es]

def metrics(rs, gamma):
    k = len(gamma)
    sse = zero = mae = sym = anti = 0.0
    signed = [0.0]*k
    tvs = {'modeled': 0.0, 'semantic_copy': 0.0, 'static_slot_copy': 0.0}
    directional = {'reverse_from_original': 0.0, 'original_from_reverse': 0.0}
    rms = []
    for r, w in weights(rs):
        y = r['_y']
        e = [a-b for a, b in zip(y, gamma)]
        energy = math.fsum(v*v for v in e)/k
        sse += w*energy
        zero += w*math.fsum(v*v for v in y)/k
        mae += w*math.fsum(abs(v) for v in e)/k
        sym += w*math.fsum(((y[j]+y[k-1-j])/2)**2 for j in range(k))/k
        anti += w*math.fsum(((y[j]-y[k-1-j])/2)**2 for j in range(k))/k
        for j in range(k):
            signed[j] += w*e[j]
        rms.append(math.sqrt(energy))
        a = slotvec(r, 'original_p', 'original_positions')
        b = slotvec(r, 'reversed_p', 'original_positions')
        pred_b = softmax([math.log(p)-g for p, g in zip(a, gamma)])
        pred_a = softmax([math.log(p)+g for p, g in zip(b, gamma)])
        fwd, back = tv(pred_b, b), tv(pred_a, a)
        directional['reverse_from_original'] += w*fwd
        directional['original_from_reverse'] += w*back
        tvs['modeled'] += w*(fwd+back)/2
        tvs['semantic_copy'] += w*tv(a, b)
        tvs['static_slot_copy'] += w*(tv(list(reversed(a)), b)+tv(list(reversed(b)), a))/2
    return {'support': inventory(rs), 'centered_log_RMSE': math.sqrt(sse), 'centered_log_MAE': mae, 'signed_residual_by_slot_1_based': signed, 'balanced_mean_squared_residual': sse, 'balanced_zero_baseline_energy': zero, 'SSE_reduction_vs_zero': 1-sse/zero if zero else None, 'observed_mirror_symmetric_energy': sym, 'observed_mirror_antisymmetric_energy': anti, 'observed_symmetric_energy_fraction': sym/zero if zero else None, 'case_RMS_unweighted_quantiles': {str(q): quantile(rms, q) for q in (0, .5, .9, 1)}, 'bidirectional_mean_TV': tvs, 'directional_modeled_TV': directional}

def analyze():
    binding = json.loads((HERE / 'input-binding.json').read_text())
    for p, h in binding['sha256'].items():
        assert sha(Path(p)) == h, p
    assert not (HERE / 'results.json').exists() and not (HERE / 'report.md').exists(), 'No rerun'
    start = now()
    import time
    cpu_start = time.process_time()
    rs = rows()
    errors = []
    sum_errors = []
    for r in rs:
        try:
            k = r['K']
            assert set(r) == set(FIELDS) and isinstance(k, int) and 2 <= k <= 6
            assert len(r['option_ids']) == k and len(set(r['option_ids'])) == k
            a, b = r['original_positions'], r['reversed_positions']
            assert sorted(a) == sorted(b) == list(range(1, k+1))
            assert all(x+y == k+1 for x, y in zip(a, b))
            for f in ('original_p', 'reversed_p'):
                ps = r[f]
                assert len(ps) == k and all(isinstance(v, (float, int)) and math.isfinite(v) and 0 <= v <= 1 for v in ps)
                error = abs(math.fsum(ps)-1)
                sum_errors.append(error)
                assert error <= 1e-6
        except (AssertionError, TypeError, ValueError):
            errors.append(r.get('case_id'))
    if errors:
        save('results.json', {'status': 'failed_validation', 'malformed_case_ids': errors, 'started_utc': start})
        raise ValueError('Malformed input; failed results preserved, no fitting')
    # Descriptive summaries include all valid pairs, including exact zeros.
    desc = {'all': describe(rs), 'family': {}, 'available_units': {}}
    for family in sorted({r['task_family'] for r in rs}):
        desc['family'][family] = describe([r for r in rs if r['task_family'] == family])
    for u in UNITS:
        desc['available_units'][u] = {str(v): describe([r for r in rs if r[u] == v]) for v in sorted({r[u] for r in rs if r[u] is not None})}
    eligible = []
    excluded = []
    for r in rs:
        if any(p == 0 for f in ('original_p', 'reversed_p') for p in r[f]):
            excluded.append(r)
            continue
        d = [math.log(a)-math.log(b) for a, b in zip(slotvec(r, 'original_p', 'original_positions'), slotvec(r, 'reversed_p', 'original_positions'))]
        center = math.fsum(d)/r['K']
        r['_y'] = [v-center for v in d]
        eligible.append(r)
    fit = [r for r in eligible if binding['partition'][r['producer']]['partition'] == 'FIT']
    hold = [r for r in eligible if binding['partition'][r['producer']]['partition'] == 'HOLDOUT']
    fits = {}
    held = {}
    for k in sorted({r['K'] for r in fit}):
        sub = [r for r in fit if r['K'] == k]
        g = [0.0]*k
        for j in range(k//2):
            g[j] = math.fsum(w*(r['_y'][j]-r['_y'][k-1-j])/2 for r, w in weights(sub))
            g[k-1-j] = -g[j]
        fits[str(k)] = {'gamma_natural_log_mirror_contrast_by_slot_1_based': g, 'support': inventory(sub), 'source_support': {p: inventory([r for r in sub if r['producer'] == p]) for p in sorted({r['producer'] for r in sub})}}
        subh = [r for r in hold if r['K'] == k]
        if subh:
            held[str(k)] = metrics(subh, g)
    bysource = {}
    for p in sorted({r['producer'] for r in hold}):
        bysource[p] = {'family': binding['partition'][p]['family'], 'K': {str(k): metrics([r for r in hold if r['producer'] == p and r['K'] == k], fits[str(k)]['gamma_natural_log_mirror_contrast_by_slot_1_based']) for k in sorted({r['K'] for r in hold if r['producer'] == p}) if str(k) in fits}}
    unsupported = [r for r in hold if str(r['K']) not in fits]
    macro = {}
    if held:
        for key in ('centered_log_RMSE', 'centered_log_MAE', 'SSE_reduction_vs_zero', 'observed_mirror_symmetric_energy', 'observed_symmetric_energy_fraction'):
            macro[key] = avg([m[key] for m in held.values() if m[key] is not None])
        macro['bidirectional_mean_TV'] = {key: avg([m['bidirectional_mean_TV'][key] for m in held.values()]) for key in ('modeled', 'semantic_copy', 'static_slot_copy')}
    out = {'status': 'complete', 'started_utc': start, 'completed_utc': now(), 'analysis_CPU_seconds': time.process_time()-cpu_start, 'binding_sha256': sha(HERE / 'input-binding.json'), 'script_sha256': sha(Path(__file__)), 'malformed_pairs': 0, 'raw_sum_error': {'maximum_absolute': max(sum_errors), 'mean_absolute': avg(sum_errors), 'nonzero_vectors': sum(e != 0 for e in sum_errors)}, 'descriptives': desc, 'log_coverage': {'eligible': inventory(eligible), 'excluded_zero_pairs': inventory(excluded), 'FIT': inventory(fit), 'HOLDOUT': inventory(hold), 'unsupported_heldout_K': sorted({r['K'] for r in unsupported}), 'unsupported_heldout_support': inventory(unsupported)}, 'fits': fits, 'heldout_by_K': held, 'heldout_by_source': bysource, 'heldout_equal_K_macro': macro}
    save('results.json', out)
    lines = ['# R6 saved paired-output analysis v1', '', 'Actual stdlib-only CPU analysis of 240 NEW-v2 frozen P3 pairs; no inference or learning.', '', '## Full-population descriptives', '', '| K | pairs | strict unique pairs | identity retained | letter/slot retained |', '|---|---:|---:|---:|---:|']
    for k, m in desc['all']['K'].items():
        lines.append(f"| {k} | {m['pairs']} | {m['strict_unique_pairs']} | {m['identity_retained']} | {m['letter_slot_retained']} |")
    lines += ['', f"Raw mean TV: option identity **{desc['all']['mean_TV_option_identity']:.6f}**; displayed slot **{desc['all']['mean_TV_displayed_slot']:.6f}**.", f"Exact zeros: {desc['all']['zero_entries']}; exact ones: {desc['all']['one_entries']}. Malformed pairs: 0. Max raw probability-sum error: {max(sum_errors):.12g}; {sum(e != 0 for e in sum_errors)}/480 vectors have nonzero last-rounding error. No renormalization of observed probabilities; raw TV may inherit last-rounding differences. Ties and full transitions, per-slot means/winners, family/K and every available nonnull unit/K are in results.json. Identity transition coordinates are original-slot ranks of semantic identities; slot transitions use displayed positions. Tied argmax cases are excluded only from strict retention/transitions; per-order tied counts are separate.", '', '## One shared FIT gamma per K', '', 'Units: natural-log mirror contrasts, gamma[j] = b[j] - b[mirror(j)], not complete b (antisymmetric b is gamma/2). Slot arrays below are ONE-based in order. Equal producer, then broad group, then rows within each K; positive-support eligibility only. All related groups stay with their producer.']
    for k, f in fits.items():
        lines.append(f"- K={k}: gamma={f['gamma_natural_log_mirror_contrast_by_slot_1_based']}; {f['support']['cases']} cases / {f['support']['units']['producer']['observed']} producers / {f['support']['producer_broad_groups']} broad groups.")
    lines += ['', '## Source-heldout descriptive fidelity', '', '| K | cases | RMSE | MAE | SSE reduction vs zero | symmetric observed energy fraction | TV model | TV semantic copy | TV static slot copy |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for k, m in held.items():
        t = m['bidirectional_mean_TV']
        lines.append(f"| {k} | {m['support']['cases']} | {m['centered_log_RMSE']:.6f} | {m['centered_log_MAE']:.6f} | {fmt(m['SSE_reduction_vs_zero'])} | {fmt(m['observed_symmetric_energy_fraction'])} | {t['modeled']:.6f} | {t['semantic_copy']:.6f} | {t['static_slot_copy']:.6f} |")
    lines += ['', f"Unsupported heldout K: {out['log_coverage']['unsupported_heldout_K']}; unscored cases: {len(unsupported)}. Zero-excluded cases: {len(excluded)}. Per-K metrics balance producers/groups/rows; macro in results.json gives supported K equal weight and averages per-K metrics (not pooled RMSE). Observed symmetric and antisymmetric energies sum to zero-baseline centered-y energy; symmetric energy is not removed before residual scoring. TV predictions use both directions, normalizing only modeled softmax. Semantic-copy and slot-copy comparators have no fitted parameters.", '', '### Heldout sources individually']
    for p, item in bysource.items():
        lines.append(f"\n- `{p}` ({item['family']}):")
        for k, m in item['K'].items():
            lines.append(f"  - K={k}, n={m['support']['cases']}, broad groups={m['support']['producer_broad_groups']}: RMSE={m['centered_log_RMSE']:.6f}, MAE={m['centered_log_MAE']:.6f}, SSE reduction={fmt(m['SSE_reduction_vs_zero'])}; signed residual slots={m['signed_residual_by_slot_1_based']}; case RMS median/p90={m['case_RMS_unweighted_quantiles']['0.5']:.6f}/{m['case_RMS_unweighted_quantiles']['0.9']:.6f}; bidirectional TV={m['bidirectional_mean_TV']}.")
    lines += ['', '## Interpretation and limits', '', 'This measures fidelity of one static mirror-antisymmetric account, not correctness, calibration, a deployed correction, or a causal mechanism. Label and slot are confounded; mirror-symmetric bias is unidentified. Residuals can include content/order changes and other violations. The three heldout producers are observed construction units, not independent samples: shared teacher/renderer dependence remains. Numerous cases/groups/options do not establish independence. Odd-middle retention can satisfy both coordinate systems. No pass threshold, p-values, intervals, alternate fit/split, epsilon sensitivity, second model, or TRAIN diagnostic was used.', '', '## Reproducibility and freeze', '', f"Frozen binding: `{out['binding_sha256']}`. Script: `{out['script_sha256']}`. Exact byte-hash scope and all metadata memberships/split are in input-binding.json; no upstream raw/private files read. Primary predeclaration outranks supporting method. Code manually reviewed in full before binding; metadata-only binding step precedes all probability statistics. Code and binding made read-only before probability statistics. No outcome-driven rewrites or refits.", '', f"Python: `{sys.version}`; platform: `{platform.platform()}`.", '', 'Actual commands (bind first, then analyze once):', '```sh', *binding['commands'], '```', f"Analysis start/end UTC: {start} / {out['completed_utc']}; CPU seconds for validation/descriptives/fitting: {out['analysis_CPU_seconds']:.6f}. No ML imports/loads, dependencies, paid work, tests/lint, tracked edits, commits, merges or mailbox. All work synchronous; no jobs remain."]
    with (HERE / 'report.md').open('x') as f:
        f.write('\n'.join(lines)+'\n')
    print(json.dumps({'macro': macro, 'descriptive_TV': {k: desc['all'][k] for k in ('mean_TV_option_identity', 'mean_TV_displayed_slot')}, 'results_sha256': sha(HERE / 'results.json'), 'CPU_seconds': out['analysis_CPU_seconds']}, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('bind', 'analyze'))
    parser.add_argument('--task-root', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args()
    ROOT = args.task_root.resolve(strict=True)
    HERE = args.output_dir.resolve()
    PUBLIC = ROOT.parents[1] / 'evaluation/r6-new-v2-probabilities-v1/public'
    PRE = ROOT / 'analysis-predeclaration-v1.md'
    METHOD = ROOT / 'method/findings.md'
    if args.command == 'bind':
        HERE.mkdir(parents=True, exist_ok=False)
    else:
        assert HERE.is_dir()
    {'bind': bind, 'analyze': analyze}[args.command]()
