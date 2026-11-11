"""Bounded metadata-only inspection for the explicit P6 FP32 export."""

import json
import math
from pathlib import Path


SOURCE = Path(__file__).resolve()


def inspect_header(path, expected, *, require):
    """Read descriptors, not tensor values; HF still owns the actual load."""
    path = Path(path)
    size = path.stat().st_size

    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate safetensors header key")
            result[key] = value
        return result

    with path.open("rb") as stream:
        prefix = stream.read(8)
        require(len(prefix) == 8, "truncated safetensors prefix")
        length = int.from_bytes(prefix, "little")
        require(2 <= length <= min(1024 * 1024, size - 8),
                "unsupported safetensors header length")
        raw = stream.read(length)
        require(len(raw) == length, "truncated safetensors header")
        header = json.loads(raw, object_pairs_hook=unique)
    require(isinstance(header, dict), "safetensors header must be an object")
    metadata = header.pop("__metadata__", None)
    require(isinstance(metadata, dict) and metadata.get("format") == "pt"
            and all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()),
            "safetensors PyTorch metadata required")
    require(set(header) == set(expected), "serialized tensor inventory differs from proof")
    ranges = []
    for name, item in header.items():
        require(isinstance(item, dict) and set(item) == {"dtype", "shape", "data_offsets"},
                "unsupported safetensors tensor descriptor")
        shape, offsets = item["shape"], item["data_offsets"]
        require(isinstance(shape, list) and all(type(n) is int and n > 0 for n in shape),
                "invalid serialized tensor shape")
        require(item["dtype"] == "F32" and expected[name]["dtype"] == "float32"
                and shape == expected[name]["shape"], "serialized tensor dtype/shape mismatch")
        require(isinstance(offsets, list) and len(offsets) == 2
                and all(type(n) is int and n >= 0 for n in offsets),
                "invalid safetensors data offsets")
        start, end = offsets
        require(end - start == 4 * math.prod(shape) == expected[name]["bytes"],
                "serialized tensor byte size mismatch")
        ranges.append((start, end, name))
    position = 0
    for start, end, _ in sorted(ranges):
        require(start == position and end > start, "overlapping or noncontiguous tensor payload")
        position = end
    require(position == size - 8 - length, "safetensors payload length mismatch")
    return {"header_bytes": length, "payload_bytes": position,
            "metadata": metadata, "tensors": header}
