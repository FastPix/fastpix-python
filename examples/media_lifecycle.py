"""Media lifecycle: create a media, get it, list media, update its metadata,
then delete it."""

import json
import os

from fastpix_python import Fastpix, models


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
        # 1. Create media from a hosted video URL.
        created = fastpix.input_video.create_media(
            inputs=[{"type": "video", "url": "https://static.fastpix.io/fp-sample-video.mp4"}],
            metadata={"key1": "value1"},
            access_policy="public",
            max_resolution="1080p",
        )
        _print("create media", created)
        media_id = created.data.id

        # 2. Fetch it back by id.
        _print("get media", fastpix.manage_videos.get_media(media_id=media_id))

        # 3. List media in the workspace.
        _print("list media", fastpix.manage_videos.list_media(limit=20, offset=1, order_by="desc"))

        # 4. Update its metadata.
        _print("update media", fastpix.manage_videos.updated_media(
            media_id=media_id, metadata={"user": "fastpix_admin"},
        ))

        # 5. Delete it.
        _print("delete media", fastpix.manage_videos.delete_media(media_id=media_id))


if __name__ == "__main__":
    main()
