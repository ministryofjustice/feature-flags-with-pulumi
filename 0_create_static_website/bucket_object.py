from pulumi import FileAsset
from pulumi_aws.s3 import BucketObject

from bucket import web_bucket

bucket_object = BucketObject(
    "index.html",
    bucket=web_bucket.id,
    source=FileAsset("index.html"),
    content_type="text/html",
    acl="public-read",
)
