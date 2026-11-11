# R5 owner-read Jev source receipts

Read2026-11-11, approximately14:57–15:04UTC. This file indexes relevant retrieved passages, not a claim of reading every reference/table or independently reproducing the papers. No API calls, code execution, repository clone, model/data download, or paid work.

## J1 official material

- https://typesafe.ai/blog/introducing-system-one-models-and-jev — sections introduction, Evidence/Technical Results, workflow-evaluation nuance, Hallucination and Type-safety. Vendor describes RLCD; no reproducible objective/optimizer/data details disclosed in inspected material. Quote: “our number is not empirical. Schema matching is guaranteed”. Type safety is not factual correctness.
- https://docs.typesafe.ai/introduction/machine-learning-primer — RLCD and calibrated decisions: “trains Jev to return decisions and calibrated probabilities instead of generated text.” Does not specify executable training recipe.
- https://docs.typesafe.ai/models — Customizing Jev: “Jev is not fine-tuned or LoRA-adapted with customer data.” Same hosted weights serve customers; version aliases can change. No inference was requested.
- https://huggingface.co/blog/decision — decision interface and toy training section. Quote: “the model returns one logit per option, so a choice question is trained with a plain cross-entropy loss over the options.” Explanatory code example, not benchmark evidence or permission to upgrade dependencies.

## J2 Li & Wagle

https://arxiv.org/html/2610.02076v2
Tool fetch responseId mwc8yk12golj03, URL0. Relevant stored-content reads22000–52000 plus targeted method/scale/compute queries; abstract/intro also fetched. No PDF processing by owner.

- §3.3: “We mitigate this during fine-tuning by randomly shuffling candidate order across training instances”.
- §3.4: full-parameter or LoRA; tree-factorized choice loss with KL anchors for legal mass, outside tokens and other positions. Single epoch, AdamW, FSDP.
- §3.5: “subsequent data iterations were motivated by error analysis on public JevBench samples”; evaluations named there are exploratory. Exclusion of exact overlap does not erase adaptive exposure.
- §4.1/Table1: examples3000(4B-only),95461,9000,21000,30000,12000; Reason+Long375steps. These budgets are not Jeff's1500.
- §4.3.2: “JevBench accuracy drops from 81.4% (zero-shot) to 77.5% at 100 steps and 74.9% after a full epoch, even as in-distribution validation loss continues to decrease monotonically.” Narrow intent supervision negative transfer in4B, not Jeff observation.
- §4.3.4:0.6B adaptation benefits are reported;4B full-tuning has no net broad gain, LoRA improves that benchmark. Neither proves an older0.5B model benefits on our data.
- AppendixB: “Training runs use four A100 80GB GPUs” (except3GPU Intent100); Reason9k takes11min for0.6B. Not local-MPS time estimate.
- §4.4: generation instability without anchors despite scores; early collapse run also had constantLR/no warmup/batch3, explicitly confounded. Our decision-only proposal makes no generation-preservation claim.

## J3 Releasing the Inner Jev

https://arxiv.org/html/2610.17205
Tool fetch responseId mwc8tewlept27j, URL0. Relevant stored-content reads19000–40000, abstract and targeted method/ablation/provenance queries. Model naming “Jeff” here is unrelated to this project.

- §4: train pool417825, ~76000 presented/400steps; rank32LoRA+affine readout correction, hard/soft choiceCE, shuffledoptions,4B–31B.31B78min/fourH200;4B23min same setup. Huge relevance gap.
- §4Calibration: “We therefore restrict temperatures to be at least one” after observing detrimental sharpening on OpenDecisions. The set was used for recipe choice.
- §5Setup: “Since we selected our training recipe using OpenDecisions, we also evaluate on seven held-out decision datasets”. Competitors choose better original/recalibrated OpenDecisions scores.
- §5.2: same4Brecipe63.0vs63.6frozen; threechanges needed for gain.12Bgainwithinnoise.31Bheadline not portable.
- §5.4/Table5: frozen79.6; headonly78.9; LoRA/frozenoriginalhead84.9; joint84.4; hardlabels84.1. Mainrecipe3seedmean, mostvariants1seed. No clear head-only/soft-target necessity established.
- §5.3JevBench: binary probability push to0.801/0.199 to escape leaderboard abstention interval disclosed. Do not copy as calibration.
- Training soft targets include teacher outputs; genuine option-logit extraction was not established in inspected passages. This source is not used to equate generated probabilities with Hinton-style KD.

## Coverage caveats

These are public preprints/vendor documents, not independently replicated findings; paper authors' causal rhetoric is not adopted wholesale. Primary memo relies first on local E4/E5 aggregates. Generic arXiv/HTML URLs can change;v2 is explicit forJ2, accessdate recorded forothers. We preserve exact section/quote anchors rather than invent source hashes. Search snippets/irrelevant guessed pages are not evidence. No claim of exhaustive2026coverage.
