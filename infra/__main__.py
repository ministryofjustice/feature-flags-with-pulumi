"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3


config = Config()
bucket_config = config.require_object("bucket")
stack = get_stack()

cors_rules = None
if bucket_config.get("cors"):
    cors_rules = [
        s3.BucketCorsRuleArgs(
            allowed_headers=["*"],
            allowed_methods=bucket_config["cors"]["allowed_methods"],
            allowed_origins=["*"],
            expose_headers=["ETag"],
            max_age_seconds=3600,
        )
    ]

bucket = s3.Bucket(
    f"{bucket_config['name']}-{stack}",
    versioning=s3.BucketVersioningArgs(enabled=bucket_config["versioning"]["enabled"]),
    cors_rules=cors_rules,
)

export("bucket_name", bucket.id)
