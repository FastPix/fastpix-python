# DirectUploadVideoMediaRequest

Request body for direct upload


## Fields

| Field                                                                             | Type                                                                              | Required                                                                          | Description                                                                       | Example                                                                           |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `cors_origin`                                                                     | *str*                                                                             | :heavy_check_mark:                                                                | Upload media directly from a device using the URL name or enter '*' to allow all. | *                                                                                 |
| `push_media_settings`                                                             | [Optional[models.PushMediaSettings]](../models/pushmediasettings.md)              | :heavy_minus_sign:                                                                | Configuration settings for media upload.                                          |                                                                                   |