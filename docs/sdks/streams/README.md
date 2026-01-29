# Streams

## Overview

### Available Operations

* [delete](#delete) - Delete a stream

## delete

Permanently deletes a specified live stream from the workspace. If the stream is active, the encoder is disconnected and ingestion stops immediately. This action is irreversible, and any future playback attempts fail as a result.

  Provide the `streamId` in the request to terminate active connections and remove the stream from the workspace. You can further look for <a href="https://docs.fastpix.io/docs/live-events#videolive_streamdeleted">video.live_stream.deleted</a> webhook to notify your system about the status.

  #### Example

  For an online concert platform, a trial stream was mistakenly made public. The event manager deletes the stream before the concert begins to avoid confusion among viewers. 

  Related guide: <a href="https://docs.fastpix.io/docs/manage-streams">Manage streams</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-live-stream" method="delete" path="/live/streams/{streamId}" -->
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

    res = fastpix.streams.delete(stream_id="your-stream-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                           | Type                                                                                | Required                                                                            | Description                                                                         | Example                                                                             |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `stream_id`                                                                         | *str*                                                                               | :heavy_check_mark:                                                                  | Upon creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                                      |
| `retries`                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                    | :heavy_minus_sign:                                                                  | Configuration to override the default retry behavior of the client.                 |                                                                                     |

### Response

**[models.DeleteLiveStreamResponse](../../models/deletelivestreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |