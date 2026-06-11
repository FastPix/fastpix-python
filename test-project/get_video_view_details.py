import json
import os
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username=os.getenv("FASTPIX_ACCESS_TOKEN"),
        password=os.getenv("FASTPIX_SECRET_KEY"),
    ),
) as fastpix:

    res = fastpix.views.get_video_view_details(view_id="view-id")

    # Handle response - convert to JSON format
    print(json.dumps(res.model_dump(by_alias=True), indent=2))