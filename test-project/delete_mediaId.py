import json
import os
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username=os.getenv("FASTPIX_ACCESS_TOKEN"),
        password=os.getenv("FASTPIX_SECRET_KEY"),
    ),
) as fastpix:

    res = fastpix.videos.delete(media_id="your-media-id")

    # Handle response - convert to JSON format
    print(json.dumps(res.model_dump(by_alias=True), indent=2))
