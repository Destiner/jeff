# P12 — fixed frozen NLI adapter (source preparation only)

## Status and interpretation

This is **unexecuted source**, not runtime readiness or an evaluation result.
Only `src/jeff/runtime/nli_challenger.py`, `configs/runtime/p12-nli.json` and this
contract are owned by this preparation. No ML/tokenizer import, weight decoding,
installation, acquisition, inference, tests, lint, build, network or commit is
part of this pass. Independent source review and the parent's frozen binding,
Model slot and whole-process-group supervisor remain prerequisites.

This is a **practical frozen NLI baseline**, not a pure architecture ablation:
pretraining, NLI supervision, tokenizer and rendering differ from prior models.
Choice-normalized scores are not calibrated confidence. Declared MIT licensing
in the Research profile is not blanket clearance of upstream training sources.

## Immutable condition

- Only `MoritzLaurer/roberta-base-zeroshot-v2.0-c`, revision
  `d825e740e0c59881cf0b0b1481ccf726b6d65341`.
- Read in full and SHA-256 checked during source preparation:
  `/Users/destiner/Code/jeff/artifacts/research/r10-20261112T011854Z/source-profile-v1.json`,
  `619365c8a158b7270d6f4aa29cab9c32f4c283d934b777d38647637ad04e2441`.
- Native labels: `0=entailment`, `1=not_entailment`. Native two-logit classifier;
  no generation, prompt selection, fitted temperature, retries or fallback.
- Premise: `Context:\n{state}\n\nQuestion:\n{question}`.
  Hypothesis: `The correct answer is:\n{option_text}`. Here `\n` denotes an actual
  LF at rendering time, not backslash-n in the model input. Preserve source fields
  verbatim, including whitespace. IDs and labels are never model features.
- Native fast RoBERTa byte-level BPE, `add_prefix_space=false`, premise first,
  hypothesis second, native special tokens included. Complete pair cap **512**;
  no truncation, dropping or text normalization. Every pair is pre-tokenized
  before model construction. Any overflow stops before any model score, with
  counts/lengths and a reason but no text dump.
- Score each option as `z[0] - logsumexp(z[1:])`, then stable T=1 softmax across
  that decision's supplied options. Stdlib math readout, not another framework.
- FP32/MPS, four intra-op and four inter-op threads, eager built-in attention,
  four **decisions** per native batch. All their candidate pairs share one native
  forward, with padding only to that batch's longest complete pair. No canaries,
  implicit warm-up call, extra forward or CPU fallback.

## P7 workload identities

The frozen P7 binding SHA-256 is
`a49a0934ea45febea4817a1a602ca6391d608bfe518d6a39ae0125ab48224f69` at
`/Users/destiner/Code/jeff/artifacts/release/p7-m9-20261111-01/binding.json`.
Its input manifest is
`/Users/destiner/Code/jeff/artifacts/release/p6-m8-20261111-01/inputs.json`, SHA-256
`77c57b75b64a0b306c8c851bb2d3a023bddd5d237334cd288316013c26d2927a`.
Only those two metadata files were read during preparation, not dataset contents
or reference/label files.

| Suite (in this order) | Decisions | Input SHA-256 |
| --- | ---: | --- |
| v2-original | 300 | `2103447bf8fbca3b43c09b0506b943179e96f7e774d7ae8363eddbf940970917` |
| v2-reversed | 300 | `ba266b3b77896d77a453b095da485b569f0cde2238d94493e0a4bcfb704c92f1` |
| probes-paired | 24 | `051a72824b9954b8a026507fe4819c37aefc0e72ec9e3af1d16c1c279f1932d6` |

Do not reverse the already-paired probes again. Exact completion requires
624 written decisions, 2,390 candidate pairs/probabilities and **156 attempted =
completed native forwards** (75 + 75 + 6), zero startup forwards. Identity checks
are per suite because original/reversed decisions intentionally share IDs.
Runtime accepts decision-only v0.1 rows and never opens a reference dataset.

## New frozen binding: `p12.binding.v1`

Parent/acquisition owner supplies a **new, immutable JSON file**. This adapter
neither downloads assets nor writes acquisition code. Do not reuse a prior
execution binding as if it describes P12. All filesystem paths below are absolute.
Duplicate JSON keys and nonfinite JSON constants are rejected.

Top-level fields, exactly:

| Field | Required value/shape |
| --- | --- |
| `schema_version` | `p12.binding.v1` |
| `model_id`, `revision` | Exact identities above |
| `model_dir` | Local directory containing exactly the eight allowed assets below; no cache directory or extra files |
| `research_profile` | File pin for the exact Research profile above |
| `p7_binding` | File pin for the exact P7 binding above |
| `input_manifest` | File pin for the exact P7 input manifest above |
| `assets` | Object keyed by each of the eight allowed public asset names |
| `sources` | Object with exactly the six source pins below |
| `versions` | Object with exactly the six installed-distribution version strings below |

A **file pin** has exactly `{"path": ABSOLUTE_PATH, "sha256": HEX_SHA256,
"bytes": INTEGER_SIZE}`; placeholder names in this description are not values to
copy. The source keys are:

- `adapter`: this `nli_challenger.py` in the execution worktree;
- `recipe`: that worktree's `configs/runtime/p12-nli.json`;
- `pyproject`: that worktree's `pyproject.toml`;
- `uv_lock`: that worktree's `uv.lock`;
- `roberta_model`: installed Transformers `modeling_roberta.py` defining the
  built-in `RobertaForSequenceClassification`;
- `roberta_tokenizer`: installed Transformers `tokenization_roberta_fast.py`
  defining the built-in `RobertaTokenizerFast`.

Pin actual installed source files without importing ML during preparation.
Runtime hashes every source before ML imports, then checks that the actual
built-in classes come from those pinned paths. Version keys are exactly `torch`,
`transformers`, `tokenizers`, `safetensors`, `huggingface-hub`, `numpy`, each equal
to the installed distribution version. Version strings are evidence, not an
independent lockfile/package integrity attestation. Python/platform and selected
non-secret runtime environment variables are also receipted.

Each `assets` entry has exactly `{"url": PUBLIC_PINNED_URL, "sha256": ACTUAL_SHA256,
"bytes": ACTUAL_SIZE}`. Allowed names are `README.md`, `config.json`,
`merges.txt`, `model.safetensors`, `special_tokens_map.json`, `tokenizer.json`,
`tokenizer_config.json`, `vocab.json`. The exact URL, published size and upstream
Git blob identity or LFS SHA-256 come from the frozen Research profile. Every
asset is hashed locally before importing torch or loading tokenizer/model; small
files additionally match their upstream Git blob SHA-1. Weights must match LFS
SHA-256 `3568bb04b99e48d6e3086656534304644f3608312aa96c52edca7e6a7eeb0336`
and exactly 249,318,428 bytes. No `training_args.bin`, Python modeling files,
`.gitattributes`, alternative checkpoint, shard, or new format is accepted.

`check_assets` is a stdlib-only helper, with no ML imports. It verifies actual
config architecture/dimensions/label maps, native tokenizer metadata and no
`auto_map`. A bounded (at most 1 MiB) safetensors JSON header audit verifies every
actual tensor name, shape, F16 dtype, contiguous nonoverlapping offsets and file
extent, **124,647,170 parameters** (cap 150M), and weights under 600,000,000 bytes.
It decodes no tensor payload. Expected shapes are the built-in RoBERTa-base
classifier shapes, not a replacement backend or checkpoint format.

The sole model load uses existing `AutoModelForSequenceClassification` and
`AutoTokenizer`, local-only, `trust_remote_code=false`, safetensors-only weights.
All four HF diagnostics (`missing_keys`, `unexpected_keys`, `mismatched_keys`,
`error_msgs`) must exist and be empty. Loaded named-parameter shapes/counts and
actual FP32 dtype are rechecked, then every parameter must actually be on MPS.
Tokenizer class/fast byte-level BPE/prefix setting and native labels are checked
again after construction. Any mismatch stops, with no repair or fallback.

## Future execution boundary (not executed here)

One fresh process only, under the parent's Model reservation and external
whole-process-group supervisor:

```sh
python -m jeff.runtime.nli_challenger predict \
  --binding /absolute/path/to/NEW-frozen-binding.json \
  --output-dir /absolute/path/to/NEW-output-directory
```

Parent provides an empty/fresh HOME, isolated offline caches, the existing pinned
ML environment and import path; no `uv` dependency resolution/network step is
implied by this command. Before process launch set `HF_HUB_OFFLINE=1`,
`TRANSFORMERS_OFFLINE=1`, `HF_DATASETS_OFFLINE=1`,
`PYTORCH_ENABLE_MPS_FALLBACK=0`, `TOKENIZERS_PARALLELISM=false`.
The adapter requires those settings rather than silently changing them. A fresh
HOME/cache and process-group isolation are **parent attestations**, not inferred
from those flags. Model scheduling covers tokenizer construction too.

The adapter cooperatively bounds preparation/loading/scoring at 480 seconds from
CLI initialization. Blocking imports/native calls cannot be preempted by Python
checks. **Parent must enforce an external whole-group wall limit including
startup and finalization, with termination grace inside the grant.** Never treat
the cooperative bound as proof of an external hard deadline.

Before/after loads and each native forward, sampled current/peak process RSS and
MPS driver allocation must each remain at most 8 GiB; estimated system headroom
must be at least 2 GiB. Headroom is macOS `vm_stat` (free + inactive pages), not
an allocation guarantee or swap-pressure audit. Driver values are samples, not
continuous peaks; RSS high-water is `getrusage` on macOS. Sampling itself checks
the clock. No memory reclaim trick, retry or CPU fallback is attempted.

## Outputs and failure evidence

A new directory is mandatory; files use exclusive creation. Successful suites
write `v2-original.jsonl`, `v2-reversed.jsonl`, `probes-paired.jsonl` in v0.1
prediction format with original IDs and original option order. Probabilities must
be finite, within [0,1], and sum to one. Entire logits batches must be finite
before that batch is written. Completed earlier batches are retained on failure;
partial outputs are never presented as a complete pass or silently retried.

`journal.jsonl` is fsynced before each tokenizer/model load attempt and each
native forward attempt, and after native completion/output batches. It records exact attempted/completed
counts, suite offsets, pair counts, timings and memory samples without task text.
The final `receipt.json` records status, failure code/type, pins, actual config,
serializer shapes/count, actual dependency versions, environment, timestamps,
token lengths/overflow count, written counts and output/journal byte sizes and
SHA-256. Caught failures and SIGTERM/SIGINT finalize partial evidence; arbitrary
library exception messages are suppressed to avoid text dumps. Files are made
read-only after finalization. The receipt does not hash itself; parent should
hash it externally.

SIGKILL, a second fatal OS failure or disk exhaustion cannot guarantee a final
receipt. Parent must retain the immutable binding, durable journal, raw process
exit/signal and external wall/resource receipt, including for killed or unstarted
attempts. There is a small unavoidable journal-to-call boundary: a signal or I/O
failure can occur after a durable attempt intent but before native entry. Counts
therefore mean recorded attempts, not proof that a native call entered GPU code.
There is no restart path.

## Concrete outstanding blockers

1. Acquisition owner's eight verified local assets and new frozen binding,
   including installed built-in source pins/version strings, are not supplied by
   this source change. Source eligibility is not local asset verification.
2. Independent review is still required. No syntax execution, build, ML import,
   tokenizer audit, load diagnostic or forward has been performed here.
3. Model activation, fresh-HOME offline launch and external group supervisor are
   parent-owned and must be frozen before execution. A nominal 480-second recipe
   does not establish those controls.
4. Actual full-pair fit, strict HF reload, FP32/MPS support, runtime/memory fit and
   exact output counts remain unknown until that sole authorized run. An overflow
   or other failed gate stops rather than changing the scientific condition.
5. Evaluation owns comparison/interpretation; no readiness, quality, calibration,
   promotion or pure architecture conclusion follows from source preparation.
