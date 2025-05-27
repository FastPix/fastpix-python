from fastpix.utilis.exceptions import APIError
from fastpix.async_client.api import make_request
from fastpix.utilis.utilis import validate_uuid, validate_request_body


class PlaybackIDs:
    def __init__(self, client):
        self.client = client

    def _get_endpoint(self, media_type, media_id):
        """Helper method to get the correct endpoint based on media type."""
        if media_type == "livestream":
            return f"/live/streams/{media_id}/playback-ids"
        elif media_type == "video_on_demand":
            return f"/on-demand/{media_id}/playback-ids"
        else:
            raise ValueError("Invalid media type. Must be 'livestream' or 'video_on_demand'.")

    async def create(self, media_type, media_id, data):
        """Create a playback ID for a media resource (livestream or video on demand)."""
        
        # Validate media_id
        validate_uuid(media_id)  # Ensure valid UUID format
        
        # Validate request body (data)
        validate_request_body(data)  # Ensure the request body is valid JSON
        
        try:
            # Get the correct endpoint based on media type
            endpoint = self._get_endpoint(media_type, media_id)

            return await make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()
    
    async def delete(self, media_type, media_id, playback_ids):
        """Delete a specific playback ID for a media resource (livestream or video on demand)."""
        
        # Validate media_id
        validate_uuid(media_id)  # Ensure valid UUID format
        
        try:
            # Get the correct endpoint based on media type
            endpoint = self._get_endpoint(media_type, media_id)

            return await make_request(
                method="DELETE", 
                endpoint=endpoint, 
                headers=self.client.headers,
                params={'playbackId': playback_ids}
            )
        except APIError as e:
            return e.to_dict()

    async def get(self, media_type, media_id, playback_id):
        """Retrieve a specific playback ID for a media resource (livestream or video on demand)."""
        
        # Validate media_id
        validate_uuid(media_id)  # Ensure valid UUID format

        if media_type == "video_on_demand":
            return {"error": "The 'get' method is not available for video_on_demand."}
    
        try:
            # Get the correct endpoint based on media type
            endpoint = self._get_endpoint(media_type, media_id) + f"/{playback_id}"

            return await make_request(
                method="GET", 
                endpoint=endpoint,
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()
