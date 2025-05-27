from fastpix.utilis.exceptions import APIError
from fastpix.async_client.api import make_request
from fastpix.utilis.utilis import validate_uuid, validate_request_body


class MediaResource:
    def __init__(self, client):
        self.client = client
    
    async def get_all_media(self, params):
        """Fetch all medias."""
        try:
            return await make_request(
                method="GET", 
                endpoint="/on-demand", 
                headers=self.client.headers,
                params=params
            )
        except APIError as e:
            return e.to_dict()

    async def get_by_mediaId(self, media_id):
        """Fetch media by its ID."""
        
        validate_uuid(media_id)  # validating media id
        
        try:
            return await make_request(
                method="GET", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()

    async def update(self, media_id, data):
        """Update media by its ID."""
        
        validate_uuid(media_id)  # validating media id 
        validate_request_body(data)  # validating request body is valid json or not
        
        try:
            return await make_request(
                method="PATCH", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()

    async def delete(self, media_id):
        """Delete media by its ID."""
        
        validate_uuid(media_id)  # validating media id
        
        try:
            return await make_request(
                method="DELETE", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()

    async def create_pull_video(self, data):
        """Create an on-demand request by calling the /on-demand endpoint."""
        endpoint = "/on-demand"

        validate_request_body(data) # validating body
        
        if "accessPolicy" not in data:
            data["accessPolicy"] = "public"
        
        try:
            response = await make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
            return response
        except APIError as e:
            return e.to_dict()

    async def get_presigned_url(self, data):
        """Create an on-demand presigned URL request by calling the /on-demand/uploads endpoint."""
        endpoint = "/on-demand/uploads"

        validate_request_body(data) # validating body
        
        if "corsOrigin" not in data:
            data["corsOrigin"] = "*"
        
        try:
            response = await make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
            return response
        except APIError as e:
            return e.to_dict()
    
    async def get_media_info(self, media_id):
        """Retrieve media input info by media ID."""
        endpoint = f"/on-demand/{media_id}/input-info"
        
        validate_uuid(media_id)  # validating media id
        
        try:
            response = await make_request(
                method="GET", 
                endpoint=endpoint, 
                headers=self.client.headers
            )
            return response
        except APIError as e:
            return e.to_dict()
            