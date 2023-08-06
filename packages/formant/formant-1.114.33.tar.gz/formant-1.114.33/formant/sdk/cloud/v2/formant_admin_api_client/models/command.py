import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.command_stream_type import CommandStreamType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.command_parameter import CommandParameter
    from ..models.command_tags import CommandTags


T = TypeVar("T", bound="Command")


@attr.s(auto_attribs=True)
class Command:
    """
    Attributes:
        device_id (str):
        command (str):
        parameter (CommandParameter):
        organization_id (Union[Unset, str]):
        user_id (Union[Unset, None, str]):
        event_trigger_id (Union[Unset, str]):
        command_template_id (Union[Unset, None, str]):
        delivered_at (Union[Unset, None, datetime.datetime]):
        canceled_at (Union[Unset, None, datetime.datetime]):
        responded_at (Union[Unset, None, datetime.datetime]):
        success (Union[Unset, None, bool]):
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, CommandStreamType]):
        tags (Union[Unset, None, CommandTags]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    device_id: str
    command: str
    parameter: "CommandParameter"
    organization_id: Union[Unset, str] = UNSET
    user_id: Union[Unset, None, str] = UNSET
    event_trigger_id: Union[Unset, str] = UNSET
    command_template_id: Union[Unset, None, str] = UNSET
    delivered_at: Union[Unset, None, datetime.datetime] = UNSET
    canceled_at: Union[Unset, None, datetime.datetime] = UNSET
    responded_at: Union[Unset, None, datetime.datetime] = UNSET
    success: Union[Unset, None, bool] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, CommandStreamType] = UNSET
    tags: Union[Unset, None, "CommandTags"] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        device_id = self.device_id
        command = self.command
        parameter = self.parameter.to_dict()

        organization_id = self.organization_id
        user_id = self.user_id
        event_trigger_id = self.event_trigger_id
        command_template_id = self.command_template_id
        delivered_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.delivered_at, Unset):
            delivered_at = self.delivered_at.isoformat() if self.delivered_at else None

        canceled_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.canceled_at, Unset):
            canceled_at = self.canceled_at.isoformat() if self.canceled_at else None

        responded_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.responded_at, Unset):
            responded_at = self.responded_at.isoformat() if self.responded_at else None

        success = self.success
        stream_name = self.stream_name
        stream_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.stream_type, Unset):
            stream_type = self.stream_type.value if self.stream_type else None

        tags: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict() if self.tags else None

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "deviceId": device_id,
                "command": command,
                "parameter": parameter,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if user_id is not UNSET:
            field_dict["userId"] = user_id
        if event_trigger_id is not UNSET:
            field_dict["eventTriggerId"] = event_trigger_id
        if command_template_id is not UNSET:
            field_dict["commandTemplateId"] = command_template_id
        if delivered_at is not UNSET:
            field_dict["deliveredAt"] = delivered_at
        if canceled_at is not UNSET:
            field_dict["canceledAt"] = canceled_at
        if responded_at is not UNSET:
            field_dict["respondedAt"] = responded_at
        if success is not UNSET:
            field_dict["success"] = success
        if stream_name is not UNSET:
            field_dict["streamName"] = stream_name
        if stream_type is not UNSET:
            field_dict["streamType"] = stream_type
        if tags is not UNSET:
            field_dict["tags"] = tags
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.command_parameter import CommandParameter
        from ..models.command_tags import CommandTags

        d = src_dict.copy()
        device_id = d.pop("deviceId")

        command = d.pop("command")

        parameter = CommandParameter.from_dict(d.pop("parameter"))

        organization_id = d.pop("organizationId", UNSET)

        user_id = d.pop("userId", UNSET)

        event_trigger_id = d.pop("eventTriggerId", UNSET)

        command_template_id = d.pop("commandTemplateId", UNSET)

        _delivered_at = d.pop("deliveredAt", UNSET)
        delivered_at: Union[Unset, None, datetime.datetime]
        if _delivered_at is None:
            delivered_at = None
        elif isinstance(_delivered_at, Unset):
            delivered_at = UNSET
        else:
            delivered_at = isoparse(_delivered_at)

        _canceled_at = d.pop("canceledAt", UNSET)
        canceled_at: Union[Unset, None, datetime.datetime]
        if _canceled_at is None:
            canceled_at = None
        elif isinstance(_canceled_at, Unset):
            canceled_at = UNSET
        else:
            canceled_at = isoparse(_canceled_at)

        _responded_at = d.pop("respondedAt", UNSET)
        responded_at: Union[Unset, None, datetime.datetime]
        if _responded_at is None:
            responded_at = None
        elif isinstance(_responded_at, Unset):
            responded_at = UNSET
        else:
            responded_at = isoparse(_responded_at)

        success = d.pop("success", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, CommandStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = CommandStreamType(_stream_type)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, None, CommandTags]
        if _tags is None:
            tags = None
        elif isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = CommandTags.from_dict(_tags)

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

        command = cls(
            device_id=device_id,
            command=command,
            parameter=parameter,
            organization_id=organization_id,
            user_id=user_id,
            event_trigger_id=event_trigger_id,
            command_template_id=command_template_id,
            delivered_at=delivered_at,
            canceled_at=canceled_at,
            responded_at=responded_at,
            success=success,
            stream_name=stream_name,
            stream_type=stream_type,
            tags=tags,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        command.additional_properties = d
        return command

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
