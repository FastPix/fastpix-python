# FastPix Python SDK

[![PyPI version](https://img.shields.io/pypi/v/fastpix-python)](https://pypi.org/project/fastpix-python/)
[![PyPI downloads](https://img.shields.io/pypi/dm/fastpix-python)](https://pypi.org/project/fastpix-python/)
[![license](https://img.shields.io/pypi/l/fastpix-python)](https://github.com/FastPix/fastpix-python/blob/main/LICENSE)
[![Python 3.9.2+](https://img.shields.io/badge/python-3.9.2%2B-3776AB?logo=python&logoColor=white)](https://pypi.org/project/fastpix-python/)

A robust, type-safe Python SDK designed for seamless integration with the FastPix API platform.

The FastPix Python SDK is a type-safe Python client for the FastPix video API. From any Python application you can upload and manage videos, run live streams and simulcasts, create and secure playback IDs, manage playlists and signing keys, pull video analytics (views, metrics, dimensions, and errors), and drive in-video AI features such as subtitles, chapters, summaries, and content moderation.

**Supported Python:** 3.9.2 and later
**Package:** `fastpix-python`
**Authentication:** HTTP Basic Authentication
**Clients:** Synchronous and asynchronous

📖 **Docs:** https://fastpix.com/docs/language-sdks/python-sdk &nbsp;·&nbsp; 🚀 **Free account:** https://dashboard.fastpix.com

<br />

## Start here

If you are using the FastPix Python SDK for the first time, follow these steps in order:

1. [Check your Python version](#1-check-your-python-version)
2. [Create a Python project](#2-create-a-python-project)
3. [Install the SDK](#3-install-the-sdk)
4. [Verify the installation](#4-verify-the-installation)
5. [Configure authentication](#5-configure-authentication)
6. [Initialize the FastPix client](#6-initialize-the-fastpix-client)
7. [Make your first API request](#7-make-your-first-api-request)
8. [Verify the API response](#8-verify-the-api-response)
9. [Understand the media workflow](#9-understand-the-media-workflow)

Do not skip the verification step. If installation or authentication fails, troubleshoot that problem before continuing to the next API operation.

---

### Before you begin

 To use the SDK make sure you have:

- Python 3.9.2 or later.
- Internet access.
- A FastPix account.
- A FastPix Access Token.
- A FastPix Secret Key.

FastPix uses Basic Authentication:

| SDK value | FastPix credential |
|---|---|
| `username` | Access Token |
| `password` | Secret Key |

You can obtain your credentials from the FastPix Dashboard. Follow the steps in the [Authentication with Basic Auth](https://fastpix.com/docs/getting-started/activate-your-account#authentication-format) guide to obtain your credentials.

---

## 1. Check your Python version

```bash
python3 --version
```

Output is similar to:

```text
Python 3.9.2
```

or a later version.

If your Python version is earlier than 3.9.2, install a supported version before continuing.

## 2. Create a Python project

a. Create a new directory for your FastPix application:

```bash
mkdir fastpix-python-demo
cd fastpix-python-demo
```

b. Create a virtual environment:

```bash
python3 -m venv .venv
```

c. Activate the virtual environment.

### macOS and Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

d. Verify that the virtual environment is active:

```bash
python --version
```

## 3. Install the SDK

### Using pip

```bash
pip install fastpix-python
```

### Using uv

```bash
uv add fastpix-python
```

### Using Poetry

```bash
poetry add fastpix-python
```

## 4. Verify the installation

Before making an API request, verify that Python can import the SDK:

```bash
python -c "import fastpix_python; print('FastPix SDK installed successfully')"
```

Output is similar to:

```text
FastPix SDK installed successfully
```

If this command fails, do not continue to API calls.

Check:

- The virtual environment is active.
- `fastpix-python` is installed.
- The Python interpreter belongs to the expected virtual environment.
- Your Python version is supported.

You can verify the installed package with:

```bash
pip show fastpix-python
```

## 5. Configure authentication

FastPix uses Basic Authentication.

Set the Access Token and Secret Key as environment variables:

### macOS and Linux

```bash
export FASTPIX_USERNAME="<YOUR_ACCESS_TOKEN>"
export FASTPIX_PASSWORD="<YOUR_SECRET_KEY>"
```

### Windows PowerShell

```powershell
$env:FASTPIX_USERNAME="<YOUR_ACCESS_TOKEN>"
$env:FASTPIX_PASSWORD="<YOUR_SECRET_KEY>"
```

The SDK maps these variables as follows:

```text
FASTPIX_USERNAME → Access Token
FASTPIX_PASSWORD → Secret Key
```

### Verify the credentials are set

Do not print the actual credential values.

Instead, run:

```bash
python -c "import os; print('Access Token:', 'set' if os.getenv('FASTPIX_USERNAME') else 'missing'); print('Secret Key:', 'set' if os.getenv('FASTPIX_PASSWORD') else 'missing')"
```

Output is similar to:

```text
Access Token: set
Secret Key: set
```

### Security

Never:

- Commit credentials to Git.
- Put credentials directly into source code.
- Include credentials in screenshots, logs, or bug reports.
- Print authentication headers during debugging in production.

Use environment variables or a secure credential-management system.

## 6. Initialize the FastPix client

a. Create a file named `example.py`:

```python
import os

from fastpix_python import Fastpix, models

fastpix = Fastpix(
    security=models.Security(
        username=os.getenv("FASTPIX_USERNAME"),
        password=os.getenv("FASTPIX_PASSWORD"),
    ),
)

print("FastPix client initialized")
```

b. Run:

```bash
python example.py
```

Output is similar to:

```text
FastPix client initialized
```

### What this code does

`Fastpix` is the top-level SDK client.

`models.Security` contains the credentials used to authenticate API requests.

The SDK client does not make an API request simply because it is initialized.

An API request occurs when you call an operation such as:

```python
fastpix.input_video.create_media(...)
```

---

## 7. Make your first API request

The easiest way to verify the complete integration is to create media from a publicly accessible video URL.

FastPix provides a sample video URL:

```text
https://static.fastpix.com/fp-sample-video.mp4
```

a. Replace the contents of `example.py` with:

```python
import json
import os

from fastpix_python import Fastpix, models

with Fastpix(
    security=models.Security(
        username=os.getenv("FASTPIX_USERNAME"),
        password=os.getenv("FASTPIX_PASSWORD"),
    ),
) as fastpix:
    response = fastpix.input_video.create_media(
        inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.com/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "source": "fastpix-python-demo",
        },
    )
    print(
        json.dumps(
            response.model_dump(
                mode="json",
                by_alias=True,
                exclude_unset=True,
            ),
            indent=2,
        )
    )
```

b. Save the file and run:

```bash
python example.py
```

---

## 8. Verify the API response

A successful request returns a response containing a media ID.

The response has the following general structure:

```json
{
  "success": true,
  "data": {
    "id": "..."
  }
}
```

The value of:

```text
data.id
```

is the unique ID assigned to the media.

### Save the media ID

You will need the media ID for subsequent media operations.

For example:

```text
MEDIA_ID=<value returned in data.id>
```

Do not confuse a `media_id` with a `playback_id`.

They identify different resources and are used for different operations.

## 9. Understand the media workflow

Creating media is usually the first operation in an on-demand video workflow.

The basic workflow is:

<Image alt="FastPix media workflow: create media returns a media ID, retrieve the media, check status until ready, create a playback ID, then play the video." border={false} src="https://static.fastpix.com/media-workflow.png" />

The media ID is the identifier you carry from one operation to the next.

A playback ID is created separately when you need playback access.

---

## Common tasks

## Create media

**Goal:** Create a FastPix media asset from a video URL.

**SDK method:**

```python
fastpix.input_video.create_media(...)
```

**Required information:**

- Video URL.
- Access policy.

**Example:**

```python
response = fastpix.input_video.create_media(
    inputs=[
        {
            "type": "video",
            "url": "https://static.fastpix.com/fp-sample-video.mp4",
        },
    ],
    access_policy="public",
)
```

**Result:**

Save the media ID from:

```text
response.data.id
```

## Next steps

After verifying your integration, you can use the SDK to:

- **Manage media** — list, retrieve, update, and delete media.
- **Create playback IDs** — generate playback access for your media.
- **Manage live streams** — create and manage live streaming sessions.
- **Create playlists** — organize media into playlists.
- **Manage signing keys** — create and manage keys for secure playback.
- **Analyze video performance** — retrieve metrics, views, dimensions, and errors.
- **Use in-video AI** — generate subtitles, summaries, chapters, and named entities.
- **Manage media tracks** — add, update, and delete audio or subtitle tracks.

See [Available Resources and Operations](#available-resources-and-operations) for the complete list.

<br />

## Available Resources and Operations

Comprehensive Python SDK for FastPix platform integration with full API coverage.

### Media API

Upload, manage, and transform video content with comprehensive media management capabilities.

For detailed documentation, see [FastPix Video on Demand Overview](https://fastpix.com/docs/video-on-demand-api/overview).

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

<br />

### Live API

Stream, manage, and transform live video content with real-time broadcasting capabilities.

For detailed documentation, see [FastPix Live Stream Overview](https://fastpix.com/docs/live-stream-api/overview).

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

<br />

### Video Data API

Monitor video performance and quality with comprehensive analytics and real-time metrics.

For detailed documentation, see [FastPix Video Data Overview](https://fastpix.com/docs/video-data-api/overview).

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

<br />

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

<br />

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
                "url": "https://static.fastpix.com/fp-sample-video.mp4",
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

    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

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
                "url": "https://static.fastpix.com/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "key1": "value1",
        },
    )

    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```
<!-- End Retries [retries] -->

<br />

## Error Handling

[`FastpixError`](./fastpix_python/errors/fastpixerror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                            |
| ------------------ | ---------------- | ------------------------------------------------------ |
| `err.message`      | `str`            | Error message                                          |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                     |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                  |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned. |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                      |

<br />

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
                    "url": "https://static.fastpix.com/fp-sample-video.mp4",
                },
            ],
            access_policy="public",
            metadata={
                "key1": "value1",
            },
        )

        print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))
    except errors.FastpixError as e:
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)
```

### Error Classes

**Primary error:**
* [`FastpixError`](./fastpix_python/errors/fastpixerror.py): The base class for HTTP error responses.

<details><summary>Less common errors (5)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`FastpixError`](./fastpix_python/errors/fastpixerror.py)**:
* [`ResponseValidationError`](./fastpix_python/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>
<!-- End Error Handling [errors] -->

<br />

## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:

```python
import os
import json

from fastpix_python import Fastpix, models


with Fastpix(
    server_url="https://api.fastpix.com/v1/",
    security=models.Security(
        username="your-access-token",
        password="your-secret-key",
    ),
) as fastpix:

    res = fastpix.input_video.create_media(
        inputs=[
            {
                "type": "video",
                "url": "https://static.fastpix.com/fp-sample-video.mp4",
            },
        ],
        access_policy="public",
        metadata={
            "key1": "value1",
        },
    )

    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2))

```
<!-- End Server Selection [server] -->

<br />

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

<br />

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

## FAQ

**How do I install the FastPix Python SDK?**
Run `pip install fastpix-python` (or `uv add fastpix-python` / `poetry add fastpix-python`). See [Start here](#start-here).

**How do I authenticate the SDK?**
FastPix uses Basic Auth: pass your access token as `username` and your secret key as `password` in `models.Security` when constructing the client. See [Before you begin](#before-you-begin).

**How do I upload a video in Python?**
Create media from a URL or a direct upload through `fastpix.input_video`, for example `fastpix.input_video.create_media(...)`. See [Create media](#create-media) and [Available Resources and Operations](#available-resources-and-operations).

**Does the SDK support async?**
Yes - it provides both synchronous and asynchronous clients. See [Custom HTTP Client](#custom-http-client).

**How do I start a live stream?**
Use the Live API resources to create and manage streams, simulcasts, and live playback IDs. See [Available Resources and Operations](#available-resources-and-operations).

**How do I get video analytics and metrics in Python?**
The Video Data API exposes metrics, views, dimensions, and errors for quality-of-experience monitoring. See [Available Resources and Operations](#available-resources-and-operations).

**How do I handle API errors?**
Wrap calls in try/except and catch `errors.FastpixError`, which exposes the message, status code, headers, and body. See [Error Handling](#error-handling).

**How do I configure automatic retries?**
Pass a `RetryConfig` per call or at client initialization to control the backoff strategy. See [Retries](#retries).

**How do I use a custom HTTP client, proxy, or timeout?**
Pass your own `httpx` client (sync or async) to configure timeouts, proxies, and custom headers. See [Custom HTTP Client](#custom-http-client).

**How do I enable debug logging?**
Pass a logger to the client or set the `FASTPIX_DEBUG` environment variable. See [Debugging](#debugging).

**Which Python versions are supported?**
Python 3.9.2 and above. See [Before you begin](#before-you-begin).

<br />

## Which FastPix SDK should I use?

FastPix publishes a server SDK for every major backend language, each generated from the same API specification:

| Language | Repo | Install |
|---|---|---|
| **Python** (this repo) | [fastpix-python](https://github.com/FastPix/fastpix-python) | `pip install fastpix-python` |
| Node.js / TypeScript | [node-sdk](https://github.com/FastPix/node-sdk) | `npm install @fastpix/fastpix-node` |
| PHP | [fastpix-php](https://github.com/FastPix/fastpix-php) | `composer require fastpix/sdk` |
| Go | [fastpix-go](https://github.com/FastPix/fastpix-go) | `go get github.com/FastPix/fastpix-go` |
| Java | [fastpix-java](https://github.com/FastPix/fastpix-java) | `io.fastpix:sdk` (Maven/Gradle) |
| C# / .NET | [fastpix-sdk-csharp](https://github.com/FastPix/fastpix-sdk-csharp) | `dotnet add package Fastpix` |
| Ruby | [fastpix-ruby](https://github.com/FastPix/fastpix-ruby) | `gem install fastpixapi` |

To upload and play the media these SDKs create, use the FastPix browser libraries: [web-uploads-sdk](https://github.com/FastPix/web-uploads-sdk), [react-web-uploader](https://github.com/FastPix/react-web-uploader), and [web-player-component](https://github.com/FastPix/web-player-component). Browse everything in the [FastPix organization](https://github.com/orgs/FastPix/repositories).

<br />

## Development

This Python SDK is programmatically generated from our API specifications. Any manual modifications to internal files will be overwritten during subsequent generation cycles.

We value community contributions and feedback. Feel free to submit pull requests or open issues with your suggestions, and we'll do our best to include them in future releases.

## Detailed Usage

For comprehensive understanding of each API's functionality, including detailed request and response specifications, parameter descriptions, and additional examples, please refer to the [FastPix API Reference](https://fastpix.com/docs/product-os-api/overview).

The API reference offers complete documentation for all available endpoints and features, enabling developers to integrate and leverage FastPix APIs effectively.
