# ListByTopContentResponseBody

Get the list of Views


## Fields

| Field                                                                             | Type                                                                              | Required                                                                          | Description                                                                       | Example                                                                           |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `success`                                                                         | *Optional[bool]*                                                                  | :heavy_minus_sign:                                                                | Shows the request status. Returns true for success and false for failure.         |                                                                                   |
| `data`                                                                            | List[[models.ViewsByTopContentDetails](../models/viewsbytopcontentdetails.md)]    | :heavy_minus_sign:                                                                | Displays the result of the request.                                               |                                                                                   |
| `timespan`                                                                        | List[*int*]                                                                       | :heavy_minus_sign:                                                                | The timespan from and to details displayed in the form of unix epoch timestamps.<br/> | {<br/>"availableValue": [<br/>1610025789,<br/>1610025947<br/>]<br/>}              |