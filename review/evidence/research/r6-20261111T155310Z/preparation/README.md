# R6 frozen order/letter packet — preparation code only

## Status and boundary

`prepare_order_packet.py` is a new, CPU/stdlib-only preparer for parent review/copy to `experiments/research/`. **It has not been run to generate a packet.** Source review and a syntax-only `ast.parse` succeeded; the preparer was not imported or executed. No model/tokenizer import, tokenization, asset/weight scan, download, inference, training, prediction inspection, paid work, dependency installation, tests, linting, mailbox action, commit or merge is part of this handoff. M6/P4/E6 and all released inputs remain unchanged. No held-out decision shards or private Evaluation/probe/D3/final data were opened.

TRAIN structural metadata and hashes were inspected to establish feasibility: the exact released manifest has nine TRAIN shards / 1,500 rows; each family has one 100-row inherited shard and two 200-row new-producer shards. Inherited intent/sentiment have 25 TRAIN groups each, inherited rules 10; each new intent/sentiment producer has 200 singleton TRAIN groups spanning 20 named domains; each new rule producer has 10 TRAIN mechanism groups. Thus the fixed 4+6+6 quota and distinct-group preference are feasible without using targets. No state, question or option text is reproduced here.

## Parent-only preparation invocation

After reviewing the source, run with an existing output parent and a **new** packet directory (this command does not run a model):

```sh
python3 -B /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/preparation/prepare_order_packet.py \
  --repo-root /Users/destiner/Code/jeff \
  --output-dir /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/packet-01
```

If copied, substitute the reviewed script path; the packet pins the actual preparer path/digest. No `uv`, packages or project-module imports are required. The script takes no prediction, label, alternative manifest, selection-seed or quota arguments. It prints only the packet path/hash and counts/status, never input text.

The preparer validates all sources and constructs all output bytes in memory before claiming the output directory via exclusive `mkdir`. Every file uses exclusive binary creation. It writes `packet.json` last, makes files mode `0444` and the directory `0555`; these are accidental-mutation guards, not security controls. Failure leaves a read-only partial directory, never an overwritten/repaired packet. Do not reuse that directory. Record the printed `packet_sha256` externally; packet.json cannot self-hash.

## Inputs and exclusions

- Only `artifacts/data/data-pilot-v2/manifest.json`, pinned to SHA-256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`, defines decision-shard identity. The nine expected TRAIN paths are an explicit allowlist in `SOURCES`.
- Only those TRAIN shards are opened/hashed. Their actual hashes, row counts, schema, TRAIN split, family, global unique case IDs, string fields, K=2..6 and unique option IDs are validated. Option objects must contain exactly `id,text`; output construction is a field whitelist. Targets are parsed incidentally with TRAIN JSON but their values are never accessed, validated, ranked or copied.
- Each TRAIN shard's sibling `group_assignments.json` is **allocation metadata, not a decision shard**. Its exact SHA is hardcoded. These files contain split allocations; only entries for loaded TRAIN groups are inspected, requiring `split=train` and a nonempty known domain and/or mechanism. Only domain/mechanism enter the metadata projection. Scenario-plan text and all other allocation fields are ignored. No metadata/source reference is followed to its referenced content.
- The manifest's nine validation entries are recorded as exclusions **from manifest metadata only**. The script checks TRAIN/excluded declared hashes are disjoint. It does not open, hash or join validation, final, probes, D3, references, predictions, source mappings or other historical decision files. It cannot independently establish cross-split content/root independence or private exclusion-list membership without unauthorized access; release identity plus the strict TRAIN path/hash allowlist is the exclusion guarantee here.
- Frozen P3 config bytes must match `2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f`. The current runtime **source file only** is hashed for handoff provenance; no runtime code is imported or executed.

## Exact pre-prediction selection

The full machine-readable algorithm is also saved in `selection.json`.

1. Visit families `intent`, `sentiment`, `rule_application`; within each, visit inherited, new A, new B in the explicit `SOURCES` order. Select exactly **4,6,6**, respectively: 16/family, 48 total. Fail on insufficient candidates; no quota redistribution, outcome-based replacement or silent reduction.
2. Project metadata only: original TRAIN ID; group; source path/producer; `provenance.parent_id`, `scenario_id`, `source`; TRAIN allocation domain/mechanism. Root is `parent_id` else `scenario_id` else case ID. Rule policy is group ID; other policy is null. Broad source is `provenance.source` before its first `#`, then before its first `;case=`. These are identity/grouping strings, never dereferenced. An ID may represent a producer-defined singleton; this is not proof of an independent semantic root.
3. Hash rank is lowercase hex SHA-256 of UTF-8 **`R6/train/orderdiagnostic/v1` + LF + original TRAIN ID**, no trailing LF. Hash ties break on ID ascending.
4. Reset counts per source bucket. At each pick first restrict to candidates with unused root, group, and non-null policy if any such candidate exists; otherwise allow repeats and flag `uniqueness_fallback`. Among that pool minimize lexicographically `(domain_count + mechanism_count, domain_count, mechanism_count, broad_source_count, group_count, hash_rank, case_id)`. Null domain/mechanism contributes zero. Update all counts after each pick. This is a deterministic greedy broad-coverage heuristic, not a claim of globally optimal stratification or representative sampling.
5. Retain bucket/pick order, then emit the four conditions below in fixed order. Input text, targets, option counts, label positions and predictions have no role in ranking. No sampling is performed after predictions.

Known metadata limits: new rule allocations provide mechanism, not domain; new intent/sentiment provide domain, not mechanism. Missing values remain null, not inferred from text or targets. Parent/scenario metadata may not identify every semantic relationship. The uniqueness preference works at released metadata granularity.

## Generated files and runner contract

| File | Contents |
| --- | --- |
| `inputs.jsonl` | Exactly 192 actual text-bearing, label/provenance-free execution records. |
| `selection.json` | 48 selected IDs, family/producer/source groups, root/policy/domain/mechanism, rank/fallback, each TRAIN shard SHA, all source hashes and exact algorithm. No targets, label basis, teacher details or decision text. |
| `config.json` | P3 config copied verbatim as JSON values except total runtime reduced from 1,200 to 300 seconds. |
| `packet.json` | Input path/SHA/rows; case count/conditions; selection/config SHA; preparer path/SHA; TRAIN and allocation hashes; manifest-only exclusions; P3 pins; rendering/resource/runner requirements. |

Each execution record has **exactly**:

```text
{id, case_id, condition, order_reversed, letters_reversed,
 state, question, options: [{id, text, letter, original_position}]}
```

`case_id` is the original external TRAIN ID. Presentation `id = case_id + '::' + condition`. There is no `schema_version` field in a record. `original_position` is the **zero-based** index in the released option array. Options are stored in displayed order. For displayed index `j` and K choices, letter is ASCII `A + (K-1-j if letters_reversed else j)`.

| Condition | Displayed option order | Displayed letters |
| --- | --- | --- |
| O0L0 | Original | First K ASCII letters ascending |
| O0L1 | Original | First K ASCII letters descending |
| O1L0 | Reversed | First K ASCII letters ascending |
| O1L1 | Reversed | First K ASCII letters descending |

**Stock `qwen_challenger` is not a compatible runner for this packet:** its reader requires three development suites and its renderer regenerates ascending letters. Its config checker also fixes the old 1,200-second bound. Runtime needs a narrow, separately recorded adapter, not a change to frozen P3/M6/P4/E6 artifacts.

Runtime must render each supplied option as `letter + '. ' + text`, joined by LF, and fill the unchanged USER template with state/question/options. Only state/question/option text/supplied letters enter the model prompt: **never IDs, original positions, conditions, targets or selection/provenance metadata**. Apply the official pinned chat template with SYSTEM+USER, `tokenize=False, add_generation_prompt=True`; encode with `add_special_tokens=False`, no truncation. Score the next-token IDs for each **supplied** letter in displayed-option order, T=1 softmax over those K scores, then map probabilities back via option IDs. Descending letters must not be silently regenerated or sorted.

Runtime must first verify packet/file hashes, full prompt length <=1,024, exclusion of template special-token strings in input text, distinct answer tokens and identical-prefix-plus-one-token answer boundaries. Preparation does not claim tokenization validity. Fail closed; no dropping/replacing over-cap cases, truncation, fallback, prompt tuning or extra arm. Prediction output may use the existing `0.1` ID/option-ID probability contract, with every presentation and option covered exactly once; keep runner/token audit/results in a separate new directory.

## Frozen P3 and execution bounds

- Model `Qwen/Qwen2.5-0.5B-Instruct`, revision `7ae557604adf67be50417f59c2c2f167def9a775`; unchanged frozen pretrained P3 weights, **not** M6's trained checkpoint.
- SYSTEM/USER copied from the pinned config, byte-identical strings. Official chat-template SHA-256 `cd8e9439f0570856fd70470bf8889ebd8b5d1107207f67a5efb46e342330527f` (public `manifests/releases/p3-qwen-20261111-01.json`). Frozen P3 code revision `49823af30d6b394a147c7b8a9f5c676526a439f3`, source SHA `325d3a6b8e5577bba3b885fe8b61d5551305b456e2586d3949b2c45c649438d5`. The packet separately records today's runtime source hash; it does not misrepresent it as the original P3 source.
- Cap 1,024; FP32/MPS; batch 1; threads 4; SDPA; `use_cache=False`; `logits_to_keep=1`; T=1. No generation, training, fallback or downloads.
- **300 seconds total process time**, including audit/tokenization/load/inference, not 300 seconds per condition. Peak CPU RSS <=8 GiB and MPS driver allocation <=8 GiB independently. These unified-memory measurements overlap and are **nonadditive**, not a 16 GiB budget.
- `startup_rows=3` is retained from P3, but the first three actual records must supply retained predictions and count toward the 192 total forwards. Do **not** copy the stock runner's discarded warmup/repeated forwards. No extra startup presentations, retries, continuation run or background job.
- Model grants the slot; Runtime executes once at lower priority than ready M6/P4 work and records exact adapted source, config, offline model/tokenizer asset identity, environment, coverage, failures, elapsed time and measured resources. Research performs preparation only. The packet is frozen before outcomes and must remain unchanged.

## Interpretation

This is an inference-only TRAIN diagnostic, not a held-out score, learning experiment, calibrated-confidence claim or model promotion. O0L0 versus O1L1 retains each option's letter while moving its displayed position; O0L0 versus O0L1 retains position while changing letters. All four allow paired content-ID/letter/position stability summaries without targets. They can distinguish some assignment/order associations, not uniquely identify internal causal mechanisms: content-position/letter interactions, prompt formatting and shared source structure remain. Do not use this packet to modify or reinterpret the frozen M6/P4/E6 experiment.
