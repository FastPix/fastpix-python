# LivePlayback

## Overview

### Available Operations

* [create_playback_id_of_stream](#create_playback_id_of_stream) - Create a playbackId
* [delete_playback_id_of_stream](#delete_playback_id_of_stream) - Delete a playbackId
* [get_live_stream_playback_id](#get_live_stream_playback_id) - Get playbackId details
* [update_live_stream_domain_restrictions](#update_live_stream_domain_restrictions) - Update domain restrictions for a playback ID
* [update_live_stream_user_agent_restrictions](#update_live_stream_user_agent_restrictions) - Update user-agent restrictions for a playback ID

## create_playback_id_of_stream

Generates a new playback ID for the live stream, allowing viewers to access the stream through this ID. The playback ID can be shared with viewers for direct access to the live broadcast. 

  By calling this endpoint with the `streamId`, FastPix returns a unique `playbackId`, which can be used to stream the live content. 

  #### Example

  A media platform needs to distribute a unique playback ID to users for an exclusive live concert. The platform can also embed the stream on various partner websites.

### Example Usage

<!-- UsageSnippet language="python" operationID="create-playbackId-of-stream" method="post" path="/live/streams/{streamId}/playback-ids" -->
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

    res = fastpix.live_playback.create_playback_id_of_stream(stream_id="your-stream-id", access_policy="public", access_restrictions={
        "domains": {
            "default_policy": "deny",
            "allow": [
                "example.com",
            ],
        },
        "user_agents": {
            "default_policy": "allow",
        },
    })

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                            | Type                                                                                 | Required                                                                             | Description                                                                          | Example                                                                              |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| `stream_id`                                                                          | *str*                                                                                | :heavy_check_mark:                                                                   | After creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                                       |
| `access_policy`                                                                      | [Optional[models.BasicAccessPolicy]](../../models/basicaccesspolicy.md)              | :heavy_minus_sign:                                                                   | Basic access policy for media content                                                |                                                                                      |
| `access_restrictions`                                                                | [Optional[models.PlaybackIDAccessRestrictions]](../../models/playbackidaccessrestrictions.md) | :heavy_minus_sign:                                                                   | Optional domain and user-agent access restrictions applied to the playback ID.       |                                                                                      |
| `retries`                                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                     | :heavy_minus_sign:                                                                   | Configuration to override the default retry behavior of the client.                  |                                                                                      |

### Response

**[models.CreatePlaybackIDOfStreamResponse](../../models/createplaybackidofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## delete_playback_id_of_stream

Deletes a previously created playback ID for a live stream.This prevents new viewers from accessing the stream using the playback ID, while current viewers can continue watching for a short period before the connection ends. FastPix deletes the ID and ensures the new playback request fails.

#### Example
A streaming service wants to prevent new users from joining a live stream that is nearing its end. The host can delete the playback ID to ensure no one can join the stream or replay it once it ends.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-playbackId-of-stream" method="delete" path="/live/streams/{streamId}/playback-ids" -->
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

    res = fastpix.live_playback.delete_playback_id_of_stream(
        stream_id="your-stream-id",
        playback_id="your-playback-id",
    )

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                           | Type                                                                                | Required                                                                            | Description                                                                         | Example                                                                             |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `stream_id`                                                                         | *str*                                                                               | :heavy_check_mark:                                                                  | Upon creating a new live stream, FastPix assigns a unique identifier to the stream. | your-stream-id                                                                      |
| `playback_id`                                                                       | *str*                                                                               | :heavy_check_mark:                                                                  | Unique identifier for the playbackId                                                | your-playback-id                                                                    |
| `retries`                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                    | :heavy_minus_sign:                                                                  | Configuration to override the default retry behavior of the client.                 |                                                                                     |

### Response

**[models.DeletePlaybackIDOfStreamResponse](../../models/deleteplaybackidofstreamresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_live_stream_playback_id

Retrieves details for an existing playback ID. When you provide the playbackId returned from a previous stream or playback creation request, FastPix returns the associated playback information, including the access policy.

#### Example
A developer needs to confirm the access policy of the playback ID to ensure whether the stream is public or private for viewers.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-live-stream-playback-id" method="get" path="/live/streams/{streamId}/playback-ids/{playbackId}" -->
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

    res = fastpix.live_playback.get_live_stream_playback_id(stream_id="your-stream-id", playback_id="your-playback-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                             | Type                                                                                  | Required                                                                              | Description                                                                           | Example                                                                               |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `stream_id`                                                                           | *str*                                                                                 | :heavy_check_mark:                                                                    | After creating a new live stream, FastPix assigns a unique identifier to the stream.  | your-stream-id                                                      |
| `playback_id`                                                                         | *str*                                                                                 | :heavy_check_mark:                                                                    | After creating a new playbackId, FastPix assigns a unique identifier to the playback. | your-playback-id                                                      |
| `retries`                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                      | :heavy_minus_sign:                                                                    | Configuration to override the default retry behavior of the client.                   |                                                                                       |

### Response

**[models.GetLiveStreamPlaybackIDResponse](../../models/getlivestreamplaybackidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |
## update_live_stream_domain_restrictions

This endpoint updates domain-level restrictions for a specific playback ID associated with a live stream.
It allows you to restrict playback to specific domains or block known unauthorized domains.

**How it works:**
1. Make a `PATCH` request to this endpoint with your desired domain access configuration.
2. Set a default policy (`allow` or `deny`) and specify domain names in the `allow` or `deny` lists.
3. This is commonly used to restrict video playback to your website or approved client domains.

**Example:**
A streaming service can allow playback only from `example.com` and deny all others by setting: `"defaultPolicy": "deny"` and `"allow": ["example.com"]`.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-live-stream-domain-restrictions" method="patch" path="/live/streams/{streamId}/playback-ids/{playbackId}/domains" -->
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

    res = fastpix.live_playback.update_live_stream_domain_restrictions(stream_id="your-stream-id", playback_id="your-playback-id", default_policy="deny", allow=[
        "example.com",
    ], deny=[])

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                                                                           | Type                                                                                                                                | Required                                                                                                                            | Description                                                                                                                         | Example                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `stream_id`                                                                                                                         | *str*                                                                                                                               | :heavy_check_mark:                                                                                                                  | N/A                                                                                                                                 | your-stream-id                                                                                                                      |
| `playback_id`                                                                                                                       | *str*                                                                                                                               | :heavy_check_mark:                                                                                                                  | N/A                                                                                                                                 | your-playback-id                                                                                                                    |
| `default_policy`                                                                                                                    | [Optional[models.UpdateLiveStreamDomainRestrictionsDefaultPolicy]](../../models/updatelivestreamdomainrestrictionsdefaultpolicy.md) | :heavy_minus_sign:                                                                                                                  | Specify the fallback behavior for domains that are not listed in the `allow` or `deny` lists.                                       | deny                                                                                                                                |
| `allow`                                                                                                                             | List[*str*]                                                                                                                         | :heavy_minus_sign:                                                                                                                  | List of domains explicitly allowed to play the stream.                                                                              | [<br/>"example.com"<br/>]                                                                                                           |
| `deny`                                                                                                                              | List[*str*]                                                                                                                         | :heavy_minus_sign:                                                                                                                  | List of domains explicitly denied from accessing the stream.                                                                        | []                                                                                                                                  |
| `retries`                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                    | :heavy_minus_sign:                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                 |                                                                                                                                     |

### Response

**[models.UpdateLiveStreamDomainRestrictionsResponseBody](../../models/updatelivestreamdomainrestrictionsresponsebody.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update_live_stream_user_agent_restrictions

This endpoint allows updating user-agent restrictions for a specific playback ID associated with a live stream. 
It can be used to allow or deny specific user-agents during playback request evaluation.

**How it works:**
1. Make a `PATCH` request to this endpoint with your desired user-agent access configuration.
2. Specify a default policy (`allow` or `deny`) and provide specific `allow` or `deny` lists.
3. Use this to restrict access to specific browsers, devices, or bots.

**Example:**
A developer may configure a playback ID to deny access from known scraping user-agents while allowing all others by default.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-live-stream-user-agent-restrictions" method="patch" path="/live/streams/{streamId}/playback-ids/{playbackId}/user-agents" -->
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

    res = fastpix.live_playback.update_live_stream_user_agent_restrictions(stream_id="your-stream-id", playback_id="your-playback-id", default_policy="allow", allow=[
        "Mozilla/55.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    ], deny=[
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/53745.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    ])

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                   | Type                                                                                                                                        | Required                                                                                                                                    | Description                                                                                                                                 | Example                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `stream_id`                                                                                                                                 | *str*                                                                                                                                       | :heavy_check_mark:                                                                                                                          | N/A                                                                                                                                         | your-stream-id                                                                                                                              |
| `playback_id`                                                                                                                               | *str*                                                                                                                                       | :heavy_check_mark:                                                                                                                          | N/A                                                                                                                                         | your-playback-id                                                                                                                            |
| `default_policy`                                                                                                                            | [Optional[models.UpdateLiveStreamUserAgentRestrictionsDefaultPolicy]](../../models/updatelivestreamuseragentrestrictionsdefaultpolicy.md)   | :heavy_minus_sign:                                                                                                                          | The default behavior when a user-agent is not listed in `allow` or `deny`.                                                                  | allow                                                                                                                                       |
| `allow`                                                                                                                                     | List[*str*]                                                                                                                                 | :heavy_minus_sign:                                                                                                                          | List of user-agent substrings explicitly allowed.                                                                                           | [<br/>"Mozilla/55.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"<br/>]        |
| `deny`                                                                                                                                      | List[*str*]                                                                                                                                 | :heavy_minus_sign:                                                                                                                          | List of user-agent substrings explicitly denied.                                                                                            | [<br/>"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/53745.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"<br/>] |
| `retries`                                                                                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                            | :heavy_minus_sign:                                                                                                                          | Configuration to override the default retry behavior of the client.                                                                         |                                                                                                                                             |

### Response

**[models.UpdateLiveStreamUserAgentRestrictionsResponseBody](../../models/updatelivestreamuseragentrestrictionsresponsebody.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |
