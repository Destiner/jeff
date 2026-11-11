# Pilot v1 generalization and shortcut audit — LD002 / R2

## Bottom line

**The strongest demonstrated weakness is an answer-text shortcut, not demonstrated train/validation source leakage.** Choosing the longest intent option by character count, without reading state or question, matches **84/100 training and 18/20 validation targets**. All 18 validation matches are uniquely longest; word count also matches 18/20. This limits the interpretation of Model's reported 20/20 intent result, but does **not** prove its scorer actually uses length or explain its two successes beyond this heuristic.

The nominal **300 train / 60 validation rows represent 60 / 12 declared source clusters**. They are not 360 independently sourced situations. Rule validation covers only **two mechanisms**, with no held-out examples of the ten trained mechanisms. We found no shared group IDs, exact normalized full inputs, or high-overlap cross-split state pairs. Manual inspection did find repeated semantic operations and cross-family topics; those are transfer opportunities / template dependence, not evidence that the same event crossed splits.

Keep v1 immutable and preserve the matched 256-token model comparison. This audit changes the strength of claims that its gains support; it does not authorize a replacement dataset, architecture change, or another ML job. Exactly three prioritized future data improvements appear below.

## Scope, prior work and evidence levels

Started by reading Data's [pilot quality/provenance document](../data/pilot-v1.md) and [data README](../data/README.md), then LD002, the published manifest and provenance. Data already checked structure, group isolation, label lineage, lexical candidates and a 48-row spot review (24 teacher-labeled and 24 rule-labeled rows). Its programmatic rule verifier consumes retained structured facts and shares the generator's author; that is not independent parsing of published rule text. This audit does not rebrand those existing checks as new semantic verification.

- **Measured by Research:** standard-library CPU counts, fixed option-only selectors, train-count lookup diagnostics, complete pairwise lexical scans, source-group summaries, and sentiment style statistics on the six manifest-listed shards. Hashes were checked before reading rows into analysis.
- **Source/manual findings:** three disjoint read-only subagents inspected source grouping/topic overlap, answer-text construction, and rule coverage; lead inspected the relevant generators and representative pairs. No generator was executed and no labels were changed. Manual review is bounded, not exhaustive semantic deduplication.
- **Reported by Model:** M2's saved-model quality figures below, from its public handoff. Research did not load or run a model in R2.

Dataset: `data-pilot-v1`; manifest SHA256 `62e9cf7538d93d377f401a89b887a988280bf1e97abc08159d6366063e9c0180`. Only **sentiment-r2**, not the excluded original sentiment shards, is evaluated. No final-evaluation files were accessed.

## 1. Rows versus independent source evidence

| Family | Train rows / declared clusters | Validation rows / declared clusters | What is held out |
| --- | ---: | ---: | --- |
| Intent | 100 / 25 | 20 / 5 | Five domain clusters; familiar explicit-request operations recur |
| Sentiment | 100 / 25 | 20 / 5 | Five subject/domain clusters; same four classes and three answer-wording sets |
| Rule application | 100 / 10 | 20 / 2 | Entire graph-reachability and Condorcet mechanisms |
| **Total** | **300 / 60** | **60 / 12** | Mixed kinds of holdout, not 60 unrelated validation tasks |

Intent/sentiment clusters each contain four cases; rule clusters each contain ten. Source IDs do not cross splits. But a cluster ID is a grouping commitment, **not a proof of statistical independence**: families share an authoring model alias, stylistic scaffolds, topics and primitive operations. We do not estimate an effective independent sample size from these data.

Each validation rule mechanism contributes 10/60 of the aggregate score, versus 4/60 for each intent/sentiment domain cluster. The three families are equally weighted by rows, but the twelve clusters are not. An individual rule error changes its mechanism score by ten percentage points. Row-level confidence intervals treating all 60 examples as iid would overstate evidential breadth; resampling only two rule clusters also cannot establish broad mechanism reliability.

## 2. Near duplicates, templates and legitimate overlap

### Complete lexical scan: no detected cross-split copies

Research scanned all **64,620** row pairs, including **18,000** train–validation pairs. Normalization matches Data's NFKC/casefold word tokenization; similarity is set Jaccard over state word trigrams (question fallback only for an empty state).

| Measure | Within one group | Across groups, same split | Across splits |
| --- | ---: | ---: | ---: |
| Raw state trigram Jaccard >=0.65 | 163 | 0 | 0 |
| All-digit tokens replaced by `NUM`, Jaccard >=0.65 | 377 | 0 | 0 |

The raw result reproduces Data's existing 163-pair observation. Number masking is the additional template probe: **39 rows share seven exact number-masked state patterns**, all within single rule groups, with no cross-split or cross-group cluster. Masking intentionally removes task-relevant numerical facts; these are **shared templates, not 39 duplicate decisions**. Boundary/parameter variants can be useful training examples while remaining dependent.

No exact normalized state or full-input duplicate was found. The largest cross-split state-trigram Jaccard is only **0.076923**, unchanged by number masking. Low trigram similarity does not exclude semantic paraphrases, shared intent operations or implicit source reuse. This is lexical evidence, not a complete leakage certificate.

### Manual pairs: distinguish operation reuse from copied events

IDs below share prefix `data:pilot-v1:`; the manifest identifies their exact files.

| Examples | Finding | Interpretation |
| --- | --- | --- |
| Train `intent:g17:r01`, validation `intent:g26:r02` | Borrow a club telescope versus reserve a loan veil for an existing course; the maximum lexical-overlap pair | Same borrowing operation in different domains. Plausible transfer, not the same event/source. |
| Train `intent:g22:r03`, validation `intent:g26:r03` | Cannot collect a finished mug this week → hold until Friday; cannot collect a honey jar this week → hold until next open day | Strong semantic task-template reuse despite low trigram overlap. New domain does not mean a new intent operation. No distinctive shared event establishes source leakage. |
| Train `sentiment-r2:g24:r02`, validation `sentiment-r2:g29:r01` | Successful sleeve alteration versus clear hearing-loop sound; both explicitly say “I am delighted” | Repeated evaluative language, but different experiences. “Delighted” is valid sentiment evidence, not a forbidden label merely because it is easy. |
| Train `intent:g09`, validation `sentiment:g26` | Pet boarding across families | Shared domain, distinct booking/care requests versus reviews. Data already disclosed this; inspected content did not show copied events. |
| Train `intent:g17` / rule `g04`, validation `sentiment:g27` | Astronomy club / observatory rota versus observatory reviews | Topic exposure crosses family/split boundaries. Rota arithmetic does not reveal the sentiment label. |
| Train rule `g05`, validation `intent:g28` / `sentiment:g30` | Seed scoring versus seed-library operations / seed-swap reviews | Shared topic and some labeling/exchange vocabulary, not a shared source scenario. Validation families also overlap one another. |

**Verdict:** no actual cross-split source leakage was demonstrated. There is real template, task-operation and domain overlap, so “new source groups” is supportable while “entirely unseen domains, operations and language” is not. Intent's four question strings all recur across splits; this is a shared task instruction, not an answer leak. Sentiment uses subject-specific questions, so low exact question reuse is not evidence of new linguistic constructions.

## 3. Answer-position and option-text shortcuts

### A per-example shortcut available to the active scorer

All selectors below were executed without state or question. Ties select the first supplied option. These are **exploratory data diagnostics**, selected while inspecting this validation set, not an independently held-out contest of baselines.

| Fixed selector | Intent train / validation | Sentiment train / validation | Rules train / validation |
| --- | ---: | ---: | ---: |
| Longest option, characters | **84/100 / 18/20** | 25/100 / 6/20 | 25/100 / 7/20 |
| Longest option, words | 76/100 / **18/20** | 33/100 / 5/20 | 26/100 / 6/20 |
| Shortest option, characters | **0/100 / 0/20** | 24/100 / 5/20 | 25/100 / 2/20 |
| First option | 27/100 / 6/20 | 25/100 / 5/20 | 29/100 / 6/20 |

Intent's uniformly random-choice expected agreement is about 25.8% because choices vary from three to five. The character-length shortcut scores 90%, spread across **all five validation groups** (4/4, 3/4, 4/4, 3/4, 4/4); it is not driven by one duplicated group. Correct intent descriptions are often more detailed/context-specific than generic distractors:

- `intent:g26:r02`: “Reserve a protective veil to borrow for the existing course booking.” versus “Book a second place on Saturday's course.” and “Buy a new hive.”
- `intent:g28:r02`: contextual instructions for labeling returned seeds versus shorter book-renewal or disease-identification alternatives.

Character and word selectors agree on the 18 validation successes, and each correct answer is uniquely longest by characters. This is not a tie-breaking artifact. Across all families, the character selector matches **31/60** validation references without context; the mixed teacher/rule provenance and cluster limits still apply. It is not a calibrated probability model.

Exact option memorization is a different issue: **none** of the intent or rule validation target texts appears among its family's training options. Separately, the per-row records confirm that **all options in all 20 validation decisions of each of these two families are unseen across the entire training pool**. A descriptive train-count option-correctness lookup therefore falls back to equal unseen scores and obtains 6/20 in each family. Thus the observed length signal transfers to new answer strings; it is not exact-string answer reuse. The lookup uses `(correct appearances + 1)/(all appearances + 2)`, pooling all training families and using no validation labels. The position prior is also pooled across training families, conditioned on choice count. Their training scores include self-observations and must not be presented as held-out performance.

### Position balancing is not independent randomization

Absolute positions are approximately balanced within choice-count strata for intent/rules, and sentiment positions are exactly 25 each in training / five each in validation. Nevertheless, in **all 240 intent/rule rows**, target positions cycle deterministically `1, 2, …, K` within family/split/choice-count publication order. Generator source confirms this construction.

That is a label-encoding **publication-order artifact**, not cross-split source leakage. It is not directly available to ordinary single-example inference, and the active shared candidate scorer does not ingest IDs, row index or candidate-position features. It therefore does **not** demonstrate that this model can exploit the cycle. A stateful/file-order-aware evaluator or a future list-aware model is a different threat model.

Rule generation has a second ordering artifact: it removes the correct option from a canonical alternative list and reinserts it at the cycling position, leaving distractors in canonical relative order. For example, `rule_application:g12:r04` publishes `Jen, Kai, nobody, Lou`, with the winner moved past the normally final “nobody”; `g12:r05` puts Nia before Mae. This is label-conditioned choice-list structure. We did not claim a perfect exploitation heuristic; the current independent pair scorer does not jointly see the ordered list. Intent rotates distractors, so the specific unrotated-rule-list finding must not be generalized to it.

### Current sentiment correction works, while style is narrow

All **120 current sentiment rows** offer all four classes; all target positions are balanced. Three unordered option-text sets recur in both splits, and every validation target string is seen in training. This is legitimate reuse of a four-class taxonomy, not correct-only answer availability. The original question-style/candidate-availability leak documented by Data is excluded from the published manifest and must not be reported as an active v1 defect.

Residual state statistics are narrow:

| Sentiment class | Mean state words, train / validation | “but” occurrences, train / validation |
| --- | ---: | ---: |
| Positive | 18.64 / 20.0 | 0/25 / 0/5 |
| Negative | 19.92 / 22.6 | 7/25 / 1/5 |
| Neutral | 15.20 / 18.2 | 0/25 / 0/5 |
| Mixed | **26.92 / 27.6** | **20/25 / 5/5** |

Mixed attitudes often explicitly summarize both sides; neutral states resemble short factual receipts/schedules. These are style correlations, not proof of label leakage or evidence that explicit sentiment words are illegitimate. The negative validation example `sentiment-r2:g29:r02` also contains “but”, so the conjunction is not sufficient. No causal contribution of these features to the trained model was measured.

## 4. Rule coverage: varied cases, few mechanisms

Each group below contains exactly ten rows. Source inspection establishes meaningful case variation, but one authored template/specification per mechanism is not ten independent reasoning tasks.

| Split / group | Mechanism | Variation and important limit |
| --- | --- | --- |
| Train g01 | First-match routing | All six orders of three rules, defaults, simultaneous flags; seven of eight flag combinations |
| Train g02 | Marginal fees | Zero usage, exact band endpoints, crossing a boundary, varied integer rates; no rounding or minimum-fee complication |
| Train g03 | Greedy capacity | Skip-and-continue, zero capacity, exact fit; only 3–4 requests |
| Train g04 | Cyclic indexing | 3–5 slots, signed/zero shifts, multiple wraps |
| Train g05 | Weighted score classification | Negative scores, exact lower/upper thresholds; not a systematic boundary grid |
| Train g06 | Symmetric difference | Empty/equal/disjoint/overlapping sets; no repeated names within a list |
| Train g07 | Half-open interval overlap | Touching endpoints, containment, multiple conflicts; integer, same-day, positive-duration intervals |
| Train g08 | Longest-prefix routing | Different matching lengths, fallback and substring traps; nine of ten entry lists shortest-to-longest |
| Train g09 | Modular checksum | 2–4 digits, varied weights/moduli, zero/exact divisibility; narrow answer/distractor construction |
| Train g10 | State-machine execution | All explicit transitions and ignored events; one fixed three-state table, logs of 1–4 events |
| Validation g11 | Directed reachability | Mostly four nodes; six cases require beyond direct-neighbour lookup; cycles, branching, empty results, self-loop; maximum necessary shortest-path depth three |
| Validation g12 | Condorcet election | Weighted blocks, ties/cycles; eight three-candidate and two four-candidate elections; neither four-candidate case has a winner |

There are **zero validation rows for the ten trained mechanisms**. Poor held-out scores cannot separate failure to learn those mechanisms from failure to transfer; good held-out scores would not prove retention of trained mechanisms. Conversely, this is a genuinely different-mechanism holdout, not merely renamed thresholds. The primitive ideas of order, sets, counting and comparisons can legitimately transfer.

Choice construction further limits reasoning claims:

- Condorcet always offers every candidate plus “nobody”; there is **no correct-only availability leak**. “Nobody” is correct 5/10, including both four-candidate cases. Longest-option selection obtains those same 5/10. All five winner cases also have a first-place vote leader that includes the Condorcet winner; a unique-plurality/no-Condorcet case (`g12:r09`) supplies one useful counterexample, not broad resistance to plurality heuristics.
- “No other junctions” is always offered in reachability, correct 2/10; longest-character selection obtains 2/10 there. Entity names must legitimately occur in state and candidate text. Correctly copying names is not the same as resolving transitive reachability.
- Training set reconciliation offers the explicitly impossible `reserve` badge in seven rows; `g06:r08` offers only “no badges” versus “reserve”. Checksum `g09:r10` puts correct 6 against 0, 1 and 2. These are weak distractor/construction cues, not evidence that validation leaked into training.

Rule verification is stronger than unchecked teacher labeling, but Data's 120/120 recomputation agreement is on retained facts using another implementation by the same author. Rendering/specification errors could survive. R2 inspected source and representative published cases; it did not independently certify all 120 labels.

## 5. What apparent pilot gains establish

Model's completed M2 handoff reports the matching **256-token** baseline → trained comparison: aggregate **20/60 → 35/60**, intent **6/20 → 20/20**, sentiment **6/20 → 11/20**, rules **8/20 → 4/20**. It also reports zero input loss at 256 and unchanged source/data/seed/budget, with MPS non-bitwise determinism acknowledged. These are **Model-reported**, not R2 model executions.

Defensible claims:

- The trained checkpoint improves reference-label agreement and log loss on these fixed, group-held-out synthetic cases, relative to its matching weak random-head baseline; gains are not uniform across families.
- Intent/sentiment transfer across the declared held-out domain clusters under familiar answer/style patterns. Rules expose difficulty on two new mechanisms after the input-loss confound is removed.
- Training/save/reload and complete-input evaluation work. The artifacts support bounded, reproducible development comparisons.

Unsupported claims:

- Broad context-grounded intent understanding from 20/20 when answer length alone gets 18/20. Conversely, neither length bias nor 18 matching selections proves the model ignores context.
- Broad unseen-rule reasoning, or even competence on the ten trained mechanisms, from the current two-mechanism validation set.
- Truly topic-disjoint or independently authored evaluation; natural-language/domain robustness; arbitrary-choice generalization from sentiment's three fixed answer sets.
- Independently verified correctness for the 40 teacher-labeled validation rows, calibrated confidence, or independent final performance after repeated development on these same groups.

The old truncated 128-token score is not the right primary comparator for the new trained model. M2's correction did not improve rule accuracy; truncation cannot be the sole explanation of its weakness. This audit does not recommend reverting input correctness for a higher aggregate score.

## 6. At most three prioritized future data improvements

These are recommendations for a **new, versioned** follow-up only; no rows, labels, groups or reservations were changed here.

1. **Remove the demonstrated choice-construction shortcuts first.** Counterbalance correct-answer length and specificity across cases, with equally contextual, plausible intent distractors—not filler padding. Fully permute all choices using recorded randomness independent of the target and publication index, including rule distractors. Acceptance evidence: inspect state-free character/word selectors by group and choice count, plus position/order cues; do not tune to beat one known heuristic on these same 20 cases. Preserve v1 for comparison.
2. **Increase genuinely distinct source coverage and separate transfer axes.** Allocate new groups before authoring; record topic and semantic operation across families instead of treating family-local domain names as universal holdouts. For rules, add independently specified scenario groups within trained mechanisms **and** more wholly held-out mechanisms, reporting seen-mechanism/new-scenario and unseen-mechanism results separately. Do not split the existing ten-case groups to manufacture validation independence, and do not consume the reserved final family. More variants of the same 12 validation clusters are not a substitute.
3. **Add small, independently reviewed linguistic/semantic contrasts.** Vary phrasing and specificity while preserving labels; include matched contexts where a changed rule/threshold, negation, requested subject or explicit request legitimately changes the answer. Cover mixed-looking wording that remains negative, rather than banning useful words such as “but” or “delighted”. Check rendered rule text and answer uniqueness independently of retained generator facts; use a different reviewer process where feasible and retain honest teacher/verification provenance. Keep related contrasts in one preassigned source group.

## Reproduction, artifacts and scope

Committed script: `experiments/research/audit_pilot_shortcuts.py`; exact invocation and artifact history are in [R2 experiment notes](../../experiments/research/pilot-shortcut-audit.md). Canonical output directory:

`/Users/destiner/Code/jeff/artifacts/research/pilot-shortcut-audit-20261111T1105/`

- `audit.json`: source hashes, cluster/mechanism map, position/option/style summaries, full pair-scan counts and top cross-split pairs.
- `heuristic-rows.json`: per-row length evidence and diagnostic selections, without modifying any input row.

Source citations: the published manifest and six shards under `artifacts/data/data-pilot-v1/`; their three `group_assignments.json` files; `intent/generate.py:206–235` and `rule_application/generate.py:14–37, 181–273` (read, never executed); Data's quality/provenance docs; Model's `/Users/destiner/Code/jeff/artifacts/handoffs/model/20261111-m2-256-complete.md`. Numbered example IDs above are locators into those immutable shards, not claims about unseen final data.

Research synchronized safely to main `19479dd`, then `4019fa7` for LD004 self-integration; edits stay in `docs/research/` and `experiments/research/`. No new model loads, training/inference, dataset edits, root dependencies, production changes, final access, paid work, software tests or linting. All statistics are CPU-only data inspection; fixed/count-based heuristics are not fitted ML models. Additional spend £0 actual / £0 pending.
