import json,hashlib
from pathlib import Path
O=Path('/Users/destiner/Code/jeff/artifacts/evaluation/e6-quality-review-v1');B=O.parent/'e6-analysis-preparation-v3/execution-01'
d=json.loads((O/'numbers.json').read_text()); cfg=json.loads((B/'recipe.json').read_text()); binding=json.loads((O.parent/'e6-p4-binding-v1/receipt.json').read_text())
checks=[];pins={}; positions=[]
for stratum in cfg['strata']:
 for suffix in ['.jsonl','-order.jsonl']:
  a=B/'study'/stratum/('m6-qwen-fresh-start'+suffix)
  b=B/'study'/stratum/('qwen25-05b-instruct-frozen'+suffix)
  checks.append(a.read_bytes()==b.read_bytes())
  for p in [a,b]:pins[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
refs={}
for c in cfg['strata'].values():
 for r in map(json.loads,Path(c['order_examples']['path']).read_text().splitlines()):refs[r['id']]=r
for suite in binding['predictions']:
 def get(v):
  p=Path(v['path']);b=p.read_bytes();h=hashlib.sha256(b).hexdigest();pins[str(p)]=h;checks.append(h==v['sha256']);return [json.loads(x) for x in b.splitlines()]
 inputs=get(suite['input']);outputs=get(suite['output']);om={r['id']:r for r in outputs}
 checks.append(len(om)==len(outputs)==len(inputs) and set(om)=={x['id'] for x in inputs})
 for r in inputs:
  checks.append(all(r[k]==refs[r['id']][k] for k in ['state','question','options']))
  ps={x['option_id']:x['probability'] for x in om[r['id']]['probabilities']};opts=[x['id'] for x in r['options']];top=max(ps.values());w=[k for k in opts if ps[k]==top]
  positions.append(dict(suite=suite['name'],id=r['id'],input_position=opts.index(w[0]),tie_size=len(w)))
checks.append(len(positions)==624 and all(x['input_position']==0 and x['tie_size']==1 for x in positions))
(O/'direct-frozen-input-receipt.json').write_text(json.dumps(dict(checks=len(checks),failed=sum(not x for x in checks),source_pins=pins,positions=positions),indent=2)+'\n')
T='m6-qwen-v2-trained';F='m6-qwen-fresh-start';P='qwen25-05b-instruct-frozen'
def table(h,rows):return '| '+' | '.join(h)+' |\n| '+' | '.join('---' for _ in h)+' |\n'+''.join('| '+' | '.join(f'{v:.6f}' if isinstance(v,float) else str(v) for v in row)+' |\n' for row in rows)
text='''# E6 quality review — report candidate

## Conclusion

**Negative learning result for this bounded final-checkpoint recipe; no promotion or default change.** Relative to its fresh starting control, M6 loses agreement in both orientations of both broad strata, loses all both-order successes, and flips every paired choice. Intent and probe retention fail. This rejects the demonstrated combined supervised-learning plus frozen TRAIN-permutation recipe on these development populations, not every decoder or permutation training in isolation. No causal diagnosis is identified. No best checkpoint, fitted score threshold, new conjunction, retuning or experiment is introduced.

Fresh start and preserved P3 are exactly equal on all saved case/option probabilities; every fresh contrast below is therefore also the P3 contrast. Strong saved-output/semantic-control comparability is supported by the existing start-control and P4-binding reviews, not independent historical loaded-tensor attestation. Prior E3/E4/E5 conclusions remain unchanged. Parallel Model/Data audits are not an approval gate.

## Populations, coverage and arithmetic

Inherited: 60 cases / 12 source groups; new: 240 / 170. Original and reverse reuse the same cases. Probes are separate: 24 presentations / 12 curated pairs, four pairs per family, teacher-only. Combined300 is not an independent sample or a pooled performance claim. Family, label-basis, domain, producer, mechanism, policy and source-group dimensions overlap. Even source-group/domain/producer grouping is coarse and leaves dependencies; no significance or independence assumption is made.

All 11 predictors are retained in each stratum: M4 MiniLM random start/trained, M4 MS MARCO pretrained start/trained, M2, M3, uniform, lexical, preserved P3, M6 fresh, M6 final. Coverage of 33 quality and 33 order reports is complete. Every assembled presentation is valid; missing, invalid, duplicate, extra, malformed/unidentifiable record diagnostics are zero. All target probabilities are positive; no infinite NLL or dropped zero-target row. Valid and failures-as-unsuccessful agreement denominators coincide. The independent arithmetic review records 24,797 checks, zero discrepancies (actual-data analysis, not a software test suite).

NLL = mean natural-log −log p(target); Brier = mean sum over options of (p−onehot)², not divided by option count. Following the unchanged core, only already-valid roundoff-level sums are normalized for scoring; no output file is changed or probability repaired. Raw probabilities, rather than rounded report cells, determine choices/ties. Every independent per-case calculation agrees with core outcomes within 1e−12; aggregate comparisons use the same arithmetic tolerance, not a promotion threshold. Full precision and source JSON pointers are indexed below.

## Primary contrast, each orientation

'''
rows=[]
for s in d['overall']:
 for orient in ['original','reversed']:
  for p in [F,T]:
   r=d['overall'][s][orient+':'+p]; rows.append([s,orient,'fresh = P3' if p==F else 'final',f"{r['correct']}/{r['n']}",r['nll'],r['brier']])
text+=table(['Population','Order','Predictor','Agreement','NLL','Brier'],rows)
text+='''
The important exception is **new reversed NLL**, improving slightly from **1.4106206775423604 to 1.407130039288739** (Δ −0.0034906382536215), while Brier worsens **0.6874023517504078 → 0.7781339061775513**, agreement falls 118→65/240 and both-order success vanishes. It is incorrect to say every proper loss worsens. Smaller NLL or total variation alone is not ranking or robustness improvement.

## Choice robustness and retention

'''
text+=table(['Population','Predictor','Pairs','Flips','Both','Original only','Reverse only','Neither','Mean TV','Max Δp'],[[s,'fresh = P3' if p==F else 'final',r['n'],r['flips'],r['both'],r['original_only'],r['reversed_only'],r['neither'],r['tv'],r['max_change']] for s,v in d['overall'].items() for p in [F,T] for r in [v['pairs:'+p]]])
text+='''
All these final flips are untied flips. Direct joins of **actual P4 raw outputs to all 624 exact frozen label-free inputs** confirm the top choice is **input position 0 in 624/624**, with **zero ties**; output-list position was not assumed. See `direct-frozen-input-receipt.json` for each presentation and source hashes. This is a positional top-choice collapse, **not flat probabilities**. Across raw saved vectors, winning probability ranges 0.29401078820228577–0.7282788157463074; top-minus-second margin ranges 0.10249418020248413–0.45655760169029236. These are conditional allowed-symbol probabilities, not full-vocabulary probabilities or calibrated confidence.

Uniform has all-option ties; its input-order tie-break happens to produce the same final top-choice counts and flips, but uniform probabilities and proper losses differ. Its tie-free flip denominator is zero, not evidence of stable untied ranking. M6's untied positional collapse must not be equated with uniform's tie-breaking behavior.

New rules (80 cases / **40 explicit policies / 10 mechanisms**, not 80 independent policies):

'''
text+=table(['Predictor','Cases','Flips','Both correct','Original only','Reverse only','Neither','TV'],[[r['predictor'],r['n'],r['flips'],r['both'],r['original_only'],r['reversed_only'],r['neither'],r['tv']] for r in d['order_units'] if r['stratum']=='new-v2' and r['dimension']=='family' and r['unit']=='["rule_application"]' and r['predictor'] in [F,T]])
text+='\nIntent retention, each broad stratum and probes (both-order agreement and each orientation’s losses/counts are fully shown in the appendix):\n\n'
text+=table(['Population','Predictor','Pairs','Both correct','Flips'],[[r['stratum'],r['predictor'],r['n'],r['both'],r['flips']] for r in d['order_units'] if r['dimension']=='family' and r['unit']=='["intent"]' and r['predictor'] in [F,T]])
text+='''
## Family proper-loss changes and paired gains/losses

Final minus fresh (= final minus P3); negative proper-loss delta is improvement. Each common-valid denominator is shown; gains/losses mean newly correct/newly wrong reference agreements. Some sentiment/rule proper scores improve despite position collapse: these probability gains are retained, not misreported as robust rule learning.

'''
text+=table(['Population','Family','Order','Common valid','Agreement gains','Losses','ΔNLL','ΔBrier'],[[r['stratum'],r['unit'],r['orientation'],r['common_valid'],r['agreement_gains'],r['agreement_losses'],r['nll_delta'],r['brier_delta']] for r in d['paired_gains_losses'] if r['dimension']=='family'])
text+='''
Reference basis matters: inherited teacher labels remain teacher agreement; new intent/sentiment are teacher-labelled. New `rule_verified` includes both programmatic and teacher-authored/executable-consistency evidence with the existing same-alias and natural-language limitations, not independent human truth. Probes remain teacher-only, including their rule family; they are not upgraded by sharing a family name. Family×label-basis and explicit reviewed policy membership are preserved in the granular appendix. No policy/group ancestry is inferred from case IDs.

## Uniform and M4 practical context, both orders

'''
text+=table(['Population','Order','Predictor','Agreement','NLL','Brier'],[[r['stratum'],r['orientation'],r['predictor'],f"{r['correct']}/{r['n']}",r['nll'],r['brier']] for r in d['orientation_units'] if r['dimension']=='all' and r['predictor'] in ['uniform','m4-minilm-trained','m4-msmarco-trained']])
text+='''
M6 final has worse NLL and Brier than current uniform in both orders of each broad stratum and on probes. M4 trained encoders are better on both broad strata in both orientations; probe comparisons are mixed (in particular MS MARCO NLL is worse than M6), not an across-the-board encoder victory. All 11 predictors, original/reverse family top-choice counts and proper scores, and all paired metrics remain in [appendix.md](appendix.md). Different capacity/pretraining/rendering/training histories make this a practical systems comparison, **not a controlled architecture ablation**.

## Separate TRAIN evidence and process qualifications

The separate `e6-train-control-review-v1/report.md` reconstructs deterministic fixed-checkpoint TRAIN agreement **805→431/1500**, mean NLL **1.357723629→1.390592028**; 1,500 presentations, 375 updates, final one-epoch checkpoint, same frozen TRAIN permutation schedule. All after-fit argmax positions are 0, but **TRAIN ties are unknown** because saved fit rows lack probability vectors. Online changing-weight mean CE is not fixed-checkpoint fit or held-out performance. That review found no demonstrated rendering/reset/target/loss/loop bug and no causal diagnosis: optimization, inputs/labels, exposure and capacity remain unresolved. This review does not repeat large byte/weight audits or claim an independently observed training execution.

The owner preserved the v2 first-attempt failure before scoring, caused by two mutable policy pins (AGENTS and coordination). The v3 runner is reported byte-identical with 94 scientific pins unchanged; it is procedural recovery, not another learning attempt or a favorable checkpoint selection. The prior failure remains preserved. This synthesis checks actual v3 arithmetic, rather than treating a completed process receipt as proof of scores.

## Numerical receipts and complete appendix

- [Full unrounded recomputation](numbers.json): all orientation × family/source-unit proper metrics and all pair metrics, plus signed paired contributions. Six-decimal display above is not the precision used for deltas.
- [Indexed appendix](appendix.md): all 11 predictor tables; every family and granular source-group/domain/producer/mechanism/**individual policy** regression is accessible via linked CSVs; all private IDs stay there rather than in this main report.
- [Paired gains/losses](paired-gains-losses.csv): each common-valid denominator and positive/negative NLL/Brier contribution sum; dimensions overlap and must not be pooled or summed as independent evidence.
- [Explicit reviewed unit mapping](explicit-case-unit-mapping.csv): case→source group/domain/producer/mechanism/policy, unknowns retained. Pair membership uses frozen `recipe.json` → strata → `order_pairs`, not ID parsing.
- [Independent review receipt](receipt.json), [source hashes](source-pins.json), [direct raw-input binding](direct-frozen-input-receipt.json), reproducible `review.py` and `synthesize.py`. Primary authoritative sources: `e6-analysis-preparation-v3/execution-01/{recipe.json,grouped-both-order-summary.json,study/*/comparison.json,study/*/*-order-report.json}`; exact file paths and SHA256s are in source-pins. Family/unit metadata ancestry is accepted from the existing E3 reviewed mapping; arithmetic is independently recomputed from actual raw vectors and reference records, not delegated to those summaries.

**Material blockers:** none for this bounded synthesis. Evidence limits are historical tensor execution/weight attestation, unknown TRAIN ties, correlated development-only groups, same-alias label limitations and one combined recipe/seed; these constrain interpretation, not a new review gate. No inference, models, weights, new data, final data, network, paid calls, tests/lint/syntax checks, mailbox, tracked edits, commit or merge. Only new files in this artifact directory; £0 new spend.
'''
# Explicit all-pair macro receipt, without pooling probes with broad strata.
a=json.loads((B/'grouped-both-order-summary.json').read_text())['strata']['probes']['probe_pair_macro']
text+='\n### Probe all-pair macro probability scores (12 pairs, separate population)\n\n'+table(['Predictor','Macro NLL','Macro Brier','Stable correct pairs'],[[p,a[p]['nll_mean'],a[p]['brier_mean'],a[p]['stable_correct']] for p in [F,P,T]])
(O/'report-candidate.md').write_text(text)
print('direct frozen-input checks',len(checks),'failed',sum(not x for x in checks))
