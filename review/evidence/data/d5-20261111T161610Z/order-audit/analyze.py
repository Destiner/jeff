#!/usr/bin/env python3
"""Bounded TRAIN ordering audit; stdlib only, no loss or model analysis."""
import collections as C
import hashlib
import json
from pathlib import Path

BASE = Path('/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01')
OUT = Path(__file__).resolve().parent
PATHS = {k: BASE / v for k, v in {'schedule': 'train-audit/schedule.jsonl', 'online': 'training/online.jsonl', 'receipt': 'training/receipt.json', 'freeze': 'full-run-freeze.json'}.items()}
def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')
def counts(xs):
    return dict(sorted(C.Counter(xs).items()))
def runs(xs):
    result = []
    for i, x in enumerate(xs):
        if not result or result[-1]['value'] != x:
            result.append(dict(value=x, start=i, end=i, length=1))
        else:
            result[-1]['end'] = i
            result[-1]['length'] += 1
    return result

def main():
    raw = {k: p.read_bytes() for k, p in PATHS.items()}
    hashes = {k: dict(path=str(PATHS[k]), sha256=hashlib.sha256(v).hexdigest(), bytes=len(v)) for k, v in raw.items()}
    rows = [json.loads(x) for x in raw['schedule'].splitlines() if x.strip()]
    # Deliberately discard every online field except schedule/update identity.
    online = [{k: x[k] for k in ('id', 'index', 'update')} for x in map(json.loads, raw['online'].splitlines())]
    receipt = json.loads(raw['receipt'])
    freeze = json.loads(raw['freeze'])
    checks = dict(schedule_rows=len(rows), online_rows=len(online), unique_ids=len({x['id'] for x in rows}),
                  indices_in_file_order=[x['index'] for x in rows] == list(range(1500)),
                  online_identity_in_order=[(x['id'], x['index']) for x in online] == [(x['id'], x['index']) for x in rows],
                  online_update_formula=all(x['update'] == i // 4 + 1 for i, x in enumerate(online)),
                  online_update_sizes=counts(C.Counter(x['update'] for x in online).values()),
                  receipt_presentations=receipt['presentations'], receipt_updates=receipt['optimizer_steps'], receipt_status=receipt['status'],
                  schedule_matches_freeze=hashes['schedule']['sha256'] == freeze['schedule_sha256'],
                  online_matches_receipt=hashes['online']['sha256'] == receipt['online_rows_sha256'])
    if not (len(rows) == len(online) == 1500 and checks['indices_in_file_order'] and checks['online_identity_in_order'] and checks['online_update_formula']):
        raise ValueError('Identity/order mismatch; stop rather than infer actual order')
    dims = {'family': [x['family'] for x in rows], 'source_group': [':'.join(x['group_id'].split(':')[:3]) for x in rows],
            'source': [x['provenance']['source'] for x in rows], 'group_id': [x['group_id'] for x in rows]}
    run_evidence = {k: runs(v) for k, v in dims.items()}
    stats = {}
    for k, xs in dims.items():
        rr = run_evidence[k]
        by = {}
        for value in sorted(set(xs)):
            pos = [i for i, x in enumerate(xs) if x == value]
            vr = [r for r in rr if r['value'] == value]
            mx = max(r['length'] for r in vr)
            by[value] = dict(count=len(pos), first=pos[0], last=pos[-1], runs=len(vr), max_run=mx,
                             max_locations=[[r['start'], r['end']] for r in vr if r['length'] == mx])
        transitions = C.Counter(zip(xs, xs[1:]))
        stats[k] = dict(values=by, runs=len(rr), changes=len(rr)-1, same_adjacent=len(xs)-len(rr),
                        run_length_histogram=counts(r['length'] for r in rr),
                        maximum=max(r['length'] for r in rr),
                        transition_counts=[dict(from_value=a, to_value=b, count=n) for (a,b),n in sorted(transitions.items())])
    windows = []
    for n in (100,250,500):
        windows.extend([(f'prefix{n}',0,n), (f'suffix{n}',1500-n,1500)])
    windows.extend((f'decile{i+1}',i*150,(i+1)*150) for i in range(10))
    window_counts = [dict(name=name,start=a,end=b-1,counts={k:{v: dims[k][a:b].count(v) for v in sorted(set(dims[k]))} for k in ('family','source_group','source')}) for name,a,b in windows]
    updates=[]
    for u in range(375):
        a,b=u*4,u*4+4
        cc={k:counts(v[a:b]) for k,v in dims.items()}
        updates.append(dict(update=u+1,start=a,end=b-1,ids=[x['id'] for x in rows[a:b]],counts=cc,
                            family_sequence=dims['family'][a:b],source_group_sequence=dims['source_group'][a:b],
                            group_sequence=dims['group_id'][a:b],repeated_groups={g:n for g,n in cc['group_id'].items() if n>1}))
    groups=[]
    for g, s in stats['group_id']['values'].items():
        pos=[i for i,v in enumerate(dims['group_id']) if v==g]
        kind='singleton scenario' if s['count']==1 else ('rule mechanism group (repeated presentations)' if dims['family'][pos[0]]=='rule_application' else 'repeated non-rule group; mechanism semantics not inferred')
        groups.append(dict(group_id=g,kind=kind,indices=pos,updates=sorted({i//4+1 for i in pos}),**s))
    mix = dict(family_distinct=counts(len(u['counts']['family']) for u in updates),
               family_count_patterns=counts('+'.join(map(str,sorted(u['counts']['family'].values(),reverse=True))) for u in updates),
               group_distinct=counts(len(u['counts']['group_id']) for u in updates),
               source_group_distinct=counts(len(u['counts']['source_group']) for u in updates),
               updates_with_repeated_group=[u['update'] for u in updates if u['repeated_groups']],
               repeated_group_excess_presentations=sum(sum(n-1 for n in u['repeated_groups'].values()) for u in updates),
               family_compositions=counts(json.dumps(u['counts']['family'],sort_keys=True) for u in updates))
    aliases=[]
    for source in sorted(set(dims['source'])):
        pos=[i for i,v in enumerate(dims['source']) if v==source]
        aliases.append(dict(source=source,source_groups=sorted({dims['source_group'][i] for i in pos}),families=sorted({dims['family'][i] for i in pos}),count=len(pos)))
    dump('summary.json',dict(inputs=hashes,checks=checks,dimensions=stats,update_mixtures=mix,group_size_histogram=counts(g['count'] for g in groups)))
    dump('runs.json',run_evidence)
    dump('windows.json',window_counts)
    dump('updates.json',updates)
    dump('groups.json',groups)
    dump('source-aliases.json',aliases)
    lines=['# D5 TRAIN presentation-order audit','',
           'Scope: recorded 1,500 TRAIN presentations and 375 consecutive four-presentation updates only. No loss values, optimizer/gradient analysis, other splits, model execution, or causal inference. Indices below are zero-based and endpoints inclusive; updates are one-based.', '',
           '## Identity and pins', '',
           f'All schedule indices are 0–1499 in file order: {checks["indices_in_file_order"]}. All online IDs/indices match position-for-position: {checks["online_identity_in_order"]}. Every online update equals floor(index/4)+1: {checks["online_update_formula"]}; 375 updates each have four rows. Receipt reports {checks["receipt_presentations"]} presentations / {checks["receipt_updates"]} updates, status `{checks["receipt_status"]}`. Schedule matches frozen SHA-256; online bytes match receipt SHA-256.', '',
           'The recorded order is analyzed directly, not reconstructed from manifest order. Interleaving is observed; no claim is made about how the pinned permutation was generated or whether it is random.', '',
           '## Family exposure', '', '| Family | Count | First–last | Runs | Maximum run: index range(s) |','|---|---:|---|---:|---|']
    for v,s in stats['family']['values'].items():
        lines.append(f'| {v} | {s["count"]} | {s["first"]}–{s["last"]} | {s["runs"]} | {s["max_run"]}: {s["max_locations"]} |')
    lines+=['', '## Source-group contiguous exposure (separate from example groups)', '',
            'Source group means the first three colon-separated components of `group_id` (pilot version + source namespace), not an asserted original file shard. Revision aliases remain exact in `source-aliases.json`; these labels are not silently merged with original-shard counts. No manifest or additional rows were needed/read.', '',
            '| Source group | Family | Count | First–last | Runs | Maximum run: index range(s) |','|---|---|---:|---|---:|---|']
    for v,s in stats['source_group']['values'].items():
        fam=sorted({dims['family'][i] for i,x in enumerate(dims['source_group']) if x==v})
        lines.append(f'| {v} | {", ".join(fam)} | {s["count"]} | {s["first"]}–{s["last"]} | {s["runs"]} | {s["max_run"]}: {s["max_locations"]} |')
    lines+=['', '## Transitions and runs', '']
    for k,s in stats.items():
        lines.append(f'- `{k}`: {s["changes"]} changes / 1499 adjacent pairs; {s["same_adjacent"]} same-label adjacent pairs; {s["runs"]} runs, maximum {s["maximum"]}; run-length histogram {s["run_length_histogram"]}.')
    lines+=['', 'Full directed transition counts (including self-transitions), per-label first/last occurrences and all tied maximum locations are in `summary.json`; every contiguous run is in `runs.json`.', '', '## Fixed windows', '', '| Window (indices) | Family counts | Source-group counts |','|---|---|---|']
    for w in window_counts:
        lines.append(f'| {w["name"]} ({w["start"]}–{w["end"]}) | '+', '.join(f'{k}={v}' for k,v in w['counts']['family'].items())+' | '+', '.join(f'{k.removeprefix("data:")}={v}' for k,v in w['counts']['source_group'].items())+' |')
    lines+=['', '`windows.json` also supplies exact provenance.source counts, with explicit zero counts, for each fixed prefix/suffix and decile.', '', '## Update mixtures and group distinction', '',
            f'- Distinct families per update: {mix["family_distinct"]}; family multiplicity patterns: {mix["family_count_patterns"]}.',
            f'- Distinct source groups per update: {mix["source_group_distinct"]}; distinct exact group IDs: {mix["group_distinct"]}.',
            f'- {len(mix["updates_with_repeated_group"])} updates repeat an exact group ID; {mix["repeated_group_excess_presentations"]} presentations beyond the first of their group within those updates. Update IDs: {mix["updates_with_repeated_group"]}.',
            f'- Observed group-size histogram (size → number of groups): {counts(g["count"] for g in groups)}.',
            '- A named rule/mechanism group can have multiple presentations; a singleton scenario group contributes only one presentation in this schedule. These are not comparable counts of independent mechanisms. Repeated non-rule groups are kept separate; their semantics are not inferred from count alone. `groups.json` records every group, its classification, indices, and update IDs.',
            '- `updates.json` records every update’s four IDs, ordered family/source-group/group sequences, exact-source and family/group compositions, and repeated-group multiplicities. `summary.json` includes every family composition frequency.', '',
            '## Reproduction and evidence', '', 'Run `python3 '+str(OUT/'analyze.py')+'`. Python standard library only. Reads exactly the four pinned input paths listed below; writes only this directory. Does not inspect loss fields semantically, fit summaries, weights, or any other rows. Source strings containing per-case fragments are retained verbatim; exact-source contiguity can therefore differ substantially from source-group contiguity.', '', '| Input | SHA-256 |','|---|---|']
    for k,h in hashes.items(): lines.append(f'| `{h["path"]}` | `{h["sha256"]}` |')
    lines+=['', 'These are descriptive exposure facts for Model/Evaluation interpretation, not an optimization diagnosis, evaluation result, recommendation to reshuffle, or authorization for another run.']
    (OUT/'report.md').write_text('\n'.join(lines)+'\n')
    dump('artifact-hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='artifact-hashes.json'})
    print(json.dumps(dict(checks=checks,mixtures=mix,source_group_maxima={k:v['max_run'] for k,v in stats['source_group']['values'].items()}),indent=2))

if __name__ == '__main__':
    main()
