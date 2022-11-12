"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3

config = Config()
data = config.require_object("data")
stack = get_stack

buckets = []
for bucket in data["buckets"]:
    buckets.append(s3.Bucket(f"{bucket}-{stack}"))

for bucket_name,bucket in zip(data["buckets"],buckets):
    export(f"{bucket_name}-name", bucket.id)
