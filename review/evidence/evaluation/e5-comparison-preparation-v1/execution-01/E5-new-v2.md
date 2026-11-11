# E5 frozen decoder comparison: new-v2 (240 presentations)

Reference: `/Users/destiner/Code/jeff/artifacts/evaluation/e3-v2-freeze-v1/new-v2/validation.jsonl`; SHA-256 `847cf4cb43df058a44366c7f3acbcebdb7faaea756fe21de8cc80cd5f90796eb`.
240 rows / 170 declared source groups. Rows and reversals are not independent observations.

## Coverage and quality

Agreement follows supplied reference-label provenance. Conditional agreement/log loss use valid predictions; all-row success counts failures as unsuccessful. Natural-log loss is unclipped; lower is better.

| Predictor | Valid/total | Conditional agreement | All-row success | Log loss | Missing/invalid/duplicate | Extra IDs | Unidentifiable | Ties |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | 240/240 | 66/240 | 66/240 | 1.332467 | 0/0/0 | 0 | 0 | 0 |
| m4-minilm-trained | 240/240 | 132/240 | 132/240 | 0.823115 | 0/0/0 | 0 | 0 | 0 |
| m4-msmarco-pretrained-start | 240/240 | 99/240 | 99/240 | 1.058568 | 0/0/0 | 0 | 0 | 0 |
| m4-msmarco-trained | 240/240 | 141/240 | 141/240 | 0.917258 | 0/0/0 | 0 | 0 | 0 |
| m2-v1-trained | 240/240 | 107/240 | 107/240 | 1.136427 | 0/0/0 | 0 | 0 | 0 |
| m3-v1-trained | 240/240 | 110/240 | 110/240 | 1.024844 | 0/0/0 | 0 | 0 | 0 |
| uniform | 240/240 | 65/240 | 65/240 | 1.333463 | 0/0/0 | 0 | 0 | 240 |
| lexical | 240/240 | 99/240 | 99/240 | 1.296868 | 0/0/0 | 0 | 0 | 121 |
| qwen25-05b-instruct-frozen | 240/240 | 129/240 | 129/240 | 1.312350 | 0/0/0 | 0 | 0 | 0 |

## Label provenance

Provenance is reported as supplied, not upgraded by this evaluator. Teacher aliases may lack immutable revisions; unknown identities remain unknown.

| Kind | Source | Label basis | Teacher model | Rows | Groups | Families |
| --- | --- | --- | --- | --- | --- | --- |
| programmatic | data-pilot-v2-rule-b-r1:original-policies-r1 | rule_verified | not applicable | 40 | 5 | rule_application |
| teacher | data-pilot-v2-intent-b-r2/source-mappings-r2 | teacher | gpt-sol | 40 | 40 | intent |
| teacher | data-pilot-v2-rule-a-r1:source_cases-r1 | rule_verified | openai/gpt-sol | 40 | 5 | rule_application |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g201 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g202 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g203 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g204 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g205 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g206 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g207 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g208 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g209 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g210 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g211 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g212 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g213 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g214 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g215 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g216 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g217 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g218 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g219 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g220 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g221 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g222 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g223 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g224 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g225 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g226 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g227 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g228 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g229 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g230 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g231 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g232 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g233 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g234 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g235 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g236 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g237 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g238 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g239 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2-sentiment-b-r2/from/data-pilot-v2-sentiment-b-r1/sentiment-b-source-s1;source_sha256=a4d16aa593648d56dbf3972ba9ae42305e96b9a60ec7045e37e45651f913a6e8;case=data:pilot-v2:sentiment-b:g240 | teacher | gpt-sol | 1 | 1 | sentiment |
| teacher | data-pilot-v2/sentiment-a:sentiment-a-authored-r1 | teacher | gpt-sol | 40 | 40 | sentiment |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g201 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g202 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g203 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g204 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g205 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g206 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g207 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g208 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g209 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g210 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g211 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g212 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g213 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g214 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g215 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g216 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g217 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g218 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g219 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g220 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g221 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g222 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g223 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g224 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g225 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g226 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g227 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g228 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g229 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g230 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g231 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g232 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g233 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g234 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g235 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g236 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g237 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g238 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g239 | teacher | openai/gpt-sol | 1 | 1 | intent |
| teacher | jeff/data-pilot-v2/intent-a-r2/choice_mappings.json#g240 | teacher | openai/gpt-sol | 1 | 1 | intent |

## Per label basis

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per label basis | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rule_verified | 80 | 10 | rule_verified_accuracy | 21/80 · 1.302037 | 15/80 · 1.343231 | 15/80 · 1.358558 | 21/80 · 1.411166 | 19/80 · 1.335358 | 14/80 · 1.405047 | 23/80 · 1.303586 | 17/80 · 1.323385 | 25/80 · 1.765476 |
| teacher | 160 | 160 | teacher_agreement | 45/160 · 1.347681 | 117/160 · 0.563057 | 84/160 · 0.908572 | 120/160 · 0.670305 | 88/160 · 1.036962 | 96/160 · 0.834742 | 42/160 · 1.348402 | 82/160 · 1.283609 | 104/160 · 1.085786 |

## Per family

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per family | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intent | 80 | 80 | teacher_agreement | 27/80 · 1.308764 | 74/80 · 0.184336 | 66/80 · 0.424631 | 77/80 · 0.091450 | 66/80 · 0.505941 | 72/80 · 0.318603 | 22/80 · 1.310510 | 63/80 · 1.179489 | 74/80 · 0.205688 |
| rule_application | 80 | 10 | rule_verified_accuracy | 21/80 · 1.302037 | 15/80 · 1.343231 | 15/80 · 1.358558 | 21/80 · 1.411166 | 19/80 · 1.335358 | 14/80 · 1.405047 | 23/80 · 1.303586 | 17/80 · 1.323385 | 25/80 · 1.765476 |
| sentiment | 80 | 80 | teacher_agreement | 18/80 · 1.386599 | 43/80 · 0.941779 | 18/80 · 1.392514 | 43/80 · 1.249159 | 22/80 · 1.567983 | 24/80 · 1.350882 | 20/80 · 1.386294 | 19/80 · 1.387730 | 30/80 · 1.965885 |

## Per source group

Each predictor cell: correct/valid · mean log loss. Coverage is shown overall above and within every group in the JSON report.

| Per source group | Rows | Groups | Metric | m4-minilm-random-start | m4-minilm-trained | m4-msmarco-pretrained-start | m4-msmarco-trained | m2-v1-trained | m3-v1-trained | uniform | lexical | qwen25-05b-instruct-frozen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data:pilot-v2:intent-a:g201 | 1 | 1 | teacher_agreement | 0/1 · 1.413703 | 1/1 · 0.044438 | 1/1 · 0.012250 | 1/1 · 0.002503 | 0/1 · 1.024760 | 1/1 · 0.052631 | 0/1 · 1.386294 | 1/1 · 1.237710 | 1/1 · 0.006998 |
| data:pilot-v2:intent-a:g202 | 1 | 1 | teacher_agreement | 0/1 · 1.107956 | 1/1 · 0.000555 | 1/1 · 0.272841 | 1/1 · 0.000055 | 1/1 · 0.070355 | 1/1 · 0.054649 | 1/1 · 1.098612 | 1/1 · 1.022815 | 1/1 · 0.116586 |
| data:pilot-v2:intent-a:g203 | 1 | 1 | teacher_agreement | 1/1 · 1.381587 | 1/1 · 0.000014 | 1/1 · 0.007432 | 1/1 · 0.000256 | 1/1 · 0.002538 | 1/1 · 0.006618 | 0/1 · 1.386294 | 1/1 · 1.120055 | 1/1 · 0.002129 |
| data:pilot-v2:intent-a:g204 | 1 | 1 | teacher_agreement | 1/1 · 1.359543 | 1/1 · 0.622616 | 0/1 · 1.245939 | 1/1 · 0.104260 | 0/1 · 1.183663 | 1/1 · 0.412086 | 1/1 · 1.386294 | 0/1 · 1.393276 | 1/1 · 0.001024 |
| data:pilot-v2:intent-a:g205 | 1 | 1 | teacher_agreement | 0/1 · 1.603907 | 1/1 · 0.001058 | 1/1 · 0.000940 | 1/1 · 0.000020 | 1/1 · 1.064378 | 1/1 · 0.043921 | 0/1 · 1.609438 | 1/1 · 1.399030 | 1/1 · 0.197934 |
| data:pilot-v2:intent-a:g206 | 1 | 1 | teacher_agreement | 1/1 · 1.077512 | 1/1 · 0.000006 | 1/1 · 0.000432 | 1/1 · 0.000007 | 1/1 · 0.006260 | 1/1 · 0.000401 | 1/1 · 1.098612 | 1/1 · 0.891166 | 1/1 · 0.552203 |
| data:pilot-v2:intent-a:g207 | 1 | 1 | teacher_agreement | 0/1 · 1.421042 | 1/1 · 0.145844 | 1/1 · 0.045981 | 0/1 · 0.889660 | 0/1 · 0.906657 | 1/1 · 0.593962 | 0/1 · 1.386294 | 1/1 · 1.247330 | 1/1 · 0.044889 |
| data:pilot-v2:intent-a:g208 | 1 | 1 | teacher_agreement | 0/1 · 1.394160 | 1/1 · 0.000015 | 1/1 · 0.000405 | 1/1 · 0.000052 | 1/1 · 0.123093 | 1/1 · 0.000700 | 0/1 · 1.386294 | 1/1 · 1.080558 | 1/1 · 0.012867 |
| data:pilot-v2:intent-a:g209 | 1 | 1 | teacher_agreement | 1/1 · 1.768110 | 1/1 · 0.000037 | 1/1 · 0.046116 | 1/1 · 0.004786 | 1/1 · 0.365553 | 1/1 · 0.107771 | 0/1 · 1.791759 | 1/1 · 1.585175 | 1/1 · 0.008377 |
| data:pilot-v2:intent-a:g210 | 1 | 1 | teacher_agreement | 1/1 · 1.084943 | 1/1 · 0.568812 | 1/1 · 0.370302 | 1/1 · 0.382773 | 1/1 · 0.437619 | 1/1 · 0.637696 | 0/1 · 1.098612 | 1/1 · 0.994405 | 1/1 · 0.003430 |
| data:pilot-v2:intent-a:g211 | 1 | 1 | teacher_agreement | 0/1 · 1.400182 | 1/1 · 0.000004 | 1/1 · 0.002220 | 1/1 · 0.000012 | 1/1 · 0.008285 | 1/1 · 0.013968 | 0/1 · 1.386294 | 1/1 · 1.175831 | 1/1 · 0.006777 |
| data:pilot-v2:intent-a:g212 | 1 | 1 | teacher_agreement | 0/1 · 1.092633 | 1/1 · 0.000164 | 1/1 · 0.151972 | 1/1 · 0.000701 | 1/1 · 0.120310 | 1/1 · 0.044336 | 0/1 · 1.098612 | 1/1 · 0.984318 | 0/1 · 0.727973 |
| data:pilot-v2:intent-a:g213 | 1 | 1 | teacher_agreement | 1/1 · 1.377532 | 0/1 · 1.092105 | 0/1 · 1.149225 | 1/1 · 0.016507 | 0/1 · 0.843080 | 1/1 · 0.305329 | 1/1 · 1.386294 | 0/1 · 1.438579 | 1/1 · 0.049182 |
| data:pilot-v2:intent-a:g214 | 1 | 1 | teacher_agreement | 1/1 · 1.377486 | 1/1 · 0.000106 | 1/1 · 0.780677 | 1/1 · 0.000354 | 1/1 · 0.145474 | 1/1 · 0.087243 | 0/1 · 1.386294 | 1/1 · 1.263048 | 1/1 · 0.104849 |
| data:pilot-v2:intent-a:g215 | 1 | 1 | teacher_agreement | 0/1 · 1.581973 | 1/1 · 0.001456 | 1/1 · 0.002374 | 1/1 · 0.002920 | 1/1 · 0.018064 | 1/1 · 0.059066 | 0/1 · 1.609438 | 1/1 · 1.383958 | 1/1 · 0.201542 |
| data:pilot-v2:intent-a:g216 | 1 | 1 | teacher_agreement | 1/1 · 1.078594 | 1/1 · 0.013927 | 1/1 · 0.301532 | 1/1 · 0.009435 | 1/1 · 0.142219 | 1/1 · 0.237493 | 0/1 · 1.098612 | 1/1 · 0.928783 | 1/1 · 0.041797 |
| data:pilot-v2:intent-a:g217 | 1 | 1 | teacher_agreement | 0/1 · 1.374753 | 1/1 · 0.000400 | 0/1 · 1.673095 | 1/1 · 0.005427 | 1/1 · 0.013552 | 1/1 · 0.331499 | 0/1 · 1.386294 | 1/1 · 1.201876 | 1/1 · 0.001610 |
| data:pilot-v2:intent-a:g218 | 1 | 1 | teacher_agreement | 0/1 · 1.398073 | 1/1 · 0.014450 | 0/1 · 3.943825 | 1/1 · 0.005484 | 1/1 · 0.295615 | 1/1 · 0.066941 | 1/1 · 1.386294 | 1/1 · 1.278446 | 1/1 · 0.249630 |
| data:pilot-v2:intent-a:g219 | 1 | 1 | teacher_agreement | 0/1 · 1.770056 | 1/1 · 0.000012 | 0/1 · 3.657008 | 1/1 · 0.001666 | 1/1 · 0.311469 | 0/1 · 1.921626 | 0/1 · 1.791759 | 0/1 · 1.775699 | 1/1 · 0.005166 |
| data:pilot-v2:intent-a:g220 | 1 | 1 | teacher_agreement | 0/1 · 1.089588 | 1/1 · 0.000586 | 1/1 · 0.031010 | 1/1 · 0.000038 | 1/1 · 0.009487 | 1/1 · 0.004234 | 1/1 · 1.098612 | 1/1 · 0.968807 | 0/1 · 1.220335 |
| data:pilot-v2:intent-a:g221 | 1 | 1 | teacher_agreement | 0/1 · 1.397123 | 1/1 · 0.000031 | 1/1 · 0.005049 | 1/1 · 0.000013 | 1/1 · 0.002492 | 1/1 · 0.002877 | 0/1 · 1.386294 | 1/1 · 1.115496 | 1/1 · 0.029702 |
| data:pilot-v2:intent-a:g222 | 1 | 1 | teacher_agreement | 1/1 · 1.082208 | 1/1 · 0.006160 | 1/1 · 0.001550 | 1/1 · 0.000009 | 1/1 · 0.341772 | 1/1 · 0.007198 | 0/1 · 1.098612 | 1/1 · 0.994194 | 1/1 · 0.001662 |
| data:pilot-v2:intent-a:g223 | 1 | 1 | teacher_agreement | 1/1 · 1.363035 | 1/1 · 0.000007 | 1/1 · 0.000412 | 1/1 · 0.000026 | 1/1 · 0.092986 | 1/1 · 0.002169 | 0/1 · 1.386294 | 1/1 · 1.176881 | 1/1 · 0.002425 |
| data:pilot-v2:intent-a:g224 | 1 | 1 | teacher_agreement | 0/1 · 1.385653 | 1/1 · 0.000483 | 1/1 · 0.068165 | 1/1 · 0.047045 | 1/1 · 0.018295 | 1/1 · 0.439815 | 1/1 · 1.386294 | 1/1 · 1.359882 | 1/1 · 0.013292 |
| data:pilot-v2:intent-a:g225 | 1 | 1 | teacher_agreement | 0/1 · 1.611278 | 1/1 · 0.000751 | 1/1 · 0.029656 | 1/1 · 0.000040 | 1/1 · 0.049012 | 1/1 · 0.028228 | 1/1 · 1.609438 | 1/1 · 1.382965 | 1/1 · 0.001313 |
| data:pilot-v2:intent-a:g226 | 1 | 1 | teacher_agreement | 1/1 · 1.093604 | 1/1 · 0.002071 | 1/1 · 0.093870 | 1/1 · 0.004361 | 1/1 · 0.003413 | 1/1 · 0.428579 | 0/1 · 1.098612 | 1/1 · 0.928414 | 1/1 · 0.000679 |
| data:pilot-v2:intent-a:g227 | 1 | 1 | teacher_agreement | 0/1 · 1.428958 | 0/1 · 2.563113 | 1/1 · 0.443731 | 1/1 · 0.486928 | 0/1 · 1.108572 | 1/1 · 0.111538 | 1/1 · 1.386294 | 0/1 · 1.350067 | 1/1 · 0.189587 |
| data:pilot-v2:intent-a:g228 | 1 | 1 | teacher_agreement | 0/1 · 1.377898 | 1/1 · 0.000001 | 1/1 · 0.000263 | 1/1 · 0.000002 | 1/1 · 0.000265 | 1/1 · 0.001192 | 0/1 · 1.386294 | 1/1 · 1.106808 | 1/1 · 0.074356 |
| data:pilot-v2:intent-a:g229 | 1 | 1 | teacher_agreement | 0/1 · 1.786763 | 1/1 · 0.027017 | 1/1 · 0.054167 | 1/1 · 0.002311 | 1/1 · 0.266412 | 1/1 · 0.327181 | 1/1 · 1.791759 | 1/1 · 1.545522 | 1/1 · 0.060115 |
| data:pilot-v2:intent-a:g230 | 1 | 1 | teacher_agreement | 1/1 · 1.074119 | 1/1 · 0.000338 | 1/1 · 0.021346 | 1/1 · 0.007001 | 1/1 · 0.017591 | 1/1 · 0.191367 | 0/1 · 1.098612 | 1/1 · 0.991228 | 1/1 · 0.000128 |
| data:pilot-v2:intent-a:g231 | 1 | 1 | teacher_agreement | 0/1 · 1.416225 | 1/1 · 0.140287 | 1/1 · 0.002160 | 1/1 · 0.000084 | 1/1 · 0.110680 | 1/1 · 0.064742 | 0/1 · 1.386294 | 1/1 · 1.193946 | 1/1 · 0.001549 |
| data:pilot-v2:intent-a:g232 | 1 | 1 | teacher_agreement | 0/1 · 1.116325 | 1/1 · 0.006890 | 1/1 · 0.052105 | 1/1 · 0.015140 | 1/1 · 0.239460 | 1/1 · 0.047028 | 1/1 · 1.098612 | 1/1 · 1.052975 | 1/1 · 0.012842 |
| data:pilot-v2:intent-a:g233 | 1 | 1 | teacher_agreement | 1/1 · 1.374048 | 1/1 · 0.029121 | 1/1 · 0.052773 | 1/1 · 0.001303 | 1/1 · 0.681135 | 1/1 · 0.077482 | 0/1 · 1.386294 | 1/1 · 1.178527 | 1/1 · 0.003506 |
| data:pilot-v2:intent-a:g234 | 1 | 1 | teacher_agreement | 0/1 · 1.375975 | 1/1 · 0.120672 | 1/1 · 0.038784 | 1/1 · 0.006297 | 1/1 · 0.143889 | 1/1 · 0.125406 | 0/1 · 1.386294 | 1/1 · 1.164647 | 1/1 · 0.000079 |
| data:pilot-v2:intent-a:g235 | 1 | 1 | teacher_agreement | 0/1 · 1.637219 | 1/1 · 0.002561 | 1/1 · 0.040467 | 1/1 · 0.000245 | 1/1 · 0.497397 | 1/1 · 0.144511 | 0/1 · 1.609438 | 1/1 · 1.404174 | 1/1 · 0.000187 |
| data:pilot-v2:intent-a:g236 | 1 | 1 | teacher_agreement | 0/1 · 1.107715 | 1/1 · 0.000284 | 1/1 · 0.001060 | 1/1 · 0.000007 | 1/1 · 0.089195 | 1/1 · 0.001265 | 0/1 · 1.098612 | 1/1 · 0.876970 | 1/1 · 0.001166 |
| data:pilot-v2:intent-a:g237 | 1 | 1 | teacher_agreement | 0/1 · 1.400275 | 1/1 · 0.000155 | 1/1 · 0.015628 | 1/1 · 0.001206 | 1/1 · 0.026009 | 1/1 · 0.010406 | 0/1 · 1.386294 | 1/1 · 1.177410 | 1/1 · 0.030207 |
| data:pilot-v2:intent-a:g238 | 1 | 1 | teacher_agreement | 0/1 · 1.382069 | 1/1 · 0.018050 | 1/1 · 0.001612 | 1/1 · 0.000005 | 1/1 · 0.015110 | 1/1 · 0.000511 | 0/1 · 1.386294 | 1/1 · 1.189547 | 1/1 · 0.000488 |
| data:pilot-v2:intent-a:g239 | 1 | 1 | teacher_agreement | 0/1 · 1.786637 | 1/1 · 0.067913 | 1/1 · 0.012444 | 1/1 · 0.010598 | 1/1 · 0.432066 | 1/1 · 0.022053 | 0/1 · 1.791759 | 1/1 · 1.675249 | 1/1 · 0.626395 |
| data:pilot-v2:intent-a:g240 | 1 | 1 | teacher_agreement | 1/1 · 1.085080 | 1/1 · 0.000591 | 1/1 · 0.004550 | 1/1 · 0.001827 | 1/1 · 0.101299 | 1/1 · 0.010520 | 0/1 · 1.098612 | 1/1 · 0.935321 | 1/1 · 0.023644 |
| data:pilot-v2:intent-b:g201 | 1 | 1 | teacher_agreement | 1/1 · 1.076358 | 1/1 · 0.086897 | 1/1 · 0.123769 | 1/1 · 0.021678 | 1/1 · 0.143512 | 0/1 · 1.146031 | 0/1 · 1.098612 | 1/1 · 1.014263 | 1/1 · 0.058072 |
| data:pilot-v2:intent-b:g202 | 1 | 1 | teacher_agreement | 0/1 · 1.397335 | 0/1 · 1.424787 | 0/1 · 1.830506 | 1/1 · 0.052910 | 0/1 · 1.455017 | 0/1 · 1.836357 | 1/1 · 1.386294 | 0/1 · 1.341665 | 0/1 · 1.046405 |
| data:pilot-v2:intent-b:g203 | 1 | 1 | teacher_agreement | 0/1 · 1.122913 | 1/1 · 0.001392 | 1/1 · 0.006296 | 1/1 · 0.000121 | 1/1 · 0.628867 | 1/1 · 0.001751 | 0/1 · 1.098612 | 1/1 · 1.000723 | 1/1 · 0.012672 |
| data:pilot-v2:intent-b:g204 | 1 | 1 | teacher_agreement | 1/1 · 1.370725 | 1/1 · 0.000021 | 1/1 · 0.008742 | 1/1 · 0.000043 | 1/1 · 0.000830 | 1/1 · 0.021071 | 0/1 · 1.386294 | 1/1 · 1.076219 | 1/1 · 0.009568 |
| data:pilot-v2:intent-b:g205 | 1 | 1 | teacher_agreement | 1/1 · 1.079120 | 1/1 · 0.008789 | 0/1 · 2.000770 | 1/1 · 0.000403 | 1/1 · 0.067856 | 1/1 · 0.051929 | 0/1 · 1.098612 | 0/1 · 1.044459 | 1/1 · 0.003672 |
| data:pilot-v2:intent-b:g206 | 1 | 1 | teacher_agreement | 0/1 · 1.394287 | 1/1 · 0.002570 | 1/1 · 0.169693 | 1/1 · 0.000129 | 1/1 · 0.254491 | 1/1 · 0.150938 | 0/1 · 1.386294 | 1/1 · 1.275746 | 1/1 · 0.083841 |
| data:pilot-v2:intent-b:g207 | 1 | 1 | teacher_agreement | 0/1 · 1.101811 | 1/1 · 0.001850 | 1/1 · 0.010450 | 1/1 · 0.000365 | 1/1 · 0.017470 | 1/1 · 0.074954 | 1/1 · 1.098612 | 1/1 · 0.902476 | 1/1 · 0.125258 |
| data:pilot-v2:intent-b:g208 | 1 | 1 | teacher_agreement | 0/1 · 1.379759 | 1/1 · 0.028084 | 1/1 · 0.070625 | 1/1 · 0.003951 | 1/1 · 0.082298 | 1/1 · 0.045008 | 0/1 · 1.386294 | 1/1 · 1.195713 | 1/1 · 0.052749 |
| data:pilot-v2:intent-b:g209 | 1 | 1 | teacher_agreement | 0/1 · 1.082649 | 1/1 · 0.002748 | 1/1 · 0.090853 | 1/1 · 0.000311 | 1/1 · 0.006203 | 1/1 · 0.041601 | 1/1 · 1.098612 | 1/1 · 0.927626 | 1/1 · 0.639522 |
| data:pilot-v2:intent-b:g210 | 1 | 1 | teacher_agreement | 1/1 · 1.367432 | 1/1 · 0.061240 | 1/1 · 0.510627 | 1/1 · 0.004847 | 1/1 · 0.415262 | 1/1 · 0.154985 | 1/1 · 1.386294 | 1/1 · 1.156006 | 0/1 · 1.691776 |
| data:pilot-v2:intent-b:g211 | 1 | 1 | teacher_agreement | 0/1 · 1.117311 | 1/1 · 0.283925 | 1/1 · 0.360439 | 1/1 · 0.085484 | 1/1 · 0.328180 | 0/1 · 0.997760 | 0/1 · 1.098612 | 1/1 · 1.019996 | 1/1 · 0.002296 |
| data:pilot-v2:intent-b:g212 | 1 | 1 | teacher_agreement | 1/1 · 1.378197 | 1/1 · 0.000347 | 1/1 · 0.259683 | 1/1 · 0.033382 | 1/1 · 0.272134 | 1/1 · 0.139870 | 0/1 · 1.386294 | 1/1 · 1.270632 | 1/1 · 0.002082 |
| data:pilot-v2:intent-b:g213 | 1 | 1 | teacher_agreement | 0/1 · 1.123735 | 1/1 · 0.000209 | 1/1 · 0.015756 | 1/1 · 0.000402 | 1/1 · 0.001928 | 1/1 · 0.002710 | 1/1 · 1.098612 | 1/1 · 0.950160 | 1/1 · 0.005476 |
| data:pilot-v2:intent-b:g214 | 1 | 1 | teacher_agreement | 0/1 · 1.397195 | 1/1 · 0.004795 | 1/1 · 0.018698 | 1/1 · 0.000168 | 1/1 · 0.055399 | 1/1 · 0.034536 | 1/1 · 1.386294 | 1/1 · 1.319695 | 1/1 · 0.008772 |
| data:pilot-v2:intent-b:g215 | 1 | 1 | teacher_agreement | 1/1 · 1.085602 | 1/1 · 0.026515 | 1/1 · 0.158300 | 1/1 · 0.000976 | 1/1 · 1.036077 | 1/1 · 0.065579 | 1/1 · 1.098612 | 1/1 · 1.011194 | 0/1 · 1.438635 |
| data:pilot-v2:intent-b:g216 | 1 | 1 | teacher_agreement | 0/1 · 1.383663 | 1/1 · 0.006149 | 1/1 · 0.096710 | 1/1 · 0.005199 | 0/1 · 1.540297 | 1/1 · 0.052338 | 0/1 · 1.386294 | 1/1 · 1.234732 | 1/1 · 0.118447 |
| data:pilot-v2:intent-b:g217 | 1 | 1 | teacher_agreement | 1/1 · 1.049646 | 1/1 · 0.000057 | 1/1 · 0.071693 | 1/1 · 0.000144 | 1/1 · 0.121479 | 1/1 · 0.127287 | 0/1 · 1.098612 | 0/1 · 1.172704 | 1/1 · 0.054783 |
| data:pilot-v2:intent-b:g218 | 1 | 1 | teacher_agreement | 0/1 · 1.611366 | 1/1 · 0.005608 | 1/1 · 0.030560 | 1/1 · 0.084943 | 0/1 · 0.958107 | 1/1 · 0.066811 | 0/1 · 1.609438 | 1/1 · 1.476982 | 1/1 · 0.661078 |
| data:pilot-v2:intent-b:g219 | 1 | 1 | teacher_agreement | 1/1 · 1.093438 | 1/1 · 0.000023 | 1/1 · 0.048431 | 1/1 · 0.001844 | 1/1 · 0.002563 | 1/1 · 0.143982 | 0/1 · 1.098612 | 1/1 · 0.946830 | 1/1 · 0.579063 |
| data:pilot-v2:intent-b:g220 | 1 | 1 | teacher_agreement | 0/1 · 1.385412 | 1/1 · 0.034409 | 1/1 · 0.119370 | 1/1 · 0.000977 | 0/1 · 0.799153 | 1/1 · 0.655142 | 0/1 · 1.386294 | 1/1 · 1.262514 | 1/1 · 0.000649 |
| data:pilot-v2:intent-b:g221 | 1 | 1 | teacher_agreement | 0/1 · 1.775878 | 0/1 · 2.022566 | 1/1 · 0.289805 | 0/1 · 0.930112 | 1/1 · 0.884229 | 1/1 · 0.214594 | 0/1 · 1.791759 | 1/1 · 1.608573 | 1/1 · 0.633155 |
| data:pilot-v2:intent-b:g222 | 1 | 1 | teacher_agreement | 1/1 · 1.084765 | 1/1 · 0.002710 | 1/1 · 0.009031 | 1/1 · 0.008467 | 1/1 · 0.345157 | 1/1 · 0.085725 | 1/1 · 1.098612 | 1/1 · 0.959398 | 1/1 · 0.008352 |
| data:pilot-v2:intent-b:g223 | 1 | 1 | teacher_agreement | 0/1 · 1.383085 | 1/1 · 0.005568 | 1/1 · 0.155054 | 1/1 · 0.038532 | 1/1 · 0.054624 | 1/1 · 0.054849 | 0/1 · 1.386294 | 1/1 · 1.198696 | 1/1 · 0.005568 |
| data:pilot-v2:intent-b:g224 | 1 | 1 | teacher_agreement | 0/1 · 1.092183 | 1/1 · 0.000082 | 0/1 · 1.268208 | 1/1 · 0.002680 | 0/1 · 0.942404 | 1/1 · 0.666320 | 0/1 · 1.098612 | 0/1 · 1.006156 | 1/1 · 0.576236 |
| data:pilot-v2:intent-b:g225 | 1 | 1 | teacher_agreement | 0/1 · 1.107164 | 1/1 · 0.001465 | 1/1 · 0.129359 | 1/1 · 0.000930 | 1/1 · 0.085537 | 1/1 · 0.145932 | 0/1 · 1.098612 | 0/1 · 1.131727 | 1/1 · 0.001750 |
| data:pilot-v2:intent-b:g226 | 1 | 1 | teacher_agreement | 1/1 · 1.366455 | 1/1 · 0.001300 | 1/1 · 0.023372 | 1/1 · 0.016637 | 1/1 · 0.082688 | 1/1 · 0.041583 | 0/1 · 1.386294 | 1/1 · 1.278982 | 1/1 · 0.139625 |
| data:pilot-v2:intent-b:g227 | 1 | 1 | teacher_agreement | 0/1 · 1.108506 | 1/1 · 0.003011 | 0/1 · 1.780221 | 1/1 · 0.071444 | 0/1 · 2.444569 | 0/1 · 1.404238 | 0/1 · 1.098612 | 1/1 · 0.978381 | 1/1 · 0.765708 |
| data:pilot-v2:intent-b:g228 | 1 | 1 | teacher_agreement | 0/1 · 1.408588 | 0/1 · 1.016333 | 1/1 · 0.193423 | 1/1 · 0.240190 | 0/1 · 1.379488 | 0/1 · 1.022634 | 0/1 · 1.386294 | 0/1 · 1.241668 | 1/1 · 0.023907 |
| data:pilot-v2:intent-b:g229 | 1 | 1 | teacher_agreement | 1/1 · 1.070054 | 1/1 · 0.000478 | 1/1 · 0.000021 | 1/1 · 0.000001 | 1/1 · 0.008734 | 1/1 · 0.000044 | 0/1 · 1.098612 | 1/1 · 0.803458 | 1/1 · 0.012036 |
| data:pilot-v2:intent-b:g230 | 1 | 1 | teacher_agreement | 0/1 · 1.457076 | 1/1 · 0.630793 | 0/1 · 0.970060 | 1/1 · 0.115090 | 1/1 · 0.680303 | 1/1 · 0.614535 | 0/1 · 1.386294 | 0/1 · 1.300450 | 1/1 · 0.009221 |
| data:pilot-v2:intent-b:g231 | 1 | 1 | teacher_agreement | 0/1 · 1.108495 | 1/1 · 0.181692 | 1/1 · 0.005815 | 1/1 · 0.008134 | 1/1 · 0.264736 | 1/1 · 0.068232 | 0/1 · 1.098612 | 0/1 · 1.206011 | 1/1 · 0.148618 |
| data:pilot-v2:intent-b:g232 | 1 | 1 | teacher_agreement | 0/1 · 1.390147 | 1/1 · 0.003088 | 1/1 · 0.065780 | 1/1 · 0.000483 | 1/1 · 0.368840 | 1/1 · 0.021090 | 1/1 · 1.386294 | 0/1 · 1.345971 | 1/1 · 0.016431 |
| data:pilot-v2:intent-b:g233 | 1 | 1 | teacher_agreement | 0/1 · 1.088805 | 1/1 · 0.000239 | 1/1 · 0.064057 | 1/1 · 0.000928 | 1/1 · 0.196956 | 1/1 · 0.038183 | 0/1 · 1.098612 | 0/1 · 1.056474 | 1/1 · 0.007989 |
| data:pilot-v2:intent-b:g234 | 1 | 1 | teacher_agreement | 0/1 · 1.392759 | 1/1 · 0.005226 | 0/1 · 2.317144 | 1/1 · 0.001719 | 1/1 · 0.156926 | 1/1 · 0.611483 | 0/1 · 1.386294 | 0/1 · 1.380122 | 1/1 · 0.051499 |
| data:pilot-v2:intent-b:g235 | 1 | 1 | teacher_agreement | 0/1 · 1.103359 | 1/1 · 0.011167 | 1/1 · 0.042178 | 1/1 · 0.008532 | 1/1 · 0.387373 | 1/1 · 0.156804 | 0/1 · 1.098612 | 1/1 · 0.982240 | 1/1 · 0.003199 |
| data:pilot-v2:intent-b:g236 | 1 | 1 | teacher_agreement | 1/1 · 1.359848 | 0/1 · 2.695519 | 0/1 · 2.857303 | 0/1 · 2.473782 | 0/1 · 6.932872 | 0/1 · 3.911699 | 0/1 · 1.386294 | 0/1 · 1.453811 | 1/1 · 0.343272 |
| data:pilot-v2:intent-b:g237 | 1 | 1 | teacher_agreement | 1/1 · 1.089962 | 1/1 · 0.000077 | 1/1 · 0.007339 | 1/1 · 0.000019 | 1/1 · 0.818753 | 1/1 · 0.001206 | 0/1 · 1.098612 | 1/1 · 0.969817 | 1/1 · 0.033823 |
| data:pilot-v2:intent-b:g238 | 1 | 1 | teacher_agreement | 0/1 · 1.389897 | 1/1 · 0.408227 | 0/1 · 1.411625 | 1/1 · 0.421711 | 0/1 · 4.641561 | 0/1 · 3.162327 | 0/1 · 1.386294 | 1/1 · 1.317943 | 1/1 · 0.049332 |
| data:pilot-v2:intent-b:g239 | 1 | 1 | teacher_agreement | 0/1 · 1.116199 | 1/1 · 0.004091 | 1/1 · 0.006772 | 1/1 · 0.000953 | 1/1 · 0.015802 | 1/1 · 0.053520 | 1/1 · 1.098612 | 1/1 · 0.979211 | 1/1 · 0.135162 |
| data:pilot-v2:intent-b:g240 | 1 | 1 | teacher_agreement | 0/1 · 1.374376 | 1/1 · 0.279740 | 0/1 · 1.736576 | 1/1 · 0.666042 | 1/1 · 0.267088 | 1/1 · 0.376348 | 1/1 · 1.386294 | 0/1 · 1.388610 | 0/1 · 2.266698 |
| data:pilot-v2:rule-a:g011 | 8 | 1 | rule_verified_accuracy | 2/8 · 1.384340 | 0/8 · 1.552475 | 1/8 · 1.421508 | 0/8 · 1.491364 | 1/8 · 1.441992 | 0/8 · 1.508778 | 3/8 · 1.386294 | 0/8 · 1.485718 | 2/8 · 2.188600 |
| data:pilot-v2:rule-a:g012 | 8 | 1 | rule_verified_accuracy | 4/8 · 1.382281 | 1/8 · 1.557083 | 1/8 · 1.573412 | 1/8 · 2.123043 | 1/8 · 1.633191 | 1/8 · 1.993223 | 2/8 · 1.386294 | 1/8 · 1.427169 | 3/8 · 1.505422 |
| data:pilot-v2:rule-a:g013 | 8 | 1 | rule_verified_accuracy | 1/8 · 1.386204 | 0/8 · 1.398381 | 0/8 · 1.391744 | 3/8 · 1.385232 | 0/8 · 1.396849 | 2/8 · 1.391818 | 2/8 · 1.386294 | 2/8 · 1.386294 | 1/8 · 2.062968 |
| data:pilot-v2:rule-a:g014 | 8 | 1 | rule_verified_accuracy | 4/8 · 1.377974 | 1/8 · 1.426493 | 1/8 · 1.401250 | 1/8 · 1.600959 | 2/8 · 1.408950 | 1/8 · 1.498519 | 1/8 · 1.386294 | 1/8 · 1.451819 | 3/8 · 2.294756 |
| data:pilot-v2:rule-a:g015 | 8 | 1 | rule_verified_accuracy | 1/8 · 1.100966 | 1/8 · 1.106696 | 4/8 · 1.097004 | 4/8 · 1.094316 | 4/8 · 1.084941 | 3/8 · 1.082073 | 3/8 · 1.098612 | 2/8 · 1.107782 | 3/8 · 1.864751 |
| data:pilot-v2:rule-b:g011 | 8 | 1 | rule_verified_accuracy | 2/8 · 1.240372 | 3/8 · 1.227640 | 2/8 · 1.267757 | 4/8 · 1.241423 | 3/8 · 1.234193 | 3/8 · 1.256601 | 1/8 · 1.242453 | 1/8 · 1.248455 | 2/8 · 1.569472 |
| data:pilot-v2:rule-b:g012 | 8 | 1 | rule_verified_accuracy | 2/8 · 1.242787 | 3/8 · 1.230084 | 2/8 · 1.251959 | 1/8 · 1.245580 | 3/8 · 1.250031 | 1/8 · 1.246473 | 3/8 · 1.242453 | 3/8 · 1.207124 | 1/8 · 2.194044 |
| data:pilot-v2:rule-b:g013 | 8 | 1 | rule_verified_accuracy | 0/8 · 1.386966 | 1/8 · 1.396268 | 2/8 · 1.383169 | 5/8 · 1.379466 | 1/8 · 1.393202 | 1/8 · 1.418862 | 5/8 · 1.386294 | 5/8 · 1.386294 | 5/8 · 0.876190 |
| data:pilot-v2:rule-b:g014 | 8 | 1 | rule_verified_accuracy | 3/8 · 1.383897 | 2/8 · 1.388008 | 1/8 · 1.598831 | 0/8 · 1.413877 | 1/8 · 1.395673 | 0/8 · 1.465794 | 0/8 · 1.386294 | 0/8 · 1.398683 | 1/8 · 1.871353 |
| data:pilot-v2:rule-b:g015 | 8 | 1 | rule_verified_accuracy | 2/8 · 1.134585 | 3/8 · 1.149183 | 1/8 · 1.198948 | 2/8 · 1.136398 | 3/8 · 1.114556 | 2/8 · 1.188327 | 3/8 · 1.134573 | 2/8 · 1.134509 | 4/8 · 1.227204 |
| data:pilot-v2:sentiment-a:g201 | 1 | 1 | teacher_agreement | 0/1 · 1.377831 | 1/1 · 1.084244 | 0/1 · 1.510612 | 0/1 · 1.822906 | 0/1 · 1.365984 | 0/1 · 1.449626 | 1/1 · 1.386294 | 0/1 · 1.402551 | 0/1 · 3.177050 |
| data:pilot-v2:sentiment-a:g202 | 1 | 1 | teacher_agreement | 0/1 · 1.385838 | 0/1 · 1.274330 | 0/1 · 1.272801 | 1/1 · 0.407901 | 0/1 · 1.147736 | 1/1 · 1.056671 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 4.227365 |
| data:pilot-v2:sentiment-a:g203 | 1 | 1 | teacher_agreement | 0/1 · 1.386433 | 1/1 · 0.166230 | 0/1 · 1.342739 | 1/1 · 0.399619 | 1/1 · 1.102751 | 0/1 · 1.398926 | 1/1 · 1.386294 | 1/1 · 1.386294 | 1/1 · 0.563217 |
| data:pilot-v2:sentiment-a:g204 | 1 | 1 | teacher_agreement | 1/1 · 1.374538 | 1/1 · 0.579345 | 1/1 · 1.356715 | 1/1 · 1.078341 | 0/1 · 1.543523 | 1/1 · 1.354288 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.381768 |
| data:pilot-v2:sentiment-a:g205 | 1 | 1 | teacher_agreement | 1/1 · 1.378683 | 1/1 · 0.934659 | 0/1 · 1.373568 | 0/1 · 2.671590 | 0/1 · 1.811803 | 0/1 · 1.442221 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 7.001487 |
| data:pilot-v2:sentiment-a:g206 | 1 | 1 | teacher_agreement | 0/1 · 1.382123 | 1/1 · 1.179177 | 1/1 · 1.204016 | 1/1 · 0.555999 | 1/1 · 0.942995 | 1/1 · 0.929998 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 3.156694 |
| data:pilot-v2:sentiment-a:g207 | 1 | 1 | teacher_agreement | 0/1 · 1.387714 | 1/1 · 0.444382 | 0/1 · 1.809960 | 1/1 · 0.952502 | 0/1 · 1.989876 | 0/1 · 1.568249 | 0/1 · 1.386294 | 1/1 · 1.279217 | 1/1 · 0.044155 |
| data:pilot-v2:sentiment-a:g208 | 1 | 1 | teacher_agreement | 0/1 · 1.400970 | 0/1 · 1.233519 | 0/1 · 1.475724 | 1/1 · 0.913133 | 0/1 · 1.738391 | 0/1 · 1.424010 | 0/1 · 1.386294 | 0/1 · 1.418140 | 1/1 · 0.543842 |
| data:pilot-v2:sentiment-a:g209 | 1 | 1 | teacher_agreement | 0/1 · 1.377895 | 1/1 · 0.802483 | 0/1 · 1.380049 | 0/1 · 1.804925 | 0/1 · 1.362682 | 1/1 · 1.295200 | 0/1 · 1.386294 | 1/1 · 1.342301 | 1/1 · 0.432880 |
| data:pilot-v2:sentiment-a:g210 | 1 | 1 | teacher_agreement | 0/1 · 1.398018 | 0/1 · 1.660757 | 0/1 · 1.418704 | 1/1 · 0.278913 | 0/1 · 1.627739 | 1/1 · 1.091635 | 0/1 · 1.386294 | 0/1 · 1.403421 | 0/1 · 3.910386 |
| data:pilot-v2:sentiment-a:g211 | 1 | 1 | teacher_agreement | 0/1 · 1.421615 | 1/1 · 0.028448 | 0/1 · 1.373967 | 1/1 · 0.396518 | 1/1 · 0.628299 | 1/1 · 1.328861 | 0/1 · 1.386294 | 0/1 · 1.388382 | 0/1 · 5.868504 |
| data:pilot-v2:sentiment-a:g212 | 1 | 1 | teacher_agreement | 0/1 · 1.380789 | 1/1 · 0.608904 | 1/1 · 1.302597 | 0/1 · 1.041296 | 0/1 · 1.690777 | 1/1 · 1.228481 | 1/1 · 1.386294 | 1/1 · 1.382487 | 1/1 · 0.084076 |
| data:pilot-v2:sentiment-a:g213 | 1 | 1 | teacher_agreement | 0/1 · 1.385947 | 0/1 · 1.111386 | 0/1 · 1.414083 | 0/1 · 1.521215 | 0/1 · 1.467030 | 0/1 · 1.349145 | 0/1 · 1.386294 | 0/1 · 1.406147 | 0/1 · 1.346927 |
| data:pilot-v2:sentiment-a:g214 | 1 | 1 | teacher_agreement | 0/1 · 1.372495 | 0/1 · 1.210424 | 0/1 · 1.473799 | 1/1 · 0.460878 | 0/1 · 2.964735 | 0/1 · 1.319174 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 3.065916 |
| data:pilot-v2:sentiment-a:g215 | 1 | 1 | teacher_agreement | 0/1 · 1.408936 | 1/1 · 0.046582 | 0/1 · 1.437801 | 1/1 · 0.295367 | 1/1 · 0.904894 | 0/1 · 1.438508 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.017150 |
| data:pilot-v2:sentiment-a:g216 | 1 | 1 | teacher_agreement | 0/1 · 1.392828 | 1/1 · 0.942759 | 0/1 · 1.545721 | 0/1 · 1.524890 | 0/1 · 1.478771 | 0/1 · 1.656162 | 1/1 · 1.386294 | 1/1 · 1.386294 | 1/1 · 0.114011 |
| data:pilot-v2:sentiment-a:g217 | 1 | 1 | teacher_agreement | 1/1 · 1.375439 | 0/1 · 1.582110 | 0/1 · 1.471796 | 0/1 · 3.162076 | 0/1 · 1.513385 | 0/1 · 1.452971 | 0/1 · 1.386294 | 0/1 · 1.412557 | 1/1 · 0.009681 |
| data:pilot-v2:sentiment-a:g218 | 1 | 1 | teacher_agreement | 0/1 · 1.389360 | 0/1 · 1.230426 | 1/1 · 1.310565 | 0/1 · 1.341011 | 0/1 · 1.960766 | 1/1 · 1.336537 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.351865 |
| data:pilot-v2:sentiment-a:g219 | 1 | 1 | teacher_agreement | 0/1 · 1.389171 | 1/1 · 0.114252 | 0/1 · 1.626489 | 1/1 · 0.794295 | 0/1 · 2.663102 | 0/1 · 1.505670 | 1/1 · 1.386294 | 1/1 · 1.386294 | 1/1 · 0.334005 |
| data:pilot-v2:sentiment-a:g220 | 1 | 1 | teacher_agreement | 1/1 · 1.376584 | 0/1 · 1.404529 | 0/1 · 1.462637 | 1/1 · 1.318039 | 0/1 · 1.044811 | 0/1 · 1.613676 | 0/1 · 1.386294 | 0/1 · 1.403421 | 0/1 · 5.056308 |
| data:pilot-v2:sentiment-a:g221 | 1 | 1 | teacher_agreement | 1/1 · 1.373479 | 0/1 · 1.682149 | 0/1 · 1.606619 | 0/1 · 2.925036 | 0/1 · 1.658473 | 0/1 · 1.336496 | 0/1 · 1.386294 | 0/1 · 1.352154 | 1/1 · 0.072155 |
| data:pilot-v2:sentiment-a:g222 | 1 | 1 | teacher_agreement | 1/1 · 1.378934 | 0/1 · 0.932463 | 1/1 · 1.230671 | 1/1 · 0.006732 | 0/1 · 3.780858 | 1/1 · 0.838583 | 0/1 · 1.386294 | 0/1 · 1.404635 | 0/1 · 1.285468 |
| data:pilot-v2:sentiment-a:g223 | 1 | 1 | teacher_agreement | 0/1 · 1.388519 | 0/1 · 1.252209 | 0/1 · 1.470181 | 1/1 · 0.561522 | 0/1 · 1.594687 | 0/1 · 1.449558 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.170114 |
| data:pilot-v2:sentiment-a:g224 | 1 | 1 | teacher_agreement | 1/1 · 1.373586 | 1/1 · 0.630517 | 0/1 · 1.443714 | 0/1 · 1.452051 | 0/1 · 1.578071 | 0/1 · 1.350913 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.692060 |
| data:pilot-v2:sentiment-a:g225 | 1 | 1 | teacher_agreement | 0/1 · 1.381947 | 1/1 · 0.957741 | 1/1 · 1.113458 | 0/1 · 1.640733 | 1/1 · 1.019971 | 0/1 · 1.287127 | 1/1 · 1.386294 | 0/1 · 1.386532 | 0/1 · 3.802090 |
| data:pilot-v2:sentiment-a:g226 | 1 | 1 | teacher_agreement | 0/1 · 1.393760 | 0/1 · 1.553831 | 0/1 · 1.423166 | 1/1 · 0.889377 | 1/1 · 1.288737 | 1/1 · 1.040411 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.523965 |
| data:pilot-v2:sentiment-a:g227 | 1 | 1 | teacher_agreement | 0/1 · 1.430830 | 1/1 · 0.269737 | 1/1 · 1.228401 | 1/1 · 0.375312 | 1/1 · 0.472973 | 0/1 · 1.286211 | 0/1 · 1.386294 | 0/1 · 1.410814 | 0/1 · 4.926005 |
| data:pilot-v2:sentiment-a:g228 | 1 | 1 | teacher_agreement | 0/1 · 1.394337 | 0/1 · 1.200721 | 0/1 · 1.520259 | 1/1 · 0.289111 | 0/1 · 1.473697 | 0/1 · 1.386881 | 0/1 · 1.386294 | 0/1 · 1.403042 | 0/1 · 4.095438 |
| data:pilot-v2:sentiment-a:g229 | 1 | 1 | teacher_agreement | 0/1 · 1.388069 | 0/1 · 1.517908 | 0/1 · 1.482310 | 0/1 · 1.771290 | 0/1 · 1.422826 | 0/1 · 1.407015 | 0/1 · 1.386294 | 0/1 · 1.371434 | 1/1 · 0.416823 |
| data:pilot-v2:sentiment-a:g230 | 1 | 1 | teacher_agreement | 0/1 · 1.383022 | 0/1 · 1.248183 | 0/1 · 1.376804 | 1/1 · 0.776100 | 0/1 · 3.178296 | 1/1 · 1.180422 | 1/1 · 1.386294 | 1/1 · 1.386294 | 1/1 · 0.272437 |
| data:pilot-v2:sentiment-a:g231 | 1 | 1 | teacher_agreement | 0/1 · 1.384482 | 1/1 · 0.164338 | 1/1 · 1.260261 | 1/1 · 0.195126 | 1/1 · 1.196809 | 0/1 · 1.368577 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.114277 |
| data:pilot-v2:sentiment-a:g232 | 1 | 1 | teacher_agreement | 0/1 · 1.387637 | 1/1 · 0.839089 | 0/1 · 1.372032 | 1/1 · 0.874902 | 0/1 · 1.303102 | 1/1 · 1.112275 | 0/1 · 1.386294 | 1/1 · 1.286007 | 1/1 · 0.207558 |
| data:pilot-v2:sentiment-a:g233 | 1 | 1 | teacher_agreement | 0/1 · 1.384989 | 1/1 · 1.059352 | 1/1 · 1.104880 | 0/1 · 2.309609 | 1/1 · 0.867479 | 0/1 · 1.465632 | 0/1 · 1.386294 | 0/1 · 1.403627 | 0/1 · 4.825024 |
| data:pilot-v2:sentiment-a:g234 | 1 | 1 | teacher_agreement | 0/1 · 1.390316 | 0/1 · 1.322469 | 0/1 · 1.394279 | 0/1 · 1.225802 | 0/1 · 1.739117 | 0/1 · 1.372929 | 1/1 · 1.386294 | 0/1 · 1.404831 | 1/1 · 0.148533 |
| data:pilot-v2:sentiment-a:g235 | 1 | 1 | teacher_agreement | 0/1 · 1.397633 | 1/1 · 0.167487 | 0/1 · 1.442048 | 1/1 · 0.287072 | 1/1 · 0.950825 | 0/1 · 1.342680 | 1/1 · 1.386294 | 1/1 · 1.386294 | 1/1 · 0.210151 |
| data:pilot-v2:sentiment-a:g236 | 1 | 1 | teacher_agreement | 0/1 · 1.378414 | 1/1 · 0.910983 | 0/1 · 1.305589 | 0/1 · 1.299633 | 0/1 · 2.533008 | 0/1 · 1.436074 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.314875 |
| data:pilot-v2:sentiment-a:g237 | 1 | 1 | teacher_agreement | 0/1 · 1.384737 | 0/1 · 1.379243 | 0/1 · 1.539915 | 0/1 · 1.731238 | 0/1 · 1.540119 | 0/1 · 1.484119 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.738523 |
| data:pilot-v2:sentiment-a:g238 | 1 | 1 | teacher_agreement | 1/1 · 1.374678 | 0/1 · 1.487408 | 0/1 · 1.525596 | 0/1 · 3.774937 | 0/1 · 2.365243 | 0/1 · 1.554783 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 5.204453 |
| data:pilot-v2:sentiment-a:g239 | 1 | 1 | teacher_agreement | 0/1 · 1.388696 | 1/1 · 0.459830 | 1/1 · 1.288126 | 1/1 · 0.420631 | 1/1 · 1.089247 | 0/1 · 1.443145 | 0/1 · 1.386294 | 0/1 · 1.404831 | 0/1 · 2.666235 |
| data:pilot-v2:sentiment-a:g240 | 1 | 1 | teacher_agreement | 1/1 · 1.381808 | 0/1 · 1.428744 | 0/1 · 1.426612 | 0/1 · 3.665120 | 0/1 · 1.084690 | 0/1 · 1.566387 | 0/1 · 1.386294 | 0/1 · 1.422003 | 0/1 · 3.235482 |
| data:pilot-v2:sentiment-b:g201 | 1 | 1 | teacher_agreement | 1/1 · 1.375192 | 0/1 · 1.107350 | 0/1 · 1.409322 | 1/1 · 0.473031 | 0/1 · 1.078187 | 0/1 · 1.325601 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 2.183680 |
| data:pilot-v2:sentiment-b:g202 | 1 | 1 | teacher_agreement | 0/1 · 1.376749 | 0/1 · 1.308974 | 1/1 · 1.218258 | 1/1 · 1.027427 | 1/1 · 0.905361 | 1/1 · 1.135346 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 4.403441 |
| data:pilot-v2:sentiment-b:g203 | 1 | 1 | teacher_agreement | 0/1 · 1.438103 | 1/1 · 0.223594 | 0/1 · 1.513070 | 0/1 · 1.382101 | 0/1 · 1.277687 | 0/1 · 1.472561 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.062595 |
| data:pilot-v2:sentiment-b:g204 | 1 | 1 | teacher_agreement | 1/1 · 1.370931 | 0/1 · 1.293064 | 0/1 · 1.430570 | 1/1 · 0.965454 | 0/1 · 2.165802 | 0/1 · 1.598291 | 0/1 · 1.386294 | 0/1 · 1.406144 | 1/1 · 0.412831 |
| data:pilot-v2:sentiment-b:g205 | 1 | 1 | teacher_agreement | 0/1 · 1.382885 | 0/1 · 1.303993 | 1/1 · 1.185401 | 1/1 · 0.993618 | 1/1 · 1.121582 | 1/1 · 1.316794 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 2.693690 |
| data:pilot-v2:sentiment-b:g206 | 1 | 1 | teacher_agreement | 0/1 · 1.382601 | 0/1 · 0.996120 | 1/1 · 1.232615 | 1/1 · 0.808409 | 0/1 · 1.801551 | 0/1 · 1.290218 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.021128 |
| data:pilot-v2:sentiment-b:g207 | 1 | 1 | teacher_agreement | 0/1 · 1.398946 | 1/1 · 0.290030 | 1/1 · 1.198420 | 1/1 · 1.065656 | 1/1 · 0.856599 | 1/1 · 1.338071 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.206485 |
| data:pilot-v2:sentiment-b:g208 | 1 | 1 | teacher_agreement | 1/1 · 1.354724 | 0/1 · 1.309925 | 0/1 · 1.467270 | 0/1 · 1.613513 | 0/1 · 1.398637 | 0/1 · 1.328740 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 1.607183 |
| data:pilot-v2:sentiment-b:g209 | 1 | 1 | teacher_agreement | 0/1 · 1.376753 | 0/1 · 1.263917 | 0/1 · 1.275084 | 1/1 · 1.177883 | 0/1 · 1.396315 | 0/1 · 1.324673 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.636085 |
| data:pilot-v2:sentiment-b:g210 | 1 | 1 | teacher_agreement | 0/1 · 1.374986 | 1/1 · 1.234154 | 0/1 · 1.287324 | 1/1 · 0.522319 | 0/1 · 1.312373 | 1/1 · 1.215773 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 5.177219 |
| data:pilot-v2:sentiment-b:g211 | 1 | 1 | teacher_agreement | 1/1 · 1.374070 | 1/1 · 1.137523 | 0/1 · 1.374802 | 0/1 · 1.586785 | 0/1 · 1.917862 | 0/1 · 1.444733 | 0/1 · 1.386294 | 0/1 · 1.405678 | 1/1 · 0.247361 |
| data:pilot-v2:sentiment-b:g212 | 1 | 1 | teacher_agreement | 0/1 · 1.378010 | 1/1 · 1.106093 | 0/1 · 1.421204 | 0/1 · 1.790918 | 0/1 · 2.098895 | 0/1 · 1.415662 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.364535 |
| data:pilot-v2:sentiment-b:g213 | 1 | 1 | teacher_agreement | 0/1 · 1.405723 | 1/1 · 0.177486 | 0/1 · 1.408260 | 0/1 · 1.368347 | 0/1 · 2.512349 | 0/1 · 1.424009 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.882463 |
| data:pilot-v2:sentiment-b:g214 | 1 | 1 | teacher_agreement | 0/1 · 1.377898 | 0/1 · 1.515996 | 0/1 · 1.366665 | 0/1 · 1.827849 | 0/1 · 1.563624 | 0/1 · 1.414729 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 5.271190 |
| data:pilot-v2:sentiment-b:g215 | 1 | 1 | teacher_agreement | 1/1 · 1.380059 | 1/1 · 1.027388 | 0/1 · 1.340832 | 0/1 · 1.414514 | 0/1 · 1.867825 | 0/1 · 1.392224 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.013739 |
| data:pilot-v2:sentiment-b:g216 | 1 | 1 | teacher_agreement | 0/1 · 1.391382 | 1/1 · 0.706025 | 0/1 · 1.511350 | 1/1 · 0.014549 | 1/1 · 0.859748 | 0/1 · 1.287874 | 0/1 · 1.386294 | 0/1 · 1.404446 | 0/1 · 3.136323 |
| data:pilot-v2:sentiment-b:g217 | 1 | 1 | teacher_agreement | 0/1 · 1.392751 | 1/1 · 0.175756 | 1/1 · 1.057104 | 1/1 · 0.551232 | 1/1 · 0.968454 | 1/1 · 1.239359 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.753148 |
| data:pilot-v2:sentiment-b:g218 | 1 | 1 | teacher_agreement | 1/1 · 1.377536 | 1/1 · 1.166667 | 0/1 · 1.519951 | 0/1 · 1.351879 | 0/1 · 1.512904 | 0/1 · 1.664021 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.470346 |
| data:pilot-v2:sentiment-b:g219 | 1 | 1 | teacher_agreement | 0/1 · 1.414308 | 1/1 · 0.110472 | 0/1 · 1.213647 | 1/1 · 0.796932 | 0/1 · 1.378627 | 0/1 · 1.254472 | 0/1 · 1.386294 | 0/1 · 1.393606 | 0/1 · 3.515560 |
| data:pilot-v2:sentiment-b:g220 | 1 | 1 | teacher_agreement | 0/1 · 1.376861 | 1/1 · 0.990134 | 0/1 · 1.387661 | 0/1 · 1.464038 | 0/1 · 1.275829 | 0/1 · 1.363935 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.622492 |
| data:pilot-v2:sentiment-b:g221 | 1 | 1 | teacher_agreement | 0/1 · 1.388015 | 0/1 · 1.115724 | 0/1 · 1.380619 | 0/1 · 1.604598 | 1/1 · 0.946518 | 0/1 · 1.480655 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.574823 |
| data:pilot-v2:sentiment-b:g222 | 1 | 1 | teacher_agreement | 0/1 · 1.374140 | 0/1 · 1.197919 | 0/1 · 1.370049 | 1/1 · 0.549729 | 0/1 · 2.208434 | 1/1 · 0.999401 | 1/1 · 1.386294 | 0/1 · 1.407057 | 1/1 · 0.313303 |
| data:pilot-v2:sentiment-b:g223 | 1 | 1 | teacher_agreement | 0/1 · 1.421140 | 1/1 · 0.231827 | 0/1 · 1.631138 | 0/1 · 1.506908 | 0/1 · 1.614398 | 0/1 · 1.617535 | 1/1 · 1.386294 | 1/1 · 1.386294 | 1/1 · 0.638310 |
| data:pilot-v2:sentiment-b:g224 | 1 | 1 | teacher_agreement | 0/1 · 1.385776 | 0/1 · 1.627564 | 0/1 · 1.672225 | 0/1 · 1.401762 | 0/1 · 2.884002 | 0/1 · 1.457268 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.038522 |
| data:pilot-v2:sentiment-b:g225 | 1 | 1 | teacher_agreement | 1/1 · 1.371646 | 1/1 · 0.974868 | 0/1 · 1.367296 | 1/1 · 0.657357 | 0/1 · 1.274735 | 0/1 · 1.370631 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 1.223842 |
| data:pilot-v2:sentiment-b:g226 | 1 | 1 | teacher_agreement | 0/1 · 1.375887 | 0/1 · 1.183264 | 0/1 · 1.226469 | 1/1 · 0.582086 | 0/1 · 1.919011 | 1/1 · 0.964439 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 4.229659 |
| data:pilot-v2:sentiment-b:g227 | 1 | 1 | teacher_agreement | 0/1 · 1.413372 | 1/1 · 0.389766 | 0/1 · 1.387106 | 1/1 · 0.930256 | 1/1 · 0.703255 | 0/1 · 1.405873 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 0.880757 |
| data:pilot-v2:sentiment-b:g228 | 1 | 1 | teacher_agreement | 0/1 · 1.384644 | 1/1 · 0.949678 | 0/1 · 1.428446 | 1/1 · 0.590794 | 0/1 · 1.360121 | 1/1 · 1.122635 | 1/1 · 1.386294 | 0/1 · 1.407560 | 0/1 · 2.189027 |
| data:pilot-v2:sentiment-b:g229 | 1 | 1 | teacher_agreement | 0/1 · 1.378272 | 1/1 · 0.882587 | 0/1 · 1.423048 | 0/1 · 1.192897 | 0/1 · 1.407594 | 0/1 · 1.356814 | 0/1 · 1.386294 | 0/1 · 1.364957 | 0/1 · 2.231930 |
| data:pilot-v2:sentiment-b:g230 | 1 | 1 | teacher_agreement | 0/1 · 1.386721 | 0/1 · 1.477442 | 0/1 · 1.754183 | 0/1 · 2.695496 | 1/1 · 1.036695 | 0/1 · 1.351121 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.290541 |
| data:pilot-v2:sentiment-b:g231 | 1 | 1 | teacher_agreement | 0/1 · 1.385458 | 0/1 · 1.082096 | 0/1 · 1.397744 | 0/1 · 1.459125 | 0/1 · 1.123962 | 0/1 · 1.469430 | 0/1 · 1.386294 | 0/1 · 1.405735 | 0/1 · 1.521419 |
| data:pilot-v2:sentiment-b:g232 | 1 | 1 | teacher_agreement | 0/1 · 1.382239 | 0/1 · 1.388661 | 1/1 · 1.235201 | 1/1 · 1.017904 | 1/1 · 0.831638 | 0/1 · 1.254469 | 1/1 · 1.386294 | 1/1 · 1.386294 | 0/1 · 5.409896 |
| data:pilot-v2:sentiment-b:g233 | 1 | 1 | teacher_agreement | 0/1 · 1.392359 | 1/1 · 0.183520 | 0/1 · 1.455245 | 1/1 · 0.865144 | 1/1 · 0.639403 | 1/1 · 1.332430 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.777791 |
| data:pilot-v2:sentiment-b:g234 | 1 | 1 | teacher_agreement | 1/1 · 1.373753 | 1/1 · 0.940294 | 0/1 · 1.399318 | 1/1 · 1.167530 | 0/1 · 1.551252 | 0/1 · 1.329499 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 2.111124 |
| data:pilot-v2:sentiment-b:g235 | 1 | 1 | teacher_agreement | 0/1 · 1.385367 | 0/1 · 1.303976 | 0/1 · 1.411340 | 0/1 · 2.406120 | 0/1 · 3.080072 | 0/1 · 1.515801 | 0/1 · 1.386294 | 0/1 · 1.405240 | 0/1 · 1.318366 |
| data:pilot-v2:sentiment-b:g236 | 1 | 1 | teacher_agreement | 0/1 · 1.384714 | 0/1 · 1.054587 | 1/1 · 1.253364 | 1/1 · 0.676184 | 0/1 · 2.057602 | 1/1 · 1.258224 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 1.512505 |
| data:pilot-v2:sentiment-b:g237 | 1 | 1 | teacher_agreement | 0/1 · 1.404837 | 1/1 · 0.136602 | 1/1 · 1.235929 | 1/1 · 0.790939 | 1/1 · 0.931985 | 1/1 · 1.348127 | 0/1 · 1.386294 | 0/1 · 1.386294 | 1/1 · 0.017570 |
| data:pilot-v2:sentiment-b:g238 | 1 | 1 | teacher_agreement | 0/1 · 1.386630 | 0/1 · 1.751545 | 0/1 · 1.523929 | 0/1 · 5.478944 | 0/1 · 3.748737 | 0/1 · 1.732691 | 0/1 · 1.386294 | 0/1 · 1.462216 | 0/1 · 2.069598 |
| data:pilot-v2:sentiment-b:g239 | 1 | 1 | teacher_agreement | 0/1 · 1.402264 | 1/1 · 0.112650 | 0/1 · 1.573031 | 0/1 · 1.378893 | 0/1 · 2.441527 | 0/1 · 1.419284 | 0/1 · 1.386294 | 1/1 · 1.325082 | 1/1 · 0.000535 |
| data:pilot-v2:sentiment-b:g240 | 1 | 1 | teacher_agreement | 1/1 · 1.367133 | 1/1 · 0.809732 | 0/1 · 1.337334 | 0/1 · 1.570855 | 0/1 · 1.319231 | 1/1 · 1.086888 | 0/1 · 1.386294 | 0/1 · 1.386294 | 0/1 · 3.630840 |

## Paired comparisons

Differences are left minus right on common-valid IDs. Positive agreement favors left; negative loss favors left. Full coverage remains above.

| Left | Right | Common/total | Agreement delta | Left loss | Right loss | Loss delta | Loss delta status | Left-only correct | Right-only correct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | m4-minilm-trained | 240/240 | -0.275000 | 1.332467 | 0.823115 | 0.509351 | finite | 27 | 93 |
| m4-minilm-random-start | m4-msmarco-pretrained-start | 240/240 | -0.137500 | 1.332467 | 1.058568 | 0.273899 | finite | 37 | 70 |
| m4-minilm-random-start | m4-msmarco-trained | 240/240 | -0.312500 | 1.332467 | 0.917258 | 0.415208 | finite | 30 | 105 |
| m4-minilm-random-start | m2-v1-trained | 240/240 | -0.170833 | 1.332467 | 1.136427 | 0.196039 | finite | 36 | 77 |
| m4-minilm-random-start | m3-v1-trained | 240/240 | -0.183333 | 1.332467 | 1.024844 | 0.307623 | finite | 36 | 80 |
| m4-minilm-random-start | uniform | 240/240 | 0.004167 | 1.332467 | 1.333463 | -0.000997 | finite | 50 | 49 |
| m4-minilm-random-start | lexical | 240/240 | -0.137500 | 1.332467 | 1.296868 | 0.035599 | finite | 38 | 71 |
| m4-minilm-random-start | qwen25-05b-instruct-frozen | 240/240 | -0.262500 | 1.332467 | 1.312350 | 0.020117 | finite | 26 | 89 |
| m4-minilm-trained | m4-msmarco-pretrained-start | 240/240 | 0.137500 | 0.823115 | 1.058568 | -0.235452 | finite | 55 | 22 |
| m4-minilm-trained | m4-msmarco-trained | 240/240 | -0.037500 | 0.823115 | 0.917258 | -0.094143 | finite | 32 | 41 |
| m4-minilm-trained | m2-v1-trained | 240/240 | 0.104167 | 0.823115 | 1.136427 | -0.313312 | finite | 43 | 18 |
| m4-minilm-trained | m3-v1-trained | 240/240 | 0.091667 | 0.823115 | 1.024844 | -0.201728 | finite | 45 | 23 |
| m4-minilm-trained | uniform | 240/240 | 0.279167 | 0.823115 | 1.333463 | -0.510348 | finite | 96 | 29 |
| m4-minilm-trained | lexical | 240/240 | 0.137500 | 0.823115 | 1.296868 | -0.473753 | finite | 51 | 18 |
| m4-minilm-trained | qwen25-05b-instruct-frozen | 240/240 | 0.012500 | 0.823115 | 1.312350 | -0.489234 | finite | 38 | 35 |
| m4-msmarco-pretrained-start | m4-msmarco-trained | 240/240 | -0.175000 | 1.058568 | 0.917258 | 0.141309 | finite | 12 | 54 |
| m4-msmarco-pretrained-start | m2-v1-trained | 240/240 | -0.033333 | 1.058568 | 1.136427 | -0.077860 | finite | 21 | 29 |
| m4-msmarco-pretrained-start | m3-v1-trained | 240/240 | -0.045833 | 1.058568 | 1.024844 | 0.033724 | finite | 20 | 31 |
| m4-msmarco-pretrained-start | uniform | 240/240 | 0.141667 | 1.058568 | 1.333463 | -0.274896 | finite | 72 | 38 |
| m4-msmarco-pretrained-start | lexical | 240/240 | 0.000000 | 1.058568 | 1.296868 | -0.238300 | finite | 30 | 30 |
| m4-msmarco-pretrained-start | qwen25-05b-instruct-frozen | 240/240 | -0.125000 | 1.058568 | 1.312350 | -0.253782 | finite | 30 | 60 |
| m4-msmarco-trained | m2-v1-trained | 240/240 | 0.141667 | 0.917258 | 1.136427 | -0.219169 | finite | 50 | 16 |
| m4-msmarco-trained | m3-v1-trained | 240/240 | 0.129167 | 0.917258 | 1.024844 | -0.107585 | finite | 43 | 12 |
| m4-msmarco-trained | uniform | 240/240 | 0.316667 | 0.917258 | 1.333463 | -0.416205 | finite | 102 | 26 |
| m4-msmarco-trained | lexical | 240/240 | 0.175000 | 0.917258 | 1.296868 | -0.379610 | finite | 61 | 19 |
| m4-msmarco-trained | qwen25-05b-instruct-frozen | 240/240 | 0.050000 | 0.917258 | 1.312350 | -0.395091 | finite | 46 | 34 |
| m2-v1-trained | m3-v1-trained | 240/240 | -0.012500 | 1.136427 | 1.024844 | 0.111583 | finite | 25 | 28 |
| m2-v1-trained | uniform | 240/240 | 0.175000 | 1.136427 | 1.333463 | -0.197036 | finite | 76 | 34 |
| m2-v1-trained | lexical | 240/240 | 0.033333 | 1.136427 | 1.296868 | -0.160441 | finite | 37 | 29 |
| m2-v1-trained | qwen25-05b-instruct-frozen | 240/240 | -0.091667 | 1.136427 | 1.312350 | -0.175922 | finite | 32 | 54 |
| m3-v1-trained | uniform | 240/240 | 0.187500 | 1.024844 | 1.333463 | -0.308620 | finite | 81 | 36 |
| m3-v1-trained | lexical | 240/240 | 0.045833 | 1.024844 | 1.296868 | -0.272024 | finite | 40 | 29 |
| m3-v1-trained | qwen25-05b-instruct-frozen | 240/240 | -0.079167 | 1.024844 | 1.312350 | -0.287506 | finite | 30 | 49 |
| uniform | lexical | 240/240 | -0.141667 | 1.333463 | 1.296868 | 0.036595 | finite | 20 | 54 |
| uniform | qwen25-05b-instruct-frozen | 240/240 | -0.266667 | 1.333463 | 1.312350 | 0.021114 | finite | 33 | 97 |
| lexical | qwen25-05b-instruct-frozen | 240/240 | -0.125000 | 1.296868 | 1.312350 | -0.015482 | finite | 22 | 52 |

## Option-order sensitivity

Quality uses complete pairs only. Tied choices can change while per-option probabilities remain unchanged. Reversal is one permutation, not proof of broad invariance.

| Predictor | Complete pairs | Groups | Original agreement | Reversed agreement | Choice consistency | Untied consistency | Either tied | Mean TV | Max probability change |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m4-minilm-random-start | 240/240 | 170 | 66/240 | 66/240 | 240/240 | 240/240 | 0 | 1.04e-10 | 1.93e-08 |
| m4-minilm-trained | 240/240 | 170 | 132/240 | 132/240 | 240/240 | 240/240 | 0 | 1.34e-10 | 1.92e-08 |
| m4-msmarco-pretrained-start | 240/240 | 170 | 99/240 | 99/240 | 240/240 | 240/240 | 0 | 1.38e-10 | 1.7e-08 |
| m4-msmarco-trained | 240/240 | 170 | 141/240 | 141/240 | 240/240 | 240/240 | 0 | 3.02e-10 | 1.96e-08 |
| m2-v1-trained | 240/240 | 170 | 107/240 | 107/240 | 240/240 | 240/240 | 0 | 3.2e-10 | 1.94e-08 |
| m3-v1-trained | 240/240 | 170 | 110/240 | 110/240 | 240/240 | 240/240 | 0 | 6.88e-11 | 3.98e-09 |
| uniform | 240/240 | 170 | 65/240 | 65/240 | 0/240 | 0/0 | 240 | 0 | 0 |
| lexical | 240/240 | 170 | 99/240 | 99/240 | 119/240 | 119/119 | 121 | 0 | 0 |
| qwen25-05b-instruct-frozen | 240/240 | 170 | 129/240 | 118/240 | 118/240 | 118/240 | 0 | 0.33 | 0.948 |

## Interpretation and reproducibility

These are validation-derived comparisons, not final evaluation. Teacher agreement is not independently verified correctness. Small correlated groups, synthetic coverage, and a single training seed limit interpretation; confidence diagnostics do not establish calibration.

Comparison report: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/comparison.json`; SHA-256 `04a0b0c6ea7de97a40f80ff0cbbd059c024cb8b4fc7acefb1fb7709ea5cb0b76`.
- m4-minilm-random-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/m4-minilm-random-start-order-report.json`; SHA-256 `f7752cc28268d8ea71f4f4b30038abdaa7388693732d38f195122d044005b979`.
- m4-minilm-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/m4-minilm-trained-order-report.json`; SHA-256 `3d2f2437718599a92e4c6a6085e35e81cd488bb013f32e9263ddaac8077ae362`.
- m4-msmarco-pretrained-start order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/m4-msmarco-pretrained-start-order-report.json`; SHA-256 `dcd2257f203753a17f66abe1b8690c4e1e4ab4fd31021eaf2db56c92d378ae16`.
- m4-msmarco-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/m4-msmarco-trained-order-report.json`; SHA-256 `1d2c3bcfebf48b2a0a3edf3c0160044d17c8355d024c550ab710dc3d79824514`.
- m2-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/m2-v1-trained-order-report.json`; SHA-256 `ec24fa67507b99cb202c74a259be39afc042195edca5bf19cb197454f4dcd0b6`.
- m3-v1-trained order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/m3-v1-trained-order-report.json`; SHA-256 `5e8676c2ac8214cbbcfd5480fce11d772a1dbf214402d375e36ce6ca7f5c50d3`.
- uniform order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/uniform-order-report.json`; SHA-256 `6c22f701ae6d8fd2208737893e2ee1f76d2218c65c43db87fbb7acc58ae8270c`.
- lexical order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/lexical-order-report.json`; SHA-256 `c9cac72db5ac161dc070284b1137b7fbb6262ef86f7b9037aa75f4c3c7d6403d`.
- qwen25-05b-instruct-frozen order: `/Users/destiner/Code/jeff/artifacts/evaluation/e5-comparison-preparation-v1/execution-01/study/new-v2/qwen25-05b-instruct-frozen-order-report.json`; SHA-256 `5b68ab0fee137719c1dcc989b8cb1fc8447e7cc840db14ddecb05f73eddac5bd`.
