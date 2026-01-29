# InVideoAIFeatures

## Overview

### Available Operations

* [update_summary](#update_summary) - Generate video summary
* [update_moderation](#update_moderation) - Enable video moderation
* [update_named_entities](#update_named_entities) - Generate named entities

## update_summary

This endpoint allows you to generate the summary for an existing media.

#### How it works
1. Send a `PATCH` request to this endpoint, replacing `<mediaId>` with the ID of the media you want to summarize.
2. Include the `generate` parameter in the request body.
3. Include the `summaryLength` parameter, specify the desired length of the summary in words (for example, 120 words), this determines how concise or detailed the summary will be. If no specific summary length is provided, the default length will be 100 words.
4. The response includes the updated media data and confirmation of the changes applied.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaaisummaryready">video.mediaAI.summary.ready</a> webhook event to track and notify about the summary generation.

**Use case**: This is particularly useful when a user uploads a video and later chooses to generate a summary without needing to re-upload the video.

Related guide: <a href="https://docs.fastpix.io/docs/generate-video-summary">Video summary</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-summary" method="patch" path="/on-demand/{mediaId}/summary" -->
```python
fimport os
import json

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

   
    res = fastpix.in_video_ai_features.update_summary(media_id="your-media-id", generate=True, summary_length=100)
    
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                           | Type                                                                                                                | Required                                                                                                            | Description                                                                                                         | Example                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                          | *str*                                                                                                               | :heavy_check_mark:                                                                                                  | The unique identifier assigned to the media when created. The value must be a valid UUID.<br/>                      | your-media-id                                                                                                     |
| `generate`                                                                                                          | *bool*                                                                                                              | :heavy_check_mark:                                                                                                  | Enable or disable the summary feature for the media. Set to true to enable summary or false to disable.<br/>        | true                                                                                                                |
| `summary_length`                                                                                                    | *Optional[int]*                                                                                                     | :heavy_minus_sign:                                                                                                  | Specifies the desired word count for the generated summary. <br/>- The value must be between **30** and **250** words.<br/> | 100                                                                                                                 |
| `retries`                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                    | :heavy_minus_sign:                                                                                                  | Configuration to override the default retry behavior of the client.                                                 |                                                                                                                     |

### Response

**[models.UpdateMediaSummaryResponse](../../models/updatemediasummaryresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_moderation

This endpoint enables moderation features, such as NSFW and profanity filtering, to detect inappropriate content in existing media.

#### How it works
1. Make a `PATCH` request to this endpoint, replacing `<mediaId>` with the ID of the media you want to update.
2. Include the `moderation` object and provide the requried `type` parameter in the request body to specify the media type (for example, video/audio/av).
4. The response contains the updated media data, confirming the changes made.

You can use the <a href="https://docs.fastpix.io/docs/ai-events#videomediaaimoderationready">video.mediaAI.moderation.ready</a> webhook event to track and notify about the detected moderation results.

**Use case:** This is particularly useful when a user uploads a video and later decides to enable moderation detection without the need to re-upload it.

Related guide: <a href="https://docs.fastpix.io/docs/using-nsfw-and-profanity-filter-for-video-moderation">Moderate NSFW & Profanity</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="update-media-moderation" method="patch" path="/on-demand/{mediaId}/moderation" -->
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

    res = fastpix.in_video_ai_features.update_moderation(media_id="your-media-id", moderation={
        "type": "video",
    })

       # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                           | Type                                                                                                | Required                                                                                            | Description                                                                                         | Example                                                                                             |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                          | *str*                                                                                               | :heavy_check_mark:                                                                                  | The unique identifier assigned to the media when created. The value must be a valid UUID.<br/>      | 0cec3c88-c69d-4232-9b96-f0976327fa2d                                                                |
| `moderation`                                                                                        | [Optional[models.UpdateMediaModerationModeration]](../../models/updatemediamoderationmoderation.md) | :heavy_minus_sign:                                                                                  | N/A                                                                                                 |                                                                                                     |
| `retries`                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                    | :heavy_minus_sign:                                                                                  | Configuration to override the default retry behavior of the client.                                 |                                                                                                     |

### Response

**[models.UpdateMediaModerationResponse](../../models/updatemediamoderationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_named_entities

This endpoint allows you to extract named entities from an existing media.
Named Entity Recognition (NER) is a fundamental natural language processing (NLP) technique that identifies and classifies key information (entities) in text into predefined categories. For instance:

  - Organizations (for example, "Microsoft", "United Nations")
  - Locations (for example, "Paris", "Mount Everest")
  - Product names (for example, "iPhone", "Coca-Cola")

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
import os
import json

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

   
    
    res = fastpix.in_video_ai_features.update_named_entities(media_id="your-media-id", named_entities=True)
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                  | Type                                                                                       | Required                                                                                   | Description                                                                                | Example                                                                                    |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `media_id`                                                                                 | *str*                                                                                      | :heavy_check_mark:                                                                         | The unique identifier assigned to the media when created. The value must be a valid UUID.<br/> | 0cec3c88-c69d-4232-9b96-f0976327fa2d                                                       |
| `named_entities`                                                                           | *bool*                                                                                     | :heavy_check_mark:                                                                         | Enable or disable named entity extraction. Set to `true` to enable or `false` to disable.<br/> | true                                                                                       |
| `retries`                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                           | :heavy_minus_sign:                                                                         | Configuration to override the default retry behavior of the client.                        |                                                                                            |

### Response

**[models.UpdateMediaNamedEntitiesResponse](../../models/updatemedianamedentitiesresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |