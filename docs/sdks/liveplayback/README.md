# LivePlayback

## Overview

### Available Operations

* [create_playback_id](#create_playback_id) - Create a playbackId
* [delete_playback_id](#delete_playback_id) - Delete a playbackId
* [get_playback_id_details](#get_playback_id_details) - Get playbackId details

## create_playback_id

Generates a new playback ID for the live stream, allowing viewers to access the stream through this ID. The playback ID can be shared with viewers for direct access to the live broadcast. 

  By calling this endpoint with the `streamId`, FastPix returns a unique `playbackId`, which can be used to stream the live content. 

  #### Example

  A media platform needs to distribute a unique playback ID to users for an exclusive live concert. The platform can also embed the stream on various partner websites.

### Example Usage

<!-- UsageSnippet language="python" operationID="create-playbackId-of-stream" method="post" path="/live/streams/{streamId}/playback-ids" -->
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

    res = fastpix.live_playback.create_playback_id(stream_id="your-stream-id", access_policy="public")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                            | Type                                                                                 | Required                                                                             | Description                                                                          | Example                                                                              |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `stream_id`                                                                          | *str*                                                                                | :heavy_check_mark:                                                                   | After creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                                       |
| `access_policy`                                                                      | [Optional[models.BasicAccessPolicy]](../../models/basicaccesspolicy.md)              | :heavy_minus_sign:                                                                   | Basic access policy for media content                                                |                                                                                      |
| `retries`                                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                     | :heavy_minus_sign:                                                                   | Configuration to override the default retry behavior of the client.                  |                                                                                      |

### Response

**[models.CreatePlaybackIDOfStreamResponse](../../models/createplaybackidofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## delete_playback_id

Deletes a previously created playback ID for a live stream.This prevents new viewers from accessing the stream using the playback ID, while current viewers can continue watching for a short period before the connection ends. FastPix deletes the ID and ensures the new playback request fails.

#### Example
A streaming service wants to prevent new users from joining a live stream that is nearing its end. The host can delete the playback ID to ensure no one can join the stream or replay it once it ends.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-playbackId-of-stream" method="delete" path="/live/streams/{streamId}/playback-ids" -->
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

    res = fastpix.live_playback.delete_playback_id(
        stream_id="your-stream-id",
        playback_id="your-playback-id",
    )

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                           | Type                                                                                | Required                                                                            | Description                                                                         | Example                                                                             |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `stream_id`                                                                         | *str*                                                                               | :heavy_check_mark:                                                                  | Upon creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                                      |
| `playback_id`                                                                       | *str*                                                                               | :heavy_check_mark:                                                                  | Unique identifier for the playbackId                                                | your-playback-id                                                                    |
| `retries`                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                    | :heavy_minus_sign:                                                                  | Configuration to override the default retry behavior of the client.                 |                                                                                     |

### Response

**[models.DeletePlaybackIDOfStreamResponse](../../models/deleteplaybackidofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_playback_id_details

Retrieves details for an existing playback ID. When you provide the playbackId returned from a previous stream or playback creation request, FastPix returns the associated playback information, including the access policy.

#### Example
A developer needs to confirm the access policy of the playback ID to ensure whether the stream is public or private for viewers.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-live-stream-playback-id" method="get" path="/live/streams/{streamId}/playback-ids/{playbackId}" -->
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

    res = fastpix.live_playback.get_playback_id_details(stream_id="61a264dcc447b63da6fb79ef925cd76d", playback_id="61a264dcc447b63da6fb79ef925cd76d")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                             | Type                                                                                  | Required                                                                              | Description                                                                           | Example                                                                               |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `stream_id`                                                                           | *str*                                                                                 | :heavy_check_mark:                                                                    | After creating a new live stream, FastPix assigns a unique identifier to the stream.  | 61a264dcc447b63da6fb79ef925cd76d                                                      |
| `playback_id`                                                                         | *str*                                                                                 | :heavy_check_mark:                                                                    | After creating a new playbackId, FastPix assigns a unique identifier to the playback. | 61a264dcc447b63da6fb79ef925cd76d                                                      |
| `retries`                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                      | :heavy_minus_sign:                                                                    | Configuration to override the default retry behavior of the client.                   |                                                                                       |

### Response

**[models.GetLiveStreamPlaybackIDResponse](../../models/getlivestreamplaybackidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |