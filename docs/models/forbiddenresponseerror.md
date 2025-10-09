# ForbiddenResponseError

Displays details about the reasons behind the request's failure.


## Fields

| Field                                                       | Type                                                        | Required                                                    | Description                                                 | Example                                                     |
| ----------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| `code`                                                      | *Optional[int]*                                             | :heavy_minus_sign:                                          | Forbidden response                                          | 403                                                         |
| `message`                                                   | *Optional[str]*                                             | :heavy_minus_sign:                                          | A descriptive message providing more details for the error. | forbidden                                                   |