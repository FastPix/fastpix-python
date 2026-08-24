"""Playback IDs & access control: create a playback id for a media, restrict
playback by domain and user agent, then delete the playback id."""

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
        # 1. Create a playback id for the media.
        playback = fastpix.playback.create_media_playback_id(
            media_id=MEDIA_ID, access_policy="public", resolution="1080p",
        )
        _print("create playback id", playback)
        playback_id = playback.data.id

        # 2. Restrict which domains and user agents may play it.
        _print("domain restrictions", fastpix.playback.update_domain_restrictions(
            media_id=MEDIA_ID, playback_id=playback_id, default_policy="allow",
            allow=["yourdomain.com"], deny=["blockeddomain.com"],
        ))
        _print("user-agent restrictions", fastpix.playback.update_user_agent_restrictions(
            media_id=MEDIA_ID, playback_id=playback_id, default_policy="allow",
            allow=["Mozilla/5.0"], deny=[],
        ))

        # 3. Remove the playback id.
        _print("delete playback id", fastpix.playback.delete_media_playback_id(
            media_id=MEDIA_ID, playback_id=playback_id,
        ))


if __name__ == "__main__":
    main()
