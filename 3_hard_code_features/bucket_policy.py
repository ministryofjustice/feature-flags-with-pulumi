import json

from pulumi_aws.s3 import BucketPolicy

from bucket import web_bucket


def public_read_policy_for_bucket(bucket_name):
    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}/*",
                    ],
                }
            ],
        }
    )


bucket_name = web_bucket.id
bucket_policy = BucketPolicy(
    "bucket-policy",
    bucket=bucket_name,
    policy=bucket_name.apply(public_read_policy_for_bucket),
)
