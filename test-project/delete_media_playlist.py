import json
import os
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username=os.getenv("FASTPIX_ACCESS_TOKEN"),
        password=os.getenv("FASTPIX_SECRET_KEY"),
    ),
) as fastpix:

    res = fastpix.playlist.delete_media(
        playlist_id="your-playlist-id",
        media_ids=[
            "your-media-id-1",
            "your-media-id-2",
        ],
    )

    # Handle response
    # Handle response - convert to JSON format
    print(json.dumps(res.model_dump(by_alias=True), indent=2))