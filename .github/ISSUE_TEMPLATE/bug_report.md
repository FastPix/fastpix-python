---
name: Bug Report
about: Report a bug or unexpected behavior in the FastPix Python SDK
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''
---

# Bug Report

Thank you for taking the time to report a bug with the FastPix Python SDK. To help us resolve your issue quickly and efficiently, please provide the following information:

## Description
**Clear and concise description of the bug:**
```
<!-- Please provide a detailed description of what you're experiencing -->
```

## Environment Information

### System Details
- **Python Version:** [e.g., 3.8, 3.9, 3.10, 3.11, 3.12]
- **Operating System:** [e.g., Windows 10, macOS 12.0, Ubuntu 20.04, etc.]
- **Package Manager:** [e.g., pip, poetry, conda]

### SDK Information
- **FastPix Python SDK Version:** [e.g., 1.0.3, 1.0.2, etc.]
- **Python Environment:** [e.g., venv, virtualenv, conda, etc.]

## Reproduction Steps

1. **Setup Environment:**
   ```bash
   pip install fastpix-python
   # or
   poetry add fastpix-python
   ```

2. **Code to Reproduce:**
   ```python
   # Please provide a minimal, reproducible example
   from fastpix import FastpixSDK
   from fastpix.models.components import Security

   fastpix = FastpixSDK(
       security=Security(
           username="your-username",
           password="your-password"
       )
   )

   # Your code here that causes the issue
   ```

3. **Expected Behavior:**

    ```
    <!-- Describe what you expected to happen -->
    ```

4. **Actual Behavior:**

    ```
    <!-- Describe what actually happened -->
    ```

5. **Error Messages/Logs:**
   ```
   <!-- Paste any error messages, stack traces, or logs here -->
   ```

## Debugging Information

### Console Output
```
<!-- Paste the complete console output here -->
```

### Error Stack Traces
```python
# Complete stack trace for Python errors
Traceback (most recent call last):
  File "/path/to/your/file.py", line 45, in <module>
    result = fastpix.some_method()
  File "/path/to/fastpix/file.py", line 123, in some_method
    raise ValueError("Error message")
ValueError: Error message
```

### HTTP Requests
```http
# Raw HTTP request (remove sensitive headers and credentials)
POST /api/endpoint HTTP/1.1
Host: [FastPix API endpoint]
Authorization: Basic ***
Content-Type: application/json

<!-- Remove credentials and sensitive headers before pasting -->
```

### Screenshots
```
<!-- If applicable, please attach screenshots that help explain your issue -->
```

## Additional Context

### Configuration
```python
# Please share your SDK configuration (remove sensitive information)
from fastpix import FastpixSDK
from fastpix.models.components import Security

fastpix = FastpixSDK(
    security=Security(
        username="***",  # Redacted
        password="***"   # Redacted
    ),
    # Any other configuration options
)
```

### Workarounds
```
<!-- If you've found any workarounds, please describe them here -->
```

## Priority
Please indicate the priority of this bug:

- [ ] Critical (Blocks production use)
- [ ] High (Significant impact on functionality)
- [ ] Medium (Minor impact)
- [ ] Low (Nice to have)

## Checklist
Before submitting, please ensure:

- [ ] I have searched existing issues to avoid duplicates
- [ ] I have provided all required information
- [ ] I have tested with the latest SDK version
- [ ] I have removed any sensitive information (credentials, API keys, etc.)
- [ ] I have provided a minimal reproduction case
- [ ] I have checked the documentation

---

**Thank you for helping improve the FastPix Python SDK! 🚀**

