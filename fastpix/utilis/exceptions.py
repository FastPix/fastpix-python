class APIError(Exception):
    """Custom exception for API-related errors."""
    def __init__(self, message, status_code=None, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details
        
    def to_dict(self):
        return {
            "error": self.message,
            "status_code": self.status_code,
            "details": self.details,
        }
