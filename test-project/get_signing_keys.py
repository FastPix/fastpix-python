from __future__ import annotations

import json
import os

from fastpix_python import Fastpix

from common import load_local_env, require_env


def main() -> None:
    load_local_env()

    require_env("FASTPIX_USERNAME")
    require_env("FASTPIX_PASSWORD")

    server_url = os.getenv("FASTPIX_SERVER_URL")
    s = Fastpix(server_url=server_url)

    # Read-only example: list signing keys
    res = s.signing_keys.list_signing_keys(limit=10, offset=1)

    payload = res.model_dump(by_alias=True) if hasattr(res, "model_dump") else res  # type: ignore[attr-defined]
    print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    main()

