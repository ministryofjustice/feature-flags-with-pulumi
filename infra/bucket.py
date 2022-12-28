from pulumi import Config, export, get_stack, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
bucket_name = config.require("bucket")
feature_flags = config.get_object("feature_flags", {})
stack = get_stack()

bucketWebsiteArgs = None
if feature_flags.get("public_website"):
    bucketWebsiteArgs = BucketWebsiteArgs(
        index_document="index.html",
    )

bucket = Bucket(f"{bucket_name}-{stack}", website=bucketWebsiteArgs)

export("bucket_name", bucket.id)
if feature_flags.get("public_website"):
    export("bucket_endpoint", Output.concat("http://", bucket.website_endpoint))
