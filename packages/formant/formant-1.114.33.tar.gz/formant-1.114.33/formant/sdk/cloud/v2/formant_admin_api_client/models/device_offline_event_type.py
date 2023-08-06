from enum import Enum


class DeviceOfflineEventType(str, Enum):
    TRIGGERED_EVENT = "triggered-event"
    DATAPOINT_EVENT = "datapoint-event"
    DEVICE_ONLINE = "device-online"
    DEVICE_OFFLINE = "device-offline"
    INTERVENTION_REQUEST = "intervention-request"
    TELEOP_SESSION_RECORD = "teleop-session-record"
    PORT_FORWARDING_SESSION_RECORD = "port-forwarding-session-record"
    COMMAND_REQUEST = "command-request"
    COMMAND_RESPONSE = "command-response"
    COMMAND_DELIVERY = "command-delivery"
    CUSTOM = "custom"
    COMMENT = "comment"
    SYSTEM = "system"
    ANNOTATION = "annotation"

    def __str__(self) -> str:
        return str(self.value)
