"""Apply the frozen E4 conjunction to existing scorer outcomes, not new metrics."""
from pathlib import Path
import math
from jeff.evaluation.common import fingerprint, load_examples, parse_json, write_json
from jeff.evaluation.metrics import loss_summary

E=Path('/Users/destiner/Code/jeff/artifacts/evaluation')
OUT=E/'e4-m5-result-v1'
OUT.mkdir(exist_ok=False)
paths={
 'criterion':E/'e4-m5-preregister-v1/criterion.json',
 'historical':E/'e4-m5-preregister-v1/historical-bindings.json',
 'controls':E/'e4-m5-control-review-v1/receipt.json',
 'pilot':E/'e4-m5-comparison-v1/pilot/comparison.json',
 'probes':E/'e4-m5-comparison-v1/probes/comparison.json',
 'pairs':E/'probes-v1/pairs.json',
 'references':E/'probes-v1/validation.jsonl',
 'order':E/'e4-m5-comparison-v1/probes/m5-low-head-lr-order.json',
}
pins={k:fingerprint(v) for k,v in paths.items()}
d={k:parse_json(v.read_text()) for k,v in paths.items() if k!='references'}
criterion=d['criterion']['criteria']
refs={r['id']:r for r in load_examples(paths['references'])}
runs=d['probes']['runs']
pairs=d['pairs']
coverage = len(refs)==24 and len(pairs)==12 and len({p['group_id'] for p in pairs})==12
coverage = coverage and {p[k] for p in pairs for k in ('original_id','reversed_id')}==set(refs)
coverage = coverage and all(run['status']=='ok' and run['overall']['coverage']['value']==1 for report in (d['pilot'],d['probes']) for run in report['runs'].values())
coverage = coverage and d['order']['overall']['complete_pair_coverage']['numerator']==12
outcomes={n:{r['id']:r for r in v['outcomes']} for n,v in runs.items()}


def detail(row):
 if row['status']!='valid':return {'status':row['status']}
 p=row['probabilities']; order={o['id']:i for i,o in enumerate(refs[row['id']]['options'])}
 ranked=sorted(p,key=lambda k:(-p[k],order[k]))
 target=row['target_id'];margin=p[target]-max(v for k,v in p.items() if k!=target)
 return {'status':'valid','target_rank':ranked.index(target)+1,'target_probability':p[target],
         'signed_target_margin':margin,'correct':row['correct'],'choice_id':row['choice_id'],
         'target_id':target,'loss':row['log_loss'],'tie_size':row['tie_size']}


groups=[];recovered=[];new_errors=[];group_losses={n:[] for n in runs}
for pair in pairs:
 gid=pair['group_id'];entry={'group_id':gid,'runs':{}}
 for name,byid in outcomes.items():
  rows=[byid[pair[k]] for k in ('original_id','reversed_id')]
  valid=[r for r in rows if r['status']=='valid']
  loss=loss_summary(valid)
  complete=len(valid)==2
  group_losses[name].append(loss['mean'] if complete and loss['status']=='finite' else None)
  entry['runs'][name]={'original':detail(rows[0]),'reversed':detail(rows[1]),
       'complete':complete,'correct_both':complete and all(r['correct'] for r in rows),
       'choice_consistent':complete and rows[0]['choice_id']==rows[1]['choice_id'],'pair_loss':loss}
 new=entry['runs']['m5-low-head-lr'];old=entry['runs']['m3-historical-trained']
 if gid in criterion['recovery']['eligible_groups'] and new['correct_both']:recovered.append(gid)
 if any(old[side].get('correct',False) and not new[side].get('correct',False) for side in ('original','reversed')):new_errors.append(gid)
 groups.append(entry)
macros={name:math.fsum(values)/12 if len(values)==12 and all(v is not None for v in values) else None for name,values in group_losses.items()}
pilot=d['pilot']['runs']['m5-low-head-lr']['overall']['log_loss']
checks={
 'coverage':bool(coverage),
 'controls_comparable':d['controls']['comparable'] is True and not d['controls']['errors'],
 'recover_lost_group':len(recovered)>=criterion['recovery']['minimum'],
 'no_new_error':len(new_errors)==0,
 'lower_probe_group_macro_loss':macros['m5-low-head-lr'] is not None and macros['m5-low-head-lr']<criterion['probe_loss']['historical_value'],
 'pilot_loss_within_ceiling':pilot['status']=='finite' and pilot['mean']<=criterion['pilot_loss']['maximum'],
}
rule_counts={}
for name,run in d['pilot']['runs'].items():
 byid={r['id']:r for r in run['outcomes']};counts={}
 for m in d['historical']['pilot_rule_category_mapping']:
  row=byid[m['id']];c=counts.setdefault(m['group_id'],{'rows':0,'valid':0,'no_result_targets':0,'no_result_choices':0,'correct':0,'correct_no_result':0,'correct_nonempty':0})
  c['rows']+=1;c['no_result_targets']+=m['target_is_no_result']
  if row['status']=='valid':
   c['valid']+=1;c['no_result_choices']+=row['choice_id']==m['no_result_option_id'];c['correct']+=row['correct']
   c['correct_no_result']+=row['correct'] and m['target_is_no_result'];c['correct_nonempty']+=row['correct'] and not m['target_is_no_result']
 rule_counts[name]=counts
result={'schema_version':'evaluation/e4-m5-result/1','pins':pins,'code':fingerprint(__file__),
 'criteria_pass':all(checks.values()),'checks':checks,'recovered_lost_groups':recovered,'newly_wrong_groups':new_errors,
 'all12_group_macro_loss':macros,'pilot_loss':pilot,'pilot_loss_ceiling':criterion['pilot_loss']['maximum'],
 'groups':groups,'pilot_rule_category_counts':rule_counts,
 'interpretation':'Fixed conjunction; no outcome-dependent exclusion. Teacher agreement, not independent correctness. M2 is context. One historical single-seed/backend comparison cannot establish causality; no default/promotion.'}
for k,v in paths.items():
 if fingerprint(v)!=pins[k]:raise ValueError('Input changed while applying criterion')
write_json(OUT/'result.json',result)
lines=['# E4 M5 fixed criterion result','',f"**Full conjunction: {'PASS' if result['criteria_pass'] else 'FAIL'}.**",'']
for k,v in checks.items():lines.append(f'- {k}: {v}')
lines+=['',f"Recovered eligible groups: {', '.join(recovered) or 'none'}. New errors: {', '.join(new_errors) or 'none'}.",
 f"All12group macro loss: historical {macros['m3-historical-trained']:.9f}; M5 {macros['m5-low-head-lr']:.9f}. Pilot M5 {pilot['mean']:.9f}, ceiling {criterion['pilot_loss']['maximum']:.9f}.",'',
 'Cells: original target rank / target probability / signed target-minus-best-rival margin / log loss. Original is counted once per group; JSON preserves both presentations and their mean losses.','',
 '| Probe group | Historical M3 start | Historical M3 trained | M5 low-head-LR |','| --- | --- | --- | --- |']
for group in groups:
 cells=[group['group_id'].removeprefix('eval.validation.')]
 for name in ('m3-pretrained-start','m3-historical-trained','m5-low-head-lr'):
  x=group['runs'][name]['original']
  cells.append(f"{x['target_rank']} / {x['target_probability']:.6f} / {x['signed_target_margin']:+.6f} / {x['loss']:.6f}" if x['status']=='valid' else x['status'])
 lines.append('| '+' | '.join(cells)+' |')
lines+=['','All probe labels are teacher labels, curator identity unknown. These repeatedly used development groups are not untouched final evidence or independent row trials. Missing/invalid coverage prevents success; all groups retained. Lower head LR alone is not supported under the full preregistered criterion; no default selection.']
with (OUT/'report.md').open('x') as f:f.write('\n'.join(lines)+'\n')
print({k:result[k] for k in ('criteria_pass','checks','recovered_lost_groups','newly_wrong_groups','all12_group_macro_loss','pilot_loss')})
