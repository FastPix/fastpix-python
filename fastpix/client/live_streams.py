from fastpix.utilis.exceptions import APIError
from fastpix.client.api import make_request
from fastpix.utilis.utilis import validate_uuid, validate_request_body


class Livestream:
    def __init__(self, client):
        self.client = client
    
    def create(self, data):
        """Create a live stream."""

        validate_request_body(data)  # validating request body is valid json or not

        try:
            return make_request(
                method="POST", 
                endpoint="/live/streams", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()
    
    def list(self, params=None):
        """Retrieve all live streams."""

        try:
            return make_request(
                method="GET", 
                endpoint="/live/streams", 
                headers=self.client.headers,
                params=params
            )
        except APIError as e:
            return e.to_dict()
    
    def get(self, stream_id):
        """Retrieve a specific live stream by ID."""

        validate_uuid(stream_id)  # validating stream_id
        
        try:
            return make_request(
                method="GET", 
                endpoint=f"/live/streams/{stream_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()
    
    def update(self, stream_id, data):
        """Update a specific live stream."""
        
        validate_uuid(stream_id) # validating stream_id
        validate_request_body(data)  # validating request body is valid json or not
        
        try:
            return make_request(
                method="PATCH", 
                endpoint=f"/live/streams/{stream_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()
    
    def delete(self, stream_id):
        """Delete a specific live stream."""
        
        validate_uuid(stream_id)  # validating stream_id
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/live/streams/{stream_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()
    
    def create_simulcast(self, stream_id, data):
        """Create a simulcast for a live stream."""
        
        validate_uuid(stream_id) # validating stream_id 
        validate_request_body(data) # validating request body as valid json body or not
        
        try:
            return make_request(
                method="POST", 
                endpoint=f"/live/streams/{stream_id}/simulcast", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()
    
    def get_simulcast(self, stream_id, simulcast_id):
        """Retrieve a specific simulcast."""

        if simulcast_id is None:
            raise ValueError("Simulcast ID must be provided.")

        validate_uuid(stream_id)  # validating stream_id 

        try:
            return make_request(
                method="GET", 
                endpoint=f"/live/streams/{stream_id}/simulcast/{simulcast_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()
    
    def update_simulcast(self, stream_id, simulcast_id, data):
        """Update a specific simulcast."""
        
        if simulcast_id is None:
            raise ValueError("Simulcast ID must be provided.")

        validate_uuid(stream_id)  # validating stream_id 
        validate_request_body(data)  # validating request body as valid json body or not
        
        try:
            return make_request(
                method="PUT", 
                endpoint=f"/live/streams/{stream_id}/simulcast/{simulcast_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()
    
    def delete_simulcast(self, stream_id, simulcast_id):
        """Delete a specific simulcast."""
        
        if simulcast_id is None:
            raise ValueError("Simulcast ID must be provided.")

        validate_uuid(stream_id)  # validating stream_id
        
        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/live/streams/{stream_id}/simulcast/{simulcast_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()
            