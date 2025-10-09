# Playback
(*playback*)

## Overview

### Available Operations

* [create_media_playback_id](#create_media_playback_id) - Create a playback ID
* [delete_media_playback_id](#delete_media_playback_id) - Delete a playback ID
* [get_playback_id](#get_playback_id) - Get a playback ID

## create_media_playback_id

You can create a new playback ID for a specific media asset. If you have already retrieved an existing `playbackId` using the <a href="https://docs.fastpix.io/reference/get-media">Get Media by ID</a> endpoint for a media asset, you can use this endpoint to generate a new playback ID with a specified access policy. 



If you want to create a private playback ID for a media asset that already has a public playback ID, this endpoint also allows you to do so by specifying the desired access policy. 

#### How it works

1. Make a `POST` request to this endpoint, replacing `<mediaId>` with the `uploadId` or `id` of the media asset. 

2. Include the `accessPolicy` in the request body with `private` or `public` as the value. 

3. Receive a response containing the newly created playback ID with the requested access level. 


#### Example
A video streaming service generates playback IDs for each media file when users request to view specific content. The playback ID is then used by the video player to stream the video.


### Example Usage

<!-- UsageSnippet language="python" operationID="create-media-playback-id" method="post" path="/on-demand/{mediaId}/playback-ids" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.playback.create_media_playback_id(media_id="dbb8a39a-e4a5-4120-9f22-22f603f1446e", access_policy="public", drm_configuration_id="123e4567-e89b-12d3-a456-426614174000", resolution="1080p")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                           | Type                                                                                                                | Required                                                                                                            | Description                                                                                                         | Example                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                          | *str*                                                                                                               | :heavy_check_mark:                                                                                                  | When creating the media, FastPix assigns a universally unique identifier with a maximum length of 255 characters.   | dbb8a39a-e4a5-4120-9f22-22f603f1446e                                                                                |
| `access_policy`                                                                                                     | [models.AccessPolicy](../../models/accesspolicy.md)                                                                 | :heavy_check_mark:                                                                                                  | Access policy for media content                                                                                     |                                                                                                                     |
| `access_restrictions`                                                                                               | [Optional[models.CreateMediaPlaybackIDAccessRestrictions]](../../models/createmediaplaybackidaccessrestrictions.md) | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |                                                                                                                     |
| `drm_configuration_id`                                                                                              | *Optional[str]*                                                                                                     | :heavy_minus_sign:                                                                                                  | DRM configuration ID (required if accessPolicy is 'drm')                                                            | 123e4567-e89b-12d3-a456-426614174000                                                                                |
| `resolution`                                                                                                        | [Optional[models.Resolution]](../../models/resolution.md)                                                           | :heavy_minus_sign:                                                                                                  | The maximum resolution for the playback ID.                                                                         | 1080p                                                                                                               |
| `retries`                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                    | :heavy_minus_sign:                                                                                                  | Configuration to override the default retry behavior of the client.                                                 |                                                                                                                     |

### Response

**[models.CreateMediaPlaybackIDResponse](../../models/createmediaplaybackidresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## delete_media_playback_id

This endpoint allows you to remove a specific playback ID associated with a media asset. Deleting a `playbackId` will revoke access to the media content linked to that ID. 


#### How it works

1. Make a `DELETE` request to this endpoint, replacing `<mediaId>` with the unique ID of the media asset from which you want to delete the playback ID. 

2. Specify the `playbackId` you wish to delete in the request body. 

#### Example

Your platform offers limited-time access to premium content. When the subscription expires, you can revoke access to the content by deleting the associated playback ID, preventing users from streaming the video further.


### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media-playback-id" method="delete" path="/on-demand/{mediaId}/playback-ids" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.playback.delete_media_playback_id(media_id="dbb8a39a-e4a5-4120-9f22-22f603f1446e", playback_id="dbb8a39a-e4a5-4120-9f22-22f603f1446e")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                             | Type                                                                                                  | Required                                                                                              | Description                                                                                           | Example                                                                                               |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                            | *str*                                                                                                 | :heavy_check_mark:                                                                                    | Return the universal unique identifier for media which can contain a maximum of 255 characters.       | dbb8a39a-e4a5-4120-9f22-22f603f1446e                                                                  |
| `playback_id`                                                                                         | *str*                                                                                                 | :heavy_check_mark:                                                                                    | Return the universal unique identifier for playbacks  which can contain a maximum of 255 characters.  | dbb8a39a-e4a5-4120-9f22-22f603f1446e                                                                  |
| `retries`                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                      | :heavy_minus_sign:                                                                                    | Configuration to override the default retry behavior of the client.                                   |                                                                                                       |

### Response

**[models.DeleteMediaPlaybackIDResponse](../../models/deletemediaplaybackidresponse.md)**

### Errors

| Error Type                          | Status Code                         | Content Type                        |
| ----------------------------------- | ----------------------------------- | ----------------------------------- |
| errors.InvalidPermissionError       | 401                                 | application/json                    |
| errors.ForbiddenError               | 403                                 | application/json                    |
| errors.MediaOrPlaybackNotFoundError | 404                                 | application/json                    |
| errors.ValidationErrorResponse      | 422                                 | application/json                    |
| errors.FastpixDefaultError          | 4XX, 5XX                            | \*/\*                               |

## get_playback_id

This endpoint retrieves details about a specific playback ID associated with a media asset. This endpoint is commonly used to check the access policy (e.g., public or private) with the specific playback ID.

**How it works:**
1. Make a GET request to the endpoint, replacing `{mediaId}` with the `id` of the media, and `{playbackId}` with the specific playback ID.
2. Useful for auditing or validation before granting playback access in your application.

**Example:**
A media platform might use this endpoint to verify if a playback ID is public or private before embedding the video in a frontend player or allowing access to a restricted group.


### Example Usage

<!-- UsageSnippet language="python" operationID="get-playback-id" method="get" path="/on-demand/{mediaId}/playback-ids/{playbackId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.playback.get_playback_id(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", playback_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `media_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                |
| `playback_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GetPlaybackIDResponse](../../models/getplaybackidresponse.md)**

### Errors

| Error Type                          | Status Code                         | Content Type                        |
| ----------------------------------- | ----------------------------------- | ----------------------------------- |
| errors.InvalidPermissionError       | 401                                 | application/json                    |
| errors.ForbiddenError               | 403                                 | application/json                    |
| errors.MediaOrPlaybackNotFoundError | 404                                 | application/json                    |
| errors.ValidationErrorResponse      | 422                                 | application/json                    |
| errors.FastpixDefaultError          | 4XX, 5XX                            | \*/\*                               |