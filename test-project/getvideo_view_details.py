import json
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.views.get_video_view_details(view_id="your-view-id")

    # Handle response - convert to JSON format
    print(json.dumps(res.model_dump(by_alias=True), indent=2))