# Videos

## Overview

### Available Operations

* [delete](#delete) - Delete a media by ID
* [delete_track](#delete_track) - Delete audio / subtitle track
* [list_clips](#list_clips) - Get all clips of a media

## delete

This endpoint allows you to permanently delete a a specific video or audio media file along with all associated data. If you wish to remove a media from FastPix storage, use this endpoint with the `mediaId` (either `uploadId` or `id`) received during the media's creation or upload. 

#### How it works

1. Send a DELETE request to this endpoint. Replace `<mediaId>` with the `uploadId` or the `id` of the media you want to delete. 

2. This action is irreversible. Make sure you no longer need the media before proceeding. Once deleted, the media can’t be retrieved or played back. 

3. Monitor the following webhook event: <a href="https://docs.fastpix.io/docs/media-events#videomediadeleted">video.media.deleted</a>

#### Example
A user on a video-sharing platform decides to remove an old video from their profile, or suppose you're running a content moderation system, and one of the videos uploaded by a user violates your platform's policies. Using this endpoint, the media is permanently deleted from your library, ensuring it's no longer accessible or viewable by other users.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media" method="delete" path="/on-demand/{mediaId}" -->
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

    res = fastpix.videos.delete(media_id="your-media-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-media-id                                                                             |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.DeleteMediaResponse](../../models/deletemediaresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## delete_track

This endpoint allows you to delete an existing audio or subtitle track from a media file. Once deleted, the track must no longer be available for playback.

#### How it works

1. Send a DELETE request to this endpoint, replacing `{mediaId}` with the media ID, and `{trackId}` with the ID of the track you want to remove.

2. The track gets deleted from the media file, and you must receive a confirmation response.

#### Webhook events

1. After successfully deleting a track, your system must receive the webhook event **video.media.track.deleted**.

2. Once the media file is updated to reflect the track removal, a <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> event must be triggered.

#### Example
Suppose you uploaded an audio track in Italian for a video but later realize it's incorrect or no longer needed. By calling this API, you can remove the specific track while keeping the rest of the media file unchanged. This is useful when:

  - A track was mistakenly added and needs to be removed.
  - The content owner requests the removal of a specific subtitle or audio track.
  - A new version of the track gets uploaded to replace the existing one.

Related guides: <a href="https://docs.fastpix.io/docs/manage-subtitle-tracks">Add own subtitle tracks</a>, <a href="https://docs.fastpix.io/docs/manage-audio-tracks">Add own audio tracks</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media-track" method="delete" path="/on-demand/{mediaId}/tracks/{trackId}" -->
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

    res = fastpix.videos.delete_track(media_id="your-media-id", track_id="your-track-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-media-id                                                                             |
| `track_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-track-id                                                                             |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.DeleteMediaTrackResponse](../../models/deletemediatrackresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## list_clips

This endpoint retrieves a list of all media clips associated with a given source media ID. It helps you organize and manage media efficiently by providing metadata such as clip media IDs and other relevant details.

A media clip is a segmented portion of an original media file (source media). Clips are often created for various purposes such as previews, highlights, or customized edits. This API allows you to fetch all such clips linked to a specific source media, making it easier to track and manage clips.

#### How it works

- The endpoint returns metadata for all media clips associated with the given `mediaId`.
- Results are paginated to efficiently handle large datasets.
- Each entry includes detailed metadata such as media `id`, `duration`, and `status`.
- Helps in organizing clips effectively by providing structured information.

#### Example

Imagine you’re managing a video editing platform where users upload full-length videos and create short clips for social media sharing. To keep track of all clips linked to a particular video, you call this API with the sourceMediaId. The response provides a list of all associated clips, allowing you to manage, edit, or repurpose them as needed.

Related guide: <a href="https://docs.fastpix.io/docs/create-clips-from-existing-media">Create clips from existing media</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="get-media-clips" method="get" path="/on-demand/{mediaId}/media-clips" -->
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

    res = fastpix.videos.list_clips(media_id="your-media-id", offset=5, limit=20, order_by="desc")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | fc733e3f-2fba-4c3d-9388-2511dc50d15f                                                      |
| `offset`                                                                                  | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Offset determines the starting point for data retrieval within a paginated list.          | 5                                                                                         |
| `limit`                                                                                   | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | The number of media clips to retrieve per request.                                        | 20                                                                                        |
| `order_by`                                                                                | [Optional[models.SortOrder]](../../models/sortorder.md)                                   | :heavy_minus_sign:                                                                        | The values in the list can be arranged in two ways DESC (Descending) or ASC (Ascending).  | desc                                                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.GetMediaClipsResponse](../../models/getmediaclipsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |