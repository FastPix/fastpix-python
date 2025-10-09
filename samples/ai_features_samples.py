"""
FastPix AI Features Samples

This sample demonstrates how to use the FastPix AI Features for:
- Content moderation and safety
- Video summarization
- Chapter generation
- Named entity extraction
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


def enable_content_moderation(media_id):
    """Enable content moderation for video content."""
    with setup_client() as fastpix:
        print("=== Enabling Content Moderation ===")
        
        # Enable video moderation
        moderation_result = fastpix.in_video_ai_features.update_media_moderation(
            media_id=media_id,
            type="video"
        )
        print(f"✅ Content moderation enabled for media: {media_id}")
        print(f"🔍 Moderation will analyze for NSFW content, violence, and other safety issues")
        
        return moderation_result


def generate_video_summary(media_id):
    """Generate AI-powered video summary."""
    with setup_client() as fastpix:
        print("\n=== Generating Video Summary ===")
        
        # Generate video summary
        summary_result = fastpix.in_video_ai_features.update_media_summary(
            media_id=media_id,
            generate=True
        )
        print(f"✅ Video summary generation initiated for media: {media_id}")
        print(f"📝 AI will analyze the content and generate a comprehensive summary")
        
        return summary_result


def create_video_chapters(media_id):
    """Create automatic video chapters."""
    with setup_client() as fastpix:
        print("\n=== Creating Video Chapters ===")
        
        # Generate video chapters
        chapters_result = fastpix.in_video_ai_features.update_media_chapters(
            media_id=media_id,
            generate=True
        )
        print(f"✅ Chapter generation initiated for media: {media_id}")
        print(f"📑 AI will analyze the content and create chapter markers")
        
        return chapters_result


def extract_named_entities(media_id):
    """Extract named entities from video content."""
    with setup_client() as fastpix:
        print("\n=== Extracting Named Entities ===")
        
        # Generate named entities
        entities_result = fastpix.in_video_ai_features.update_media_named_entities(
            media_id=media_id,
            generate=True
        )
        print(f"✅ Named entity extraction initiated for media: {media_id}")
        print(f"🏷️ AI will identify and categorize people, places, organizations, and other entities")
        
        return entities_result


def process_ai_features_batch(media_ids):
    """Process AI features for multiple media files."""
    with setup_client() as fastpix:
        print("\n=== Processing AI Features for Multiple Media ===")
        
        results = {}
        
        for media_id in media_ids:
            print(f"\nProcessing media: {media_id}")
            
            try:
                # Enable moderation
                moderation = fastpix.in_video_ai_features.update_media_moderation(
                    media_id=media_id,
                    type="video"
                )
                
                # Generate summary
                summary = fastpix.in_video_ai_features.update_media_summary(
                    media_id=media_id,
                    generate=True
                )
                
                # Create chapters
                chapters = fastpix.in_video_ai_features.update_media_chapters(
                    media_id=media_id,
                    generate=True
                )
                
                # Extract entities
                entities = fastpix.in_video_ai_features.update_media_named_entities(
                    media_id=media_id,
                    generate=True
                )
                
                results[media_id] = {
                    "moderation": moderation,
                    "summary": summary,
                    "chapters": chapters,
                    "entities": entities
                }
                
                print(f"✅ All AI features processed for {media_id}")
                
            except Exception as e:
                print(f"⚠️ Error processing {media_id}: {str(e)}")
                results[media_id] = {"error": str(e)}
        
        return results


def demonstrate_content_safety():
    """Demonstrate content safety and moderation features."""
    with setup_client() as fastpix:
        print("\n=== Content Safety Demonstration ===")
        
        # This would typically be done with actual media
        print("🛡️ Content Moderation Features:")
        print("   - NSFW content detection")
        print("   - Violence and graphic content detection")
        print("   - Hate speech and harassment detection")
        print("   - Self-harm content detection")
        print("   - Confidence scoring for each category")
        
        print("\n📊 Moderation Results Include:")
        print("   - Category classification")
        print("   - Confidence scores (0-1)")
        print("   - Timestamp information")
        print("   - Actionable recommendations")


def demonstrate_content_enhancement():
    """Demonstrate content enhancement features."""
    with setup_client() as fastpix:
        print("\n=== Content Enhancement Demonstration ===")
        
        print("🤖 AI-Powered Content Enhancement:")
        print("   - Automatic video summarization")
        print("   - Smart chapter generation")
        print("   - Named entity recognition")
        print("   - Content categorization")
        
        print("\n📈 Enhancement Benefits:")
        print("   - Improved content discoverability")
        print("   - Better user experience")
        print("   - Automated content organization")
        print("   - Enhanced search capabilities")


def complete_ai_features_workflow(media_id):
    """Complete AI features workflow for a media file."""
    try:
        print("🚀 Starting FastPix AI Features Workflow\n")
        
        # Step 1: Enable content moderation
        enable_content_moderation(media_id)
        
        # Step 2: Generate video summary
        generate_video_summary(media_id)
        
        # Step 3: Create video chapters
        create_video_chapters(media_id)
        
        # Step 4: Extract named entities
        extract_named_entities(media_id)
        
        # Step 5: Demonstrate features
        demonstrate_content_safety()
        demonstrate_content_enhancement()
        
        print(f"\n🎉 AI Features workflow completed for media: {media_id}")
        print(f"💡 Check your FastPix dashboard to see the AI-generated content")
        print(f"⏱️ Processing may take a few minutes depending on video length")
        
    except Exception as e:
        print(f"❌ Error in AI features workflow: {str(e)}")


def batch_process_ai_features(media_ids):
    """Process AI features for multiple media files."""
    try:
        print("🚀 Starting Batch AI Features Processing\n")
        
        results = process_ai_features_batch(media_ids)
        
        print(f"\n📊 Batch Processing Results:")
        for media_id, result in results.items():
            if "error" in result:
                print(f"   ❌ {media_id}: {result['error']}")
            else:
                print(f"   ✅ {media_id}: All features processed")
        
        print(f"\n🎉 Batch processing completed!")
        
    except Exception as e:
        print(f"❌ Error in batch processing: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("FASTPIX_ACCESS_TOKEN") or not os.getenv("FASTPIX_SECRET_KEY"):
        print("❌ Please set FASTPIX_ACCESS_TOKEN and FASTPIX_SECRET_KEY environment variables")
        exit(1)
    
    # Example usage - replace with actual media ID
    sample_media_id = "your-media-id-here"
    
    # Single media processing
    complete_ai_features_workflow(sample_media_id)
    
    # Batch processing example
    # sample_media_ids = ["media-id-1", "media-id-2", "media-id-3"]
    # batch_process_ai_features(sample_media_ids)
