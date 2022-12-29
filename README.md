# Feature Flags (AKA Toggles) with Pulumi

This github repository explains how to implement feature flags with a minimal AWS Python Pulumi program.

For more details please refer to the [accompanying article](https://medium.com/@soumaya-mauthoor/feature-flags-with-pulumi-df578fc9ea43).

## Optional Instructions

Please follow these steps to provision the infrastructure in this repository:

1. Set up Pulumi and AWS access as explained on the [tutorial](https://www.pulumi.com/docs/get-started/aws/begin/)
2. Checkout this GitHub repository
3. Create and activate a python environment based on the `requirements.txt`
4. Change directory to `infra` 
5. Login to your preferred Pulumi [backend](https://www.pulumi.com/docs/intro/concepts/state/)
6. `pulumi up` on all three stacks
7. Don't forget to `pulumi destroy` once you're done!
