import json, math, hashlib, csv
from pathlib import Path
from collections import Counter
ROOT=Path('/Users/destiner/Code/jeff')
BASE=ROOT/'artifacts/evaluation/e6-analysis-preparation-v3/execution-01'
OUT=ROOT/'artifacts/evaluation/e6-quality-review-v1'
pins={}; checks=[]; discrepancies=[]
def load(p,lines=False):
 p=Path(p); raw=p.read_bytes(); pins[str(p)]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
 return [json.loads(x) for x in raw.splitlines() if x.strip()] if lines else json.loads(raw)
def check(name,ok):
 checks.append({'check':name,'ok':bool(ok)})
 if not ok: discrepancies.append(name)
def dump(name,x): (OUT/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def csvout(name,rows):
 if rows:
  with (OUT/name).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def mean(xs):return math.fsum(xs)/len(xs)
def metrics(xs):
 return dict(n=len(xs),correct=sum(x['correct'] for x in xs),nll=mean([x['nll'] for x in xs]),brier=mean([x['brier'] for x in xs]),ties=sum(x['ties']>1 for x in xs),zero_target=sum(x['target_probability']==0 for x in xs))
def pairmetrics(xs):
 return dict(n=len(xs),flips=sum(x['flip'] for x in xs),flips_without_ties=sum(x['flip'] and not x['tied'] for x in xs),untied_pairs=sum(not x['tied'] for x in xs),both=sum(x['both'] for x in xs),original_only=sum(x['original_only'] for x in xs),reversed_only=sum(x['reversed_only'] for x in xs),neither=sum(x['neither'] for x in xs),tv=mean([x['tv'] for x in xs]),max_change=max(x['max_change'] for x in xs))
cfg=load(BASE/'recipe.json'); auth=load(BASE/'grouped-both-order-summary.json')
metadata=load(ROOT/'artifacts/evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json')['by_validation_id']
T='m6-qwen-v2-trained'; F='m6-qwen-fresh-start'; P='qwen25-05b-instruct-frozen'
allmetrics=[]; allpairs=[]; gains=[]; case_rows=[]; mapping=[]; position=[]; diagnostics=[]; results={}
for stratum,conf in cfg['strata'].items():
 refs0=load(conf['examples']['path'],True); refs=load(conf['order_examples']['path'],True); ref={x['id']:x for x in refs}; pairs=load(conf['order_pairs']['path']); gs=auth['strata'][stratum]
 for r in refs0:
  m=metadata.get(r['id'],{})
  mapping.append(dict(stratum=stratum,id=r['id'],family=r['task_family'],label_basis=r['provenance']['label_basis'],source_group=r['group_id'],producer=m.get('producer'),domain=m.get('domain'),mechanism=m.get('mechanism'),policy_instance=m.get('policy_instance')))
 outcomes={}; pruns={}
 comparison=load(BASE/'study'/stratum/'comparison.json')
 for predictor in conf['predictors']:
  raw=load(BASE/'study'/stratum/(predictor+'-order.jsonl'),True); rawmap={x['id']:x for x in raw}
  check(stratum+'/'+predictor+'/coverage',len(raw)==len(rawmap)==len(ref) and set(rawmap)==set(ref))
  run={}; margins=[]; confidences=[]; pos=Counter()
  orderreport=load(BASE/'study'/stratum/(predictor+'-order-report.json'))
  core={x['id']:x for x in orderreport['prediction_report']['outcomes']}
  for ident,r in ref.items():
   items=rawmap[ident]['probabilities']; ps={x['option_id']:x['probability'] for x in items}; opts=[x['id'] for x in r['options']]
   valid=len(ps)==len(items)==len(opts) and set(ps)==set(opts) and all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) and 0<=x<=1 for x in ps.values()) and abs(sum(ps.values())-1)<=1e-6
   check(stratum+'/'+predictor+'/'+ident+'/valid',valid)
   # Reproduce the existing core's roundoff-only normalization, not a new repair policy.
   s=sum(ps.values()); norm={k:v/s for k,v in ps.items()}
   top=max(ps.values()); choice=next(k for k in opts if ps[k]==top); tie=sum(v==top for v in ps.values()); target=norm[r['target_id']]
   nll=-math.log(target) if target else math.inf; brier=sum((norm[k]-(k==r['target_id']))**2 for k in opts)
   o=dict(id=ident,correct=choice==r['target_id'],choice=choice,ties=tie,nll=nll,brier=brier,target_probability=target,probabilities=norm)
   run[ident]=o
   check(stratum+'/'+predictor+'/'+ident+'/core_arithmetic',abs(nll-core[ident]['log_loss'])<1e-12 and abs(brier-core[ident]['brier'])<1e-12 and choice==core[ident]['choice_id'] and tie==core[ident]['tie_size'])
   if predictor==T:
    ordered=sorted(ps.values(),reverse=True); margins.append(ordered[0]-ordered[1]);confidences.append(top);pos[opts.index(choice)]+=1
   case_rows.append(dict(stratum=stratum,predictor=predictor,id=ident,family=r['task_family'],source_group=r['group_id'],correct=o['correct'],choice=choice,ties=tie,nll=nll,brier=brier))
  outcomes[predictor]=run
  if predictor==T:position.append(dict(stratum=stratum,n=len(run),input_position_counts=dict(pos),ties=sum(x['ties']>1 for x in run.values()),raw_margin_min=min(margins),raw_margin_max=max(margins),raw_confidence_min=min(confidences),raw_confidence_max=max(confidences)))
  prs={}
  for pair in pairs:
   a=run[pair['original_id']];b=run[pair['reversed_id']]; dif=[abs(a['probabilities'][k]-b['probabilities'][k]) for k in a['probabilities']]
   prs[pair['original_id']]=dict(flip=a['choice']!=b['choice'],tied=a['ties']>1 or b['ties']>1,both=a['correct'] and b['correct'],original_only=a['correct'] and not b['correct'],reversed_only=b['correct'] and not a['correct'],neither=not a['correct'] and not b['correct'],tv=sum(dif)/2,max_change=max(dif))
  pruns[predictor]=prs
  diag=orderreport['prediction_report'];diagnostics.append(dict(stratum=stratum,predictor=predictor,records=len(raw),missing=0,invalid=0,duplicates=len(diag['duplicate_prediction_ids']),extra=len(diag['extra_prediction_ids']),unidentifiable=diag['unidentifiable_records'],record_diagnostics=len(diag['record_diagnostics'])))
 check(stratum+'/fresh_P3_exact',all(outcomes[F][k]==outcomes[P][k] for k in ref))
 results[stratum]={}
 for orient,groups in gs['orientations'].items():
  for key,group in groups.items():
   ids=group['reference_ids']; unit=json.loads(key)
   for pred,run in outcomes.items():
    met=metrics([run[k] for k in ids]); row=dict(stratum=stratum,orientation=orient,dimension=unit[0],unit=json.dumps(unit[1:]),predictor=pred,**met);allmetrics.append(row)
    am=group['runs'][pred]
    check(stratum+'/'+orient+'/'+key+'/'+pred+'/aggregate',abs(met['nll']-am['log_loss']['mean'])<1e-12 and abs(met['brier']-am['brier']['mean'])<1e-12 and met['correct']==am['top_choice']['on_valid']['numerator'])
    if unit==['all']:results[stratum][orient+':'+pred]=met
   a=[outcomes[T][i] for i in ids];b=[outcomes[F][i] for i in ids]
   dl=[x['nll']-y['nll'] for x,y in zip(a,b)]; db=[x['brier']-y['brier'] for x,y in zip(a,b)]
   gains.append(dict(stratum=stratum,orientation=orient,dimension=unit[0],unit=json.dumps(unit[1:]),common_valid=len(ids),agreement_gains=sum(x['correct'] and not y['correct'] for x,y in zip(a,b)),agreement_losses=sum(y['correct'] and not x['correct'] for x,y in zip(a,b)),nll_delta=mean(dl),brier_delta=mean(db),nll_improving_cases=sum(x<0 for x in dl),nll_worsening_cases=sum(x>0 for x in dl),nll_negative_sum=math.fsum(x for x in dl if x<0),nll_positive_sum=math.fsum(x for x in dl if x>0),brier_negative_sum=math.fsum(x for x in db if x<0),brier_positive_sum=math.fsum(x for x in db if x>0)))
 for pred,groups in ((p,gs['predictors'][p]['both_order_groups']) for p in outcomes):
  for key,g in groups.items():
   unit=json.loads(key); xs=[pruns[pred][p['original_id']] for p in g['pairs']];met=pairmetrics(xs)
   allpairs.append(dict(stratum=stratum,dimension=unit[0],unit=json.dumps(unit[1:]),predictor=pred,**met))
   check(stratum+'/'+key+'/'+pred+'/pair_arithmetic',met['both']==g['metrics']['both_correct'] and met['flips']==met['n']-g['metrics']['choice_consistency']['numerator'] and abs(met['tv']-g['metrics']['mean_total_variation'])<1e-12)
   if unit==['all']:results[stratum]['pairs:'+pred]=met
 # Both complete source domains/producers and source groups are preserved as overlapping units.
 if stratum=='probes':
  for pred,run in outcomes.items():
   macro=mean([mean([run[p['original_id']]['nll'],run[p['reversed_id']]['nll']]) for p in pairs]);check('probe_macro/'+pred,abs(macro-gs['probe_pair_macro'][pred]['nll_mean'])<1e-12)
csvout('all-orientation-unit-metrics.csv',allmetrics);csvout('all-unit-order-metrics.csv',allpairs);csvout('paired-gains-losses.csv',gains);csvout('per-presentation-arithmetic.csv',case_rows);csvout('explicit-case-unit-mapping.csv',mapping);csvout('coverage.csv',diagnostics)
dump('numbers.json',dict(overall=results,orientation_units=allmetrics,order_units=allpairs,paired_gains_losses=gains,position=position));dump('source-pins.json',pins)
dump('receipt.json',dict(command='/Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python -B '+str(OUT/'review.py'),checks=len(checks),failed_checks=discrepancies,all_11_predictors_per_stratum=True,quality_reports_checked=33,order_reports_checked=33,position=position,recomputed='All raw assembled per-option records joined to frozen references; independent normalized NLL/summed Brier, input-order top choice/ties, family/unit means, paired gain/loss contributions, choice flips, both/either/neither, TV/max changes; all compared with core per-case/group artifacts.',checked_authoritative='Reviewed E3 metadata ancestry; grouped membership identities; control/TRAIN/P4 lineage reviews read, not repeated tensor/execution audits.',limits='No weights/models/inference/tests/lint/network/final access; only new review artifacts. Source grouping dimensions overlap. No causal identification or significance claim.'))
print('checks',len(checks),'discrepancies',len(discrepancies));print(json.dumps(results,indent=2));print('POSITION',position)
# Compact six-decimal tables; full precision is in numbers.json and CSVs.
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+''.join('| '+' | '.join(f'{v:.6f}' if isinstance(v,float) else str(v) for v in row)+' |\n' for row in rows)
appendix='# E6 arithmetic appendix\n\nAll numbers recomputed from saved predictions, except explicitly noted metadata ancestry. Full precision: [numbers.json](numbers.json). Dimensions overlap; do not sum them as independent samples.\n\n'
for s in results:
 appendix+='## '+s+' — all 11 predictors\n\n'+table(['Predictor','Order','n','Agreement count','NLL','Brier','Ties'],[[r['predictor'],r['orientation'],r['n'],r['correct'],r['nll'],r['brier'],r['ties']] for r in allmetrics if r['stratum']==s and r['dimension']=='all'])+'\n'
 appendix+='### Every family, all predictors\n\n'+table(['Family','Predictor','Order','n','Agreement count','NLL','Brier','Ties'],[[r['unit'],r['predictor'],r['orientation'],r['n'],r['correct'],r['nll'],r['brier'],r['ties']] for r in allmetrics if r['stratum']==s and r['dimension']=='family'])+'\n'
 appendix+='### Order robustness: all predictors and families\n\n'+table(['Family/unit','Predictor','Pairs','Flips','Both','Original only','Reverse only','Neither','TV','Max change'],[[r['unit'],r['predictor'],r['n'],r['flips'],r['both'],r['original_only'],r['reversed_only'],r['neither'],r['tv'],r['max_change']] for r in allpairs if r['stratum']==s and r['dimension'] in ['all','family']])+'\n'
appendix+='## Granular index\n\n- [All orientation × source-unit × predictor metrics](all-orientation-unit-metrics.csv): every source group, producer, domain, mechanism, individual explicit policy, family × label basis, and unknown units.\n- [All order × source-unit × predictor metrics](all-unit-order-metrics.csv): flips, tie-free flips, both-correct, original/reverse-only, neither, TV/max change.\n- [All paired gains/losses and signed contributions](paired-gains-losses.csv): final minus fresh (= final minus P3); common-valid denominators; positive/negative NLL and Brier sums and case counts.\n- [Every presentation arithmetic](per-presentation-arithmetic.csv), including all private case IDs only here.\n- [Explicit E3 reviewed case→unit mapping](explicit-case-unit-mapping.csv): no ancestry parsed from IDs; policy null stays null. Frozen pair identities remain in source recipe order_pairs files pinned by source-pins.json.\n- [Coverage and invalid diagnostics](coverage.csv), 33 order reports; original quality reports are checked through comparison and grouped means.\n- [Exact source SHA256s](source-pins.json) and [review receipt](receipt.json).\n'
(OUT/'appendix.md').write_text(appendix)
