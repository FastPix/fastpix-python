# CreatePlaylistRequestManual


## Fields

| Field                                                   | Type                                                    | Required                                                | Description                                             | Example                                                 |
| ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| `name`                                                  | *str*                                                   | :heavy_check_mark:                                      | Name of the playlist.                                   | Playlist name                                           |
| `reference_id`                                          | *str*                                                   | :heavy_check_mark:                                      | Unique string value assigned by user to the playlist.   | a1                                                      |
| `type`                                                  | *Literal["manual"]*                                     | :heavy_check_mark:                                      | Manual playlist type (no `playOrder`).                  | manual                                                  |
| `description`                                           | *Optional[str]*                                         | :heavy_minus_sign:                                      | Description for a playlist (Optional).                  | This is a playlist                                      |
| `limit`                                                 | *Optional[int]*                                         | :heavy_minus_sign:                                      | Optional parameter to limit no. of media in a playlist. |                                                         |