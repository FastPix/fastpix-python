# Playlists

## Overview

### Available Operations

* [get_all](#get_all) - Get all playlists
* [update](#update) - Update a playlist by ID
* [change_media_order](#change_media_order) - Change media order in a playlist by ID

## get_all

This endpoint retrieves all playlists in a specified workspace. It allows you to view the collection of manual and smart playlists along with their associated metadata.
#### How it works

 - When a user sends a GET request to this endpoint, FastPix returns a list of all playlists in the workspace, including details such as playlist IDs, titles, creation mode (manual or smart), and other relevant metadata.

#### Example

  An e-learning platform requests all playlists within a workspace to display an overview of available learning paths. The response includes multiple playlists like "Beginner Python Series" and "Advanced Java Tutorials," enabling the platform to show users a catalog of curated content collections.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-all-playlists" method="get" path="/on-demand/playlists" -->
```python
import os
import json

from fastpix_python import Fastpix, models
from response_utils import to_api_payload

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlists.get_all(limit=1, offset=1)

    
    print(json.dumps(to_api_payload(res), indent=2))

```

### Parameters

| Parameter                                                                                          | Type                                                                                               | Required                                                                                           | Description                                                                                        | Example                                                                                            |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `limit`                                                                                            | *Optional[int]*                                                                                    | :heavy_minus_sign:                                                                                 | The number of playlists to return (default is 10, max is 50).                                      | 1                                                                                                  |
| `offset`                                                                                           | *Optional[int]*                                                                                    | :heavy_minus_sign:                                                                                 | The page number to retrieve, starting from 1. Use this parameter to paginate the playlist results. | 1                                                                                                  |
| `retries`                                                                                          | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                   | :heavy_minus_sign:                                                                                 | Configuration to override the default retry behavior of the client.                                |                                                                                                    |

### Response

**[models.GetAllPlaylistsResponseResponse](../../models/getallplaylistsresponseresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## update

This endpoint allows you to update the name and description of an existing playlist. It enables modifications to the playlist's metadata without altering the media items or playlist structure.
#### How it works

 - When a user sends a PUT request to this endpoint with the `playlistId` and updated name and description in the request body, FastPix updates the playlist metadata accordingly and returns the updated playlist details.

#### Example
An e-learning platform updates the playlist titled "Beginner Python Series" to rename it as "Python Basics" and add a more detailed description. The updated metadata is reflected when retrieving the playlist, helping users better understand the playlist content.

### Example Usage

<!-- UsageSnippet language="python" operationID="update-a-playlist" method="put" path="/on-demand/playlists/{playlistId}" -->
```python
import os
import json

from fastpix_python import Fastpix, models
from response_utils import to_api_payload

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlists.update(
        playlist_id="your-playlist-id",
        name="updated name",
        description="updated description",
    )

    
    print(json.dumps(to_api_payload(res), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `playlist_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The unique id of the playlist you want to retrieve.                 |                                                                     |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | New name to the playlist.                                           | updated name                                                        |
| `description`                                                       | *str*                                                               | :heavy_check_mark:                                                  | Updated description to the playlist.                                | updated description                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.UpdateAPlaylistResponse](../../models/updateaplaylistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## change_media_order

This endpoint allows you to change the order of media items within a playlist. By passing the complete list of media IDs in the desired sequence, the playlist's play order is updated accordingly.
#### How it works

 - When a user sends a PUT request to this endpoint with the `playlistId` as path parameter and the reordered list of all media IDs in the request body, FastPix updates the playlist to reflect the new media sequence and returns the updated playlist details.

#### Example
An e-learning platform rearranges the "Beginner Python Series" playlist by submitting a reordered list of media IDs. The playlist now follows the new sequence, providing learners with a better structured learning path.

### Example Usage

<!-- UsageSnippet language="python" operationID="change-media-order-in-playlist" method="put" path="/on-demand/playlists/{playlistId}/media" -->
```python
import os
import json

from fastpix_python import Fastpix, models
from response_utils import to_api_payload

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlists.change_media_order(
        playlist_id="your-playlist-id",
        media_ids=[
            "your-media-id-1",
            "your-media-id-2",
            "your-media-id-3",
        ],
    )

    
    print(json.dumps(to_api_payload(res), indent=2))

```

### Parameters

| Parameter                                                                                                                  | Type                                                                                                                       | Required                                                                                                                   | Description                                                                                                                | Example                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `playlist_id`                                                                                                              | *str*                                                                                                                      | :heavy_check_mark:                                                                                                         | The unique id of the playlist you want to perform the operation on.                                                        |                                                                                                                            |
| `media_ids`                                                                                                                | List[*str*]                                                                                                                | :heavy_check_mark:                                                                                                         | N/A                                                                                                                        | [<br/>"a1cd180e-f9b5-4e99-9d44-b9c9baabad89",<br/>"245800c3-7b73-47d9-a201-e961260dcb30",<br/>"41316aac-5396-4278-8f44-08d5f2495b12"<br/>] |
| `retries`                                                                                                                  | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                           | :heavy_minus_sign:                                                                                                         | Configuration to override the default retry behavior of the client.                                                        |                                                                                                                            |

### Response

**[models.ChangeMediaOrderInPlaylistResponse](../../models/changemediaorderinplaylistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |