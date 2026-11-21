"""Local sound asset catalogue. No downloads, cloud calls or paid generation."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(os.environ.get("VOICEFORGE_DATA_DIR", "./voiceforge-data")).resolve()
CATALOGUE = ROOT / "assets.json"
ALLOWED_EXT = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
CATEGORIES = {"music", "effect", "dialogue", "narration", "ambience"}


def resolve_asset(relative_path: str) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise ValueError("Use an asset path relative to VoiceForge data directory.")
    path = (ROOT / relative_path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError("Asset must be an existing file inside VoiceForge data directory.")
    if path.suffix.lower() not in ALLOWED_EXT:
        raise ValueError("Unsupported audio extension.")
    return path


def read_catalogue() -> dict:
    if not CATALOGUE.exists():
        return {}
    data = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Invalid asset catalogue.")
    return data


def register_asset(asset_id: str, path: str, category: str, rights_note: str,
                   approved_for_publication: bool = False) -> dict:
    """Register an existing audio asset; rights must be described explicitly."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]{2,64}", asset_id):
        raise ValueError("Invalid asset ID.")
    if category not in CATEGORIES:
        raise ValueError("Unknown category.")
    if not rights_note.strip():
        raise ValueError("Provide an asset rights note; no assumed free commercial use.")
    asset = resolve_asset(path)
    catalogue = read_catalogue()
    if asset_id in catalogue:
        raise ValueError("Asset ID already exists; no silent overwrites.")
    record = {"path": str(asset.relative_to(ROOT)), "category": category,
              "rights_note": rights_note[:500],
              "approved_for_publication": bool(approved_for_publication)}
    catalogue[asset_id] = record
    ROOT.mkdir(parents=True, exist_ok=True)
    temporary = CATALOGUE.with_suffix(".tmp")
    temporary.write_text(json.dumps(catalogue, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(CATALOGUE)
    return record


def list_assets(category: str = "", approved_only: bool = True) -> dict:
    """List original/licensed assets, excluding unpublished assets by default."""
    catalogue = read_catalogue()
    return {k: v for k, v in catalogue.items()
            if (not category or v["category"] == category)
            and (not approved_only or v["approved_for_publication"])}
