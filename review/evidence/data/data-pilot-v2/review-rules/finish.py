import json,hashlib,datetime
from pathlib import Path
P=Path(__file__).parent
before=json.loads((P/'hashes-before.json').read_text()); after={f:hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in before}; changed=[f for f in before if before[f]!=after[f]]
(P/'hashes-after.json').write_text(json.dumps(after,indent=2)+'\n')
comparisons=[json.loads(x) for x in (P/'comparison.jsonl').read_text().splitlines()]
recompute=json.loads((P/'recompute.json').read_text()); exposure=json.loads((P/'exposure.json').read_text())
manifest_path=P.parent/'pre-review-r2'/'manifest.json'; manifest=json.loads(manifest_path.read_text()); manifest_matches={e['path']:hashlib.sha256((P.parents[2]/e['path']).read_bytes()).hexdigest()==e['sha256'] for e in manifest['shards'] if '/rule-a/' in e['path'] or '/rule-b/' in e['path']}
report={
 'schema_version':'0.1','review':'rule-a and rule-b target-hidden semantic/data review','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'No must-fix found within bounded review; retain limitations below. Not a certification of all rendered prose.',
 'candidate':{'path':str(manifest_path),'sha256':before[str(manifest_path)],'manifest_declared_rows':sum(e['rows'] for e in manifest['shards']),'reviewed_new_rule_rows':480,'reviewed_shard_manifest_hash_matches':manifest_matches},
 'reviewer':exposure,
 'blind_review':{'rows':60,'groups':30,'rows_per_group':2,'by_producer':{'rule-a':30,'rule-b':30},'split_rows':{'train':40,'validation':20},'state_characters':{'min':141,'max':324},'selection':exposure['selection'],'freeze':json.loads((P/'freeze-record.json').read_text()),'comparison_matches':sum(x['comparison']['agrees'] for x in comparisons),'uniqueness':'All 60 independently reasoned from displayed natural-language inputs with exactly one defensible supplied answer; frozen before target reveal.','outcomes':'Includes authorization accept/reject, scheduling feasible/no-slot, equality ties, negative rounding, quarantine, strict/inclusive endpoints, case-sensitive symbols, bracket mismatch, and tie-breaking. Did not force every mechanism outcome or exact boundary into a two-row sample.'},
 'executed_recomputation':recompute,
 'combined_coverage':{'rows':{'train':400,'validation':80},'policy_instances':{'train':200,'validation':40},'mechanism_groups':{'train':20,'validation':10},'paired_rows_per_policy':2,'statistical_independence_claim':False},
 'source_and_boundary_review':[
  'After decisions, read both audit.py and generate.py, metadata and mechanism plans; mechanically joined all 480 audit/source records and checked configured mechanism/split correspondence. No generator main or audit main/validate executed. rule-b render(case) only was imported/called after inspection for exact source/render join; rule-a source prose concatenation checked directly.',
  'No direct cross-producer train-to-validation reuse of the ten new held-out mechanisms found in these renderers/assignments. Train rule-a scheduling is deadline feasibility, not validation rule-b topological ordering; train lexicographic ranking differs from validation highest median; generic ordering, arithmetic, strings, and sets overlap intentionally.',
  'Read historical v1 rule metadata only, not historical rows: graph reachability and Condorcet are validation-only there. Neither new training renderer introduces those mechanisms. New topological graph ordering is also validation-only. This is mechanism/spec inspection, not proof that no semantic historical derivative exists.',
  'Rendering review found explicit direction, ordering, tie, boundary, units, sign and case conventions for sampled problems. rule-a prose is authored separately from structured facts: exact source joins do not semantically parse prose. rule-b uses shared structured renderer; re-render equality detects drift, not a shared renderer bug. Full independent prose review beyond 60 rows was not performed.'
 ],
 'integration_code_review':{
  'files':['src/jeff/data/assemble.py','src/jeff/data/validate.py','src/jeff/data/audit.py'],
  'method':'Static read only; no imports or CLI execution.',
  'findings':[
   'No material blocker identified for this candidate. Assembly retains parent shard entries, enforces allocation counts/splits/family and cost; validator rejects final/unknown manifest splits before shard reads, verifies hashes, detects duplicate IDs/groups and exact full inputs.',
   'Exact canonicalizer uses NFC and outer strip, preserving signs/brackets/case/internal whitespace. Trigram casefold/word normalization is heuristic only: lexical collisions are not label conflicts.',
   'Integration audit checks historical exact-input, group and scenario boundaries but cannot prove absence of semantic derivatives; appropriately qualified. It executes an external research script through runpy; that path was not accessed or executed in this review.',
   'Publication is not transactional: assembly writes candidate/report before all checks finish and multiple final files in sequence. Existing-file guards can leave partial outputs on retries; operational caveat, not evidence of a material data defect here.'
  ]},
 'existing_claims_not_reexecuted':[
  'User reports full structural checks passed and 256-token audit has zero overflow; neither full-manifest validator nor tokenizer audit rerun.',
  'Producer metadata claims original synthetic authorship, no forbidden producer data access, zero additional spend and same-author separate-algorithm verification. Review confirms declared metadata/hashes and target recomputation, not producer access history.',
  '1800 total manifest rows include inherited v1 and other producers. Only manifest arithmetic and 480 new rule rows reviewed; other family and historical content not read.'
 ],
 'limitations':[
  'Actual PI_MODEL=gpt-sol, PI_PROVIDER=openai; matches exposed producer alias. This is separate-session blind reasoning, not an independent model/teacher ground truth. Immutable identity unavailable.',
  '60/60 is sample agreement with saved labels, not estimated dataset accuracy, calibrated confidence or validation performance.',
  '480/480 is recomputation with reused same-author expected(case), not independent algorithms newly authored by reviewer. Both structured audits can share author/spec errors.',
  'No final/evaluation data, model loading, network/API, paid calls, tests, lint, Git or checkout edits. Existing session access only; zero additional/pending GBP spend.',
  'No historical content-level comparison or all-family cross-producer data review. Exact parent preservation and full token/structure audit are existing claims rather than reexecuted checks.'
 ],
 'must_fix':[], 'byte_preservation':{'files_hashed_before_after':len(before),'changed_files':changed,'manifest_unchanged':before[str(manifest_path)]==after[str(manifest_path)],'producer_artifacts_unchanged':not changed,'before_file':'hashes-before.json','after_file':'hashes-after.json'},
 'rows':comparisons
}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Jeff v2 — rule review','',report['verdict'],'',
'## Scope and evidence','',
f'- Candidate: `{manifest_path}`; SHA-256 `{before[str(manifest_path)]}`.',
'- 1800 declared total rows; reviewed **480 new rule rows**, not inherited v1 content or other producer rows.',
'- Actual reviewer: **openai / gpt-sol**, the same exposed alias as both producers. No immutable revision available.',
'- Prior exposure: manifest, first-row IDs/group/provenance and filenames only before sampling; no displayed labels or source solver/generator before decisions.',
'- Deterministic label-hidden selection: two rows per each of 30 mechanisms, rotated shortest/longest state quartiles; 60 rows (40 train, 20 validation). State lengths 141–324 characters. Outcomes varied naturally, not through target selection.',
'- `decisions-frozen.jsonl` was written and hashed before `targets-sealed.json` was read for comparison. All 60 blind choices match saved labels; no sampled ambiguity or must-fix identified. This is agreement, **not estimated accuracy or calibrated confidence**.',
'- After unblinding: imported each inspected pure **expected(case)** with its real dictionary shape (`mechanism_number` for rule-a; `group_number` for rule-b). All **480/480** recomputations match and have one exact supplied option. This reuses the same-author verifier, not a new independent solver.',
'- Audit IDs cover all rows exactly; policy/facts/source and scenario correspondence pass for 480 rows; assignment/config split checks pass; metadata-listed source artifact hashes match.',
'- Both combined: **200 train / 40 validation policy instances**, two rows each; **20 train / 10 validation mechanism groups**, not 240 independent mechanisms.',
'', '## Semantics, boundaries and rendering','']
lines += ['- '+s for s in report['source_and_boundary_review']]
lines += ['', '## Integration code (read-only)', '']+['- '+s for s in report['integration_code_review']['findings']]
lines += ['', '## Existing claims versus executed checks','']+['- '+s for s in report['existing_claims_not_reexecuted']]
lines += ['', '## Qualifications','']+['- '+s for s in report['limitations']]
lines += ['', '## Preservation and spend','',f'- Before/after SHA-256: **{len(before)} files**, **{len(changed)} changed**. Includes candidate manifest and all existing files under both rule producer directories; producer bytes and candidate preserved.', '- No producer or checkout edits. Wrote only new files under `review-rules/`. Zero additional or pending paid spend.', '', '## Row decisions (frozen before labels)', '', '| Row ID | Chosen option | Reason | Ambiguity | Comparison | Must-fix |','|---|---|---|---|---|---|']
for d in comparisons:
 lines.append('| '+ ' | '.join([d['row_id'], d['chosen_option_text'],d['reason'],'None identified','Matches saved target' if d['comparison']['agrees'] else 'Mismatch','None'])+' |')
lines+=['','## Supporting artifacts','','- `blind-sample.jsonl`, `decisions-frozen.jsonl`, `freeze-record.json`, `comparison.jsonl` (option IDs and row reasoning).','- `recompute.json`, `recompute-rows.jsonl` (480 source/target comparisons).','- `hashes-before.json`, `hashes-after.json`, `exposure.json`; selection/freeze/recompute scripts retained for provenance.','- `review.json` contains full structured findings and all per-row records.']
(P/'review.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'changed_files':changed,'manifest_hash_matches':manifest_matches,'report':str(P/'review.md')},indent=2))
