"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3

config = Config()
data = config.require_object("data")
stack = get_stack()

bucket = s3.Bucket(f"{data['bucket']}-{stack}")

export("bucket_name", bucket.id)
