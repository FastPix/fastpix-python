# DrmConfigurations

## Overview

### Available Operations

* [list](#list) - Get list of DRM configuration IDs
* [get_by_id](#get_by_id) - Get DRM configuration by ID

## list

This endpoint retrieves the DRM configuration (DRM ID) associated with a workspace. It returns a list of DRM configurations, identified by a unique DRM ID, which is used for creating DRM encrypted asset.

**How it works:**
1. Make a GET request to this endpoint.  
2. Optionally use the `offset` and `limit` query parameters to paginate through the list of DRM configurations.  
3. The response includes a list of DRM IDs and pagination metadata.

**Example:**  
A media service provider may retrieve DRM configuration for a workspace to create DRM content.

Related guide: <a href="https://docs.fastpix.io/docs/secure-playback-with-drm">Manage DRM configuration</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="getDrmConfiguration" method="get" path="/on-demand/drm-configurations" -->
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

    res = fastpix.drm_configurations.list(offset=1, limit=10)

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                                        | Type                                                                             | Required                                                                         | Description                                                                      | Example                                                                          |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `offset`                                                                         | *Optional[int]*                                                                  | :heavy_minus_sign:                                                               | Offset determines the starting point for data retrieval within a paginated list. | 1                                                                                |
| `limit`                                                                          | *Optional[int]*                                                                  | :heavy_minus_sign:                                                               | Limit specifies the maximum number of items to display per page.                 | 10                                                                               |
| `retries`                                                                        | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                 | :heavy_minus_sign:                                                               | Configuration to override the default retry behavior of the client.              |                                                                                  |

### Response

**[models.GetDrmConfigurationResponse](../../models/getdrmconfigurationresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |

## get_by_id

This endpoint retrieves a DRM configuration ID. It is used to fetch the DRM-related ID for a workspace, typically required when validating or applying DRM policies to video assets.

**How it works:**
1. Make a GET request to this endpoint, replacing `{drmConfigurationId}` with the UUID of the DRM configuration.  
2. The response contains the associated DRM configuration ID.

Related guide: <a href="https://docs.fastpix.io/docs/secure-playback-with-drm">Manage DRM configuration</a>

### Example Usage

<!-- UsageSnippet language="python" operationID="getDrmConfigurationById" method="get" path="/on-demand/drm-configurations/{drmConfigurationId}" -->
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

    res = fastpix.drm_configurations.get_by_id(drm_configuration_id="your-drm-configuration-id")

    # Handle response
    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `drm_configuration_id`                                              | *str*                                                               | :heavy_check_mark:                                                  | The unique identifier of the DRM configuration.                     | your-drm-configuration-id                                           |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.GetDrmConfigurationByIDResponse](../../models/getdrmconfigurationbyidresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.FastpixDefaultError | 4XX, 5XX                   | \*/\*                      |