from pulumi import Config, export, get_stack, FileAsset, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
bucket_config = config.require_object("bucket")
stack = get_stack()

bucket = Bucket(
    f"{bucket_config['name']}-{stack}",
    website=BucketWebsiteArgs(
        index_document="index.html",
    ),
)

export("bucket_name", bucket.id)
