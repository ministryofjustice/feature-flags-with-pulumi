"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3
import getpass

config = Config()
stack = get_stack()

buckets_config = config.require_object("buckets")

for bucket_config in buckets_config:

    cors_rules = None
    if bucket_config.get("cors"):
        cors_rules = [
            s3.BucketCorsRuleArgs(
                allowed_headers=["*"],
                allowed_methods=bucket_config["cors"]["allowed_methods"],
                allowed_origins=bucket_config["cors"]["allowed_origins"],
                expose_headers=["ETag"],
                max_age_seconds=3600,
            )
        ]

    bucket = s3.Bucket(
        f"{bucket_config['name']}-{stack}",
        versioning=s3.BucketVersioningArgs(
            enabled=bucket_config["versioning"]["enabled"]
        ),
        cors_rules=cors_rules,
    )

    export(bucket_config["name"], bucket.id)
