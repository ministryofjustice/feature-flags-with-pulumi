"""An AWS Python Pulumi program"""

from pulumi import Config, export, get_stack
from pulumi_aws import s3

config = Config()
data = config.require_object("data")
use_new_infrastructure = data['use_new_infrastructure']
stack = get_stack()

if use_new_infrastructure:
    buckets = []
    for bucket in data["buckets"]:
        buckets.append(s3.Bucket(f"{bucket}-{stack}"))
else:
    bucket = s3.Bucket(f"{data['bucket']}-{stack}")

if use_new_infrastructure:
    for bucket_name,bucket in zip(data["buckets"],buckets):
        export(f"{bucket_name}-name", bucket.id)
else:
    export("bucket_name", bucket.id)
