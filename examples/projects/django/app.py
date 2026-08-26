"""Minimal single-file Django app for FastPix: signed upload URLs + webhooks.

    POST /uploads   create a signed direct-upload URL (the browser PUTs the file to it)
    POST /webhooks  verify the FastPix-Signature header, then react to the event

Sync request cycle: Django's classic (WSGI) views are synchronous, so we call
the SDK's blocking methods directly. That is correct and safe — the call just
occupies the worker thread until FastPix responds (like any outbound HTTP call).
Two things to keep in mind:
  * Don't call the SDK's ``*_async`` methods from a sync view (there is no event
    loop). If you use Django async views instead, either use those ``*_async``
    methods with ``await``, or wrap the sync ones in ``asgiref.sync.sync_to_async``
    so they don't block the loop.
  * A blocking call ties up one worker for its duration; size your worker pool
    accordingly, or move heavy work to a task queue.

Run:
    pip install -r requirements.txt
    python app.py runserver
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

settings.configure(
    DEBUG=os.environ.get("DJANGO_DEBUG") == "1",
    ALLOWED_HOSTS=os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(","),
    ROOT_URLCONF=__name__,
    SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY", "dev-only-not-a-real-secret"),
)

from fastpix_python import Fastpix, models  # noqa: E402  (after settings.configure)


def client() -> Fastpix:
    return Fastpix(
        security=models.Security(
            username=os.environ["FASTPIX_USERNAME"],
            password=os.environ["FASTPIX_PASSWORD"],
        ),
    )


# CSRF-exempt is safe here only because this is a token-authenticated JSON API
# (no browser cookie, so CSRF does not apply). Add your own auth check below —
# this endpoint mints upload URLs and must NOT be left open in production.
@csrf_exempt
def create_upload(request):
    """Return a signed URL your frontend can PUT a file to directly."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    # Blocking SDK call inside a sync view — fine in a WSGI worker.
    with client() as fastpix:
        res = fastpix.input_video.direct_upload_video_media(request={
            "cors_origin": "*",
            "push_media_settings": {"access_policy": "public"},
        })
    return JsonResponse({"uploadId": res.data.upload_id, "url": res.data.url})


def is_valid_signature(raw_body: bytes, signature: str | None) -> bool:
    secret = os.getenv("FASTPIX_WEBHOOK_SECRET")
    if not secret or not signature:
        return False
    key = base64.b64decode(secret)  # Signing Secret is Base64; use its decoded bytes.
    expected = base64.b64encode(hmac.new(key, raw_body, hashlib.sha256).digest()).decode()
    return hmac.compare_digest(expected, signature)


# CSRF-exempt is required and safe here: webhooks are server-to-server (no browser
# cookie), and every request is authenticated by the HMAC signature check below.
# CSRF only defends cookie-based form posts — which this is not.
@csrf_exempt
def webhooks(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    raw = request.body  # raw bytes — read and verify before parsing
    if not is_valid_signature(raw, request.headers.get("FastPix-Signature")):
        return HttpResponse("Invalid signature.", status=401)

    event = json.loads(raw)
    if event.get("type") == "video.media.ready":
        print("media ready:", event.get("data", {}).get("id"))
    elif event.get("type") == "video.media.failed":
        print("media failed:", event.get("data", {}).get("id"))
    # Acknowledge fast; FastPix retries on any non-2xx response.
    return JsonResponse({"received": True})


urlpatterns = [
    path("uploads", create_upload),
    path("webhooks", webhooks),
]


if __name__ == "__main__":
    execute_from_command_line(sys.argv)
