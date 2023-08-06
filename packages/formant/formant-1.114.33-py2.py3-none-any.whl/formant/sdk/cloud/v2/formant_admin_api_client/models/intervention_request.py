import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.intervention_request_intervention_type import InterventionRequestInterventionType
from ..models.intervention_request_severity import InterventionRequestSeverity
from ..models.intervention_request_stream_type import InterventionRequestStreamType
from ..models.intervention_request_type import InterventionRequestType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.intervention_request_tags import InterventionRequestTags
    from ..models.labeling_request_data import LabelingRequestData
    from ..models.selection_request_data import SelectionRequestData
    from ..models.teleop_request_data import TeleopRequestData


T = TypeVar("T", bound="InterventionRequest")


@attr.s(auto_attribs=True)
class InterventionRequest:
    """
    Attributes:
        data (Union['LabelingRequestData', 'SelectionRequestData', 'TeleopRequestData']):
        time (datetime.datetime):
        type (Union[Unset, InterventionRequestType]):
        intervention_type (Union[Unset, InterventionRequestInterventionType]):
        responses (Union[Unset, List[Any]]):
        agent_id (Union[Unset, str]):
        severity (Union[Unset, InterventionRequestSeverity]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        organization_id (Union[Unset, str]):
        end_time (Union[Unset, None, datetime.datetime]):
        message (Union[Unset, str]):
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]):
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, InterventionRequestStreamType]):
        tags (Union[Unset, None, InterventionRequestTags]):
        notification_enabled (Union[Unset, bool]):
    """

    data: Union["LabelingRequestData", "SelectionRequestData", "TeleopRequestData"]
    time: datetime.datetime
    type: Union[Unset, InterventionRequestType] = UNSET
    intervention_type: Union[Unset, InterventionRequestInterventionType] = UNSET
    responses: Union[Unset, List[Any]] = UNSET
    agent_id: Union[Unset, str] = UNSET
    severity: Union[Unset, InterventionRequestSeverity] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    organization_id: Union[Unset, str] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, InterventionRequestStreamType] = UNSET
    tags: Union[Unset, None, "InterventionRequestTags"] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.labeling_request_data import LabelingRequestData
        from ..models.selection_request_data import SelectionRequestData

        data: Dict[str, Any]

        if isinstance(self.data, SelectionRequestData):
            data = self.data.to_dict()

        elif isinstance(self.data, LabelingRequestData):
            data = self.data.to_dict()

        else:
            data = self.data.to_dict()

        time = self.time.isoformat()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        intervention_type: Union[Unset, str] = UNSET
        if not isinstance(self.intervention_type, Unset):
            intervention_type = self.intervention_type.value

        responses: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.responses, Unset):
            responses = self.responses

        agent_id = self.agent_id
        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        organization_id = self.organization_id
        end_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat() if self.end_time else None

        message = self.message
        viewed = self.viewed
        device_id = self.device_id
        stream_name = self.stream_name
        stream_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.stream_type, Unset):
            stream_type = self.stream_type.value if self.stream_type else None

        tags: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict() if self.tags else None

        notification_enabled = self.notification_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
                "time": time,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if intervention_type is not UNSET:
            field_dict["interventionType"] = intervention_type
        if responses is not UNSET:
            field_dict["responses"] = responses
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if severity is not UNSET:
            field_dict["severity"] = severity
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if message is not UNSET:
            field_dict["message"] = message
        if viewed is not UNSET:
            field_dict["viewed"] = viewed
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if stream_name is not UNSET:
            field_dict["streamName"] = stream_name
        if stream_type is not UNSET:
            field_dict["streamType"] = stream_type
        if tags is not UNSET:
            field_dict["tags"] = tags
        if notification_enabled is not UNSET:
            field_dict["notificationEnabled"] = notification_enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.intervention_request_tags import InterventionRequestTags
        from ..models.labeling_request_data import LabelingRequestData
        from ..models.selection_request_data import SelectionRequestData
        from ..models.teleop_request_data import TeleopRequestData

        d = src_dict.copy()

        def _parse_data(data: object) -> Union["LabelingRequestData", "SelectionRequestData", "TeleopRequestData"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = SelectionRequestData.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_1 = LabelingRequestData.from_dict(data)

                return data_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            data_type_2 = TeleopRequestData.from_dict(data)

            return data_type_2

        data = _parse_data(d.pop("data"))

        time = isoparse(d.pop("time"))

        _type = d.pop("type", UNSET)
        type: Union[Unset, InterventionRequestType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = InterventionRequestType(_type)

        _intervention_type = d.pop("interventionType", UNSET)
        intervention_type: Union[Unset, InterventionRequestInterventionType]
        if isinstance(_intervention_type, Unset):
            intervention_type = UNSET
        else:
            intervention_type = InterventionRequestInterventionType(_intervention_type)

        responses = cast(List[Any], d.pop("responses", UNSET))

        agent_id = d.pop("agentId", UNSET)

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, InterventionRequestSeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = InterventionRequestSeverity(_severity)

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

        organization_id = d.pop("organizationId", UNSET)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, None, datetime.datetime]
        if _end_time is None:
            end_time = None
        elif isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, InterventionRequestStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = InterventionRequestStreamType(_stream_type)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, None, InterventionRequestTags]
        if _tags is None:
            tags = None
        elif isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = InterventionRequestTags.from_dict(_tags)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        intervention_request = cls(
            data=data,
            time=time,
            type=type,
            intervention_type=intervention_type,
            responses=responses,
            agent_id=agent_id,
            severity=severity,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            organization_id=organization_id,
            end_time=end_time,
            message=message,
            viewed=viewed,
            device_id=device_id,
            stream_name=stream_name,
            stream_type=stream_type,
            tags=tags,
            notification_enabled=notification_enabled,
        )

        intervention_request.additional_properties = d
        return intervention_request

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
