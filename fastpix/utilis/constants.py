BASE_URL = "https://api.fastpix.io/v1"

import re
import uuid
from typing import Any, Dict

def validate_uuid(uuid_str: str) -> bool:
    """
    Validate if the given string is a valid UUID.
    
    Args:
        uuid_str (str): The UUID string to validate
        
    Returns:
        bool: True if valid UUID, False otherwise
    """
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return str(uuid_obj) == uuid_str
    except ValueError:
        return False

def validate_request_body(body: Dict[str, Any]) -> bool:
    """
    Validate if the request body is a non-empty dictionary.
    
    Args:
        body (Dict[str, Any]): The request body to validate
        
    Returns:
        bool: True if valid request body, False otherwise
    """
    return isinstance(body, dict) and len(body) > 0
