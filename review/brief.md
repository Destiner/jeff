# Mission and constraints

This is a reconstruction from the project's user-approved instructions and decisions, NOT a verbatim transcript or an independent description of Jev. Sources: ../AGENTS.md, ../docs/plan.md and ../docs/contracts.md. More specific measured evidence supersedes stale early planning assumptions.

## Intended product
A small pretrained text model receives context/state, a question, and caller-supplied answer choices, then returns probabilities over those choices. Choice sets and their text can vary; this is not merely one fixed class vocabulary. Initial scope is single-choice, including yes/no. Generated explanations and a polished application are not the primary deliverable.

The ambition is learning that transfers across more than one task family. Jev supplies interface/purpose inspiration only: no proprietary architecture or algorithm is available, and capability equivalence is not claimed.

A genuine trained, saved, reloadable checkpoint and held-out comparison were the day-one milestone. The higher goal is useful decision behavior, not just functioning infrastructure. The user values blunt assessment, meaningful baselines, negative results and consequential qualifications.

## Hard constraints for this review
- Python3.12/uv, pretrained weights rather than language pretraining from scratch.
- Local-first Apple silicon; current machine measured24GiB unified memory (earlier plan says unconfirmed16–24GB). Larger/remote resources may be proposed with explicit cost and authorization requirements, not assumed.
- Combined additional teacher/compute budget ceiling £50. Reported extra paid allocations/actual/pending spend through cutoff: £0. Existing agent/token access is available; zero spend is not itself an objective.
- Deadline2026-11-12 23:59 Europe/London. Coding window opened2026-11-11.
- NO software tests, test runners or linting. Actual model/data evaluation, executable numerical/factual analysis and builds are permitted.
- Keep final evaluation sealed and prior artifacts immutable. No validation/probe/diagnostic case or paraphrase may become a new training example.
- Strong-model labels are allowed; agreement with them is not automatically independent correctness. Probabilities are not automatically calibrated.
- This external assignment is read-only: no training/inference/model downloads, dependency installation, paid calls, external uploads, publication, or production edits.

## Current preferences and choices you may challenge
Full fine-tuning, particular backbones/objectives, synthetic task mix, data volume, prompt/readout, exact experiment sequence and the coordination design are choices—not fundamental truths. Six teams are currently retained at the user's preference; recommendations to change allocation/structure are welcome, but are not permission to do so. Model owns substantial local ML scheduling; owners otherwise work independently.

The strategy discussion must not stop ongoing teams. At the cutoff, one bounded further learning contrast and its independent runtime/evaluation are already authorized; this review does not gate them.

## Important unspecified questions
No concrete production workload/distribution, deployment latency target, acceptable failure cost, precise parameter ceiling, or quantitative definition of generalization has been agreed. The meaning and intended use of output probabilities need scrutiny. Treat these as unanswered product/research questions, not a license to invent requirements.

The hackathon rubric in docs/plan.md values ambition, novelty, usefulness and working software. Distinguish those incentives from evidence of useful learning. The user has coding/LLM experience but is new to training models; explain consequential recommendations plainly.
