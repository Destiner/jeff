"""Canonical M8 tensor evidence; no ML imports, construction, or I/O at import.

Callers supply already-loaded tensors and an optional cooperative guard. Hashes
cover C-order little-endian CPU float32 bytes, independent of device/name. Runtime
may reuse these read-only helpers on its sole authorized fresh reload.
"""

import hashlib

SCHEMA = "jeff.qwen-readout-proof.v1"
ADAPTATION = "frozen-base-six-row-readout"
REPRESENTATION = "hf-untied-full-vocab"
VOCAB_SIZE = 151936
HIDDEN_SIZE = 896
ORIGINAL_PARAMETERS = 494032768
HEAD_PARAMETERS = 5376
CHUNK_ELEMENTS = 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def _update(digest, tensor, guard):
    require(str(tensor.dtype) == "torch.float32", "canonical evidence requires actual FP32")
    require(tensor.is_contiguous(), "canonical evidence requires contiguous storage")
    flat = tensor.detach().view(-1)
    for start in range(0, flat.numel(), CHUNK_ELEMENTS):
        if guard is not None:
            guard("tensor_hash_chunk")
        chunk = flat[start:start + CHUNK_ELEMENTS].cpu().contiguous().numpy()
        digest.update(chunk.astype("<f4", copy=False).tobytes(order="C"))


def tensor_record(tensor, guard=None):
    digest = hashlib.sha256()
    _update(digest, tensor, guard)
    return {"shape": list(tensor.shape), "dtype": "float32",
            "sha256": digest.hexdigest(), "bytes": tensor.numel() * 4}


def nonanswer_record(table, answer_token_ids, guard=None):
    """Ascending rows excluding the six answers; bounded transfers, no big gather."""
    require(list(table.shape) == [VOCAB_SIZE, HIDDEN_SIZE], "wrong full-vocabulary table")
    excluded = sorted(answer_token_ids)
    require(len(excluded) == len(set(excluded)) == 6 and
            all(type(i) is int and 0 <= i < VOCAB_SIZE for i in excluded), "invalid answer IDs")
    digest = hashlib.sha256()
    start = 0
    for stop in [*excluded, VOCAB_SIZE]:
        _update(digest, table[start:stop], guard)
        start = stop + 1
    return {"shape": [VOCAB_SIZE - 6, HIDDEN_SIZE], "dtype": "float32",
            "sha256": digest.hexdigest(), "bytes": (VOCAB_SIZE - 6) * HIDDEN_SIZE * 4}


def backbone_records(model, guard=None):
    """Full model.* keys, lm_head excluded; nonpersistent buffers included."""
    parameters = {name: tensor_record(value, guard)
                  for name, value in model.named_parameters() if name.startswith("model.")}
    buffers = {name: tensor_record(value, guard)
               for name, value in model.named_buffers() if name.startswith("model.")}
    require(parameters and sum(r["bytes"] // 4 for r in parameters.values()) == ORIGINAL_PARAMETERS,
            "incomplete original backbone parameter scope")
    return {"parameters": parameters, "fixed_buffers": buffers}


def storage_disjoint(left, right):
    """Whole backing-storage intervals, not Python identities or view pointers."""
    if left.device != right.device:
        return True
    a, b = left.untyped_storage(), right.untyped_storage()
    return a.data_ptr() + a.nbytes() <= b.data_ptr() or b.data_ptr() + b.nbytes() <= a.data_ptr()


def output_records(table, answer_token_ids, guard=None):
    return {"full_head": tensor_record(table, guard),
            "ordered_answer_rows": tensor_record(table[answer_token_ids].contiguous(), guard),
            "answer_rows": {str(i): tensor_record(table[i], guard) for i in answer_token_ids},
            "nonanswer_rows": nonanswer_record(table, answer_token_ids, guard)}
