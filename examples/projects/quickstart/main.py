"""FastPix quickstart: load credentials from .env and list your media."""
from __future__ import annotations

import json
import os

from fastpix_python import Fastpix, models

from common import load_local_env, require_env


def main() -> None:
    load_local_env()
    username = require_env("FASTPIX_USERNAME")
    password = require_env("FASTPIX_PASSWORD")
    server_url = os.getenv("FASTPIX_SERVER_URL")  # optional override

    with Fastpix(
        security=models.Security(username=username, password=password),
        server_url=server_url,
    ) as fastpix:
        res = fastpix.manage_videos.list_media(limit=10, offset=1, order_by="desc")
        print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2, default=str))


if __name__ == "__main__":
    main()
