# ListLiveClipsResponse

List of video media


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    | Example                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `success`                                                                      | *Optional[bool]*                                                               | :heavy_minus_sign:                                                             | Demonstrates whether the request is successful or not.                         | true                                                                           |
| `data`                                                                         | List[[models.Media](../models/media.md)]                                       | :heavy_minus_sign:                                                             | Displays the result of the request.                                            |                                                                                |
| `pagination`                                                                   | [Optional[models.Pagination]](../models/pagination.md)                         | :heavy_minus_sign:                                                             | Pagination organizes content into pages for better readability and navigation. |                                                                                |