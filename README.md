# Features Flags (AKA Toggles) with Pulumi

## Introduction

Feature flags (or toggles) is a software engineering technique which can be used with GitHub flow to limit long-living feature branches[1]. This encourages developers to commit early and often, and highlight issues earlier in the development cycle. It can also be used to easily disable features or resources which are causing issues, instead of reverting the change. 

However, as with any design patterns, feature flags need to be handled carefully. Having too many feature flags can be confusing, so they should be used sparingly. You also need to be diligent to remove feature flags once the feature has been fully enabled.

There are multiple online resources about using features flags with Terraform[2]. However I couldn't find similar resources for pulumi. This could be because pulumi encourages the use GitHub Flow[4], with a branch per stack/environment[5]. This makes the need for feature flags less relevant because changes can be independently deployed to the different environments as code is promoted to the different branches. It's also difficult to remove feature flags from multiple branches.

However, it is possible to use GitFlow, with a single main branch [6] which is sequentially deployed to the different stacks/environments once a feature is merged in. This repo explains how and when to use feature flags with a pulumi AWS python project using a simple S3 bucket example. It also calls a GitHub custom action for flagging feature flags which are obsolete.

This repo assumes you are already familiar with [infrastructure as code](), [pulumi](https://www.pulumi.com/docs/) and specifically the pulumi [Bucket](https://www.pulumi.com/registry/packages/aws/api-docs/s3/bucket/) resource. You'll need to have access to an AWS account to deploy the bucket, however you should be able to follow the explanation without deploying to AWS. 

I will not be discusing how to set up a CI/CD pipeline and the relevant best practice to limit the scope of this repository.

## Structure

The repo defines the infrastructure for a fictional service, which consists of bucket(s) for simplicity. The repo uses a monolithic project named `infra`. The repo deploys resources against two stacks/environments: `dev` and `prod` (see [Organizing Projects and Stacks](https://www.pulumi.com/docs/guides/organizing-projects-stacks/) for more details).

The repo is split up into multiple directories to show the state of the code at different stages. Think of each directory as the state of the main branch after a feature branch has been merged to main. 

All directories refer to the same `infra` pulumi project and deploy to the same `dev` and `prod` stacks.

## Explanation

### 1_before_toggle

The service consists of a single bucket. 

Pulumi up will print the following:

```
Updating (dev):
     Type                 Name           Status      
 +   pulumi:pulumi:Stack  infra-dev      created     
 +   └─ aws:s3:Bucket     my-bucket-dev  created     
 
Outputs:
    bucket_name: "my-bucket-dev-9be74da"

Resources:
    + 2 created
```

and the same for the prod stack

### Toggle Less

The service still consists of a single bucket, but versioning is now enabled on the dev stack. This is achieved without using a feature flag.

```
Updating (dev):
     Type                 Name           Status       Info
     pulumi:pulumi:Stack  infra-dev                   
 +-  └─ aws:s3:Bucket     my-bucket-dev  replaced     [diff: +bucketPrefix~versioning]
 
Outputs:
  ~ bucket_name: "my-bucket-dev-9be74da" => => "my-bucket-dev-soumaya.mauthoor"

Resources:
    +-1 replaced
    1 unchanged
```

No changes are recorded for the prod environment, even with the code changes:

```
Updating (prod):
     Type                 Name        Status     
     pulumi:pulumi:Stack  infra-prod             
 
Outputs:
    bucket_name: "my-bucket-prod-e246589"

Resources:
    2 unchanged
```

### With Toggle

The service is migrating to two buckets, which is toggle on for the dev stack only

```
Updating (dev):
     Type                 Name             Status      
     pulumi:pulumi:Stack  infra-dev                    
 +   ├─ aws:s3:Bucket     my-bucket-2-dev  created     
 +   ├─ aws:s3:Bucket     my-bucket-1-dev  created     
 -   └─ aws:s3:Bucket     my-bucket-dev    deleted     
 
Outputs:
  - bucket_name                                                                  : "my-bucket-dev-soumaya.mauthoor"
  + {'fixed': True, 'name': 'my-bucket-1', 'versioning': {'enabled': True}}-name : "my-bucket-1-dev-soumaya.mauthoor"
  + {'fixed': True, 'name': 'my-bucket-2', 'versioning': {'enabled': False}}-name: "my-bucket-2-dev-soumaya.mauthoor"

Resources:
    + 2 created
    - 1 deleted
    3 changes. 1 unchanged
```

`prod` remains unchanged and prints the same message as previous.

### Enable cross-origin resource sharing (CORS)

We optionally enable CORS on the buckets using the same variables:

```
Updating (dev):
     Type                 Name             Status      Info
     pulumi:pulumi:Stack  infra-dev                    
 ~   ├─ aws:s3:Bucket     my-bucket-2-dev  updated     [diff: ~corsRules]
 ~   └─ aws:s3:Bucket     my-bucket-1-dev  updated     [diff: ~corsRules]
 
Outputs:
    {'fixed': True, 'name': 'my-bucket-1', 'versioning': {'enabled': True}}-name : "my-bucket-1-dev-soumaya.mauthoor"
    {'fixed': True, 'name': 'my-bucket-2', 'versioning': {'enabled': False}}-name: "my-bucket-2-dev-soumaya.mauthoor"

Resources:
    ~ 2 updated
    1 unchanged
```

`prod` remains unchanged and prints the same message as previous.

### Deploy features to prod

`dev` remains unchanged, however the prod is updated:

```
Updating (prod):
     Type                 Name              Status      
     pulumi:pulumi:Stack  infra-prod                    
 +   ├─ aws:s3:Bucket     my-bucket-2-prod  created     
 +   ├─ aws:s3:Bucket     my-bucket-1-prod  created     
 -   └─ aws:s3:Bucket     my-bucket-prod    deleted     
 
Outputs:
  - bucket_name                                                                  : "my-bucket-prod-e246589"
  + {'fixed': True, 'name': 'my-bucket-1', 'versioning': {'enabled': True}}-name : "my-bucket-1-prod-soumaya.mauthoor"
  + {'fixed': True, 'name': 'my-bucket-2', 'versioning': {'enabled': False}}-name: "my-bucket-2-prod-soumaya.mauthoor"

Resources:
    + 2 created
    - 1 deleted
    3 changes. 1 unchanged
```

### Remove the flags

The flags must be removed once the features have been deployed to prod and work as expected.

This time neither stacks show any changes during deployment.

## References

[1](https://github.blog/2021-04-27-ship-code-faster-safer-feature-flags/)
