# Overnight findings — 12 November 2026

## Bottom line

**Jeff learns, saves real checkpoints, and runs after an independent reload. It has not become a dependable general-purpose decision model.** Familiar intent/sentiment gains are substantial, but stronger TRAIN fit does not reliably transfer to rules or new families. Option-position sensitivity and poor probability quality remain consequential.

The eight-hour shift added three learning controls, a frozen NLI baseline, a public-source exploration/confirmation exercise, and a genuinely executed offline CPU reference. It did not promote a default model or establish calibrated confidence.

## Learning controls

| Control | What changed | What the evidence says |
| --- | --- | --- |
| M10 | Replicated M7's low-learning-rate full Qwen fine-tuning with seed7 | TRAIN 777→1,214/1,500; new development 182/178 of240 native/reversed, versus M7's171/170. M10 recovers4/80 both-order rule successes versus M7's0/80, but severe rule/order failure persists; positions shift from first-slot to third-slot dominance. Probe agreement falls from M7's21/24 to19/24. Two seeds are not a variance estimate or automatic winner selection. |
| M11 | Fresh MS MARCO encoder, thirty total epochs instead of twelve | TRAIN 1,314→1,414/1,500 and rules314→414/500, but new development165→162/240 with NLL.699→.860. On96 D3 decisions, agreement26→29 yet NLL1.419→1.914, worse than all retained D3 comparators. |
| M12 | Frozen original Qwen backbone; only5,376 readout scalars trained, head LR100×M8 | TRAIN NLL1.358→1.136 but agreement805→786/1,500. New development121/113 of240 and both75, below the original decoder129/118 and both82. Better proper scores did not rescue choices or robustness. Head movement35.805× is not convergence or a capacity result. |

M11's mechanism analysis makes the fit/transfer distinction particularly clear: three mapped20-row TRAIN mechanism sets were fitted completely, yet their D3 agreement was only6/12,1/12 and3/12. Small-set fit is not mechanism mastery. These are different source groups and limited designs, not an isolated architecture diagnosis.

Reports: [E11 seed replication](evaluation/e11-seed-replication.md), [E12 encoder duration](evaluation/e12-encoder-duration30.md), [R14 mechanism alignment](research/m11-mechanism-fit-append.md), [E15 head learning rate](evaluation/e15-head-learning-rate.md). All unsuccessful runs and fixed endpoints remain available; no best-seed restart or post-update numerical rescue was used.

## New external confirmation

The new exercise contains200 exploration and200 separate confirmation cases:100COPA causal-choice and100WinoGrande coreference cases in each phase. Selection used the frozen input-only ranking/grouping/eligibility method, without label balancing or refill. SocialIQA yielded no selectable cases under its exact prerequisite filter; coverage was narrowed rather than reinterpreted. Public source labels, unknown pretraining exposure, and imperfect detected grouping limit the claims.

At the06:30 evidence cutoff, no external quality or mean result was available for optional selection. The cohort therefore stayed at the four mandatory raw predictors: original P3, M7seed42, original MS MARCO pretrained-ranking-head START, and M9. **Zero optional candidates or mean rules were admitted.** The cutoff record was actually published06:32:54, not backdated. Later exploratory results cannot reopen it. The original final24 remains sealed.

### Locked four-raw results

Each row below represents100 cases/100 detected source groups, evaluated in two dependent option orders. NLL is natural-log loss; Brier sums both option coordinates. Uniform probabilities have NLL0.693147 and Brier0.5. Full coverage; no top ties.

| Family | Predictor | Agreement native/reversed /100 | Correct in both /100 | Answer flips /100 | NLL native/reversed |
| --- | --- | ---: | ---: | ---: | ---: |
| COPA | Original P3 | 72/72 | 58 | 28 | .6017/.6113 |
| COPA | M7 | 62/64 | 30 | 66 | 1.0534/.8225 |
| COPA | MS MARCO START | 58/58 | 58 | 0 | .7431/.7431 |
| COPA | M9 | 50/50 | 50 | 0 | .8047/.8047 |
| WinoGrande | Original P3 | 48/49 | 5 | 87 | 1.6143/1.7188 |
| WinoGrande | M7 | 48/47 | 5 | 85 | .9570/.9770 |
| WinoGrande | MS MARCO START | 55/55 | 55 | 0 | .7080/.7080 |
| WinoGrande | M9 | 48/48 | 48 | 0 | .8005/.8005 |

The original, **not Jeff-trained**, Qwen baseline provides the clearest useful signal on COPA:72/100 in each order and both proper scores better than uniform. M7 training weakens that result and its robustness. M9 training also lowers agreement and worsens proper scores relative to its own pretrained encoder start in both families. No architecture attribution follows from comparing unrelated pretrained models.

All four raw predictors have worse WinoGrande NLL **and Brier** than uniform. Order-invariant encoder scoring is useful structural behavior, not evidence of correct reasoning. No pooled cross-family or cross-phase headline, significance claim, calibration claim, or general-purpose promotion is warranted.

**Independent numerical review passed with qualifications:**1,600 vectors/3,200 values and9,600 recomputed outcome fields matched, with no unexplained numerical discrepancy. This is not an all-checks-passed or producer-authentication claim: stale diagnostic headers and locator/assertion failures remain, and a post-lock reviewer inspection printed selected case content/IDs into its tool output contrary to the requested confinement. Original logs/artifacts remain unchanged; no evidence of changed selection, native rerun, or expanded consumer permission follows. See the [safe aggregate report](../artifacts/evaluation/e13-confirmation-public-v1/report.md) and its superseding [qualified numerical closure](../artifacts/evaluation/e13-confirmation-quality-v1/closure-report.md).

### Exploration is not confirmation

In Evaluation's [post-cutoff exploration analysis](../artifacts/evaluation/e13-firstfour-analysis-v1/report.md), the unchanged two-order probability mean improved exploratory COPA agreement to76/100 for P3 and81/100 for M7. However, WinoGrande mean agreement fell to48/100 and47/100; both mean proper scores remained worse than uniform. M7's higher COPA agreement did not beat P3's COPA mean proper scores. These are interesting exploratory trade-offs, **not confirmed selections**.

The fixed mean guarantees proper loss no worse than the *average constituent loss*, not either constituent, its better order, accuracy, calibration, or reasoning. It costs two forwards. Reversal invariance of the distribution and maximal set is constructed; selected-answer invariance additionally needs a unique maximum because first-input tie-breaking can break it. Beyond two options it covers only that reversal orbit. [E16](evaluation/e16-reversal-mean.md) records the rule and earlier development results, not these external measurements.

The [later exploration report](../artifacts/evaluation/e13-laterfour-analysis-v1/public-report.md) adds the remaining fixed raw candidates:

| Exploration only | COPA native/reversed /100 | WinoGrande native/reversed /100 |
| --- | ---: | ---: |
| M10 seed7 | 76/76 | 58/51 |
| M11 thirty epochs | 53/53 | 49/49 |
| M12 higher head LR | 57/44 | 50/55 |
| Original frozen NLI | 62/62 | 53/53 |

M10's mean reaches79/100 COPA with NLL.465957/Brier.284518, but53/100 WinoGrande with both proper scores worse than uniform. M12's COPA raw choices flip in99/100 cases; its mean reaches75/100 COPA but only48/100 WinoGrande. Every measured WinoGrande raw/mean rule remains worse than uniform on both proper scores in this exploration sample. Later-exploration independent arithmetic review is pending at this draft. None can enter the closed confirmation cohort, and no unselected confirmation mean was computed.

## Frozen NLI and the resource deviation

The single pinned native NLI classifier scored126/240 new development cases, identically in both orders, and7/12 probe pairs. That improves agreement over the original MS MARCO START's99/240, but worsens both NLL and Brier relative to that start. It is a practical baseline, not an architecture-controlled comparison or a new trained Jeff model.

**Historical P12 did not measure or enforce its required recommended-MPS-headroom guard.** It measured physical free+inactive memory instead. The stored predictions are retained with this disclosed execution deviation; physical completion does not establish full resource-contract compliance. The later external NLI pass actually used the prospective `recommended_max_memory() - driver_allocated_memory()` guard: Model verified308 post-Torch samples, all passing, with minimum recorded headroom17,978,408,960bytes. These are overlapping samples, not continuous physical peaks, and cannot retroactively repair P12. No old624 replay or retrospective headroom reconstruction occurred. See [E14](evaluation/e14-frozen-nli.md).

The R12 NLI adaptation proposal remains unexecuted. Its65–135 owner-minute preparation estimate risked displacing the unfinished external exercise; deferral is queue triage, not evidence that adaptation cannot work.

## Portable local reference

[Open the durable M9 reference](../artifacts/lead/night-20261112/local-reference/README.md). The unchanged255,928,739-byte archive contains checkpoint/tokenizer, Jeff wheel,25 pinned dependency wheels, notices, and three TRAIN examples. An existing compatible CPython3.12/macOS-arm64 installation is required; Python itself is not bundled. Wheel tags require macOS≥14, but the actual demonstration was on macOS26.7.1, not a macOS14 or other-host execution claim.

A fresh environment was installed offline outside the checkout. Actual CPU inference on the three fixed TRAIN cases retained identical complete maximal option sets, with maximum probability difference5.21540641784668e-7≤1e-5. File-backed Python-module origins and exact virtual Torch namespace definers were checked—not all native binary provenance or all-input portability.

The first smoke attempt loaded the model/tokenizer but made zero forwards before a synthetic-filename origin check failed. A specifically authorized narrow repair and one extra load succeeded. Both attempts remain: two loads, three total forwards,12s conservatively charged. The durable delivery was copied and checked once; it did not rerun inference. M9 is a portable reference, not a promoted best/general model. No public redistribution or blanket licensing clearance is implied.

## Execution, cost, and remaining decision

- All eight external exploration predictors completed:3,200 scored presentations,6,400 probabilities,12 existing startup forwards and2,012 physical model calls. Exploration whole-batch times44.02s+50.66s;98s conservatively charged to its1,200s ceiling.
- The separate four-raw confirmation completed1,600 scored presentations,3,200 probabilities,6 startup and1,006 physical calls:43.46s actual,45s charged to its separate900s ceiling. These counts are not independent samples or a serving-latency benchmark.
- Reported additional teacher/compute spend is **£0**; this is not a claim that existing agent access, attention, or engineering was free. No new external compute, root dependency/platform expansion, or repository/artifact publication to a remote service was undertaken; the reviewer tool-output confinement deviation is disclosed above.
- Environment, sandbox, metadata and supervision failures consumed substantial engineering/attention time. All are retained, including P9's wrong interpreter and five failed D8 tokenizer processes before the successful pass. The bottleneck was not demonstrated to be insufficient GPU compute.
- Lead and owners had real reading/writing/helper gaps. Lead specifically records approximately04:11–04:22 and06:55–07:12; Model records delayed handoffs and07:12–07:25; Evaluation records07:09–07:23 plus synchronous scoring. This was foreground coordination, not uninterrupted monitoring or a daemon. Owners completed confirmation autonomously during the later lead gap.
- The immutable five-report Fable snapshot has not changed. These overnight results are later evidence, not retroactive corrections to its cutoff. The original final24 and unreleased D7 drafts were not used.

## Recommended next controlled step — not authorized tonight

[R15's bounded decision memo](../artifacts/research/r15-20261112T073414Z/morning-decision-memo.md) recommends a **matched complete-versus-limited within-policy rate-coverage contrast**, rather than another duration/LR/seed setting. Both arms would use fresh original MS MARCO and the same M9 twelve-epoch recipe, adding36 examples each to the unchanged1,500 TRAIN rows:12policies×3cases, matched aggregate relations/labels/arity/answer slots/style, but different within-policy coverage.

This requires separately authorized Data acceptance, confound/exclusion checks, fresh unreused new-policy evaluation frozen before either fit, owner estimates, and two new training grants. It does **not** release or assume readiness of D7's72 drafts, train on D3/E13, or reuse this confirmation for unselected treatments. Existing D7 qualifications include policy-local answer-slot/majority differences, unmatched numeric magnitudes/denominators/cross-product margins, and an authoring cap not entailed by the prose. Aggregate matching alone does not make those drafts a clean single-factor treatment; acceptance must address or explicitly qualify the remaining differences. Prioritize that coverage remedy only if its complete arm improves new-policy complete success and both proper scores in both orders; better TRAIN fit alone fails. Inadequate fit or crossed outcomes are inconclusive, not a sweep or capacity verdict. This narrow rates experiment cannot explain every external-family failure.

A deployment workload, error/latency costs and success criterion remain unspecified. Those product choices still need agreement before choosing a default or pursuing a representative calibration claim. More compute or a higher development leaderboard score is not a substitute.
