# Playback

## Overview

Operations for video playback management

### Available Operations

* [create](#create) - Create a playback ID
* [list_playback_ids](#list_playback_ids) - Get all playback IDs details for a media
* [delete](#delete) - Delete a playback ID
* [get_by_id](#get_by_id) - Get a playback ID
* [update_domain_restrictions](#update_domain_restrictions) - Update domain restrictions for a playback ID
* [update_user_agent_restrictions](#update_user_agent_restrictions) - Update user-agent restrictions for a playback ID

## create

You can create a new playback ID for a specific media asset. If you have already retrieved an existing `playbackId` using the <a href="https://docs.fastpix.io/reference/get-media">Get Media by ID</a> endpoint for a media asset, you can use this endpoint to generate a new playback ID with a specified access policy. 

If you want to create a private playback ID for a media asset that already has a public playback ID, this endpoint also allows you to do so by specifying the desired access policy. 

#### How it works

1. Make a `POST` request to this endpoint, replacing `<mediaId>` with the `uploadId` or `id` of the media asset. 

2. Include the `accessPolicy` in the request body with `private` or `public` as the value. 

3. You receive a response containing the newly created playback ID with the specified access level.

#### Example
A video streaming service generates playback IDs for each media file when users request to view specific content. The video player then uses the playback ID to stream the video.

### Example Usage

<!-- UsageSnippet language="python" operationID="create-media-playback-id" method="post" path="/on-demand/{mediaId}/playback-ids" -->
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

    res = fastpix.playback.create(media_id="your-media-id", access_policy="public", drm_configuration_id="your-drm-configuration-id", resolution="1080p")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                           | Type                                                                                                                | Required                                                                                                            | Description                                                                                                         | Example                                                                                                             |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                          | *str*                                                                                                               | :heavy_check_mark:                                                                                                  | The unique identifier assigned to the media when created. The value must be a valid UUID.                           | your-media-id                                                                                                     |
| `access_policy`                                                                                                     | [models.AccessPolicy](../../models/accesspolicy.md)                                                                 | :heavy_check_mark:                                                                                                  | Access policy for media content                                                                                     |                                                                                                                     |
| `access_restrictions`                                                                                               | [Optional[models.CreateMediaPlaybackIDAccessRestrictions]](../../models/createmediaplaybackidaccessrestrictions.md) | :heavy_minus_sign:                                                                                                  | N/A                                                                                                                 |                                                                                                                     |
| `drm_configuration_id`                                                                                              | *Optional[str]*                                                                                                     | :heavy_minus_sign:                                                                                                  | DRM configuration ID (required if accessPolicy is "drm")                                                            | 123e4567-e89b-12d3-a456-426614174000                                                                                |
| `resolution`                                                                                                        | [Optional[models.CreateMediaPlaybackIDResolution]](../../models/createmediaplaybackidresolution.md)                 | :heavy_minus_sign:                                                                                                  | The maximum resolution for the playback ID.                                                                         | 1080p                                                                                                               |
| `retries`                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                    | :heavy_minus_sign:                                                                                                  | Configuration to override the default retry behavior of the client.                                                 |                                                                                                                     |

### Response

**[models.CreateMediaPlaybackIDResponse](../../models/createmediaplaybackidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## list_playback_ids

Retrieves all playback IDs associated with a given media asset, including each playback ID’s access policy and detailed access restrictions such as allowed or denied domains and user agents.

**How it works:**
1. Send a `GET` request to this endpoint with the target `mediaId`.
2. The response includes an array of playback ID records with their respective access controls.

**Use case:**
Useful for validating and managing playback permissions programmatically, reviewing restriction settings, or powering an access control dashboard.

### Example Usage

<!-- UsageSnippet language="python" operationID="list-playback-ids" method="get" path="/on-demand/{mediaId}/playback-ids" -->
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

    res = fastpix.playback.list_playback_ids(media_id="your-media-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `media_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 | your-media-id                                                       |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.ListPlaybackIdsResponse](../../models/listplaybackidsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## delete

This endpoint deletes a specific playback ID associated with a media asset. Deleting a `playback ID` revokes access to the media content linked to that ID.

#### How it works

1. Make a `DELETE` request to this endpoint, replacing `<mediaId>` with the unique ID of the media asset from which you want to delete the playback ID. 

2. Include the `playbackId` you want to delete in the request body.

#### Example

Your platform offers limited-time access to premium content. When the subscription expires, you can revoke access to the content by deleting the associated playback ID, preventing users from streaming the video further.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media-playback-id" method="delete" path="/on-demand/{mediaId}/playback-ids" -->
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

    res = fastpix.playback.delete(
        media_id="your-media-id",
        playback_id="your-playback-id",
    )

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                             | Type                                                                                                  | Required                                                                                              | Description                                                                                           | Example                                                                                               |
| ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                            | *str*                                                                                                 | :heavy_check_mark:                                                                                    | The unique identifier assigned to the media when created. The value must be a valid UUID.             | your-media-id                                                                                          |
| `playback_id`                                                                                         | *str*                                                                                                 | :heavy_check_mark:                                                                                    | Return the universal unique identifier for playbacks  which can contain a maximum of 255 characters.  | your-playback-id                                                                                       |
| `retries`                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                      | :heavy_minus_sign:                                                                                    | Configuration to override the default retry behavior of the client.                                   |                                                                                                       |

### Response

**[models.DeleteMediaPlaybackIDResponse](../../models/deletemediaplaybackidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_by_id

This endpoint retrieves details about a specific playback ID associated with a media asset. Use it to check the access policy for that specific playback ID, such as whether it is public or private.

**How it works:**
1. Make a GET request to the endpoint, replacing `{mediaId}` with the media ID and `{playbackId}` with the playback ID.
2. This request is useful for auditing or validation before granting playback access in your application.

**Example:**
A media platform might use this endpoint to verify if a playback ID is public or private before embedding the video in a frontend player or allowing access to a restricted group.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-playback-id" method="get" path="/on-demand/{mediaId}/playback-ids/{playbackId}" -->
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

    res = fastpix.playback.get_by_id(media_id="4fa85f64-5717-4562-b3fc-2c963f66afa6", playback_id="4fa85f64-5717-4562-b3fc-2c963f66afa6")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

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

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_domain_restrictions

This endpoint updates domain-level restrictions for a specific playback ID associated with a media asset.
It allows you to restrict playback to specific domains or block known unauthorized domains.

**How it works:**
1. Make a `PATCH` request to this endpoint with your desired domain access configuration.
2. Set a default policy (`allow` or `deny`) and specify domain names in the `allow` or `deny` lists.
3. This is commonly used to restrict video playback to your website or approved client domains.

**Example:**
A streaming service can allow playback only from `example.com` and deny all others by setting: `"defaultPolicy": "deny"` and `"allow": ["example.com"]`.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-domain-restrictions" method="patch" path="/on-demand/{mediaId}/playback-ids/{playbackId}/domains" -->
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

    res = fastpix.playback.update_domain_restrictions(media_id="your-media-id", playback_id="your-secret-key", default_policy="allow", allow=[
        "yourdomain.com",
        "sampledomain.com",
    ], deny=[
        "yourworkdomain.com",
    ])
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                       | Type                                                                                                            | Required                                                                                                        | Description                                                                                                     | Example                                                                                                         |
| --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                      | *str*                                                                                                           | :heavy_check_mark:                                                                                              | N/A                                                                                                             | 5ebfa8f7-3ff1-4a35-8b1a-d3a16e22184c                                                                            |
| `playback_id`                                                                                                   | *str*                                                                                                           | :heavy_check_mark:                                                                                              | N/A                                                                                                             | 0199deff-9aef-457e-9461-7a28afdf8773                                                                            |
| `default_policy`                                                                                                | [Optional[models.UpdateDomainRestrictionsDefaultPolicy]](../../models/updatedomainrestrictionsdefaultpolicy.md) | :heavy_minus_sign:                                                                                              | Specify the fallback behavior for domains that are not listed in the `allow` or `deny` lists.                   | allow                                                                                                           |
| `allow`                                                                                                         | List[*str*]                                                                                                     | :heavy_minus_sign:                                                                                              | List of domains explicitly allowed to play the media.                                                           | [<br/>"yourdomain.com",<br/>"sampledomain.com"<br/>]                                                            |
| `deny`                                                                                                          | List[*str*]                                                                                                     | :heavy_minus_sign:                                                                                              | List of domains explicitly denied from accessing the media.                                                     | [<br/>"yourworkdomain.com"<br/>]                                                                                |
| `retries`                                                                                                       | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                | :heavy_minus_sign:                                                                                              | Configuration to override the default retry behavior of the client.                                             |                                                                                                                 |

### Response

**[models.UpdateDomainRestrictionsResponse](../../models/updatedomainrestrictionsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_user_agent_restrictions

This endpoint allows updating user-agent restrictions for a specific playback ID associated with a media asset. 
It can be used to allow or deny specific user-agents during playback request evaluation.

**How it works:**
1. Make a `PATCH` request to this endpoint with your desired user-agent access configuration.
2. Specify a default policy (`allow` or `deny`) and provide specific `allow` or `deny` lists.
3. Use this to restrict access to specific browsers, devices, or bots.

**Example:**
A developer may configure a playback ID to deny access from known scraping user-agents while allowing all others by default.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-user-agent-restrictions" method="patch" path="/on-demand/{mediaId}/playback-ids/{playbackId}/user-agents" -->
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

    res = fastpix.playback.update_user_agent_restrictions(media_id="your-media-id", playback_id="your-playback-id", default_policy="allow", allow=[
        "Mozilla/55.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    ], deny=[
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/53745.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    ])
    
    # Handle response (convert datetimes to JSON-serializable strings)
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                   | Type                                                                                                                                        | Required                                                                                                                                    | Description                                                                                                                                 | Example                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `media_id`                                                                                                                                  | *str*                                                                                                                                       | :heavy_check_mark:                                                                                                                          | N/A                                                                                                                                         | 5ebfa8f7-3ff1-4a35-8b1a-d3a16e22184c                                                                                                        |
| `playback_id`                                                                                                                               | *str*                                                                                                                                       | :heavy_check_mark:                                                                                                                          | N/A                                                                                                                                         | 0199deff-9aef-457e-9461-7a28afdf8773                                                                                                        |
| `default_policy`                                                                                                                            | [Optional[models.UpdateUserAgentRestrictionsDefaultPolicy]](../../models/updateuseragentrestrictionsdefaultpolicy.md)                       | :heavy_minus_sign:                                                                                                                          | The default behavior when a user-agent is not listed in `allow` or `deny`.                                                                  | allow                                                                                                                                       |
| `allow`                                                                                                                                     | List[*str*]                                                                                                                                 | :heavy_minus_sign:                                                                                                                          | List of user-agent substrings explicitly allowed.                                                                                           | [<br/>"Mozilla/55.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"<br/>]        |
| `deny`                                                                                                                                      | List[*str*]                                                                                                                                 | :heavy_minus_sign:                                                                                                                          | List of user-agent substrings explicitly denied.                                                                                            | [<br/>"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/53745.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"<br/>] |
| `retries`                                                                                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                            | :heavy_minus_sign:                                                                                                                          | Configuration to override the default retry behavior of the client.                                                                         |                                                                                                                                             |

### Response

**[models.UpdateUserAgentRestrictionsResponse](../../models/updateuseragentrestrictionsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |