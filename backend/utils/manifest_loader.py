import json
from pathlib import Path

def load_manifest(manifest_path: Path) -> dict:
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_catalog(catalog_path: Path) -> dict:
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)
