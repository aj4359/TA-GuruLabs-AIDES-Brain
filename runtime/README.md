# JingWu 60-second editor: execution instructions

Files:
- `astra_adapter.py`: GPT-6.2 Astra Responses API editorial decisions, disabled by default.
- `ffmpeg_renderer.py`: clips and soundtrack to actual MP4, FFprobe verification.
- `test_astra_adapter.py`: budget gates.
- `ASTRA_CODEX_VIDEO_INTEGRATION.md` in playbooks: complete engineering plan.

Example manifest (local paths refer to files on the rendering computer):

```json
{
  "brief": "I Need It Tonight: beat-matched nightclub montage; preserve approved lead",
  "clips": [{"id":"opening", "path":"/media/intro.mp4", "duration":65}],
  "music": "/media/song.mp3"
}
```

Execute from `runtime/` with Python 3.11+ and ffmpeg/ffprobe installed:

```python
import json
from astra_adapter import create_edit_plan
from ffmpeg_renderer import render

manifest=json.load(open("my_manifest.json"))
plan=create_edit_plan(manifest, allow_paid=True)
print(render(manifest,plan,"demo.mp4"))
```

Live API invocation requires server-only OPENAI_API_KEY, AI_ENABLED=true,
and AI_MAX_COST_GBP_PER_JOB > 0. This numeric gate does not itself limit real API
charges: set a hard project limit/budget externally and monitor token usage.
Do not activate until a founder-approved spend ceiling exists.

No credentials, working user footage, render backend deployment, or API session
are configured by committing these files. The current renderer is a basic
trim-and-concatenate MVP, not a generative animation engine. It does not validate
resemblance, musical beat sync, compositing, or creative story quality.
