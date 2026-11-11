# D3 seen-mechanism / new-policy diagnostic

96 cases, 48 correlated two-case policies, eight intentionally seen mechanisms; originals only, native 256. Never pooled with v2/probes. No threshold or promotion.

All labels: rule_verified/programmatic. Same openai/gpt-sol author/reviewer alias (immutable revision unknown), not independent ground truth. Initial review 31/32; final-content review 64/64 across 40 policies only. Residual hints are a separate authoring quality: FIFO fewest-zero 6/12; rates slot-two 6/12; scheduling non-none 11/12; easy boundary cases. These are not measured model improvements.

Exact metrics, all 48 policy results, reliability bins, macro undefined/infinity accounting and paired results: report.json. Raw record diagnostics and all pairwise comparisons: comparison.json. Coverage/conditional quality definitions: shared-report.md.

## Overall

| Predictor | Unit | Coverage | Agreement | Loss | Brier | ECE | Failures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minilm_start | all | 96/96 | 27/96 | 1.316860 | 0.7297168837483841 | 0.010136262700749799 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | all | 96/96 | 31/96 | 1.342824 | 0.7431145660641721 | 0.026157783617935575 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | all | 96/96 | 30/96 | 1.347340 | 0.7487295618884601 | 0.052032901271562175 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | all | 96/96 | 26/96 | 1.355202 | 0.752642004045784 | 0.06381823368344534 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | all | 96/96 | 27/96 | 1.317371 | 0.7300347222222222 | 0.01128472222222221 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | all | 96/96 | 24/96 | 1.319115 | 0.7309119411011653 | 0.033143208431488824 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |

## All eight mechanisms (12 cases / 6 policies each)

| Predictor | Unit | Coverage | Agreement | Loss | Brier | ECE | Failures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| minilm_start | packs | 12/12 | 3/12 | 1.314182 | 0.7288852290304008 | 0.021991736135725748 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | rates | 12/12 | 3/12 | 1.195292 | 0.6946731874614502 | 0.05732403827699367 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | coordinates | 12/12 | 3/12 | 1.386724 | 0.7502151919585246 | 0.0010584720199820485 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | cooldown | 12/12 | 3/12 | 1.386081 | 0.7498933943135055 | 0.0003554920396151573 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | lexicographic | 12/12 | 5/12 | 1.382846 | 0.7482762781531632 | 0.1644635989032448 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | fifo | 12/12 | 4/12 | 1.097704 | 0.6660612947860772 | 0.0008229480809355816 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | discount | 12/12 | 3/12 | 1.385567 | 0.749636347866187 | 0.0006845382138006006 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_start | rounding | 12/12 | 3/12 | 1.386480 | 0.7500941464177644 | 0.001136272530193605 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | packs | 12/12 | 6/12 | 1.261849 | 0.7121825980466822 | 0.258515347463956 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | rates | 12/12 | 3/12 | 1.230830 | 0.7203408200537657 | 0.08842412629741049 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | coordinates | 12/12 | 3/12 | 1.372659 | 0.7437727174414239 | 0.03194446679663032 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | cooldown | 12/12 | 1/12 | 1.597780 | 0.8647668319706764 | 0.32391976972150743 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | lexicographic | 12/12 | 5/12 | 1.397716 | 0.7558812530289698 | 0.13837594952979654 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | fifo | 12/12 | 6/12 | 1.003416 | 0.6000623096010801 | 0.0940087680122399 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | discount | 12/12 | 5/12 | 1.369773 | 0.739834561186428 | 0.07483133914546339 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| minilm_trained | rounding | 12/12 | 2/12 | 1.508566 | 0.808075437184351 | 0.20285980421667416 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | packs | 12/12 | 5/12 | 1.276753 | 0.706531928249026 | 0.1254758999828232 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | rates | 12/12 | 6/12 | 1.174383 | 0.6811245564475031 | 0.1749761800516445 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | coordinates | 12/12 | 2/12 | 1.382215 | 0.7484117983223885 | 0.09651182882700474 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | cooldown | 12/12 | 2/12 | 1.416606 | 0.7667281664509837 | 0.11468489447549604 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | lexicographic | 12/12 | 5/12 | 1.363521 | 0.7384426214776134 | 0.12634484773022192 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | fifo | 12/12 | 2/12 | 1.114671 | 0.6772839840646538 | 0.1731675490676757 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | discount | 12/12 | 6/12 | 1.355092 | 0.7320294023348133 | 0.2125376626630835 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_start | rounding | 12/12 | 2/12 | 1.695480 | 0.9392840377606987 | 0.31501754326278325 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | packs | 12/12 | 4/12 | 1.291678 | 0.7167276077502861 | 0.051883492700606104 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | rates | 12/12 | 3/12 | 1.202002 | 0.6993598922182951 | 0.06594553417569987 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | coordinates | 12/12 | 3/12 | 1.384492 | 0.749114103821673 | 0.003736514550693737 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | cooldown | 12/12 | 1/12 | 1.608404 | 0.8834873448648465 | 0.3333602988777607 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | lexicographic | 12/12 | 2/12 | 1.378059 | 0.7456184548543732 | 0.10499248417230853 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | fifo | 12/12 | 7/12 | 1.092312 | 0.6624592621045161 | 0.24358091670998588 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | discount | 12/12 | 5/12 | 1.381418 | 0.7477577508006171 | 0.15408295826234203 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| msmarco_trained | rounding | 12/12 | 1/12 | 1.503249 | 0.8166116159516642 | 0.2483381145796002 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | packs | 12/12 | 4/12 | 1.314374 | 0.7291666666666666 | 0.0625 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | rates | 12/12 | 2/12 | 1.194506 | 0.6944444444444445 | 0.13888888888888887 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | coordinates | 12/12 | 3/12 | 1.386294 | 0.75 | 0.0 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | cooldown | 12/12 | 5/12 | 1.386294 | 0.75 | 0.16666666666666669 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | lexicographic | 12/12 | 4/12 | 1.386294 | 0.75 | 0.08333333333333331 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | fifo | 12/12 | 4/12 | 1.098612 | 0.6666666666666666 | 0.0 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | discount | 12/12 | 2/12 | 1.386294 | 0.75 | 0.08333333333333334 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| uniform | rounding | 12/12 | 3/12 | 1.386294 | 0.75 | 0.0 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | packs | 12/12 | 3/12 | 1.317745 | 0.7325003910690423 | 0.03955998876825362 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | rates | 12/12 | 2/12 | 1.194506 | 0.6944444444444445 | 0.13888888888888887 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | coordinates | 12/12 | 3/12 | 1.372161 | 0.7432166568547386 | 0.019129237515657427 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | cooldown | 12/12 | 1/12 | 1.417308 | 0.7661838139706206 | 0.20015963762516248 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | lexicographic | 12/12 | 4/12 | 1.386294 | 0.75 | 0.08333333333333331 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | fifo | 12/12 | 7/12 | 1.083803 | 0.6565891704075008 | 0.23942130864630146 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | discount | 12/12 | 2/12 | 1.386892 | 0.7503121580714452 | 0.09102663243098916 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |
| lexical | rounding | 12/12 | 2/12 | 1.394210 | 0.7540488939915302 | 0.09913592420259362 | {'missing': 0, 'invalid': 0, 'duplicate': 0} |

## Equal-unit macros

Strict mean is null when any unit is undefined; positive-infinite loss is separately flagged. Finite-only means are explicitly conditional, not the headline macro.

### minilm_start
```json
{
  "equal_policy_macro": {
    "agreement_valid": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "agreement_all": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "coverage": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7297168837483841,
      "finite_only_mean": 0.7297168837483841
    },
    "ece": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2786179899173031,
      "finite_only_mean": 0.2786179899173031
    },
    "log_loss": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3168596880207917,
      "finite_only_mean": 1.3168596880207917
    }
  },
  "equal_mechanism_macro": {
    "agreement_valid": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "agreement_all": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "coverage": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7297168837483842,
      "finite_only_mean": 0.7297168837483842
    },
    "ece": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.0309796370250614,
      "finite_only_mean": 0.0309796370250614
    },
    "log_loss": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3168596880207917,
      "finite_only_mean": 1.3168596880207917
    }
  }
}
```

### minilm_trained
```json
{
  "equal_policy_macro": {
    "agreement_valid": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3229166666666667,
      "finite_only_mean": 0.3229166666666667
    },
    "agreement_all": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3229166666666667,
      "finite_only_mean": 0.3229166666666667
    },
    "coverage": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7431145660641721,
      "finite_only_mean": 0.7431145660641721
    },
    "ece": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3161334795936767,
      "finite_only_mean": 0.3161334795936767
    },
    "log_loss": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3428235283463337,
      "finite_only_mean": 1.3428235283463337
    }
  },
  "equal_mechanism_macro": {
    "agreement_valid": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3229166666666667,
      "finite_only_mean": 0.3229166666666667
    },
    "agreement_all": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3229166666666667,
      "finite_only_mean": 0.3229166666666667
    },
    "coverage": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7431145660641721,
      "finite_only_mean": 0.7431145660641721
    },
    "ece": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.15160994639795977,
      "finite_only_mean": 0.15160994639795977
    },
    "log_loss": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3428235283463335,
      "finite_only_mean": 1.3428235283463335
    }
  }
}
```

### msmarco_start
```json
{
  "equal_policy_macro": {
    "agreement_valid": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3125,
      "finite_only_mean": 0.3125
    },
    "agreement_all": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3125,
      "finite_only_mean": 0.3125
    },
    "coverage": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7487295618884601,
      "finite_only_mean": 0.7487295618884601
    },
    "ece": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2989692653155895,
      "finite_only_mean": 0.2989692653155895
    },
    "log_loss": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.347340246736404,
      "finite_only_mean": 1.347340246736404
    }
  },
  "equal_mechanism_macro": {
    "agreement_valid": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3125,
      "finite_only_mean": 0.3125
    },
    "agreement_all": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.3125,
      "finite_only_mean": 0.3125
    },
    "coverage": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7487295618884601,
      "finite_only_mean": 0.7487295618884601
    },
    "ece": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.1673395507575916,
      "finite_only_mean": 0.1673395507575916
    },
    "log_loss": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.347340246736404,
      "finite_only_mean": 1.347340246736404
    }
  }
}
```

### msmarco_trained
```json
{
  "equal_policy_macro": {
    "agreement_valid": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2708333333333333,
      "finite_only_mean": 0.2708333333333333
    },
    "agreement_all": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2708333333333333,
      "finite_only_mean": 0.2708333333333333
    },
    "coverage": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.752642004045784,
      "finite_only_mean": 0.752642004045784
    },
    "ece": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.32940256326437534,
      "finite_only_mean": 0.32940256326437534
    },
    "log_loss": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3552017711379147,
      "finite_only_mean": 1.3552017711379147
    }
  },
  "equal_mechanism_macro": {
    "agreement_valid": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2708333333333333,
      "finite_only_mean": 0.2708333333333333
    },
    "agreement_all": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2708333333333333,
      "finite_only_mean": 0.2708333333333333
    },
    "coverage": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.752642004045784,
      "finite_only_mean": 0.752642004045784
    },
    "ece": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.15074003925362464,
      "finite_only_mean": 0.15074003925362464
    },
    "log_loss": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3552017711379147,
      "finite_only_mean": 1.3552017711379147
    }
  }
}
```

### uniform
```json
{
  "equal_policy_macro": {
    "agreement_valid": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "agreement_all": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "coverage": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7300347222222222,
      "finite_only_mean": 0.7300347222222222
    },
    "ece": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.2890625,
      "finite_only_mean": 0.2890625
    },
    "log_loss": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3173705312616515,
      "finite_only_mean": 1.3173705312616515
    }
  },
  "equal_mechanism_macro": {
    "agreement_valid": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "agreement_all": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.28125,
      "finite_only_mean": 0.28125
    },
    "coverage": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7300347222222222,
      "finite_only_mean": 0.7300347222222222
    },
    "ece": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.06684027777777778,
      "finite_only_mean": 0.06684027777777778
    },
    "log_loss": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3173705312616515,
      "finite_only_mean": 1.3173705312616515
    }
  }
}
```

### lexical
```json
{
  "equal_policy_macro": {
    "agreement_valid": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.25,
      "finite_only_mean": 0.25
    },
    "agreement_all": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.25,
      "finite_only_mean": 0.25
    },
    "coverage": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7309119411011653,
      "finite_only_mean": 0.7309119411011653
    },
    "ece": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.26670978103230353,
      "finite_only_mean": 0.26670978103230353
    },
    "log_loss": {
      "units": 48,
      "finite_units": 48,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.31911496650676,
      "finite_only_mean": 1.31911496650676
    }
  },
  "equal_mechanism_macro": {
    "agreement_valid": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.25,
      "finite_only_mean": 0.25
    },
    "agreement_all": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.25,
      "finite_only_mean": 0.25
    },
    "coverage": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.0,
      "finite_only_mean": 1.0
    },
    "brier": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.7309119411011653,
      "finite_only_mean": 0.7309119411011653
    },
    "ece": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 0.11383186892639749,
      "finite_only_mean": 0.11383186892639749
    },
    "log_loss": {
      "units": 8,
      "finite_units": 8,
      "undefined_units": 0,
      "positive_infinity_units": 0,
      "status": "finite",
      "mean": 1.3191149665067599,
      "finite_only_mean": 1.3191149665067599
    }
  }
}
```

## Paired own-start → trained

### minilm_trained
```json
{
  "start": "minilm_start",
  "cases": {
    "total_cases": 96,
    "common_valid": 96,
    "unpaired": 0,
    "wins": 19,
    "losses": 15,
    "both_correct": 12,
    "both_wrong": 50
  },
  "full_policy_2_of_2": {
    "wins": 4,
    "losses": 3,
    "both_correct": 0,
    "both_wrong": 41,
    "incomplete": 0
  },
  "total_policies": 48,
  "per_mechanism": {
    "packs": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 6,
      "losses": 3,
      "both_correct": 0,
      "both_wrong": 3
    },
    "rates": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 2,
      "losses": 2,
      "both_correct": 1,
      "both_wrong": 7
    },
    "coordinates": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 3,
      "losses": 3,
      "both_correct": 0,
      "both_wrong": 6
    },
    "cooldown": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 0,
      "losses": 2,
      "both_correct": 1,
      "both_wrong": 9
    },
    "lexicographic": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 0,
      "losses": 0,
      "both_correct": 5,
      "both_wrong": 7
    },
    "fifo": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 4,
      "losses": 2,
      "both_correct": 2,
      "both_wrong": 4
    },
    "discount": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 4,
      "losses": 2,
      "both_correct": 1,
      "both_wrong": 5
    },
    "rounding": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 0,
      "losses": 1,
      "both_correct": 2,
      "both_wrong": 9
    }
  }
}
```

### msmarco_trained
```json
{
  "start": "msmarco_start",
  "cases": {
    "total_cases": 96,
    "common_valid": 96,
    "unpaired": 0,
    "wins": 15,
    "losses": 19,
    "both_correct": 11,
    "both_wrong": 51
  },
  "full_policy_2_of_2": {
    "wins": 5,
    "losses": 3,
    "both_correct": 0,
    "both_wrong": 40,
    "incomplete": 0
  },
  "total_policies": 48,
  "per_mechanism": {
    "packs": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 2,
      "losses": 3,
      "both_correct": 2,
      "both_wrong": 5
    },
    "rates": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 2,
      "losses": 5,
      "both_correct": 1,
      "both_wrong": 4
    },
    "coordinates": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 3,
      "losses": 2,
      "both_correct": 0,
      "both_wrong": 7
    },
    "cooldown": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 1,
      "losses": 2,
      "both_correct": 0,
      "both_wrong": 9
    },
    "lexicographic": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 0,
      "losses": 3,
      "both_correct": 2,
      "both_wrong": 7
    },
    "fifo": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 5,
      "losses": 0,
      "both_correct": 2,
      "both_wrong": 5
    },
    "discount": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 2,
      "losses": 3,
      "both_correct": 3,
      "both_wrong": 4
    },
    "rounding": {
      "total_cases": 12,
      "common_valid": 12,
      "unpaired": 0,
      "wins": 0,
      "losses": 1,
      "both_correct": 1,
      "both_wrong": 10
    }
  }
}
```

