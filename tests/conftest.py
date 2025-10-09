"""Test configuration and fixtures for FastPix SDK tests."""

import os
import sys
from typing import Optional

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Fastpix import Fastpix
from Fastpix.models import Security


def get_fastpix_client() -> Optional[Fastpix]:
    """Get a configured FastPix client for testing."""
    username = os.getenv('FASTPIX_USERNAME')
    password = os.getenv('FASTPIX_PASSWORD')
    
    if not username or not password:
        return None
    
    security = Security(username=username, password=password)
    return Fastpix(security=security)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
