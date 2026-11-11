# Jeff: independent Fable review

A frozen, private review of a small text decision model and the way it is being developed. This is not a production release or a claim of reliable decision capability.

**Code base:** `91e09919bdf3b38370bf18c7bee0f6a2bbb26871`  
**Evidence cutoff:** 2026-11-11 16:53:50 UTC  
**Review tag:** `fable-review-20261111-v1`  
**Audience:** five separate, initially independent Claude Fable sessions.

## Start on the other machine

Use existing GitHub authentication; do not paste credentials into prompts.

```sh
git clone https://github.com/Destiner/jeff.git
cd jeff
git checkout --detach fable-review-20261111-v1
git rev-parse HEAD
python3 review/resolve_path.py --verify
```

Give each fresh session the contents of exactly one prompt:

| Session | Prompt |
|---|---|
| 1. Problem framing and feasibility | [01-framing.md](prompts/01-framing.md) |
| 2. Learning mechanics and implementation | [02-learning.md](prompts/02-learning.md) |
| 3. Data and evaluation validity | [03-data-evaluation.md](prompts/03-data-evaluation.md) |
| 4. Next experiments and alternatives | [04-experiments.md](prompts/04-experiments.md) |
| 5. Execution and ways of working | [05-execution.md](prompts/05-execution.md) |

Session1 has a deliberately staged reading order. Do not give it our diagnostic conclusions before its initial framing memo. Other sessions may start with the observations.

All sessions read [protocol.md](protocol.md); [brief.md](brief.md) states the reconstructed mission and constraints. [observations.md](observations.md) is an evidence-qualified orientation, not a required diagnosis. [evidence-map.md](evidence-map.md) leads to deeper evidence. Read selectively; do not dump the entire artifact collection into context.

## What is portable

The code history retains actual execution revisions. `evidence/` contains912 explicitly selected original artifacts (~93.4MiB uncompressed), including TRAIN/development data, predictions, training logs, scientific recipes, evaluations and bounded operational observations. [manifest.json](manifest.json) records each original path, portable path, byte count and SHA256. Copies are byte-identical; existing JSON/Markdown absolute paths have NOT been rewritten.

Resolve an old artifact path rather than trying to access its original machine:

```sh
python3 review/resolve_path.py artifacts/model/m6-qwen-20261111-01/training/receipt.json
python3 review/resolve_path.py --list artifacts/research/r6
```

These files support code inspection and independent CPU arithmetic, not complete model-execution reproduction. Model/tokenizer assets, pretrained/trained weights, environments, live mailbox, raw agent sessions and all sealed final cases/labels/predictions are intentionally absent. Some omitted or redundant evidence is described in the manifest; missing files are not evidence of a live-project defect.

## Snapshot versus live work

M6/P4, E6, D5 and the R6 diagnostic are completed evidence here. M7/P5/E7 and D6/R7/I5 are authorized plans at the cutoff, NOT results in this packet. Do not infer later outcomes from a plan. The live teams continue independently; do not pull a moving branch during review or follow paths into their workspaces.

The root README and early planning documents are historical and sometimes lag later reports (for example, later runs include MPS execution). This index fixes the review boundary without rewriting that history. A future update must be a new version/tag, not a replacement of this snapshot.

## Return and synthesis

Return each review as a standalone Markdown document, named01-framing through05-execution, with its actual review commit and the common output structure. Store outputs outside this checkout; do not edit code or publish the review. Keep sessions independent until their first answers are complete.

We will distinguish verified defects, falsifiable hypotheses and strategic choices, then choose a few actions. Agreement among sessions using the same model is not independent proof.

Private review only. No project open-source license is selected; existing upstream notices remain. See [publication-audit.md](publication-audit.md) and [artifact-audit.md](artifact-audit.md) for the bounded publication checks and limitations.
