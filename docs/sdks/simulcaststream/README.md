# SimulcastStream
(*simulcast_stream*)

## Overview

### Available Operations

* [create_simulcast_of_stream](#create_simulcast_of_stream) - Create a simulcast
* [delete_simulcast_of_stream](#delete_simulcast_of_stream) - Delete a simulcast
* [get_specific_simulcast_of_stream](#get_specific_simulcast_of_stream) - Get a specific simulcast
* [update_specific_simulcast_of_stream](#update_specific_simulcast_of_stream) - Update a simulcast

## create_simulcast_of_stream

Lets you to create a simulcast for a parent live stream. Simulcasting enables you to broadcast the live stream to multiple social platforms simultaneously (e.g., YouTube, Facebook, or Twitch). This feature is useful for expanding your audience reach across different platforms. However, a simulcast can only be created when the parent live stream is in idle state (i.e., not currently live or disabled). Additionally, only one simulcast target can be created per API call. 
#### How it works

1. Upon calling this endpoint, you need to provide the parent `streamId` and the details of the simulcast target (platform and credentials). The system will generate a unique `simulcastId`, which can be used to manage the simulcast later. 

2. To notify your application about the status of simulcast related events check for the <a href="https://docs.fastpix.io/docs/webhooks-collection#simulcast-target-events">webhooks for simulcast</a> target events. 

#### Example
An event manager sets up a live stream for a virtual conference and wants to simulcast the stream on YouTube and Facebook Live. They first create the primary live stream in FastPix, ensuring it's in the idle state. Then, they use the API to create a simulcast target for YouTube. 

Related guide: <a href="https://docs.fastpix.io/docs/simulcast-to-3rd-party-platforms">Simulcast to 3rd party platforms</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="create-simulcast-of-stream" method="post" path="/live/streams/{streamId}/simulcast" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.simulcast_stream.create_simulcast_of_stream(stream_id="8717422d89288ad5958d4a86e9afe2a2", url="rtmp://hyd01.contribute.live-video.net/app/", stream_key="live_1012464221_DuM8W004MoZYNxQEZ0czODgfHCFBhk", metadata={
        "livestream_name": "Tech-Connect Summit",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                             | Type                                                                                                                                                                                                                                                                  | Required                                                                                                                                                                                                                                                              | Description                                                                                                                                                                                                                                                           | Example                                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stream_id`                                                                                                                                                                                                                                                           | *str*                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                    | Upon creating a new live stream, FastPix assigns a unique identifier to the stream.                                                                                                                                                                                   | 8717422d89288ad5958d4a86e9afe2a2                                                                                                                                                                                                                                      |
| `url`                                                                                                                                                                                                                                                                 | *Optional[str]*                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                    | The RTMPS hostname, combined with the application name, is crucial for connecting to third-party live streaming services and transmitting the live stream.                                                                                                            | rtmp://hyd01.contribute.live-video.net/app/                                                                                                                                                                                                                           |
| `stream_key`                                                                                                                                                                                                                                                          | *Optional[str]*                                                                                                                                                                                                                                                       | :heavy_minus_sign:                                                                                                                                                                                                                                                    | A unique stream key is generated for streaming, allowing the user to start streaming on any third-party platform using this key.                                                                                                                                      | 9310547d1df9c219d851d91d5b768b36k61a264dcc447b63da6fb79ef925cd76d                                                                                                                                                                                                     |
| `metadata`                                                                                                                                                                                                                                                            | Dict[str, *str*]                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                    | You can search for videos with specific key value pairs using metadata, when you tag a video in "key":"value"s pairs. Dynamic Metadata allows you to define a key that allows any value pair. You can have maximum of 255 characters and upto 10 entries are allowed. | {<br/>"livestream_name": "Tech-Connect Summit"<br/>}                                                                                                                                                                                                                  |
| `retries`                                                                                                                                                                                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                    | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                       |

### Response

**[models.SimulcastResponse](../../models/simulcastresponse.md)**

### Errors

| Error Type                       | Status Code                      | Content Type                     |
| -------------------------------- | -------------------------------- | -------------------------------- |
| errors.SimulcastUnavailableError | 400                              | application/json                 |
| errors.UnauthorizedError         | 401                              | application/json                 |
| errors.InvalidPermissionError    | 403                              | application/json                 |
| errors.LiveNotFoundError         | 404                              | application/json                 |
| errors.ValidationErrorResponse   | 422                              | application/json                 |
| errors.FastpixDefaultError       | 4XX, 5XX                         | \*/\*                            |

## delete_simulcast_of_stream

Allows you to delete a simulcast using its unique `simulcastId`, which was returned during the simulcast creation process. Deleting a simulcast stops the broadcast to the associated platform, but the parent stream will continue to run if it is live. This action is irreversible, and a new simulcast would need to be created if you want to resume streaming to the same platform. 

Webhook event: <a href="https://docs.fastpix.io/docs/live-events#videolive_streamsimulcast_targetdeleted">video.live_stream.simulcast_target.deleted</a>


#### Example
A broadcaster needs to stop simulcasting to one platform due to technical difficulties while keeping the stream active on others. For instance, a tech company is simulcasting a product launch on multiple platforms. Midway through the event, they decide to stop the simulcast on Facebook due to performance issues, but keep it running on YouTube. They call this API to delete the Facebook simulcast target.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-simulcast-of-stream" method="delete" path="/live/streams/{streamId}/simulcast/{simulcastId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.simulcast_stream.delete_simulcast_of_stream(stream_id="8717422d89288ad5958d4a86e9afe2a2", simulcast_id="9217422d89288ad5958d4a86e9afe2a1")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                      | Type                                                                                                                           | Required                                                                                                                       | Description                                                                                                                    | Example                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `stream_id`                                                                                                                    | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | Upon creating a new live stream, FastPix assigns a unique identifier to the stream.                                            | 8717422d89288ad5958d4a86e9afe2a2                                                                                               |
| `simulcast_id`                                                                                                                 | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | When you create the new simulcast, FastPix assign a universal unique identifier which can contain a maximum of 255 characters. | 9217422d89288ad5958d4a86e9afe2a1                                                                                               |
| `retries`                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                               | :heavy_minus_sign:                                                                                                             | Configuration to override the default retry behavior of the client.                                                            |                                                                                                                                |

### Response

**[models.SimulcastdeleteResponse](../../models/simulcastdeleteresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.UnauthorizedError       | 401                            | application/json               |
| errors.InvalidPermissionError  | 403                            | application/json               |
| errors.NotFoundErrorSimulcast  | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## get_specific_simulcast_of_stream

Retrieves the details of a specific simulcast associated with a parent live stream. By providing both the `streamId` of the parent stream and the `simulcastId`, FastPix returns detailed information about the simulcast, such as the stream URL, the status of the simulcast, and metadata. 

#### Example
This endpoint can be used to verify the status of the simulcast on external platforms before the live stream begins. For instance, before starting a live gaming event, the organizer wants to ensure that the simulcast to Twitch is set up correctly. They retrieve the simulcast information to confirm that everything is properly configured.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-specific-simulcast-of-stream" method="get" path="/live/streams/{streamId}/simulcast/{simulcastId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.simulcast_stream.get_specific_simulcast_of_stream(stream_id="8717422d89288ad5958d4a86e9afe2a2", simulcast_id="8717422d89288ad5958d4a86e9afe2a2")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                      | Type                                                                                                                           | Required                                                                                                                       | Description                                                                                                                    | Example                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `stream_id`                                                                                                                    | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | Upon creating a new live stream, FastPix assigns a unique identifier to the stream.                                            | 8717422d89288ad5958d4a86e9afe2a2                                                                                               |
| `simulcast_id`                                                                                                                 | *str*                                                                                                                          | :heavy_check_mark:                                                                                                             | When you create the new simulcast, FastPix assign a universal unique identifier which can contain a maximum of 255 characters. | 8717422d89288ad5958d4a86e9afe2a2                                                                                               |
| `retries`                                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                               | :heavy_minus_sign:                                                                                                             | Configuration to override the default retry behavior of the client.                                                            |                                                                                                                                |

### Response

**[models.SimulcastResponse](../../models/simulcastresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.UnauthorizedError       | 401                            | application/json               |
| errors.InvalidPermissionError  | 403                            | application/json               |
| errors.NotFoundErrorSimulcast  | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |

## update_specific_simulcast_of_stream

Allows you to enable or disable a specific simulcast associated with a parent live stream. The status of the simulcast can be updated at any point, whether the live stream is active or idle. However, once the live stream is disabled, the simulcast can no longer be modified. 

Webhook event: <a href="https://docs.fastpix.io/docs/live-events#videolive_streamsimulcast_targetupdated">video.live_stream.simulcast_target.updated</a>

#### Example
When a `PATCH` request is made to this endpoint, the API updates the status of the simulcast. This can be useful for pausing or resuming a simulcast on a particular platform without stopping the parent live stream.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-specific-simulcast-of-stream" method="put" path="/live/streams/{streamId}/simulcast/{simulcastId}" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.simulcast_stream.update_specific_simulcast_of_stream(stream_id="9714422d89287ad5758d4a86e9afe1a2", simulcast_id="8717422d89288ad5958d4a86e9afe2a2", is_enabled=False, metadata={
        "simulcast_name": "Tech today",
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                             | Type                                                                                                                                                                                                                                                                  | Required                                                                                                                                                                                                                                                              | Description                                                                                                                                                                                                                                                           | Example                                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `stream_id`                                                                                                                                                                                                                                                           | *str*                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                    | Upon creating a new live stream, FastPix assigns a unique identifier to the stream.                                                                                                                                                                                   | 9714422d89287ad5758d4a86e9afe1a2                                                                                                                                                                                                                                      |
| `simulcast_id`                                                                                                                                                                                                                                                        | *str*                                                                                                                                                                                                                                                                 | :heavy_check_mark:                                                                                                                                                                                                                                                    | When you create the new simulcast, FastPix assign a universal unique identifier which can contain a maximum of 255 characters.                                                                                                                                        | 8717422d89288ad5958d4a86e9afe2a2                                                                                                                                                                                                                                      |
| `is_enabled`                                                                                                                                                                                                                                                          | *Optional[bool]*                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                    | When the value is set to false, the simulcast will be disabled for the given stream.                                                                                                                                                                                  | false                                                                                                                                                                                                                                                                 |
| `metadata`                                                                                                                                                                                                                                                            | Dict[str, *str*]                                                                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                    | You can search for videos with specific key value pairs using metadata, when you tag a video in "key":"value"s pairs. Dynamic Metadata allows you to define a key that allows any value pair. You can have maximum of 255 characters and upto 10 entries are allowed. |                                                                                                                                                                                                                                                                       |
| `retries`                                                                                                                                                                                                                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                      | :heavy_minus_sign:                                                                                                                                                                                                                                                    | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                       |

### Response

**[models.SimulcastUpdateResponse](../../models/simulcastupdateresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.UnauthorizedError       | 401                            | application/json               |
| errors.InvalidPermissionError  | 403                            | application/json               |
| errors.NotFoundErrorSimulcast  | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |