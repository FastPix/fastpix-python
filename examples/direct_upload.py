"""Direct upload: create an upload URL to push a local file, PUT the file to the
returned url, then list and cancel pending uploads."""

import json
import os

from fastpix_python import Fastpix, models


def _print(label, res):
    print(f"\n=== {label} ===")
    print(json.dumps(res.model_dump(mode="json", by_alias=True, exclude_unset=True), indent=2, default=str))


def main():
    fastpix = Fastpix(
        security=models.Security(
            username=os.getenv("FASTPIX_USERNAME"),
            password=os.getenv("FASTPIX_PASSWORD"),
        ),
    )
    with fastpix:
        # 1. Create a direct upload. `cors_origin` "*" allows a browser upload from any origin.
        upload = fastpix.input_video.direct_upload_video_media(request={
            "cors_origin": "*",
            "push_media_settings": {
                "access_policy": "public",
                "metadata": {"key1": "value1"},
            },
        })
        _print("create upload", upload)

        upload_id = upload.data.upload_id
        # 2. Upload your file with an HTTP PUT to the returned url, e.g.:
        #    requests.put(upload.data.url, data=open("video.mp4", "rb"),
        #                 headers={"Content-Type": "application/octet-stream"})
        print(f"\nPUT your file to: {upload.data.url}")

        # 3. List uploads and cancel this one if it hasn't started.
        _print("list uploads", fastpix.manage_videos.list_uploads(limit=20, offset=1, order_by="desc"))
        _print("cancel upload", fastpix.manage_videos.cancel_upload(upload_id=str(upload_id)))


if __name__ == "__main__":
    main()
