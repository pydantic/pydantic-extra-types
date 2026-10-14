from typing import Annotated, Any

import phonenumbers
import pytest
from phonenumbers import PhoneNumber
from pydantic import BaseModel, TypeAdapter, ValidationError

from pydantic_extra_types.phone_numbers import PhoneNumberValidator

Number = Annotated[str | PhoneNumber, PhoneNumberValidator()]
NANumber = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(
        supported_regions=['US', 'CA'],
        default_region='US',
    ),
]
UKNumber = Annotated[
    str | PhoneNumber,
    PhoneNumberValidator(
        supported_regions=['GB'],
        default_region='GB',
        number_format='E164',
    ),
]

number_adapter = TypeAdapter(Number)


class Numbers(BaseModel):
    phone_number: Number | None = None
    na_number: NANumber | None = None
    uk_number: UKNumber | None = None


def test_validator_constructor() -> None:
    PhoneNumberValidator()
    PhoneNumberValidator(supported_regions=['US', 'CA'], default_region='US')
    PhoneNumberValidator(supported_regions=['GB'], default_region='GB', number_format='E164')
    with pytest.raises(ValueError, match='Invalid default region code: XX'):
        PhoneNumberValidator(default_region='XX')
    with pytest.raises(ValueError, match='Invalid number format: XX'):
        PhoneNumberValidator(number_format='XX')
    with pytest.raises(ValueError, match='Invalid supported region code: XX'):
        PhoneNumberValidator(supported_regions=['XX'])


# Note: the 555 area code will result in an invalid phone number
def test_valid_phone_number() -> None:
    Numbers(phone_number='+1 901 555 1212')


def test_when_extension_provided() -> None:
    Numbers(phone_number='+1 901 555 1212 ext 12533')


def test_when_phonenumber_instance() -> None:
    phone_number = phonenumbers.parse('+1 901 555 1212', region='US')
    numbers = Numbers(phone_number=phone_number)
    assert numbers.phone_number == 'tel:+1-901-555-1212'
    # Additional validation is still performed on the instance
    with pytest.raises(ValidationError, match='value is not from a supported region'):
        Numbers(uk_number=phone_number)


@pytest.mark.parametrize('invalid_number', ['', '123', 12, object(), '55 121'])
def test_invalid_phone_number(invalid_number: Any) -> None:
    # Use a TypeAdapter to test the validation logic for None otherwise
    # optional fields will not attempt to validate
    with pytest.raises(ValidationError, match='value is not a valid phone number'):
        number_adapter.validate_python(invalid_number)


def test_formats_phone_number() -> None:
    result = Numbers(phone_number='+1 901 555 1212 ext 12533', uk_number='+44 20 7946 0958')
    assert result.phone_number == 'tel:+1-901-555-1212;ext=12533'
    assert result.uk_number == '+442079460958'


def test_default_region() -> None:
    result = Numbers(na_number='901 555 1212')
    assert result.na_number == 'tel:+1-901-555-1212'
    with pytest.raises(ValidationError, match='value is not a valid phone number'):
        Numbers(phone_number='901 555 1212')


def test_supported_regions() -> None:
    assert Numbers(na_number='+1 901 555 1212')
    assert Numbers(uk_number='+44 20 7946 0958')
    with pytest.raises(ValidationError, match='value is not from a supported region'):
        Numbers(na_number='+44 20 7946 0958')


def test_parse_error() -> None:
    with pytest.raises(ValidationError, match='value is not a valid phone number'):
        Numbers(phone_number='555 1212')


def test_parsed_but_not_a_valid_number() -> None:
    with pytest.raises(ValidationError, match='value is not a valid phone number'):
        Numbers(phone_number='+1 555-1212')


@pytest.mark.parametrize(
    'input_number,expected',
    [
        ('+44 20 7946 0958', '020 7946 0958'),
        ('020 7946 0958', '020 7946 0958'),
        ('+1 650 253 0000', '+1 650-253-0000'),
        ('+33 1 23 45 67 89', '+33 1 23 45 67 89'),
        ('+49 30 901820', '+49 30 901820'),
        ('+91 22 2778 8888', '+91 22 2778 8888'),
    ],
)
def test_national_format_keeps_country_code_outside_default_region(input_number: str, expected: str) -> None:
    adapter = TypeAdapter(Annotated[str, PhoneNumberValidator(default_region='GB', number_format='NATIONAL')])
    result = adapter.validate_python(input_number)
    assert result == expected
    assert adapter.validate_python(result) == result


def test_national_format_shared_country_code() -> None:
    # CA shares +1 with US, so the national form still parses back to the same number
    adapter = TypeAdapter(Annotated[str, PhoneNumberValidator(default_region='US', number_format='NATIONAL')])
    assert adapter.validate_python('+1 416 555 0123') == '(416) 555-0123'
    assert adapter.validate_python('(416) 555-0123') == '(416) 555-0123'


def test_national_format_without_default_region() -> None:
    adapter = TypeAdapter(Annotated[str, PhoneNumberValidator(number_format='NATIONAL')])
    result = adapter.validate_python('+44 20 7946 0958')
    assert result == '+44 20 7946 0958'
    assert adapter.validate_python(result) == result
