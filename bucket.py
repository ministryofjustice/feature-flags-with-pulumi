from pulumi import Config, export, get_stack, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
feature_flags = config.get_object("feature_flags", [])
aws_config = Config("aws")
region = aws_config.require("region")
stack = get_stack()


web_bucket = Bucket(
    f"s3-website-bucket-{stack}-{region}",
    website=BucketWebsiteArgs(index_document="index.html")
    if "website_flag" in feature_flags
    else None,
)

export("bucket_name", web_bucket.id)
if "website_flag" in feature_flags:
    export("website_url", Output.concat("http://", web_bucket.website_endpoint))
