# Method: client.media.create_pull_video()

The `client.media.create_pull_video()` method allows you to upload media directly from a URL. This method requires the `inputs` array, which contains media objects specifying different types such as `video`, `audio` and `watermark`. Each media object can include various optional parameters like `audio`, `metadata`, `subtitle`, and `watermark`, depending on the media type specified.

In the response, a unique `id` is returned, which serves as the `media_id` for managing further media operations such as retrieving media details, generating playback IDs, updating metadata, or deleting the asset.

### Parameters Details:

| **Parameter**             | **Description**                                                                                             | **Type** | **Accepted Values**                                               |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------- |
| `inputs` (required)       | Array of media objects containing details about each media type (`video`, `audio`, `text`, `watermark`).    | Array    | Array of objects specifying media details (see below).            |
| `accessPolicy` (required) | Determines whether access to the streamed content is kept private or available to all.                      | String   | `public`, `private`, `drm`                                        |
| `metadata`                | Metadata key-value pairs for the media (max 10 entries, each with a `key` and `value`).                     | Object   | Key-value pairs (max 255 chars per key-value pair).               |
| `subtitles`               | Subtitles details for the video, including language name and BCP 47 language code.                          | Object   | Subtitle object containing `name`, `metadata` and `languageCode`. |
| `optimizeAudio`           | If `True`, enhances audio quality and volume. Defaults to `False`. Available only for pre-recorded content. | Boolean  | `True`, `False`                                                   |
| `maxResolution`           | The maximum resolution available for the video (e.g., `1080p`, `4k`).                                       | String   | `360p`, `480p`, `720p`, `1080p`, `1440p`, `1880p`                 |
| `mp4Support`              | Specifies MP4 video support options: `capped_4k`, `audioOnly`, or both for offline viewing.                 | String   | `capped_4k`, `audioOnly`, `audioOnly,capped_4k`                   |

### Inputs Array

Each element in the `inputs` array represents a media object containing different media types (like `video`, `audio`, `watermark`) with the following structure:

| **Parameter**     | **Description**                                                                 | **Type** | **Accepted Values**                                                          |
| ----------------- | ------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| `type` (required) | The type of media (e.g., `video`, `audio`, `watermark`).                        | String   | `video`, `audio`, `watermark`                                                |
| `url` (required)  | URL of the media file to be uploaded (MP4, MOV, MKV, MP3, TS, etc.).            | String   | Valid URL path for the media file (e.g., MP4, MOV, MKV, MP3, TS).            |
| `startTime`       | Start time in seconds for encoding the media.                                   | Number   | Any non-negative integer value                                               |
| `endTime`         | End time in seconds for encoding the media.                                     | Number   | Any non-negative integer value greater than `startTime`.                     |
| `introUrl`        | URL of the intro video to add at the beginning of the media.                    | String   | Valid URL path for the intro media file.                                     |
| `outroUrl`        | URL of the outro video to add at the end of the media.                          | String   | Valid URL path for the outro media file.                                     |
| `expungeSegments` | List of `startTime-endTime` strings to remove specific segments from the video. | Array    | Array of strings representing time ranges in the format `startTime-endTime`. |
| `watermark`       | Watermark details to overlay on the video.                                      | Object   | See below for watermark parameters.                                          |
| `audio`           | Audio details, including any audio swap or overlay settings.                    | Object   | See below for audio parameters.                                              |

#### Watermark Object

If the media type is `"watermark"`, the following parameters are required:

| **Parameter** | **Description**                                                         | **Type** | **Accepted Values**                                                       |
| ------------- | ----------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------- |
| `type`        | Type of overlay (currently only supports `'watermark'`).                | String   | `'watermark'`                                                             |
| `url`         | URL of the watermark image to overlay on the media.                     | String   | Valid URL path to the watermark image (PNG, JPEG, etc.).                  |
| `placement`   | Placement details for positioning the watermark on the video.           | Object   | Placement object with alignment, margin, and size properties (see below). |
| `width`       | Width of the watermark in pixels or percentage (e.g., `20%`, `200px`).  | String   | Any valid string for width (e.g., `20%`, `200px`).                        |
| `height`      | Height of the watermark in pixels or percentage (e.g., `20%`, `200px`). | String   | Any valid string for height (e.g., `20%`, `200px`).                       |
| `opacity`     | Opacity of the watermark in percentage (0-100%).                        | String   | Any integer value from `0` to `100`                                       |

#### Placement Object for Watermark

| **Parameter** | **Description**                                                                    | **Type** | **Accepted Values**                                                |
| ------------- | ---------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------ |
| `xAlign`      | Horizontal alignment of the watermark. Possible values: `left`, `center`, `right`. | String   | `left`, `center`, `right`                                          |
| `xMargin`     | Horizontal margin from the edge of the video (in pixels).                          | String   | Any non-negative integer value or percentage (e.g., `10px`, `5%`). |
| `yAlign`      | Vertical alignment of the watermark. Possible values: `top`, `center`, `bottom`.   | String   | `top`, `center`, `bottom`                                          |
| `yMargin`     | Vertical margin from the edge of the video (in pixels).                            | String   | Any non-negative integer value or percentage (e.g., `10px`, `5%`). |

#### Audio Object

If the media type is `"audio"`, the following parameters are relevant:

| **Parameter**  | **Description**                                                    | **Type** | **Accepted Values**                                                                                 |
| -------------- | ------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------- |
| `type`         | Type of overlay (currently only supports `'audio'`).               | String   | `'audio'`                                                                                           |
| `swapTrackUrl` | URL of the audio track to replace the existing audio in the video. | String   | Valid URL path for the new audio track (MP3, WAV, etc.).                                            |
| `imposeTracks` | List of additional audio tracks to overlay on the video.           | Array    | Array of audio track objects with `url`, `startTime`, `endTime`, `fadeInLevel`, and `fadeOutLevel`. |

#### Impose Tracks Object for Audio

| **Parameter**  | **Description**                                                            | **Type** | **Accepted Values**                                           |
| -------------- | -------------------------------------------------------------------------- | -------- | ------------------------------------------------------------- |
| `url`          | URL of the audio track to impose on the video.                             | String   | Valid URL path to the additional audio file (MP3, WAV, etc.). |
| `startTime`    | Start time in seconds for the imposed audio to begin.                      | Number   | Any non-negative integer value                                |
| `endTime`      | End time in seconds for the imposed audio to stop.                         | Number   | Any non-negative integer value greater than `startTime`.      |
| `fadeInLevel`  | Level of fade-in effect in seconds for the imposed audio at the beginning. | Number   | Any non-negative integer value                                |
| `fadeOutLevel` | Level of fade-out effect in seconds for the imposed audio at the end.      | Number   | Any non-negative integer value                                |

#### Metadata Object

| **Parameter** | **Description**                                                                                              | **Type** | **Accepted Values**                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------ |
| `metadata`    | Tag the video with key-value pairs for searchable metadata. Maximum of 10 entries, each with 255 characters. | Object   | Up to 10 key-value pairs, each key and value being alphanumeric strings of up to 255 characters. |

#### Subtitles Object

| **Parameter**     | **Description**                                             | **Type** | **Accepted Values**                                            |
| ----------------- | ----------------------------------------------------------- | -------- | -------------------------------------------------------------- |
| `metadata`        | Metadata key-value pairs for the subtitles. Optional field. | Object   | Key-value pairs (max 255 characters per key-value pair).       |
| `name` (required) | Name of the language for the subtitles.                     | String   | Any string, such as `"English"`, `"French"`, `"Spanish"`, etc. |
| `languageCode`    | BCP 47 compliant language code (e.g., `"en"` for English).  | String   | Any valid BCP 47 language code (e.g., `"en"`, `"fr"`, `"es"`)  |

### Example Request:

```python
# Note for Async SDK Users: When using the AsyncClient, all API methods must be prefixed with the await keyword. 
# For example: await client.media.create_pull_video(media_from_url_request)

# Define the request payload for uploading media from a URL.
media_from_url_request = {
  "metadata": {
    "newKey": "New Value",
  },
  "subtitles": {
    "metadata": {
      "newKey": "New Value",
      "newKey-1": "New Value",
    },
    "name": "english",
    "languageCode": "en",
  },
  "accessPolicy": "public", # required
  "optimizeAudio": True,
  "maxResolution": "1080p",
  "inputs": [
      {
        "type": "video", # required
        "url": "https://static.fastpix.io/sample.mp4", # required
        "startTime": 0,
        "endTime": 5,
        "introUrl": "https://static.fastpix.io/sample.mp4",
        "outroUrl": "https://static.fastpix.io/sample.mp4",
        "expungeSegments": ["3-5", "6-8"],
      },
      {
        "placement": {
          "xAlign": "left",
          "xMargin": "10%",
          "yAlign": "middle",
          "yMargin": "10%",
        },
        "type": "watermark",
        "url": "https://static.fastpix.io/watermark-4k.png",
        "width": "25%",
        "height": "25%",
        "opacity": "80%",
      },
      {
        "type": "audio",
        "swapTrackUrl":
          "https://file-examples.com/storage/fe0e9b723466913cf9611b7/2017/11/file_example_MP3_700KB.mp3",
        "imposeTracks": [
          {
            "url": "https://muxed.s3.amazonaws.com/example-impose-audio-track.m4a",
            "startTime": 0,
            "endTime": 5,
            "fadeInLevel": 1,
            "fadeOutLevel": 4,
          },
          {
            "url": "https://muxed.s3.amazonaws.com/example-impose-audio-track.m4a",
            "startTime": 0,
            "endTime": 5,
            "fadeInLevel": 1,
            "fadeOutLevel": 4,
          },
        ],
      },
  ],
  "mp4Support": "capped_4k",
}

media_response = client.media.create_pull_video(media_from_url_request)
print("media_response", media_response)
```

---

# Method: client.media.get_presigned_url()

This method allows you to upload a video file directly from your local device to FastPix. By using this method with your desired media settings, you will receive an `uploadId` and a `url`. You can then use the `url` to upload your media via a HTTP `PUT` request. Note that `corsOrigin` and `accessPolicy` are mandatory fields, while the other parameters are optional.

In the response, a unique `uploadId` is returned, which serves as the `media_id` for managing further media operations such as retrieving media details, generating playback IDs, updating metadata, or deleting the asset.

### Parameters Details:

| **Parameter**                  | **Description**                                                                                           | **Type** | **Accepted Values**    |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- | -------- | ---------------------- |
| `corsOrigin` (required)        | The allowed origin for Cross-Origin Resource Sharing (CORS). Set to `"*"` to allow all origins.           | String   | Any valid URL or `"*"` |
| `pushMediaSettings` (required) | Configuration settings for the media upload, including access policy, resolution, and audio optimization. | Object   | -                      |

### Push Media Settings Object

| **Parameter**             | **Description**                                                                                                   | **Type** | **Accepted Values**                                                                              |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------ |
| `accessPolicy` (required) | Determines whether the media access is private, public, or drm.                                                   | String   | `private`, `public`, `drm`                                                                       |
| `startTime`               | The start time (in seconds) for encoding to begin within the video file.                                          | Number   | Any non-negative integer value                                                                   |
| `endTime`                 | The end time (in seconds) for encoding to stop within the video file.                                             | Number   | Any non-negative integer value, must be greater than `startTime`.                                |
| `inputs`                  | Array of media input objects, each containing details such as URL, type, and additional metadata.                 | Array    | Array of objects representing media input.                                                       |
| `metadata`                | Tag the video with key-value pairs for searchable metadata. Maximum of 10 entries, each with 255 characters.      | Object   | Up to 10 key-value pairs, each key and value being alphanumeric strings of up to 255 characters. |
| `subtitles`               | Subtitles details for the video, including language name and BCP 47 language code.                                | Object   | Subtitle object containing `name`, `metadata` and `languageCode`.                                |
| `optimizeAudio`           | If set to True, enhances the audio quality and volume. Defaults to True. Only available for pre-recorded content. | Boolean  | `True`, `False`                                                                                  |
| `maxResolution`           | Specifies the highest resolution available for the media (e.g., `"1080p"`). Defaults to `1080p`.                  | String   | `144p`, `240p`, `360p`, `480p`, `720p`, `1080p`, `1440p`, `2160p`                                |
| `mp4Support`              | Defines the MP4 video support options (`"capped_4k"`, `"audioOnly"`, or both for offline viewing).                | String   | `"capped_4k"`, `"audioOnly"`, `"both"`                                                           |

#### Inputs Object

| **Parameter**     | **Description**                                                                                                   | **Type** | **Accepted Values**                                               |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------- |
| `type`            | The type of input. Possible values: `video`, `audio`, `text`, or `watermark`.                                     | String   | `video`, `audio`, `text`, `watermark`                             |
| `startTime`       | The start time (in seconds) for the segment of the media to encode.                                               | Number   | Any non-negative integer value                                    |
| `endTime`         | The end time (in seconds) for the segment of the media to encode.                                                 | Number   | Any non-negative integer value, must be greater than `startTime`. |
| `introUrl`        | URL of the intro video to add at the beginning of the media.                                                      | String   | Valid URL for intro media                                         |
| `outroUrl`        | URL of the outro video to add at the end of the media.                                                            | String   | Valid URL for outro media                                         |
| `expungeSegments` | Array of strings specifying start and end times of segments to remove from the video (e.g., `"0-10"`, `"50-60"`). | Array    | Array of strings with the format `"startTime-endTime"`.           |
| `watermark`       | Watermark details, if `type = "watermark"`. Contains watermark URL and placement info.                            | Object   | Object with watermark parameters.                                 |
| `audio`           | Audio track details if `type = "audio"`. Includes information on replacing or overlaying audio tracks.            | Object   | Object with audio-related parameters.                             |

#### Watermark Object

If the media type is `"watermark"`, the following parameters are required:

| **Parameter** | **Description**                                                         | **Type** | **Accepted Values**                                                       |
| ------------- | ----------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------- |
| `type`        | Type of overlay (currently only supports `'watermark'`).                | String   | `'watermark'`                                                             |
| `url`         | URL of the watermark image to overlay on the media.                     | String   | Valid URL path to the watermark image (PNG, JPEG, etc.).                  |
| `placement`   | Placement details for positioning the watermark on the video.           | Object   | Placement object with alignment, margin, and size properties (see below). |
| `width`       | Width of the watermark in pixels or percentage (e.g., `20%`, `200px`).  | String   | Any valid string for width (e.g., `20%`, `200px`).                        |
| `height`      | Height of the watermark in pixels or percentage (e.g., `20%`, `200px`). | String   | Any valid string for height (e.g., `20%`, `200px`).                       |
| `opacity`     | Opacity of the watermark in percentage (0-100%).                        | String   | Any integer value from `0` to `100`                                       |

#### Placement Object for Watermark

| **Parameter** | **Description**                                                                    | **Type** | **Accepted Values**                                                |
| ------------- | ---------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------ |
| `xAlign`      | Horizontal alignment of the watermark. Possible values: `left`, `center`, `right`. | String   | `left`, `center`, `right`                                          |
| `xMargin`     | Horizontal margin from the edge of the video (in pixels).                          | String   | Any non-negative integer value or percentage (e.g., `10px`, `5%`). |
| `yAlign`      | Vertical alignment of the watermark. Possible values: `top`, `center`, `bottom`.   | String   | `top`, `center`, `bottom`                                          |
| `yMargin`     | Vertical margin from the edge of the video (in pixels).                            | String   | Any non-negative integer value or percentage (e.g., `10px`, `5%`). |

#### Audio Object

If the media type is `"audio"`, the following parameters are relevant:

| **Parameter**  | **Description**                                                    | **Type** | **Accepted Values**                                                                                 |
| -------------- | ------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------- |
| `type`         | Type of overlay (currently only supports `'audio'`).               | String   | `'audio'`                                                                                           |
| `swapTrackUrl` | URL of the audio track to replace the existing audio in the video. | String   | Valid URL path for the new audio track (MP3, WAV, etc.).                                            |
| `imposeTracks` | List of additional audio tracks to overlay on the video.           | Array    | Array of audio track objects with `url`, `startTime`, `endTime`, `fadeInLevel`, and `fadeOutLevel`. |

#### Impose Tracks Object for Audio

| **Parameter**  | **Description**                                                            | **Type** | **Accepted Values**                                           |
| -------------- | -------------------------------------------------------------------------- | -------- | ------------------------------------------------------------- |
| `url`          | URL of the audio track to impose on the video.                             | String   | Valid URL path to the additional audio file (MP3, WAV, etc.). |
| `startTime`    | Start time in seconds for the imposed audio to begin.                      | Number   | Any non-negative integer value                                |
| `endTime`      | End time in seconds for the imposed audio to stop.                         | Number   | Any non-negative integer value greater than `startTime`.      |
| `fadeInLevel`  | Level of fade-in effect in seconds for the imposed audio at the beginning. | Number   | Any non-negative integer value                                |
| `fadeOutLevel` | Level of fade-out effect in seconds for the imposed audio at the end.      | Number   | Any non-negative integer value                                |

#### Metadata Object

| **Parameter** | **Description**                                                                                              | **Type** | **Accepted Values**                                                                              |
| ------------- | ------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------ |
| `metadata`    | Tag the video with key-value pairs for searchable metadata. Maximum of 10 entries, each with 255 characters. | Object   | Up to 10 key-value pairs, each key and value being alphanumeric strings of up to 255 characters. |

#### Subtitles Object

| **Parameter**     | **Description**                                             | **Type** | **Accepted Values**                                            |
| ----------------- | ----------------------------------------------------------- | -------- | -------------------------------------------------------------- |
| `metadata`        | Metadata key-value pairs for the subtitles. Optional field. | Object   | Key-value pairs (max 255 characters per key-value pair).       |
| `name` (required) | Name of the language for the subtitles.                     | String   | Any string, such as `"English"`, `"French"`, `"Spanish"`, etc. |
| `languageCode`    | BCP 47 compliant language code (e.g., `"en"` for English).  | String   | Any valid BCP 47 language code (e.g., `"en"`, `"fr"`, `"es"`)  |

### Example Request:

```python
media_from_device_request = {
    "corsOrigin": "*", # required
    "pushMediaSettings": {
    "accessPolicy": "public", # required
    "startTime": 0,
    "endTime": 120,
    "subtitles": {
    "metadata": {
      "newKey": "New Value",
      "newKey-1": "New Value",
    },
    "name": "english",
    "languageCode": "en",
    },
    "inputs": [
      {
        "type": "video", # required
        "url": "https://static.fastpix.io/sample.mp4", # required
        "startTime": 0,
        "endTime": 60,
        "introUrl": "https://static.fastpix.io/sample.mp4",
        "outroUrl": "https://static.fastpix.io/sample.mp4",
        "expungeSegments": ["3-5", "6-8"],
      },
      {
        "placement": {
          "xAlign": "left",
          "xMargin": "10%",
          "yAlign": "middle",
          "yMargin": "10%",
        },
        "type": "watermark",
        "url": "https://static.fastpix.io/watermark-4k.png",
        "width": "25%",
        "height": "25%",
        "opacity": "80%",
      },
      {
        "type": "audio",
        "swapTrackUrl":
          "https://file-examples.com/storage/fe0e9b723466913cf9611b7/2017/11/file_example_MP3_700KB.mp3",
        "imposeTracks": [
          {
            "url": "https://muxed.s3.amazonaws.com/example-impose-audio-track.m4a",
            "startTime": 0,
            "endTime": 5,
            "fadeInLevel": 1,
            "fadeOutLevel": 4,
          },
          {
            "url": "https://muxed.s3.amazonaws.com/example-impose-audio-track.m4a",
            "startTime": 0,
            "endTime": 5,
            "fadeInLevel": 1,
            "fadeOutLevel": 4,
          },
        ],
      },
    ]
    "optimizeAudio": True,
    "maxResolution": "1080p",
    "mp4Support": "capped_4k"
  }
}

media_from_device_response = client.media.get_presigned_url(media_from_device_request)
print("Media uploaded successfully", media_from_device_response)
```
