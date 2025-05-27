# Method: client.livestreams.create()

The `client.livestreams.create()` method allows you to start a live stream with specific configurations. You can define settings for playback, input media, and metadata. This method returns the details of the initiated stream, including the unique `stream_id` and `stream_key` that you can use for managing further live stream operations.

### Parameter Details:


| **Parameter**        | **Description**                                                           | **Type** | **Accepted Values** |
| -------------------- | ------------------------------------------------------------------------- | -------- | ------------------- |
| `playbackSettings`   | Defines settings related to playback, such as access policy.              | `Object` | See details below   |
| `inputMediaSettings` | Defines settings related to the media being streamed, such as resolution. | `Object` | See details below   |

#### playbackSettings

| **Parameter**  | **Description**                                                                   | **Type** | **Accepted Values**     |
| -------------- | --------------------------------------------------------------------------------- | -------- | ----------------------- |
| `accessPolicy` | Determines if access to the streamed content is kept private or available to all. | `String` | `"public"`, `"private"` |

#### inputMediaSettings

| **Parameter**     | **Description**                                                                                | **Type**  | **Accepted Values**                                             |
| ----------------- | ---------------------------------------------------------------------------------------------- | --------- | --------------------------------------------------------------- |
| `maxResolution`   | Sets the maximum resolution for the live stream.                                               | `String`  | `"1080p"`, `"720p"`, `"480p"`                                   |
| `reconnectWindow` | The time in seconds to wait before reconnecting the stream if it's interrupted.                | `Integer` | 60 to 1800 seconds                                              |
| `mediaPolicy`     | Determines whether the recorded stream is private or public when converted to VOD.             | `String`  | `"public"`, `"private"`                                         |
| `metadata`        | Optional metadata for tagging the live stream. Up to 10 key-value pairs.                       | `Object`  | Any valid key-value pair (max 255 characters per key and value) |
| `enableDvrMode`   | Enables or disables DVR mode for the live stream. When enabled, viewers can rewind the stream. | `Boolean` | `True`, `False`                                                 |

### Example Request:

```python
# Note for Async SDK Users: When using the AsyncClient, all API methods must be prefixed with the await keyword. 
# For example: await client.livestreams.create(livestream_request)

# Define the live stream request with custom configurations
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
