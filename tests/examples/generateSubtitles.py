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


    
    res = fastpix.manage_videos.generate_subtitle_track(media_id="cece130e-3d96-4f94-99f7-0c7eef84e70f", track_id="b1bd90ce-d7cf-4d48-8686-0023a4a17e18", language_name="Spanish", language_code="es-ES", metadata={
        "key1": "value1",
    })
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

