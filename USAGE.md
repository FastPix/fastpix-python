<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(inputs=[
        {
            "type": "video",
            "url": "https://static.fastpix.io/sample.mp4",
        },
    ], access_policy="public", metadata={
        "key1": "value1",
    }, subtitles={
        "language_name": "english",
        "metadata": {
            "key1": "value1",
        },
        "language_code": "en",
    }, mp4_support="capped_4k", source_access=True, optimize_audio=True, max_resolution="1080p", summary={
        "generate": True,
    }, chapters=True, named_entities=True)

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
            username = "your-access-token",
            password = "secret-key",
        ),
    ) as fastpix:

        res = await fastpix.input_video.create_media_async(inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.io/sample.mp4",
            },
        ], access_policy="public", metadata={
            "key1": "value1",
        }, subtitles={
            "language_name": "english",
            "metadata": {
                "key1": "value1",
            },
            "language_code": "en",
        }, mp4_support="capped_4k", source_access=True, optimize_audio=True, max_resolution="1080p", summary={
            "generate": True,
        }, chapters=True, named_entities=True)

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->