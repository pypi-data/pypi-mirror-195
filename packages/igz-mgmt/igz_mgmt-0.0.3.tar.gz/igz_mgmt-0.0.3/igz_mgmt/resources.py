# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""This module represents resources.

Most of the resources support all CRUD methods.
"""
import collections
import json
import time
import typing
from contextlib import contextmanager

import inflection
import pydantic
import semver
from pydantic import Field, SecretStr
from pydantic.utils import GetterDict

from igz_mgmt.app_services import AppServiceBase, AppServiceSpec
from igz_mgmt.client import APIClient
from igz_mgmt.common.helpers import (
    RetryUntilSuccessfulFatalError,
    RetryUntilSuccessfulInProgressErrorMessage,
    retry_until_successful,
)
from igz_mgmt.constants import (
    AdminStatuses,
    ApplyServicesMode,
    AppServiceDesiredStates,
    AppServicesManifestStates,
    ForceApplyAllMode,
    JobStates,
    SessionPlanes,
    TenantManagementRoles,
)
from igz_mgmt.cruds import ResourceListPagingQueryParams, _BaseCrud, _CrudFactory
from igz_mgmt.exceptions import (
    AppServiceNotExistsException,
    ResourceDeleteException,
    ResourceListException,
    ResourceNotFoundException,
    ResourceUpdateException,
)


class BaseResource(pydantic.BaseModel):
    """Base resource contains common attributes and methods for resources in the system."""

    type: str
    id: typing.Optional[typing.Union[int, str]]
    relationships: typing.Optional[dict]

    class Config:
        class _BaseGetter(GetterDict):
            def get(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
                if key in ["id", "type"]:
                    return self._obj["data"][key]
                elif key == "relationships":
                    return self._obj["data"].get("relationships", {})
                elif key in self._obj["data"]["attributes"]:
                    return self._obj["data"]["attributes"][key]
                return default

        orm_mode = True
        use_enum_values = True
        underscore_attrs_are_private = True
        getter_dict = _BaseGetter

        # be forward compatible
        extra = "allow"

    @classmethod
    def get(
        cls,
        http_client: APIClient,
        resource_id: typing.Union[int, str],
        include: typing.Optional[typing.List[str]] = None,
    ) -> "BaseResource":
        """Gets the resource record.

        Args:
            http_client (APIClient): The client to use.
            resource_id (int or str): Record id.
            include (typing.List[str], optional): Include related resources. None by default.

        Returns:
            BaseResource: The resource record.
        """
        params = {}
        if include:
            params["include"] = ",".join(include)
        resource = cls._get_crud().get(http_client, resource_id, params=params)
        return cls.from_orm(resource)

    @classmethod
    def list(
        cls,
        http_client: APIClient,
        filter_by: typing.Optional[typing.Mapping[str, str]] = None,
        sort_by: typing.Optional[typing.List[str]] = None,
        paging: typing.Optional[ResourceListPagingQueryParams] = None,
        include: typing.Optional[typing.List[str]] = None,
    ) -> typing.List["BaseResource"]:
        """Lists resource records.

        Args:
            http_client (APIClient): The client to use.
            filter_by (typing.Mapping[str, str], optional): Filter by field values. None by default.
            sort_by (typing.List[str], optional): Sort by field names. None by default.
            paging (ResourceListPagingQueryParams, optional): Allow to paginate resource by given records size.
            None by default.
            include (typing.List[str], optional): Include related resources. None by default.

        Returns:
            typing.List[BaseResource]: List of records for the specific resource.
        """
        list_resource = cls._get_crud().list(
            http_client, filter_by, sort_by, paging, include
        )
        return [
            cls.from_orm({"data": item, "included": item.get("included", [])})
            for item in list_resource["data"]
        ]

    def update(self, http_client: APIClient, relationships=None) -> "BaseResource":
        """Updates resource record.

        Args:
            http_client (APIClient): The client to use.
            relationships (optional): The resource relationships. None by default.

        Returns:
            BaseResource: The updated record.
        """
        self._get_crud().update(
            http_client,
            self.id,
            attributes=self._fields_to_attributes(),
            relationships=relationships,
        )

        # TODO: build cls from response when BE will return the updated resource within the response body
        updated_resource = self.get(http_client, self.id)
        self.__dict__.update(updated_resource)
        return self

    def delete(
        self,
        http_client: APIClient,
        ignore_missing: bool = False,
        wait_for_job_deletion: bool = True,
    ):
        """Deletes resource record.

        Args:
            http_client (APIClient): The client to use.
            ignore_missing (bool, optional): When True, don't raise an exception in case the record does not exist.
            False by default.
            wait_for_job_deletion (bool, optional): Whether to wait for the job to complete. True by default.
        """
        job_id = self._get_crud().delete(http_client, self.id, ignore_missing)
        if job_id and wait_for_job_deletion:
            Job.wait_for_completion(
                http_client, job_id, job_completion_retry_interval=10
            )

    @classmethod
    def _get_crud(cls) -> _BaseCrud:
        return _CrudFactory.create(
            inflection.underscore(cls.__fields__["type"].default)
        )

    @classmethod
    def _get_resource_by_name(
        cls, http_client: APIClient, filter_key, name, include=None
    ) -> "BaseResource":
        """Gets a resource by name, by listing all resource instances and filtering by name.

        If resource is not found, ResourceNotFoundException is raised
        """
        resources = cls.list(http_client, filter_by={filter_key: name})
        if not resources:
            raise ResourceNotFoundException(cls.__fields__["type"].default, name)
        resource_id = resources[0].id

        # although we already have the user, we need to get it again to get the relationships
        # passed in the include parameter
        return cls.get(http_client, resource_id, include=include)

    def _fields_to_attributes(self, exclude_unset=True):
        return self.dict(
            exclude={"type", "relationships", "id"},
            exclude_none=True,
            exclude_unset=exclude_unset,
            by_alias=True,
        )


class User(BaseResource):
    """User resource represents user in the system."""

    type: str = "user"
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    uid: int = 0
    created_at: str = ""
    data_access_mode: str = ""
    authentication_scheme: str = ""
    send_password_on_creation: bool = False
    assigned_policies: typing.List[TenantManagementRoles] = []
    operational_status: str = ""
    admin_status: str = AdminStatuses.up
    password: SecretStr = Field(None, exclude=True)

    @classmethod
    def create(
        cls,
        http_client: APIClient,
        username: str,
        password: str,
        email: str,
        first_name: str,
        last_name: str,
        uid: int = None,
        assigned_policies: typing.List[TenantManagementRoles] = None,
        primary_group: typing.Union[str, "Group", None] = None,
        groups: typing.Union[typing.List[str], typing.List["Group"], None] = None,
    ) -> "User":
        """Creates a new User.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
            assigned_policies (typing.List[TenantManagementRoles], optional): The assigned policies of the group.
            None by default.
            primary_group (str or Group or None): None by default.
            groups (typing.Union[typing.List[str], typing.List["Group"], None], optional): A list of group objects
            or group ids to add user to the groups. None by default.

        Returns:
            User
        """
        assigned_policies = assigned_policies or [
            TenantManagementRoles.developer.value,
            TenantManagementRoles.application_read_only.value,
        ]
        attributes = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "assigned_policies": assigned_policies,
        }
        if uid:
            attributes["uid"] = uid
        relationships = collections.defaultdict(dict)
        if primary_group:
            primary_group_id = (
                primary_group.id if isinstance(primary_group, Group) else primary_group
            )
            relationships["primary_group"] = {
                "data": {
                    "type": "user_group",
                    "id": primary_group_id,
                },
            }

            # ensure primary group is in groups list
            if groups:
                primary_group_in_groups = False
                for group in groups:
                    group_id = group.id if isinstance(group, Group) else group
                    if primary_group_id == group_id:
                        primary_group_in_groups = True
                        break
                if not primary_group_in_groups:
                    groups += primary_group_id
            else:
                groups = [primary_group_id]

        if groups:
            for group in groups:
                relationships["user_groups"].setdefault("data", []).append(
                    {
                        "type": "user_group",
                        "id": group.id if isinstance(group, Group) else group,
                    }
                )

        created_resource = cls._get_crud().create(
            http_client,
            attributes=attributes,
            relationships=relationships,
        )
        return cls.from_orm(created_resource)

    @classmethod
    def get_by_username(
        cls, http_client: APIClient, username: str, include=None
    ) -> "User":
        """A convenience method to get a user by username.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
            include (optional): Include related resources. None by default.

        Returns:
            User: The user instance by username.

        Raises:
            ResourceNotFoundException: If user is not found
        """
        return cls._get_resource_by_name(
            http_client, "username", username, include=include
        )

    @classmethod
    def self(cls, http_client: APIClient) -> "User":
        """Gets the current user.

        Args:
            http_client (APIClient): The client to use.

        Returns:
            User: The current user instance.
        """
        user = cls._get_crud().get_custom(http_client, "self")
        return cls.from_orm(user)

    def add_to_group(self, http_client: APIClient, group: typing.Union[str, "Group"]):
        """Adds a user to a group.

        1. get the user
        2. add the group to the user
        3. update the user

        Args:
            http_client (APIClient): The client to use.
            group (str or Group): The group id or group instance to add user into it.
        """
        user = self.get(http_client, self.id, include=["user_groups"])
        if "user_groups" not in user.relationships:
            user.relationships["user_groups"] = {"data": []}

        group_id = group.id if isinstance(group, Group) else group
        if User._ensure_user_in_group(user, group_id):
            user.update(http_client, relationships=user.relationships)

    def remove_from_group(
        self, http_client: APIClient, group: typing.Union[str, "Group"]
    ):
        """Removes a user from a group.

        Args:
            http_client (APIClient): The client to use.
            group (str or Group): The group id or group instance to remove user from it.
        """
        user = self.get(http_client, self.id, include=["user_groups"])
        group_id = group.id if isinstance(group, Group) else group
        if "user_groups" in user.relationships:
            user.relationships["user_groups"]["data"] = [
                group
                for group in user.relationships["user_groups"]["data"]
                if group["id"] != group_id
            ]
            user.update(http_client, relationships=user.relationships)

    def set_primary_group(
        self, http_client: APIClient, group: typing.Union[str, "Group"]
    ):
        """Sets the primary group of a user.

        Args:
            http_client (APIClient): The client to use.
            group (str or Group): The primary group id or group instance.
        """
        group_id = group.id if isinstance(group, Group) else group

        # we need primary group
        user = self.get(http_client, self.id, include=["user_groups"])
        if "primary_group" not in user.relationships:
            user.relationships["primary_group"] = {"data": None}
        if "user_groups" not in user.relationships:
            user.relationships["user_groups"] = {"data": []}

        User._ensure_user_in_group(user, group_id)
        user.relationships["primary_group"]["data"] = {
            "id": group_id,
            "type": "user_group",
        }
        user.update(http_client, relationships=user.relationships)

    def disable(self, http_client: APIClient):
        """Disables the user instance.

        Args:
            http_client (APIClient): The client to use.
        """
        self.admin_status = AdminStatuses.down
        return self.update(http_client)

    @classmethod
    def disable_by_username(cls, http_client: APIClient, username: str):
        """Disables the user by username.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
        """
        user = cls.get_by_username(http_client, username)
        return user.disable(http_client)

    @classmethod
    def disable_by_id(cls, http_client: APIClient, user_id: str):
        """Disables the user by user id.

        Args:
            http_client (APIClient): The client to use.
            user_id (str): The user id.
        """
        user = cls.get(http_client, user_id)
        return user.disable(http_client)

    def enable(self, http_client: APIClient):
        """Enables the user instance.

        Args:
            http_client (APIClient): The client to use.
        """
        self.admin_status = AdminStatuses.up
        return self.update(http_client)

    @classmethod
    def enable_by_username(cls, http_client: APIClient, username: str):
        """Enables the user by username.

        Args:
            http_client (APIClient): The client to use.
            username (str): The user username.
        """
        user = cls.get_by_username(http_client, username)
        return user.enable(http_client)

    @classmethod
    def enable_by_id(cls, http_client: APIClient, user_id: str):
        """Enables the user by user id.

        Args:
            http_client (APIClient): The client to use.
            user_id (str): The user id.
        """
        user = cls.get(http_client, user_id)
        return user.enable(http_client)

    @staticmethod
    def _ensure_user_in_group(user, group_id: str) -> bool:
        """Ensures that a user has a group in its relationships.

        e.g.:
        If group is not in user relationships, add it and return True
        Alternatively, if group is in user relationships, return False

        Returns:
            bool: True if the group was added to the user relationship, False otherwise.
        """
        if group_id not in [
            group["id"] for group in user.relationships["user_groups"]["data"]
        ]:
            user.relationships["user_groups"]["data"].append(
                {"id": group_id, "type": "user_group"}
            )
            return True

        return False


class Group(BaseResource):
    """Group resource represents user group in the system."""

    type: str = "user_group"
    name: str = ""
    description: str = None
    data_access_mode: str = "enabled"
    gid: int = 0
    kind: str = "local"
    assigned_policies: typing.List[TenantManagementRoles] = []
    system_provided: bool = False

    @classmethod
    def create(
        cls,
        http_client: APIClient,
        name: typing.Optional[str],
        assigned_policies: typing.Optional[typing.List[TenantManagementRoles]] = None,
        description: typing.Optional[str] = None,
        gid: typing.Optional[int] = None,
        users: typing.Optional[typing.List[typing.Union[int, str, User]]] = None,
    ) -> "Group":
        """Creates a new group.

        Args:
            http_client (APIClient): The client to use.
            name (str, optional): Group name.
            assigned_policies (typing.List[TenantManagementRoles], optional): The assigned policies of the group.
            None by default.
            description (str, optional): The description of the group. None by default.
            gid (int, optional): The gid of the group (leave empty for auto-assign). None by default.
            users (typing.List[typing.Union[int, str, User]], optional): A list of User objects or user ids
            to add to the group. None by default.

        Returns:
            Group
        """
        if not assigned_policies:
            assigned_policies = [
                TenantManagementRoles.data.value,
                TenantManagementRoles.application_admin.value,
            ]
        relationships = {}
        if users:
            relationships["users"] = {
                "data": [
                    {"id": user.id if isinstance(user, User) else user, "type": "user"}
                    for user in users
                ]
            }
        created_resource = cls._get_crud().create(
            http_client,
            attributes={
                "name": name,
                "description": description,
                "gid": gid,
                "assigned_policies": assigned_policies,
            },
            relationships=relationships,
        )
        return cls.from_orm(created_resource)

    @classmethod
    def get_by_name(cls, http_client: APIClient, name: str, include=None) -> "Group":
        """A convenience method to get a group by name.

        Args:
            http_client (APIClient): The client to use.
            name (str): Group name.
            include (optional): Include related resources. None by default.

        Returns:
            Group: The group instance by group name.

        Raises:
            ResourceNotFoundException: If group is not found
        """
        return cls._get_resource_by_name(http_client, "name", name, include=include)

    def add_user(self, http_client: APIClient, user: typing.Union[str, int, "User"]):
        """Adds a user to group.

        1. get the user
        2. add the group to the user
        3. update the group

        Args:
            http_client (APIClient): The client to use.
            user (str or int or User): The user id or user instance to add.
        """
        if not isinstance(user, User):
            user = User.get(http_client, user)
        user.add_to_group(http_client, self)
        self.__dict__.update(Group.get(http_client, self.id))

    def remove_user(self, http_client: APIClient, user: typing.Union[str, int, "User"]):
        """Removes a user from group.

        Args:
            http_client (APIClient): The client to use.
            user (str ot int or User): The user id or user instance to remove.
        """
        if not isinstance(user, User):
            user = User.get(http_client, user)
        user.remove_from_group(http_client, self)
        self.__dict__.update(Group.get(http_client, self.id))


class AccessKey(BaseResource):
    """AccessKey resource represents access key in the system."""

    type: str = "access_key"
    tenant_id: str = ""
    ttl: int = 315360000  # 10 years
    created_at: str = ""
    updated_at: str = ""
    group_ids: typing.List[str] = []
    uid: int = 0
    gids: typing.List[int] = []
    expires_at: int = 0  # EPOCH
    interface_kind: str = "web"
    label: str = ""
    kind: str = "accessKey"
    planes: typing.List[SessionPlanes] = SessionPlanes.all()

    @classmethod
    def create(
        cls,
        http_client: APIClient,
        planes: typing.List[SessionPlanes] = SessionPlanes.all(),
        label: str = None,
    ):
        """Creates a new access key.

        Args:
            http_client (APIClient): The client to use.
            planes (typing.List[SessionPlanes], optional): The planes of the access key.
            label (str, optional): The label of the access key.
        """
        created_resource = cls._get_crud().create(
            http_client,
            attributes={
                "planes": planes,
                "label": label,
            },
        )
        return cls.from_orm(created_resource)


class Job(BaseResource):
    """Job is an abstraction for long-running operations in the API.

    Some operations, cannot be finished within a reasonable amount of time for a normal HTTP request.
    Job has a state, id and can be awaited on asynchronously.
    """

    type: str = "job"
    kind: str = ""
    params: str = ""
    max_total_execution_time: int = 3 * 60 * 60  # in seconds
    max_worker_execution_time: typing.Optional[int] = None  # in seconds
    delay: float = 0  # in seconds
    state: JobStates = JobStates.created
    result: str = ""
    created_at: str = ""
    on_success: typing.List[dict] = None
    on_failure: typing.List[dict] = None
    updated_at: str = ""
    handler: str = ""
    ctx_id: str = ""

    def delete(self, http_client: APIClient, **kwargs):
        """This method is forbidden."""
        raise ResourceDeleteException

    def update(self, http_client: APIClient, **kwargs):
        """This method is forbidden."""
        raise ResourceUpdateException

    @staticmethod
    def wait_for_completion(
        http_client: APIClient,
        job_id: str,
        job_completion_retry_interval: float = 30,
        timeout: int = 3600,
    ):
        """Wait for a job to be finished.

        Args:
            http_client (APIClient): The client to use.
            job_id (str): The job id.
            job_completion_retry_interval (float, optional): The default is 30.
            timeout (int, optional): The default is 3600.
        """

        def _verify_job_in_terminal_state():
            try:
                job_obj = Job.get(http_client, job_id)
            except ResourceNotFoundException as exc:
                http_client._logger.warn_with(
                    "Job not found, bail out",
                    job_id=job_id,
                )
                raise RetryUntilSuccessfulFatalError(
                    "Resource was not found", caused_by_exc=exc
                )
            if job_obj.state not in JobStates.terminal_states():
                http_client._logger.info_with(
                    "Job is not in a terminal state yet, retrying",
                    current_state=job_obj.state,
                    job_id=job_id,
                )
                raise RetryUntilSuccessfulInProgressErrorMessage(
                    "Waiting for job completion",
                    variables={
                        "job_id": job_id,
                        "job_state": job_obj.state,
                    },
                )
            return job_obj

        http_client._logger.info_with("Waiting for job completion", job_id=job_id)
        job = retry_until_successful(
            job_completion_retry_interval,
            timeout,
            http_client._logger,
            True,
            _verify_job_in_terminal_state,
        )
        if job.state != JobStates.completed:
            error_message = f"Job {job_id} failed with state: {job.state}"
            try:
                parsed_result = json.loads(job.result)
                error_message += f", message: {parsed_result['message']}"
                # status is optional
                if "status" in parsed_result:
                    status_code = int(parsed_result["status"])
                    error_message = f", status: {status_code}"

            except Exception:
                error_message += f", message: {job.result}"

            raise RuntimeError(error_message)
        http_client._logger.info_with("Job completed successfully", job_id=job_id)


class AppServicesManifest(BaseResource):
    """AppServicesManifest resource."""

    type: str = "app_services_manifest"
    cluster_name: str = ""
    tenant_name: str = ""
    tenant_id: str = ""
    app_services: typing.List[AppServiceBase] = []
    state: typing.Optional[AppServicesManifestStates]
    last_error: typing.Optional[str]
    last_modification_job: str = ""
    apply_services_mode: typing.Optional[ApplyServicesMode]
    running_modification_job: str = ""
    force_apply_all_mode: typing.Optional[ForceApplyAllMode]

    _skip_apply: bool = False

    @staticmethod
    @contextmanager
    def apply_services(
        http_client: APIClient,
        force_apply_all_mode: ForceApplyAllMode = ForceApplyAllMode.disabled,
    ):
        """A context manager to apply services with multiple changes at once.

        Args:
            http_client (APIClient): The client to use.
            force_apply_all_mode (ForceApplyAllMode, optional): Disabled by default.

        Returns:
            AppServicesManifest: The app service manifest instance.
        """
        app_services_manifest = AppServicesManifest.get(http_client)
        app_services_manifest._skip_apply = True
        try:
            yield app_services_manifest
        finally:
            app_services_manifest._apply(
                http_client,
                # writing it down here for explicitness
                wait_for_completion=True,
                force_apply_all_mode=force_apply_all_mode,
            )
            app_services_manifest._skip_apply = False

    def delete(self, http_client: APIClient, **kwargs):
        """This method is forbidden."""
        raise ResourceDeleteException

    def update(self, http_client: APIClient, **kwargs):
        """This method is forbidden."""
        raise ResourceUpdateException

    def list(self, http_client: APIClient, **kwargs):
        """This method is forbidden."""
        raise ResourceListException

    @classmethod
    def get(cls, http_client: APIClient, **kwargs) -> "AppServicesManifest":
        """Gets the app services manifest from the API.

        Args:
            http_client (APIClient): The client to use.
            **kwargs: Arbitrary keyword arguments (not in used).

        Returns:
            AppServicesManifest: The app service manifest instance.
        """
        resource = cls._get_crud().list(http_client)
        return [cls.from_orm({"data": item}) for item in resource["data"]][0]

    def set_apply_mode(self, apply_mode: ApplyServicesMode):
        """Sets the apply mode of the app services manifest.

        Args:
            apply_mode (ApplyServicesMode): apply services mode value.
        """
        self.apply_services_mode = apply_mode

    def resolve_service(
        self,
        app_service_spec_name: str,
    ) -> typing.Optional[AppServiceBase]:
        """Gets the app service that matches the given spec name.

        Args:
            app_service_spec_name (str): The name of the app service spec.

        Returns:
            AppServiceBase, optional: The app service instance that matches the given spec name.
        """
        for app_service in self.app_services:
            if app_service.spec.name == app_service_spec_name:
                return app_service
        return None

    def create_or_update(
        self,
        http_client: APIClient,
        app_service: typing.Union[AppServiceSpec, AppServiceBase],
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Creates or updates an app service.

        Args:
            http_client (APIClient): The client to use.
            app_service (AppServiceSpec or AppServiceBase): The app service to create or update
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_spec = (
            app_service.spec if isinstance(app_service, AppServiceBase) else app_service
        )
        app_service_spec.mark_as_changed = True
        app_service_spec_obj = self.resolve_service(app_service_spec.name)
        if app_service_spec_obj:
            for position, service in enumerate(self.app_services):
                if service.spec.name == app_service_spec_obj.spec.name:
                    self.app_services[position].spec = app_service_spec
                    break
        else:
            self.app_services.append(AppServiceBase(spec=app_service_spec))
        if not self._skip_apply:
            return self._apply(http_client, wait_for_completion)

    def restart(
        self,
        http_client: APIClient,
        app_service_spec_name: str,
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Restarts an app service.

        Args:
            http_client (APIClient): The client to use.
            app_service_spec_name (str): Name of the app service to restart
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_obj = self.resolve_service(app_service_spec_name)
        if not app_service_obj:
            raise AppServiceNotExistsException(name=app_service_spec_name)
        for position, app_service in enumerate(self.app_services):
            if app_service.spec.name == app_service_obj.spec.name:
                self.app_services[position].spec.mark_for_restart = True
                break
        if not self._skip_apply:
            return self._apply(http_client, wait_for_completion)

    def remove_service(
        self,
        http_client: APIClient,
        app_service_spec_name: str,
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Removes an app service.

        Args:
            http_client (APIClient): The client to use.
            app_service_spec_name (str): Name of the app service to remove
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_obj = self.resolve_service(app_service_spec_name)
        if not app_service_obj:
            raise AppServiceNotExistsException(name=app_service_spec_name)
        for position, app_service in enumerate(self.app_services):
            if app_service.spec.name == app_service_obj.spec.name:
                del self.app_services[position]
                break
        if not self._skip_apply:
            return self._apply(http_client, wait_for_completion)

    def scale_from_zero(
        self,
        http_client: APIClient,
        app_service_spec_name: str,
        wait_for_completion=True,
    ) -> typing.Optional[Job]:
        """Scales an app service from zero.

        Args:
            http_client (APIClient): The client to use.
            app_service_spec_name (str): Name of the app service to scale from zero
            wait_for_completion (bool): Whether to wait for the job to complete

        Returns:
            Job, optional: the job that was created or None if wait_for_completion is False.
        """
        app_service_obj = self.resolve_service(app_service_spec_name)
        if not app_service_obj:
            raise AppServiceNotExistsException(name=app_service_spec_name)
        app_service_obj.spec.mark_as_changed = True
        app_service_obj.spec.desired_state = AppServiceDesiredStates.ready
        for position, app_service in enumerate(self.app_services):
            if app_service.spec.name == app_service_obj.spec.name:
                self.app_services[position].spec = app_service_obj.spec
                break
        if not self._skip_apply:
            current_apply_mode = self.apply_services_mode

            # In 3.5.3, the ApplyServicesMode.scale_from_zero_only mode is deprecated.
            # because we can scale services from zero by using the mark_as_changed and desired_state fields
            if http_client.version >= semver.VersionInfo.parse("3.5.3"):
                self.set_apply_mode(ApplyServicesMode.service_owner_edit)
            else:
                self.set_apply_mode(ApplyServicesMode.scale_from_zero_only)
            apply_result = self._apply(http_client, wait_for_completion)

            # set to the previous apply mode
            self.set_apply_mode(current_apply_mode)
            return apply_result

    def _apply(
        self,
        http_client: APIClient,
        wait_for_completion=True,
        force_apply_all_mode=ForceApplyAllMode.disabled,
    ) -> Job:
        """Apply the current state of the manifest to the API.

        Args:
            http_client (APIClient): The client to use.
            wait_for_completion (bool, optional): Whether to wait for the job to complete. True by default.
            force_apply_all_mode (ForceApplyAllMode, optional): Disabled by default.

        Returns:
            Job: the job that was created.
        """
        # TODO: handle errors
        self.force_apply_all_mode = force_apply_all_mode
        response = self._get_crud().update(
            http_client,
            None,
            # don't ignore unset fields
            attributes=self._fields_to_attributes(exclude_unset=False),
            relationships=self.relationships,
        )

        job_id = response.json().get("data", {}).get("id")
        if not wait_for_completion:
            return Job.get(http_client, job_id)

        # wait few seconds before checking job status
        time.sleep(5)
        apply_exc = None
        try:
            Job.wait_for_completion(
                http_client, job_id, job_completion_retry_interval=10
            )
        except Exception as exc:
            apply_exc = exc

        updated_resource = self.get(http_client)
        self.__dict__.update(updated_resource)
        if apply_exc:
            errors = []
            for service in updated_resource.app_services:
                if service.status.error_info and service.status.error_info.description:
                    errors.append(
                        f"Service {service.spec.name} failed due to {service.status.error_info.description}"
                    )
            if errors:
                raise RuntimeError(", ".join(errors)) from apply_exc
            else:
                raise apply_exc
        return Job.get(http_client, job_id)
