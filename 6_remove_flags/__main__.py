"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3
import getpass

config = Config()
stack = get_stack()
user = getpass.getuser()


cors_config = config.require_object("cors")
cors_rules = [s3.BucketCorsRuleArgs(
    allowed_headers=["*"],
    allowed_methods=[
        "PUT",
        "POST",
    ],
    allowed_origins=cors_config["allowed_origins"],
    expose_headers=["ETag"],
    max_age_seconds=cors_config["max_age_seconds"],
    )]

bucket_config = config.require_object("buckets")
buckets = []
for bucket in bucket_config:
    resource = s3.Bucket(
        f"{bucket['name']}-{stack}",
        bucket=f"{bucket['name']}-{stack}-{user}" if bucket["fixed"] else None,
        versioning=s3.BucketVersioningArgs(enabled=bucket["versioning"]["enabled"]),
        cors_rules= cors_rules
    )
    buckets.append(resource)

for bucket_name, bucket in zip(bucket_config, buckets):
    export(f"{bucket_name}-name", bucket.id)
