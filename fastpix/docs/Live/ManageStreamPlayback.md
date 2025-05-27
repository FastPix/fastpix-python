# Managing Live Stream Playback

To manage playback, you must first initiate a live stream, which will provide you with a unique `stream_id`. This `stream_id` will be used across all playback management operations, such as generating playback IDs, retrieving policies, and deleting them. Make sure to save this `stream_id` for future use.

---

# Method: client.livestream_playback_ids.create()

The `client.livestream_playback_ids.create()` method allows you to generate a playback ID for a live stream. This requires the `stream_id` of the live stream you want to generate the playback ID for, as well as the desired `accessPolicy` which controls whether the stream will be public or private.

### Parameter Details:

| **Parameter**             | **Description**                                                                                       | **Type** | **Default Value** | **Accepted Values**                   |
| ------------------------- | ----------------------------------------------------------------------------------------------------- | -------- | ----------------- | ------------------------------------- |
| `stream_id` (required)     | The unique identifier assigned to the live stream. You receive this ID when creating the live stream. | `String` | -                 | Any valid string (max 255 characters) |
| `accessPolicy` (optional) | Determines if access to the streamed content is kept private or available to all.                     | `String` | `"public"`        | `"public"`, `"private"`               |

### Example Request:

```python
# Note for Async SDK Users: When using the AsyncClient, all API methods must be prefixed with the await keyword. 
# For example: await client.playback_ids.create(media_type, stream_id, body)

# Generate a live stream playback ID for an existing stream
media_type = "livestream"
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
body = { accessPolicy: "public" }

generate_livestream_playback_id = client.playback_ids.create(media_type, stream_id, body)

print("Generated Live Stream Playback ID:", generate_livestream_playback_id)
```

---

# Method: client.livestream_playback_ids.delete()

The `client.livestream_playback_ids.delete()` method allows you to delete a specific playback ID for a live stream. To use this method, you need to provide both the `stream_id` of the live stream and the `playback_id` of the stream you wish to delete. This method will permanently remove the playback ID for that specific live stream.

### Parameter Details:

| **Parameter**           | **Description**                                                                                       | **Type** | **Accepted Values**                   |
| ----------------------- | ----------------------------------------------------------------------------------------------------- | -------- | ------------------------------------- |
| `stream_id` (required)   | The unique identifier assigned to the live stream. You receive this ID when creating the live stream. | `String` | Any valid string (max 255 characters) |
| `playback_id` (required) | The unique identifier for the playback ID associated with the live stream.                            | `String` | Any valid string (max 255 characters) |

### Example Request:

```python
# Delete a playback ID for an existing live stream
media_type = "livestream"
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
playback_id = "632029b4-7c53-4dcf-a4d3-1884c29e90f8"  # Replace with actual playback ID

delete_livestream_playback_id = client.playback_ids.delete(media_type, stream_id, playback_id)

print("Deleted Live Stream Playback ID:", delete_livestream_playback_id)
```

---

# Method: client.livestream_playback_ids.get()

The `client.livestream_playback_ids.get()` method allows you to retrieve the playback policy for a specific live stream playback ID. You need to provide both the `stream_id` of the live stream and the `playback_id` associated with that stream to fetch the playback policy.

### Parameter Details:

| **Parameter**           | **Description**                                                                                       | **Type** | **Accepted Values**                   |
| ----------------------- | ----------------------------------------------------------------------------------------------------- | -------- | ------------------------------------- |
| `stream_id` (required)   | The unique identifier assigned to the live stream. You receive this ID when creating the live stream. | `String` | Any valid string (max 255 characters) |
| `playback_id` (required) | The unique identifier for the playback ID associated with the live stream.                            | `String` | Any valid string (max 255 characters) |

### Example Request:

```python
# Retrieve the playback policy for a specific live stream playback ID
media_type = "livestream"
stream_id = "1c5e8abcc2080cba74f5d0ac91c7833e"  # Replace with the actual stream ID
playback_id = "95ce872d-0b58-44f3-be72-8ed8b97ee2c9"  # Replace with the actual playback ID

get_livestream_playback_policy = client.playback_ids.get(media_type, stream_id, playback_id)

print("Live Stream Playback Policy:", get_livestream_playback_policy)
```
