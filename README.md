# FastPix Python SDK

A robust, type-safe Python SDK designed for seamless integration with the FastPix API platform.


## Introduction

The FastPix Python SDK simplifies integration with the FastPix platform. It provides a clean, Python interface for secure and efficient communication with the FastPix API, enabling easy management of media uploads, live streaming, on‑demand content, playlists, video analytics, and signing keys for secure access and token management. It is intended for use with Python 3.9.2 and above.

## Prerequisites

### Environment and Version Support

| Requirement | Version | Description |
|---|---:|---|
| Python | `3.9.2+` | Core runtime environment |
| pip/uv/poetry | `Latest` | Package manager for dependencies |
| Internet | `Required` | API communication and authentication |

> Pro Tip: We recommend using Python 3.11+ for optimal performance and the latest language features.

### Getting Started with FastPix

To get started with the FastPix Python SDK, ensure you have the following:

- The FastPix APIs are authenticated using a **Username** and a **Password**. You must generate these credentials to use the SDK.
- Follow the steps in the [Authentication with Basic Auth](https://docs.fastpix.io/docs/basic-authentication) guide to obtain your credentials.

### Environment Variables (Optional)

Configure your FastPix credentials using environment variables for enhanced security and convenience:

```bash
# Set your FastPix credentials
export FASTPIX_USERNAME="your-access-token"
export FASTPIX_PASSWORD="your-secret-key"
```

> Security Note: Never commit your credentials to version control. Use environment variables or secure credential management systems.

## Table of Contents

* [FastPix Python SDK](#fastpix-python-sdk)
  * [Setup](#setup)
  * [Example Usage](#example-usage)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Debugging](#debugging)
  * [Development](#development)

## Setup

### Installation

Install the FastPix Python SDK using your preferred package manager:

#### uv

*uv* is a fast Python package installer and resolver, designed as a drop-in replacement for pip and pip-tools. It's recommended for its speed and modern Python tooling capabilities.

```bash
uv add fastpix-python
```

#### pip

*pip* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install fastpix-python
```

#### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add fastpix-python
```

### Shell and Script Usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from fastpix-python python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "fastpix-python",
# ]
# ///

from fastpix_python import Fastpix, models

sdk = Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where `script.py` can be replaced with the actual file name.

### IDE Support

#### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)

### Initialization

Initialize the FastPix SDK with your credentials:

```python
from fastpix_python import Fastpix, models

fastpix = Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
)
```

Or using environment variables:

```python
import os
from fastpix_python import Fastpix, models

fastpix = Fastpix(
    security=models.Security(
        username=os.getenv("FASTPIX_USERNAME"),  # Your Access Token
        password=os.getenv("FASTPIX_PASSWORD"),  # Your Secret Key
    ),
)
```

## Example Usage

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

    res = fastpix.input_video.create_media(
        inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.io/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "key1": "value1",
        },
    )

    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))
```

## Available Resources and Operations

Comprehensive Python SDK for FastPix platform integration with full API coverage.

### Media API

Upload, manage, and transform video content with comprehensive media management capabilities.

For detailed documentation, see [FastPix Video on Demand Overview](https://docs.fastpix.io/docs/video-on-demand-overview).

#### Input Video
- [Create from URL](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/inputvideo/README.md#create_from_url) - Upload video content from external URL
- [Upload from Device](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/inputvideo/README.md#direct_upload) - Upload video files directly from device

#### Manage Videos
- [List All Media](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#list_media) - Retrieve complete list of all media files
- [Get Media by ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/mediasdk/README.md#get) - Get detailed information for specific media
- [Update Media](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#update_media) - Modify media metadata and settings
- [Delete Media](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/videos/README.md#delete) - Remove media files from library
- [Cancel Upload](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#cancel_upload) - Stop ongoing media upload process
- [Get Input Info](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#retrievemediainputinfo) - Retrieve detailed input information
- [Get Summary](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#get_summary) - Retrieve AI-generated video summary
- [List Uploads](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#list_unused_upload_urls) - Get all available upload URLs

#### Playback
- [Create Playback ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playback/README.md#create) - Generate secure playback identifier
- [Delete Playback ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playback/README.md#delete) - Remove playback access
- [Get Playback ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playback/README.md#get_by_id) - Retrieve playback configuration details
- [List Playback IDs](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playback/README.md#list_playback_ids) - Get all playback IDs for a media
- [Update Domain Restrictions](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playback/README.md#update_domain_restrictions) - Configure domain-based access control
- [Update User-Agent Restrictions](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playback/README.md#update_user_agent_restrictions) - Configure user-agent-based access control

#### Playlist
- [Create Playlist](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlist/README.md#create) - Create new video playlist
- [List Playlists](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlists/README.md#get_all) - Get all available playlists
- [Get Playlist](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlist/README.md#get) - Retrieve specific playlist details
- [Update Playlist](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlists/README.md#update) - Modify playlist settings and metadata
- [Delete Playlist](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlist/README.md#delete) - Remove playlist from library
- [Add Media](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlist/README.md#add_media) - Add media items to playlist
- [Reorder Media](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlists/README.md#change_media_order) - Change order of media in playlist
- [Remove Media](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/playlist/README.md#delete_media) - Remove media from playlist

#### Signing Keys
- [Create Key](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/signingkeys/README.md#create) - Generate new signing key pair
- [List Keys](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/signingkeys/README.md#list_signing_keys) - Get all available signing keys
- [Delete Key](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/signingkeys/README.md#delete_signing_key) - Remove signing key from system
- [Get Key](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/signingkeys/README.md#get_signing_key_by_id) - Retrieve specific signing key details

#### DRM Configurations
- [List DRM Configs](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/drmconfigurations/README.md#list) - Get all DRM configuration options
- [Get DRM Config](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/drmconfigurations/README.md#get_by_id) - Retrieve specific DRM configuration

### Live API

Stream, manage, and transform live video content with real-time broadcasting capabilities.

For detailed documentation, see [FastPix Live Stream Overview](https://docs.fastpix.io/docs/live-stream-overview).

#### Start Live Stream
- [Create Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/startlivestream/README.md#create_stream) - Initialize new live streaming session with DVR mode support

#### Manage Live Stream
- [List Streams](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/livestreams/README.md#list) - Retrieve all active live streams
- [Get Viewer Count](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managelivestream/README.md#get_viewer_count) - Get real-time viewer statistics
- [Get Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/livestreams/README.md#get_by_id) - Retrieve detailed stream information
- [Delete Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/streams/README.md#delete) - Terminate and remove live stream
- [Update Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managelivestream/README.md#update) - Modify stream settings and configuration
- [Enable Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/livestreams/README.md#enable) - Activate live streaming
- [Disable Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/livestreams/README.md#disable) - Pause live streaming
- [Complete Stream](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managelivestream/README.md#complete) - Finalize and archive stream
- [List Live Clips](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/mediasdk/README.md#list_live_clips) - Get all clips of a live stream

#### Live Playback
- [Create Playback ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/liveplayback/README.md#create_playback_id) - Generate secure live playback access
- [Delete Playback ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/liveplayback/README.md#delete_playback_id) - Revoke live playback access
- [Get Playback ID](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/liveplayback/README.md#get_playback_id_details) - Retrieve live playback configuration

#### Simulcast Stream
- [Create Simulcast](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/simulcaststream/README.md#create) - Set up multi-platform streaming
- [Delete Simulcast](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/simulcast/README.md#delete) - Remove simulcast configuration
- [Get Simulcast](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/simulcaststream/README.md#get_simulcast) - Retrieve simulcast settings
- [Update Simulcast](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/simulcaststream/README.md#update_simulcast) - Modify simulcast parameters

### Video Data API

Monitor video performance and quality with comprehensive analytics and real-time metrics.

For detailed documentation, see [FastPix Video Data Overview](https://docs.fastpix.io/docs/video-data-overview).

#### Metrics
- [List Breakdown Values](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/metrics/README.md#list_breakdown_values) - Get detailed breakdown of metrics by dimension
- [List Overall Values](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/metrics/README.md#list_overall_values) - Get aggregated metric values across all content
- [Get Timeseries Data](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/metrics/README.md#get_timeseries_data) - Retrieve time-based metric trends and patterns
- [List Comparison Values](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/metrics/README.md#list_comparison_values) - Compare metrics across different time periods

#### Views
- [List Video Views](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/viewssdk/README.md#list_video_views) - Get comprehensive list of video viewing sessions
- [Get View Details](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/viewssdk/README.md#get_video_view_details) - Retrieve detailed information about specific video views
- [List Top Content](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/viewssdk/README.md#list_by_top_content) - Find your most popular and engaging content

#### Dimensions
- [List Dimensions](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/dimensions/README.md#list) - Get available data dimensions for filtering and analysis
- [List Filter Values](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/dimensions/README.md#list_filter_values) - Get specific values for a particular dimension

#### Errors
- [List Errors](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/errors/README.md#list) - Retrieve playback errors and issues

### Transformations

Transform and enhance your video content with powerful AI and editing capabilities.

#### In-Video AI Features

Enhance video content with AI-powered features including moderation, summarization, and intelligent categorization.

- [Update Summary](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/invideoaifeatures/README.md#update_summary) - Create AI-generated video summaries
- [Create Chapters](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/invideoai/README.md#update_chapters) - Automatically generate video chapter markers
- [Extract Entities](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/invideoaifeatures/README.md#update_named_entities) - Identify and extract named entities from content
- [Enable Moderation](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/invideoaifeatures/README.md#update_moderation) - Activate content moderation and safety checks

#### Media Clips

- [Get Media Clips](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/videos/README.md#list_clips) - Retrieve all clips associated with a source media

#### Subtitles

- [Generate Subtitles](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#generate_subtitles) - Create automatic subtitles for media

#### Media Tracks

- [Add Track](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/mediatracks/README.md#add) - Add audio or subtitle tracks to media
- [Update Track](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/mediatracks/README.md#update) - Modify existing audio or subtitle tracks
- [Delete Track](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/videos/README.md#delete_track) - Remove audio or subtitle tracks

#### Access Control

- [Update Source Access](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#update_source_access) - Control access permissions for media source

#### Format Support

- [Update MP4 Support](https://github.com/FastPix/fastpix-python/blob/feature/fixed-missing-parameters/docs/sdks/managevideos/README.md#update_mp4_support) - Configure MP4 download capabilities

<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:

```python
import os
import json

from fastpix_python import Fastpix, models
from fastpix_python.utils import BackoffStrategy, RetryConfig

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(
        inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.io/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "key1": "value1",
        },
        retries=RetryConfig(
            "backoff",
            BackoffStrategy(1, 50, 1.1, 100),
            False
        ),
    )

    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))
```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:

```python
import os
import json

from fastpix_python import Fastpix, models
from fastpix_python.utils import BackoffStrategy, RetryConfig

with Fastpix(
    retry_config=RetryConfig(
        "backoff",
        BackoffStrategy(1, 50, 1.1, 100),
        False
    ),
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(
        inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.io/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "key1": "value1",
        },
    )

    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))
```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`FastpixError`](./src/fastpix_python/errors/fastpixerror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                            |
| ------------------ | ---------------- | ------------------------------------------------------ |
| `err.message`      | `str`            | Error message                                          |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                     |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                  |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned. |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                      |

### Example

```python
import os
import json

from fastpix_python import Fastpix, errors, models

with Fastpix(
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:
    try:
        res = fastpix.input_video.create_media(
            inputs=[
                {
                    "type": "video",
                    "url": "https://static.fastpix.io/fp-sample-video.mp4",
                },
            ],
            access_policy="public",
            metadata={
                "key1": "value1",
            },
        )

        print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))
    except errors.FastpixError as e:
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)
```

### Error Classes
**Primary error:**
* [`FastpixError`](./src/fastpix_python/errors/fastpixerror.py): The base class for HTTP error responses.

<details><summary>Less common errors (5)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`FastpixError`](./src/fastpix_python/errors/fastpixerror.py)**:
* [`ResponseValidationError`](./src/fastpix_python/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:

```python
import os
import json

from fastpix_python import Fastpix, models

with Fastpix(
    server_url="https://api.fastpix.io/v1/",
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(
        inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.io/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "key1": "value1",
        },
    )

    print(json.dumps(res.model_dump(mode="json", by_alias=True), indent=2))
```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library. In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.

Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.

This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this SDK makes as follows:

```python
from fastpix_python import Fastpix, models
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Fastpix(
    client=http_client,
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
)
```

Or you could wrap the client with your own custom logic:

```python
from fastpix_python import Fastpix, models
from fastpix_python.httpclient import AsyncHttpClient
import httpx
from typing import Union, Optional, Any

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Fastpix(
    async_client=CustomClient(httpx.AsyncClient()),
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
)
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.

> [!WARNING]
> Beware that debug logging will reveal secrets, like API tokens in headers, in log messages printed to a console or files. It's recommended to use this feature only during local development and not in production.

```python
from fastpix_python import Fastpix, models
import logging

logging.basicConfig(level=logging.DEBUG)
s = Fastpix(
    debug_logger=logging.getLogger("fastpix_python"),
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
)
```

You can also enable a default debug logger by setting an environment variable `FASTPIX_DEBUG` to true.
<!-- End Debugging [debug] -->

# Development

This Python SDK is programmatically generated from our API specifications. Any manual modifications to internal files will be overwritten during subsequent generation cycles. 

We value community contributions and feedback. Feel free to submit pull requests or open issues with your suggestions, and we'll do our best to include them in future releases.

## Detailed Usage

For comprehensive understanding of each API's functionality, including detailed request and response specifications, parameter descriptions, and additional examples, please refer to the [FastPix API Reference](https://docs.fastpix.io/reference/signingkeys-overview).

The API reference offers complete documentation for all available endpoints and features, enabling developers to integrate and leverage FastPix APIs effectively.
