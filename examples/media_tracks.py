"""Media tracks: add an alternate audio track and a subtitle track to a media.

Updating, deleting, or generating subtitles from a track requires it to finish
processing first — listen for the `track.ready` webhook before those calls."""

import json
import os

from fastpix_python import Fastpix, models

# A READY media in your workspace (see media_lifecycle.py / list_media).
MEDIA_ID = "your-ready-media-id"


def _print(label, res):
    print(f"\n=== {label} ===")
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2, default=str))


def main():
    fastpix = Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_USERNAME"),
            password=os.getenv("FASTPIX_PASSWORD"),
        ),
    )
    with fastpix:
        # Add an alternate audio track (e.g. a dubbed language).
        _print("add audio track", fastpix.manage_videos.add_media_track(media_id=MEDIA_ID, tracks={
            "url": "https://static.fastpix.io/sample.m4a",
            "type": "audio",
            "language_code": "fr",
            "language_name": "French",
        }))

        # Add a subtitle track.
        _print("add subtitle track", fastpix.manage_videos.add_media_track(media_id=MEDIA_ID, tracks={
            "url": "https://static.fastpix.io/sample.vtt",
            "type": "subtitle",
            "language_code": "es",
            "language_name": "Spanish",
        }))


if __name__ == "__main__":
    main()
