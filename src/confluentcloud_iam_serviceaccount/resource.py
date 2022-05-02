#  SPDX-License-Identifier: GPL-2.0-only
#  Copyright 2020-2022 John Mille <john@compose-x.io>

"""
Troposphere resource definition
"""

from troposphere import AWSObject, AWSProperty, PropsDictType


class ConfluentCloudAPISecrets(AWSProperty):
    """
    ApiKey and ApiSecret to make API calls to Confluent Cloud
    """

    props: PropsDictType = {"ApiKey": (str, True), "ApiSecret": (str, True)}


class ServiceAccount(AWSObject):
    resource_type = "ConfluentCloud::IAM::ServiceAccount"
    props: PropsDictType = {
        "Description": (str, False),
        "Name": (str, True),
        "ConfluentCloudCredentials": (ConfluentCloudAPISecrets, True),
    }
