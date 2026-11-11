"""Deterministic, CPU-only immutable candidate revision; no model predictions.
Run once in a NEW output directory containing this script, with sibling ordering/.
Uses only parent ordering/ inputs. Exclusive creation; no overwrites, no imports
with side effects, no original audit main. No third-party packages required.
"""
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import importlib.util
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

OUT = Path(__file__).resolve().parent
PARENT = OUT.parent / 'ordering'
JOB = 'data-d3-seen-rules-v1-ordering-r2'
AUTHOR = {'provider': os.environ.get('PI_PROVIDER'), 'model_alias': os.environ.get('PI_MODEL'), 'immutable_revision': None}
if not all(AUTHOR[k] for k in ('provider', 'model_alias')):
    raise RuntimeError('Actual revision author PI_PROVIDER and PI_MODEL required')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def encode(x):
    return (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()

def save(name, data):
    with (OUT / name).open('xb') as f:
        f.write(data)

def dump(name, x):
    save(name, encode(x))

def load(name):
    return [json.loads(s) for s in (PARENT / name).read_text().splitlines()]

parent_hashes = {p.name: sha(p.read_bytes()) for p in sorted(PARENT.iterdir()) if p.is_file()}
parent_meta = json.loads((PARENT / 'metadata.json').read_text())
# Copy the pure audit helper, including its old authoring main, byte-for-byte.
# Never execute that main: its old provenance and on-grid assumptions are obsolete.
for name in ['audit.py', 'audit_cases.jsonl', 'source_cases.jsonl', 'group_assignments.json']:
    save(name, (PARENT / name).read_bytes())
spec = importlib.util.spec_from_file_location('parent_audit', OUT / 'audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
old = load('validation.jsonl')
rows = copy.deepcopy(old)
cases = load('audit_cases.jsonl')
sources = load('source_cases.jsonl')
assignments = json.loads((PARENT / 'group_assignments.json').read_text())['groups']

# Explicit misconceived-operation programs, not offsets from a target.
# Each triple lists the three wrong programs in authored order, before an
# ID-seeded, label-independent permutation into the existing wrong slots.
DISCOUNT = {
'p01:c01': [('reverse', 'Reverse the two reductions'), ('skip_percent', 'Omit percentage reduction'), ('double_fixed', 'Apply the booking credit twice')],
'p01:c02': [('reverse', 'Reverse the two reductions'), ('double_fixed', 'Apply the booking credit twice'), ('percent_as_cash', 'Read 20 percent as a £20 credit')],
'p02:c01': [('reverse', 'Deduct voucher before percentage'), ('skip_fixed', 'Omit voucher'), ('skip_percent', 'Omit trade reduction')],
'p02:c02': [('reverse', 'Deduct voucher before percentage'), ('skip_fixed', 'Omit voucher'), ('fixed_as_percent', 'Read £9 voucher as a sequential 9 percent reduction')],
'p03:c01': [('reverse', 'Reverse all three steps'), ('fixed_last', 'Apply both fixed credits after percentage'), ('double_last_fixed', 'Apply the final site credit twice')],
'p03:c02': [('skip_first', 'Omit installation credit'), ('reverse', 'Reverse all three steps'), ('skip_percent', 'Omit percentage reduction')],
'p04:c01': [('original_base', 'Calculate each percentage reduction from the original invoice'), ('fixed_last', 'Move fixed credit after both percentages'), ('double_fixed', 'Apply the fixed credit twice at its step')],
'p04:c02': [('skip_fixed', 'Omit fixed credit'), ('add_percent', 'Add percentage rates and apply them before fixed credit'), ('reverse', 'Reverse all three steps')],
'p05:c01': [('add_percent', 'Add membership and early-booking percentages'), ('fixed_last', 'Deduct fixed credit after both percentages'), ('skip_first_percent', 'Omit membership percentage')],
'p05:c02': [('skip_fixed', 'Omit fixed credit'), ('skip_first_percent', 'Omit membership percentage'), ('skip_last_percent', 'Omit early-booking percentage')],
'p06:c01': [('fixed_first', 'Deduct reuse credit before both percentages'), ('fixed_last', 'Deduct reuse credit after both percentages'), ('add_percent', 'Add percentage rates and apply before fixed credit')],
'p06:c02': [('reverse', 'Reverse all three steps'), ('fixed_first', 'Deduct reuse credit before both percentages'), ('skip_fixed', 'Omit reuse credit')],
}

def discount_value(c, code):
    base = F(c['facts']['base'])
    steps = [(op, F(v)) for op, v in c['policy']['steps']]
    if code == 'original_base':
        return base - sum(v if op == 'fixed' else base*v/100 for op, v in steps)
    if code == 'add_percent':
        total = sum(v for op, v in steps if op == 'percent')
        first = next(i for i,s in enumerate(steps) if s[0] == 'percent')
        steps = [s if s[0] == 'fixed' else ('percent',total) for i,s in enumerate(steps) if s[0] == 'fixed' or i == first]
    elif code == 'reverse':
        steps = steps[::-1]
    elif code in ('fixed_first', 'fixed_last'):
        first = 'fixed' if code == 'fixed_first' else 'percent'
        steps = [s for s in steps if s[0] == first] + [s for s in steps if s[0] != first]
    elif code in ('skip_percent', 'skip_fixed'):
        skip = code.removeprefix('skip_')
        steps = [s for s in steps if s[0] != skip]
    elif code == 'skip_first':
        steps = steps[1:]
    elif code in ('skip_first_percent', 'skip_last_percent'):
        ix = [i for i, s in enumerate(steps) if s[0] == 'percent']
        steps.pop(ix[0] if code == 'skip_first_percent' else ix[-1])
    elif code == 'double_fixed':
        steps = [s for s in steps for _ in range(2 if s[0] == 'fixed' else 1)]
    elif code == 'double_last_fixed':
        steps = steps + [next(s for s in reversed(steps) if s[0] == 'fixed')]
    elif code == 'percent_as_cash':
        steps = [('fixed', v) for op, v in steps]
    elif code == 'fixed_as_percent':
        steps = [('percent', v) for op, v in steps]
    else:
        raise ValueError(code)
    v = base
    for op, a in steps:
        v = v-a if op == 'fixed' else v*(100-a)/100
    return v

# Wrong-grid or wrong-mode programs. Grid and mode are explicit; amounts are
# computed from the measured value, never supplied as filler or target offsets.
ROUNDING = {
'p01:c01': [('0.1','floor'), ('1','nearest'), ('0.2','floor')],
'p01:c02': [('0.1','ceil'), ('0.5','ceil'), ('1','ceil')],
'p02:c01': [('5','tie_down'), ('1','floor'), ('1','nearest')],
'p02:c02': [('5','ceil'), ('1','nearest'), ('2','ceil')],
'p03:c01': [('0.01','tie_down'), ('1','nearest'), ('0.1','ceil')],
'p03:c02': [('0.01','ceil'), ('0.1','nearest'), ('0.05','ceil')],
'p04:c01': [('10','tie_down'), ('5','nearest'), ('100','nearest')],
'p04:c02': [('10','ceil'), ('1','nearest'), ('100','nearest')],
'p05:c01': [('0.5','tie_down'), ('0.1','nearest'), ('1','ceil')],
'p05:c02': [('0.5','floor'), ('0.1','nearest'), ('1','floor')],
'p06:c01': [('2','tie_down'), ('1','nearest'), ('10','floor')],
'p06:c02': [('2','ceil'), ('1','nearest'), ('5','ceil')],
}

def rounded(value, grid, mode):
    v, g = F(value), F(grid)
    q = v // g
    if mode == 'floor':
        return q*g
    if mode == 'ceil':
        return (q + (v != q*g))*g
    if mode == 'tie_down':
        return (q + (v-q*g > g/2))*g
    if mode == 'nearest':
        return (q + (v-q*g >= g/2))*g
    raise ValueError(mode)

def allocation(c, priority):
    stock = {b[0]: b[2] for b in c['facts']['batches']}
    left = c['facts']['request']
    take = dict.fromkeys(stock, 0)
    for name in priority:
        take[name] = min(left, stock[name])
        left -= take[name]
    assert left == 0
    return '; '.join(f'{n} {take[n]}' for n in sorted(take))

def seed_order(key, values):
    return sorted(values, key=lambda x: sha((key+'|'+json.dumps(x, sort_keys=True)).encode()))

changes = []
construction = []
for r, c, src, original in zip(rows, cases, sources, old):
    assert r['id'] == c['id'] == src['id']
    assert {k:v for k,v in c.items() if k != 'display_order'} == src
    m = c['mechanism_id']
    key = ':'.join(c['id'].split(':')[-2:])
    answer = audit.expected(c)
    candidates = []
    if m == 'discount':
        for code, why in DISCOUNT[key]:
            candidates.append({'text': '£'+audit.fixed(discount_value(c,code),2), 'rule_error': code, 'description': why})
    elif m == 'rounding':
        for grid, mode in ROUNDING[key]:
            candidates.append({'text': audit.fixed(rounded(c['facts']['value'],grid,mode),c['policy']['places'])+' '+c['policy']['unit'], 'rule_error': {'grid':grid,'mode':mode}, 'description': 'Use grid '+grid+' with '+mode+' instead of the stated nearest/half-up grid'})
    elif m == 'fifo':
        # Enumerate ALL greedy priority permutations, remove correct and duplicate
        # allocations, then ID-hash order. No zero-count or label-rank selection.
        priorities = itertools.permutations(sorted(b[0] for b in c['facts']['batches']))
        seen = {answer}
        for priority in seed_order(c['id']+'|priority', list(priorities)):
            text = allocation(c,priority)
            if text not in seen:
                candidates.append({'text':text, 'rule_error':{'priority':list(priority)}, 'description':'Exhaust batches in priority order '+', '.join(priority)+' instead of increasing arrival number'})
                seen.add(text)
        candidates = candidates[:len(r['options'])-1]
    if m != 'lexicographic':
        assert len(candidates) == len(r['options'])-1
        assert len({answer} | {x['text'] for x in candidates}) == len(r['options'])
        candidates = iter(seed_order(c['id']+'|wrong_slots',candidates))
        for slot, o in enumerate(r['options'],1):
            if o['id'] != r['target_id']:
                candidate = next(candidates)
                construction.append({'id':r['id'], 'option_id':o['id'], 'slot':slot, **candidate})
                o['text'] = candidate['text']
    r['provenance']['source'] = JOB
    r['provenance']['teacher_model'] = 'openai/gpt-sol'
    # Full recursive field-level change map, including metadata-only changes.
    for before, after in zip(original['options'],r['options']):
        if before['text'] != after['text']:
            changes.append({'id':r['id'],'field':'options.'+after['id']+'.text','old':before['text'],'new':after['text']})
    for field in ['source','teacher_model']:
        changes.append({'id':r['id'],'field':'provenance.'+field,'old':original['provenance'][field],'new':r['provenance'][field]})

save('validation.jsonl', ''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows).encode())
dump('distractor_constructions.json',construction)
dump('change_map.json',changes)
dump('parent_refs.json', {'path':str(PARENT), 'file_sha256':parent_hashes, 'metadata':parent_meta})

def take_values(text):
    return {s.rsplit(' ',1)[0]:int(s.rsplit(' ',1)[1]) for s in text.split('; ')}

def numeric(text,m):
    return F(text[1:]) if m == 'discount' else F(text.split()[0])

def summarize(rs):
    summary = {}
    details = []
    for m in ['lexicographic','fifo','discount','rounding']:
        selected = [r for r,c in zip(rs,cases) if c['mechanism_id']==m]
        d = {'rows':len(selected),'target_slots':Counter(), 'first_choice_hits':0, 'shortest_first_tie_hits':0,'longest_first_tie_hits':0,'shortest_fractional_credit':0,'longest_fractional_credit':0,'unique_shortest_targets':0,'unique_longest_targets':0,'numeric_target_ranks':Counter(),'numeric_min_first_tie_hits':0,'numeric_max_first_tie_hits':0,'numeric_median_lower_hits':0,'numeric_interior_targets':0,'discount_unique_v_plus1_minus2_candidates':0,'discount_unique_v_plus1_minus2_correct':0,'fifo_most_zeros_first_tie_hits':0,'fifo_fewest_zeros_first_tie_hits':0,'fifo_target_zero_counts':Counter(),'numeric_decimal_places':Counter(),'numeric_target_last_digit':Counter()}
        for r in selected:
            ts = [o['text'] for o in r['options']]
            i = [o['id'] for o in r['options']].index(r['target_id'])
            d['target_slots'][str(i+1)]+=1
            d['first_choice_hits'] += i==0
            ls = list(map(len,ts))
            row = {'id':r['id'],'target_slot':i+1,'character_lengths':ls,'target_character_length':ls[i]}
            for extreme,label in [(min,'shortest'),(max,'longest')]:
                ix = [j for j,l in enumerate(ls) if l==extreme(ls)]
                d[label+'_first_tie_hits'] += i==ix[0]
                d[label+'_fractional_credit'] += (1/len(ix) if i in ix else 0)
                d['unique_'+label+'_targets'] += ix==[i]
            if m in ('discount','rounding'):
                ns = [numeric(t,m) for t in ts]
                rank = sorted(ns).index(ns[i])+1
                d['numeric_target_ranks'][str(rank)] += 1
                d['numeric_interior_targets'] += 1<rank<len(ns)
                d['numeric_min_first_tie_hits'] += i==ns.index(min(ns))
                d['numeric_max_first_tie_hits'] += i==ns.index(max(ns))
                d['numeric_median_lower_hits'] += ns[i]==sorted(ns)[(len(ns)-1)//2]
                row['numeric_values'] = [str(n) for n in ns]
                row['target_numeric_rank'] = rank
                for t in ts:
                    n = t[1:] if m=='discount' else t.split()[0]
                    d['numeric_decimal_places'][str(len(n.split('.')[1]) if '.' in n else 0)] += 1
                d['numeric_target_last_digit'][ts[i][-1] if m=='discount' else ts[i].split()[0][-1]] += 1
                if m == 'discount':
                    candidates = [j for j,v in enumerate(ns) if v+1 in ns and v-2 in ns]
                    row['v_plus1_minus2_slots'] = [j+1 for j in candidates]
                    d['discount_unique_v_plus1_minus2_candidates'] += len(candidates)==1
                    d['discount_unique_v_plus1_minus2_correct'] += candidates==[i]
            if m == 'fifo':
                zs = [sum(q==0 for q in take_values(t).values()) for t in ts]
                d['fifo_most_zeros_first_tie_hits'] += i==zs.index(max(zs))
                d['fifo_fewest_zeros_first_tie_hits'] += i==zs.index(min(zs))
                d['fifo_target_zero_counts'][str(zs[i])]+=1
                row['option_zero_counts'] = zs
                row['target_zero_count'] = zs[i]
            details.append(row)
        summary[m] = d
    return {'by_mechanism':summary,'per_row':details}

# Same-author dataset consistency audit, not software tests or independent text
# verification. Pure expected/stated are byte-identical to the approved helper.
results = []
invariants = Counter()
for before,r,c,src in zip(old,rows,cases,sources):
    for field in before:
        if field not in ('options','provenance'):
            assert r[field] == before[field]
    assert [o['id'] for o in r['options']] == [o['id'] for o in before['options']]
    target = next(o['text'] for o in r['options'] if o['id']==r['target_id'])
    old_target = next(o['text'] for o in before['options'] if o['id']==before['target_id'])
    assert target == old_target == audit.expected(c)
    assert (r['state'],r['question']) == audit.stated(c)
    assert {k:v for k,v in c.items() if k!='display_order'} == src
    assert len({o['text'] for o in r['options']}) == len(r['options'])
    assert len({o['id'] for o in r['options']}) == len(r['options'])
    assert r['split']=='validation' and r['provenance']['usage']=='validation_only_never_train'
    assert r['provenance']['label_basis']==before['provenance']['label_basis']
    g = assignments[r['group_id']]
    assert g['mechanism_id']==c['mechanism_id'] and g['policy_domain']==c['policy_domain'] and g['split']=='validation'
    if c['mechanism_id']=='fifo':
        stock = {b[0]:b[2] for b in c['facts']['batches']}
        for o in r['options']:
            take = take_values(o['text'])
            assert set(take)==set(stock) and sum(take.values())==c['facts']['request']
            assert all(0<=v<=stock[n] for n,v in take.items())
    if c['mechanism_id'] in ('rounding','discount'):
        for o in r['options']:
            assert numeric(o['text'],c['mechanism_id']) >= 0
            n = o['text'][1:] if c['mechanism_id']=='discount' else o['text'].split()[0]
            places = 2 if c['mechanism_id']=='discount' else c['policy']['places']
            assert n == audit.fixed(F(n),places)
            if c['mechanism_id']=='rounding':
                assert o['text'].split()[1] == c['policy']['unit']
    results.append({'id':r['id'],'expected_text':audit.expected(c),'old_target_text':old_target,'target_text':target,'agreement':True,'rendered_text_fact_match':True})
    invariants['all_facts_policy_state_question_ids_group_split_arity_order_target_preserved']+=1
assert len(rows)==48 and len(assignments)==24
assert Counter(r['group_id'] for r in rows)==dict.fromkeys(assignments,2)
assert Counter(c['mechanism_id'] for c in cases)==dict.fromkeys(['lexicographic','fifo','discount','rounding'],12)
assert {p.name:sha(p.read_bytes()) for p in PARENT.iterdir() if p.is_file()} == parent_hashes
row_hashes = []
for old_line,new_line,r in zip((PARENT/'validation.jsonl').read_bytes().splitlines(),(OUT/'validation.jsonl').read_bytes().splitlines(), rows):
    row_hashes.append({'id':r['id'],'parent_row_sha256':sha(old_line),'revised_row_sha256':sha(new_line)})
report = {'schema_version':'0.1','revision':JOB,'audit_type':'same_author_expected_and_rendered_consistency_no_independent_verification','rows':48,'groups':24,'expected_agreement':48,'rendered_text_fact_matches':48,'failure_count':0,'invariants':dict(invariants),'parent_files_unchanged':True,'row_hash_convention':'Exact UTF-8 JSONL row bytes excluding LF; full files hashed separately','row_hashes':row_hashes,'case_results':results,'old':summarize(old),'new':summarize(rows),'scope':'Choice-only descriptive CPU diagnostics; no predictions, model execution, training, held-out inference or independent text verification. No historical inputs accessed.'}
dump('validation_report.json',report)

review = '''# Ordering r2: immutable choice-construction revision

Only wrong option text and per-row provenance source/teacher representation changed.
All 48 target texts, target IDs/slots, ordered option IDs, arities, facts, policy
wording, questions, states, stable row/group IDs, named assignment plan and split
are preserved. This is a new candidate identity; IDs name the same policy cases,
not new independent examples. Validation only, including every derivative.

## Construction and helper handling

`distractor_constructions.json` records every revised wrong slot and its generating
misapplication. Discount errors are explicit wrong-order, omitted/repeated-step,
wrong-base, cash/percent confusion and additive-percent programs. Rounding errors
are computed from the measured value using named wrong grids, tie directions or
floor/ceiling modes. All option numbers retain the target's stated precision and
unit; no arbitrary offsets or padding. FIFO alternatives greedily exhaust different
batch priorities, selected by ID-hashed permutation enumeration, deduplicating
allocations before selection. Every FIFO choice meets demand and capacities.
The exact programs and per-case selections are in `revise.py`; no search over
heuristic scores, reauthoring of facts or target changes was performed.

`audit.py`, `audit_cases.jsonl`, `source_cases.jsonl` and assignments are byte-identical
copies. Source cases contain only policies/facts, not distractor descriptions, so
there are no stale distractor descriptions to replace. Pure `expected` and `stated`
were imported with bytecode disabled, without running the helper main. No helper
edit was needed. The copied helper's OLD authoring main is intentionally NOT the r2
validator: it assumes old provenance and all rounding distractors on the correct
grid. Off-grid wrong-grid answers are now intentional; `revise.py` validates units,
precision, uniqueness, nonnegative values and recorded construction instead.
The parent authoring/generator/finalization scripts were not executed or copied as
r2 entry points. `revise.py` is the revision/audit entry point and refuses overwrites.
To reproduce, copy it alone to a fresh sibling output directory of `ordering/`
and invoke with actual PI_PROVIDER/PI_MODEL set. It never mutates parent files.

## Provenance

Teacher is actual source alias openai/gpt-sol; source teacher_model object was
normalized to its equivalent string, a metadata-only change. Revision author is
recorded from actual PI_PROVIDER/PI_MODEL, not inferred from source. No new model
calls or costs occurred; source authoring attribution is preserved separately from
revision authorship. Parent metadata and every source file hash are in
`parent_refs.json`; exact old/new JSONL row hashes and full expected recomputation
are in `validation_report.json`. Manifest hashes distinguish the immutable drafts.

## Interpretation and limits

Same-author expected recomputation and exact rendered state/question reconstruction
passed 48/48 each. This is arithmetic/renderer consistency, NOT independently
verified natural-language correctness. Descriptive old/new shortcut counts and
per-row evidence follow in `validation_report.json`. First/length diagnostics use
first-option tie-break; fractional length credits are also included. Numeric ranks,
extremes, lower median, decimal formats, terminal digits and FIFO most/fewest-zero
choices are inspected, not treated as held-out shortcut accuracy. Arity and target
slots are intentionally immutable. A correct FIFO allocation with two zero batches
has an unavoidable depletion signature at low demand; boundary cases remain easy.
No claim that options alone are statistically independent of labels is warranted
from 12 cases/mechanism. Wrong rounding grids are pedagogically meaningful but can
sometimes be rejected by grid membership. Omitted-discount errors often increase
an amount. Paired dependence, repeated policies, common author/templates and small
sample size remain limitations. No hidden or final data, history, model predictions,
network, API, training, spend, Git, mailbox, tests or lint were used.
'''
save('generation_review.md',review.encode())
meta = copy.deepcopy(parent_meta)
meta['shard_id'] = JOB
meta['source_job'] = JOB
meta['revision_author'] = AUTHOR
meta['parent'] = {'directory':str(PARENT),'metadata_sha256':parent_hashes['metadata.json'],'validation_sha256':parent_hashes['validation.jsonl'],'all_refs':'parent_refs.json'}
meta['changed_field_scope'] = ['options[].text where id != target_id (discount, rounding, fifo only)','provenance.source (all rows)','provenance.teacher_model equivalent object-to-string normalization (all rows)']
meta['preserved_meanings'] = ['all states/questions/policy and source facts','all IDs/group/split/arity/ordered option IDs','all correct target IDs, slots and exact texts','all named policy group assignments','expected(case) semantics and audit cases','validation_only_never_train']
meta['generation_settings']['parent_generation_settings'] = parent_meta['generation_settings']
meta['generation_settings']['method'] = 'Deterministic standard-library CPU choice-only r2; explicit rule misapplications; unchanged pure expected/stated audit'
meta['generation_settings']['choice_shuffle'] = 'Existing target slots and ordered option IDs unchanged; wrong constructions ID-SHA256 shuffled within wrong slots only'
meta['generation_settings']['revision_script'] = 'revise.py'
meta['generation_settings']['revision_script_sha256'] = sha((OUT/'revise.py').read_bytes())
meta['generation_settings']['hashes'] = {p.name:sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file()}
meta['verification'] = {'kind':'same_author_expected_and_rendered_consistency','agreement_rows':48,'rendered_text_fact_matches':48,'failures':0,'independent_authorship':False,'report':'validation_report.json','review':'generation_review.md','tokenizer_audit':'not performed; no model/tokenizer jobs'}
meta['limitations'] += ['Revised after exposed choice-only weaknesses; not untouched validation.','Residual shortcut measurements descriptive, 12 cases per mechanism; no independence claim.','Pure copied audit helpers used; copied authoring main is parent-only and must not be run as r2 validator.','No independent verification of rendered text correctness.']
dump('metadata.json',meta)
manifest = {'schema_version':'0.1','dataset_id':JOB,'usage':'validation_only_never_train','parent_validation_sha256':parent_hashes['validation.jsonl'],'shards':[{'path':'data/data-d3-seen-rules-v1/ordering-r2/validation.jsonl','split':'validation','sha256':sha((OUT/'validation.jsonl').read_bytes()),'rows':48}], 'files':{p.name:sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file()},'freeze':'All payload files finalized before this manifest; manifest self-hash reported separately at handoff.'}
dump('manifest.json',manifest)
print(json.dumps({'rows':48,'expected_agreement':48,'text_fact_matches':48,'parent_unchanged':True,'manifest_sha256':sha((OUT/'manifest.json').read_bytes()),'summary':report['new']['by_mechanism']},ensure_ascii=False))
