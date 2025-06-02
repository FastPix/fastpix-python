# Introduction:

The FastPix Python SDK simplifies integration with the FastPix platform. This SDK is designed for secure and efficient communication with the FastPix API, enabling easy management of media uploads, live streaming, and simulcasting. It is intended for use with Python 3.7 or later.

## Key Features:

- ### Media API:

  - **Upload Media**: Upload media files seamlessly from URLs or devices.
  - **Manage Media**: Perform operations such as listing, fetching, updating, and deleting media assets.
  - **Playback IDs**: Generate and manage playback IDs for media access.

- ### Live API:

  - **Create & Manage Live Streams:**: Create, list, update, and delete live streams effortlessly.
  - **Control Stream Access**: Generate playback IDs for live streams to control and manage access.
  - **Simulcast to Multiple Platforms**: Stream content to multiple platforms simultaneously.

For detailed usage, refer to the [FastPix API Reference](https://docs.fastpix.io/reference).

## Latest Release
  - Current Version: 0.1.5
   - View our [changelog](CHANELOG.md) for details on recent updates
   - Download the latest release from our [releases page](https://github.com/FastPix/python-server-sdk/releases/tag/v1.0.0)

## Prerequisites:

### Getting started with FastPix:

To get started with the **FastPix Python SDK**, ensure you have the following:

- The FastPix APIs are authenticated using an **Access Token** and a **Secret Key**. You must generate these credentials to use the SDK.

- Follow the steps in the [Authentication with Access Tokens](https://docs.fastpix.io/docs/authentication-with-access-tokens) guide to obtain your credentials.

## Installation:

To install the SDK, use pip with the GitHub repository URL to easily download and install the required libraries.

```bash
pip install git+https://github.com/FastPix/fastpix_python
```
(you may need to run `pip` with root permission)

## Basic Usage:

### Importing the SDK

```python
from fastpix.client import Client
```

### Initialization:

Initialize the FastPix SDK with your API credentials.

```python
from fastpix.client import Client

client = Client(username="your-access-token-id", password="your-secret-key")
```

### Example Usage:

Below is an example of configuring `FastPix Python SDK` into your project.

`Note:-` For Async SDK Users: When using the AsyncClient, all SDK methods must be prefixed with the await keyword.
```python
# Sync Usage
from fastpix.client import Client

client = Client(username="your-access-token-id", password="your-secret-key")

# Define the parameters for fetching media assets in a separate variable.
media_request_params = {
    "limit": 10,  # Number of media assets to fetch in one request.
    "offset": 1,  # Starting position for the list of media assets (useful for pagination).
    "orderBy": "desc"  # Sort order for the media assets ("desc" for descending, "asc" for ascending).
}

try:
   media = client.media.get_all_media(params=media_request_params)
   print("Media:", media)
except Exception as e:
   print(f"Error fetching media: {str(e)}")

# Async Usage 
from fastpix import AsyncClient as Client
import asyncio
 
async def main():
    # Initialize the AsyncClient with username and password.
    client = Client(username="your-access-token-id", password="your-secret-key")
 
    # Define the parameters for fetching media assets in a separate variable.
    media_request_params = {
        "limit": 10,  # Number of media assets to fetch in one request.
        "offset": 1,  # Starting position for the list of media assets (useful for pagination).
        "orderBy": "desc"  # Sort order for the media assets ("desc" for descending, "asc" for ascending).
    }
 
    try:
        # Fetch media assets asynchronously using the await keyword.
        media = await client.media.get_all_media(params=media_request_params)
        print("Media:", media)
    except Exception as e:
        print(f"Error fetching media: {str(e)}")
 
# Run the async function
asyncio.run(main())
```

## Usage:

### 1. Media Operations:

#### 1.1. Media Uploads:

##### Upload Media from a URL:

Use the `client.media.create_pull_video()` method to upload media directly from a URL. For detailed configuration options, refer to the [Create media from URL](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/UploadMedia.md#method-clientmediacreate_pull_video) API documentation.

```python
# Define the request payload for uploading media from a URL.
media_from_url_request = {
"inputs": [{
  "type": "video", # Specifies the type of media being uploaded (e.g., "video").
  "url": "https://static.fastpix.io/sample.mp4" # URL of the media file to be uploaded.
 }],
"metadata": {
  "video_title": "Big_Buck_Bunny" # Metadata to associate with the media, such as its title.
},
"accessPolicy": "public", # Access policy for the media ("public" or "private").
"maxResolution": "1080p"
}

media_response = client.media.create_pull_video(media_from_url_request)
print("media_response", media_response)
```

##### Upload Media from a Local Device:

Use the `client.media.get_presigned_url()` method to obtain a `signedUrl` and upload media directly from a local device. For more details on configuration options, refer to the [Upload media from device](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/UploadMedia.md#method-clientmediaget_presigned_url) API documentation.

```python
# Define the request payload for uploading media from a device.
media_from_device_request = {
  "corsOrigin": "*", # Specifies the allowed origin for CORS (Cross-Origin Resource Sharing). "*" allows all origins.
  "pushMediaSettings": {
    "accessPolicy": "private", # Sets the access policy for the uploaded media (e.g., "private" or "public").
    "optimizeAudio": True, # Enables audio optimization for the uploaded media.
    "maxResolution": "1080p" # Specifies the maximum resolution allowed for the uploaded media.
  },
}

media_from_device_response = client.media.get_presigned_url(media_from_device_request)
print("Upload Response:", media_from_device_response)
```

#### 1.2. Media Management:

##### Get List of All Media:

Use the `client.media.get_all_media()` method to fetch a list of all media assets. You can customize the query by modifying parameters such as `limit`, `offset`, and `orderBy`. Refer to the [Get list of all media](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMedia.md#method-clientmediaget_all_media) API documentation for the accepted values.

```python
# Define the parameters for fetching media assets in a separate variable.
media_request_params = {
    "limit": 10,  # Number of media assets to fetch in one request.
    "offset": 1,  # Starting position for the list of media assets (useful for pagination).
    "orderBy": "desc"  # Sort order for the media assets ("desc" for descending, "asc" for ascending).
}

# Assuming `client` is already initialized with the proper credentials
all_media_assets = client.media.get_all_media(media_request_params)

# Print the fetched media assets
print("All Media Assets:", all_media_assets)
```

##### Get Media Asset by ID:

Use the `client.media.get_by_mediaId()` method to retrieve a specific media asset by its ID. Provide `media_id`of the asset to fetch its details. Refer to the [Get a media by ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMedia.md#method-clientmediaget_by_mediaid) API documentation for more details.

```python
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

get_media_asset = client.media.get_by_mediaId(media_id)

# Print the retrieved media asset by ID
print("Retrieved media asset by ID:", get_media_asset)
```

##### Update Media Asset:

Use the `client.media.update()` method to update metadata or other properties of a specific media asset. Provide the `media_id` of the asset along with the metadata to be updated. Refer to the [Update a media by ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMedia.md#method-clientmediaupdate) API documentation for more details.

```python
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

# Define the payload with the updates to be applied to the media asset.
update_payload = {
    "metadata": {
        "key": "value"  # Replace "key" and "value" with actual metadata keys and values
    },
}

update_media_asset = client.media.update(media_id, update_payload)

# Print the updated media asset details
print("Updated Media Asset:", update_media_asset)
```

##### Delete Media Asset:

Use the `client.media.delete()` method to delete a specific media asset by its ID. Pass the `media_id` of the asset you want to delete. Refer to the [Delete a media by ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMedia.md#method-clientmediadelete) API documentation for more information.

```python
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

# Assuming `client` is already initialized with the necessary credentials
delete_media_asset = client.media.delete(media_id)

# Print the response indicating the media asset has been deleted
print("Deleted Media Asset:", delete_media_asset)
```

##### Get Media Asset Info:

Use the `client.media.get_media_info()` method to retrieve detailed information about a specific media asset. Pass the `media_id` to fetch its details. Refer to the [Get info of media inputs](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMedia.md#method-clientmediaget_media_info) API documentation for more details.

```python
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

get_media_info =  client.media.get_media_info(media_id)
print("Media Asset Info:", get_media_info)
```

#### 1.3. Manage Media Playback:

##### Generate Media Playback ID:

Use the `client.media_playback_ids.create()` method to generate a playback ID for a specific media asset. You can pass an `media_id` and configure options such as the `accessPolicy`. For detailed configuration options, refer to the [Create a playback ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMediaPlayback.md#method-clientmedia_playback_idscreate) API documentation.

```python
# Define the media_id and accessPolicy dynamically
media_type = "video_on_demand"
media_id =  "media-id" # Unique identifier for the media asset.

playback_options = {
  "accessPolicy": "public", # Can be 'public' or 'private'.
}

playback_id_response = client.playback_ids.create(media_type, media_id, playback_options)

print("Playback ID Creation Response:", playback_id_response)
```

##### Delete Media Playback ID:

Use the `client.media_playback_ids.delete()` method to delete a playback ID for a specific media asset. You need to pass both the `media_id` and the `playback_id` to delete the playback ID. For detailed configuration options, refer to the [Delete a playback ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/VideoOnDemand/ManageMediaPlayback.md#method-clientmedia_playback_idsdelete) API documentation.

```python
# Define the media_id and playback_id dynamically
media_type = "video_on_demand"
media_id = "media-id"; # The ID of the media asset for which you want to delete the playback ID.
playback_ids = ["id1", "id2"]; # The playback ID that you want to delete.

delete_playback_response = client.playback_ids.delete(media_type, media_id, playback_ids)

print("Playback ID Deletion Response:", delete_playback_response)
```

----

### 2. Live Stream Operations:

#### 2.1. Start Live Stream:

Use the `client.livestreams.create()` method to start a live stream with specific configurations. For detailed configuration options, refer to the [Create a new stream](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/CreateLiveStream.md#method-clientlivestreamscreate) API documentation.

```python
livestream_request = {
  "playbackSettings": {
    "accessPolicy": "public", # Defines the access level of the live stream (public or private)
  },
  "inputMediaSettings": {
    "maxResolution": "1080p", # Set the maximum resolution of the live stream
    "reconnectWindow": 1800, # Set the duration for reconnecting the stream in seconds
    "mediaPolicy": "private", # Define media policy (private or public)
    "metadata": {
      "liveStream": "fp_livestream", # Custom metadata for the live stream
    },
    "enableDvrMode": True, # Enable DVR mode to allow viewers to rewind the live stream
  },
}

# Initiating the live stream
generate_livestream = client.livestreams.create(livestream_request)
print("Live Stream initiated successfully:", generate_livestream)
```

#### 2.2. Live Stream Management:

##### Get List of All Live Streams:

Use the `client.livestreams.list()` method to fetch a list of all live streams. You can customize the query by modifying parameters such as `limit`, `offset`, and `orderBy`. For detailed configuration options, refer to the [Get all live streams](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageLiveStreams.md#method-clientlivestreamslist) API documentation.

```python
get_all_livestream_pagination = {
  "limit": 10, # Limit the number of live streams retrieved.
  "offset": 1, # Skip a specified number of streams for pagination.
  "orderBy": "asc", # Order the results based on the specified criteria ("asc" or "desc").
}

get_all_livestreams = client.livestreams.list(get_all_livestream_pagination)
print("All Live Streams:", get_all_livestreams)
```

##### Get Live Stream by ID:

Use the `client.livestreams.get()` method to retrieve a specific live stream by its ID. Provide the `stream_id` of the stream you wish to fetch. For more details, refer to the [Get stream by ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageLiveStreams.md#method-clientlivestreamsget) API documentation.

```python
stream_id =  "a09f3e958c16ed00e85bfe798abd9845" # Replace with actual stream ID
get_livestream_by_id = client.livestreams.get(stream_id)

print("Live Stream Details:", get_livestream_by_id)
```

##### Update Live Stream:

Use the `client.livestreams.update()` method to update a live stream's configuration. Provide the `stream_id` of the stream and specify the fields you want to update. For more details, refer to the [Update a stream](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageLiveStreams.md#method-clientlivestreamsupdate) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845" # Provide the stream ID for the live stream to update
update_livestream_request = {
  "metadata": {
    "livestream_name": "Game_streaming",
  },
  "reconnectWindow": 100,
}

update_livestream = client.livestreams.update(stream_id,update_livestream_request)

print("Updated Live Stream:", update_livestream)
```

##### Delete Live Stream:

Use the `client.livestreams.delete()` method to delete a live stream by its ID. Provide `stream_id` of the stream you want to delete. For more details, refer to the [Delete a stream](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageLiveStreams.md#method-clientlivestreamsdelete) API documentation.

```python
delete_livestream = client.livestreams.delete("a09f3e958c16ed00e85bfe798abd9845")  # Provide the stream ID of the live stream to delete
print("Deleted Live Stream:", delete_livestream)
```

#### 2.3. Manage Live Stream Playback:

##### Generate Live Stream Playback ID:

Use the `client.livestream_playback_ids.create()` method to generate a playback ID for a live stream. Replace `stream_id` with the actual ID of the live stream and specify the desired `accessPolicy`. For more details, refer to the [Create a playback ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamPlayback.md#method-clientlivestream_playback_idscreate) API documentation.

```python
media_type = "livestream"
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
body = { "accessPolicy": "public" }

generate_livestream_playback_id = client.playback_ids.create(media_type, stream_id, body)

print("Generated Live Stream Playback ID:", generate_livestream_playback_id)
```

##### Delete Live Stream Playback ID:

Use the `client.livestream_playback_ids.delete()` method to delete a specific playback ID for a live stream. You need to provide both the `stream_id` of the live stream and the `playback_id` to delete. For more details, refer to the [Delete a playback ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamPlayback.md#method-clientlivestream_playback_idsdelete) API documentation.

```python
media_type = "livestream"
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
playback_id = "632029b4-7c53-4dcf-a4d3-1884c29e90f8"  # Replace with actual playback ID

delete_livestream_playback_id = client.playback_ids.delete(media_type, stream_id, playback_id)

print("Deleted Live Stream Playback ID:", delete_livestream_playback_id)
```

##### Get Live Stream Playback Policy:

Use the `client.livestream_playback_ids.get()` method to retrieve the playback policy for a specific live stream playback ID. Replace `stream_id` with the stream's ID and `playback_id` with the actual playback ID to fetch the policy. For more details, refer to the [Get stream's playback ID](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamPlayback.md#method-clientlivestream_playback_idsget) API documentation.

```python
media_type = "livestream"
stream_id = "1c5e8abcc2080cba74f5d0ac91c7833e"  # Replace with the actual stream ID
playback_id = "95ce872d-0b58-44f3-be72-8ed8b97ee2c9"  # Replace with the actual playback ID

get_livestream_playback_policy = client.playback_ids.get(media_type, stream_id, playback_id)

print("Live Stream Playback Policy:", get_livestream_playback_policy )
```

#### 2.4. Manage Live Stream Simulcast:

##### Initiate Live Stream Simulcast:

Use the `client.livestreams.create_simulcast()` method to create a new simulcast for a live stream. Provide the stream ID and simulcast payload with the URL and stream key. For more details, refer to the [Create a simulcast](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamSimulcast.md#method-clientlivestreamscreate_simulcast) API documentation.

```python
simulcast_payload = {
    "url": "rtmps://live.fastpix.io:443/live",
    "streamKey": "46c3457fa8a579b2d4da64125a2b6e83ka09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream key
}

stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID

generate_simulcast = client.livestreams.create_simulcast(stream_id, simulcast_payload)

print("Generate Simulcast:", generate_simulcast)
```

##### Get Live Stream Simulcast:

Use the `client.livestreams.get_simulcast()` method to retrieve details of a specific simulcast stream. Provide the `stream_id` and `simulcast_id` of the simulcast you want to fetch. For more details, refer to the [Get a specific simulcast of a stream](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamSimulcast.md#method-clientlivestreamsget_simulcast) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
simulcast_id = "7269209ff0299319b6321c9a6e7850ff"  # Replace with actual simulcast ID

get_livestream_simulcast = client.livestreams.get_simulcast(stream_id, simulcast_id)

print("Live Stream Simulcast Details:", get_livestream_simulcast )
```

##### Update Live Stream Simulcast:

Use the `client.livestreams.update_simulcast()` method to update the configuration of a simulcast stream. Provide the `stream_id`, `simulcast_id`, and the fields you want to update. For more details, refer to the [Update a specific simulcast of a stream](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamSimulcast.md#method-clientlivestreamsupdate_simulcast) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
simulcast_id = "7269209ff0299319b6321c9a6e7850ff"  # Replace with actual simulcast ID

update_payload = {
    "isEnabled": False,  # Disable the simulcast stream (set to True to enable)
    "metadata": {
        "simulcast2": "media"  # Update the metadata as needed
    }
}

update_live_simulcast = client.livestreams.update_simulcast(stream_id, simulcast_id, update_payload)

print("Updated Live Stream Simulcast:", update_live_simulcast)
```

##### Delete Live Stream Simulcast:

Use the `client.livestreams.delete_simulcast()` method to remove a specific simulcast from a live stream. Provide the `stream_id` and `simulcast_id` for the simulcast you want to delete. For more details, refer to the [Delete a simulcast](https://github.com/FastPix/python-server-sdk/blob/main/fastpix/docs/Live/ManageStreamSimulcast.md#method-deletelivestreamsimulcast) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
simulcast_id = "7269209ff0299319b6321c9a6e7850ff"  # Replace with actual simulcast ID

delete_live_simulcast = client.livestreams.delete_simulcast(stream_id, simulcast_id)

print("Deleted Live Stream Simulcast:", delete_live_simulcast)
```

### Detailed Usage:

For a complete understanding of each API's functionality, including request and response details, parameter descriptions, and additional examples, please refer to the [FastPix API Reference](https://docs.fastpix.io/reference/signingkeys-overview).

The API reference provides comprehensive documentation for all available endpoints and features, ensuring developers can integrate and utilize FastPix APIs efficiently.
