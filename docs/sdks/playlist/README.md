# Playlist

## Overview

Operations for playlist management

### Available Operations

* [create](#create) - Create a new playlist
* [get](#get) - Get a playlist by ID
* [delete](#delete) - Delete a playlist by ID
* [add_media](#add_media) - Add media to a playlist by ID
* [delete_media](#delete_media) - Delete media in a playlist by ID

## create

This endpoint creates a new playlist within a specified workspace. A playlist acts as a container for organizing media items either manually or based on filters and metadata. <br> <br>
### Playlists can be created in two modes
- **Manual:** Creates an empty playlist without any initial media items. Use this mode for manual curation, where you add items later in a user-defined sequence.
- **Smart:** Auto-populates the playlist at creation time based on the filter criteria (for example, a video creation date range) that you provide in the request.

For more details, see <a href="https://docs.fastpix.io/docs/create-and-manage-playlist">Create and manage playlist</a>.

#### How it works 

 - When you send a `POST` request to this endpoint, FastPix creates a playlist and returns a playlist ID, using which items can be added later in a user-defined sequence.
 - You can create a smart playlist that is auto-populated based on the metadata in the request body.


#### Example
An e-learning platform creates a new playlist titled Beginner Python Series through the API. The response returns a unique playlist ID. The platform uses this ID to add a series of video tutorials to the playlist in a defined order. The playlist appears on the frontend as a structured learning path for learners.

### Example Usage

<!-- UsageSnippet language="python" operationID="create-a-playlist" method="post" path="/on-demand/playlists" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlist.create(
        request=models.CreatePlaylistRequestSmart(
            name="playlist name",
            reference_id="a1",
            description="This is a playlist",
            play_order="createdDate DESC",
            limit=20,
            metadata=models.Metadata(
                created_date=models.DateRange(
                    start_date="2024-11-11",
                    end_date="2024-12-12",
                ),
                updated_date=models.DateRange(
                    start_date="2024-11-11",
                    end_date="2024-12-12",
                ),
            ),
        )
    )

    
    print(json.dumps(to_api_payload(res), indent=2))


```

### Parameters

| Parameter                                                             | Type                                                                  | Required                                                              | Description                                                           |
| --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `request`                                                             | [models.CreatePlaylistRequest](../../models/createplaylistrequest.md) | :heavy_check_mark:                                                    | The request object to use for the request.                            |
| `retries`                                                             | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)      | :heavy_minus_sign:                                                    | Configuration to override the default retry behavior of the client.   |

### Response

**[models.CreateAPlaylistResponse](../../models/createaplaylistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get

This endpoint retrieves detailed information about a specific playlist using its unique `playlistId`. It provides comprehensive metadata about the playlist, including its title, creation mode (manual or smart), media items along with the metadata of each media in the playlist.


#### Example
An e-learning platform requests details for the playlist "Beginner Python Series" by providing its unique `playlistId`. The response includes the playlist"s title, creation mode, and the ordered list of video tutorials contained within, enabling the platform to present the full learning path to users.

### Example Usage

<!-- UsageSnippet language="python" operationID="get-playlist-by-id" method="get" path="/on-demand/playlists/{playlistId}" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlist.get(playlist_id="<id>")

    
    print(json.dumps(to_api_payload(res), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `playlist_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The unique id of the playlist you want to retrieve.                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetPlaylistByIDResponse](../../models/getplaylistbyidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## delete

This endpoint allows you to delete an existing playlist from the workspace. After deleted, the playlist and its metadata are permanently removed and cannot be recovered.
#### How it works
 - When a user sends a DELETE request to this endpoint with the `playlistId`, FastPix removes the specified playlist from the workspace and returns a confirmation of successful deletion.

#### Example
An e-learning platform deletes an outdated playlist titled "Old Python Tutorials" by providing its unique playlist ID. The platform receives confirmation that the playlist has been removed, ensuring learners no longer see the obsolete content.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-a-playlist" method="delete" path="/on-demand/playlists/{playlistId}" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlist.delete(playlist_id="<id>")

    
    print(json.dumps(to_api_payload(res), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `playlist_id`                                                       | *str*                                                               | :heavy_check_mark:                                                  | The unique id of the playlist you want to delete.                   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DeleteAPlaylistResponse](../../models/deleteaplaylistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## add_media

This endpoint allows you to add one or more media items to an existing playlist. By passing the media ID(s) in the request, the specified media items are appended to the playlist in the order provided.
#### How it works

 - When a user sends a PATCH request to this endpoint with the `playlistId` as path parameter and a list of media ID(s) in the request body, FastPix adds the specified media items to the playlist and returns the updated playlist details.

#### Example
An e-learning platform adds new video tutorials to the "Beginner Python Series" playlist by sending their media IDs in the request. The playlist is updated with the new content, ensuring learners have access to the latest tutorials in sequence.

### Example Usage

<!-- UsageSnippet language="python" operationID="add-media-to-playlist" method="patch" path="/on-demand/playlists/{playlistId}/media" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlist.add_media(
        playlist_id="your-playlist-id",
        media_ids=["your-media-id"],
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

**[models.AddMediaToPlaylistResponse](../../models/addmediatoplaylistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## delete_media

This endpoint allows you to delete one or more media items from an existing playlist. By passing the media ID(s) in the request, the specified media items are removed from the playlist.
#### How it works

 - When a user sends a DELETE request to this endpoint with the playlist ID as the path parameter and the media ID(s) to be removed in the request body, FastPix deletes the specified media items from the playlist and returns the updated playlist details.

#### Example
An e-learning platform removes outdated video tutorials from the "Beginner Python Series" playlist by specifying their media IDs in the request. The playlist is updated to exclude these items, ensuring learners only access relevant content.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete-media-from-playlist" method="delete" path="/on-demand/playlists/{playlistId}/media" -->
```python
import os
import sys
import json

# Add the src directory to the Python path so we can import fastpix_python
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastpix_python import Fastpix, models
from response_utils import to_api_payload


with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    res = fastpix.playlist.delete_media(
        playlist_id="<id>",
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

**[models.DeleteMediaFromPlaylistResponse](../../models/deletemediafromplaylistresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |