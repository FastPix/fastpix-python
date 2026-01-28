# TracksSubtitles


## Fields

| Field                                                           | Type                                                            | Required                                                        | Description                                                     | Example                                                         |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `status`                                                        | *Optional[str]*                                                 | :heavy_minus_sign:                                              | Current status of the generated subtitle track.                 | preparing                                                       |
| `url`                                                           | *OptionalNullable[str]*                                         | :heavy_minus_sign:                                              | URL of the generated subtitle file (VTT). Null while preparing. | https://stream.fastpix.io/subtitles/abc123.vtt                  |