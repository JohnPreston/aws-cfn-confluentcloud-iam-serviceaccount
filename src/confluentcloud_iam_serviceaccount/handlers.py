#  SPDX-License-Identifier: GPL-2.0-only
#  Copyright 2020-2022 John Mille <john@compose-x.io>

import logging
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)
from confluent_cloud_sdk.client_factory import ConfluentClient
from confluent_cloud_sdk.confluent_iam_v2 import ServiceAccount
from confluent_cloud_sdk.errors import (
    ConfluentApiException,
    GenericConflict,
    GenericForbidden,
    GenericNotFound,
    GenericRequestError,
    GenericUnauthorized,
)

from .models import ConfluentCloudAPISecrets, ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
TYPE_NAME = "ConfluentCloud::IAM::ServiceAccount"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


def get_client(resource: ResourceModel) -> ConfluentClient:
    """
    Function to get the credentials and create the API client

    :param ResourceModel resource:
    :return:
    :rtype: ConfluentClient
    """

    if not resource.ConfluentCloudCredentials or not isinstance(
        resource.ConfluentCloudCredentials, ConfluentCloudAPISecrets
    ):
        raise ValueError("Invalid ConfluentCloudCredentials")
    client = ConfluentClient(
        resource.ConfluentCloudCredentials.ApiKey,
        resource.ConfluentCloudCredentials.ApiSecret,
    )
    return client


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:

    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    progress.status = OperationStatus.FAILED
    try:
        client = get_client(model)
        service_account = ServiceAccount(client, None, model.Name, model.Description)
        service_account.create()
        primary_identifier = service_account.obj_id
        model.ServiceAccountId = service_account.obj_id
        progress.status = OperationStatus.SUCCESS
        LOG.info(f"Successfully created new SA - {service_account.obj_id}")
        return progress
    except GenericConflict as error:
        LOG.critical("Action.CREATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AlreadyExists
        progress.message = f"Action.CREATE - Resource already exists"
        return progress
    except (GenericForbidden, GenericUnauthorized) as error:
        LOG.critical("Action.CREATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.CREATE {error}"
        return progress
    except GenericRequestError as error:
        LOG.critical("Action.CREATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.CREATE - {error}"
        return progress
    except Exception as error:
        LOG.critical("Action.CREATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.CREATE - Unmanaged error - {error}"
        return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.FAILED,
        resourceModel=model,
    )
    try:
        client = get_client(model)
        service_account = ServiceAccount(
            client, model.ServiceAccountId, model.Name, model.Description
        )
        service_account.obj_id = model.ServiceAccountId
        service_account.set_from_read()
        progress.status = OperationStatus.SUCCESS
        progress.message = "Action.READ SUCCESS"
        progress.resourceModel = model
        return progress
    except GenericNotFound as error:
        LOG.critical("Action.READ")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.NotFound
        progress.message = f"Action.READ - Resource does not exist."
        return progress
    except GenericConflict as error:
        LOG.critical("Action.READ")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AlreadyExists
        progress.message = f"Action.READ - Resource already exists"
        return progress
    except (GenericForbidden, GenericUnauthorized) as error:
        LOG.critical("Action.READ")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.READ {error}"
        return progress
    except GenericRequestError as error:
        LOG.critical("Action.READ")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.READ - {error}"
        return progress
    except Exception as error:
        LOG.critical("Action.READ")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.READ UNMANAGED- {error}"
        return progress


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:

    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )
    progress.status = OperationStatus.FAILED
    try:
        client = get_client(model)
        service_account = ServiceAccount(
            client, model.ServiceAccountId, model.Name, model.Description
        )
        service_account.obj_id = model.ServiceAccountId
        service_account.update(model.Description)
        progress.status = OperationStatus.SUCCESS
        return progress
    except GenericNotFound as error:
        LOG.critical("Action.UPDATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.NotFound
        progress.message = f"Action.UPDATE - Resource does not exist."
        return progress
    except GenericConflict as error:
        LOG.critical("Action.UPDATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AlreadyExists
        progress.message = f"Action.UPDATE - Resource already exists"
        return progress
    except (GenericForbidden, GenericUnauthorized) as error:
        LOG.critical("Action.UPDATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.UPDATE {error}"
        return progress
    except GenericRequestError as error:
        LOG.critical("Action.UPDATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.UPDATE - {error}"
        return progress
    except Exception as error:
        LOG.critical("Action.UPDATE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.UPDATE UNMANAGED- {error}"
        return progress


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:

    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )
    progress.status = OperationStatus.FAILED
    print("IN DELETE ID FROM MODEL", model.ServiceAccountId)
    try:
        client = get_client(model)
        service_account = ServiceAccount(
            client, model.ServiceAccountId, model.Name, model.Description
        )
        if not model.ServiceAccountId:
            LOG.error("ServiceAccountId was not set in model. Trying lookup")
            service_account.set_from_read(model.Name)
            if not service_account.obj_id:
                progress.status = OperationStatus.FAILED
                progress.errorCode = HandlerErrorCode.NotFound
                progress.message = f"Action.DELETE - Resource does not exist."
                return progress
        else:
            LOG.info("Setting obj_id from ServiceAccountId")
            service_account.obj_id = model.ServiceAccountId
        service_account.delete()
        progress.status = OperationStatus.SUCCESS
        return progress
    except (GenericNotFound, GenericForbidden) as error:
        LOG.critical("Action.DELETE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.NotFound
        progress.message = f"Action.DELETE - Resource does not exist."
        return progress
    except GenericUnauthorized as error:
        LOG.critical("Action.DELETE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.AccessDenied
        progress.message = f"Action.DELETE {error}"
        return progress
    except GenericRequestError as error:
        LOG.critical("Action.DELETE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.DELETE - {error}"
        return progress
    except Exception as error:
        LOG.critical("Action.DELETE")
        LOG.exception(error)
        progress.errorCode = HandlerErrorCode.InternalFailure
        progress.message = f"Action.DELETE UNMANAGED- {error}"
        return progress


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=[],
    )
