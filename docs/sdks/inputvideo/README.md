# InputVideo
(*input_video*)

## Overview

### Available Operations

* [create_media](#create_media) - Create media from URL
* [direct_upload_video_media](#direct_upload_video_media) - Upload media from device

## create_media

This endpoint allows developers or users to create a new video or audio media in FastPix using a publicly accessible URL. FastPix will fetch the media from the provided URL, process it, and store it on the platform for use. 



#### Public URL requirement:


  The provided URL must be publicly accessible and should point to a video stored in one of the following supported formats: .m4v, .ogv, .mpeg, .mov, .3gp, .f4v, .rm, .ts, .wtv, .avi, .mp4, .wmv, .webm, .mts, .vob, .mxf, asf, m2ts 



#### Supported storage types:

The URL can originate from various cloud storage services or content delivery networks (CDNs) such as: 


* **Amazon S3:** URLs from Amazon's Simple Storage Service. 

* **Google Cloud Storage:** URLs from Google Cloud's storage solution. 

* **Azure Blob Storage:** URLs from Microsoft's Azure storage. 

* **Public CDNs:** URLs from public content delivery networks that host video files. 

Upon successful creation, the API returns an `id` that should be retained for future operations related to this media. 

#### How it works


1. Send a POST request to this endpoint with the media URL (typically a video or audio file) and optional media settings. 

2. FastPix uploads the video from the provided URL to its storage. 

3. Receive a response containing the unique id for the newly created media item. 

4. Use the id in subsequent API calls, such as checking the status of the media with the <a href="https://docs.fastpix.io/reference/get-media">Get Media by ID</a> endpoint to determine when the media is ready for playback. 

FastPix uses webhooks to tell your application about things that happen in the background, outside of the API regular request flow. For instance, once the media file is created (but not yet processed or encoded), we'll shoot a `POST` message to the address you give us with the webhook event <a href="https://docs.fastpix.io/docs/media-events#videomediacreated">video.media.created</a>. 


Once processing is done you can look for the events <a href="https://docs.fastpix.io/docs/media-events#/videomediaready">video.media.ready<a/> and <a href="https://docs.fastpix.io/docs/media-events#videomediafailed">video.media.failed</a> to see the status of your new media file.

Related guide: <a href="https://docs.fastpix.io/docs/upload-videos-from-url">Upload videos from URL</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="create-media" method="post" path="/on-demand" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(inputs=[
        {
            "type": "video",
            "url": "https://static.fastpix.io/sample.mp4",
        },
    ], access_policy="public", metadata={
        "key1": "value1",
    }, subtitles={
        "language_name": "english",
        "metadata": {
            "key1": "value1",
        },
        "language_code": "en",
    }, mp4_support="capped_4k", source_access=True, optimize_audio=True, max_resolution="1080p", summary={
        "generate": True,
    }, chapters=True, named_entities=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                              | Type                                                                                                                                                                                                                                                                   | Required                                                                                                                                                                                                                                                               | Description                                                                                                                                                                                                                                                            | Example                                                                                                                                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `inputs`                                                                                                                                                                                                                                                               | List[[models.Input](../../models/input.md)]                                                                                                                                                                                                                            | :heavy_check_mark:                                                                                                                                                                                                                                                     | N/A                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                        |
| `access_policy`                                                                                                                                                                                                                                                        | [models.CreateMediaRequestAccessPolicy](../../models/createmediarequestaccesspolicy.md)                                                                                                                                                                                | :heavy_check_mark:                                                                                                                                                                                                                                                     | Determines whether access to the streamed content is kept private or available to all.<br/>                                                                                                                                                                            | public                                                                                                                                                                                                                                                                 |
| `metadata`                                                                                                                                                                                                                                                             | Dict[str, *str*]                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | You can search for videos with specific key value pairs using metadata, when you tag a video in "key" : "value" pairs. Dynamic Metadata allows you to define a key that allows any value pair. You can have maximum of 255 characters and upto 10 entries are allowed. | {<br/>"key1": "value1"<br/>}                                                                                                                                                                                                                                           |
| `subtitles`                                                                                                                                                                                                                                                            | [Optional[models.Subtitles]](../../models/subtitles.md)                                                                                                                                                                                                                | :heavy_minus_sign:                                                                                                                                                                                                                                                     | Generates subtitle files for audio/video files.<br/>                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                        |
| `mp4_support`                                                                                                                                                                                                                                                          | [Optional[models.CreateMediaRequestMp4Support]](../../models/createmediarequestmp4support.md)                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                                     | "capped_4k": Generates an mp4 video file up to 4k resolution "audioOnly": Generates an m4a audio file of the media file "audioOnly,capped_4k": Generates both video and audio media files for offline viewing<br/>                                                     | capped_4k                                                                                                                                                                                                                                                              |
| `source_access`                                                                                                                                                                                                                                                        | *Optional[bool]*                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | The sourceAccess parameter determines whether the original media file is accessible. Set to true to enable access or false to restrict it                                                                                                                              | true                                                                                                                                                                                                                                                                   |
| `optimize_audio`                                                                                                                                                                                                                                                       | *Optional[bool]*                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | normalize volume of the audio track. This is available for pre-recorded content only.<br/>                                                                                                                                                                             | true                                                                                                                                                                                                                                                                   |
| `max_resolution`                                                                                                                                                                                                                                                       | [Optional[models.CreateMediaRequestMaxResolution]](../../models/createmediarequestmaxresolution.md)                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                     | The maximum resolution tier determines the highest quality your media will be available in.<br/>                                                                                                                                                                       | 1080p                                                                                                                                                                                                                                                                  |
| `summary`                                                                                                                                                                                                                                                              | [Optional[models.Summary]](../../models/summary.md)                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                     | N/A                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                        |
| `chapters`                                                                                                                                                                                                                                                             | *Optional[bool]*                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | Enable or disable the chapters feature for the media. Set to `true` to enable chapters or `false` to disable.<br/>                                                                                                                                                     | true                                                                                                                                                                                                                                                                   |
| `named_entities`                                                                                                                                                                                                                                                       | *Optional[bool]*                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | Enable or disable named entity extraction. Set to `true` to enable or `false` to disable.<br/>                                                                                                                                                                         | true                                                                                                                                                                                                                                                                   |
| `moderation`                                                                                                                                                                                                                                                           | [Optional[models.Moderation]](../../models/moderation.md)                                                                                                                                                                                                              | :heavy_minus_sign:                                                                                                                                                                                                                                                     | N/A                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                        |
| `access_restrictions`                                                                                                                                                                                                                                                  | [Optional[models.CreateMediaRequestAccessRestrictions]](../../models/createmediarequestaccessrestrictions.md)                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                                     | N/A                                                                                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                        |
| `retries`                                                                                                                                                                                                                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                     | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                    |                                                                                                                                                                                                                                                                        |

### Response

**[models.CreateMediaSuccessResponse](../../models/createmediasuccessresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.BadRequestError         | 400                            | application/json               |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## direct_upload_video_media

This endpoint enables accelerated uploads of large media files directly from your local device to FastPix for processing and storage.

> **PLEASE NOTE**
>
> This version now supports uploads with no file size limitations and offers faster uploads. The previous endpoint (which had a 500MB size limit) is now deprecated. You can find details in the [changelog](https://docs.fastpix.io/changelog/api-update-direct-upload-media-from-device).

#### How it works

1. Send a POST request to this endpoint with optional media settings.  

2. The response includes an `uploadId` and a signed `url` for direct video file upload.

3. Upload your video file to the provided `url` by making `PUT` request. The API accepts the media file from the device and uploads it to the FastPix platform. 

4. Once uploaded, the media undergoes processing and is assigned a unique ID for tracking. Retain this `uploadId` for any future operations related to this upload. 




After uploading, you can use the <a href="https://docs.fastpix.io/reference/get-media">Get Media by ID</a> endpoint to check the status of the uploaded media asset and see if it has transitioned to a `ready` status for playback. 

To notify your application about the status of this API request check for the webhooks for <a href="https://docs.fastpix.io/docs/webhooks-collection#media-related-events">media related events</a>.  


#### Example

A social media platform allows users to upload video content directly from their phones or computers. This endpoint facilitates the upload process. For example, if you are developing a video-sharing app where users can upload short clips from their mobile devices, this endpoint enables them to select a video, upload it to the platform.

Related guide: <a href="https://docs.fastpix.io/docs/upload-videos-directly">Upload videos directly</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="direct-upload-video-media" method="post" path="/on-demand/upload" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.direct_upload_video_media(request=models.DirectUploadVideoMediaRequest(
        cors_origin="*",
        push_media_settings=models.PushMediaSettings(
            access_policy="public",
            metadata={
                "key1": "value1",
            },
        ),
    ))

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                             | Type                                                                                  | Required                                                                              | Description                                                                           |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `request`                                                                             | [models.DirectUploadVideoMediaRequest](../../models/directuploadvideomediarequest.md) | :heavy_check_mark:                                                                    | The request object to use for the request.                                            |
| `retries`                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                      | :heavy_minus_sign:                                                                    | Configuration to override the default retry behavior of the client.                   |

### Response

**[models.DirectUploadVideoMediaResponse](../../models/directuploadvideomediaresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.BadRequestError         | 400                            | application/json               |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |