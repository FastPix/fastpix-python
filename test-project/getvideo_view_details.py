import json
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username="34539a06-62d4-4a60-95ca-99dfe8679487",
        password="da6bc2a8-58a8-4703-8332-0f469ce69d06",
    ),
) as fastpix:

    res = fastpix.views.get_video_view_details(view_id="64bb9e7c-bf00-4939-b145-4008aca47fc7")

    # Handle response - convert to JSON format
    print(json.dumps(res.model_dump(by_alias=True), indent=2))