"""
FastPix Error Handling Samples

This sample demonstrates how to implement comprehensive error handling for:
- API errors and exceptions
- Network connectivity issues
- Authentication and authorization errors
- Rate limiting and retry logic
- Custom error handling strategies
"""

import os
import time
from fastpix_python import Fastpix, models, errors
from fastpix_python.utils import BackoffStrategy, RetryConfig


def setup_client():
    """Initialize the FastPix client with credentials."""
    return Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_ACCESS_TOKEN"),
            password=os.getenv("FASTPIX_SECRET_KEY"),
        ),
    )


def setup_client_with_retry():
    """Initialize the FastPix client with retry configuration."""
    retry_config = RetryConfig(
        strategy="backoff",
        backoff_strategy=BackoffStrategy(
            initial_interval=1,
            max_interval=60,
            multiplier=2,
            max_elapsed_time=300
        ),
        retry_connection_errors=True
    )
    
    return Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_ACCESS_TOKEN"),
            password=os.getenv("FASTPIX_SECRET_KEY"),
        ),
        retry_config=retry_config
    )


def handle_basic_errors():
    """Demonstrate basic error handling."""
    with setup_client() as fastpix:
        print("=== Basic Error Handling ===")
        
        try:
            # This will likely fail with invalid media ID
            media = fastpix.manage_videos.get_media(media_id="invalid-id")
            print(f"Media found: {media.title}")
            
        except errors.MediaNotFoundError as e:
            print(f"❌ Media not found: {e.message}")
            print(f"   Status Code: {e.status_code}")
            print(f"   Media ID: invalid-id")
            
        except errors.FastpixError as e:
            print(f"❌ FastPix Error: {e.message}")
            print(f"   Status Code: {e.status_code}")
            print(f"   Headers: {e.headers}")
            
        except Exception as e:
            print(f"❌ Unexpected Error: {str(e)}")


def handle_authentication_errors():
    """Demonstrate authentication error handling."""
    print("\n=== Authentication Error Handling ===")
    
    # Create client with invalid credentials
    invalid_client = Fastpix(
        security=models.Security(
            username="invalid-token",
            password="invalid-secret",
        ),
    )
    
    try:
        with invalid_client as fastpix:
            media = fastpix.manage_videos.get_media(media_id="any-id")
            
    except errors.UnauthorizedError as e:
        print(f"❌ Authentication failed: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Solution: Check your access token and secret key")
        
    except errors.FastpixError as e:
        print(f"❌ FastPix Error: {e.message}")
        print(f"   Status Code: {e.status_code}")


def handle_permission_errors():
    """Demonstrate permission error handling."""
    with setup_client() as fastpix:
        print("\n=== Permission Error Handling ===")
        
        try:
            # This might fail due to insufficient permissions
            streams = fastpix.manage_live_stream.get_all_streams()
            print(f"✅ Streams retrieved: {len(streams.data)}")
            
        except errors.ForbiddenError as e:
            print(f"❌ Permission denied: {e.message}")
            print(f"   Status Code: {e.status_code}")
            print(f"   Solution: Check your account permissions")
            
        except errors.InvalidPermissionError as e:
            print(f"❌ Invalid permission: {e.message}")
            print(f"   Status Code: {e.status_code}")
            print(f"   Solution: Contact support for permission upgrade")


def handle_validation_errors():
    """Demonstrate validation error handling."""
    with setup_client() as fastpix:
        print("\n=== Validation Error Handling ===")
        
        try:
            # This will fail due to invalid input
            media = fastpix.input_video.create_media(
                inputs=[{
                    "type": "video",
                    "url": "invalid-url-format"
                }],
                access_policy="invalid-policy"
            )
            
        except errors.BadRequestError as e:
            print(f"❌ Bad Request: {e.message}")
            print(f"   Status Code: {e.status_code}")
            if hasattr(e, 'data') and e.data:
                print(f"   Validation Details: {e.data}")
            print(f"   Solution: Check your input parameters")
            
        except errors.ValidationErrorResponse as e:
            print(f"❌ Validation Error: {e.message}")
            print(f"   Status Code: {e.status_code}")
            print(f"   Solution: Fix the validation errors and retry")


def handle_retry_logic():
    """Demonstrate retry logic for transient errors."""
    print("\n=== Retry Logic Handling ===")
    
    with setup_client_with_retry() as fastpix:
        try:
            # This will use the retry configuration
            media_list = fastpix.manage_videos.list_media()
            print(f"✅ Media list retrieved: {len(media_list.data)} items")
            
        except errors.FastpixError as e:
            print(f"❌ Error after retries: {e.message}")
            print(f"   Status Code: {e.status_code}")
            
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")


def handle_network_errors():
    """Demonstrate network error handling."""
    print("\n=== Network Error Handling ===")
    
    # Simulate network issues by using invalid server URL
    try:
        network_client = Fastpix(
            server_url="https://invalid-server.fastpix.io",
            security=models.Security(
                username=os.getenv("FASTPIX_ACCESS_TOKEN"),
                password=os.getenv("FASTPIX_SECRET_KEY"),
            ),
        )
        
        with network_client as fastpix:
            media = fastpix.manage_videos.list_media()
            
    except errors.FastpixError as e:
        print(f"❌ Network Error: {e.message}")
        print(f"   Status Code: {e.status_code}")
        print(f"   Solution: Check your internet connection and server URL")
        
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        print(f"   Solution: Verify network connectivity and server availability")


def comprehensive_error_handling():
    """Demonstrate comprehensive error handling strategy."""
    with setup_client() as fastpix:
        print("\n=== Comprehensive Error Handling ===")
        
        try:
            # Attempt to get media with error handling
            media = fastpix.manage_videos.get_media(media_id="test-media-id")
            print(f"✅ Media retrieved: {media.title}")
            
        except errors.MediaNotFoundError as e:
            print(f"❌ Media Not Found:")
            print(f"   Message: {e.message}")
            print(f"   Status: {e.status_code}")
            print(f"   Action: Check media ID or create new media")
            
        except errors.UnauthorizedError as e:
            print(f"❌ Authentication Error:")
            print(f"   Message: {e.message}")
            print(f"   Status: {e.status_code}")
            print(f"   Action: Verify credentials and permissions")
            
        except errors.ForbiddenError as e:
            print(f"❌ Permission Error:")
            print(f"   Message: {e.message}")
            print(f"   Status: {e.status_code}")
            print(f"   Action: Check account permissions")
            
        except errors.BadRequestError as e:
            print(f"❌ Bad Request Error:")
            print(f"   Message: {e.message}")
            print(f"   Status: {e.status_code}")
            print(f"   Action: Validate input parameters")
            
        except errors.FastpixError as e:
            print(f"❌ FastPix Error:")
            print(f"   Message: {e.message}")
            print(f"   Status: {e.status_code}")
            print(f"   Headers: {e.headers}")
            print(f"   Body: {e.body}")
            
        except Exception as e:
            print(f"❌ Unexpected Error:")
            print(f"   Type: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            print(f"   Action: Check logs and contact support")


def demonstrate_error_recovery():
    """Demonstrate error recovery strategies."""
    print("\n=== Error Recovery Strategies ===")
    
    with setup_client() as fastpix:
        # Strategy 1: Retry with exponential backoff
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                media_list = fastpix.manage_videos.list_media()
                print(f"✅ Success on attempt {attempt + 1}")
                break
                
            except errors.FastpixError as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"⚠️ Attempt {attempt + 1} failed: {e.message}")
                    print(f"   Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"❌ All retry attempts failed: {e.message}")
                    
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                break


def log_errors_properly():
    """Demonstrate proper error logging."""
    print("\n=== Proper Error Logging ===")
    
    with setup_client() as fastpix:
        try:
            # Simulate an operation that might fail
            media = fastpix.manage_videos.get_media(media_id="non-existent-id")
            
        except errors.FastpixError as e:
            # Log error with context
            error_context = {
                "error_type": type(e).__name__,
                "message": e.message,
                "status_code": e.status_code,
                "timestamp": time.time(),
                "operation": "get_media",
                "media_id": "non-existent-id"
            }
            
            print(f"📝 Error logged:")
            for key, value in error_context.items():
                print(f"   {key}: {value}")
                
        except Exception as e:
            # Log unexpected errors
            error_context = {
                "error_type": type(e).__name__,
                "message": str(e),
                "timestamp": time.time(),
                "operation": "get_media"
            }
            
            print(f"📝 Unexpected error logged:")
            for key, value in error_context.items():
                print(f"   {key}: {value}")


def complete_error_handling_workflow():
    """Complete error handling demonstration workflow."""
    try:
        print("🚀 Starting FastPix Error Handling Workflow\n")
        
        # Step 1: Basic error handling
        handle_basic_errors()
        
        # Step 2: Authentication errors
        handle_authentication_errors()
        
        # Step 3: Permission errors
        handle_permission_errors()
        
        # Step 4: Validation errors
        handle_validation_errors()
        
        # Step 5: Retry logic
        handle_retry_logic()
        
        # Step 6: Network errors
        handle_network_errors()
        
        # Step 7: Comprehensive error handling
        comprehensive_error_handling()
        
        # Step 8: Error recovery
        demonstrate_error_recovery()
        
        # Step 9: Proper logging
        log_errors_properly()
        
        print(f"\n🎉 Error handling workflow completed!")
        print(f"💡 Best Practices:")
        print(f"   1. Always catch specific exception types")
        print(f"   2. Implement retry logic for transient errors")
        print(f"   3. Log errors with sufficient context")
        print(f"   4. Provide meaningful error messages to users")
        print(f"   5. Monitor error rates and patterns")
        
    except Exception as e:
        print(f"❌ Error in error handling workflow: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("FASTPIX_ACCESS_TOKEN") or not os.getenv("FASTPIX_SECRET_KEY"):
        print("❌ Please set FASTPIX_ACCESS_TOKEN and FASTPIX_SECRET_KEY environment variables")
        exit(1)
    
    complete_error_handling_workflow()
