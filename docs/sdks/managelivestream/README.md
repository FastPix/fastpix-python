# ManageLiveStream

## Overview

### Available Operations

* [get_live_stream_viewer_count_by_id](#get_live_stream_viewer_count_by_id) - Get stream views by ID
* [update_live_stream](#update_live_stream) - Update a stream
* [complete_live_stream](#complete_live_stream) - Complete a stream

## get_live_stream_viewer_count_by_id

This endpoint retrieves the current number of viewers watching a specific live stream, identified by its unique `streamId`.

The viewer count is an **approximate value**, optimized for performance. It provides a near-real-time estimate of how many clients are actively watching the stream. This approach ensures high efficiency, especially when the stream is being watched at large scale across multiple devices or platforms.

#### Example

Suppose a content creator is hosting a live concert and wants to display the number of live viewers on their dashboard. This endpoint can be queried to show up-to-date viewer statistics.

Related guide: <a href="https://fastpix.com/docs/manage-live-streams/create-and-manage-live-streams">Manage streams</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="get-live-stream-viewer-count-by-id" method="get" path="/live/streams/{streamId}/viewer-count" -->
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

    res = fastpix.manage_live_stream.get_live_stream_viewer_count_by_id(stream_id="your-stream-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                            | Type                                                                                 | Required                                                                             | Description                                                                          | Example                                                                              |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `stream_id`                                                                          | *str*                                                                                | :heavy_check_mark:                                                                   | After creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                     |
| `retries`                                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                     | :heavy_minus_sign:                                                                   | Configuration to override the default retry behavior of the client.                  |                                                                                      |

### Response

**[models.GetLiveStreamViewerCountByIDResponse](../../models/getlivestreamviewercountbyidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_live_stream

This endpoint allows you to modify the parameters of an existing live stream, such as its `metadata` (title, description) or the `reconnectWindow`. It’s useful for making changes to a stream that has already been created but not yet ended. After the live stream is disabled, you cannot update a stream. 

  The updated stream parameters and the `streamId` needs to be shared in the request, and FastPix returns the updated stream details. After the update, <a href="https://fastpix.com/docs/live-stream-events/live-events#videolive_streamupdated">video.live_stream.updated</a> webhook event notifies your system.

 #### Example

 A host realizes they need to extend the reconnect window for their live stream in case they lose connection temporarily during the event. Or suppose during a multi-day online conference, the event organizers need to update the stream title to reflect the next day"s session while keeping the same stream ID for continuity. 

  Related guide: <a href="https://fastpix.com/docs/manage-live-streams/create-and-manage-live-streams">Manage streams</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="update-live-stream" method="patch" path="/live/streams/{streamId}" -->
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

   
    res = fastpix.manage_live_stream.update_live_stream(stream_id="your-stream-id", metadata={
        "livestream_name": "your-livestream-name",
    }, reconnect_window=100)
    
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                      | Type                                                                                                                                                                                                                                                                                                           | Required                                                                                                                                                                                                                                                                                                       | Description                                                                                                                                                                                                                                                                                                    | Example                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stream_id`                                                                                                                                                                                                                                                                                                    | *str*                                                                                                                                                                                                                                                                                                          | :heavy_check_mark:                                                                                                                                                                                                                                                                                             | After creating a new live stream, FastPix assigns a unique identifier to the stream.                                                                                                                                                                                                                           | your-stream-id                                                                                                                                                                                                                                                                               |
| `metadata`                                                                                                                                                                                                                                                                                                     | Dict[str, *str*]                                                                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                                                                             | You can search for videos with specific key value pairs using metadata, when you tag a video in "key":"value"s pairs. Dynamic metadata allows you to define a key that allows any value pair. You can have maximum of 255 characters and upto 10 entries are allowed.                                          | {<br/>"livestream_name": "your-livestream-name"<br/>}                                                                                                                                                                                                                                                                 |
| `reconnect_window`                                                                                                                                                                                                                                                                                             | *Optional[int]*                                                                                                                                                                                                                                                                                                | :heavy_minus_sign:                                                                                                                                                                                                                                                                                             | In case the software streaming the live, gets disrupted for any reason and gets disconnected from FastPix, the reconnect window defines the duration FastPix waits before automatically terminating the stream. Before starting the stream, you can set the reconnect window time which is up to 1800 seconds. | 60                                                                                                                                                                                                                                                                                                             |
| `retries`                                                                                                                                                                                                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                               | :heavy_minus_sign:                                                                                                                                                                                                                                                                                             | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                |

### Response

**[models.UpdateLiveStreamResponse](../../models/updatelivestreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## complete_live_stream

This endpoint marks a livestream as completed by stopping the active stream and transitioning its status to `idle`. It is typically used after a livestream session has ended.

This operation only works when the stream is in the `active` state.

Completing a stream can help finalize the session and trigger post-processing events like VOD generation.

#### Example

A virtual event ends, and the system or host needs to close the livestream to prevent further streaming. This endpoint ensures the livestream status is changed from `active` to `idle`, indicating it's officially completed.

Related guide <a href="https://fastpix.com/docs/manage-live-streams/create-and-manage-live-streams">Manage streams</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="complete-live-stream" method="put" path="/live/streams/{streamId}/finish" -->
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

    res = fastpix.manage_live_stream.complete_live_stream(stream_id="your-stream-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                           | Type                                                                                | Required                                                                            | Description                                                                         | Example                                                                             |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `stream_id`                                                                         | *str*                                                                               | :heavy_check_mark:                                                                  | Upon creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                    |
| `retries`                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                    | :heavy_minus_sign:                                                                  | Configuration to override the default retry behavior of the client.                 |                                                                                     |

### Response

**[models.CompleteLiveStreamResponse](../../models/completelivestreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |