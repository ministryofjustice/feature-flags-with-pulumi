from pulumi import Config

config = Config()
feature_flags = config.get_object("feature_flags", [])

import bucket
import bucket_object
import bucket_policy
