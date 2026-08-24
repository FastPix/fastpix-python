"""Tests for the example scripts in examples/.

- Every example is well-formed: compiles, reads credentials from env vars,
  and is guarded by __main__ so importing is safe.
- The webhook verifier has real logic, so it gets a real unit test.
"""

import ast
import base64
import hashlib
import hmac
import importlib.util
import re
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
# Example scripts at the examples/ root.
# (projects/ has its own runnable structure and is excluded.)
EXAMPLE_FILES = sorted(EXAMPLES_DIR.glob("*.py"))
HARDCODED_SECRET = re.compile(r'(username|password)\s*=\s*"[0-9a-fA-F-]{20,}"')

assert EXAMPLE_FILES, f"no example scripts found in {EXAMPLES_DIR}"


@pytest.mark.parametrize("path", EXAMPLE_FILES, ids=lambda p: p.name)
def test_example_is_wellformed(path):
    src = path.read_text(encoding="utf-8")
    ast.parse(src)
    assert not HARDCODED_SECRET.search(src), "example has hardcoded credentials"
    assert '__name__ == "__main__"' in src, "example missing __main__ guard"


def _load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_verify_webhook_signature(monkeypatch):
    wh = _load(EXAMPLES_DIR / "verify_webhooks.py")
    secret = base64.b64encode(b"test-secret").decode()  # FastPix secrets are Base64
    monkeypatch.setenv("FASTPIX_WEBHOOK_SECRET", secret)
    payload = b'{"type":"video.media.ready"}'
    # A valid signature: HMAC over the raw body, keyed with the decoded secret.
    signature = base64.b64encode(
        hmac.new(base64.b64decode(secret), payload, hashlib.sha256).digest()
    ).decode()

    assert wh.is_valid_signature(payload, signature) is True
    assert wh.is_valid_signature(payload, "not-the-signature") is False
    # Tampered body must fail against a signature made for the original body.
    assert wh.is_valid_signature(payload + b"x", signature) is False
