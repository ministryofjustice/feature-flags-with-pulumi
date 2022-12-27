from pulumi import Config

config = Config()
feature_flags = config.get_object("feature_flags", {})


from bucket import bucket

if feature_flags.get("bucket_object"):
    from bucket_object import bucketObject
