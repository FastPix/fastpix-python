import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="1b92c0d6-5548-4642-b13e-4bb7d77dbaf4",
        password="ff32012b-ec02-40ca-b0d4-711d81537e73",
    ),
) as fastpix:
    res = fastpix.playlist.change_media_order_in_playlist(
        playlist_id="fbd59e4d-2d77-4f11-be38-c19e3a931919",
        media_ids=[
            "cefe817b-046e-4d78-b2a8-800f2d2ad6cf",
            "238b2f41-3a78-4921-b6ea-e0846059873f",
            "5737f4ca-c0f9-46a9-936a-2b2515aa6be6"
        ],
    )

    
    print(json.dumps(to_api_payload(res), indent=2))

