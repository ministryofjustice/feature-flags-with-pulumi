# Feature Flags (AKA Toggles) with Pulumi

## Introduction

Feature flags (or toggles) is a software engineering technique which has many [advantages](https://martinfowler.com/articles/feature-toggles.html). Feature flags can help to:

- Limit long-living feature branches
- Encourage developers to commit early and often
- Highlight issues earlier in the development cycle
- Disable features or resources which are causing issues

However, as with any design patterns, feature flags introduce complexity and need to be handled carefully:

- Having too many feature flags can be confusing, so they should be used sparingly
- You need to be diligent to remove feature flags once the feature has been fully enabled

Feature flags can be used with [IAC (Infrastructure As Code)](https://en.wikipedia.org/wiki/Infrastructure_as_code) projects and has been used with [Terraform](https://build5nines.com/terraform-feature-flags-environment-toggle-design-patterns/). This repo demos how and when to use feature flags with [pulumi](https://www.pulumi.com/docs/). This demo is relevant to pulumi projects using [GitHub-Flow](https://docs.github.com/en/get-started/quickstart/github-flow) for branch management, with a single main branch which is sequentially deployed to the different pulumi stacks once feature branches are merged in. Feature flags are [recommended by GitHub](https://github.blog/2021-04-27-ship-code-faster-safer-feature-flags/) when using GitHub flow.

Pulumi is also compatible with [Git-Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) for branch management, with one [branch-per-stack](https://www.pulumi.com/docs/guides/continuous-delivery/). However, feature flags are less relevant to Git-Flow because changes can be independently deployed to the different environments as code is promoted to the different branches. It can also be difficult to remove feature flags from multiple branches.

This repo uses an AWS python project with a simple S3 bucket example but the concepts could be applied to other languages. The example is somewhat contrived to simplify the code, but should help as a basis for applying to more complex, real-life examples. The process for automating the deployment changes is also out-of-scope for the sake of clarity.

This repo assumes you are already familiar with pulumi and specifically the pulumi [Bucket](https://www.pulumi.com/registry/packages/aws/api-docs/s3/bucket/) resource. You'll need to have access to an AWS account to deploy the bucket, however you should be able to follow the explanation without deploying to AWS. 

## Structure

The repo uses a monolithic project named `infra`, but the concepts are compatible with micro-stacks (see [Organizing Projects and Stacks](https://www.pulumi.com/docs/guides/organizing-projects-stacks/) for more details). In fact, having micro-stacks makes it easier to manage multiple feature flags.
 
The repo deploys resources against only two stacks/environments for simplicity: `dev` and `prod`, but the concepts are compatible with more than 2 stacks.

The repo is split up into multiple directories. All directories refer to the same `infra` pulumi project and deploy to the same `dev` and `prod` stacks. The directories are supposed to show the state of the code after a feature branch has been merged to main. The prefix indicates the order of the stages. I could have changed the structure of the project as follows and saved each stage as a separate commit:

```
|- infra
|   |- __main__.py
|   |- Pulumi.dev.yaml
|   |- Pulumi.prod.yaml
|   |- Pulumi.yaml
|- README.md
|- requirements.txt
```

However I thought it was easier to switch between directories instead of switching between commits.

The repo defines the feature flags in the pulumi stack [config](https://www.pulumi.com/docs/intro/concepts/config/) files `Pulumi.<stack-name>.yml`. The feature flags are stored under the feature_flags object. This means all feature flags are stored in one location per stack and can be tracked more easily. If undefined, the code assumes the feature flags are disabled to ensure features are not deployed to `prod` by mistake.

## Explanation

### 1. Create bucket

At this stage the service consists of a single bucket which has been created in both stacks.

Running a `pulumi up` prints the following output:

<details>
  <summary>Click me</summary>

    Updating (dev):
        Type                 Name           Status      
    +   pulumi:pulumi:Stack  infra-dev      created     
    +   └─ aws:s3:Bucket     my-bucket-dev  created
     
    Outputs:
        bucket_name: "my-bucket-dev-9be74da"

    Resources:
        + 2 created

</details>

and similarly for the prod stack.

### 2. Modify bucket

The service still consists of a single bucket, but the bucket properties on the `dev` have been updated:
  
- Versioning is enabled. Since versioning is disabled by default, you can deploy the change to `dev` only by setting `enabled` to `False`.

- Cross-account resource sharing [CORS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cors.html) is enabled. You can deploy the changes to `dev` only by conditioning on the existence of the `cors` variable.

Note that this was achieved **without** using feature flags. You should avoid using feature flags if you can achieve the same objective using config variables.

Running a `pulumi up` shows that the bucket properties are updated in `dev` but no changes are detected in `prod`:

<details>
  <summary>Click me</summary>



</details>

### 3. Multiple buckets

The service now needs two buckets, and uses the `multiple_buckets` feature flag to make sure the change is only deployed to `dev`.

Note that you could have achieved the same result without using 

Running a `pulumi up` shows that a second bucket is created in `dev` but no changes are detected in `prod`:

<details>
  <summary>Click me</summary>



</details>

### 4. Deploy features to `prod`

During testing you realised that the CORS allowed origin should be restricted to a single origin for security reasons. 

Note that you in a real-life example you should deploy the features independently.

Running a `pulumi up` shows that two buckets are created in `prod` but no changes are detected in `dev`:

<details>
  <summary>Click me</summary>



</details>

### 5. Remove the feature flags

All new features have been tested and reviewed in `prod` and the feature flags have now been removed.

This time, neither stacks show any changes when running a `pulumi up`.
