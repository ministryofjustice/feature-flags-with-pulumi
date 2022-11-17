"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3

config = Config()
bucket_config = config.require_object("bucket")
stack = get_stack()

bucket = s3.Bucket(f"{bucket_config['name']}-{stack}")

export("bucket_name", bucket.id)
