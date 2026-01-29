import json
from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
     username="your-access-token",
     password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.playlist.delete(playlist_id="your-playlist-id")

    # Handle response
print(json.dumps(res.model_dump(by_alias=True), indent=2))