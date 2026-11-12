# P12 frozen NLI — execution with resource qualification

## Original P12: complete counts, incomplete resource compliance

The original pass used source commit
`7a3bd87798c808b04773c15effc7d9130d545f99` and completed **624 decisions**, with
**156 attempted/completed native forwards**, **2,390 candidate pairs** and
**zero startup forwards**. There was one tokenizer load and one model load.
Outputs comprise 300 original, 300 reversed and 24 paired-probe decisions.
The parent measured **19.51626120880246 seconds** (about 19.52); conservative
charge was **21 / 480 seconds**. Its clock excludes initial interpreter/time
import; the retained external time log and actual zero exit qualify that clock.
The process group was absent after completion.

**The authorized headroom metric was neither measured nor enforced.** Read the
adjacent canonical `resource-qualification.json` together with the delivery and
native receipts; successful counts do not establish resource compliance.

| Resource item | Original P12 evidence |
| --- | --- |
| Required headroom | `torch.mps.recommended_max_memory() - torch.mps.driver_allocated_memory()` |
| Actually observed | `vm_stat` free + inactive pages multiplied by page size — the wrong metric |
| Required headroom actual | **Unknown / null** |
| Observed maximum driver allocation | 1,082,867,712 bytes (samples) |
| Minimum physical free + inactive | 8,559,722,496 bytes; not a substitute for required headroom |

RSS/driver checks were present, but resource compliance remains incomplete.
Never impute the missing value from adjacent runs, substitute historical
recommended values, or retrospectively reconstruct compliance. The frozen
source and old 624-decision pass were not edited or rerun to repair this gap.
The earlier [source-preparation contract](p12-nli-contract.md) describes its
then-current implementation, including the wrong headroom metric; it does not
override this execution qualification.

## Later E13 NLI: distinct prospective corrected guard

A separate post-07:30 exploration pass used corrected source commit
`0d2edfe499ed1d45c5835efae54b95655c3a8771`, with the actual required
recommended-minus-driver guard. Its native receipt starts at
**2026-11-12T07:31:06.295727Z**. It completed **400 presentations / 800 candidate
pairs / 100 native forwards**, zero startup forwards, with one model and one
tokenizer load. This was **not a rerun of the original 624 decisions**.

The later NLI receipt has **308 post-Torch resource samples**, minimum recorded
recommended-minus-driver headroom **17,978,408,960 bytes**, maximum sampled
driver allocation **1,091,256,320 bytes**, and lifetime process RSS high-water
**1,120,092,160 bytes**. These are nonadditive quantities with different scope;
samples are not continuous peaks. This prospective guard evidence does not
repair, replace or establish the missing original-P12 headroom evidence.
The multi-candidate E13 delivery's aggregate counts and charges must not be
attributed solely to this NLI pass.

## Frozen scientific condition and interpretation

Original R10 assets, renderer and scorer remain fixed: the pinned
`MoritzLaurer/roberta-base-zeroshot-v2.0-c` revision
`d825e740e0c59881cf0b0b1481ccf726b6d65341`, complete native pair cap **512**, no
truncation, and no adaptation. Native entailment-vs-not-entailment scores are
normalized across supplied options at T=1. The rendering/scoring contract is
linked above; no prompt, score or cap repair is implied here.

This is a practical frozen NLI baseline, not a pure architecture ablation.
Choice-normalized probabilities are not calibrated confidence. Declared MIT
licensing is not blanket clearance of upstream training sources. Runtime
completion is not quality or promotion. See Evaluation's
[qualified E14 interpretation](../evaluation/e14-frozen-nli.md); this publication
neither recomputes quality nor authorizes another experiment.

## Canonical evidence

Relative to `/Users/destiner/Code/jeff/artifacts/release/`:

- `p12-nli-20261112-01/delivery-summary.json`
- **`p12-nli-20261112-01/resource-qualification.json`** (mandatory companion)
- `p12-nli-20261112-01/execution-01/run/receipt.json` (original native receipt)
- `p12-nli-20261112-01/execution-01/process-receipt.json`
- `e13-later-exploration-20261112-01/delivery-summary.json`
- `e13-later-exploration-20261112-01/execution-01/p12-nli/receipt.json` (later native receipt)
- `e13-later-exploration-20261112-01/execution-01/p12-nli.process-receipt.json`

[Small P12 provenance manifest](../../manifests/releases/p12-nli-20261112-01.json).
Only existing metadata/receipts support this publication; no input/reference
contents, weights, model execution or new scoring are needed to read it.
