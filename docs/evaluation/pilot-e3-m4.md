# E3: frozen Data-v2 and independent M4 comparison

## Conclusion

**Both M4 candidates improve on newly authored v2 validation versus their own
fresh starts. Neither passes the pre-result robustness gate versus its v1-trained
predecessor.** Preserve all candidates; no default is promoted.

MS MARCO gets more new labels right than MiniLM, but its log loss and Brier are
worse. Inherited/probe regressions survive the larger dataset. These are measured
trade-offs, not failed inference: every predictor has full valid coverage.

Protocol: [e3-plan.md](e3-plan.md). Recipe: `configs/evaluation/e3-m4-v1.json`.
Pinned index: `manifests/evaluation/e3-m4-report-v1.json`. Artifact paths below
are relative to `/Users/destiner/Code/jeff/artifacts/`.

## Frozen boundary, provenance and coverage

Data008 published `data/data-pilot-v2/manifest.json`, SHA-256
`d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`.
It is byte-identical to the revised r3 candidate, not superseded r2. The release
has 1,500 train / 300 validation rows. Every inherited row is unchanged; new
rows are bound to published metadata, group assignments and revision lineage.

| Validation stratum | Rows | Declared groups | Label basis | Relevant source units |
| --- | ---: | ---: | --- | --- |
| Inherited-v1 | 60 | 12 | 40 teacher / 20 rule_verified | 5 intent, 5 sentiment, 2 rule groups |
| Newly authored v2 | 240 | 170 | 160 teacher / 80 rule_verified | Intent/sentiment: 80 singleton groups each, 8 domains and 2 producers per family; rules: 40 policies in 10 mechanism groups |
| Existing probes, separate | 24 | 12 | 24 teacher, unknown curator model | 12 original/reversed pairs, 4 groups per family |
| Combined v2, overlapping summary | 300 | 182 | 200 teacher / 100 rule_verified | Inherited plus new; not extra independent evidence |

Teacher aliases are `gpt-sol` / `openai/gpt-sol`; immutable revisions are
unavailable. Metadata resolves aliases but does not independently authenticate
an upstream model. Revision-author identity is not automatically the label
teacher. Rules use executable `rule_verified` basis, including teacher-kind
rule-a; same-author specifications/checks are not independent natural-language
ground truth. Same-alias hidden-target review is not independent verification.
Use **label_basis**, not provenance kind. Aggregate metrics are supplied-label
agreement, not uniformly verified correctness.

Fresh CPU review checked 123 expected hashes, all 1,440 newly authored train/
validation rows against source metadata/assignments, and 720 revised-parent
joins. All six parent shards are exact. There were zero hits in 168 released-train
versus historical validation/probe checks: IDs/groups, ordered and order-free
content, state, NFC and outer-strip variants. This is bounded exact exclusion,
**not semantic-derivative clearance or proof of historical non-exposure**.
An overly strict redundant-output-hash check on sentiment-b-r2 was resolved by
independently reconstructing both complete released byte streams from its pinned
parent/revision; initial diagnostics remain. Zero unresolved identity errors.

References/inputs: `evaluation/e3-v2-{assembly,freeze,order,new-order}-v1/`.
Each inference input contains only schema/id/state/question/option id+text.
Model's 16 jobs were rehashed and bound to those exact ordered inputs. Existing
M2/M3 inherited/probe predictions were reused only after full reference and
ordered-input identity checks; no duplicate inference. The 32 predictor/stratum
reports have **300/300, 60/60, 240/240 or 24/24 valid predictions**, respectively,
with no missing, invalid, duplicate, extra or unidentifiable records. Paired
common-valid denominators therefore equal full denominators in this study.

## Main results

Cells are **correct labels / denominator; natural-log loss**. Lower loss is
better. Uniform uses first-option tie-breaking, not random sampled choices.

| Predictor | New-v2 | Inherited-v1 | Existing probes |
| --- | --- | --- | --- |
| Uniform | 65/240; 1.333463 | 17/60; 1.378765 | 8/24; 1.055008 |
| Lexical | 99/240; 1.296868 | 29/60; 1.323710 | 9/24; 1.047044 |
| M4 MiniLM fresh random-head start | 66/240; 1.332467 | 20/60; 1.378267 | 2/24; 1.057107 |
| M4 MiniLM trained | **132/240; 0.823115** | 34/60; 0.907554 | 12/24; 1.025456 |
| M4 MS MARCO fresh pretrained start | 99/240; 1.058568 | 30/60; 1.026878 | 14/24; 1.453783 |
| M4 MS MARCO trained | **141/240; 0.917258** | 42/60; 0.712621 | 10/24; **1.876464** |
| M2 retained v1-trained MiniLM | 107/240; 1.136427 | 35/60; 0.855288 | **16/24; 0.710407** |
| M3 retained v1-trained MS MARCO | 110/240; 1.024844 | 40/60; 0.793701 | 8/24; 1.360701 |

M4 MiniLM's new agreement is 55%; MS MARCO's is 58.75%. Against respective
historical models, paired new-row wins/losses are 43/18 and 43/12. These are not
independent Bernoulli trials. Combined-v2 M4 totals are 166/300 (loss 0.840003)
and 183/300 (0.876331), but these overlap the two primary strata above.

The pre-result descriptive gate requires better new-v2 agreement **and** loss
than each own start, then no inherited/probe family agreement or loss regression
against its corresponding v1-trained predecessor for a robustness claim.
Both pass the first condition; **both fail the second**. This is not a statistical
significance test or a selection policy.

## Family results and consequential regressions

Each new family has 80 rows; inherited has 20; probes have 8 presentations / 4
groups. Cells are correct counts followed by loss. Full starting/baseline family
metrics are in each generated `report.md` and `comparison.json`.

| Stratum / family | M2 v1 | M4 MiniLM | M3 v1 | M4 MS MARCO |
| --- | --- | --- | --- | --- |
| New intent | 66; .505941 | 74; .184336 | 72; .318603 | 77; .091450 |
| New sentiment | 22; 1.567983 | 43; .941779 | 24; 1.350882 | 43; 1.249159 |
| New rules | 19; 1.335358 | **15; 1.343231** | 14; 1.405047 | 21; **1.411166** |
| Inherited intent | 20; .067838 | **17; .500164** | 19; .211817 | **18; .251990** |
| Inherited sentiment | 11; 1.066200 | 13; .845449 | 14; .806437 | 17; .569368 |
| Inherited rules | 4; 1.431825 | 4; 1.377048 | 7; 1.362848 | 7; 1.316504 |
| Probe intent | 6; .598436 | 6; **.765721** | 4; .919648 | **2; 1.412754** |
| Probe sentiment | 6; .620252 | **4; 1.001136** | 0; 1.078186 | 4; **1.579008** |
| Probe rules | 4; .912532 | **2; 1.309512** | 4; 2.084269 | 4; **2.637630** |

MiniLM regresses on new rules even versus its fresh random-head start (21→15/80,
loss 1.302037→1.343231). MS MARCO improves new-rule ranking but worsens its
loss versus both its start (1.358558) and M3. Both M4 new-rule scores remain below
deterministic uniform's 23/80; its expected random agreement is a separate metric.
No broad rule-reasoning claim is supported. Lexical gets 63/80 new intent labels
right, versus the trained models' 74 and 77: a useful simple baseline remains.

MiniLM's probes lose four presentations relative to M2 (paired 4 wins/8 losses,
equivalent to 2/4 paired groups). MS MARCO gains two presentations over M3
(6 wins/4 losses; 3/2 groups), while **every probe family log loss worsens**.
Compared with its own pretrained start, MS MARCO loses 14→10/24 and loss rises
1.453783→1.876464. More agreeing labels do not guarantee better probabilities.

## Source groups, domains and mechanisms

Every declared group is reported in `evaluation/e3-m4-v1/<stratum>/report.md`
and JSON. `evaluation/e3-m4-source-units-v1/summary.{md,json}` additionally gives
source-group/producer/domain/mechanism/policy-instance summaries and equal-unit
macros within families, including explicit missing metadata. Dimensions overlap;
macros are not independent estimates. Probes have no invented Data-domain map.

Selected material differences, not a replacement for the complete tables:

- Inherited MiniLM intent loss worsens in 4/5 domains/groups. Canal-boat hire
  (`data:pilot-v1:intent:g27`, four rows) falls 4→2, loss .163599→2.115364;
  makerspace-laser g29 falls 4→3, loss .006365→.248637. MS MARCO's inherited
  intent loss also worsens at canal-boat hire: 4→3, .194188→.501848.
- New MiniLM sentiment improves all eight domain losses, yet worsens 16/80
  singleton source-group losses. New MS MARCO sentiment worsens 2/8 domains
  and 25/80 source groups despite the family gain: community darkroom sessions
  improve 4→5/10 while loss worsens 1.374684→1.681164; folding picnic benches
  improve 1→4/10 while loss worsens 1.414660→1.578407.
- New MiniLM rule loss worsens in 6/10 groups; MS MARCO worsens in 3/10.
  Complete rule-group agreement/loss follows (each eight cases / four policies):

| New rule group (`data:pilot-v2:` prefix) | M2 | M4 MiniLM | M3 | M4 MS MARCO |
| --- | --- | --- | --- | --- |
| rule-a:g011 | 1; 1.4420 | 0; 1.5525 | 0; 1.5088 | 0; 1.4914 |
| rule-a:g012 | 1; 1.6332 | 1; 1.5571 | 1; 1.9932 | 1; 2.1230 |
| rule-a:g013 | 0; 1.3968 | 0; 1.3984 | 2; 1.3918 | 3; 1.3852 |
| rule-a:g014 | 2; 1.4090 | 1; 1.4265 | 1; 1.4985 | 1; 1.6010 |
| rule-a:g015 | 4; 1.0849 | 1; 1.1067 | 3; 1.0821 | 4; 1.0943 |
| rule-b:g011 | 3; 1.2342 | 3; 1.2276 | 3; 1.2566 | 4; 1.2414 |
| rule-b:g012 | 3; 1.2500 | 3; 1.2301 | 1; 1.2465 | 1; 1.2456 |
| rule-b:g013 | 1; 1.3932 | 1; 1.3963 | 1; 1.4189 | 5; 1.3795 |
| rule-b:g014 | 1; 1.3957 | 2; 1.3880 | 0; 1.4658 | 0; 1.4139 |
| rule-b:g015 | 3; 1.1146 | 3; 1.1492 | 2; 1.1883 | 2; 1.1364 |

New rules have ten held-out named mechanisms; **no seen-mechanism validation
stratum exists**. Shared logical primitives prevent claiming wholly unseen
computation. Group IDs, policy instances, domains and independent samples are
not interchangeable. Intent/sentiment each have only two new producers with the
same exposed teacher alias. Data's exploratory longest-character selector still
matches 32/80 new intent labels (producer-a 21/40), versus inherited 18/20. This
residual construction shortcut is not proof neural models used it. Revisions
were targeted authoring repairs, so fresh authorship is not untouched evidence.

On probes, MiniLM loses intent.01 (2→0; loss .350200→2.722793) and
rule_application.03 (2→0; .713718→1.596698). MS MARCO rule_application.01 stays
wrong in both presentations while loss worsens 7.142956→9.418985; rule_application.04
falls 2→0. Conversely, MS MARCO gains two sentiment groups. These are specific
reused development observations, not cases to copy into training.

## Probability quality, not calibration

Brier is the sum over options, not divided by option count. ECE uses five fixed
confidence bins and is descriptive; sparse/correlated groups and label uncertainty
preclude calibration claims. All losses here are finite, with no zero target
probabilities; undefined/infinite cases remain explicit in the tooling.

| Candidate | New Brier / ECE | Probe Brier / ECE |
| --- | --- | --- |
| M2 v1 trained | .606945 / .072067 | .441728 / .088320 |
| M4 MiniLM trained | .460115 / .045960 | **.628466 / .218652** |
| M3 v1 trained | .555299 / .052193 | .653598 / .442556 |
| M4 MS MARCO trained | .481392 / .023151 | **.770313 / .416654** |

MS MARCO's nine-label new-v2 advantage over MiniLM coexists with worse loss and
Brier; new sentiment ties at 43/80 but loss is 1.249159 versus .941779. On probes,
MS MARCO has 16 presentations in the .8–1 confidence bin: mean .955239,
agreement .625. They represent only eight correlated pairs. Its probe ECE is
numerically better than M3 while loss/Brier worsen: do not select on ECE alone.

## Option order

All eight predictors have complete pair coverage: 300 combined, 60 inherited,
240 new, 12 probes. These sets overlap; probes already had two presentations.
All six neural predictors keep the same choice on every pair, without ties;
maximum probability change across them is at most 1.9613e-8. This establishes
observed exact-reversal consistency only, not arbitrary permutations, renamed
IDs, general correctness or calibrated confidence.

Uniform changes choice on every reversal because all options tie, despite zero
probability change. Lexical has 135 tied combined pairs; 165/165 untied pairs
are consistent, with probabilities unchanged. Original/reversed uniform combined
agreement is 82/78, lexical 128/130. Tie-driven choice movement is not a model
probability-order failure. M4 MiniLM remains wrong on both sides of 134/300
combined pairs; MS MARCO on 117/300: consistency does not cure errors.

## Controls, reviews and reproducibility

Independent metadata/source review found matching seed42, cap256, decision
batch4, 3 epochs, 1,125 updates / 4,500 presentations, LR2e-5/5e-4, AdamW settings,
MPS/four threads, exact released split and clean recorded code812a655. Fresh
respective pretrained initialization was source/metadata-backed, not warm-started
from M2/M3. Both full-token audits record 6,848 pairs, max169, zero input loss
at256. Model's sequential training took 74.403/76.622 seconds. These recorded
training/reload facts are separate from Evaluation's package builds.

Sixteen invocation/completion receipts support fresh-process offline reload;
Evaluation rehashed inputs/outputs, not loaded weights. Receipts identify
checkpoint paths rather than authenticating historical loaded weight bytes.
Embedded checkpoint run.status snapshots still say `running`; completed standalone
run records and later successful inference receipts supersede that stale snapshot.
Matching budgets do not remove architecture/pretraining differences or MPS
nondeterminism. Compared with v1, dataset mixture **and** update count change:
this is not a pure data-only causal ablation. One seed gives no seed uncertainty.

Fresh reviewers found no blocking report-integrity issue: 819 hash declarations
across229 unique files matched; 3,456 inference-input row occurrences matched
stripped references; 48 raw bundles reconstructed byte-for-byte (11,088 retained
lines / 3,600 known out-of-stratum exclusions), and 40/40 study commands exited0.
The excluded rows are known other-stratum inputs, not silently dropped failures.
Independent control and source-unit review separately verified gate conclusions.

Actual study and supplemental commands, from the Evaluation worktree:

```sh
export JEFF_ARTIFACTS_DIR=/Users/destiner/Code/jeff/artifacts
export PYTHONPATH="$PWD/src"
.venv/bin/python -m jeff.evaluation.study \
  --config configs/evaluation/e3-m4-v1.json \
  --output-dir "$JEFF_ARTIFACTS_DIR/evaluation/<new-reproduction-id>"
.venv/bin/python \
  "$JEFF_ARTIFACTS_DIR/evaluation/e3-source-unit-analysis-v1/summarize.py" \
  --comparison inherited-v1="$JEFF_ARTIFACTS_DIR/evaluation/e3-m4-v1/inherited-v1/comparison.json" \
  --comparison new-v2="$JEFF_ARTIFACTS_DIR/evaluation/e3-m4-v1/new-v2/comparison.json" \
  --comparison probes="$JEFF_ARTIFACTS_DIR/evaluation/e3-m4-v1/probes/comparison.json" \
  --output-dir "$JEFF_ARTIFACTS_DIR/evaluation/<new-source-unit-id>"
```

Original execution used the byte-identical artifact recipe at
`evaluation/e3-v2-assembly-v1/m4-study.json`; `evaluation/e3-m4-v1/receipt.json`
contains every actual compare/order/render command and output hash. Supporting
scripts `bind_historical.py` and `build_recipe.py` are pinned in the index.
Artifacts are exclusive-create; reproduction uses a new namespace, never edits
frozen reports. Source-unit supplement reuses shared `metrics.summarize` on saved
outcomes, not a second scorer.

Final wheel/sdist build succeeded with `uv build --no-sources`. Installed the wheel
with `uv pip install --no-deps` into an isolated Python3.12 environment; from the
artifact directory with `PYTHONPATH` unset, reran the same pinned study into
`evaluation/e3-m4-wheel-v1/`. All32 scoring reports, paired comparisons and32
order summaries reproduced exactly numerically (only local prediction paths
change). Receipt: `evaluation/e3-final-packaging-v1/reproduction.json`. No ML
extras or models were loaded. This is actual evaluation/packaging evidence,
not a software test suite and not a rerun of Model inference.

Other key evidence: `evaluation/e3-release-identity-review-v1/`,
`evaluation/e3-final-integrity-review-v1/`, `evaluation/e3-control-audit-v1/`;
Model's `model/m4-v2-20261111-01/`; Data's released provenance/quality audit.
Review findings were sent directly to Model/Data/Research before final integration;
no relay or approval gate. Final data and reserved unseen-family content were not
opened, exported, scored or used for decisions. No software tests, linting,
competing model loads or separately billed services. £0 additional/pending spend.
