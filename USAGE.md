<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(inputs=[
        {
            "type": "video",
            "url": "https://static.fastpix.io/fp-sample-video.mp4",
        },
    ], metadata={
        "key1": "value1",
    }, drm_configuration_id="your-drm-configuration-id", title="My Video Title", creator_id="your-creator-id", subtitles={
        "language_name": "english",
        "metadata": {
            "key1": "value1",
        },
        "language_code": "en",
    }, access_policy="public", mp4_support="capped_4k", source_access=True, optimize_audio=True, max_resolution="1080p", media_quality="standard", chapters=True, named_entities=True)

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from fastpix_python import Fastpix, models

async def main():

    async with Fastpix(
        security=models.Security(
            username="your-access-token",
            password="your-secret-key",
        ),
    ) as fastpix:

        res = await fastpix.input_video.create_media_async(inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.io/fp-sample-video.mp4",
            },
        ], metadata={
            "key1": "value1",
        }, drm_configuration_id="your-drm-configuration-id", title="My Video Title", creator_id="your-creator-id", subtitles={
            "language_name": "english",
            "metadata": {
                "key1": "value1",
            },
            "language_code": "en",
        }, access_policy="public", mp4_support="capped_4k", source_access=True, optimize_audio=True, max_resolution="1080p", media_quality="standard", chapters=True, named_entities=True)

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->
