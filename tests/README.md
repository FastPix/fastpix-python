# FastPix Python SDK Test Suite

This directory contains the test suite for the FastPix Python SDK.

## 🚀 Quick Start

### Prerequisites

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Credentials**
   
   **Option 1: Environment Variables (Recommended)**
   ```bash
   export FASTPIX_USERNAME="your_username"
   export FASTPIX_PASSWORD="your_password"
   ```
   
   **Option 2: Command Line Arguments**
   ```bash
   python run_tests.py --username your_username --password your_password
   ```

### Running Tests

**Run All 7 Tests (Single Command)**
```bash
python run_tests.py
```

**Run Tests with Verbose Output**
```bash
python run_tests.py --verbose
```

**Run Tests Directly**
```bash
python -m tests.test_fastpix_sdk
```

## 📊 Test Cases

The test suite includes 7 core functionality tests:

1. **List Media** - Test media file retrieval
2. **List Live Streams** - Test live stream management
3. **List Playlists** - Test playlist functionality
4. **List Signing Keys** - Test signing key management
5. **List Dimensions** - Test analytics dimensions
6. **List DRM Configurations** - Test DRM configuration (may be skipped if none exist)
7. **List Video Views** - Test video analytics

## 🎯 Expected Results

- **6-7 tests should pass** (85-100% success rate)
- **DRM test may be skipped** if no DRM configurations exist (expected)
- **All other tests should pass** if credentials are valid

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FASTPIX_USERNAME` | Your FastPix username | Yes |
| `FASTPIX_PASSWORD` | Your FastPix password | Yes |

## 📝 Test Structure

- `test_fastpix_sdk.py` - Main test file with 7 test cases
- `conftest.py` - Test configuration and fixtures
- `run_tests.py` - Test runner script
- `README.md` - This documentation

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify username/password are correct
   - Check if credentials have proper permissions

2. **Import Errors**
   - Ensure FastPix SDK is installed
   - Check Python path and virtual environment

3. **Network Errors**
   - Check internet connection
   - Verify API endpoint accessibility

## 📈 Success Criteria

- **100% Pass Rate**: All endpoints working correctly
- **85%+ Pass Rate**: Most functionality working (DRM may be skipped)
- **<85% Pass Rate**: Significant issues requiring attention
