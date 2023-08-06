from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="Bitset")


@attr.s(auto_attribs=True)
class Bitset:
    """
    Attributes:
        keys (List[str]):
        values (List[bool]):
    """

    keys: List[str]
    values: List[bool]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keys = self.keys

        values = self.values

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keys": keys,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        keys = cast(List[str], d.pop("keys"))

        values = cast(List[bool], d.pop("values"))

        bitset = cls(
            keys=keys,
            values=values,
        )

        bitset.additional_properties = d
        return bitset

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
