import mimetypes
import os

from pulumi import Config, FileAsset
from pulumi_aws.s3 import BucketObject

from bucket import web_bucket

config = Config()
bucket_object_config = config.get_object("bucket_object", {})

content_version = bucket_object_config.get('version','')
content_dir = f"www{content_version}"
for file in os.listdir(content_dir):
    filepath = os.path.join(content_dir, file)
    mime_type, _ = mimetypes.guess_type(filepath)
    bucket_object = BucketObject(
        file,
        bucket=web_bucket.id,
        source=FileAsset(filepath),
        content_type=mime_type,
        acl=bucket_object_config.get("acl"),
    )
