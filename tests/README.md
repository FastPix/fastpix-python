# Tests

Two layers: fast offline pytest suites, and a live validation harness that
exercises every endpoint against a real workspace.

## Offline tests (no credentials needed)

```bash
pip install -e . pytest
pytest tests/test_models.py tests/test_async_errors.py tests/test_return_annotations.py tests/test_examples.py
```

- `test_models.py` — model contract tests (field types, aliases, defaults,
  serialized body shapes). Pure pydantic, no network.
- `test_async_errors.py` — mocked-transport checks that sync and async methods
  raise typed errors on failed responses.
- `test_return_annotations.py` — asserts every resource method's declared return
  type is the response class it actually unmarshals.
- `test_examples.py` — sanity checks on `examples/` (compiles, has a
  `__main__` guard, no hardcoded credentials).

## Live validation harness

Calls every endpoint through the SDK against a real FastPix workspace and
validates each response against the OpenAPI spec.

### Setup

1. Copy `tests/.env.example` to `tests/.env` and fill in your credentials.
2. Place the OpenAPI spec at the repo root as `openapi.yaml`.
3. Install dependencies (the response validator runs in a small Node sidecar):

```bash
pip install -e . httpx pyyaml
npm install
```

### Run

```bash
set -a; source tests/.env; set +a
python -m tests.validate_get_endpoints      # read-only endpoints
python -m tests.validate_non_get_endpoints  # creates, updates, deletes (cleans up after itself)
```

Each run writes a markdown report and per-endpoint response artifacts into
`tests/` (gitignored). Endpoints needing existing resource IDs read them from
`tests/get_endpoints_fixtures.json`; non-GET request bodies come from
`tests/non_get_endpoints_fixtures.json`.

## Utilities

- `check_broken_links.py` — verifies every external URL in the repo's markdown
  docs resolves (`pip install httpx`, then `python tests/check_broken_links.py`).
