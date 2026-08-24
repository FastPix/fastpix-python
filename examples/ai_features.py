"""In-video AI: enable summary, chapters, moderation and named entities on a
media. Each runs asynchronously; results arrive via webhooks or a later fetch."""

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
        _print("summary", fastpix.in_video_ai_features.update_media_summary(
            media_id=MEDIA_ID, generate=True, summary_length=100,
        ))
        _print("chapters", fastpix.in_video_ai_features.update_media_chapters(media_id=MEDIA_ID, chapters=True))
        _print("moderation", fastpix.in_video_ai_features.update_media_moderation(
            media_id=MEDIA_ID, moderation={"type": "video"},
        ))
        _print("named entities", fastpix.in_video_ai_features.update_media_named_entities(
            media_id=MEDIA_ID, named_entities=True,
        ))


if __name__ == "__main__":
    main()
