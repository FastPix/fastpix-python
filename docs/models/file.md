# File

Contains metadata and structural details about the media file.


## Fields

| Field                                                                                   | Type                                                                                    | Required                                                                                | Description                                                                             | Example                                                                                 |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `container_format`                                                                      | *Optional[str]*                                                                         | :heavy_minus_sign:                                                                      | Specifies the container format that encapsulates audio, video, subtitles, and metadata. | mp4                                                                                     |
| `tracks`                                                                                | List[[models.RetrieveMediaInputInfoTrack](../models/retrievemediainputinfotrack.md)]    | :heavy_minus_sign:                                                                      | A list of all media tracks including video, audio, and subtitles.                       |                                                                                         |