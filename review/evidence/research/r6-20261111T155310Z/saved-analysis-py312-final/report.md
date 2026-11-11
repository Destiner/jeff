# R6 saved paired-output analysis v1

Actual stdlib-only CPU analysis of 240 NEW-v2 frozen P3 pairs; no inference or learning.

## Full-population descriptives

| K | pairs | strict unique pairs | identity retained | letter/slot retained |
|---|---:|---:|---:|---:|
| 3 | 55 | 55 | 28 | 36 |
| 4 | 175 | 175 | 82 | 49 |
| 5 | 5 | 5 | 4 | 0 |
| 6 | 5 | 5 | 4 | 0 |

Raw mean TV: option identity **0.330491**; displayed slot **0.574207**.
Exact zeros: 0; exact ones: 0. Malformed pairs: 0. Max raw probability-sum error: 1.34110450745e-07; 470/480 vectors have nonzero last-rounding error. No renormalization of observed probabilities; raw TV may inherit last-rounding differences. Ties and full transitions, per-slot means/winners, family/K and every available nonnull unit/K are in results.json. Identity transition coordinates are original-slot ranks of semantic identities; slot transitions use displayed positions. Tied argmax cases are excluded only from strict retention/transitions; per-order tied counts are separate.

## One shared FIT gamma per K

Units: natural-log mirror contrasts, gamma[j] = b[j] - b[mirror(j)], not complete b (antisymmetric b is gamma/2). Slot arrays below are ONE-based in order. Equal producer, then broad group, then rows within each K; positive-support eligibility only. All related groups stay with their producer.
- K=3: gamma=[-2.0886958807649383, 0.0, 2.0886958807649383]; 35 cases / 2 producers / 7 broad groups.
- K=4: gamma=[-0.9870496782305934, -0.04127290273730519, 0.04127290273730519, 0.9870496782305934]; 83 cases / 3 producers / 13 broad groups.
- K=5: gamma=[0.8410969012878414, 0.24483783984520924, 0.0, -0.24483783984520924, -0.8410969012878414]; 1 cases / 1 producers / 1 broad groups.
- K=6: gamma=[2.09175780190513, 0.9637603701643316, -1.0896558436295047, 1.0896558436295047, -0.9637603701643316, -2.09175780190513]; 1 cases / 1 producers / 1 broad groups.

## Source-heldout descriptive fidelity

| K | cases | RMSE | MAE | SSE reduction vs zero | symmetric observed energy fraction | TV model | TV semantic copy | TV static slot copy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 20 | 1.125938 | 0.902020 | 0.782182 | 0.048691 | 0.194357 | 0.415462 | 0.377486 |
| 4 | 92 | 1.466827 | 1.077667 | 0.115156 | 0.139791 | 0.283012 | 0.303617 | 0.671847 |
| 5 | 4 | 2.696967 | 1.914028 | -0.110429 | 0.493822 | 0.243507 | 0.256219 | 0.989616 |
| 6 | 4 | 2.414795 | 1.729087 | -0.462677 | 0.374552 | 0.454945 | 0.443046 | 0.980380 |

Unsupported heldout K: []; unscored cases: 0. Zero-excluded cases: 0. Per-K metrics balance producers/groups/rows; macro in results.json gives supported K equal weight and averages per-K metrics (not pooled RMSE). Observed symmetric and antisymmetric energies sum to zero-baseline centered-y energy; symmetric energy is not removed before residual scoring. TV predictions use both directions, normalizing only modeled softmax. Semantic-copy and slot-copy comparators have no fitted parameters.

### Heldout sources individually

- `2130e39a-4c66-4679-a236-3b73a3e497e5` (rule_application):
  - K=3, n=8, broad groups=1: RMSE=1.027734, MAE=0.817377, SSE reduction=0.789884; signed residual slots=[-0.4356406869877286, 0.10841679814877293, 0.3272238888389557]; case RMS median/p90=0.815475/1.564834; bidirectional TV={'modeled': 0.25965881463832174, 'semantic_copy': 0.5361458115221467, 'static_slot_copy': 0.2786915121541824}.
  - K=4, n=32, broad groups=4: RMSE=0.942753, MAE=0.737371, SSE reduction=0.310835; signed residual slots=[0.039087798454028315, 0.011125167325170559, 0.09053816146856683, -0.14075112724776578]; case RMS median/p90=0.833141/1.420236; bidirectional TV={'modeled': 0.3150592581525614, 'semantic_copy': 0.4337167964586115, 'static_slot_copy': 0.3753467728711257}.

- `3f9deab4-0acd-43b8-9a0b-dfeb977563ae` (sentiment):
  - K=4, n=40, broad groups=4: RMSE=1.580346, MAE=1.203122, SSE reduction=-0.503862; signed residual slots=[1.4405086666490003, 0.11394205284523802, -0.32921042440019593, -1.2252402950940426]; case RMS median/p90=1.352766/2.329095; bidirectional TV={'modeled': 0.4304483238671911, 'semantic_copy': 0.38136612525063357, 'static_slot_copy': 0.6652670776189097}.

- `96cbb91d-4c56-4f68-b5b4-a593b9633faf` (intent):
  - K=3, n=12, broad groups=4: RMSE=1.216240, MAE=0.986663, SSE reduction=0.776328; signed residual slots=[-0.8020809989958403, 0.00573526962198305, 0.796345729373857]; case RMS median/p90=0.829206/1.708727; bidirectional TV={'modeled': 0.12905591212787712, 'semantic_copy': 0.29477779070937987, 'static_slot_copy': 0.4762810791023639}.
  - K=4, n=20, broad groups=4: RMSE=1.751704, MAE=1.292509, SSE reduction=0.293698; signed residual slots=[-0.8546316692587063, 0.5699017470125358, -0.5020557795695207, 0.7867857018156912]; case RMS median/p90=1.414816/2.823487; bidirectional TV={'modeled': 0.10352952924783837, 'semantic_copy': 0.09576857069623086, 'static_slot_copy': 0.9749267445826661}.
  - K=5, n=4, broad groups=4: RMSE=2.696967, MAE=1.914028, SSE reduction=-0.110429; signed residual slots=[-1.0159292452783566, -0.9229842118277175, -0.07305052239426102, 0.33037386352842113, 1.6815901159719142]; case RMS median/p90=2.720799/3.514385; bidirectional TV={'modeled': 0.24350698759338643, 'semantic_copy': 0.2562188067066984, 'static_slot_copy': 0.9896163077109179}.
  - K=6, n=4, broad groups=4: RMSE=2.414795, MAE=1.729087, SSE reduction=-0.462677; signed residual slots=[-3.429599453221928, -0.9612967044500591, 1.1121685808441437, 1.1587460842180286, 0.40674478847093704, 1.713236704138878]; case RMS median/p90=1.938617/3.353263; bidirectional TV={'modeled': 0.4549448910885321, 'semantic_copy': 0.44304569697033, 'static_slot_copy': 0.9803795609977897}.

## Interpretation and limits

This measures fidelity of one static mirror-antisymmetric account, not correctness, calibration, a deployed correction, or a causal mechanism. Label and slot are confounded; mirror-symmetric bias is unidentified. Residuals can include content/order changes and other violations. The three heldout producers are observed construction units, not independent samples: shared teacher/renderer dependence remains. Numerous cases/groups/options do not establish independence. Odd-middle retention can satisfy both coordinate systems. No pass threshold, p-values, intervals, alternate fit/split, epsilon sensitivity, second model, or TRAIN diagnostic was used.

## Reproducibility and freeze

Frozen binding: `aefc3eeaad4f1ef1a82ce3425154f8a3e28da6ef66ace9bec9aa191de3cf0b8a`. Script: `116ae8197479a378d23f6cd36db6ebabe1b3251c6f736ecb63a39bcfde328724`. Exact byte-hash scope and all metadata memberships/split are in input-binding.json; no upstream raw/private files read. Primary predeclaration outranks supporting method. Code manually reviewed in full before binding; metadata-only binding step precedes all probability statistics. Code and binding made read-only before probability statistics. No outcome-driven rewrites or refits.

Python: `3.12.16 (main, Oct 26 2026, 13:59:40) [Clang 23.1.3 ]`; platform: `macOS-26.7.1-arm64-arm-64bit`.

Actual commands (bind first, then analyze once):
```sh
/Users/destiner/Code/jeff/.venv/bin/python -I -S /Users/destiner/Code/jeff/.worktrees/research/experiments/research/analyze_order_bias.py bind --task-root /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z --output-dir /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/saved-analysis-py312-final
/Users/destiner/Code/jeff/.venv/bin/python -I -S /Users/destiner/Code/jeff/.worktrees/research/experiments/research/analyze_order_bias.py analyze --task-root /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z --output-dir /Users/destiner/Code/jeff/artifacts/research/r6-20261111T155310Z/saved-analysis-py312-final
```
Analysis start/end UTC: 2026-11-11T16:25:56.304529+00:00 / 2026-11-11T16:25:56.315846+00:00; CPU seconds for validation/descriptives/fitting: 0.011208. No ML imports/loads, dependencies, paid work, tests/lint, tracked edits, commits, merges or mailbox. All work synchronous; no jobs remain.
