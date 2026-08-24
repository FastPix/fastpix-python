# FastPix Quickstart

A tiny, self-contained project showing how to use the FastPix Python SDK with a
`.env` file. Copy this folder as a starting point for your own app.

## Run

```bash
cd examples/projects/quickstart

# 1. Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Add your credentials
cp .env.example .env

# 3. Run — lists your media
python main.py
```

> You can use any virtual environment tool — [uv](https://docs.astral.sh/uv/),
> virtualenv, conda, pipenv, etc.

`main.py` loads credentials from `.env` (via the zero-dependency `common.py`
loader) and calls `list_media`. Swap in any call from the top-level
[`examples/`](../..) to explore other endpoints.

Web-framework integrations (Django, Flask, FastAPI) belong alongside this folder
under [`examples/projects/`](..).
