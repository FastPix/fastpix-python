# NotFoundErrorPlaybackIDError

Displays details about the reasons behind the request's failure.


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    | Example                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `code`                                                                         | *Optional[float]*                                                              | :heavy_minus_sign:                                                             | Displays the error code indicating the type of the error.                      | 404                                                                            |
| `message`                                                                      | *Optional[str]*                                                                | :heavy_minus_sign:                                                             | A descriptive message providing more details for the error.                    | stream/playbackId not found                                                    |
| `description`                                                                  | *Optional[str]*                                                                | :heavy_minus_sign:                                                             | A detailed explanation of the possible causes for the error.<br/>              | The requested resource (eg:streamId/playbackId) doesn't exist in the workspace |