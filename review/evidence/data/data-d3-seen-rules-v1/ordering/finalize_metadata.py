"""Freeze metadata for the successfully audited validation payload."""
import hashlib,json,os
from pathlib import Path
P=Path(__file__).resolve().parent
CONFIG=Path('/Users/destiner/Code/jeff/.worktrees/data/configs/data/d3-seen-rules-v1.json')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    report=json.loads((P/'validation_report.json').read_text())
    if report['failure_count'] or not report['rule_verified']:raise SystemExit('Audit must succeed first')
    rows=[json.loads(s) for s in (P/'validation.jsonl').read_text().splitlines()]
    if len(rows)!=48 or any(r['provenance']['label_basis']!='rule_verified' for r in rows):raise SystemExit('Unverified rows')
    files=['validation.jsonl','source_cases.jsonl','audit_cases.jsonl','group_assignments.json','author_sources.py','generator.py','audit.py','validation_report.json','generation_review.md','finalize_metadata.py']
    metadata=dict(
        schema_version='0.1',shard_id='data-d3-seen-rules-v1-ordering',
        source_job='data-d3-seen-rules-v1-ordering-original-731904',
        teacher=dict(provider=os.environ['PI_PROVIDER'],model_alias=os.environ['PI_MODEL'],immutable_revision=None),
        cost=dict(currency='GBP',additional_spend=0,pending_spend=0),
        generation_settings=dict(seed=731904,method='original agent-authored structured policies; deterministic Python rendering and programmatic arithmetic; same-agent separate-algorithm audit',
            source_revision=sha(P/'source_cases.jsonl'),assignment_revision=sha(P/'group_assignments.json'),
            config_revision={'path':str(CONFIG),'sha256':sha(CONFIG)},
            source_authoring_revision=sha(P/'author_sources.py'),
            harness_sampling={'temperature':'unknown','top_p':'unknown','sampling_seed':'unknown','immutable_teacher_revision':'not exposed'},
            choice_shuffle='Seeded balanced target positions randomly assigned within arity; separate distractor and candidate-list shuffles. Ordered procedures and arrival ranks unchanged.',
            hashes={name:sha(P/name) for name in files}),
        usage_constraints={'split':'validation','usage':'validation_only_never_train','permanently_training_excluded':True,'derivatives_never_train':True,'material':'Original synthetic content under existing provider terms; no private records; no additional redistribution licence asserted.'},
        row_counts={'validation':48},group_counts={'validation':24},mechanism_count=4,policy_count=24,
        mechanisms=['lexicographic','fifo','discount','rounding'],
        novelty={'stratum':'seen_mechanism_new_policy','intentional_training_mechanism_overlap':True,'historical_rows_inspected':False,'new_source_policy_groups':24,'empirical_historical_text_comparison':False},
        verification={'algorithmic_checks':report['check_count'],'failures':report['failure_count'],'agreement_rows':48,'semantic_self_review_policies':24,'semantic_self_review_cases':24,'independent_authorship':False,'kind':'same_agent_separate_algorithm_consistency','report':'validation_report.json','review':'generation_review.md','tokenizer_audit':'not performed; parent responsibility'},
        limitations=['Development diagnostic, not final evaluation.','Seen mechanisms intentionally overlap v2 train; policy instances and source cases newly authored.','Paired dependence: two cases share each authored policy.','Permanently validation-only; never train, including derivatives.','Same-agent audit and semantic review, not independent authorship or external validation.','Templates and author commonality may create residual shortcuts; no empirical comparison with historical rows.','Whitespace state length is not tokenizer length; parent owns 256-token audit.','Teacher is the exposed alias only; immutable revision and harness sampling settings unknown.'])
    (P/'metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'rows':len(rows),'metadata_sha256':sha(P/'metadata.json'),'validation_sha256':sha(P/'validation.jsonl'),'files_hashed':len(files)}))
if __name__=='__main__':main()
