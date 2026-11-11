# Runtime P4: reusable scoring semantics and M6 checkpoint execution

P3 is complete and preserved. Model M6 is now authorized for one full-parameter Qwen decision-learning run using R5's primary recipe and existing dependencies, with a capacity check first. No Linux/packaging/platform work is assigned.

Coordinate directly with Model on narrow reuse of P3's exact prompt/chat-template, answer-boundary mapping and conditional readout, plus an explicit trained-checkpoint identity. Model owns training and checkpoint production; you own only needed additive changes in existing Runtime paths. Do not refactor the framework or edit Model files. Agree a minimal HF-compatible checkpoint/manifest handoff before implementing competing loaders.

Model produces fresh START predictions on E6's624 existing label-free inputs and deterministic TRAIN fit summaries. You own the one fresh-process TRAINED-checkpoint prediction pass on those same624 inputs after the checkpoint is ready. Preserve P3's original base-model pins/behavior; never mislabel trained weights as the old frozen revision or overwrite P3 artifacts.

Prepare the loader/inference extension while Model implements/trains. Ensure all source/tokenizer/checkpoint/config/input identities are explicit and frozen before your predictions. Keep the P3 prompt, scorer, device/dtype/cap and output contracts unchanged unless a genuine implementation limitation is reported before outcomes.

Under Model's bounded slot, demonstrate actual fresh-process offline reload, execute the complete trained prediction pass, and record coverage, errors, runtime/memory with the same timing/accounting qualifications as P3. No independent model load before a grant, redundant model run, new prompt search or performance framework. Return the slot and deliver immutable outputs directly to E6.

If M6 cannot pass its capacity preflight or complete training, stop downstream execution; retain useful narrow preparation and report the dependency honestly. No fallback experiment, new dependencies, cloud or bundle proliferation.

Use the canonical peer mailbox and existing self-review/self-merge ownership rules. No software tests/lint, protected final data, external publication, paid calls, or dependency changes. Preserve all prior checkpoints/releases and failed attempts. £0 new paid allocation; existing agent capacity is available. Do not wait for a support-team review gate.
