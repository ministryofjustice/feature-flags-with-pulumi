"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3
import getpass


config = Config()
bucket_config = config.require_object("bucket")
stack = get_stack()
user = getpass.getuser()
feature_flags = config.require_object("feature_flags")

cors_rules = None
if feature_flags["cors"]:
    cors_rules = [
        s3.BucketCorsRuleArgs(
            allowed_headers=["*"],
            allowed_methods=[
                "PUT",
                "POST",
            ],
            allowed_origins=['*'],
            expose_headers=["ETag"],
            max_age_seconds=3600,
        )
    ]

bucket = s3.Bucket(
    f"{bucket_config['name']}-{stack}",
    bucket=f"{bucket_config['name']}-{stack}-{user}"
    if bucket_config["fixed"]
    else None,
    versioning=s3.BucketVersioningArgs(enabled=bucket_config["versioning"]["enabled"]),
    cors_rules=cors_rules,
)

export("bucket_name", bucket.id)
