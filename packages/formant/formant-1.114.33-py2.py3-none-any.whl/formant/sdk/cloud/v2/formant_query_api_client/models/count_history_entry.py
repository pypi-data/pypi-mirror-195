from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.count_history_entry_count import CountHistoryEntryCount


T = TypeVar("T", bound="CountHistoryEntry")


@attr.s(auto_attribs=True)
class CountHistoryEntry:
    """
    Attributes:
        id (str):
        counts (List['CountHistoryEntryCount']):
    """

    id: str
    counts: List["CountHistoryEntryCount"]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        counts = []
        for counts_item_data in self.counts:
            counts_item = counts_item_data.to_dict()

            counts.append(counts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "counts": counts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.count_history_entry_count import CountHistoryEntryCount

        d = src_dict.copy()
        id = d.pop("id")

        counts = []
        _counts = d.pop("counts")
        for counts_item_data in _counts:
            counts_item = CountHistoryEntryCount.from_dict(counts_item_data)

            counts.append(counts_item)

        count_history_entry = cls(
            id=id,
            counts=counts,
        )

        count_history_entry.additional_properties = d
        return count_history_entry

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
