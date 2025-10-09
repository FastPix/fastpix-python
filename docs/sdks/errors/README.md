# Errors
(*errors*)

## Overview

### Available Operations

* [list_errors](#list_errors) - List errors

## list_errors

This endpoint returns the total number of playback errors that occurred, along with the total number of views captured, based on the specified timespan and filters. It provides insights into the overall playback quality and helps identify potential issues that may impact viewer experience. 


#### Key fields in response

* **percentage:** The percentage of views affected by the specific error. 
* **uniqueViewersEffectedPercentage:** The percentage of unique viewers affected by the specific error (available only in the topErrors section). 
* **notes:** Additional notes or information about the specific error. 
* **message:** The error message or description. 
* **lastSeen:** The timestamp of when the error was last observed. 
* **id:** The unique identifier for the specific error. 
* **description:** A description of the specific error. 
* **count:** The number of occurrences of the specific error. 
* **code:** The error code associated with the specific error. 


Related guide: <a href="https://docs.fastpix.io/docs/track-playback-errors">Troubleshoot errors</a>


### Example Usage

<!-- UsageSnippet language="python" operationID="list_errors" method="get" path="/data/errors" -->
```python
from fastpix_python import Fastpix, models


with Fastpix(
    security=models.Security(
        username = "your-access-token",
        password = "secret-key",
    ),
) as fastpix:

    res = fastpix.errors.list_errors(timespan="7:days", filterby="browser_name:Chrome", limit=1)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                | Type                                                                                                                                                                                                                                                                                                                     | Required                                                                                                                                                                                                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                              | Example                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `timespan`                                                                                                                                                                                                                                                                                                               | [models.ListErrorsTimespan](../../models/listerrorstimespan.md)                                                                                                                                                                                                                                                          | :heavy_check_mark:                                                                                                                                                                                                                                                                                                       | This parameter specifies the time span between which the video views list should be retrieved by. You can provide either from and to unix epoch timestamps or time duration. The scope of duration is between 60 minutes to 30 days.<br/>                                                                                | 7:days                                                                                                                                                                                                                                                                                                                   |
| `filterby`                                                                                                                                                                                                                                                                                                               | *Optional[str]*                                                                                                                                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                       | Pass the dimensions and their corresponding values you want to filter the views by. For excluding the values in the filter we can pass '!' before the filter value. The list of filters can be obtained from list of dimensions endpoint.<br/>Example Values : [ browser_name:Chrome , os_name:macOS , device_name:Galaxy ]<br/> | browser_name:Chrome                                                                                                                                                                                                                                                                                                      |
| `limit`                                                                                                                                                                                                                                                                                                                  | *Optional[int]*                                                                                                                                                                                                                                                                                                          | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                       | Pass the limit to display only the rows specified by the value for top errors.<br/>                                                                                                                                                                                                                                      | 1                                                                                                                                                                                                                                                                                                                        |
| `retries`                                                                                                                                                                                                                                                                                                                | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                         | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                       | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                      |                                                                                                                                                                                                                                                                                                                          |

### Response

**[models.ListErrorsResponse](../../models/listerrorsresponse.md)**

### Errors

| Error Type                     | Status Code                    | Content Type                   |
| ------------------------------ | ------------------------------ | ------------------------------ |
| errors.InvalidPermissionError  | 401                            | application/json               |
| errors.ViewNotFoundError       | 404                            | application/json               |
| errors.ValidationErrorResponse | 422                            | application/json               |
| errors.FastpixDefaultError     | 4XX, 5XX                       | \*/\*                          |