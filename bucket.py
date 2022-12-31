from pulumi import Config, export, get_stack, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
feature_flags = config.get("feature_flags", [])
stack = get_stack()


web_bucket = Bucket(
    f"s3-website-bucket-{stack}",
    website=BucketWebsiteArgs(index_document="index.html")
    if "public_website_flag" in feature_flags
    else None,
)

export("bucket_name", web_bucket.id)
if "public_website_flag" in feature_flags:
    export("website_url", Output.concat("http://", web_bucket.website_endpoint))
