"""Simulcast: create a stream, add a simulcast target (an external RTMP
destination like YouTube/Twitch), update it, then remove it and the stream."""

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
        # 1. Create a stream to simulcast.
        stream = fastpix.start_live_stream.create_new_stream(
            playback_settings={},
            input_media_settings={"metadata": {"livestream_name": "fastpix_livestream"}},
        )
        stream_id = stream.data.stream_id

        # 2. Add a simulcast target (RTMP url + stream key of the destination).
        simulcast = fastpix.simulcast_stream.create_simulcast_of_stream(
            stream_id=stream_id,
            url="rtmps://a.rtmp.youtube.com/live2",
            stream_key="your-destination-stream-key",
            metadata={"livestream_name": "Tech-Connect Summit"},
        )
        _print("create simulcast", simulcast)
        simulcast_id = simulcast.data.simulcast_id

        # 3. Enable/disable it, then remove it and the stream.
        _print("update simulcast", fastpix.simulcast_stream.update_specific_simulcast_of_stream(
            stream_id=stream_id, simulcast_id=simulcast_id, is_enabled=True,
            metadata={"simulcast_name": "Tech today"},
        ))
        _print("delete simulcast", fastpix.simulcast_stream.delete_simulcast_of_stream(
            stream_id=stream_id, simulcast_id=simulcast_id,
        ))
        _print("delete stream", fastpix.manage_live_stream.delete_live_stream(stream_id=stream_id))


if __name__ == "__main__":
    main()
