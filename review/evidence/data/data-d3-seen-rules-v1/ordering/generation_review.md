# Ordering shard: frozen authoring and audit review

## Scope and novelty

48 validation-only decisions; 24 policy groups; four mechanisms, six policies per mechanism, two cases per policy. Group assignments were written before any case content. Domain order and named training-group references come only from the frozen D3 config. No old data, evaluation, model, final, probe, training row, or historical manifest was inspected. No checkout, Git, mailbox, shared contract, or other owner's files were changed.

Mechanism overlap with the named v2 training mechanisms is **intentional**. Novelty is newly authored policy instances and source facts, not unseen operations: ranking directions/field meanings differ; FIFO stocks, units and demand boundaries differ; credit order and percentage sequences differ; rounding grids and measurement precision differ. This is not broad training expansion or an unseen-mechanism challenge. Policies share templates within mechanisms, and paired cases are dependent. No empirical textual novelty comparison against inaccessible old rows was performed.

## Actual procedure

1. Read the specified AGENTS.md, contract, and frozen config only for project inputs. Captured exposed teacher identity: provider `openai`, alias `gpt-sol`; immutable revision unavailable.
2. Wrote `group_assignments.json` first (24 groups, all validation).
3. Authored original structured facts in `author_sources.py`; materialized `source_cases.jsonl`.
4. `generator.py` used seed 731904. Label slots were balanced within each arity and randomly assigned to row IDs before rendering; distractors and displayed candidates/batches were shuffled separately. Ranking precedence and FIFO arrival numbers were never shuffled semantically. FIFO distractors are feasible quantities summing to demand, not impossible inventories. Rounding distractors vary the numerical rank of the correct answer without making it an extreme.
5. Ran generation, then `audit.py` on all 48 rendered outputs. Audit does not import the generator. Its pure `expected(case)` sees structured facts only, never saved labels. It uses pairwise dominance, cumulative-stock interval overlap, rational affine composition, and rational distance comparisons, versus the generator's tuple sort, stock depletion, sequential Decimal arithmetic, and Decimal half-up quantization.
6. Audit checked exact rendered state/question correspondence with all source facts, all option uniqueness, answer presence, all selected labels, assignments, IDs, provenance, split, feasible FIFO options, ranking candidate coverage, rounding grids, currency formatting, and target balance. Only after success were labels changed from provisional to `rule_verified`.
7. Reviewed the rendered c01 case of every policy semantically (below), including rule wording, units, answer, and competing options. Parent separately owns rendered-text review and tokenizer audit.

The initial dataset audit had zero failures. Before the final rerun, rounding distractor selection was diversified to avoid a constant numerical answer rank; this was a design refinement, not a discovered incorrect label. Final generation/audit: **584 checks, zero failures**, 48/48 answer agreement. Four-choice slots each have nine targets; three-choice slots each have four. Of 12 ranking cases, four happen to select the first displayed candidate, eight do not. Correct option character length: 42 tied, two uniquely shortest, four uniquely longest; no universal length cue. Maximum state length is 61 whitespace-delimited words; this is **not** a tokenizer count or confirmation of the parent's 256-token budget.

## Same-agent semantic self-review (24 policies)

All entries below concern c01; both cases in each group also received the full mechanical audit.

| Mechanism/policy | Human-readable check of rendered semantics |
|---|---|
| lexicographic/p01 | Cove: survival 92 ties, six hours beats eight, cost 49 beats Shoal's 54. Lagoon's cheap fast route cannot override survival. |
| lexicographic/p02 | Elm: damage 3 and consent age 80 tie Birch; 39 running minutes beats 44. Yew's older consent cannot override damage. |
| lexicographic/p03 | Gully: five offline days, 45-minute walk; asset 12 beats Ridge's 18. Spur's asset 3 cannot override its longer walk. |
| lexicographic/p04 | Ochre: day 12, 85% shelf use; request 28 beats Willow's 31. Reed's shelf use cannot override its later deadline. |
| lexicographic/p05 | Tern: zero passengers able to board unaided, 22-minute wait; berth 2 beats berth 4. Ibis's longer wait cannot override its unassisted count. |
| lexicographic/p06 | Hedge: 14 native species, 30-metre gap; grant 790 beats 800. Verge's zero gap cannot override species count. |
| fifo/p01 | Issue 23 tiles: exhaust Amber 12, then Chalk 11, Indigo 0. Alternate allocations meet demand but violate arrival precedence. |
| fifo/p02 | Withdraw 75 litres: North 30 plus East 45 exactly exhausts two batches; West remains unused. Alphabetical option order is not arrival order. |
| fifo/p03 | Issue 19 metres: Moss 8 and Rust 11; Ink 0. Explicit cutting permission supports a partial roll. |
| fifo/p04 | Issue 17 tins: Glow 6 plus Halo 10 plus Spark 1. All inspected stock is eligible; expiry is not an alternative priority. |
| fifo/p05 | Issue 18 blocks: Brass 9 and Steel 9; Iron 0. Equal block mass makes counts sufficient. |
| fifo/p06 | Dispatch 14 packs: Polar 5 and Frost 9; Snow 0. All are ready; return date does not compete with arrival order. |
| discount/p01 | (90−12)×0.80 = £62.40. A reversed-order £60.00 is a real competing error, not the label. |
| discount/p02 | 120×0.85−9 = £93.00. Reversing the voucher gives £94.35. |
| discount/p03 | (260−40)×0.75−5 = £160.00. The two distinct fixed credits bracket the percentage. |
| discount/p04 | (80×0.90−6)×0.80 = £52.80. Each percentage is applied to its own current subtotal. |
| discount/p05 | (115−15)×0.90×0.80 = £72.00. Sequential reductions are not a single 30% reduction. |
| discount/p06 | (96×0.75−8)×0.90 = £57.60. The credit belongs between percentages. |
| rounding/p01 | 2.35 g is halfway between 2.3 and 2.4; choose 2.4 g. |
| rounding/p02 | 42.5 kPa is halfway between 40 and 45; choose 45 kPa. Grid anchored at zero is explicit. |
| rounding/p03 | 1.205 ppt is halfway between 1.20 and 1.21; choose 1.21 ppt, not a floating-point approximation. |
| rounding/p04 | 125 kg ties 120 and 130; choose 130 kg. |
| rounding/p05 | 7.25 mm ties 7.0 and 7.5; choose 7.5 mm. |
| rounding/p06 | 19 cm ties 18 and 20; choose 20 cm. |

Paired FIFO cases include partial first batch, partial middle batch, exact two-batch exhaustion, and crossing into the third batch. Paired rounding cases compare explicit ties with near-boundary non-ties; several correctly retain the same answer, so paired flips were not forced. Discount pairs are distinct starting invoices under the same ordered credits, not independent policy evidence. Ranking pairs change ties and winners while preserving each policy's precedence.

## Limits, usage, and freeze

This is **same-agent separate-algorithm consistency**, not independent authorship, independent human verification, or evidence of external policy validity. The same author designed the policy, rendering, audit, and semantic review; common-mode mistakes remain possible. `rule_verified` means the explicit synthetic rule agrees with the implemented structured-fact calculation and text correspondence checks. It does not claim held-out model performance or calibrated probabilities.

Original synthetic material under existing provider terms; no private records, scraped sources, or invented redistribution licence. Permanently validation-only and never usable for weight updates, including derived variants. Development diagnostic, seen mechanism/new authored policy, paired dependence. No network/API calls, paid generation, extra model execution, tests, or lint. **Additional spend £0; pending spend £0.**

Reproduction (lightweight local Python only): `python3 author_sources.py`, `python3 generator.py`, `python3 audit.py`, `python3 finalize_metadata.py`, in this directory. Generator requires the actual `PI_PROVIDER` and `PI_MODEL` environment variables. Metadata hashes bind the final audited payload and authoring/audit code. No train file or dataset manifest is produced. Outputs are frozen after the final report; regeneration is not authorization to mutate a published version.
