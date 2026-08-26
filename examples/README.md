# FastPix Python SDK — Examples

Each example is an **end-to-end flow** that groups related methods into one
realistic sequence (create → use → clean up), rather than a single call.
For single-method usage and parameter reference, see [`docs/sdks/`](../docs/sdks).

## Setup

```bash
pip install fastpix-python
export FASTPIX_USERNAME="your-access-token"
export FASTPIX_PASSWORD="your-secret-key"
```

Credentials come from your [FastPix Dashboard](https://dashboard.fastpix.com)
(Access Token = username, Secret Key = password). You can also copy
[`.env.example`](.env.example) to `.env` and load it in your shell.

Run any flow:

```bash
python examples/media_lifecycle.py
```

Flows that create a resource clean it up at the end. A few (`playlists.py`) use
placeholder ids marked at the top of the file — replace them with real ids.

## Flows

| Flow | Methods it chains |
| --- | --- |
| [`media_lifecycle.py`](media_lifecycle.py) | create → get → list → update → source-access → mp4-support → delete media |
| [`direct_upload.py`](direct_upload.py) | create upload URL → list uploads → cancel upload |
| [`playback_ids.py`](playback_ids.py) | create playback id → domain & user-agent restrictions → delete |
| [`playlists.py`](playlists.py) | create → add/reorder/remove media → get/list → update → delete |
| [`media_tracks.py`](media_tracks.py) | add audio track → update → generate subtitles → delete track |
| [`live_streaming.py`](live_streaming.py) | create stream → playback id → update → enable/disable/complete → delete |
| [`simulcasting.py`](simulcasting.py) | create stream → add simulcast target → update → delete |
| [`signing_keys.py`](signing_keys.py) | create → list → get → delete signing key |
| [`ai_features.py`](ai_features.py) | summary → chapters → moderation → named entities → get summary |
| [`verify_webhooks.py`](verify_webhooks.py) | verify a `FastPix-Signature` webhook (offline, no API call) |

## Projects

Framework-style projects live in [`projects/`](projects):

- [`projects/quickstart`](projects/quickstart) — smallest possible script-style project
- [`projects/fastapi`](projects/fastapi) — async FastAPI app: signed upload URLs + webhook handling
- [`projects/django`](projects/django) — sync Django app: signed upload URLs + webhook handling
