from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="SlackAuthRequest")


@attr.s(auto_attribs=True)
class SlackAuthRequest:
    """
    Attributes:
        code (str):
        redirect_uri (str):
    """

    code: str
    redirect_uri: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        redirect_uri = self.redirect_uri

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "redirectUri": redirect_uri,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        redirect_uri = d.pop("redirectUri")

        slack_auth_request = cls(
            code=code,
            redirect_uri=redirect_uri,
        )

        slack_auth_request.additional_properties = d
        return slack_auth_request

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
