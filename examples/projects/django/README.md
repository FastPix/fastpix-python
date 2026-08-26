# FastPix + Django (sync)

A minimal single-file Django app with two views:

- `POST /uploads` — creates a **signed direct-upload URL**; your frontend PUTs
  the file straight to it (the file never passes through your server).
- `POST /webhooks` — verifies the `FastPix-Signature` header, then reacts to the
  event (e.g. `video.media.ready`).

Everything lives in [`app.py`](app.py) (settings, URLs, views) to keep the
example short. In a real project these become `settings.py`, `urls.py`, and an
app's `views.py` — the view code is identical.

## Run

```bash
# 1. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Add your credentials + webhook secret
cp .env.example .env
set -a; source .env; set +a

# 3. Start the server
python app.py runserver
```

> You can use any virtual environment tool — [uv](https://docs.astral.sh/uv/),
> virtualenv, conda, pipenv, etc.

## Create an upload, then send the file

`POST /uploads` hands you a signed URL. The client uploads the file straight to
that URL, so the bytes never touch your server, and once it finishes FastPix
processes the video and sends the `video.media.ready` webhook.

We keep this example simple and just PUT the whole file in one request — good
enough for small files. For larger ones you'll usually want a resumable upload
(chunked, with retries and progress); the same signed URL supports that too.

```bash
# 1. Ask your app for a signed upload URL
UPLOAD_URL=$(
  curl -s -X POST localhost:8000/uploads \
    | python3 -c "import sys, json; print(json.load(sys.stdin)['url'])"
)

# 2. Upload the file straight to it
curl -X PUT --upload-file video.mp4 \
  -H "Content-Type: video/mp4" \
  "$UPLOAD_URL"
```

Or from the browser, straight off a file input:

```js
// 1. Ask your app for a signed upload URL
const res = await fetch("/uploads", { method: "POST" });
const { url } = await res.json();

// 2. Upload the file straight to it
await fetch(url, {
  method: "PUT",
  headers: { "Content-Type": file.type || "application/octet-stream" },
  body: file,
});
```

We create uploads with `corsOrigin: "*"` so the browser can PUT from anywhere —
lock that down before you ship. The docs go deeper (resumable included):
https://fastpix.com/docs/upload-videos/upload-videos-from-device

Point a FastPix webhook at `https://<your-host>/webhooks` (use a tunnel like
ngrok for local testing).

## Calling the SDK from Django's synchronous request cycle — any issue?

No. Classic Django views (WSGI) are synchronous, and the SDK's blocking methods
are exactly what you want there: the call occupies the worker thread until
FastPix responds, like any outbound HTTP request. Keep in mind:

- **Don't** call the SDK's `*_async` methods from a sync view — there's no event
  loop to await them. Use the plain (sync) methods, as shown here.
- If you use **async** Django views instead, either call the `*_async` SDK
  methods with `await`, or wrap the sync ones in `asgiref.sync.sync_to_async` so
  they don't block the event loop.
- A blocking call holds one worker for its duration — size your worker pool for
  it, or offload heavy work to a task queue (Celery/RQ).
- The webhook view reads `request.body` (raw bytes) and is `@csrf_exempt`, since
  the POST comes from FastPix, not a browser form.
