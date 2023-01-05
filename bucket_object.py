import mimetypes
import os

from pulumi import Config, FileAsset
from pulumi_aws.s3 import BucketObject

from bucket import web_bucket

config = Config()
bucket_object_config = config.get_object("bucket_object", {})

content_dir = "www"
for file in os.listdir(content_dir):
    filepath = os.path.join(content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    bucketObject = BucketObject(
        file,
        bucket=web_bucket.id,
        source=FileAsset(filepath),
        content_type=mime_type,
        acl=bucket_object_config.get("acl"),
    )
