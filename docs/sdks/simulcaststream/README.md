# SimulcastStream

## Overview

### Available Operations

* [create](#create) - Create a simulcast
* [get_simulcast](#get_simulcast) - Get a specific simulcast
* [update_simulcast](#update_simulcast) - Update a simulcast

## create

Creates a simulcast for a parent live stream. Simulcasting allows you to broadcast a live stream to multiple social platforms simultaneously (for example, YouTube, Facebook, or Twitch). This helps expand your audience reach across platforms. A simulcast can only be created when the parent live stream is in the idle state (not currently live or disabled). Only one simulcast target can be created per API call. 
#### How it works

1. Change to: When you call this endpoint, provide the parent `streamId` along with the simulcast target details (such as platform and credentials). The API returns a unique `simulcastId`, which you can use to manage the simulcast later.  

2. To notify your application about the status of simulcast related events check for the <a href="https://docs.fastpix.io/docs/webhooks-collection#simulcast-target-events">webhooks for simulcast</a> target events. 

#### Example
An event manager sets up a live stream for a virtual conference and wants to simulcast the stream on YouTube and Facebook Live. They first create the primary live stream in FastPix, ensuring it's in the idle state. Then, they use the API to create a simulcast target for YouTube. 

Related guide: <a href="https://docs.fastpix.io/docs/simulcast-to-3rd-party-platforms">Simulcast to 3rd party platforms</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="create-simulcast-of-stream" method="post" path="/live/streams/{streamId}/simulcast" -->
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

    res = fastpix.simulcast_stream.create(stream_id="your-stream-id", url="rtmp://hyd01.contribute.live-video.net/app/", stream_key="live_1012464221_DuM8W004MoZYNxQEZ0czODgfHCFBhk", metadata={
        "livestream_name": "Tech-Connect Summit",
    })

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                                  | Type                                                                                                                                                       | Required                                                                                                                                                   | Description                                                                                                                                                | Example                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stream_id`                                                                                                                                                | *str*                                                                                                                                                      | :heavy_check_mark:                                                                                                                                         | After creating a new live stream, FastPix assigns a unique identifier to the stream.                                                                       | your-stream-id                                                                                                                                             |
| `url`                                                                                                                                                      | *Optional[str]*                                                                                                                                            | :heavy_minus_sign:                                                                                                                                         | The RTMPS hostname, combined with the application name, is crucial for connecting to third-party live streaming services and transmitting the live stream. | rtmp://hyd01.contribute.live-video.net/app/                                                                                                                |
| `stream_key`                                                                                                                                               | *Optional[str]*                                                                                                                                            | :heavy_minus_sign:                                                                                                                                         | A unique stream key is generated for streaming, allowing the user to start streaming on any third-party platform using this key.                           | live_1012464221_DuM8W004MoZYNxQEZ0czODgfHCFBhk                                                                                                             |
| `metadata`                                                                                                                                                 | Dict[str, *str*]                                                                                                                                           | :heavy_minus_sign:                                                                                                                                         | You can search for videos with specific key-value pairs using metadata, when you tag a video in "key":"value" pairs.                                       | {<br/>"livestream_name": "Tech-Connect Summit"<br/>}                                                                                                       |
| `retries`                                                                                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                           | :heavy_minus_sign:                                                                                                                                         | Configuration to override the default retry behavior of the client.                                                                                        |                                                                                                                                                            |

### Response

**[models.CreateSimulcastOfStreamResponse](../../models/createsimulcastofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_simulcast

Retrieves the details of a specific simulcast associated with a parent live stream. By providing both the `streamId` of the parent stream and the `simulcastId`, FastPix returns detailed information about the simulcast, such as the stream URL, the status of the simulcast, and metadata. 

#### Example
This endpoint can be used to verify the status of the simulcast on external platforms before the live stream begins. For example, before starting a live gaming event, the organizer wants to ensure that the simulcast to Twitch is set up correctly. They retrieve the simulcast information to confirm that everything is properly configured.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-specific-simulcast-of-stream" method="get" path="/live/streams/{streamId}/simulcast/{simulcastId}" -->
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

    res = fastpix.simulcast_stream.get_simulcast(stream_id="your-stream-id", simulcast_id="your-simulcast-id")

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

**[models.GetSpecificSimulcastOfStreamResponse](../../models/getspecificsimulcastofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_simulcast

Updates the status of a specific simulcast linked to a parent live stream. You can enable or disable the simulcast at any time while the parent stream is active or idle. After the live stream is disabled, the simulcast can no longer be modified.

Webhook event: <a href="https://docs.fastpix.io/docs/live-events#videolive_streamsimulcast_targetupdated">video.live_stream.simulcast_target.updated</a>

#### Example
When a `PATCH` request is made to this endpoint, the API updates the status of the simulcast. This can be useful for pausing or resuming a simulcast on a particular platform without stopping the parent live stream.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-specific-simulcast-of-stream" method="put" path="/live/streams/{streamId}/simulcast/{simulcastId}" -->
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

    res = fastpix.simulcast_stream.update_simulcast(stream_id="your-stream-id", simulcast_id="your-simulcast-id", is_enabled=True, metadata={
        "simulcast_name": "Tech today",
    })

     # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                      | Type                                                                                                                           | Required                                                                                                                       | Description                                                                                                                    | Example                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `stream_id`                                                                                                                    | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | Upon creating a new live stream, FastPix assigns a unique identifier to the stream.                                            | 9714422d89287ad5758d4a86e9afe1a2                                                                                               |
| `simulcast_id`                                                                                                                 | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | When you create the new simulcast, FastPix assign a universal unique identifier which can contain a maximum of 255 characters. | 8717422d89288ad5958d4a86e9afe2a2                                                                                               |
| `is_enabled`                                                                                                                   | *Optional[bool]*                                                                                                               | :heavy_minus_sign:                                                                                                             | When set to false, the simulcast is disabled for the specified stream.                                                         | true                                                                                                                           |
| `metadata`                                                                                                                     | Dict[str, *str*]                                                                                                               | :heavy_minus_sign:                                                                                                             | You can search for videos with specific key-value pairs using metadata, when you tag a video in "key":"value" pairs.           | {<br/>"livestream_name": "Tech today"<br/>}                                                                                    |
| `retries`                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                               | :heavy_minus_sign:                                                                                                             | Configuration to override the default retry behavior of the client.                                                            |                                                                                                                                |

### Response

**[models.UpdateSpecificSimulcastOfStreamResponse](../../models/updatespecificsimulcastofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |