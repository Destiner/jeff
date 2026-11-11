"""Identity-only validation of the flat P4 trained-checkpoint manifest."""

from pathlib import Path
import re
import stat


SOURCE = Path(__file__).resolve()
MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"
SCORING_SHA256 = "2698ed67deead6cd3e234255fb0fc5182a990ac99d397e659a804d3562cce77f"
TOKENIZERS = {
    "merges.txt": "599bab54075088774b1733fde865d5bd747cbcc7a547c5bc12610e874e26f5e3",
    "tokenizer.json": "c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539",
    "tokenizer_config.json": "5b5d4f65d0acd3b2d56a35b56d374a36cbc1c8fa5cf3b3febbbfabf22f359583",
    "vocab.json": "ca10d7e9fb3ed18575dd1e277a2579c16d108e32f27439684afa0e10b1440910",
}
REQUIRED_FILES = {"model.safetensors", "config.json", "generation_config.json", *TOKENIZERS}
ALLOWED_FILES = REQUIRED_FILES | {"README.md", "LICENSE"}


def validate_checkpoint(manifest_path, model_dir, config_path, cfg, *,
                        require, load, digest, safe_path, assets):
    """Check identity without following training provenance or parsing its receipt.

    Adapter helpers keep JSON/path/hash semantics identical to P3. Strict flat
    inventory checks precede assets(), so it cannot follow checkpoint symlinks.
    """
    model_dir = safe_path(model_dir)
    raw_manifest = Path(manifest_path).absolute()
    require(not raw_manifest.is_symlink(), "checkpoint manifest must not be a symlink")
    manifest_path = safe_path(raw_manifest)
    require(manifest_path.parent == model_dir.parent and
            not manifest_path.is_relative_to(model_dir),
            "checkpoint manifest must be outside and sibling to model directory")
    require(manifest_path.is_file(), "checkpoint manifest must be an existing file")
    manifest = load(manifest_path)
    require(isinstance(manifest, dict), "checkpoint manifest must be an object")
    version = manifest.get("schema_version")
    require(version in ("jeff.qwen-trained-checkpoint.v1", "jeff.qwen-trained-checkpoint.v2"),
            "unsupported checkpoint schema version")
    fixed = {"schema_version": version, "status": "complete",
             "kind": "trained", "base_model_id": MODEL, "base_revision": REVISION}
    require(all(manifest.get(k) == v for k, v in fixed.items()), "checkpoint identity/status")
    for key in ("checkpoint_id", "run_id"):
        require(isinstance(manifest.get(key), str) and manifest[key].strip(),
                f"nonempty checkpoint {key} required")
    for key, width in (("training_code_revision", 40),
                       ("training_data_manifest_sha256", 64),
                       ("training_recipe_sha256", 64),
                       ("training_schedule_sha256", 64),
                       ("p3_scoring_config_sha256", 64)):
        require(isinstance(manifest.get(key), str) and
                re.fullmatch(r"[0-9a-fA-F]{%d}" % width, manifest[key]),
                f"invalid checkpoint {key}")
    require(manifest["p3_scoring_config_sha256"] == SCORING_SHA256 == digest(config_path),
            "checkpoint scoring config must match original P3 bytes")
    require(manifest.get("tokenizer_assets") == TOKENIZERS,
            "checkpoint must preserve all four original tokenizer hashes")
    inventory = manifest.get("files")
    require(isinstance(inventory, dict), "checkpoint files inventory required")
    require(REQUIRED_FILES <= set(inventory) <= ALLOWED_FILES,
            "unsupported or missing checkpoint assets")
    for name, entry in inventory.items():
        require(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name)
                and Path(name).name == name, "checkpoint inventory names must be safe and flat")
        require(isinstance(entry, dict) and set(entry) == {"sha256", "bytes"},
                "checkpoint file entry fields")
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0,
                "checkpoint file bytes must be a nonnegative integer")
        require(isinstance(entry["sha256"], str) and
                re.fullmatch(r"[0-9a-fA-F]{64}", entry["sha256"]),
                "invalid checkpoint file hash")
    local_files = {}
    for path in model_dir.iterdir():
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode),
                "checkpoint directory must contain only regular flat files; no symlinks")
        local_files[path.name] = info.st_size
    require(set(local_files) == set(inventory), "checkpoint file inventory mismatch")
    require(all(local_files[name] == entry["bytes"] for name, entry in inventory.items()),
            "checkpoint file size mismatch")
    asset_hashes = assets(model_dir, cfg)
    require(all(asset_hashes.get(name) == entry["sha256"].lower()
                for name, entry in inventory.items()), "checkpoint file hash mismatch")
    require(all(asset_hashes.get(name) == value for name, value in TOKENIZERS.items()),
            "checkpoint tokenizer bytes differ from original P3")
    receipt = manifest.get("source_run_receipt")
    require(isinstance(receipt, dict) and isinstance(receipt.get("path"), str)
            and receipt["path"].strip() and isinstance(receipt.get("sha256"), str)
            and re.fullmatch(r"[0-9a-fA-F]{64}", receipt["sha256"]),
            "checkpoint source run receipt path/hash required")
    receipt_path = safe_path(manifest_path.parent / receipt["path"])
    require(receipt_path.is_file(), "checkpoint source run receipt must exist")
    receipt_hash = digest(receipt_path)
    require(receipt_hash == receipt["sha256"].lower(), "checkpoint source run receipt hash mismatch")
    binding = {"manifest_path": str(manifest_path), "manifest_sha256": digest(manifest_path),
               "manifest": manifest, "source_run_receipt": {"path": str(receipt_path),
               "sha256": receipt_hash}, "validator_source_sha256": digest(SOURCE)}
    if version == "jeff.qwen-trained-checkpoint.v2":
        from jeff.runtime.qwen_readout import validate_metadata

        binding["readout_proof"] = validate_metadata(
            manifest_path, model_dir, manifest, receipt_path, require=require,
            load=load, digest=digest, safe_path=safe_path)
    return binding, asset_hashes
