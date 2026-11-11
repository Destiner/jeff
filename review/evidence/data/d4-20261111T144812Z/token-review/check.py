"""Fixed D4 selected-TRAIN rendering/token audit; no model imports."""
import ast
from collections import Counter, defaultdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
from tokenizers import Tokenizer

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
BASE = Path('/Users/destiner/Code/jeff')
HELPER = BASE / '.worktrees/data/experiments/research/audit_token_budget.py'
MODEL = BASE / '.worktrees/model/src/jeff/model'
TOKENIZER = BASE / 'artifacts/research/tokenizer-audit-20261111T1029/tokenizer.json'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name, value):
    with (OUT / name).open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False); f.write('\n')
rows = [json.loads(line) for line in (ROOT / 'selected-reference.jsonl').read_text().splitlines() if line.strip()]
selection = json.loads((ROOT / 'selection.json').read_text())
pins = {s['id']: s for s in selection['selection']}
assert len(rows) == len(pins) == 24
assert {r['id'] for r in rows} == set(pins)
assert all(r['split'] == 'train' and r['group_id'] == pins[r['id']]['group_id'] for r in rows)
# Read formatter expressions as syntax only; never import either model module.
formatters = {}
for name in ('scorer.py', 'cross_encoder.py'):
    tree = ast.parse((MODEL / name).read_text())
    first = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'context' for t in n.targets))
    second = next(n.args[0] for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'second' and n.func.attr == 'append')
    formatters[name] = (compile(ast.Expression(first), name, 'eval'), compile(ast.Expression(second), name, 'eval'))
full = Tokenizer.from_file(str(TOKENIZER)); full.no_padding(); full.no_truncation()
capped = Tokenizer.from_file(str(TOKENIZER)); capped.no_padding(); capped.enable_truncation(256, strategy='longest_first', direction='right')
def signature(enc):
    return [(s, off, tok) for s, off, tok, special in zip(enc.sequence_ids, enc.offsets, enc.ids, enc.special_tokens_mask) if not special]
rendered = []
groups = defaultdict(lambda: {'rows': 0, 'pairs': 0, 'lengths': [], 'over_budget_pairs': 0, 'state_loss_pairs': 0, 'question_loss_pairs': 0, 'choice_loss_pairs': 0, 'token_identity_loss_pairs': 0})
for row in rows:
    pin = pins[row['id']]
    group = groups[pin['group_id']]; group['rows'] += 1
    group['source_shard'] = pin['shard']
    # Formatter evaluation receives ONLY the actual state/question and choice text.
    input_row = {k: row[k] for k in ('state', 'question')}
    first = eval(formatters['scorer.py'][0], {'__builtins__': {}}, {'row': input_row})
    qstart = len('State:\n' + row['state'] + '\nQuestion:\n')
    state_start, state_end = len('State:\n'), len('State:\n' + row['state'])
    for option in row['options']:
        text_option = {'text': option['text']}
        second = eval(formatters['scorer.py'][1], {'__builtins__': {}}, {'option': text_option})
        assert first == f"State:\n{row['state']}\nQuestion:\n{row['question']}"
        assert second == 'Candidate:\n' + option['text']
        for a, b in formatters.values():
            assert eval(a, {'__builtins__': {}}, {'row': input_row}) == first
            assert eval(b, {'__builtins__': {}}, {'option': text_option}) == second
        ref, cap = full.encode(first, second), capped.encode(first, second)
        missing = Counter(signature(ref)) - Counter(signature(cap))
        losses = Counter()
        for (seq, (start, end), token), count in missing.items():
            if seq == 0 and end > state_start and start < state_end: losses['state'] += count
            if seq == 0 and end > qstart: losses['question'] += count
            if seq == 1 and end > len('Candidate:\n'): losses['choice'] += count
        group['pairs'] += 1; group['lengths'].append(len(ref.ids))
        group['over_budget_pairs'] += int(len(ref.ids) > 256)
        group['token_identity_loss_pairs'] += bool(missing)
        for field in ('state', 'question', 'choice'): group[field + '_loss_pairs'] += bool(losses[field])
        rendered.append({'row_id': row['id'], 'option_id': option['id'], 'group_id': row['group_id'], 'first': first, 'second': second, 'full_tokens': len(ref.ids), 'native256_tokens': len(cap.ids), 'lost_tokens': dict(losses), 'exact_token_ids_preserved': ref.ids == cap.ids})
with (OUT / 'rendered-pairs.jsonl').open('x') as f:
    for pair in rendered: f.write(json.dumps(pair, ensure_ascii=False) + '\n')
for group in groups.values():
    lengths = group.pop('lengths'); group['min_tokens'] = min(lengths); group['max_tokens'] = max(lengths)
manifest = {'dataset_id': 'D4-audit-only-selected24-old-TRAIN', 'shards': [{'path': 'selected-reference.jsonl', 'split': 'train', 'rows': 24, 'sha256': sha(ROOT / 'selected-reference.jsonl')}]}
save('subset-manifest.json', manifest)
subprocess.run([sys.executable, '-B', str(HELPER), '--manifest', str(OUT / 'subset-manifest.json'), '--artifacts-dir', str(ROOT), '--tokenizer', str(TOKENIZER), '--tokenizer-source', 'existing pinned local tokenizer JSON; no model load', '--max-length', '256', '--output', str(OUT / 'helper-report.json')], check=True)
inputs = [HELPER, TOKENIZER, MODEL / 'scorer.py', MODEL / 'cross_encoder.py', ROOT / 'selection.json', ROOT / 'selected-reference.jsonl', Path(__file__)]
save('review.json', {'rows': len(rows), 'pairs': len(rendered), 'source_groups': len(groups), 'native_cap': 256, 'token_min': min(p['full_tokens'] for p in rendered), 'token_max': max(p['full_tokens'] for p in rendered), 'all_exact_token_ids_preserved': all(p['exact_token_ids_preserved'] for p in rendered), 'groups': dict(groups), 'inputs_sha256': {str(p): sha(p) for p in inputs}, 'tokenizers_version': importlib.metadata.version('tokenizers'), 'consumer_identity': 'Current Model worktree scorer.py CandidateScorer and cross_encoder.py RetainedCrossEncoder; AST-only formatter extraction; no imports/initialization. SHA256 identities above, no Git used.', 'input_check': 'All actual rendered pairs equal state/question/choice-only templates in both consumers. Formatter expressions evaluated with state/question and option.text only; IDs/targets/provenance are audit metadata, never formatter inputs.', 'limits': 'Selected24 purposive dependent old TRAIN only; 14 source groups. Existing full-v2 audit already passed256; current selected-input cross-check, not new discovery. Truncation is not demonstrated on this sample; no claim all data or model learning is sound. No extra examples read; no model execution. No128 contrast run.'})
print(json.dumps({'rows': len(rows), 'pairs': len(rendered), 'groups': len(groups), 'min': min(p['full_tokens'] for p in rendered), 'max': max(p['full_tokens'] for p in rendered), 'all_exact': all(p['exact_token_ids_preserved'] for p in rendered)}))
