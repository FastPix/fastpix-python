import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlist.delete(playlist_id="your-playlist-id")

    
    print(json.dumps(to_api_payload(res), indent=2))
