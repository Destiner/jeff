"""Verify a local directory bundle without importing the model stack."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from ._bundle import (
    CHECKPOINT_FILES, EXPORTER_REVISION, RUNTIME, SCHEMA, SUPPORT_FILES,
    checkpoint_summary, digest, inventory, read_json, regular_file, require,
    safe_path, text, wheel_metadata,
)


def verify_bundle(bundle: str | Path) -> dict:
    root = Path(bundle)
    # Check the control files before using any paths supplied by the manifest.
    with regular_file(root / "manifest.sha256") as handle:
        sidecar = handle.read(256)
    actual = digest(root / "manifest.json")["sha256"]
    require(sidecar == (actual + "  manifest.json\n").encode("ascii"), "manifest sidecar mismatch")
    manifest = read_json(root / "manifest.json")
    require(set(manifest) == {
        "schema_version", "bundle_id", "code_revision", "exporter", "checkpoint",
        "package", "provenance", "runtime", "files",
    } and manifest["schema_version"] == SCHEMA, "unsupported manifest schema")
    require(text(manifest["bundle_id"]) and text(manifest["code_revision"]), "missing bundle/code identity")
    exporter = manifest["exporter"]
    require(isinstance(exporter, dict) and set(exporter) == {"revision", "source_sha256"}, "invalid exporter record")
    require(exporter["revision"] == EXPORTER_REVISION, "unsupported exporter revision")
    sources = exporter["source_sha256"]
    require(isinstance(sources, dict) and set(sources) == {"__init__.py", "_bundle.py", "export.py", "verify.py"}, "invalid exporter source inventory")
    require(all(isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) for value in sources.values()), "invalid exporter source hash")
    require(manifest["runtime"] == RUNTIME, "invalid model/install distinction")
    require(isinstance(manifest["provenance"], dict) and bool(manifest["provenance"]), "provenance must be a nonempty object")
    package = manifest["package"]
    require(isinstance(package, dict) and text(package.get("path")), "invalid package record")
    wheel_path = safe_path(package["path"])
    require(wheel_path.startswith("package/") and wheel_path.count("/") == 1 and wheel_path.endswith(".whl"), "invalid wheel path")
    checkpoint = manifest["checkpoint"]
    require(isinstance(checkpoint, dict), "invalid checkpoint record")
    architecture = checkpoint.get("architecture")
    require(isinstance(architecture, str) and architecture in CHECKPOINT_FILES, "unsupported architecture")
    expected = {"checkpoint/" + name for name in CHECKPOINT_FILES[architecture]} | set(SUPPORT_FILES) | {wheel_path}
    files = manifest["files"]
    require(isinstance(files, dict), "files must be an inventory object")
    for name, entry in files.items():
        safe_path(name)
        require(isinstance(entry, dict) and set(entry) == {"bytes", "sha256"}, "invalid inventory entry")
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0, "invalid byte count")
        require(isinstance(entry["sha256"], str) and re.fullmatch(r"[a-f0-9]{64}", entry["sha256"]), "invalid SHA256")
    require(set(files) == expected, "manifest inventory does not match required bundle layout")
    inventory(root, expected | {"manifest.json", "manifest.sha256"})
    for name in sorted(expected):
        require(digest(root / name) == files[name], "file size/hash mismatch: " + name)
    require(checkpoint_summary(root / "checkpoint") == checkpoint, "checkpoint metadata mismatch")
    require(wheel_metadata(root / wheel_path) == package, "wheel metadata mismatch")
    require(read_json(root / "provenance.json") == manifest["provenance"], "provenance mismatch")
    return {
        "status": "ok", "bundle_id": manifest["bundle_id"], "manifest_sha256": actual,
        "files": len(files), "bytes": sum(entry["bytes"] for entry in files.values()),
        "original_paths_present": checkpoint["original_path_disclosure"]["present"],
    }


def main() -> None:
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    try:
        result = verify_bundle(args.bundle)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"verification failed: {error}\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
