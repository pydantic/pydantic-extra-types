from __future__ import annotations

from typing import Any, Callable, Generator

from pydantic import GetCoreSchemaHandler
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
    An international phone number
    """

    supported_regions: list[str] = sorted(phonenumbers.SUPPORTED_REGIONS)
    supported_formats: list[str] = sorted([f for f in phonenumbers.PhoneNumberFormat.__dict__.keys() if f.isupper()])

    default_region_code: str | None = None
    phone_format: str = 'RFC3966'
    min_length: int = 7
    max_length: int = 64

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[Any], handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.general_after_validator_function(
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
