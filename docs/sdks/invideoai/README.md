# InVideoAI

## Overview

### Available Operations

* [update_chapters](#update_chapters) - Generate video chapters

## update_chapters

This endpoint enables you to generate chapters for an existing media file.

#### How it works
1. Make a `PATCH` request to this endpoint, replacing `<mediaId>` with the ID of the media for which you want to generate chapters.
2. Include the `chapters` parameter in the request body to enable.
3. The response contains the updated media data, confirming the changes made.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaaichaptersready">video.mediaAI.chapters.ready</a> webhook event to track and notify about the chapters generation.

**Use case:** This is particularly useful when a user uploads a video and later decides to enable chapters without re-uploading the entire video.

Related guide: <a href="https://docs.fastpix.io/docs/generate-video-chapters">Video chapters</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-chapters" method="patch" path="/on-demand/{mediaId}/chapters" -->
```python
import os
import json

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

   
    res = fastpix.in_video_ai.update_chapters(media_id="your-media-id", chapters=True )
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                      | Type                                                                                                           | Required                                                                                                       | Description                                                                                                    | Example                                                                                                        |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                     | *str*                                                                                                          | :heavy_check_mark:                                                                                             | The unique identifier assigned to the media when created. The value must be a valid UUID.<br/>                 | your-media-id                                                                                                  |
| `chapters`                                                                                                     | *Optional[bool]*                                                                                               | :heavy_minus_sign:                                                                                             | Enable or disable the chapters feature for the media. Set to `true` to enable chapters or `false` to disable.<br/> | true                                                                                                           |
| `retries`                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                               | :heavy_minus_sign:                                                                                             | Configuration to override the default retry behavior of the client.                                            |                                                                                                                |

### Response

**[models.UpdateMediaChaptersResponse](../../models/updatemediachaptersresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |