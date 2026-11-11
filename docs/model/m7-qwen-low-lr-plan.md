# M7: one lower-learning-rate control

Lead separately authorized M7 while strategy discussion continued. The **default lower-LR branch** was selected before learning: no concrete learning-path defect was established by Model/D5, so the contingent minimal-correction branch was not used. This is one controlled follow-up, not a rescue inferred from M6's failure or a sweep.

## Treatment and unchanged controls

Start from ORIGINAL pinned P3 `Qwen/Qwen2.5-0.5B-Instruct@7ae557604adf67be50417f59c2c2f167def9a775`, never the trained M6 checkpoint. **Only treatment change: full-parameter AdamW LR2e-5→2e-6.** Preserve M6's exact released1500TRAIN decisions, materialized row/option order and target mapping, seed42,375updates/oneepoch,microbatch1/accum4,betas(.9,.999),eps1e-8,decay.01,globalclip1,foreachFalse,no scheduler. Original P3 prompt/template/conditional-symbol readout/T1/cap1024/no truncation,FP32/MPS/SDPA/fourthreads/no cache/last-token projection stay unchanged.

[Fixed M7 config](../../configs/model/m7-qwen-low-lr.json) differs from M6 only in recipe schema and LR. Hypothesis: smaller updates may preserve pretrained discrimination while reducing the objective. This is **not an established cause** of M6's collapse, and outperforming failed M6 alone is not success versus the original base. One full attempt only; no retry, extraepoch, fallback, alternate objective, new data, LoRA, temperature fitting or default migration.

## Exact pre-outcome bindings

Artifact root `R=/Users/destiner/Code/jeff/artifacts/model/m7-qwen-low-lr-20261111-01/`:

- Clean execution source `574774d631d707de9398c80dc5b936d9563e386c` adds explicit `--experiment m7`; existing M6 default semantics/schemas remain. A fresh read-only reviewer approved treatment isolation, capacity reuse and telemetry/handoff before execution.
- `full-run-freeze.json`, SHA256 `6dbda21d2973331b90e7aab42d02737f0a32af3cf150141dc57a8802b05c942c`: exact branch/source/config/schedule/guards/control/E7/launcher pins before the full invocation. This document describes that earlier freeze, not retroactive preregistration.
- `train-audit/audit.json`, `schedule.jsonl`:1500complete original-boundary prompts89–220tokens at1024; each regenerated schedule byte must equal actual M6 schedule SHA256 `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8`. TRAIN-only loaders and never-train/final isolation remain.
- `control-reuse.json`, SHA256 `74fe6b26adcf1626c0f65f02548405277d4a4a9b2b05971742cec9ad900663f5`: retained M6fresh/P3starting624outputs still byte-identical/maxdelta0; exact assets/config/template/runtime/backend/inputs/outputs rechecked. Original renderer/config/model-load/readout AST matches executed M6source; wholeRuntime file differs through additive P4 metadata and is not claimed byte-identical. **Zero new START forwards.** Metadata/source equivalence is not cryptographic installed-binary identity or a new numerical execution.
- `capacity-reuse.json`, SHA256 `01702d3a05521d7b499ce9f54992e5414c220bd84a16a95b9c9146bc7cc3f13f`: actual M6 capacity receipt/audit/process/events hard pins revalidated. No new disposable update, backwards or capacity model load. Historical source remains historical; model/shapes/data/schedule/template/runtime/guards must match, with only LR/schema/source/observation provenance allowed to differ.
- E7 plan `artifacts/evaluation/e7-predeclared-v1/plan.md`, SHA256 `91b5e28e2a597052d1750f0e05be76b315911cd9ec05aed18ba620bc21a64110`, frozen16:48:03.876UTC. Same624presentations/units, originalP3 and failedM6 controls, all retained encoders; scientific pins separate from mutable operational policies.

## Capacity, reset and observation-only changes

Reuse M6's successful longest-input allocation evidence, not its trained state. Historical one-step/four-extra-backwards probe ended before M6 and saved no weights. M7 loads original base bytes in a fresh process, seeds Python/CPU/MPS42 and creates a new empty optimizer. Same16GiB CPUlifetimeRSS/MPSdriver and≥2GiB recommended-headroom guards, no allocator override/fallback. One whole-process cap2700s including revalidation/bothfits/save; supervisor TERM2690/KILL2700. Historical2100.338s projection and observed capacity are not peak/deadline guarantees. No concurrent substantial Model/Runtime load.

Observation-only additions use already computed results:

- Both existing deterministic TRAIN-fit passes save full allowed-symbol logits/probabilities in option order, option/token/target IDs,K, exact probability and logit top sets/tie counts, top-two probability margin, CE/argmax and source/family metadata. No extra forward or changed loss; both top-set definitions remain distinct under floating-point rounding.
- `gradient-norms.jsonl` saves every already computed preclip norm once per update,375values on completion; no extra norm calculation or weight scan.
- M6's missing TRAIN vectors are **not** backfilled. Earlier scalar CE/argmax limits remain historically true. New scientific observations do not amend M6's outcome or become post-outcome checkpoint criteria.

## Handoff and interpretation

Keep final weights only, ordinary safe FP32 HF directory with byte-copied original four tokenizer files and the same flat `jeff.qwen-trained-checkpoint.v1` sibling manifest. M7 producer IDs qualify the training directory with its parent run root; exact manifest path/hash remains authoritative. Completed source receipt is hashed before manifest publication, without a hash cycle. P5 audit/reload contract does not change.

Model supplies TRAIN fits and reused-start binding. **Runtime P5 alone** performs one fresh-process final300original+300reversed+24already-paired pass under a later≤310s explicit Model grant; no duplicate Model final inference, D3 or extra reversal. Hand off immediately after save, without waiting for docs/merge/strategy.

E7 compares M7 to originalP3 first, separately to failedM6, retaining both-order inherited/new NLL/Brier/agreement, exact raw top-set/tie-aware stability, uniqueness/strict both-order correctness, new-rule flips/success and intent/probe/family/source regressions. Uniform overlapping top sets are not robust discrimination; improved TRAIN fit is not transfer. No combined acceptance score, significance/calibration claim or automatic promotion. All previous artifacts/releases remain immutable;£0additionalactual/pending/allocation, no tests/lint/new dependencies/protectedfinal/paidcalls/uploads.
