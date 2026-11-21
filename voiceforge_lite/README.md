# VoiceForge Lite (prototype — NOT deployed)

A minimal **local-first** MCP service for TA GuruLabs. This is an independently built interface using open tools, **not** a copy of ElevenLabs software or models. No ElevenLabs credentials, hosted model requests, or paid APIs.

## Included tools
- `capabilities`: discover locally available utilities.
- `speak`: Piper text-to-speech, requiring an explicitly installed local voice model.
- `prepare_audio`: trim leading silence and normalise speech using FFmpeg, retaining the original.
- `transcribe`: local faster-whisper speech-to-text (requires an already-cached tiny model).

**Not included yet:** sound-effect generation, voice cloning, licensing automation, website deployment, live voice conversations, or upload of private files to third parties. A sound library can initially be a folder of original or appropriately licensed effects.

## Installation (developer machine, Windows supported)
1. Create a virtual environment with Python 3.10+.
2. Install `mcp` (and optionally `faster-whisper`): `pip install mcp faster-whisper`.
3. Install FFmpeg and Piper separately from their official distribution sources. Check their licences and the licences of specific voice models and assets before any commercial release.
4. Download an appropriately licensed Piper voice model to your own machine, then set `PIPER_MODEL` to its path.
5. Set `VOICEFORGE_DATA_DIR` to a local folder with sufficient free space (preferably D: on Windows if C: is full).
6. Place input audio files under that folder; run `python -m voiceforge_lite.server` from the repository root.
7. Configure the local MCP client to run the above as a stdio process. Never expose this prototype directly to the public internet.

Example Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install mcp faster-whisper
$env:VOICEFORGE_DATA_DIR = "D:\VoiceForge"
$env:PIPER_MODEL = "D:\VoiceForge\models\voice.onnx"
python -m voiceforge_lite.server
```

## Budget and safety gates
- **Hard rule:** no paid API calls and no automatic subscriptions.
- The MCP server only operates on a designated folder. It never deletes original audio.
- Speech input is capped at 2,500 characters per request.
- No automatic voice cloning; only use voices and assets whose licences permit intended use.
- The faster-whisper `tiny` model must be cached before the server runs transcription, otherwise the call fails rather than downloading anything.
- Local processing uses CPU, disk and electricity; £0 means no additional software/API charges, not literally zero computing cost.
- Keep human review for commercial release, especially pronunciation, script accuracy, sound mix and licensing.
- Prototype is untested in a production environment. Run local tests before connecting an AIDE.

## Recommended first test
Run `capabilities`. Then use a short, original 30-second TA GuruLabs script for `speak`, manually listen and check the file before integrating into a podcast or the Sicario workflow.
