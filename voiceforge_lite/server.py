"""TA GuruLabs VoiceForge Lite — local-first, no paid API calls.

Optional prerequisites:
    pip install mcp
    pip install faster-whisper     # for transcription
    Install ffmpeg and Piper TTS separately; configure PIPER_MODEL path.

Run: python -m voiceforge_lite.server
Works locally with an MCP client supporting stdio.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from .library import register_asset, list_assets

ROOT = Path(os.environ.get("VOICEFORGE_DATA_DIR", "./voiceforge-data")).resolve()
ROOT.mkdir(parents=True, exist_ok=True)
MCP = FastMCP("TA GuruLabs VoiceForge Lite")


def safe_file(relative_path: str, must_exist: bool = True) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise ValueError("Use a relative path inside the VoiceForge data directory.")
    target = (ROOT / relative_path).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("Path outside VoiceForge data directory.")
    if must_exist and not target.is_file():
        raise FileNotFoundError(relative_path)
    return target


def run(command: list[str], timeout: int = 180) -> None:
    subprocess.run(command, check=True, timeout=timeout, capture_output=True, text=True)


@MCP.tool()
def capabilities() -> dict:
    """Show locally installed tools, without accessing external services."""
    return {
        "cost_policy": "No paid API calls; local execution only.",
        "piper_available": bool(shutil.which("piper")) and bool(os.getenv("PIPER_MODEL")),
        "ffmpeg_available": bool(shutil.which("ffmpeg")),
        "transcription_dependency": "Install faster-whisper separately; initial model download requires internet.",
        "storage": str(ROOT),
    }


@MCP.tool()
def speak(text: str, filename: str = "") -> str:
    """Generate a WAV narration locally with Piper. Requires PIPER_MODEL."""
    if not text.strip() or len(text) > 2500:
        raise ValueError("Speech text must contain between 1 and 2500 characters.")
    model = Path(os.environ.get("PIPER_MODEL", "")).expanduser()
    if not shutil.which("piper") or not model.is_file():
        raise RuntimeError("Install Piper and set PIPER_MODEL to an existing local voice model.")
    name = filename or f"narration-{uuid.uuid4().hex[:12]}.wav"
    if not re.fullmatch(r"[A-Za-z0-9_-]+\.wav", name):
        raise ValueError("Output filename must be a simple .wav filename.")
    output = safe_file("narration/" + name, must_exist=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["piper", "--model", str(model), "--output_file", str(output)],
                   input=text, encoding="utf-8", capture_output=True, check=True, timeout=180)
    return str(output)


@MCP.tool()
def prepare_audio(source: str, filename: str = "") -> str:
    """Normalise loudness and trim silence using local FFmpeg; never overwrite source."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError("Install ffmpeg before preparing audio.")
    src = safe_file(source)
    if src.suffix.lower() not in {".wav", ".mp3", ".m4a", ".flac", ".ogg"}:
        raise ValueError("Unsupported audio input.")
    name = filename or f"prepared-{uuid.uuid4().hex[:12]}.wav"
    if not re.fullmatch(r"[A-Za-z0-9_-]+\.wav", name):
        raise ValueError("Output filename must be a simple .wav filename.")
    output = safe_file("prepared/" + name, must_exist=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(src),
         "-af", "silenceremove=start_periods=1:start_silence=0.15:start_threshold=-45dB,"
                "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ac", "1", "-ar", "44100", str(output)])
    return str(output)


@MCP.tool()
def transcribe(source: str, language: str = "en") -> str:
    """Transcribe a local file offline after the faster-whisper model is cached."""
    src = safe_file(source)
    if src.suffix.lower() not in {".wav", ".mp3", ".m4a", ".flac", ".ogg"}:
        raise ValueError("Unsupported audio input.")
    try:
        from faster_whisper import WhisperModel
    except ImportError as e:
        raise RuntimeError("Install faster-whisper to use transcription.") from e
    # Set local_files_only=True so running this tool cannot fetch or pay for a hosted model.
    model = WhisperModel("tiny", device="cpu", compute_type="int8", local_files_only=True)
    segments, _ = model.transcribe(str(src), language=language)
    return " ".join(segment.text.strip() for segment in segments).strip()


@MCP.tool()
def add_asset(asset_id: str, path: str, category: str, rights_note: str) -> dict:
    """Catalogue an audio file for review; MCP tools cannot approve publication."""
    return register_asset(asset_id, path, category, rights_note, approved_for_publication=False)


MCP.tool()(list_assets)

if __name__ == "__main__":
    MCP.run(transport="stdio")
