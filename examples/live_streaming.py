"""Live streaming: create a stream, attach a playback id, read/update it, toggle
enable/disable/complete, then delete it. Point your encoder at the stream key."""

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
        # 1. Create a live stream.
        stream = fastpix.start_live_stream.create_new_stream(
            playback_settings={},
            input_media_settings={"metadata": {"livestream_name": "fastpix_livestream"}, "enable_recording": True},
        )
        _print("create stream", stream)
        stream_id = stream.data.stream_id

        # 2. Give it a playback id.
        playback = fastpix.live_playback.create_playback_id_of_stream(
            stream_id=stream_id, access_policy="public",
        )
        _print("create playback id", playback)
        playback_id = playback.data.id

        # Restrict playback to example.com only.
        _print("update domain restrictions", fastpix.live_playback.update_live_stream_domain_restrictions(
            stream_id=stream_id, playback_id=playback_id, default_policy="deny", allow=["example.com"], deny=[],
        ))

        # 3. Read + update + toggle state.
        _print("get stream", fastpix.manage_live_stream.get_live_stream_by_id(stream_id=stream_id))
        _print("update stream", fastpix.manage_live_stream.update_live_stream(
            stream_id=stream_id, metadata={"livestream_name": "renamed_stream"}, reconnect_window=100,
        ))
        # New streams start enabled, so disable first, then re-enable.
        _print("disable stream", fastpix.manage_live_stream.disable_live_stream(stream_id=stream_id))
        _print("enable stream", fastpix.manage_live_stream.enable_live_stream(stream_id=stream_id))

        # 4. Delete it.
        _print("delete stream", fastpix.manage_live_stream.delete_live_stream(stream_id=stream_id))


if __name__ == "__main__":
    main()
