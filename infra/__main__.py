from pulumi import Config, get_stack

config = Config()
stack = get_stack()
feature_flags = config.get_object("modules", {})

if feature_flags.get("bucket"):
    from bucket import bucket

if feature_flags.get("bucket_object"):
    from bucket_object import bucketObject
