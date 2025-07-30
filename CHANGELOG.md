# Changelog

All notable changes to this project will be documented in this file.

## [0.1.8]
- Version update and ReadMe update

## [0.1.7]
- Updated the Base URL

## [0.1.6]
- Updated the project URLs

## [0.1.5]
- Updated the version and added the file

## [0.1.4]
- Changed package name

## [0.1.3]
- Version update

## [0.1.2]
- workflow update

## [0.1.1]

- Long description is added.

## [0.1.0]

### Features:

- **Sync and Async SDK**: Users can now choose between synchronous and asynchronous SDKs based on their requirements.
- **Media API Integration**: Full integration with FastPix Media APIs, enabling:
  - **Media Upload**: Users can upload and manage video content seamlessly.
  - **Manage Playback IDs**: Users can generate and manage playback IDs for video content.
    - **Create Playback ID**: Generate a playback ID for a media file.
    - **Delete Playback ID**: Remove a playback ID for a media file.
  - **Media Listing and Deletion**: List and delete media files efficiently.
    - **Get All Media**: Retrieve a list of all media files.
    - **Get Media by ID**: Retrieve details of a specific media file using its media ID.
    - **Update Media**: Update metadata or settings for a specific media file.
    - **Create Pull Video**: Initiate a pull to import a video from an external source.
    - **Get Media Info**: Retrieve detailed information about a media file.
     - **Get Presigned URL**: Create a pre-signed URL that users can use to upload video content through the Upload SDK or the Push Video API.

- **Livestream API Integration**: Features for managing live streams, including:
  - **Create and Manage Livestreams**: Users can create, update, and delete live streams.
    - **Create Livestream**: Initiate the creation of a new livestream.
    - **Get All Livestreams**: List all available live streams.
    - **Get Livestream by ID**: Retrieve details of a specific livestream using its stream ID.
    - **Update Livestream**: Modify settings or details of an existing livestream.
    - **Delete Livestream**: Remove a livestream from the platform.
  - **Manage Playback IDs for Livestreams**: Users can generate and manage playback IDs for livestreams.
    - **Create Playback ID for Livestream**: Generate a playback ID for a livestream.
    - **Get Playback ID for Livestream**: Retrieve a playback ID for a livestream.
    - **Delete Playback ID for Livestream**: Remove a playback ID for a livestream.

- **Simulcast for Livestreams**: Below are the simulcast features for livestreams:
  - **Create Simulcast Configuration**: Enable simulcasting by creating a new simulcast configuration.
  - **Get Simulcast Configuration**: Retrieve details of an existing simulcast configuration.
  - **Update Simulcast Configuration**: Modify an existing simulcast configuration.
  - **Delete Simulcast Configuration**: Remove a simulcast configuration.
