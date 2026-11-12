# E16 append — M12 under the unchanged reversal mean

**The fixed mean improves M12's new-case agreement from121/113 to132/240, but does not rescue the stronger-head-LR treatment.** It remains below original P3's mean134 and ties M8's mean132; probes reach9/12 versus11 for either earlier mean. Native-to-mean gains coexist with losses, and probe Brier worsens despite better NLL. The [raw E15 result](e15-head-learning-rate.md) and [initial five-candidate E16 report](e16-reversal-mean.md) remain separate and unchanged.

## Fixed method and actual exposure

The initial E16 rule was adopted03:01UTC after earlier component outcomes/position tendencies were known, before its arithmetic. Its authorized M12 extension was applied once to actual completed P13/E15 outputs at04:49UTC. Each native/reversed vector is validated and normalized by the existing scorer, aligned by explicit example/option IDs, then averaged exactly `(p_native+p_reversed)/2`. Missing/mismatched pairs stop derivation; no dropping, imputation, temperature, alternate weight, log pooling or better-order selection.

All12probe pairs are existing exact reversals; they produce12native references, not24new derived observations. M12 adds **three new score calls /312native-reference vectors**, separately60inherited/240new/12probes, with zero old scoring, model/tokenizer loads or extra forwards. Across the initial five and this append there are18new score calls /1872derived vectors, not1872independent cases. Serving the rule still costs two forwards per request.

## Actual M12 results

| Population | Raw native / reversed agreement | Mean agreement | Mean NLL | Mean Brier | Native→mean gains / losses |
|---|---:|---:|---:|---:|---:|
| Inherited /60 |34 /36|36|.886571564|.468159931|5 /3|
| New /240 |121 /113|132|1.072924953|.564642226|27 /16|
| Probes /12pairs |10 /6|9|.488627589|.304523158|1 /2|

New-family mean agreement is76/80intent,32/80sentiment and24/80rules. Native→mean gains/losses are4/1intent,13/7sentiment and10/8rules. The inherited36comprises20intent,9sentiment and7rules of20each. High intent agreement does not erase weak sentiment/rule performance.

Probe intent stays4/4, yet NLL worsens.187544→.383495 and Brier.084578→.213448. Probe rules fall3/4→2/4, with NLL.559763→.669413 and Brier.337729→.440772. Overall native probe NLL improves.523827→.488628, but agreement falls10→9 and Brier worsens.299046→.304523. Exact gained/lost memberships and source units are retained, not inferred from the net count.

| Completed new-case mean context | Agreement /240 | NLL | Brier | Probe mean agreement /12 |
|---|---:|---:|---:|---:|
| P3 |134|1.171135|.587258|11|
| M8 |132|1.165015|.585362|11|
| M12 |132|1.072925|.564642|9|

These P3/M8 figures are reused completed summaries, not rescored or a newly computed matched mean-to-mean membership analysis. Equal132 does not establish identical successful cases. Original MS MARCO START raw new NLL1.058568 is below M12 mean1.072925, while M12 mean has better agreement/Brier; M7/M9/M10/M11 remain materially stronger broad new-quality contexts. No architecture-controlled comparison follows.

## Verification and limits

[Independent review](../../artifacts/evaluation/e15-quality-review-v1/findings.md) reconstructed all312means from raw normalized constituents by explicit option ID. Every derived vector matches exactly; outcomes and aggregate dimensions agree. This covers actual M12 raw and means; Research R13's earlier initial-four source/math review alone does not cover this append. No scoring CLI or model was rerun by the reviewer.

All measured M12 constituent and mean vectors are untied with positive probabilities. There are zero NLL/Brier convexity violations at1e-12 floating allowance, zero failures to retain both-unique-correct pairs, maximum Brier identity residual3.191891195797325e-16 and maximum mean-sum deviation1.1102230246251565e-16. The unchanged scorer may renormalize admitted roundoff; this is not a tolerance-based definition of a top tie.

NLL cannot exceed the mean constituent NLL; the summed-Brier reduction against the constituent mean is `||p−q||²/4`, independent of target. These facts do **not** guarantee improvement over the better order, uniform, argmax agreement or calibration. Distribution/maximal-set reversal invariance is constructed; deterministic first-input tie choices need not be invariant. K2 covers both permutations; larger K covers only the reversal orbit. Nonconstant probabilities and mean gains are not proof of semantic reasoning.

Teacher/source-label agreement, same-alias verification, unknown revisions, reused development and dependent source/order dimensions retain their qualifications. No composite, significance, independence, capacity or promotion claim. Checkpoint+mean is a separate exposed candidate and uses an optional confirmation slot if selected; no automatic admission, unselected derived confirmation scoring or extra underlying raw-quality report. E13 exploration extensions remain pending actual authorized paired outputs, with separate populations/exposure accounting and the unchanged06:30cohort lock.

[Append binding](../../configs/evaluation/e16-m12-append-v1.json) · [publication index](../../manifests/evaluation/e16-m12-append-report-v1.json). Initial five-candidate arithmetic remains immutable; this is a separately bound append. Additional actual/pending spend £0.
