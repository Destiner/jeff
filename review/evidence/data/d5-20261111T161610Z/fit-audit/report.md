# D5 bounded TRAIN fit audit

## Scope and method

Exactly **1,500 paired TRAIN IDs**, each joined in order to the same schedule for identity, label, option ordering, arity and source. No frozen manifest/shard join was needed: the independently read schedule supplies every baseline label and arity. No protected data, weights, model execution, new learning, optimizer/gradient source, network, dependencies, Git, tests or lint were used.

Thresholds were declared in `analyze.py` before computation: absolute CE deviations in nats = [1e-06, 0.0001, 0.001, 0.01, 0.1]; absolute target-p deviations = [1e-06, 0.0001, 0.001, 0.01, 0.05]. All are descriptive, not tuned criteria. Exact comparisons use parsed stored floats against Python `math.log(k)` / `1/k`; threshold membership is inclusive. SD is population SD; quantiles use linear interpolation. All aggregates are record-weighted, not equal-weighted across groups.

Agreement is recomputed as predicted_position == target_position, with zero-based positions. Brier uses the sum-over-classes convention. The uniform comparator is a mathematical same-schedule baseline, not generated model output. Random choice and deterministic first-tie choice are distinct comparators.

## Overall results

| Metric | Before | After | Same-schedule uniform baseline |
|---|---:|---:|---:|
| Agreement | 805/1500 (53.666666667%) | 431/1500 (28.733333333%) | Random expected 26.941111111%; first-tie 28.733333333% |
| Mean CE (nats) | 1.357723628623 | 1.390592028141 | 1.322382805560 |
| Mean CE − uniform | 0.035340823063 | 0.068209222581 | 0 |
| Mean CE-derived target p | 0.503287447047 | 0.273069544409 | 0.269411111111 |
| Actual mean Brier | Missing vectors | Missing vectors | 0.730588888889 |

Stored agreement mismatch counts: before 0, after 0. Expected random agreement count is 404.116666666667; deterministic first-tie count is 431. These are not interchangeable.

Predicted-position counts: before `{"0": 417, "1": 384, "2": 411, "3": 278, "4": 7, "5": 3}`; after `{"0": 1500}`. Target counts: `{"0": 431, "1": 423, "2": 368, "3": 266, "4": 11, "5": 1}`.

Paired transitions: `{"agreement_transitions": {"correct -> correct": 229, "correct -> incorrect": 576, "incorrect -> correct": 202, "incorrect -> incorrect": 493}, "ce_after_minus_before": {"max": 2.2049833582204883, "mean": 0.03286839951792687, "median": 0.47309619188308716, "min": -8.687062740325928, "population_sd": 1.6598529244232383, "q05": -3.3610959559679032, "q95": 1.8707618087064475, "range": 10.892046098546416, "unique_exact_saved_float_values": 1500}, "ce_decreased_rows": 593, "ce_increased_rows": 907, "ce_unchanged_rows": 0}`.

## Stratified agreement and CE

Complete exact-source and all 880 (source, group_id) cells per phase, including each cell’s same-schedule baseline and CE/target-p statistics, are in `report.json`. Source-group means are descriptive, often based on few rows, not independent causal evidence. The tables below do not relabel or normalize source identities.

### family

| Cell | n | Before agreement | After agreement | Before CE | After CE | Uniform CE | Random agreement | First-tie agreement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| intent | 500 | 88.400000% | 28.000000% | 0.396152925 | 1.391937832 | 1.314858234 | 27.320000% | 28.000000% |
| rule_application | 500 | 36.800000% | 30.800000% | 1.657126115 | 1.335712646 | 1.265995822 | 28.503333% | 30.800000% |
| sentiment | 500 | 35.800000% | 27.400000% | 2.019891845 | 1.444125607 | 1.386294361 | 25.000000% | 27.400000% |

### option_arity

| Cell | n | Before agreement | After agreement | Before CE | After CE | Uniform CE | Random agreement | First-tie agreement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 100.000000% | 0.000000% | 0.589677095 | 1.306376457 | 0.693147181 | 50.000000% | 0.000000% |
| 3 | 394 | 61.421320% | 35.279188% | 1.157842136 | 1.182190413 | 1.098612289 | 33.333333% | 35.279188% |
| 4 | 1035 | 48.599034% | 26.666667% | 1.499568172 | 1.450310878 | 1.386294361 | 25.000000% | 26.666667% |
| 5 | 56 | 85.714286% | 19.642857% | 0.398776651 | 1.675641573 | 1.609437912 | 20.000000% | 19.642857% |
| 6 | 14 | 78.571429% | 35.714286% | 0.387243860 | 1.706496860 | 1.791759469 | 16.666667% | 35.714286% |

### target_position

| Cell | n | Before agreement | After agreement | Before CE | After CE | Uniform CE | Random agreement | First-tie agreement |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 431 | 53.132251% | 100.000000% | 1.412589134 | 0.812336753 | 1.303914075 | 27.463264% | 100.000000% |
| 1 | 423 | 54.609929% | 0.000000% | 1.231813667 | 1.790865680 | 1.299451048 | 27.576832% | 0.000000% |
| 2 | 368 | 57.065217% | 0.000000% | 1.286381888 | 1.626891939 | 1.304344016 | 27.454710% | 0.000000% |
| 3 | 266 | 47.744361% | 0.000000% | 1.590883211 | 1.352821204 | 1.400095017 | 24.699248% | 0.000000% |
| 4 | 11 | 63.636364% | 0.000000% | 0.869043760 | 1.563803814 | 1.609437912 | 20.000000% | 0.000000% |
| 5 | 1 | 100.000000% | 0.000000% | 0.579394817 | 2.486203194 | 1.791759469 | 16.666667% | 0.000000% |

## Uniformity sensitivity and justified certificates

### before

Exact stored CE versus ln(k): `{"below": 920, "equal": 0, "above": 580}`.
CE-derived target p versus 1/k: `{"below": 580, "equal": 0, "above": 920}`.

| Absolute CE threshold | Below −threshold | Within ±threshold (inclusive) | Above threshold |
|---:|---:|---:|---:|
| 1e-06 | 920 | 0 | 580 |
| 0.0001 | 920 | 0 | 580 |
| 0.001 | 920 | 0 | 580 |
| 0.01 | 918 | 3 | 579 |
| 0.1 | 894 | 47 | 559 |

| Absolute target-p threshold | Below −threshold | Within ±threshold (inclusive) | Above threshold |
|---:|---:|---:|---:|
| 1e-06 | 580 | 0 | 920 |
| 0.0001 | 580 | 0 | 920 |
| 0.001 | 579 | 2 | 919 |
| 0.01 | 576 | 12 | 912 |
| 0.05 | 535 | 92 | 873 |

Conditional strict-winner certificate counts: `{"target_p_gt_half_and_correct": 733, "target_p_gt_half_but_incorrect": 0, "correct_without_this_certificate": 72}`.
CE values exactly representable as binary32: 1500/1500. This characterizes saved scalars only, not unretained logits.

### after

Exact stored CE versus ln(k): `{"below": 708, "equal": 0, "above": 792}`.
CE-derived target p versus 1/k: `{"below": 792, "equal": 0, "above": 708}`.

| Absolute CE threshold | Below −threshold | Within ±threshold (inclusive) | Above threshold |
|---:|---:|---:|---:|
| 1e-06 | 708 | 0 | 792 |
| 0.0001 | 708 | 0 | 792 |
| 0.001 | 708 | 0 | 792 |
| 0.01 | 708 | 0 | 792 |
| 0.1 | 434 | 274 | 792 |

| Absolute target-p threshold | Below −threshold | Within ±threshold (inclusive) | Above threshold |
|---:|---:|---:|---:|
| 1e-06 | 792 | 0 | 708 |
| 0.0001 | 792 | 0 | 708 |
| 0.001 | 792 | 0 | 708 |
| 0.01 | 792 | 21 | 687 |
| 0.05 | 788 | 281 | 431 |

Conditional strict-winner certificate counts: `{"target_p_gt_half_and_correct": 139, "target_p_gt_half_but_incorrect": 0, "correct_without_this_certificate": 292}`.
CE values exactly representable as binary32: 1500/1500. This characterizes saved scalars only, not unretained logits.

## Within-(arity, target position) across-input spread

Each row of this table describes separate TRAIN inputs, never entries of one reconstructed probability vector. Unique counts are exact parsed CE / CE-derived-p float counts, not rounded bins. Input counts use the schedule’s prompt hashes. Full means, SDs and quantiles are in JSON.

| Phase | [k, target position] | n / unique inputs | CE min … max | CE SD | Unique CE / p | Target-p min … max | Target-p SD |
|---|---|---:|---:|---:|---:|---:|---:|
| before | [2, 1] | 1 / 1 | 0.589677095413 … 0.589677095413 | 0 | 1 / 1 | 0.55450630846 … 0.55450630846 | 0 |
| before | [3, 0] | 139 / 139 | 2.74177600659e-05 … 9.28396511078 | 1.82089164 | 139 / 139 | 9.29020253689e-05 … 0.999972582616 | 0.366501798 |
| before | [3, 1] | 136 / 136 | 1.00135303001e-05 … 6.55760574341 | 1.47917821 | 136 / 136 | 0.00141927976554 … 0.99998998652 | 0.402105989 |
| before | [3, 2] | 119 / 119 | 4.76836021335e-06 … 6.35170507431 | 1.37822076 | 119 / 119 | 0.00174377134029 … 0.999995231651 | 0.359190852 |
| before | [4, 0] | 276 / 276 | 2.65833186859e-05 … 9.18410682678 | 1.61940909 | 276 / 276 | 0.000102658067346 … 0.999973417035 | 0.348650942 |
| before | [4, 1] | 273 / 273 | 5.72202952753e-06 … 6.57661056519 | 1.36538604 | 273 / 273 | 0.00139256130056 … 0.999994277987 | 0.393703576 |
| before | [4, 2] | 234 / 234 | 0.000264847971266 … 6.74008178711 | 1.61316182 | 234 / 234 | 0.00118255043528 … 0.999735187098 | 0.37797366 |
| before | [4, 3] | 252 / 252 | 7.74857380748e-06 … 8.07177066803 | 1.72070357 | 252 / 252 | 0.00031222993575 … 0.999992251456 | 0.353685431 |
| before | [5, 0] | 11 / 11 | 4.72057654406e-05 … 2.56462883949 | 0.842539152 | 11 / 11 | 0.0769477361031 … 0.999952795349 | 0.329864968 |
| before | [5, 1] | 12 / 12 | 2.00269605557e-05 … 1.50223958492 | 0.411989206 | 12 / 12 | 0.22263100037 … 0.99997997324 | 0.215042488 |
| before | [5, 2] | 11 / 11 | 0.00022825972701 … 4.84141683578 | 1.38928958 | 11 / 11 | 0.00789585898712 … 0.999771766322 | 0.282899388 |
| before | [5, 3] | 11 / 11 | 0.0169946812093 … 0.47798448801 | 0.1373788 | 11 / 11 | 0.620031814834 … 0.983148913784 | 0.111177386 |
| before | [5, 4] | 11 / 11 | 0.000306916830596 … 5.86247396469 | 1.63704877 | 11 / 11 | 0.00284419852481 … 0.999693130264 | 0.334776683 |
| before | [6, 0] | 5 / 5 | 0.000124923535623 … 1.25148129463 | 0.481113853 | 5 / 5 | 0.286080713017 … 0.999875084267 | 0.269077024 |
| before | [6, 1] | 1 / 1 | 9.59588724072e-05 … 9.59588724072e-05 | 0 | 1 / 1 | 0.999904045731 … 0.999904045731 | 0 |
| before | [6, 2] | 4 / 4 | 0.00364342378452 … 0.651883900166 | 0.277241852 | 4 / 4 | 0.521063220445 … 0.99636320543 | 0.202417629 |
| before | [6, 3] | 3 / 3 | 0.196534752846 … 1.40682852268 | 0.510671945 | 3 / 3 | 0.244918807167 … 0.821572778807 | 0.252232396 |
| before | [6, 5] | 1 / 1 | 0.579394817352 … 0.579394817352 | 0 | 1 / 1 | 0.560237309892 … 0.560237309892 | 0 |
| after | [2, 1] | 1 / 1 | 1.30637645721 … 1.30637645721 | 0 | 1 / 1 | 0.270799534422 … 0.270799534422 | 0 |
| after | [3, 0] | 139 / 139 | 0.589450001717 … 0.602368533611 | 0.00274911715 | 139 / 139 | 0.547513295476 … 0.554632247646 | 0.00151447169 |
| after | [3, 1] | 136 / 136 | 1.57535016537 … 1.58594918251 | 0.00260906435 | 136 / 136 | 0.20475335255 … 0.206935078495 | 0.000536967083 |
| after | [3, 2] | 119 / 119 | 1.40070819855 … 1.42057847977 | 0.00566345264 | 119 / 119 | 0.241574230665 … 0.246422386155 | 0.00138152116 |
| after | [4, 0] | 276 / 276 | 0.895228087902 … 0.906547904015 | 0.00203891808 | 276 / 276 | 0.403916177488 … 0.408514410819 | 0.000828408181 |
| after | [4, 1] | 273 / 273 | 1.86926078796 … 1.89328289032 | 0.00546650362 | 273 / 273 | 0.150576669846 … 0.154237634001 | 0.000833826051 |
| after | [4, 2] | 234 / 234 | 1.70365405083 … 1.72741174698 | 0.00516371125 | 234 / 234 | 0.177743861211 … 0.18201720729 | 0.000930021697 |
| after | [4, 3] | 252 / 252 | 1.32996463776 … 1.34681499004 | 0.00358276816 | 250 / 250 | 0.260067259758 … 0.264486613975 | 0.000939755667 |
| after | [5, 0] | 11 / 11 | 1.13278675079 … 1.13837361336 | 0.00185680125 | 11 / 11 | 0.320339594413 … 0.322134296409 | 0.000596377757 |
| after | [5, 1] | 12 / 12 | 2.11931228638 … 2.12414312363 | 0.00134561393 | 12 / 12 | 0.119535351414 … 0.120114204289 | 0.000161226923 |
| after | [5, 2] | 11 / 11 | 1.93824100494 … 1.94699716568 | 0.00274215664 | 11 / 11 | 0.142701939138 … 0.14395694676 | 0.000393112622 |
| after | [5, 3] | 11 / 11 | 1.57069838047 … 1.57705748081 | 0.00227963325 | 11 / 11 | 0.206582076468 … 0.207899938388 | 0.00047254007 |
| after | [5, 4] | 11 / 11 | 1.56054615974 … 1.5663446188 | 0.00178876278 | 11 / 11 | 0.208807058431 … 0.210021334673 | 0.000374528097 |
| after | [6, 0] | 5 / 5 | 1.22180056572 … 1.22513282299 | 0.0011489319 | 5 / 5 | 0.293718685138 … 0.294699063893 | 0.000338026831 |
| after | [6, 1] | 1 / 1 | 2.20507931709 … 2.20507931709 | 0 | 1 / 1 | 0.1102417809 … 0.1102417809 | 0 |
| after | [6, 2] | 4 / 4 | 2.02305555344 … 2.02958774567 | 0.00231263649 | 4 / 4 | 0.131389675948 … 0.13225074785 | 0.000304850132 |
| after | [6, 3] | 3 / 3 | 1.65577757359 … 1.66154110432 | 0.00235305 | 3 / 3 | 0.189846181773 … 0.190943525325 | 0.000448010934 |
| after | [6, 5] | 1 / 1 | 2.48620319366 … 2.48620319366 | 0 | 1 / 1 | 0.0832253580228 … 0.0832253580228 | 0 |

## Actual-record examples (TRAIN ID only)

The examples are deterministically selected extrema, closest-to-uniform CE, and first strict-winner certificate; they are not additional model outputs. No question, context or option text is reproduced.

### before

```json
{
  "min_ce_minus_uniform": {
    "train_id": "data:pilot-v2:intent-a-r2:g119:r01",
    "option_arity": 6,
    "target_position": 1,
    "predicted_position": 1,
    "ce": 9.595887240720913e-05,
    "ce_derived_target_p": 0.9999040457314982,
    "uniform_target_p": 0.16666666666666666,
    "ce_minus_uniform": -1.7916635103556477
  },
  "max_ce_minus_uniform": {
    "train_id": "data:pilot-v2:intent-b-r2:g109:r01",
    "option_arity": 3,
    "target_position": 0,
    "predicted_position": 1,
    "ce": 9.283965110778809,
    "ce_derived_target_p": 9.290202536894882e-05,
    "uniform_target_p": 0.3333333333333333,
    "ce_minus_uniform": 8.1853528221107
  },
  "nearest_ce_to_uniform": {
    "train_id": "data:pilot-v2:sentiment-a:g085:r01",
    "option_arity": 4,
    "target_position": 0,
    "predicted_position": 1,
    "ce": 1.3849785327911377,
    "ce_derived_target_p": 0.2503291736026696,
    "uniform_target_p": 0.25,
    "ce_minus_uniform": -0.0013158283287528771
  },
  "first_correct_target_p_gt_half": {
    "train_id": "data:pilot-v2:intent-a-r2:g098:r01",
    "option_arity": 4,
    "target_position": 3,
    "predicted_position": 3,
    "ce": 0.16993775963783264,
    "ce_derived_target_p": 0.8437173282342713,
    "uniform_target_p": 0.25,
    "ce_minus_uniform": -1.216356601482058
  }
}
```

### after

```json
{
  "min_ce_minus_uniform": {
    "train_id": "data:pilot-v2:intent-a-r2:g019:r01",
    "option_arity": 6,
    "target_position": 0,
    "predicted_position": 0,
    "ce": 1.2218005657196045,
    "ce_derived_target_p": 0.2946990638925017,
    "uniform_target_p": 0.16666666666666666,
    "ce_minus_uniform": -0.5699589035084505
  },
  "max_ce_minus_uniform": {
    "train_id": "data:pilot-v2:intent-a-r2:g039:r01",
    "option_arity": 6,
    "target_position": 5,
    "predicted_position": 0,
    "ce": 2.486203193664551,
    "ce_derived_target_p": 0.0832253580227771,
    "uniform_target_p": 0.16666666666666666,
    "ce_minus_uniform": 0.6944437244364958
  },
  "nearest_ce_to_uniform": {
    "train_id": "data:pilot-v1:intent:g14:r03",
    "option_arity": 5,
    "target_position": 3,
    "predicted_position": 0,
    "ce": 1.5770574808120728,
    "ce_derived_target_p": 0.20658207646822385,
    "uniform_target_p": 0.2,
    "ce_minus_uniform": -0.03238043162202753
  },
  "first_correct_target_p_gt_half": {
    "train_id": "data:pilot-v2:rule-a:g001:r14",
    "option_arity": 3,
    "target_position": 0,
    "predicted_position": 0,
    "ce": 0.6022367477416992,
    "ce_derived_target_p": 0.5475854547467741,
    "uniform_target_p": 0.3333333333333333,
    "ce_minus_uniform": -0.49637554092641056
  }
}
```

## Official receipt reconciliation

**MATCH**: both fit-row hashes and the schedule hash match the official receipt. Every official overall, family and source-group statistic was recomputed. Integer counts are exact; numeric comparisons use absolute tolerance 1e-10.

Issues: `[]`. Official online mean CE = 1.4003377714039138; it is not the same aggregate as either frozen fit pass. No implementation-level cause is inferred.

## Scientifically bounded conclusion

The recorded agreement changes from 53.666667% to 28.733333%; mean CE changes from 1.357723629 to 1.390592028. All 1500 after rows select position zero, which numerically matches the deterministic first-choice baseline’s agreement on this schedule. This does **not** establish tied logits or uniform probability vectors. The CE-derived target probabilities and per-cell variation must be assessed separately from the argmax positions.

Under unsmoothed categorical CE, target p ≈ exp(−CE). A target p differing materially from 1/k rules out an exactly uniform vector for that row, subject to stored-CE precision. A correct target with p > 0.5 is necessarily a strict winner because all non-target mass sums to less than p. Neither statement identifies other probabilities. No all-non-target-equal assumption or cross-record vector reconstruction is used.

**Unresolved evidence gap:** actual Brier, entropy, top-two margin and exact tie counts require the missing vectors/logits. The strict-winner certificates provide only a lower bound on strict winners, not a count of ties among the remaining rows. First-position argmax is not evidence of ties by itself. Saved decimal digits and observed binary32 representability do not expose internal-logit precision. This audit makes no generalization, causal, ranking-quality or calibration claim.

## Provenance and reproduction

Inputs and output files are SHA-256-addressed below / in `SHA256SUMS`; the local deliverables are set read-only (not an append-only or external authenticity guarantee). Input contents are not modified. `analyze.py` refuses to overwrite reports and permits output only inside the authorized audit directory. Reproduce with stdlib Python into a fresh child directory:

```sh
python3 /Users/destiner/Code/jeff/artifacts/data/d5-20261111T161610Z/fit-audit/analyze.py --output /Users/destiner/Code/jeff/artifacts/data/d5-20261111T161610Z/fit-audit/reproduction-new
```

| Input | Bytes | SHA-256 |
|---|---:|---|
| before: `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/fit-before.jsonl` | 574608 | `d13d8602294732339056781f1148426be1ef3003b9b8ce9bc833142ecdd83312` |
| after: `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/fit-after.jsonl` | 574021 | `a099822f30a234b0b3d2ff588888d712897bf5b1af4cbb878369cc23e619ca84` |
| receipt: `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/training/receipt.json` | 9478378 | `893c6a1b154734133d49ce41036a05bef2b5830c3615070b3547d56aebff1657` |
| schedule: `/Users/destiner/Code/jeff/artifacts/model/m6-qwen-20261111-01/train-audit/schedule.jsonl` | 3124848 | `7fa68f68c5cab98d23af8d9e9be8c305b74e30a588eb68eea6e98f783a2418e8` |

Analyzer SHA-256: `9d9cdddf4a1e22a103f81f1707c73f9e449179a06881ac7d60bacf6556b89aa5`.

All detailed limitations:
- Full probabilities and logits were not retained. Actual Brier, entropy, top-two margin and exact ties cannot be computed.
- Target p is approximately exp(-stored CE), conditional on the recorded unsmoothed categorical CE interpretation. It is not a separately retained probability.
- Stored decimal CE precision and binary32 representability do not establish precision or tiedness of unretained internal logits.
- Exact saved-float comparisons are arithmetic facts, not infinite-precision or internal-logit equality tests.
- Different target p from 1/k rules out exact uniformity for that row under the CE interpretation; equality would not prove full uniformity for k>2.
- No probabilities from different TRAIN records are combined into a reconstructed vector. Equal target p never implies equal non-target probabilities.
- Position-zero argmax alone does not prove ties. A correct argmax with target p > 0.5 certifies a strict winner under the CE interpretation, not the remaining tie count.
- TRAIN fit is descriptive agreement with saved labels, including teacher labels; not independent correctness, generalization, calibration or a causal account of performance/ranking.
