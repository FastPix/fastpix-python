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
    res = fastpix.playlist.create_a_playlist(
        name="playlist name",
        reference_id="a5",
        type_="smart",
        description="This is a playlist",
        play_order="createdDate DESC",
        limit=20,
        metadata={
            "created_date": models.DateRange(
                start_date="2024-11-11",
                end_date="2024-12-12",
            ),
            "updated_date": models.DateRange(
                start_date="2024-11-11",
                end_date="2024-12-12",
            ),
        },
    )

    
    print(json.dumps(to_api_payload(res), indent=2))

