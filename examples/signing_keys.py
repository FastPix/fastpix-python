"""Signing keys: create, list, fetch, and delete a signing key (used to sign
JWTs for secure playback). The private key is only returned once, at creation."""

import json
import os

from fastpix_python import Fastpix, models


def _print(label, res):
    print(f"\n=== {label} ===")
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2, default=str))


def main():
    fastpix = Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_USERNAME"),
            password=os.getenv("FASTPIX_PASSWORD"),
        ),
    )
    with fastpix:
        created = fastpix.signing_keys.create_signing_key()
        _print("create signing key", created)
        key_id = created.data.id

        _print("list signing keys", fastpix.signing_keys.list_signing_keys(limit=10, offset=1))
        _print("get signing key", fastpix.signing_keys.get_signing_key_by_id(signing_key_id=key_id))
        _print("delete signing key", fastpix.signing_keys.delete_signing_key(signing_key_id=key_id))


if __name__ == "__main__":
    main()
