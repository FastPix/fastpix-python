"""
FastPix Live API Samples

This sample demonstrates how to use the FastPix Live API for:
- Creating and managing live streams
- Setting up simulcast streaming
- Managing live playback
- Monitoring stream performance
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


def create_and_manage_live_stream():
    """Create a live stream and manage its lifecycle."""
    with setup_client() as fastpix:
        print("=== Creating Live Stream ===")
        
        # Create new live stream
        stream = fastpix.start_live_stream.create_new_stream(
            name="Sample Live Stream",
            description="A sample live streaming event",
            access_policy="public",
            metadata={
                "category": "demo",
                "tags": ["live", "sample"]
            }
        )
        print(f"✅ Live stream created with ID: {stream.id}")
        print(f"📡 Stream URL: {stream.rtmp_url}")
        
        # Enable the stream
        fastpix.manage_live_stream.enable_live_stream(stream_id=stream.id)
        print("✅ Stream enabled and ready for broadcasting")
        
        # Get stream details
        stream_details = fastpix.manage_live_stream.get_live_stream_by_id(stream_id=stream.id)
        print(f"📊 Stream status: {stream_details.status}")
        print(f"👥 Max viewers: {stream_details.max_viewers}")
        
        return stream.id


def setup_live_playback(stream_id):
    """Set up live playback for the stream."""
    with setup_client() as fastpix:
        print("\n=== Setting Up Live Playback ===")
        
        # Create playback ID for live stream
        playback = fastpix.live_playback.create_playback_id_of_stream(
            stream_id=stream_id,
            access_policy="public"
        )
        print(f"✅ Live playback ID created: {playback.id}")
        
        # Get playback details
        playback_details = fastpix.live_playback.get_live_stream_playback_id(
            playback_id=playback.id
        )
        print(f"▶️ Playback URL: {playback_details.playback_url}")
        
        return playback.id


def setup_simulcast_streaming(stream_id):
    """Set up simulcast streaming to multiple platforms."""
    with setup_client() as fastpix:
        print("\n=== Setting Up Simulcast Streaming ===")
        
        # Create simulcast for YouTube
        youtube_simulcast = fastpix.simulcast_stream.create_simulcast_of_stream(
            stream_id=stream_id,
            platform="youtube",
            rtmp_url="rtmp://a.rtmp.youtube.com/live2/your-stream-key"
        )
        print(f"✅ YouTube simulcast created: {youtube_simulcast.id}")
        
        # Create simulcast for Twitch
        twitch_simulcast = fastpix.simulcast_stream.create_simulcast_of_stream(
            stream_id=stream_id,
            platform="twitch",
            rtmp_url="rtmp://live.twitch.tv/live/your-stream-key"
        )
        print(f"✅ Twitch simulcast created: {twitch_simulcast.id}")
        
        # List all simulcasts
        simulcasts = fastpix.simulcast_stream.get_specific_simulcast_of_stream(
            stream_id=stream_id
        )
        print(f"📡 Active simulcasts: {len(simulcasts.data)}")
        
        return [youtube_simulcast.id, twitch_simulcast.id]


def monitor_stream_performance(stream_id):
    """Monitor stream performance and viewer statistics."""
    with setup_client() as fastpix:
        print("\n=== Monitoring Stream Performance ===")
        
        # Get viewer count
        viewer_count = fastpix.manage_live_stream.get_live_stream_viewer_count_by_id(
            stream_id=stream_id
        )
        print(f"👥 Current viewers: {viewer_count.count}")
        
        # Get all streams for comparison
        all_streams = fastpix.manage_live_stream.get_all_streams()
        print(f"📊 Total active streams: {len(all_streams.data)}")
        
        # Update stream settings
        fastpix.manage_live_stream.update_live_stream(
            stream_id=stream_id,
            name="Updated Live Stream",
            description="Updated description with new settings"
        )
        print("✅ Stream settings updated")


def complete_live_stream_workflow():
    """Complete live streaming workflow."""
    try:
        print("🚀 Starting FastPix Live API Workflow\n")
        
        # Step 1: Create and manage live stream
        stream_id = create_and_manage_live_stream()
        
        # Step 2: Setup live playback
        playback_id = setup_live_playback(stream_id)
        
        # Step 3: Setup simulcast streaming
        simulcast_ids = setup_simulcast_streaming(stream_id)
        
        # Step 4: Monitor performance
        monitor_stream_performance(stream_id)
        
        print(f"\n🎉 Live streaming workflow completed!")
        print(f"📡 Stream ID: {stream_id}")
        print(f"▶️ Playback ID: {playback_id}")
        print(f"📺 Simulcast IDs: {simulcast_ids}")
        print(f"\n💡 Use the RTMP URL to start broadcasting from OBS or similar software")
        
        # Note: In a real application, you would keep the stream running
        # and handle the complete stream lifecycle
        
    except Exception as e:
        print(f"❌ Error in live streaming workflow: {str(e)}")


def cleanup_live_stream(stream_id):
    """Clean up live stream resources."""
    with setup_client() as fastpix:
        print(f"\n=== Cleaning Up Stream {stream_id} ===")
        
        try:
            # Complete the stream
            fastpix.manage_live_stream.complete_live_stream(stream_id=stream_id)
            print("✅ Stream completed and archived")
            
            # Delete the stream
            fastpix.manage_live_stream.delete_live_stream(stream_id=stream_id)
            print("✅ Stream deleted")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("FASTPIX_ACCESS_TOKEN") or not os.getenv("FASTPIX_SECRET_KEY"):
        print("❌ Please set FASTPIX_ACCESS_TOKEN and FASTPIX_SECRET_KEY environment variables")
        exit(1)
    
    complete_live_stream_workflow()
    
    # Uncomment to test cleanup
    # cleanup_live_stream("your-stream-id")
