import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.device_type import DeviceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.device_follower import DeviceFollower
    from ..models.device_state import DeviceState
    from ..models.device_tags import DeviceTags
    from ..models.scope_filter import ScopeFilter


T = TypeVar("T", bound="Device")


@attr.s(auto_attribs=True)
class Device:
    """
    Attributes:
        name (str):
        public_key (str):
        organization_id (Union[Unset, str]):
        type (Union[Unset, DeviceType]):
        user_id (Union[Unset, None, str]):
        scope (Union[Unset, None, ScopeFilter]):
        desired_agent_version (Union[Unset, None, str]):
        desired_configuration_version (Union[Unset, None, int]):
        temporary_configuration_version (Union[Unset, None, int]):
        temporary_configuration_expiration (Union[Unset, None, datetime.datetime]):
        temporary_configuration_template_id (Union[Unset, None, str]):
        followers (Union[Unset, List['DeviceFollower']]):
        phone_number (Union[Unset, None, str]):
        state (Union[Unset, DeviceState]):
        enabled (Union[Unset, bool]):
        fully_configured (Union[Unset, bool]):
        disabled_at (Union[Unset, None, datetime.datetime]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        tags (Union[Unset, DeviceTags]):
    """

    name: str
    public_key: str
    organization_id: Union[Unset, str] = UNSET
    type: Union[Unset, DeviceType] = UNSET
    user_id: Union[Unset, None, str] = UNSET
    scope: Union[Unset, None, "ScopeFilter"] = UNSET
    desired_agent_version: Union[Unset, None, str] = UNSET
    desired_configuration_version: Union[Unset, None, int] = UNSET
    temporary_configuration_version: Union[Unset, None, int] = UNSET
    temporary_configuration_expiration: Union[Unset, None, datetime.datetime] = UNSET
    temporary_configuration_template_id: Union[Unset, None, str] = UNSET
    followers: Union[Unset, List["DeviceFollower"]] = UNSET
    phone_number: Union[Unset, None, str] = UNSET
    state: Union[Unset, "DeviceState"] = UNSET
    enabled: Union[Unset, bool] = UNSET
    fully_configured: Union[Unset, bool] = UNSET
    disabled_at: Union[Unset, None, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    tags: Union[Unset, "DeviceTags"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        public_key = self.public_key
        organization_id = self.organization_id
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        user_id = self.user_id
        scope: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.scope, Unset):
            scope = self.scope.to_dict() if self.scope else None

        desired_agent_version = self.desired_agent_version
        desired_configuration_version = self.desired_configuration_version
        temporary_configuration_version = self.temporary_configuration_version
        temporary_configuration_expiration: Union[Unset, None, str] = UNSET
        if not isinstance(self.temporary_configuration_expiration, Unset):
            temporary_configuration_expiration = (
                self.temporary_configuration_expiration.isoformat() if self.temporary_configuration_expiration else None
            )

        temporary_configuration_template_id = self.temporary_configuration_template_id
        followers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.followers, Unset):
            followers = []
            for followers_item_data in self.followers:
                followers_item = followers_item_data.to_dict()

                followers.append(followers_item)

        phone_number = self.phone_number
        state: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.to_dict()

        enabled = self.enabled
        fully_configured = self.fully_configured
        disabled_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.disabled_at, Unset):
            disabled_at = self.disabled_at.isoformat() if self.disabled_at else None

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "publicKey": public_key,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if type is not UNSET:
            field_dict["type"] = type
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if scope is not UNSET:
            field_dict["scope"] = scope
        if desired_agent_version is not UNSET:
            field_dict["desiredAgentVersion"] = desired_agent_version
        if desired_configuration_version is not UNSET:
            field_dict["desiredConfigurationVersion"] = desired_configuration_version
        if temporary_configuration_version is not UNSET:
            field_dict["temporaryConfigurationVersion"] = temporary_configuration_version
        if temporary_configuration_expiration is not UNSET:
            field_dict["temporaryConfigurationExpiration"] = temporary_configuration_expiration
        if temporary_configuration_template_id is not UNSET:
            field_dict["temporaryConfigurationTemplateId"] = temporary_configuration_template_id
        if followers is not UNSET:
            field_dict["followers"] = followers
        if phone_number is not UNSET:
            field_dict["phoneNumber"] = phone_number
        if state is not UNSET:
            field_dict["state"] = state
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if fully_configured is not UNSET:
            field_dict["fullyConfigured"] = fully_configured
        if disabled_at is not UNSET:
            field_dict["disabledAt"] = disabled_at
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.device_follower import DeviceFollower
        from ..models.device_state import DeviceState
        from ..models.device_tags import DeviceTags
        from ..models.scope_filter import ScopeFilter

        d = src_dict.copy()
        name = d.pop("name")

        public_key = d.pop("publicKey")

        organization_id = d.pop("organizationId", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, DeviceType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DeviceType(_type)

        user_id = d.pop("userId", UNSET)

        _scope = d.pop("scope", UNSET)
        scope: Union[Unset, None, ScopeFilter]
        if _scope is None:
            scope = None
        elif isinstance(_scope, Unset):
            scope = UNSET
        else:
            scope = ScopeFilter.from_dict(_scope)

        desired_agent_version = d.pop("desiredAgentVersion", UNSET)

        desired_configuration_version = d.pop("desiredConfigurationVersion", UNSET)

        temporary_configuration_version = d.pop("temporaryConfigurationVersion", UNSET)

        _temporary_configuration_expiration = d.pop("temporaryConfigurationExpiration", UNSET)
        temporary_configuration_expiration: Union[Unset, None, datetime.datetime]
        if _temporary_configuration_expiration is None:
            temporary_configuration_expiration = None
        elif isinstance(_temporary_configuration_expiration, Unset):
            temporary_configuration_expiration = UNSET
        else:
            temporary_configuration_expiration = isoparse(_temporary_configuration_expiration)

        temporary_configuration_template_id = d.pop("temporaryConfigurationTemplateId", UNSET)

        followers = []
        _followers = d.pop("followers", UNSET)
        for followers_item_data in _followers or []:
            followers_item = DeviceFollower.from_dict(followers_item_data)

            followers.append(followers_item)

        phone_number = d.pop("phoneNumber", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, DeviceState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = DeviceState.from_dict(_state)

        enabled = d.pop("enabled", UNSET)

        fully_configured = d.pop("fullyConfigured", UNSET)

        _disabled_at = d.pop("disabledAt", UNSET)
        disabled_at: Union[Unset, None, datetime.datetime]
        if _disabled_at is None:
            disabled_at = None
        elif isinstance(_disabled_at, Unset):
            disabled_at = UNSET
        else:
            disabled_at = isoparse(_disabled_at)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, DeviceTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = DeviceTags.from_dict(_tags)

        device = cls(
            name=name,
            public_key=public_key,
            organization_id=organization_id,
            type=type,
            user_id=user_id,
            scope=scope,
            desired_agent_version=desired_agent_version,
            desired_configuration_version=desired_configuration_version,
            temporary_configuration_version=temporary_configuration_version,
            temporary_configuration_expiration=temporary_configuration_expiration,
            temporary_configuration_template_id=temporary_configuration_template_id,
            followers=followers,
            phone_number=phone_number,
            state=state,
            enabled=enabled,
            fully_configured=fully_configured,
            disabled_at=disabled_at,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags,
        )

        device.additional_properties = d
        return device

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
