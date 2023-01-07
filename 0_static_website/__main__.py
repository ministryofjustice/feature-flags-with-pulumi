from pulumi import Config, export, get_stack, Output, FileAsset
from pulumi_aws.s3 import (
    Bucket,
    BucketObject,
    BucketWebsiteArgs,
)

config = Config()
aws_config = Config("aws")
region = aws_config.require("region")
stack = get_stack()


web_bucket = Bucket(
    f"s3-website-bucket-{stack}-{region}",
    website=BucketWebsiteArgs(
        index_document="index.html",
    ),
)

bucket_object = BucketObject(
    "index.html",
    bucket=web_bucket.id,
    source=FileAsset("index.html"),
    content_type="text/html",
    acl="public-read",
)

export("bucket_name", web_bucket.id)
export("website_url", Output.concat("http://", web_bucket.website_endpoint))
