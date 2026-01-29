# Dimensions

## Overview

Operations involving dimensions

### Available Operations

* [list](#list) - List the dimensions
* [list_filter_values](#list_filter_values) - List the filter values for a dimension

## list

Retrieves a list of dimensions that can be used as query parameters across various data endpoints. Each dimension has a unique id that can be used to filter data effectively. 

The dimensions retrieved from this endpoint can be used in conjunction with the <a href="https://docs.fastpix.io/reference/list_video_views">list video views</a> and <a href="https://docs.fastpix.io/reference/list_by_top_content">list by top content</a> endpoints to filter results based on specific criteria. For example, you can filter views by `browser_name`, `os_name`, `device_type`, and more.

Related guides: <a href="https://docs.fastpix.io/page/what-video-data-do-we-capture#/">What Video Data do we capture?</a> ,   <a href="https://docs.fastpix.io/docs/user-passable-metadata-1">Use passable dimensions</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="list_dimensions" method="get" path="/data/dimensions" -->
```python
import os
import json

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.dimensions.list()

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.ListDimensionsResponse](../../models/listdimensionsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## list_filter_values

This endpoint returns the filter values associated with a specific dimension, along with the total number of video views for each value. For example, it can list all `browser_name` (dimension) and show how many views occurred for all available browsers like Chrome, Safari (filter values). 

In order to use the <a href="https://docs.fastpix.io/docs/custom-business-metadata">Custom Dimensions</a>, you must enable them in the dashboard under settings option based on the plan you have opted for.

#### Example

A developer wants to know how their video content performs across different browsers. By calling this endpoint for the `device_type` dimension, they can retrieve a breakdown of video views by each device (for example, Desktop, Mobile, Tablet). This data helps the developer understand where optimizations or troubleshooting is necessary.

Related guide: <a href="https://docs.fastpix.io/docs/understand-dashboard-ui#filters-and-timeframes">Filters and timespan</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="list_filter_values_for_dimension" method="get" path="/data/dimensions/{dimensionsId}" -->
```python
import os
import json

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.dimensions.list_filter_values(dimensions_id="browser_name", timespan="24:hours", filterby="browser_name:Chrome")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                                                                                                                                                                                                                                                                                                                                                                        | Type                                                                                                                                                                                                                                                                                                                                                                                                                             | Required                                                                                                                                                                                                                                                                                                                                                                                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                      | Example                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dimensions_id`                                                                                                                                                                                                                                                                                                                                                                                                                  | [models.DimensionsID](../../models/dimensionsid.md)                                                                                                                                                                                                                                                                                                                                                                              | :heavy_check_mark:                                                                                                                                                                                                                                                                                                                                                                                                               | Pass Dimensions Id<br/>                                                                                                                                                                                                                                                                                                                                                                                                          | browser_name                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `timespan`                                                                                                                                                                                                                                                                                                                                                                                                                       | [Optional[models.ListFilterValuesForDimensionTimespan]](../../models/listfiltervaluesfordimensiontimespan.md)                                                                                                                                                                                                                                                                                                                    | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                               | This parameter specifies the time span between which the video views list must be retrieved by. You can provide either from and to unix epoch timestamps or time duration. The scope of duration is between 60 minutes to 30 days.<br/><br/>**Accepted formats are:**<br/><br/>array of epoch timestamps for example <br/>`timespan[]=1498867200&timespan[]=1498953600`<br/><br/>duration string for example  <br/>`timespan[]=24:hours` or `timespan[]=7:days`<br/> | 24:hours                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `filterby`                                                                                                                                                                                                                                                                                                                                                                                                                       | *Optional[str]*                                                                                                                                                                                                                                                                                                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                               | Pass the dimensions and their corresponding values you want to filter the views by. For excluding the values in the filter we can pass "!" before the filter value. The list of filters can be obtained from list of dimensions endpoint.<br/>Example Values : [ browser_name:Chrome , os_name:macOS , !device_name:Galaxy ]<br/>                                                                                                | browser_name:Chrome                                                                                                                                                                                                                                                                                                                                                                                                              |
| `retries`                                                                                                                                                                                                                                                                                                                                                                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                                                                                                                                                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                                                                                                                                                                                                                                                                               | Configuration to override the default retry behavior of the client.                                                                                                                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                                                                                                                                                                  |

### Response

**[models.ListFilterValuesForDimensionResponse](../../models/listfiltervaluesfordimensionresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |