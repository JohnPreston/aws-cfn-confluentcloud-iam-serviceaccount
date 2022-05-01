# Confluent::IAMv2::ServiceAccount

Allows to create a new Service Account into an organization in Confluent Cloud via API.

See the [docs](./docs/README.md) for properties


## Requirements

You need

* An account on Confluent Cloud Platform
* Create a new API key for cloud resource, ie. as follows from CLI.

```bash
confluent api-key create --resource cloud
```

## Example

### Set up requirements

```bash

# Optionally create an API key via the CLI
confluent api-key create --resource cloud -o json

export API_KEY=THEAPIKEYRETURNED
export API_SECRET=THEAPISECRETRETURNED

aws cloudformation deploy --stack-name confluent-cloud-api-credentials --template confluent-secrets.template \
  --parameter-overrides ConfluentApiKey=${API_KEY} ConfluentSecretKey=${API_SECRET}

export SECRET_ARN=`aws cloudformation describe-stack-resources --stack-name confluent-cloud-api-credentials --logical-resource-id ConfluentSecret | jq -r .StackResources[0].PhysicalResourceId`

```

### Activate the 3rd party CloudFormation resource

```bash
aws cloudformation deploy --stack cfn-resource--confluentcloud-iam-serviceaccount --template activate.template \
  --capabilities CAPABILITY_IAM
```


### Create a new Service account

```bash
aws cloudformation deploy --stack-name my-first-service-account --template resource-test.template \
  --parameter-overrides ConfluentCloudApiSecrets=${SECRET_ARN}
```
