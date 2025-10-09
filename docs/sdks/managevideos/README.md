# ManageVideos
(*manage_videos*)

## Overview

### Available Operations

* [list_media](#list_media) - Get list of all media
* [list_live_clips](#list_live_clips) - Get all clips of a live stream
* [get_media](#get_media) - Get a media by ID
* [updated_media](#updated_media) - Update a media by ID
* [delete_media](#delete_media) - Delete a media by ID
* [add_media_track](#add_media_track) - Add audio / subtitle track
* [cancel_upload](#cancel_upload) - Cancel ongoing upload
* [update_media_track](#update_media_track) - Update audio / subtitle track
* [delete_media_track](#delete_media_track) - Delete audio / subtitle track
* [generate_subtitle_track](#generate_subtitle_track) - Generate track subtitle
* [updated_source_access](#updated_source_access) - Update the source access of a media by ID
* [updated_mp4_support](#updated_mp4_support) - Update the mp4Support of a media by ID
* [retrieve_media_input_info](#retrieve_media_input_info) - Get info of media inputs
* [list_uploads](#list_uploads) - Get all unused upload URLs
* [get_media_clips](#get_media_clips) - Get all clips of a media

## list_media

This endpoint returns a list of all media files uploaded to FastPix within a specific workspace. Each media entry contains data such as the media `id`, `createdAt`, `status`, `type` and more. It allows you to retrieve an overview of your media assets, making it easier to manage and review them. 


#### How it works

Use the access token and secret key related to the workspace in the request header. When called, the API provides a paginated response containing all the media items in that specific workspace. This is helpful for retrieving a large volume of media and managing content in bulk. 



#### Example
You're managing a video platform and need to check all the uploaded media in your library to ensure no outdated or low-quality content is being served. Using this endpoint, you can retrieve a complete list of media, allowing you to filter, sort, or update items as needed.


### Example Usage

<!-- UsageSnippet language="python" operationID="list-media" method="get" path="/on-demand" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.list_media(limit=20, offset=1, order_by="desc")

    # Handle response
    print(res)

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

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## list_live_clips

Retrieves a list of all media clips generated from a specific livestream. Each media entry includes metadata such as the clip media IDs, and other relevant details. A media clip is a segmented portion of an original media file (source live stream). Clips are often created for various purposes such as previews, highlights, or customized edits.
#### How it works
To use this endpoint, provide the `livestreamId` as a parameter. The API then returns a paginated list of clipped media items created from that livestream. Pagination ensures optimal performance and usability when dealing with a large number of media files, making it easier to organize and manage content in bulk.

Related guide: <a href="https://docs.fastpix.io/docs/instant-live-clipping">Instant live clipping</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="list-live-clips" method="get" path="/on-demand/{livestreamId}/live-clips" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.list_live_clips(livestream_id="b6f71268143f70c798a7851a0a92dcbf", limit=20, offset=1, order_by="desc")

    # Handle response
    print(res)

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

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## get_media

By calling this endpoint, you can retrieve detailed information about a specific media item, including its current `status` and a `playbackId`. This is particularly useful for retrieving specific media details when managing large content libraries. 



#### How it works 



1. Make a GET request to this endpoint, using the `<mediaId>` received after uploading the media file. 


2. Receive a response that includes details about the media: 

* `status` Indicates whether the media is still `preparing` or has transitioned to `ready`.  

* The `playbackId` is a unique identifier that allows you to stream the media once it is `ready`. You can construct the stream URL in this format: `https://stream.fastpix.io/<playbackId>.m3u8`


#### Example

Suppose your platform provides users with an interface where they can manage their uploaded content. A user requests detailed information about a specific video to see if it has been fully processed and is available for playback. Using the media ID, you can fetch the information from FastPix and display it in the user's dashboard.


### Example Usage

<!-- UsageSnippet language="python" operationID="get-media" method="get" path="/on-demand/{mediaId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.get_media(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                              | Type                                                                                                   | Required                                                                                               | Description                                                                                            | Example                                                                                                |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| `media_id`                                                                                             | *str*                                                                                                  | :heavy_check_mark:                                                                                     | The Media Id is assigned a universal unique identifier, which can contain a maximum of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                   |
| `retries`                                                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                       | :heavy_minus_sign:                                                                                     | Configuration to override the default retry behavior of the client.                                    |                                                                                                        |

### Response

**[models.GetMediaResponse](../../models/getmediaresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## updated_media

This endpoint allows you to update specific parameters of an existing media file. You can modify the key-value pairs of the metadata that were provided in the payload during the creation of media from a URL or when uploading the media directly from device. 


#### How it works

1. Make a PATCH request to this endpoint, replacing `<mediaId>` with the unique ID (`uploadId` or `id`) of the media received after uploading to FastPix. 

2. Include the updated parameters in the request body. 

3. Receive a response containing the updated media data, confirming the changes made. 

Once you have made the update request, you can also look for the webhook event <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> to notify your system about update status. 

#### Example
Imagine a scenario where a user uploads a video and later realizes they need to change the title, add a new description or tags. You can use this endpoint to update the media metadata without having to re-upload the entire video.


### Example Usage

<!-- UsageSnippet language="python" operationID="updated-media" method="patch" path="/on-demand/{mediaId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.updated_media(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", metadata={
        "metadata": "{\"user\":\"fastpix_admin\"}",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                         | Type                                                                                                              | Required                                                                                                          | Description                                                                                                       | Example                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `metadata`                                                                                                        | Dict[str, *str*]                                                                                                  | :heavy_minus_sign:                                                                                                | N/A                                                                                                               | {<br/>"metadata": {<br/>"user": "fastpix_admin"<br/>}<br/>}                                                       |
| `retries`                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                  | :heavy_minus_sign:                                                                                                | Configuration to override the default retry behavior of the client.                                               |                                                                                                                   |

### Response

**[models.UpdatedMediaResponse](../../models/updatedmediaresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## delete_media

This endpoint allows you to permanently delete a a specific video or audio media file along with all associated data. If you wish to remove a media from FastPix storage, use this endpoint with the `mediaId` (either `uploadId` or `id`) received during the media's creation or upload. 


#### How it works


1. Make a DELETE request to this endpoint, replacing `<mediaId>` with the `uploadId` or the `id` of the media you want to delete. 

2. Since this action is irreversible, ensure that you no longer need the media before proceeding. Once deleted, the media cannot be retrieved or played back. 

3. Webhook event to look for: <a href="https://docs.fastpix.io/docs/media-events#videomediadeleted">video.media.deleted</a>

#### Example
A user on a video-sharing platform decides to remove an old video from their profile, or suppose you're running a content moderation system, and one of the videos uploaded by a user violates your platform's policies. Using this endpoint, the media is permanently deleted from your library, ensuring it's no longer accessible or viewable by other users.


### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media" method="delete" path="/on-demand/{mediaId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.delete_media(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                         | Type                                                                                                              | Required                                                                                                          | Description                                                                                                       | Example                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `retries`                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                  | :heavy_minus_sign:                                                                                                | Configuration to override the default retry behavior of the client.                                               |                                                                                                                   |

### Response

**[models.DeleteMediaResponse](../../models/deletemediaresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## add_media_track

This endpoint allows you to add an audio or subtitle track to an existing media file using its `mediaId`. You need to provide the track `url` along with its `type` (audio or subtitle), `languageName` and `languageCode` in the request payload.


#### How it works

1. Send a POST request to this endpoint, replacing `{mediaId}` with the media ID (`uploadId` or `id`).

2. Provide the necessary details in the request body.

3. Receive a response containing a unique track ID and the details of the newly added track.


#### Webhook events

1. After successfully adding a track, your system will receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackcreated">video.media.track.created</a>.

2. Once the track is processed and ready, you will receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackready">video.media.track.ready</a>.

3. Finally, an update event <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> will notify your system about the media's updated status.


#### Example
Suppose you have a video uploaded to the FastPix platform, and you want to add an Italian audio track to it. By calling this API, you can attach an external audio file (https://static.fastpix.io/music-1.mp3) to the media file. Similarly, if you need to add subtitles in different languages, you can specify type: `subtitle` with the corresponding subtitle `url`, `languageCode` and `languageName`.

Related guides: <a href="https://docs.fastpix.io/docs/manage-subtitle-tracks">Add own subtitle tracks</a>, <a href="https://docs.fastpix.io/docs/manage-audio-tracks">Add own audio tracks</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="Add-media-track" method="post" path="/on-demand/{mediaId}/tracks" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.add_media_track(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", tracks={
        "url": "https://static.fastpix.io/music-1.mp3",
        "type": "audio",
        "language_code": "it",
        "language_name": "Italian",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                         | Type                                                                                                              | Required                                                                                                          | Description                                                                                                       | Example                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `tracks`                                                                                                          | [Optional[models.AddTrackRequest]](../../models/addtrackrequest.md)                                               | :heavy_minus_sign:                                                                                                | Contains details about the track being added to the media file.                                                   |                                                                                                                   |
| `retries`                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                  | :heavy_minus_sign:                                                                                                | Configuration to override the default retry behavior of the client.                                               |                                                                                                                   |

### Response

**[models.AddMediaTrackResponse](../../models/addmediatrackresponse.md)**

### Errors

| Error Type                        | Status Code                       | Content Type                      |
| --------------------------------- | --------------------------------- | --------------------------------- |
| errors.TrackDuplicateRequestError | 400                               | application/json                  |
| errors.InvalidPermissionError     | 401                               | application/json                  |
| errors.ForbiddenError             | 403                               | application/json                  |
| errors.MediaNotFoundError         | 404                               | application/json                  |
| errors.ValidationErrorResponse    | 422                               | application/json                  |
| errors.FastpixDefaultError        | 4XX, 5XX                          | \*/\*                             |

## cancel_upload

This endpoint allows you to cancel ongoing upload by its `uploadId`. Once cancelled, the upload will be marked as cancelled. Use this if a user aborts an upload or if you want to programmatically stop an in-progress upload.

#### How it works

1. Make a PUT request to this endpoint, replacing `{uploadId}` with the unique upload ID received after starting the upload.
2. The response will confirm the cancellation and provide the status of the upload.

#### Webhook Events

Once the upload is cancelled, you will receive the webhook event <a href="https://docs.fastpix.io/docs/media-events#videomediauploadcancelled-event">video.media.upload.cancelled</a>.

#### Example

Suppose a user starts uploading a large video file but decides to cancel before completion. By calling this API, you can immediately stop the upload and free up resources.


### Example Usage

<!-- UsageSnippet language="python" operationID="cancel-upload" method="put" path="/on-demand/upload/{uploadId}/cancel" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.cancel_upload(upload_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                          | Type                                                                                                               | Required                                                                                                           | Description                                                                                                        | Example                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| `upload_id`                                                                                                        | *str*                                                                                                              | :heavy_check_mark:                                                                                                 | When uploading the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                               |
| `retries`                                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                   | :heavy_minus_sign:                                                                                                 | Configuration to override the default retry behavior of the client.                                                |                                                                                                                    |

### Response

**[models.CancelUploadResponse](../../models/canceluploadresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.BadRequestError         | 400                            | application/json               |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## update_media_track

This endpoint allows you to update an existing audio or subtitle track associated with a media file. When updating a track, you must provide the new track `url`, `languageName`, and `languageCode`, ensuring all three parameters are included in the request.


#### How it works

1. Send a PATCH request to this endpoint, replacing `{mediaId}` with the media ID, and `{trackId}` with the ID of the track you want to update.

2. Provide the necessary details in the request body.

3. Receive a response confirming the track update.

#### Webhook Events

After updating a track, your system will receive webhook notifications:

1. After successfully updating a track, your system will receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackupdated">video.media.track.updated</a>.

2. Once the new track is processed and ready, you will receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediatrackready">video.media.track.ready</a>.

3. Once the media file is updated with the new track details, a <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> event will be triggered.


#### Example
Suppose you previously added a French subtitle track to a video but now need to update it with a different file. By calling this API, you can replace the existing subtitle file (.vtt) with a new one while keeping the same track ID. This is useful when:

  - The original track file has errors and needs correction.
  - You want to improve subtitle translations or replace an audio track with a better-quality version.
  
Related guides: <a href="https://docs.fastpix.io/docs/manage-subtitle-tracks">Add own subtitle tracks</a>, <a href="https://docs.fastpix.io/docs/manage-audio-tracks">Add own audio tracks</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-track" method="patch" path="/on-demand/{mediaId}/tracks/{trackId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.update_media_track(track_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", url="http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.vtt", language_code="fr", language_name="french")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                         | Type                                                                                                              | Required                                                                                                          | Description                                                                                                       | Example                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `track_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `media_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `url`                                                                                                             | *Optional[str]*                                                                                                   | :heavy_minus_sign:                                                                                                | The direct URL of the track file. It should point to a valid audio or subtitle file.                              | http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.vtt                                  |
| `language_code`                                                                                                   | *Optional[str]*                                                                                                   | :heavy_minus_sign:                                                                                                | The BCP 47 language code representing the track's language.                                                       | fr                                                                                                                |
| `language_name`                                                                                                   | *Optional[str]*                                                                                                   | :heavy_minus_sign:                                                                                                | The full name of the language corresponding to the `languageCode`.                                                | french                                                                                                            |
| `retries`                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                  | :heavy_minus_sign:                                                                                                | Configuration to override the default retry behavior of the client.                                               |                                                                                                                   |

### Response

**[models.UpdateMediaTrackResponse](../../models/updatemediatrackresponse.md)**

### Errors

| Error Type                        | Status Code                       | Content Type                      |
| --------------------------------- | --------------------------------- | --------------------------------- |
| errors.TrackDuplicateRequestError | 400                               | application/json                  |
| errors.InvalidPermissionError     | 401                               | application/json                  |
| errors.ForbiddenError             | 403                               | application/json                  |
| errors.MediaNotFoundError         | 404                               | application/json                  |
| errors.ValidationErrorResponse    | 422                               | application/json                  |
| errors.FastpixDefaultError        | 4XX, 5XX                          | \*/\*                             |

## delete_media_track

This endpoint allows you to delete an existing audio or subtitle track from a media file. Once deleted, the track will no longer be available for playback.


#### How it works


1. Send a DELETE request to this endpoint, replacing `{mediaId}` with the media ID, and `{trackId}` with the ID of the track you want to remove.

2. The track will be deleted from the media file, and you will receive a confirmation response.

#### Webhook events

1. After successfully deleting a track, your system will receive the webhook event **video.media.track.deleted**.

2. Once the media file is updated to reflect the track removal, a <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> event will be triggered.


#### Example
Suppose you uploaded an audio track in Italian for a video but later realize it's incorrect or no longer needed. By calling this API, you can remove the specific track while keeping the rest of the media file unchanged. This is useful when:

  - A track was mistakenly added and needs to be removed.
  - The content owner requests the removal of a specific subtitle or audio track.
  - A new version of the track will be uploaded to replace the existing one.
  
Related guides: <a href="https://docs.fastpix.io/docs/manage-subtitle-tracks">Add own subtitle tracks</a>, <a href="https://docs.fastpix.io/docs/manage-audio-tracks">Add own audio tracks</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media-track" method="delete" path="/on-demand/{mediaId}/tracks/{trackId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.delete_media_track(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", track_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                         | Type                                                                                                              | Required                                                                                                          | Description                                                                                                       | Example                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `track_id`                                                                                                        | *str*                                                                                                             | :heavy_check_mark:                                                                                                | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                              |
| `retries`                                                                                                         | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                  | :heavy_minus_sign:                                                                                                | Configuration to override the default retry behavior of the client.                                               |                                                                                                                   |

### Response

**[models.DeleteMediaTrackResponse](../../models/deletemediatrackresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## generate_subtitle_track

This endpoint allows you to generate subtitles for an existing audio track in a media file. By calling this API, you can generate subtitles automatically using speech recognition

#### How it works

1. Send a `POST` request to this endpoint, replacing `{mediaId}` with the media ID and `{trackId}` with the track ID.

2. Provide the necessary details in the request body, including the languageName and languageCode.

3. Receive a response containing a unique subtitle track ID and its details.

#### Webhook Events

1. Once the subtitle track is generated and ready, you will receive the webhook event <a href="https://docs.fastpix.io/docs/transform-media-events#videomediasubtitlegeneratedready">video.media.subtitle.generated.ready</a>.

2. Finally, an update event <a href="https://docs.fastpix.io/docs/media-events#videomediaupdated">video.media.updated</a> will notify your system about the media's updated status.

</br> Related guide: <a href="https://docs.fastpix.io/docs/add-auto-generated-subtitles-to-videos">Add auto-generated subtitles</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="Generate-subtitle-track" method="post" path="/on-demand/{mediaId}/tracks/{trackId}/generate-subtitles" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.generate_subtitle_track(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", track_id="d46f5df9-1a8f-4f0a-b56e-9f5b5d5b9e21", language_name="Italian", metadata={
        "key1": "value1",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                              | Type                                                                                                                                                                                                                                                                   | Required                                                                                                                                                                                                                                                               | Description                                                                                                                                                                                                                                                            | Example                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                                                                                                                                                                             | *str*                                                                                                                                                                                                                                                                  | :heavy_check_mark:                                                                                                                                                                                                                                                     | A universally unique identifier (UUID) assigned to the media by FastPix.                                                                                                                                                                                               | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                                                                                                                                                                   |
| `track_id`                                                                                                                                                                                                                                                             | *str*                                                                                                                                                                                                                                                                  | :heavy_check_mark:                                                                                                                                                                                                                                                     | A universally unique identifier (UUID) assigned to the specific track for which subtitles should be generated.                                                                                                                                                         | d46f5df9-1a8f-4f0a-b56e-9f5b5d5b9e21                                                                                                                                                                                                                                   |
| `language_name`                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                  | :heavy_check_mark:                                                                                                                                                                                                                                                     | The full name of the language in which subtitles will be generated.                                                                                                                                                                                                    | English                                                                                                                                                                                                                                                                |
| `language_code`                                                                                                                                                                                                                                                        | [models.LanguageCode](../../models/languagecode.md)                                                                                                                                                                                                                    | :heavy_check_mark:                                                                                                                                                                                                                                                     | Language code for content localization                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                        |
| `metadata`                                                                                                                                                                                                                                                             | Dict[str, *str*]                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | You can search for videos with specific key value pairs using metadata, when you tag a video in "key" : "value" pairs. Dynamic Metadata allows you to define a key that allows any value pair. You can have maximum of 255 characters and upto 10 entries are allowed. | {<br/>"key1": "value1"<br/>}                                                                                                                                                                                                                                           |
| `retries`                                                                                                                                                                                                                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                        |

### Response

**[models.GenerateSubtitleTrackResponse](../../models/generatesubtitletrackresponse.md)**

### Errors

| Error Type                        | Status Code                       | Content Type                      |
| --------------------------------- | --------------------------------- | --------------------------------- |
| errors.TrackDuplicateRequestError | 400                               | application/json                  |
| errors.InvalidPermissionError     | 401                               | application/json                  |
| errors.ForbiddenError             | 403                               | application/json                  |
| errors.MediaNotFoundError         | 404                               | application/json                  |
| errors.ValidationErrorResponse    | 422                               | application/json                  |
| errors.FastpixDefaultError        | 4XX, 5XX                          | \*/\*                             |

## updated_source_access

This endpoint allows you to update the `sourceAccess` setting of an existing media file. The `sourceAccess` parameter determines whether the original media file is accessible or restricted. Setting this to `true` enables access to the media source, while setting it to `false` restricts access. 

#### How it works

1. Make a `PATCH` request to this endpoint, replacing `{mediaId}` with the ID of the media you want to update.

2. Include the updated `sourceAccess` parameter in the request body.

3. Receive a response confirming the update to the media's source access status.
4. Webhook events: <a href="https://docs.fastpix.io/docs/transform-media-events#videomediasourceready">video.media.source.ready</a>, <a href="https://docs.fastpix.io/docs/transform-media-events#videomediasourcedeleted">video.media.source.deleted</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="updated-source-access" method="patch" path="/on-demand/{mediaId}/source-access" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.updated_source_access(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", source_access=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                  | Type                                                                                                                                       | Required                                                                                                                                   | Description                                                                                                                                | Example                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `media_id`                                                                                                                                 | *str*                                                                                                                                      | :heavy_check_mark:                                                                                                                         | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters.<br/>                     | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                                       |
| `source_access`                                                                                                                            | *Optional[bool]*                                                                                                                           | :heavy_minus_sign:                                                                                                                         | The sourceAccess parameter determines whether the original media file is accessible. Set to true to enable access or false to restrict it. | true                                                                                                                                       |
| `retries`                                                                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                           | :heavy_minus_sign:                                                                                                                         | Configuration to override the default retry behavior of the client.                                                                        |                                                                                                                                            |

### Response

**[models.UpdatedSourceAccessResponse](../../models/updatedsourceaccessresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## updated_mp4_support

This endpoint allows you to update the `mp4Support` setting of an existing media file using its media ID. You can specify the MP4 support level, such as `none`, `capped_4k`, `audioOnly`, or a combination of `audioOnly`, `capped_4k`, in the request payload.

#### How it works

1. Send a PATCH request to this endpoint, replacing `{mediaId}` with the media ID.

2. Provide the desired `mp4Support` value in the request body.

3. Receive a response confirming the update, including the media's updated MP4 support status.

#### MP4 Support Options

- `none` – MP4 support is disabled for this media.

- `capped_4k` – The media will have mp4 renditions up to 4K resolution.

- `audioOnly` – The media will generate an m4a file containing only the audio track.

- `audioOnly,capped_4k` – The media will have both an audio-only m4a file and mp4 renditions up to 4K resolution.

#### Webhook events

- <a href="https://docs.fastpix.io/docs/transform-media-events#videomediamp4supportready">video.media.mp4Support.ready</a> – Triggered when the MP4 support setting is successfully updated.

#### Example
Suppose you have a video uploaded to the FastPix platform, and you want to allow users to download the video in MP4 format. By setting "mp4Support": "capped_4k", the system will generate an MP4 rendition of the video up to 4K resolution, making it available for download via the stream URL(`https://stream.fastpix.io/{playbackId}/{capped-4k.mp4 | audio.m4a}`).
If you want users to stream only the audio from the media file, you can set "mp4Support": "audioOnly". This will provide an audio-only stream URL that allows users to listen to the media without video.
By setting "mp4Support": "audioOnly,capped_4k", both options will be enabled. Users will be able to download the MP4 video and also stream just the audio version of the media.


Related guide: <a href="https://docs.fastpix.io/docs/mp4-support-for-offline-viewing">Use MP4 support for offline viewing</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="updated-mp4Support" method="patch" path="/on-demand/{mediaId}/update-mp4Support" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.updated_mp4_support(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", mp4_support="capped_4k")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                           | Type                                                                                                                                                                                                                                                                                                                                | Required                                                                                                                                                                                                                                                                                                                            | Description                                                                                                                                                                                                                                                                                                                         | Example                                                                                                                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                                                                                                                                                                                                                                          | *str*                                                                                                                                                                                                                                                                                                                               | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                  | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters.<br/>                                                                                                                                                                                                              | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                                                                                                                                                                                                                                |
| `mp4_support`                                                                                                                                                                                                                                                                                                                       | [Optional[models.UpdatedMp4SupportMp4Support]](../../models/updatedmp4supportmp4support.md)                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                  | Determines the type of MP4 support for the media.   - **none**: Disables MP4 support.   - **capped_4k**: Enables MP4 downloads with resolutions up to 4K.   - **audioOnly**: Provides an MP4 stream containing only the audio.   - **audioOnly,capped_4k**: Enables both MP4 video downloads (up to 4K) and an audio-only stream.   | capped_4k                                                                                                                                                                                                                                                                                                                           |
| `retries`                                                                                                                                                                                                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                     |

### Response

**[models.UpdatedMp4SupportResponse](../../models/updatedmp4supportresponse.md)**

### Errors

| Error Type                      | Status Code                     | Content Type                    |
| ------------------------------- | ------------------------------- | ------------------------------- |
| errors.DuplicateMp4SupportError | 400                             | application/json                |
| errors.InvalidPermissionError   | 401                             | application/json                |
| errors.ForbiddenError           | 403                             | application/json                |
| errors.MediaNotFoundError       | 404                             | application/json                |
| errors.ValidationErrorResponse  | 422                             | application/json                |
| errors.FastpixDefaultError      | 4XX, 5XX                        | \*/\*                           |

## retrieve_media_input_info

Allows you to retrieve detailed information about the media inputs associated with a specific media item. You can use this endpoint to verify the media file's input URL, track creation status, and container format. The `mediaId` (either `uploadId` or `id`) must be provided to fetch the information. 


#### How it works

Upon making a `GET` request with the mediaId, FastPix returns a response with: 

* The public storage input `url` of the uploaded media file. 

* Information about the `tracks` associated with the media, including both video and audio tracks, indicating whether they have been successfully created. 

* The format of the uploaded media file container (e.g., MP4, MKV). 

This endpoint is particularly useful for ensuring that all necessary tracks (video and audio) have been correctly associated with the media during the upload or media creation process.


### Example Usage

<!-- UsageSnippet language="python" operationID="retrieveMediaInputInfo" method="get" path="/on-demand/{mediaId}/input-info" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.retrieve_media_input_info(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                 | Type                                                                                      | Required                                                                                  | Description                                                                               | Example                                                                                   |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `media_id`                                                                                | *str*                                                                                     | :heavy_check_mark:                                                                        | Pass the list of the input objects used to create the media, along with applied settings. | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                      |
| `retries`                                                                                 | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                          | :heavy_minus_sign:                                                                        | Configuration to override the default retry behavior of the client.                       |                                                                                           |

### Response

**[models.RetrieveMediaInputInfoResponse](../../models/retrievemediainputinforesponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## list_uploads

This endpoint retrieves a paginated list of all unused upload signed URLs within your organization. It provides comprehensive metadata including upload IDs, creation dates, status, and URLs, helping you manage your media resources efficiently.

An unused upload URL is a signed URL that gets generated when an user initiates upload but never completed the upload process. This can happen due to reasons like network issues, manual cancellation of upload, browser/app crashes or session timeouts.These URLs remain in the system as "unused" since they were created but never resulted in a successful media file upload.

#### How it works

 - The endpoint returns metadata for all unused upload URLs in your organization's library.
 - Results are paginated to manage large datasets effectively.
 - Signed URLs expire after 24 hours from creation.
 - Each entry includes full metadata about the unused upload.



#### Example

A video management team for a media organization regularly uploads content to their system but often forgets to delete or utilize unused uploads. These unused uploads, which have signed URLs that expire after 24 hours, need to be managed efficiently. By using this API, they can retrieve metadata for all unused uploads, identify expired signed URLs, and decide whether to regenerate URLs, reuse the uploads, or delete them.


### Example Usage

<!-- UsageSnippet language="python" operationID="list-uploads" method="get" path="/on-demand/uploads" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.list_uploads(limit=20, offset=1, order_by="desc")

    # Handle response
    print(res)

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

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## get_media_clips

This endpoint retrieves a list of all media clips associated with a given source media ID. It helps in organizing and managing media's efficiently by providing metadata, including clip media IDs and other relevant details.

A media clip is a segmented portion of an original media file (source media). Clips are often created for various purposes such as previews, highlights, or customized edits. This API allows you to fetch all such clips linked to a specific source media, making it easier to track and manage clips.


#### How it works

- The endpoint returns metadata for all media clips associated with the given `sourceMediaId`.
- Results are paginated to efficiently handle large datasets.
- Each entry includes detailed metadata such as media `id`, `duration`, and `status`.
- Helps in organizing clips effectively by providing structured information.


#### Example

Imagine you're managing a video editing platform where users upload full-length videos and create short clips for social media sharing. To keep track of all clips linked to a particular video, you call this API with the sourceMediaId. The response provides a list of all associated clips, allowing you to manage, edit, or repurpose them as needed.

Related guide: <a href="https://docs.fastpix.io/docs/create-clips-from-existing-media">Create clips from existing media</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="get-media-clips" method="get" path="/on-demand/{sourceMediaId}/media-clips" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.manage_videos.get_media_clips(source_media_id="fc733e3f-2fba-4c3d-9388-2511dc50d15f", offset=5, limit=20, order_by="desc")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                | Type                                                                                     | Required                                                                                 | Description                                                                              | Example                                                                                  |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `source_media_id`                                                                        | *str*                                                                                    | :heavy_check_mark:                                                                       | The unique identifier of the source media.                                               | fc733e3f-2fba-4c3d-9388-2511dc50d15f                                                     |
| `offset`                                                                                 | *Optional[int]*                                                                          | :heavy_minus_sign:                                                                       | Offset determines the starting point for data retrieval within a paginated list.         | 5                                                                                        |
| `limit`                                                                                  | *Optional[int]*                                                                          | :heavy_minus_sign:                                                                       | The number of media clips to retrieve per request.                                       | 20                                                                                       |
| `order_by`                                                                               | [Optional[models.SortOrder]](../../models/sortorder.md)                                  | :heavy_minus_sign:                                                                       | The values in the list can be arranged in two ways DESC (Descending) or ASC (Ascending). | desc                                                                                     |
| `retries`                                                                                | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                         | :heavy_minus_sign:                                                                       | Configuration to override the default retry behavior of the client.                      |                                                                                          |

### Response

**[models.MediaClipResponse](../../models/mediaclipresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaClipNotFoundError  | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |