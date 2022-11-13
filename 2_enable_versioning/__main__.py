"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3
import getpass


config = Config()
bucket_config = config.require_object("bucket")
stack = get_stack()
user = getpass.getuser()

bucket = s3.Bucket(
    f"{bucket_config['name']}-{stack}",
    bucket=f"{bucket_config['name']}-{stack}-{user}" if bucket_config['fixed'] else None,
    versioning=s3.BucketVersioningArgs(enabled=bucket_config["versioning"]["enabled"]),
)

export("bucket_name", bucket.id)
