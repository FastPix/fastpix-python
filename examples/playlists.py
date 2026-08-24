"""Playlists: create a playlist, add/reorder/remove media, read it back, update
it, then delete it. Set MEDIA_IDS to real media ids from your workspace."""

import json
import os

from fastpix_python import Fastpix, models

# Replace with real media ids from your workspace.
MEDIA_IDS = ["a9f446cd-c401-4e5e-bc40-75d36300cce1", "5fb72062-ea92-4276-abcb-4f9c4ccc65b7"]


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
        # 1. Create a playlist.
        created = fastpix.playlist.create_a_playlist(
            name="My Playlist",
            reference_id="playlist001",  # must be alphanumeric and unique in your workspace
            type_="smart",
            description="A sample playlist",
            play_order="createdDate DESC",
            limit=20,
            # A "smart" playlist requires metadata (its filter criteria).
            metadata={
                "created_date": models.DateRange(start_date="2024-01-01", end_date="2024-12-31"),
            },
        )
        _print("create playlist", created)
        playlist_id = created.data.id

        # 2. Add media, then reorder them.
        _print("add media", fastpix.playlist.add_media_to_playlist(
            playlist_id=playlist_id, media_ids=MEDIA_IDS,
        ))
        _print("reorder media", fastpix.playlist.change_media_order_in_playlist(
            playlist_id=playlist_id, media_ids=list(reversed(MEDIA_IDS)),
        ))

        # 3. Read it back (single + list).
        _print("get playlist", fastpix.playlist.get_playlist_by_id(playlist_id=playlist_id))
        _print("list playlists", fastpix.playlist.get_all_playlists(limit=10, offset=1))

        # 4. Update, remove media, then delete.
        _print("update playlist", fastpix.playlist.update_a_playlist(
            playlist_id=playlist_id, name="Renamed Playlist", description="Updated",
        ))
        _print("remove media", fastpix.playlist.delete_media_from_playlist(
            playlist_id=playlist_id, media_ids=MEDIA_IDS,
        ))
        _print("delete playlist", fastpix.playlist.delete_a_playlist(playlist_id=playlist_id))


if __name__ == "__main__":
    main()
