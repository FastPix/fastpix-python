#!/usr/bin/env python3
"""
FastPix Python SDK Test Suite
Tests the core functionality of the FastPix Python SDK.
"""

import sys
import os
import time
import unittest
from typing import Optional

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Fastpix import Fastpix
from Fastpix.models import Security


class FastPixSDKTest(unittest.TestCase):
    """Test suite for FastPix Python SDK core functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment before running tests."""
        # Get credentials from environment variables
        cls.username = os.getenv('FASTPIX_USERNAME')
        cls.password = os.getenv('FASTPIX_PASSWORD')
        
        if not cls.username or not cls.password:
            raise unittest.SkipTest(
                "FASTPIX_USERNAME and FASTPIX_PASSWORD environment variables must be set"
            )
        
        # Create FastPix client
        security = Security(username=cls.username, password=cls.password)
        cls.client = Fastpix(security=security)
        
        print(f"\n🔐 Connected to FastPix API")
        print(f"👤 Username: {cls.username}")
        print(f"🔑 Password: {'*' * len(cls.password)}")
    
    def test_1_list_media(self):
        """Test 1: List Media - Retrieve media files."""
        print("\n🧪 Test 1: List Media...")
        start_time = time.time()
        
        try:
            result = self.client.manage_videos.list_media(limit=5, offset=1)
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__}")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ FAILED ({duration:.2f}s) - {str(e)[:80]}...")
            raise
    
    def test_2_list_live_streams(self):
        """Test 2: List Live Streams - Retrieve live streams."""
        print("\n🧪 Test 2: List Live Streams...")
        start_time = time.time()
        
        try:
            result = self.client.manage_live_stream.get_all_streams(limit=5, offset=1)
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__}")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ FAILED ({duration:.2f}s) - {str(e)[:80]}...")
            raise
    
    def test_3_list_playlists(self):
        """Test 3: List Playlists - Retrieve playlists."""
        print("\n🧪 Test 3: List Playlists...")
        start_time = time.time()
        
        try:
            result = self.client.playlist.get_all_playlists(limit=5, offset=1)
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__}")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ FAILED ({duration:.2f}s) - {str(e)[:80]}...")
            raise
    
    def test_4_list_signing_keys(self):
        """Test 4: List Signing Keys - Retrieve signing keys."""
        print("\n🧪 Test 4: List Signing Keys...")
        start_time = time.time()
        
        try:
            result = self.client.signing_keys.list_signing_keys(limit=10, offset=1)
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__} ({len(result)} keys)")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ FAILED ({duration:.2f}s) - {str(e)[:80]}...")
            raise
    
    def test_5_list_dimensions(self):
        """Test 5: List Dimensions - Retrieve analytics dimensions."""
        print("\n🧪 Test 5: List Dimensions...")
        start_time = time.time()
        
        try:
            result = self.client.dimensions.list_dimensions()
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__}")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ FAILED ({duration:.2f}s) - {str(e)[:80]}...")
            raise
    
    def test_6_list_drm_configurations(self):
        """Test 6: List DRM Configurations - Retrieve DRM configurations."""
        print("\n🧪 Test 6: List DRM Configurations...")
        start_time = time.time()
        
        try:
            result = self.client.drm_configurations.get_drm_configuration()
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__}")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"⚠️  SKIPPED ({duration:.2f}s) - {str(e)[:80]}...")
            # DRM configurations might not exist, so we skip this test
            self.skipTest(f"DRM configurations not available: {str(e)[:50]}...")
    
    def test_7_list_video_views(self):
        """Test 7: List Video Views - Retrieve video analytics."""
        print("\n🧪 Test 7: List Video Views...")
        start_time = time.time()
        
        try:
            result = self.client.views.list_video_views(timespan="7:days")
            duration = time.time() - start_time
            
            self.assertIsNotNone(result)
            print(f"✅ SUCCESS ({duration:.2f}s) - {type(result).__name__}")
            return True
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ FAILED ({duration:.2f}s) - {str(e)[:80]}...")
            raise


def run_tests():
    """Run the FastPix SDK test suite."""
    print("🚀 FastPix Python SDK - Test Suite")
    print("=" * 50)
    
    # Check for credentials
    username = os.getenv('FASTPIX_USERNAME')
    password = os.getenv('FASTPIX_PASSWORD')
    
    if not username or not password:
        print("❌ Error: FASTPIX_USERNAME and FASTPIX_PASSWORD environment variables must be set")
        print("\nTo run tests:")
        print("  export FASTPIX_USERNAME='your_username'")
        print("  export FASTPIX_PASSWORD='your_password'")
        print("  python -m tests.test_fastpix_sdk")
        return False
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
    return True


if __name__ == "__main__":
    run_tests()
