# ManageVideos

## Overview

### Available Operations

* [list_media](#list_media) - Get list of all media
* [update_media](#update_media) - Update a media by ID
* [cancel_upload](#cancel_upload) - Cancel ongoing upload
* [generate_subtitles](#generate_subtitles) - Generate track subtitle
* [get_summary](#get_summary) - Get the summary of a video
* [update_source_access](#update_source_access) - Update the source access of a media by ID
* [update_mp4_support](#update_mp4_support) - Update the mp4Support of a media by ID
* [list_unused_upload_urls](#list_unused_upload_urls) - Get all unused upload URLs

## list_media

This endpoint returns a list of all media files uploaded to FastPix within a specific workspace. Each media entry contains data such as the media `id`, `createdAt`, `status`, `type` and more. It allows you to retrieve an overview of your media assets, making it easier to manage and review them. 

#### How it works

Use the access token and secret key related to the workspace in the request header. When called, the API provides a paginated response containing all the media items in that specific workspace. This is helpful for retrieving a large volume of media and managing content in bulk. 

#### Example
If you manage a video platform and need to review all uploaded media in your library to ensure that outdated or low-quality content isn’t being served, you can use this endpoint to retrieve a complete list of media. You can then filter, sort, or update items as needed.

### Example Usage

<!-- UsageSnippet language="python" operationID="list-media" method="get" path="/on-demand" -->
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

    res = fastpix.manage_videos.list_media(limit=20, offset=1, order_by="desc")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `limit`                                                                                   | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Limit specifies the maximum number of items to display per page.                          | 20                                                                                        |
| `offset`                                                                                  | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Offset determines the starting point for data retrieval within a paginated list.          | 1                                                                                         |
| `order_by`                                                                                | [Optional[models.SortOrder]](../../models/sortorder.md)                                   | :heavy_minus_sign:                                                                        | The values in the list can be arranged in two ways: DESC (Descending) or ASC (Ascending). | desc                                                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.ListMediaResponse](../../models/listmediaresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_media

This endpoint allows you to update specific parameters of an existing media file. You can modify the key-value pairs of the metadata that were provided in the payload during the creation of media from a URL or when uploading the media directly from device. 

#### How it works

1. Make a PATCH request to this endpoint. Replace `<mediaId>` with the unique ID (`uploadId` or `id`) of the media you received after uploading to FastPix

2. Include the updated parameters in the request body.

3. The response returns the updated media data, confirming the changes. 

4. Monitor the <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> webhook event to track the update status in your system.

#### Example
If a user uploads a video and later needs to change the title, add a new description, or update tags, you can use this endpoint to update the media metadata without re-uploading the entire video.

### Example Usage

<!-- UsageSnippet language="python" operationID="updated-media" method="patch" path="/on-demand/{mediaId}" -->
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

   
    res = fastpix.manage_videos.update_media(media_id="your-media-id", metadata={
        "user": "fastpix_admin",
    }, title="test title", creator_id="your-creator-id")
    
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                      |
| `metadata`                                                                                | Dict[str, *str*]                                                                          | :heavy_minus_sign:                                                                        | N/A                                                                                       | {<br/>"user": "fastpix_admin"<br/>}                                                       |
| `title`                                                                                   | *Optional[str]*                                                                           | :heavy_minus_sign:                                                                        | Title of the media file.                                                                  | My Video Title                                                                            |
| `creator_id`                                                                              | *Optional[str]*                                                                           | :heavy_minus_sign:                                                                        | The unique identifier of the user who created this media.                                 | 8fa85f64-5717-4562-b3fc-2c963f66afa6                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.UpdatedMediaResponse](../../models/updatedmediaresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## cancel_upload

This endpoint allows you to cancel ongoing upload by its `uploadId`. Once cancelled, the upload is marked as cancelled. Use this if a user aborts an upload or if you want to programmatically stop an in-progress upload.

#### How it works

1. Make a PUT request to this endpoint, replacing `{uploadId}` with the unique upload ID received after starting the upload.
2. The response confirms the cancellation and provide the status of the upload.

#### Webhook Events

Once the upload is cancelled, you must receive the webhook event <a href="https://docs.fastpix.io/docs/media-events#videomediauploadcancelled">video.media.upload.cancelled</a>.

#### Example

Suppose a user starts uploading a large video file but decides to cancel before completion. By calling this API, you can immediately stop the upload and free up resources.

### Example Usage

<!-- UsageSnippet language="python" operationID="cancel-upload" method="put" path="/on-demand/upload/{uploadId}/cancel" -->
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

    
    res = fastpix.manage_videos.cancel_upload(upload_id="your-upload-id")
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                          | Type                                                                                                               | Required                                                                                                           | Description                                                                                                        | Example                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `upload_id`                                                                                                        | *str*                                                                                                              | :heavy_check_mark:                                                                                                 | When uploading the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                               |
| `retries`                                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                   | :heavy_minus_sign:                                                                                                 | Configuration to override the default retry behavior of the client.                                                |                                                                                                                    |

### Response

**[models.CancelUploadResponse](../../models/canceluploadresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## generate_subtitles

This endpoint allows you to generate subtitles for an existing audio track in a media file. By calling this API, you can generate subtitles automatically using speech recognition

#### How it works

1. Send a `POST` request to this endpoint, replacing `{mediaId}` with the media ID and `{trackId}` with the track ID.

2. Provide the necessary details in the request body, including the languageName and languageCode.

3. You receive a response containing a unique subtitle track ID and its details.

#### Webhook Events

1. After the subtitle track is generated and ready, you receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediasubtitlegeneratedready">video.media.subtitle.generated.ready</a>.

2. Finally the <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> event notifies your system about the media’s updated status.

</br> Related guide: <a href="https://docs.fastpix.io/docs/add-auto-generated-subtitles-to-videos">Add auto-generated subtitles</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="Generate-subtitle-track" method="post" path="/on-demand/{mediaId}/tracks/{trackId}/generate-subtitles" -->
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

    
    res = fastpix.manage_videos.generate_subtitles(media_id="your-media-id", track_id="your-track0-id", language_name="Italian", metadata={
        "key1": "value1",
    })
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                                                                                                                                               | Type                                                                                                                                                                                                                                                                    | Required                                                                                                                                                                                                                                                                | Description                                                                                                                                                                                                                                                             | Example                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                                                                                                                                                                              | *str*                                                                                                                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                                                                                                                      | The unique identifier assigned to the media when created. The value must be a valid UUID.                                                                                                                                                                               | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                                                                                                                                                                    |
| `track_id`                                                                                                                                                                                                                                                              | *str*                                                                                                                                                                                                                                                                   | :heavy_check_mark:                                                                                                                                                                                                                                                      | A universally unique identifier (UUID) assigned to the specific track for which subtitles must be generated.                                                                                                                                                            | d46f5df9-1a8f-4f0a-b56e-9f5b5d5b9e21                                                                                                                                                                                                                                    |
| `language_name`                                                                                                                                                                                                                                                         | *Optional[str]*                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                      | The full name of the language used to generate the subtitles.                                                                                                                                                                                                           | English                                                                                                                                                                                                                                                                 |
| `metadata`                                                                                                                                                                                                                                                              | Dict[str, *str*]                                                                                                                                                                                                                                                        | :heavy_minus_sign:                                                                                                                                                                                                                                                      | You can search for videos with specific key value pairs using metadata, when you tag a video in "key" : "value" pairs. Dynamic metadata allows you to define a key that allows any value pair. You can have maximum of 255 characters and upto 10 entries are allowed.<br/> | {<br/>"key1": "value1"<br/>}                                                                                                                                                                                                                                            |
| `language_code`                                                                                                                                                                                                                                                         | [Optional[models.LanguageCode]](../../models/languagecode.md)                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                                      | Language code for content localization                                                                                                                                                                                                                                  | en-US                                                                                                                                                                                                                                                                   |
| `retries`                                                                                                                                                                                                                                                               | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                        | :heavy_minus_sign:                                                                                                                                                                                                                                                      | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                     |                                                                                                                                                                                                                                                                         |

### Response

**[models.GenerateSubtitleTrackResponse](../../models/generatesubtitletrackresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_summary

This endpoint returns the generated summary of a video.  

The summary is created using the **InVideo Summary** feature, which processes the video content and produces a textual summary.  

To use this endpoint, you must first generate the video summary using the Generate Video Summary endpoint. This endpoint can return the summary only after that process is complete. 

Typical use cases include:  
- Providing viewers with a quick preview of the video's main content.  
- Enabling search or recommendation systems to surface summarized insights.  
- Supporting accessibility and content discovery without requiring users to watch the full video.  

If the summary has not been generated or the feature is disabled for the requested media, the endpoint returns an error indicating that the summary is unavailable. 

### Example Usage

<!-- UsageSnippet language="python" operationID="get-media-summary" method="get" path="/on-demand/{mediaId}/summary" -->
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

    res = fastpix.manage_videos.get_summary(media_id="fc733e3f-2fba-4c3d-9388-2511dc50d15f")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | The unique identifier assigned to the media when created. The value must be a valid UUID. | fc733e3f-2fba-4c3d-9388-2511dc50d15f                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.GetMediaSummaryResponse](../../models/getmediasummaryresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_source_access

This endpoint allows you to update the `sourceAccess` setting of an existing media file. The `sourceAccess` parameter determines whether the original media file is accessible or restricted. Setting this to `true` enables access to the media source, while setting it to `false` restricts access. 

#### How it works

1. Make a `PATCH` request to this endpoint, replacing `{mediaId}` with the ID of the media you want to update.

2. Include the updated `sourceAccess` parameter in the request body.

3. You receive a response confirming the update to the media’s source access status.
4. Webhook events: <a href="https://docs.fastpix.io/docs/transform-media-events#videomediasourceready">video.media.source.ready</a>, <a href="https://docs.fastpix.io/docs/transform-media-events#videomediasourcedeleted">video.media.source.deleted</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="updated-source-access" method="patch" path="/on-demand/{mediaId}/source-access" -->
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

   
    res = fastpix.manage_videos.update_source_access(media_id="your-media-id", source_access=True)
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                  | Type                                                                                                                                       | Required                                                                                                                                   | Description                                                                                                                                | Example                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `media_id`                                                                                                                                 | *str*                                                                                                                                      | :heavy_check_mark:                                                                                                                         | The unique identifier assigned to the media when created. The value must be a valid UUID.<br/>                                             | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                                       |
| `source_access`                                                                                                                            | *bool*                                                                                                                                     | :heavy_check_mark:                                                                                                                         | The sourceAccess parameter determines whether the original media file is accessible. Set to true to enable access or false to restrict it. | true                                                                                                                                       |
| `retries`                                                                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                           | :heavy_minus_sign:                                                                                                                         | Configuration to override the default retry behavior of the client.                                                                        |                                                                                                                                            |

### Response

**[models.UpdatedSourceAccessResponse](../../models/updatedsourceaccessresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_mp4_support

This endpoint allows you to update the `mp4Support` setting of an existing media file using its media ID. You can specify the MP4 support level, such as `none`, `capped_4k`, `audioOnly`, or a combination of `audioOnly`, `capped_4k`, in the request payload.

#### How it works

1. Send a PATCH request to this endpoint, replacing `{mediaId}` with the media ID.

2. Provide the desired `mp4Support` value in the request body.

3. You receive a response confirming the update, including the media’s updated MP4 support status.

#### MP4 Support Options

- `none` – MP4 support is disabled for this media.

- `capped_4k` – Generates MP4 renditions up to 4K resolution.

- `audioOnly` – Generates an M4A file that contains only the audio track.

- `audioOnly,capped_4k` – Generates both an audio-only M4A file and MP4 renditions up to 4K resolution.

#### Webhook events

- <a href="https://docs.fastpix.io/docs/transform-media-events#videomediamp4supportready">video.media.mp4Support.ready</a> – Triggered when the MP4 support setting is successfully updated.

#### Example
Suppose you have a video uploaded to the FastPix platform, and you want to allow users to download the video in MP4 format. By setting "mp4Support": "capped_4k", the system generates an MP4 rendition of the video up to 4K resolution, making it available for download through the stream URL(`https://stream.fastpix.io/{playbackId}/{capped-4k.mp4 | audio.m4a}`). If you want users to stream only the audio from the media file, you can set "mp4Support": "audioOnly". This provides an audio-only stream URL that allows users to listen to the media without video. By setting "mp4Support": "audioOnly,capped_4k", both options are enabled. Users can download the MP4 video and also stream just the audio version of the media. 

Related guide: <a href="https://docs.fastpix.io/docs/mp4-support-for-offline-viewing">Use MP4 support for offline viewing</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="updated-mp4Support" method="patch" path="/on-demand/{mediaId}/update-mp4Support" -->
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

    res = fastpix.manage_videos.update_mp4_support(media_id="your-media-id", mp4_support="capped_4k")
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                  | Type                                                                                                                                                                                                                                                                                                                       | Required                                                                                                                                                                                                                                                                                                                   | Description                                                                                                                                                                                                                                                                                                                | Example                                                                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                                                                                                                                                                                                                                 | *str*                                                                                                                                                                                                                                                                                                                      | :heavy_check_mark:                                                                                                                                                                                                                                                                                                         | The unique identifier assigned to the media when created. The value must be a valid UUID.<br/>                                                                                                                                                                                                                             | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                                                                                                                                                                                                                       |
| `mp4_support`                                                                                                                                                                                                                                                                                                              | [Optional[models.UpdatedMp4SupportMp4Support]](../../models/updatedmp4supportmp4support.md)                                                                                                                                                                                                                                | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                         | Determines the type of MP4 support for the media. - **none**: Disables MP4 support. - **capped_4k**: Enables MP4 downloads with resolutions up to 4K. - **audioOnly**: Provides an MP4 stream containing only the audio. - **audioOnly,capped_4k**: Enables both MP4 video downloads (up to 4K) and an audio-only stream.<br/> | capped_4k                                                                                                                                                                                                                                                                                                                  |
| `retries`                                                                                                                                                                                                                                                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                           | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                         | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                        |                                                                                                                                                                                                                                                                                                                            |

### Response

**[models.UpdatedMp4SupportResponse](../../models/updatedmp4supportresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## list_unused_upload_urls

This endpoint retrieves a paginated list of all unused upload signed URLs within your organization. It provides comprehensive metadata including upload IDs, creation dates, status, and URLs, helping you manage your media resources efficiently.

An unused upload URL is a signed URL that gets generated when an user initiates upload but never completed the upload process. This can happen due to reasons like network issues, manual cancellation of upload, browser/app crashes or session timeouts.These URLs remain in the system as "unused" since they were created but never resulted in a successful media file upload.

#### How it works

 - The endpoint returns metadata for all unused upload URLs in your organization's library.
 - Results are paginated to manage large datasets effectively.
 - Signed URLs expire after 24 hours from creation.
 - Each entry includes full metadata about the unused upload.

#### Example

A video management team at a media organization regularly uploads content but often forgets to delete or use unused uploads. These unused uploads have signed URLs that expire after 24 hours and need to be managed efficiently. By using this API, the team can retrieve metadata for all unused uploads, identify expired signed URLs, and decide whether to regenerate URLs, reuse the uploads, or delete them.

### Example Usage

<!-- UsageSnippet language="python" operationID="list-uploads" method="get" path="/on-demand/uploads" -->
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

    res = fastpix.manage_videos.list_unused_upload_urls(limit=20, offset=1, order_by="desc")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `limit`                                                                                   | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Limit specifies the maximum number of items to display per page.                          | 20                                                                                        |
| `offset`                                                                                  | *Optional[int]*                                                                           | :heavy_minus_sign:                                                                        | Offset determines the starting point for data retrieval within a paginated list.          | 1                                                                                         |
| `order_by`                                                                                | [Optional[models.SortOrder]](../../models/sortorder.md)                                   | :heavy_minus_sign:                                                                        | The values in the list can be arranged in two ways: DESC (Descending) or ASC (Ascending). | desc                                                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.ListUploadsResponse](../../models/listuploadsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |