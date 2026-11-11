# R6 frozen order/letter diagnostic packet

**Executed once by Runtime on2026-11-11,16:22:50–16:23:03UTC:**192/192 forwards, original frozen P3, Model's single-use grant after M6/P4 completed; slot returned. [Scientific diagnosis](order-instability-diagnosis.md) and [Runtime execution report](../runtime/r6-order-diagnostic.md) distinguish outcomes from preparation. Research never loaded the model. The sections below preserve the input/execution freeze, not a change to M6/E6. The immutable packet's original `prepared_not_executed` status is historical, not today's execution state.

## Frozen scope

Artifact root `/Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/`.

- `packet-v1/packet.json` SHA256 **`7598451302c5389e62476c88e7c2489fa355e0c40611e91cfbd6da1d9dc35e03`**.
- `inputs.jsonl`: **48 preselected TRAIN cases ×4 conditions =192 presentations**, SHA256 `178708cd6a620c395d29131a0eb0bad65f66f8a71e608950f7282a4e9e2ed061`.
- `selection.json` SHA256 `8e008f2c39e37529d32942b15eaba5e5b13cc0b9b3766f6d9b12722f15304a8f`; `config.json` SHA256 `128d550e355af4772a8f996ccb1f49675e5ba6bdc61d2ed7a1c84e11c4b6090f`.
- Original released v2 manifest SHA256 `d97e965b7332ec8ae933c1f5bbf261816fb0db47b2fc06b347b053aabd2066ac`. Preparation loaded only its9 TRAIN shards, not validation/probe/D3/final rows. Allocation metadata supplied explicit TRAIN domain/mechanism groups.

[`prepare_order_packet.py`](../../experiments/research/prepare_order_packet.py) was actually run with stdlib Python. It selected16 cases/family:4inherited+6each of two new producers, without accessing target values or using prediction outcomes/text/option count to rank candidates. Fixed SHA256 salt and greedy unused-group/root/broad-stratum coverage are recorded verbatim in selection.json. There are48 declared source groups,48 recorded roots,12 explicit new-rule policy instances; missing inherited policy identities remain unknown. Zero uniqueness fallbacks. These are dependent authored sources, not48 independent collections. K distribution:3→11cases,4→34,5→2,6→1; no K2 selected, no outcome-based replacement.

## The four conditions

For a semantic option originally at zero-based index j, r(j)=K−1−j:

| Condition | Display order | Letter attached to original option j |
| --- | --- | --- |
| O0L0 | Original | A+j |
| O0L1 | Original | A+r(j) |
| O1L0 | Reversed | A+r(j) |
| O1L1 | Reversed | A+j |

Only order and letter assignment change. State/question/option text and the complete letter set stay fixed. IDs, groups, positions and conditions are external join fields, never prompt features. Actual supplied letters determine answer-token readout before mapping back to original option IDs. The stock P3 reader/renderer is **not** compatible with this packet; it would regenerate ascending letters and has discarded startup forwards.

## Execute once, only through Runtime

Use [`run_order_packet.py`](../../experiments/research/run_order_packet.py), a separate owned diagnostic—not an edit to Runtime's P3/P4 code. Source review and actual packet arithmetic are in `packet-review.md`. Parent closed its pre-audit substitution concern by hard-pinning packet.json and checking its declared input/config/selection hashes. Runtime must additionally pin the exact reviewed runner hash from the ready handoff. Its preselected packet cannot be swapped for a subset/replacement.

Required controls: original Qwen2.5-0.5B revision `7ae557604adf67be50417f59c2c2f167def9a775`, original weight SHA256 `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe`, same P3 SYSTEM/USER/official chat template, cap1024/no truncation, FP32/MPS, batch1/fourthreads/SDPA, eval/inference mode, use_cache=False, logits_to_keep=1, T1 allowed-symbol softmax. No trained M6 checkpoint, download, dependency addition, generation, fallback, retries or extra startup forwards.

Runtime first performs the runner's tokenizer-only `audit` in its existing isolated environment; `USE_TORCH=0` prevents model imports. It verifies actual custom-letter boundaries and complete prompts. Original P3 audit metadata is pinned at `artifacts/release/p3-qwen-20261111-01/audit-02/audit.json`; no referenced Evaluation files are opened. Audit uses its weight-hash attestation; predict verifies actual weight contents once before loading. The same interpreter/package versions and file paths must be used for audit/predict. Missing/broken audit stops, not a fallback.

Both commands require explicit `--inputs`, `--config`, `--selection`, `--model-dir`, `--p3-audit`, `--audit-dir`, and `--train-only-confirmed`. `predict` also requires a new `--output-dir`. Use absolute paths; outputs/audit must be new directories outside the frozen packet. All arguments/data hashes are in the ready handoff. No Research ML environment was installed; Research's package-only environment cannot tokenize the packet.

**Resource/attempt boundary:** one Model grant consumed once; at most192 model calls including the first forward, which is retained rather than warmed up/repeated. Runtime must use its existing external supervisor with **300seconds total budget across audit+predict** (remaining time passed to predict), preserve normal P3 process environment/fallback prohibition, and stop/report partial failure with no automatic second attempt. Runner guards300s per command and8GiB CPU-RSS/MPS-driver separately are only cooperative; they do not replace that shared supervisor deadline. The two memory measurements overlap and are not additive or true unified-memory peaks. No slot is reserved merely because this document exists.

Outputs preserve all option probabilities/allowed logits, observed full-vocabulary allowed mass, first-forward and complete timings, memory samples, code/input/asset hashes, and attempted/completed/written counts. Runtime must return supervisor evidence plus passed receipt and192/192 complete outputs; partial/error evidence stays immutable. No raw full-vocabulary vector, target or input text is copied into predictions. A low allowed mass alone does not invalidate conditional classification.

## Predeclared interpretation

`analysis-predeclaration-v1.md` was written before export inspection or any new outcomes. The focused two-source method review and exact quotations are in `method/`. For centered log probabilities x aligned by semantic identity:

- Label-assignment contrast: `alpha=((x00−x01)+(x11−x10))/2`.
- Position/order contrast: `beta=((x00−x11)+(x01−x10))/2`.
- Additivity residual: `R=x00−x01+x10−x11` (zero under the invariant-content additive model).

Report these magnitudes, mirror-symmetry violations, paired identity/letter/position retention and TV, by family/source units with all coverage. No labels/accuracy fit or second learned correction model. Ordinary reversal alone confounds labels/positions and identifies only mirror-antisymmetric effects. Four cells separate some label-assignment-associated versus position/order-associated variation under assumptions, **not** static token prior from alphabet familiarity/symbol binding, nor position from altered content context. Middle/symmetric biases and general interactions remain unidentified. TRAIN behavioral observations are not new held-out task evidence; M6 already trains on shuffled options, and this diagnostic does not amend its recipe.
