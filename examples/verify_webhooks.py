"""Verify a FastPix webhook signature before trusting the payload.

FastPix signs the raw request body with your webhook Signing Secret (Dashboard
> Webhooks) and sends it as a Base64 HMAC-SHA256 in the `FastPix-Signature`
header. The Signing Secret is itself Base64-encoded — sign with its decoded
bytes as the key. Verify the body exactly as received: parsing and
re-serializing changes the bytes and the signature will never match.
"""

import base64
import hashlib
import hmac
import os


def is_valid_signature(raw_body: bytes, signature: str) -> bool:
    secret = os.getenv("FASTPIX_WEBHOOK_SECRET")
    if not secret or not signature:
        return False
    key = base64.b64decode(secret)  # Signing Secret is Base64; use its decoded bytes.
    expected = base64.b64encode(hmac.new(key, raw_body, hashlib.sha256).digest()).decode()
    return hmac.compare_digest(expected, signature)  # constant-time compare


def main() -> None:
    os.environ.setdefault("FASTPIX_WEBHOOK_SECRET", base64.b64encode(b"demo-secret").decode())
    raw_body = b'{"type":"video.media.ready","data":{"id":"abc-123"}}'
    key = base64.b64decode(os.environ["FASTPIX_WEBHOOK_SECRET"])
    signature = base64.b64encode(hmac.new(key, raw_body, hashlib.sha256).digest()).decode()

    print("verified" if is_valid_signature(raw_body, signature) else "rejected")


if __name__ == "__main__":
    main()
