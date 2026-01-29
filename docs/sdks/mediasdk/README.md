# Media

## Overview

### Available Operations

* [list_live_clips](#list_live_clips) - Get all clips of a live stream
* [get](#get) - Get a media by ID
* [get_input_info](#get_input_info) - Get info of media inputs

## list_live_clips

Retrieves a list of all media clips generated from a specific livestream. Each media entry includes metadata such as the clip media IDs, and other relevant details. A media clip is a segmented portion of an original media file (source live stream). Clips are often created for various purposes such as previews, highlights, or customized edits.
#### How it works
1. Provide the livestreamId as a parameter when calling this endpoint.

2. The API returns a paginated list of media clips created from the specified livestream.

3. Pagination helps maintain performance and usability when handling large sets of media files, making it easier to organize and manage content in bulk.

#### Use case
Suppose you’re hosting a live gaming event and want to showcase key moments from the stream — such as top plays or final match highlights. You can use this endpoint to fetch all clips generated from that livestream, display them in your dashboard, or use them for post-event editing and sharing.


Related guide: <a href="https://docs.fastpix.io/docs/instant-live-clipping">Instant live clipping</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="list-live-clips" method="get" path="/on-demand/{livestreamId}/live-clips" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.media.list_live_clips(livestream_id="b6f71268143f70c798a7851a0a92dcbf", limit=20, offset=1, order_by="desc")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `livestream_id`                                                                           | *str*                                                                                     | :heavy_check_mark:                                                                        | The stream Id is unique identifier assigned to the live stream.                           | b6f71268143f70c798a7851a0a92dcbf                                                          |
| `limit`                                                                                   | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Limit specifies the maximum number of items to display per page.                          | 20                                                                                        |
| `offset`                                                                                  | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Offset determines the starting point for data retrieval within a paginated list.          | 1                                                                                         |
| `order_by`                                                                                | [Optional[models.SortOrder]](../../models/sortorder.md)                                   | :heavy_minus_sign:                                                                        | The values in the list can be arranged in two ways: DESC (Descending) or ASC (Ascending). | desc                                                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.ListLiveClipsResponse](../../models/listliveclipsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get

By calling this endpoint, you can retrieve detailed information about a specific media item, including its current `status` and a `playbackId`. This is particularly useful for retrieving specific media details when managing large content libraries. 



#### How it works

1. Send a GET request to this endpoint. Use the `<mediaId>` you received after uploading the media file.

2. The response includes details about the media:
   - **status** – Indicates whether the media is still *Processing* or has transitioned to *Ready*.
   - **playbackId** – A unique identifier that allows you to stream the media once it is *Ready*.  
     You can construct the stream URL as follows:  
     `https://stream.fastpix.io/<playbackId>.m3u8`

#### Example

If your platform provides users with a dashboard to manage uploaded content, a user might want to check whether a video has finished processing and is ready for playback. You can use the media ID to retrieve the information from FastPix and display it in the user’s dashboard.


### Example Usage

<!-- UsageSnippet language="python" operationID="get-media" method="get" path="/on-demand/{mediaId}" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.media.get(media_id="your-media-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-media-id                                                                             |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.GetMediaResponseResponse](../../models/getmediaresponseresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_input_info

This endpoint lets you retrieve detailed information about the media inputs associated with a specific media item. You can use it to verify the media file’s input URL, track its creation status, and check its container format. You must provide the mediaId (either the uploadId or the id) to fetch this information.


#### How it works

Upon making a `GET` request with the mediaId, FastPix returns a response with: 

* The public storage input `url` of the uploaded media file. 

* Information about the media’s video and audio tracks, including whether they were successfully created.

* The container format of the uploaded media file (for example, MP4, MKV).

This endpoint is particularly useful for ensuring that all necessary tracks (video and audio) have been correctly associated with the media during the upload or media creation process.


### Example Usage

<!-- UsageSnippet language="python" operationID="retrieveMediaInputInfo" method="get" path="/on-demand/{mediaId}/input-info" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.media.get_input_info(media_id="your-media-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | Pass the list of the input objects used to create the media, along with applied settings. | your-media-id                                                                             |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.RetrieveMediaInputInfoResponse](../../models/retrievemediainputinforesponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |