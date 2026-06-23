import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
username="1b92c0d6-5548-4642-b13e-4bb7d77dbaf4",
password="ff32012b-ec02-40ca-b0d4-711d81537e73",
    ),
) as fastpix:

    res = fastpix.simulcast_stream.create_simulcast_of_stream(stream_id="fec5854f0cc5c10d47a8c0b9c39628ae", url="rtmp://hyd01.contribute.live-video.net/app/", stream_key="live_1012464221_DuM8W004MoZYNxQEZ0czODgfHCFBhk", metadata={
        "livestream_name": "Tech-Connect Summit",
    })

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))
