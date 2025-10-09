# InVideoAIFeatures
(*in_video_ai_features*)

## Overview

### Available Operations

* [update_media_summary](#update_media_summary) - Generate video summary
* [update_media_chapters](#update_media_chapters) - Generate video chapters
* [update_media_named_entities](#update_media_named_entities) - Generate named entities
* [update_media_moderation](#update_media_moderation) - Enable video moderation

## update_media_summary

This endpoint allows you to generate the summary for an existing media.

#### How it works
1. Send a PATCH request to this endpoint, replacing `<mediaId>` with the unique ID of the media for which you wish to generate a summary.
2. Include the `generate` parameter in the request body.
3. Include the `summaryLength` parameter, specify the desired length of the summary in words (e.g., 120 words), this determines how concise or detailed the summary will be. If no specific summary length is provided, the default length will be 100 words. 
4. The response will include the updated media data and confirmation of the changes applied.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaaisummaryready">video.mediaAI.summary.ready</a> webhook event to track and notify about the summary generation.





**Use case**: This is particularly useful when a user uploads a video and later chooses to generate a summary without needing to re-upload the video.

Related guide: <a href="https://docs.fastpix.io/docs/generate-video-summary">Video summary</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-summary" method="patch" path="/on-demand/{mediaId}/summary" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.in_video_ai_features.update_media_summary(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", generate=True, summary_length=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                           | Type                                                                                                                | Required                                                                                                            | Description                                                                                                         | Example                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                          | *str*                                                                                                               | :heavy_check_mark:                                                                                                  | The unique identifier assigned to the media when created. The value should be a valid UUID.<br/>                    | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                                |
| `generate`                                                                                                          | *bool*                                                                                                              | :heavy_check_mark:                                                                                                  | Enable or disable the summary feature for the media. Set to true to enable summary or false to disable.<br/>        | true                                                                                                                |
| `summary_length`                                                                                                    | *Optional[int]*                                                                                                     | :heavy_minus_sign:                                                                                                  | Specifies the desired word count for the generated summary. <br/>- The value must be between **30** and **250** words.<br/> | 100                                                                                                                 |
| `retries`                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                    | :heavy_minus_sign:                                                                                                  | Configuration to override the default retry behavior of the client.                                                 |                                                                                                                     |

### Response

**[models.UpdateMediaSummaryResponse](../../models/updatemediasummaryresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## update_media_chapters

This endpoint enables you to generate chapters for an existing media file.

#### How it works
1. Make a `PATCH` request to this endpoint, replacing `<mediaId>` with the ID of the media for which you want to generate chapters.
2. Include the `chapters` parameter in the request body to enable.
3. The response will contain the updated media data, confirming the changes made.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaaichaptersready">video.mediaAI.chapters.ready</a> webhook event to track and notify about the chapters generation.

**Use case:** This is particularly useful when a user uploads a video and later decides to enable chapters without re-uploading the entire video.

Related guide: <a href="https://docs.fastpix.io/reference/update-media-chapters">Video chapters</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-chapters" method="patch" path="/on-demand/{mediaId}/chapters" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.in_video_ai_features.update_media_chapters(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", chapters=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                      | Type                                                                                                           | Required                                                                                                       | Description                                                                                                    | Example                                                                                                        |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                     | *str*                                                                                                          | :heavy_check_mark:                                                                                             | The unique identifier assigned to the media when created. The value should be a valid UUID.<br/>               | 4fa85f64-5717-4562-b3fc-2c963f66afa6                                                                           |
| `chapters`                                                                                                     | *bool*                                                                                                         | :heavy_check_mark:                                                                                             | Enable or disable the chapters feature for the media. Set to `true` to enable chapters or `false` to disable.<br/> | true                                                                                                           |
| `retries`                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                               | :heavy_minus_sign:                                                                                             | Configuration to override the default retry behavior of the client.                                            |                                                                                                                |

### Response

**[models.UpdateMediaChaptersResponse](../../models/updatemediachaptersresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## update_media_named_entities

This endpoint allows you to extract named entities from an existing media.
Named Entity Recognition (NER) is a fundamental natural language processing (NLP) technique that identifies and classifies key information (entities) in text into predefined categories. For instance:

  - Organizations (e.g., "Microsoft", "United Nations")
  - Locations (e.g., "Paris", "Mount Everest")
  - Product names (e.g., "iPhone", "Coca-Cola")

#### How it works
1. Make a PATCH request to this endpoint, replacing `<mediaId>` with the ID of the media you want to extract named-entities.
2. Include the `namedEntities` parameter in the request body to enable.
3. Receive a response containing the updated media data, confirming the changes made.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaainamedentitiesready">video.mediaAI.named-entities.ready</a> webhook event to track and notify about the named entities extraction.

**Use case:** If a user uploads a video and later decides to enable named entity extraction without re-uploading the entire video.

Related guide: <a href="https://docs.fastpix.io/docs/generate-named-entities">Named entities</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-named-entities" method="patch" path="/on-demand/{mediaId}/named-entities" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.in_video_ai_features.update_media_named_entities(media_id="0cec3c88-c69d-4232-9b96-f0976327fa2d", named_entities=True)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                    | Type                                                                                         | Required                                                                                     | Description                                                                                  | Example                                                                                      |
| -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `media_id`                                                                                   | *str*                                                                                        | :heavy_check_mark:                                                                           | The unique identifier assigned to the media when created. The value should be a valid UUID.<br/> | 0cec3c88-c69d-4232-9b96-f0976327fa2d                                                         |
| `named_entities`                                                                             | *bool*                                                                                       | :heavy_check_mark:                                                                           | Enable or disable named entity extraction. Set to `true` to enable or `false` to disable.<br/> | true                                                                                         |
| `retries`                                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                             | :heavy_minus_sign:                                                                           | Configuration to override the default retry behavior of the client.                          |                                                                                              |

### Response

**[models.UpdateMediaNamedEntitiesResponse](../../models/updatemedianamedentitiesresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## update_media_moderation

This endpoint enables moderation features, such as NSFW and profanity filtering, to detect inappropriate content in existing media.

#### How it works
1. Make a PATCH request to this endpoint, replacing `<mediaId>` with the ID of the media you want to update.
2. Include the `moderation` object and provide the requried `type` parameter in the request body to specify the media type (e.g., video/audio/av).
4. The response will contain the updated media data, confirming the changes made.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaaimoderationready">video.mediaAI.moderation.ready</a> webhook event to track and notify about the detected moderation results.

**Use case:** This is particularly useful when a user uploads a video and later decides to enable moderation detection without the need to re-upload it.

Related guide: <a href="https://docs.fastpix.io/docs/using-nsfw-and-profanity-filter-for-video-moderation">Moderate NSFW & Profanity</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-moderation" method="patch" path="/on-demand/{mediaId}/moderation" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.in_video_ai_features.update_media_moderation(media_id="0cec3c88-c69d-4232-9b96-f0976327fa2d", moderation={
        "type": "video",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         | Example                                                                                             |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                          | *str*                                                                                               | :heavy_check_mark:                                                                                  | The unique identifier assigned to the media when created. The value should be a valid UUID.<br/>    | 0cec3c88-c69d-4232-9b96-f0976327fa2d                                                                |
| `moderation`                                                                                        | [Optional[models.UpdateMediaModerationModeration]](../../models/updatemediamoderationmoderation.md) | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |                                                                                                     |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |                                                                                                     |

### Response

**[models.UpdateMediaModerationResponse](../../models/updatemediamoderationresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ForbiddenError          | 403                            | application/json               |
| errors.MediaNotFoundError      | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |