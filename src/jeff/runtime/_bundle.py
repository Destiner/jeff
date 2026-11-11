"""Small shared bundle contract and byte-level inspection helpers."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import stat
import zipfile
from contextlib import contextmanager
from email.parser import BytesParser
from pathlib import Path, PurePosixPath

SCHEMA = "jeff.runtime.bundle.v1"
EXPORTER_REVISION = "jeff.runtime.export.v1"
COMMON = frozenset({
    "checkpoint.json", "encoder/config.json", "encoder/model.safetensors",
    "tokenizer/tokenizer.json", "tokenizer/tokenizer_config.json",
    "tokenizer/special_tokens_map.json", "tokenizer/vocab.txt",
})
CHECKPOINT_FILES = {
    "jeff.joint_encoder_mean_pool_scalar.v1": COMMON | {"head.safetensors"},
    "jeff.pretrained_cross_encoder_scalar.v1": COMMON,
}
SUPPORT_FILES = frozenset({
    "README.md", "requirements-macos-arm64-py312.txt", "provenance.json",
    "demo/inputs.jsonl", "licenses/APACHE-2.0.txt", "licenses/NOTICE.md",
    "licenses/upstream-model-card.md",
})
RUNTIME = {
    "model_extra": "model",
    "requirements_file": "requirements-macos-arm64-py312.txt",
    "requirements_scope": "macOS arm64, Python 3.12; owner-prepared dependency pins",
    "installation": "Wheel and Python dependencies must be installed separately; dependency downloads may require network access. Dependency wheels are not bundled.",
    "inference": "Checkpoint contains local model/tokenizer weights; use the existing jeff.model.predict loader with offline flags. Export/verification does not execute inference.",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def safe_path(value: object) -> str:
    require(isinstance(value, str) and bool(value), "inventory path must be a string")
    require(not any(c in value for c in ("\\", ":", "\x00")), "unsafe path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and all(p not in {"", ".", ".."} for p in value.split("/")), "unsafe path")
    return value


@contextmanager
def regular_file(path: Path):
    """Open without following links, including links in ancestor components."""
    absolute = Path(os.path.abspath(path))
    directory = os.open(absolute.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in absolute.parts[1:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        fd = os.open(absolute.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        with os.fdopen(fd, "rb") as handle:
            info = os.fstat(handle.fileno())
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "expected regular unlinked file: " + str(path))
            yield handle
    finally:
        os.close(directory)


def unique_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path: Path) -> dict:
    with regular_file(path) as handle:
        value = json.load(handle, object_pairs_hook=unique_object)
    require(isinstance(value, dict), "JSON must contain an object: " + str(path))
    json.dumps(value, allow_nan=False)
    return value


def serialized(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def directories(files: set | frozenset) -> set[str]:
    return {str(parent) for name in files for parent in PurePosixPath(name).parents if str(parent) != "."}


def inventory(root: Path, expected: set | frozenset) -> None:
    """Inspect the tree, but never use discovery as a copying allowlist."""
    for ancestor in (root, *root.absolute().parents):
        require(not ancestor.is_symlink(), "linked directory: " + str(ancestor))
    require(stat.S_ISDIR(root.lstat().st_mode), "expected directory: " + str(root))
    found, dirs = set(), set()
    for current, subdirs, files in os.walk(root, followlinks=False):
        for name in subdirs + files:
            item = Path(current) / name
            info = item.lstat()
            relative = item.relative_to(root).as_posix()
            safe_path(relative)
            if stat.S_ISDIR(info.st_mode):
                dirs.add(relative)
            else:
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "links/special files forbidden: " + relative)
                found.add(relative)
    require(found == set(expected), f"inventory mismatch: missing={sorted(set(expected) - found)}, unexpected={sorted(found - set(expected))}")
    require(dirs == directories(expected), "unexpected or missing directories")


def digest(path: Path) -> dict:
    sha, size = hashlib.sha256(), 0
    with regular_file(path) as handle:
        while chunk := handle.read(1024 * 1024):
            sha.update(chunk)
            size += len(chunk)
    return {"sha256": sha.hexdigest(), "bytes": size}


def checkpoint_summary(root: Path) -> dict:
    config = read_json(root / "checkpoint.json")
    architecture = config.get("architecture")
    require(isinstance(architecture, str) and architecture in CHECKPOINT_FILES, "unsupported checkpoint architecture")
    require(config.get("schema_version") == "0.1", "unsupported checkpoint schema")
    for key in ("model_id", "revision"):
        require(text(config.get(key)), "missing checkpoint " + key)
    require(config.get("resolved_revision") is None or text(config["resolved_revision"]), "invalid resolved revision")
    require(type(config.get("max_length")) is int and 8 <= config["max_length"] <= 1_000_000, "invalid max_length")
    temperature = config.get("temperature")
    require(type(temperature) in (int, float) and math.isfinite(temperature) and temperature > 0, "invalid temperature")
    require(isinstance(config.get("input_formatting"), dict) and isinstance(config.get("metadata"), dict), "missing checkpoint settings/metadata")
    settings = {key: config[key] for key in (
        "input_formatting", "max_length", "temperature", "scoring", "head_initialization",
        "hidden_size", "tokenizer_id", "tokenizer_revision", "tokenizer_resolved_revision",
    ) if key in config}
    # Report locations, not private values. The original JSON remains byte-for-byte intact.
    locations = []
    def inspect(value, pointer):
        if isinstance(value, dict):
            for key, item in value.items():
                escaped = key.replace("~", "~0").replace("/", "~1")
                if key.startswith(("/", "~\\", "~//")):
                    locations.append(pointer + "/<absolute-path-key>")
                inspect(item, pointer + "/" + escaped if not key.startswith("/") else pointer + "/<absolute-path-key>")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                inspect(item, pointer + "/" + str(index))
        elif isinstance(value, str) and (value.startswith(("/", "~/", "file://", "\\\\")) or re.match(r"^[A-Za-z]:[\\/]", value)):
            locations.append(pointer)
    inspect(config, "")
    return {
        "architecture": architecture, "model_id": config["model_id"],
        "revision": config["revision"], "resolved_revision": config.get("resolved_revision"),
        "settings": settings,
        "original_path_disclosure": {
            "present": bool(locations), "json_pointers": sorted(set(locations)),
            "note": "Original checkpoint JSON is preserved, including historical local paths; these are provenance, not bundled dependencies. Do not publish without reviewing privacy.",
        },
    }


def wheel_metadata(path: Path) -> dict:
    require(path.suffix == ".whl", "package must be a wheel")
    safe_path(path.name)
    with regular_file(path) as handle, zipfile.ZipFile(handle) as wheel:
        names = wheel.namelist()
        require(len(names) == len(set(names)), "duplicate wheel members")
        metadata = [name for name in names if name.endswith(".dist-info/METADATA") and name.count("/") == 1]
        require(len(metadata) == 1, "wheel must have exactly one METADATA")
        message = BytesParser().parsebytes(wheel.read(metadata[0]))
    for field in ("Name", "Version", "Requires-Python"):
        require(len(message.get_all(field, [])) == 1 and text(message[field]), "missing/duplicate wheel " + field)
    require(message["Name"] == "jeff", "expected jeff package")
    extras = message.get_all("Provides-Extra", [])
    require("model" in extras, "wheel must provide model extra")
    return {
        "path": "package/" + path.name, "name": message["Name"], "version": message["Version"],
        "requires_python": message["Requires-Python"],
        "requires_dist": message.get_all("Requires-Dist", []), "provides_extra": extras,
    }
