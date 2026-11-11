#!/usr/bin/env python3
"""Frozen R6 four-cell descriptives; stdlib only, no referenced paths followed."""
import argparse
import collections
import datetime
import hashlib
import json
import math
from pathlib import Path
import shlex
import sys
import time

CELLS = ('O0L0', 'O0L1', 'O1L0', 'O1L1')
PAIRS = (('O0L0','O0L1'), ('O1L1','O1L0'), ('O0L0','O1L1'), ('O0L1','O1L0'), ('O0L0','O1L0'), ('O0L1','O1L1'))
PINS = {'run/predictions.jsonl':'c9068e41915629f9419066941124c74fd7f181e93c840ca05e807d9e0056494d', 'run/receipt.json':'9c0e1e530bd88d0ce08f55fc26c82efdbc83dca50c20efd8748979d0d1799c7a', 'packet-v1/packet.json':'7598451302c5389e62476c88e7c2489fa355e0c40611e91cfbd6da1d9dc35e03'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def save(path, obj):
    with path.open('x') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n')

def mean(v):
    return sum(v)/len(v)

def quantile(v, q):
    a = sorted(v)
    t = (len(a)-1)*q
    lo = int(t)
    return a[lo] + (a[min(lo+1,len(a)-1)]-a[lo])*(t-lo)

def weights(rows):
    units = collections.defaultdict(lambda: collections.Counter())
    for c in rows:
        units[c['source']][c['group']] += 1
    return [1/len(units)/len(units[c['source']])/units[c['source']][c['group']] for c in rows]

def aggregate(rows, balanced):
    w = weights(rows) if balanced else [1/len(rows)]*len(rows)
    out = {'cases':len(rows), 'sources':len({c['source'] for c in rows}), 'groups':len({(c['source'],c['group']) for c in rows})}
    positive = [c for c in rows if c['log_valid']]
    out['log_cases'] = len(positive)
    if positive:
        lw = weights(positive) if balanced else [1/len(positive)]*len(positive)
        out['contrasts'] = {}
        for name in ('alpha','beta','R'):
            vectors = [c[name] for c in positive]
            out['contrasts'][name] = {
                'rms':math.sqrt(sum(a*mean([x*x for x in v]) for a,v in zip(lw,vectors))),
                'mean_abs':sum(a*mean([abs(x) for x in v]) for a,v in zip(lw,vectors)),
                'mirror_symmetric_component_rms':math.sqrt(sum(a*mean([((v[j]+v[-1-j])/2)**2 for j in range(len(v))]) for a,v in zip(lw,vectors)))
            }
            odd = [(a,v[len(v)//2]) for a,v in zip(lw,vectors) if len(v)%2]
            out['contrasts'][name]['odd_middle_cases'] = len(odd)
            out['contrasts'][name]['odd_middle_rms'] = math.sqrt(sum(a*x*x for a,x in odd)/sum(a for a,x in odd)) if odd else None
            out['contrasts'][name]['odd_middle_mean_abs'] = sum(a*abs(x) for a,x in odd)/sum(a for a,x in odd) if odd else None
    out['pairs'] = {}
    for pair in PAIRS:
        key = '~'.join(pair)
        vals = [c['pairs'][key] for c in rows]
        d = {metric:sum(a*v[metric] for a,v in zip(w,vals)) for metric in ('tv_semantic','tv_letter','tv_display_position')}
        eligible = [(a,v) for a,v in zip(w,vals) if v['unique_pair']]
        d['unique_pairs'] = len(eligible)
        for metric in ('identity_retention','letter_retention','position_retention'):
            d[metric] = sum(a*v[metric] for a,v in eligible)/sum(a for a,v in eligible) if eligible else None
        out['pairs'][key] = d
    return out

def main():
    started = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-root', type=Path, required=True)
    parser.add_argument('--runtime-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=False)
    task_names = ['packet-v1/selection.json','packet-v1/packet.json','packet-v1/config.json','analysis-predeclaration-v1.md','method/findings.md']
    runtime_names = ['run/predictions.jsonl','run/receipt.json','audit/audit.json','completion-summary.json','output-validation.json','audit-process.json','predict-process.json']
    blobs = {n:(args.task_root/n).read_bytes() for n in task_names}
    blobs.update({n:(args.runtime_root/n).read_bytes() for n in runtime_names})
    hashes = {n:digest(b) for n,b in blobs.items()}
    for n,h in PINS.items():
        require(hashes[n] == h, 'Pin mismatch '+n)
    command = shlex.join([sys.executable,'-I','-S',str(Path(__file__).resolve()),*sys.argv[1:]])
    receipt = {
        'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'command':command,
        'python':sys.version, 'script_sha256':digest(Path(__file__).read_bytes()), 'input_sha256':hashes,
        'method_frozen_before_derived_metrics':True,
        'method':'Four-cell section of analysis-predeclaration-v1.md only; overrides optional fit/sensitivity suggestions in method/findings.md. No source fit, targets, accuracy, correction, entropy or max-prob summaries.',
        'mapping':'Join option_id strictly; semantic index=option_scores.original_position; slot=j if O0 else K-1-j; letter index=slot if L0 else K-1-slot. Score arrays are semantic order, not display order; sort by derived slot for prepared-token and tie checks.',
        'contrasts':{'x':'log(p)-mean_options(log(p)) per condition','alpha':'((x00-x01)+(x11-x10))/2','beta':'((x00-x11)+(x01-x10))/2','R':'x00-x01+x10-x11'},
        'weights':'source=(family,producer); sources equal, domain for intent/sentiment or mechanism for rules else source_group, groups equal within source, rows equal within group, options 1/K. Rebalance within each reported subset and positive log support; raw row summaries separate.',
        'zero_tie_rules':'Finite [0,1], sums tolerance 1e-6, no renormalization. Any zero excludes whole case from logs only; no floor. Exact maximum ties counted; retention uses strict unique pairs only.',
        'mirror_definition':'(v[j]+v[K-1-j])/2; odd middle v[K//2]. Across-case heterogeneity = within-K/semantic-slot weighted SD, option average; descriptive, no correction.',
        'mass_quantiles':'Unweighted linear interpolation at (n-1)q; source/group balanced mean separately.',
        'receipt_scope':'Runtime execution and asset/source attestations only, not independent scientific-quality verification. No referenced paths opened.'
    }
    save(out/'input-receipt.json', receipt)
    data = {n:json.loads(b) for n,b in blobs.items() if n.endswith('.json')}
    packet = data['packet-v1/packet.json']; config = data['packet-v1/config.json']
    selected = data['packet-v1/selection.json']['cases']
    run = data['run/receipt.json']; audit = data['audit/audit.json']; summary = data['completion-summary.json']
    for n in ('selection','config'):
        require(hashes['packet-v1/'+n+'.json'] == packet[n]['sha256'], 'Packet binding '+n)
    require(packet['split']=='train' and packet['cases']==48 and packet['conditions']==list(CELLS), 'TRAIN packet')
    require(len(selected)==48 and len({c['case_id'] for c in selected})==48, 'Selection coverage')
    require(collections.Counter(c['family'] for c in selected)=={'intent':16,'sentiment':16,'rule_application':16}, 'Family quotas')
    for r in (run, audit):
        require(r['status']=='pass', 'Runtime status')
        e = r['evidence']
        for n in ('packet.json','selection.json','config.json'):
            require(e['packet_files'][n] == hashes['packet-v1/'+n], 'Runtime packet pin')
        for k in ('model_id','revision','chat_template_sha256'):
            require(e[k] == packet['p3'][k], 'P3 pin '+k)
        require(e['p3_audited_source_sha256']==packet['p3']['frozen_source_sha256'], 'Frozen source attestation')
        require(e['p3_config_sha256']==packet['p3']['config_sha256'], 'P3 config pin')
        require(e['inputs_sha256']==packet['input']['sha256'], 'Input attestation')
        require(e['source_sha256']==r['executor_source_sha256'], 'Executor attestation')
        for k,v in config.items():
            if k != 'maximum_run_seconds':
                require(e['p3_config'][k]==v, 'Unchanged config '+k)
    require(run['evidence']['source_sha256']==audit['evidence']['source_sha256'], 'Executor unchanged')
    require(run['evidence']['model_assets']==audit['evidence']['model_assets'] and run['actual_model_asset_hashes_verified'], 'Asset attestation')
    for k in ('written_rows','forward_attempts','completed_forwards'):
        require(run[k]==192 and summary[k]==192, 'Forward coverage')
    require(audit['completed_forwards']==0 and run['evidence']['controls']['startup_extra_forwards']==0, 'No extra forwards')
    for k in ('batch_size','threads','dtype','device','attention','use_cache','logits_to_keep','temperature'):
        require(run['evidence']['controls'][k]==config[k], 'Actual control '+k)
    require(config['temperature']==1 and config['max_input_tokens']==1024 and config['maximum_run_seconds']==300, 'T/cap')
    for n in ('audit-process.json','predict-process.json'):
        require(data[n]['returncode']==0 and data[n]['wall_seconds']>0, 'Finished process')
        require(data[n]['environment']['PYTORCH_ENABLE_MPS_FALLBACK']=='0', 'No fallback')
    require(data['predict-process.json']['combined_audit_predict_wall_seconds']<300, 'Time bound')
    require(summary['output_sha256']==hashes['run/predictions.jsonl'] and summary['receipt_sha256']==hashes['run/receipt.json'], 'Completion pins')
    records = [json.loads(line) for line in blobs['run/predictions.jsonl'].splitlines() if line.strip()]
    require(len(records)==192, 'Rows')
    prepared = {r['id']:r for r in audit['evidence']['prepared']}
    require(len(prepared)==192 and run['evidence']['prepared']==audit['evidence']['prepared'], 'Prepared binding')
    byid = {c['case_id']:c for c in selected}
    joined = collections.defaultdict(dict)
    validation = {'probability_slots':0,'zeros':0,'ones':0,'tied_presentations':0,'max_sum_error':0.,'max_T1_probability_error':0.,'max_full_vocab_logmass_error':0.,'max_mass_exp_error':0.}
    token_by_letter = {}
    for r in records:
        cid = r['case_id']; cell = r['condition']
        require(cid in byid and cell in CELLS and cell not in joined[cid] and r['id']==cid+'::'+cell, 'Case/cell identity')
        scores = r['option_scores']; probs = r['probabilities']; K = len(scores)
        require(K in (3,4,5,6) and len(probs)==K, 'K coverage')
        pmap = {v['option_id']:v['probability'] for v in probs}
        require(len(pmap)==K and len({v['option_id'] for v in scores})==K and set(pmap)=={v['option_id'] for v in scores}, 'Strict option IDs')
        require(sorted(v['original_position'] for v in scores)==list(range(K)), 'Original positions')
        p = [0.]*K; ids = [None]*K; letters = [None]*K; slots = [None]*K
        display_scores = sorted(scores, key=lambda s: s['original_position'] if cell[1]=='0' else K-1-s['original_position'])
        for slot,s in enumerate(display_scores):
            j = s['original_position']; expected_slot = j if cell[1]=='0' else K-1-j
            letter_index = slot if cell[3]=='0' else K-1-slot
            require(slot==expected_slot and s['letter']==chr(65+letter_index), 'Condition mapping')
            require(math.isfinite(s['logit']), 'Finite logit')
            letter = s['letter']; token = s['token_id']
            require(token_by_letter.setdefault(letter,token)==token, 'Letter token consistency')
            p[j]=pmap[s['option_id']]; ids[j]=s['option_id']; letters[j]=letter; slots[j]=slot
        require(all(math.isfinite(v) and 0<=v<=1 for v in p), 'Finite probabilities')
        error = abs(sum(p)-1); require(error<=1e-6, 'Probability sum')
        validation['max_sum_error']=max(validation['max_sum_error'],error)
        validation['probability_slots']+=K; validation['zeros']+=p.count(0); validation['ones']+=p.count(1)
        top = [s['option_id'] for s in display_scores if pmap[s['option_id']]==max(p)]
        require(r['chosen_option_id']==top[0] and r['tied_top_option_ids_display_order']==top, 'Choice/tie mapping')
        validation['tied_presentations']+=int(len(top)>1)
        logits = [s['logit'] for s in scores]; m=max(logits); z=sum(math.exp(v-m) for v in logits)
        err=max(abs(pmap[s['option_id']]-math.exp(s['logit']-m)/z) for s in scores)
        require(err<=1e-6, 'T1 softmax consistency')
        validation['max_T1_probability_error']=max(validation['max_T1_probability_error'],err)
        mass=r['allowed_full_vocab_mass']; logmass=r['allowed_full_vocab_logmass']; fullz=r['log_full_vocab_normalizer']
        require(all(math.isfinite(v) for v in (mass,logmass,fullz)) and 0<=mass<=1 and logmass<=0, 'Mass validity')
        masserr=abs(math.exp(logmass)-mass); lmerr=abs(m+math.log(z)-fullz-logmass)
        require(masserr<=1e-6 and lmerr<=1e-5, 'Mass/logit consistency')
        validation['max_mass_exp_error']=max(validation['max_mass_exp_error'],masserr)
        validation['max_full_vocab_logmass_error']=max(validation['max_full_vocab_logmass_error'],lmerr)
        prep=prepared[r['id']]
        require(prep['answer_token_ids']==[s['token_id'] for s in display_scores] and prep['input_tokens']==r['input_tokens']<=1024, 'Prepared token binding')
        joined[cid][cell]={'p':p,'ids':ids,'letters':letters,'slots':slots,'winner':ids.index(top[0]),'unique':len(top)==1,'mass':mass}
    require(validation['probability_slots']==740 and len(joined)==48, '740 slots / 48 cases')
    cases=[]
    for index,meta in enumerate(selected):
        cells=joined[meta['case_id']]
        require(set(cells)==set(CELLS), 'Four cells')
        require(all(cells[c]['ids']==cells[CELLS[0]]['ids'] for c in CELLS), 'Cross-condition semantic IDs')
        K=len(cells[CELLS[0]]['p'])
        group=(meta.get('domain') if meta['family'] in ('intent','sentiment') else meta.get('mechanism')) or meta.get('source_group') or 'unknown'
        c={'case_index':index,'split':'train','family':meta['family'],'producer':meta['producer'],'source':meta['family']+'/'+meta['producer'],'group':group,'K':K,'log_valid':all(v>0 for cell in cells.values() for v in cell['p']),'mass':{k:v['mass'] for k,v in cells.items()},'pairs':{}}
        if c['log_valid']:
            x={k:[math.log(v)-mean([math.log(u) for u in cell['p']]) for v in cell['p']] for k,cell in cells.items()}
            a,b,d,e=[x[k] for k in CELLS]
            c['alpha']=[((a[j]-b[j])+(e[j]-d[j]))/2 for j in range(K)]
            c['beta']=[((a[j]-e[j])+(b[j]-d[j]))/2 for j in range(K)]
            c['R']=[a[j]-b[j]+d[j]-e[j] for j in range(K)]
        for ca,cb in PAIRS:
            a=cells[ca]; b=cells[cb]
            def tv(coord):
                aa={a[coord][j]:a['p'][j] for j in range(K)}; bb={b[coord][j]:b['p'][j] for j in range(K)}
                return sum(abs(aa[k]-bb[k]) for k in aa)/2
            wa=a['winner']; wb=b['winner']
            c['pairs'][ca+'~'+cb]={'tv_semantic':tv('ids'),'tv_letter':tv('letters'),'tv_display_position':tv('slots'),'unique_pair':a['unique'] and b['unique'],'identity_retention':int(a['ids'][wa]==b['ids'][wb]),'letter_retention':int(a['letters'][wa]==b['letters'][wb]),'position_retention':int(a['slots'][wa]==b['slots'][wb])}
        cases.append(c)
    require(len({c['source'] for c in cases})==9, 'Nine source units')
    partitions={'global':cases}
    for field in ('family','source','K'):
        for value in sorted({c[field] for c in cases},key=str):
            partitions[field+':'+str(value)]=[c for c in cases if c[field]==value]
    results={'validation':validation,'counts_by_K':dict(collections.Counter(c['K'] for c in cases)), 'summaries':{},'mass':{},'heterogeneity':{},'cases':cases,'execution_command':command}
    for label,rows in partitions.items():
        results['summaries'][label]={mode:aggregate(rows,mode=='source_balanced') for mode in ('raw_row','source_balanced')}
    w=weights(cases)
    for cell in CELLS:
        masses=[c['mass'][cell] for c in cases]
        results['mass'][cell]={'min':min(masses),'p10':quantile(masses,.1),'median':quantile(masses,.5),'p90':quantile(masses,.9),'max':max(masses),'raw_row_mean':mean(masses),'source_balanced_mean':sum(a*v for a,v in zip(w,masses))}
    for K in sorted({c['K'] for c in cases}):
        rows=[c for c in cases if c['K']==K and c['log_valid']]; ww=weights(rows)
        results['heterogeneity'][str(K)]={}
        for name in ('alpha','beta','R'):
            means=[sum(a*c[name][j] for a,c in zip(ww,rows)) for j in range(K)]
            sd=[math.sqrt(sum(a*(c[name][j]-means[j])**2 for a,c in zip(ww,rows))) for j in range(K)]
            results['heterogeneity'][str(K)][name]={'slot_weighted_mean':means,'slot_weighted_sd':sd,'across_case_sd_rms':math.sqrt(mean([v*v for v in sd]))}
    results['elapsed_cpu_workflow_seconds']=time.monotonic()-started
    save(out/'results.json',results)
    lines=['# R6 executed frozen four-cell diagnostic','', '48 preselected TRAIN cases, 16 per family; 9 (family, producer) source units; 192 conditions and 740 probability slots. These correlated cases are not IID or held-out task evidence. No targets/accuracy, second fitted bias model, source fit, learned correction, entropy or max-prob analysis.', '', '## Execution and integrity', '', f'Input receipt was saved before derived metrics. All three supplied SHA256 pins matched. Coverage, strict option-ID joins and original-position/actual-letter/display-position mapping passed. K counts: {results["counts_by_K"]}.', f'Zeros: {validation["zeros"]}; ones: {validation["ones"]}; tied presentations: {validation["tied_presentations"]}; maximum sum error {validation["max_sum_error"]:.3g}; maximum float64 T=1 reconstruction error {validation["max_T1_probability_error"]:.3g}. No normalization or epsilon repair.', f'Allowed-mass exp consistency maximum error {validation["max_mass_exp_error"]:.3g}; log-sum-exp/full-vocabulary logmass maximum error {validation["max_full_vocab_logmass_error"]:.3g}.', '', 'Runtime receipts attest unchanged pinned frozen P3 model revision, asset hashes, frozen source, chat template, prompt/readout, FP32 MPS, T=1, cap1024, batch1, threads4, SDPA, no cache/fallback, zero extra startup forwards. R6 executor hash matches across audit/predict; P3 config differs only by predeclared 300s process bound (P3 1200s). This analysis checks receipts, not assets/source files themselves. No referenced paths were followed.', f'Runtime completed 192/192 forwards; its prediction-process workflow took {summary["process_runtime_seconds"]:.3f}s including non-forward work; externally supervised audit+predict {data["predict-process.json"]["combined_audit_predict_wall_seconds"]:.3f}s, both exit0. Runtime validated execution/identity/finite normalization only, not scientific model-output quality. Research owns this arithmetic and limited interpretation.', '', '## Natural-log contrasts/scales', '', 'x is condition-wise centered log p aligned by original semantic identity. alpha=((x00-x01)+(x11-x10))/2; beta=((x00-x11)+(x01-x10))/2; R=x00-x01+x10-x11. RMS is sqrt(weighted mean across cases of option-mean squares), not mean case RMS. Alpha is letter-assignment-associated, beta position/order-associated. R should be zero under additive invariant content. These are natural-log contrasts, not recovered complete biases.', '', 'Weights: sources equal, then domains (intent/sentiment) or mechanisms (rules), falling back to source_group, then rows equal; options 1/K. Each subset is rebalanced. Raw rows are separate estimands, not deployment prevalence.', '', '| Subset | n | alpha RMS / MA | beta RMS / MA | R RMS / MA |','|---|---:|---:|---:|---:|']
    for label,sm in results['summaries'].items():
        for mode in (('raw_row','source_balanced') if label=='global' else ('source_balanced',)):
            a=sm[mode]; nums=[f'{a["contrasts"][n]["rms"]:.4f} / {a["contrasts"][n]["mean_abs"]:.4f}' for n in ('alpha','beta','R')]
            lines.append(f'| {label} ({mode}) | {a["cases"]} | '+ ' | '.join(nums)+' |')
    lines += ['', '## Mirror restrictions and across-case heterogeneity', '', 'Mirror violation is the RMS of the mirror-symmetric component (v[j]+v[K-1-j])/2; it must vanish for a fixed mirror-antisymmetric account. Odd-middle is the centered-log contrast at the unmoved middle semantic option. Raw middle probability need not stay constant.', '', '| Global source-balanced contrast | mirror violation RMS | odd-middle n | odd-middle RMS / MA |','|---|---:|---:|---:|']
    for name,v in results['summaries']['global']['source_balanced']['contrasts'].items():
        lines.append(f'| {name} | {v["mirror_symmetric_component_rms"]:.4f} | {v["odd_middle_cases"]} | {v["odd_middle_rms"]:.4f} / {v["odd_middle_mean_abs"]:.4f} |')
    lines += ['', 'Descriptive across-case heterogeneity: within each K and original semantic slot, source-balanced SD, then RMS over slots. Means and SD vectors remain in results.json for reproduction; no fitted predictor/correction is made.', '', '| K | alpha SD RMS | beta SD RMS | R SD RMS |','|---|---:|---:|---:|']
    for K,d in results['heterogeneity'].items():
        lines.append('| '+K+' | '+' | '.join(f'{d[n]["across_case_sd_rms"]:.4f}' for n in ('alpha','beta','R'))+' |')
    lines += ['', '## Paired probability and choice retention', '', 'First two pairs change letters at fixed order; next two change order at fixed option letter; last two change both factors (standard and reversed-letter reversal). TV is aligned in each indicated coordinate system. Retention uses only strict unique argmax pairs; identity/letter/position events can overlap at odd middle. Full family/source/K breakdowns, both weighting schemes and eligibility counts are in results.json.', '', '| Pair | weighting | TV identity / letter / position | retention identity / letter / position | unique n |','|---|---|---:|---:|---:|']
    for mode,sm in results['summaries']['global'].items():
        for pair,v in sm['pairs'].items():
            tv=' / '.join(f'{v[n]:.4f}' for n in ('tv_semantic','tv_letter','tv_display_position'))
            ret=' / '.join(f'{v[n]:.4f}' if v[n] is not None else 'undefined' for n in ('identity_retention','letter_retention','position_retention'))
            lines.append(f'| {pair} | {mode} | {tv} | {ret} | {v["unique_pairs"]} |')
    lines += ['', '## Measured allowed full-vocabulary mass', '', 'Unweighted distribution quantiles use linear interpolation. Mean is shown both raw and source-balanced. Low allowed mass alone does not invalidate conditional classification.', '', '| Condition | min | p10 | median | p90 | max | raw mean | balanced mean |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for cell,v in results['mass'].items():
        lines.append('| '+cell+' | '+' | '.join(f'{v[n]:.6f}' for n in ('min','p10','median','p90','max','raw_row_mean','source_balanced_mean'))+' |')
    lines += ['', '## Interpretation and limits', '', 'Nonzero R, mirror violations, odd-middle contrasts and across-case heterogeneity describe departures from a shared static additive mirror account; none uniquely identifies a neural mechanism or reasoning failure. A zero R would not establish additivity either. Letter-assignment naturalness (ascending versus descending alphabet, binding and context) remains confounded with letter effects. Content-order interactions remain confounded with position effects. Only mirror pairings are observed; mirror-symmetric letter/position preferences are unidentified. TRAIN sample/source/template/teacher dependencies prevent generalization, causal exclusivity, calibration or accuracy claims. No M6/E6 outcomes, Evaluation/probe/D3/final inputs or references were opened.', '', '## Actual commands', '', 'This output directory records one invocation of the final script and refuses any overwrite. The earlier artifact prototype stopped before derived metrics on a semantic-order versus display-order validation error; its first receipt was overwritten with an embedded previous-attempt summary, not preserved as a standalone immutable file. That provenance limitation remains disclosed in the owner diagnosis. The binding correction and later path/report/output-immutability changes did not alter the declared estimator or weights.', '', '```sh',command,'```', '', f'Python: {sys.version.splitlines()[0]}. Analysis workflow elapsed {results["elapsed_cpu_workflow_seconds"]:.3f}s. Standalone stdlib CPU run only; all commands/jobs completed; no tests/lint, ML imports/load/inference/training/dependencies, mailbox, commits or merges.']
    with (out/'report.md').open('x') as f:
        f.write('\n'.join(lines)+'\n')
    print(json.dumps({'output_dir':str(out),'validation':validation,'global':results['summaries']['global'],'mass':results['mass'],'elapsed_seconds':time.monotonic()-started},indent=2))

if __name__=='__main__':
    main()
