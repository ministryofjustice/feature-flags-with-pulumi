from pulumi import Config

config = Config()
feature_flags = config.get("feature_flags", [])


from bucket import bucket

if "bucket_object_flag" in feature_flags:
    from bucket_object import bucketObject
