# FastPix Python SDK Samples

This directory contains sample code demonstrating how to integrate with each FastPix API. Each sample focuses on common use cases and best practices.

## Sample Files

- [media_api_samples.py](media_api_samples.py) - Media management, playlists, and content operations
- [live_api_samples.py](live_api_samples.py) - Live streaming and real-time broadcasting
- [video_data_api_samples.py](video_data_api_samples.py) - Analytics and performance monitoring
- [ai_features_samples.py](ai_features_samples.py) - AI-powered content enhancement
- [security_samples.py](security_samples.py) - Authentication and access control
- [error_handling_samples.py](error_handling_samples.py) - Comprehensive error management

## Quick Start

1. Install the FastPix Python SDK:
   ```bash
   pip install fastpix-python
   ```

2. Set up your credentials:
   ```bash
   export FASTPIX_ACCESS_TOKEN="your-access-token"
   export FASTPIX_SECRET_KEY="your-secret-key"
   ```

3. Run any sample:
   ```bash
   python samples/media_api_samples.py
   ```

## Prerequisites

- Python 3.8+
- FastPix account with valid credentials
- Internet connection for API calls

## Configuration

All samples use environment variables for credentials. Make sure to set:
- `FASTPIX_ACCESS_TOKEN`: Your FastPix access token
- `FASTPIX_SECRET_KEY`: Your FastPix secret key

Alternatively, you can modify the samples to use direct credential configuration.
