from pulumi import Config

config = Config()
feature_flags = config.get_object("feature_flags", [])
bucket_object_config = config.get_object("bucket_object", {})

import bucket

if bucket_object_config:
    import bucket_object

if "bucket_policy_flag" in feature_flags:
    import bucket_policy
