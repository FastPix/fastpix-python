import uuid
import json


def validate_uuid(id_str):
    try:
        uuid.UUID(str(id_str))
    except ValueError:
        raise ValueError(f"Invalid UUID format: {id_str}")


def validate_request_body(data):
    try:
        json.dumps(data)
    except (TypeError, ValueError):
        raise ValueError("Invalid JSON data in request body")

