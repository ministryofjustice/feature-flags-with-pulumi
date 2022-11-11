"""An AWS Python Pulumi program"""

from pulumi import Config, export
from pulumi_aws import s3

config = Config()
data = config.require_object("data")
use_new_infrastructure = data['use_new_infrastructure']

# Create an AWS resource (S3 Bucket)
if data.get("bucket"):
    bucket = s3.Bucket(data["bucket"])
elif data.get("buckets"):
    buckets = []
    for bucket in data["buckets"]:
        buckets.append(s3.Bucket(bucket))

# Export the name of the bucket
if use_new_infrastructure:
    for bucket_name,bucket in zip(data["buckets"],buckets):
        export(bucket_name, bucket.id)
else:
    export(data["bucket"], bucket.id)
