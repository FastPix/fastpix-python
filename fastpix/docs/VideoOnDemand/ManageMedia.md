# Manage Media Methods

To manage your media assets, the **`media_id`** is the mandatory parameter required for most methods. This `media_id` is the unique identifier for a media asset and is generated during the media upload process.

- If you upload a media asset using **`client.media.create_pull_video()`**, the `id` of the media asset is returned as part of the response.
- If you upload a media asset from a local device using **`client.media.get_presigned_url()`**, the `uploadId` is returned as part of the response.

---

# Method: client.media.get_all_media()

The `client.media.get_all_media()` method allows you to fetch a list of all media assets. This method accepts three optional parameters: `limit`, `offset`, and `orderBy`. If not provided, the method will use the default values for these parameters.

### Parameters Details:

| **Parameter** | **Description**                                                                            | **Type** | **Default Value** | **Accepted Values**                         |
| ------------- | ------------------------------------------------------------------------------------------ | -------- | ----------------- | ------------------------------------------- |
| `limit`       | Specifies the maximum number of items to display per page.                                 | `Number` | `10`              | 1 to 50                                     |
| `offset`      | Determines the starting point for data retrieval in a paginated list.                      | `Number` | `1`               | Any positive integer (e.g., `1`, `5`, `10`) |
| `orderBy`     | Sorts the values in the list. The values can be arranged in descending or ascending order. | `String` | `desc`            | `"desc"`, `"asc"`                           |

### Example Request:

```python
# Note for Async SDK Users: When using the AsyncClient, all API methods must be prefixed with the await keyword. 
# For example: await client.media.get_all_media(media_asset_request_params)

# Define the parameters for fetching media assets in a separate variable.
media_asset_request_params = {
    "limit": 10,  # Number of media assets to fetch in one request.
    "offset": 1,  # Starting position for the list of media assets (useful for pagination).
    "orderBy": "desc",  # Sort order for the media assets ("desc" for descending, "asc" for ascending).
}

# Assuming `client` is already initialized with the proper credentials
all_media_assets = client.media.get_all_media(media_asset_request_params)

# Print the fetched media assets
print("All Media Assets:", all_media_assets)
```

---

# Method: client.media.get_by_mediaId()

The `client.media.get_by_mediaId()` method allows you to retrieve a specific media asset by its unique `media_id`. You must provide the `media_id` of the asset you want to fetch.

### Parameters Details:

| **Parameter**        | **Description**                                                                                | **Type** | **Required** | **Accepted Values**                |
| -------------------- | ---------------------------------------------------------------------------------------------- | -------- | ------------ | ---------------------------------- |
| `media_id` (required) | The unique identifier assigned to the media asset. It can contain a maximum of 255 characters. | `String` | Yes          | Any valid string (up to 255 chars) |

### Example Request:

```python
# Define the parameter for fetching a specific media asset by ID.
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

get_media_asset = client.media.get_by_mediaId(media_id)

# Print the retrieved media asset by ID
print("Retrieved media asset by ID:", get_media_asset)
```

---

# Method: client.media.update()

The `client.media.update()` method allows you to update metadata or other properties of a specific media asset. You must provide the `media_id` of the asset you wish to update, along with the metadata or other fields to be updated.

### Parameters Details:

| **Parameter**         | **Description**                                                                                | **Type** | **Accepted Values**                |
| --------------------- | ---------------------------------------------------------------------------------------------- | -------- | ---------------------------------- |
| `media_id` (required)  | The unique identifier assigned to the media asset. It can contain a maximum of 255 characters. | `String` | Any valid string (up to 255 chars) |
| `metadata` (required) | Metadata key-value pairs to be updated for the media asset.                                    | `Object` | Key-value pairs (max 10 entries)   |

### Metadata Object

| **Parameter** | **Description**                                                | **Type** | **Accepted Values**                |
| ------------- | -------------------------------------------------------------- | -------- | ---------------------------------- |
| `key`         | A key for the metadata entry (max 255 characters).             | `String` | Any string (up to 255 characters). |
| `value`       | The value for the specified metadata key (max 255 characters). | `String` | Any string (up to 255 characters). |

You can add up to 10 metadata entries to the `metadata` object. Each entry is a key-value pair. This allows you to tag your media asset for easier identification or categorization.

### Example Request:

```python
# Define the parameter for specifying the media asset to be updated.
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

# Define the payload with the updates to be applied to the media asset.
update_payload = {
    "metadata": {
        "key": "value",  # Replace "key" and "value" with actual metadata keys and values
    },
}

update_media_asset = client.media.update(media_id , update_payload)

# Print the updated media asset details
print("Updated Media Asset:", update_media_asset)
```

---

# Method: client.media.delete()

The `client.media.delete()` method allows you to delete a specific media asset by its unique ID. You must provide the `media_id` of the asset to delete.

### Parameters Details:

| **Parameter**        | **Description**                                                                                | **Type** | **Accepted Values**                     |
| -------------------- | ---------------------------------------------------------------------------------------------- | -------- | --------------------------------------- |
| `media_id` (required) | The unique identifier assigned to the media asset. It can contain a maximum of 255 characters. | `String` | Any valid string (up to 255 characters) |

### Example Request:

```python
#Define the parameter for specifying the media asset to be deleted.
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

# Assuming `client` is already initialized with the necessary credentials
delete_media_asset = client.media.delete(media_id)

# Print the response indicating the media asset has been deleted
print("Deleted Media Asset:", delete_media_asset)
```

---

# Method: client.media.get_media_info()

The `client.media.get_media_info()` method allows you to retrieve detailed information about the media inputs associated with a specific media asset. You can use this endpoint to verify the media file’s input URL, track creation status, and container format. The `media_id` (either `uploadId` or `id`) must be provided to fetch the information.

### Parameters Details:

| **Parameter**        | **Description**                                                                                | **Type** | **Accepted Values**                     |
| -------------------- | ---------------------------------------------------------------------------------------------- | -------- | --------------------------------------- |
| `media_id` (required) | The unique identifier assigned to the media asset. It can contain a maximum of 255 characters. | `String` | Any valid string (up to 255 characters) |

### Example Request:

```python
#Define the parameter for specifying the media asset whose info is to be retrieved.
media_id = "media_id"  # Unique identifier for the media asset to be retrieved

get_media_info =  client.media.get_media_info(media_id)
print("Media Asset Info:", get_media_info)
```
