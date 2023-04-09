

from typing import Any
from pydantic import BaseModel, ValidationError
import pytest

from pydantic_extra_types.types.phone_numbers import PhoneNumber, USPhoneNumber


class TestPhoneNumber:
    # Note: the 555 area code will result in an invalid phone number
    def test_valid_phone_number(self) -> None:
        class Something(BaseModel):
            phone_number: PhoneNumber

        Something(phone_number="+1 901 555 1212")

    def test_when_extension_provided(self) -> None:
        class Something(BaseModel):
            phone_number: PhoneNumber

        Something(phone_number="+1 901 555 1212 ext 12533")


    @pytest.mark.parametrize(
        "invalid_number", [
            "",
            "123",
            12,
            None,
            object()
        ]
    )
    def test_invalid_phone_number(self, invalid_number: Any) -> None:
        class Something(BaseModel):
            phone_number: PhoneNumber

        with pytest.raises(ValidationError):
            Something(phone_number="55 1212")


class TestUSPhoneNumber:
    def test_defaults_to_us(self) -> None:
        class Something(BaseModel):
            phone_number: USPhoneNumber

        Something(phone_number="(901) 555-1212")
