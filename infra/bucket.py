from pulumi import Config, export, get_stack, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
feature_flags = config.get("feature_flags", [])
stack = get_stack()

bucketWebsiteArgs = None
if "public_website_flag" in feature_flags:
    bucketWebsiteArgs = BucketWebsiteArgs(
        index_document="index.html",
    )

bucket = Bucket(f"my-bucket-{stack}", website=bucketWebsiteArgs)

export("bucket_name", bucket.id)
if "public_website_flag" in feature_flags:
    export("bucket_endpoint", Output.concat("http://", bucket.website_endpoint))
