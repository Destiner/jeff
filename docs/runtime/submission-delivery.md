# M9 delivery and recorded application execution

**2026-11-12.** [85-second demonstration](https://github.com/Destiner/jeff/releases/download/m9-browser-v1/jeff-actual-demo.mp4) · [M9 release](https://github.com/Destiner/jeff/releases/tag/m9-browser-v1) · [Setup commands](../../web/README.md).

Six frozen, previously scored examples returned actual M9 predictions through normal production buttons: two queue **Suggest destination**, two chat **Suggest reaction**, and two playground **Run locally**. The executed source was **`1e804a332c475fbaa24a69f91df6ad476029258d`**, with SDK identity **`4a1334d585bec2dd69aec9f07eb68e0fcc4c3771`**, from a fresh local checkout. Runtime: owned, isolated **Chromium 151.0.7922.34**, macOS arm64, single-thread WASM, unchanged FP32 M9 assets. No native replay, retraining, Qwen retry, new diagnostic cases or inference-server fallback occurred.

This is a new delivery phase. The original 20:15 final-app phase remains **UNATTEMPTED**. The earlier [packed-SDK Safari proof](final-sdk.md) remains separate. The new app graph's offline inference is still **unverified**.

## Saved-output and functional results

An independent reviewer compared the saved browser outputs with the frozen native packet, without another model run:

- **6 unique predictions / 24 raw probabilities**. Complete input identity, model descriptor, semantic option IDs/order, finite range and all six top choices matched.
- Maximum absolute raw probability difference: **0.00000168745643670**, below the fixed **0.0001** limit.
- Maximum recorded-decimal probability-sum error: **6.8×10⁻¹⁷**, below **10⁻⁶**. No normalization, clipping or repair.
- Four complete rendered distributions—queue and playground—matched displayed rounding/order. Chat snapshots established the two displayed top suggestions, not full rendered distributions.
- Both separate manual queue actions completed: **“Routed to Writing.”** and **“Routed to Scheduling.”** Routing changes local state only.
- All six were plain `predict` calls. **No token-parity claim** is made for this phase.

| App / frozen case | Actual top choice | Raw relative probability |
| --- | --- | ---: |
| Queue / sorter-07 described | Writing desk | 0.9353098657548541 |
| Queue / sorter-08 described | Schedule planner | 0.5150723149717549 |
| Chat / sentiment-01 | Positive | 0.9745414897415463 |
| Chat / sentiment-02 | Negative | 0.9985530773677748 |
| Playground / sentiment-13 | Positive | 0.9496298358535692 |
| Playground / sentiment-14 | Mixed | 0.8918443481139946 |

The last example is a polite negative complaint; the recorded model ranks **Mixed**, displayed **89.18%**. It is retained in the video, not replaced by a favorable example. Matching native output demonstrates runtime agreement, not that the decision is correct. These authored development examples do not establish general accuracy, calibration or appropriate social behavior. Emoji mapping is fixed; there is no external chat/workspace integration.

## Interrupted attempts and closure

1. **Safari submission attempt, 21:29–21:31:** first queue request reached initialization but returned no prediction before its 100-second stage cap. The saved bridge state was disposed/closed, idle and null-metadata after abort; asynchronous attempt completion was not established within the external cap. Window capture rendered blank app content. The initialization/rendering root cause is not established. The three task documents were subsequently destroyed; Apple Events retained an empty window shell with zero tabs. No user Safari process was killed. Charge **121 seconds**; sampled browser RSS peaked at **6,280,658,944 bytes**, pressure level1.
2. **Chromium first recording, 21:50:57–21:51:44:** two queue, two chat and the first playground prediction completed. Queue/chat engines were disposed and their targets closed before successors. A strict missing-or-zero per-process RSS guard then stopped and killed only the owned Chromium group. This whole controller remains **FAILED**, not retroactively passed. Its rejected sample's rows were not retained, so the precise cause is unknown; a zero-RSS/zombie explanation is not established. Earlier valid samples remained below8GiB with pressure1; sampled conservative peak **6,394,183,680 bytes**. Charge **48 seconds**.
3. **Explicitly authorized final-case continuation, 21:56:56–21:57:08:** only the unattempted `demo-s2:sentiment-14` ran, once, in a fresh owned Chromium session. No preceding prediction was repeated. This controller completed, disposed the engine and closed its target. Its prospective guard accepted explicit nonnegative kernel RSS for unrelated processes while requiring a positive owned root, valid rows, pressure1 and the unchanged conservative8GiB ceiling. Actual zero rows/status were retained. Charge **13 seconds**.

Both Chromium parent exits were observed, owned groups were terminated, and group absence was checked before continuation/final handoff. Guard samples target a two-second cadence; sampled RSS is not a continuous peak or general device-memory guarantee. Models ran serially. The closed shared accounting is **6 historical +121 +48 +13 =188/300 seconds**; remaining budget is not a new execution grant.

## Release and clean setup

Release **`m9-browser-v1`** contains the reviewed model-only archive:

- **`jeff-m9-browser-v1.tar.gz`**, **83,457,505 bytes**.
- SHA-256 **`eae183b0814afd62c54f1efe169aae8bc36cfa717809cc77a117963239c29286`**; adjacent checksum file.
- Eleven allowlisted regular files. ONNX/model descriptor/tokenizer payloads are byte-identical to the preceding local candidate. No new export, training/evaluation data, Qwen weights, ORT binaries or Python environment is included.
- Nested tokenizer layout works with the existing asset copier. The archive retains the pinned upstream Apache-2.0 model card, canonical license text, attribution and modification notices. No project-wide first-party license was selected.

The actual GitHub release archive/checksum were downloaded and verified. A fresh local Git clone at the executed commit installed pinned dependencies and built/staged/served the apps with **Bun1.4.4** in an isolated, credential-free install/build/serving environment. Source acquisition used local Git transport; release acquisition used authenticated GitHub because the owner had made the repository private again. **Anonymous clone/download verification remains deferred.** This is not a cold-machine or cache-independent setup benchmark.

The first launch rejected macOS `/var` as a symlink. Repeating only launch with canonical `/private/var` asset paths succeeded: **2.56 seconds** for relaunch, **65.1 seconds** overall from the initial setup start. No source/model changes were needed. All three pages and the descriptor returned HTTP200 at21:11:21; actual inference happened later in the phases above. The README uses `pwd -P` to avoid this path issue.

The owner will decide when to make the repository public. Delivery work did not change it back to public. Release access follows repository visibility.

## Recording

**`jeff-actual-demo.mp4`**: **85.08 seconds**, 1280×900, H.264, silent with factual chapter/end cards; **905,405 bytes**, SHA-256 **`06301bb22c7426929a00944dcc145fe539e5bf2d51725e28cf6d850d8913c53a`**.

Actual page-only PNG captures were sampled approximately every400ms. Original frames were retained and encoded with their timestamp spacing; output24fps duplicates frames, without interpolation or speed changes. Each folder's last sample receives a disclosed0.4-second hold. Navigation/interruption gaps between folders were cut. The video identifies the two Chromium recording segments and that each of the six decisions was computed once. It neither shows nor claims successful Safari production-app execution. No desktop, personal/work tabs, microphone, credentials or unrelated windows were captured in the delivered video.

The video shows **M9 only**. Qwen was genuinely fine-tuned and ran natively, but its separate historical browser attempt stopped without a prediction. The end card preserves that distinction and the uncalibrated-score limitation.

## Evidence custody

The small [delivery manifest](../../manifests/releases/submission-delivery-20261112-01.json) records artifact hashes and aggregate claims. Large/local receipts remain ignored; they were not uploaded as a bundle. Under `artifacts/lead/submission-20261112-01/`:

- `asset-publication.json`, `clean-setup.json`, `clean-setup-02.json` and preserved launch/install logs.
- `execution/` contains the actual Safari activation/controller/failed attempt; the original earlier `artifacts/release/final-app-20261112-01/closure.json` remains unchanged.
- `chromium/` contains source/activation records, separate runs, raw histories, DOM captures, guard samples, external returns and source pins.
- `comparison/{compare.py,receipt.json,report.md}` contains independent saved-evidence arithmetic and functional scope.
- `video/final/edit-manifest.json` identifies every source frame folder, timing and cut.

Source publication, package builds, asset acquisition, model execution and later saved-evidence review are distinct steps. No protected evaluation references were accessed for this delivery.
