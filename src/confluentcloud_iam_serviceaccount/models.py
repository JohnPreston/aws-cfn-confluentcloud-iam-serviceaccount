# DO NOT modify this file by hand, changes will be overwritten
import sys
from dataclasses import dataclass
from inspect import getmembers, isclass
from typing import (
    AbstractSet,
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

T = TypeVar("T")


def set_or_none(value: Optional[Sequence[T]]) -> Optional[AbstractSet[T]]:
    if value:
        return set(value)
    return None


@dataclass
class ResourceHandlerRequest(BaseResourceHandlerRequest):
    # pylint: disable=invalid-name
    desiredResourceState: Optional["ResourceModel"]
    previousResourceState: Optional["ResourceModel"]
    typeConfiguration: Optional["TypeConfigurationModel"]


@dataclass
class ResourceModel(BaseModel):
    Description: Optional[str]
    Name: Optional[str]
    ServiceAccountId: Optional[str]
    ConfluentCloudCredentials: Optional["_ConfluentCloudAPISecrets"]

    @classmethod
    def _deserialize(
        cls: Type["_ResourceModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourceModel"]:
        if not json_data:
            return None
        dataclasses = {n: o for n, o in getmembers(sys.modules[__name__]) if isclass(o)}
        recast_object(cls, json_data, dataclasses)
        return cls(
            Description=json_data.get("Description"),
            Name=json_data.get("Name"),
            ServiceAccountId=json_data.get("ServiceAccountId"),
            ConfluentCloudCredentials=ConfluentCloudAPISecrets._deserialize(
                json_data.get("ConfluentCloudCredentials")
            ),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class ConfluentCloudAPISecrets(BaseModel):
    ApiKey: Optional[str]
    ApiSecret: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_ConfluentCloudAPISecrets"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ConfluentCloudAPISecrets"]:
        if not json_data:
            return None
        return cls(
            ApiKey=json_data.get("ApiKey"),
            ApiSecret=json_data.get("ApiSecret"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ConfluentCloudAPISecrets = ConfluentCloudAPISecrets


@dataclass
class TypeConfigurationModel(BaseModel):
    @classmethod
    def _deserialize(
        cls: Type["_TypeConfigurationModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TypeConfigurationModel"]:
        if not json_data:
            return None
        return cls()


# work around possible type aliasing issues when variable has same name as a model
_TypeConfigurationModel = TypeConfigurationModel
