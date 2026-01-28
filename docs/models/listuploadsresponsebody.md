# ListUploadsResponseBody

List of video media


## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    | Example                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `success`                                                                      | *Optional[bool]*                                                               | :heavy_minus_sign:                                                             | Shows the request status. Returns true for success and false for failure.      | true                                                                           |
| `data`                                                                         | List[[models.UnusedDirectUpload](../models/unuseddirectupload.md)]             | :heavy_minus_sign:                                                             | Displays the result of the request.                                            |                                                                                |
| `pagination`                                                                   | [Optional[models.Pagination]](../models/pagination.md)                         | :heavy_minus_sign:                                                             | Pagination organizes content into pages for better readability and navigation. |                                                                                |