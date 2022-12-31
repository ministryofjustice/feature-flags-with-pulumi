from pulumi import Config

config = Config()
feature_flags = config.get("feature_flags", [])


import bucket

if "bucket_object_flag" in feature_flags:
    import bucket_object

if "public_website_flag" in feature_flags:
    import bucket_policy
