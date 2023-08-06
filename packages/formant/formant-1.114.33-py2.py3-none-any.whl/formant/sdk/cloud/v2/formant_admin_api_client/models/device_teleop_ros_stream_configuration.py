from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.device_teleop_ros_stream_configuration_audio_codec import DeviceTeleopRosStreamConfigurationAudioCodec
from ..models.device_teleop_ros_stream_configuration_mode import DeviceTeleopRosStreamConfigurationMode
from ..models.device_teleop_ros_stream_configuration_numeric_control_visualization import (
    DeviceTeleopRosStreamConfigurationNumericControlVisualization,
)
from ..models.device_teleop_ros_stream_configuration_quality import DeviceTeleopRosStreamConfigurationQuality
from ..models.device_teleop_ros_stream_configuration_topic_type import DeviceTeleopRosStreamConfigurationTopicType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DeviceTeleopRosStreamConfiguration")


@attr.s(auto_attribs=True)
class DeviceTeleopRosStreamConfiguration:
    """
    Attributes:
        topic_name (str):
        topic_type (DeviceTeleopRosStreamConfigurationTopicType):
        mode (DeviceTeleopRosStreamConfigurationMode):
        value_topic_name (Union[Unset, str]):
        encode_video (Union[Unset, bool]):
        status_topic (Union[Unset, str]):
        planned_topic (Union[Unset, str]):
        end_effector_topic (Union[Unset, str]):
        end_effector_link_name (Union[Unset, str]):
        plan_valid_topic (Union[Unset, str]):
        base_reference_frame (Union[Unset, str]):
        local_frame (Union[Unset, str]):
        audio_codec (Union[Unset, DeviceTeleopRosStreamConfigurationAudioCodec]):
        min_ (Union[Unset, float]):
        max_ (Union[Unset, float]):
        default_value (Union[Unset, float]):
        step (Union[Unset, float]):
        numeric_control_visualization (Union[Unset, DeviceTeleopRosStreamConfigurationNumericControlVisualization]):
        quality (Union[Unset, DeviceTeleopRosStreamConfigurationQuality]):
        mouse_events_target_stream (Union[Unset, str]):
    """

    topic_name: str
    topic_type: DeviceTeleopRosStreamConfigurationTopicType
    mode: DeviceTeleopRosStreamConfigurationMode
    value_topic_name: Union[Unset, str] = UNSET
    encode_video: Union[Unset, bool] = UNSET
    status_topic: Union[Unset, str] = UNSET
    planned_topic: Union[Unset, str] = UNSET
    end_effector_topic: Union[Unset, str] = UNSET
    end_effector_link_name: Union[Unset, str] = UNSET
    plan_valid_topic: Union[Unset, str] = UNSET
    base_reference_frame: Union[Unset, str] = UNSET
    local_frame: Union[Unset, str] = UNSET
    audio_codec: Union[Unset, DeviceTeleopRosStreamConfigurationAudioCodec] = UNSET
    min_: Union[Unset, float] = UNSET
    max_: Union[Unset, float] = UNSET
    default_value: Union[Unset, float] = UNSET
    step: Union[Unset, float] = UNSET
    numeric_control_visualization: Union[Unset, DeviceTeleopRosStreamConfigurationNumericControlVisualization] = UNSET
    quality: Union[Unset, DeviceTeleopRosStreamConfigurationQuality] = UNSET
    mouse_events_target_stream: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        topic_name = self.topic_name
        topic_type = self.topic_type.value

        mode = self.mode.value

        value_topic_name = self.value_topic_name
        encode_video = self.encode_video
        status_topic = self.status_topic
        planned_topic = self.planned_topic
        end_effector_topic = self.end_effector_topic
        end_effector_link_name = self.end_effector_link_name
        plan_valid_topic = self.plan_valid_topic
        base_reference_frame = self.base_reference_frame
        local_frame = self.local_frame
        audio_codec: Union[Unset, str] = UNSET
        if not isinstance(self.audio_codec, Unset):
            audio_codec = self.audio_codec.value

        min_ = self.min_
        max_ = self.max_
        default_value = self.default_value
        step = self.step
        numeric_control_visualization: Union[Unset, str] = UNSET
        if not isinstance(self.numeric_control_visualization, Unset):
            numeric_control_visualization = self.numeric_control_visualization.value

        quality: Union[Unset, str] = UNSET
        if not isinstance(self.quality, Unset):
            quality = self.quality.value

        mouse_events_target_stream = self.mouse_events_target_stream

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topicName": topic_name,
                "topicType": topic_type,
                "mode": mode,
            }
        )
        if value_topic_name is not UNSET:
            field_dict["valueTopicName"] = value_topic_name
        if encode_video is not UNSET:
            field_dict["encodeVideo"] = encode_video
        if status_topic is not UNSET:
            field_dict["statusTopic"] = status_topic
        if planned_topic is not UNSET:
            field_dict["plannedTopic"] = planned_topic
        if end_effector_topic is not UNSET:
            field_dict["endEffectorTopic"] = end_effector_topic
        if end_effector_link_name is not UNSET:
            field_dict["endEffectorLinkName"] = end_effector_link_name
        if plan_valid_topic is not UNSET:
            field_dict["planValidTopic"] = plan_valid_topic
        if base_reference_frame is not UNSET:
            field_dict["baseReferenceFrame"] = base_reference_frame
        if local_frame is not UNSET:
            field_dict["localFrame"] = local_frame
        if audio_codec is not UNSET:
            field_dict["audioCodec"] = audio_codec
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value
        if step is not UNSET:
            field_dict["step"] = step
        if numeric_control_visualization is not UNSET:
            field_dict["numericControlVisualization"] = numeric_control_visualization
        if quality is not UNSET:
            field_dict["quality"] = quality
        if mouse_events_target_stream is not UNSET:
            field_dict["mouseEventsTargetStream"] = mouse_events_target_stream

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        topic_name = d.pop("topicName")

        topic_type = DeviceTeleopRosStreamConfigurationTopicType(d.pop("topicType"))

        mode = DeviceTeleopRosStreamConfigurationMode(d.pop("mode"))

        value_topic_name = d.pop("valueTopicName", UNSET)

        encode_video = d.pop("encodeVideo", UNSET)

        status_topic = d.pop("statusTopic", UNSET)

        planned_topic = d.pop("plannedTopic", UNSET)

        end_effector_topic = d.pop("endEffectorTopic", UNSET)

        end_effector_link_name = d.pop("endEffectorLinkName", UNSET)

        plan_valid_topic = d.pop("planValidTopic", UNSET)

        base_reference_frame = d.pop("baseReferenceFrame", UNSET)

        local_frame = d.pop("localFrame", UNSET)

        _audio_codec = d.pop("audioCodec", UNSET)
        audio_codec: Union[Unset, DeviceTeleopRosStreamConfigurationAudioCodec]
        if isinstance(_audio_codec, Unset):
            audio_codec = UNSET
        else:
            audio_codec = DeviceTeleopRosStreamConfigurationAudioCodec(_audio_codec)

        min_ = d.pop("min", UNSET)

        max_ = d.pop("max", UNSET)

        default_value = d.pop("defaultValue", UNSET)

        step = d.pop("step", UNSET)

        _numeric_control_visualization = d.pop("numericControlVisualization", UNSET)
        numeric_control_visualization: Union[Unset, DeviceTeleopRosStreamConfigurationNumericControlVisualization]
        if isinstance(_numeric_control_visualization, Unset):
            numeric_control_visualization = UNSET
        else:
            numeric_control_visualization = DeviceTeleopRosStreamConfigurationNumericControlVisualization(
                _numeric_control_visualization
            )

        _quality = d.pop("quality", UNSET)
        quality: Union[Unset, DeviceTeleopRosStreamConfigurationQuality]
        if isinstance(_quality, Unset):
            quality = UNSET
        else:
            quality = DeviceTeleopRosStreamConfigurationQuality(_quality)

        mouse_events_target_stream = d.pop("mouseEventsTargetStream", UNSET)

        device_teleop_ros_stream_configuration = cls(
            topic_name=topic_name,
            topic_type=topic_type,
            mode=mode,
            value_topic_name=value_topic_name,
            encode_video=encode_video,
            status_topic=status_topic,
            planned_topic=planned_topic,
            end_effector_topic=end_effector_topic,
            end_effector_link_name=end_effector_link_name,
            plan_valid_topic=plan_valid_topic,
            base_reference_frame=base_reference_frame,
            local_frame=local_frame,
            audio_codec=audio_codec,
            min_=min_,
            max_=max_,
            default_value=default_value,
            step=step,
            numeric_control_visualization=numeric_control_visualization,
            quality=quality,
            mouse_events_target_stream=mouse_events_target_stream,
        )

        device_teleop_ros_stream_configuration.additional_properties = d
        return device_teleop_ros_stream_configuration

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
