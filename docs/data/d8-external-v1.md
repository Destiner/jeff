# D8: source-preserving external evaluation populations

Released 2026-11-12 at05:42:20UTC; actual-byte/membership validation completed05:43:46UTC. **Evaluation only: both populations and all derivatives are permanently excluded from training.** No training validator, family enum or final-storage guard was widened.

| Population | Split | COPA | WinoGrande | Total |
| --- | --- | ---: | ---: | ---: |
| Exploration | validation |100|100|200|
| Sealed confirmation | final |100|100|200|

The families are `commonsense_causal_choice` and `coreference_cloze`. These operational source/task formats differ from Jeff's explicit fine-tuning families; they are not disjoint cognitive faculties or proof of absence from backbone pretraining/instruction tuning. No model quality or calibrated/general-purpose capability is claimed by this data release.

## Canonical artifacts and access

Paths below are relative to `/Users/destiner/Code/jeff/artifacts`:

| Phase | Canonical manifest | SHA256 |
| --- | --- | --- |
| Exploration | `data/d8-external-v1/manifest.json` | `69851eb2ac3960dc4b76ddab662ab5c7f246c5b837c5ba2b60ce7cb8e4166454` |
| Confirmation | `evaluation/final/e13-external-v1/data/release-v1/manifest.json` | `3a02e3269441e3970df18a974ab933b0ee64c80b9b5507f7a5b3264373bb8079` |

Byte-identical metadata mirrors are `manifests/data/d8-external-exploration-v1.json` and `manifests/data/d8-external-confirmation-v1.json`. They contain paths/hashes, not case payloads, and do not grant access to protected references.

Each canonical directory has two native reference shards, `selection.json`, `selection-accounting.json` and `source-audit-receipt.json`. The manifests are separate; exploration stays outside final. Every row retains `provenance.kind=public_dataset`, `label_basis=source_label`, and `usage=validation_only_never_train`.

These are **labeled references, not inference inputs**. Evaluation alone strips labels/provenance and produces native/reversed consumer inputs. Model/Runtime require those exact inputs and a separately scheduled actual-count grant, not a reference manifest or an assumed quota. Confirmation references/labels are restricted to authorized Data/Evaluation construction custody and must not guide recipes before the locked protocol permits them. Publication itself authorizes neither exploration nor confirmation inference.

The explicit D8 exception covers only the new `evaluation/final/e13-external-v1/data/` child. Old final24 and other protected Evaluation inputs remain outside Data's scope. Ordinary `jeff.data.validate` deliberately rejects final storage and these non-training families; do not relax it or pass these manifests to training. Frozen v2/M7, D3 and the unreleased D7 draft remain unchanged.

## Sources and fidelity

Use [Research's source/rights assessment](../research/external-family-sources.md) and [Evaluation's protocol](../evaluation/e13-external-protocol.md), including the later cohort-v2 treatment. Native source train partitions do not authorize Jeff training.

- **COPA original:** author archive at Git revision `14496936a3bed7b386aa8f517656d6f91e3fa77a`, 109432bytes, SHA256 `5145348834d2081ad90da0397d1db3d70fa044e506bd8ce224194d24b04cdbbe`. Native500dev→exploration,500test→confirmation; original public gold, not hidden/dummy SuperGLUE test targets. BSD-2-Clause author-package grant. Attribution/notices and native item/gold associations are retained.
- **WinoGrande1.1:** official archive, GCS generation1600272206460138,3395492bytes, SHA256 `3619ab104d8be2977b25c90ff420cb42d491707dcc75362a1e5d22bc082b7318`. Only9248debiased train→exploration and1267dev→confirmation. Dataset README CC BY2.0, not the code's Apache license. No public test dummy labels or guessed qID-prefix twin relations.
- **SocialIQA2019:** all35364native contexts remain grouping connectors, but every representative is quarantined with null target index. The exact case-sensitive prerequisite-question template matched185train/0dev; independent target-mapping proof remained unresolved. No template expansion, guessed labels or forced third family. Original native label associations are retained as evidence, not converted into eligible targets.
- **HellaSwag:** held for concrete access/text-rights issues; no mirror workaround or downloaded content.

Only fixed task questions were added for COPA/Wino; native words, facts, Unicode/whitespace, options/order and labels were preserved. Independent source parsing checked all46879inventory records across six pools against the pinned archives, including exact COPA ID/gold joins and Wino label agreement, with no omitted/duplicated locators or native-field mismatch. That establishes mechanical fidelity, **not semantic correctness of public gold**. A separate12-presentation rendered-construction check is retained under Data/Evaluation custody; it is not candidate-model performance or independent human ground truth.

Publisher grants support the authorized local assessment with attribution and usage qualifications. They are not blanket upstream chain-of-title/legal clearance or authorization to redistribute a dataset publicly. Frozen archives, publisher evidence, notices and citations remain in the source artifacts. No downloaded archive code was executed.

## Prospective grouping and selection

Evaluation froze the scientific method at01:13:19.807719UTC, before selection or external predictions: `evaluation/e13-phase-freeze-v1/plan.md`, SHA256 `bb3ed4770d991f89faeaad6aca077c74ffdcc6065d7dbdc9eb8abe491c2fa5d2`. Subsequent explicit Social quarantine narrows source eligibility; it does not invent a third family.

Grouping operates on all native contexts, including ineligible connectors, across sources and phases. Group-only normalization is NFKC/casefold/Unicode-whitespace collapse with maximal Unicode-alphanumeric tokens; rendered output is never normalized. Exact context/input relations, the common `10*intersection >= 7*max(token-set lengths)` relation, and the two frozen Wino option-pair/symmetric-token-masking relations form complete transitive components. Cross-phase/cross-family components and genuine exact-input conflicting target texts are quarantined. Labels do not enter rank identities, similarities or balancing.

The first complete exact run retained46879nodes/43537components;34389components were quarantined (reason counts overlap). Postgroup eligible groups were COPA482exploration/479confirmation and Wino7206/981. These detected lexical/provenance components are not statistically independent sources or semantic-equivalence guarantees: both undermerging and transitive overmerging remain possible.

Seed `jeff-unseen-night-20261112-v1`, native input-only identities and all-member component identities determine one representative/group and fixed ranks. Exactly200representatives per surviving phase/family cell formed the immutable800case token pool. The exact algorithm completed only after a prospective computational-bound amendment; earlier failed/incomplete grouping roots are retained and never consumed as completed outputs. No threshold, seed, template, connector or representative change was used to force quotas.

Runtime's one completed actual tokenizer/case pass checked800native plus800reversed presentations:3200complete encoder text pairs and1600decoder prompts through the original pinned renderers/tokenizers, without truncation, weights, models or forwards. All800pairs fit both encoder256 and decoder1024 limits; maxima54/89tokens. Thus final selection is exactly **ranks1–100 per cell**:400selected,400passing beyond the fixed cap,0ineligible/overflow/shortfall. No refill or alternate member was needed or authorized.

Five failed native startup/loader attempts and prepared-but-unexecuted05 remain preserved. Actual successful07 parent time6.101216292s; cumulative native parent time20.819555624/180s, peak native RSS477200384B. Torch definitions were imported; this was not Torch-free. Python file logs are incomplete for native opens; scope is qualified by the retained Seatbelt policy. RSS is native child high-water/sample-group evidence, not a kernel allocation hard limit. Unused time grants no further pass.

## Actual release evidence

`data/d8-20261112T004100Z/publication-preparation/` contains the frozen publisher, owner source review, accepted admission, first execution receipt and actual released-population validation. Publisher SHA256 `2b5a1ddd552e325555a4d2aa3f9a9f21554210682343fd79eaff7394091822a9`; its first execution succeeded without a population retry. All400released reference lines are byte-for-byte copies of the frozen candidate references, with400unique IDs/components and0cross-phase ID/group collisions. All12released files are hashed and read-only. No target-position frequencies or confirmation correctness/example summaries were computed for this release report.

Evaluation's `evaluation/e13-token-binding-v1/eligibility-adoption-receipt.json` records20859passed checks on actual audit/source/input/pair/coverage evidence. Model independently closed the successful reservation. These reviews did not duplicate tokenization. Data then independently validated released bytes, exact original-rank membership, separate splits, provenance and exclusion markers. Evaluation owns subsequent materialization/input verification, exposure records, predictor lock and scoring; those are not implied completed by this document.

Detailed delivery: `handoffs/data/026-d8-populations-released-evaluation.md`; safe aggregate notice `027-d8-safe-release-status.md`. The candidate index remains explicitly a historical pre-audit pool, not silently relabeled as the release. All earlier failed/revised construction evidence is retained.

Additional external actual/pending spend **£0/£0**; existing agent-session billing was not independently metered. No software tests/lint, Data model/tokenizer load, training or inference. This delivery adds metadata/documentation only; it does not change package behavior or training permissions.
