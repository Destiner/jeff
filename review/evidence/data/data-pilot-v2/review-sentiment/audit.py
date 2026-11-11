"""Read-only post-freeze audit; writes new review files only, never runs producers."""
import ast
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def constants(path, names):
    result = {}
    for node in ast.parse(path.read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'tuple':
                        result[target.id] = tuple(ast.literal_eval(node.value.args[0]))
                    else:
                        try:
                            result[target.id] = ast.literal_eval(node.value)
                        except ValueError:
                            # sentiment-b uses dict(zip(CLASSES, literal texts)); interpret only this static form.
                            result[target.id] = [dict(zip(('P','N','U','M'), ast.literal_eval(x.args[0].args[1]))) for x in node.value.elts]
    return result

result = {}
all_states = []
for producer in ('sentiment-a', 'sentiment-b'):
    base = ROOT / producer
    const = constants(base/'generate.py', {'OPTION_STYLES', 'STYLES', 'QUESTIONS'})
    styles = const.get('OPTION_STYLES', const.get('STYLES'))
    textmap = {text:(i,code) for i,style in enumerate(styles) for code,text in style.items()}
    cases = []
    heading = None
    for line in (base/'source_cases.txt').read_text().splitlines():
        if not line or line.startswith('#'): continue
        if line.startswith('@'): heading = line[1:]; continue
        if producer == 'sentiment-a': code,subject,state = line.split('|',2)
        else: code,state = line.split('|',1); subject = heading
        cases.append({'code':code,'subject':subject,'state':state,'heading':heading})
    by_group = {f'data:pilot-v2:{producer}:g{i:03d}':c for i,c in enumerate(cases,1)}
    assignments = json.loads((base/'group_assignments.json').read_text())['groups']
    stats = {}
    failures = []
    for split in ('train','validation'):
        rows = [json.loads(line) for line in (base/f'{split}.jsonl').read_text().splitlines()]
        recs = []
        for r in rows:
            case = by_group[r['group_id']]
            decoded = [textmap.get(o['text']) for o in r['options']]
            target = next(i for i,o in enumerate(r['options']) if o['id']==r['target_id'])
            style = decoded[0][0]
            code = decoded[target][1]
            qstyles = [i for i,q in enumerate(const['QUESTIONS']) if q.format(subject=case['subject'])==r['question']]
            checks = {'four_classes':len(decoded)==4 and {d[1] for d in decoded}=={'P','N','U','M'}, 'single_style':len({d[0] for d in decoded})==1,'source_label_matches_target':code==case['code'],'source_state_matches':r['state']==case['state'],'subject_question_exact':len(qstyles)==1,'assignment_split':assignments[r['group_id']]['split']==split}
            for name,passed in checks.items():
                if not passed: failures.append({'id':r['id'],'check':name})
            recs.append({'code':code,'position':target+1,'style':style,'question_style':qstyles[0],'domain':assignments[r['group_id']]['domain']})
            all_states.append(r['state'])
        stats[split] = {'rows':len(rows),'domains':dict(collections.Counter(x['domain'] for x in recs)), 'classes':dict(collections.Counter(x['code'] for x in recs)), 'target_positions':dict(collections.Counter(x['position'] for x in recs)), 'by_class':{code:{key:dict(sorted(collections.Counter(x[key] for x in recs if x['code']==code).items())) for key in ('position','style','question_style')} for code in ('P','N','U','M')}}
    result[producer] = {'splits':stats,'failures':failures,'source_cases':len(cases),'source_headings':len({x['heading'] for x in cases})}
result['combined']={'rows':len(all_states),'distinct_exact_states':len(set(all_states)),'distinct_case_and_punctuation_preserving_whitespace_normalized_states':len({' '.join(s.split()) for s in all_states})}
(HERE/'post-freeze-audit.json').open('x').write(json.dumps(result,indent=2))
print(json.dumps({'combined':result['combined'],'failures':{p:result[p]['failures'] for p in ('sentiment-a','sentiment-b')},'summary':{p:{s:{k:v for k,v in st.items() if k not in ('by_class','domains')} for s,st in result[p]['splits'].items()} for p in ('sentiment-a','sentiment-b')}},indent=2))
