# Independent E4 / D3 result delivery review

**Disposition: no delivery blockers found.** Actual project-Python 3.12 comparison and rendering completed against the same 96 reference rows and the same six original, unfiltered prediction files. Independent standard-library arithmetic agrees with the shared results, including every policy/mechanism summary, own-start pair and equal-unit macro. `audit.json` records 1,358 successful bounded checks, exact executed CLI argument lists, exit codes/stdout/stderr, reviewed report/config hashes, source pins and output hashes. `independent-metrics.json` contains independently computed per-case quality and transitions.

## Reproduction and interpreter history

The original `e4-d3-comparison-v1/receipt.json` honestly records `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`. This review does not retrospectively relabel that execution. Both new comparison invocations and both new renderer invocations used exactly `/Users/destiner/Code/jeff/.worktrees/evaluation/.venv/bin/python -B` with the worktree's `src` as PYTHONPATH and bytecode writing disabled. This is real saved-prediction model evaluation, not fixtures or software tests.

The first comparison succeeded and produced `comparison.json`; first render succeeded and produced `shared-report.md`. The review's initial expectation of literal Markdown byte equality was too strict: the renderer correctly embeds the new comparison path in its last line. The orchestration stopped at that assertion, not at scoring. Those outputs remain preserved. A second actual comparison/render execution wrote separate `comparison-reproduced.json` / `shared-report-reproduced.md` outputs and completed the full audit. Comparison JSON is identical to the original, SHA-256 `652d21c03342bc835260f1ed28b161b5fc4f2b59ddce0a8efd4abf6e613dcb5f`. Render content matches exactly after replacing only its required new-path footer. No metric discrepancy exists. The tracked report's statement that an independent Python-3.12 reproduction exists is now backed by actual execution, not a promise.

## Numeric conclusions

| Predictor | Correct / 96 | Natural log loss | Summed Brier |
|---|---:|---:|---:|
| MiniLM start | 27 | 1.316860 | 0.729717 |
| MiniLM trained | 31 | 1.342824 | 0.743115 |
| MARCO start | 30 | 1.347340 | 0.748730 |
| MARCO trained | 26 | 1.355202 | 0.752642 |
| Uniform | 27 | 1.317371 | 0.730035 |
| Lexical | 24 | 1.319115 | 0.730912 |

All six have exactly 96 unique, identifiable, valid predictions, zero missing/invalid/duplicate/extra records and zero diagnostics. Arithmetic normalizes only permitted sum roundoff; no clipping. Reference-order tie-breaking reproduces uniform's 27 agreements. Independent five-bin ECE and all policy/mechanism ECE macros agree. These are descriptive reliability metrics, not calibration claims.

Explicit `units.json` maps 96 cases into all 48 two-case policies and eight mechanisms, each containing six policies / 12 cases. No ID-string inference. All equal-policy macros divide by 48; mechanism macros divide by eight. Every unit is finite/defined, including zero-agreement policies; none is silently discarded. Macro ECE averages unit ECE rather than pooled ECE.

MiniLM case transitions: 19 wins, 15 losses, 12 both correct, 50 both wrong. Complete policies: **3→4**, four gained, three lost, zero retained correct, 41 not fully correct on either side. MARCO: 15 wins, 19 losses, 11 both correct, 51 both wrong; complete policies **3→5**, five gained, three lost, zero retained correct, 40 not fully correct on either side. All 96 cases common-valid and 48 policies fully observed. Policy `both_wrong` means failure to achieve 2/2 on both sides: it does **not** mean both cases wrong (0/2). This naming is potentially easy to misread, but the tracked prose correctly disambiguates it; not a blocker.

| Mechanism | MiniLM start→trained | MARCO start→trained |
|---|---:|---:|
| Packs | 3→6 | 5→4 |
| Rates | 3→3 | 6→3 |
| Coordinates | 3→3 | 2→3 |
| Cooldown | 3→1 | 2→1 |
| Lexicographic | 5→5 | 5→2 |
| FIFO | 4→6 | 2→7 |
| Discount | 3→5 | 6→5 |
| Rounding | 3→2 | 2→1 |

All mechanism narrative conclusions match the raw outcomes: FIFO improves both, MARCO's five FIFO wins have zero regressions; MiniLM packs has six wins and three regressions. Cooldown deteriorates for both with loss 1.386081→1.597780 and 1.416606→1.608404. MARCO rates and lexicographic each lose three net agreements. MARCO rounding loss improves 1.695480→1.503249 despite fewer agreements.

## Provenance and bounded claims

Frozen reference/input/units hashes, publication/source pins and exact five-field export were rechecked. Boundary time precedes published preflight and every job start. All four individual receipts match aggregate jobs, exact original input/output paths and hashes, recorded command input/output/checkpoint arguments and expected checkpoint directories. Successful fresh-process/unchanged-checkpoint declarations and wall times are receipt evidence, not an independently witnessed inference trace. Published token audits bind 361 pairs, maximum 129 tokens, cap 256, zero overflow and the inventoried tokenizer hashes. Saved checkpoint metadata confirms cap 256; all 30 inventoried file sizes and before/after inventory record bytes match.

No model or tokenizer was loaded or executed; this review did not read tokenizer asset bytes or giant tensor bytes. **Current giant weights / loaded tensors are not independently attested.** Token counts were not recomputed. The earlier scorer's broader non-tensor hashing claim remains its published evidence, not a new claim that this review hashed tokenizer assets.

The labels are programmatic `rule_verified` agreement targets, not independently established semantic truth. Same `openai/gpt-sol` author/reviewer alias with unknown immutable revision is correlated evidence: 31/32 initial review and 64/64 repaired-content review across only 40 policies do not independently verify 96 cases / 48 policies. Same-author separate-algorithm consistency is not independent rendered-text verification. Residual FIFO fewest-zero, rates slot-two, scheduling non-none and easy-boundary hints remain qualifications, not reasons to claim broad rule generalization. Shared policies and algorithms invalidate iid/significance interpretations.

Prior exclusion receipts report zero ID/group/exact/NFC+outerstrip hits/errors over declared development/training corpora. This is bounded identity/content-key exclusion, **not semantic novelty clearance**. The superseded sentiment-training exclusion supplement is separately bound by the owner receipt. No final-evaluation content was accessed.

The two starts differ materially: random MiniLM scalar head versus retained pretrained MARCO cross-encoder head. The comparison does not isolate architecture. MiniLM gains four agreements while both proper scores worsen; MARCO loses four agreements and worsens both proper scores. No threshold/default promotion is supported or performed.

## Scope and handoff

Only new files under `artifacts/evaluation/e4-d3-result-review-v1/` were written. No tracked edits, merge, mailbox, network, inference, training, dependency changes, software tests, lint or syntax tests. No subagents/workers were launched; no review jobs remain running. Additional/pending spend £0. Owner retains manifest/build/commit responsibility; this review does not claim a package build.
