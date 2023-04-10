from typing import Any

import pytest

from pydantic import BaseModel, ValidationError
from pydantic_extra_types import PhoneNumber


class TestPhoneNumber:
    class Something(BaseModel):
        phone_number: PhoneNumber

    # Note: the 555 area code will result in an invalid phone number
    def test_valid_phone_number(self) -> None:
        TestPhoneNumber.Something(phone_number='+1 901 555 1212')

    def test_when_extension_provided(self) -> None:
        TestPhoneNumber.Something(phone_number='+1 901 555 1212 ext 12533')

    @pytest.mark.parametrize('invalid_number', ['', '123', 12, None, object()])
    def test_invalid_phone_number(self, invalid_number: Any) -> None:
        with pytest.raises(ValidationError):
            TestPhoneNumber.Something(phone_number='55 1212')

    def test_formats_phone_number(self) -> None:
        result = TestPhoneNumber.Something(phone_number='+1 901 555 1212 ext 12533')
        assert result.phone_number == 'tel:+1-901-555-1212;ext=12533'

    def test_supported_regions(self) -> None:
        assert 'US' in PhoneNumber.supported_regions
        assert 'GB' in PhoneNumber.supported_regions

    def test_supported_formats(self) -> None:
        assert 'E164' in PhoneNumber.supported_formats
        assert 'RFC3966' in PhoneNumber.supported_formats
        assert '__dict__' not in PhoneNumber.supported_formats
        assert 'to_string' not in PhoneNumber.supported_formats


PARAMS_AMOUNT = 10


@pytest.fixture(scope='module', name='PhoneNumbers')
def phone_numbers_fixture():
    class PhoneNumbers(BaseModel):
        phone_number: PhoneNumber

    return PhoneNumbers


@pytest.mark.parametrize(
    'phone_number',
    [
        '+1 901 555 1212',
        '+1 901 555 1212;ext=12533',
    ][:PARAMS_AMOUNT],
)
def test_valid_phone_number(phone_number: str, PhoneNumbers) -> None:
    PhoneNumbers(phone_number=phone_number)


@pytest.mark.parametrize(
    'phone_number',
    [
        '',
        '123',
        12,
        None,
        object(),
    ],
)
def test_invalid_phone_number(phone_number: Any, PhoneNumbers) -> None:
    with pytest.raises(ValidationError):
        PhoneNumbers(phone_number=phone_number)
