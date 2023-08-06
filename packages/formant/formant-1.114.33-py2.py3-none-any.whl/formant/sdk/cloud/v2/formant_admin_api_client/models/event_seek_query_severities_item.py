from enum import Enum


class EventSeekQuerySeveritiesItem(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    def __str__(self) -> str:
        return str(self.value)
