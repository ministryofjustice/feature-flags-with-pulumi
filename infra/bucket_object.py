from pulumi import Config, export, get_stack, FileAsset, Output
from pulumi_aws.s3 import (
    BucketObject,
)

from bucket import bucket

config = Config()
bucket_config = config.require_object("bucket")
bucket_object_config = config.get_object("bucket_object", {})
stack = get_stack()


bucketObject = BucketObject(
    "index.html",
    acl=bucket_object_config.get("acl"),
    content_type="text/html",
    bucket=bucket.id,
    source=FileAsset(f"{stack}/index.html"),
)

export("bucket_endpoint", Output.concat("http://", bucket.website_endpoint))
