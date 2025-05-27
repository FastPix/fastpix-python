from fastpix.utilis.exceptions import APIError
from fastpix.client.api import make_request
from fastpix.utilis.utilis import validate_uuid, validate_request_body


class MediaResource:
    def __init__(self, client):
        self.client = client
    
    def get_all_media(self, params):
        """Fetch all medias."""
        try:
            return make_request(
                method="GET", 
                endpoint="/on-demand", 
                headers=self.client.headers,
                params=params
            )
        except APIError as e:
            return e.to_dict()

    def get_by_mediaId(self, media_id):
        """Fetch media by its ID."""
        validate_uuid(media_id)  # Validate media ID
        try:
            return make_request(
                method="GET", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()

    def update(self, media_id, data):
        """Update media by its ID."""
        validate_uuid(media_id)  # Validate media ID
        validate_request_body(data)  # Validate request body

        try:
            return make_request(
                method="PATCH", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            return e.to_dict()

    def delete(self, media_id):
        """Delete media by its ID."""
        validate_uuid(media_id)  # Validate media ID

        try:
            return make_request(
                method="DELETE", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()

    def create_pull_video(self, data):
        """Create an on-demand request by calling the /on-demand endpoint."""
        endpoint = "/on-demand"
        validate_request_body(data)  # Validate body

        if "accessPolicy" not in data:
            data["accessPolicy"] = "public"

        try:
            return make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
        except APIError as e:
            return e.to_dict()

    def get_presigned_url(self, data):
        """Create an on-demand presigned URL request by calling the /on-demand/uploads endpoint."""
        endpoint = "/on-demand/uploads"
        validate_request_body(data)  # Validate body

        if "corsOrigin" not in data:
            data["corsOrigin"] = "*"

        try:
            return make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
        except APIError as e:
            return e.to_dict()

    def get_media_info(self, media_id):
        """Retrieve media input info by media ID."""
        validate_uuid(media_id)  # Validate media ID

        try:
            endpoint = f"/on-demand/{media_id}/input-info"
            return make_request(
                method="GET", 
                endpoint=endpoint, 
                headers=self.client.headers
            )
        except APIError as e:
            return e.to_dict()
