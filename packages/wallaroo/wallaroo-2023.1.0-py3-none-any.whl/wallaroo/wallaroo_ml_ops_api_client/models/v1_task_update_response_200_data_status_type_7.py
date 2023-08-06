from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="V1TaskUpdateResponse200DataStatusType7")

@attr.s(auto_attribs=True)
class V1TaskUpdateResponse200DataStatusType7:
    """
    Attributes:
        other (str):
    """

    other: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        other = self.other

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "Other": other,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        other = d.pop("Other")

        v1_task_update_response_200_data_status_type_7 = cls(
            other=other,
        )

        v1_task_update_response_200_data_status_type_7.additional_properties = d
        return v1_task_update_response_200_data_status_type_7

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
