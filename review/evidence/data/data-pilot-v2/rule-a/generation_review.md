# Generation review — rule-a r1

## Scope and production
- 200 new train rows in g001–g010; 40 new validation rows in g011–g015. Full namespace: `data:pilot-v2:rule-a:`.
- 100 train and 20 validation authored policy instances, each with two related cases; **15 mechanism groups**, not 240 independent groups or 120 independent mechanisms. Algorithmic templates remain shared within mechanisms.
- `group_assignments.json` was written before source content. Exact config mechanism ordering and frozen split ranges retained. No parent, old examples, other producer artifacts, or evaluation data inspected. Historical boundaries followed from config only; global deduplication remains the parent assembler's responsibility.
- Authored material is original synthetic text through existing approved OpenAI access (`gpt-sol`). No network/API calls, ML loads, tokenizers, paid services, tests, linting or Git operations. CPU Python only.

## Actual execution and reproducibility
From this directory: `python3 author_cases.py`, `python3 generate.py`, `PYTHONDONTWRITEBYTECODE=1 python3 finalize.py`.
Source: `author_cases.py` → `source_cases.jsonl`; rendering: `generate.py`; structured audit inputs: `audit_cases.jsonl`; separate semantics: `audit.py`; final provenance and reports: `finalize.py`.
Deterministic option seed 813502; name/list-order seed 174031. Revisions and SHA-256 are in metadata and the final validation report. No Git revision was queried. Sampling settings and immutable teacher revision are unavailable, not inferred.

## Label and text review
All 240 saved targets are compared against `expected(case)` before promotion to `rule_verified`. The audit does not import the generator, consult saved labels inside expected(), or infer facts from answer texts. Alternate implementations include per-unit FIFO allocation, affine conversion composition, middle order-statistic counting, dynamic-programming common substrings and two-pointer stable merge.
This is separate code by the **same agent**, not independent authorship or an independent teacher review. All 120 source policy specifications and their paired case definitions were self-reviewed for prose/fact fidelity; all 240 rendered states and structured audit facts are additionally joined exactly to those sources. That exact join is not natural-language semantic verification.

Mechanism review: authorization counts distinct eligible signers only; tuples state every priority direction; FIFO explicitly skips quarantine; conversions state both stages and input units; discounts specify order, eligibility and zero floor; accrual caps each day before total; rounding ties choose numerically larger even for negative inputs; RLE counts adjacent runs and includes singletons; EDF includes setup and permits equality; permission vetoes are permission-specific and override union grants. Validation uses explicitly stated substring tie breaks, bracket first-error precedence, stable queue ties, numbered-bit parity and even-sample median averaging.

## Diversity, shortcuts and remaining limitations
Candidate descriptions retain the same style within each decision. Candidate names and state listing order for tuple/median choices are randomly permuted without consulting labels. Answer choices are shuffled separately; target positions are balanced within each split/option-count (train 3-choice: 20/20/20; train 4-choice: 35/35/35/35; validation 3-choice: 3/3/2; validation 4-choice: 8/8/8/8).
The final report gives exact target text frequencies, source-candidate winner positions, and target length shortcuts. Semantic outcome frequencies are not uniform: authorization, scheduling feasibility, access allowance and parity passing have real class priors. Choice-length ties are common in arithmetic/encoding; longest-choice success is not universal. Numeric distractors include wrong stage/order, caps, floors and nearby alternatives; not all are equally hard.
States are compact (within the requested usual range on this shard). Whitespace pair length is only a proxy, not a token audit: the parent must check its actual 256-token formatting. No independent correctness, cross-shard lexical novelty, broad domain disjointness, redistribution license, tokenizer-cap pass, or separate-session teacher review is claimed. Original synthetic data remains subject to the existing provider terms; there are no private records.

## Handoff
`train.jsonl`, `validation.jsonl`, `metadata.json`, `validation_report.json`, source/assignment files and the scripts are the frozen r1 bundle. No manifest or shared checkout was edited. Additional and pending spend are both GBP 0. No process remains running after finalization.
