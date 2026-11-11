"""CPU-only report extraction from completed shared-scored outcomes; no scoring or inference."""
import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path('/Users/destiner/Code/jeff')
BASE = ROOT / 'artifacts/evaluation/e5-comparison-preparation-v1/execution-01'
OUT = ROOT / 'artifacts/evaluation/e5-quality-analysis-v1'
inputs = []
def load(path):
    raw = path.read_bytes()
    inputs.append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
    return json.loads(raw)

comparisons = {s: load(BASE / 'study' / s / 'comparison.json') for s in ['inherited-v1', 'new-v2', 'probes']}
units = load(BASE / 'source-units/summary.json')
mapping = load(ROOT / 'artifacts/evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json')['by_validation_id']
margins = load(BASE / 'exact-order-margins.json')
q = 'qwen25-05b-instruct-frozen'
names = list(comparisons['new-v2']['runs'])
short = dict(zip(names, ['M4 MiniLM start (random head)', 'M4 MiniLM trained', 'M4 MARCO pretrained start', 'M4 MARCO trained', 'M2 retained', 'M3 retained', 'Uniform', 'Lexical', 'Qwen frozen']))
lines = []
def add(text=''):
    lines.append(text)
def table(headers, rows):
    add('| ' + ' | '.join(headers) + ' |')
    add('|' + '|'.join(['---'] * len(headers)) + '|')
    for row in rows:
        add('| ' + ' | '.join(map(str, row)) + ' |')
    add()
def cell(m):
    a = m['top_choice']['on_valid']
    return f"{a['numerator']}/{a['denominator']}; {m['log_loss']['mean']:.6f}; {m['brier']['mean']:.6f}"

add('# E5 quality — report candidate for owner review')
add('**Review draft, not final integration or a model-selection gate.** CPU-only analysis of the completed E5 execution. No new predictions, scoring definitions, thresholds, calibration, prompt changes, training, or default promotion. Evidence paths are relative to `/Users/destiner/Code/jeff/` unless absolute.\n')
add('## Recommendation')
add('**One bounded decoder-learning experiment is worth proposing, not starting.** The frozen decoder shows strong reused-probe performance and some new-rule ranking signal, but does not demonstrate net better probability quality or robust rules. Preserve encoder candidates and the frozen decoder comparator. Owner review is discretionary; no automated success gate is introduced.\n')
add('The useful learning question is whether one fixed supervised update can improve supplied-choice probability quality on independent training groups without sacrificing the observed probe/intent signal or aggravating reversal instability. Before execution, Model must choose and freeze one feasible learning recipe, obtain explicit compute and any new dependency authorization, and account for training memory (unmeasured here). Use existing authorized train data only; do not copy these validation failures, probes, or paraphrases into training. Retain this exact prompt/scoring recipe and references; evaluate with the existing scorer by stratum, family, source units, and both orders. Report costs and regressions for human review, not a newly tuned numerical pass threshold. No dynamic prompts, threshold search, architecture ablation, calibration or default change.\n')
add('## Scope and provenance')
table(['Stratum', 'Rows / declared groups', 'Label basis', 'Source units'], [
['Inherited-v1', '60 / 12', '40 teacher; 20 rule_verified', 'Intent/sentiment 5 groups each; rules 2 groups; related variants'],
['New-v2', '240 / 170', '160 teacher; 80 rule_verified', 'Intent/sentiment 80 singleton groups each, 8 domains and 2 producers per family; rules 40 policies / 10 mechanisms'],
['Reused probes', '24 / 12', '24 teacher; curator model unknown', '12 original/reversed groups, 4 per family; NOT 24 independent cases']])
add('Mapping is the explicit E3 reviewed `evaluation/e3-release-identity-review-v1/validation-source-units-reviewed.json`, joined by exact row ID, never parsed from IDs. Rule policy IDs come from reviewed provenance and mechanism names from assignments. Teacher aliases gpt-sol/openai/gpt-sol have no immutable revision; agreement is not independently verified correctness. Rule_verified means executable structured checks, not independent authorship or proof of every natural-language interpretation. New rules are held-out named mechanisms, with shared logical primitives; this is not D3 seen-mechanism evidence. Fresh authorship and reused development probes are not untouched final evidence.\n')
add('## All nine predictors: coverage and proper losses')
add('Cells: **correct/valid; natural-log loss; summed-option Brier** (lower losses better). Every run has full valid coverage: 60/60, 240/240, 24/24, respectively; zero missing/invalid/duplicate/extra/unidentifiable records. Conditional agreement therefore equals all-row success.\n')
table(['Predictor', 'Inherited-v1', 'New-v2', 'Probes'], [[short[n]] + [cell(comparisons[s]['runs'][n]['overall']) for s in comparisons] for n in names])
add('MiniLM start has a random scoring head, not an equally meaningful pretrained decision head; MARCO start retains its pretrained head. M2/M3 are retained historical trained systems. Uniform uses first-option tie breaking, not a random draw. Qwen has no ties; baseline tie counts remain in the source comparisons.\n')
add('## Complete family results (all nine family/stratum rows, all eight comparators)')
add('Cells retain correct/valid; log loss; Brier. Teacher agreement applies to intent/sentiment and all probes; rule_verified accuracy applies only to inherited/new rules.\n')
table(['Stratum / family / groups'] + [short[n] for n in names], [[f"{s} / {f} / {comparisons[s]['runs'][q]['per_family'][f]['groups']}"] + [cell(comparisons[s]['runs'][n]['per_family'][f]) for n in names] for s in comparisons for f in ['intent', 'rule_application', 'sentiment']])
add('### What matters')
add('- Qwen is 35/60 inherited (loss 1.194707, Brier .599128), 129/240 new (1.312350, .633492), and 20/24 probe presentations (.534509, .284486). M4 MiniLM and MARCO both have better inherited/new probability quality; MARCO also has more agreeing new labels (141 vs 129).')
add('- New rules: Qwen 25/80 vs MiniLM 15 and MARCO 21, but loss 1.765476 vs 1.343231 / 1.411166, even worse than uniform 1.303586. Ranking gain is weak evidence of useful rule signal, not reliable rule probabilities.')
add('- New sentiment is a hard regression: Qwen 30/80 vs 43 for either M4; loss 1.965885 vs .941779 / 1.249159. Inherited sentiment also regresses (9/20 vs 13 / 17). Intent and probes do not cancel these failures.')
add('- Probe gain is real on this reused development slice, not 20 independent wins: 9/12 groups are correct in BOTH orders; four groups per family offer limited breadth. No significance or calibration claims.\n')
add('## Exact reversal sensitivity')
orders = {s: {n: load(BASE / 'study' / s / (n + '-order-report.json')) for n in names} for s in comparisons}
table(['Stratum', 'Qwen flips / complete pairs', 'Both correct', 'Original-only / reversed-only / neither', 'Mean TV', 'Max option probability delta'], [[s, f"{o['pairs']-o['choice_consistency']['numerator']}/{o['pairs']}", o['both_correct'], f"{o['original_only_correct']} / {o['reversed_only_correct']} / {o['neither_correct']}", f"{o['mean_total_variation']:.6f}", f"{o['max_probability_change']:.6f}"] for s in orders for o in [orders[s][q]['overall']]])
add('All Qwen pairs complete, with no ties. TV is half the sum of absolute probability changes aligned by option identity. These are paired presentation observations, not independent sources.\n')
table(['Stratum / family', 'Orig correct', 'Rev correct', 'Both', 'Orig-only / rev-only / neither', 'Flips / pairs', 'Mean TV', 'Max delta'], [[f'{s} / {f}', o['both_correct']+o['original_only_correct'], o['both_correct']+o['reversed_only_correct'], o['both_correct'], f"{o['original_only_correct']} / {o['reversed_only_correct']} / {o['neither_correct']}", f"{o['pairs']-o['choice_consistency']['numerator']}/{o['pairs']}", f"{o['mean_total_variation']:.6f}", f"{o['max_probability_change']:.6f}"] for s in orders for f,o in orders[s][q]['per_family'].items()])
add('New rules fall 25→22/80 under reversal, only 4/80 cases correct both ways, with 65/80 choice flips; new sentiment is 30→29 with 14/80 both correct and 43/80 flips. Neither set is 80 independent sources: rules share 40 policies and 10 mechanisms; sentiment shares producers/domains. By contrast all six stored encoder systems have zero untied flips in every stratum (probabilities stable to tiny numerical noise); this is consistency, not correctness. Uniform flips are tie-driven despite unchanged probabilities; lexical untied choices are stable. Exact-order margins are preserved in the source artifact, without imposing a new margin threshold.\n')
add('## Source-unit results and hard regressions')
add('Equal-unit macros below come directly from the completed shared-scorer supplement, not a new metric implementation. Dimensions overlap; no iid, confidence interval or significance interpretation. Unknown metadata is not a fabricated unit. Inherited policy metadata and probe producer/domain/mechanism/policy metadata are absent; new intent/sentiment mechanisms/policies and new-rule domains are absent.\n')
selected = ['m4-minilm-trained', 'm4-msmarco-trained', q]
rows=[]
for s in comparisons:
    for f in ['intent','rule_application','sentiment']:
        ds = units['strata'][s]['runs'][q]['families'][f]['dimensions']
        dims = ['source_group'] + (['domain'] if s=='new-v2' and f!='rule_application' else []) + (['policy_instance','mechanism'] if s=='new-v2' and f=='rule_application' else [])
        for dim in dims:
            vals=[]
            for n in selected:
                mac=units['strata'][s]['runs'][n]['families'][f]['dimensions'][dim]['macro']
                vals.append(f"{mac['full_row_failure_as_unsuccessful_agreement']['value']:.4f}; {mac['valid_only_log_loss']['mean']:.6f}")
            rows.append([f'{s} / {f}',dim,ds[dim]['macro']['unit_count']]+vals)
table(['Stratum / family','Equal unit','Units']+[short[n]+' agreement; loss' for n in selected],rows)
add('### All ten named new-rule mechanisms (8 cases / 4 policies each)')
rows=[]
for g,m in comparisons['new-v2']['runs'][q]['per_source_group'].items():
    ref=next((v for v in mapping.values() if v['group_id']==g and v['stratum']=='new-v2'),None)
    if ref and ref['task_family']=='rule_application':
        rows.append([ref['mechanism'],g]+[cell(comparisons['new-v2']['runs'][n]['per_source_group'][g]) for n in selected])
table(['Reviewed mechanism','Group']+[short[n] for n in selected],rows)
add('### New sentiment domains: losses cannot be hidden by intent')
rows=[]
for unit in units['strata']['new-v2']['runs'][q]['families']['sentiment']['dimensions']['domain']['units']:
    vals=[]
    for n in selected:
        found=next(x for x in units['strata']['new-v2']['runs'][n]['families']['sentiment']['dimensions']['domain']['units'] if x['value']==unit['value'])
        vals.append(cell(found['metrics']))
    rows.append([unit['value']]+vals)
table(['Reviewed domain']+[short[n] for n in selected],rows)
add('Each domain has 10 singleton groups. Full group/policy metrics, including all 40 policies and every inherited/probe group, remain in the cited supplement; no claim that the macro erases local regressions.\n')
# Retain exact extracted summaries so review does not depend on Markdown rounding.
extracted={'status':'review-candidate-not-integrated','overall':{s:{n:d['overall'] for n,d in c['runs'].items()} for s,c in comparisons.items()},'qwen_order':{s:{k:v for k,v in orders[s][q].items() if k in ['overall','per_family','original','reversed','paired_quality']} for s in orders}}
(OUT/'extracted-evidence.json').write_text(json.dumps(extracted,indent=2)+'\n')
(OUT/'report-candidate.md').write_text('\n'.join(lines)+'\n')
(OUT/'input-receipt.json').write_text(json.dumps({'scope':'CPU extraction of existing scored outcomes only; no scoring/ML','inputs':inputs},indent=2)+'\n')
print('Wrote report-candidate.md, extracted-evidence.json, input-receipt.json')
