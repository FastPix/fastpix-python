"""
FastPix Media API Samples

This sample demonstrates how to use the FastPix Media API for:
- Uploading and managing video content
- Creating and managing playlists
- Setting up playback and security
- Managing media tracks and metadata
"""

import os
from fastpix_python import Fastpix, models


def setup_client():
    """Initialize the FastPix client with credentials."""
    return Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_ACCESS_TOKEN"),
            password=os.getenv("FASTPIX_SECRET_KEY"),
        ),
    )


def upload_and_manage_video():
    """Upload video content and manage it."""
    with setup_client() as fastpix:
        print("=== Uploading Video Content ===")
        
        # Upload video from URL
        media = fastpix.input_video.create_media(
            inputs=[{
                "type": "video",
                "url": "https://example.com/sample-video.mp4"
            }],
            access_policy="public",
            metadata={
                "title": "Sample Video",
                "description": "A sample video for testing",
                "tags": ["demo", "sample"]
            },
            mp4_support="capped_4k",
            optimize_audio=True,
            max_resolution="1080p"
        )
        print(f"✅ Video uploaded with ID: {media.id}")
        
        # Get media details
        media_details = fastpix.manage_videos.get_media(media_id=media.id)
        print(f"📹 Media title: {media_details.title}")
        print(f"📊 Status: {media_details.status}")
        
        return media.id


def create_and_manage_playlist(media_id):
    """Create a playlist and add media to it."""
    with setup_client() as fastpix:
        print("\n=== Creating and Managing Playlist ===")
        
        # Create playlist
        playlist = fastpix.playlist.create_a_playlist(
            name="My Sample Playlist",
            description="A collection of sample videos",
            access_policy="public"
        )
        print(f"✅ Playlist created with ID: {playlist.id}")
        
        # Add media to playlist
        fastpix.playlist.add_media_to_playlist(
            playlist_id=playlist.id,
            media_id=media_id
        )
        print(f"✅ Media added to playlist")
        
        # List all playlists
        playlists = fastpix.playlist.get_all_playlists()
        print(f"📋 Total playlists: {len(playlists.data)}")
        
        return playlist.id


def setup_playback_and_security(media_id):
    """Set up playback and security features."""
    with setup_client() as fastpix:
        print("\n=== Setting Up Playback and Security ===")
        
        # Create playback ID
        playback = fastpix.playback.create_media_playback_id(
            media_id=media_id,
            access_policy="public"
        )
        print(f"✅ Playback ID created: {playback.id}")
        
        # Create signing key for secure playback
        signing_key = fastpix.signing_keys.create_signing_key(
            name="Sample Signing Key",
            expires_at="2024-12-31T23:59:59Z"
        )
        print(f"✅ Signing key created: {signing_key.id}")
        
        # Get DRM configurations
        drm_configs = fastpix.drm_configurations.get_drm_configuration()
        print(f"🔐 Available DRM configurations: {len(drm_configs.data)}")
        
        return playback.id, signing_key.id


def manage_media_tracks(media_id):
    """Manage audio and subtitle tracks."""
    with setup_client() as fastpix:
        print("\n=== Managing Media Tracks ===")
        
        # Add subtitle track
        subtitle_track = fastpix.manage_videos.add_media_track(
            media_id=media_id,
            type="subtitle",
            language_code="en",
            language_name="English"
        )
        print(f"✅ Subtitle track added: {subtitle_track.id}")
        
        # Generate automatic subtitles
        fastpix.manage_videos.generate_subtitle_track(
            media_id=media_id,
            language_code="en",
            language_name="English (Auto-generated)"
        )
        print("✅ Auto-generated subtitles created")
        
        # Update source access
        fastpix.manage_videos.updated_source_access(
            media_id=media_id,
            source_access=True
        )
        print("✅ Source access updated")


def complete_media_workflow():
    """Complete media management workflow."""
    try:
        print("🚀 Starting FastPix Media API Workflow\n")
        
        # Step 1: Upload video
        media_id = upload_and_manage_video()
        
        # Step 2: Create playlist
        playlist_id = create_and_manage_playlist(media_id)
        
        # Step 3: Setup playback and security
        playback_id, signing_key_id = setup_playback_and_security(media_id)
        
        # Step 4: Manage tracks
        manage_media_tracks(media_id)
        
        print(f"\n🎉 Workflow completed successfully!")
        print(f"📹 Media ID: {media_id}")
        print(f"📋 Playlist ID: {playlist_id}")
        print(f"▶️ Playback ID: {playback_id}")
        print(f"🔑 Signing Key ID: {signing_key_id}")
        
    except Exception as e:
        print(f"❌ Error in workflow: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("FASTPIX_ACCESS_TOKEN") or not os.getenv("FASTPIX_SECRET_KEY"):
        print("❌ Please set FASTPIX_ACCESS_TOKEN and FASTPIX_SECRET_KEY environment variables")
        exit(1)
    
    complete_media_workflow()
