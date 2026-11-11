"""Create a new read-only local bundle from an existing M2/M3 checkpoint.

An atomically created output directory reserves the name (no overwrite/rename).
Until completion it contains .incomplete and cannot pass verification. Handled
failures remove it; a killed process can leave an explicitly incomplete directory.
Inputs and the destination parent must not be concurrently modified by others.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from ._bundle import (
    CHECKPOINT_FILES, EXPORTER_REVISION, RUNTIME, SCHEMA, SUPPORT_FILES,
    checkpoint_summary, digest, inventory, read_json, regular_file, require,
    serialized, text, wheel_metadata,
)
from .verify import verify_bundle


def export_bundle(*, checkpoint: Path, wheel: Path, support_dir: Path,
                  output_dir: Path, bundle_id: str, code_revision: str) -> dict:
    require(text(bundle_id) and text(code_revision), "bundle-id and code-revision must be nonempty")
    checkpoint, wheel, support_dir = Path(checkpoint), Path(wheel), Path(support_dir)
    output = Path(os.path.abspath(output_dir))
    require(not os.path.lexists(output), "output path already exists")
    summary = checkpoint_summary(checkpoint)
    checkpoint_files = CHECKPOINT_FILES[summary["architecture"]]
    inventory(checkpoint, checkpoint_files)
    inventory(support_dir, SUPPORT_FILES)
    package = wheel_metadata(wheel)
    provenance = read_json(support_dir / "provenance.json")
    require(bool(provenance), "provenance object must not be empty")
    for ancestor in (output.parent, *output.parent.parents):
        require(not ancestor.is_symlink(), "output parent must not be linked")
    require(output.parent.is_dir(), "output parent must already exist")
    # Reject nesting even before reserving a name in the immutable source tree.
    for source in (checkpoint, support_dir):
        require(not output.is_relative_to(source.resolve()), "output cannot be inside an input directory")
    sources = {"checkpoint/" + name: checkpoint / name for name in checkpoint_files}
    sources.update({name: support_dir / name for name in SUPPORT_FILES})
    sources[package["path"]] = wheel
    before = {name: digest(path) for name, path in sorted(sources.items())}
    source_dir = Path(__file__).parent
    exporter = {
        "revision": EXPORTER_REVISION,
        "source_sha256": {name: digest(source_dir / name)["sha256"] for name in (
            "__init__.py", "_bundle.py", "export.py", "verify.py",
        )},
    }
    output.mkdir(mode=0o700, exist_ok=False)
    try:
        (output / ".incomplete").write_text("Export in progress; not a verified bundle.\n", encoding="utf-8")
        for name, source in sorted(sources.items()):
            destination = output / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with regular_file(source) as handle, destination.open("xb") as target:
                shutil.copyfileobj(handle, target, length=1024 * 1024)
            require(digest(destination) == before[name], "source changed while copying: " + name)
        inventory(checkpoint, checkpoint_files)
        inventory(support_dir, SUPPORT_FILES)
        require(all(digest(path) == before[name] for name, path in sources.items()), "input changed during export")
        require(checkpoint_summary(output / "checkpoint") == summary, "checkpoint changed during export")
        require(wheel_metadata(output / package["path"]) == package, "wheel changed during export")
        require(read_json(output / "provenance.json") == provenance, "provenance changed during export")
        manifest = {
            "schema_version": SCHEMA, "bundle_id": bundle_id, "code_revision": code_revision,
            "exporter": exporter, "checkpoint": summary, "package": package,
            "provenance": provenance, "runtime": RUNTIME, "files": before,
        }
        (output / "manifest.json").write_bytes(serialized(manifest))
        manifest_hash = digest(output / "manifest.json")["sha256"]
        (output / "manifest.sha256").write_text(manifest_hash + "  manifest.json\n", encoding="ascii")
        (output / ".incomplete").unlink()
        result = verify_bundle(output)
        for current, dirs, files in os.walk(output, topdown=False):
            for name in files:
                (Path(current) / name).chmod(0o444)
            for name in dirs:
                (Path(current) / name).chmod(0o555)
        output.chmod(0o555)
        return result
    except BaseException:
        # chmod may have failed part-way through; restore only our output tree.
        output.chmod(0o700)
        (output / ".incomplete").write_text("Export failed; not a completed bundle.\n", encoding="utf-8")
        for current, dirs, _ in os.walk(output):
            for name in dirs:
                (Path(current) / name).chmod(0o700)
        shutil.rmtree(output)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--support-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--code-revision", required=True)
    args = parser.parse_args()
    try:
        result = export_bundle(**vars(args))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"export failed: {error}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
