# P1 portable runtime delivery — 2026-11-11

## What actually shipped locally

Two immutable-by-convention directory bundles preserve existing checkpoint bytes and use the same Jeff wheel/loader. M2 is first; M3 compatibility is additional evidence, not model promotion. Large artifacts remain outside Git under:

`/Users/destiner/Code/jeff/artifacts/release/p1-20261111-01/`

| Candidate | Bundle | Checkpoint / inventoried payload files | Payload bytes | Whole directory bytes¹ |
| --- | --- | ---: | ---: | ---: |
| M2 | `m2-bundle/` | 8 / 16 | 92,001,155 | 92,008,828 |
| M3 | `m3-bundle/` | 7 / 15 | 92,000,837 | 92,008,797 |

¹ Sum of file lengths including manifest and sidecar; not filesystem allocated blocks. Approximately 87.75 MiB each, uncompressed. Completed files/directories are 0444/0555; reversible permissions are not WORM storage.

Each contains checkpoint, wheel, exact inventory/hash manifest, provenance, pinned requirements, three synthetic label-free decisions, install/run README, Apache-2.0 text, upstream model card and modification/rights notice. No training rows, dependency wheelhouse, credentials or author cache is bundled. The original checkpoints were not changed.

Trusted local manifest receipts (also committed verbatim as `manifests/releases/p1-{m2,m3}-20261111-01.json`):

```text
M2 manifest.json  1c1fc4bc742beb7ec396e5b6b51550df216d38a097b467b9ce3fe0aa4f190e59
M3 manifest.json  c7564f6c9f2edb0e44d0332ad51c16fedb3bc2042ec1137b75dcb249e724054f
Jeff wheel       191d6e3b8c051b6e5c21ab60b6d8733b563b2930c16d8a8bb1c4089773ec0e01
requirements     463e17a2f6f4bcecfb4dd0fd995d086083c25475be6379a90030f80c3c35636d
```

Wheel: `jeff-0.1.0-py3-none-any.whl`, 61,191 bytes, built with `uv build --no-sources` at runtime implementation commit `82c327a7ba6def23e77123f3e768b31255feb2b5`. Both bundle manifests separately record this code revision, exporter source hashes, upstream architecture/revision, training revision/config and dataset hash. Later support/docs commits are not misrepresented as the wheel's source revision. The final main merge is recorded in the completed Release handoff, avoiding a self-referential commit hash here.

## Actual external install and isolation

Copied bundles to `/private/tmp/jeff-p1-20261111-01/{m2,m3}-bundle` with normal file copying. Copied the resolved standalone Python distribution to `standalone-python/`, then created `isolated-venv/` with `include-system-site-packages=false`. Installed hash-pinned dependencies with `uv pip install --link-mode copy --only-binary :all: --require-hashes -r ...`, and the bundled wheel with `--no-deps`; not editable. Install commands were network-capable and used the package cache. **No fully offline installation claim.** The interpreter itself is an external prerequisite, not part of either bundle.

Measured host: Apple M5, 24 GiB unified memory, macOS 26.7.1 arm64. Runtime: CPython 3.12.16, Jeff 0.1.0, torch 2.15.0, transformers 4.57.6, tokenizers 0.22.2, safetensors 0.8.0, huggingface-hub 0.36.2, NumPy 2.5.4. Full installed distribution versions are in `manifests/releases/p1-runtime-20261111-01.json` and artifact `runtime-evidence/summary.json`.

Before each isolated load, an operational stdlib preflight confirmed permission denial for original home, original `AGENTS.md`, original model-cache directory, and a socket operation. The actual macOS sandbox profile denied **all network** and **all file reads under `/Users/destiner`**, while permitting writes only to this external stage and `/dev/null`. Thus the original checkpoint, checkout, user-site packages, and known original caches were unavailable, rather than merely unused by intention. The installed Jeff module resolved inside the external venv; Python's base and sys.path resolved outside the denied home.

Each process used a new empty HOME/HF/XDG/Torch cache, a deliberately constructed environment (no inherited tokens, proxy or Python paths), isolated Python `-I`, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, telemetry/implicit token disabled, explicit CPU, batch size 1, and two-thread OpenMP/MKL/vecLib limits. **All model cache inventories remained empty before and after every run.** M3 reused the external installed environment after M2, but had its own empty caches and fresh process; OS/library page caches were not flushed.

Existing CLI, as actually launched for M2 inside that environment:

```sh
/usr/bin/sandbox-exec -f /private/tmp/jeff-p1-20261111-01/evidence/offline.sb \
  /usr/bin/time -l /private/tmp/jeff-p1-20261111-01/isolated-venv/bin/python \
  -I -m jeff.model.predict \
  --checkpoint /private/tmp/jeff-p1-20261111-01/m2-bundle/checkpoint \
  --input /private/tmp/jeff-p1-20261111-01/m2-bundle/demo/inputs.jsonl \
  --output /private/tmp/jeff-p1-20261111-01/evidence/m2-isolated/predictions.jsonl \
  --device cpu --batch-size 1
```

Exact `argv`, clean environment and CWD for every invocation: `runtime-evidence/{m2,m3}-{isolated,source}/invocation.json`. Profile SHA-256: `c04232f51b00f4e5c697996b41e953844e50d4ede57c58b8e6ad6babcf792d9f`. The existing loader additionally uses local-only safetensors/tokenizer loading and no remote custom code. Sandbox enforcement is macOS-specific; no other platform/accelerator is claimed.

## Real inference results

Model explicitly granted the exclusive local ML slot 11:35–11:45 UTC, at most four sequential CPU invocations and no starts after 11:43. All four completed by **11:41:08Z**, and Release immediately returned the slot in a public receipt. No MPS, training or competing model load was used.

| Candidate / process | Coverage | Total process wall | CLI load + predict² | Lifetime max RSS³ | Source equivalence |
| --- | --- | ---: | ---: | ---: | --- |
| M2 isolated bundle | 3/3 decisions, 8/8 options | 9.8904 s | 0.143 s | 421,396,480 B | Byte-identical to source |
| M2 source comparison | 3/3 decisions, 8/8 options | 1.4561 s | see raw log | 379,387,904 B | Same CPU/env/input |
| M3 isolated bundle | 3/3 decisions, 8/8 options | 1.3791 s | 0.066 s | 378,372,096 B | Byte-identical to source |
| M3 source comparison | 3/3 decisions, 8/8 options | 1.4109 s | see raw log | 378,241,024 B | Same CPU/env/input |

² Existing CLI timer excludes interpreter/import startup. Total wall includes subprocess/sandbox/time/interpreter/import/load/inference/output, not installation. The first library import was slower; these are individual observations, **not an M2/M3 performance benchmark or flushed-disk cold-start comparison**.

³ macOS `/usr/bin/time -l` process-lifetime maximum resident set size, in bytes; not total-system memory or an accelerator peak. Both sandboxed runs emitted OpenMP warning #179 about a temporary-file sizing operation denied by the restrictive environment, then returned exit 0 with complete valid predictions. No warning is hidden and no failed inference was retried.

Every probability was finite, in [0,1], with complete option identity coverage and sums within tolerance. Example M2 intent distribution: address 0.8217263, cancel 0.0885343, refund 0.0897395. The same source/bundle output files match byte-for-byte for each candidate (maximum probability difference zero on these three inputs). Source comparisons deliberately ran outside the read-denying sandbox so they could access source checkpoints; they do **not** establish isolation themselves.

These original synthetic examples are not evaluation/accuracy evidence. M2 even ranks neutral slightly above positive for the demonstration lamp review. No final data was accessed, no calibration claim is made, and M3's prior independent-probe regression remains relevant despite its pilot gain.

## Review, build, failures and qualifications

Fresh bounded subagents implemented the stdlib exporter in a separate worktree, investigated licenses/isolation read-only, and independently reviewed code/manifests/runtime evidence. Owner reviewed and adopted the exporter commit, executed real exports/install/inference, then prepared the final docs/receipts. Review found no local-P1 blocker; its pre-install trust-hardening advice is included in the runtime README. A final deadline recheck was added immediately before launch in the reusable harness; the retained executed driver predates that guard, and all actual starts were already inside the grant.

Actual builds succeeded on the exporter and delivery worktrees; integrated-tree build is required by the shared merge-lock protocol. No software tests, test suite or linter was written/run. The runtime preflight and prediction/byte comparisons are actual delivery evidence, not a software test suite.

Preparation issues were corrected before inference: the first support-export attempt lacked its parent directory and produced no bundle; the first external Python copy copied an alias symlink back to the original home. That preliminary environment was **not** used for claimed inference. The resolved standalone interpreter was copied to a new location and a fresh `isolated-venv` created; sandbox preflight and runtime receipts establish the successful isolation. Existing outputs were not overwritten/reset. All four authorized inference calls succeeded once.

Licensing and portability remain bounded: model cards declare Apache-2.0 and accompany the full license and explicit adjacent modification notices; no upstream NOTICE exists at these pins. Jeff project/new-head and provider/account redistribution rights are unresolved. Checkpoint metadata preserves historical absolute project paths and its save-time job-status snapshot. No external publication or blanket legal clearance is claimed; local privacy and redistribution review is required before any future upload. No Python/dependency wheelhouse, Linux CPU, Intel macOS, Windows, accelerator, general-input equivalence, hardened hostile-file service or fully offline install was demonstrated.

Resources: four short sequential CPU calls finished, ML slot released, all subagents completed, no background release job. £0 actual / £0 pending / £0 allocation. Next useful bounded step is a local runtime export of a future owner-selected checkpoint through the same path; publication or platform expansion needs its own authorization/evidence, not implicit continuation of P1.
