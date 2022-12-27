from pulumi import Config, export, get_stack, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
bucket_config = config.require_object("bucket")
feature_flags = config.get_object("feature_flags", {})
stack = get_stack()

bucketWebsiteArgs = None
if feature_flags.get("bucket_object"):
    bucketWebsiteArgs = BucketWebsiteArgs(
        index_document="index.html",
    )

bucket = Bucket(f"{bucket_config['name']}-{stack}", website=bucketWebsiteArgs)

export("bucket_name", bucket.id)
if feature_flags.get("bucket_object"):
    export("bucket_endpoint", Output.concat("http://", bucket.website_endpoint))
