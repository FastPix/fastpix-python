# Method: client.media_playback_ids.create()

The `client.media_playback_ids.create()` method allows you to generate a playback ID for a specific media asset. You must provide the `media_id` of the asset for which you want to generate the playback ID, and you can also configure options such as the `accessPolicy` to control the visibility of the media.

### Parameters Details:

| **Parameter**             | **Description**                                                                                                                             | **Type** | **Accepted Values**                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------- |
| `media_id` (required)      | The unique identifier assigned to the media asset. This is required to specify the media for which you want to generate a playback ID.      | `String` | Any valid string (up to 255 characters) |
| `accessPolicy` (required) | Determines if access to the streamed content is kept private or available to all. This can be set to either `public` or `private` or `drm`. | `String` | `"public"`, `"private"`, `"drm"`        |

### Example Request:

```python
# Note for Async SDK Users: When using the AsyncClient, all API methods must be prefixed with the await keyword. 
# For example: await client.playback_ids.create(media_type, media_id, playback_options)

# Define the media_id and accessPolicy dynamically
media_type = "video_on_demand"
media_id =  "media-id" # Unique identifier for the media asset.

playback_options = {
  "accessPolicy": "public", # Can be 'public' or 'private'.
}

playback_id_response = client.playback_ids.create(media_type, media_id, playback_options)

print("Playback ID Creation Response:", playback_id_response)
```

---

# Method: client.media_playback_ids.delete()

The `client.media_playback_ids.delete()` method allows you to delete a specific playback ID for a media asset. You must provide both the `media_id` (the unique identifier for the media) and the `playback_id` (the unique identifier for the playback) to delete the playback ID.

### Parameters Details:

| **Parameter**           | **Description**                                                                                      | **Type** | **Accepted Values**                     |
| ----------------------- | ---------------------------------------------------------------------------------------------------- | -------- | --------------------------------------- |
| `media_id` (required)    | The unique identifier assigned to the media asset. It can contain a maximum of 255 characters.       | `String` | Any valid string (up to 255 characters) |
| `playback_id` (required) | The unique identifier for the playback ID to be deleted. It can contain a maximum of 255 characters. | `String` | Any valid string (up to 255 characters) |

### Example Request:

```python
# Define the media_id and playback_id dynamically
media_type = "video_on_demand"
media_id = "media-id"; # The ID of the media asset for which you want to delete the playback ID.
playback_ids = ["id1", "id2"]; # The playback ID that you want to delete.

delete_playback_response = client.playback_ids.delete(media_type, media_id, playback_ids)

print("Playback ID Deletion Response:", delete_playback_response)
```
