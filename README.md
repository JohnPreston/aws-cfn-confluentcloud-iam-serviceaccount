# ConfluentCloud::IAM::ServiceAccount

Allows to create a new Service Account into an organization in Confluent Cloud via API.

See the [docs](./docs/README.md) for properties


## Install

### Requirements

You need

* An account on Confluent Cloud Platform
* Have a Confluent Cloud API Key
* AWS Account, and for the following installation steps, aws cli

### Confluent API Key

```bash

# Optionally create an API key via the CLI
confluent api-key create --resource cloud -o json

export API_KEY=<API KEY RETURNED>
export API_SECRET=<API SECRET RETURNED>

```

### Create a secret in AWS Secrets Manager with the API key

```bash
aws cloudformation deploy --stack-name confluent-cloud-api-credentials --template confluent-secrets.template \
  --parameter-overrides ConfluentApiKey=${API_KEY} ConfluentSecretKey=${API_SECRET}
```

### Save the secret ARN into a variable

```bash
export SECRET_ARN=`aws cloudformation describe-stack-resources --stack-name confluent-cloud-api-credentials --logical-resource-id ConfluentSecret | jq -r .StackResources[0].PhysicalResourceId`
```

### Activate the 3rd party CloudFormation resource

#### Option 1 - IAM and Resource together

Using the [activate.template](activate.template) we create IAM roles and enable the resource in the account, all at once.

```bash
aws cloudformation deploy --stack cfn-resource--confluentcloud-iam-serviceaccount --template activate.template \
  --capabilities CAPABILITY_IAM
```

This option offers the "extra security" to have a different IAM Execution role for that resource than others.


#### Option 2 - IAM first, resource separate

**Most recommended if you consider enabling multiple ConfluentCloud:: resources published**

We are going to use [cfn-resources-iam-roles.template](cfn-resources-iam-roles.template) template to create the _Execution_
and _LoggingRole_ first, then use these in the [activate.template](activate.template) as parameters.

```bash
aws cloudformation deploy --stack-name iam--cfn--confluentcloud-resources --template cfn-resources-iam-roles.template \
  --capabilities CAPABILITY_IAM
```

Export the IAM Roles to env vars

```bash
EXEC_ROLE_ARN=`aws cloudformation describe-stacks --stack-name iam--cfn--confluentcloud-resources | jq -r '.Stacks[0].Outputs[] |  select(.OutputKey=="ExecutionRoleArn")' | jq -r .OutputValue`
LOGGING_ROLE_ARN=`aws cloudformation describe-stacks --stack-name iam--cfn--confluentcloud-resources | jq -r '.Stacks[0].Outputs[] |  select(.OutputKey=="CloudWatchRoleArn")' | jq -r .OutputValue`
```

Now, we activate the resource using these IAM Roles

```bash
aws cloudformation deploy --stack cfn-resource--confluentcloud-iam-serviceaccount --template activate.template \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ExecutionRoleArn=${EXEC_ROLE_ARN} LoggingRoleArn=${LOGGING_ROLE_ARN}
```

### Create a new Service account

```bash
aws cloudformation deploy --stack-name my-first-service-account --template resource-test.template \
  --parameter-overrides ConfluentCloudApiSecrets=${SECRET_ARN} ServiceAccountName=cfn-test-service-account
```

## Troubleshooting

If you are getting errors with the resource, you can see in the logs what issues occurred that lead to this issue.
With the template [activate.template](activate.template), you can see that there is a CloudWatch log group that
will be logging the code execution and so you can open an [issue](https://github.com/JohnPreston/aws-cfn-confluentcloud-iam-serviceaccount/issues) on GitHub

If at any point in the logging you'd notice information that is not supposed to be there, please notify it immediately.
With that said, as the "vendor" of that resource, we will **never** have access to these logs or anything in your account.
