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
    res = fastpix.playlist.add_media_to_playlist(
        playlist_id="1a288073-4c88-46a0-bc9b-c490738e9670",
        media_ids=["a9f446cd-c401-4e5e-bc40-75d36300cce1","5fb72062-ea92-4276-abcb-4f9c4ccc65b7"],
    )

    
    print(json.dumps(to_api_payload(res), indent=2))
