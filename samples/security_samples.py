"""
FastPix Security Samples

This sample demonstrates how to use the FastPix Security features for:
- Managing signing keys for secure playback
- Configuring DRM settings
- Setting up access control
- Implementing secure token-based authentication
"""

import os
import jwt
import time
from datetime import datetime, timedelta
from fastpix_python import Fastpix, models


def setup_client():
    """Initialize the FastPix client with credentials."""
    return Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_ACCESS_TOKEN"),
            password=os.getenv("FASTPIX_SECRET_KEY"),
        ),
    )


def manage_signing_keys():
    """Manage signing keys for secure playback."""
    with setup_client() as fastpix:
        print("=== Managing Signing Keys ===")
        
        # Create a new signing key
        signing_key = fastpix.signing_keys.create_signing_key(
            name="Sample Signing Key",
            expires_at=(datetime.now() + timedelta(days=365)).isoformat()
        )
        print(f"✅ Signing key created: {signing_key.id}")
        print(f"🔑 Key name: {signing_key.name}")
        print(f"⏰ Expires: {signing_key.expires_at}")
        
        # List all signing keys
        keys = fastpix.signing_keys.list_signing_keys()
        print(f"\n📋 Total signing keys: {len(keys.data)}")
        
        for key in keys.data:
            print(f"   - {key.name} (ID: {key.id})")
        
        # Get specific key details
        key_details = fastpix.signing_keys.get_signing_key_by_id(
            signing_key_id=signing_key.id
        )
        print(f"\n🔍 Key details for {key_details.name}:")
        print(f"   Created: {key_details.created_at}")
        print(f"   Status: {key_details.status}")
        
        return signing_key.id


def configure_drm_settings():
    """Configure DRM settings for content protection."""
    with setup_client() as fastpix:
        print("\n=== Configuring DRM Settings ===")
        
        # List available DRM configurations
        drm_configs = fastpix.drm_configurations.get_drm_configuration()
        print(f"🔐 Available DRM configurations: {len(drm_configs.data)}")
        
        for config in drm_configs.data:
            print(f"   - {config.id}: {config.name}")
        
        # Get specific DRM configuration details
        if drm_configs.data:
            config_details = fastpix.drm_configurations.get_drm_configuration_by_id(
                config_id=drm_configs.data[0].id
            )
            print(f"\n🔍 DRM Configuration Details:")
            print(f"   ID: {config_details.id}")
            print(f"   Name: {config_details.name}")
            print(f"   Type: {config_details.type}")
        
        return drm_configs.data[0].id if drm_configs.data else None


def create_secure_token(signing_key_id, media_id, expiration_hours=24):
    """Create a secure JWT token for media access."""
    with setup_client() as fastpix:
        print(f"\n=== Creating Secure Token ===")
        
        # Get signing key details
        key_details = fastpix.signing_keys.get_signing_key_by_id(
            signing_key_id=signing_key_id
        )
        
        # Create JWT payload
        now = int(time.time())
        payload = {
            "iss": "fastpix-sdk",
            "sub": media_id,
            "aud": "fastpix-api",
            "iat": now,
            "exp": now + (expiration_hours * 3600),
            "media_id": media_id,
            "access_level": "view"
        }
        
        # Note: In a real implementation, you would use the private key
        # to sign the JWT. For this example, we'll create the structure.
        print(f"🔐 JWT Token created for media: {media_id}")
        print(f"⏰ Expires in: {expiration_hours} hours")
        print(f"📋 Payload: {payload}")
        
        # In production, you would sign with the private key:
        # token = jwt.encode(payload, private_key, algorithm="RS256")
        
        return payload


def demonstrate_access_control():
    """Demonstrate access control features."""
    with setup_client() as fastpix:
        print("\n=== Access Control Features ===")
        
        print("🛡️ Security Features Available:")
        print("   - JWT-based authentication")
        print("   - Time-limited access tokens")
        print("   - Media-specific permissions")
        print("   - Domain restrictions")
        print("   - User-agent filtering")
        print("   - Geographic restrictions")
        
        print("\n🔐 Token Types:")
        print("   - View tokens: Read-only access")
        print("   - Download tokens: Media download access")
        print("   - Admin tokens: Full management access")
        
        print("\n⏰ Token Expiration:")
        print("   - Short-term: 1-24 hours")
        print("   - Medium-term: 1-7 days")
        print("   - Long-term: 1-30 days")


def implement_secure_playback(media_id, signing_key_id):
    """Implement secure playback with token-based access."""
    with setup_client() as fastpix:
        print(f"\n=== Implementing Secure Playback ===")
        
        # Create secure token
        token_payload = create_secure_token(signing_key_id, media_id)
        
        # Create playback ID with security
        playback = fastpix.playback.create_media_playback_id(
            media_id=media_id,
            access_policy="private"
        )
        print(f"✅ Secure playback ID created: {playback.id}")
        
        # In a real implementation, you would:
        # 1. Sign the token with the private key
        # 2. Include the token in the playback URL
        # 3. Validate the token on the client side
        
        print(f"🔗 Secure playback URL structure:")
        print(f"   https://playback.fastpix.io/{playback.id}?token=<JWT_TOKEN>")
        
        return playback.id


def manage_security_lifecycle():
    """Manage the complete security lifecycle."""
    with setup_client() as fastpix:
        print("\n=== Security Lifecycle Management ===")
        
        # Create signing key
        signing_key_id = manage_signing_keys()
        
        # Configure DRM
        drm_config_id = configure_drm_settings()
        
        # Demonstrate access control
        demonstrate_access_control()
        
        # Example media ID (replace with actual)
        media_id = "sample-media-id"
        
        # Implement secure playback
        playback_id = implement_secure_playback(media_id, signing_key_id)
        
        print(f"\n🎉 Security setup completed!")
        print(f"🔑 Signing Key ID: {signing_key_id}")
        print(f"🔐 DRM Config ID: {drm_config_id}")
        print(f"▶️ Playback ID: {playback_id}")
        
        return {
            "signing_key_id": signing_key_id,
            "drm_config_id": drm_config_id,
            "playback_id": playback_id
        }


def cleanup_security_resources(signing_key_id):
    """Clean up security resources."""
    with setup_client() as fastpix:
        print(f"\n=== Cleaning Up Security Resources ===")
        
        try:
            # Delete signing key
            fastpix.signing_keys.delete_signing_key(
                signing_key_id=signing_key_id
            )
            print(f"✅ Signing key {signing_key_id} deleted")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {str(e)}")


def complete_security_workflow():
    """Complete security implementation workflow."""
    try:
        print("🚀 Starting FastPix Security Workflow\n")
        
        # Step 1: Manage security lifecycle
        security_resources = manage_security_lifecycle()
        
        print(f"\n💡 Security Implementation Tips:")
        print(f"   1. Store private keys securely (use environment variables)")
        print(f"   2. Implement token refresh mechanisms")
        print(f"   3. Monitor key usage and rotation")
        print(f"   4. Use HTTPS for all token transmission")
        print(f"   5. Implement proper error handling for expired tokens")
        
        print(f"\n🎉 Security workflow completed successfully!")
        
        # Uncomment to test cleanup
        # cleanup_security_resources(security_resources["signing_key_id"])
        
    except Exception as e:
        print(f"❌ Error in security workflow: {str(e)}")


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("FASTPIX_ACCESS_TOKEN") or not os.getenv("FASTPIX_SECRET_KEY"):
        print("❌ Please set FASTPIX_ACCESS_TOKEN and FASTPIX_SECRET_KEY environment variables")
        exit(1)
    
    complete_security_workflow()
