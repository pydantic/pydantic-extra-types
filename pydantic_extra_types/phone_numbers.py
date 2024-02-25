"""
The `pydantic_extra_types.phone_numbers` module provides the
[`PhoneNumber`][pydantic_extra_types.phone_numbers.PhoneNumber] data type.

This class depends on the [phonenumbers] package, which is a Python port of Google's [libphonenumber].
"""
from __future__ import annotations

from typing import Any, Callable, ClassVar, Generator

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

try:
    import phonenumbers
except ModuleNotFoundError:  # pragma: no cover
    raise RuntimeError(
        '`PhoneNumber` requires "phonenumbers" to be installed. You can install it with "pip install phonenumbers"'
    )

GeneratorCallableStr = Generator[Callable[..., str], None, None]


class PhoneNumber(str):
    """
    A wrapper around [phonenumbers](https://pypi.org/project/phonenumbers/) package, which
    is a Python port of Google's [libphonenumber](https://github.com/google/libphonenumber/).
    """

    supported_regions: list[str] = sorted(phonenumbers.SUPPORTED_REGIONS)
    """The supported regions."""
    supported_formats: list[str] = sorted([f for f in phonenumbers.PhoneNumberFormat.__dict__.keys() if f.isupper()])
    """The supported phone number formats."""

    default_region_code: ClassVar[str | None] = None
    """The default region code to use when parsing phone numbers without an international prefix."""
    phone_format: str = 'RFC3966'
    """The format of the phone number."""
    min_length: int = 7
    """The minimum length of the phone number."""
    max_length: int = 64
    """The maximum length of the phone number."""

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        json_schema = handler(schema)
        json_schema.update({'format': 'phone'})
        return json_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(min_length=cls.min_length, max_length=cls.max_length),
        )

    @classmethod
    def _validate(cls, phone_number: str, _: core_schema.ValidationInfo) -> str:
        try:
            parsed_number = phonenumbers.parse(phone_number, cls.default_region_code)
        except phonenumbers.phonenumberutil.NumberParseException as exc:
            raise PydanticCustomError('value_error', 'value is not a valid phone number') from exc
        if not phonenumbers.is_valid_number(parsed_number):
            raise PydanticCustomError('value_error', 'value is not a valid phone number')

        return phonenumbers.format_number(parsed_number, getattr(phonenumbers.PhoneNumberFormat, cls.phone_format))
