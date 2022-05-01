# ConfluentCloud::IAM::ServiceAccount

Service Account as defined in Confluent Cloud IAM v2 API.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "ConfluentCloud::IAM::ServiceAccount",
    "Properties" : {
        "<a href="#description" title="Description">Description</a>" : <i>String</i>,
        "<a href="#name" title="Name">Name</a>" : <i>String</i>,
        "<a href="#confluentcloudcredentials" title="ConfluentCloudCredentials">ConfluentCloudCredentials</a>" : <i><a href="confluentcloudapisecrets.md">ConfluentCloudAPISecrets</a></i>
    }
}
</pre>

### YAML

<pre>
Type: ConfluentCloud::IAM::ServiceAccount
Properties:
    <a href="#description" title="Description">Description</a>: <i>String</i>
    <a href="#name" title="Name">Name</a>: <i>String</i>
    <a href="#confluentcloudcredentials" title="ConfluentCloudCredentials">ConfluentCloudCredentials</a>: <i><a href="confluentcloudapisecrets.md">ConfluentCloudAPISecrets</a></i>
</pre>

## Properties

#### Description

The description associated with the Service Account

_Required_: No

_Type_: String

_Pattern_: <code>^[\x20-\x7E]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Name

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9-_.]+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### ConfluentCloudCredentials

_Required_: Yes

_Type_: <a href="confluentcloudapisecrets.md">ConfluentCloudAPISecrets</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the ServiceAccountId.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### ServiceAccountId

Service Account in Confluent Cloud (sa-xxxx)

