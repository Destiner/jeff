# Fresh read-only M6 review

Reviewed dafd5d235b53af341fbf539e4bf32dcf09a399f2 source/config and agreed P4 flat manifest against current Runtime validator. No concrete code blockers; approval for scheduled capacity, with full training conditional on successful capacity and parent's frozen initial-control comparison.

Confirmed TRAIN-only1500 validated unique rows, seed42 materialized row/option order with identity remapping, exact replay before execution, source/config/local asset/runtime/tokenization pins, full-parameter FP32 grouped-symbol CE AdamW2e-5 accumulation4/375updates, one disposable capacity step plus4steady backwards/no second step, separate pinned reload/reseed for training, deterministic same-schedule eval/no-grad before/afterfit, originaltokenizer bytecopy and completed-only manifest. Local base lineage retains P3's downloaded-asset attestation, not new independent remote authentication.

Sampled memory is not peak and blocked native operations need external600/2700s deadlines; longest-input projection is not a full-runtime guarantee. Independent fresh reload is Runtime P4's later evidence. Reviewer ran no loads/tests/lint/builds/data access or writes; no contention.
