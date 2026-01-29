# MediaTracks

## Overview

### Available Operations

* [add](#add) - Add audio / subtitle track
* [update](#update) - Update audio / subtitle track

## add

This endpoint allows you to add an audio or subtitle track to an existing media file using its `mediaId`. You need to provide the track `url` along with its `type` (audio or subtitle), `languageName` and `languageCode` in the request payload.

#### How it works

1. Send a POST request to this endpoint, replacing `{mediaId}` with the media ID (`uploadId` or `id`).

2. Provide the necessary details in the request body.

3. Receive a response containing a unique track ID and the details of the newly added track.

#### Webhook events

1. After successfully adding a track, your system must receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackcreated">video.media.track.created</a>.

2. Once the track is processed and ready, you must receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackready">video.media.track.ready</a>.

3. Finally, an update event <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> must notify your system about the media's updated status.

#### Example
Suppose you have a video uploaded to the FastPix platform, and you want to add an Italian audio track to it. By calling this API, you can attach an external audio file (https://static.fastpix.io/music-1.mp3) to the media file. Similarly, if you need to add subtitles in different languages, you can specify type: `subtitle` with the corresponding subtitle `url`, `languageCode` and `languageName`.

Related guides: <a href="https://docs.fastpix.io/docs/manage-subtitle-tracks">Add own subtitle tracks</a>, <a href="https://docs.fastpix.io/docs/manage-audio-tracks">Add own audio tracks</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="Add-media-track" method="post" path="/on-demand/{mediaId}/tracks" -->
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

    res = fastpix.media_tracks.add(media_id="your-media-id", tracks={})

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-media-id                                                                             |
| `tracks`                                                                                  | [models.AddTrackRequest](../../models/addtrackrequest.md)                                 | :heavy_check_mark:                                                                        | Contains details about the track being added to the media file.                           |                                                                                           |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.AddMediaTrackResponse](../../models/addmediatrackresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update

This endpoint allows you to update an existing audio or subtitle track associated with a media file. When updating a track, you must provide the new track `url`, `languageName`, and `languageCode`, ensuring all three parameters are included in the request.

#### How it works

1. Send a PATCH request to this endpoint, replacing `{mediaId}` with the media ID, and `{trackId}` with the ID of the track you want to update.

2. Provide the necessary details in the request body.

3. Receive a response confirming the track update.

#### Webhook Events

After updating a track, your system must receive webhook notifications:

1. After successfully updating a track, your system must receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackupdated">video.media.track.updated</a>.

2. Once the new track is processed and ready, you must receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackready">video.media.track.ready</a>.

3. Once the media file is updated with the new track details, a <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> event must be triggered.

#### Example
Suppose you previously added a French subtitle track to a video but now need to update it with a different file. By calling this API, you can replace the existing subtitle file (.vtt) with a new one while keeping the same track ID. This is useful when:

  - The original track file has errors and needs correction.
  - You want to improve subtitle translations or replace an audio track with a better-quality version.

Related guides: <a href="https://docs.fastpix.io/docs/manage-subtitle-tracks">Add own subtitle tracks</a>, <a href="https://docs.fastpix.io/docs/manage-audio-tracks">Add own audio tracks</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-track" method="patch" path="/on-demand/{mediaId}/tracks/{trackId}" -->
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

   
    res = fastpix.media_tracks.update(track_id="your-track-id", media_id="your-media-id", url="http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.vtt", language_code="fr", language_name="french")
    
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `track_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-track-id                                                                             |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | your-media-id                                                                             |
| `url`                                                                                     | *Optional[str]*                                                                           | :heavy_minus_sign:                                                                        | The direct URL of the track file. It must point to a valid audio or subtitle file.        | http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.vtt          |
| `language_code`                                                                           | *Optional[str]*                                                                           | :heavy_minus_sign:                                                                        | The BCP 47 language code representing the track’s language.                               | fr                                                                                        |
| `language_name`                                                                           | *Optional[str]*                                                                           | :heavy_minus_sign:                                                                        | The full name of the language corresponding to the `languageCode`.                        | French                                                                                    |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.UpdateMediaTrackResponse](../../models/updatemediatrackresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |