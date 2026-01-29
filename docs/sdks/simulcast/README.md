# Simulcast

## Overview

### Available Operations

* [delete](#delete) - Delete a simulcast

## delete

Deletes a simulcast using its unique simulcastId, which you received during the simulcast creation process. Deleting a simulcast stops the broadcast to the associated platform, while the parent stream continues if it’s live. This action can’t be undone, and you must create a new simulcast to resume streaming to the same platform.

Webhook event: <a href="https://docs.fastpix.io/docs/live-events#videolive_streamsimulcast_targetdeleted">video.live_stream.simulcast_target.deleted</a>

#### Example
A broadcaster may need to stop simulcasting to one platform while keeping the stream active on others. For example, a tech company is simulcasting a product launch across multiple platforms. Midway through the event, they decide to stop the simulcast on Facebook due to performance issues but continue streaming on YouTube. They use this API to delete the Facebook simulcast target. 

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-simulcast-of-stream" method="delete" path="/live/streams/{streamId}/simulcast/{simulcastId}" -->
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

    res = fastpix.simulcast.delete(
        stream_id="your-stream-id",
        simulcast_id="your-simulcast-id",
    )

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                      | Type                                                                                                                           | Required                                                                                                                       | Description                                                                                                                    | Example                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `stream_id`                                                                                                                    | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | After creating a new live stream, FastPix assigns a unique identifier to the stream.                                           | your-stream-id                                                                                                                 |
| `simulcast_id`                                                                                                                 | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | When you create the new simulcast, FastPix assign a universal unique identifier which can contain a maximum of 255 characters. | your-simulcast-id                                                                                                              |
| `retries`                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                               | :heavy_minus_sign:                                                                                                             | Configuration to override the default retry behavior of the client.                                                            |                                                                                                                                |

### Response

**[models.DeleteSimulcastOfStreamResponse](../../models/deletesimulcastofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |