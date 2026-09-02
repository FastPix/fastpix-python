# Changelog

All notable changes to this project will be documented in this file.


---

## [1.2.0]

### Breaking

- **Media `duration` is now a float (seconds)** instead of an `"HH:MM:SS"`
  string, matching the updated API. Affects the media responses returned by
  `get_media`, `list_media`, `list_live_clips`, `updated_media`,
  `updated_source_access`, `updated_mp4_support`, `get_media_clips`, and the
  playlist `mediaList` items.

### Added

- **`enable_recording`** on live stream creation (`inputMediaSettings`,
  defaults to `true`) — controls whether the livestream is recorded to a VOD
  asset.
- **`access_restrictions`** (domain and user-agent allow/deny policies) on
  live playback ID create/get and on live stream `playbackSettings`.
- **`update_live_stream_domain_restrictions()` /
  `update_live_stream_user_agent_restrictions()`** (and `_async` variants) —
  `PATCH /live/streams/{streamId}/playback-ids/{playbackId}/domains` and
  `/user-agents`.
- **Async variants** for the on-demand `update_domain_restrictions` and
  `update_user_agent_restrictions`, which were sync-only.
- **Model contract test suite** (`tests/test_models.py`).

### Fixed

- **Async error handling never raised** — `_raise_for_status_async` was called
  without `await` across the async methods, so failed responses returned
  `None` instead of raising typed errors.
- **Live playback ID create/get return annotations** corrected to the actual
  `PlaybackIDSuccessResponse` envelope.

---

## [1.1.5]

### Fixed

- **`import fastpix_python` crashed on Python 3.9–3.13** — `playback.py` used
  `List` without importing it, raising `NameError` at import time. Affected
  1.1.3 and 1.1.4; masked on 3.14 by lazy annotations.
- **Playback restriction methods had invalid return annotations** — corrected to
  the actual `...ResponseBody` types.
- **`models.DefaultError` was unregistered**, so the playback error path failed
  to resolve.
- **`fastpix.errors.list_errors` was unreachable** — `errors.py` was shadowed by
  the `errors/` exception package; the resource module is now `errors_sdk.py`.
- **`mp4Support` is a list of renditions**, not a string — deserialization
  failed on `get_media`, `list_media`, `updated_media`, `updated_source_access`,
  `updated_mp4Support`, `list_live_clips`.
- **`updated_mp4_support()` sent an empty body** when `mp4_support` was omitted
  (`400`). Now required.
- **`sourceResolution` rejected bare numeric values** (`"1080"`, `"720"`). Both
  forms are accepted, and the `360` tier was added.
- **`maxDuration` and `resolution` rejected uncapped resources** — `maxDuration`
  is now `0` or `60`–`28800`, and `CreatePlaybackId.resolution` is nullable.
- **Version metadata disagreed** — `setup.py` `1.1.3` vs `1.1.5` elsewhere.

### Added

- **`get_summary()` / `get_summary_async()`** — `GET /on-demand/{mediaId}/summary`.
- **Track `title`** on the track models and on `update_media_track()` /
  `generate_subtitle_track()`.
- **`optimize_audio`** on the live-clip response.

### Removed

- **`models.MediaMp4Support`** — use `models.MediaMp4SupportEntry`.
- **`update_media_track()` no longer accepts `url`** — raises `TypeError`.
- **Dead `ValidationErrorResponseError` export** — it pointed at a module that
  was never generated, so importing it always raised `ImportError`.

### Documentation

- MP4 model pages point at `MediaMp4SupportEntry`; `mp4_support` marked required.
- Doc links migrated to the restructured site;
  `video.media.subtitle.generated.ready` → `video.media.subtitle.generated`.

> The spec marks `mp4Support` on the update-mp4Support body both `required` and
> `default: capped_4k`, which conflict. The SDK implements `required`.

---

## [1.1.4]

### Changed
- **SDK version bump: `1.1.3` → `1.1.4`.**
  A maintenance release that aligns the SDK's internal version identifiers and
  applies behaviour-preserving code-quality cleanup. It contains no functional,
  API, or behavioural changes and is fully backward compatible with `1.1.3`.

  Updated identifiers:
  - `__version__` / package version — now reports `1.1.4` (the internal
    identifiers were previously lagging at `1.0.1`; they are now aligned with
    the package version).
  - `User-Agent` header — outbound requests now identify as
    `fastpix-sdk/python 1.1.4`.

  Maintainability:
  - Internal static-analysis (SonarQube) cleanup across the SDK, samples, and
    test harness — bundled request-builder parameters, shared response-handling
    helpers, duplicated string literals extracted into constants, and nested
    conditionals merged. No public-surface impact.

### Compatibility
- No changes to public types, method signatures, request/response models,
  default server URLs, hooks, or retry logic.
- No action required for existing integrations — upgrade the dependency and
  re-run `pip install --upgrade fastpix_python`.

---

## [1.1.3]

### ⚠️ Important — FastPix is migrating from `.io` to `.com`

All FastPix-owned hosts, API endpoints, and documentation links are being moved from the `.io` TLD to `.com`. The `.io` hosts continue to serve traffic during the transition window, **but they are slated for deprecation soon** — please update any hard-coded references in your application as part of your next deploy.

| Old (`.io`) | New (`.com`) |
|---|---|
| `api.fastpix.io` | `api.fastpix.com` |
| `stream.fastpix.io` | `stream.fastpix.com` |
| `images.fastpix.io` | `images.fastpix.com` |
| `dashboard.fastpix.io` | `dashboard.fastpix.com` |
| `www.fastpix.io` | `www.fastpix.com` |
| `docs.fastpix.io/...` | `fastpix.com/docs/...` |

What this means for users of `fastpix_python`:

- **If you rely on SDK defaults**, no code change is required. The default `server_url` in this release points at `https://api.fastpix.com/v1/`, so bumping to `1.1.3` and re-running `pip install --upgrade fastpix_python` is enough.
- **If you have an explicit `server_url` override** (e.g. `Fastpix(server_url="https://api.fastpix.io/v1/")`), change it to `https://api.fastpix.com/v1/`.
- **If your application code references FastPix asset URLs directly** — playback URLs (`stream.fastpix.io/...`), image CDN (`images.fastpix.io/...`), dashboard deep links, or doc links in your own README — update them to the `.com` equivalents before the `.io` hosts are decommissioned.
- We strongly recommend upgrading **every official FastPix SDK** in your stack to its latest release as part of the same change — every SDK is being rolled out with the same migration.

### Changed

- All README, USAGE, and per-SDK documentation pages updated end-to-end from `dashboard.fastpix.io` / `docs.fastpix.io/...` to `dashboard.fastpix.com` / `fastpix.com/docs/...` so every link in the package points at the post-migration host structure.
- Reference links (Homepage, Dashboard, API Reference, "Detailed Usage") repointed to `fastpix.com`.
- Sample playback URLs in code examples updated from `stream.fastpix.io` to `stream.fastpix.com`.

### Docs

- 173 documentation links across 70 markdown files verified reachable after migration; zero `fastpix.com/docs/*` URLs are broken. The handful of remaining broken links in the link-check report are expired example assets / placeholder thumbnails inside API response snippets, not navigation targets.

---

## [1.1.2]

### Fixed
- Fixed `events` field in `get_video_view_details` response returning empty objects — added `validation_alias` mappings for abbreviated API keys (`pt`, `e`, `vt`, `d`) to full camelCase names (`playerPlayheadTime`, `eventName`, `viewerTime`, `eventDetails`)
- Fixed `eventDetails` nested object returning raw abbreviated keys — introduced `EventDetails` model with proper field mappings (`host`→`hostName`, `txt`→`text`, `c`→`code`, `err`→`error`, `t`→`type`, `u`→`url`, `br`→`bitrate`, `h`→`height`, `fps`→`fps`, `cd`→`codec`, `w`→`width`)
- Fixed `fpSDK` and `fpSDKVersion` fields missing from response — added `AliasChoices` to accept both `fpSdk` and `fpSDK` variants from the API
- Fixed `experimentName` null value being excluded from serialized output
- Added missing `custom` field to `Views` model to capture user-defined metadata object

### Improved
- Response models for video view details now fully conform to the OpenAPI spec field names

---

## [1.1.1]

### Fixed
- Fixed SDK import paths in `_sub_sdk_map` - changed from `Fastpix.*` to `fastpix_python.*` to resolve `ModuleNotFoundError` for end users
- Fixed all documentation examples - removed unnecessary `sys.path.append()` statements
- Updated method name from `create_from_url` to `create_media` in examples

### Improved
- All SDK documentation examples now work out-of-the-box without workarounds
- Consistent import statements across all documentation files

## [1.1.0]

### Fixed
- Fixed missing parameters in multiple API methods.

### Improved
- Improved overall developer experience through more accurate typings.

## [1.0.3]

### Fixed
- Fixed pyproject.toml file Packaging Issue


## [1.0.2]

### Fixed
- Fixed Packaging Issue


## [1.0.1]

### Fixed
- Fixed all error handling links in README.md documentation
  - Corrected typos in file paths (e.g., `fFastpix` → `Fastpix`)
  - Updated filenames to match actual error class files (added missing underscores)
  - Fixed 23 error class links to properly redirect to correct files
  - Verified all links now point to existing files in `src/Fastpix/errors/` directory

## [1.0.0]

### Added
- Complete API coverage for Media, Live Streaming, Video Data, and Signing Keys
- Python 3.9+ support with async/await patterns and type hints
- Media upload, management, and processing capabilities
- Live streaming with simulcasting support
- Video analytics and performance tracking
- Cryptographic signing keys for secure authentication
- In-video AI processing features
- DRM configuration and management
- Playlist creation and management
- Comprehensive error handling with specific exception types
- Both sync and async client implementations
- Built-in retry mechanisms and timeout handling

### Changed
- Reorganized package structure for better maintainability
- Updated dependencies to modern Python packages (httpx, pydantic, httpcore)
- Improved API design with better error handling
- Enhanced documentation and examples

### Fixed
- Improved error handling with specific exception types
- Fixed type annotation issues for better IDE support
- Ensured consistent API patterns across modules

---

## [0.1.8]

### Added
- Enhanced README documentation with comprehensive usage examples
- Improved project setup and installation instructions

### Changed
- Updated version number to reflect latest improvements
- Restructured documentation for better user experience
- Enhanced code examples and API usage guides

---

## [0.1.7]

### Added
- New base URL configuration system for better API connectivity
- Support for different API environments (production, staging, development)

### Changed
- Updated base URL configuration for improved API endpoint resolution
- Enhanced connection stability and reliability
- Improved error handling for connection issues

---

## [0.1.6]

### Added
- Project URL management system for better package distribution
- Enhanced package metadata and configuration

### Changed
- Updated project URLs in configuration files for better package identification
- Improved package metadata and distribution information
- Enhanced project discoverability and documentation links

---

## [0.1.5]

### Added
- Comprehensive version tracking and file management system
- Automated version control and release management
- Initial project structure and configuration framework

### Changed
- Updated version number and project configuration
- Improved project organization and file structure
- Enhanced build and deployment processes

---

## [0.1.4]

### Added
- New package naming convention for better identification
- Enhanced package metadata and distribution information

### Changed
- Changed package name for better identification and distribution
- Updated package metadata and configuration
- Improved package discoverability and installation process

---

## [0.1.3]

### Added
- Version management improvements
- Enhanced configuration system

### Changed
- Updated version number to reflect latest changes
- Improved project configuration and build processes
- Enhanced package metadata and dependencies

---

## [0.1.2]

### Added
- Comprehensive documentation link validation system
- Enhanced workflow automation and CI/CD pipeline

### Fixed
- Corrected redirection links in README documentation
- Fixed broken documentation links for better user experience
- Resolved navigation issues in project documentation

### Changed
- Updated workflow configuration and processes
- Improved project automation and deployment pipeline
- Enhanced documentation structure and organization

---

## [0.1.1]

### Changed
- Updated codebase with consistent naming conventions
- Added comprehensive package description

### Fixed
- Resolved naming convention inconsistencies

---

## [0.1.0]

### Added
- Initial release of FastPix Python SDK
- Sync and async client support
- Media API integration with upload, management, and processing
- Playback ID management for media files
- Media operations (list, get, update, delete)
- Presigned URL generation for video uploads
- Livestream API integration
- Livestream management (create, update, delete)
- Playback ID management for livestreams
- Simulcast configuration for livestreams