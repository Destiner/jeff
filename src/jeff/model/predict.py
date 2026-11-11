"""Decision-only JSONL prediction: python -m jeff.model.predict --help."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import tempfile
import time
from pathlib import Path

import torch

from .scorer import (
    _DECISION_FIELDS,
    _reject_constant,
    _unique_object,
    load_checkpoint,
    resolve_device,
    validate_decision,
)


def _rows(path: Path):
    seen = set()
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            try:
                if not line.strip():
                    raise ValueError("empty lines are not allowed")
                row = json.loads(line, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
                validate_decision(row)
                if set(row) != _DECISION_FIELDS:
                    raise ValueError("inference accepts decision fields only; remove labels/metadata")
                if any(set(option) != {"id", "text"} for option in row["options"]):
                    raise ValueError("inference options accept id and text only")
                if row["id"] in seen:
                    raise ValueError(f"duplicate decision id: {row['id']!r}")
                seen.add(row["id"])
            except (ValueError, TypeError) as error:
                raise ValueError(f"input line {line_number}: {error}") from error
            yield row
    if not seen:
        raise ValueError("input contains no decisions")


def _write_batch(model, rows: list[dict], output) -> None:
    probabilities = model.probabilities(rows).cpu()
    expected_shape = (len(rows), max(len(row["options"]) for row in rows))
    if tuple(probabilities.shape) != expected_shape:
        raise ValueError("model returned an incorrect prediction shape")
    for row, values in zip(rows, probabilities.tolist()):
        count = len(row["options"])
        scores = values[:count]
        if (
            any(not math.isfinite(value) or not 0 <= value <= 1 for value in scores)
            or not math.isclose(sum(scores), 1.0, rel_tol=1e-5, abs_tol=1e-6)
            or any(value != 0 for value in values[count:])
        ):
            raise ValueError(f"invalid probabilities for decision {row['id']!r}")
        result = {
            "schema_version": "0.1",
            "id": row["id"],
            "probabilities": [
                {"option_id": option["id"], "probability": score}
                for option, score in zip(row["options"], scores)
            ],
        }
        output.write(json.dumps(result, ensure_ascii=False, allow_nan=False) + "\n")


def _predict(args) -> int:
    started = time.perf_counter()
    destination = Path(args.output)
    if os.path.lexists(destination):
        raise FileExistsError(f"refusing to overwrite output: {destination}")
    device = resolve_device(args.device)
    print(f"device={device}", file=sys.stderr)
    model = load_checkpoint(args.checkpoint, device=str(device))
    model.eval()
    temporary = None
    completed = 0
    try:
        # The temporary file shares the destination filesystem, so link publication
        # is atomic and fails if another process creates the destination first.
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=destination.parent,
            prefix=f".{destination.name}.", suffix=".tmp", delete=False,
        ) as output:
            temporary = Path(output.name)
            batch = []
            with torch.inference_mode():
                for row in _rows(Path(args.input)):
                    batch.append(row)
                    if len(batch) == args.batch_size:
                        _write_batch(model, batch, output)
                        completed += len(batch)
                        batch.clear()
                if batch:
                    _write_batch(model, batch, output)
                    completed += len(batch)
            output.flush()
            os.fsync(output.fileno())
        os.link(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"predictions={completed} duration_seconds={time.perf_counter() - started:.3f}", file=sys.stderr)
    return completed


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Score decision-only v0.1 JSONL using a local Jeff checkpoint.")
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--device", choices=("auto", "cpu", "mps"), default="auto")
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args(argv)
    if args.batch_size < 1:
        parser.error("--batch-size must be positive")
    started = time.perf_counter()
    try:
        _predict(args)
    except Exception as error:
        parser.exit(1, f"prediction failed after {time.perf_counter() - started:.3f}s: {error}\n")


if __name__ == "__main__":
    main()
