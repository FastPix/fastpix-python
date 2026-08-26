"""Minimal async FastAPI app for FastPix: signed upload URLs + webhooks.

    POST /uploads   create a signed direct-upload URL (the browser PUTs the file to it)
    POST /webhooks  verify the FastPix-Signature header, then react to the event

The SDK ships async methods (``*_async``), so this uses them directly with
``async with Fastpix(...)`` — no thread offloading needed.

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

from fastapi import FastAPI, Request, Response
from fastpix_python import Fastpix, models

app = FastAPI()


def client() -> Fastpix:
    return Fastpix(
        security=models.Security(
            username=os.environ["FASTPIX_USERNAME"],
            password=os.environ["FASTPIX_PASSWORD"],
        ),
    )


@app.post("/uploads")
async def create_upload():
    """Return a signed URL your frontend can PUT a file to directly."""
    async with client() as fastpix:
        res = await fastpix.input_video.direct_upload_video_media_async(request={
            "cors_origin": "*",
            "push_media_settings": {"access_policy": "public"},
        })
    return {"uploadId": res.data.upload_id, "url": res.data.url}


def is_valid_signature(raw_body: bytes, signature: str | None) -> bool:
    secret = os.getenv("FASTPIX_WEBHOOK_SECRET")
    if not secret or not signature:
        return False
    key = base64.b64decode(secret)  # Signing Secret is Base64; use its decoded bytes.
    expected = base64.b64encode(hmac.new(key, raw_body, hashlib.sha256).digest()).decode()
    return hmac.compare_digest(expected, signature)


@app.post("/webhooks")
async def webhooks(request: Request):
    raw = await request.body()  # raw bytes — verify before parsing
    if not is_valid_signature(raw, request.headers.get("FastPix-Signature")):
        return Response("Invalid signature.", status_code=401)

    event = await request.json()
    if event.get("type") == "video.media.ready":
        print("media ready:", event.get("data", {}).get("id"))
    elif event.get("type") == "video.media.failed":
        print("media failed:", event.get("data", {}).get("id"))
    return {"received": True}
