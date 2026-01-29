# StartLiveStream

## Overview

### Available Operations

* [create_stream](#create_stream) - Create a new stream

## create_stream

Creates a new <a href="https://docs.fastpix.io/docs/get-started-with-live-streaming">RTMPS</a> or <a href="https://docs.fastpix.io/docs/using-srt-to-live-stream">SRT</a> live stream in FastPix. When you create a stream, FastPix generates a unique `streamKey` and `srtSecret` that you can use with broadcasting software such as OBS to connect to FastPix RTMPS or SRT servers. Use SRT for live streaming in unstable network conditions, as it provides error correction and encryption for a more reliable and secure broadcast.

Leverage SRT for live streaming in environments with unstable networks, taking advantage of its error correction and encryption features for a resilient and secure broadcast. 

<h4>How it works</h4> 

1. Send a `POST` request to this endpoint. You can configure the stream settings, including `metadata` (such as stream name and description), `reconnectWindow` (in case of disconnection), and privacy options (`public` or `private`). 

2. FastPix returns the stream details for both RTMPS and SRT configurations. These keys and IDs from the stream details are essential for connecting the broadcasting software to FastPix’s servers and transmitting the live stream to viewers.

3. After the live stream is created, FastPix sends a `POST` request to your specified webhook endpoint with the event <a href="https://docs.fastpix.io/docs/live-events#videolive_streamcreated">video.live_stream.created</a>.

**Example:**

  Imagine a gaming platform that allows users to live stream gameplay directly from their dashboard. The API creates a new stream, provides the necessary stream key, and sets it to "private" so that only specific viewers can access it. 

Related guide: <a href="https://docs.fastpix.io/docs/how-to-livestream">How to live stream</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="create-new-stream" method="post" path="/live/streams" -->
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

    res = fastpix.start_live_stream.create_stream(playback_settings={}, input_media_settings={
        "metadata": {
            "livestream_name": "fastpix_livestream",
        },
    })

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `playback_settings`                                                 | [models.PlaybackSettings](../../models/playbacksettings.md)         | :heavy_check_mark:                                                  | Displays the result of the playback settings.                       |
| `input_media_settings`                                              | [models.InputMediaSettings](../../models/inputmediasettings.md)     | :heavy_check_mark:                                                  | Contains configuration details for input media settings.            |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateNewStreamResponse](../../models/createnewstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |