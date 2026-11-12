# P11 — local portable M9 runtime record

P11 packages the fixed M9 twelve-epoch encoder and records offline installation plus installed CPU execution on exactly three fixed TRAIN cases. This is runtime evidence, **not quality certification, calibration, default selection or promotion**. This publication reads existing metadata only; it adds no execution or scoring and changes no evidence.

## Recipient handoff

The actual durable local delivery is [/Users/destiner/Code/jeff/artifacts/lead/night-20261112/local-reference/](/Users/destiner/Code/jeff/artifacts/lead/night-20261112/local-reference/). Start with its existing [user README](/Users/destiner/Code/jeff/artifacts/lead/night-20261112/local-reference/README.md), not this historical execution report. Infra's public message `592af6ac-5b2b-4fff-a9d1-f1c6c25db9e8` identifies this location; [delivery metadata](/Users/destiner/Code/jeff/artifacts/lead/night-20261112/local-reference/delivery.json) and [source map](/Users/destiner/Code/jeff/artifacts/lead/night-20261112/local-reference/source-map.json) bind the copies. It is a local path, not a hosted download or public release.

The README tells the recipient to preserve the archive, extract into a new writable directory, and follow the preserved recipient addendum with explicit relocated `KIT`, external compatible `PYTHON`, and separate new writable `WORK`/venv/output paths. Requires CPython 3.12 with venv/ensurepip on macOS arm64; native wheel tags require macOS >=14. Actual observation was CPython 3.12.16/macOS 26.7.1, **not macOS14 or another-host execution**. Python, a working environment and caches are not bundled. Pip offline flags alone are not OS denial; the historical sandbox has stage-specific absolute paths and must not be blindly reused. Old “future/unverified” instructions predate the successful smoke receipt; unused budget does not authorize a replay.

## Exact integrity references

Hashes below are transcribed from existing receipts, not fresh archive/weight hashing. Machine-readable index: [p11-m9-20261112-01.json](../../manifests/releases/p11-m9-20261112-01.json).

| Object / link | SHA256 |
| --- | --- |
| [Durable archive](/Users/destiner/Code/jeff/artifacts/lead/night-20261112/local-reference/jeff-p11-m9-offline-macos-arm64-py312.tar.gz), 255,928,739 bytes | `5e4a0cc8b1d5b69f8a33edd026be64ab3c854e699b79773a6d81b1e1e29e87a2` |
| [Outer inventory](/private/tmp/jeff-p11-20261112-01/kit/inventory.json) | `6d5c2102070eebf4a6ca647c9f3b70adbbe999881833b88e8e66e14a20bd7153` |
| [Inner manifest](/private/tmp/jeff-p11-20261112-01/kit/m9-bundle/manifest.json) | `878edf5360827eb050523ee4fb7bd977cf806cc29908a0852efed0c98552b87e` |
| [Three-case comparison binding](/private/tmp/jeff-p11-20261112-01/kit/train-comparison-binding.json) | `1873ff67543dded71dfefc6d7ae829a739af06ce97a027d8c848ce15b07bec73` |
| [Successful parent](/private/tmp/jeff-p11-20261112-01/smoke-run-02/parent.json) | `25d4d517fc104e295a123e148621313ef639e92745559d5c10f2d190fe221c6f` |
| [Successful child](/private/tmp/jeff-p11-20261112-01/smoke-run-02/child.json) | `d1cd49de1b89e223f6f4122992271c846e18881a7e3355fe7c222345666a2447` |
| [Model success/resource return](/Users/destiner/Code/jeff/artifacts/model/night-20261112/p11-success-return.json) | `44f6ab636f0b4a718cea67d653c011d871c5cebc3631bb413fa82f30bd191bd7` |
| Durable user README (above) | `00c6aa766d71dc710e565e40ccb0fd3e9098bcff3bbbc315a17dbfc41910de5c` |
| Durable source map (above) | `c6bae7bd7afecc51e72a74cfc8d2715b88888acc7c7057801249104cd994392f` |

Canonical release evidence root: [/Users/destiner/Code/jeff/artifacts/release/p11-m9-20261112-01/](/Users/destiner/Code/jeff/artifacts/release/p11-m9-20261112-01/). Its [execution handoff](/Users/destiner/Code/jeff/artifacts/release/p11-m9-20261112-01/execution-0152/README.md) is historical packaging evidence, not the current recipient guide. Outside-stage [packaging receipt](/private/tmp/jeff-p11-20261112-01/final-receipt.json) predates inference and correctly says inference false at that stage; later receipts supplement, not rewrite it.

## Failure, repair and observed execution

Original installation plumbing failures remain in `kit/evidence/install-failed-attempt-{1,2}/`: restricted root metadata caused SIGABRT; a guessed nonexistent HF-cache path then caused ENOENT. The final offline install retained receipts and OS-denial preflights, without an unsandboxed fallback. Installation alone was never inference proof.

[Smoke01](/private/tmp/jeff-p11-20261112-01/smoke-run-01/parent.json) failed **after tokenizer/checkpoint loading and before any forward**: `torch.ops` exposed a synthetic `_ops.py` filename rejected by physical-origin checking. Native elapsed 7.68s, conservative charge9s (parent supervision elapsed7.663261s). This was **not zero-load** and is not erased by the later success.

The [explicit preparation02 repair](/Users/destiner/Code/jeff/artifacts/release/p11-m9-20261112-01/smoke-preparation-02/README.md) treats only exact `torch.ops` and `torch.classes` virtual namespaces, with exact defining-class and singleton identity, class/instance synthetic filename checks, and installed `_ops.py`/`_classes.py` definer origins. No blanket Torch, namespace or relative-filename exemption. Other physical-origin checks, scorer, cap256, temperature1, CPU, batch1, inputs and comparison criteria remained fixed. Both one-shot latches and the old failure remain.

Smoke02: native elapsed1.90s, charge3s (parent1.879783708s), exit0, exactly three completed native TRAIN classifier calls. Deterministic selection was minimum canonical ID per intent/sentiment/rule_application over pinned M9 TRAIN shards, not outcome filtering:

| Fixed TRAIN ID | Option-aligned maximum probability difference |
| --- | ---: |
| `data:pilot-v1:intent:g01:r01` | `9.968061931431293e-10` |
| `data:pilot-v1:sentiment-r2:g01:r01` | `2.7284841053187847e-11` |
| `data:pilot-v1:rule_application:g01:r01` | `5.21540641784668e-7` |

All three satisfy <=1e-5 **and identical complete exact-maximum top sets** against retained vectors. These are existing comparisons, not new scores. Model independently recorded comparison/closure. Aggregate **two actual loads, three productive forwards, 12/120s charged**, process group absent and slot returned; closed, unused108s not authority.

## Qualifications retained

- 1338 physical module-origin records plus exact virtual-definer records are not all-native-binary/dynamic-library/interpreter provenance. Fileless modules remain disclosed in child metadata.
- Read-only files0444/directories0555 protect against accidental editing; not WORM, signatures or authenticity guarantees.
- Recipient addendum corrects the already-shipped tqdm `LICENCE` inventory omission. Supplemental tokenizers source license is not complete Rust/vendor attribution, reproducible wheel-source proof or blanket redistribution/legal clearance. Project/publication rights remain unresolved; local handoff only.
- Three TRAIN cases do not certify all inputs, relocation, other hosts/platforms, held-out quality or calibrated probabilities. Known M9 rule-fitting/transfer and probe/source regressions remain; this runtime publication does not reevaluate or promote M9.
- No evidence or executed tree was modified. This bounded publication performs no model/tokenizer imports, payload/weights/archive reads, inference, scoring, network, tests or linting. Only the separately required offline package build accompanies the documentation commit.
