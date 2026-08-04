# MediaMp4SupportEntry

A single MP4 rendition generated for the media.

`Media.mp4_support` holds a list of these entries — one per downloadable rendition
requested via `mp4Support` (for example, a capped-4K video file and an audio-only
m4a file). The field is omitted when no MP4 support has been requested.

Every field is optional: the `audioOnly` rendition carries no `height`/`width`.

## Example Usage

```python
from fastpix_python import Fastpix

with Fastpix(
    username="your-access-token",
    password="your-secret-key",
) as fastpix:

    res = fastpix.manage_videos.get_media(media_id="your-media-id")

    for rendition in res.data.mp4_support or []:
        print(rendition.type, rendition.status, rendition.ext)
```

## Fields

| Field       | Type                                                                        | Required           | Description                                                                                                                              | Example   |
| ----------- | --------------------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `type`      | [Optional[models.MediaMp4SupportEntryType]](#mediamp4supportentrytype)     | :heavy_minus_sign: | The MP4 rendition type. `capped_4k` is a downloadable MP4 video capped at 4K resolution, `audioOnly` is a downloadable m4a audio-only file. | capped_4k |
| `status`    | [Optional[models.MediaMp4SupportEntryStatus]](#mediamp4supportentrystatus) | :heavy_minus_sign: | Generation status of this MP4 rendition.                                                                                                   | ready     |
| `height`    | *Optional[int]*                                                            | :heavy_minus_sign: | Pixel height of the rendition. Omitted for the `audioOnly` type.                                                                           | 1080      |
| `width`     | *Optional[int]*                                                            | :heavy_minus_sign: | Pixel width of the rendition. Omitted for the `audioOnly` type.                                                                            | 1920      |
| `ext`       | [Optional[models.MediaMp4SupportEntryExt]](#mediamp4supportentryext)       | :heavy_minus_sign: | File extension of the downloadable rendition.                                                                                              | mp4       |

## Related enums

### MediaMp4SupportEntryType

| Name          | Value       |
| ------------- | ----------- |
| `CAPPED_4K`   | capped_4k   |
| `AUDIO_ONLY`  | audioOnly   |

### MediaMp4SupportEntryStatus

| Name        | Value     |
| ----------- | --------- |
| `PREPARING` | preparing |
| `READY`     | ready     |
| `FAILED`    | failed    |

### MediaMp4SupportEntryExt

| Name   | Value |
| ------ | ----- |
| `MP4`  | mp4   |
| `M4A`  | m4a   |

Unrecognised values returned by the API pass through as plain strings rather than
raising, so new rendition types do not break deserialization.
