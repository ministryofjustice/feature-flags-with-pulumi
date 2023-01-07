from pulumi import Config, export, get_stack, Output
from pulumi_aws.s3 import (
    Bucket,
    BucketWebsiteArgs,
)

config = Config()
aws_config = Config("aws")
region = aws_config.require("region")
stack = get_stack()


web_bucket = Bucket(
    f"s3-website-bucket-{stack}-{region}",
    website=BucketWebsiteArgs(index_document="index.html"),
)

export("bucket_name", web_bucket.id)
export("website_url", Output.concat("http://", web_bucket.website_endpoint))
